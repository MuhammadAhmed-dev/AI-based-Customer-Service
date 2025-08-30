from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-mpnet-base-v2")

def get_embeddings(texts):
    return model.encode(texts, convert_to_tensor=True)

def get_model_dimension():
    return model.get_sentence_embedding_dimension()