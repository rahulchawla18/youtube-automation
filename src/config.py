"""
Configuration and constants for the YouTube AI Daily Digest.

All sensitive values are loaded from environment variables.
For local development, create a .env file from .env.example.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ─── Search Configuration ─────────────────────────────────────────────────────

SEARCH_QUERIES = [
    "AI news today",
    "Generative AI tutorial",
    "Agentic AI agents",
    "AI automation tools",
    "Large Language Models LLM",
    "AI coding assistant",
    "ChatGPT Claude Gemini AI",
]

MAX_RESULTS_PER_QUERY = 5       # Videos fetched per search query
TOTAL_VIDEOS_IN_EMAIL = 10      # Final curated count in the digest

# ─── YouTube Data API v3 ──────────────────────────────────────────────────────

YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "")

# ─── Gmail SMTP ───────────────────────────────────────────────────────────────

GMAIL_ADDRESS = os.environ.get("GMAIL_ADDRESS", "")
GMAIL_APP_PASSWORD = os.environ.get("GMAIL_APP_PASSWORD", "")
RECIPIENT_EMAIL = os.environ.get("RECIPIENT_EMAIL", "") or GMAIL_ADDRESS
