"""An absolute request address split into the parts a connection and a request line need."""

from __future__ import annotations

from dataclasses import dataclass
from urllib.parse import parse_qsl, unquote, urlencode, urlsplit


@dataclass(frozen=True)
class Url:
    """Scheme, host and port pick the connection; the encoded path and query form the request target."""

    scheme: str
    host: str
    port: int | None
    target: str

    @classmethod
    def parse(cls, text: str, params: dict[str, str] | None = None) -> Url:
        """Split an absolute ``http`` or ``https`` address, appending ``params`` to any query it has."""
        parts = urlsplit(text)
        if parts.scheme not in ("http", "https") or not parts.hostname:
            raise ValueError(f"Not an absolute HTTP address: {text!r}")
        query = "&".join(item for item in (parts.query, urlencode(params or {})) if item)
        target = (parts.path or "/") + (f"?{query}" if query else "")
        return cls(parts.scheme, parts.hostname, parts.port, target)

    @property
    def path(self) -> str:
        """The decoded path without its query."""
        return unquote(self.target.split("?", 1)[0])

    @property
    def raw_path(self) -> bytes:
        """The encoded path and query exactly as the request line carries them."""
        return self.target.encode("ascii")

    @property
    def query(self) -> bytes:
        """The encoded query without its question mark."""
        return self.target.partition("?")[2].encode("ascii")

    @property
    def params(self) -> dict[str, str]:
        """Decoded query parameters; a repeated name keeps its first value."""
        values: dict[str, str] = {}
        for name, value in parse_qsl(self.target.partition("?")[2], keep_blank_values=True):
            values.setdefault(name, value)
        return values

    @property
    def authority(self) -> str:
        """The host and any explicit port, as the Host header names them."""
        host = f"[{self.host}]" if ":" in self.host else self.host
        return host if self.port is None else f"{host}:{self.port}"

    def __str__(self) -> str:
        """The whole address."""
        return f"{self.scheme}://{self.authority}{self.target}"
