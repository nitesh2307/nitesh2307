from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import os
from data_collector import StockDataCollector
from analyzer import StockAnalyzer
from database import Database, Stock
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'

# Initialize components
db = Database()
collector = StockDataCollector()
analyzer = StockAnalyzer()

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/scan')
def scan_stocks():
    """API endpoint to scan for stocks meeting criteria"""
    try:
        # Get list of NSE stocks
        stocks = collector.get_nse_stocks()
        logger.info(f"Found {len(stocks)} NSE stocks to analyze")
        
        results = []
        for stock_symbol in stocks[:50]:  # Limit to first 50 for demo
            try:
                # Get stock data
                stock_data = collector.get_stock_data(stock_symbol)
                if not stock_data:
                    continue
                
                # Analyze stock
                analysis = analyzer.analyze_stock(stock_data)
                if analysis and analysis['meets_criteria']:
                    results.append({
                        'symbol': stock_symbol,
                        'name': stock_data.get('name', stock_symbol),
                        'current_price': analysis['current_price'],
                        'price_decline': analysis['price_decline'],
                        'fundamental_score': analysis['fundamental_score'],
                        'technical_score': analysis['technical_score'],
                        'overall_score': analysis['overall_score'],
                        'recommendation': analysis['recommendation']
                    })
                    
            except Exception as e:
                logger.error(f"Error analyzing {stock_symbol}: {str(e)}")
                continue
        
        # Sort by overall score
        results.sort(key=lambda x: x['overall_score'], reverse=True)
        
        return jsonify({
            'success': True,
            'stocks': results[:20],  # Return top 20
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        logger.error(f"Error in scan_stocks: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/stock/<symbol>')
def get_stock_details(symbol):
    """Get detailed analysis for a specific stock"""
    try:
        stock_data = collector.get_stock_data(symbol)
        if not stock_data:
            return jsonify({'success': False, 'error': 'Stock not found'}), 404
        
        analysis = analyzer.get_detailed_analysis(stock_data)
        
        return jsonify({
            'success': True,
            'stock': analysis
        })
        
    except Exception as e:
        logger.error(f"Error getting details for {symbol}: {str(e)}")
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/update')
def update_data():
    """Manually trigger data update"""
    try:
        collector.update_stock_list()
        return jsonify({
            'success': True,
            'message': 'Data update initiated'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

if __name__ == '__main__':
    # Create database tables
    db.create_tables()
    
    # Run the app
    app.run(debug=True, host='0.0.0.0', port=5000)