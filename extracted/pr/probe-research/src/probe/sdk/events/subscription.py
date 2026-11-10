"""Subscription: an EventStream read on a background thread, each event handed to the caller's callback. A
callback that raises is logged and counted, never raised into the script (D79)."""

from __future__ import annotations

import logging
import threading
from collections.abc import Callable

from ...generated.live import LiveEvent
from .follower import EventStream

log = logging.getLogger("probe.events")

#: How long `close()` waits for the thread by default.
CLOSE_WAIT_S = 5.0


class Subscription:
    """A running `probe.events.subscribe(...)`. `cursor` is the last seq it reached (pass it as `since=` to
    pick up later); `error` is what stopped it, when something did; `callback_errors` counts raised callbacks."""

    def __init__(self, events: EventStream, on_event: Callable[[LiveEvent], object]) -> None:
        self.events = events
        self.on_event = on_event
        self.error: BaseException | None = None
        self.callback_errors = 0
        self._thread = threading.Thread(target=self._run, name="probe-events", daemon=True)

    def start(self) -> Subscription:
        self._thread.start()
        return self

    def __enter__(self) -> Subscription:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    @property
    def cursor(self) -> int | None:
        return self.events.cursor

    @property
    def is_running(self) -> bool:
        return self._thread.is_alive()

    def wait_connected(self, timeout: float | None = None) -> bool:
        """Block until the stream is open on the server (its first frame came), at most `timeout` seconds."""
        return self.events.connected.wait(timeout)

    def close(self, timeout: float | None = CLOSE_WAIT_S) -> None:
        """Stop the subscription and wait up to `timeout` seconds for its thread."""
        self.events.close()
        if self._thread.is_alive() and self._thread is not threading.current_thread():
            self._thread.join(timeout)

    def _run(self) -> None:
        try:
            for event in self.events:
                self._deliver(event)
        except Exception as exc:  # noqa: BLE001 -- the script never sees it: kept on `error` and logged
            self.error = exc
            log.warning("probe.events: the subscription stopped: %s", exc)

    def _deliver(self, event: LiveEvent) -> None:
        try:
            self.on_event(event)
        except Exception:  # noqa: BLE001 -- D79: a callback's failure is logged, never raised into the script
            self.callback_errors += 1
            log.exception("probe.events: on_event raised on %s (seq %s); the subscription goes on",
                          event.kind, event.seq)
