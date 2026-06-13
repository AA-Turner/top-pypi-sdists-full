"""Shared lifecycle for the editor's listener WebSockets.

The editor front opens broadcast-style WebSockets (stdio/listen,
codebase/events, linters/events) where the server pushes messages from other
threads and the client only sends an application-level keepalive frame every
30s (desktop: webSocketService.ts). The handler thread's single job is to keep
the connection open until the client goes away.
"""

from typing import Any, Callable, Optional, Protocol

from abstra_internals.logger import AbstraLogger

# The front sends a keepalive frame every 30s, but Chrome throttles timers on
# hidden/occluded pages down to a ~60s cadence (measured live: keepalives stop
# ~2.5min after the page is hidden, and a 40s window cycled those connections
# every ~3min). 130s tolerates a throttled 60s keepalive plus one lost tick
# before treating the client as gone.
DEFAULT_INACTIVITY_TIMEOUT_SECONDS = 130


class ListenerSocket(Protocol):
    """The slice of simple_websocket.Server this lifecycle relies on."""

    thread: Any

    def receive(self, *, timeout: Optional[float] = None) -> Any: ...


class ListenerRegistry(Protocol):
    """A broadcast controller holding a listener list (register/unregister)."""

    def register(self, listener: Any, /) -> None: ...

    def unregister(self, listener: Any, /) -> None: ...


def drain_inbound_frames(
    ws: ListenerSocket,
    *,
    inactivity_timeout: float = DEFAULT_INACTIVITY_TIMEOUT_SECONDS,
) -> None:
    """Hold the connection open, consuming and discarding inbound frames.

    Returns when the client disconnects (receive raises) or stays silent for
    `inactivity_timeout` seconds (receive returns None) — with the front's 30s
    keepalive, silence means the client is gone.

    Do NOT replace this loop with `ws.event.wait()`: simple_websocket sets
    that Event both on disconnect AND on every inbound data frame, so the
    front's keepalive would wake the handler, the handler would return and
    flask_sock would close a perfectly healthy connection every ~30s.
    """
    while True:
        try:
            message = ws.receive(timeout=inactivity_timeout)
        except Exception:
            # ConnectionClosed on disconnect, or any socket-level error:
            # either way this connection is done.
            break
        if message is None:
            break


def serve_listener_websocket(
    ws: ListenerSocket,
    *,
    thread_name: str,
    registry: ListenerRegistry,
    on_registered: Optional[Callable[[Any], None]] = None,
    inactivity_timeout: float = DEFAULT_INACTIVITY_TIMEOUT_SECONDS,
) -> None:
    """Run the standard listener-WebSocket lifecycle; never raises.

    Names the reader thread, registers the socket in `registry`, optionally
    runs `on_registered(ws)` (e.g. to send an initial payload), then blocks
    draining inbound frames until disconnect/inactivity. Always unregisters.
    """
    try:
        ws.thread.name = thread_name
        registry.register(ws)
        if on_registered is not None:
            on_registered(ws)
        drain_inbound_frames(ws, inactivity_timeout=inactivity_timeout)
    except Exception as e:
        AbstraLogger.capture_exception(e)
    finally:
        registry.unregister(ws)
