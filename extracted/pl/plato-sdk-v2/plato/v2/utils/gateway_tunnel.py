"""TLS + SNI gateway tunnel for database connections.

Routes traffic through gateway.plato.so:443 using SNI-based routing,
replacing the deprecated HTTP CONNECT proxy approach.
"""

from __future__ import annotations

import asyncio
import logging
import os
import socket
import ssl

logger = logging.getLogger(__name__)

# Default gateway configuration
DEFAULT_GATEWAY_HOST = "gateway.plato.so"
DEFAULT_GATEWAY_PORT = 443


def get_gateway_config() -> tuple[str, int]:
    """Get gateway host and port from environment or defaults.

    Returns:
        Tuple of (host, port) for the gateway.
    """
    host = os.environ.get("PLATO_GATEWAY_HOST", DEFAULT_GATEWAY_HOST)
    port = int(os.environ.get("PLATO_GATEWAY_PORT", str(DEFAULT_GATEWAY_PORT)))
    return host, port


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


class GatewayTunnel:
    """Async TLS + SNI gateway tunnel for database connections.

    Routes local connections through gateway.plato.so using SNI-based routing.
    This replaces the deprecated HTTP CONNECT proxy tunnel.

    Usage:
        tunnel = GatewayTunnel(job_id="abc123", remote_port=5432, local_port=55432)
        await tunnel.start()
        # Connect to localhost:55432 to reach the VM's port 5432
        await tunnel.stop()
    """

    def __init__(
        self,
        job_id: str,
        remote_port: int,
        local_port: int,
        gateway_host: str | None = None,
        gateway_port: int | None = None,
        verify_ssl: bool = True,
    ):
        """Initialize the gateway tunnel.

        Args:
            job_id: The job/environment ID to connect to.
            remote_port: Port on the VM to forward to.
            local_port: Local port to listen on.
            gateway_host: Gateway hostname (default: from env or gateway.plato.so).
            gateway_port: Gateway port (default: from env or 443).
            verify_ssl: Whether to verify SSL certificates.
        """
        self.job_id = job_id
        self.remote_port = remote_port
        self.local_port = local_port
        self.verify_ssl = verify_ssl

        # Get gateway config
        default_host, default_port = get_gateway_config()
        self.gateway_host = gateway_host or default_host
        self.gateway_port = gateway_port or default_port

        # SNI for routing: {job_id}--{port}.gateway.plato.so
        self.sni = f"{job_id}--{remote_port}.{self.gateway_host}"

        self._server: asyncio.AbstractServer | None = None
        self._client_tasks: set[asyncio.Task] = set()

    async def _open_gateway_connection(
        self,
        timeout: float = 30.0,
    ) -> tuple[asyncio.StreamReader, asyncio.StreamWriter]:
        """Open a TLS connection to the gateway with SNI routing.

        Returns:
            Tuple of (reader, writer) for the gateway connection.
        """
        # Create SSL context
        ssl_ctx = ssl.create_default_context()
        if not self.verify_ssl:
            ssl_ctx.check_hostname = False
            ssl_ctx.verify_mode = ssl.CERT_NONE

        # Connect with TLS, using SNI for routing
        reader, writer = await asyncio.wait_for(
            asyncio.open_connection(
                self.gateway_host,
                self.gateway_port,
                ssl=ssl_ctx,
                server_hostname=self.sni,  # SNI determines which VM/port to route to
            ),
            timeout=timeout,
        )

        # Enable TCP keepalive
        sock = writer.get_extra_info("socket")
        if isinstance(sock, socket.socket):
            try:
                sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                # macOS/BSD keepalive idle time
                TCP_KEEPALIVE = getattr(socket, "TCP_KEEPALIVE", 0x10)
                sock.setsockopt(socket.IPPROTO_TCP, TCP_KEEPALIVE, 30)
            except OSError:
                pass  # Best effort

        return reader, writer

    async def _pipe(
        self,
        src: asyncio.StreamReader,
        dst: asyncio.StreamWriter,
    ) -> None:
        """Forward data from src to dst until EOF."""
        try:
            while True:
                data = await src.read(65536)
                if not data:
                    break
                dst.write(data)
                await dst.drain()
        except (ConnectionResetError, BrokenPipeError, OSError):
            pass
        finally:
            try:
                dst.close()
                await dst.wait_closed()
            except Exception:
                pass

    async def _handle_client(
        self,
        client_reader: asyncio.StreamReader,
        client_writer: asyncio.StreamWriter,
    ) -> None:
        """Handle a single client connection by forwarding through gateway."""
        task = asyncio.current_task()
        if task:
            self._client_tasks.add(task)

        try:
            # Connect to gateway via TLS with SNI
            gateway_reader, gateway_writer = await self._open_gateway_connection()

            # Bidirectional forwarding
            await asyncio.gather(
                self._pipe(client_reader, gateway_writer),
                self._pipe(gateway_reader, client_writer),
            )
        except Exception as e:
            logger.warning(f"Gateway tunnel error: {e}")
            try:
                client_writer.close()
                await client_writer.wait_closed()
            except Exception:
                pass
        finally:
            if task:
                self._client_tasks.discard(task)

    async def start(self) -> None:
        """Start the gateway tunnel server.

        If ``local_port`` is 0, the OS assigns a free port and
        ``self.local_port`` is updated to reflect the actual port.
        """
        logger.info(
            f"Starting gateway tunnel: localhost:{self.local_port} -> "
            f"{self.job_id}:{self.remote_port} via {self.gateway_host}"
        )

        self._server = await asyncio.start_server(
            self._handle_client,
            host="127.0.0.1",
            port=self.local_port,
        )

        # Small delay to ensure binding is settled
        await asyncio.sleep(0.1)

        if not self._server.sockets:
            raise RuntimeError("Gateway tunnel failed to start: no listening sockets")

        # When local_port=0, read back the OS-assigned port.
        if self.local_port == 0:
            self.local_port = self._server.sockets[0].getsockname()[1]

        logger.info(f"Gateway tunnel established on port {self.local_port}")

    async def stop(self, timeout: float = 5.0) -> None:
        """Stop the gateway tunnel server.

        Shutdown is best-effort and bounded by ``timeout`` so callers do not
        hang indefinitely during teardown.
        """
        timeout = max(0.0, timeout)
        server = self._server
        tasks = list(self._client_tasks)

        if server is None and not tasks:
            return

        logger.info("Stopping gateway tunnel")
        loop = asyncio.get_running_loop()
        deadline = loop.time() + timeout

        # Stop accepting new connections immediately to avoid creating new
        # _handle_client tasks while teardown is in progress.
        if server is not None:
            server.close()

        # Cancel active client handlers first so server shutdown doesn't wait
        # on long-lived proxy tasks.
        while self._client_tasks:
            current_tasks = list(self._client_tasks)
            for task in current_tasks:
                task.cancel()

            remaining = max(0.0, deadline - loop.time())
            if remaining <= 0:
                logger.warning(
                    "Timed out waiting for %d gateway client task(s) to stop",
                    len(self._client_tasks),
                )
                break

            _, pending = await asyncio.wait(current_tasks, timeout=remaining)
            if pending and max(0.0, deadline - loop.time()) <= 0:
                logger.warning(
                    "Timed out waiting for %d gateway client task(s) to stop",
                    len(self._client_tasks),
                )
                break

        # Stop accepting new connections.
        if server is not None:
            remaining = max(0.0, deadline - loop.time())
            try:
                await asyncio.wait_for(server.wait_closed(), timeout=remaining)
            except asyncio.TimeoutError:
                logger.warning("Timed out waiting for gateway server socket to close")
            self._server = None

        if self._client_tasks:
            logger.warning(
                "Gateway tunnel still has %d client task(s) after stop timeout",
                len(self._client_tasks),
            )

        logger.info("Gateway tunnel stopped")
