// Stock Recovery Analyzer - Frontend JavaScript

class StockAnalyzer {
    constructor() {
        this.isScanning = false;
        this.currentData = [];
        this.init();
    }

    init() {
        // Add fade-in animation to main content
        document.querySelector('.container').classList.add('fade-in');
        
        // Load initial statistics
        this.loadStatistics();
        
        // Set up event listeners
        this.setupEventListeners();
        
        console.log('Stock Analyzer initialized');
    }

    setupEventListeners() {
        // Add event listener for stock details modal
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('btn-details')) {
                const symbol = e.target.getAttribute('data-symbol');
                this.showStockDetails(symbol);
            }
        });

        // Add to watchlist functionality
        document.getElementById('addToWatchlist').addEventListener('click', () => {
            const symbol = document.getElementById('addToWatchlist').getAttribute('data-symbol');
            this.addToWatchlist(symbol);
        });
    }

    async loadStatistics() {
        try {
            // For now, show placeholder data
            // In a real implementation, you'd fetch this from an API endpoint
            document.getElementById('total-stocks').textContent = '50';
            document.getElementById('meeting-criteria').textContent = '-';
            document.getElementById('strong-buys').textContent = '-';
            document.getElementById('last-updated').textContent = 'Never';
            
        } catch (error) {
            console.error('Error loading statistics:', error);
        }
    }

    async startScan() {
        if (this.isScanning) {
            this.showMessage('Scan already in progress', 'warning');
            return;
        }

        this.isScanning = true;
        const scanBtn = document.getElementById('scan-btn');
        const originalText = scanBtn.innerHTML;
        
        // Update button state
        scanBtn.innerHTML = '<span class="loading-spinner me-2"></span>Scanning...';
        scanBtn.disabled = true;
        
        // Show progress container
        const progressContainer = document.getElementById('progress-container');
        const progressBar = document.getElementById('progress-bar');
        const progressText = document.getElementById('progress-text');
        
        progressContainer.style.display = 'block';
        
        try {
            // Simulate progress updates
            this.updateProgress(20, 'Fetching stock list...');
            
            // Make API call to scan stocks
            const response = await fetch('/api/scan');
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            this.updateProgress(60, 'Analyzing stocks...');
            
            const data = await response.json();
            
            this.updateProgress(90, 'Processing results...');
            
            if (data.success) {
                this.currentData = data.stocks;
                this.displayResults(data.stocks);
                this.updateStatistics(data);
                this.showMessage(`Scan completed successfully! Found ${data.stocks.length} stocks meeting criteria.`, 'success');
                
                // Update last updated time
                document.getElementById('last-updated').textContent = new Date(data.timestamp).toLocaleString();
            } else {
                throw new Error(data.error || 'Scan failed');
            }
            
            this.updateProgress(100, 'Complete!');
            
        } catch (error) {
            console.error('Error during scan:', error);
            this.showMessage(`Scan failed: ${error.message}`, 'danger');
        } finally {
            // Reset button state
            setTimeout(() => {
                scanBtn.innerHTML = originalText;
                scanBtn.disabled = false;
                this.isScanning = false;
                progressContainer.style.display = 'none';
            }, 1000);
        }
    }

    updateProgress(percentage, text) {
        const progressBar = document.getElementById('progress-bar');
        const progressText = document.getElementById('progress-text');
        
        progressBar.style.width = percentage + '%';
        progressText.textContent = text;
    }

    displayResults(stocks) {
        const resultsSection = document.getElementById('results-section');
        const tbody = document.getElementById('results-tbody');
        
        // Clear existing results
        tbody.innerHTML = '';
        
        if (stocks.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="8" class="text-center text-muted py-4">
                        <i class="fas fa-search fa-2x mb-2"></i><br>
                        No stocks found meeting the criteria
                    </td>
                </tr>
            `;
        } else {
            stocks.forEach(stock => {
                const row = this.createStockRow(stock);
                tbody.appendChild(row);
            });
        }
        
        // Show results section
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    createStockRow(stock) {
        const row = document.createElement('tr');
        
        const recommendationBadge = this.getRecommendationBadge(stock.recommendation);
        const scoreClass = this.getScoreClass(stock.overall_score);
        const fundamentalScoreClass = this.getScoreClass(stock.fundamental_score);
        const technicalScoreClass = this.getScoreClass(stock.technical_score);
        
        row.innerHTML = `
            <td>
                <div class="stock-symbol">${stock.symbol.replace('.NS', '')}</div>
                <div class="stock-name">${stock.name}</div>
            </td>
            <td class="price">₹${stock.current_price.toFixed(2)}</td>
            <td class="price-decline">${stock.price_decline.toFixed(1)}%</td>
            <td>
                <span class="score ${fundamentalScoreClass}">${stock.fundamental_score}/10</span>
            </td>
            <td>
                <span class="score ${technicalScoreClass}">${stock.technical_score}/10</span>
            </td>
            <td>
                <span class="score ${scoreClass}">${stock.overall_score}/10</span>
            </td>
            <td>${recommendationBadge}</td>
            <td>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary btn-details" data-symbol="${stock.symbol}">
                        <i class="fas fa-chart-line"></i>
                    </button>
                    <button class="btn btn-outline-success" onclick="app.addToWatchlist('${stock.symbol}')">
                        <i class="fas fa-plus"></i>
                    </button>
                </div>
            </td>
        `;
        
        return row;
    }

    getRecommendationBadge(recommendation) {
        const badgeClass = {
            'Strong Buy': 'badge-strong-buy',
            'Buy': 'badge-buy',
            'Moderate Buy': 'badge-moderate-buy',
            'Hold': 'badge-hold',
            'Avoid': 'badge-avoid'
        };
        
        const className = badgeClass[recommendation] || 'badge-hold';
        return `<span class="badge ${className}">${recommendation}</span>`;
    }

    getScoreClass(score) {
        if (score >= 8) return 'score-excellent';
        if (score >= 6.5) return 'score-good';
        if (score >= 5) return 'score-average';
        return 'score-poor';
    }

    async showStockDetails(symbol) {
        try {
            // Show loading in modal
            const modal = new bootstrap.Modal(document.getElementById('stockModal'));
            const modalTitle = document.getElementById('stockModalTitle');
            const modalBody = document.getElementById('stockModalBody');
            
            modalTitle.textContent = `Loading ${symbol}...`;
            modalBody.innerHTML = '<div class="text-center"><div class="loading-spinner"></div> Loading stock details...</div>';
            
            modal.show();
            
            // Fetch stock details
            const response = await fetch(`/api/stock/${symbol}`);
            const data = await response.json();
            
            if (data.success) {
                this.renderStockDetails(data.stock, symbol);
                document.getElementById('addToWatchlist').setAttribute('data-symbol', symbol);
            } else {
                modalBody.innerHTML = `<div class="alert alert-danger">Error loading stock details: ${data.error}</div>`;
            }
            
        } catch (error) {
            console.error('Error loading stock details:', error);
            document.getElementById('stockModalBody').innerHTML = 
                `<div class="alert alert-danger">Error loading stock details: ${error.message}</div>`;
        }
    }

    renderStockDetails(stock, symbol) {
        const modalTitle = document.getElementById('stockModalTitle');
        const modalBody = document.getElementById('stockModalBody');
        
        modalTitle.textContent = `${symbol.replace('.NS', '')} - ${stock.name || symbol}`;
        
        const metrics = stock.detailed_metrics || {};
        
        modalBody.innerHTML = `
            <div class="row">
                <div class="col-md-6">
                    <h6 class="fw-bold mb-3">Performance Metrics</h6>
                    <table class="table table-sm">
                        <tr>
                            <td>Current Price</td>
                            <td class="fw-bold">₹${stock.current_price ? stock.current_price.toFixed(2) : 'N/A'}</td>
                        </tr>
                        <tr>
                            <td>Price Decline</td>
                            <td class="text-danger fw-bold">${stock.price_decline ? stock.price_decline.toFixed(1) : 'N/A'}%</td>
                        </tr>
                        <tr>
                            <td>Volatility</td>
                            <td>${metrics.volatility ? metrics.volatility + '%' : 'N/A'}</td>
                        </tr>
                        <tr>
                            <td>RSI</td>
                            <td>${metrics.rsi ? metrics.rsi.toFixed(1) : 'N/A'}</td>
                        </tr>
                    </table>
                </div>
                <div class="col-md-6">
                    <h6 class="fw-bold mb-3">Fundamental Metrics</h6>
                    <table class="table table-sm">
                        <tr>
                            <td>P/E Ratio</td>
                            <td>${metrics.pe_ratio ? metrics.pe_ratio.toFixed(2) : 'N/A'}</td>
                        </tr>
                        <tr>
                            <td>P/B Ratio</td>
                            <td>${metrics.pb_ratio ? metrics.pb_ratio.toFixed(2) : 'N/A'}</td>
                        </tr>
                        <tr>
                            <td>ROE</td>
                            <td>${metrics.roe ? (metrics.roe * 100).toFixed(1) + '%' : 'N/A'}</td>
                        </tr>
                        <tr>
                            <td>Debt/Equity</td>
                            <td>${metrics.debt_to_equity ? metrics.debt_to_equity.toFixed(2) : 'N/A'}</td>
                        </tr>
                    </table>
                </div>
            </div>
            <hr>
            <div class="row">
                <div class="col-12">
                    <h6 class="fw-bold mb-3">Analysis Scores</h6>
                    <div class="row text-center">
                        <div class="col-4">
                            <div class="metric-card">
                                <div class="metric-value text-info">${stock.fundamental_score || 'N/A'}/10</div>
                                <div class="metric-label">Fundamental Score</div>
                            </div>
                        </div>
                        <div class="col-4">
                            <div class="metric-card">
                                <div class="metric-value text-warning">${stock.technical_score || 'N/A'}/10</div>
                                <div class="metric-label">Technical Score</div>
                            </div>
                        </div>
                        <div class="col-4">
                            <div class="metric-card">
                                <div class="metric-value text-success">${stock.overall_score || 'N/A'}/10</div>
                                <div class="metric-label">Overall Score</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <div class="mt-3">
                <div class="alert alert-info">
                    <strong>Recommendation:</strong> ${this.getRecommendationBadge(stock.recommendation)}
                </div>
            </div>
        `;
    }

    async addToWatchlist(symbol) {
        try {
            this.showMessage(`Added ${symbol.replace('.NS', '')} to watchlist`, 'success');
            // In a real implementation, you'd make an API call here
            // const response = await fetch('/api/watchlist', { method: 'POST', body: JSON.stringify({ symbol }) });
        } catch (error) {
            this.showMessage(`Error adding to watchlist: ${error.message}`, 'danger');
        }
    }

    async updateData() {
        try {
            this.showMessage('Updating stock data...', 'info');
            
            const response = await fetch('/api/update');
            const data = await response.json();
            
            if (data.success) {
                this.showMessage('Stock data updated successfully', 'success');
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            this.showMessage(`Error updating data: ${error.message}`, 'danger');
        }
    }

    updateStatistics(data) {
        const meetingCriteria = data.stocks.length;
        const strongBuys = data.stocks.filter(s => s.recommendation === 'Strong Buy').length;
        
        document.getElementById('meeting-criteria').textContent = meetingCriteria;
        document.getElementById('strong-buys').textContent = strongBuys;
    }

    showMessage(message, type = 'info') {
        const statusContainer = document.getElementById('status-message');
        
        const alertClass = {
            'success': 'alert-success',
            'danger': 'alert-danger',
            'warning': 'alert-warning',
            'info': 'alert-info'
        };
        
        const icon = {
            'success': 'fas fa-check-circle',
            'danger': 'fas fa-exclamation-triangle',
            'warning': 'fas fa-exclamation-circle',
            'info': 'fas fa-info-circle'
        };
        
        statusContainer.innerHTML = `
            <div class="alert ${alertClass[type]} alert-dismissible fade show">
                <i class="${icon[type]} me-2"></i>
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            </div>
        `;
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            const alert = statusContainer.querySelector('.alert');
            if (alert) {
                const bsAlert = new bootstrap.Alert(alert);
                bsAlert.close();
            }
        }, 5000);
    }

    formatCurrency(amount) {
        return new Intl.NumberFormat('en-IN', {
            style: 'currency',
            currency: 'INR',
            minimumFractionDigits: 2
        }).format(amount);
    }

    formatNumber(number, decimals = 2) {
        return number ? number.toFixed(decimals) : 'N/A';
    }
}

// Global functions for HTML onclick handlers
function startScan() {
    app.startScan();
}

function updateData() {
    app.updateData();
}

// Initialize the application
const app = new StockAnalyzer();

// Export for module usage if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = StockAnalyzer;
}