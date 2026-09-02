"""Hosted out-of-band (OAST) collector for cross-cloud callback proof.

The local honeytoken collector (:class:`dreadnode.airt.honeytoken.LocalCollector`) only
works when the target can reach 127.0.0.1. For a remote agent (cloud, third-party), the
callback needs a collector reachable from the target's network. This module provides:

- :class:`OASTCollector` - a minimal, dependency-free callback server (stdlib http.server)
  that records DNS/HTTP-style beacon hits on ``/c/<id>`` and answers match queries on
  ``/hits?q=<value>`` (representation-invariant via the honeytoken canonicalizer). Bind it
  on a reachable host and mint canaries against its ``base_url``.
- :class:`RemoteCollector` - a client with the same ``.saw(canary)`` contract the effect
  scorers expect, so a detection process on another host can confirm callbacks.

Generic and sector-agnostic: a callback correlated to a unique per-test token proves
execution / SSRF / exfiltration regardless of the target's tools or domain.
"""

import threading
import time
import typing as t
import urllib.parse
from http.server import BaseHTTPRequestHandler, HTTPServer

from dreadnode.airt.honeytoken import canonicalize

__all__ = ["OASTCollector", "RemoteCollector"]


class OASTCollector:
    """A reachable callback server that records hits and answers match queries."""

    def __init__(self, host: str = "0.0.0.0", port: int = 0) -> None:  # noqa: S104 - a collector must be reachable by the target
        self._host = host
        self._port = port
        self._hits: list[dict[str, t.Any]] = []
        self._server: HTTPServer | None = None
        self._thread: threading.Thread | None = None
        self.base_url: str = ""

    def start(self) -> str:
        hits = self._hits

        class _Handler(BaseHTTPRequestHandler):
            def log_message(self, format: str, *args: t.Any) -> None:  # noqa: ARG002
                return

            def _reply(self, body: str) -> None:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(body.encode())

            def do_GET(self) -> None:
                parsed = urllib.parse.urlparse(self.path)
                if parsed.path.rstrip("/") == "/hits":
                    q = urllib.parse.parse_qs(parsed.query).get("q", [""])[0]
                    corpus = canonicalize(" ".join(h["path"] + " " + h["body"] for h in hits))
                    self._reply("1" if q and q.lower() in corpus else "0")
                    return
                hits.append({"path": self.path, "body": "", "ts": time.time()})
                self._reply("ok")

            def do_POST(self) -> None:
                length = int(self.headers.get("Content-Length", 0) or 0)
                body = self.rfile.read(length).decode("utf-8", "ignore") if length else ""
                hits.append({"path": self.path, "body": body, "ts": time.time()})
                self._reply("ok")

        self._server = HTTPServer((self._host, self._port), _Handler)
        self._port = self._server.server_address[1]
        reachable = "127.0.0.1" if self._host in ("0.0.0.0", "") else self._host  # noqa: S104
        self.base_url = f"http://{reachable}:{self._port}"
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()
        return self.base_url

    def stop(self) -> None:
        if self._server is not None:
            self._server.shutdown()
            self._server.server_close()
            self._server = None
        self._hits.clear()

    def saw(self, canary: t.Any) -> bool:
        """True if the canary value appears in any recorded hit (canonicalized)."""
        value = str(getattr(canary, "value", canary)).lower()
        corpus = canonicalize(" ".join(h["path"] + " " + h["body"] for h in self._hits))
        return bool(value) and value in corpus

    def __enter__(self) -> "OASTCollector":
        self.start()
        return self

    def __exit__(self, *exc: object) -> None:
        self.stop()


class RemoteCollector:
    """Client for a hosted :class:`OASTCollector`, with the effect-scorer ``.saw`` contract."""

    def __init__(self, base_url: str) -> None:
        self.base_url = base_url.rstrip("/")

    def saw(self, canary: t.Any) -> bool:
        import httpx

        value = str(getattr(canary, "value", canary))
        if not value:
            return False
        try:
            r = httpx.get(f"{self.base_url}/hits", params={"q": value}, timeout=5)
            return r.text.strip() == "1"
        except Exception:
            return False
