import json
from pathlib import Path

import faiss
import numpy as np
from e02_embeddings.e02_01_embeddingmodel import get_embedding

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INDEX_FILE = (
    PROJECT_ROOT /
    "v03_vector_store" /
    "faiss_index.bin"
)

METADATA_FILE = (
    PROJECT_ROOT /
    "v03_vector_store" /
    "metadata.json"
)

def load_index():

    index = faiss.read_index(str(INDEX_FILE))

    with open(METADATA_FILE, "r", encoding="utf-8") as f:

        metadata = json.load(f)

    return index, metadata

def embed_query(query):

    embedding = get_embedding(query)

    return np.array(
        [embedding],
        dtype=np.float32
    )

def search(index, metadata, query, top_k=3):

    query_embedding = embed_query(query)

    scores, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for score, idx in zip(scores[0], indices[0]):

        result = metadata[idx].copy()

        result["score"] = float(score)

        results.append(result)

    return results

def display_results(results):

    print("\nTop Results\n")

    for i, result in enumerate(results, start=1):

        print("=" * 60)

        print(f"Result {i}")

        print(f"Similarity : {result['score']:.4f}")

        print(f"SOG        : {result['sog_id']}")

        print(f"Title      : {result['title']}")

        print(f"Section    : {result['section']}")

        print()

        print(result["text"])

        print()


def main():

    index, metadata = load_index()

    query = input("Enter your question: ")

    results = search(
        index,
        metadata,
        query,
        top_k=3
    )

    display_results(results)


if __name__ == "__main__":
    main()