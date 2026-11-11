import json
with open("data/career_requirements.json", "r") as file:
    career_requirements = json.load(file)
def normalize(skill):
    return skill.strip().casefold()
def analyze_skill_gap(student_skills, career):
    if career not in career_requirements:
        print("Career not found in knowledge base!")
        return None
    required_skills = career_requirements[career]

    # Normalize skills for comparison
    student_set = {
        normalize(skill): skill
        for skill in student_skills
    }

    required_set = {
        normalize(skill): skill
        for skill in required_skills
    }

    # Find matching skills
    matched_skills = [
        required_set[skill]
        for skill in student_set
        if skill in required_set
    ]

    # Find missing skills
    missing_skills = [
        skill
        for skill in required_set
        if skill not in student_set
    ]

    # Calculate skill coverage
    total_required = len(required_set)

    coverage = (
        len(matched_skills) / total_required
    ) * 100 if total_required else 0

    # Return analysis
    return {
        "career": career,
        "matched_skills": matched_skills,
        "missing_skills": missing_skills,
        "coverage": round(coverage, 2)
    }


# =====================================
# TEST WITH SAMPLE STUDENT
# =====================================

student_skills = [
    "Python",
    "SQL",
    "Statistics"
]

selected_career = "Data Scientist"

result = analyze_skill_gap(
    student_skills,
    selected_career
)


# Display results
if result:

    print("\n========== SKILL GAP ANALYSIS ==========")

    print("\nSelected Career:", result["career"])

    print("\nExisting Skills:")
    for skill in result["matched_skills"]:
        print("  ✓", skill)

    print("\nSkills To Learn:")
    for skill in result["missing_skills"]:
        print("  -", skill)

    print("\nSkill Coverage:", result["coverage"], "%")