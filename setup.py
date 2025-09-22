#!/usr/bin/env python3
"""
Setup script for Charger Status Monitor
Handles initial configuration and testing
"""

import os
import sys
import subprocess
import json
import sqlite3
from pathlib import Path

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} is not compatible. Please use Python 3.7 or later.")
        return False

def install_dependencies():
    """Install required Python packages"""
    return run_command("pip install -r requirements.txt", "Installing Python dependencies")

def test_scraper():
    """Test the charger scraper"""
    print("🧪 Testing charger scraper...")
    try:
        from charger_scraper import ChargerScraper
        scraper = ChargerScraper()
        status = scraper.scrape_charger_status()
        print(f"✅ Scraper test successful. Status: {status}")
        return True
    except Exception as e:
        print(f"❌ Scraper test failed: {e}")
        return False

def test_database():
    """Test database functionality"""
    print("🗄️ Testing database...")
    try:
        from charger_scraper import ChargerScraper
        scraper = ChargerScraper()
        
        # Test storing and retrieving data
        test_status = "Available"
        success = scraper.store_status(test_status)
        
        if success:
            latest = scraper.get_latest_status()
            if latest and latest['status'] == test_status:
                print("✅ Database test successful")
                return True
        
        print("❌ Database test failed")
        return False
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def create_config_file():
    """Create a configuration file with user settings"""
    print("⚙️ Creating configuration file...")
    
    config = {
        "github_username": input("Enter your GitHub username: ").strip(),
        "update_interval": 5,  # minutes
        "database_path": "charger_data.db",
        "log_level": "INFO"
    }
    
    with open('config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("✅ Configuration file created")
    return config

def update_widget_urls(config):
    """Update widget files with the user's GitHub username"""
    print("🔗 Updating widget URLs...")
    
    username = config['github_username']
    github_url = f"https://raw.githubusercontent.com/{username}/State_of_the_Charge/main/data.json"
    
    # Update Übersicht widget
    widget_file = "ubersicht_widget/charger-status.widget/get_status.py"
    if os.path.exists(widget_file):
        with open(widget_file, 'r') as f:
            content = f.read()
        
        content = content.replace("YOUR_USERNAME", username)
        
        with open(widget_file, 'w') as f:
            f.write(content)
        
        print(f"✅ Updated Übersicht widget with URL: {github_url}")
    
    # Update iOS guide
    guide_file = "ios_shortcuts_guide.md"
    if os.path.exists(guide_file):
        with open(guide_file, 'r') as f:
            content = f.read()
        
        content = content.replace("YOUR_USERNAME", username)
        
        with open(guide_file, 'w') as f:
            f.write(content)
        
        print("✅ Updated iOS shortcuts guide")

def create_gitignore():
    """Create .gitignore file"""
    print("📝 Creating .gitignore...")
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Database
*.db
*.sqlite
*.sqlite3

# Logs
*.log

# Environment
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Local config
config.json
"""
    
    with open('.gitignore', 'w') as f:
        f.write(gitignore_content)
    
    print("✅ .gitignore created")

def main():
    """Main setup function"""
    print("🚀 Charger Status Monitor Setup")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Setup failed at dependency installation")
        return 1
    
    # Test scraper
    if not test_scraper():
        print("⚠️ Scraper test failed, but continuing setup...")
    
    # Test database
    if not test_database():
        print("⚠️ Database test failed, but continuing setup...")
    
    # Create configuration
    try:
        config = create_config_file()
        update_widget_urls(config)
    except KeyboardInterrupt:
        print("\n⚠️ Configuration skipped (user cancelled)")
        config = {"github_username": "YOUR_USERNAME"}
    
    # Create .gitignore
    create_gitignore()
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Push this repository to GitHub")
    print("2. Install Übersicht and copy the widget folder")
    print("3. Follow the iOS shortcuts guide")
    print("4. Run 'python scheduler.py' to start local monitoring")
    
    return 0

if __name__ == "__main__":
    exit(main())
