import os
# disable tokenizers parallelism
os.environ["TOKENIZERS_PARALLELISM"] = "false"

from typing import List, Tuple, Union, Dict
import numpy as np
import torch
from sentence_transformers import SentenceTransformer
from canonmap.services.entity_mapping.utils.get_cpu_count import get_cpu_count
from canonmap.utils.logger import setup_logger

logger = setup_logger(__name__)

class Embedder:
    """
    Encapsulates embedding logic using SentenceTransformer with flexible model loading.
    Supports offline mode and custom model directories.
    """
    def __init__(
        self,
        model_name: str = "all-MiniLM-L6-v2",
        batch_size: int = 1024,
        num_workers: int = None
    ):
        self.device = self._resolve_device()
        self.batch_size = batch_size
        self.num_workers = num_workers or get_cpu_count()
        
        logger.info(f"Using device: {self.device}")
        logger.info(f"Detected {self.num_workers} CPU cores for parallel processing.")
        logger.info(f"Loading SentenceTransformer '{model_name}'...")
        
        try:
            self._model = SentenceTransformer(
                model_name,
                device=self.device
            )
            logger.info(f"Model '{model_name}' loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load model '{model_name}': {e}")
            logger.error(
                "Please run:\n"
                f"\033[94m    canonmap-download-model {model_name}\n\033[0m"
                "to download and cache the model, then try again."
            )
            raise

    def _resolve_device(self) -> str:
        if torch.cuda.is_available():
            return "cuda"
        if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
            return "mps"
        return "cpu"

    def embed_texts(
        self,
        texts_or_jobs: Union[List[str], List[Tuple[str, List[str]]]],
        tag: str = "embedding"
    ) -> Union[np.ndarray, Dict[str, np.ndarray]]:
        """
        If given a simple list of strings, returns a single np.ndarray.
        If given a list of (name, [texts]) jobs, returns a dict mapping
        each name to its embeddings array.
        """
        # single‐job fallback
        if isinstance(texts_or_jobs[0], str):
            return self._model.encode(
                texts_or_jobs,
                batch_size=self.batch_size,
                show_progress_bar=False,
                num_workers=self.num_workers
            )

        # multiple jobs: flatten them into one big list, then slice results
        all_texts: List[str] = []
        boundaries: Dict[str, Tuple[int,int]] = {}
        for name, texts in texts_or_jobs:
            start = len(all_texts)
            all_texts.extend(texts)
            end = len(all_texts)
            boundaries[name] = (start, end)

        if not all_texts:
            # nothing to embed
            empty_shape = (0, self._model.get_sentence_embedding_dimension())
            return {name: np.empty(empty_shape) for name, _ in texts_or_jobs}

        logger.info(f"Embedding {len(all_texts)} texts across {len(boundaries)} jobs…")
        embeddings = self._model.encode(
            all_texts,
            batch_size=self.batch_size,
            show_progress_bar=False,
            num_workers=self.num_workers
        )

        # slice back out per job
        result: Dict[str, np.ndarray] = {}
        for name, (start, end) in boundaries.items():
            result[name] = embeddings[start:end]
        return result 