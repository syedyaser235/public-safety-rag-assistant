from sentence_transformers import SentenceTransformer

modelname = "BAAI/bge-small-en-v1.5"
model = SentenceTransformer(modelname)

def get_embedding(text: str):
    """
    Generate an embedding for the given text using the specified model.

    """
    return model.encode(text, 
                        normalize_embeddings=True)

def main():
    # Example usage
    text = "This is a sample text for generating an embedding."
    embedding = get_embedding(text)
    print(f"Embedding for the text: {embedding}")

if __name__ == "__main__":
    main()