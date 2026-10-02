"""SuperDoc runtime — thin layer over host transport.

Resolves the selected host process, holds a transport instance, and delegates invoke().
All protocol, process lifecycle, and I/O logic lives in transport.py and
protocol.py. The CLI compatibility path applies default_change_mode during argv
construction; the standalone document-host v0 path rejects that option.
"""

from __future__ import annotations

import os
from typing import Any, Dict, Literal, Optional, Tuple

from .embedded_cli import resolve_embedded_cli_path
from .embedded_document_host import resolve_embedded_document_host_path
from .errors import SuperDocError
from .generated.contract import OPERATION_INDEX
from .protocol import normalize_default_change_mode
from .transport import (
    DEFAULT_STDOUT_BUFFER_LIMIT_BYTES,
    DEFAULT_WATCHDOG_TIMEOUT_MS,
    AsyncHostTransport,
    SyncHostTransport,
)


def _resolve_runtime_process(
    env: Dict[str, str],
    document_host_path: Optional[str],
) -> Tuple[str, Literal['cli', 'document']]:
    if document_host_path is not None and not document_host_path.strip():
        raise SuperDocError(
            'document_host_path must be a non-empty path.',
            code='INVALID_ARGUMENT',
        )
    if document_host_path is not None:
        return document_host_path, 'document'
    if 'SUPERDOC_SDK_DOCUMENT_HOST_BIN' in env:
        configured_document_host = env['SUPERDOC_SDK_DOCUMENT_HOST_BIN']
    else:
        configured_document_host = os.environ.get('SUPERDOC_SDK_DOCUMENT_HOST_BIN')
    if configured_document_host is not None:
        if not configured_document_host.strip():
            raise SuperDocError(
                'SUPERDOC_SDK_DOCUMENT_HOST_BIN must be a non-empty path.',
                code='INVALID_ARGUMENT',
            )
        document_host = (
            resolve_embedded_document_host_path()
            if configured_document_host == 'embedded'
            else configured_document_host
        )
        return document_host, 'document'

    cli_bin = env.get('SUPERDOC_CLI_BIN') or os.environ.get('SUPERDOC_CLI_BIN') or resolve_embedded_cli_path()
    return cli_bin, 'cli'


class SuperDocSyncRuntime:
    """Synchronous runtime backed by a persistent host transport."""

    def __init__(
        self,
        *,
        document_host_path: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        startup_timeout_ms: int = 5_000,
        shutdown_timeout_ms: int = 5_000,
        request_timeout_ms: Optional[int] = None,
        watchdog_timeout_ms: int = DEFAULT_WATCHDOG_TIMEOUT_MS,
        default_change_mode: Optional[str] = None,
        user: Optional[Dict[str, str]] = None,
    ) -> None:
        self._env = dict(env or {})
        host_bin, process_mode = _resolve_runtime_process(self._env, document_host_path)
        self._default_change_mode = normalize_default_change_mode(default_change_mode)
        self._transport = SyncHostTransport(
            host_bin,
            process_mode=process_mode,
            env=self._env,
            startup_timeout_ms=startup_timeout_ms,
            shutdown_timeout_ms=shutdown_timeout_ms,
            request_timeout_ms=request_timeout_ms,
            watchdog_timeout_ms=watchdog_timeout_ms,
            default_change_mode=self._default_change_mode,
            user=user,
        )

    def connect(self) -> None:
        self._transport.connect()

    def dispose(self) -> None:
        self._transport.dispose()

    def invoke(
        self,
        operation_id: str,
        params: Optional[Dict[str, Any]] = None,
        *,
        timeout_ms: Optional[int] = None,
        stdin_bytes: Optional[bytes] = None,
        collaboration_auth: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        operation = OPERATION_INDEX[operation_id]
        return self._transport.invoke(
            operation, params or {},
            timeout_ms=timeout_ms,
            stdin_bytes=stdin_bytes,
            collaboration_auth=collaboration_auth,
        )


class SuperDocAsyncRuntime:
    """Asynchronous runtime backed by a persistent host transport."""

    def __init__(
        self,
        *,
        document_host_path: Optional[str] = None,
        env: Optional[Dict[str, str]] = None,
        startup_timeout_ms: int = 5_000,
        shutdown_timeout_ms: int = 5_000,
        request_timeout_ms: Optional[int] = None,
        watchdog_timeout_ms: int = DEFAULT_WATCHDOG_TIMEOUT_MS,
        max_queue_depth: int = 100,
        stdout_buffer_limit_bytes: int = DEFAULT_STDOUT_BUFFER_LIMIT_BYTES,
        default_change_mode: Optional[str] = None,
        user: Optional[Dict[str, str]] = None,
    ) -> None:
        self._env = dict(env or {})
        host_bin, process_mode = _resolve_runtime_process(self._env, document_host_path)
        self._default_change_mode = normalize_default_change_mode(default_change_mode)
        self._transport = AsyncHostTransport(
            host_bin,
            process_mode=process_mode,
            env=self._env,
            startup_timeout_ms=startup_timeout_ms,
            shutdown_timeout_ms=shutdown_timeout_ms,
            request_timeout_ms=request_timeout_ms,
            watchdog_timeout_ms=watchdog_timeout_ms,
            max_queue_depth=max_queue_depth,
            stdout_buffer_limit_bytes=stdout_buffer_limit_bytes,
            default_change_mode=self._default_change_mode,
            user=user,
        )

    async def connect(self) -> None:
        await self._transport.connect()

    async def dispose(self) -> None:
        await self._transport.dispose()

    async def invoke(
        self,
        operation_id: str,
        params: Optional[Dict[str, Any]] = None,
        *,
        timeout_ms: Optional[int] = None,
        stdin_bytes: Optional[bytes] = None,
        collaboration_auth: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        operation = OPERATION_INDEX[operation_id]
        return await self._transport.invoke(
            operation, params or {},
            timeout_ms=timeout_ms,
            stdin_bytes=stdin_bytes,
            collaboration_auth=collaboration_auth,
        )
