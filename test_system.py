#!/usr/bin/env python3
"""
Test script to verify the entire charger monitoring system
"""

import sys
import os
import json
from datetime import datetime

def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing imports...")
    try:
        from charger_scraper import ChargerScraper
        from api_server import app
        import utilization_analysis
        print("✅ All imports successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_scraper():
    """Test the scraper functionality"""
    print("🔍 Testing scraper...")
    try:
        from charger_scraper import ChargerScraper
        scraper = ChargerScraper()
        
        # Test scraping
        status = scraper.scrape_charger_status()
        print(f"✅ Scraper test successful. Status: {status}")
        
        # Test database storage
        success = scraper.store_status(status)
        if success:
            print("✅ Database storage successful")
        else:
            print("❌ Database storage failed")
            return False
        
        # Test data retrieval
        latest = scraper.get_latest_status()
        if latest:
            print(f"✅ Data retrieval successful: {latest}")
        else:
            print("❌ Data retrieval failed")
            return False
        
        return True
    except Exception as e:
        print(f"❌ Scraper test failed: {e}")
        return False

def test_api():
    """Test API functionality"""
    print("🌐 Testing API...")
    try:
        from api_server import app
        from charger_scraper import ChargerScraper
        
        scraper = ChargerScraper()
        
        # Test with a test client
        with app.test_client() as client:
            # Test health endpoint
            response = client.get('/api/health')
            if response.status_code == 200:
                print("✅ Health endpoint working")
            else:
                print("❌ Health endpoint failed")
                return False
            
            # Test status endpoint
            response = client.get('/api/status')
            if response.status_code == 200:
                data = response.get_json()
                print(f"✅ Status endpoint working: {data}")
            else:
                print("❌ Status endpoint failed")
                return False
        
        return True
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False

def test_analysis():
    """Test utilization analysis"""
    print("📊 Testing analysis...")
    try:
        import utilization_analysis
        
        analyzer = utilization_analysis.UtilizationAnalyzer()
        df = analyzer.load_data(1)  # Last 1 day
        
        if df is not None and not df.empty:
            insights = analyzer.generate_insights(df)
            print(f"✅ Analysis successful. Data points: {insights.get('data_points', 0)}")
        else:
            print("⚠️ No data for analysis (this is normal for a fresh system)")
        
        return True
    except Exception as e:
        print(f"❌ Analysis test failed: {e}")
        return False

def test_data_file():
    """Test data.json file creation"""
    print("📄 Testing data file...")
    try:
        from charger_scraper import ChargerScraper
        
        scraper = ChargerScraper()
        latest = scraper.get_latest_status()
        
        if latest:
            data = {
                'timestamp': latest['timestamp'],
                'status': latest['status'],
                'last_updated': datetime.now().isoformat(),
                'source': 'test'
            }
        else:
            data = {
                'timestamp': None,
                'status': 'Unknown',
                'last_updated': datetime.now().isoformat(),
                'source': 'test',
                'error': 'No data available'
            }
        
        with open('data.json', 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✅ Data file created: {data}")
        return True
    except Exception as e:
        print(f"❌ Data file test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Charger Status Monitor - System Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_scraper,
        test_api,
        test_analysis,
        test_data_file
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
            print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready to use.")
        return 0
    else:
        print("⚠️ Some tests failed. Check the output above.")
        return 1

if __name__ == "__main__":
    exit(main())
