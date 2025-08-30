# utils/semantic_cache.py
from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer("all-MiniLM-L6-v2")

cache = []  # List of dicts: { "question": str, "embedding": np.array, "answer": str }

def get_embedding(text):
    return model.encode([text])[0]

def cosine_sim(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def get_cached_answer(new_question, threshold=0.9):
    new_embedding = get_embedding(new_question)
    for entry in cache:
        sim = cosine_sim(entry["embedding"], new_embedding)
        if sim >= threshold:
            return entry["answer"]
    return None

def store_answer(question, answer):
    cache.append({
        "question": question,
        "embedding": get_embedding(question),
        "answer": answer
    })
