from r04_retrieval.r04_01_search import load_index, search
from g05_generation.g05_01_prompt_builder import build_prompt
from g05_generation.g05_02_llm import generate_answer
import time

INDEX, METADATA = load_index()

def answer_question(question):

    t0 = time.perf_counter()

    results = search(INDEX, METADATA, question)
    print(f"Search: {time.perf_counter()-t0:.2f}s")

    t1 = time.perf_counter()

    prompt = build_prompt(question, results)
    print(f"Prompt: {time.perf_counter()-t1:.2f}s")

    t2 = time.perf_counter()

    answer = generate_answer(prompt)
    print(f"Generation: {time.perf_counter()-t2:.2f}s")

    return answer, results