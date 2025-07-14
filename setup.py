#!/usr/bin/env python3
"""
Setup script for Indian Stock Recovery Analyzer
"""

import subprocess
import sys
import os
from pathlib import Path

def print_header():
    print("=" * 60)
    print("    Indian Stock Recovery Analyzer - Setup")
    print("=" * 60)
    print()

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    print("🐍 Checking Python version...")
    if sys.version_info < (3, 8):
        print("❌ Error: Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        sys.exit(1)
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} is supported")
    print()

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        print("   Please run: pip install -r requirements.txt")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ requirements.txt not found")
        print("   Please ensure you're in the correct directory")
        sys.exit(1)
    print()

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    directories = ['static/css', 'static/js', 'templates', 'data', 'logs']
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directories created successfully")
    print()

def create_env_file():
    """Create .env file if it doesn't exist"""
    print("⚙️  Setting up configuration...")
    
    env_file = Path('.env')
    if not env_file.exists():
        env_content = """# Flask Configuration
FLASK_ENV=development
SECRET_KEY=your-secret-key-change-this-in-production
DATABASE_URL=stock_analyzer.db

# Data Collection Settings
MAX_STOCKS_PER_SCAN=50
SCAN_TIMEOUT_SECONDS=300
UPDATE_FREQUENCY_HOURS=24

# Analysis Parameters
MIN_FUNDAMENTAL_SCORE=6.0
MIN_TECHNICAL_SCORE=5.5
MIN_OVERALL_SCORE=6.0
MIN_PRICE_DECLINE=30.0
MAX_PRICE_DECLINE=40.0

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print("✅ Created .env configuration file")
    else:
        print("✅ Configuration file already exists")
    print()

def verify_installation():
    """Verify that the installation was successful"""
    print("🔍 Verifying installation...")
    
    try:
        # Test importing main modules
        import flask
        import yfinance
        import pandas
        import numpy
        print("✅ Core dependencies verified")
        
        # Check if main files exist
        required_files = ['app.py', 'data_collector.py', 'analyzer.py', 'database.py']
        for file in required_files:
            if not Path(file).exists():
                print(f"❌ Missing required file: {file}")
                return False
        
        print("✅ All required files present")
        
        # Test database creation
        from database import Database
        db = Database()
        db.create_tables()
        print("✅ Database initialization successful")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Verification error: {e}")
        return False

def print_usage_instructions():
    """Print usage instructions"""
    print("\n" + "=" * 60)
    print("    Setup Complete! 🎉")
    print("=" * 60)
    print()
    print("To start the application:")
    print("  python app.py")
    print()
    print("Then open your browser and go to:")
    print("  http://localhost:5000")
    print()
    print("Important Notes:")
    print("  • This application is for educational purposes only")
    print("  • Always consult financial professionals before investing")
    print("  • Internet connection required for data fetching")
    print("  • First scan may take several minutes")
    print()
    print("For help and documentation:")
    print("  • Read the README.md file")
    print("  • Check the troubleshooting section")
    print("  • Report issues on the project repository")
    print()
    print("Happy investing! 📈")
    print()

def main():
    """Main setup function"""
    print_header()
    
    try:
        check_python_version()
        create_directories()
        install_dependencies()
        create_env_file()
        
        if verify_installation():
            print_usage_instructions()
        else:
            print("\n❌ Setup completed with errors. Please check the output above.")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n❌ Setup interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()