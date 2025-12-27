import os
import json
from openai import OpenAI


def verify_solution(problem: str, solution: str) -> dict:
    """
    Verifies correctness and confidence of the solution.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""
You are a strict math verifier.

Problem:
{problem}

Proposed Solution:
{solution}

Return STRICT JSON:
- is_correct (true/false)
- confidence (0.0 to 1.0)
- issues (string, empty if none)
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return json.loads(response.choices[0].message.content)
