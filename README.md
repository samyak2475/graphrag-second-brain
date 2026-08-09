# Local GraphRAG Second Brain

> **Fully local • Privacy-first • Knowledge Graph + Multi-hop Reasoning**  
> Turn your notes & PDFs into an intelligent knowledge graph that can answer complex questions by reasoning over relationships — not just vector similarity.

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-ff4b4b)
![NetworkX](https://img.shields.io/badge/Graph-NetworkX-orange)
![License](https://img.shields.io/badge/License-MIT-green)

---

### Why this project stands out

Most RAG systems only do **vector similarity search**.  
This project implements a **lightweight GraphRAG** pipeline that:

- Extracts entities & relationships from documents
- Builds a real **knowledge graph**
- Answers questions using **multi-hop reasoning** over the graph
- Runs **100% locally** (Ollama + small quantized models)
- Works on modest hardware (16 GB RAM + 4 GB VRAM)

Perfect for anyone who wants a private “second brain” or wants to demonstrate advanced RAG techniques without cloud costs.

---

### Features

- **Knowledge Graph Construction** – Automatic entity & relation extraction using local LLMs
- **Interactive Graph Visualization** – Beautiful, draggable, color-coded graph (PyVis)
- **Multi-hop Question Answering** – Reasons across multiple connected concepts
- **Streamlit Web UI** – Clean interface for asking questions + viewing the graph
- **Document Upload** – Add new `.txt` / `.pdf` files and expand the knowledge base
- **Fully Local & Private** – No data ever leaves your machine
- **Hardware Friendly** – Designed for laptops with limited VRAM

---

### Architecture (Simplified)
Documents (.txt / .pdf)
↓
Chunking + LLM Extraction
↓
Knowledge Graph (NetworkX)
↓
┌─────────────────────┐
│  Query Engine       │
│  (Graph Traversal   │
│   + Local LLM)      │
└─────────────────────┘
↓
Streamlit UI + Interactive Viz


---

### Tech Stack

| Component              | Technology              |
|------------------------|-------------------------|
| Local LLM & Embeddings | Ollama (`llama3.2:3b`, `nomic-embed-text`) |
| Knowledge Graph        | NetworkX                |
| Visualization          | PyVis                   |
| Web Interface          | Streamlit               |
| PDF Parsing            | pypdf                   |
| Language               | Python 3.11             |

---

### Quick Start

#### 1. Prerequisites
- Python 3.11+
- [Ollama](https://ollama.com) installed

#### 2. Pull the models
```bash
ollama pull llama3.2:3b
ollama pull nomic-embed-text
```

#### 3. Setup the project
```bash
Bashgit clone https://github.com/samyak2475/graphrag-second-brain.git
cd graphrag-second-brain

python -m venv venv
# Windows
.\venv\Scripts\activate
# macOS/Linux
source venv/bin/activate

pip install networkx ollama pypdf numpy matplotlib pyvis tqdm streamlit
```

#### 4. Run the application

streamlit run src/app.py

Usage Tips

Ask questions that require connecting concepts (best results):
“How does GraphRAG improve upon normal RAG?”
“What is the relationship between Deep Learning and Neural Networks?”
“Which technique combines Large Language Models with external knowledge?”

Click Show / Refresh Graph to explore the interactive knowledge graph.
Upload new .txt or .pdf files from the sidebar to expand your second brain.


Example Output
Question:
Which technique combines Large Language Models with external knowledge?
Answer:
Retrieval-Augmented Generation (RAG)
Graph context used: Large Language Models --[combines_with_external_knowledge]--> Retrieval-Augmented Generation (RAG)

Future Improvements

 True multi-hop path highlighting in the graph
 Community detection & topic clustering
 Hybrid Graph + Vector retrieval fallback
 Side-by-side Normal RAG vs GraphRAG comparison
 Better entity resolution & relation direction correction
 Persistent conversation memory


Why I built this
I wanted a personal knowledge system that goes beyond basic RAG — one that understands relationships between concepts and can perform multi-hop reasoning, while remaining completely private and runnable on a normal laptop.
This project demonstrates practical skills in:

Local LLM orchestration
Knowledge graph construction
Graph-based retrieval
Full-stack AI application design (backend + interactive UI)

Built with and a lot of late-night debugging.
If you find this useful, feel free to star the repo!
text---

### How to add it

1. In VS Code → right-click the root of the project → New File → `README.md`
2. Paste the entire content above
3. Save
4. Then run these commands:

```powershell
git add README.md
git commit -m "Add professional README"
git push

