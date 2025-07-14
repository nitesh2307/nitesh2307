# Indian Stock Recovery Analyzer

A comprehensive web application to scan and analyze Indian stocks that have fallen 30-40% in the last 2 years and show potential for recovery based on fundamental and technical analysis.

## 🎯 Purpose

This application helps investors identify:
- Fundamentally strong Indian stocks that have declined 30-40% in the last 2 years
- Stocks currently hovering in the declined range for recent months
- Potential recovery candidates based on technical indicators
- Investment opportunities with good risk-reward ratios

## ✨ Features

### 📊 Stock Analysis
- **Fundamental Analysis**: Evaluates P/E ratio, P/B ratio, ROE, debt levels, profitability metrics
- **Technical Analysis**: RSI, MACD, moving averages, volume trends, support/resistance levels
- **Combined Scoring**: Weighted scoring system combining fundamental and technical metrics
- **Price Decline Detection**: Identifies stocks in the 30-40% decline range
- **Trend Analysis**: Checks if stocks are hovering in the decline range recently

### 🌐 Web Interface
- Modern, responsive design with Bootstrap 5
- Real-time progress tracking during scans
- Interactive stock details with comprehensive metrics
- Recommendation system (Strong Buy, Buy, Moderate Buy, Hold, Avoid)
- Watchlist functionality for tracking interesting stocks

### 📈 Data Sources
- Yahoo Finance API for historical and current price data
- Real-time fundamental metrics extraction
- NSE stock universe coverage
- Automated data updates

## 🛠 Technology Stack

### Backend
- **Flask** - Python web framework
- **yfinance** - Yahoo Finance API wrapper
- **pandas/numpy** - Data manipulation and analysis
- **SQLite** - Database for storing analysis results
- **requests/BeautifulSoup** - Web scraping capabilities

### Frontend
- **Bootstrap 5** - Responsive UI framework
- **Font Awesome** - Icons
- **Vanilla JavaScript** - Frontend functionality
- **Chart.js** (planned) - Data visualization

### Analysis Libraries
- **TA-Lib** - Technical analysis indicators
- **SciPy** - Statistical analysis
- **Custom algorithms** - Proprietary scoring mechanisms

## 🚀 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Internet connection for data fetching

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd stock-recovery-analyzer
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
```bash
python app.py
```

The application will start on `http://localhost:5000`

## � Usage Guide

### 1. Starting a Stock Scan
1. Open the application in your web browser
2. Click the "Start Scan" button
3. Wait for the analysis to complete (may take several minutes)
4. Review the results in the table below

### 2. Understanding the Results
- **Stock**: Symbol and company name
- **Current Price**: Latest trading price in INR
- **Price Decline**: Percentage decline from 2-year high
- **Fundamental Score**: 0-10 rating based on financial health
- **Technical Score**: 0-10 rating based on chart patterns
- **Overall Score**: Combined weighted score
- **Recommendation**: Buy/Sell/Hold recommendation

### 3. Viewing Stock Details
- Click the chart icon (📈) next to any stock
- View detailed fundamental and technical metrics
- See comprehensive analysis breakdown
- Add stocks to your watchlist

### 4. Score Interpretation
- **8.0-10.0**: Excellent opportunity (Strong Buy)
- **7.0-7.9**: Good opportunity (Buy)
- **6.0-6.9**: Moderate opportunity (Moderate Buy)
- **5.0-5.9**: Hold or watch
- **Below 5.0**: Avoid

## 🧮 Analysis Methodology

### Fundamental Analysis Criteria
1. **P/E Ratio**: 5-25 range preferred
2. **P/B Ratio**: Below 3.0 preferred
3. **Return on Equity**: 10%+ preferred
4. **Debt-to-Equity**: Below 1.0 preferred
5. **Current Ratio**: Above 1.2 for liquidity
6. **Profit Margin**: 5%+ preferred
7. **Revenue Growth**: Positive growth preferred

### Technical Analysis Criteria
1. **RSI**: 30-50 range (oversold to neutral)
2. **MACD**: Positive crossover signals
3. **Moving Averages**: Price above key MAs
4. **Volume**: Above-average volume trends
5. **Support/Resistance**: Price above support levels

### Selection Criteria
- Price decline of 30-40% from 2-year high
- Currently trading in declined range for 2+ months
- Fundamental score of 6.0+ out of 10
- Technical score of 5.5+ out of 10
- Overall combined score of 6.0+

## ⚠️ Important Disclaimers

### Investment Risk Warning
- **Educational Purpose Only**: This tool is for educational and research purposes
- **Not Financial Advice**: Results should not be considered as investment advice
- **Consult Professionals**: Always consult with qualified financial advisors
- **Past Performance**: Historical data doesn't guarantee future results
- **Market Risks**: Stock investments carry inherent risks of loss

### Data Accuracy
- Data is sourced from public APIs and may have delays
- Analysis is based on available historical data
- Real-time prices may differ from displayed values
- Always verify data from official sources before investing

## 🔧 Configuration

### Environment Variables
Create a `.env` file for configuration:
```
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=stock_analyzer.db
```

### Customizing Analysis Parameters
Edit the scoring weights in `analyzer.py`:
```python
self.fundamental_weights = {
    'pe_ratio': 0.15,
    'pb_ratio': 0.10,
    'roe': 0.15,
    # ... customize as needed
}
```

## 📊 Sample Output

```
Top Recovery Candidates:
┌─────────────┬─────────────┬──────────────┬─────────────┬─────────────┐
│ Stock       │ Price       │ Decline      │ Fund Score  │ Tech Score  │
├─────────────┼─────────────┼──────────────┼─────────────┼─────────────┤
│ EXAMPLE.NS  │ ₹1,250.00   │ 35.2%        │ 7.5/10      │ 6.8/10      │
│ SAMPLE.NS   │ ₹890.50     │ 32.1%        │ 8.0/10      │ 7.2/10      │
└─────────────┴─────────────┴──────────────┴─────────────┴─────────────┘
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🐛 Troubleshooting

### Common Issues

1. **"Module not found" errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **Yahoo Finance API issues**
   - Check internet connection
   - Verify stock symbols are correct
   - Try again later if API is temporarily down

3. **Database issues**
   - Delete `stock_analyzer.db` and restart
   - Check file permissions

4. **Slow performance**
   - Reduce number of stocks analyzed
   - Increase timeout values
   - Check system resources

### Getting Help
- Check the Issues section for common problems
- Create a new issue if you encounter bugs
- Contact the maintainers for support

## 🔮 Future Enhancements

- [ ] Real-time price alerts
- [ ] Portfolio tracking
- [ ] Backtesting capabilities
- [ ] Mobile app version
- [ ] Advanced charting
- [ ] Machine learning predictions
- [ ] Multi-timeframe analysis
- [ ] Sector-wise comparison
- [ ] Export functionality
- [ ] Custom screening criteria

---

**Remember**: This tool is for educational purposes only. Always do your own research and consult financial professionals before making investment decisions.
