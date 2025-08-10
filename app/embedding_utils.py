import faiss
from sentence_transformers import SentenceTransformer

class EmbeddingStore:
    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)
        self.index = None
        self.chunks = []

    def fit(self, chunks):
        self.chunks = chunks
        emb = self.model.encode(chunks, show_progress_bar=False)
        self.index = faiss.IndexFlatL2(len(emb[0]))
        self.index.add(emb)
        self.emb = emb

    def search(self, query: str, k=3):
        query_vec = self.model.encode([query])[0]
        D, I = self.index.search(query_vec.reshape(1, -1), k)
        return [self.chunks[i] for i in I[0]], [float(d) for d in D[0]]
