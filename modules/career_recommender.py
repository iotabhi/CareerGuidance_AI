
import networkx as nx
from pathlib import Path


# ==========================================
# LOAD DIRECTED SEMANTIC NETWORK
# ==========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

GRAPH_FILE = PROJECT_ROOT / "data" / "semantic_network.gexf"

G = nx.read_gexf(GRAPH_FILE)


# ==========================================
# RECOMMENDATION CATEGORY WEIGHTS
# ==========================================

CATEGORY_WEIGHTS = {
    "Skill": 0.35,
    "SoftSkill": 0.15,
    "Interest": 0.30,
    "Stream": 0.20,
    "Subject": 0.30,
    "CareerArea": 0.30
}


# ==========================================
# TEXT NORMALIZATION
# ==========================================

def normalize(value):
    return str(value).strip().casefold()


# ==========================================
# CREATE NODE LOOKUP DICTIONARY
# ==========================================

node_lookup = {}

for node, data in G.nodes(data=True):

    category = data.get("category", "")
    label = data.get("label", "")

    key = (normalize(category), normalize(label))

    node_lookup[key] = node


# ==========================================
# CAREER RECOMMENDATION FUNCTION
# ==========================================

def recommend_careers(profile, top_n=5):

    scores = {}
    matched_features = {}

    for category, features in profile.items():

        feature_weight = CATEGORY_WEIGHTS.get(category, 0)

        if feature_weight == 0:
            continue

        for feature in features:

            key = (normalize(category), normalize(feature))

            node = node_lookup.get(key)

            if node is None:
                continue

            # Find outgoing relationships
            connections = list(
                G.out_edges(node, data=True)
            )

            total_weight = sum(
                float(data.get("weight", 1))
                for _, _, data in connections
            )

            if total_weight == 0:
                continue

            # Calculate career contributions
            for _, target, data in connections:

                target_data = G.nodes[target]

                target_category = target_data.get("category")

                if target_category not in ["Career", "JobRole"]:
                    continue

                career = target_data.get("label", target)

                edge_weight = float(
                    data.get("weight", 1)
                )

                probability = edge_weight / total_weight

                contribution = probability * feature_weight

                scores[career] = (
                    scores.get(career, 0) + contribution
                )

                matched_features.setdefault(career, [])

                matched_features[career].append(feature)

    # Sort recommendations
    results = []

    for career, score in scores.items():

        results.append({
            "career": career,
            "score": round(score, 4),
            "matched_features": sorted(
                set(matched_features[career])
            )
        })

    results.sort(
        key=lambda item: item["score"],
        reverse=True
    )

    return results[:top_n]


# ==========================================
# TEST WITH SAMPLE STUDENT PROFILE
# ==========================================

if __name__ == "__main__":

    student_profile = {

        "Skill": [
            "Python",
            "SQL"
        ],

        "SoftSkill": [
            "Problem Solving"
        ],

        "Interest": [
            "Data Science"
        ],

        "Stream": [
            "IT"
        ]
    }

    print("\n========== CAREER RECOMMENDATIONS ==========")

    recommendations = recommend_careers(
        student_profile,
        top_n=5
    )

    if recommendations:

        for index, result in enumerate(recommendations, 1):

            print(f"\n{index}. {result['career']}")
            print("Score:", result["score"])
            print("Matched features:", result["matched_features"])

    else:
        print("No matching careers found.")
