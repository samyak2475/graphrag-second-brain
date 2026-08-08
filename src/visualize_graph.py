import json
import networkx as nx
from pyvis.network import Network
from pathlib import Path

GRAPH_FILE = Path("graph/knowledge_graph.json")
OUTPUT_HTML = Path("viz/knowledge_graph.html")

def visualize():
    # Load the graph
    with open(GRAPH_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    G = nx.node_link_graph(data)

    # Create interactive network
    net = Network(height="750px", width="100%", bgcolor="#1a1a1a", font_color="white")
    net.barnes_hut()

    # Add nodes and edges
    for node, attrs in G.nodes(data=True):
        net.add_node(node, label=node, title=str(attrs), color="#4fc3f7")

    for source, target, attrs in G.edges(data=True):
        relation = attrs.get("relation", "related_to")
        net.add_edge(source, target, title=relation, label=relation)

    # Save
    OUTPUT_HTML.parent.mkdir(exist_ok=True)
    net.save_graph(str(OUTPUT_HTML))
    print(f"Interactive graph saved to: {OUTPUT_HTML}")
    print("Open this file in your browser to explore the knowledge graph.")

if __name__ == "__main__":
    visualize()