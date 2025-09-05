from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load a pre-trained model. This will be downloaded on first run.
# 'all-MiniLM-L6-v2' is a small but powerful model for this task.
try:
    model = SentenceTransformer('all-MiniLM-L6-v2')
except Exception as e:
    print(f"Error loading SentenceTransformer model: {e}")
    model = None

def find_relevant_documents(query: str, documents: dict, top_k: int = 3) -> list:
    """
    Finds the most relevant documents for a query using semantic search.
    
    Args:
        query (str): The user's meeting topic.
        documents (dict): A dictionary where keys are source names and values are the full text.
        top_k (int): The number of top documents to return.

    Returns:
        list: A list of the texts of the most relevant documents.
    """
    if not model or not documents:
        return []

    # Separate the names and the text content
    source_names = list(documents.keys())
    source_texts = list(documents.values())

    # Generate embeddings for the query and all document texts
    query_embedding = model.encode([query])
    doc_embeddings = model.encode(source_texts)

    # Calculate cosine similarity
    similarities = cosine_similarity(query_embedding, doc_embeddings)[0]

    # Get the indices of the top_k most similar documents
    top_k_indices = np.argsort(similarities)[-top_k:][::-1]

    # Return the full text of the most relevant documents
    relevant_texts = [source_texts[i] for i in top_k_indices]
    
    return relevant_texts