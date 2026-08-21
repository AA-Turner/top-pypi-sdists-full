"""One hardened fetch for every user-supplied URL (SSRF guard).

Our services run inside the cluster and can reach `deployment-manager:8000`,
`redis:6379`, `kubernetes.default.svc` and `169.254.169.254`. A user hands us a
URL (task `files`, webhooks, MCP, chat upload) and we fetch it to read the file.
Without a guard, that URL can point at any of those, and at least one call site
inlines the response body straight into the model's prompt.

This module is the single fetch policy: resolve the host, reject every internal
address, connect to the exact validated IP (so a second lookup cannot rebind the
name to a private address), disable automatic redirects and re-validate each hop,
cap the bytes while streaming, and bound the whole call by a single deadline.

Self-contained by design (stdlib + httpx + loguru only, nothing from the rest of
`xpander_dev_utils`) so it can be mirrored into xpander-sdk and vendored into the
voice service, which install neither package. Keep the three copies identical.

Modes, via `XPANDER_SAFE_FETCH`:
- unset / "enforce": block internal destinations (default).
- "warn": log what would be blocked, then fetch anyway (observation window).
- "legacy": no checks, plain follow-redirects fetch (kill switch).
"""

import asyncio
import ipaddress
import os
import socket
import time
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple
from urllib.parse import urljoin, urlsplit

import httpx
from loguru import logger

# CGNAT (RFC 6598) — Python reports these as is_private=False, so it is listed
# explicitly. Everything else is covered by the ipaddress flags below.
_CGNAT_V4 = ipaddress.ip_network("100.64.0.0/10")

_MAX_REDIRECTS = 5
_DEFAULT_TIMEOUT = 15.0
_DEFAULT_MAX_BYTES = 30 * 1024 * 1024


def _mode() -> str:
    return (os.getenv("XPANDER_SAFE_FETCH", "") or "").strip().lower()


def _legacy() -> bool:
    return _mode() == "legacy"


def _warn_only() -> bool:
    return _mode() == "warn"


class SafeFetchError(Exception):
    """A fetch was refused, or failed under policy; the message names the host only."""


@dataclass
class FetchResult:
    """Outcome of a safe fetch: response bytes, content-type, final URL, status, headers."""

    content: bytes
    content_type: Optional[str]
    final_url: str
    status: int
    headers: Dict[str, str]


def _ip_is_blocked(ip_text: str) -> bool:
    """Whether a resolved address is one we must never connect to."""
    try:
        ip = ipaddress.ip_address(ip_text)
    except ValueError:
        return True  # unparseable is not something we connect to
    mapped = getattr(ip, "ipv4_mapped", None)
    if mapped is not None:
        ip = mapped
    if isinstance(ip, ipaddress.IPv4Address) and ip in _CGNAT_V4:
        return True
    return (
        ip.is_private
        or ip.is_loopback
        or ip.is_link_local
        or ip.is_multicast
        or ip.is_unspecified
        or ip.is_reserved
    )


def literal_host_blocked(host: str) -> bool:
    """Block an IP-literal host in any encoding, without DNS; a hostname returns False."""
    h = host.strip().strip("[]").lower()
    if h in ("localhost",):
        return True
    try:
        return _ip_is_blocked(str(ipaddress.ip_address(h)))
    except ValueError:
        pass
    # integer and short-form IPv4 spellings that ip_address() rejects but the
    # resolver would accept as numeric (0x7f000001, 2130706433, 127.1)
    try:
        packed = socket.inet_aton(h)
        return _ip_is_blocked(socket.inet_ntoa(packed))
    except OSError:
        pass
    try:
        n = int(h, 16) if h.startswith("0x") else (int(h) if h.isdigit() else None)
        if n is not None and 0 <= n <= 0xFFFFFFFF:
            return _ip_is_blocked(str(ipaddress.IPv4Address(n)))
    except ValueError:
        pass
    return False


def _split_target(url: str) -> Tuple[str, str, int]:
    """(scheme, host, port) for *url*, raising SafeFetchError on a malformed URL/port."""
    try:
        parts = urlsplit(url)
        scheme = parts.scheme
        host = parts.hostname
        port = parts.port or (443 if scheme == "https" else 80)
    except ValueError as exc:  # e.g. a non-numeric port like http://h:abc/
        raise SafeFetchError("url is malformed") from exc
    if scheme not in ("http", "https"):
        raise SafeFetchError("url must be http or https")
    if not host:
        raise SafeFetchError("url has no host")
    return scheme, host, port


def _resolve_validated(host: str, port: int) -> List[str]:
    """Resolve *host*, returning its addresses in order, or raise if any is internal."""
    try:
        infos = socket.getaddrinfo(host, port, proto=socket.IPPROTO_TCP)
    except socket.gaierror as exc:
        raise SafeFetchError(f"cannot resolve host {host!r}") from exc

    addrs: List[str] = []
    for info in infos:
        ip_text = info[4][0]
        if _ip_is_blocked(ip_text):
            raise SafeFetchError(f"host {host!r} resolves to a blocked address")
        if ip_text not in addrs:
            addrs.append(ip_text)
    if not addrs:
        raise SafeFetchError(f"host {host!r} did not resolve")
    return addrs


def is_blocked_host(url: str) -> Tuple[bool, str]:
    """Classify a URL without fetching it, honoring the mode. Returns (blocked, reason).

    Enforce blocks internal destinations; warn never blocks but marks the reason so a
    caller can log a would-block; legacy never blocks. Shared by validate-only callers.
    """
    if _legacy():
        return (False, "legacy")
    try:
        _, host, port = _split_target(url)
        _resolve_validated(host, port)
    except SafeFetchError as exc:
        if _warn_only():
            return (False, f"warn-would-block: {exc}")
        return (True, str(exc))
    return (False, "")


async def ais_blocked_host(url: str) -> Tuple[bool, str]:
    """is_blocked_host off the event loop (getaddrinfo is a blocking call)."""
    return await asyncio.to_thread(is_blocked_host, url)


def _authority(host: str, port: int) -> str:
    """Host[:port] for a Host header, bracketing IPv6 literals."""
    bare = host.strip("[]")
    hostpart = f"[{bare}]" if ":" in bare else bare
    return hostpart if port in (80, 443) else f"{hostpart}:{port}"


def _pinned_transport(ip: str, *, is_async: bool, verify: bool):
    """A transport that dials *ip* while keeping Host + SNI as the real hostname.

    Connecting by IP would break TLS name verification and virtual-host routing,
    so the socket target is swapped to the validated IP while the URL host (used
    for SNI) and the Host header are preserved.
    """
    base = httpx.AsyncHTTPTransport if is_async else httpx.HTTPTransport

    class _Pinned(base):  # type: ignore[valid-type,misc]
        def _rewrite(self, request: httpx.Request) -> httpx.Request:
            host = request.url.host
            port = request.url.port or (443 if request.url.scheme == "https" else 80)
            request.extensions = dict(request.extensions)
            request.extensions["sni_hostname"] = host
            request.headers["Host"] = _authority(host, port)
            request.url = request.url.copy_with(host=ip)
            return request

    if is_async:
        class _AsyncPinned(_Pinned):
            async def handle_async_request(self, request):
                return await super().handle_async_request(self._rewrite(request))

        return _AsyncPinned(verify=verify)

    class _SyncPinned(_Pinned):
        def handle_request(self, request):
            return super().handle_request(self._rewrite(request))

    return _SyncPinned(verify=verify)


def _next_redirect(response: httpx.Response, base_url: str) -> Optional[str]:
    """Redirect target resolved against the *logical* (hostname) URL, not the pinned IP.

    The transport rewrites the request host to the validated IP, so joining a
    relative `Location` against `response.url` would carry the IP into the next hop
    and break vhost / TLS name checks. `base_url` is the hostname URL.
    """
    if response.status_code not in (301, 302, 303, 307, 308):
        return None
    loc = response.headers.get("location")
    if not loc:
        return None
    return urljoin(base_url, loc)


def _headers(extra: Optional[Dict[str, str]]) -> Dict[str, str]:
    return dict(extra or {})


def _remaining(deadline: float) -> float:
    """Seconds left before the whole-call deadline, or raise once it is spent."""
    left = deadline - time.monotonic()
    if left <= 0:
        raise SafeFetchError("fetch deadline exceeded")
    return left


def _read_capped(response: httpx.Response, max_bytes: int, host: str) -> bytes:
    if max_bytes <= 0:  # headers-only probe: do not consume the body
        return b""
    buf = bytearray()
    for chunk in response.iter_bytes():
        buf.extend(chunk)
        if len(buf) > max_bytes:
            raise SafeFetchError(f"response from {host!r} exceeds {max_bytes} bytes")
    return bytes(buf)


async def _aread_capped(response: httpx.Response, max_bytes: int, host: str) -> bytes:
    if max_bytes <= 0:  # headers-only probe: do not consume the body
        return b""
    buf = bytearray()
    async for chunk in response.aiter_bytes():
        buf.extend(chunk)
        if len(buf) > max_bytes:
            raise SafeFetchError(f"response from {host!r} exceeds {max_bytes} bytes")
    return bytes(buf)


def _legacy_sync(
    url: str, method: str, headers: Dict[str, str], max_bytes: int, timeout: float
) -> FetchResult:
    with httpx.Client(follow_redirects=True, timeout=timeout) as client:
        with client.stream(method, url, headers=headers) as resp:
            resp.raise_for_status()
            host = resp.url.host or ""
            content = _read_capped(resp, max_bytes, host)
            return FetchResult(content, resp.headers.get("content-type"), str(resp.url), resp.status_code, dict(resp.headers))


async def _legacy_async(
    url: str, method: str, headers: Dict[str, str], max_bytes: int, timeout: float
) -> FetchResult:
    async with httpx.AsyncClient(follow_redirects=True, timeout=timeout) as client:
        async with client.stream(method, url, headers=headers) as resp:
            resp.raise_for_status()
            host = resp.url.host or ""
            content = await _aread_capped(resp, max_bytes, host)
            return FetchResult(content, resp.headers.get("content-type"), str(resp.url), resp.status_code, dict(resp.headers))


def safe_fetch(
    url: str,
    *,
    max_bytes: int = _DEFAULT_MAX_BYTES,
    timeout: float = _DEFAULT_TIMEOUT,
    method: str = "GET",
    extra_headers: Optional[Dict[str, str]] = None,
) -> FetchResult:
    """Fetch *url* under the SSRF policy, bounded by a single *timeout* deadline."""
    headers = _headers(extra_headers)
    if _legacy():
        return _legacy_sync(url, method, headers, max_bytes, timeout)

    deadline = time.monotonic() + timeout
    current = url
    for _hop in range(_MAX_REDIRECTS + 1):
        _, host, port = _split_target(current)
        try:
            addrs = _resolve_validated(host, port)
        except SafeFetchError:
            if _warn_only():
                logger.warning(f"safe_fetch(warn): would block host {host!r}")
                return _legacy_sync(current, method, headers, max_bytes, _remaining(deadline))
            raise

        last_err: Optional[Exception] = None
        redirect_to: Optional[str] = None
        scheme_https = current.lower().startswith("https")
        for ip in addrs:  # multi-IP CDN: fall through to the next validated address
            transport = _pinned_transport(ip, is_async=False, verify=scheme_https)
            try:
                with httpx.Client(transport=transport, timeout=_remaining(deadline), follow_redirects=False) as client:
                    with client.stream(method, current, headers=headers) as resp:
                        nxt = _next_redirect(resp, current)
                        if nxt is not None:
                            redirect_to = nxt
                            break
                        if resp.status_code >= 400:
                            # a real HTTP answer, not a connection failure: do not
                            # retry across IPs, and surface the actual status
                            raise SafeFetchError(f"host {host!r} returned status {resp.status_code}")
                        content = _read_capped(resp, max_bytes, host)
                        return FetchResult(content, resp.headers.get("content-type"), current, resp.status_code, dict(resp.headers))
            except SafeFetchError:
                raise
            except httpx.HTTPError as exc:  # transport-level: try the next address
                last_err = exc
                continue
        if redirect_to is not None:
            current = redirect_to
            continue
        raise SafeFetchError(f"could not connect to host {host!r}") from last_err
    raise SafeFetchError("too many redirects")


async def asafe_fetch(
    url: str,
    *,
    max_bytes: int = _DEFAULT_MAX_BYTES,
    timeout: float = _DEFAULT_TIMEOUT,
    method: str = "GET",
    extra_headers: Optional[Dict[str, str]] = None,
) -> FetchResult:
    """asyncio counterpart of safe_fetch, bounded by a single *timeout* deadline."""
    headers = _headers(extra_headers)
    if _legacy():
        return await _legacy_async(url, method, headers, max_bytes, timeout)

    deadline = time.monotonic() + timeout
    current = url
    for _hop in range(_MAX_REDIRECTS + 1):
        _, host, port = _split_target(current)
        try:
            addrs = await asyncio.to_thread(_resolve_validated, host, port)
        except SafeFetchError:
            if _warn_only():
                logger.warning(f"safe_fetch(warn): would block host {host!r}")
                return await _legacy_async(current, method, headers, max_bytes, _remaining(deadline))
            raise

        last_err: Optional[Exception] = None
        redirect_to: Optional[str] = None
        scheme_https = current.lower().startswith("https")
        for ip in addrs:
            transport = _pinned_transport(ip, is_async=True, verify=scheme_https)
            try:
                async with httpx.AsyncClient(transport=transport, timeout=_remaining(deadline), follow_redirects=False) as client:
                    async with client.stream(method, current, headers=headers) as resp:
                        nxt = _next_redirect(resp, current)
                        if nxt is not None:
                            redirect_to = nxt
                            break
                        if resp.status_code >= 400:
                            raise SafeFetchError(f"host {host!r} returned status {resp.status_code}")
                        content = await _aread_capped(resp, max_bytes, host)
                        return FetchResult(content, resp.headers.get("content-type"), current, resp.status_code, dict(resp.headers))
            except SafeFetchError:
                raise
            except httpx.HTTPError as exc:
                last_err = exc
                continue
        if redirect_to is not None:
            current = redirect_to
            continue
        raise SafeFetchError(f"could not connect to host {host!r}") from last_err
    raise SafeFetchError("too many redirects")
