import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Retrieve the YouTube API key
api_key = os.getenv("YOUTUBE_API_KEY")

if api_key:
    print("SUCCESS: YouTube API key loaded!")
else:
    print("ERROR: YouTube API key not found.")