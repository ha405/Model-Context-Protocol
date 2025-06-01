# embeddings.py
import numpy as np
from numpy.linalg import norm
from sentence_transformers import SentenceTransformer
from retriever import Retriever

class EmbeddingRetriever:
    def __init__(self, server_url="http://localhost:4000/rpc", chunk_size=300, overlap=50):
        self.retriever = Retriever(server_url)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.chunks = []
        self.embeddings = None
        self.chunk_size = chunk_size
        self.overlap = overlap

    def initialize(self, owner, repo, branch="main"):
        self.retriever.initialize(owner, repo, branch)

    def load_and_embed(self):
        raw_chunks = self.retriever.load_and_chunk_files(self.chunk_size, self.overlap)
        self.chunks = [rc["chunk"] for rc in raw_chunks]
        if not self.chunks:
            raise ValueError("No chunks available")
        encs = self.model.encode(self.chunks, convert_to_numpy=True)
        self.embeddings = encs / np.linalg.norm(encs, axis=1, keepdims=True)

    def retrieve_topk(self, query, k=3):
        if self.embeddings is None:
            self.load_and_embed()
        qv = self.model.encode(query, convert_to_numpy=True)
        qv = qv / norm(qv)
        sims = np.dot(self.embeddings, qv)
        idxs = np.argsort(sims)[-k:][::-1]
        return [{"chunk": self.chunks[i], "score": float(sims[i])} for i in idxs]
