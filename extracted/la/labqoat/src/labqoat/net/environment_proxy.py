"""The HTTPS proxy a person's environment names, as command-line tools honor it."""

from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from urllib.parse import unquote, urlsplit


@dataclass(frozen=True)
class EnvironmentProxy:
    """A proxy that tunnels TLS with ``CONNECT``, taken from ``HTTPS_PROXY`` unless ``NO_PROXY`` exempts the host."""

    host: str
    port: int
    authorization: str | None

    @classmethod
    def for_host(cls, host: str) -> EnvironmentProxy | None:
        """The proxy to reach ``host`` through, or nothing for a direct connection."""
        address = os.environ.get("HTTPS_PROXY") or os.environ.get("https_proxy")
        if not address or cls._exempt(host):
            return None
        parts = urlsplit(address if "://" in address else f"http://{address}")
        if not parts.hostname:
            return None
        authorization = None
        if parts.username is not None:
            secret = f"{unquote(parts.username)}:{unquote(parts.password or '')}".encode()
            authorization = "Basic " + base64.b64encode(secret).decode("ascii")
        return cls(parts.hostname, parts.port or 8080, authorization)

    @staticmethod
    def _exempt(host: str) -> bool:
        """Whether ``NO_PROXY`` names the host, a parent domain of it, or everything."""
        listed = os.environ.get("NO_PROXY") or os.environ.get("no_proxy") or ""
        names = [name.strip().lower().lstrip(".") for name in listed.split(",") if name.strip()]
        host = host.lower()
        return any(name == "*" or host == name or host.endswith("." + name) for name in names)

    def headers(self) -> dict[str, str]:
        """The fields the tunnel request carries."""
        return {} if self.authorization is None else {"Proxy-Authorization": self.authorization}
