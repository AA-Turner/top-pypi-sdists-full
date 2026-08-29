import warnings
from typing import Any, Callable, NamedTuple, Type, TypeVar

import httpx
import structlog
from mistralai.client import Mistral
from mistralai.extra.observability.telemetry import configure_telemetry
from pydantic import BaseModel

from mistralai.workflows._version import USER_AGENT
from mistralai.workflows.core import _http_transport as http_transport
from mistralai.workflows.core.auth import TokenProvider, get_token_provider
from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.logging import extract_error_context
from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context
from mistralai.workflows.exceptions import WorkflowError
from mistralai.workflows.hooks.cross_origin_auth_guard import (
    AsyncCrossOriginAuthGuardHook,
    CrossOriginAuthGuardHook,
)
from mistralai.workflows.hooks.executor_credentials_hook import (
    AsyncExecutorCredentialsHook,
    SyncExecutorCredentialsHook,
)
from mistralai.workflows.hooks.metadata_hook import inject_metadata, inject_metadata_async
from mistralai.workflows.hooks.token_provider_hook import (
    AsyncTokenProviderHook,
    TokenProviderHook,
)

logger = structlog.get_logger(__name__)


def _get_headers(
    headers: httpx.Headers | dict[str, str] | None = None,
) -> httpx.Headers:
    headers = (
        headers
        if isinstance(headers, httpx.Headers)
        else httpx.Headers(headers or config.worker.mistral_api_headers or {})
    )
    # Authorization is set per-request by the auth/executor hook, never statically here.
    headers.setdefault("User-Agent", USER_AGENT)
    return headers


class _HookVariants(NamedTuple):
    metadata: Callable
    auth: type[AsyncTokenProviderHook] | type[TokenProviderHook]
    executor: type[AsyncExecutorCredentialsHook] | type[SyncExecutorCredentialsHook]
    guard: type[AsyncCrossOriginAuthGuardHook] | type[CrossOriginAuthGuardHook]


_ASYNC_HOOKS = _HookVariants(
    metadata=inject_metadata_async,
    auth=AsyncTokenProviderHook,
    executor=AsyncExecutorCredentialsHook,
    guard=AsyncCrossOriginAuthGuardHook,
)
_SYNC_HOOKS = _HookVariants(
    metadata=inject_metadata,
    auth=TokenProviderHook,
    executor=SyncExecutorCredentialsHook,
    guard=CrossOriginAuthGuardHook,
)


def _get_hooks(
    client_cls: type[httpx.AsyncClient] | type[httpx.Client],
    server_url: str | None = None,
    token_provider: TokenProvider | None = None,
    use_executor_credentials: bool = False,
) -> dict[str, list]:
    hooks = _ASYNC_HOOKS if client_cls is httpx.AsyncClient else _SYNC_HOOKS
    request_hooks: list = [hooks.metadata]
    if use_executor_credentials:
        missing = [name for name, val in [("server_url", server_url), ("token_provider", token_provider)] if not val]
        if missing:
            raise WorkflowError(
                f"use_executor_credentials requires {', '.join(missing)}",
                non_retryable=True,
            )
        assert server_url and token_provider is not None
        logger.info("ExecutorCredentialsHook registered, using the executor's identity")
        request_hooks.append(hooks.executor(server_url=server_url, token_provider=token_provider))
    elif token_provider is not None:
        request_hooks.append(hooks.auth(token_provider))
    # Strip the bearer token on cross-origin redirect hops. MUST stay last so it runs after every
    # token-setting hook above; otherwise a later hook would re-add the header it just removed.
    request_hooks.append(hooks.guard(server_url or config.worker.server_url))
    return {"request": request_hooks}


def _get_sync_client(
    timeout: float | None = None,
    *,
    token_provider: TokenProvider | None = None,
    headers: httpx.Headers | dict[str, str] | None = None,
    server_url: str | None = None,
    use_executor_credentials: bool = False,
    api_key: str | None = None,
) -> httpx.Client:
    if token_provider is None:
        token_provider = get_token_provider(api_key)
    return httpx.Client(
        timeout=timeout if timeout is not None else config.http.timeout,
        verify=http_transport.verify(),
        headers=_get_headers(headers=headers),
        follow_redirects=True,
        event_hooks=_get_hooks(
            httpx.Client,
            server_url=server_url,
            token_provider=token_provider,
            use_executor_credentials=use_executor_credentials,
        ),
        transport=http_transport.sync_transport(),
        mounts=http_transport.sync_mounts(),
        limits=http_transport.limits(),
    )


def _get_async_client(
    timeout: float | None = None,
    *,
    token_provider: TokenProvider | None = None,
    headers: httpx.Headers | dict[str, str] | None = None,
    server_url: str | None = None,
    use_executor_credentials: bool = False,
    api_key: str | None = None,
) -> httpx.AsyncClient:
    if token_provider is None:
        token_provider = get_token_provider(api_key)
    return httpx.AsyncClient(
        timeout=timeout if timeout is not None else config.http.timeout,
        verify=http_transport.verify(),
        headers=_get_headers(headers=headers),
        follow_redirects=True,
        event_hooks=_get_hooks(
            httpx.AsyncClient,
            server_url=server_url,
            token_provider=token_provider,
            use_executor_credentials=use_executor_credentials,
        ),
        transport=http_transport.async_transport(),
        mounts=http_transport.async_mounts(),
        limits=http_transport.limits(),
    )


def get_async_client(*args: Any, **kwargs: Any) -> httpx.AsyncClient:
    warnings.warn(
        "get_async_client is deprecated and will be removed in a future version. Use _get_async_client instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return _get_async_client(*args, **kwargs)


def should_use_executor_credentials() -> bool:
    """Return True when the current execution runs on behalf of a user (obo),
    meaning downstream calls should use the executor's identity rather than the
    worker's credentials. Returns False when there is no workflow context or the
    worker is running in obo mode.
    """
    context = retrieve_context()
    return bool(context and context.on_behalf_of)


def get_mistral_client(
    server_url: str | None = None,
    api_key: str | None = None,
    use_executor_credentials: bool = False,
    server: str | None = None,
    url_params: dict[str, str] | None = None,
    timeout_ms: int | None = None,
    token_provider: TokenProvider | None = None,
) -> Mistral:
    provider = token_provider or get_token_provider(api_key)
    resolved_server_url = server_url or config.worker.server_url
    # Only the httpx client-level timeout tracks config.http.timeout. timeout_ms is left as the caller
    # passed it (None -> the SDK's longer per-request default) so config.http.timeout (default 60s)
    # does not cap long LLM completions. The LLM timeout is set via timeout_ms / agent.mistral_client_timeout_ms.
    timeout = timeout_ms / 1000 if timeout_ms is not None else config.http.timeout
    # Auth is carried per-request by the token-provider hook on the httpx client below, so the SDK's
    # own api_key is left unset.
    client = Mistral(
        api_key=None,
        server=server,
        server_url=resolved_server_url,
        url_params=url_params,
        timeout_ms=timeout_ms,
        client=_get_sync_client(
            timeout=timeout,
            token_provider=provider,
            server_url=resolved_server_url,
            use_executor_credentials=use_executor_credentials,
        ),
        async_client=_get_async_client(
            timeout=timeout,
            token_provider=provider,
            server_url=resolved_server_url,
            use_executor_credentials=use_executor_credentials,
        ),
    )
    _configure_client_telemetry(client)
    return client


def _configure_client_telemetry(client: Mistral) -> None:
    """Route Mistral SDK spans to the workflow's global OTel provider."""
    if not config.common.otel_enabled:
        return
    try:
        # Note: redaction is set to false as the SDK can't apply it to the global provider
        # so it logs a warning instead. Redaction is handled when defining the global
        # provider exporter
        configure_telemetry(client, provider="global", redaction=False)
    except Exception as exc:
        logger.warning("Failed to configure Mistral SDK telemetry", **extract_error_context(exc), exc_info=exc)


_TargetModel = TypeVar("_TargetModel", bound=BaseModel)


def translate_model(target_cls: Type[_TargetModel], source: BaseModel) -> _TargetModel:
    """Translate a protocol model into a worker_client (Speakeasy-generated) model, or vice-versa.

    A translation layer is required because the Pydantic models in `protocol/v1/` and the ones
    Speakeasy generates in `worker_client/models/` are not strictly equivalent: Speakeasy
    serialises `uuid` and `datetime` fields as `str`, while the protocol models use native Python
    types. Using `model_dump(mode="json")` normalises every field to JSON-safe primitives before
    re-validating into the target class, ensuring the two model families stay interoperable without
    manual field mapping.

    This translation layer is temporary. The long-term fix is to move `protocol/` out of
    `workflow_sdk` into `abraxas` and have `workflow_sdk` consume Speakeasy-generated models
    directly, which will eliminate the type mismatch and make this helper unnecessary.
    See WFL-468 for details.
    """
    return target_cls.model_validate(source.model_dump(mode="json"))
