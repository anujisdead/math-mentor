from openai import OpenAI
import json

client = OpenAI()

def verify_solution(problem_text, solution_text):
    prompt = f"""
You are a strict math verifier.

Problem:
{problem_text}

Proposed solution:
{solution_text}

Tasks:
1. Check correctness
2. Check logical steps
3. Identify missing cases or errors
4. Rate confidence from 0 to 1

Respond ONLY in JSON:

{{
  "is_correct": true/false,
  "confidence": 0.0,
  "issues": ""
}}
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return json.loads(response.choices[0].message.content)
