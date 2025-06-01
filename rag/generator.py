# generator.py
from google import genai
from embeddings import EmbeddingRetriever
import os
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

client = genai.Client(api_key=api_key)

def generate_answer(prompt):
    resp = client.models.generate_content(model="gemini-2.0-flash", contents=[prompt])
    return resp.text.strip()

class RAGGenerator:
    def __init__(self, server_url="http://model-context-protocol-production.up.railway.app/rpc", chunk_size=300, overlap=50):
        self.retriever = EmbeddingRetriever(server_url, chunk_size, overlap)

    def initialize(self, owner, repo, branch="main"):
        self.retriever.initialize(owner, repo, branch)

    def answer_query(self, query, top_k=3):
        top = self.retriever.retrieve_topk(query, top_k)
        context = "\n\n----\n\n".join(item["chunk"] for item in top)
        prompt = (
            "You are an AI Engineer helping answer questions related to LLMs and LLM Compression (Quantization) based on the following code context.\n\n"
            f"Context (top {top_k} chunks):\n{context}\n\n"
            f"User question:\n{query}\n\n"
            "Answer:"
        )
        return generate_answer(prompt)
