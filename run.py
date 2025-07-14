#!/usr/bin/env python3
"""
Run script for Indian Stock Recovery Analyzer
"""

import os
import sys
import logging
from pathlib import Path

def setup_logging():
    """Setup logging configuration"""
    log_dir = Path('logs')
    log_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_dir / 'app.log'),
            logging.StreamHandler(sys.stdout)
        ]
    )

def check_dependencies():
    """Check if all required dependencies are installed"""
    required_packages = [
        'flask', 'yfinance', 'pandas', 'numpy', 
        'requests', 'beautifulsoup4', 'sqlalchemy'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nPlease run: python setup.py")
        return False
    
    return True

def check_files():
    """Check if all required files exist"""
    required_files = [
        'app.py', 'data_collector.py', 'analyzer.py', 
        'database.py', 'templates/index.html'
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ Missing required files:")
        for file_path in missing_files:
            print(f"   - {file_path}")
        return False
    
    return True

def print_startup_banner():
    """Print startup banner"""
    print("=" * 60)
    print("    Indian Stock Recovery Analyzer")
    print("    🚀 Starting Application...")
    print("=" * 60)
    print()
    print("📊 Features:")
    print("  • Fundamental Analysis")
    print("  • Technical Analysis") 
    print("  • Recovery Stock Detection")
    print("  • Investment Recommendations")
    print()
    print("⚠️  Disclaimer: For educational purposes only")
    print("   Always consult financial professionals before investing")
    print()

def main():
    """Main function to start the application"""
    print_startup_banner()
    
    # Setup logging
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Check dependencies
        print("🔍 Checking dependencies...")
        if not check_dependencies():
            sys.exit(1)
        print("✅ All dependencies found")
        
        # Check required files
        print("📁 Checking required files...")
        if not check_files():
            sys.exit(1)
        print("✅ All required files found")
        
        # Set environment variables
        os.environ.setdefault('FLASK_ENV', 'development')
        
        # Import and run the app
        print("🌐 Starting Flask application...")
        print("   URL: http://localhost:5000")
        print("   Press Ctrl+C to stop")
        print()
        
        # Import here to avoid circular imports
        from app import app
        
        # Run the application
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
            use_reloader=False  # Disable reloader to avoid issues
        )
        
    except ImportError as e:
        logger.error(f"Import error: {e}")
        print("❌ Error importing application modules")
        print("   Please run: python setup.py")
        sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n\n👋 Application stopped by user")
        logger.info("Application stopped by user")
        
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()