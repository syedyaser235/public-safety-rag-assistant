# 🔥 Public Safety RAG Assistant

A Retrieval-Augmented Generation (RAG) application that enables intelligent question answering over Fire Department Standard Operating Guidelines (SOGs).

The system preprocesses Fire SOP documents, converts them into semantic chunks, generates vector embeddings, stores them in a vector database, and retrieves the most relevant procedures to answer user queries accurately.

> **Current Status:** 🚧 In Development

---

# Project Goals

- Parse Fire Department SOP manuals.
- Extract and clean SOP content.
- Split documents into meaningful semantic sections.
- Generate vector embeddings for each section.
- Store embeddings in a vector database.
- Retrieve relevant SOPs based on user questions.
- Provide context-aware responses using an LLM.

---

# Current Features

✅ Extract selected pages from a Fire SOP PDF

✅ Clean and normalize extracted text

✅ Split the manual into individual SOP documents

✅ Structure-aware chunking (section-based)

✅ Generate metadata-rich chunks

✅ Export chunks to JSON

---

# Project Structure

```text
Fire-SOP-RAG/
│
├── data/
│   ├── Safety-SOGs.pdf
│   ├── processed/
│   │    ├── vehicle_fires.txt
│   │    ├── vehicle_accidents.txt
│   │    └── ...
│   │
│   └── chunks/
│        └── fire_sop_chunks.json
│
├── data_ingestion/
│   ├── preprocessFireSop.py
│   └── chunking.py
│
├── embeddings/
│
├── retrieval/
│
├── app.py
│
├── requirements.txt
│
└── README.md
```

---

# Data Processing Pipeline

```text
Safety-SOGs.pdf
        │
        ▼
Extract Selected Pages
        │
        ▼
Extract Text
        │
        ▼
Clean Text
        │
        ▼
Split into Individual SOPs
        │
        ▼
Extract Metadata
        │
        ▼
Split into Logical Sections
        │
        ▼
Create Semantic Chunks
        │
        ▼
fire_sop_chunks.json
        │
        ▼
Generate Embeddings
        │
        ▼
Vector Database
        │
        ▼
Retriever
        │
        ▼
LLM Response
```

---

# Chunking Strategy

Instead of splitting documents into fixed-size chunks, this project uses **structure-aware chunking**.

Each SOP is divided into its logical operational sections such as:

- Introduction
- Definitions
- Arrival on Scene
- Scene Safety
- Incident Actions
- Reports and Documentation
- Clean-Up

This preserves procedural context and produces much more meaningful retrieval results compared to arbitrary text splitting.

Example:

```json
{
    "chunk_id": "7.2_2",
    "sog_id": "7.2",
    "title": "Vehicle Fires",
    "section": "Scene Safety",
    "text": "Ensure that unauthorized personnel do not enter the hazardous area..."
}
```

---

# Why Structure-Aware Chunking?

Fire SOPs are procedural documents.

If fixed-size chunking were used, important operational procedures could be split across multiple chunks, resulting in incomplete retrieval.

Using section-based chunking provides:

- Better semantic retrieval
- Clearer context
- Smaller search space
- Easier citation of source procedures
- More accurate LLM responses

---

# Current Modules

## preprocessFireSop.py

Responsible for:

- Extracting relevant PDF pages
- Text extraction
- Text cleaning
- Splitting the manual into individual SOP files

---

## chunking.py

Responsible for:

- Loading SOP files
- Reading SOP content
- Extracting metadata
- Splitting SOPs into logical sections
- Creating semantic chunks
- Exporting chunks to JSON

---

# Sample Chunk

```json
{
    "chunk_id": "7.6_4",
    "sog_id": "7.6",
    "title": "Natural Gas Incidents",
    "section": "Incidents with an Explosion - Incident Actions",
    "text": "Units arriving on scene of an explosion must consider natural gas as a possible cause..."
}
```

---

# Technologies

- Python
- Pymupdf (Fitz)
- Regular Expressions (Regex)
- JSON
- pathlib

**Planned**

- Sentence Transformers
- FAISS / ChromaDB
- LangChain
- OpenAI / Local LLM
- Streamlit / FastAPI

---

# Future Work

- Generate sentence embeddings
- Build vector database
- Implement similarity search
- Add metadata filtering
- Build conversational RAG pipeline
- Add citations in responses
- Web interface
- Evaluation pipeline
- Hybrid Retrieval (Keyword + Vector Search)

---

# Getting Started

Clone the repository

```bash
git clone https://github.com/<your-username>/Fire-SOP-RAG.git
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run preprocessing

```bash
python data_ingestion/preprocessFireSop.py
```

Generate chunks

```bash
python data_ingestion/chunking.py
```

---

# Example Use Cases

- "How should firefighters respond to a carbon monoxide incident?"

- "What PPE is required during a natural gas leak?"

- "What are the scene safety procedures for vehicle fires?"

- "What should be done first at a trench rescue?"

---

# Project Status

| Module | Status |
|---------|--------|
| PDF Extraction | ✅ Complete |
| Text Cleaning | ✅ Complete |
| SOP Splitting | ✅ Complete |
| Metadata Extraction | ✅ Complete |
| Structure-aware Chunking | ✅ Complete |
| JSON Export | ✅ Complete |
| Embedding Generation | 🚧 In Progress |
| Vector Database | ⏳ Planned |
| Retrieval Pipeline | ⏳ Planned |
| LLM Integration | ⏳ Planned |
| UI | ⏳ Planned |

---

# License

This project is intended for educational and research purposes.