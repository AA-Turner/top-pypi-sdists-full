"""Agent-side tunnel client — local TCP listener + WebSocket relay to cube-cloud.

Usage flow:
1. User calls app_proxy tool with an app name and optional local port
2. Agent opens a WebSocket to cube-cloud /tunnel endpoint
3. Agent starts a local TCP listener on localhost:<port>
4. Each incoming TCP connection gets a stream_id
5. Agent sends CONNECT frame to server with app_name
6. Server connects to the Teleport app via tbot certificates
7. DATA frames relay TCP bytes bidirectionally
8. When client disconnects, agent sends CLOSE frame

This replaces the local `tsh proxy app` command entirely.
"""

from __future__ import annotations

import asyncio
import logging
import struct
from urllib.parse import urlparse

import httpx

from cube_agent.config import get_api_key, get_cloud_url

logger = logging.getLogger(__name__)

# Frame protocol (same as server-side relay.py)
CMD_CONNECT = 0x01
CMD_DATA = 0x02
CMD_CLOSE = 0x03
CMD_ERROR = 0x04
CMD_CONNECTED = 0x05
HEADER_SIZE = 5


def _pack_frame(cmd: int, stream_id: int, payload: bytes = b"") -> bytes:
    return struct.pack("!BI", cmd, stream_id) + payload


def _unpack_frame(data: bytes) -> tuple[int, int, bytes]:
    if len(data) < HEADER_SIZE:
        raise ValueError(f"Frame too short: {len(data)} bytes")
    cmd, stream_id = struct.unpack("!BI", data[:HEADER_SIZE])
    return cmd, stream_id, data[HEADER_SIZE:]


class AppProxyTunnel:
    """Manages a single app proxy tunnel session.

    Opens a WebSocket to cube-cloud, listens on a local TCP port, and relays
    traffic between local clients and the remote Teleport app.
    """

    def __init__(self, app_name: str, local_port: int = 0) -> None:
        self.app_name = app_name
        self.local_port = local_port
        self._ws: httpx.AsyncClient | None = None
        self._ws_connection = None
        self._server: asyncio.Server | None = None
        self._next_stream_id = 1
        self._streams: dict[int, asyncio.StreamWriter] = {}
        self._pending_connects: dict[int, asyncio.Future] = {}
        self._ws_send_lock = asyncio.Lock()
        self._actual_port: int | None = None
        self._running = False

    @property
    def actual_port(self) -> int | None:
        return self._actual_port

    async def start(self) -> int:
        """Start the tunnel. Returns the actual local port."""
        api_key = get_api_key()
        if not api_key:
            raise RuntimeError("Not authenticated. Set CUBE_API_KEY or run: cube-agent login <key>")

        cloud_url = get_cloud_url()
        parsed = urlparse(cloud_url)
        ws_scheme = "wss" if parsed.scheme == "https" else "ws"
        ws_url = f"{ws_scheme}://{parsed.netloc}/tunnel?token={api_key}"

        # Connect WebSocket using httpx websocket support
        # We use a raw websocket library since httpx doesn't natively support websockets
        # Use websockets library for the client connection
        try:
            import websockets
        except ImportError:
            raise RuntimeError(
                "websockets package required for app proxy tunnel. "
                "Install with: pip install websockets"
            )

        self._ws_connection = await websockets.connect(
            ws_url,
            max_size=2**20,  # 1MB max frame
        )

        # Start local TCP listener
        self._server = await asyncio.start_server(
            self._handle_client,
            "127.0.0.1",
            self.local_port,
        )
        addr = self._server.sockets[0].getsockname()
        self._actual_port = addr[1]
        self._running = True

        # Start WebSocket reader task
        asyncio.create_task(self._ws_reader())

        logger.info("Tunnel started: localhost:%d -> %s", self._actual_port, self.app_name)
        return self._actual_port

    async def stop(self) -> None:
        """Stop the tunnel."""
        self._running = False

        if self._server:
            self._server.close()
            await self._server.wait_closed()

        # Close all streams
        for stream_id, writer in list(self._streams.items()):
            try:
                writer.close()
                await writer.wait_closed()
            except Exception:
                pass
        self._streams.clear()

        # Close WebSocket
        if self._ws_connection:
            try:
                await self._ws_connection.close()
            except Exception:
                pass

    async def _handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        """Handle an incoming TCP connection."""
        stream_id = self._next_stream_id
        self._next_stream_id += 1

        self._streams[stream_id] = writer
        logger.info("New TCP client -> stream %d for %s", stream_id, self.app_name)

        # Send CONNECT to server
        connect_future: asyncio.Future = asyncio.get_event_loop().create_future()
        self._pending_connects[stream_id] = connect_future

        await self._ws_send(_pack_frame(CMD_CONNECT, stream_id, self.app_name.encode("utf-8")))

        # Wait for CONNECTED or ERROR
        try:
            await asyncio.wait_for(connect_future, timeout=15)
        except asyncio.TimeoutError:
            logger.error("CONNECT timeout for stream %d", stream_id)
            writer.close()
            self._streams.pop(stream_id, None)
            return
        except Exception as e:
            logger.error("CONNECT failed for stream %d: %s", stream_id, e)
            writer.close()
            self._streams.pop(stream_id, None)
            return

        # Relay TCP → WebSocket
        try:
            while self._running:
                data = await reader.read(32768)
                if not data:
                    break
                await self._ws_send(_pack_frame(CMD_DATA, stream_id, data))
        except Exception as e:
            logger.debug("TCP read done stream=%d: %s", stream_id, e)
        finally:
            # Send CLOSE
            try:
                await self._ws_send(_pack_frame(CMD_CLOSE, stream_id))
            except Exception:
                pass
            writer.close()
            self._streams.pop(stream_id, None)

    async def _ws_reader(self) -> None:
        """Background task: read WebSocket frames and dispatch."""
        try:
            async for raw in self._ws_connection:
                if isinstance(raw, str):
                    continue  # Ignore text frames

                cmd, stream_id, payload = _unpack_frame(raw)

                if cmd == CMD_CONNECTED:
                    fut = self._pending_connects.pop(stream_id, None)
                    if fut and not fut.done():
                        fut.set_result(True)

                elif cmd == CMD_DATA:
                    writer = self._streams.get(stream_id)
                    if writer:
                        try:
                            writer.write(payload)
                            await writer.drain()
                        except Exception:
                            pass

                elif cmd == CMD_CLOSE:
                    writer = self._streams.pop(stream_id, None)
                    if writer:
                        try:
                            writer.close()
                        except Exception:
                            pass

                elif cmd == CMD_ERROR:
                    error_msg = payload.decode("utf-8", errors="replace")
                    logger.error("Tunnel error stream=%d: %s", stream_id, error_msg)
                    fut = self._pending_connects.pop(stream_id, None)
                    if fut and not fut.done():
                        fut.set_exception(RuntimeError(error_msg))
                    writer = self._streams.pop(stream_id, None)
                    if writer:
                        try:
                            writer.close()
                        except Exception:
                            pass

        except Exception as e:
            if self._running:
                logger.error("WebSocket reader error: %s", e)
        finally:
            # Fail all pending connects
            for fut in self._pending_connects.values():
                if not fut.done():
                    fut.set_exception(RuntimeError("WebSocket disconnected"))
            self._pending_connects.clear()

    async def _ws_send(self, data: bytes) -> None:
        """Thread-safe WebSocket send."""
        async with self._ws_send_lock:
            await self._ws_connection.send(data)


# ---------------------------------------------------------------------------
# Module-level proxy management (mirrors the original _running_proxies dict)
# ---------------------------------------------------------------------------

_running_tunnels: dict[str, AppProxyTunnel] = {}


async def start_proxy(app_name: str, port: int | None = None) -> str:
    """Start a tunnel proxy for an app. Returns status message."""
    if app_name in _running_tunnels:
        tunnel = _running_tunnels[app_name]
        if tunnel._running:
            return f"Proxy for '{app_name}' is already running on localhost:{tunnel.actual_port}.\nUse app_proxy_stop to stop it first."

    tunnel = AppProxyTunnel(app_name, local_port=port or 0)
    try:
        actual_port = await tunnel.start()
    except Exception as e:
        return f"Failed to start proxy for '{app_name}': {e}"

    _running_tunnels[app_name] = tunnel

    lines = [f"Proxy started for: {app_name}", f"Local address: localhost:{actual_port}"]

    # Usage hints
    app_lower = app_name.lower()
    if "mosquitto" in app_lower or "mqtt" in app_lower:
        lines.append(f"\nMQTT: mosquitto_sub -h localhost -p {actual_port} -t '#'")
    elif "rabbit" in app_lower:
        lines.append(f"\nRabbitMQ UI: http://localhost:{actual_port}")

    lines.append("\nUse app_proxy_stop to stop the proxy when done.")
    return "\n".join(lines)


async def stop_proxy(app_name: str | None = None) -> str:
    """Stop tunnel proxy(s). Returns status message."""
    if not _running_tunnels:
        return "No proxies are currently running."

    stopped = []

    if app_name:
        tunnel = _running_tunnels.pop(app_name, None)
        if not tunnel:
            return f"No proxy running for '{app_name}'.\nRunning proxies: {', '.join(_running_tunnels.keys())}"
        await tunnel.stop()
        stopped.append(app_name)
    else:
        for name, tunnel in list(_running_tunnels.items()):
            await tunnel.stop()
            stopped.append(name)
        _running_tunnels.clear()

    return f"Stopped proxies: {', '.join(stopped)}"


async def proxy_status() -> str:
    """Return status of running tunnels."""
    if not _running_tunnels:
        return "No proxies are currently running.\nUse app_proxy to start one."

    lines = ["Running App Proxies:", "=" * 40]
    for name, tunnel in _running_tunnels.items():
        status = "running" if tunnel._running else "stopped"
        lines.append(f"  {name} -> localhost:{tunnel.actual_port} ({status})")

    lines.append("")
    lines.append("Use app_proxy_stop to stop proxies.")
    return "\n".join(lines)
