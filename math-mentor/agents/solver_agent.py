import os
from openai import OpenAI


def solve_problem(parsed: dict, context_docs: list) -> str:
    """
    Solves the math problem using retrieved context.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    context_text = "\n\n".join(
        doc.page_content for doc in context_docs
    ) if context_docs else "No external context available."

    prompt = f"""
You are a JEE-level math solver.

Problem:
{parsed['problem_text']}

Relevant Knowledge:
{context_text}

Solve the problem step-by-step.
Be mathematically correct and concise.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    return response.choices[0].message.content
