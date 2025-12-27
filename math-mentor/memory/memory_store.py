import json
import os
import uuid
from datetime import datetime

MEMORY_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "memory.json"
)

def load_memory():
    if not os.path.exists(MEMORY_PATH):
        return []

    with open(MEMORY_PATH, "r") as f:
        try:
            data = json.load(f)
            # Defensive: ensure memory is always a list
            if isinstance(data, list):
                return data
            else:
                return []
        except json.JSONDecodeError:
            return []

def save_memory(memory):
    with open(MEMORY_PATH, "w") as f:
        json.dump(memory, f, indent=2)

def add_memory(entry):
    memory = load_memory()

    entry["id"] = str(uuid.uuid4())
    entry["timestamp"] = datetime.now().isoformat()

    memory.append(entry)
    save_memory(memory)

def search_memory(problem_text, top_k=3):
    memory = load_memory()
    matches = []

    for m in memory:
        if problem_text.lower() in m.get("raw_input", "").lower():
            matches.append(m)

    return matches[:top_k]
