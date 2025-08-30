from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")
print("Model loaded. Embedding dimension:", model.get_sentence_embedding_dimension())
