#!/usr/bin/env python3
"""
Charger Status Scraper for University of Waterloo FLO Charger
Monitors the 50kW FLO charger at ChargeHub LocID: 62901
"""

import requests
from bs4 import BeautifulSoup
import sqlite3
import json
import time
from datetime import datetime, timezone
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('charger_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ChargerScraper:
    def __init__(self, db_path='charger_data.db'):
        self.db_path = db_path
        self.url = "https://chargehub.com/en/ev-charging-stations/canada/ontario/waterloo/university-of-waterloo/electric-car-stations-near-me?locId=62901"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
        }
        self.init_database()
    
    def init_database(self):
        """Initialize SQLite database with utilization table"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS utilization (
                    timestamp TEXT PRIMARY KEY,
                    status TEXT CHECK(status IN ('Available', 'In Use', 'Out of Order', 'Unknown'))
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise
    
    def scrape_charger_status(self):
        """Scrape the current charger status from ChargeHub"""
        try:
            logger.info("Fetching charger status from ChargeHub...")
            response = requests.get(self.url, headers=self.headers, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Look for Level 3 (DC fast charger) availability information
            # This selector may need adjustment based on actual page structure
            status_selectors = [
                'div.availability',
                'div[class*="availability"]',
                'span[class*="available"]',
                'div[class*="status"]',
                '.charger-status',
                '.dc-fast-charger'
            ]
            
            status = 'Unknown'
            
            for selector in status_selectors:
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text().strip().lower()
                    if 'available' in text and '1/1' in text:
                        status = 'Available'
                        break
                    elif 'available' in text and '0/1' in text:
                        status = 'In Use'
                        break
                    elif 'out of order' in text or 'maintenance' in text:
                        status = 'Out of Order'
                        break
                if status != 'Unknown':
                    break
            
            # Fallback: look for any text containing availability info
            if status == 'Unknown':
                page_text = soup.get_text().lower()
                if '1/1 available' in page_text or 'available' in page_text:
                    # Try to determine if it's actually available or in use
                    if '0/1' in page_text:
                        status = 'In Use'
                    else:
                        status = 'Available'
                elif 'out of order' in page_text or 'maintenance' in page_text:
                    status = 'Out of Order'
            
            logger.info(f"Scraped status: {status}")
            return status
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Network error while scraping: {e}")
            return 'Unknown'
        except Exception as e:
            logger.error(f"Error parsing page: {e}")
            return 'Unknown'
    
    def store_status(self, status):
        """Store the charger status in the database"""
        try:
            timestamp = datetime.now(timezone.utc).isoformat()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT OR REPLACE INTO utilization (timestamp, status)
                VALUES (?, ?)
            ''', (timestamp, status))
            
            conn.commit()
            conn.close()
            
            logger.info(f"Stored status: {status} at {timestamp}")
            return True
            
        except Exception as e:
            logger.error(f"Database storage failed: {e}")
            return False
    
    def get_latest_status(self):
        """Get the most recent status from the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT timestamp, status FROM utilization
                ORDER BY timestamp DESC LIMIT 1
            ''')
            
            result = cursor.fetchone()
            conn.close()
            
            if result:
                return {
                    'timestamp': result[0],
                    'status': result[1]
                }
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving latest status: {e}")
            return None
    
    def get_status_history(self, limit=100):
        """Get historical status data"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT timestamp, status FROM utilization
                ORDER BY timestamp DESC LIMIT ?
            ''', (limit,))
            
            results = cursor.fetchall()
            conn.close()
            
            return [
                {'timestamp': row[0], 'status': row[1]}
                for row in results
            ]
            
        except Exception as e:
            logger.error(f"Error retrieving status history: {e}")
            return []
    
    def run_single_check(self):
        """Run a single status check and store result"""
        status = self.scrape_charger_status()
        success = self.store_status(status)
        return success, status

def main():
    """Main function for running the scraper"""
    scraper = ChargerScraper()
    
    logger.info("Starting charger status check...")
    success, status = scraper.run_single_check()
    
    if success:
        logger.info(f"Status check completed successfully: {status}")
        return 0
    else:
        logger.error("Status check failed")
        return 1

if __name__ == "__main__":
    exit(main())
