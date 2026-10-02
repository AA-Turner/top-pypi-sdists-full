"""Read the proxy settings for the Anyscale API clients from the environment."""

from typing import Dict, Optional, Tuple
from urllib.parse import unquote, urlsplit, urlunsplit

# Typeshed does not declare proxy_bypass_environment.
from urllib.request import (  # type: ignore[attr-defined]
    getproxies_environment,
    proxy_bypass_environment,
)

from urllib3.util import make_headers


def get_proxy_config(host_url: str) -> Tuple[Optional[str], Optional[Dict[str, str]]]:
    """Return the proxy URL and the proxy headers for host_url, or (None, None)."""
    proxies = getproxies_environment()
    proxy = proxies.get("https")
    if not proxy:
        return None, None
    if proxy_bypass_environment(urlsplit(host_url).hostname or "", proxies):
        return None, None

    if "://" not in proxy:
        proxy = "http://" + proxy
    parts = urlsplit(proxy)
    if parts.username is None:
        return proxy, None
    # Keep the host unchanged, so that IPv6 brackets stay.
    sanitized = urlunsplit(parts._replace(netloc=parts.netloc.rpartition("@")[2]))
    userinfo = f"{unquote(parts.username)}:{unquote(parts.password or '')}"
    return sanitized, make_headers(proxy_basic_auth=userinfo)
