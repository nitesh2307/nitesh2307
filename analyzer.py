import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class StockAnalyzer:
    def __init__(self):
        self.fundamental_weights = {
            'pe_ratio': 0.15,
            'pb_ratio': 0.10,
            'roe': 0.15,
            'debt_to_equity': 0.10,
            'current_ratio': 0.10,
            'profit_margin': 0.15,
            'revenue_growth': 0.15,
            'dividend_yield': 0.10
        }
        
        self.technical_weights = {
            'rsi': 0.25,
            'macd': 0.25,
            'moving_averages': 0.20,
            'volume_trend': 0.15,
            'support_resistance': 0.15
        }
    
    def analyze_stock(self, stock_data):
        """Main analysis function to evaluate if stock meets criteria"""
        try:
            # Check basic price decline criteria (30-40% in last 2 years)
            price_decline = stock_data['price_decline']
            if not (30 <= price_decline <= 40):
                return None
            
            # Check if hovering in range for last few months
            if not self.is_hovering_in_range(stock_data):
                return None
            
            # Fundamental analysis
            fundamental_score = self.analyze_fundamentals(stock_data['fundamental_data'])
            
            # Technical analysis
            technical_score = self.analyze_technical(stock_data)
            
            # Overall score
            overall_score = (fundamental_score * 0.6) + (technical_score * 0.4)
            
            meets_criteria = (
                fundamental_score >= 6.0 and  # Good fundamentals
                technical_score >= 5.5 and    # Positive technical signs
                overall_score >= 6.0
            )
            
            recommendation = self.get_recommendation(overall_score, fundamental_score, technical_score)
            
            return {
                'meets_criteria': meets_criteria,
                'current_price': stock_data['current_price'],
                'price_decline': price_decline,
                'fundamental_score': round(fundamental_score, 2),
                'technical_score': round(technical_score, 2),
                'overall_score': round(overall_score, 2),
                'recommendation': recommendation
            }
            
        except Exception as e:
            logger.error(f"Error analyzing stock: {str(e)}")
            return None
    
    def is_hovering_in_range(self, stock_data):
        """Check if stock is hovering in the declined range for recent months"""
        try:
            recent_data = stock_data['recent_data']
            if len(recent_data) < 30:  # Need at least 30 days of data
                return False
            
            max_price_2y = stock_data['max_price_2y']
            recent_prices = recent_data['Close']
            
            # Calculate decline range for recent prices
            recent_declines = [(max_price_2y - price) / max_price_2y * 100 for price in recent_prices]
            
            # Check if most recent prices are in 25-45% decline range (with some buffer)
            in_range_count = sum(1 for decline in recent_declines if 25 <= decline <= 45)
            
            return (in_range_count / len(recent_declines)) >= 0.7  # 70% of recent prices in range
            
        except Exception as e:
            logger.error(f"Error checking hovering range: {str(e)}")
            return False
    
    def analyze_fundamentals(self, fundamental_data):
        """Analyze fundamental strength of the stock"""
        try:
            score = 0
            max_score = 10
            
            # P/E Ratio Analysis
            pe_ratio = fundamental_data.get('pe_ratio')
            if pe_ratio and 5 <= pe_ratio <= 25:  # Reasonable P/E
                score += 1.5
            elif pe_ratio and pe_ratio <= 15:  # Good P/E
                score += 2
            
            # P/B Ratio Analysis
            pb_ratio = fundamental_data.get('pb_ratio')
            if pb_ratio and pb_ratio <= 3:  # Good P/B
                score += 1
            elif pb_ratio and pb_ratio <= 1.5:  # Excellent P/B
                score += 1.5
            
            # Return on Equity
            roe = fundamental_data.get('roe')
            if roe and roe >= 0.15:  # ROE >= 15%
                score += 2
            elif roe and roe >= 0.10:  # ROE >= 10%
                score += 1.5
            
            # Debt to Equity
            debt_to_equity = fundamental_data.get('debt_to_equity')
            if debt_to_equity is not None:
                if debt_to_equity <= 0.5:  # Low debt
                    score += 1.5
                elif debt_to_equity <= 1.0:  # Moderate debt
                    score += 1
            
            # Current Ratio
            current_ratio = fundamental_data.get('current_ratio')
            if current_ratio and current_ratio >= 1.5:  # Good liquidity
                score += 1
            elif current_ratio and current_ratio >= 1.2:  # Adequate liquidity
                score += 0.5
            
            # Profit Margin
            profit_margin = fundamental_data.get('profit_margin')
            if profit_margin and profit_margin >= 0.10:  # 10%+ profit margin
                score += 1.5
            elif profit_margin and profit_margin >= 0.05:  # 5%+ profit margin
                score += 1
            
            # Revenue Growth
            revenue_growth = fundamental_data.get('revenue_growth')
            if revenue_growth and revenue_growth >= 0.10:  # 10%+ growth
                score += 1.5
            elif revenue_growth and revenue_growth >= 0.05:  # 5%+ growth
                score += 1
            
            # Dividend Yield (bonus points)
            dividend_yield = fundamental_data.get('dividend_yield')
            if dividend_yield and dividend_yield >= 0.02:  # 2%+ dividend
                score += 0.5
            
            return min(score, max_score)  # Cap at max_score
            
        except Exception as e:
            logger.error(f"Error in fundamental analysis: {str(e)}")
            return 0
    
    def analyze_technical(self, stock_data):
        """Analyze technical indicators for potential upward movement"""
        try:
            hist_data = stock_data['historical_data']
            recent_data = stock_data['recent_data']
            
            score = 0
            max_score = 10
            
            # RSI Analysis
            rsi = self.calculate_rsi(hist_data['Close'])
            if rsi and 30 <= rsi <= 50:  # Oversold to neutral (good for entry)
                score += 2.5
            elif rsi and 50 <= rsi <= 70:  # Neutral to overbought
                score += 1.5
            
            # MACD Analysis
            macd_score = self.analyze_macd(hist_data['Close'])
            score += macd_score
            
            # Moving Average Analysis
            ma_score = self.analyze_moving_averages(hist_data['Close'])
            score += ma_score
            
            # Volume Trend Analysis
            volume_score = self.analyze_volume_trend(hist_data)
            score += volume_score
            
            # Support/Resistance Analysis
            sr_score = self.analyze_support_resistance(hist_data['Close'])
            score += sr_score
            
            return min(score, max_score)
            
        except Exception as e:
            logger.error(f"Error in technical analysis: {str(e)}")
            return 0
    
    def calculate_rsi(self, prices, period=14):
        """Calculate Relative Strength Index"""
        try:
            delta = prices.diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            
            avg_gain = gain.rolling(window=period).mean()
            avg_loss = loss.rolling(window=period).mean()
            
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            
            return rsi.iloc[-1] if not rsi.empty else None
            
        except Exception as e:
            logger.error(f"Error calculating RSI: {str(e)}")
            return None
    
    def analyze_macd(self, prices):
        """Analyze MACD for trend direction"""
        try:
            exp1 = prices.ewm(span=12).mean()
            exp2 = prices.ewm(span=26).mean()
            macd = exp1 - exp2
            signal = macd.ewm(span=9).mean()
            histogram = macd - signal
            
            # Check recent MACD signals
            recent_macd = macd.tail(5)
            recent_signal = signal.tail(5)
            recent_histogram = histogram.tail(5)
            
            score = 0
            
            # MACD above signal line (bullish)
            if recent_macd.iloc[-1] > recent_signal.iloc[-1]:
                score += 1
            
            # MACD trending up
            if recent_macd.iloc[-1] > recent_macd.iloc[-3]:
                score += 1
            
            # Histogram increasing (momentum building)
            if recent_histogram.iloc[-1] > recent_histogram.iloc[-2]:
                score += 0.5
            
            return min(score, 2.5)
            
        except Exception as e:
            logger.error(f"Error analyzing MACD: {str(e)}")
            return 0
    
    def analyze_moving_averages(self, prices):
        """Analyze moving average trends"""
        try:
            ma20 = prices.rolling(window=20).mean()
            ma50 = prices.rolling(window=50).mean()
            ma200 = prices.rolling(window=200).mean()
            
            current_price = prices.iloc[-1]
            
            score = 0
            
            # Price above MA20
            if current_price > ma20.iloc[-1]:
                score += 0.5
            
            # MA20 above MA50 (short term uptrend)
            if ma20.iloc[-1] > ma50.iloc[-1]:
                score += 1
            
            # Price near MA200 (potential bounce level)
            if abs(current_price - ma200.iloc[-1]) / ma200.iloc[-1] <= 0.05:
                score += 0.5
            
            return min(score, 2)
            
        except Exception as e:
            logger.error(f"Error analyzing moving averages: {str(e)}")
            return 0
    
    def analyze_volume_trend(self, hist_data):
        """Analyze volume trends"""
        try:
            recent_volume = hist_data['Volume'].tail(20)
            avg_volume = hist_data['Volume'].mean()
            
            score = 0
            
            # Recent volume above average (interest building)
            if recent_volume.mean() > avg_volume:
                score += 1
            
            # Volume increasing trend
            if recent_volume.iloc[-5:].mean() > recent_volume.iloc[-10:-5].mean():
                score += 0.5
            
            return min(score, 1.5)
            
        except Exception as e:
            logger.error(f"Error analyzing volume trend: {str(e)}")
            return 0
    
    def analyze_support_resistance(self, prices):
        """Analyze support and resistance levels"""
        try:
            recent_prices = prices.tail(60)  # Last 60 days
            
            # Find potential support level (recent lows)
            support_level = recent_prices.min()
            current_price = prices.iloc[-1]
            
            score = 0
            
            # Price above recent support
            if current_price > support_level * 1.02:  # 2% above support
                score += 1
            
            # Price bounced from support recently
            if any(price <= support_level * 1.01 for price in recent_prices.tail(10)):
                score += 0.5
            
            return min(score, 1.5)
            
        except Exception as e:
            logger.error(f"Error analyzing support/resistance: {str(e)}")
            return 0
    
    def get_recommendation(self, overall_score, fundamental_score, technical_score):
        """Generate recommendation based on scores"""
        if overall_score >= 8:
            return "Strong Buy"
        elif overall_score >= 7:
            return "Buy"
        elif overall_score >= 6:
            return "Moderate Buy"
        elif overall_score >= 5:
            return "Hold"
        else:
            return "Avoid"
    
    def get_detailed_analysis(self, stock_data):
        """Get detailed analysis for a specific stock"""
        try:
            analysis = self.analyze_stock(stock_data)
            if not analysis:
                return None
            
            # Add more detailed metrics
            fundamental_data = stock_data['fundamental_data']
            hist_data = stock_data['historical_data']
            
            # Calculate additional metrics
            volatility = hist_data['Close'].pct_change().std() * np.sqrt(252) * 100  # Annualized volatility
            rsi = self.calculate_rsi(hist_data['Close'])
            
            detailed = {
                **analysis,
                'detailed_metrics': {
                    'volatility': round(volatility, 2) if volatility else None,
                    'rsi': round(rsi, 2) if rsi else None,
                    'pe_ratio': fundamental_data.get('pe_ratio'),
                    'pb_ratio': fundamental_data.get('pb_ratio'),
                    'roe': fundamental_data.get('roe'),
                    'debt_to_equity': fundamental_data.get('debt_to_equity'),
                    'market_cap': fundamental_data.get('market_cap'),
                    'dividend_yield': fundamental_data.get('dividend_yield')
                }
            }
            
            return detailed
            
        except Exception as e:
            logger.error(f"Error in detailed analysis: {str(e)}")
            return None