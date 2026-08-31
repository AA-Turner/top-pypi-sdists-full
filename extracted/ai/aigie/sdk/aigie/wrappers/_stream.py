"""Streaming support shared by the provider wrappers.

A streamed call is over on the last chunk, or when the caller walks away - not
when the method that returned the stream returned. Each provider supplies only
what is its own: how to read a chunk, and what to do at the end.
"""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Any

from aigie.context_manager import RunContext
from aigie.wrappers._base import contained, emit_span_now, record_failure

logger = logging.getLogger(__name__)


class TracedStream:
    """A provider's event stream, wrapped so its span is emitted exactly once.

    Not a generator: an unstarted generator never runs its `finally`, so a
    caller that raises before reading loses the span on the error path most
    worth tracing. This emits from `close` and `__del__`, behind a flag so it
    happens once however the stream ends.
    """

    def __init__(
        self,
        run_ctx: RunContext,
        events: Any,
        *,
        collect: Callable[[Any], None],
        finish: Callable[[], None],
    ) -> None:
        self._run_ctx = run_ctx
        self._events = events
        self._iterator: Any = None
        self._collect = collect
        self._finish = finish
        self._emitted = False
        self._closed = False

    def __iter__(self) -> TracedStream:
        return self

    def __next__(self) -> Any:
        if self._closed:
            # The span is already on the wire; anything read now would be
            # recorded into a payload nobody will send again.
            raise StopIteration
        try:
            event = next(self._source())
        except StopIteration:
            self._run_ctx.metadata.setdefault("status", "success")
            self._emit()
            raise
        except BaseException as error:
            record_failure(self._run_ctx, error)
            self._emit()
            raise

        contained("reading a stream chunk", self._collect, event)
        return event

    def __copy__(self) -> TracedStream:
        """Copying a stream yields the same stream.

        A real copy would share the provider stream and the run context but take
        its own emit flag, so dropping it would close the caller's stream and
        burn the span's one emission. A stream is a resource rather than a
        value - `deepcopy` of a response dict is an ordinary thing to do, and
        instrumentation does not get to turn it into an exception.
        """
        return self

    def __deepcopy__(self, memo: dict) -> TracedStream:
        memo[id(self)] = self
        return self

    def __reduce__(self) -> Any:
        """Refuse to be pickled.

        Unlike a copy, a pickle round-trip produces a genuinely separate object
        with its own emit flag over a stream it cannot own - a duplicate span
        under an id already on the wire. There is no honest reduction.
        """
        raise TypeError(f"{type(self).__name__} cannot be pickled")

    def __getattr__(self, name: str) -> Any:
        """Delegate anything we do not implement to the provider's own stream.

        A Bedrock `EventStream` carries more than iteration - `get_initial_response`
        among it - and the wrapper promises the caller the same object.

        `__dict__` directly, never `self._events`: that attribute is itself
        resolved through here, so on a half-built instance - which is what the
        copy and pickle protocols probe - the lookup would recurse until the
        stack ran out rather than raising `AttributeError`.
        """
        events = self.__dict__.get("_events")
        if events is None or name.startswith("__"):
            raise AttributeError(name)
        return getattr(events, name)

    def disarm(self) -> None:
        """Neutralize a stream the caller never received.

        If installing this wrapper fails, the object is dropped mid-statement
        and `__del__` runs - which would close the provider's stream out from
        under the caller who is about to be handed it, and file the call as
        abandoned. Disarming makes both no-ops.
        """
        self._emitted = True
        self._closed = True

    def close(self) -> None:
        """End a stream the caller stopped reading, or never started.

        Closes the provider's stream too. `__getattr__` cannot do it: `close` is
        defined here, so delegation never reaches the one underneath, and an
        unreturned connection is a pool slot lost for the life of the process.
        """
        if self._closed:
            return
        self._closed = True
        self._run_ctx.metadata.setdefault("status", "cancelled")
        self._emit()
        close = getattr(self.__dict__.get("_events"), "close", None)
        if callable(close):
            contained("closing the provider stream", close)

    def _source(self) -> Any:
        """Resolve the underlying iterator on first use.

        Deferred so an uniterable stream raises in the caller's own loop rather
        than earlier, from inside the wrapper.
        """
        if self._iterator is None:
            self._iterator = iter(self._events)
        return self._iterator

    def _emit(self) -> None:
        if self._emitted:
            return
        self._emitted = True
        contained("finalizing the stream", self._finish)
        emit_span_now(self._run_ctx)

    def __del__(self) -> None:
        # Last resort, for a stream dropped without being read or closed. It
        # runs during garbage collection, where raising is not an option.
        try:
            self.close()
        except Exception as e:  # noqa: BLE001 - GC has no caller to raise to
            logger.debug("[wrapper] Emitting a dropped stream's span failed: %s", e)
