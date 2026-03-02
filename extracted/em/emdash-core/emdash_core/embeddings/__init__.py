"""Embedding generation and semantic search for EmDash."""

from .models import EmbeddingModel, ModelSpec
from .service import EmbeddingService
from .indexer import EmbeddingIndexer
from .registry import ProviderRegistry, get_provider, get_available_model
from .providers import EmbeddingProvider, OpenAIProvider, FireworksProvider

__all__ = [
    # Models
    "EmbeddingModel",
    "ModelSpec",
    # Service
    "EmbeddingService",
    "EmbeddingIndexer",
    # Registry
    "ProviderRegistry",
    "get_provider",
    "get_available_model",
    # Providers
    "EmbeddingProvider",
    "OpenAIProvider",
    "FireworksProvider",
]
