import faiss
import numpy as np
import os

class FaissService:
    def __init__(self, dim: int, index_path: str = './index.faiss', db_path: str = './db.faiss.npy'):
        self.index_path = index_path
        self.db_path = db_path

        if os.path.exists(self.index_path) and os.path.exists(self.db_path):
            self.index = faiss.read_index(self.index_path)
            self.vectors = np.load(self.db_path)
            print(f"Loaded {self.vectors.shape[0]} vectors from {self.db_path}")
        else:
            self.index = faiss.IndexFlatL2(dim)
            self.vectors = np.empty((0, dim), dtype='float32')
            self.save_index()

    def add_to_index(self, vectors: np.ndarray):
        self.index.add(vectors)
        self.vectors = np.vstack([self.vectors, vectors])
        self.save_index()

    def search_index(self, query_vector: np.ndarray, top_k: int = 5):
        distances, indices = self.index.search(query_vector, top_k)
        return distances, indices

    def save_index(self):
        if self.index_path:
            faiss.write_index(self.index, self.index_path)
            print(f"FAISS index saved to {self.index_path}")
        else:
            print("No index path provided, FAISS index not saved.")

        if self.db_path:
            np.save(self.db_path, self.vectors)
            print(f"Saved {self.vectors.shape[0]} vectors to {self.db_path}")
        else:
            print("No database path provided, FAISS database not saved.")
