from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def solve_problem(parsed_problem, retrieved_docs):
    context = "\n\n".join([doc.page_content for doc in retrieved_docs])

    prompt = f"""
You are a JEE-level math solver.

Problem:
{parsed_problem["problem_text"]}

Relevant knowledge:
{context}

Instructions:
- Solve step by step
- Use correct mathematical notation
- Do NOT assume missing information
- Final answer must be clearly stated

Solution:
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content
