"""
HTML email template builder for the YouTube AI Daily Digest.

Generates a premium dark-themed HTML email with video cards,
thumbnails, stats, and AI summaries. Uses table-based layout
for maximum email client compatibility.
"""

from datetime import datetime, timedelta, timezone


def build_email_html(videos: list[dict]) -> str:
    """Build the full HTML email with all video cards."""
    ist = timezone(timedelta(hours=5, minutes=30))
    today = datetime.now(ist).strftime("%B %d, %Y")

    video_cards = "\n".join(
        _build_video_card(v, i + 1) for i, v in enumerate(videos)
    )

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Video Digest - {today}</title>
</head>
<body style="margin:0;padding:0;background-color:#0d1117;font-family:'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;">

<table width="100%" cellpadding="0" cellspacing="0" role="presentation" style="background-color:#0d1117;padding:20px 0;">
<tr><td align="center">
<table width="640" cellpadding="0" cellspacing="0" style="max-width:640px;width:100%;">

<!-- ═══ HEADER ═══ -->
<tr><td style="background:linear-gradient(135deg,#7c3aed 0%,#2563eb 50%,#06b6d4 100%);border-radius:16px 16px 0 0;padding:40px 32px;text-align:center;">
  <h1 style="margin:0;color:#fff;font-size:28px;font-weight:800;letter-spacing:-0.5px;">
    &#127916; AI Video Digest
  </h1>
  <p style="margin:8px 0 0;color:rgba(255,255,255,0.85);font-size:15px;">
    Your daily curated feed &mdash; {today}
  </p>
</td></tr>

<!-- ═══ INTRO ═══ -->
<tr><td style="background-color:#161b22;padding:24px 32px 8px;">
  <p style="margin:0;color:#8b949e;font-size:14px;line-height:1.6;">
    &#128075; Here are today's <strong style="color:#c9d1d9;">{len(videos)} top AI videos</strong>
    curated from YouTube &mdash; covering Generative AI, Agentic AI, LLMs,
    AI automation, and more.
  </p>
</td></tr>

<!-- ═══ VIDEO CARDS ═══ -->
{video_cards}

<!-- ═══ FOOTER ═══ -->
<tr><td style="background-color:#161b22;border-radius:0 0 16px 16px;padding:24px 32px;text-align:center;border-top:1px solid #21262d;">
  <p style="margin:0;color:#484f58;font-size:12px;line-height:1.6;">
    &#9889; Powered by YouTube Data API<br>
    &#128260; Delivered daily via GitHub Actions<br>
    <span style="color:#6e7681;">Built with &#10084;&#65039; by your AI automation agent</span>
  </p>
</td></tr>

</table>
</td></tr>
</table>

</body>
</html>"""


def _build_video_card(video: dict, rank: int) -> str:
    """Build an HTML card for a single video."""
    title = _escape_html(video.get("title", "Untitled"))
    channel = _escape_html(video.get("channel", "Unknown Channel"))
    views = _format_number(video.get("views", 0))
    likes = _format_number(video.get("likes", 0))
    comments = _format_number(video.get("comments", 0))
    thumbnail = video.get("thumbnail", "")
    url = video.get("url", "#")
    # Rank badge colors — gold / purple / green for top 3
    badge_colors = {1: "#fbbf24", 2: "#a78bfa", 3: "#34d399"}
    badge_bg = badge_colors.get(rank, "#6b7280")

    return f"""<tr><td style="background-color:#161b22;padding:12px 32px;">
<table width="100%" cellpadding="0" cellspacing="0" style="background-color:#0d1117;border:1px solid #21262d;border-radius:12px;overflow:hidden;">
<tr><td>
  <a href="{url}" target="_blank" style="text-decoration:none;">
    <img src="{thumbnail}" alt="" width="100%" style="display:block;border-radius:12px 12px 0 0;" />
  </a>
</td></tr>
<tr><td style="padding:16px 20px;">
<table width="100%" cellpadding="0" cellspacing="0">
<tr><td>
  <span style="display:inline-block;background-color:{badge_bg};color:#000;font-size:11px;font-weight:800;padding:2px 8px;border-radius:4px;">#{rank}</span>
  <a href="{url}" target="_blank" style="text-decoration:none;">
    <h2 style="margin:8px 0 4px;color:#e6edf3;font-size:16px;font-weight:700;line-height:1.3;">{title}</h2>
  </a>
  <p style="margin:0 0 12px;color:#7c3aed;font-size:13px;font-weight:600;">{channel}</p>
  <p style="margin:0;color:#8b949e;font-size:12px;">
    &#128065; {views} views &nbsp;&middot;&nbsp; &#128077; {likes} likes &nbsp;&middot;&nbsp; &#128172; {comments} comments
  </p>
</td></tr>
</table>
</td></tr>
</table>
</td></tr>"""


def _format_number(n: int) -> str:
    """Format large numbers with K/M suffixes."""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def _escape_html(text: str) -> str:
    """Escape special HTML characters in user-generated content."""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )
