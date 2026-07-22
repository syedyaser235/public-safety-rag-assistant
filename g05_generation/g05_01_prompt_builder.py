"""
Prompt Builder

This module builds the prompt that will be sent to the LLM.
"""


def build_context(results):
    """
    Converts retrieved SOP chunks into a formatted context string.

    Args:
        results (list): List of retrieved SOP chunks.

    Returns:
        str: Formatted SOP context.
    """

    context = ""

    for result in results:
        context += (
            f"SOG: {result['sog_id']}\n"
            f"Title: {result['title']}\n"
            f"Section: {result['section']}\n\n"
            f"{result['text']}\n\n"
            + "=" * 60
            + "\n\n"
        )

    return context


def build_prompt(question, results):
    """
    Builds the final prompt that will be sent to the LLM.

    Args:
        question (str): User's question.
        results (list): Retrieved SOP chunks.

    Returns:
        str: Final prompt.
    """

    context = build_context(results)

    prompt = f"""
You are an AI Operational Assistant for Firefighters.

Your responsibility is to answer the user's question using ONLY the provided Fire Department Standard Operating Guidelines (SOGs).

Instructions:
- Use ONLY the provided SOP information.
- Do NOT invent or assume any information.
- If the answer cannot be found in the SOPs, reply:
  "The provided SOPs do not contain enough information to answer this question."
- Summarize the SOPs into clear, concise action guidance.
- If multiple SOP sections are relevant, combine them into one coherent answer.
- Maintain a professional and operational tone.
- Do not mention chunk numbers or internal processing.

==========================
REFERENCE SOPS
==========================

{context}

==========================
USER QUESTION
==========================

{question}

==========================
ANSWER
==========================
"""

    return prompt