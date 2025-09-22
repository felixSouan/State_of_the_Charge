#!/usr/bin/env python3
"""
Status fetcher for Übersicht widget
Fetches the latest charger status from GitHub or local database
"""

import json
import requests
import sqlite3
import os
import sys
from datetime import datetime

def get_status_from_github():
    """Try to get status from GitHub data file"""
    try:
        # Replace with your actual GitHub username and repo
        github_url = "https://raw.githubusercontent.com/felixSouan/State_of_the_Charge/main/data.json"
        
        response = requests.get(github_url, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        return {
            'status': data.get('status', 'Unknown'),
            'timestamp': data.get('timestamp'),
            'last_updated': data.get('last_updated'),
            'source': 'github'
        }
    except Exception as e:
        return None

def get_status_from_local_db():
    """Get status from local database"""
    try:
        # Look for database in parent directories
        db_paths = [
            'charger_data.db',
            '../charger_data.db',
            '../../charger_data.db'
        ]
        
        for db_path in db_paths:
            if os.path.exists(db_path):
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                cursor.execute('''
                    SELECT timestamp, status FROM utilization
                    ORDER BY timestamp DESC LIMIT 1
                ''')
                
                result = cursor.fetchone()
                conn.close()
                
                if result:
                    return {
                        'status': result[1],
                        'timestamp': result[0],
                        'last_updated': result[0],
                        'source': 'local_db'
                    }
                break
    except Exception as e:
        pass
    
    return None

def main():
    """Main function to get and return status"""
    # Try GitHub first, then local database
    status_data = get_status_from_github()
    
    if not status_data:
        status_data = get_status_from_local_db()
    
    if not status_data:
        # Fallback to unknown status
        status_data = {
            'status': 'Unknown',
            'timestamp': None,
            'last_updated': datetime.now().isoformat(),
            'source': 'fallback'
        }
    
    # Output JSON for the widget
    print(json.dumps(status_data))

if __name__ == "__main__":
    main()
