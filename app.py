"""
Angel Broking Live Market Data Stream
Real-time market data streaming with web interface

Author: Keshav D Kaushik
Email: kdkaushik@gmail.com
"""

from SmartApi import SmartConnect
from SmartApi.smartWebSocketV2 import SmartWebSocketV2
import threading
import pyotp, time
from logzero import logger
from datetime import datetime
import mysql.connector
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from config import *

# Initialize SmartAPI
smartApi = SmartConnect(API_KEY)

try:
    totp = pyotp.TOTP(TOTP_TOKEN).now()
    print(f"TOTP: {totp}")
except Exception as e:
    logger.error("Invalid Token: The provided token is not valid.")
    raise e

# Generate session
data = smartApi.generateSession(USERNAME, PASSWORD, totp)

if not data['status']:
    logger.error(data)
    raise Exception("Login failed")

authToken = data['data']['jwtToken']
refreshToken = data['data']['refreshToken']
feedToken = smartApi.getfeedToken()
res = smartApi.getProfile(refreshToken)
smartApi.generateToken(refreshToken)

print(f"Logged in as: {res['data']['name']}")

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = FLASK_SECRET_KEY
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables
last_data = {}
last_save_time = time.time()

def get_tokens_from_db():
    """Fetch option tokens based on NIFTY price and expiries"""
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    # Get current NIFTY price
    cursor.execute("SELECT ltp FROM live_data WHERE token = '26000' ORDER BY microtime DESC LIMIT 1")
    result = cursor.fetchone()
    nifty_ltp = result[0] if result else 24700
    
    strike_min = nifty_ltp - STRIKE_RANGE
    strike_max = nifty_ltp + STRIKE_RANGE
    
    # Get active expiries
    cursor.execute("SELECT expiry_date FROM expiries WHERE is_active = 1 ORDER BY expiry_date ASC LIMIT %s", (EXPIRY_COUNT,))
    expiries = [row[0] for row in cursor.fetchall()]
    
    if len(expiries) >= 2:
        current_expiry = expiries[0]
        last_expiry = expiries[-1]
        
        cursor.execute(
            "SELECT token FROM instruments WHERE strike_price BETWEEN %s AND %s AND expiry_date BETWEEN %s AND %s LIMIT %s",
            (strike_min, strike_max, current_expiry, last_expiry, MAX_TOKENS)
        )
        tokens = [str(row[0]) for row in cursor.fetchall()]
    else:
        tokens = []
    
    conn.close()
    return tokens

def save_to_database():
    """Save sampled data to database"""
    global last_data, last_save_time
    
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        if last_data:
            cursor.executemany(
                "INSERT INTO live_data (token, ltp, volume, oi, microtime) VALUES (%s, %s, %s, %s, %s)",
                list(last_data.values())
            )
            conn.commit()
            print(f"Saved {len(last_data)} sampled records")
            last_data.clear()
        
        conn.close()
        last_save_time = time.time()
    except Exception as e:
        print(f"Database save error: {e}")

def on_data(wsapp, message):
    """Handle incoming market data"""
    global last_data, last_save_time
    
    if isinstance(message, dict):
        token = message.get('token', '')
        ltp = message.get('last_traded_price', 0) / 100
        volume = message.get('volume_trade_for_the_day', 0)
        oi = message.get('open_interest', 0)
        timetext = message.get('exchange_timestamp', None)
        
        # Update latest data (sampling)
        last_data[token] = (token, ltp, volume, oi, timetext)
        
        # Stream to browser
        socketio.emit('live_data', {
            'token': token,
            'ltp': ltp,
            'volume': volume,
            'oi': oi,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        
        # Save every SAVE_INTERVAL seconds
        if time.time() - last_save_time >= SAVE_INTERVAL:
            save_to_database()

def on_open(wsapp):
    """WebSocket connection opened"""
    print("WebSocket connected")
    
    try:
        db_tokens = get_tokens_from_db()
        print(f"Fetched {len(db_tokens)} tokens from database")
        
        token_list = [{"exchangeType": 1, "tokens": ["26000"]}]  # NIFTY 50
        if db_tokens:
            token_list.append({"exchangeType": 2, "tokens": db_tokens})  # Options
        
        sws.subscribe("live_data", 3, token_list)
    except Exception as e:
        print(f"Subscription error: {e}")

def on_error(wsapp, error):
    """WebSocket error handler"""
    print(f"WebSocket error: {error}")

def on_close(wsapp):
    """WebSocket connection closed"""
    print("WebSocket closed")

# Initialize WebSocket
sws = SmartWebSocketV2(authToken, API_KEY, USERNAME, feedToken)
sws.on_open = on_open
sws.on_data = on_data
sws.on_error = on_error
sws.on_close = on_close

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print('Client connected')

if __name__ == '__main__':
    # Start WebSocket in separate thread
    threading.Thread(target=sws.connect, daemon=True).start()
    
    # Start Flask-SocketIO server
    print(f'Starting server on http://{FLASK_HOST}:{FLASK_PORT}')
    print('Press Ctrl+C to stop...')
    
    try:
        socketio.run(app, host=FLASK_HOST, port=FLASK_PORT, debug=False)
    except KeyboardInterrupt:
        print('\nStopping servers...')
        sws.close_connection()