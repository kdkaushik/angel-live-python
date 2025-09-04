# Angel Broking Live Market Data Stream

Real-time market data streaming application with web interface for Angel Broking SmartAPI.

![Python](https://img.shields.io/badge/python-v3.7+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)

## 🚀 Features

- **Real-time Data Streaming**: Live market data via WebSocket
- **Web Dashboard**: Browser-based real-time data visualization  
- **Smart Sampling**: Database saves every 2 seconds (no memory accumulation)
- **NIFTY Options**: Dynamic strike range based on current NIFTY price
- **Multi-expiry Support**: Tracks 4 expiry cycles simultaneously
- **Zero Memory Leak**: Efficient data sampling without memory buildup

## 📋 Prerequisites

- Python 3.7+
- MySQL 5.7+
- Angel Broking SmartAPI account
- TOTP app (Google Authenticator, etc.)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/angel-live-data.git
   cd angel-live-data
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup database**
   ```bash
   mysql -u root -p < database/schema.sql
   ```

4. **Configure credentials**
   ```bash
   cp config.example.py config.py
   # Edit config.py with your Angel Broking credentials
   ```

## ⚙️ Configuration

Edit `config.py` with your credentials:

```python
# Angel Broking API Configuration
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
```

## 🚀 Usage

1. **Start the application**
   ```bash
   python app.py
   ```

2. **Open web dashboard**
   ```
   http://localhost:5000
   ```

3. **View live data**
   - Real-time market data updates
   - NIFTY 50 and options data
   - Volume and Open Interest tracking

## 📊 Database Schema

```sql
-- Live market data (sampled every 2 seconds)
CREATE TABLE live_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    token VARCHAR(20),
    ltp DECIMAL(10,2),
    volume BIGINT,
    oi BIGINT,
    microtime BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Instruments master
CREATE TABLE instruments (
    token VARCHAR(20) PRIMARY KEY,
    symbol VARCHAR(50),
    strike_price DECIMAL(10,2),
    expiry_date DATE
);

-- Active expiries
CREATE TABLE expiries (
    expiry_date DATE PRIMARY KEY,
    is_active BOOLEAN DEFAULT 1
);
```

## 🔧 API Reference

### WebSocket Events

| Event | Description |
|-------|-------------|
| `live_data` | Real-time market data updates |
| `connect` | Client connection established |

### Data Format

```json
{
  "token": "26000",
  "ltp": 24750.50,
  "volume": 1234567,
  "oi": 987654,
  "timestamp": "2024-01-15 10:30:45"
}
```

## 📈 Performance

- **Database Writes**: Every 2 seconds (sampled data)
- **Browser Updates**: Real-time (all ticks)
- **Memory Usage**: Minimal (no data accumulation)
- **Concurrent Users**: Unlimited (WebSocket broadcasting)

## 🔒 Security

- Credentials stored in separate config file
- Config file excluded from version control
- TOTP-based authentication
- Secure WebSocket connections

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Keshav D Kaushik**
- Email: kdkaushik@gmail.com
- Website: [VoIP Builder](https://voipbuilder.com/)
- Business: [SSL Retail](https://sslretail.com/)
- GitHub: [@yourusername](https://github.com/yourusername)

## 🙏 Acknowledgments

- Angel Broking for SmartAPI
- Flask-SocketIO for real-time communication
- MySQL for reliable data storage

## 📞 Support

If you have any questions or issues, please open an issue on GitHub or contact kdkaushik@gmail.com

---

⭐ **Star this repository if it helped you!**