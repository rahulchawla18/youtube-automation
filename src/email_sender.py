"""
Gmail SMTP email sender.

Sends HTML emails via Gmail using TLS and App Password authentication.
"""

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.config import GMAIL_ADDRESS, GMAIL_APP_PASSWORD, RECIPIENT_EMAIL

logger = logging.getLogger(__name__)

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def send_email(subject: str, html_body: str) -> bool:
    """
    Send an HTML email via Gmail SMTP.

    Args:
        subject:   Email subject line.
        html_body: Full HTML content of the email.

    Returns:
        True if the email was sent successfully.

    Raises:
        Exception: If sending fails after connection.
    """
    msg = MIMEMultipart("alternative")
    msg["From"] = f"AI Video Digest <{GMAIL_ADDRESS}>"
    msg["To"] = RECIPIENT_EMAIL
    msg["Subject"] = subject

    msg.attach(MIMEText(html_body, "html"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(GMAIL_ADDRESS, GMAIL_APP_PASSWORD)
            server.sendmail(GMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())

        logger.info(f"✅ Email sent successfully to {RECIPIENT_EMAIL}")
        return True

    except Exception as e:
        logger.error(f"❌ Failed to send email: {e}")
        raise
