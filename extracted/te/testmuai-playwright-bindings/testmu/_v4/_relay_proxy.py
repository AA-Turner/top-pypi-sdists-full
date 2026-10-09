"""Playwright WebSocket relay proxy for persistent cloud sessions.

Used on cloud runs so an external client can take over the browser (via
--ws-endpoint) and the main test can reconnect with full state replay.

Cloud-only — local sessions do not start this proxy.
"""
import asyncio
import json
import logging
from collections import deque

import websockets

logger = logging.getLogger("testmu")


# ── MessageBuffer ──

class MessageBuffer:
    """Bounded message buffer with drop-oldest overflow policy."""

    def __init__(self, max_size: int = 1000):
        self._buffer: deque = deque(maxlen=max_size)

    def add(self, message: str | bytes) -> None:
        """Add a message. If buffer is full, oldest message is dropped."""
        self._buffer.append(message)

    def flush(self) -> list[str | bytes]:
        """Return all buffered messages and clear the buffer."""
        messages = list(self._buffer)
        self._buffer.clear()
        return messages

    def __len__(self) -> int:
        return len(self._buffer)


# ── ObjectSnapshot ──

class ObjectSnapshot:
    """Tracks Playwright object lifecycle via __create__/__dispose__ messages.

    Maintains an ordered dict of live objects keyed by GUID.
    Provides replay() to return __create__ messages for all live objects
    in insertion order (parent-before-child).
    """

    def __init__(self):
        self._objects: dict[str, str] = {}  # guid -> raw __create__ message

    def track(self, message: str | bytes) -> None:
        """Inspect a server-to-client message and update the snapshot."""
        if isinstance(message, bytes):
            return
        try:
            data = json.loads(message)
        except (json.JSONDecodeError, TypeError):
            return

        method = data.get("method")
        params = data.get("params", {})

        if method == "__create__":
            guid = params.get("guid")
            if guid:
                self._objects[guid] = message
        elif method == "__dispose__":
            guid = params.get("guid")
            if guid:
                self._objects.pop(guid, None)

    @staticmethod
    def is_lifecycle_message(message: str | bytes) -> bool:
        """Check if a message is a __create__ or __dispose__ lifecycle message."""
        if isinstance(message, bytes):
            return False
        try:
            data = json.loads(message)
            return data.get("method") in ("__create__", "__dispose__")
        except (json.JSONDecodeError, TypeError):
            return False

    def replay(self) -> list[str]:
        """Return __create__ messages for all live objects in insertion order."""
        return list(self._objects.values())


# ── PlaywrightRelayProxy ──

def _is_ws_closed(ws) -> bool:
    """Check if a WebSocket connection is closed (compatible with websockets 12+)."""
    return ws.close_code is not None


def _is_response_message(msg) -> bool:
    """Check if a message is an RPC response (carries a truthy "id").

    Matches playwright._impl._connection.Connection.dispatch() exactly: it pops
    self._callbacks[id] whenever `id` is truthy, unconditionally — it does not
    check for the absence of "method" first. Some response envelopes carry a
    "method" alongside "id", so filtering on "method not in data" as well let
    those slip through replay and still triggered KeyError on the new client's
    Connection, which never registered that id.
    """
    if not isinstance(msg, str):
        return False
    try:
        data = json.loads(msg)
    except (json.JSONDecodeError, TypeError):
        return False
    return bool(data.get("id"))


class UpstreamConnectionError(Exception):
    """Raised when the upstream connection fails or is lost."""
    pass


class PlaywrightRelayProxy:
    """WebSocket relay proxy for persistent Playwright connections.

    Connects to an upstream Playwright server and keeps the connection alive.
    Exposes a local WebSocket server for client scripts to connect to.

    Protocol-aware behavior:
    - First client: full transparent relay (including `initialize` handshake)
    - Reconnecting clients: intercepts `initialize`, replays cached object tree,
      then resumes transparent relay for all subsequent messages.
    """

    def __init__(self, upstream_url: str, local_port: int = 8765):
        self.upstream_url = upstream_url
        self.local_port = local_port
        self._upstream_ws = None
        self._client_ws = None
        self._snapshot = ObjectSnapshot()
        self._buffer = MessageBuffer(max_size=1000)
        self._ready = asyncio.Event()
        self._shutdown = asyncio.Event()
        self._server = None
        self._drain_task = None
        self._initialized = False  # True after first client completes initialize
        self._init_response = None  # cached initialize response (without id)
        self._server_messages = []  # ALL server→client messages (for full replay)
        # Synchronization
        self._client_connected = asyncio.Event()
        self._client_disconnected = asyncio.Event()
        self._client_disconnected.set()

    async def wait_ready(self):
        await self._ready.wait()

    def shutdown(self):
        self._shutdown.set()

    async def start(self):
        logger.info(f"Connecting to upstream: {self.upstream_url[:80]}...")
        print(f"[RelayProxy] Connecting to upstream: {self.upstream_url[:80]}...", flush=True)
        try:
            self._upstream_ws = await asyncio.wait_for(
                websockets.connect(
                    self.upstream_url, max_size=None, close_timeout=10,
                    open_timeout=5 * 60,
                    # Disable client-side keepalive pings. The `websockets`
                    # default (ping_interval=20s, ping_timeout=20s) closes the
                    # upstream when the grid does not pong within 20s — which
                    # happens whenever the grid is briefly backed up (e.g. a
                    # kane-cli network-capture burst during execute_kane_cli),
                    # closing the browser mid-handoff (TargetClosedError). The
                    # TypeScript relay uses Node `ws`, which does not auto-ping,
                    # so the same handoff survives there; this matches it.
                    ping_interval=None,
                ),
                timeout=5 * 60,
            )
        except asyncio.TimeoutError:
            raise UpstreamConnectionError(
                f"Timeout connecting to upstream (5m): {self.upstream_url[:80]}"
            )
        except Exception as e:
            raise UpstreamConnectionError(
                f"Failed to connect to upstream {self.upstream_url[:80]}: {e}"
            ) from e

        logger.info(f"Connected to upstream")
        print("[RelayProxy] Connected to upstream", flush=True)

        self._server = await websockets.serve(
            self._handle_client, "127.0.0.1", self.local_port, max_size=None,
        )
        self.local_port = self._server.sockets[0].getsockname()[1]
        logger.info(f"Local server listening on ws://127.0.0.1:{self.local_port}")

        self._drain_task = asyncio.create_task(self._drain_upstream())
        self._ready.set()

        await self._shutdown.wait()

        # Clean shutdown
        self._drain_task.cancel()
        try:
            await self._drain_task
        except asyncio.CancelledError:
            pass
        if not _is_ws_closed(self._upstream_ws):
            await self._upstream_ws.close()
        if self._client_ws and not _is_ws_closed(self._client_ws):
            await self._client_ws.close()
        self._server.close()
        await self._server.wait_closed()
        logger.info("Proxy shut down.")

    async def _drain_upstream(self):
        """Buffer upstream messages when no client is connected."""
        while not self._shutdown.is_set():
            try:
                await asyncio.wait_for(self._client_disconnected.wait(), timeout=0.1)
            except asyncio.TimeoutError:
                continue
            if self._client_connected.is_set():
                await asyncio.sleep(0)
                continue
            try:
                msg = await asyncio.wait_for(self._upstream_ws.recv(), timeout=0.5)
                self._track_server_message(msg)
                # Orphaned responses (answering a now-dead client's own call) must
                # not be replayed to whichever different client connects next.
                if not _is_response_message(msg):
                    self._buffer.add(msg)
            except asyncio.TimeoutError:
                continue
            except websockets.exceptions.ConnectionClosed:
                logger.error("Upstream connection closed")
                self._shutdown.set()
                return

    def _track_server_message(self, msg):
        """Track server-to-client messages for replay on reconnect."""
        self._snapshot.track(msg)
        # Store all non-response messages for full replay
        if isinstance(msg, str):
            if _is_response_message(msg):
                return
            self._server_messages.append(msg)
        else:
            self._server_messages.append(msg)

    async def _handle_client(self, ws):
        if self._client_ws is not None and not _is_ws_closed(self._client_ws):
            logger.warning("Rejecting client: another client is already connected")
            await ws.close(1013, "Another client is already connected")
            return

        self._client_connected.set()
        self._client_disconnected.clear()
        self._drain_task.cancel()
        try:
            await self._drain_task
        except asyncio.CancelledError:
            pass

        self._client_ws = ws
        logger.info(f"Client connected from {ws.remote_address}")

        try:
            if not self._initialized:
                # First client: transparent relay, capture init handshake
                await self._handle_first_client(ws)
            else:
                # Reconnecting client: intercept initialize, replay state
                await self._handle_reconnecting_client(ws)
        except websockets.exceptions.ConnectionClosed:
            logger.info("Client disconnected")
        finally:
            self._client_ws = None
            self._client_connected.clear()
            self._client_disconnected.set()
            self._drain_task = asyncio.create_task(self._drain_upstream())

    async def _handle_first_client(self, ws):
        """First client: relay everything, but capture init response and objects."""
        logger.info("First client — transparent relay with init capture")

        # Wait for client to send initialize
        init_msg = await ws.recv()
        init_data = json.loads(init_msg)
        init_id = init_data.get("id")
        logger.info(f"Relaying initialize (id={init_id})")

        # Relay initialize to upstream
        await self._upstream_ws.send(init_msg)

        # Read responses until we get the initialize response (matching id)
        while True:
            resp = await self._upstream_ws.recv()
            self._track_server_message(resp)
            await ws.send(resp)

            if isinstance(resp, str):
                try:
                    data = json.loads(resp)
                    if data.get("id") == init_id:
                        # Cache the init response structure (without the id)
                        self._init_response = {k: v for k, v in data.items() if k != "id"}
                        self._initialized = True
                        logger.info("Initialize handshake captured")
                        break
                except (json.JSONDecodeError, TypeError):
                    pass

        # Flush any buffered messages
        for msg in self._buffer.flush():
            await ws.send(msg)

        # Continue with normal relay
        await self._relay(ws)

    async def _handle_reconnecting_client(self, ws):
        """Reconnecting client: intercept initialize, replay cached state."""
        logger.info("Reconnecting client — intercepting initialize")

        # Wait for client's initialize message
        init_msg = await ws.recv()
        init_data = json.loads(init_msg)
        init_id = init_data.get("id")
        logger.info(f"Intercepted initialize (id={init_id}), replaying cached state")

        # Replay ALL cached server→client messages (events, __create__, __adopt__, etc.)
        # This includes everything the server sent during previous sessions,
        # which builds the complete object tree with all relationships.
        for msg in self._server_messages:
            await ws.send(msg)
        logger.info(f"Replayed {len(self._server_messages)} server messages")

        # Send synthesized initialize response with client's id
        init_resp = {"id": init_id, **self._init_response}
        await ws.send(json.dumps(init_resp))
        logger.info("Sent synthesized initialize response")

        # Flush any buffered messages
        buffered = self._buffer.flush()
        for msg in buffered:
            await ws.send(msg)

        # Resume normal relay
        await self._relay(ws)

    async def _relay(self, client_ws):
        """Bidirectional relay between client and upstream."""
        async def client_to_upstream():
            while True:
                msg = await client_ws.recv()
                await self._upstream_ws.send(msg)

        async def upstream_to_client():
            while True:
                msg = await self._upstream_ws.recv()
                self._track_server_message(msg)
                await client_ws.send(msg)

        client_task = asyncio.create_task(client_to_upstream())
        upstream_task = asyncio.create_task(upstream_to_client())

        try:
            done, pending = await asyncio.wait(
                [client_task, upstream_task],
                return_when=asyncio.FIRST_COMPLETED,
            )
            for task in pending:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            for task in done:
                try:
                    task.result()
                except websockets.exceptions.ConnectionClosedOK:
                    pass
                except websockets.exceptions.ConnectionClosedError:
                    if task is upstream_task:
                        logger.error("Upstream connection lost during relay")
                        self._shutdown.set()
                except Exception as exc:
                    if task is upstream_task:
                        logger.error(f"Upstream error: {exc}")
                        self._shutdown.set()
        except Exception as e:
            logger.error(f"Relay error: {e}")
