import os
from openai import OpenAI


def explain_solution(problem: str, solution: str) -> str:
    """
    Generates a student-friendly explanation.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""
You are a math tutor explaining solutions to students.

Problem:
{problem}

Solution:
{solution}

Explain the solution step-by-step in simple language.
Avoid jargon where possible.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content
