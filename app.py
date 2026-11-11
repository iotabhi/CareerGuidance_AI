
import streamlit as st
import json
import sys
from pathlib import Path

# ==========================================
# PROJECT PATHS
# ==========================================

BASE_DIR = Path(__file__).resolve().parent
MODULES_DIR = BASE_DIR / "modules"
DATA_DIR = BASE_DIR / "data"

sys.path.insert(0, str(MODULES_DIR))

from career_recommender import recommend_careers
from roadmap_generator import generate_roadmap
from youtube_resources import search_youtube


# ==========================================
# PAGE CONFIGURATION
# ==========================================

st.set_page_config(
    page_title="Career Guidance AI",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI-Based Career Guidance System")

st.subheader(
    "Career Recommendation and Personalized Learning Roadmap"
)

st.write(
    "Discover suitable career paths using a semantic network, "
    "identify skill gaps, and access personalized learning resources."
)

st.divider()


# ==========================================
# LOAD CAREER REQUIREMENTS
# ==========================================

@st.cache_data
def load_requirements():
    file_path = DATA_DIR / "career_requirements.json"

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


career_requirements = load_requirements()


# ==========================================
# HELPER FUNCTIONS
# ==========================================

def normalize(value):
    return str(value).strip().casefold()


def analyze_skill_gap(career, student_skills):

    required_skills = career_requirements.get(career)

    if required_skills is None:
        return None

    known_skills = {
        normalize(skill) for skill in student_skills
    }

    matched = [
        skill for skill in required_skills
        if normalize(skill) in known_skills
    ]

    missing = [
        skill for skill in required_skills
        if normalize(skill) not in known_skills
    ]

    coverage = (
        len(matched) / len(required_skills) * 100
        if required_skills else 0
    )

    return {
        "matched": matched,
        "missing": missing,
        "coverage": coverage
    }


def display_roadmap(career, skills):

    roadmap = generate_roadmap(career, skills)

    if not roadmap:
        st.info(
            "A detailed learning roadmap is not yet available "
            "for this career."
        )
        return

    st.header("🗺️ Personalized Learning Roadmap")

    for index, stage in enumerate(roadmap):

        title = stage.get("title", "Learning Stage")
        stage_number = stage.get("stage", index + 1)
        status = stage.get("status", "Recommended")

        with st.expander(
            f"Stage {stage_number}: {title} — {status}",
            expanded=(index == 0)
        ):

            if status == "Already covered":
                st.success("Skills reported as already covered.")
            else:
                st.info("Recommended learning stage.")

            st.markdown("#### Topics to Learn")

            for topic in stage.get("topics", []):
                st.write(f"• {topic}")

            missing_skills = stage.get("missing_skills", [])

            if missing_skills:
                st.markdown("#### Skills to Develop")
                st.write(", ".join(missing_skills))

            prerequisites = stage.get(
                "prerequisites",
                stage.get("prerequisite", [])
            )

            if isinstance(prerequisites, str):
                prerequisites = [prerequisites]

            if prerequisites:
                st.markdown("#### Prerequisites")
                st.write(", ".join(prerequisites))

            st.markdown("#### 📺 YouTube Learning Resources")

            # Search only when requested, reducing API quota usage.
            if st.button(
                "Find YouTube Tutorials",
                key=f"videos_{career}_{index}"
            ):
                topics = stage.get("topics", [])

                focus = (
                    ", ".join(missing_skills)
                    if missing_skills
                    else ", ".join(topics[:2])
                )

                query = (
                    f"{career} {focus} "
                    "Python tutorial course"
                )

                with st.spinner("Finding learning resources..."):
                    videos = search_youtube(
                        query,
                        max_results=3
                    )

                st.session_state[
                    f"resources_{career}_{index}"
                ] = videos

            videos = st.session_state.get(
                f"resources_{career}_{index}",
                None
            )

            if videos is not None:

                if videos:
                    for video in videos:

                        st.markdown(
                            f"**{video['title']}**"
                        )

                        st.caption(
                            f"Channel: {video['channel']}"
                        )

                        st.link_button(
                            "Watch on YouTube",
                            video["url"]
                        )

                else:
                    st.warning(
                        "No videos found or the API request failed."
                    )


# ==========================================
# STUDENT PROFILE
# ==========================================

st.header("👩‍🎓 Student Profile")

with st.form("student_profile_form"):

    name = st.text_input("Enter your name")

    col1, col2 = st.columns(2)

    with col1:

        stream = st.selectbox(
            "Academic Stream",
            [
                "CSE", "IT", "ECE", "EEE",
                "Mechanical", "Civil",
                "Commerce", "BBA", "Other"
            ]
        )

        technical_skills = st.multiselect(
            "Technical Skills",
            [
                "Python", "Java", "C++", "SQL",
                "HTML/CSS", "JavaScript",
                "React", "Node.js", "Data Analysis",
                "Excel", "Statistics",
                "Linear Algebra", "Machine Learning",
                "Deep Learning", "Data Visualization",
                "Data Structures", "Algorithms",
                "Networking", "Linux",
                "Cybersecurity", "Security Fundamentals"
            ]
        )

    with col2:

        academic_level = st.selectbox(
            "Current Academic Level",
            [
                "School", "Diploma",
                "Undergraduate",
                "Postgraduate", "Other"
            ]
        )

        soft_skills = st.multiselect(
            "Soft Skills",
            [
                "Communication", "Problem Solving",
                "Teamwork", "Leadership",
                "Creativity", "Time Management"
            ]
        )

    interests = st.multiselect(
        "Fields of Interest",
        [
            "Data Science", "AI/ML",
            "Software Development",
            "Cybersecurity", "Design",
            "Marketing", "Management"
        ]
    )

    submitted = st.form_submit_button(
        "🚀 Generate Career Recommendations",
        use_container_width=True
    )


# ==========================================
# GENERATE RECOMMENDATIONS
# ==========================================

if submitted:

    if not name.strip():
        st.warning("Please enter your name.")

    elif not technical_skills and not soft_skills and not interests:
        st.warning(
            "Please select at least one skill or interest."
        )

    else:

        profile = {
            "Skill": technical_skills,
            "SoftSkill": soft_skills,
            "Interest": interests,
            "Stream": [stream]
        }

        with st.spinner("Analyzing your semantic network profile..."):

            recommendations = recommend_careers(
                profile,
                top_n=5
            )

        st.session_state["recommendations"] = recommendations
        st.session_state["student_skills"] = technical_skills
        st.session_state["student_name"] = name.strip()
        st.session_state["selected_profile"] = {
            "stream": stream,
            "academic_level": academic_level,
            "technical_skills": technical_skills,
            "soft_skills": soft_skills,
            "interests": interests
        }


# ==========================================
# DISPLAY CAREER RECOMMENDATIONS
# ==========================================

if "recommendations" in st.session_state:

    recommendations = st.session_state["recommendations"]
    student_skills = st.session_state["student_skills"]
    student_name = st.session_state["student_name"]

    st.divider()

    st.success(
        f"Career analysis completed for {student_name}!"
    )

    st.header("🎯 Top Career Recommendations")

    if recommendations:

        st.caption(
            "Scores represent relative semantic-network ranking "
            "values, not probabilities or guaranteed career suitability."
        )

        for index, result in enumerate(recommendations, start=1):

            with st.container(border=True):

                col1, col2 = st.columns([3, 1])

                with col1:

                    st.subheader(
                        f"{index}. {result['career']}"
                    )

                    matched = result.get(
                        "matched_features", []
                    )

                    st.write(
                        "**Matched Features:** "
                        + (
                            ", ".join(matched)
                            if matched else "None"
                        )
                    )

                with col2:

                    st.metric(
                        "Ranking Score",
                        f"{result['score']:.4f}"
                    )

        st.divider()

        # ==========================================
        # SELECT CAREER
        # ==========================================

        st.header("🔍 Explore a Career")

        career_names = [
            result["career"]
            for result in recommendations
        ]

        selected_career = st.selectbox(
            "Select a recommended career",
            career_names
        )

        st.subheader(
            f"Selected Career: {selected_career}"
        )

        # ==========================================
        # SKILL GAP ANALYSIS
        # ==========================================

        st.header("📊 Skill Gap Analysis")

        gap = analyze_skill_gap(
            selected_career,
            student_skills
        )

        if gap is None:

            st.info(
                "Detailed skill requirements are not yet "
                "available for this career."
            )

        else:

            st.metric(
                "Required Skills Covered",
                f"{gap['coverage']:.1f}%"
            )

            st.progress(
                min(max(gap["coverage"] / 100, 0.0), 1.0)
            )

            st.caption(
                "Coverage is based on a curated skill checklist, "
                "not a verified assessment of proficiency."
            )

            col1, col2 = st.columns(2)

            with col1:

                st.markdown("#### ✅ Existing Skills")

                if gap["matched"]:
                    for skill in gap["matched"]:
                        st.write(f"• {skill}")
                else:
                    st.write("No required skills matched yet.")

            with col2:

                st.markdown("#### 📚 Missing Skills")

                if gap["missing"]:
                    for skill in gap["missing"]:
                        st.write(f"• {skill}")
                else:
                    st.success(
                        "All listed required skills are covered!"
                    )

        st.divider()

        # ==========================================
        # PERSONALIZED ROADMAP
        # ==========================================

        display_roadmap(
            selected_career,
            student_skills
        )

    else:

        st.warning(
            "No matching careers were found. "
            "Try selecting different skills or interests."
        )


# ==========================================
# FOOTER
# ==========================================

st.divider()

st.caption(
    "Career Guidance AI | Semantic Networks | "
    "Skill Gap Analysis | Personalized Learning | YouTube API"
)
