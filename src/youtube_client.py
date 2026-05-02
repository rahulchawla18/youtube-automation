"""
YouTube Data API v3 client for searching and fetching video data.

Searches across multiple AI-related queries, deduplicates results,
enriches them with statistics, and ranks by engagement score.
"""

import logging
from datetime import datetime, timedelta, timezone

from googleapiclient.discovery import build

from src.config import YOUTUBE_API_KEY, MAX_RESULTS_PER_QUERY, SEARCH_QUERIES

logger = logging.getLogger(__name__)


def _build_youtube_service():
    """Build the YouTube API service client."""
    return build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


def search_videos() -> list[dict]:
    """
    Search YouTube for AI-related videos published in the last 24 hours.

    Returns a deduplicated, engagement-ranked list of video metadata.
    Each video dict contains: video_id, title, description, channel,
    published_at, thumbnail, url, views, likes, comments.
    """
    youtube = _build_youtube_service()

    # Only look at videos from the last 24 hours
    published_after = (
        datetime.now(timezone.utc) - timedelta(days=1)
    ).isoformat()

    all_videos: dict[str, dict] = {}  # video_id → video_data (dedup)

    for query in SEARCH_QUERIES:
        try:
            search_response = (
                youtube.search()
                .list(
                    q=query,
                    part="snippet",
                    type="video",
                    order="relevance",
                    publishedAfter=published_after,
                    maxResults=MAX_RESULTS_PER_QUERY,
                    relevanceLanguage="en",
                )
                .execute()
            )

            for item in search_response.get("items", []):
                video_id = item["id"]["videoId"]
                if video_id not in all_videos:
                    thumbnails = item["snippet"]["thumbnails"]
                    thumb = thumbnails.get(
                        "high", thumbnails.get("medium", thumbnails["default"])
                    )
                    all_videos[video_id] = {
                        "video_id": video_id,
                        "title": item["snippet"]["title"],
                        "description": item["snippet"]["description"],
                        "channel": item["snippet"]["channelTitle"],
                        "published_at": item["snippet"]["publishedAt"],
                        "thumbnail": thumb["url"],
                        "url": f"https://www.youtube.com/watch?v={video_id}",
                    }

            count = len(search_response.get("items", []))
            logger.info(f"✅ Fetched {count} videos for query: '{query}'")

        except Exception as e:
            logger.warning(f"⚠️  Failed to search for '{query}': {e}")

    # Fetch statistics for all videos
    video_ids = list(all_videos.keys())
    if video_ids:
        _enrich_with_stats(youtube, all_videos, video_ids)

    # Sort by engagement score and return
    ranked = sorted(
        all_videos.values(), key=_engagement_score, reverse=True
    )
    logger.info(f"📊 Total unique videos found: {len(ranked)}")
    return ranked


def _enrich_with_stats(
    youtube, videos: dict, video_ids: list[str]
) -> None:
    """Fetch view count, like count, and comment count for each video."""
    # YouTube API allows up to 50 IDs per request
    for i in range(0, len(video_ids), 50):
        batch = video_ids[i : i + 50]
        try:
            stats_response = (
                youtube.videos()
                .list(part="statistics", id=",".join(batch))
                .execute()
            )

            for item in stats_response.get("items", []):
                vid = item["id"]
                stats = item.get("statistics", {})
                videos[vid]["views"] = int(stats.get("viewCount", 0))
                videos[vid]["likes"] = int(stats.get("likeCount", 0))
                videos[vid]["comments"] = int(
                    stats.get("commentCount", 0)
                )

        except Exception as e:
            logger.warning(f"⚠️  Failed to fetch stats batch: {e}")


def _engagement_score(video: dict) -> float:
    """
    Calculate a weighted engagement score for ranking.

    Weights:
      - Views   × 0.4  (broad reach)
      - Likes   × 30   (quality signal)
      - Comments × 50   (deep engagement)
    """
    views = video.get("views", 0)
    likes = video.get("likes", 0)
    comments = video.get("comments", 0)
    return views * 0.4 + likes * 30 + comments * 50
