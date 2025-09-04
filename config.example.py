# Angel Broking API Configuration
# Copy this file to config.py and update with your credentials

API_KEY = 'your_api_key_here'
USERNAME = 'your_username_here'
PASSWORD = 'your_password_here'
TOTP_TOKEN = 'your_totp_token_here'

# Database Configuration
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_db_password',
    'database': 'nifty3m'
}

# Application Settings
FLASK_SECRET_KEY = 'your-secret-key-here'
FLASK_HOST = '0.0.0.0'
FLASK_PORT = 5000

# Market Data Settings
STRIKE_RANGE = 700  # Points above/below NIFTY
MAX_TOKENS = 300    # Maximum option contracts
SAVE_INTERVAL = 2   # Database save interval in seconds
EXPIRY_COUNT = 4    # Number of expiry cycles to track