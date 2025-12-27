from openai import OpenAI

client = OpenAI()

def explain_solution(problem_text, solution_text):
    prompt = f"""
You are a JEE Mathematics tutor.

Problem:
{problem_text}

Solved Answer:
{solution_text}

Explain the solution step-by-step in a clear, student-friendly manner.
Rules:
- Start from the basic idea
- Explain why each step is taken
- Avoid skipping steps
- Use simple language
- End with the final answer clearly highlighted

Explanation:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content
