import warnings
from typing import Any, Callable, NamedTuple, Type, TypeVar

import httpx
from mistralai.client import Mistral
from mistralai.extra.observability.telemetry import configure_telemetry
from pydantic import BaseModel

from mistralai.workflows._mistral_http import MISTRAL_HTTP, HttpBackend
from mistralai.workflows._version import USER_AGENT
from mistralai.workflows.core import _http_transport as http_transport
from mistralai.workflows.core._logger import get_logger
from mistralai.workflows.core.auth import RunAs, TokenProvider, get_token_provider
from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.logging import extract_error_context
from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context
from mistralai.workflows.exceptions import WorkflowError
from mistralai.workflows.hooks.cross_origin_auth_guard import (
    AsyncCrossOriginAuthGuardHook,
    CrossOriginAuthGuardHook,
)
from mistralai.workflows.hooks.default_identity_warning_hook import (
    CallSite,
    caller_call_site,
    warn_default_identity,
    warn_default_identity_async,
)
from mistralai.workflows.hooks.executor_credentials_hook import (
    _EXECUTOR_POLICY,
    AsyncExecutorCredentialsHook,
    SyncExecutorCredentialsHook,
)
from mistralai.workflows.hooks.metadata_hook import inject_metadata, inject_metadata_async
from mistralai.workflows.hooks.token_provider_hook import (
    AsyncTokenProviderHook,
    TokenProviderHook,
)

logger = get_logger(__name__)


def _get_headers(
    headers: httpx.Headers | dict[str, str] | None = None,
    http: HttpBackend = MISTRAL_HTTP,
) -> httpx.Headers:
    headers = (
        headers
        if isinstance(headers, http.Headers)
        else http.Headers(headers if headers is not None else config.worker.mistral_api_headers or {})
    )
    # Authorization is set per-request by the auth/executor hook, never statically here.
    headers.setdefault("User-Agent", USER_AGENT)
    return headers


def _resolve_run_as(use_executor_credentials: bool, run_as: RunAs | None) -> RunAs | None:
    if run_as is None:
        return RunAs.EXECUTOR if use_executor_credentials else None
    if use_executor_credentials:
        raise ValueError("run_as conflicts with use_executor_credentials=True")
    return RunAs(run_as)


class _HookVariants(NamedTuple):
    metadata: Callable
    auth: type[AsyncTokenProviderHook] | type[TokenProviderHook]
    executor: type[AsyncExecutorCredentialsHook] | type[SyncExecutorCredentialsHook]
    guard: type[AsyncCrossOriginAuthGuardHook] | type[CrossOriginAuthGuardHook]
    default_identity_warning: Callable


_ASYNC_HOOKS = _HookVariants(
    metadata=inject_metadata_async,
    auth=AsyncTokenProviderHook,
    executor=AsyncExecutorCredentialsHook,
    guard=AsyncCrossOriginAuthGuardHook,
    default_identity_warning=warn_default_identity_async,
)
_SYNC_HOOKS = _HookVariants(
    metadata=inject_metadata,
    auth=TokenProviderHook,
    executor=SyncExecutorCredentialsHook,
    guard=CrossOriginAuthGuardHook,
    default_identity_warning=warn_default_identity,
)


def _get_hooks(
    is_async: bool,
    server_url: str | None = None,
    token_provider: TokenProvider | None = None,
    run_as: RunAs | None = None,
    executor_credentials_server_url: str | None = None,
    executor_credentials_headers: dict[str, str] | None = None,
    v4_default_identity_call_site: CallSite | None = None,
) -> dict[str, list]:
    hooks = _ASYNC_HOOKS if is_async else _SYNC_HOOKS
    request_hooks: list = [hooks.metadata]
    if run_as == RunAs.AUTO:
        request_hooks.append(
            hooks.executor(
                server_url=executor_credentials_server_url or server_url or "",
                token_provider=token_provider,
                run_as=run_as,
                headers=executor_credentials_headers,
            )
        )
    elif run_as == RunAs.EXECUTOR:
        if not server_url:
            raise WorkflowError(
                f"{_EXECUTOR_POLICY} requires server_url",
                non_retryable=True,
            )
        logger.info("ExecutorCredentialsHook registered, using the executor's identity")
        request_hooks.append(
            hooks.executor(
                server_url=executor_credentials_server_url or server_url,
                token_provider=token_provider,
                run_as=run_as,
                headers=executor_credentials_headers,
            )
        )
    elif token_provider is not None:
        request_hooks.append(hooks.auth(token_provider))
    if v4_default_identity_call_site is not None:
        request_hooks.append(hooks.default_identity_warning(v4_default_identity_call_site))
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
    run_as: RunAs | None = None,
    executor_credentials_server_url: str | None = None,
    executor_credentials_headers: dict[str, str] | None = None,
    _v4_default_identity_call_site: CallSite | None = None,
    _http: HttpBackend = MISTRAL_HTTP,
) -> httpx.Client:
    if token_provider is None:
        token_provider = get_token_provider(api_key)
    run_as = _resolve_run_as(use_executor_credentials, run_as)
    return _http.Client(
        timeout=timeout if timeout is not None else config.http.timeout,
        verify=http_transport.verify(),
        headers=_get_headers(
            headers={} if run_as in (RunAs.AUTO, RunAs.EXECUTOR) and headers is None else headers,
            http=_http,
        ),
        follow_redirects=True,
        event_hooks=_get_hooks(
            is_async=False,
            server_url=server_url,
            token_provider=token_provider,
            run_as=run_as,
            executor_credentials_server_url=executor_credentials_server_url,
            executor_credentials_headers=executor_credentials_headers,
            v4_default_identity_call_site=_v4_default_identity_call_site,
        ),
        transport=http_transport.sync_transport(_http),
        mounts=http_transport.sync_mounts(_http),
        limits=http_transport.limits(_http),
    )


def _get_async_client(
    timeout: float | None = None,
    *,
    token_provider: TokenProvider | None = None,
    headers: httpx.Headers | dict[str, str] | None = None,
    server_url: str | None = None,
    use_executor_credentials: bool = False,
    api_key: str | None = None,
    run_as: RunAs | None = None,
    executor_credentials_server_url: str | None = None,
    executor_credentials_headers: dict[str, str] | None = None,
    _v4_default_identity_call_site: CallSite | None = None,
    _http: HttpBackend = MISTRAL_HTTP,
) -> httpx.AsyncClient:
    if token_provider is None:
        token_provider = get_token_provider(api_key)
    run_as = _resolve_run_as(use_executor_credentials, run_as)
    return _http.AsyncClient(
        timeout=timeout if timeout is not None else config.http.timeout,
        verify=http_transport.verify(),
        headers=_get_headers(
            headers={} if run_as in (RunAs.AUTO, RunAs.EXECUTOR) and headers is None else headers,
            http=_http,
        ),
        follow_redirects=True,
        event_hooks=_get_hooks(
            is_async=True,
            server_url=server_url,
            token_provider=token_provider,
            run_as=run_as,
            executor_credentials_server_url=executor_credentials_server_url,
            executor_credentials_headers=executor_credentials_headers,
            v4_default_identity_call_site=_v4_default_identity_call_site,
        ),
        transport=http_transport.async_transport(_http),
        mounts=http_transport.async_mounts(_http),
        limits=http_transport.limits(_http),
    )


def get_async_client(*args: Any, **kwargs: Any) -> httpx.AsyncClient:
    warnings.warn(
        "get_async_client is deprecated and will be removed in a future version. Use _get_async_client instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    return _get_async_client(*args, **kwargs)


def should_use_executor_credentials() -> bool:
    """Return True when the current execution runs on behalf of a user (obo).

    Deprecated: removed in v4. Pass ``run_as=RunAs.AUTO`` to ``get_mistral_client`` instead.
    """
    warnings.warn(
        "should_use_executor_credentials() is deprecated and will be removed in v4; "
        "pass run_as=RunAs.AUTO to get_mistral_client instead.",
        FutureWarning,
        stacklevel=2,
    )
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
    *,
    run_as: RunAs | None = None,
    executor_credentials_server_url: str | None = None,
    executor_credentials_headers: dict[str, str] | None = None,
) -> Mistral:
    """Create a client whose identity policy is applied to each request.

    run_as=AUTO follows the current execution's on_behalf_of flag; DEPLOYMENT
    always uses the configured token provider. run_as=EXECUTOR always uses the
    executor and raises when the workflow is not on_behalf_of. Without run_as,
    use_executor_credentials selects deployment (False) or EXECUTOR (True);
    combining run_as with True is rejected. Both forms emit a FutureWarning where
    v4 behaves differently: use_executor_credentials is removed in v4, and the
    default becomes AUTO.

    AUTO requires workflow context at request time and uses deployment credentials
    only for non-OBO executions. Missing context, missing OBO execution tokens, and
    failed identity exchanges raise instead of falling back to deployment.
    Use DEPLOYMENT explicitly for requests outside a workflow execution.

    Executor token exchange defaults to the API URL and worker credentials. Set
    ``executor_credentials_server_url`` and ``executor_credentials_headers`` for an internal
    Abraxas endpoint with header authentication. These headers default to ``MISTRAL_API_HEADERS``
    and are only sent to the token-exchange endpoint, never to downstream executor API calls.
    Non-empty exchange headers replace API-key and token-provider authentication for the exchange.
    Pass ``executor_credentials_headers={}`` to use bearer authentication without worker headers.
    """
    if use_executor_credentials:
        warnings.warn(
            "use_executor_credentials=True is deprecated and will be removed in v4; "
            "pass run_as=RunAs.EXECUTOR instead.",
            FutureWarning,
            stacklevel=2,
        )
    v4_default_identity_call_site = caller_call_site(1) if run_as is None and not use_executor_credentials else None
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
            run_as=run_as,
            executor_credentials_server_url=executor_credentials_server_url,
            executor_credentials_headers=executor_credentials_headers,
            _v4_default_identity_call_site=v4_default_identity_call_site,
        ),
        async_client=_get_async_client(
            timeout=timeout,
            token_provider=provider,
            server_url=resolved_server_url,
            use_executor_credentials=use_executor_credentials,
            run_as=run_as,
            executor_credentials_server_url=executor_credentials_server_url,
            executor_credentials_headers=executor_credentials_headers,
            _v4_default_identity_call_site=v4_default_identity_call_site,
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
