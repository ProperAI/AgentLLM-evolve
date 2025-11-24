from pathlib import Path

Proj = "SampleProj1"

structure = [
    "ai_eng_proj/app.py",
    "ai_eng_proj/config.yaml",
    "ai_eng_proj/rag/ingest.py",
    "ai_eng_proj/rag/retriever.py",
    "ai_eng_proj/data/notes/",
    "ai_eng_proj/artifacts/faiss_index/",
    "ai_eng_proj/artifacts/docstore.pkl",
]

for p in structure:
    path = Path(p)
    if p.endswith("/"):
        path.mkdir(parents=True, exist_ok=True)
    else:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.touch(exist_ok=True)
