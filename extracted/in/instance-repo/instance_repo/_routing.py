"""Private data-plane route planning and reachability classification."""
from __future__ import annotations

import errno
import re
import socket
import ssl
from dataclasses import dataclass
from enum import Enum

from .errors import InstanceRepoError, TransportError


class _OperationIntent(str, Enum):
    DOWNLOAD = "download"
    NON_DOWNLOAD = "nonDownload"


@dataclass(frozen=True)
class _EndpointRoute:
    private_endpoint: str
    public_endpoint: str | None = None
    standard: bool = False


_OSS_RE = re.compile(
    r"^(?P<base>oss-[a-z0-9-]+?)(?:-internal)?\.aliyuncs\.com$"
)
_ACR_RE = re.compile(
    r"^(?P<name>[a-z0-9-]+?)(?:-vpc)?\.(?P<region>[a-z0-9-]+)\.cr\.aliyuncs\.com$"
)
_REACHABILITY_ERRNOS = frozenset({
    errno.ECONNREFUSED,
    errno.ECONNRESET,
    errno.ENETUNREACH,
    errno.EHOSTUNREACH,
    errno.ETIMEDOUT,
})


def _split_scheme(endpoint: str) -> tuple[str, str]:
    for scheme in ("https://", "http://"):
        if endpoint.startswith(scheme):
            return scheme, endpoint[len(scheme):]
    return "", endpoint


def _probe_private_endpoint(endpoint: str, timeout: float = 0.5) -> bool:
    """Quick TCP connect probe to decide whether a private endpoint is reachable.

    Performs a raw TCP connect (no TLS handshake) to the endpoint host/port.
    Returns True if the connect succeeds, False on any error.  The default
    timeout is 0.5 seconds — 内网 TCP 握手通常在几十毫秒内完成，0.5s 足够
    判定可达性，同时把公网环境下私网不可达的探测开销从 3s 压到 0.5s
    （结果按 store 缓存 5 分钟，仅端点变更或缓存过期才重探）。
    """
    _, host = _split_scheme(endpoint)
    # Determine port: default 443 for https, 80 for http.
    scheme, _ = _split_scheme(endpoint)
    default_port = 443 if scheme == "https://" else 80
    # Parse host:port — handle IPv4 with optional port.
    if ":" in host:
        parts = host.rsplit(":", 1)
        hostname = parts[0]
        try:
            port = int(parts[1])
        except (ValueError, IndexError):
            hostname = host
            port = default_port
    else:
        hostname = host
        port = default_port
    # Strip any trailing path from hostname.
    if "/" in hostname:
        hostname = hostname.split("/", 1)[0]
    try:
        conn = socket.create_connection((hostname, port), timeout=timeout)
        conn.close()
        return True
    except Exception:  # noqa: BLE001 - any failure means unreachable
        return False


def _plan_oss_route(endpoint: str) -> _EndpointRoute:
    value = (endpoint or "").strip()
    scheme, host = _split_scheme(value)
    match = _OSS_RE.fullmatch(host)
    if match is None:
        return _EndpointRoute(value)
    base = match.group("base")
    return _EndpointRoute(
        f"{scheme}{base}-internal.aliyuncs.com",
        f"{scheme}{base}.aliyuncs.com",
        True,
    )


def _plan_acr_route(endpoint: str) -> _EndpointRoute:
    value = (endpoint or "").strip()
    scheme, host = _split_scheme(value)
    match = _ACR_RE.fullmatch(host)
    if match is None:
        return _EndpointRoute(value)
    base = f"{match.group('name')}.{match.group('region')}.cr.aliyuncs.com"
    private = f"{match.group('name')}-vpc.{match.group('region')}.cr.aliyuncs.com"
    return _EndpointRoute(f"{scheme}{private}", f"{scheme}{base}", True)


def _requests_connection_error_type():
    """Resolve ``requests.exceptions.ConnectionError`` lazily.

    requests only reaches a base install through the optional ``oss2`` extra, so
    it must never be imported at module scope. Returns ``None`` when requests is
    unavailable, in which case no exception can be an instance of it anyway.
    """
    try:
        from requests.exceptions import ConnectionError as RequestsConnectionError
    except Exception:  # noqa: BLE001 - any import failure means "unavailable"
        return None
    return RequestsConnectionError


def _urllib3_exception_types():
    """Resolve the urllib3 transport exception classes lazily.

    Like requests, urllib3 is only present via optional extras. Returns ``None``
    when it cannot be imported; otherwise a mapping of classification buckets:
    ``read_timeout`` (veto), ``connect`` (typed reachability), and ``neutral``
    (retry/protocol wrappers whose real cause is traversed via ``.reason``/args).
    """
    try:
        from urllib3.exceptions import (
            ConnectTimeoutError,
            MaxRetryError,
            NewConnectionError,
            ProtocolError,
            ReadTimeoutError,
        )
    except Exception:  # noqa: BLE001 - any import failure means "unavailable"
        return None
    return {
        "read_timeout": (ReadTimeoutError,),
        "connect": (NewConnectionError, ConnectTimeoutError),
        "neutral": (MaxRetryError, ProtocolError),
    }


def _is_raw_reachability_error(exc: BaseException) -> bool:
    if isinstance(exc, socket.gaierror):
        return True
    if isinstance(exc, (TimeoutError, ConnectionRefusedError, ConnectionResetError)):
        return True
    return isinstance(exc, OSError) and exc.errno in _REACHABILITY_ERRNOS


def _exception_graph(exc: BaseException) -> list[BaseException]:
    pending: list[BaseException] = [exc]
    graph: list[BaseException] = []
    seen: set[int] = set()
    while pending:
        current = pending.pop()
        if id(current) in seen:
            continue
        seen.add(id(current))
        graph.append(current)

        nested = [
            getattr(current, "exception", None),
            getattr(current, "reason", None),
            current.__cause__,
            current.__context__,
        ]
        grouped = getattr(current, "exceptions", ())
        if isinstance(grouped, tuple):
            nested.extend(grouped)
        nested.extend(
            arg for arg in getattr(current, "args", ())
            if isinstance(arg, BaseException)
        )
        pending.extend(item for item in nested if isinstance(item, BaseException))
    return graph


def _is_reachability_error(exc: BaseException) -> bool:
    """Return whether *exc* is a typed failure to reach a remote endpoint.

    The complete exception graph is checked before connectivity classification so
    that HTTP, business, and TLS/certificate failures always win. Only raw
    network errors and recognized SDK/OSS transport wrappers are eligible.
    """
    graph = _exception_graph(exc)
    has_reachability_error = False
    requests_connection_error = _requests_connection_error_type()
    urllib3_types = _urllib3_exception_types()

    for current in graph:
        if isinstance(current, (ssl.SSLError, ssl.CertificateError)):
            return False

        if urllib3_types is not None:
            # A urllib3 read timeout means the connection was established and the
            # read then timed out — an HTTP-level failure, never a connect-level
            # reachability failure. It vetoes even alongside a connect error.
            if isinstance(current, urllib3_types["read_timeout"]):
                return False
            if isinstance(current, urllib3_types["connect"]):
                has_reachability_error = True
                continue
            if isinstance(current, urllib3_types["neutral"]):
                # MaxRetryError / ProtocolError only wrap the real cause, which
                # is reached via .reason / args during graph traversal.
                continue

        if isinstance(current, InstanceRepoError):
            if not isinstance(current, TransportError):
                return False
            status = getattr(current, "status", None)
            if isinstance(status, int) and status >= 0:
                return False
            continue

        if _is_raw_reachability_error(current):
            has_reachability_error = True
            continue

        if requests_connection_error is not None and isinstance(
                current, requests_connection_error):
            continue

        status = getattr(current, "status", None)
        if isinstance(status, int) and status >= 0:
            return False
        if (
            isinstance(status, int)
            and status < 0
            and isinstance(getattr(current, "exception", None), BaseException)
        ):
            continue

        return False

    return has_reachability_error
