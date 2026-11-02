"""the HTTP opener for a call that carries a credential: no redirects, the environment's proxies (ALL_PROXY too)."""

from __future__ import annotations
import urllib.error
import urllib.request
from probe.foundation.tls.tls import ssl_context


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    """Refuse every redirect. urllib's default handler would turn the POST into
    a GET and copy the headers -- the bearer included -- to whatever host
    `Location` names (an SSO proxy in front of a self-hosted API, an https ->
    http downgrade). The SDK's httpx client never follows redirects either; a
    3xx here surfaces as an HTTPError and reads as unreachable."""

    def redirect_request(self, *_args, **_kwargs):
        return None


def _proxies() -> dict[str, str]:
    """The environment's proxies as urllib reads them, plus `ALL_PROXY`, which
    urllib ignores and httpx (the SDK, and the calls this replaced) honours."""
    proxies = urllib.request.getproxies()
    everything = proxies.get("all")
    if everything:
        proxies.setdefault("http", everything)
        proxies.setdefault("https", everything)
    return proxies


def _urllib_cannot_reach(base_url: str) -> bool:
    """Whether the environment routes `base_url` through a proxy urllib cannot
    speak -- a TLS (`https://`) or SOCKS proxy -- that httpx (the SDK, which the
    old calls use) can. Such a machine asks the old way from the start."""
    from urllib.parse import urlsplit

    parts = urlsplit(base_url)
    proxy = _proxies().get(parts.scheme)
    # host:port, as urllib's own ProxyHandler asks: NO_PROXY can name a port.
    authority = parts.hostname or ""
    if parts.port:
        authority = f"{authority}:{parts.port}"
    if not proxy or urllib.request.proxy_bypass(authority):
        return False
    # A scheme-less proxy ("proxy:8080") is plain HTTP to urllib; only an
    # explicit other scheme (https://, socks5://) is one it cannot speak.
    if "://" not in proxy:
        return False
    return urlsplit(proxy).scheme.lower() != "http"


def _credential_opener() -> urllib.request.OpenerDirector:
    """The opener for a request that carries a credential: no redirects, the
    environment's proxies, the CLI's TLS trust."""
    return urllib.request.build_opener(
        _NoRedirect,
        urllib.request.ProxyHandler(_proxies()),
        urllib.request.HTTPSHandler(context=ssl_context()),
    )
