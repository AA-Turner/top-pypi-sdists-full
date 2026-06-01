"""Shared WebSocket connection to the app service event gateway.

A single :class:`SharedWebSocket` instance is shared across all product
modules (config, flags) within one :class:`SmplClient`.  Product modules
register listeners for specific event types; the shared connection
dispatches incoming events to the appropriate listeners.
"""

from __future__ import annotations

import asyncio
import json
import logging
import threading
import traceback
from collections import defaultdict
from collections.abc import Callable
from typing import Any

import websockets
import websockets.asyncio.client

from smplkit._debug import debug
from smplkit._version import __version__

logger = logging.getLogger("smplkit.ws")

_BACKOFF_SCHEDULE = [1, 2, 4, 8, 16, 32, 60]
_WS_USER_AGENT = f"smplkit-python-sdk/{__version__}"


class SharedWebSocket:
    """Manages a single WebSocket connection to the app service event gateway.

    The app service gateway protocol:
    - Connect to ``wss://app.smplkit.com/api/ws/v1/events?api_key={key}``
    - Receive ``{"type": "connected"}`` on success
    - Receive events: ``{"event": "config_changed", ...}``, ``{"event": "flag_changed", ...}``
    - No subscribe message — the API key determines the account
    - Heartbeat: server sends ``"ping"`` (text), client responds with ``"pong"``
    """

    def __init__(self, *, app_base_url: str, api_key: str, metrics: Any = None) -> None:
        self._app_base_url = app_base_url
        self._api_key = api_key
        self._metrics = metrics

        self._listeners: dict[str, list[Callable[[dict[str, Any]], None]]] = defaultdict(list)
        self._listeners_lock = threading.Lock()

        self._connection_status: str = "disconnected"
        self._closed = False
        self._ws: Any = None
        self._ws_loop: asyncio.AbstractEventLoop | None = None
        self._ws_thread: threading.Thread | None = None

    # ------------------------------------------------------------------
    # Listener registration
    # ------------------------------------------------------------------

    def on(self, event_name: str, callback: Callable[[dict[str, Any]], None]) -> None:
        """Register a listener for a specific event type."""
        with self._listeners_lock:
            self._listeners[event_name].append(callback)

    def off(self, event_name: str, callback: Callable[[dict[str, Any]], None]) -> None:
        """Unregister a listener for a specific event type."""
        with self._listeners_lock:
            try:
                self._listeners[event_name].remove(callback)
            except ValueError:
                pass

    def _dispatch(self, event_name: str, data: dict[str, Any]) -> None:
        """Dispatch an event to all registered listeners."""
        with self._listeners_lock:
            callbacks = list(self._listeners.get(event_name, []))
        if not callbacks:
            debug("websocket", f"no handler registered for event: {event_name!r}")
            return
        debug("websocket", f"routing {event_name!r} to {len(callbacks)} handler(s)")
        for cb in callbacks:
            try:
                cb(data)
            except Exception:
                logger.error("Exception in event listener for %r", event_name, exc_info=True)

    # ------------------------------------------------------------------
    # Connection status
    # ------------------------------------------------------------------

    @property
    def connection_status(self) -> str:
        """Return the current connection status."""
        return self._connection_status

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    def start(self) -> None:
        """Start the background WebSocket thread."""
        debug("websocket", "starting shared WebSocket background thread")
        self._closed = False
        thread = threading.Thread(
            target=self._ws_thread_entry,
            name="smplkit-shared-ws",
            daemon=True,
        )
        self._ws_thread = thread
        thread.start()

    def stop(self) -> None:
        """Stop the WebSocket connection and background thread."""
        debug("websocket", "stopping shared WebSocket")
        self._closed = True
        self._connection_status = "disconnected"

        if self._ws is not None and self._ws_loop is not None:
            try:
                future = asyncio.run_coroutine_threadsafe(self._ws.close(), self._ws_loop)
                future.result(timeout=2.0)
            except Exception:
                pass

        if self._ws_thread is not None and self._ws_thread.is_alive():
            self._ws_thread.join(timeout=2.0)

    # ------------------------------------------------------------------
    # Background thread
    # ------------------------------------------------------------------

    def _ws_thread_entry(self) -> None:
        """Entry point for the WebSocket background thread."""
        loop = asyncio.new_event_loop()
        self._ws_loop = loop
        try:
            loop.run_until_complete(self._ws_main())
        except Exception:
            logger.error("Shared WebSocket thread exited unexpectedly", exc_info=True)
        finally:
            pending = asyncio.all_tasks(loop)
            for task in pending:
                task.cancel()
            if pending:
                loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            loop.close()

    async def _ws_main(self) -> None:
        """Main async routine: connect and enter the receive loop."""
        try:
            await self._connect()
        except Exception as exc:
            safe_url = self._build_ws_url().split("?")[0]
            logger.warning(
                "Shared WebSocket connection failed on startup (url: %s), will attempt reconnection: %s",
                safe_url,
                exc,
            )
            debug("websocket", traceback.format_exc().strip())
            await self._reconnect()

    # ------------------------------------------------------------------
    # URL construction
    # ------------------------------------------------------------------

    def _build_ws_url(self) -> str:
        """Construct the WebSocket URL from the app base URL."""
        url = self._app_base_url
        if url.startswith("https://"):
            ws_url = "wss://" + url[len("https://") :]
        elif url.startswith("http://"):
            ws_url = "ws://" + url[len("http://") :]
        else:
            ws_url = "wss://" + url
        ws_url = ws_url.rstrip("/")
        return f"{ws_url}/api/ws/v1/events?api_key={self._api_key}"

    # ------------------------------------------------------------------
    # Connect / receive / reconnect
    # ------------------------------------------------------------------

    async def _connect(self) -> None:
        """Open a WebSocket connection and wait for the connected confirmation."""
        url = self._build_ws_url()
        self._connection_status = "connecting"
        safe_url = url.split("?")[0]
        debug("websocket", f"connecting to {safe_url}")

        # CloudFront's WAF blocks WebSocket upgrades that omit a User-Agent
        # header. The `websockets` library doesn't set one by default
        # (browsers do), so inject it explicitly to match the User-Agent
        # we'd send on HTTP. Without this, the upgrade returns HTTP 403
        # before reaching our backend.
        self._ws = await websockets.asyncio.client.connect(
            url,
            additional_headers={"User-Agent": _WS_USER_AGENT},
        )
        debug("websocket", "WebSocket connected, waiting for confirmation")

        # Wait for {"type": "connected"} confirmation
        raw = await self._ws.recv()
        data = json.loads(raw)
        if data.get("type") == "error":
            err_msg = data.get("message")
            debug("websocket", f"connection error from server: {err_msg!r}")
            raise RuntimeError(f"Connection error: {err_msg}")

        self._connection_status = "connected"
        debug("websocket", f"connected to {safe_url}")
        if self._metrics is not None:
            self._metrics.record_gauge("platform.websocket_connections", 1, unit="connections")
        await self._receive_loop()

    async def _receive_loop(self) -> None:
        """Process incoming WebSocket messages until closed."""
        while not self._closed:
            try:
                message = await self._ws.recv()

                # Heartbeat: server sends "ping" (text), we respond with "pong"
                if message == "ping":
                    debug("websocket", "ping received, sending pong")
                    await self._ws.send("pong")
                    continue

                debug("websocket", f"event received: {message}")
                data = json.loads(message)
                event = data.get("event")
                if event:
                    self._dispatch(event, data)
            except websockets.ConnectionClosed as exc:
                if self._closed:
                    break
                close_code = exc.rcvd.code if exc.rcvd else None
                logger.warning(
                    "Shared WebSocket closed (code=%s), reconnecting...",
                    close_code,
                )
                debug("websocket", f"connection closed (code={close_code}), reconnecting")
                self._connection_status = "reconnecting"
                if self._metrics is not None:
                    self._metrics.record_gauge("platform.websocket_connections", 0, unit="connections")
                await self._reconnect()
                break
            except Exception as exc:
                if self._closed:
                    break
                logger.error(
                    "Unexpected error in shared WebSocket receive loop",
                    exc_info=True,
                )
                debug("websocket", f"unexpected error in receive loop: {exc!r}")
                self._connection_status = "reconnecting"
                if self._metrics is not None:
                    self._metrics.record_gauge("platform.websocket_connections", 0, unit="connections")
                await self._reconnect()
                break

    async def _reconnect(self) -> None:
        """Reconnect with exponential backoff."""
        attempt = 0
        while not self._closed:
            delay = _BACKOFF_SCHEDULE[min(attempt, len(_BACKOFF_SCHEDULE) - 1)]
            logger.info(
                "Shared WebSocket reconnecting in %d seconds (attempt %d)...",
                delay,
                attempt + 1,
            )
            debug("websocket", f"reconnecting in {delay}s (attempt {attempt + 1})")
            await asyncio.sleep(delay)
            if self._closed:
                return
            try:
                await self._connect()
                debug("websocket", "reconnected successfully")
                logger.info("Shared WebSocket reconnected successfully.")
                return
            except Exception as exc:
                logger.warning("Shared WebSocket reconnect attempt %d failed.", attempt + 1)
                debug("websocket", f"reconnect attempt {attempt + 1} failed: {exc!r}")
                attempt += 1
