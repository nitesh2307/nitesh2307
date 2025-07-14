import yfinance as yf
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class StockDataCollector:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # NSE stock symbols - you can expand this list
        self.nse_stocks = [
            'RELIANCE.NS', 'TCS.NS', 'HDFCBANK.NS', 'INFY.NS', 'HDFC.NS',
            'ICICIBANK.NS', 'KOTAKBANK.NS', 'HINDUNILVR.NS', 'SBIN.NS', 'BHARTIARTL.NS',
            'ITC.NS', 'ASIANPAINT.NS', 'LT.NS', 'AXISBANK.NS', 'MARUTI.NS',
            'SUNPHARMA.NS', 'ULTRACEMCO.NS', 'BAJFINANCE.NS', 'HCLTECH.NS', 'WIPRO.NS',
            'NESTLEIND.NS', 'POWERGRID.NS', 'TITAN.NS', 'NTPC.NS', 'TECHM.NS',
            'ONGC.NS', 'BAJAJFINSV.NS', 'M&M.NS', 'TATASTEEL.NS', 'ADANIGREEN.NS',
            'JSWSTEEL.NS', 'INDUSINDBK.NS', 'GRASIM.NS', 'BRITANNIA.NS', 'CIPLA.NS',
            'DRREDDY.NS', 'EICHERMOT.NS', 'BPCL.NS', 'COALINDIA.NS', 'HINDALCO.NS',
            'TATACONSUM.NS', 'UPL.NS', 'BAJAJ-AUTO.NS', 'HEROMOTOCO.NS', 'DIVISLAB.NS',
            'SHREECEM.NS', 'VEDL.NS', 'TATAMOTORS.NS', 'APOLLOHOSP.NS', 'SBILIFE.NS'
        ]
    
    def get_nse_stocks(self):
        """Get list of NSE stock symbols"""
        return self.nse_stocks
    
    def get_stock_data(self, symbol):
        """Get comprehensive stock data for analysis"""
        try:
            # Add .NS suffix if not present for Yahoo Finance
            if not symbol.endswith('.NS'):
                symbol = symbol + '.NS'
            
            ticker = yf.Ticker(symbol)
            
            # Get historical data (2 years)
            end_date = datetime.now()
            start_date = end_date - timedelta(days=730)  # ~2 years
            
            hist_data = ticker.history(start=start_date, end=end_date)
            if hist_data.empty:
                logger.warning(f"No historical data found for {symbol}")
                return None
            
            # Get stock info
            info = ticker.info
            
            # Get recent data (last 3 months for current trend analysis)
            recent_start = end_date - timedelta(days=90)
            recent_data = ticker.history(start=recent_start, end=end_date)
            
            # Calculate key metrics
            current_price = hist_data['Close'].iloc[-1]
            max_price_2y = hist_data['Close'].max()
            price_decline = ((max_price_2y - current_price) / max_price_2y) * 100
            
            # Get fundamental data
            fundamental_data = self.get_fundamental_metrics(info)
            
            return {
                'symbol': symbol,
                'name': info.get('longName', symbol),
                'current_price': current_price,
                'historical_data': hist_data,
                'recent_data': recent_data,
                'price_decline': price_decline,
                'max_price_2y': max_price_2y,
                'fundamental_data': fundamental_data,
                'info': info
            }
            
        except Exception as e:
            logger.error(f"Error collecting data for {symbol}: {str(e)}")
            return None
    
    def get_fundamental_metrics(self, info):
        """Extract fundamental metrics from stock info"""
        try:
            return {
                'pe_ratio': info.get('trailingPE'),
                'pb_ratio': info.get('priceToBook'),
                'debt_to_equity': info.get('debtToEquity'),
                'roe': info.get('returnOnEquity'),
                'roa': info.get('returnOnAssets'),
                'current_ratio': info.get('currentRatio'),
                'quick_ratio': info.get('quickRatio'),
                'gross_margin': info.get('grossMargins'),
                'operating_margin': info.get('operatingMargins'),
                'profit_margin': info.get('profitMargins'),
                'revenue_growth': info.get('revenueGrowth'),
                'earnings_growth': info.get('earningsGrowth'),
                'book_value': info.get('bookValue'),
                'market_cap': info.get('marketCap'),
                'enterprise_value': info.get('enterpriseValue'),
                'dividend_yield': info.get('dividendYield'),
                'payout_ratio': info.get('payoutRatio')
            }
        except Exception as e:
            logger.error(f"Error extracting fundamental metrics: {str(e)}")
            return {}
    
    def get_sector_pe(self, sector):
        """Get average P/E ratio for a sector (simplified implementation)"""
        # This would ideally fetch real sector data
        sector_pe_map = {
            'Technology': 25,
            'Financial Services': 15,
            'Consumer Goods': 30,
            'Healthcare': 35,
            'Energy': 12,
            'Utilities': 18,
            'Industrial': 20,
            'Materials': 16
        }
        return sector_pe_map.get(sector, 20)  # Default to 20 if sector not found
    
    def update_stock_list(self):
        """Update the list of stocks to analyze"""
        try:
            # In a real implementation, you might fetch this from NSE website
            # For now, we'll use the predefined list
            logger.info("Stock list updated successfully")
            return True
        except Exception as e:
            logger.error(f"Error updating stock list: {str(e)}")
            return False
    
    def get_financial_statements(self, symbol):
        """Get financial statements data (simplified)"""
        try:
            ticker = yf.Ticker(symbol)
            
            # Get financial data
            financials = ticker.financials
            balance_sheet = ticker.balance_sheet
            cashflow = ticker.cashflow
            
            return {
                'financials': financials,
                'balance_sheet': balance_sheet,
                'cashflow': cashflow
            }
        except Exception as e:
            logger.error(f"Error getting financial statements for {symbol}: {str(e)}")
            return None