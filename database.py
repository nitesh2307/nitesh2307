import sqlite3
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path='stock_analyzer.db'):
        self.db_path = db_path
        self.init_db()
    
    def init_db(self):
        """Initialize database connection"""
        try:
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
        except Exception as e:
            logger.error(f"Error initializing database: {str(e)}")
    
    def create_tables(self):
        """Create necessary tables"""
        try:
            cursor = self.conn.cursor()
            
            # Stocks table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS stocks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    sector TEXT,
                    market_cap REAL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Analysis results table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS analysis_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    current_price REAL,
                    price_decline REAL,
                    fundamental_score REAL,
                    technical_score REAL,
                    overall_score REAL,
                    recommendation TEXT,
                    meets_criteria BOOLEAN,
                    analysis_data TEXT,  -- JSON string for detailed analysis
                    FOREIGN KEY (symbol) REFERENCES stocks (symbol)
                )
            ''')
            
            # Price history table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS price_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    date DATE NOT NULL,
                    open_price REAL,
                    high_price REAL,
                    low_price REAL,
                    close_price REAL,
                    volume INTEGER,
                    FOREIGN KEY (symbol) REFERENCES stocks (symbol),
                    UNIQUE(symbol, date)
                )
            ''')
            
            # Watchlist table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS watchlist (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    symbol TEXT NOT NULL,
                    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    notes TEXT,
                    FOREIGN KEY (symbol) REFERENCES stocks (symbol)
                )
            ''')
            
            self.conn.commit()
            logger.info("Database tables created successfully")
            
        except Exception as e:
            logger.error(f"Error creating tables: {str(e)}")
    
    def save_stock(self, symbol, name, sector=None, market_cap=None):
        """Save or update stock information"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO stocks (symbol, name, sector, market_cap, updated_at)
                VALUES (?, ?, ?, ?, ?)
            ''', (symbol, name, sector, market_cap, datetime.now()))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error saving stock {symbol}: {str(e)}")
            return False
    
    def save_analysis_result(self, analysis_result):
        """Save analysis result to database"""
        try:
            cursor = self.conn.cursor()
            
            cursor.execute('''
                INSERT INTO analysis_results (
                    symbol, current_price, price_decline, fundamental_score,
                    technical_score, overall_score, recommendation,
                    meets_criteria, analysis_data
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                analysis_result['symbol'],
                analysis_result['current_price'],
                analysis_result['price_decline'],
                analysis_result['fundamental_score'],
                analysis_result['technical_score'],
                analysis_result['overall_score'],
                analysis_result['recommendation'],
                analysis_result['meets_criteria'],
                json.dumps(analysis_result.get('detailed_data', {}))
            ))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error saving analysis result: {str(e)}")
            return False
    
    def get_latest_analysis_results(self, limit=50):
        """Get latest analysis results"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT ar.*, s.name
                FROM analysis_results ar
                JOIN stocks s ON ar.symbol = s.symbol
                WHERE ar.meets_criteria = 1
                ORDER BY ar.overall_score DESC, ar.analysis_date DESC
                LIMIT ?
            ''', (limit,))
            
            results = []
            for row in cursor.fetchall():
                result = dict(row)
                if result['analysis_data']:
                    result['analysis_data'] = json.loads(result['analysis_data'])
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Error getting analysis results: {str(e)}")
            return []
    
    def get_stock_analysis_history(self, symbol, days=30):
        """Get analysis history for a specific stock"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT *
                FROM analysis_results
                WHERE symbol = ? AND analysis_date >= datetime('now', '-{} days')
                ORDER BY analysis_date DESC
            '''.format(days), (symbol,))
            
            results = []
            for row in cursor.fetchall():
                result = dict(row)
                if result['analysis_data']:
                    result['analysis_data'] = json.loads(result['analysis_data'])
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Error getting stock analysis history: {str(e)}")
            return []
    
    def save_price_history(self, symbol, price_data):
        """Save historical price data"""
        try:
            cursor = self.conn.cursor()
            
            for date, row in price_data.iterrows():
                cursor.execute('''
                    INSERT OR REPLACE INTO price_history 
                    (symbol, date, open_price, high_price, low_price, close_price, volume)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    symbol,
                    date.strftime('%Y-%m-%d'),
                    row['Open'],
                    row['High'],
                    row['Low'],
                    row['Close'],
                    row['Volume']
                ))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error saving price history for {symbol}: {str(e)}")
            return False
    
    def get_price_history(self, symbol, days=365):
        """Get price history for a stock"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT *
                FROM price_history
                WHERE symbol = ? AND date >= date('now', '-{} days')
                ORDER BY date ASC
            '''.format(days), (symbol,))
            
            return [dict(row) for row in cursor.fetchall()]
            
        except Exception as e:
            logger.error(f"Error getting price history: {str(e)}")
            return []
    
    def add_to_watchlist(self, symbol, notes=""):
        """Add stock to watchlist"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                INSERT OR IGNORE INTO watchlist (symbol, notes)
                VALUES (?, ?)
            ''', (symbol, notes))
            
            self.conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error adding to watchlist: {str(e)}")
            return False
    
    def get_watchlist(self):
        """Get watchlist stocks"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
                SELECT w.*, s.name, 
                       ar.overall_score, ar.recommendation, ar.current_price
                FROM watchlist w
                JOIN stocks s ON w.symbol = s.symbol
                LEFT JOIN (
                    SELECT symbol, overall_score, recommendation, current_price,
                           ROW_NUMBER() OVER (PARTITION BY symbol ORDER BY analysis_date DESC) as rn
                    FROM analysis_results
                ) ar ON w.symbol = ar.symbol AND ar.rn = 1
                ORDER BY w.added_at DESC
            ''')
            
            return [dict(row) for row in cursor.fetchall()]
            
        except Exception as e:
            logger.error(f"Error getting watchlist: {str(e)}")
            return []
    
    def remove_from_watchlist(self, symbol):
        """Remove stock from watchlist"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('DELETE FROM watchlist WHERE symbol = ?', (symbol,))
            self.conn.commit()
            return True
            
        except Exception as e:
            logger.error(f"Error removing from watchlist: {str(e)}")
            return False
    
    def get_statistics(self):
        """Get database statistics"""
        try:
            cursor = self.conn.cursor()
            
            stats = {}
            
            # Total stocks
            cursor.execute('SELECT COUNT(*) as count FROM stocks')
            stats['total_stocks'] = cursor.fetchone()['count']
            
            # Total analysis results
            cursor.execute('SELECT COUNT(*) as count FROM analysis_results')
            stats['total_analyses'] = cursor.fetchone()['count']
            
            # Stocks meeting criteria
            cursor.execute('SELECT COUNT(*) as count FROM analysis_results WHERE meets_criteria = 1')
            stats['stocks_meeting_criteria'] = cursor.fetchone()['count']
            
            # Latest analysis date
            cursor.execute('SELECT MAX(analysis_date) as latest FROM analysis_results')
            stats['latest_analysis'] = cursor.fetchone()['latest']
            
            return stats
            
        except Exception as e:
            logger.error(f"Error getting statistics: {str(e)}")
            return {}
    
    def close(self):
        """Close database connection"""
        if hasattr(self, 'conn'):
            self.conn.close()

class Stock:
    """Stock model class"""
    def __init__(self, symbol, name, sector=None, market_cap=None):
        self.symbol = symbol
        self.name = name
        self.sector = sector
        self.market_cap = market_cap
    
    def to_dict(self):
        return {
            'symbol': self.symbol,
            'name': self.name,
            'sector': self.sector,
            'market_cap': self.market_cap
        }