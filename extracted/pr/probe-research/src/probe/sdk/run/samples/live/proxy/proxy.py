"""RolloutProxy: Probe's opt-in rollout proxy (rl-next W35, B.6) in the producer's process: a local HTTP server on its
own thread and event loop that gives each rollout its own model URL, forwards its calls untouched, and records what it
sees through that rollout's producer. Health-checked at each hand-off; if it dies, only its rollouts fail."""

from __future__ import annotations

import asyncio
import logging
import socket
import threading
import time
from typing import TYPE_CHECKING, Any

from ......foundation.safe_warn import safe_warn as _diagnostics
from ......generated.records import Command, CommandKind
from ......generated.samples import AttemptOutcome
from .. import CommandRefused
from .observer import CallObserver, RouteFailed, WatchStarted
from .routes import RouteTable
from .server import ControlRoutes, ProxyServer

if TYPE_CHECKING:
    from ...samples import RunSamples
    from .. import CommandHandler
    from .routes import Route

log = logging.getLogger("probe.samples.proxy")

LOCALHOST = "127.0.0.1"
START_SECONDS = 5.0
STOP_SECONDS = 5.0
TICK_SECONDS = 0.5
#: A loop that has not ticked for this long is wedged: rollouts get the upstream URL instead.
HEALTH_STALE_SECONDS = 5.0
#: The refusal of a cancel for a sample whose calls do not go through the proxy.
NOT_ROUTED = "this sample's model calls do not go through the Probe proxy"
_ANY_HOST = frozenset({"", "0.0.0.0", "::"})


class RolloutProxy:
    """``host``: where it listens (127.0.0.1 unless remote sandboxes must reach it); ``control``: a sidecar's
    control routes. Thread-safe."""

    def __init__(self, *, host: str = LOCALHOST, port: int = 0, control: ControlRoutes | None = None) -> None:
        self.routes = RouteTable()
        self.observer = CallObserver()
        self._server = ProxyServer(self.routes, self.observer, control)
        self._host = host
        self._port = port
        self._loop: asyncio.AbstractEventLoop | None = None
        self._main: asyncio.Task | None = None
        self._stopping: asyncio.Event | None = None
        self._thread = threading.Thread(target=self._run, name="probe-rollout-proxy", daemon=True)
        self._ready = threading.Event()
        self._error: BaseException | None = None
        self._has_listened = False
        self._url_host = host
        self._last_tick = 0.0
        self._is_stopping = False
        self._declared: set[tuple[str, CommandKind]] = set()
        self._lock = threading.Lock()

    @property
    def base_url(self) -> str:
        host = self._url_host
        return f"http://{f'[{host}]' if ':' in host else host}:{self._port}"

    def start(self) -> None:
        """Listen, on the proxy's own thread. Raises when it cannot (the caller hands out upstream URLs)."""
        if self._host in _ANY_HOST:
            self._url_host = socket.getfqdn()  # listening everywhere: hand out this machine's name, looked up once
        self.observer.start()
        self._thread.start()
        if not self._ready.wait(START_SECONDS) or not self._has_listened:
            self._is_stopping = True
            self.observer.stop(STOP_SECONDS)
            raise RuntimeError(f"the Probe rollout proxy could not listen on {self._host}:{self._port}: "
                               f"{type(self._error).__name__ if self._error else 'timed out'}")  # fmt: skip

    def is_healthy(self) -> bool:
        """Listening, and its loop answered within the last few seconds."""
        return (not self._is_stopping and self._thread.is_alive() and self._server.is_serving()
                and time.monotonic() - self._last_tick < HEALTH_STALE_SECONDS)  # fmt: skip

    # -- rollouts ---------------------------------------------------------------------------------
    def open_route(self, samples: RunSamples, attempt_key: str, upstream: str) -> str:
        """The rollout's model URL (`http://127.0.0.1:<port>/r/<secret>/v1`), or ``upstream`` itself when the proxy
        fails its health check: a sick proxy never sits in a new rollout's model path."""
        if not self.is_healthy():
            return upstream
        route = self.routes.open(samples, attempt_key, upstream)
        return f"{self.base_url}/r/{route.secret}/v1"

    def end_route(self, attempt_key: str) -> None:
        """The rollout ended (`attempt_end`): its late calls still forward, unrecorded."""
        self.routes.end(attempt_key)

    def register_handlers(self, samples: RunSamples, *, can_cancel: bool) -> None:
        """The producer's `watch` (and `cancel`, only when it declares it: D84) go through this proxy for its
        routed samples; a handler it registered before still serves the others. Once per producer and kind."""
        kinds = (CommandKind.WATCH, CommandKind.CANCEL) if can_cancel else (CommandKind.WATCH,)
        for kind in kinds:
            with self._lock:
                if (samples.producer, kind) in self._declared:
                    continue
                self._declared.add((samples.producer, kind))
            samples._wrap_handler(kind, lambda previous, kind=kind: self._make_handler(kind, previous))

    def _make_handler(self, kind: CommandKind, previous: CommandHandler | None) -> CommandHandler:
        def handle(attempt_key: str, command: Command) -> Any:
            route = self.routes.find(attempt_key)
            if route is None or route.is_ended:
                if previous is not None:
                    return previous(attempt_key, command)
                if kind is CommandKind.CANCEL:
                    raise CommandRefused(NOT_ROUTED)
                return None
            return self._cancel(route) if kind is CommandKind.CANCEL else self._watch(route)

        return handle

    def _cancel(self, route: Route) -> dict:
        """Abort the rollout's call in flight, refuse its later calls (`403 probe_canceled`), end it `canceled`."""
        route.is_canceled = True
        loop = self._loop
        if loop is not None and loop.is_running():
            loop.call_soon_threadsafe(self._server.stop_calls, route)
        route.samples.attempt_end(route.attempt_key, AttemptOutcome.CANCELED)
        self.routes.end(route.attempt_key)
        return {}

    def _watch(self, route: Route) -> None:
        """Send the conversation so far, then each turn (the observer's thread does both, in call order)."""
        self.observer.submit_waiting(WatchStarted(route))

    # -- stopping ---------------------------------------------------------------------------------
    def stop(self, *, should_fail_live: bool) -> None:
        """Stop serving. ``should_fail_live``: rollouts still running through it lose their model path, so each is
        ended `error`, reason `probe_proxy` (a sidecar's stop); a run closing leaves them as they are."""
        with self._lock:
            if self._is_stopping:
                return
            self._is_stopping = True
        if should_fail_live:
            self._fail_live_routes()
        loop, stopping = self._loop, self._stopping
        if loop is not None and stopping is not None and not loop.is_closed():
            try:
                loop.call_soon_threadsafe(stopping.set)
            except RuntimeError:
                pass  # the loop closed in between
        self._thread.join(STOP_SECONDS)
        self.observer.stop(STOP_SECONDS)

    def _fail_live_routes(self) -> int:
        live = self.routes.get_live()
        for route in live:
            self.observer.submit_waiting(RouteFailed(route))
            self.routes.end(route.attempt_key)
        return len(live)

    # -- the proxy's thread -----------------------------------------------------------------------
    def _run(self) -> None:
        loop = asyncio.new_event_loop()
        self._loop = loop
        try:
            asyncio.set_event_loop(loop)
            self._main = loop.create_task(self._serve())
            loop.run_until_complete(self._main)
        except BaseException as exc:  # noqa: BLE001 -- the proxy dying is recorded, never raised into training
            self._error = exc
        finally:
            self._ready.set()
            _close_loop(loop)
            if self._has_listened and not self._is_stopping:
                failed = self._fail_live_routes()
                _diagnostics.warn(f"probe: the rollout proxy stopped ({type(self._error).__name__}); later samples call "
                               f"the model server directly, and {failed} running through it are recorded error "
                               f"(probe_proxy). Training goes on.")  # fmt: skip

    async def _serve(self) -> None:
        self._stopping = asyncio.Event()
        self._port = await self._server.start(self._host, self._port)
        self._last_tick = time.monotonic()
        self._has_listened = True
        self._ready.set()
        try:
            while not self._stopping.is_set():
                self._last_tick = time.monotonic()
                try:
                    await asyncio.wait_for(self._stopping.wait(), TICK_SECONDS)
                except asyncio.TimeoutError:
                    pass
        finally:
            await self._server.stop()


def _close_loop(loop: asyncio.AbstractEventLoop) -> None:
    try:
        loop.run_until_complete(loop.shutdown_asyncgens())
    except Exception:  # noqa: BLE001 -- closing what is left of a dead loop
        pass
    loop.close()


__all__ = ["LOCALHOST", "NOT_ROUTED", "RolloutProxy"]
