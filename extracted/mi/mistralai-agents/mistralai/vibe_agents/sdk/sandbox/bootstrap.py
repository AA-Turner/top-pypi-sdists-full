"""Private client for the public Sandbox Proxy bootstrap API."""

from dataclasses import dataclass
from http import HTTPMethod
from typing import Any, Self

import httpx
from pydantic import BaseModel, ConfigDict, Field, ValidationError

from mistralai.vibe_agents._http import _InternalHTTPClient
from mistralai.vibe_agents.sdk.app.config import (
    MISTRAL_API_URL_ENV_VARS,
    ControlPlaneSettings,
    SandboxProxyBootstrapSettings,
    mistral_api_url,
)
from mistralai.workflows.core.auth import TokenProvider, get_token_provider
from mistralai.workflows.core.config.config import config as workflows_config
from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context
from mistralai.workflows.core.worker_client import get_worker_client
from mistralai.workflows.exceptions import WorkflowError
from mistralai.workflows.worker_client.errors import SDKError
from mistralai.workflows.worker_client.sdk import PrivateWorkerClient

from .proxy_integrations import (
    GitHubProxyConfig,
    SandboxProxyIntegration,
    SecretInjectionProxyConfig,
)

MISTRAL_API_BASE_URL = "https://api.mistral.ai"
_ORIGIN_SERVICE = "agents-sdk"
_MAX_RETRIES_AFTER_INITIAL_ATTEMPT = 2
_RETRYABLE_STATUS_CODES = frozenset({429, 500, 502, 503, 504})


class SandboxBootstrapError(RuntimeError):
    """Credential-free error from the Sandbox Proxy bootstrap client."""


class SandboxBootstrapResult(BaseModel):
    """Validated bootstrap data consumed within one sandbox effect."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    setup_env: dict[str, str]
    setup_command: str = Field(min_length=1)
    renewal_command: str = Field(min_length=1)
    runtime_env: dict[str, str]
    expires_at: int = Field(gt=0)


@dataclass(frozen=True, slots=True)
class _LocalAuthentication:
    api_key: str
    base_url: str


@dataclass(frozen=True, slots=True)
class _WorkflowTokenAuthentication:
    token_provider: TokenProvider
    base_url: str


@dataclass(frozen=True, slots=True)
class _WorkflowHeaderAuthentication:
    """Identity headers of an internal shared worker, captured when authentication is resolved."""

    headers: dict[str, str]
    base_url: str


type _WorkflowAuthentication = _WorkflowTokenAuthentication | _WorkflowHeaderAuthentication
type _CurrentAuthentication = _LocalAuthentication | _WorkflowAuthentication


class SandboxProxyBootstrapClient(_InternalHTTPClient):
    """Call public Sandbox Proxy bootstrap endpoints as the current user."""

    def __init__(
        self,
        *,
        api_key: str | None,
        base_url: str = MISTRAL_API_BASE_URL,
        timeout_seconds: float = 30.0,
        workflow_authentication: _WorkflowAuthentication | None = None,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> None:
        self._api_key = api_key.strip() if api_key is not None else ""
        self._workflow_authentication = workflow_authentication
        self._has_authentication = bool(self._api_key or workflow_authentication is not None)
        super().__init__(
            base_url=base_url,
            api_key=self._api_key or None,
            timeout_seconds=timeout_seconds,
            extra_headers={"x-internal-service": _ORIGIN_SERVICE},
            transport=transport,
        )

    @classmethod
    def from_current_environment(
        cls,
        *,
        base_url: str | None = None,
        timeout_seconds: float = 30.0,
        transport: httpx.AsyncBaseTransport | None = None,
    ) -> Self:
        """Select API-key authentication locally and executor identity in a Workflow."""

        authentication = _resolve_current_authentication(base_url=base_url)
        if isinstance(authentication, _LocalAuthentication):
            return cls(
                api_key=authentication.api_key,
                base_url=authentication.base_url,
                timeout_seconds=timeout_seconds,
                transport=transport,
            )
        return cls(
            api_key=None,
            base_url=base_url or _configured_bootstrap_url() or authentication.base_url,
            timeout_seconds=timeout_seconds,
            workflow_authentication=authentication,
            transport=transport,
        )

    async def bootstrap(
        self,
        integration: SandboxProxyIntegration,
    ) -> SandboxBootstrapResult:
        """Bootstrap one configured Sandbox Proxy integration."""

        if not self._has_authentication:
            raise SandboxBootstrapError("Sandbox Proxy bootstrap requires Mistral authentication")

        path, body = _bootstrap_request(integration)
        try:
            response = await self.make_request(
                HTTPMethod.POST,
                path,
                retries=_MAX_RETRIES_AFTER_INITIAL_ATTEMPT,
                retries_codes=_RETRYABLE_STATUS_CODES,
                headers=await self._authorization_headers(),
                json=body,
            )
        except (SDKError, WorkflowError):
            raise SandboxBootstrapError(
                "Sandbox Proxy bootstrap could not obtain Workflow executor credentials"
            ) from None
        except httpx.TransportError:
            raise SandboxBootstrapError("Sandbox Proxy bootstrap could not reach the Mistral API") from None
        _raise_for_response(response)
        return _parse_bootstrap_response(response)

    async def _authorization_headers(self) -> dict[str, str] | None:
        authentication = self._workflow_authentication
        if authentication is None:
            return None
        execution_token = _require_workflow_execution_token()
        async with _worker_client(authentication) as client:
            response = await client.executor_identity_token_async(execution_token=execution_token)
        return {"Authorization": f"Bearer {response.token}"}


def _worker_client(authentication: _WorkflowAuthentication) -> PrivateWorkerClient:
    if isinstance(authentication, _WorkflowTokenAuthentication):
        return get_worker_client(
            base_url=authentication.base_url,
            token_provider=authentication.token_provider,
        )
    return get_worker_client(
        base_url=authentication.base_url,
        headers=dict(authentication.headers),
    )


def _bootstrap_request(integration: SandboxProxyIntegration) -> tuple[str, dict[str, Any]]:
    if isinstance(integration, GitHubProxyConfig):
        return (
            "/bootstrap/github",
            {
                "scope": {
                    "repo_whitelist": list(integration.repo_whitelist),
                    "all_accessible_repos": integration.all_accessible_repos,
                },
                "ttl_seconds": integration.ttl_seconds,
            },
        )
    if isinstance(integration, SecretInjectionProxyConfig):
        return "/bootstrap/secret-injection", {}
    raise SandboxBootstrapError(f"Unsupported Sandbox Proxy integration: {integration.type!r}")


def _resolve_current_authentication(*, base_url: str | None = None) -> _CurrentAuthentication:
    context = retrieve_context()
    if context is None:
        api_key = ControlPlaneSettings().api_key
        if not api_key:
            raise SandboxBootstrapError("Sandbox Proxy bootstrap requires MISTRAL_API_KEY")
        return _LocalAuthentication(
            api_key=api_key,
            base_url=_resolve_local_base_url(base_url),
        )

    _require_workflow_execution_token()
    resolved_base_url = (base_url or workflows_config.worker.server_url).rstrip("/")
    token_provider = get_token_provider()
    if token_provider is not None:
        return _WorkflowTokenAuthentication(token_provider=token_provider, base_url=resolved_base_url)
    headers = workflows_config.worker.mistral_api_headers
    if headers:
        return _WorkflowHeaderAuthentication(headers=dict(headers), base_url=resolved_base_url)
    raise SandboxBootstrapError("Workflow Sandbox Proxy bootstrap requires worker credentials")


def _configured_bootstrap_url() -> str | None:
    url = (SandboxProxyBootstrapSettings().url or "").strip()
    return url.rstrip("/") or None


def _resolve_local_base_url(base_url: str | None) -> str:
    if base_url is not None and base_url.strip():
        return base_url.strip().rstrip("/")
    return mistral_api_url(("MISTRAL_BASE_URL", *MISTRAL_API_URL_ENV_VARS)) or MISTRAL_API_BASE_URL


def _require_workflow_execution_token() -> str:
    context = retrieve_context()
    if context is None or not context.execution_token or not context.on_behalf_of:
        raise SandboxBootstrapError("Sandbox Proxy bootstrap requires an on-behalf-of Workflow execution token")
    return context.execution_token


def _parse_bootstrap_response(response: httpx.Response) -> SandboxBootstrapResult:
    try:
        return SandboxBootstrapResult.model_validate(response.json())
    except (ValueError, ValidationError):
        raise SandboxBootstrapError("Sandbox Proxy returned an invalid bootstrap response") from None


def _raise_for_response(response: httpx.Response) -> None:
    if response.status_code == 401:
        raise SandboxBootstrapError("The credentials were rejected by the Sandbox Proxy bootstrap service")
    if response.status_code == 403:
        raise SandboxBootstrapError("The credentials are not authorized to bootstrap Sandbox Proxy access")
    if response.status_code == 429:
        raise SandboxBootstrapError("Sandbox Proxy bootstrap was rate limited")
    if 400 <= response.status_code < 500:
        raise SandboxBootstrapError("Sandbox Proxy bootstrap request was rejected")
    if response.status_code >= 500:
        raise SandboxBootstrapError("Sandbox Proxy bootstrap service failed")


__all__ = [
    "MISTRAL_API_BASE_URL",
    "SandboxBootstrapError",
    "SandboxBootstrapResult",
    "SandboxProxyBootstrapClient",
]
