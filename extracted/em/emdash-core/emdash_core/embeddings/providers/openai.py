"""OpenAI embedding provider."""

from typing import Optional

from ..models import EmbeddingModel
from .base import EmbeddingProvider
from ...core.config import get_config
from ...utils.logger import log


class OpenAIProvider(EmbeddingProvider):
    """
    OpenAI embedding provider.

    Uses the OpenAI API to generate embeddings.
    Requires OPENAI_API_KEY environment variable.
    """

    # Models this provider handles
    SUPPORTED_MODELS = {
        EmbeddingModel.OPENAI_TEXT_3_SMALL,
        EmbeddingModel.OPENAI_TEXT_3_LARGE,
        EmbeddingModel.OPENAI_ADA_002,
    }

    def __init__(self, model: EmbeddingModel):
        """
        Initialize OpenAI provider.

        Args:
            model: The embedding model to use (must be an OpenAI model)
        """
        if model not in self.SUPPORTED_MODELS:
            raise ValueError(f"Model {model} is not supported by OpenAIProvider")
        super().__init__(model)
        self._client = None
        self._config = get_config().openai

    @property
    def is_available(self) -> bool:
        """Check if OpenAI API key is configured."""
        return self._config.is_available

    @property
    def _client_instance(self):
        """Lazy-load OpenAI client."""
        if self._client is None:
            if not self.is_available:
                raise RuntimeError(
                    "OpenAI API key not configured. Set OPENAI_API_KEY environment variable."
                )
            try:
                from openai import OpenAI

                self._client = OpenAI(api_key=self._config.api_key)
            except ImportError:
                raise RuntimeError(
                    "OpenAI library not installed. Run: pip install openai"
                )
        return self._client

    def embed_texts(self, texts: list[str]) -> list[Optional[list[float]]]:
        """
        Generate embeddings using OpenAI API.

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
                # Use dimensions parameter for text-embedding-3 models
                kwargs = {
                    "model": self._model.model_id,
                    "input": cleaned_batch,
                }

                # text-embedding-3 models support custom dimensions
                if self._model in {
                    EmbeddingModel.OPENAI_TEXT_3_SMALL,
                    EmbeddingModel.OPENAI_TEXT_3_LARGE,
                }:
                    kwargs["dimensions"] = self._model.dimensions

                response = self._client_instance.embeddings.create(**kwargs)
                batch_embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(batch_embeddings)

            except Exception as e:
                log.error(f"OpenAI embedding error: {e}")
                all_embeddings.extend([None] * len(cleaned_batch))

        return all_embeddings
