
import pandas as pd
import networkx as nx

# Load cleaned datasets
df1 = pd.read_csv("data/cleaned_career_path.csv")
df2 = pd.read_csv("data/cleaned_career_roles.csv")

# Create an undirected semantic network
G = nx.DiGraph()


# Function to add nodes
def add_node(node_id, label, category):
    G.add_node(
        node_id,
        label=label,
        category=category
    )


# Function to connect two entities
def add_relationship(source, source_type,
                     target, target_type):

    source_id = f"{source_type}::{source}"
    target_id = f"{target_type}::{target}"

    add_node(source_id, source, source_type)
    add_node(target_id, target, target_type)

    if G.has_edge(source_id, target_id):
        G[source_id][target_id]["weight"] += 1
    else:
        G.add_edge(
            source_id,
            target_id,
            relation=f"{source_type}_associated_with_{target_type}",
            weight=1
        )


# Extract comma-separated values
def extract_items(value):
    if pd.isna(value):
        return []

    return [
        item.strip()
        for item in str(value).split(",")
        if item.strip()
    ]


# =====================================
# DATASET 1: Student Career Relationships
# =====================================

for _, row in df1.iterrows():

    career = str(row["Suggested_Career_Path"]).strip()

    # Technical skills
    for skill in extract_items(row["Technical_Skills"]):
        add_relationship(
            skill, "Skill",
            career, "Career"
        )

    # Soft skills
    for skill in extract_items(row["Soft_Skills"]):
        add_relationship(
            skill, "SoftSkill",
            career, "Career"
        )

    # Interests
    interest = str(row["Fields_of_Interest"]).strip()

    add_relationship(
        interest, "Interest",
        career, "Career"
    )

    # Academic stream
    stream = str(row["Stream"]).strip()

    add_relationship(
        stream, "Stream",
        career, "Career"
    )


# =====================================
# DATASET 2: Academic and Job Relationships
# =====================================

for _, row in df2.iterrows():

    job = str(row["Suggested Job Role"]).strip()

    # Interested subjects
    subject = str(row["Interested subjects"]).strip()

    add_relationship(
        subject, "Subject",
        job, "JobRole"
    )

    # Interested career areas
    area = str(row["interested career area "]).strip()

    add_relationship(
        area, "CareerArea",
        job, "JobRole"
    )


# =====================================
# DISPLAY GRAPH INFORMATION
# =====================================

print("\n========== SEMANTIC NETWORK ==========")

print("Total Nodes:", G.number_of_nodes())
print("Total Edges:", G.number_of_edges())

print("\nNode Categories:")

categories = {}

for _, data in G.nodes(data=True):
    category = data["category"]
    categories[category] = categories.get(category, 0) + 1

for category, count in categories.items():
    print(category, ":", count)


print("\nTop 10 Relationships:")

sorted_edges = sorted(
    G.edges(data=True),
    key=lambda x: x[2]["weight"],
    reverse=True
)

for source, target, data in sorted_edges[:10]:

    print(
        G.nodes[source]["label"],
        "<-->",
        G.nodes[target]["label"],
        "| Weight:",
        data["weight"]
    )


# Save graph
nx.write_gexf(G, "data/semantic_network.gexf")

print("\nSemantic network created successfully!")
