import json
import networkx as nx
from pathlib import Path

GRAPH_FILE = Path("graph/knowledge_graph.json")

with open(GRAPH_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

G = nx.node_link_graph(data)

print("===== NODES =====")
for node in G.nodes():
    print(f"- {node}")

print("\n===== EDGES =====")
for u, v, d in G.edges(data=True):
    relation = d.get("relation", "related_to")
    print(f"{u}  --[{relation}]-->  {v}")