# GmailOrganiser
A Python application that interacts with the Gmail API to fetch and organize emails based on specific criteria. The application allows users to label emails with specific keywords, helping to keep their inbox organized.
## Features
- Authenticate with Gmail API using OAuth 2.0
- Fetch emails based on specific keywords in the subject line
- Automatically add labels to matching emails
- Customizable label and keyword options
## Used
- Python
- Google API Client Library
- Gmail API
## Setup
1. Create a project in the [Google Cloud Console](https://console.developers.google.com/).
2. Enable the Gmail API for your project.
3. Create OAuth 2.0 credentials and download the `credentials.json` file.
4. Place the `credentials.json` file in the project directory.
## Usage
1. Run the application:
   ```bash
   python fetch_emails.py
   ```
2. Follow the on-screen instructions to authenticate with your Google account.
3. Customize the `keyword` and `label_id` in the script to filter and label your emails.
## Acknowledgments
- Special thanks to the Google for the documentation and resources.
