# Deployment Guide

This guide walks you through deploying the Charger Status Monitor system.

## Prerequisites

- Python 3.7 or later
- Git
- GitHub account
- macOS (for Übersicht widget)
- iOS device (for phone widget)

## Step 1: Local Setup

### 1.1 Install Dependencies

```bash
# Clone or download the project
cd State_of_the_Charge

# Install Python dependencies
pip3 install -r requirements.txt
```

### 1.2 Test the System

```bash
# Run the comprehensive test suite
python3 test_system.py

# Test individual components
python3 charger_scraper.py
python3 utilization_analysis.py --days 1
```

## Step 2: GitHub Deployment

### 2.1 Create GitHub Repository

1. Create a new public repository on GitHub
2. Name it `State_of_the_Charge` (or your preferred name)
3. Initialize with README

### 2.2 Push Your Code

```bash
# Initialize git repository
git init
git add .
git commit -m "Initial commit: Charger Status Monitor"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/State_of_the_Charge.git
git branch -M main
git push -u origin main
```

### 2.3 Update Configuration

1. Edit `ubersicht_widget/charger-status.widget/get_status.py`
2. Replace `YOUR_USERNAME` with your actual GitHub username
3. Edit `ios_shortcuts_guide.md` and replace `YOUR_USERNAME`
4. Commit and push the changes

### 2.4 Verify GitHub Actions

1. Go to your repository on GitHub
2. Click on "Actions" tab
3. The workflow should start automatically
4. Check that it runs every 5 minutes

## Step 3: macOS Widget Setup

### 3.1 Install Übersicht

1. Download from [Übersicht website](https://github.com/felixhageloh/uebersicht)
2. Install the application
3. Launch Übersicht

### 3.2 Install the Widget

1. Copy the `ubersicht_widget/charger-status.widget` folder to:
   ```
   ~/Library/Application Support/Übersicht/widgets/
   ```

2. The widget should appear in Übersicht
3. Drag it to your desired position on the desktop

### 3.3 Configure the Widget

1. Right-click the widget
2. Select "Edit Widget"
3. Verify the GitHub URL is correct
4. Save and refresh

## Step 4: iOS Widget Setup

### 4.1 Create Shortcut

1. Open the **Shortcuts** app on your iPhone
2. Create a new shortcut named "Charger Status"
3. Follow the detailed instructions in `ios_shortcuts_guide.md`

### 4.2 Install Pushcut (Optional)

1. Download **Pushcut** from the App Store
2. Create a widget using your shortcut
3. Add to home screen

### 4.3 Alternative: Native Widget

1. Long press on home screen
2. Tap "+" and search for "Shortcuts"
3. Select your "Charger Status" shortcut
4. Add to home screen

## Step 5: Verification

### 5.1 Check GitHub Actions

1. Verify the workflow runs every 5 minutes
2. Check that `data.json` is updated
3. Ensure the database file is committed

### 5.2 Test Widgets

1. **macOS Widget**: Should show current status and update every 5 minutes
2. **iOS Widget**: Should display status when tapped or refreshed

### 5.3 Monitor Logs

1. Check GitHub Actions logs for any errors
2. Monitor the scraper output
3. Verify data is being stored correctly

## Step 6: Local Development (Optional)

### 6.1 Run Local Scheduler

```bash
# Start the background scheduler
python3 scheduler.py
```

### 6.2 Run Local API Server

```bash
# Start the API server
python3 api_server.py

# Test the API
curl http://localhost:5000/api/status
```

### 6.3 Analyze Data

```bash
# Generate utilization report
python3 utilization_analysis.py --days 7 --output report.json
```

## Troubleshooting

### Common Issues

1. **Widget Not Updating**
   - Check GitHub Actions are running
   - Verify repository is public
   - Ensure URL is correct in widget files

2. **Scraper Errors**
   - Check internet connection
   - Verify ChargeHub is accessible
   - Review GitHub Actions logs

3. **Database Issues**
   - Check file permissions
   - Verify SQLite is working
   - Reset database if corrupted

4. **API Errors**
   - Check Flask installation
   - Verify port availability
   - Review error logs

### Debug Commands

```bash
# Test scraper manually
python3 charger_scraper.py

# Check database contents
sqlite3 charger_data.db "SELECT * FROM utilization ORDER BY timestamp DESC LIMIT 5;"

# Test API endpoints
curl http://localhost:5000/api/health
curl http://localhost:5000/api/status

# Run analysis
python3 utilization_analysis.py --days 1
```

## Maintenance

### Regular Tasks

1. **Monitor GitHub Actions**: Check that workflows are running
2. **Review Logs**: Look for any errors or issues
3. **Update Dependencies**: Keep Python packages updated
4. **Check Data Quality**: Verify status data is accurate

### Updates

1. **Code Updates**: Push changes to GitHub
2. **Widget Updates**: Update local widget files
3. **Configuration Changes**: Update URLs and settings

## Security Considerations

- Repository is public (required for widgets to work)
- No sensitive data is exposed
- Scraper respects rate limits
- Follows ChargeHub terms of service

## Support

If you encounter issues:

1. Check the troubleshooting section
2. Review GitHub Actions logs
3. Test components individually
4. Create an issue with detailed information

---

**Note**: This system is designed for personal use. Please respect the terms of service of all involved services and use responsibly.
