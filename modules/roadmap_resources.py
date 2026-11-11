from modules.roadmap_generator import generate_roadmap
from youtube_resources import search_youtube


def get_roadmap_resources(career, student_skills):

    roadmap = generate_roadmap(career, student_skills)

    for stage in roadmap:

        topics = stage.get("topics", [])

        search_query = ( f"{stage['title']} " + " ".join(topics[:3]) + " tutorial for Data Science")
        print(f"\n{'=' * 65}")
        print(f"STAGE {stage['stage']}: {stage['title']}")
        print(f"Status: {stage['status']}")
        print(f"Searching YouTube: {search_query}")

        videos = search_youtube(search_query, max_results=3)

        if videos:
            for index, video in enumerate(videos, start=1):
                print(f"\n{index}. {video['title']}")
                print(f"Channel: {video['channel']}")
                print(f"Link: {video['url']}")
        else:
            print("No videos found.")


if __name__ == "__main__":

    career = "Data Scientist"

    student_skills = [
        "Python",
        "SQL",
        "Statistics"
    ]

    get_roadmap_resources(career, student_skills)