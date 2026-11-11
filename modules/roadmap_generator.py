
import json

# Load learning roadmap data
with open("data/learning_roadmaps.json", "r") as file:
    roadmaps = json.load(file)


def normalize(value):
    return str(value).strip().casefold()


def generate_roadmap(career, student_skills):

    # Check career availability
    if career not in roadmaps:
        print("No roadmap available for this career.")
        return []

    stages = roadmaps[career]

    student_skills_set = {
        normalize(skill)
        for skill in student_skills
    }

    personalized_roadmap = []

    for stage in stages:

        required_skills = stage["skills"]

        # Find missing skills for this stage
        missing_skills = [
            skill for skill in required_skills
            if normalize(skill) not in student_skills_set
        ]

        # Determine stage status
        if not required_skills:
            status = "Recommended"
        elif not missing_skills:
            status = "Already covered"
        else:
            status = "Recommended"

        personalized_roadmap.append({

            "stage": stage["stage"],
            "title": stage["title"],
            "topics": stage["topics"],
            "prerequisite": stage["prerequisite"],
            "missing_skills": missing_skills,
            "status": status

        })

    return personalized_roadmap


# =====================================
# TEST WITH SAMPLE STUDENT
# =====================================

student_skills = [
    "Python",
    "SQL",
    "Statistics"
]

selected_career = "Data Scientist"

roadmap = generate_roadmap(
    selected_career,
    student_skills
)


# Display roadmap
print("\n========== PERSONALIZED LEARNING ROADMAP ==========")

print("\nCareer:", selected_career)

for stage in roadmap:

    print(f"\nStage {stage['stage']}: {stage['title']}")

    print("Status:", stage["status"])

    print("Topics:")

    for topic in stage["topics"]:
        print("  -", topic)

    if stage["missing_skills"]:
        print("Skills to develop:", stage["missing_skills"])

    if stage["prerequisite"]:
        print("Prerequisites:", stage["prerequisite"])

print("\nRoadmap generated successfully!")
