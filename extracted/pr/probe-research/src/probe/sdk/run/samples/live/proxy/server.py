"""ProxyServer: the proxy's HTTP side, on its own event loop. `/health`; `/r/<secret>/...` forwarded to that
rollout's upstream (request and response bodies byte for byte, an SSE answer as it streams); a sidecar's control
routes. Nothing here waits on Probe: what it saw goes to the observer's queue."""

from __future__ import annotations

import asyncio
import hmac
import logging
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Protocol

import httpx

from ......foundation.tls.tls import ssl_context
from .dialect import Dialect
from .dialects import DEFAULT_DIALECT, get_dialect
from .framing import (
    CHUNKED_END,
    HOP_HEADERS,
    MAX_HEAD_BYTES,
    FramingError,
    Request,
    has_no_body,
    make_chunk,
    make_head,
    make_json_response,
    read_request,
)
from .observer import CallEnded, CallObserver, CallStarted
from .routes import Route, RouteTable

log = logging.getLogger("probe.samples.proxy")

UPSTREAM_CONNECT_SECONDS = 30.0
UPSTREAM_KEEPALIVE = 256
#: Response bytes kept per call for the observer; the rest streams on unread.
MAX_TEE_BYTES = 8 * 1024 * 1024
#: A canceled rollout's calls answer `403` with this code: the OpenAI and Anthropic SDKs never retry a 403.
CANCELED_CODE = "probe_canceled"
CANCELED_MESSAGE = "Probe canceled this sample (`probe samples cancel`): its model calls are refused"
UPSTREAM_ERROR_CODE = "probe_upstream_error"
UNKNOWN_ROUTE_CODE = "probe_unknown_route"
#: Both SDKs read this header before their own retry rules.
NO_RETRY = (("x-should-retry", "false"),)
CONTROL_PREFIX = "/control/"
ROUTE_PREFIX = "/r/"
#: Why a call stopped before its answer ended.
CANCELED = "canceled"
CLIENT_GONE = "client_gone"


class ControlRoutes(Protocol):
    """A sidecar's control routes (`/control/<token>/...`); `handle` runs on a worker thread."""

    token: str

    def handle(self, method: str, path: str, body: bytes) -> tuple[int, dict]: ...


class Call:
    """One call in flight on a route: its connection's task, stopped by a cancel or the client leaving."""

    def __init__(self, task: asyncio.Task) -> None:
        self.task = task
        self.reason: str | None = None
        self.has_extra_bytes = False

    def stop(self, reason: str) -> None:
        if self.reason is None:
            self.reason = reason
            self.task.cancel()


@dataclass
class _Relay:
    """One answer on its way back: what was sent so far, and the copy kept for the observer."""

    writer: asyncio.StreamWriter
    response: httpx.Response | None = None
    status: int = 0
    content_type: str = ""
    content_encoding: str = ""
    is_head_sent: bool = False
    is_chunked: bool = False
    tee: bytearray = field(default_factory=bytearray)

    def keep(self, chunk: bytes) -> None:
        room = MAX_TEE_BYTES - len(self.tee)
        if room > 0:
            self.tee += chunk[:room]

    async def write_canceled(self, shape: Dialect, is_keep_alive: bool) -> bool:
        """Answer a canceled call: a 403 when nothing was sent yet, else the API's own SSE error to end the stream.
        Returns whether the connection can be used again."""
        if not self.is_head_sent:
            self.writer.write(make_json_response(403, shape.make_error(CANCELED_CODE, CANCELED_MESSAGE),
                                                 extra=NO_RETRY, is_keep_alive=is_keep_alive))  # fmt: skip
            await self.writer.drain()
            return is_keep_alive
        if self.is_chunked and "text/event-stream" in self.content_type:
            self.writer.write(make_chunk(shape.make_stream_error(CANCELED_CODE, CANCELED_MESSAGE)) + CHUNKED_END)
            await self.writer.drain()
        return False


class ProxyServer:
    """Runs on the proxy's event loop only (`stop_calls` too: the proxy calls it with `call_soon_threadsafe`)."""

    def __init__(self, routes: RouteTable, observer: CallObserver, control: ControlRoutes | None = None) -> None:
        self._routes = routes
        self._observer = observer
        self._control = control
        self._client: httpx.AsyncClient | None = None
        self._server: asyncio.AbstractServer | None = None
        self._connections: set[asyncio.Task] = set()

    async def start(self, host: str, port: int) -> int:
        """Listen; returns the port."""
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(None, connect=UPSTREAM_CONNECT_SECONDS), follow_redirects=False,
            limits=httpx.Limits(max_connections=None, max_keepalive_connections=UPSTREAM_KEEPALIVE),
            verify=ssl_context(),  # the package's shared trust (a corporate CA bundle reaches the upstream too)
        )  # fmt: skip
        self._server = await asyncio.start_server(self._serve, host, port, limit=MAX_HEAD_BYTES)
        return int(self._server.sockets[0].getsockname()[1])  # type: ignore[attr-defined]

    def is_serving(self) -> bool:
        return self._server is not None and self._server.is_serving()

    def stop_calls(self, route: Route) -> int:
        """Abort the route's calls in flight (a cancel). Returns how many."""
        calls = list(route.calls)
        for call in calls:
            call.stop(CANCELED)
        return len(calls)

    async def stop(self) -> None:
        if self._server is not None:
            self._server.close()
        for task in list(self._connections):
            task.cancel()
        await asyncio.gather(*self._connections, return_exceptions=True)
        if self._server is not None:
            await self._server.wait_closed()
        if self._client is not None:
            await self._client.aclose()

    # -- a connection -----------------------------------------------------------------------------
    async def _serve(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
        task = asyncio.current_task()
        self._connections.add(task)  # type: ignore[arg-type]
        try:
            while True:
                request = await read_request(reader)
                if request is None or not await self._answer(request, reader, writer):
                    break
        except FramingError as exc:
            writer.write(make_json_response(exc.status, DEFAULT_DIALECT.make_error("probe_bad_request", str(exc)),
                                            is_keep_alive=False))  # fmt: skip
        except (OSError, asyncio.IncompleteReadError, asyncio.LimitOverrunError):
            pass  # the client went away
        except Exception as exc:  # noqa: BLE001 -- one connection's failure never stops the proxy
            log.debug("probe: a proxy connection failed (%s: %s)", type(exc).__name__, exc)
        finally:
            self._connections.discard(task)  # type: ignore[arg-type]
            writer.close()

    async def _answer(self, request: Request, reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> bool:
        """Answer one request; returns whether the connection takes another."""
        path, _, query = request.target.partition("?")
        if path == "/health":
            return await _write(writer, make_json_response(200, {"ok": True}, is_keep_alive=request.is_keep_alive),
                                request.is_keep_alive)  # fmt: skip
        if path.startswith(ROUTE_PREFIX):
            secret, _, rest = path[len(ROUTE_PREFIX):].partition("/")
            route = self._routes.get(secret)
            if route is not None:
                return await self._forward(request, route, "/" + rest, query, reader, writer)
        elif self._control is not None and path.startswith(CONTROL_PREFIX):
            token, _, rest = path[len(CONTROL_PREFIX):].partition("/")
            if hmac.compare_digest(token.encode(), self._control.token.encode()):
                status, payload = await asyncio.get_running_loop().run_in_executor(
                    None, self._control.handle, request.method, "/" + rest, request.body)
                return await _write(writer, make_json_response(status, payload, is_keep_alive=request.is_keep_alive),
                                    request.is_keep_alive)  # fmt: skip
        missing = DEFAULT_DIALECT.make_error(UNKNOWN_ROUTE_CODE, "no rollout has this Probe proxy address")
        return await _write(writer, make_json_response(404, missing, is_keep_alive=request.is_keep_alive),
                            request.is_keep_alive)  # fmt: skip

    # -- a call through a route -------------------------------------------------------------------
    async def _forward(self, request: Request, route: Route, api_path: str, query: str,
                       reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> bool:  # fmt: skip
        dialect = get_dialect(api_path) if request.method == "POST" else None
        shape = dialect or DEFAULT_DIALECT
        is_keep_alive = request.is_keep_alive
        if route.is_canceled:
            refused = make_json_response(403, shape.make_error(CANCELED_CODE, CANCELED_MESSAGE), extra=NO_RETRY,
                                         is_keep_alive=is_keep_alive)  # fmt: skip
            return await _write(writer, refused, is_keep_alive)
        call = Call(asyncio.current_task())  # type: ignore[arg-type]
        route.calls.add(call)
        watcher = asyncio.ensure_future(_watch_client(reader, call))
        if dialect is not None:
            self._routes.keep_request(route, dialect, request.body)
            self._observer.submit(CallStarted(route))
        relay = _Relay(writer)
        failure: str | None = None
        try:
            await self._relay(request, route.make_target(api_path, query), relay)
        except asyncio.CancelledError:
            if call.reason is None:
                raise  # the proxy is stopping
            _clear_cancel(call.task)
            failure = call.reason
            is_keep_alive = call.reason == CANCELED and await _write_canceled(relay, shape, is_keep_alive)
        except (httpx.HTTPError, httpx.InvalidURL) as exc:
            failure = f"upstream {type(exc).__name__}"
            is_keep_alive = not relay.is_head_sent and await _write(writer, make_json_response(
                502, shape.make_error(UPSTREAM_ERROR_CODE, f"the Probe proxy could not reach the model server "
                                      f"({type(exc).__name__})"), is_keep_alive=is_keep_alive), is_keep_alive)  # fmt: skip
        finally:
            route.calls.discard(call)  # first: a cancel during the awaits below must not reach this call
            watcher.cancel()
            await asyncio.wait({watcher})  # its read is gone before the connection reads the next request
            await _close(relay.response)
            if dialect is not None:
                self._observer.submit(CallEnded(route, dialect, request.body, relay.status, relay.content_type,
                                                relay.content_encoding, bytes(relay.tee), failure))  # fmt: skip
        return is_keep_alive and not call.has_extra_bytes

    async def _relay(self, request: Request, target: str, relay: _Relay) -> None:
        """Send the request upstream as it came (minus hop headers) and stream the answer back as it comes."""
        assert self._client is not None
        headers = [(name.encode("latin-1"), value.encode("latin-1")) for name, value in request.headers
                   if name.lower() not in HOP_HEADERS]  # the bytes as they came  # fmt: skip
        upstream = httpx.Request(request.method, target, headers=headers, content=request.body)
        response = relay.response = await self._client.send(upstream, stream=True)
        relay.status = response.status_code
        relay.content_type = response.headers.get("content-type", "")
        relay.content_encoding = response.headers.get("content-encoding", "")
        answer: list[tuple[str | bytes, str | bytes]] = [
            (name, value) for name, value in response.headers.raw if name.decode("latin-1").lower() not in HOP_HEADERS]
        length = response.headers.get("content-length")
        is_bodiless = has_no_body(request.method, response.status_code)
        if length is not None and "chunked" not in response.headers.get("transfer-encoding", "").lower():
            answer.append(("content-length", length))
        elif not is_bodiless:
            answer.append(("transfer-encoding", "chunked"))
            relay.is_chunked = True
        if not request.is_keep_alive:
            answer.append(("connection", "close"))
        relay.writer.write(make_head(response.status_code, answer))
        relay.is_head_sent = True
        if not is_bodiless:
            async for chunk in response.aiter_raw():
                if chunk:
                    relay.writer.write(make_chunk(chunk) if relay.is_chunked else chunk)
                    relay.keep(chunk)
                    await relay.writer.drain()
            if relay.is_chunked:
                relay.writer.write(CHUNKED_END)
        await relay.writer.drain()


async def _watch_client(reader: asyncio.StreamReader, call: Call) -> None:
    """While a call is in flight: the client closing (its SDK timed out) stops the upstream call, as a direct
    connection's close would. Bytes instead mean a pipelined request: the connection closes after this answer."""
    try:
        data = await reader.read(65536)
    except OSError:
        data = b""
    if data:
        call.has_extra_bytes = True
    else:
        call.stop(CLIENT_GONE)


async def _write_canceled(relay: _Relay, shape: Dialect, is_keep_alive: bool) -> bool:
    try:
        return await relay.write_canceled(shape, is_keep_alive)
    except OSError:
        return False


async def _write(writer: asyncio.StreamWriter, data: bytes, is_keep_alive: bool) -> bool:
    writer.write(data)
    await writer.drain()
    return is_keep_alive


async def _close(response: httpx.Response | None) -> None:
    """Close the upstream answer (an unfinished one closes its connection, which aborts the upstream request)."""
    if response is not None:
        try:
            await response.aclose()
        except Exception:  # noqa: BLE001 -- closing never fails the call
            pass


def _clear_cancel(task: asyncio.Task) -> None:
    """The cancel was this proxy's own (Python 3.11+ counts cancels; the task goes on serving)."""
    uncancel: Callable[[], int] | None = getattr(task, "uncancel", None)
    if uncancel is not None:
        uncancel()
