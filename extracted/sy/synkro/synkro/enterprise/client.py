"""Synkro enterprise client — main entry point."""

from __future__ import annotations

from synkro.enterprise._http import AsyncBaseHTTPClient, BaseHTTPClient
from synkro.enterprise.resources.integrations import AsyncIntegrations, Integrations
from synkro.enterprise.resources.policies import AsyncPolicies, Policies
from synkro.enterprise.resources.projects import AsyncProjects, Projects

DEFAULT_BASE_URL = "https://api.synkro.sh"


class Synkro:
    """Synkro enterprise client (synchronous).

    Args:
        api_key: API key (sk-synkro-xxx).
        base_url: CRUD server URL. Defaults to https://api.synkro.sh.
        timeout: Request timeout in seconds.

    Example::

        synkro = Synkro(api_key="sk-synkro-xxx")
        projects = synkro.projects.list()
    """

    projects: Projects
    policies: Policies
    integrations: Integrations

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
    ):
        self._http = BaseHTTPClient(base_url=base_url, api_key=api_key, timeout=timeout)
        self.projects = Projects(self._http)
        self.policies = Policies(self._http)
        self.integrations = Integrations(self._http)

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
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
    ):
        self._http = AsyncBaseHTTPClient(base_url=base_url, api_key=api_key, timeout=timeout)
        self.projects = AsyncProjects(self._http)
        self.policies = AsyncPolicies(self._http)
        self.integrations = AsyncIntegrations(self._http)

    async def close(self) -> None:
        """Close the underlying HTTP client."""
        await self._http.close()

    async def __aenter__(self) -> AsyncSynkro:
        return self

    async def __aexit__(self, *args) -> None:
        await self.close()
