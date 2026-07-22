import json
from pathlib import Path

import faiss
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parent.parent

EMBEDDINGS_FILE = (PROJECT_ROOT / "data" / "chunks" / "fire_sop_embeddings.json")

INDEX_DIR = PROJECT_ROOT / "v03_vector_store"

INDEX_FILE = INDEX_DIR / "faiss_index.bin"

METADATA_FILE = INDEX_DIR / "metadata.json"

def load_embeddings(file_path: Path) -> list[dict]:
    "Load embedded chunks from a JSON file."
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def build_embedding_matrix(chunks):
    """
    Convert embeddings into a NumPy matrix and
    separate metadata.
    """

    embeddings = []

    metadata = []

    for chunk in chunks:

        embeddings.append(chunk["embedding"])

        metadata.append(
            {
                "chunk_id": chunk["chunk_id"],
                "sog_id": chunk["sog_id"],
                "title": chunk["title"],
                "section": chunk["section"],
                "text": chunk["text"]
            }
        )

    embedding_matrix = np.array(
        embeddings,
        dtype=np.float32
    )

    return embedding_matrix, metadata

def create_index(embedding_matrix):
    """
    Build a FAISS index.
    """

    dimension = embedding_matrix.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embedding_matrix)

    return index

def save_index(index, metadata):
    """
    Save the FAISS index and metadata.
    """

    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    faiss.write_index(
        index,
        str(INDEX_FILE)
    )

    with open(METADATA_FILE, "w", encoding="utf-8") as f:

        json.dump(
            metadata,
            f,
            indent=4,
            ensure_ascii=False
        )


def load_index():
    """
    Load the FAISS index and metadata from disk.
    """

    index = faiss.read_index(str(INDEX_FILE))

    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    return index, metadata

def main():
    # Step 1: Load the embedded chunks
    chunks = load_embeddings(EMBEDDINGS_FILE)
    # Step 2: Build the embedding matrix and metadata
    embedding_matrix, metadata = build_embedding_matrix(chunks)
    # Step 3: Create the FAISS index
    index = create_index(embedding_matrix)
    # Step 4: Save the index and metadata
    save_index(index, metadata)

    print(f"Successfully indexed {len(metadata)} chunks.")

    print(f"FAISS index saved to: {INDEX_FILE}")

if __name__ == "__main__":
    main()
