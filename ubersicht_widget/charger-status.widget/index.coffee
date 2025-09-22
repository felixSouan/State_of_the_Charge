# Charger Status Widget for Übersicht
# Displays the current status of the University of Waterloo FLO charger

# Configuration
command: "python3 #{@path}/get_status.py"
refreshFrequency: 300000 # 5 minutes

# Widget styling
style: """
  top: 20px
  right: 20px
  width: 200px
  background: rgba(0, 0, 0, 0.8)
  border-radius: 10px
  padding: 15px
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif
  color: white
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3)
  backdrop-filter: blur(10px)
  border: 1px solid rgba(255, 255, 255, 0.1)
"""

# Status color mapping
statusColors:
  'Available': '#4CAF50'  # Green
  'In Use': '#F44336'     # Red
  'Out of Order': '#FF9800' # Orange
  'Unknown': '#9E9E9E'    # Gray

render: (output) ->
  try
    data = JSON.parse(output)
    status = data.status || 'Unknown'
    timestamp = data.timestamp || 'No data'
    lastUpdated = data.last_updated || timestamp
    
    # Format timestamp for display
    if timestamp and timestamp != 'No data'
      date = new Date(timestamp)
      timeStr = date.toLocaleTimeString('en-US', { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: true 
      })
    else
      timeStr = 'Unknown'
    
    # Get status color
    color = @statusColors[status] || @statusColors['Unknown']
    
    """
    <div class="widget-container">
      <div class="header">
        <h3>🔌 FLO Charger</h3>
        <div class="location">UW Campus</div>
      </div>
      
      <div class="status-section">
        <div class="status-indicator" style="background-color: #{color}"></div>
        <div class="status-text">#{status}</div>
      </div>
      
      <div class="timestamp">
        <div class="label">Last Check:</div>
        <div class="time">#{timeStr}</div>
      </div>
      
      <div class="footer">
        <div class="refresh-info">Updates every 5 min</div>
      </div>
    </div>
    """
  catch error
    """
    <div class="widget-container">
      <div class="header">
        <h3>🔌 FLO Charger</h3>
        <div class="location">UW Campus</div>
      </div>
      
      <div class="status-section">
        <div class="status-indicator" style="background-color: #{@statusColors['Unknown']}"></div>
        <div class="status-text">Error</div>
      </div>
      
      <div class="timestamp">
        <div class="label">Status:</div>
        <div class="time">Connection failed</div>
      </div>
    </div>
    """

# CSS styling
css: """
  .widget-container {
    display: flex;
    flex-direction: column;
    gap: 10px;
  }
  
  .header {
    text-align: center;
    border-bottom: 1px solid rgba(255, 255, 255, 0.2);
    padding-bottom: 8px;
  }
  
  .header h3 {
    margin: 0;
    font-size: 16px;
    font-weight: 600;
  }
  
  .location {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.7);
    margin-top: 2px;
  }
  
  .status-section {
    display: flex;
    align-items: center;
    gap: 10px;
    justify-content: center;
  }
  
  .status-indicator {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    animation: pulse 2s infinite;
  }
  
  @keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.5; }
    100% { opacity: 1; }
  }
  
  .status-text {
    font-size: 18px;
    font-weight: 600;
    text-align: center;
  }
  
  .timestamp {
    text-align: center;
    font-size: 12px;
    color: rgba(255, 255, 255, 0.8);
  }
  
  .label {
    font-weight: 500;
    margin-bottom: 2px;
  }
  
  .time {
    font-family: 'SF Mono', Monaco, monospace;
  }
  
  .footer {
    text-align: center;
    font-size: 10px;
    color: rgba(255, 255, 255, 0.5);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding-top: 8px;
  }
  
  .refresh-info {
    font-style: italic;
  }
"""
