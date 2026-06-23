import warnings
from typing import Any, Type, TypeVar

import httpx
import structlog
from mistralai.client import Mistral
from pydantic import BaseModel

from mistralai.workflows._version import USER_AGENT
from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.temporal.context_handler_interceptor import retrieve_context
from mistralai.workflows.exceptions import WorkflowError
from mistralai.workflows.hooks.executor_credentials_hook import (
    AsyncExecutorCredentialsHook,
    SyncExecutorCredentialsHook,
)
from mistralai.workflows.hooks.metadata_hook import inject_metadata, inject_metadata_async

logger = structlog.get_logger(__name__)

_HttpClientT = TypeVar("_HttpClientT", httpx.Client, httpx.AsyncClient)


def _get_headers(
    api_key: str | None = None,
    headers: httpx.Headers | dict[str, str] | None = None,
) -> httpx.Headers:
    headers = (
        headers
        if isinstance(headers, httpx.Headers)
        else httpx.Headers(headers or config.worker.mistral_api_headers or {})
    )
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"
    headers.setdefault("User-Agent", USER_AGENT)
    return headers


def _get_hooks(
    client_cls: type[httpx.AsyncClient] | type[httpx.Client],
    server_url: str | None = None,
    api_key: str | None = None,
    use_executor_credentials: bool = False,
) -> dict[str, list]:
    metadata_hook = inject_metadata_async if client_cls is httpx.AsyncClient else inject_metadata
    request_hooks: list = [metadata_hook]
    if use_executor_credentials:
        missing = [name for name, val in [("server_url", server_url), ("api_key", api_key)] if not val]
        if missing:
            raise WorkflowError(
                f"use_executor_credentials requires {', '.join(missing)}",
                non_retryable=True,
            )
        assert server_url and api_key
        hook_cls = AsyncExecutorCredentialsHook if client_cls is httpx.AsyncClient else SyncExecutorCredentialsHook
        logger.info("ExecutorCredentialsHook registered, using the executor's identity")
        request_hooks.append(hook_cls(server_url=server_url, api_key=api_key))
    return {"request": request_hooks}


def _get_client(
    client_cls: type[_HttpClientT],
    timeout: float = 60.0,
    api_key: str | None = None,
    headers: httpx.Headers | dict[str, str] | None = None,
    server_url: str | None = None,
    use_executor_credentials: bool = False,
) -> _HttpClientT:
    return client_cls(
        timeout=timeout,
        verify=config.common.ca_bundle or True,
        headers=_get_headers(api_key=api_key, headers=headers),
        follow_redirects=True,
        event_hooks=_get_hooks(
            client_cls, server_url=server_url, api_key=api_key, use_executor_credentials=use_executor_credentials
        ),
    )


def _get_sync_client(
    timeout: float = 60.0,
    api_key: str | None = None,
    headers: httpx.Headers | dict[str, str] | None = None,
    server_url: str | None = None,
    use_executor_credentials: bool = False,
) -> httpx.Client:
    return _get_client(
        httpx.Client,
        timeout=timeout,
        api_key=api_key,
        headers=headers,
        server_url=server_url,
        use_executor_credentials=use_executor_credentials,
    )


def _get_async_client(
    timeout: float = 60.0,
    api_key: str | None = None,
    headers: httpx.Headers | dict[str, str] | None = None,
    server_url: str | None = None,
    use_executor_credentials: bool = False,
) -> httpx.AsyncClient:
    return _get_client(
        httpx.AsyncClient,
        timeout=timeout,
        api_key=api_key,
        headers=headers,
        server_url=server_url,
        use_executor_credentials=use_executor_credentials,
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
) -> Mistral:
    if api_key is None:
        api_key_secret = config.common.mistral_api_key
        if api_key_secret is not None:
            api_key = api_key_secret.get_secret_value()
    resolved_server_url = server_url or config.worker.server_url
    timeout = timeout_ms / 1000 if timeout_ms is not None else 60.0
    return Mistral(
        api_key=api_key,
        server=server,
        server_url=resolved_server_url,
        url_params=url_params,
        timeout_ms=timeout_ms,
        client=_get_sync_client(
            timeout=timeout,
            api_key=api_key,
            server_url=resolved_server_url,
            use_executor_credentials=use_executor_credentials,
        ),
        async_client=_get_async_client(
            timeout=timeout,
            api_key=api_key,
            server_url=resolved_server_url,
            use_executor_credentials=use_executor_credentials,
        ),
    )


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
