import os

PROJECT_STRUCTURE = {
    "math-mentor": {
        "app.py": "",
        "requirements.txt": "",
        ".env.example": "",
        "README.md": "",
        "agents": {
            "parser_agent.py": "",
            "router_agent.py": "",
            "solver_agent.py": "",
            "verifier_agent.py": "",
            "explainer_agent.py": "",
        },
        "rag": {
            "kb_docs": {},
            "build_index.py": "",
            "retriever.py": "",
        },
        "multimodal": {
            "ocr.py": "",
            "asr.py": "",
        },
        "memory": {
            "memory_store.py": "",
            "memory.json": "{}",
        },
        "utils": {
            "confidence.py": "",
            "math_tools.py": "",
        },
        "diagrams": {
            "architecture.mmd": "",
        },
    }
}


def create_structure(base_path, structure):
    for name, content in structure.items():
        path = os.path.join(base_path, name)

        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        else:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                f.write(content)


if __name__ == "__main__":
    create_structure(".", PROJECT_STRUCTURE)
    print("✅ math-mentor project structure created successfully!")
