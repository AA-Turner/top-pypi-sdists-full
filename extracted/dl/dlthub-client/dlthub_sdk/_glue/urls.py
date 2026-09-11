"""Where the web UI lives, derived from the control-plane URL.

Mirrors ``dlt_runtime/urls.py`` and ``web/src/misc/routes.tsx``; the three must
agree on the host split, so change them together.

A leaf module: it imports nothing else from the package.
"""

from __future__ import annotations

# Python internals
import re
from urllib.parse import quote, urlparse

#: Lives here rather than beside the transport so `context` can name it without
#: importing the transport, which would drag every generated operation in.
DEFAULT_BASE_URL = "https://api.dlthub.com"

_LEGACY_BASE_URL = re.compile(
    r"^(?P<scheme>https?)://dlthub\.(?P<tld>app|net|test|dev)/api/(?:api|auth)/?$"
)


def normalize_base_url(url: str) -> str:
    """Rewrite a legacy split-host control-plane URL to the gateway form.

    Args:
        url: A control-plane base URL, in either form.

    Returns:
        The gateway form, or the input unchanged when it is not legacy.
    """
    match = _LEGACY_BASE_URL.match(url.strip())
    if not match:
        return url
    return f"{match['scheme']}://api.dlthub.{match['tld']}"


def web_ui_base(base_url: str) -> str:
    """Return the web UI origin for a control-plane URL.

    Args:
        base_url: The control-plane base URL.

    Returns:
        The web origin: the API host without its ``api.`` prefix, except in
        production, where ``dlthub.com`` serves marketing and the app lives on
        ``app.dlthub.com``.
    """
    parsed = urlparse(normalize_base_url(base_url))
    bare = parsed.netloc.removeprefix("api.")
    host = f"app.{bare}" if bare.startswith("dlthub.com") else bare
    return f"{parsed.scheme}://{host}"


def segment(value: str) -> str:
    """Percent-encode one path segment.

    Args:
        value: The raw value.

    Returns:
        The value with every reserved character encoded, so a ref containing a
        slash cannot forge a path.
    """
    return quote(value, safe="")
