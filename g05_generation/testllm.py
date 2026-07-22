from g05_generation.g05_01_prompt_builder import build_prompt
from g05_generation.g05_02_llm import generate_answer


def main():

    results = [
        {
            "sog_id": "7.8",
            "title": "Confined Space Rescue",
            "section": "Scene Safety",
            "text": "Establish hot, warm and cold zones. Ensure unauthorized personnel do not enter the confined space."
        }
    ]

    question = "A worker is trapped inside a manhole. What should firefighters do?"

    prompt = build_prompt(question, results)

    print(prompt)   # Just to see the generated prompt

    answer = generate_answer(prompt)

    print("\nGenerated Answer:\n")
    print(answer)


if __name__ == "__main__":
    main()