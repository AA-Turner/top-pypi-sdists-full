"""Provider factory: resolves node_type to configured provider instance."""

from __future__ import annotations

import os
import threading
from collections.abc import Callable, Mapping

from agentic_devtools.orchestration.llm.base_provider import LLMProvider
from agentic_devtools.orchestration.llm.config import LLMConfigSnapshot, load_config, resolve_node_config
from agentic_devtools.orchestration.llm.errors import AuthenticationError
from agentic_devtools.orchestration.llm.types import NodeConfig, ProviderType

# (provider_id, effective_model, temperature, max_tokens, timeout_seconds)
_CacheKey = tuple[str | None, str | None, float | None, int | None, int | None]


class ProviderFactory:
    """Factory that resolves node types to configured LLM provider instances.

    Instantiated once per workflow execution. Loads configuration once
    (immutable snapshot) and creates provider instances on demand.
    """

    def __init__(
        self,
        config: LLMConfigSnapshot | None = None,
        *,
        copilot_transport_factory: Callable[[NodeConfig], object] | None = None,
    ) -> None:
        """Initialize factory with configuration snapshot.

        Args:
            config: Pre-loaded config. If None, loads from default path.
            copilot_transport_factory: Optional injectable factory that receives
                a resolved ``NodeConfig`` and returns a Copilot transport
                instance.  When provided, Copilot providers use this instead of
                creating the default SDK-backed transport.
        """
        self._config = config if config is not None else load_config()
        self._providers: dict[_CacheKey, LLMProvider] = {}
        self._providers_lock = threading.Lock()
        self._copilot_transport_factory = copilot_transport_factory

    @property
    def config(self) -> LLMConfigSnapshot:
        """Return the configuration snapshot."""
        return self._config

    def get_provider(
        self,
        node_type: str,
        workflow: str = "default",
    ) -> LLMProvider:
        """Get a configured provider for the given node type.

        Args:
            node_type: The node type requesting a provider.
            workflow: The workflow context. Defaults to "default".

        Returns:
            Configured LLMProvider instance.

        Raises:
            AuthenticationError: If API key env var is not set.
        """
        node_config = resolve_node_config(self._config, workflow, node_type)
        # Cache key based on provider_id + effective model + temperature + max_tokens + timeout.
        # Use a tuple (not a ':'-joined string) to avoid collisions when any component
        # contains ':' (e.g. a provider_id like "team:azure" or a model name with ":").
        effective_timeout = _get_effective_timeout_seconds(node_config)
        cache_key = (
            node_config.provider_id,
            node_config.effective_model,
            node_config.effective_temperature,
            node_config.effective_max_tokens,
            effective_timeout,
        )
        with self._providers_lock:
            if cache_key in self._providers:
                return self._providers[cache_key]

            if self._copilot_transport_factory is None:
                provider = _create_provider(node_config)
            else:
                provider = _create_provider(node_config, self._copilot_transport_factory)
            self._providers[cache_key] = provider
            return provider

    async def preflight(
        self,
        node_type: str,
        workflow: str = "default",
        *,
        models: list[str] | None = None,
    ) -> LLMProvider:
        """Resolve a provider and complete any provider-specific readiness checks."""
        provider = self.get_provider(node_type, workflow)
        preflight = getattr(provider, "preflight", None)
        if preflight is not None:
            await preflight(models)
        return provider


def get_provider(
    node_type: str,
    workflow: str = "default",
    config: LLMConfigSnapshot | None = None,
) -> LLMProvider:
    """Convenience function to get a provider for a node type.

    Args:
        node_type: The node type requesting a provider.
        workflow: The workflow context.
        config: Optional pre-loaded config.

    Returns:
        Configured LLMProvider instance.
    """
    factory = ProviderFactory(config)
    return factory.get_provider(node_type, workflow)


def _create_provider(
    node_config: NodeConfig,
    copilot_transport_factory: Callable[[NodeConfig], object] | None = None,
) -> LLMProvider:
    """Create a provider instance from resolved node configuration."""
    effective_timeout = _get_effective_timeout_seconds(node_config)

    if node_config.provider_type == ProviderType.COPILOT and node_config.api_key_env:
        raise ValueError("api_key_env is not valid for the copilot provider; use Copilot login")

    # Resolve API key from environment
    api_key: str | None = None
    if (
        node_config.provider_type in (ProviderType.AZURE_OPENAI, ProviderType.OPENAI_DIRECT)
        and not node_config.api_key_env
    ):
        raise AuthenticationError(
            f"api_key_env must be configured for provider type '{node_config.provider_type.value}'",
            provider_type=node_config.provider_type.value,
            env_var="",
        )

    if node_config.api_key_env:
        api_key = os.environ.get(node_config.api_key_env)
        if not api_key:
            raise AuthenticationError(
                f"Environment variable '{node_config.api_key_env}' not set",
                provider_type=node_config.provider_type.value,
                env_var=node_config.api_key_env,
            )

    if node_config.provider_type == ProviderType.AZURE_OPENAI:
        from agentic_devtools.orchestration.llm.providers.azure_openai import AzureOpenAIProvider

        if not node_config.endpoint:
            raise ValueError("Azure OpenAI provider requires endpoint configuration")

        return AzureOpenAIProvider(
            api_key=api_key or "",
            endpoint=node_config.endpoint,
            model=node_config.effective_model,
            api_version=node_config.api_version or "2024-02-01",
            temperature=node_config.effective_temperature,
            max_tokens=node_config.effective_max_tokens,
            timeout_seconds=effective_timeout,
        )
    elif node_config.provider_type == ProviderType.OPENAI_DIRECT:
        from agentic_devtools.orchestration.llm.providers.openai_direct import OpenAIDirectProvider

        return OpenAIDirectProvider(
            api_key=api_key or "",
            model=node_config.effective_model,
            temperature=node_config.effective_temperature,
            max_tokens=node_config.effective_max_tokens,
            timeout_seconds=effective_timeout,
        )
    elif node_config.provider_type == ProviderType.LOCAL_MODEL:
        from agentic_devtools.orchestration.llm.providers.local_model import LocalModelProvider

        return LocalModelProvider(
            endpoint=node_config.endpoint or "http://localhost:11434/v1",
            model=node_config.effective_model,
            temperature=node_config.effective_temperature,
            max_tokens=node_config.effective_max_tokens,
            timeout_seconds=effective_timeout,
        )
    elif node_config.provider_type == ProviderType.COPILOT:
        from agentic_devtools.orchestration.llm.providers.copilot import CopilotProvider

        transport = copilot_transport_factory(node_config) if copilot_transport_factory else None
        return CopilotProvider(
            model=node_config.effective_model,
            temperature=node_config.effective_temperature,
            max_tokens=node_config.effective_max_tokens,
            timeout_seconds=effective_timeout,
            transport=transport,  # type: ignore[arg-type]
        )
    else:
        msg = f"Unsupported provider type: {node_config.provider_type}"
        raise ValueError(msg)


def _get_effective_timeout_seconds(node_config: NodeConfig) -> int | None:
    """Resolve timeout override from params_override first, then base timeout."""
    params_override = getattr(node_config, "params_override", {})
    if isinstance(params_override, Mapping) and "timeout_seconds" in params_override:
        return params_override["timeout_seconds"]
    return node_config.timeout_seconds
