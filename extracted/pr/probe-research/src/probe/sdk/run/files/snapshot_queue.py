"""The run-open snapshot's off-thread part: the execution-record POST on its own thread with a hard
deadline, and the two writes its answer feeds, queued in order and never after the close."""

from __future__ import annotations

import atexit
import os
import threading
import time
import weakref
from collections.abc import Callable
from typing import Any

from ....foundation.durable.durable import backoff_delays
from ....foundation.safe_warn import safe_warn as _diagnostics
from ... import errors
from ...capture import code as _snapshot

#: The execution record's POST at run open, on its own thread: every attempt (retries
#: included) ends by this many seconds after the first one starts. The server hashes the body
#: AFTER its content guard scrubs it, so the client cannot name `content_hash` itself.
EXECUTION_RECORD_TIMEOUT_SECONDS = 5.0
#: How long the record waits for the pushed base before it POSTs: it is part of the record
#: (`base_commit`/`remote`), so the env_ref matches what `run.snapshot()` would pin.
PUSHED_BASE_WAIT_SECONDS = _snapshot.LS_REMOTE_OPEN_CAP + 0.5
#: How long past the record's deadline a close still waits for its thread to say how it went
#: (the request ends AT the deadline; the answer takes milliseconds more).
_ANSWER_GRACE_SECONDS = 0.25
#: The least time a close must have left to wake a record still waiting for `ls-remote`: with
#: less, a POST started now would most likely land after the close gave up on it (an orphan).
_RECORD_WAKE_FLOOR_SECONDS = 0.5
#: The retry pause, 0.2 s doubling to 1 s: a blip's scale, inside a 5 s budget.
_RETRY_BACKOFF = (0.2, 1.0)
_RETRY_STATUSES = frozenset({408, 425, 429, 500, 502, 503, 504})

#: The most the interpreter's exit waits for open snapshots nobody closed (`client.run()`
#: without `finish()`): their records, then their writes, before the process is gone.
_AT_EXIT_WAIT_SECONDS = 3.0

_WAITING: Any = object()
#: Every started snapshot of this process, for `_settle_at_exit`.
_STARTED: weakref.WeakSet = weakref.WeakSet()
_at_exit_lock = threading.Lock()
_is_at_exit_registered = False


def post_execution_record(
    client: Any, body: dict, *, deadline: float, should_stop: Callable[[], bool] | None = None
) -> str | None:
    """POST the record by ``deadline`` (`time.monotonic()`), retrying what a retry can fix (a
    lost connection, 429, 5xx): its `content_hash`. Content-addressed, so a replay is harmless.
    ``should_stop`` (the close shut the gate) ends the retries: one landing then is a record
    nobody pins. Raises the last error."""
    from ...delivery.transport.deadlines import deadline_scope

    pauses = backoff_delays(None, _RETRY_BACKOFF)
    while True:
        try:
            with deadline_scope(deadline):
                reply = client.transport.post("/v1/execution-records", body)
            return (reply or {}).get("content_hash")
        except errors.DeadlineExceeded:
            raise
        except errors.RosError as exc:
            if not isinstance(exc, errors.TransportError) and exc.status not in _RETRY_STATUSES:
                raise
            pause = max(next(pauses), exc.retry_after or 0.0)
            if time.monotonic() + pause >= deadline:
                raise
            time.sleep(pause)
            if should_stop is not None and should_stop():
                raise


def note_record_gap(client: Any, why: str) -> str:
    """A record the open could not get: a capture gap (counted in the outbox). Returns the one
    warning to say, which the caller says after the gate's work is done (a stderr may block)."""
    reason = f"execution record not recorded at run open: {why}"
    try:
        client.journal.note_capture_gap(reason)
    except Exception:  # noqa: BLE001 -- a client with no journal has no gap ledger
        pass
    return (
        f"probe: {reason}; this run has no env_ref. Its code bytes, code-snapshot row and "
        "launch context were queued at open."
    )


class PendingSnapshot:
    """The open's writes that wait for the execution record, queued once each, in this order:
    the env_ref PATCH (``pin``), then the code-snapshot row again with its env_ref and pushed
    base (``rewrite_row``; the open already queued it without them).

    One thread waits for the pushed base (`answer_pushed`, the `ls-remote` thread), POSTs the
    record and queues both. `settle` (a close, a terminal status, an explicit `snapshot()`)
    shuts the gate: it waits for the record at most to its deadline, then queues whatever is
    missing itself, and an answer arriving after it queues nothing. Writes run under one lock
    and are journal appends only (`queue_only`); warnings go out after the lock is released.
    So no write of this snapshot lands behind the run's terminal status however long its POST
    hangs, and a close never waits on more than one local append (O3).
    """

    def __init__(
        self,
        client: Any,
        record_body: dict,
        *,
        pin: Callable[[str | None], str | None],
        rewrite_row: Callable[[str | None, str | None, str | None], None],
        should_wait_for_pushed: bool,
    ) -> None:
        self._client = client
        self._record_body = record_body
        self._pin = pin
        self._rewrite_row = rewrite_row
        self._lock = threading.Lock()
        self._record: Any = _WAITING
        self._pushed: Any = _WAITING if should_wait_for_pushed else (None, None)
        self._pushed_answered = threading.Event()
        if not should_wait_for_pushed:
            self._pushed_answered.set()
        self._is_pinned = False
        self._is_row_final = False
        self._is_settled = False
        #: When a close woke the record (`settle`): its POST must end by then, while the close
        #: still waits for the answer.
        self._post_by: float | None = None
        #: Set once the record's outcome is final and its PATCH queued (or the gate shut).
        self._record_done = threading.Event()
        self._deadline = time.monotonic()
        #: The process that owns this snapshot: a forked child never settles it (it would wait
        #: on a lock its fork may have copied held, and blank the parent's row).
        self._pid = os.getpid()

    @property
    def is_settled(self) -> bool:
        return self._is_settled

    def start(self) -> None:
        """Start the record's thread: the pushed-base wait, then the POST's own deadline."""
        self._deadline = (
            time.monotonic() + PUSHED_BASE_WAIT_SECONDS + EXECUTION_RECORD_TIMEOUT_SECONDS
        )
        _settle_at_exit_once()
        _STARTED.add(self)
        thread = threading.Thread(
            target=self._post_record, name="probe-execution-record", daemon=True
        )
        try:
            thread.start()
        except RuntimeError:
            # No thread to be had: the record (pushed-base wait included, up to ~7.5 s)
            # runs on the caller's thread instead.
            self._post_record()

    def answer_pushed(self, base: str | None, remote: str | None) -> None:
        """The `ls-remote` thread's answer. Queues nothing: it rides the record and the row."""
        with self._lock:
            if self._pushed is _WAITING:
                self._pushed = (base, remote)
        self._pushed_answered.set()

    def wait_for_record(self) -> None:
        """Block until the record's outcome is final (its PATCH queued), at most until its
        deadline: for a reader of `Run.env_ref` that must not race the pin."""
        self._record_done.wait(self._get_seconds_left(None))

    def settle(self, wait_until: float | None = None) -> None:
        """Shut the gate: wait for the record until ``wait_until`` (never past its own
        deadline), then queue what is still missing, here. Idempotent, and a second call
        finishes what an interrupted first one left. A no-op in a forked child."""
        if os.getpid() != self._pid:
            return
        try:
            seconds_left = 0.0 if self._is_settled else self._get_seconds_left(wait_until)
            if seconds_left >= _RECORD_WAKE_FLOOR_SECONDS:
                # A close does not wait out `ls-remote`: the pushed base rides the record only if
                # it answered first (plan T5), so the POST starts now. Only with time to wait
                # for its answer, and ending in it: with less, or past it, the gate shuts first
                # and the woken thread could POST an orphan record after it.
                with self._lock:
                    self._post_by = time.monotonic() + seconds_left - _ANSWER_GRACE_SECONDS
                self.answer_pushed(None, None)
            if seconds_left > 0:
                self._record_done.wait(seconds_left)  # a record already on its way
        finally:
            # Even when the wait is interrupted (Ctrl-C in a close): the status queued next
            # must still find the gate shut.
            self._shut_gate()

    def _get_seconds_left(self, wait_until: float | None) -> float:
        until = self._deadline + _ANSWER_GRACE_SECONDS
        if wait_until is not None:
            until = min(until, wait_until)
        return max(0.0, until - time.monotonic())

    def _post_record(self) -> None:
        self._pushed_answered.wait(PUSHED_BASE_WAIT_SECONDS)
        with self._lock:
            if self._pushed is _WAITING:
                self._pushed = (None, None)  # too late to be part of the record
            base, remote = self._pushed
            is_settled = self._is_settled
            post_by = self._post_by
        if is_settled:
            return  # the close shut the gate first: a record now is one nobody pins (an orphan)
        body = _with_pushed_base(self._record_body, base, remote)
        failure: Exception | None = None
        deadline = min(self._deadline, time.monotonic() + EXECUTION_RECORD_TIMEOUT_SECONDS)
        if post_by is not None:
            deadline = min(deadline, post_by)
        try:
            content_hash = post_execution_record(
                self._client, body, deadline=deadline, should_stop=lambda: self._is_settled
            )
        except Exception as exc:  # noqa: BLE001 -- capture never fails a run
            content_hash, failure = None, exc
        with self._lock:
            if self._is_settled:
                return  # the close gave up waiting and recorded the gap itself
            self._record = content_hash
            notices = self._queue_ready()
        if failure is not None:
            notices.insert(0, note_record_gap(self._client, f"{type(failure).__name__} ({failure})"))
        # Done before anything is said (a successful async open always has a notice): a stderr
        # that blocks must not hold a reader of the pin, queued already (final review of #3792).
        self._record_done.set()
        self._say(notices)

    def _shut_gate(self) -> None:
        with self._lock:
            self._is_settled = True
            is_abandoned = self._record is _WAITING
            if is_abandoned:
                self._record = None
            if self._pushed is _WAITING:
                self._pushed = (None, None)
        # A record thread still waiting for the pushed base wakes, sees the gate shut, posts nothing.
        self._pushed_answered.set()
        gap = note_record_gap(self._client, "no answer before the run closed") if is_abandoned else None
        notices: list[str] = []
        try:
            with self._lock:
                notices = self._queue_ready()
            self._record_done.set()
        finally:
            # Said even when a Ctrl-C cut the queueing short: the gap is said once, here.
            self._say([gap, *notices] if gap else notices)

    def _queue_ready(self) -> list[str]:
        """Under the lock: queue whatever the answers allow, in order, as journal appends only
        (`queue_only`: never a direct send, which a hung DNS lookup could hold past any
        deadline). Each flag flips only after its write returned, so an interrupted write is
        retried by the next settle."""
        from ...delivery.sender import queue_only
        from ..context.context import detached

        notices: list[str] = []
        if self._record is _WAITING:
            return notices
        # `detached`: the row belongs to the run, not to a unit the settling thread has open.
        with queue_only(), detached():
            self._queue_writes(notices)
        return notices

    def _queue_writes(self, notices: list[str]) -> None:
        if not self._is_pinned:
            notice = self._run_quietly(self._pin, self._record)
            self._is_pinned = True
            if notice:
                notices.append(notice)
        if self._pushed is _WAITING or self._is_row_final:
            return
        self._run_quietly(self._rewrite_row, self._record, *self._pushed)
        self._is_row_final = True

    @staticmethod
    def _run_quietly(write: Callable[..., Any], *args: Any) -> Any:
        try:
            return write(*args)
        except Exception as exc:  # noqa: BLE001 -- runs on a daemon thread or in a close
            return f"probe: the open's code snapshot was not fully queued ({exc})"

    @staticmethod
    def _say(notices: list[str]) -> None:
        for notice in notices:
            _diagnostics.warn(notice)


def _settle_at_exit_once() -> None:
    global _is_at_exit_registered
    with _at_exit_lock:
        if not _is_at_exit_registered:
            atexit.register(_settle_at_exit)
            _is_at_exit_registered = True


def _settle_at_exit() -> None:
    """The interpreter is exiting: settle this process's snapshots nobody closed, so their
    records' answers (or the gaps saying there were none) are queued, not lost silently.
    A closed run's is settled already: a no-op."""
    deadline = time.monotonic() + _AT_EXIT_WAIT_SECONDS
    for pending in list(_STARTED):
        try:
            pending.settle(deadline)
        except Exception:  # noqa: BLE001 -- interpreter teardown: never raise from here
            pass


def _with_pushed_base(body: dict, base: str | None, remote: str | None) -> dict:
    """The record body with the pushed base in its manifest, as `run.snapshot()` sends it."""
    manifest = (body.get("code") or {}).get("manifest")
    if not isinstance(manifest, dict):
        return body
    return {
        **body,
        "code": {**body["code"], "manifest": {**manifest, "base_commit": base, "remote": remote}},
    }
