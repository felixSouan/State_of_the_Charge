#!/usr/bin/env python3
"""
Background scheduler for automated charger status polling
Runs the scraper every 5 minutes
"""

import schedule
import time
import logging
from charger_scraper import ChargerScraper
import signal
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ChargerScheduler:
    def __init__(self):
        self.scraper = ChargerScraper()
        self.running = True
        
        # Set up signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
    
    def signal_handler(self, signum, frame):
        """Handle shutdown signals gracefully"""
        logger.info(f"Received signal {signum}, shutting down...")
        self.running = False
    
    def run_status_check(self):
        """Run a single status check"""
        try:
            logger.info("Running scheduled status check...")
            success, status = self.scraper.run_single_check()
            
            if success:
                logger.info(f"Scheduled check completed: {status}")
            else:
                logger.error("Scheduled check failed")
                
        except Exception as e:
            logger.error(f"Error in scheduled check: {e}")
    
    def start_scheduler(self):
        """Start the background scheduler"""
        logger.info("Starting charger status scheduler...")
        
        # Schedule the status check every 5 minutes
        schedule.every(5).minutes.do(self.run_status_check)
        
        # Run an initial check
        self.run_status_check()
        
        # Main scheduler loop
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(30)  # Check every 30 seconds for pending jobs
            except KeyboardInterrupt:
                logger.info("Received keyboard interrupt, shutting down...")
                break
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                time.sleep(60)  # Wait a minute before retrying
        
        logger.info("Scheduler stopped")

def main():
    """Main function"""
    scheduler = ChargerScheduler()
    scheduler.start_scheduler()

if __name__ == "__main__":
    main()
