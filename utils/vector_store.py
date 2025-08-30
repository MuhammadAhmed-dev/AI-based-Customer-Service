import faiss
import torch

class VectorStore:
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.text_chunks = []

    def add(self, embeddings, texts):
        self.index.add(embeddings.cpu().numpy())
        self.text_chunks.extend(texts)

    def search(self, query_embedding, top_k=4):
        D, I = self.index.search(query_embedding.cpu().numpy(), top_k)
        return [self.text_chunks[i] for i in I[0]]
