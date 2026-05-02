"""
YouTube AI Daily Digest — Main Entry Point

Orchestrates the full pipeline:
  1. Search YouTube for top AI videos (last 24h)
  2. Generate AI summaries via Google Gemini
  3. Build a premium HTML email digest
  4. Send it via Gmail SMTP
"""

import logging
import sys
from datetime import datetime, timedelta, timezone

from src.config import (
    YOUTUBE_API_KEY,
    GMAIL_ADDRESS,
    GMAIL_APP_PASSWORD,
    RECIPIENT_EMAIL,
    TOTAL_VIDEOS_IN_EMAIL,
)
from src.youtube_client import search_videos
from src.email_builder import build_email_html
from src.email_sender import send_email

# ─── Logging Setup ────────────────────────────────────────────────────────────

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s │ %(levelname)-7s │ %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)


def main():
    """Run the full daily digest pipeline."""

    logger.info("🚀 Starting YouTube Daily Digest...")

    # ── Validate required configuration ──────────────────────────────
    missing = []
    if not YOUTUBE_API_KEY:
        missing.append("YOUTUBE_API_KEY")
    if not GMAIL_ADDRESS:
        missing.append("GMAIL_ADDRESS")
    if not GMAIL_APP_PASSWORD:
        missing.append("GMAIL_APP_PASSWORD")

    if missing:
        logger.error(
            f"❌ Missing required environment variables: {', '.join(missing)}"
        )
        sys.exit(1)

    recipient = RECIPIENT_EMAIL or GMAIL_ADDRESS
    logger.info(f"📧 Recipient: {recipient}")

    # ── Step 1: Fetch videos from YouTube ────────────────────────────
    logger.info("📡 Step 1/3 — Searching YouTube for top AI videos...")
    videos = search_videos()

    if not videos:
        logger.warning("⚠️  No videos found. Exiting without sending email.")
        sys.exit(0)

    # Take only the top N
    videos = videos[:TOTAL_VIDEOS_IN_EMAIL]
    logger.info(f"📋 Curated top {len(videos)} videos")

    # ── Step 2: Build HTML email ─────────────────────────────────────
    logger.info("🎨 Step 2/3 — Building HTML email digest...")
    ist = timezone(timedelta(hours=5, minutes=30))
    today = datetime.now(ist).strftime("%B %d, %Y")
    subject = f"🎬 AI Video Digest — {today}"
    html = build_email_html(videos)

    # ── Step 3: Send email ───────────────────────────────────────────
    logger.info(f"📧 Step 3/3 — Sending email to {recipient}...")
    send_email(subject, html)

    logger.info("✅ Daily digest pipeline complete!")


if __name__ == "__main__":
    main()
