"""
cvc.ipc — WebSocket broadcast server for inter-process communication.

Runs on ws://127.0.0.1:7843.  Any number of processes can connect as
publishers or subscribers; every message received from any client is
broadcast to all other connected clients.

Message schema
--------------
All messages are JSON with the following envelope:

    {
        "type":    str,        # event type, e.g. "commit", "ping", "agent_event"
        "source":  str,        # sender identifier, e.g. "gateway", "agent:abc"
        "payload": dict,       # arbitrary event data
        "ts":      float       # unix timestamp (filled by server on receipt)
    }

Reconnect logic (IPCClient)
---------------------------
The client uses exponential back-off: initial_delay=0.5s, cap=30s, factor=2.
After ``max_retries`` attempts the client stops trying (default: unlimited).

Usage
-----
Server (standalone process or embedded in gateway):

    import asyncio
    from cvc.ipc import IPCServer

    async def main():
        server = IPCServer()
        await server.start()
        await server.wait_closed()

    asyncio.run(main())

Client:

    import asyncio
    from cvc.ipc import IPCClient

    async def main():
        async with IPCClient() as client:
            await client.publish("ping", {"hello": "world"}, source="my_tool")
            async for msg in client.subscribe():
                print(msg)

    asyncio.run(main())
"""

from __future__ import annotations

import asyncio
import json
import logging
import time
from dataclasses import dataclass, field
from typing import Any, AsyncIterator

logger = logging.getLogger("cvc.ipc")

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

IPC_HOST = "127.0.0.1"
IPC_PORT = 7843

# ---------------------------------------------------------------------------
# Message schema
# ---------------------------------------------------------------------------


@dataclass
class IPCMessage:
    """Envelope for all IPC messages."""

    type: str
    payload: dict[str, Any] = field(default_factory=dict)
    source: str = "unknown"
    ts: float = field(default_factory=time.time)

    # ------------------------------------------------------------------
    # Serialisation helpers
    # ------------------------------------------------------------------

    def to_json(self) -> str:
        return json.dumps(
            {
                "type": self.type,
                "source": self.source,
                "payload": self.payload,
                "ts": self.ts,
            }
        )

    @classmethod
    def from_json(cls, raw: str) -> "IPCMessage":
        data = json.loads(raw)
        return cls(
            type=data.get("type", "unknown"),
            source=data.get("source", "unknown"),
            payload=data.get("payload", {}),
            ts=data.get("ts", time.time()),
        )

    @classmethod
    def ping(cls, source: str = "server") -> "IPCMessage":
        return cls(type="ping", source=source)

    @classmethod
    def pong(cls, source: str = "server") -> "IPCMessage":
        return cls(type="pong", source=source)


# ---------------------------------------------------------------------------
# Server
# ---------------------------------------------------------------------------


class IPCServer:
    """WebSocket broadcast server on port 7843.

    All connected clients receive every message published by any client.
    The server adds/stamps `ts` on every received message before forwarding.
    """

    def __init__(self, host: str = IPC_HOST, port: int = IPC_PORT) -> None:
        self.host = host
        self.port = port
        self._clients: set[Any] = set()
        self._server: Any = None
        self._lock = asyncio.Lock()

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def start(self) -> None:
        """Start the WebSocket server (non-blocking)."""
        try:
            import websockets  # type: ignore[import-untyped]
        except ImportError as exc:
            raise ImportError(
                "websockets package required for IPCServer — install with: pip install websockets"
            ) from exc

        self._server = await websockets.serve(
            self._handle_client,
            self.host,
            self.port,
            ping_interval=20,
            ping_timeout=10,
        )
        logger.info("IPC server listening on ws://%s:%s", self.host, self.port)

    async def stop(self) -> None:
        """Gracefully shut down the server."""
        if self._server is not None:
            self._server.close()
            await self._server.wait_closed()
            self._server = None
        logger.info("IPC server stopped")

    async def wait_closed(self) -> None:
        """Block until the server is stopped (e.g. via KeyboardInterrupt)."""
        if self._server is not None:
            await self._server.wait_closed()

    # ------------------------------------------------------------------
    # Connection handler
    # ------------------------------------------------------------------

    async def _handle_client(self, ws: Any) -> None:
        """Register a client and relay all its messages to peers."""
        async with self._lock:
            self._clients.add(ws)
        logger.debug("IPC client connected (total=%d)", len(self._clients))
        try:
            async for raw in ws:
                await self._relay(raw, sender=ws)
        except Exception:
            pass
        finally:
            async with self._lock:
                self._clients.discard(ws)
            logger.debug("IPC client disconnected (total=%d)", len(self._clients))

    async def _relay(self, raw: str | bytes, sender: Any) -> None:
        """Stamp the message and broadcast it to all clients including sender."""
        try:
            data = json.loads(raw)
        except (json.JSONDecodeError, TypeError):
            logger.warning("IPC: received non-JSON message, skipping")
            return

        # Server-side timestamp stamping
        data["ts"] = time.time()
        stamped = json.dumps(data)

        # Broadcast to all connected clients
        async with self._lock:
            recipients = list(self._clients)

        results = await asyncio.gather(
            *[self._safe_send(c, stamped) for c in recipients],
            return_exceptions=True,
        )
        errors = sum(1 for r in results if isinstance(r, Exception))
        if errors:
            logger.debug("IPC relay: %d send error(s) ignored", errors)

    @staticmethod
    async def _safe_send(ws: Any, message: str) -> None:
        try:
            await ws.send(message)
        except Exception as exc:
            raise exc  # gathered so exceptions are collected, not raised

    # ------------------------------------------------------------------
    # Server-side publish (inject messages without an external client)
    # ------------------------------------------------------------------

    async def broadcast(self, msg: IPCMessage) -> None:
        """Broadcast a message from the server itself to all connected clients."""
        stamped = msg.to_json()
        async with self._lock:
            recipients = list(self._clients)
        await asyncio.gather(
            *[self._safe_send(c, stamped) for c in recipients],
            return_exceptions=True,
        )


# ---------------------------------------------------------------------------
# Client
# ---------------------------------------------------------------------------


class IPCClient:
    """WebSocket client with exponential back-off reconnection.

    Designed for use as an async context manager:

        async with IPCClient() as client:
            await client.publish("event", {"key": "val"})
            async for msg in client.subscribe():
                ...

    Parameters
    ----------
    host, port     : IPC server address (default 127.0.0.1:7843)
    source         : identifies this client in the message envelope
    initial_delay  : first reconnect wait in seconds (default 0.5)
    backoff_factor : multiplier per retry (default 2.0)
    max_delay      : cap on reconnect delay (default 30.0)
    max_retries    : give up after N retries; None = unlimited (default)
    """

    def __init__(
        self,
        host: str = IPC_HOST,
        port: int = IPC_PORT,
        source: str = "client",
        initial_delay: float = 0.5,
        backoff_factor: float = 2.0,
        max_delay: float = 30.0,
        max_retries: int | None = None,
    ) -> None:
        self.url = f"ws://{host}:{port}"
        self.source = source
        self.initial_delay = initial_delay
        self.backoff_factor = backoff_factor
        self.max_delay = max_delay
        self.max_retries = max_retries

        self._ws: Any = None
        self._closed = False

    # ------------------------------------------------------------------
    # Context manager
    # ------------------------------------------------------------------

    async def __aenter__(self) -> "IPCClient":
        await self.connect()
        return self

    async def __aexit__(self, *_: Any) -> None:
        await self.close()

    # ------------------------------------------------------------------
    # Connection with reconnect
    # ------------------------------------------------------------------

    async def connect(self) -> None:
        """Connect to the IPC server, retrying with back-off on failure."""
        try:
            import websockets  # type: ignore[import-untyped]
        except ImportError as exc:
            raise ImportError(
                "websockets package required for IPCClient — install with: pip install websockets"
            ) from exc

        delay = self.initial_delay
        attempt = 0
        while not self._closed:
            try:
                self._ws = await websockets.connect(self.url)
                logger.info("IPC client connected to %s", self.url)
                return
            except Exception as exc:
                attempt += 1
                if self.max_retries is not None and attempt >= self.max_retries:
                    raise ConnectionError(
                        f"IPC: could not connect to {self.url} after {attempt} attempt(s)"
                    ) from exc
                logger.warning(
                    "IPC: connection failed (%s), retrying in %.1fs (attempt %d)…",
                    exc,
                    delay,
                    attempt,
                )
                await asyncio.sleep(delay)
                delay = min(delay * self.backoff_factor, self.max_delay)

    async def close(self) -> None:
        """Close the connection."""
        self._closed = True
        if self._ws is not None:
            try:
                await self._ws.close()
            except Exception:
                pass
            self._ws = None

    # ------------------------------------------------------------------
    # Publish
    # ------------------------------------------------------------------

    async def publish(
        self,
        type: str,  # noqa: A002
        payload: dict[str, Any] | None = None,
        source: str | None = None,
    ) -> None:
        """Send a message to the IPC server (broadcast to all peers)."""
        msg = IPCMessage(
            type=type,
            payload=payload or {},
            source=source or self.source,
        )
        await self._send_with_reconnect(msg.to_json())

    async def send(self, msg: IPCMessage) -> None:
        """Send a pre-built IPCMessage."""
        await self._send_with_reconnect(msg.to_json())

    async def _send_with_reconnect(self, raw: str) -> None:
        for _ in range(2):
            try:
                if self._ws is None:
                    await self.connect()
                await self._ws.send(raw)
                return
            except Exception:
                logger.warning("IPC: send failed, reconnecting…")
                self._ws = None
                if not self._closed:
                    await self.connect()
        raise ConnectionError("IPC: unable to send message after reconnect attempt")

    # ------------------------------------------------------------------
    # Subscribe
    # ------------------------------------------------------------------

    async def subscribe(self) -> AsyncIterator[IPCMessage]:
        """Yield IPCMessage objects as they arrive.

        Automatically reconnects on disconnect unless close() was called.
        """
        while not self._closed:
            try:
                if self._ws is None:
                    await self.connect()
                async for raw in self._ws:
                    try:
                        yield IPCMessage.from_json(raw)
                    except (json.JSONDecodeError, TypeError) as exc:
                        logger.warning("IPC: bad message skipped: %s", exc)
            except Exception as exc:
                if self._closed:
                    return
                logger.warning("IPC: subscribe disconnected (%s), reconnecting…", exc)
                self._ws = None
                await asyncio.sleep(self.initial_delay)


# ---------------------------------------------------------------------------
# Convenience: run a standalone server
# ---------------------------------------------------------------------------


async def run_server(host: str = IPC_HOST, port: int = IPC_PORT) -> None:
    """Run the IPC broadcast server until cancelled."""
    server = IPCServer(host=host, port=port)
    await server.start()
    try:
        await server.wait_closed()
    except (asyncio.CancelledError, KeyboardInterrupt):
        pass
    finally:
        await server.stop()


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(run_server())
