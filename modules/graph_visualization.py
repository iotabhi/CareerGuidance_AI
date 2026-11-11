
import networkx as nx
from pyvis.network import Network

# Load directed semantic network
G = nx.read_gexf("data/semantic_network.gexf")

# Calculate fixed node positions
pos = nx.spring_layout(
    G,
    seed=42,
    k=1.5,
    iterations=300
)

# Create Pyvis network
net = Network(
    height="800px",
    width="100%",
    directed=True,
    bgcolor="#ffffff",
    font_color="#222222"
)

# Node colors
colors = {
    "Skill": "#3498db",
    "SoftSkill": "#1abc9c",
    "Interest": "#9b59b6",
    "Career": "#2ecc71",
    "Stream": "#e67e22",
    "Subject": "#f1c40f",
    "JobRole": "#e74c3c",
    "CareerArea": "#34495e"
}

# Add nodes with fixed positions
for node, data in G.nodes(data=True):

    label = data.get("label", node)
    category = data.get("category", "Unknown")

    x = float(pos[node][0]) * 1200
    y = float(pos[node][1]) * 1200

    net.add_node(
        node,
        label=label,
        title=f"Name: {label}\nCategory: {category}",
        color=colors.get(category, "#95a5a6"),
        size=20,
        x=x,
        y=y,
        physics=False
    )


# Add edges
for source, target, data in G.edges(data=True):

    weight = int(data.get("weight", 1))

    net.add_edge(
        source,
        target,
        arrows="to",
        width=0.8,
        color="#999999",
        title=f"Association count: {weight}"
    )


# Disable physics completely
net.set_options("""
{
  "physics": {
    "enabled": false
  },
  "interaction": {
    "hover": true,
    "navigationButtons": true,
    "zoomView": true,
    "dragNodes": true
  },
  "edges": {
    "smooth": false,
    "arrows": {
      "to": {
        "enabled": true,
        "scaleFactor": 0.5
      }
    }
  },
  "nodes": {
    "font": {
      "size": 16,
      "face": "Arial"
    },
    "borderWidth": 2
  }
}
""")

# Save visualization
net.write_html("assets/semantic_network.html")

print("Stable semantic network generated!")
print("Nodes:", G.number_of_nodes())
print("Edges:", G.number_of_edges())
