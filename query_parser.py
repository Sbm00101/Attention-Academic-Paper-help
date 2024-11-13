from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

embedding_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

intents = {
    "fetch_papers": "Find and store research papers on a specific topic",
    "qna": "Answer a specific question from existing research papers",
    "future_work": "Suggest areas for future work based on reviewed papers"
}

intent_embeddings = {intent: embedding_model.encode(description) for intent, description in intents.items()}

def detect_intent(query):
    query_embedding = embedding_model.encode(query)
    similarities = {intent: cosine_similarity([query_embedding], [embedding])[0][0] for intent, embedding in intent_embeddings.items()}
    return max(similarities, key=similarities.get)
