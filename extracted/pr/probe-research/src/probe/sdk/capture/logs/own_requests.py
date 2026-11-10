"""The lines an HTTP client logs for Probe's own requests, recognised by the API base URL, so the live log never
ships them: a framework that sets the root logger to INFO (verl's hydra) turned each upload into the next (W41c)."""

from __future__ import annotations

import re
from typing import Any
from urllib.parse import urlsplit

#: The port a client leaves out of a URL it prints.
_DEFAULT_PORTS = {"http": 80, "https": 443}
#: Splits text after each newline, keeping it.
_LINE_ENDS = re.compile(r"(?<=\n)")


class OwnRequestFilter:
    """Drops httpx's `HTTP Request: POST https://api…/v1/… "HTTP/1.1 202 Accepted"` and urllib3's
    `https://api…:443 "POST /v1/… HTTP/1.1" 202 0` for the API at ``base_url``. Any other line stays, the user's
    own lines that name the URL included."""

    def __init__(self, scheme: str, host: str, port: int, path: str) -> None:
        shown = scheme + "://" + host + ("" if port == _DEFAULT_PORTS.get(scheme) else f":{port}") + path
        #: In both shapes: the cheap first test, so a chunk without it is never split.
        self.host = host
        self._pattern = re.compile(
            # httpx prints the full URL (default port left out, `_client.py` `HTTP Request: %s %s "%s %d %s"`);
            # urllib3 prints the origin with its port, then the path (`connectionpool.py` `%s://%s:%s "%s %s %s"`).
            rf"HTTP Request: [A-Z]+ {re.escape(shown)}(?:[/?#\s\"]|$)"
            rf"|{re.escape(f'{scheme}://{host}:{port}')} \"[A-Z]+ {re.escape(path)}/"
        )

    def remove_lines(self, text: str) -> str:
        """``text`` without its request lines (each with its newline)."""
        if self.host not in text:
            return text
        lines = _LINE_ENDS.split(text)
        kept = [line for line in lines if not self._pattern.search(line)]
        return text if len(kept) == len(lines) else "".join(kept)


def build_filter(client: Any) -> OwnRequestFilter | None:
    """The filter for ``client``'s API base URL; None when it has none this can read."""
    base_url = getattr(getattr(client, "settings", None), "base_url", None)
    if not isinstance(base_url, str):
        return None
    try:
        parts = urlsplit(base_url.strip())
        scheme = (parts.scheme or "").lower()
        port = parts.port or _DEFAULT_PORTS.get(scheme)
    except ValueError:  # a port that is not a number
        return None
    host = (parts.hostname or "").lower()
    if not host or port is None:
        return None
    if ":" in host:
        host = f"[{host}]"  # an IPv6 address, bracketed as clients print it
    return OwnRequestFilter(scheme, host, port, parts.path.rstrip("/"))
