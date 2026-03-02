"""Provider registry for embedding models."""

from typing import Type, Optional

from .models import EmbeddingModel
from .providers.base import EmbeddingProvider
from .providers.openai import OpenAIProvider
from .providers.fireworks import FireworksProvider


class ProviderRegistry:
    """
    Registry for embedding providers.

    Maps provider names to provider classes. No if-else chains needed.
    Just register your provider once and it's available everywhere.

    Usage:
        registry = ProviderRegistry()
        provider = registry.get_provider(EmbeddingModel.OPENAI_TEXT_3_SMALL)
        embeddings = provider.embed_texts(["hello world"])
    """

    # Provider class registry: provider_name -> provider_class
    _providers: dict[str, Type[EmbeddingProvider]] = {}

    @classmethod
    def register(cls, provider_name: str, provider_class: Type[EmbeddingProvider]):
        """
        Register a provider class.

        Args:
            provider_name: Name of the provider (e.g., "openai", "fireworks")
            provider_class: The provider class to register
        """
        cls._providers[provider_name] = provider_class

    @classmethod
    def get_provider_class(cls, provider_name: str) -> Optional[Type[EmbeddingProvider]]:
        """
        Get the provider class for a provider name.

        Args:
            provider_name: Name of the provider

        Returns:
            Provider class or None if not registered
        """
        return cls._providers.get(provider_name)

    @classmethod
    def get_provider(cls, model: EmbeddingModel) -> EmbeddingProvider:
        """
        Get an instantiated provider for a model.

        Args:
            model: The embedding model

        Returns:
            Instantiated provider for the model

        Raises:
            ValueError: If no provider is registered for the model's provider
        """
        provider_class = cls._providers.get(model.provider)
        if provider_class is None:
            raise ValueError(
                f"No provider registered for '{model.provider}'. "
                f"Available providers: {list(cls._providers.keys())}"
            )
        return provider_class(model)

    @classmethod
    def list_providers(cls) -> list[str]:
        """List all registered provider names."""
        return list(cls._providers.keys())

    @classmethod
    def is_provider_available(cls, provider_name: str) -> bool:
        """
        Check if a provider is available (registered and configured).

        Args:
            provider_name: Name of the provider

        Returns:
            True if provider is registered and has valid credentials
        """
        provider_class = cls._providers.get(provider_name)
        if provider_class is None:
            return False

        # Get any model for this provider to check availability
        models = EmbeddingModel.list_by_provider(provider_name)
        if not models:
            return False

        try:
            provider = provider_class(models[0])
            return provider.is_available
        except Exception:
            return False


# ═══════════════════════════════════════════════════════════════════════════════
# Register all providers
# ═══════════════════════════════════════════════════════════════════════════════

ProviderRegistry.register("openai", OpenAIProvider)
ProviderRegistry.register("fireworks", FireworksProvider)


# ═══════════════════════════════════════════════════════════════════════════════
# Convenience functions
# ═══════════════════════════════════════════════════════════════════════════════


def get_provider(model: EmbeddingModel) -> EmbeddingProvider:
    """Get an instantiated provider for a model."""
    return ProviderRegistry.get_provider(model)


def get_default_provider() -> EmbeddingProvider:
    """Get the default embedding provider (OpenAI text-embedding-3-small)."""
    return ProviderRegistry.get_provider(EmbeddingModel.get_default())


def get_available_model() -> Optional[EmbeddingModel]:
    """
    Get the first available model (has valid API credentials).

    Checks OpenAI first, then Fireworks.

    Returns:
        First available model or None if no providers are configured
    """
    # Priority order
    priority = ["openai", "fireworks"]

    for provider_name in priority:
        if ProviderRegistry.is_provider_available(provider_name):
            models = EmbeddingModel.list_by_provider(provider_name)
            if models:
                return models[0]

    return None
