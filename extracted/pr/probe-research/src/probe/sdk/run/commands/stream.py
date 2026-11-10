"""ProducerStream: one run handle's producer stream, shared by every follower of the run's own notices. The server
keeps ONE producer stream per writer session (a newer one replaces the older, `app/live/admission.py`), so the sample
command listener (`samples.command`, rl-next W34) and the run command listener (`run.command`, agentic W&B W20) must
not open one each: they would replace each other in turn. Each follows its kind here; the stream carries the union
and hands each event to the kind's followers (control events to all). Why: DESIGN.md "The live stream"."""

from __future__ import annotations

import logging
import threading
import weakref
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..run import Run

logger = logging.getLogger(__name__)

#: Kinds about the stream, not the data: every follower gets them (`resync` says to read again).
CONTROL_KINDS = frozenset({"resync", "lagged"})


class ProducerStream:
    """The handle's one `probe.events.subscribe(run, writer=<session>)`, over the union of the kinds followed."""

    def __init__(self, run: Run) -> None:
        try:
            self._run: Callable[[], Run | None] = weakref.ref(run)
        except TypeError:  # a stand-in with no weakref slot (a test's namespace): held plainly
            self._run = lambda: run
        self._lock = threading.Lock()
        self._followers: dict[str, list[Callable[[Any], object]]] = {}
        self.subscription: Any = None

    def follow(self, kind: str, handler: Callable[[Any], object], *, since: int | None = None) -> Any:
        """Hand `kind`'s events to `handler`; (re)open the stream when the kind is new or the stream stopped. Returns
        the subscription (None when it could not open: the writer beat stays the backstop)."""
        with self._lock:
            handlers = self._followers.setdefault(kind, [])
            is_new_kind = not handlers
            if handler not in handlers:
                handlers.append(handler)
            current = self.subscription
            if current is not None and getattr(current, "is_running", True) and not is_new_kind:
                return current
            cursor = since if since is not None else getattr(current, "cursor", None)
            if current is not None:
                _close(current)
            self.subscription = self._open(cursor)
            return self.subscription

    def stop_following(self, kind: str, handler: Callable[[Any], object]) -> None:
        """Stop handing `kind` to `handler`; the stream closes once nothing follows it (the other followers keep it)."""
        with self._lock:
            handlers = self._followers.get(kind, [])
            if handler in handlers:
                handlers.remove(handler)
            if not handlers:
                self._followers.pop(kind, None)
            if self._followers:
                return
            current, self.subscription = self.subscription, None
        if current is not None:
            _close(current)

    def close(self) -> None:
        with self._lock:
            current, self.subscription = self.subscription, None
            self._followers.clear()
        if current is not None:
            _close(current)

    def _open(self, since: int | None) -> Any:
        run = self._run()
        if run is None:
            return None
        try:
            from probe.sdk import events

            return events.subscribe(run=str(run.id), writer=str(run.session_id), kinds=sorted(self._followers),
                                    on_event=self._hand_on, client=run._client, since=since)  # fmt: skip
        except Exception as exc:  # noqa: BLE001 -- the writer beat still delivers
            logger.debug("probe: run %s: the producer stream did not open: %s", run.id, exc)
            return None

    def _hand_on(self, event: Any) -> None:
        kind = getattr(event, "kind", None)
        if kind in CONTROL_KINDS:
            targets = [handler for handlers in list(self._followers.values()) for handler in handlers]
        else:
            targets = list(self._followers.get(kind, ()))
        for handler in targets:
            try:
                handler(event)
            except Exception:  # noqa: BLE001 -- one follower's failure never stops the others
                logger.exception("probe: a producer stream follower raised on %s", kind)


def _close(subscription: Any) -> None:
    try:
        subscription.close(timeout=1.0)
    except Exception as exc:  # noqa: BLE001 -- closing a follower never fails a finish
        logger.debug("probe: closing a producer stream: %s", exc)


__all__ = ["CONTROL_KINDS", "ProducerStream"]
