"""Registry for context providers."""

from typing import Type, Optional

from ..graph.connection import KuzuConnection


class ContextProviderRegistry:
    """Registry for context providers using class-method pattern.

    Providers register themselves at import time, allowing for
    easy extensibility without modifying existing code.

    Example:
        ContextProviderRegistry.register("my_provider", MyProvider)
        provider = ContextProviderRegistry.get_provider("my_provider", connection)
    """

    _providers: dict[str, Type] = {}

    @classmethod
    def register(cls, name: str, provider_class: Type):
        """Register a context provider.

        Args:
            name: Unique name for the provider
            provider_class: Provider class (must subclass ContextProvider)
        """
        cls._providers[name] = provider_class

    @classmethod
    def get_provider(cls, name: str, connection: KuzuConnection, config: Optional[dict] = None):
        """Get a provider instance by name.

        Args:
            name: Provider name
            connection: Kuzu database connection
            config: Optional provider-specific configuration

        Returns:
            Instantiated provider

        Raises:
            ValueError: If provider name not found
        """
        if name not in cls._providers:
            available = ", ".join(cls._providers.keys()) or "none"
            raise ValueError(f"Unknown context provider: '{name}'. Available: {available}")
        return cls._providers[name](connection, config)

    @classmethod
    def list_providers(cls) -> list[str]:
        """Get list of registered provider names."""
        return list(cls._providers.keys())

    @classmethod
    def is_registered(cls, name: str) -> bool:
        """Check if a provider is registered."""
        return name in cls._providers


def get_provider(name: str, connection: KuzuConnection, config: Optional[dict] = None):
    """Convenience function to get a provider.

    Args:
        name: Provider name
        connection: Kuzu database connection
        config: Optional provider-specific configuration

    Returns:
        Instantiated provider
    """
    return ContextProviderRegistry.get_provider(name, connection, config)
