import os
import json
import networkx as nx
from pathlib import Path
from pypdf import PdfReader
from ollama import chat
from tqdm import tqdm

# ======================
# SETTINGS (edit later if needed)
# ======================
INPUT_DIR = Path("data/input")
OUTPUT_GRAPH = Path("graph/knowledge_graph.json")
LLM_MODEL = "llama3.2:3b"
CHUNK_SIZE = 800          # characters
CHUNK_OVERLAP = 100

# ======================
# HELPER FUNCTIONS
# ======================
def load_documents(folder: Path):
    """Load all .txt and .pdf files from the input folder."""
    docs = []
    for file in folder.glob("*"):
        if file.suffix.lower() == ".txt":
            text = file.read_text(encoding="utf-8", errors="ignore")
            docs.append({"name": file.name, "text": text})
        elif file.suffix.lower() == ".pdf":
            reader = PdfReader(str(file))
            text = "\n".join([page.extract_text() or "" for page in reader.pages])
            docs.append({"name": file.name, "text": text})
    return docs

def chunk_text(text: str, size: int = CHUNK_SIZE, overlap: int = CHUNK_OVERLAP):
    """Split text into overlapping chunks."""
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap
    return chunks

def extract_entities_relations(chunk: str):
    """Ask the local LLM to extract entities and relations from a chunk."""
    prompt = f"""You are an expert knowledge graph extractor.
From the text below, extract important entities and the relationships between them.

Rules:
- Entities should be specific concepts, techniques, tools, or fields (e.g. "Deep Learning", "Ollama", "GraphRAG")
- Relationships should be clear and meaningful (e.g. "is_a_subset_of", "uses", "built_using", "improves_upon", "inspired_by")
- Only extract what is clearly stated or strongly implied
- Return ONLY valid JSON, nothing else

Format:
{{
  "entities": ["Entity1", "Entity2", "Entity3"],
  "relations": [
    {{"source": "Entity1", "relation": "is_a_subset_of", "target": "Entity2"}},
    {{"source": "Entity3", "relation": "uses", "target": "Entity1"}}
  ]
}}

Text:
{chunk}
"""
    try:
        response = chat(model=LLM_MODEL, messages=[{"role": "user", "content": prompt}])
        content = response["message"]["content"].strip()
        # Clean possible markdown
        if content.startswith("```"):
            content = content.split("```")[1]
            if content.startswith("json"):
                content = content[4:]
        return json.loads(content)
    except Exception as e:
        print(f"  [skip] LLM error: {e}")
        return {"entities": [], "relations": []}

# ======================
# MAIN BUILD PROCESS
# ======================
def build_graph():
    print("Loading documents...")
    docs = load_documents(INPUT_DIR)
    if not docs:
        print("No documents found in data/input/")
        print("Please put some .txt or .pdf files there and run again.")
        return

    G = nx.Graph()

    for doc in docs:
        print(f"\nProcessing: {doc['name']}")
        chunks = chunk_text(doc["text"])
        print(f"  → {len(chunks)} chunks")

        for chunk in tqdm(chunks, desc="  Extracting"):
            result = extract_entities_relations(chunk)

            # Add entities as nodes
            for ent in result.get("entities", []):
                if ent and isinstance(ent, str):
                    G.add_node(ent.strip(), source=doc["name"])

            # Add relations as edges
            for rel in result.get("relations", []):
                src = rel.get("source", "").strip()
                tgt = rel.get("target", "").strip()
                relation = rel.get("relation", "related_to").strip()
                if src and tgt:
                    G.add_edge(src, tgt, relation=relation, source=doc["name"])

    # Save graph
    OUTPUT_GRAPH.parent.mkdir(exist_ok=True)
    data = nx.node_link_data(G)
    with open(OUTPUT_GRAPH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    print(f"\nDone! Graph saved to {OUTPUT_GRAPH}")
    print(f"Nodes: {G.number_of_nodes()} | Edges: {G.number_of_edges()}")

if __name__ == "__main__":
    build_graph()