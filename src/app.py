import streamlit as st
import json
import networkx as nx
from pathlib import Path
from ollama import chat
from pyvis.network import Network
import streamlit.components.v1 as components
import shutil

GRAPH_FILE = Path("graph/knowledge_graph.json")
INPUT_DIR = Path("data/input")
LLM_MODEL = "llama3.2:3b"

st.set_page_config(page_title="Local GraphRAG Second Brain", layout="wide")
st.title("Local GraphRAG Second Brain")
st.caption("Fully local • Knowledge Graph + Multi-hop Reasoning • Ollama")

@st.cache_resource
def load_graph():
    with open(GRAPH_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return nx.node_link_graph(data)

def get_graph_context(G, question):
    question_lower = question.lower()
    matched = [n for n in G.nodes() if n.lower() in question_lower or any(w in n.lower() for w in question_lower.split() if len(w) > 4)]
    if not matched:
        matched = list(G.nodes())[:10]

    lines = []
    seen = set()
    for node in matched:
        for neighbor in G.neighbors(node):
            rel = G.get_edge_data(node, neighbor).get("relation", "related_to")
            key = tuple(sorted([node, neighbor])) + (rel,)
            if key not in seen:
                lines.append(f"{node} --[{rel}]--> {neighbor}")
                seen.add(key)
    return "\n".join(lines) if lines else "No direct relations found."

def ask(question, G):
    context = get_graph_context(G, question)
    prompt = f"""You are a precise knowledge-graph assistant.
Answer using ONLY the relations below. Be short and factual.

Relations:
{context}

Question: {question}

Answer:"""
    response = chat(model=LLM_MODEL, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"], context

def create_interactive_graph(G):
    net = Network(height="650px", width="100%", bgcolor="#0e1117", font_color="white", directed=False)
    net.set_options("""
    {
      "nodes": {
        "font": {"size": 18, "face": "arial", "color": "#ffffff"},
        "scaling": {"min": 20, "max": 40},
        "borderWidth": 2
      },
      "edges": {
        "color": {"color": "#4fc3f7", "highlight": "#ff9800"},
        "font": {"size": 12, "color": "#bbbbbb", "strokeWidth": 0},
        "smooth": {"type": "continuous"}
      },
      "physics": {
        "barnesHut": {
          "gravitationalConstant": -8000,
          "centralGravity": 0.3,
          "springLength": 150
        },
        "minVelocity": 0.75
      }
    }
    """)

    colors = ["#4fc3f7", "#81c784", "#ffb74d", "#e57373", "#ba68c8", "#4db6ac"]
    for i, node in enumerate(G.nodes()):
        net.add_node(
            node,
            label=node,
            title=node,
            color=colors[i % len(colors)],
            size=28
        )

    for u, v, d in G.edges(data=True):
        rel = d.get("relation", "")
        net.add_edge(u, v, title=rel, label=rel)

    net.save_graph("viz/temp_graph.html")
    return "viz/temp_graph.html"

# ========== SIDEBAR ==========
st.sidebar.header("Graph Info")
G = load_graph()
st.sidebar.metric("Nodes", G.number_of_nodes())
st.sidebar.metric("Edges", G.number_of_edges())

st.sidebar.markdown("---")
st.sidebar.subheader("Sample Questions")
samples = [
    "What is the relationship between Deep Learning and Neural Networks?",
    "How does GraphRAG improve upon normal RAG?",
    "Which technique combines Large Language Models with external knowledge?",
    "What is Ollama used for?"
]
for s in samples:
    if st.sidebar.button(s, key=s):
        st.session_state["question"] = s

st.sidebar.markdown("---")
st.sidebar.subheader("Add Documents")
uploaded = st.sidebar.file_uploader("Upload .txt or .pdf", type=["txt", "pdf"], accept_multiple_files=True)
if uploaded:
    INPUT_DIR.mkdir(parents=True, exist_ok=True)
    for f in uploaded:
        with open(INPUT_DIR / f.name, "wb") as out:
            out.write(f.getbuffer())
    st.sidebar.success(f"Saved {len(uploaded)} file(s) to data/input/")

if st.sidebar.button("Rebuild Graph from Documents"):
    st.sidebar.warning("Rebuilding uses the automatic extractor (quality may vary with small models).")
    st.sidebar.info("Run this in terminal instead for now:\npython src/build_graph.py")

# ========== MAIN ==========
question = st.text_input(
    "Ask a question about the knowledge graph:",
    value=st.session_state.get("question", ""),
    placeholder="Type your question here..."
)

if question:
    with st.spinner("Reasoning over the graph..."):
        answer, context = ask(question, G)
    st.subheader("Answer")
    st.success(answer)
    with st.expander("Graph context used"):
        st.code(context)

st.markdown("---")
st.subheader("Interactive Knowledge Graph")

if st.button("Show / Refresh Graph", type="primary"):
    with st.spinner("Building visualization..."):
        html_path = create_interactive_graph(G)
        with open(html_path, "r", encoding="utf-8") as f:
            components.html(f.read(), height=680, scrolling=True)
else:
    st.info("Click the button above to load the interactive graph.")