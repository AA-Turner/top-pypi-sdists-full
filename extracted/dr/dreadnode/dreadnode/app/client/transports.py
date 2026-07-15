import asyncio
import contextlib
import queue
import threading
import typing as t
from urllib.parse import urlsplit

import httpx
from loguru import logger

from dreadnode.app.api.client import AuthenticationError

if t.TYPE_CHECKING:
    import concurrent.futures


_SENTINEL = object()


class _ThreadSafeQueueStream(httpx.AsyncByteStream):
    """Async byte stream backed by a thread-safe queue."""

    def __init__(self, q: queue.Queue[bytes | object]) -> None:
        self._queue = q

    async def __aiter__(self) -> t.AsyncIterator[bytes]:
        while True:
            chunk = await asyncio.to_thread(self._queue.get)
            if chunk is _SENTINEL:
                break
            assert isinstance(chunk, bytes)
            yield chunk


class _RuntimeSocketProtocol(t.Protocol):  # noqa: PYI046 — used structurally for typing, not subclassed
    """Minimal websocket-like transport contract used by the runtime client."""

    async def send_text(self, message: str) -> None: ...

    async def recv_text(self) -> str: ...

    async def close(self) -> None: ...


class StreamingASGITransport(httpx.AsyncBaseTransport):
    """ASGI transport backed by a single persistent server loop."""

    def __init__(
        self,
        app: t.Any,
        *,
        raise_app_exceptions: bool = True,
        root_path: str = "",
        client: tuple[str, int] = ("127.0.0.1", 0),
    ) -> None:
        self.app = app
        self.raise_app_exceptions = raise_app_exceptions
        self.root_path = root_path
        self.client = client
        self._server_loop: asyncio.AbstractEventLoop | None = None
        self._server_thread: threading.Thread | None = None
        self._websockets: set[_ASGIWebSocketConnection] = set()
        self._websockets_lock = threading.Lock()
        self._start_server_loop()

    @property
    def server_loop(self) -> asyncio.AbstractEventLoop | None:
        """Expose the owned server loop for lifecycle coordination."""
        return self._server_loop

    def require_server_loop(self) -> asyncio.AbstractEventLoop:
        """Return the active server loop or raise a structured lifecycle error."""
        loop = self._server_loop
        if loop is None or not loop.is_running():
            raise RuntimeError("In-process runtime transport server loop is not running")
        return loop

    def _start_server_loop(self) -> None:
        started = threading.Event()

        def _run() -> None:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self._server_loop = loop
            started.set()
            loop.run_forever()
            loop.close()

        self._server_thread = threading.Thread(target=_run, daemon=True, name="asgi-server-loop")
        self._server_thread.start()
        started.wait()

    async def aclose(self) -> None:
        with self._websockets_lock:
            websockets = list(self._websockets)
            self._websockets.clear()
        for websocket in websockets:
            with contextlib.suppress(Exception):
                await websocket.close()

        loop = self._server_loop
        if loop is not None and loop.is_running():
            shutdown_future = asyncio.run_coroutine_threadsafe(
                self._cancel_server_tasks(loop),
                loop,
            )
            with contextlib.suppress(Exception):
                await asyncio.to_thread(shutdown_future.result, 5)
            loop.call_soon_threadsafe(loop.stop)
        if self._server_thread is not None:
            self._server_thread.join(timeout=5)
        self._server_loop = None
        self._server_thread = None

    async def _cancel_server_tasks(self, loop: asyncio.AbstractEventLoop) -> None:
        current_task = asyncio.current_task(loop)
        tasks = [
            task for task in asyncio.all_tasks(loop) if task is not current_task and not task.done()
        ]
        for task in tasks:
            task.cancel()
        if tasks:
            await asyncio.gather(*tasks, return_exceptions=True)
        await loop.shutdown_asyncgens()
        await loop.shutdown_default_executor()

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        server_loop = self.require_server_loop()

        scope = {
            "type": "http",
            "asgi": {"version": "3.0"},
            "http_version": "1.1",
            "method": request.method,
            "headers": [(k.lower(), v) for (k, v) in request.headers.raw],
            "scheme": request.url.scheme,
            "path": request.url.path,
            "raw_path": request.url.raw_path.split(b"?")[0],
            "query_string": request.url.query,
            "server": (request.url.host, request.url.port),
            "client": self.client,
            "root_path": self.root_path,
        }

        request_body = b"".join([chunk async for chunk in request.stream])  # ty: ignore[not-iterable]
        body_queue: queue.Queue[bytes | object] = queue.Queue()
        headers_ready = threading.Event()
        status_code: int | None = None
        response_headers: list[tuple[bytes, bytes]] | None = None

        async def _serve_request() -> None:
            nonlocal status_code, response_headers
            request_sent = False

            async def receive() -> dict[str, t.Any]:
                nonlocal request_sent
                if request_sent:
                    await asyncio.sleep(3600)
                    return {"type": "http.disconnect"}
                request_sent = True
                return {"type": "http.request", "body": request_body, "more_body": False}

            async def send(message: dict[str, t.Any]) -> None:
                nonlocal status_code, response_headers
                if message["type"] == "http.response.start":
                    status_code = message["status"]
                    response_headers = message.get("headers", [])
                    headers_ready.set()
                elif message["type"] == "http.response.body":
                    body = message.get("body", b"")
                    more_body = message.get("more_body", False)
                    if body and request.method != "HEAD":
                        body_queue.put(body)
                    if not more_body:
                        body_queue.put(_SENTINEL)

            await self.app(scope, receive, send)

        future = asyncio.run_coroutine_threadsafe(_serve_request(), server_loop)

        def _on_done(fut: "concurrent.futures.Future[None]") -> None:
            nonlocal status_code, response_headers
            try:
                exc = fut.exception()
            except Exception:
                return
            if exc is None:
                return
            if self.raise_app_exceptions:
                body_queue.put(_SENTINEL)
                headers_ready.set()
            else:
                logger.opt(exception=True).debug("ASGI app exception suppressed, synthesizing 500")
                if status_code is None:
                    status_code = 500
                if response_headers is None:
                    response_headers = []
                body_queue.put(_SENTINEL)
                headers_ready.set()

        future.add_done_callback(_on_done)
        await asyncio.to_thread(headers_ready.wait)

        exc = future.exception() if future.done() else None
        if exc is not None and self.raise_app_exceptions:
            raise exc

        assert status_code is not None
        assert response_headers is not None

        return httpx.Response(
            status_code,
            headers=response_headers,
            stream=_ThreadSafeQueueStream(body_queue),
        )

    async def websocket_connect(
        self,
        *,
        url: str,
        headers: dict[str, str] | None = None,
    ) -> "_ASGIWebSocketConnection":
        """Open an in-process websocket connection on the persistent server loop."""
        connection = await _ASGIWebSocketConnection.connect(
            app=self.app,
            server_loop=self.require_server_loop(),
            url=url,
            client=self.client,
            root_path=self.root_path,
            headers=headers or {},
            raise_app_exceptions=self.raise_app_exceptions,
        )
        with self._websockets_lock:
            self._websockets.add(connection)
        connection.add_close_callback(self._discard_websocket)
        return connection

    def _discard_websocket(self, connection: "_ASGIWebSocketConnection") -> None:
        with self._websockets_lock:
            self._websockets.discard(connection)


class _ASGIWebSocketConnection:
    """Thread-bridged websocket connection against an in-process ASGI app."""

    def __init__(
        self,
        *,
        inbound: queue.Queue[dict[str, t.Any] | object],
        outbound: queue.Queue[dict[str, t.Any] | BaseException | object],
        app_future: "concurrent.futures.Future[None]",
        open_event: threading.Event,
        close_event: threading.Event,
        close_state: dict[str, t.Any],
    ) -> None:
        self._inbound = inbound
        self._outbound = outbound
        self._app_future = app_future
        self._open_event = open_event
        self._close_event = close_event
        self._close_state = close_state
        self._closed = False
        self._on_close: list[t.Callable[[_ASGIWebSocketConnection], None]] = []

    def add_close_callback(
        self,
        callback: t.Callable[["_ASGIWebSocketConnection"], None],
    ) -> None:
        self._on_close.append(callback)

    @classmethod
    async def connect(
        cls,
        *,
        app: t.Any,
        server_loop: asyncio.AbstractEventLoop,
        url: str,
        client: tuple[str, int],
        root_path: str,
        headers: dict[str, str],
        raise_app_exceptions: bool,
    ) -> "_ASGIWebSocketConnection":
        parsed = urlsplit(url)
        inbound: queue.Queue[dict[str, t.Any] | object] = queue.Queue()
        outbound: queue.Queue[dict[str, t.Any] | BaseException | object] = queue.Queue()
        open_event = threading.Event()
        close_event = threading.Event()
        close_state: dict[str, t.Any] = {"accepted": False, "code": None, "reason": None}

        inbound.put({"type": "websocket.connect"})

        scope = {
            "type": "websocket",
            "asgi": {"version": "3.0"},
            "scheme": parsed.scheme or "ws",
            "path": parsed.path or "/",
            "raw_path": (parsed.path or "/").encode("utf-8"),
            "query_string": parsed.query.encode("utf-8"),
            "headers": [
                (key.lower().encode("utf-8"), value.encode("utf-8"))
                for key, value in headers.items()
            ],
            "server": (
                parsed.hostname or "127.0.0.1",
                parsed.port or (443 if parsed.scheme == "wss" else 80),
            ),
            "client": client,
            "root_path": root_path,
            "subprotocols": [],
        }

        async def _serve_socket() -> None:
            async def receive() -> dict[str, t.Any]:
                message = await asyncio.to_thread(inbound.get)
                if message is _SENTINEL:
                    return {"type": "websocket.disconnect", "code": 1000}
                assert isinstance(message, dict)
                return t.cast("dict[str, t.Any]", message)

            async def send(message: dict[str, t.Any]) -> None:
                msg_type = message.get("type")
                if msg_type == "websocket.accept":
                    close_state["accepted"] = True
                    open_event.set()
                    return
                if msg_type == "websocket.send":
                    outbound.put(message)
                    return
                if msg_type == "websocket.close":
                    close_state["code"] = message.get("code")
                    close_state["reason"] = message.get("reason")
                    close_event.set()
                    open_event.set()
                    outbound.put(message)

            await app(scope, receive, send)

        app_future = asyncio.run_coroutine_threadsafe(_serve_socket(), server_loop)

        def _on_done(future: "concurrent.futures.Future[None]") -> None:
            try:
                exc = future.exception()
            except Exception:
                return
            if exc is not None:
                outbound.put(exc)
                open_event.set()

        app_future.add_done_callback(_on_done)
        connection = cls(
            inbound=inbound,
            outbound=outbound,
            app_future=app_future,
            open_event=open_event,
            close_event=close_event,
            close_state=close_state,
        )

        await asyncio.to_thread(open_event.wait)
        if not close_state["accepted"]:
            await connection.close()
            detail = close_state.get("reason") or "WebSocket connection rejected"
            code = int(close_state.get("code") or 1008)
            if code == 4401:
                raise AuthenticationError(f"401: {detail}")
            raise RuntimeError(f"WebSocket connect failed ({code}): {detail}")

        if app_future.done():
            exc = app_future.exception()
            if exc is not None and raise_app_exceptions:
                raise exc

        return connection

    async def send_text(self, message: str) -> None:
        if self._closed:
            raise RuntimeError("WebSocket connection already closed")
        self._inbound.put({"type": "websocket.receive", "text": message})

    async def recv_text(self) -> str:
        raw = await asyncio.to_thread(self._outbound.get)
        if isinstance(raw, BaseException):
            raise raw
        if raw is _SENTINEL:
            raise RuntimeError("WebSocket connection closed")
        assert isinstance(raw, dict)
        message = t.cast("dict[str, t.Any]", raw)
        msg_type = str(message.get("type", ""))
        if msg_type == "websocket.send":
            text = message.get("text")
            if isinstance(text, str):
                return text
            bytes_payload = message.get("bytes")
            if isinstance(bytes_payload, bytes):
                return bytes_payload.decode("utf-8")
            raise RuntimeError("WebSocket frame missing text or bytes payload")
        if msg_type == "websocket.close":
            self._closed = True
            code = int(message.get("code") or 1000)
            reason = str(message.get("reason") or "closed")
            if code == 4401:
                raise AuthenticationError(f"401: {reason}")
            raise RuntimeError(f"WebSocket closed ({code}): {reason}")
        raise RuntimeError(f"Unexpected websocket message: {msg_type}")

    async def close(self) -> None:
        if self._closed:
            return
        self._closed = True
        try:
            self._inbound.put({"type": "websocket.disconnect", "code": 1000})
            self._inbound.put(_SENTINEL)
            self._outbound.put(_SENTINEL)
            with contextlib.suppress(Exception):
                await asyncio.to_thread(self._app_future.result, 5)
        finally:
            for callback in self._on_close:
                callback(self)


class _WebsocketsRuntimeSocket:
    """Runtime websocket backed by the network websockets client."""

    def __init__(self, connection: t.Any) -> None:
        self._connection = connection

    async def send_text(self, message: str) -> None:
        await self._connection.send(message)

    async def recv_text(self) -> str:
        message = await self._connection.recv()
        if isinstance(message, bytes):
            return message.decode("utf-8")
        return str(message)

    async def close(self) -> None:
        await self._connection.close()
