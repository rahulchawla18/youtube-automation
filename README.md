# YouTube Daily Digest

Automated YouTube video digest that searches for top AI videos and sends a curated HTML email daily.

## Features

- 🔍 Searches YouTube for trending AI videos from the last 24 hours
- 📧 Sends beautifully formatted HTML email digests
- 🎨 Premium dark-themed email template with video cards
- 📊 Displays video stats (views, likes, comments)
- ⚡ Automated daily delivery via GitHub Actions

## Prerequisites

- Python 3.8+
- YouTube Data API v3 key
- Gmail account with App Password

## Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd youtube-automation
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Copy `.env.example` to `.env`:

```bash
copy .env.example .env
```

Fill in your actual values in `.env`:

```env
YOUTUBE_API_KEY=your_youtube_api_key_here
GMAIL_ADDRESS=your_email@gmail.com
GMAIL_APP_PASSWORD=your_16_char_app_password
RECIPIENT_EMAIL=recipient@gmail.com
```

### 4. Get API Keys

#### YouTube Data API v3 Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable YouTube Data API v3 in "APIs & Services" > "Library"
4. Create credentials: "APIs & Services" > "Credentials" > "Create Credentials" > "API Key"
5. Copy the API key

#### Gmail App Password

1. Enable 2-Step Verification on your Google account
2. Go to [Google Account Security](https://myaccount.google.com/security)
3. Under "How you sign in to Google", click "App passwords"
4. Select "Mail" and "Other (Custom name)"
5. Generate and copy the 16-character password

## Usage

### Manual Execution

Run the script manually:

```bash
python main.py
```

The script will:
1. Search YouTube for top AI videos from the last 24 hours
2. Build an HTML email digest with video cards
3. Send the email to the specified recipient

### Automated Daily Execution (GitHub Actions)

To set up automated daily delivery:

1. **Push your code to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Add secrets to your GitHub repository:**
   - Go to your repository on GitHub
   - Navigate to: Settings > Secrets and variables > Actions
   - Click "New repository secret" and add each of these:
     - `YOUTUBE_API_KEY` - Your YouTube Data API key
     - `GMAIL_ADDRESS` - Your Gmail address
     - `GMAIL_APP_PASSWORD` - Your Gmail App Password
     - `RECIPIENT_EMAIL` - Email recipient (optional, defaults to GMAIL_ADDRESS)

3. **The workflow will automatically run:**
   - Every day at 6:00 AM UTC (11:30 AM IST)
   - You can also trigger it manually from the "Actions" tab on GitHub

4. **Monitor execution:**
   - Go to the "Actions" tab in your GitHub repository
   - View logs and execution history

## Project Structure

```
youtube-automation/
├── src/
│   ├── __init__.py
│   ├── config.py           # Configuration and environment variables
│   ├── youtube_client.py   # YouTube API integration
│   ├── email_builder.py    # HTML email template builder
│   └── email_sender.py     # Gmail SMTP email sender
├── main.py                 # Main entry point
├── requirements.txt        # Python dependencies
├── .env.example           # Environment variables template
└── README.md              # This file
```

## Configuration

Edit `src/config.py` to customize:

- `SEARCH_QUERIES`: YouTube search terms
- `MAX_RESULTS_PER_QUERY`: Videos fetched per query (default: 5)
- `TOTAL_VIDEOS_IN_EMAIL`: Final video count in digest (default: 10)

## Dependencies

- `google-api-python-client` - YouTube Data API v3 client
- `python-dotenv` - Environment variable management

## License

MIT License - see LICENSE file for details

## Author

Built with ❤️ by your AI automation agent
