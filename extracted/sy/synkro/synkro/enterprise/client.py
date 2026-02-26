"""Synkro enterprise client — main entry point."""

from __future__ import annotations

from synkro.enterprise._http import AsyncBaseHTTPClient, BaseHTTPClient
from synkro.enterprise.resources.integrations import AsyncIntegrations, Integrations
from synkro.enterprise.resources.policies import AsyncPolicies, Policies
from synkro.enterprise.resources.projects import AsyncProjects, Projects

DEFAULT_BASE_URL = "https://api.synkro.sh"
SYNKRO_GATEWAY_URL = "https://gateway.synkro.sh"

_PREFIX_MAP: dict[str, str] = {
    "gpt-": "openai",
    "o1-": "openai",
    "o3-": "openai",
    "o4-": "openai",
    "claude-": "anthropic",
    "gemini/": "google",
    "gemini-": "google",
    "llama-": "groq",
    "mistral-": "mistral",
    "deepseek-": "deepseek",
    "cerebras/": "cerebras",
}

# litellm provider → gateway provider name
_PROVIDER_ALIASES: dict[str, str] = {
    "gemini": "google",
}


def _detect_provider(model: str) -> str:
    """Resolve provider from model name via litellm, falling back to prefix matching."""
    try:
        from litellm import get_llm_provider

        _, provider, _, _ = get_llm_provider(model)
        return _PROVIDER_ALIASES.get(provider, provider)
    except Exception:
        pass

    for prefix, provider in _PREFIX_MAP.items():
        if model.startswith(prefix):
            return provider

    raise ValueError(
        f"Could not auto-detect provider for model '{model}'. "
        "Pass provider= explicitly, e.g. provider='openai'"
    )


def _strip_provider_prefix(model: str) -> str:
    """Strip litellm provider prefix (e.g. 'gemini/gemini-2.5-flash' → 'gemini-2.5-flash')."""
    if "/" in model:
        return model.split("/", 1)[1]
    return model


def createHeaders(  # noqa: N802
    api_key: str,
    provider: str | None = None,
    user_id: str | None = None,
) -> dict[str, str]:
    """Build Synkro gateway headers for use with any HTTP client.

    Args:
        api_key: Synkro API key (sk-synkro-xxx).
        provider: Provider name (e.g. "gemini", "openai").
        user_id: Optional user identifier for per-user tracking.

    Returns:
        Dict of headers to attach to requests.
    """
    headers: dict[str, str] = {"x-synkro-api-key": api_key}
    if provider:
        headers["x-synkro-provider"] = provider
    if user_id:
        headers["x-synkro-user-id"] = user_id
    return headers


class Synkro:
    """Synkro enterprise client (synchronous).

    Args:
        api_key: API key (sk-synkro-xxx).
        gateway_url: Gateway URL including project slug (required for .gateway()).
        base_url: CRUD server URL. Defaults to https://api.synkro.sh.
        timeout: Request timeout in seconds.

    Example::

        synkro = Synkro(
            api_key="sk-synkro-xxx",
            gateway_url="https://gateway.synkro.sh/v1/projects/my-slug",
        )
        llm = ChatOpenAI(
            **synkro.gateway(api_key=GEMINI_KEY, provider="google"),
            model="gemini-2.5-flash-lite",
        )
    """

    projects: Projects
    policies: Policies
    integrations: Integrations

    def __init__(
        self,
        api_key: str,
        *,
        gateway_url: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
    ):
        self._api_key = api_key
        self._gateway_url = gateway_url
        self._http = BaseHTTPClient(base_url=base_url, api_key=api_key, timeout=timeout)
        self.projects = Projects(self._http)
        self.policies = Policies(self._http)
        self.integrations = Integrations(self._http)

    def gateway(
        self,
        api_key: str,
        user_id: str | None = None,
        provider: str | None = None,
    ) -> dict:
        """Return kwargs to unpack into ChatOpenAI.

        Usage::

            llm = ChatOpenAI(
                **synkro.gateway(api_key=GEMINI_KEY, user_id="passenger-42"),
                model="gemini-2.5-flash-lite",
                temperature=1,
            )

        Args:
            api_key: The *provider's* API key (NOT the Synkro API key).
            user_id: Optional user identifier for per-user tracking.
            provider: Provider name for the gateway (e.g. "google", "openai").

        Returns:
            Dict of kwargs (``client``, ``async_client``, ``api_key``) for ChatOpenAI.
        """
        if not self._gateway_url:
            raise ValueError(
                "No gateway_url configured. Pass gateway_url= to Synkro() constructor."
            )

        try:
            from openai import AsyncOpenAI, OpenAI
        except ImportError:
            raise ImportError(
                "openai is required for synkro.gateway(). " "Install it with: pip install openai"
            )

        headers = createHeaders(api_key=self._api_key, provider=provider, user_id=user_id)

        sync_client = OpenAI(
            base_url=self._gateway_url,
            api_key=api_key,
            default_headers=headers,
        )
        async_client = AsyncOpenAI(
            base_url=self._gateway_url,
            api_key=api_key,
            default_headers=headers,
        )

        return {
            "client": sync_client.chat.completions,
            "async_client": async_client.chat.completions,
            "api_key": api_key,
        }

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._http.close()

    def __enter__(self) -> Synkro:
        return self

    def __exit__(self, *args) -> None:
        self.close()


class AsyncSynkro:
    """Synkro enterprise client (asynchronous).

    Args:
        api_key: API key (sk-synkro-xxx).
        gateway_url: Gateway URL including project slug (required for .gateway()).
        base_url: CRUD server URL. Defaults to https://api.synkro.sh.
        timeout: Request timeout in seconds.

    Example::

        synkro = AsyncSynkro(api_key="sk-synkro-xxx")
        projects = await synkro.projects.list()
    """

    projects: AsyncProjects
    policies: AsyncPolicies
    integrations: AsyncIntegrations

    def __init__(
        self,
        api_key: str,
        *,
        gateway_url: str | None = None,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
    ):
        self._api_key = api_key
        self._gateway_url = gateway_url
        self._http = AsyncBaseHTTPClient(base_url=base_url, api_key=api_key, timeout=timeout)
        self.projects = AsyncProjects(self._http)
        self.policies = AsyncPolicies(self._http)
        self.integrations = AsyncIntegrations(self._http)

    def gateway(
        self,
        api_key: str,
        user_id: str | None = None,
        provider: str | None = None,
    ) -> dict:
        """Return kwargs to unpack into ChatOpenAI.

        Usage::

            llm = ChatOpenAI(
                **synkro.gateway(api_key=GEMINI_KEY, user_id="passenger-42"),
                model="gemini-2.5-flash-lite",
                temperature=1,
            )

        Args:
            api_key: The *provider's* API key (NOT the Synkro API key).
            user_id: Optional user identifier for per-user tracking.
            provider: Provider name for the gateway (e.g. "google", "openai").

        Returns:
            Dict of kwargs (``client``, ``async_client``, ``api_key``) for ChatOpenAI.
        """
        if not self._gateway_url:
            raise ValueError(
                "No gateway_url configured. Pass gateway_url= to Synkro() constructor."
            )

        try:
            from openai import AsyncOpenAI, OpenAI
        except ImportError:
            raise ImportError(
                "openai is required for synkro.gateway(). " "Install it with: pip install openai"
            )

        headers = createHeaders(api_key=self._api_key, provider=provider, user_id=user_id)

        sync_client = OpenAI(
            base_url=self._gateway_url,
            api_key=api_key,
            default_headers=headers,
        )
        async_client = AsyncOpenAI(
            base_url=self._gateway_url,
            api_key=api_key,
            default_headers=headers,
        )

        return {
            "client": sync_client.chat.completions,
            "async_client": async_client.chat.completions,
            "api_key": api_key,
        }

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._http.close()

    async def __aenter__(self) -> AsyncSynkro:
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()
