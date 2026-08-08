import json
import networkx as nx
from pathlib import Path
from ollama import chat

GRAPH_FILE = Path("graph/knowledge_graph.json")
LLM_MODEL = "llama3.2:3b"

def load_graph():
    with open(GRAPH_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return nx.node_link_graph(data)

def get_graph_context(G, question, max_nodes=12):
    """Build a clear text description of the relevant part of the graph."""
    question_lower = question.lower()

    # Find nodes that appear in the question
    matched = []
    for node in G.nodes():
        if node.lower() in question_lower or any(
            word in node.lower() for word in question_lower.split() if len(word) > 4
        ):
            matched.append(node)

    if not matched:
        matched = list(G.nodes())[:max_nodes]

    # Collect relations involving these nodes
    lines = []
    seen = set()
    for node in matched:
        lines.append(f"Concept: {node}")
        for neighbor in G.neighbors(node):
            edge_data = G.get_edge_data(node, neighbor) or {}
            relation = edge_data.get("relation", "related_to")
            key = tuple(sorted([node, neighbor])) + (relation,)
            if key not in seen:
                lines.append(f"  - {node} --[{relation}]--> {neighbor}")
                seen.add(key)

    return "\n".join(lines)

def answer_question(question: str):
    G = load_graph()
    print(f"Graph loaded: {G.number_of_nodes()} nodes, {G.number_of_edges()} edges")

    context = get_graph_context(G, question)
    print("\nRelevant graph context used:")
    print(context)
    print()

    prompt = f"""You are a precise knowledge-graph assistant.
Answer the question using ONLY the relationships shown below.
Be direct and clear. Prefer short, factual answers.
If the exact answer is present in the relations, state it clearly.

Knowledge Graph Relations:
{context}

Question: {question}

Answer:"""

    response = chat(model=LLM_MODEL, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]

if __name__ == "__main__":
    print("=== Local GraphRAG Query Engine ===")
    print("Type your question (or 'quit' to exit)\n")

    while True:
        question = input("You: ").strip()
        if question.lower() in ["quit", "exit", "q"]:
            break
        if not question:
            continue

        print("\nThinking...")
        answer = answer_question(question)
        print(f"\nAnswer:\n{answer}\n")
        print("-" * 50)