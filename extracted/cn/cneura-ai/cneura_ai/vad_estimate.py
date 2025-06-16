import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class VADEstimator:
    def __init__(self, csv_path: str, model_name: str = 'all-MiniLM-L6-v2', top_k: int = 5):
        self.top_k = top_k
        self.df = pd.read_csv(csv_path)
        self.model = SentenceTransformer(model_name)
        self.texts = self.df['text'].astype(str).tolist()
        self.vads = self.df[['V', 'A', 'D']].values
        self.embeddings = self.model.encode(self.texts, convert_to_tensor=False, normalize_embeddings=True)

    def estimate_vad(self, input_text: str):
        input_embedding = self.model.encode([input_text], convert_to_tensor=False, normalize_embeddings=True)
        sims = cosine_similarity(input_embedding, self.embeddings)[0]
        
        # Get top k similar indices
        top_k_idx = np.argsort(sims)[-self.top_k:][::-1]
        top_sims = sims[top_k_idx]
        top_vads = self.vads[top_k_idx]
        
        weighted_vad = np.average(top_vads, weights=top_sims, axis=0)
        return {
            'input': input_text,
            'vad': {
                'valence': float(weighted_vad[0]),
                'arousal': float(weighted_vad[1]),
                'dominance': float(weighted_vad[2])
            },
            'top_similar_texts': [self.texts[i] for i in top_k_idx],
            'similarities': top_sims.tolist()
        }