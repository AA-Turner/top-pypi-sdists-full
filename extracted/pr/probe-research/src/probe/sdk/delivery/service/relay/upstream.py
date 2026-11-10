"""The relay's side toward the API, shared by its lanes and its held streams: an httpx client per caller's
network settings, `api.call`'s timeouts, and the failure kind an exception answers as."""

from __future__ import annotations

from probe.foundation.service_api.vocabularies import RelayFailure

#: A response body up to this size rides in the answer (base64 keeps the line under 1 MiB).
INLINE_BYTES = 512 * 1024
#: Headers that describe the wire, not the body handed back (it is decoded here).
DECODED_DROPS = frozenset({"content-encoding", "content-length", "transfer-encoding"})


def make_client(env: dict, limits):
    """An httpx client sending through `env`'s proxies and CAs (the caller's; a fenced caller's are this
    service's own): no redirects, nothing read from this process's environment."""
    import httpx

    from probe.foundation.tls.tls import ssl_context

    verify = ssl_context(env)
    mounts = {pattern: (None if proxy is None else httpx.HTTPTransport(proxy=proxy, verify=verify))
              for pattern, proxy in _get_proxy_mounts(env).items()}
    return httpx.Client(verify=verify, mounts=mounts, trust_env=False, follow_redirects=False, limits=limits)


def get_timeout_parts(parts: dict) -> dict:
    """httpx's four timeouts from `api.call`'s (30 s each when the caller named none)."""
    return {name: parts.get(name, 30.0) for name in ("connect", "read", "write", "pool")}


def get_failure_kind(exc: Exception) -> str:
    import httpx

    if isinstance(exc, (httpx.ConnectError, httpx.ConnectTimeout, httpx.PoolTimeout, httpx.UnsupportedProtocol)):
        return RelayFailure.CONNECT
    if isinstance(exc, httpx.TimeoutException):
        return RelayFailure.TIMEOUT
    if isinstance(exc, (httpx.RemoteProtocolError, httpx.ReadError, httpx.WriteError, httpx.LocalProtocolError)):
        return RelayFailure.PROTOCOL
    return RelayFailure.OTHER


def _get_proxy_mounts(env: dict) -> dict:
    """httpx's mounts for `env`'s proxy variables, as httpx reads its own environment
    (`httpx._utils.get_environment_proxies`): lower case first, NO_PROXY hosts go direct."""
    proxies: dict[str, str] = {}
    for name, value in sorted(env.items(), key=lambda item: item[0].islower()):
        if value and name.lower().endswith("_proxy"):
            proxies[name.lower()[: -len("_proxy")]] = value
    mounts: dict[str, str | None] = {}
    for scheme in ("http", "https", "all"):
        url = proxies.get(scheme)
        if url:
            mounts[f"{scheme}://"] = url if "://" in url else f"http://{url}"
    for host in (h.strip() for h in proxies.get("no", "").split(",")):
        if host == "*":
            return {}
        if not host:
            continue
        if "://" in host:
            mounts[host] = None
        elif host.replace(".", "").isdigit() or host.lower() == "localhost":
            mounts[f"all://{host}"] = None
        elif ":" in host:
            mounts[f"all://[{host}]"] = None
        else:
            mounts[f"all://*{host}"] = None
    return mounts
