"""Low-level synchronous REST client for runta-api."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from pathlib import Path
import time
import tarfile
from typing import Any, Callable
from uuid import uuid4

import httpx

import runta as _public

from .user_agent import USER_AGENT

from .http_limits import connection_limits

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
    retry_sync,
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


class _SyncHttpClient:
    """Adapter around the generated OpenAPI client."""

    def __init__(
        self,
        endpoint: str,
        token: str,
        timeout: float = 30.0,
        retry_max_attempts: int = 16,
        connection_pool_maxsize: int | None = 250,
    ) -> None:
        from .streaming_transfer import _WebSocketTLS

        self._websocket_tls = _WebSocketTLS()
        self.endpoint = endpoint.rstrip("/")
        self.token = token
        self.timeout = timeout
        self.retry_max_attempts = retry_max_attempts
        self._client = AuthenticatedClient(
            base_url=self.endpoint,
            token=token,
            timeout=httpx.Timeout(timeout),
            headers={"user-agent": USER_AGENT},
            httpx_args={
                "trust_env": False,
                "limits": connection_limits(connection_pool_maxsize),
            },
        )

    def close(self) -> None:
        self._client.get_httpx_client().close()

    def _request(
        self,
        func: Callable[..., Response[Any]],
        *args: Any,
        _timeout: float | None = None,
        **kwargs: Any,
    ) -> Response[Any]:
        module = _endpoint_module(func)
        request_kwargs = module._get_kwargs(*args, **kwargs)
        try:
            response = self._client.get_httpx_client().request(
                **request_kwargs,
                timeout=min(self.timeout, _timeout)
                if _timeout is not None
                else self.timeout,
            )
        except httpx.HTTPError as exc:
            raise _public.ApiError(f"HTTP request failed: {exc}") from exc
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

    def _call(
        self, func: Callable[..., Response[Any]], *args: Any, **kwargs: Any
    ) -> Any:
        return unwrap_response(self._request(func, *args, **kwargs))

    def _retry_read(
        self,
        operation: Callable[[float | None], Any],
        *,
        name: str,
        deadline: float | None = None,
    ) -> Any:
        return retry_sync(
            operation,
            name=name,
            attempts=self.retry_max_attempts,
            retryable=retryable_http_error,
            deadline=read_retry_deadline() if deadline is None else deadline,
            delay=http_retry_delay,
        )

    def health(self) -> bool:
        unwrap_response(self._request(healthz_api.sync_detailed))
        return True

    def create_runtime(
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
        data = retry_sync(
            lambda remaining: self._call(
                create_runtime_api.sync_detailed,
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

    def list_runtimes(self, status: str | None = None) -> list[_public.RuntimeInfo]:
        deadline = read_retry_deadline()
        state = ListPaginationState()
        runtimes: list[_public.RuntimeInfo] = []
        while True:
            request_kwargs = list_runtimes_api._get_kwargs(
                status=status if status is not None else UNSET,
                limit=LIST_PAGE_LIMIT,
                after=state.after if state.after is not None else UNSET,
            )
            payload = self._retry_read(
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

    def get_runtime(self, runtime_id: str) -> _public.RuntimeInfo:
        data = self._retry_read(
            lambda remaining: self._get_runtime_model(runtime_id, _timeout=remaining),
            name="get runtime",
        )
        return runtime_info(data)

    def _get_runtime_model(
        self, runtime_id: str, *, _timeout: float | None = None
    ) -> Any:
        return self._call(get_runtime_api.sync_detailed, runtime_id, _timeout=_timeout)

    def delete_runtime(self, runtime_id: str) -> None:
        deadline = time.monotonic() + 480

        def delete(remaining: float | None) -> None:
            try:
                revision = (
                    self._get_runtime_model(runtime_id, _timeout=remaining)
                ).revision
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError("delete runtime exceeded its operation deadline")
                self._call(
                    delete_runtime_api.sync_detailed,
                    runtime_id,
                    expected_revision=revision,
                    _timeout=remaining,
                )
            except _public.ApiError as error:
                if error.status_code != 404:
                    raise

        retry_sync(
            delete,
            name="delete runtime",
            attempts=self.retry_max_attempts,
            retryable=retryable_delete_error,
            deadline=deadline,
            delay=http_retry_delay,
        )

    def patch_runtime(
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

        def patch(remaining: float | None) -> Any:
            nonlocal revision
            if revision is None:
                revision = self._get_runtime_model(
                    runtime_id, _timeout=remaining
                ).revision
            try:
                return self._call(
                    patch_runtime_api.sync_detailed,
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
                    current = self._get_runtime_model(runtime_id, _timeout=remaining)
                    if patch_matches(body, current):
                        return current
                raise

        data = retry_sync(
            patch,
            name="patch runtime",
            attempts=self.retry_max_attempts,
            retryable=retryable_http_error,
            deadline=deadline,
        )
        return runtime_info(data)

    def read_file(self, runtime_id: str, path: str) -> bytes:
        def read(remaining: float | None) -> bytes:
            response = self._request(
                read_runtime_file_api.sync_detailed,
                runtime_id,
                path=path,
                _timeout=remaining,
            )
            unwrap_response(response)
            return response.content

        return self._retry_read(read, name="read file")

    def write_file(self, runtime_id: str, path: str, content: bytes | str) -> None:
        if isinstance(content, str):
            content = content.encode()
        self._call(
            write_runtime_file_api.sync_detailed,
            runtime_id,
            body=OpenApiFile(payload=content),
            path=path,
        )

    def upload_path(self, runtime_id: str, src: Path, dst: str) -> None:
        from .streaming_transfer import upload_path

        upload_path(
            self.endpoint,
            self.token,
            runtime_id,
            src,
            dst,
            timeout=self.timeout,
            attempts=self.retry_max_attempts,
            _tls=self._websocket_tls,
        )

    def download_path(
        self,
        runtime_id: str,
        src: str,
        dst: Path,
        *,
        destination_is_directory: bool,
    ) -> None:
        from .streaming_transfer import download_path

        download_path(
            self.endpoint,
            self.token,
            runtime_id,
            src,
            dst,
            destination_is_directory=destination_is_directory,
            timeout=self.timeout,
            attempts=self.retry_max_attempts,
            _tls=self._websocket_tls,
        )

    def download_dir_contents(
        self,
        runtime_id: str,
        src: str,
        dst: Path,
        *,
        paths: Sequence[str] | None = None,
        filter: Callable[[tarfile.TarInfo, str], tarfile.TarInfo | None] | None = None,
    ) -> None:
        from .streaming_transfer import download_dir_contents

        download_dir_contents(
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
        )

    def update_runtime_status(
        self, runtime_id: str, action: str
    ) -> _public.RuntimeInfo:
        endpoint = {
            "boot": start_runtime_api.sync_detailed,
            "pause": pause_runtime_api.sync_detailed,
            "resume": resume_runtime_api.sync_detailed,
            "shutdown": stop_runtime_api.sync_detailed,
        }[action]
        revision = self._get_runtime_model(runtime_id).revision
        return runtime_info(
            self._call(endpoint, runtime_id, expected_revision=revision)
        )

    def execute(
        self,
        runtime_id: str,
        command: str,
        args: Sequence[str] = (),
        *,
        env: Mapping[str, str] | None = None,
        stdin: bytes | str | None = None,
        timeout: float | None = None,
        cwd: str | None = None,
        max_output_bytes: int | None = None,
        idle_timeout: float | None = None,
    ) -> _public.CommandResult:
        from .streaming_transfer import execute

        return execute(
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

    def set_secret(
        self, name: str, value: str, cache_ttl_secs: int = 0
    ) -> _public.SecretInfo:
        data = self._call(
            set_secret_api.sync_detailed,
            name,
            body=SetSecretRequest(value=value, cache_ttl_secs=cache_ttl_secs),
        )
        return _public.SecretInfo.from_json(data.to_dict())

    def list_secrets(self) -> list[_public.SecretInfo]:
        data = self._retry_read(
            lambda remaining: self._call(
                list_secrets_api.sync_detailed, _timeout=remaining
            ),
            name="list secrets",
        )
        return [_public.SecretInfo.from_json(item.to_dict()) for item in data]

    def get_secret(self, secret_id: str) -> _public.SecretInfo:
        data = self._retry_read(
            lambda remaining: self._call(
                get_secret_api.sync_detailed, secret_id, _timeout=remaining
            ),
            name="get secret",
        )
        return _public.SecretInfo.from_json(data.to_dict())

    def delete_secret(self, secret_id: str) -> None:
        self._call(delete_secret_api.sync_detailed, secret_id)

    def create_checkpoint(
        self, runtime_id: str, name: str | None = None, kind: str = "full"
    ) -> _public.CheckpointInfo:
        data = self._call(
            create_checkpoint_api.sync_detailed,
            runtime_id,
            body=CreateCheckpointRequest(
                name=name if name is not None else UNSET,
                kind=CreateCheckpointRequestKind(kind),
            ),
        )
        return checkpoint_info(data)

    def list_checkpoints(self) -> list[_public.CheckpointInfo]:
        deadline = read_retry_deadline()
        state = ListPaginationState()
        checkpoints: list[_public.CheckpointInfo] = []
        while True:
            request_kwargs = list_checkpoints_api._get_kwargs(
                limit=LIST_PAGE_LIMIT,
                after=state.after if state.after is not None else UNSET,
            )
            payload = self._retry_read(
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

    def get_checkpoint(self, checkpoint_id: str) -> _public.CheckpointInfo:
        data = self._retry_read(
            lambda remaining: self._call(
                get_checkpoint_api.sync_detailed, checkpoint_id, _timeout=remaining
            ),
            name="get checkpoint",
        )
        return checkpoint_info(data)

    def delete_checkpoint(self, checkpoint_id: str) -> None:
        self._call(delete_checkpoint_api.sync_detailed, checkpoint_id)

    def _request_list_payload(
        self,
        module: Any,
        request_kwargs: dict[str, Any],
        *,
        _timeout: float | None = None,
    ) -> object:
        try:
            response = self._client.get_httpx_client().request(
                **request_kwargs,
                timeout=min(self.timeout, _timeout)
                if _timeout is not None
                else self.timeout,
            )
        except httpx.HTTPError as exc:
            raise _public.ApiError(f"HTTP request failed: {exc}") from exc
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


def _endpoint_module(func: Callable[..., Response[Any]]) -> Any:
    return __import__(func.__module__, fromlist=["_build_response", "_get_kwargs"])
