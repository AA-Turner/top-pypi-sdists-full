"""Outbound HTTP(S) proxy and CA-bundle resolution for the SDK transport.

Resolution follows the conventions established by ``requests``:

* ``HTTP_PROXY`` / ``HTTPS_PROXY`` name the proxy per target scheme, with
  ``ALL_PROXY`` as the fallback for both; lowercase variants win over
  uppercase.
* ``NO_PROXY`` lists hosts to reach directly — exact matches or dot-boundary
  suffixes (``NO_PROXY=internal.example`` bypasses the proxy for
  ``registry.internal.example`` but not ``notinternal.example``), with ``*``
  bypassing everything.
* An explicit ``Configuration.proxy_url`` overrides the proxy environment
  variables. ``NO_PROXY`` is still honored, so control-plane traffic that
  rides a direct route (e.g. a site-to-site VPN) keeps bypassing the proxy.
* ``Configuration.trust_env=False`` ignores every proxy and CA environment
  variable; the explicit configuration fields still apply.
* The CA bundle for TLS verification comes from ``Configuration.ca_bundle``,
  falling back to ``REQUESTS_CA_BUNDLE`` then ``SSL_CERT_FILE``. A bundle is
  needed when a proxy terminates and re-signs TLS; plain CONNECT tunneling
  needs proxy settings only.

Credentials embedded in a proxy URL are stripped and converted into a
``Proxy-Authorization`` header, because urllib3 ignores userinfo in the proxy
URL itself.
"""

from __future__ import annotations

import os
import re
from typing import Mapping, Optional
from urllib.parse import SplitResult, unquote, urlsplit
from urllib.request import getproxies_environment

import urllib3

_CA_BUNDLE_ENV_VARS = ("REQUESTS_CA_BUNDLE", "SSL_CERT_FILE")
_PROXIED_SCHEMES = ("http", "https")


def resolve_ca_certs(ca_bundle: Optional[str], trust_env: bool) -> Optional[str]:
    """CA bundle path for TLS verification: explicit setting first, then environment."""
    if ca_bundle:
        return ca_bundle
    if trust_env:
        for var in _CA_BUNDLE_ENV_VARS:
            value = os.environ.get(var)
            if value:
                return value
    return None


def resolve_proxies(proxy_url: Optional[str], trust_env: bool) -> dict[str, str]:
    """Scheme -> proxy-URL mapping, plus ``no`` carrying the bypass list."""
    environment = getproxies_environment() if trust_env else {}
    if proxy_url:
        proxies = {scheme: proxy_url for scheme in _PROXIED_SCHEMES}
        if "no" in environment:
            proxies["no"] = environment["no"]
        return proxies
    return {
        key: value
        for key, value in environment.items()
        if key in ("all", "no", *_PROXIED_SCHEMES)
    }


def proxy_url_for(url: str, proxies: Mapping[str, str]) -> Optional[str]:
    """The proxy to use for ``url``, or None for a direct connection."""
    if not proxies:
        return None
    parts = urlsplit(url)
    scheme = parts.scheme.lower()
    if scheme not in _PROXIED_SCHEMES:
        return None
    host = _host_port(parts)
    if host and _bypasses_proxy(host, proxies.get("no")):
        return None
    return proxies.get(scheme) or proxies.get("all")


_HOST_PORT_RE = re.compile(r"^(.*):([0-9]*)$")


def _bypasses_proxy(host: str, no_proxy: Optional[str]) -> bool:
    """NO_PROXY semantics (mirrors the stdlib): ``*`` bypasses everything;
    entries (optional leading dot, optional port) match the host exactly or
    as a dot-boundary suffix."""
    if not no_proxy:
        return False
    if no_proxy == "*":
        return True
    host = host.lower()
    match = _HOST_PORT_RE.match(host)
    host_only = match.group(1) if match else host
    for raw_entry in no_proxy.split(","):
        entry = raw_entry.strip().lstrip(".").lower()
        if not entry:
            continue
        if host_only == entry or host == entry:
            return True
        suffix = "." + entry
        if host_only.endswith(suffix) or host.endswith(suffix):
            return True
    return False


def proxy_headers_for(proxy_url: str) -> tuple[str, Optional[dict[str, str]]]:
    """Split userinfo out of ``proxy_url``: (credential-free URL, auth headers)."""
    if "://" not in proxy_url:  # requests-compatible: a bare host:port means http
        proxy_url = f"http://{proxy_url}"
    parts = urlsplit(proxy_url)
    if parts.username is None and parts.password is None:
        return proxy_url, None
    credentials = f"{unquote(parts.username or '')}:{unquote(parts.password or '')}"
    headers = urllib3.util.make_headers(proxy_basic_auth=credentials)
    clean_url = parts._replace(netloc=_host_port(parts)).geturl()
    return clean_url, dict(headers)


def _host_port(parts: SplitResult) -> str:
    host = parts.hostname or ""
    if ":" in host:  # a bare IPv6 address needs its brackets back
        host = f"[{host}]"
    return f"{host}:{parts.port}" if parts.port else host
