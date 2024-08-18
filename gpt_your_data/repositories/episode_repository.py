import numpy as np
import torch
from sqlalchemy.orm import Session
from transformers import AutoTokenizer, AutoModel

from gpt_your_data.models.episode import Episode
from gpt_your_data.services.faiss_service import FaissService
from gpt_your_data.config.database import SessionLocal 


faiss_service = FaissService(dim=384)

class EpisodeRepository:
    def __init__(self, db: Session = None):
        self.db = db or SessionLocal() 
        self.faiss_service = faiss_service
        self.tokenizer = AutoTokenizer.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")
        self.model = AutoModel.from_pretrained("sentence-transformers/all-MiniLM-L6-v2")

    def add_episode(self, name: str, description: str) -> Episode:
        episode = Episode(name=name, description=description)

        with self.db.begin():
            self.db.add(episode)
            self.db.flush()
            self.db.refresh(episode)

            vector = self.extract_vector(episode_description=description)
            self.faiss_service.add_to_index(vector)

        return episode
    

    def extract_vector(self, episode_description: str = None) -> np.ndarray:        
        if episode_description is None:
            raise ValueError("Either a Pokemon object or text must be provided.")

        inputs = self.tokenizer(episode_description, return_tensors="pt", padding=True, truncation=True)
        with torch.no_grad():
            outputs = self.model(**inputs)

        embedding = outputs.last_hidden_state[:, 0, :].numpy()

        return embedding.reshape(1, -1)

    def search_episode_by_vector(self, query_vector: np.ndarray, top_k: int = 5):
        distances, indices = self.faiss_service.search_index(query_vector, top_k)
        return distances, indices
