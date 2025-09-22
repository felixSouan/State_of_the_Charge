#!/usr/bin/env python3
"""
Flask API server for charger status data
Provides endpoints for widgets to fetch current and historical data
"""

from flask import Flask, jsonify, request
from charger_scraper import ChargerScraper
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
scraper = ChargerScraper()

@app.route('/api/status', methods=['GET'])
def get_current_status():
    """Get the current/latest charger status"""
    try:
        status_data = scraper.get_latest_status()
        if status_data:
            return jsonify({
                'success': True,
                'data': status_data
            })
        else:
            return jsonify({
                'success': False,
                'error': 'No status data available'
            }), 404
    except Exception as e:
        logger.error(f"Error getting current status: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@app.route('/api/history', methods=['GET'])
def get_status_history():
    """Get historical status data"""
    try:
        limit = request.args.get('limit', 100, type=int)
        if limit > 1000:  # Prevent excessive data requests
            limit = 1000
            
        history = scraper.get_status_history(limit)
        return jsonify({
            'success': True,
            'data': history,
            'count': len(history)
        })
    except Exception as e:
        logger.error(f"Error getting status history: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@app.route('/api/check', methods=['POST'])
def trigger_status_check():
    """Manually trigger a status check"""
    try:
        success, status = scraper.run_single_check()
        if success:
            return jsonify({
                'success': True,
                'message': f'Status check completed: {status}'
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Status check failed'
            }), 500
    except Exception as e:
        logger.error(f"Error triggering status check: {e}")
        return jsonify({
            'success': False,
            'error': 'Internal server error'
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'healthy',
        'service': 'Charger Status API'
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('DEBUG', 'False').lower() == 'true'
    
    logger.info(f"Starting API server on port {port}")
    app.run(host='0.0.0.0', port=port, debug=debug)
