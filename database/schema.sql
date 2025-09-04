-- Angel Broking Market Data Database Schema
-- Author: Keshav D Kaushik (kdkaushik@gmail.com)

CREATE DATABASE IF NOT EXISTS nifty3m;
USE nifty3m;

-- Live market data table (sampled every 2 seconds)
CREATE TABLE live_data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    token VARCHAR(20) NOT NULL,
    ltp DECIMAL(10,2) NOT NULL,
    volume BIGINT DEFAULT 0,
    oi BIGINT DEFAULT 0,
    microtime BIGINT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_token (token),
    INDEX idx_microtime (microtime),
    INDEX idx_created_at (created_at),
    INDEX idx_token_time (token, created_at)
);

-- Instruments master table
CREATE TABLE instruments (
    token VARCHAR(20) PRIMARY KEY,
    symbol VARCHAR(50) NOT NULL,
    name VARCHAR(100),
    strike_price DECIMAL(10,2),
    expiry_date DATE,
    instrument_type ENUM('EQ', 'CE', 'PE') DEFAULT 'EQ',
    lot_size INT DEFAULT 1,
    INDEX idx_strike_expiry (strike_price, expiry_date),
    INDEX idx_expiry (expiry_date),
    INDEX idx_symbol (symbol)
);

-- Active expiries table
CREATE TABLE expiries (
    expiry_date DATE PRIMARY KEY,
    is_active BOOLEAN DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_active (is_active)
);

-- Sample data for NIFTY 50
INSERT INTO instruments (token, symbol, name, instrument_type) 
VALUES ('26000', 'NIFTY 50', 'NIFTY 50 Index', 'EQ');

-- Sample expiry dates (update these with current expiry dates)
INSERT INTO expiries (expiry_date, is_active) VALUES 
('2024-01-25', 1),
('2024-02-01', 1),
('2024-02-08', 1),
('2024-02-15', 1);

-- Create a view for latest data
CREATE VIEW latest_data AS
SELECT 
    l.token,
    i.symbol,
    l.ltp,
    l.volume,
    l.oi,
    l.created_at
FROM live_data l
JOIN instruments i ON l.token = i.token
WHERE l.created_at >= DATE_SUB(NOW(), INTERVAL 1 HOUR)
ORDER BY l.created_at DESC;