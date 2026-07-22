from r04_retrieval.r04_01_search import load_index, search
from g05_generation.g05_01_prompt_builder import build_prompt
from g05_generation.g05_02_llm import generate_answer
import time

def main():

    print("Loading index...")
    index, metadata = load_index()

    question = input("Enter your question: ")
    start_time = time.perf_counter()
    print("Searching...")
    results = search(index, metadata, question)

    print("Building prompt...")
    prompt = build_prompt(question, results)
    print(f"Prompt length: {len(prompt)} characters")
    print("Generating answer...")
    answer = generate_answer(prompt)
    end_time = time.perf_counter()
    elapsed = end_time - start_time
    print("\n" + "=" * 80)
    print("ANSWER")
    print("=" * 80)
    print(answer)
    print(f"\nExecution Time: {elapsed:.2f} seconds")


if __name__ == "__main__":
    main()