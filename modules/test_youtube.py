from data.youtube_resources import search_youtube

videos = search_youtube("Python for Data Science beginner tutorial")

if videos:
    print("\nYouTube Videos Found:\n")

    for index, video in enumerate(videos, start=1):
        print(f"{index}. {video['title']}")
        print(f"   Channel: {video['channel']}")
        print(f"   URL: {video['url']}")
        print("-" * 60)

else:
    print("No videos found. Check your API configuration.")