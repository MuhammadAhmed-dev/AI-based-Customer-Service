from utils.embedder import get_embeddings
from utils.llm_generator import generate_answer
from utils.semantic_cache import get_cached_answer, store_answer

def retrieve_answer(user_query, vector_store, history=[]):
    # 1. Check cache first
    cached = get_cached_answer(user_query)
    if cached:
        return cached

    # 2. Search + LLM
    query_embedding = get_embeddings([user_query])
    retrieved_chunks = vector_store.search(query_embedding, top_k=4)
    context = "\n".join(retrieved_chunks)
    answer = generate_answer(context, user_query, history)

    # 3. Store in cache
    store_answer(user_query, answer)

    return answer
