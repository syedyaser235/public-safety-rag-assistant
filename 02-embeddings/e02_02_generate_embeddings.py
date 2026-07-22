import json
from pathlib import Path

from e02_01_embeddingmodel import get_embedding

PROJECT_ROOT = Path(__file__).resolve().parent.parent

chunk_dir = (PROJECT_ROOT / "data" / "chunks" / "fire_sop_chunks.json")

output_file = (PROJECT_ROOT / "data" / "chunks" / "fire_sop_embeddings.json")

def load_chunks(file_path: Path) -> list[dict]:
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
    
def generate_embeddings(chunks: list[dict]) -> list[dict]:

    embedded_chunks = []

    for chunk in chunks:

        embedding = get_embedding(chunk["text"])

        chunk["embedding"] = embedding.tolist()

        embedded_chunks.append(chunk)

    return embedded_chunks

def save_embeddings(chunks: list[dict], output_path: Path):

    with open(output_path, "w", encoding="utf-8") as f:

        json.dump(
            chunks,
            f,
            indent=4,
            ensure_ascii=False
        )

def main():

    chunks = load_chunks(chunk_dir)

    embedded_chunks = generate_embeddings(chunks)

    save_embeddings(
        embedded_chunks,
        output_file
    )

    print(f"Generated embeddings for {len(embedded_chunks)} chunks.")

if __name__ == "__main__":
    main()
    