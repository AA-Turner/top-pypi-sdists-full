"""Embedding service with multi-provider support."""

from typing import Optional, Union

from .models import EmbeddingModel
from .registry import get_provider, get_available_model, ProviderRegistry
from .providers.base import EmbeddingProvider
from ..core.config import get_config
from ..core.models import PullRequestEntity, FunctionEntity, ClassEntity
from ..utils.logger import log


class EmbeddingService:
    """
    Unified embedding service with multi-provider support.

    Supports OpenAI, Fireworks AI, and other providers through a registry.
    Falls back to the first available provider if none is specified.

    Usage:
        # Use default model (OpenAI text-embedding-3-small)
        service = EmbeddingService()

        # Use specific model
        service = EmbeddingService(model=EmbeddingModel.FIREWORKS_NOMIC_EMBED_V1_5)

        # Use model from string
        service = EmbeddingService(model="fireworks:nomic-ai/nomic-embed-text-v1.5")

        # Generate embeddings
        embeddings = service.embed_texts(["hello", "world"])
    """

    def __init__(
        self,
        model: Optional[Union[EmbeddingModel, str]] = None,
        provider: Optional[EmbeddingProvider] = None,
    ):
        """
        Initialize embedding service.

        Args:
            model: Embedding model to use. Can be EmbeddingModel enum or string.
                  If None, uses first available model (OpenAI > Fireworks).
            provider: Pre-configured provider instance. If provided, model is ignored.
        """
        if provider is not None:
            self._provider = provider
            self._model = provider.model
        elif model is not None:
            # Parse model from string if needed
            if isinstance(model, str):
                parsed = EmbeddingModel.from_string(model)
                if parsed is None:
                    raise ValueError(f"Unknown embedding model: {model}")
                model = parsed
            self._model = model
            self._provider = None  # Lazy-load
        else:
            # Auto-select first available model
            self._model = get_available_model()
            self._provider = None

    @property
    def model(self) -> Optional[EmbeddingModel]:
        """Get the embedding model."""
        return self._model

    @property
    def provider(self) -> Optional[EmbeddingProvider]:
        """Get the provider, lazy-loading if needed."""
        if self._provider is None and self._model is not None:
            self._provider = get_provider(self._model)
        return self._provider

    @property
    def is_available(self) -> bool:
        """Check if embedding service is available."""
        if self._model is None:
            return False
        try:
            return self.provider is not None and self.provider.is_available
        except Exception:
            return False

    @property
    def dimensions(self) -> int:
        """Get embedding dimensions for the current model."""
        if self._model is None:
            return 1536  # Default OpenAI dimensions
        return self._model.dimensions

    def embed_texts(self, texts: list[str]) -> list[Optional[list[float]]]:
        """
        Generate embeddings for multiple texts.

        Args:
            texts: List of text strings to embed

        Returns:
            List of embedding vectors. None for failed embeddings.
        """
        if not texts:
            return []

        if not self.is_available:
            log.warning("No embedding provider available")
            return [None] * len(texts)

        return self.provider.embed_texts(texts)

    def embed_text(self, text: str) -> Optional[list[float]]:
        """
        Generate embedding for a single text.

        Args:
            text: Text string to embed

        Returns:
            Embedding vector or None if failed
        """
        if not text:
            return None
        embeddings = self.embed_texts([text])
        return embeddings[0] if embeddings else None

    def embed_query(self, query: str) -> Optional[list[float]]:
        """
        Generate embedding for a search query.

        Args:
            query: Search query string

        Returns:
            Embedding vector or None if failed
        """
        if not query:
            return None

        if not self.is_available:
            log.warning("No embedding provider available")
            return None

        return self.provider.embed_query(query)

    def embed_pr(self, pr: PullRequestEntity) -> Optional[list[float]]:
        """
        Generate embedding for a PR (title + description).

        Args:
            pr: PullRequestEntity

        Returns:
            Embedding vector or None
        """
        text = f"{pr.title}\n\n{pr.description or ''}"
        return self.embed_text(text)

    def embed_function(self, func: FunctionEntity) -> Optional[list[float]]:
        """
        Generate embedding for a function (name + docstring).

        Args:
            func: FunctionEntity

        Returns:
            Embedding vector or None
        """
        text = f"{func.name}\n\n{func.docstring or ''}"
        return self.embed_text(text)

    def embed_class(self, cls: ClassEntity) -> Optional[list[float]]:
        """
        Generate embedding for a class (name + docstring).

        Args:
            cls: ClassEntity

        Returns:
            Embedding vector or None
        """
        text = f"{cls.name}\n\n{cls.docstring or ''}"
        return self.embed_text(text)

    @staticmethod
    def list_models() -> list[dict]:
        """List all available embedding models."""
        return EmbeddingModel.list_all()

    @staticmethod
    def list_available_providers() -> list[str]:
        """List providers that are configured and available."""
        return [
            name
            for name in ProviderRegistry.list_providers()
            if ProviderRegistry.is_provider_available(name)
        ]

    @staticmethod
    def get_model_info(model: Union[EmbeddingModel, str]) -> Optional[dict]:
        """Get information about a specific model."""
        if isinstance(model, str):
            model = EmbeddingModel.from_string(model)
            if model is None:
                return None

        return {
            "name": model.name,
            "provider": model.provider,
            "model_id": model.model_id,
            "dimensions": model.dimensions,
            "max_tokens": model.spec.max_tokens,
            "batch_size": model.spec.batch_size,
            "description": model.spec.description,
        }
