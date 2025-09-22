# Product Requirements Document (PRD) for Charger Status Monitoring App

## Project Overview
### Project Name
Charger Status Monitor

### Project Description
This application monitors the real-time status ("Available", "In Use", or "Out of Order") of a specific 50kW FLO electric vehicle charger located at the University of Waterloo (ChargeHub LocID: 62901, Address: 263 Philip Street, Waterloo, ON, N2L 3G1). The system will scrape public data from ChargeHub.com, poll for updates every 5 minutes, store historical status data in a local database, and provide near-real-time visibility through widgets on macOS and iOS devices. The scraper will run in the background on a free cloud service to ensure availability even when the user's local machine is off. The goal is to help the user identify low-utilization times for better charging planning, assuming good-faith personal use and compliance with ChargeHub's terms (no excessive polling).

This PRD is designed for integration with a Context Engineering workflow (e.g., using Cursor AI or Claude Code). It provides structured features, priorities, and constraints to enable AI-generated documentation such as Implementation.md, project_structure.md, and UI_UX_doc.md. The AI will analyze this PRD to recommend a tech stack, break down implementation stages, and ensure modular context management to avoid hallucinations.

### Target Users
- University student (e.g., the primary user) with an EV, needing to monitor charger availability without constant manual checks.
- Assumptions: User has basic technical skills for setup (e.g., deploying to cloud, configuring widgets); devices include macOS laptop and iOS phone.

### Business Objectives
- Enable data-driven charging decisions by tracking utilization patterns.
- Provide cross-device access (Mac and phone) with minimal user intervention.
- Keep the solution free, reliable, and low-maintenance.

### Scope
- MVP: Core scraping, DB storage, cloud background running, and basic widgets.
- Full App: Add utilization analysis and notifications.
- Out of Scope: Mobile app development (use native widgets/shortcuts); Integration with FLO's private API; Multi-charger support; Paid services.

## Features and Requirements

### Identified Features
For each feature, include a description, user story, technical notes, and complexity estimate (low/medium/high) to aid AI analysis in the Context Engineering workflow.

1. **Data Scraping from ChargeHub**
   - Description: Periodically fetch the charger's status from the public ChargeHub page (URL: https://chargehub.com/en/ev-charging-stations/canada/ontario/waterloo/university-of-waterloo/electric-car-stations-near-me?locId=62901). Parse the Level 3 (DC fast charger) section for availability text (e.g., "1/1 Available" → Available; "0/1 Available" → In Use). Handle errors gracefully (e.g., return "Unknown" on failure).
   - User Story: As a user, I want the system to automatically check the charger's status every 5 minutes so I don't have to visit the website manually.
   - Technical Notes: Use Python with Requests and BeautifulSoup for parsing; Mimic browser headers to avoid blocks; Respect robots.txt and rate limits (e.g., no more than 12 polls/hour). ***Pseudo-code: response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}); soup = BeautifulSoup(response.text, 'html.parser'); status = soup.find('div', class_='availability').text.strip() if soup.find('div', class_='availability') else 'Unknown'.***
   - Complexity: Medium.
   - Acceptance Criteria:
     - Successfully parses and extracts correct status from at least 10 test page loads with varying availability.
     - Handles network errors (e.g., timeouts) and invalid HTML by returning 'Unknown' without crashing.
     - Respects rate limits by not exceeding 12 requests per hour in testing

2. **Data Storage in Database**
   - Description: Store each poll result (timestamp in ISO format, status as string) in a SQLite database. Initialize the DB if it doesn't exist with a table (utilization: timestamp TEXT, status TEXT).
   - User Story: As a user, I want historical data stored so I can analyze utilization patterns later.
   - Technical Notes: Use sqlite3 library; Local file-based DB (charger_data.db); Ensure thread-safety for background running. ***Exact schema: CREATE TABLE IF NOT EXISTS utilization (timestamp TEXT PRIMARY KEY, status TEXT CHECK(status IN ('Available', 'In Use', 'Out of Order', 'Unknown'))); For widgets/endpoints, output latest data as JSON: {"timestamp": "ISO_STRING", "status": "STRING"} or full history as array of objects.***
   - Complexity: Low.
   - Acceptance Criteria:
     - Initializes DB and table correctly on first run; inserts data without duplicates (using PRIMARY KEY).
     - Retrieves latest or historical data accurately in queries.
     - Handles concurrent access without data corruption in background mode.

3. **Background Polling and Cloud Hosting**
   - Description: Run the scraper in a loop every 5 minutes using a scheduler. Host on a free cloud platform (e.g., ***GitHub Actions*** with free credits) for always-on operation, exposing a simple endpoint (e.g., via Flask) to query the latest status/DB data remotely.
   - User Story: As a user, I want the monitoring to continue even if my Mac is off or offline, so I can check status from my phone anytime.
   - Technical Notes: Use Schedule library for polling; Deploy as a Python service on ***GitHub Actions*** (Git push, auto-deploy); Handle idle timeouts with pings if needed; Free tier only (no costs). ***For GitHub Actions: Define a .github/workflows/scraper.yml with cron schedule '*/5 * * * *'; Store data in JSON file pushed to repo; Widgets fetch from raw GitHub URL (e.g., https://raw.githubusercontent.com/username/repo/main/data.json). Pseudo-code for workflow step: - name: Run Scraper; run: python scraper.py && git add data.json && git commit -m 'Update data' && git push.***
   - Complexity: Medium.
   - Acceptance Criteria:
     - Runs scraper every 5 minutes reliably in free tier without exceeding limits (e.g., <2000 minutes/month usage).
     - Exposes data via static URL or endpoint that widgets can fetch successfully.
     - Continues operation independently of user's local machine.

4. **Mac Widget Display**
   - Description: Create a desktop widget (using Übersicht) that displays the current status (or last known from ~5 min ago), fetched from the cloud endpoint or local DB. Update every 5 minutes; Show "Available" (green), "In Use" (red), or "Unknown" with timestamp.
   - User Story: As a user on my Mac, I want a home screen widget showing the charger's status without opening an app.
   - Technical Notes: CoffeeScript/JS for widget; Fetch via HTTP if cloud-hosted, or read DB if local; Handle offline by showing cached data.
   - Complexity: Low.
   - Acceptance Criteria:
     - Displays correct status and timestamp from fetched data; updates every 5 minutes.
     - Shows appropriate colors and handles 'Unknown' gracefully.
     - Falls back to cached data when offline.

5. **iOS Phone Widget Display**
   - Description: Use iOS Shortcuts (with Pushcut for advanced widgets) to create a home/lock screen widget that pulls the latest status from the cloud endpoint. Refresh in background; Display similar to Mac widget.
   - User Story: As a user on my phone, I want to glance at the charger's status without needing my Mac.
   - Technical Notes: Shortcuts workflow to HTTP GET the endpoint; Pushcut for persistent widgets; Free version sufficient; Fallback to last-known if offline.
   - Complexity: Medium.
   - Acceptance Criteria:
     - Pulls and displays latest status via HTTP; refreshes in background.
     - Handles offline mode with last-known data.
     - Integrates with free Pushcut features without errors.

6. **Utilization Analysis**
   - Description: A script to query the DB and compute patterns (e.g., average utilization by hour/day using Pandas; Output low-usage times like "2-4 AM: 10% utilized").
   - User Story: As a user, I want insights into when the charger is typically free so I can plan my charging sessions.
   - Technical Notes: Use Pandas for analysis; Run on-demand (e.g., CLI script); Integrate with widgets if possible (e.g., show predicted availability).
   - Complexity: Medium.
   - Acceptance Criteria:
     - Computes accurate averages and patterns from sample DB data (e.g., >1 week).
     - Outputs readable insights (e.g., via console or file).
     - Runs without errors on historical data queries.

### Feature Categorization
- **Must-Have Features**: Data Scraping from ChargeHub, Data Storage in Database, Background Polling and Cloud Hosting (to enable always-on access).
- **Should-Have Features**: Mac Widget Display, iOS Phone Widget Display (for cross-device visibility).
- **Nice-to-Have Features**: Utilization Analysis (for added value post-MVP).

## Technical Requirements and Constraints
### Recommended Tech Stack Considerations
- Allow AI to research and suggest based on best practices (e.g., Python for core; Free cloud like ***GitHub Actions*** over Heroku/PythonAnywhere due to free tier limits). ***GitHub Actions preferred for sustainable free scheduling and static data exposure via repo files.***
- Factors: Low complexity, free tools, minimal dependencies; Scalability not critical (personal use); Timeline: MVP in hours/days.
- Constraints: No paid services (e.g., free ***GitHub Actions*** credits; No ChargeHub API—scrape public page only); Full internet access for scraping; Handle delays (status is "live-ish" with 1-5 min lag); Ethical: Poll sparingly to avoid abuse.

### Integration Requirements
- Cloud endpoint for widgets to fetch data (e.g., simple JSON response with latest status).
- Dependencies: Python libs (Requests, BeautifulSoup, Schedule, sqlite3, Flask for endpoint); macOS tools (Übersicht); iOS (Shortcuts/Pushcut).

### Performance and Scalability
- Polling: Every 5 min (288/day); DB: Handle months of data (~few MB).
- Offline Handling: Widgets show last-known status if no internet.

### Security and Compliance
- No sensitive data; Use headers to mimic browser; Comply with ChargeHub terms (personal use only).
- Error Handling: Graceful failures (e.g., retry on network issues).

### Timeline and Resources
- MVP: 1-2 days of AI-guided development.
- Full: 3-5 days including analysis and testing.
- Team: Solo user with AI assistance; Assume basic Python knowledge.

## Risks and Assumptions
### Technical Risks
- Site changes break scraper; Mitigation: Use robust CSS selectors with fallbacks in parsing.
- Cloud limits exceeded; Mitigation: Monitor usage and optimize script efficiency (e.g., quick executions).
### Operational Risks
- Data inaccuracies from ChargeHub lags; Mitigation: Timestamp all entries and note in widgets.
### Assumptions
- User has Git for deployment; ChargeHub status updates reliably; No legal issues from ethical scraping