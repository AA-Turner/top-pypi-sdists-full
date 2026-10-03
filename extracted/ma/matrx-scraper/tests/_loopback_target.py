"""A real loopback HTTP server holding a planted secret — the attack target.

Used by the address-refusal tests: the server records every TCP connection it
accepts, so a test can assert that NOTHING reached it, whichever engine,
proxy or fallback was involved. Real sockets, no stubs: the census proved the
leak with exactly this shape (a 200 carrying the secret from 127.0.0.1).
"""

from __future__ import annotations

import socket
import threading
from dataclasses import dataclass, field

SECRET = "harbor-dental-internal-admin-token-7f3a91"


@dataclass
class LoopbackTarget:
    port: int
    accepted: list[str] = field(default_factory=list)

    @property
    def url(self) -> str:
        return f"http://127.0.0.1:{self.port}/admin/settings"

    @property
    def https_url(self) -> str:
        return f"https://127.0.0.1:{self.port}/admin/settings"


def start_target() -> tuple[LoopbackTarget, threading.Event]:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", 0))
    sock.listen(16)
    sock.settimeout(0.2)
    target = LoopbackTarget(port=sock.getsockname()[1])
    stop = threading.Event()
    body = (
        "<html><head><title>Practice admin</title></head><body><main><h1>Admin</h1>"
        f"<p>Service token: {SECRET}. " + "Internal settings for the practice. " * 30
        + "</p></main></body></html>"
    ).encode()

    def serve() -> None:
        while not stop.is_set():
            try:
                conn, _ = sock.accept()
            except TimeoutError:
                continue
            except OSError:
                break
            target.accepted.append("connection")
            try:
                conn.settimeout(2)
                conn.recv(65536)
                conn.sendall(
                    b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: "
                    + str(len(body)).encode()
                    + b"\r\nConnection: close\r\n\r\n"
                    + body
                )
            except OSError:
                pass
            finally:
                conn.close()
        sock.close()

    threading.Thread(target=serve, daemon=True).start()
    return target, stop


def start_refusing_proxy() -> tuple[str, threading.Event]:
    """A proxy that refuses every CONNECT with 403 — our vendor declining a destination."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", 0))
    sock.listen(16)
    sock.settimeout(0.2)
    stop = threading.Event()

    def serve() -> None:
        while not stop.is_set():
            try:
                conn, _ = sock.accept()
            except TimeoutError:
                continue
            except OSError:
                break
            try:
                conn.settimeout(2)
                conn.recv(65536)
                conn.sendall(b"HTTP/1.1 403 Forbidden\r\nContent-Length: 0\r\n\r\n")
            except OSError:
                pass
            finally:
                conn.close()
        sock.close()

    threading.Thread(target=serve, daemon=True).start()
    return f"http://127.0.0.1:{sock.getsockname()[1]}", stop
