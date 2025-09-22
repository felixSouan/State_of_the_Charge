# Charger Status Monitor

A real-time monitoring system for the University of Waterloo FLO electric vehicle charger (ChargeHub LocID: 62901). This system scrapes public data from ChargeHub.com, stores historical data, and provides cross-device access through macOS and iOS widgets.

## Features

- 🔄 **Automated Polling**: Checks charger status every 5 minutes
- ☁️ **Cloud Hosting**: Runs on GitHub Actions for 24/7 availability
- 📊 **Data Storage**: SQLite database for historical analysis
- 🖥️ **macOS Widget**: Übersicht widget for desktop monitoring
- 📱 **iOS Widget**: Shortcuts-based widget for iPhone
- 📈 **Analytics**: Utilization pattern analysis

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Test the Scraper

```bash
python charger_scraper.py
```

### 3. Set Up GitHub Actions

1. Fork this repository
2. Update the GitHub URL in the widget files with your username
3. Push to GitHub - the workflow will start automatically

### 4. Install macOS Widget

1. Install [Übersicht](https://github.com/felixhageloh/uebersicht)
2. Copy the `ubersicht_widget` folder to your Übersicht widgets directory
3. Update the GitHub URL in `get_status.py`

### 5. Set Up iOS Widget

Follow the detailed guide in `ios_shortcuts_guide.md`

## Project Structure

```
State_of_the_Charge/
├── charger_scraper.py          # Main scraper script
├── api_server.py              # Flask API server
├── scheduler.py               # Background scheduler
├── utilization_analysis.py    # Data analysis script
├── requirements.txt           # Python dependencies
├── .github/workflows/         # GitHub Actions configuration
├── ubersicht_widget/          # macOS widget files
├── ios_shortcuts_guide.md     # iOS setup instructions
└── data.json                  # Public data endpoint
```

## Usage

### Manual Status Check

```bash
python charger_scraper.py
```

### Run Background Scheduler

```bash
python scheduler.py
```

### Start API Server

```bash
python api_server.py
```

### Analyze Utilization Patterns

```bash
python utilization_analysis.py --days 7
```

## API Endpoints

When running the API server locally:

- `GET /api/status` - Get current charger status
- `GET /api/history?limit=100` - Get historical data
- `POST /api/check` - Trigger manual status check
- `GET /api/health` - Health check

## Data Format

The system stores and provides data in this format:

```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "status": "Available",
  "last_updated": "2024-01-01T12:05:00Z",
  "source": "github_actions"
}
```

Status values:
- `Available` - Charger is free
- `In Use` - Charger is occupied
- `Out of Order` - Charger is not working
- `Unknown` - Status could not be determined

## Configuration

### GitHub Actions

The scraper runs automatically every 5 minutes via GitHub Actions. To modify the schedule, edit `.github/workflows/scraper.yml`:

```yaml
schedule:
  - cron: '*/5 * * * *'  # Every 5 minutes
```

### Widget URLs

Update these files with your GitHub username:
- `ubersicht_widget/charger-status.widget/get_status.py`
- `ios_shortcuts_guide.md`

Replace `YOUR_USERNAME` with your actual GitHub username.

## Troubleshooting

### Scraper Issues

1. **Network Errors**: Check internet connection and ChargeHub accessibility
2. **Parsing Errors**: The website structure may have changed
3. **Rate Limiting**: The scraper respects 12 requests/hour limit

### Widget Issues

1. **Not Updating**: Check GitHub Actions are running
2. **Connection Errors**: Verify repository is public and URL is correct
3. **Permission Errors**: Ensure Übersicht has necessary permissions

### Database Issues

1. **File Permissions**: Ensure write access to current directory
2. **Corruption**: Delete `charger_data.db` to reset
3. **Concurrent Access**: Only one process should write to the database

## Development

### Adding New Features

1. **New Data Sources**: Extend `ChargerScraper` class
2. **Additional Widgets**: Create new widget files
3. **Enhanced Analytics**: Modify `utilization_analysis.py`

### Testing

```bash
# Test scraper
python charger_scraper.py

# Test API
python api_server.py
curl http://localhost:5000/api/status

# Test analysis
python utilization_analysis.py --days 1
```

## Legal and Ethical Considerations

- ✅ **Public Data Only**: Only scrapes publicly available information
- ✅ **Rate Limited**: Respects 12 requests/hour limit
- ✅ **Personal Use**: Designed for individual use only
- ✅ **Terms Compliant**: Follows ChargeHub's terms of service

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is for personal use only. Please respect ChargeHub's terms of service and use responsibly.

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review GitHub Actions logs
3. Test components individually
4. Create an issue with detailed information

---

**Note**: This system is designed for personal use to help with EV charging planning. Please use responsibly and respect the terms of service of all involved services.
