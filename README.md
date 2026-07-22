# 🚒 Public Safety RAG Assistant

An AI-powered Retrieval-Augmented Generation (RAG) application that helps firefighters and emergency responders retrieve relevant Standard Operating Guidelines (SOGs) using natural language.

Instead of manually searching lengthy SOP documents, users can simply ask a question such as:

> "A worker is trapped inside a manhole. What should firefighters do?"

The system retrieves the most relevant SOP sections using semantic search and generates a grounded response using a locally hosted Large Language Model.

---

## Features

- Semantic search using Sentence Transformers
- FAISS vector database for efficient retrieval
- Retrieval-Augmented Generation (RAG)
- Local LLM inference using Ollama
- Interactive Streamlit interface
- Response time tracking
- Displays retrieved SOP sections as references

---

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python |
| UI | Streamlit |
| Embedding Model | BAAI/bge-small-en-v1.5 |
| Vector Database | FAISS |
| LLM | Qwen 2.5 (via Ollama) |
| Document Processing | PyMuPDF |
| Data Format | JSON |

---

# Project Architecture

```
                 Fire Department SOP PDF
                           │
                           ▼
                 Data Ingestion & Cleaning
                           │
                           ▼
                     Document Chunking
                           │
                           ▼
             Sentence Transformer Embeddings
                           │
                           ▼
                    FAISS Vector Index
                           │
─────────────────────────────────────────────────────
                    User asks a question
                           │
                           ▼
                  Query Embedding Creation
                           │
                           ▼
                Semantic Similarity Search
                           │
                           ▼
              Top-K Relevant SOP Sections
                           │
                           ▼
                    Prompt Construction
                           │
                           ▼
               Qwen 2.5 (Ollama Local LLM)
                           │
                           ▼
                  Grounded AI Response
```

---

# Folder Structure

```
PUBLIC-SAFETY-RAG-ASSISTANT/

│
├── 01_data_ingestion/
├── e02_embeddings/
├── v03_vector_store/
├── r04_retrieval/
├── g05_generation/
├── services/
├── data/
├── app.py
├── test_app.py
├── requirements.txt
└── README.md
```

---

# Pipeline

### 1. Data Ingestion

- Extract Fire Department SOP pages
- Clean raw text
- Separate individual SOPs
- Save processed text

---

### 2. Chunking

Each SOP is divided into logical sections.

Each chunk stores:

- Chunk ID
- SOP Number
- Title
- Section
- Text

---

### 3. Embeddings

Each chunk is converted into a dense vector using:

```
BAAI/bge-small-en-v1.5
```

The embeddings capture semantic meaning instead of simple keyword matching.

---

### 4. Vector Database

Embeddings are indexed using **FAISS**, enabling fast semantic retrieval using cosine similarity.

---

### 5. Retrieval

When a user asks a question:

- The question is embedded.
- Similar chunks are retrieved from FAISS.
- The top matching SOP sections are selected.

---

### 6. Generation

The retrieved SOPs are combined into a prompt and passed to a locally hosted Qwen 2.5 model through Ollama.

The model is instructed to:

- Answer only using retrieved SOPs
- Avoid hallucinations
- Generate concise operational guidance

---

# Example Query

```
Vehicle fire near a school.
```

### Response

```
• Secure the incident scene.

• Prevent unauthorized personnel from entering.

• Approach the vehicle from the side.

• Cool the engine compartment.

• Disconnect the battery when safe.

• Follow HazMat procedures if required.
```

---

# Installation

Clone the repository.

```bash
git clone https://github.com/<your-username>/public-safety-rag-assistant.git

cd public-safety-rag-assistant
```

Install dependencies.

```bash
pip install -r requirements.txt
```

Install Ollama.

Download from:

https://ollama.com/

Pull the language model.

```bash
ollama pull qwen2.5:3b
```

---

# Running the Application

Start Ollama.

```bash
ollama serve
```

Launch the Streamlit interface.

```bash
streamlit run app.py
```

---

# Future Improvements

- Chat history
- Conversation memory
- Hybrid Search (Keyword + Semantic)
- Reranking
- Source citation highlighting
- Multi-document support
- Voice input
- Authentication
- Docker deployment
- Cloud deployment

---

# Learning Outcomes

This project demonstrates practical implementation of:

- Retrieval-Augmented Generation (RAG)
- Semantic Search
- Vector Databases
- Sentence Embeddings
- Prompt Engineering
- Local LLM Inference
- Streamlit Application Development

---

# License

This project is intended for educational and portfolio purposes.