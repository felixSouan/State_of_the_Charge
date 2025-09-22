#!/usr/bin/env python3
"""
Utilization analysis script for charger status data
Analyzes patterns and provides insights on optimal charging times
"""

import pandas as pd
import sqlite3
from datetime import datetime, timedelta
import argparse
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UtilizationAnalyzer:
    def __init__(self, db_path='charger_data.db'):
        self.db_path = db_path
    
    def load_data(self, days_back=7):
        """Load utilization data from the database"""
        try:
            conn = sqlite3.connect(self.db_path)
            
            # Get data from the last N days
            cutoff_date = datetime.now() - timedelta(days=days_back)
            cutoff_str = cutoff_date.isoformat()
            
            query = '''
                SELECT timestamp, status FROM utilization
                WHERE timestamp >= ?
                ORDER BY timestamp
            '''
            
            df = pd.read_sql_query(query, conn, params=[cutoff_str])
            conn.close()
            
            if df.empty:
                logger.warning("No data found in the specified time range")
                return None
            
            # Convert timestamp to datetime
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.day_name()
            df['date'] = df['timestamp'].dt.date
            
            # Convert status to numeric for analysis
            status_mapping = {
                'Available': 0,      # 0% utilization
                'In Use': 1,         # 100% utilization
                'Out of Order': 0.5, # 50% utilization (assume half the time)
                'Unknown': None      # Exclude from analysis
            }
            df['utilization'] = df['status'].map(status_mapping)
            
            # Remove unknown statuses
            df = df.dropna(subset=['utilization'])
            
            logger.info(f"Loaded {len(df)} data points from the last {days_back} days")
            return df
            
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            return None
    
    def analyze_hourly_patterns(self, df):
        """Analyze utilization patterns by hour of day"""
        if df is None or df.empty:
            return None
        
        hourly_stats = df.groupby('hour')['utilization'].agg([
            'mean', 'count', 'std'
        ]).round(3)
        
        # Calculate availability percentage
        hourly_stats['availability_pct'] = (1 - hourly_stats['mean']) * 100
        
        # Sort by availability (highest first)
        hourly_stats = hourly_stats.sort_values('availability_pct', ascending=False)
        
        return hourly_stats
    
    def analyze_daily_patterns(self, df):
        """Analyze utilization patterns by day of week"""
        if df is None or df.empty:
            return None
        
        daily_stats = df.groupby('day_of_week')['utilization'].agg([
            'mean', 'count', 'std'
        ]).round(3)
        
        # Calculate availability percentage
        daily_stats['availability_pct'] = (1 - daily_stats['mean']) * 100
        
        # Reorder days of week
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_stats = daily_stats.reindex(day_order)
        
        return daily_stats
    
    def find_optimal_times(self, df, min_availability=80):
        """Find times with high availability"""
        if df is None or df.empty:
            return None
        
        hourly_stats = self.analyze_hourly_patterns(df)
        if hourly_stats is None:
            return None
        
        # Find hours with high availability
        optimal_hours = hourly_stats[hourly_stats['availability_pct'] >= min_availability]
        
        return optimal_hours
    
    def generate_insights(self, df):
        """Generate comprehensive insights"""
        if df is None or df.empty:
            return {
                'error': 'No data available for analysis',
                'data_points': 0
            }
        
        insights = {
            'data_points': len(df),
            'date_range': {
                'start': df['timestamp'].min().isoformat(),
                'end': df['timestamp'].max().isoformat()
            },
            'overall_utilization': {
                'average': round(df['utilization'].mean() * 100, 1),
                'availability': round((1 - df['utilization'].mean()) * 100, 1)
            }
        }
        
        # Hourly patterns
        hourly_stats = self.analyze_hourly_patterns(df)
        if hourly_stats is not None:
            insights['hourly_patterns'] = {
                'best_hours': hourly_stats.head(3).index.tolist(),
                'worst_hours': hourly_stats.tail(3).index.tolist(),
                'details': hourly_stats.to_dict('index')
            }
        
        # Daily patterns
        daily_stats = self.analyze_daily_patterns(df)
        if daily_stats is not None:
            insights['daily_patterns'] = {
                'best_days': daily_stats.nlargest(3, 'availability_pct').index.tolist(),
                'worst_days': daily_stats.nsmallest(3, 'availability_pct').index.tolist(),
                'details': daily_stats.to_dict('index')
            }
        
        # Optimal times
        optimal_times = self.find_optimal_times(df)
        if optimal_times is not None and not optimal_times.empty:
            insights['optimal_times'] = {
                'hours': optimal_times.index.tolist(),
                'average_availability': round(optimal_times['availability_pct'].mean(), 1)
            }
        
        return insights
    
    def print_report(self, insights):
        """Print a formatted analysis report"""
        print("\n" + "="*60)
        print("CHARGER UTILIZATION ANALYSIS REPORT")
        print("="*60)
        
        if 'error' in insights:
            print(f"Error: {insights['error']}")
            return
        
        print(f"Data Points: {insights['data_points']}")
        print(f"Date Range: {insights['date_range']['start']} to {insights['date_range']['end']}")
        print(f"Overall Availability: {insights['overall_utilization']['availability']}%")
        print(f"Overall Utilization: {insights['overall_utilization']['average']}%")
        
        if 'optimal_times' in insights:
            print(f"\nOptimal Charging Times (80%+ availability):")
            for hour in insights['optimal_times']['hours']:
                print(f"  - {hour}:00 - {hour+1}:00")
            print(f"  Average availability: {insights['optimal_times']['average_availability']}%")
        
        if 'hourly_patterns' in insights:
            print(f"\nBest Hours for Charging:")
            for hour in insights['hourly_patterns']['best_hours']:
                availability = insights['hourly_patterns']['details'][hour]['availability_pct']
                print(f"  - {hour}:00 ({availability:.1f}% available)")
        
        if 'daily_patterns' in insights:
            print(f"\nBest Days for Charging:")
            for day in insights['daily_patterns']['best_days']:
                availability = insights['daily_patterns']['details'][day]['availability_pct']
                print(f"  - {day} ({availability:.1f}% available)")
        
        print("\n" + "="*60)

def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description='Analyze charger utilization patterns')
    parser.add_argument('--days', type=int, default=7, help='Number of days to analyze (default: 7)')
    parser.add_argument('--output', type=str, help='Output file for JSON results')
    parser.add_argument('--db', type=str, default='charger_data.db', help='Database file path')
    
    args = parser.parse_args()
    
    analyzer = UtilizationAnalyzer(args.db)
    df = analyzer.load_data(args.days)
    insights = analyzer.generate_insights(df)
    
    # Print report
    analyzer.print_report(insights)
    
    # Save to file if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(insights, f, indent=2)
        print(f"\nResults saved to {args.output}")

if __name__ == "__main__":
    main()
