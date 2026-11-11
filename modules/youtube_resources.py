import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("YOUTUBE_API_KEY")

YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"


def search_youtube(query, max_results=5):

    if not API_KEY:
        print("Error: YouTube API key not found.")
        return []

    params = {
        "part": "snippet",
        "q": query,
        "type": "video",
        "maxResults": max_results,
        "order": "relevance",
        "key": API_KEY
    }

    try:
        response = requests.get(
            YOUTUBE_SEARCH_URL,
            params=params,
            timeout=15
        )

        response.raise_for_status()
        data = response.json()

        videos = []

        for item in data.get("items", []):
            video_id = item["id"]["videoId"]
            snippet = item["snippet"]

            videos.append({
                "title": snippet["title"],
                "channel": snippet["channelTitle"],
                "description": snippet["description"],
                "thumbnail": snippet["thumbnails"]["high"]["url"],
                "url": f"https://www.youtube.com/watch?v={video_id}"
            })

        return videos

    except requests.exceptions.RequestException as error:
        print("YouTube API request failed:", error)
        return []