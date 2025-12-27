from openai import OpenAI
import json
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def parse_problem(raw_text: str):
    prompt = f"""
You are a strict parser for a JEE-level MATH mentor.

Tasks:
1. Clean the problem text
2. Identify if the problem is IN-SCOPE (math only)
   Allowed topics:
   - algebra
   - probability
   - calculus
   - linear_algebra
3. Extract variables and constraints if present
4. Detect ambiguity or missing information

Return ONLY valid JSON in the following format:

{{
  "problem_text": "...",
  "topic": "...",
  "variables": [],
  "constraints": [],
  "needs_clarification": true/false,
  "is_in_scope": true/false,
  "reason_if_out_of_scope": ""
}}

Problem:
\"\"\"{raw_text}\"\"\"
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return json.loads(response.choices[0].message.content)
