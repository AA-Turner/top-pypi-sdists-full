"""Low-level async REST client for runta-api."""

from __future__ import annotations

from collections.abc import Awaitable, Mapping, Sequence
from pathlib import Path
import time
import tarfile
from typing import Any, Callable
from uuid import uuid4

import asyncio
import ssl

import aiohttp
import certifi
import httpx
from yarl import URL

import runta as _public

from .user_agent import USER_AGENT

from .async_file_io import _AsyncFileIO
from .http_limits import connection_limits
from .rest_tls import _RestTLS

from .openapi.api.checkpoints import (
    create_checkpoint as create_checkpoint_api,
)
from .openapi.api.checkpoints import (
    delete_checkpoint as delete_checkpoint_api,
)
from .openapi.api.checkpoints import (
    get_checkpoint as get_checkpoint_api,
)
from .openapi.api.checkpoints import (
    list_checkpoints as list_checkpoints_api,
)
from .openapi.api.files import read_runtime_file as read_runtime_file_api
from .openapi.api.files import write_runtime_file as write_runtime_file_api
from .openapi.api.health import healthz as healthz_api
from .openapi.api.runtimes import (
    create_runtime as create_runtime_api,
)
from .openapi.api.runtimes import (
    delete_runtime as delete_runtime_api,
)
from .openapi.api.runtimes import (
    get_runtime as get_runtime_api,
)
from .openapi.api.runtimes import (
    list_runtimes as list_runtimes_api,
)
from .openapi.api.runtimes import (
    patch_runtime as patch_runtime_api,
)
from .openapi.api.runtimes import (
    pause_runtime as pause_runtime_api,
)
from .openapi.api.runtimes import (
    resume_runtime as resume_runtime_api,
)
from .openapi.api.runtimes import (
    start_runtime as start_runtime_api,
)
from .openapi.api.runtimes import (
    stop_runtime as stop_runtime_api,
)
from .openapi.api.secrets import (
    delete_secret as delete_secret_api,
)
from .openapi.api.secrets import (
    get_secret as get_secret_api,
)
from .openapi.api.secrets import (
    list_secrets as list_secrets_api,
)
from .openapi.api.secrets import (
    set_secret as set_secret_api,
)
from .openapi.client import AuthenticatedClient
from .openapi.models import (
    CreateCheckpointRequest,
    CreateCheckpointRequestKind,
    SetSecretRequest,
)
from .openapi.types import UNSET, Response
from .openapi.types import File as OpenApiFile
from .pagination import LIST_PAGE_LIMIT, ListPaginationState
from .retry import (
    http_retry_delay,
    read_retry_deadline,
    is_revision_conflict,
    patch_matches,
    retry_async,
    retryable_http_error,
    retryable_delete_error,
)
from .transport import (
    checkpoint_info,
    create_runtime_request,
    patch_runtime_request,
    runtime_info,
    unwrap_response,
)


class _AsyncHttpClient:
    """Adapter around the generated OpenAPI client."""

    def __init__(
        self,
        endpoint: str,
        token: str,
        timeout: float = 30.0,
        retry_max_attempts: int = 16,
        connection_pool_maxsize: int | None = 250,
        file_io_workers: int | None = None,
    ) -> None:
        from .streaming_transfer import _AsyncWebSocketTLS

        self._websocket_tls = _AsyncWebSocketTLS(self._bind_loop)
        self._file_io = _AsyncFileIO(file_io_workers, self._bind_loop)
        self.endpoint = endpoint.rstrip("/")
        self.token = token
        self.timeout = timeout
        self.retry_max_attempts = retry_max_attempts
        # Validate without creating loop-bound resources.
        connection_limits(connection_pool_maxsize)
        self._pool_size = connection_pool_maxsize
        self._session: aiohttp.ClientSession | None = None
        self._loop: asyncio.AbstractEventLoop | None = None
        self._closed = False
        self._rest_tls: _RestTLS | None = None
        self._client = AuthenticatedClient(
            base_url=self.endpoint,
            token=token,
            headers={"user-agent": USER_AGENT},
        )

    def _check_loop(self) -> asyncio.AbstractEventLoop:
        loop = asyncio.get_running_loop()
        if self._loop is not None and loop is not self._loop:
            raise RuntimeError(
                "AsyncRunta must be used and closed in its owning event loop"
            )
        return loop

    def _bind_loop(self) -> asyncio.AbstractEventLoop:
        loop = self._check_loop()
        if self._closed:
            raise RuntimeError("AsyncRunta is closed")
        self._loop = loop
        return loop

    def _get_session(self) -> aiohttp.ClientSession:
        loop = self._bind_loop()
        if self._session is None:
            connector = aiohttp.TCPConnector(
                limit=0 if self._pool_size is None else self._pool_size,
                limit_per_host=0,
                keepalive_timeout=30.0,
                ssl=ssl.create_default_context(cafile=certifi.where()),
            )
            self._session = aiohttp.ClientSession(
                connector=connector,
                trust_env=False,
                auto_decompress=False,
                # Match httpx cookie handling for endpoints using IP addresses.
                cookie_jar=aiohttp.CookieJar(unsafe=True),
            )
            # aiohttp 3.14 otherwise retries broken persistent connections.
            # Only the SDK may spend the operation's attempt budget.
            self._session._retry_connection = False
            self._loop = loop
        return self._session

    async def close(self) -> None:
        if self._closed:
            return
        self._check_loop()
        self._closed = True
        self._file_io.close()
        try:
            if self._session is not None:
                await self._session.close()
        finally:
            self._websocket_tls.close()
            if self._rest_tls is not None:
                self._rest_tls.close()

    def _build_request(self, kwargs: dict[str, Any], timeout: float) -> httpx.Request:
        kwargs = dict(kwargs)
        url = httpx.URL(self.endpoint + "/").join(str(kwargs.pop("url")).lstrip("/"))
        headers = httpx.Headers({"Accept": "*/*", "Accept-Encoding": "gzip, deflate"})
        headers.update(self._client._headers)
        headers["Authorization"] = f"Bearer {self.token}"
        headers.update(kwargs.pop("headers", {}))
        return httpx.Request(
            url=url,
            headers=headers,
            extensions={
                "timeout": dict.fromkeys(("connect", "read", "write", "pool"), timeout)
            },
            **kwargs,
        )

    async def _send_request(
        self, request: httpx.Request, timeout: float
    ) -> httpx.Response:
        session = self._get_session()
        tls_options: dict[str, Any] = {}
        if request.url.scheme == "https":
            if self._rest_tls is None:
                self._rest_tls = _RestTLS()
            tls_options["ssl"] = self._rest_tls.context(
                request.url.host, request.url.port or 443
            )
        async with session.request(
            request.method,
            URL(str(request.url), encoded=True),
            headers=request.headers.multi_items(),
            data=request.read(),
            allow_redirects=False,
            timeout=aiohttp.ClientTimeout(total=timeout, ceil_threshold=float("inf")),
            **tls_options,
        ) as response:
            content = await response.read()
            return httpx.Response(
                response.status,
                headers=response.raw_headers,
                content=content,
                request=request,
            )

    async def _send(
        self, request_kwargs: dict[str, Any], *, _timeout: float | None = None
    ) -> httpx.Response:
        timeout = min(self.timeout, _timeout) if _timeout is not None else self.timeout
        if timeout <= 0:
            raise _public.ApiError(
                "HTTP request failed: operation deadline exceeded"
            ) from TimeoutError()
        request = self._build_request(request_kwargs, timeout)
        try:
            return await self._send_request(request, timeout)
        except (
            aiohttp.ClientError,
            asyncio.TimeoutError,
            TimeoutError,
            httpx.DecodingError,
        ) as exc:
            raise _public.ApiError(f"HTTP request failed: {exc}") from exc

    async def _request(
        self,
        func: Callable[..., Awaitable[Response[Any]]],
        *args: Any,
        _timeout: float | None = None,
        **kwargs: Any,
    ) -> Response[Any]:
        module = _endpoint_module(func)
        request_kwargs = module._get_kwargs(*args, **kwargs)
        response = await self._send(request_kwargs, _timeout=_timeout)
        try:
            return module._build_response(client=self._client, response=response)
        except (AttributeError, KeyError, TypeError, ValueError):
            if response.status_code >= 400:
                return Response(
                    status_code=response.status_code,
                    content=response.content,
                    headers=response.headers,
                    parsed=None,
                )
            raise

    async def _call(
        self, func: Callable[..., Awaitable[Response[Any]]], *args: Any, **kwargs: Any
    ) -> Any:
        return unwrap_response(await self._request(func, *args, **kwargs))

    async def _retry_read(
        self,
        operation: Callable[[float | None], Any],
        *,
        name: str,
        deadline: float | None = None,
    ) -> Any:
        return await retry_async(
            operation,
            name=name,
            attempts=self.retry_max_attempts,
            retryable=retryable_http_error,
            deadline=read_retry_deadline() if deadline is None else deadline,
            delay=http_retry_delay,
        )

    async def health(self) -> bool:
        unwrap_response(await self._request(healthz_api.asyncio_detailed))
        return True

    async def create_runtime(
        self,
        name: str | None = None,
        *,
        checkpoint_id: str | None = None,
        vcpus: int = 1,
        memory_mib: int = 1024,
        memory_max_mib: int | None = None,
        resources: _public.CreateRuntimeResources | Mapping[str, Any] | None = None,
        ingress_specs: Sequence[dict[str, Any]] | None = None,
        egress_policy: _public.EgressPolicy | None = None,
        auto_shutdown_after_secs: int | None = None,
        auto_delete_after_secs: int | None = None,
        tcp_allowlist: Sequence[str] | None = None,
        idle_suspend_after_secs: int | None = None,
    ) -> _public.RuntimeInfo:
        body = create_runtime_request(
            name,
            checkpoint_id=checkpoint_id,
            vcpus=vcpus,
            memory_mib=memory_mib,
            memory_max_mib=memory_max_mib,
            resources=resources,
            ingress_specs=ingress_specs,
            egress_policy=egress_policy,
            auto_shutdown_after_secs=auto_shutdown_after_secs,
            auto_delete_after_secs=auto_delete_after_secs,
            tcp_allowlist=tcp_allowlist,
            idle_suspend_after_secs=idle_suspend_after_secs,
        )
        key = str(uuid4())
        data = await retry_async(
            lambda remaining: self._call(
                create_runtime_api.asyncio_detailed,
                body=body,
                idempotency_key=key,
                _timeout=remaining,
            ),
            name="create runtime",
            attempts=self.retry_max_attempts,
            retryable=retryable_http_error,
            deadline=time.monotonic() + 480,
        )
        return runtime_info(data)

    async def list_runtimes(
        self, status: str | None = None
    ) -> list[_public.RuntimeInfo]:
        deadline = read_retry_deadline()
        state = ListPaginationState()
        runtimes: list[_public.RuntimeInfo] = []
        while True:
            request_kwargs = list_runtimes_api._get_kwargs(
                status=status if status is not None else UNSET,
                limit=LIST_PAGE_LIMIT,
                after=state.after if state.after is not None else UNSET,
            )
            payload = await self._retry_read(
                lambda remaining: self._request_list_payload(
                    list_runtimes_api, request_kwargs, _timeout=remaining
                ),
                name="list runtimes",
                deadline=deadline,
            )
            data, has_more = state.consume(payload, operation="listRuntimes")
            runtimes.extend(_public.RuntimeInfo.from_json(dict(item)) for item in data)
            if not has_more:
                return runtimes

    async def get_runtime(self, runtime_id: str) -> _public.RuntimeInfo:
        data = await self._retry_read(
            lambda remaining: self._get_runtime_model(runtime_id, _timeout=remaining),
            name="get runtime",
        )
        return runtime_info(data)

    async def _get_runtime_model(
        self, runtime_id: str, *, _timeout: float | None = None
    ) -> Any:
        return await self._call(
            get_runtime_api.asyncio_detailed, runtime_id, _timeout=_timeout
        )

    async def delete_runtime(self, runtime_id: str) -> None:
        deadline = time.monotonic() + 480

        async def delete(remaining: float | None) -> None:
            try:
                revision = (
                    await self._get_runtime_model(runtime_id, _timeout=remaining)
                ).revision
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError("delete runtime exceeded its operation deadline")
                await self._call(
                    delete_runtime_api.asyncio_detailed,
                    runtime_id,
                    expected_revision=revision,
                    _timeout=remaining,
                )
            except _public.ApiError as error:
                if error.status_code != 404:
                    raise

        await retry_async(
            delete,
            name="delete runtime",
            attempts=self.retry_max_attempts,
            retryable=retryable_delete_error,
            deadline=deadline,
            delay=http_retry_delay,
        )

    async def patch_runtime(
        self,
        runtime_id: str,
        *,
        resources: _public.PatchRuntimeResources | Mapping[str, Any] | None = None,
        egress_policy: _public.EgressPolicy | None = None,
        auto_shutdown_after_secs: int | None = None,
        auto_delete_after_secs: int | None = None,
        tcp_allowlist: Sequence[str] | None = None,
    ) -> _public.RuntimeInfo:
        deadline = time.monotonic() + 480
        body = patch_runtime_request(
            resources=resources,
            egress_policy=egress_policy,
            auto_shutdown_after_secs=auto_shutdown_after_secs,
            auto_delete_after_secs=auto_delete_after_secs,
            tcp_allowlist=tcp_allowlist,
        )
        revision: int | None = None

        async def patch(remaining: float | None) -> Any:
            nonlocal revision
            if revision is None:
                revision = (
                    await self._get_runtime_model(runtime_id, _timeout=remaining)
                ).revision
            try:
                return await self._call(
                    patch_runtime_api.asyncio_detailed,
                    runtime_id,
                    expected_revision=revision,
                    body=body,
                    _timeout=remaining,
                )
            except _public.ApiError as error:
                if is_revision_conflict(error):
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        raise
                    current = await self._get_runtime_model(
                        runtime_id, _timeout=remaining
                    )
                    if patch_matches(body, current):
                        return current
                raise

        data = await retry_async(
            patch,
            name="patch runtime",
            attempts=self.retry_max_attempts,
            retryable=retryable_http_error,
            deadline=deadline,
        )
        return runtime_info(data)

    async def read_file(self, runtime_id: str, path: str) -> bytes:
        async def read(remaining: float | None) -> bytes:
            response = await self._request(
                read_runtime_file_api.asyncio_detailed,
                runtime_id,
                path=path,
                _timeout=remaining,
            )
            unwrap_response(response)
            return response.content

        return await self._retry_read(read, name="read file")

    async def write_file(
        self, runtime_id: str, path: str, content: bytes | str
    ) -> None:
        if isinstance(content, str):
            content = content.encode()
        await self._call(
            write_runtime_file_api.asyncio_detailed,
            runtime_id,
            body=OpenApiFile(payload=content),
            path=path,
        )

    async def upload_path(self, runtime_id: str, src: Path, dst: str) -> None:
        from .streaming_transfer import async_upload_path

        await async_upload_path(
            self.endpoint,
            self.token,
            runtime_id,
            src,
            dst,
            timeout=self.timeout,
            attempts=self.retry_max_attempts,
            _tls=self._websocket_tls,
        )

    async def download_path(
        self,
        runtime_id: str,
        src: str,
        dst: Path,
        *,
        destination_is_directory: bool,
    ) -> None:
        from .streaming_transfer import async_download_path

        await async_download_path(
            self.endpoint,
            self.token,
            runtime_id,
            src,
            dst,
            destination_is_directory=destination_is_directory,
            timeout=self.timeout,
            attempts=self.retry_max_attempts,
            _tls=self._websocket_tls,
            _file_io=self._file_io,
        )

    async def download_dir_contents(
        self,
        runtime_id: str,
        src: str,
        dst: Path,
        *,
        paths: Sequence[str] | None = None,
        filter: Callable[[tarfile.TarInfo, str], tarfile.TarInfo | None] | None = None,
    ) -> None:
        from .streaming_transfer import async_download_dir_contents

        await async_download_dir_contents(
            self.endpoint,
            self.token,
            runtime_id,
            src,
            dst,
            paths=paths,
            filter=filter,
            timeout=self.timeout,
            attempts=self.retry_max_attempts,
            _tls=self._websocket_tls,
            _file_io=self._file_io,
        )

    async def update_runtime_status(
        self, runtime_id: str, action: str
    ) -> _public.RuntimeInfo:
        endpoint = {
            "boot": start_runtime_api.asyncio_detailed,
            "pause": pause_runtime_api.asyncio_detailed,
            "resume": resume_runtime_api.asyncio_detailed,
            "shutdown": stop_runtime_api.asyncio_detailed,
        }[action]
        revision = (await self._get_runtime_model(runtime_id)).revision
        return runtime_info(
            await self._call(endpoint, runtime_id, expected_revision=revision)
        )

    async def execute(
        self,
        runtime_id: str,
        command: str,
        args: Sequence[str] = (),
        *,
        env: Mapping[str, str] | None = None,
        stdin: bytes | str | None = None,
        timeout: float | None = None,
        max_output_bytes: int | None = None,
        idle_timeout: float | None = None,
    ) -> _public.CommandResult:
        from .streaming_transfer import async_execute

        return await async_execute(
            self.endpoint,
            self.token,
            runtime_id,
            command,
            list(args),
            env=dict(env) if env else None,
            stdin=stdin,
            timeout=timeout,
            max_output_bytes=max_output_bytes,
            connect_timeout=self.timeout,
            idle_timeout=idle_timeout,
            _tls=self._websocket_tls,
        )

    async def set_secret(
        self, name: str, value: str, cache_ttl_secs: int = 0
    ) -> _public.SecretInfo:
        data = await self._call(
            set_secret_api.asyncio_detailed,
            name,
            body=SetSecretRequest(value=value, cache_ttl_secs=cache_ttl_secs),
        )
        return _public.SecretInfo.from_json(data.to_dict())

    async def list_secrets(self) -> list[_public.SecretInfo]:
        data = await self._retry_read(
            lambda remaining: self._call(
                list_secrets_api.asyncio_detailed, _timeout=remaining
            ),
            name="list secrets",
        )
        return [_public.SecretInfo.from_json(item.to_dict()) for item in data]

    async def get_secret(self, secret_id: str) -> _public.SecretInfo:
        data = await self._retry_read(
            lambda remaining: self._call(
                get_secret_api.asyncio_detailed, secret_id, _timeout=remaining
            ),
            name="get secret",
        )
        return _public.SecretInfo.from_json(data.to_dict())

    async def delete_secret(self, secret_id: str) -> None:
        await self._call(delete_secret_api.asyncio_detailed, secret_id)

    async def create_checkpoint(
        self,
        runtime_id: str,
        name: str | None = None,
        kind: str = "full",
    ) -> _public.CheckpointInfo:
        data = await self._call(
            create_checkpoint_api.asyncio_detailed,
            runtime_id,
            body=CreateCheckpointRequest(
                name=name if name is not None else UNSET,
                kind=CreateCheckpointRequestKind(kind),
            ),
        )
        return checkpoint_info(data)

    async def list_checkpoints(self) -> list[_public.CheckpointInfo]:
        deadline = read_retry_deadline()
        state = ListPaginationState()
        checkpoints: list[_public.CheckpointInfo] = []
        while True:
            request_kwargs = list_checkpoints_api._get_kwargs(
                limit=LIST_PAGE_LIMIT,
                after=state.after if state.after is not None else UNSET,
            )
            payload = await self._retry_read(
                lambda remaining: self._request_list_payload(
                    list_checkpoints_api, request_kwargs, _timeout=remaining
                ),
                name="list checkpoints",
                deadline=deadline,
            )
            data, has_more = state.consume(payload, operation="listCheckpoints")
            checkpoints.extend(
                _public.CheckpointInfo.from_json(dict(item)) for item in data
            )
            if not has_more:
                return checkpoints

    async def get_checkpoint(self, checkpoint_id: str) -> _public.CheckpointInfo:
        data = await self._retry_read(
            lambda remaining: self._call(
                get_checkpoint_api.asyncio_detailed, checkpoint_id, _timeout=remaining
            ),
            name="get checkpoint",
        )
        return checkpoint_info(data)

    async def delete_checkpoint(self, checkpoint_id: str) -> None:
        await self._call(delete_checkpoint_api.asyncio_detailed, checkpoint_id)

    async def _request_list_payload(
        self,
        module: Any,
        request_kwargs: dict[str, Any],
        *,
        _timeout: float | None = None,
    ) -> object:
        response = await self._send(request_kwargs, _timeout=_timeout)
        if response.status_code >= 400:
            try:
                parsed = module._build_response(client=self._client, response=response)
            except (AttributeError, KeyError, TypeError, ValueError):
                parsed = Response(
                    status_code=response.status_code,
                    content=response.content,
                    headers=response.headers,
                    parsed=None,
                )
            unwrap_response(parsed)
        try:
            return response.json()
        except ValueError as exc:
            raise _public.ApiError("List response was not valid JSON") from exc


def _endpoint_module(func: Callable[..., Awaitable[Response[Any]]]) -> Any:
    return __import__(func.__module__, fromlist=["_build_response", "_get_kwargs"])
