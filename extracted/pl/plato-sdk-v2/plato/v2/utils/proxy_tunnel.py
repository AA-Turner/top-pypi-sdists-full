"""HTTP CONNECT proxy tunnel for database connections."""

from __future__ import annotations

import asyncio
import base64
import contextlib
import logging
import os
import socket
import ssl
from urllib.parse import quote_plus, urlparse

from plato._generated.models import DbConfigResponse

logger = logging.getLogger(__name__)

PROXY_HOST = "127.0.0.1"


def find_free_port(start_port: int = 55432) -> int:
    """Find the first available TCP port starting from start_port."""
    port = start_port
    while port < 65535:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("127.0.0.1", port))
                return port
        except OSError:
            port += 1
    raise RuntimeError(f"No free port found starting from {start_port}")


def make_db_url(config: DbConfigResponse, port: int) -> str:
    """Create SQLAlchemy connection URL for the given DB config.

    Args:
        config: Database configuration with db_type, db_user, db_password, db_database.
        port: Local port to connect to (via proxy tunnel).

    Returns:
        SQLAlchemy async connection URL.

    Raises:
        ValueError: If database type is not supported.
    """
    db = config.db_type.lower()
    user = quote_plus(config.db_user)
    password = quote_plus(config.db_password)
    database = quote_plus(config.db_database)

    if db == "postgresql":
        return f"postgresql+asyncpg://{user}:{password}@{PROXY_HOST}:{port}/{database}"
    elif db == "mysql":
        return f"mysql+aiomysql://{user}:{password}@{PROXY_HOST}:{port}/{database}"
    elif db == "sqlite":
        return f"sqlite+aiosqlite:///{config.db_database}"
    raise ValueError(f"Unsupported database type: {db}")


class ProxyTunnel:
    """Manages an in-process HTTP CONNECT tunnel for database connections."""

    def __init__(self, env_id: str, db_port: int, temp_password: str, host_port: int):
        self.env_id = env_id
        self.db_port = db_port
        self.temp_password = temp_password
        self.host_port = host_port

        self._server: asyncio.AbstractServer | None = None
        self._client_tasks: set[asyncio.Task] = set()

    # ---------- helpers ----------

    @staticmethod
    def _set_keepalive(sock: socket.socket, idle_sec: int = 30) -> None:
        """macOS/BSD-friendly TCP keepalive: enable + set idle seconds."""
        try:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        except OSError:
            return
        try:
            TCP_KEEPALIVE = getattr(socket, "TCP_KEEPALIVE", 0x10)  # macOS name
            sock.setsockopt(socket.IPPROTO_TCP, TCP_KEEPALIVE, idle_sec)
        except OSError:
            pass  # best effort

    async def _open_http_connect(
        self,
        proxy_host: str,
        proxy_port: int,
        dest_host: str,
        dest_port: int,
        proxy_user: str | None,
        proxy_pass: str | None,
        use_tls_to_proxy: bool,
        timeout: float = 20.0,
    ) -> tuple[asyncio.StreamReader, asyncio.StreamWriter]:
        """Open a tunneled connection to dest via proxy using HTTP CONNECT."""
        ssl_ctx = None
        if use_tls_to_proxy:
            ssl_ctx = ssl.create_default_context()

        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(
                proxy_host,
                proxy_port,
                ssl=ssl_ctx,
                server_hostname=proxy_host if ssl_ctx else None,
            ),
            timeout=timeout,
        )

        # enable TCP keepalive on underlying socket
        sock = writer.get_extra_info("socket")
        if isinstance(sock, socket.socket):
            self._set_keepalive(sock, idle_sec=30)

        # Build CONNECT request (Basic auth if provided)
        auth = ""
        if proxy_user and proxy_pass:
            token = base64.b64encode(f"{proxy_user}:{proxy_pass}".encode()).decode()
            auth = f"Proxy-Authorization: Basic {token}\r\n"

        req = (
            f"CONNECT {dest_host}:{dest_port} HTTP/1.1\r\n"
            f"Host: {dest_host}:{dest_port}\r\n"
            f"{auth}"
            f"Proxy-Connection: keep-alive\r\n"
            f"Connection: keep-alive\r\n"
            f"\r\n"
        ).encode("ascii")
        writer.write(req)
        await writer.drain()

        # Read response headers
        header = b""
        while b"\r\n\r\n" not in header:
            chunk = await reader.read(4096)
            if not chunk:
                raise RuntimeError("Proxy closed before responding to CONNECT")
            header += chunk

        # Simple status check
        first_line = header.split(b"\r\n", 1)[0]
        parts = first_line.split()
        if len(parts) < 2 or parts[1] != b"200":
            # surface the first line for debugging
            raise RuntimeError(f"CONNECT failed: {first_line.decode(errors='ignore')}")

        return reader, writer

    async def _pipe(self, src: asyncio.StreamReader, dst: asyncio.StreamWriter):
        try:
            while True:
                data = await src.read(65536)
                if not data:
                    break
                dst.write(data)
                await dst.drain()
        finally:
            with contextlib.suppress(Exception):
                dst.close()
                await dst.wait_closed()

    async def _handle_client(
        self,
        client_reader: asyncio.StreamReader,
        client_writer: asyncio.StreamWriter,
        *,
        proxy_host: str,
        proxy_port: int,
        proxy_user: str | None,
        proxy_pass: str | None,
        use_tls_to_proxy: bool,
        dest_host: str,
        dest_port: int,
    ):
        peer = client_writer.get_extra_info("peername")
        task = asyncio.current_task()
        if task:
            self._client_tasks.add(task)
        try:
            # Establish CONNECT tunnel via proxy to the destination
            server_reader, server_writer = await self._open_http_connect(
                proxy_host=proxy_host,
                proxy_port=proxy_port,
                dest_host=dest_host,
                dest_port=dest_port,
                proxy_user=proxy_user,
                proxy_pass=proxy_pass,
                use_tls_to_proxy=use_tls_to_proxy,
            )

            # Bi-directional piping
            await asyncio.gather(
                self._pipe(client_reader, server_writer),
                self._pipe(server_reader, client_writer),
            )
        except Exception as e:
            logger.warning(f"Tunnel handler error for {peer}: {e}")
            with contextlib.suppress(Exception):
                client_writer.close()
                await client_writer.wait_closed()
        finally:
            if task:
                self._client_tasks.discard(task)

    # ---------- public API ----------

    async def start(self):
        """Start the proxy tunnel server (replaces the proxytunnel subprocess)."""
        base_url = os.getenv("PLATO_BASE_URL", "https://plato.so")
        parsed_url = urlparse(base_url)
        hostname = parsed_url.hostname or "plato.so"

        # Determine proxy URL host:port (matching Go logic)
        if hostname == "localhost" or hostname.startswith("127.0.0.1"):
            proxy_url = "localhost:9000"
        elif hostname == "plato.so":
            proxy_url = "proxy.plato.so:9000"
        else:
            parts = hostname.split(".", 1)
            if len(parts) == 2:
                subdomain, domain = parts
                proxy_url = f"{subdomain}.proxy.{domain}:9000"
            else:
                proxy_url = f"proxy.{hostname}:9000"

        # Parse proxy host/port
        if "://" in proxy_url:
            # tolerate schemes if someone sets them
            pu = urlparse(proxy_url)
            proxy_host = pu.hostname or "localhost"
            proxy_port = pu.port or 9000
        else:
            host, _, port = proxy_url.partition(":")
            proxy_host = host or "localhost"
            proxy_port = int(port or "9000")

        # -E equivalent: TLS to proxy unless explicitly disabled
        use_tls_to_proxy = os.getenv("PROXY_TLS", "1").lower() not in (
            "0",
            "false",
            "no",
        )

        # -P user:pass mapping (format: f"{env_id}@{db_port}:{temp_password}")
        proxy_user = f"{self.env_id}@{self.db_port}"
        proxy_pass = self.temp_password

        logger.info(f"Using proxy URL: {proxy_url} (from base URL: {base_url})")

        # Start local listener that mimics: -d 127.0.0.1:<db_port> -a <host_port>
        # i.e., we listen on host_port and forward through proxy to 127.0.0.1:db_port
        def handler(r, w):
            return self._handle_client(
                r,
                w,
                proxy_host=proxy_host,
                proxy_port=proxy_port,
                proxy_user=proxy_user,
                proxy_pass=proxy_pass,
                use_tls_to_proxy=use_tls_to_proxy,
                dest_host="127.0.0.1",
                dest_port=self.db_port,
            )

        # Bind on localhost for safety, same as proxytunnel's typical usage
        self._server = await asyncio.start_server(handler, host="127.0.0.1", port=self.host_port)
        addrs = ", ".join(str(s.getsockname()) for s in (self._server.sockets or []))

        # Mirror your previous logs
        logger.info(f"Starting proxy tunnel listener on {addrs} -> 127.0.0.1:{self.db_port} via {proxy_url}")

        # Small delay to mirror your readiness wait and allow binding to settle
        await asyncio.sleep(0.2)

        # Sanity check: ensure server is active (no "poll" in async variant; just check sockets)
        if not self._server.sockets:
            raise RuntimeError("Proxy tunnel failed to start: no listening sockets")

        logger.info(f"Proxy tunnel established on port {self.host_port}")

    async def stop(self) -> None:
        """Stop the proxy tunnel server."""
        if self._server is not None:
            logger.info("Stopping proxy tunnel")

            # Stop accepting new connections
            self._server.close()
            await self._server.wait_closed()

            self._server = None

            # Cancel any active client piping tasks
            for t in list(self._client_tasks):
                t.cancel()
            self._client_tasks.clear()

            logger.info("Proxy tunnel stopped")
