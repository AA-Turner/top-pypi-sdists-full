"""Fireworks AI embedding provider."""

from typing import Optional

from ..models import EmbeddingModel
from .base import EmbeddingProvider
from ...core.config import get_config
from ...utils.logger import log


class FireworksProvider(EmbeddingProvider):
    """
    Fireworks AI embedding provider.

    Uses the Fireworks API (OpenAI-compatible) to generate embeddings.
    Requires FIREWORKS_API_KEY environment variable.

    API docs: https://docs.fireworks.ai/guides/querying-embeddings-models
    """

    # Fireworks API base URL
    BASE_URL = "https://api.fireworks.ai/inference/v1"

    # Models this provider handles
    SUPPORTED_MODELS = {
        EmbeddingModel.FIREWORKS_NOMIC_EMBED_V1_5,
        EmbeddingModel.FIREWORKS_E5_MISTRAL_7B,
        EmbeddingModel.FIREWORKS_UAE_LARGE_V1,
        EmbeddingModel.FIREWORKS_GTE_LARGE,
        EmbeddingModel.FIREWORKS_BGE_LARGE_EN,
    }

    def __init__(self, model: EmbeddingModel):
        """
        Initialize Fireworks provider.

        Args:
            model: The embedding model to use (must be a Fireworks model)
        """
        if model not in self.SUPPORTED_MODELS:
            raise ValueError(f"Model {model} is not supported by FireworksProvider")
        super().__init__(model)
        self._client = None

    @property
    def _api_key(self) -> Optional[str]:
        """Get Fireworks API key from config."""
        config = get_config()
        # Check if fireworks config exists
        if hasattr(config, "fireworks") and config.fireworks.api_key:
            return config.fireworks.api_key
        return None

    @property
    def is_available(self) -> bool:
        """Check if Fireworks API key is configured."""
        return self._api_key is not None and len(self._api_key) > 0

    @property
    def _client_instance(self):
        """Lazy-load OpenAI client configured for Fireworks."""
        if self._client is None:
            if not self.is_available:
                raise RuntimeError(
                    "Fireworks API key not configured. Set FIREWORKS_API_KEY environment variable."
                )
            try:
                from openai import OpenAI

                # Fireworks uses OpenAI-compatible API
                self._client = OpenAI(
                    api_key=self._api_key,
                    base_url=self.BASE_URL,
                )
            except ImportError:
                raise RuntimeError(
                    "OpenAI library not installed. Run: pip install openai"
                )
        return self._client

    def embed_texts(self, texts: list[str]) -> list[Optional[list[float]]]:
        """
        Generate embeddings using Fireworks API.

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors. None for failed embeddings.
        """
        if not texts:
            return []

        all_embeddings = []
        batch_size = self._model.spec.batch_size

        for i in range(0, len(texts), batch_size):
            batch = texts[i : i + batch_size]
            cleaned_batch = self._clean_batch(batch)

            try:
                # Fireworks requires accounts/ prefix for model IDs
                model_id = f"accounts/fireworks/models/{self._model.model_id}"

                response = self._client_instance.embeddings.create(
                    model=model_id,
                    input=cleaned_batch,
                )
                batch_embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(batch_embeddings)

            except Exception as e:
                log.error(f"Fireworks embedding error: {e}")
                all_embeddings.extend([None] * len(cleaned_batch))

        return all_embeddings

    def embed_query(self, query: str) -> Optional[list[float]]:
        """
        Generate embedding for a search query.

        Some Fireworks models (like Nomic, E5) benefit from query prefixes.

        Args:
            query: Search query string

        Returns:
            Embedding vector or None if failed
        """
        if not query:
            return None

        # E5 models expect "query: " prefix for queries
        if self._model == EmbeddingModel.FIREWORKS_E5_MISTRAL_7B:
            query = f"query: {query}"

        # Nomic models can optionally use "search_query: " prefix
        elif self._model == EmbeddingModel.FIREWORKS_NOMIC_EMBED_V1_5:
            query = f"search_query: {query}"

        return self.embed_text(query)
