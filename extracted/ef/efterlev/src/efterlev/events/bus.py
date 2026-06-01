"""The event bus + the active-bus context, mirroring `active_store`.

`EventBus` is a minimal synchronous pub/sub: producers call `publish`,
renderers `subscribe`. Synchronous is the right primitive for the spine —
the scan producer is synchronous, and the eventual Textual renderer
bridges into its async loop by posting a message from its subscriber
callback (a sync→async hand-off Textual supports). No async machinery is
needed here, so none is added.

`emit(event)` is the producer-facing entry point: it publishes to the
bus bound by `active_event_bus(...)` for the current call chain, or
no-ops when none is bound. That keeps event emission additive — the
normal CLI path has no active bus, so `emit` does nothing and behavior is
unchanged; Studio (or a test) binds a bus to receive the stream.
"""

from __future__ import annotations

import contextvars
from collections.abc import Callable, Iterator
from contextlib import contextmanager

from efterlev.events.schema import StudioEvent

Subscriber = Callable[[StudioEvent], None]


class EventBus:
    """A minimal synchronous event bus."""

    def __init__(self) -> None:
        self._subscribers: list[Subscriber] = []

    def subscribe(self, callback: Subscriber) -> Callable[[], None]:
        """Register `callback`; returns an unsubscribe function."""
        self._subscribers.append(callback)

        def _unsubscribe() -> None:
            if callback in self._subscribers:
                self._subscribers.remove(callback)

        return _unsubscribe

    def publish(self, event: StudioEvent) -> None:
        """Deliver `event` to every subscriber, in registration order.

        Iterates a copy so a subscriber may unsubscribe during delivery
        without disturbing the walk.
        """
        for callback in list(self._subscribers):
            callback(event)


_active_bus: contextvars.ContextVar[EventBus | None] = contextvars.ContextVar(
    "efterlev_active_event_bus",
    default=None,
)


def get_active_bus() -> EventBus | None:
    """Return the bus bound for the current call chain, or None."""
    return _active_bus.get()


@contextmanager
def active_event_bus(bus: EventBus) -> Iterator[EventBus]:
    """Scope-bind `bus` so `emit(...)` reaches it for the duration."""
    token = _active_bus.set(bus)
    try:
        yield bus
    finally:
        _active_bus.reset(token)


def set_active_bus(bus: EventBus) -> None:
    """Bind `bus` for the rest of this process (no scope, no reset).

    Unlike `active_event_bus`, this is process-global — for a one-shot CLI
    subprocess that records its whole run to a sink (see
    `efterlev.events.recorder`). A Typer callback can call this so every
    subsequent `emit(...)` in that invocation reaches the bus. Don't use it
    in long-lived processes or tests; use `active_event_bus` there.
    """
    _active_bus.set(bus)


def emit(event: StudioEvent) -> None:
    """Publish `event` to the active bus, or no-op when none is bound.

    The producer-facing API. Cheap and safe to call unconditionally — in
    the normal CLI path there is no active bus, so this returns immediately.
    """
    bus = _active_bus.get()
    if bus is not None:
        bus.publish(event)
