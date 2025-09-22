# iOS Shortcuts Setup Guide

This guide explains how to set up iOS Shortcuts to display the charger status on your iPhone.

## Prerequisites

- iPhone with iOS 14 or later
- Shortcuts app (pre-installed)
- Pushcut app (free version available on App Store)

## Setup Steps

### 1. Create the Shortcut

1. Open the **Shortcuts** app on your iPhone
2. Tap the **"+"** button to create a new shortcut
3. Name it "Charger Status"

### 2. Add HTTP Request Action

1. Search for "Get Contents of URL" and add it
2. Configure the URL to point to your GitHub data file:
   ```
   https://raw.githubusercontent.com/felixSouan/State_of_the_Charge/main/data.json
   ```

3. Set Method to **GET**
4. Add Headers:
   - Key: `Accept`
   - Value: `application/json`

### 3. Parse JSON Response

1. Add "Get Value from Input" action
2. Set Key to `status`
3. Add another "Get Value from Input" action
4. Set Key to `timestamp`

### 4. Format the Output

1. Add "Text" action with this format:
   ```
   🔌 FLO Charger Status
   
   Status: [Status from previous step]
   Last Updated: [Timestamp from previous step]
   
   Tap to refresh
   ```

2. Add "Show Result" action to display the text

### 5. Create Widget with Pushcut

1. Download **Pushcut** from the App Store
2. Open Pushcut and create a new widget
3. Select your "Charger Status" shortcut
4. Choose widget size (Small, Medium, or Large)
5. Add the widget to your home screen

### 6. Advanced: Auto-Refresh Widget

1. In Pushcut, enable "Auto Refresh"
2. Set refresh interval to 5 minutes
3. Enable "Background Refresh" in iOS Settings > Shortcuts

## Alternative: Simple Home Screen Widget

If you prefer not to use Pushcut, you can create a simple widget:

1. Long press on your home screen
2. Tap the "+" button
3. Search for "Shortcuts"
4. Select your "Charger Status" shortcut
5. Choose widget size and add to home screen

## Troubleshooting

### Widget Not Updating
- Check that Background App Refresh is enabled for Shortcuts
- Ensure your GitHub repository is public
- Verify the URL in your shortcut is correct

### Connection Errors
- Check your internet connection
- Verify the GitHub URL is accessible
- Try running the shortcut manually first

### Status Shows "Unknown"
- The scraper might not have run yet
- Check the GitHub Actions tab in your repository
- Verify the scraper is working by running it locally

## Customization

You can customize the widget by:

1. **Changing Colors**: Modify the text format to include emoji or symbols
2. **Adding More Info**: Include additional data like utilization percentage
3. **Different Sizes**: Create multiple shortcuts for different widget sizes
4. **Notifications**: Add notification actions for status changes

## Example Shortcut Actions

Here's the complete action sequence for your shortcut:

1. **Get Contents of URL**
   - URL: `https://raw.githubusercontent.com/felixSouan/State_of_the_Charge/main/data.json`
   - Method: GET

2. **Get Value from Input**
   - Key: `status`

3. **Get Value from Input**
   - Key: `timestamp`

4. **Text**
   - Content: Custom formatted text with status and timestamp

5. **Show Result**

## Security Notes

- The GitHub repository should be public for the widget to work
- No sensitive data is exposed (only charger status)
- The scraper respects rate limits and terms of service
