"""HTTPS-as-probe decision routing with loopback-gated fallback (#925).

Routes a CLI decision action to the local server's HTTP endpoint so the
server's chain-safe :class:`AuditWriter` is the sole writer for that
durable action. The HTTP attempt itself is the probe — the
:func:`call_decision_endpoint` function does **not** consult any
secondary "is the server up" oracle. This eliminates the false-negative
class that would let server-up + CLI-local-write states form independent
HMAC chain segments.

Failure-mode taxonomy
---------------------

==========================================  ====================================
HTTP outcome                                Action
==========================================  ====================================
2xx                                         return parsed JSON response
``ConnectionRefusedError`` + loopback       raise ``ServerNotRunningError``
                                            (caller MAY fall back to local
                                            chain-safe writer)
``ConnectionRefusedError`` + non-loopback   raise ``ServerHttpError``
                                            (caller MUST surface; ECONNREFUSED
                                            on a remote endpoint is ambiguous
                                            — the real server may be alive
                                            elsewhere)
Connect timeout / read timeout              raise ``ServerHttpError``
TLS handshake / DNS / network unreachable   raise ``ServerHttpError``
4xx / 5xx                                   raise ``ServerHttpError``
==========================================  ====================================

The ``ServerNotRunningError`` path is the **only** circumstance under
which the caller may legitimately invoke the local fallback writer. All
other failures must surface to the user, because the server may be alive
and writing to its own audit chain — a parallel local write would split
the chain and silently break tamper evidence.

Loopback definition
-------------------

A target is "loopback" iff *every* address that ``socket.getaddrinfo``
returns for the configured ``app.host`` is in IPv4 ``127.0.0.0/8`` or
IPv6 ``::1``. ``getaddrinfo`` failures (DNS resolution failures) and
mixed loopback/non-loopback resolutions are conservatively treated as
non-loopback so unknown hosts never authorise local fallback.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import ipaddress
import json
import logging
import socket
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..config import AppConfig

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# Exceptions
# ---------------------------------------------------------------------------


class ServerNotRunningError(Exception):
    """OS-attested absence of the configured local server.

    Only raised when ``ConnectionRefusedError`` is observed AND the
    configured target resolves to loopback. Callers MAY treat this as a
    license to fall back to a local chain-safe writer.
    """


class ServerHttpError(Exception):
    """Any non-success HTTP outcome that is NOT an OS-attested loopback absence.

    Raised for: connect/read timeouts, TLS handshake failures, DNS
    failures, network-unreachable, ECONNREFUSED on a non-loopback target,
    and any 4xx/5xx HTTP response. Callers MUST surface this error and
    MUST NOT fall back to local writes; the server may still be alive
    and writing to its own audit chain.
    """

    def __init__(self, message: str, *, status_code: int | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code


# ---------------------------------------------------------------------------
# Loopback detection
# ---------------------------------------------------------------------------


def _target_is_loopback(host: str) -> bool:
    """Return True iff every address *host* resolves to is loopback.

    Conservative: any non-loopback address among the resolution results
    disqualifies the host. Failure to parse or resolve also returns
    False (non-loopback) so unknown hosts never authorise local fallback.

    Examples
    --------
    >>> _target_is_loopback("127.0.0.1")
    True
    >>> _target_is_loopback("::1")
    True
    >>> _target_is_loopback("192.168.1.10")
    False
    >>> _target_is_loopback("localhost")  # depends on /etc/hosts; usually True
    """
    if not host:
        return False
    # Direct IP literal first — avoids DNS for the common case.
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        pass
    # Hostname — resolve all addresses.
    try:
        infos = socket.getaddrinfo(host, None)
    except socket.gaierror:
        return False
    if not infos:
        return False
    for info in infos:
        sockaddr = info[4]
        # IPv4 sockaddr is (host, port); IPv6 is (host, port, flowinfo, scopeid).
        if not sockaddr:
            return False
        addr = sockaddr[0]
        try:
            ip = ipaddress.ip_address(addr)
        except ValueError:
            return False
        if not ip.is_loopback:
            return False
    return True


# ---------------------------------------------------------------------------
# Auth token derivation (mirrors ``app._derive_auth_token``)
# ---------------------------------------------------------------------------


def _derive_bearer_token(config: AppConfig) -> str:
    """Derive the bearer token from the identity PEM.

    Mirrors ``app._derive_auth_token`` so the CLI presents the same
    token shape that ``BearerTokenMiddleware`` validates server-side.
    """
    identity = getattr(config, "identity", None)
    if identity is None or not getattr(identity, "private_key", ""):
        raise ServerHttpError("Cannot route to server: no identity private key available to derive bearer token.")
    raw = hmac.new(
        identity.private_key.encode("utf-8"),
        b"anteroom-session-v1",
        hashlib.sha256,
    ).digest()
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")[:43]


# ---------------------------------------------------------------------------
# Routing
# ---------------------------------------------------------------------------


def call_decision_endpoint(
    config: AppConfig,
    method: str,
    path: str,
    *,
    json_body: dict[str, Any] | None = None,
    timeout: float = 10.0,
) -> dict[str, Any]:
    """Issue an authenticated HTTPS request to the local server.

    On 2xx, returns the parsed JSON response body.

    Raises :class:`ServerNotRunningError` ONLY when ``httpx`` raises
    :class:`httpx.ConnectError` whose ``__cause__`` is
    :class:`ConnectionRefusedError` AND the configured ``app.host``
    resolves to loopback. Callers MAY fall back to local execution +
    local chain-safe writer in this case.

    Raises :class:`ServerHttpError` on any other failure: timeout, TLS
    handshake failure, non-2xx response, network unreachable,
    non-loopback ECONNREFUSED, etc. Callers MUST surface this error to
    the user and MUST NOT write locally.

    *path* is the URL path beginning with ``/``; it is appended to the
    server's base URL derived from ``config.app.host``/``port`` (with
    ``https://`` if ``config.app.tls.enabled`` else ``http://``).
    """
    try:
        import httpx
    except ImportError as exc:  # pragma: no cover — httpx is transitive via openai
        raise ServerHttpError("httpx is required for CLI server routing but is not installed.") from exc

    method_upper = method.upper()
    if method_upper not in ("GET", "POST", "PUT", "PATCH", "DELETE"):
        raise ValueError(f"Unsupported HTTP method: {method!r}")

    host = getattr(config.app, "host", "127.0.0.1")
    port = getattr(config.app, "port", 8080)
    tls = getattr(getattr(config.app, "tls", None), "enabled", False)
    scheme = "https" if tls else "http"
    url = f"{scheme}://{host}:{port}{path}"

    token = _derive_bearer_token(config)
    headers = {"Authorization": f"Bearer {token}"}

    # In local server mode (loopback), self-signed certs are normal — the
    # server's TLS cert is the localhost cert minted by ``services.tls``.
    # ``verify=False`` is acceptable here precisely because the connection
    # is loopback (no MITM surface). For non-loopback targets, the operator
    # is responsible for cert config; we leave verify=True so a real cert
    # mismatch surfaces as ServerHttpError rather than silently passing.
    verify_tls = not _target_is_loopback(host)

    try:
        response = httpx.request(
            method_upper,
            url,
            json=json_body,
            headers=headers,
            timeout=timeout,
            verify=verify_tls,
        )
    except httpx.ConnectError as exc:
        # httpx may wrap the OS error via either ``__cause__`` (explicit
        # ``raise X from Y``) or ``__context__`` (automatic nested raise).
        # On py3.14 + httpx 0.28+ the ``ConnectionRefusedError`` is reached
        # only through ``__context__``; earlier stacks exposed it via
        # ``__cause__``.  Walk both chains up to a shallow depth and treat
        # a hit on either as "connection refused".
        def _find_refused(top_exc: BaseException) -> bool:
            seen: set[int] = set()
            stack: list[BaseException] = [top_exc]
            depth = 0
            while stack and depth < 8:
                current = stack.pop()
                if id(current) in seen:
                    continue
                seen.add(id(current))
                if isinstance(current, ConnectionRefusedError):
                    return True
                for attr in ("__cause__", "__context__"):
                    nxt = getattr(current, attr, None)
                    if nxt is not None:
                        stack.append(nxt)
                depth += 1
            return False

        if _find_refused(exc):
            if _target_is_loopback(host):
                raise ServerNotRunningError(
                    f"Loopback server at {host}:{port} refused connection (no socket bound)."
                ) from exc
            raise ServerHttpError(
                f"Connection refused by configured server endpoint ({host}:{port}); "
                "refusing to write audit entry locally on a non-loopback target."
            ) from exc
        # Any other ConnectError (TLS, DNS, network unreachable) is ambiguous.
        raise ServerHttpError(f"Connection error reaching {url}: {exc}") from exc
    except httpx.TimeoutException as exc:
        raise ServerHttpError(f"Timeout reaching {url}: {exc}") from exc
    except httpx.HTTPError as exc:
        raise ServerHttpError(f"HTTP error reaching {url}: {exc}") from exc

    if response.status_code >= 400:
        try:
            body_preview = response.text[:200]
        except Exception:  # pragma: no cover
            body_preview = "<unreadable>"
        raise ServerHttpError(
            f"Server returned {response.status_code} for {method_upper} {path}: {body_preview}",
            status_code=response.status_code,
        )

    try:
        return response.json()  # type: ignore[no-any-return]
    except (ValueError, json.JSONDecodeError) as exc:
        raise ServerHttpError(f"Server returned non-JSON 2xx response for {method_upper} {path}") from exc
