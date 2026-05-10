from __future__ import annotations

import asyncio
import contextvars
import inspect
import io
import json
import os
import sys
import threading
from typing import Callable

from ..clients.capsule import IntegrationCredential, LogRecord
from ..constants import DEFAULT_TOKEN_TYPE
from ..home import HomeContext
from ..integration import IntegrationCredentials, KNOWN_SECRET_INTEGRATIONS
from ..session import RequestContext, Session

# Query keys reserved by the gateway for routing/identity; strip before
# handing off to user-defined data sources so they don't collide with kwargs.
_RESERVED_QUERY_KEYS = frozenset({"version_id", "session_id"})
_GRPC_RETRY_DELAY = 2
_BRANDING_LOGO_ROUTE = "/branding/logo"
_PORT = 8080
_HEARTBEAT_INTERVAL = 10
_MAX_BACKOFF = 5
_GRPC_RETRY_TRIES = 4
_SUBMIT_RESULT_WORKERS = int(os.environ.get("CAPSULE_SUBMIT_RESULT_WORKERS", "1"))
_RPC_WORKERS = int(os.environ.get("CAPSULE_RPC_WORKERS", "16"))

_current_task_id: contextvars.ContextVar[str] = contextvars.ContextVar(
    "_current_task_id", default=""
)

_log_buffer: list[LogRecord] = []
_log_buffer_lock = threading.Lock()
_LOG_BUFFER_MAX = 500
_ASSET_MAX_BYTES = 512 * 1024  # 512 KB — skip data-URI for huge files


def _asset_to_data_uri(path: str) -> str | None:
    """Read a local asset file and return a data URI, or None if unreadable."""
    import base64
    import mimetypes

    full = os.path.join(os.getcwd(), path)
    if not os.path.isfile(full):
        _log(f"theme asset not found: {full}")
        return None
    if os.path.getsize(full) > _ASSET_MAX_BYTES:
        _log(f"theme asset too large for inline: {full}")
        return None
    ct = mimetypes.guess_type(full)[0] or "application/octet-stream"
    data = open(full, "rb").read()
    return f"data:{ct};base64,{base64.b64encode(data).decode()}"


def _serialize_collection_columns(columns) -> list | None:
    if not columns:
        return None
    has_types = any(
        getattr(c, "type", "text") != "text"
        or getattr(c, "label", None)
        or getattr(c, "format", None)
        for c in columns
    )
    if has_types:
        return [
            {
                k: v
                for k, v in {
                    "key": c.key,
                    "type": getattr(c, "type", "text") or "text",
                    "label": getattr(c, "label", None),
                    "format": getattr(c, "format", None),
                }.items()
                if v is not None
            }
            for c in columns
        ]
    return [c.key for c in columns]


def _parse_integration_credential(ic: IntegrationCredential) -> IntegrationCredentials:
    """Build an IntegrationCredentials from a protobuf IntegrationCredential.

    For secret-based integrations the gateway JSON-encodes the field map
    into ``access_token``. We unpack it here so ``cred.fields`` is populated.
    """
    is_secret = ic.type in KNOWN_SECRET_INTEGRATIONS
    secret_fields: dict[str, str] = {}
    if is_secret and ic.access_token:
        try:
            parsed = json.loads(ic.access_token)
            if isinstance(parsed, dict):
                secret_fields = parsed
        except (json.JSONDecodeError, TypeError):
            pass

    return IntegrationCredentials(
        access_token="" if secret_fields else ic.access_token,
        token_type=ic.token_type or DEFAULT_TOKEN_TYPE,
        scopes=list(ic.scopes),
        expires_at=ic.expires_at,
        fields=secret_fields,
    )


class StdoutJsonInterceptor(io.TextIOBase):
    """Intercepts stdout/stderr and writes structured JSON lines to the original stream.

    The Go side (serve controller) tails the process output, parses JSON lines,
    and routes them to S2. For deploy-type apps the runner also flushes buffered
    records to the gateway via IngestLogs gRPC (see _flush_log_buffer).
    """

    def __init__(self, stream=sys.__stdout__):
        self._stream = stream

    def write(self, buf: str) -> int:
        if not buf:
            return 0
        try:
            task_id = _current_task_id.get("")
            for line in buf.splitlines():
                if not line:
                    continue
                record = {"message": line, "stream": "stdout"}
                if task_id:
                    record["task_id"] = task_id
                self._stream.write(json.dumps(record) + "\n")
                with _log_buffer_lock:
                    if len(_log_buffer) < _LOG_BUFFER_MAX:
                        _log_buffer.append(LogRecord(stream="stdout", text=line, task_id=task_id))
            self._stream.flush()
        except Exception:
            self._stream.write(buf)
            self._stream.flush()
        return len(buf)

    def flush(self) -> None:
        self._stream.flush()

    def fileno(self) -> int:
        try:
            return self._stream.fileno()
        except (AttributeError, io.UnsupportedOperation):
            return -1

    def isatty(self) -> bool:
        return False

    def writable(self) -> bool:
        return True


_HOP_HEADERS = frozenset(
    (
        "connection",
        "keep-alive",
        "proxy-authenticate",
        "proxy-authorization",
        "te",
        "trailers",
        "transfer-encoding",
        "upgrade",
        "host",
    )
)


def _resolve_message_handler(
    handlers: dict[str, Callable],
    default_handler: Callable | None,
    chat_name: str,
) -> Callable | None:
    if chat_name:
        handler = handlers.get(chat_name)
        if handler is None:
            available = sorted(name for name in handlers if name)
            suffix = f" Available named chats: {', '.join(available)}." if available else ""
            raise RuntimeError(f"Unknown chat surface {chat_name!r}.{suffix}")
        return handler
    return default_handler


def _log(msg: str) -> None:
    print(f"[cpsl] {msg}", flush=True)


def _find_hook(instance: object, attr: str):
    for name in dir(instance):
        fn = getattr(instance, name, None)
        if callable(fn) and getattr(fn, attr, False):
            return fn
    return None


async def _maybe_await(result):
    if asyncio.iscoroutine(result):
        return await result
    return result


def _wants_request_context(fn) -> bool:
    """True if fn's first parameter is named 'ctx' or type-hinted as a context object."""
    try:
        sig = inspect.signature(fn)
        params = list(sig.parameters.values())
        if not params:
            return False
        first = params[0]
        if first.name == "ctx":
            return True
        hint = first.annotation
        if hint is inspect.Parameter.empty:
            return False
        return hint in (RequestContext, HomeContext) or (
            isinstance(hint, str) and ("RequestContext" in hint or "HomeContext" in hint)
        )
    except (ValueError, TypeError):
        return False


def _wants_session(fn) -> bool:
    """True if fn declares a parameter named 'session' or type-hinted as Session."""
    try:
        sig = inspect.signature(fn)
        for param in sig.parameters.values():
            if param.name == "session":
                return True
            hint = param.annotation
            if hint is inspect.Parameter.empty:
                continue
            if hint is Session or (isinstance(hint, str) and "Session" in hint):
                return True
    except (ValueError, TypeError):
        return False
    return False
