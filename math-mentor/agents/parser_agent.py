import os
import json
from openai import OpenAI


def parse_problem(text: str) -> dict:
    """
    Parses raw math problem text into structured JSON.
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    prompt = f"""
You are a math problem parser.

Given the following input, extract structured information.

Problem:
{text}

Return STRICT JSON with fields:
- problem_text
- topic (algebra, calculus, probability, linear_algebra, or other)
- variables (list)
- constraints (list)
- needs_clarification (true/false)
- is_in_scope (true/false)
- reason_if_out_of_scope (string)

Do not add explanations. Return JSON only.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return json.loads(response.choices[0].message.content)
