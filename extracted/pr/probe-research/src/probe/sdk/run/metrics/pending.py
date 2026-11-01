"""PendingRowsMixin, Run's methods: log(commit=False): hold a step's values until it commits, and
flush held rows before anything that needs them."""

from __future__ import annotations
import json
from typing import Any

from ....foundation.safe_warn import safe_warn as _diagnostics
from ..context import context as unit_context
from ....models import MetricPointIn

#: How long ``finish()`` waits for a lock ``log()`` holds before giving up on the
#: held rows (#2025 review). A signal handler that calls ``finish()`` -- SLURM
#: ``--signal=USR1``, submitit preemption -- runs on the thread it interrupted,
#: so if that thread was inside ``log()`` the lock is never released and a
#: plain wait would hang the handler forever.
_CLOSE_LOCK_WAIT_SECONDS = 0.5


class _PendingRow:
    """One step's values held by ``Run.log(commit=False)`` (plan (f)).

    Last value per key wins. A numeric point's identity includes its
    dimensions and labels, as a series' does, so two ranks' ``loss`` stay two
    points; a key logged as a number and then as a string (or back) keeps only
    the latest. ``wall_clock`` is the latest contributing call's time."""

    __slots__ = ("step", "points", "other", "wall_clock")

    def __init__(self, step: int | None) -> None:
        self.step = step
        self.points: dict[tuple[str, str, str], tuple] = {}
        self.other: dict[str, Any] = {}
        self.wall_clock: str | None = None

    def merge(
        self,
        numeric: dict[str, float],
        other: dict[str, Any],
        dims: dict[str, Any],
        labs: dict[str, Any],
        span_id: str | None,
        agg: str | None,
        wall_clock: str,
    ) -> None:
        if other:
            for ident in [i for i in self.points if i[0] in other]:
                del self.points[ident]
            self.other.update(other)
        if numeric:
            coords = json.dumps(dims, sort_keys=True, default=repr)
            labels = json.dumps(labs, sort_keys=True, default=repr)
            for key, value in numeric.items():
                self.other.pop(key, None)
                ident = (key, coords, labels)
                self.points.pop(ident, None)
                self.points[ident] = (key, value, dims, labs, span_id, agg)
        self.wall_clock = wall_clock

    def point_list(self) -> list[tuple]:
        return list(self.points.values())


class PendingRowsMixin:
    """Part of Run: its methods run with `self` the Run; compose() folds them into Run."""

    def _log_pending(
        self,
        kind: str,
        step: Any,
        numeric: dict[str, float],
        other: dict[str, Any],
        dimensions: dict[str, Any] | None,
        labels: dict[str, Any] | None,
        span_id: str | None,
        agg: str | None,
        wall_clock: str | None,
        strict: bool | None,
        commit: bool | None,
    ):
        """Plan (f)'s buffered path; the rules are in :meth:`log`'s docstring.

        A pending row with an omitted step PEEKS the auto counter rather than
        drawing from it, so ``commit=False`` never advances the axis; the row
        claims its step when it is written. The network I/O runs outside the
        lock.

        A signal handler's ``log()`` runs on the thread it interrupted, so if
        that thread was inside the locked block below, the lock is never
        released. Past a short wait this call is then written at once, as an
        ordinary write, instead of hanging. This call holds and flushes
        nothing; the row the interrupted call was building stays pending."""
        dims, labs = unit_context.merged(dimensions, labels)
        stamp = wall_clock if wall_clock is not None else _log_stamp()
        if commit is False:
            # Validate NOW (#2025 review): a bad point surfacing at the next,
            # innocent call would lose both that call and this row.
            for key, value in numeric.items():
                MetricPointIn(
                    key=key, kind=kind, value=value, wall_clock=stamp, dimensions=dims,
                    labels=labs or None, span_id=span_id, agg=agg,
                )
            if self._closed_status is not None and not self._commit_after_finish_warned:
                self._commit_after_finish_warned = True
                _diagnostics.warn(
                    "probe.log(commit=False) after finish(): this row is held until the "
                    "next log() call on this run, and finish() will not send it.",
                    stacklevel=3,
                )
        flush: _PendingRow | None = None
        row: _PendingRow | None = None
        if self._pending_lock.acquire(timeout=_CLOSE_LOCK_WAIT_SECONDS):
            try:
                row = self._pending_rows.get(kind)
                if step is _UNSET:
                    target = row.step if row is not None else self._peek_step(kind)
                else:
                    target = None if step is None else int(step)
                if row is not None and row.step != target:
                    flush, row = self._pending_rows.pop(kind), None
                if commit is False:
                    if numeric or other:
                        if row is None:
                            row = self._pending_rows[kind] = _PendingRow(target)
                        row.merge(numeric, other, dims, labs, span_id, agg, stamp)
                    row = None
                elif row is not None:
                    del self._pending_rows[kind]
                    row.merge(numeric, other, dims, labs, span_id, agg, stamp)
            finally:
                self._pending_lock.release()
            if flush is not None:
                self._flush_row(kind, flush)
            if commit is False:
                return None
        else:
            # Held by the log() this call interrupted (see docstring).
            target = self._peek_step(kind) if step is _UNSET else (None if step is None else int(step))
        if row is None:
            # Nothing was pending at this call's step (a row at another step was
            # just flushed): this call is an ordinary write.
            if not numeric and not other:
                return None
            row = _PendingRow(target)
            row.merge(numeric, other, dims, labs, span_id, agg, stamp)
        self._claim_step(kind, row.step)
        return self._write_row(
            kind, row.step, row.point_list(), row.other, row.wall_clock, strict, stacklevel=4
        )

    def _flush_row(self, kind: str, row: "_PendingRow") -> None:
        """Write a pending row fail-open, and never raise: this runs inside a
        later ``log()`` or inside ``finish()``, and a row the caller already let
        go of must not fail either. ``strict=False`` journals it on a transport
        failure (even on a ``fail_open=False`` client) so the close barrier
        delivers it."""
        try:
            self._claim_step(kind, row.step)
            # 5 frames: _write_row <- here <- _log_pending/_flush_pending_rows
            # <- log/finish <- the caller's line.
            self._write_row(
                kind, row.step, row.point_list(), row.other, row.wall_clock, False, stacklevel=5
            )
        except Exception as exc:  # noqa: BLE001 -- see docstring
            _diagnostics.warn(
                f"probe.log: could not write the commit=False row for step {row.step} "
                f"({type(exc).__name__}: {_diagnostics.describe(exc)}); it was dropped.",
                stacklevel=4,
            )

    def _flush_pending_rows(self) -> None:
        """Write every row ``log(commit=False)`` still holds. Called first thing
        in ``finish()``, which every close funnels through (``__exit__``, the
        exit hook). Never raises."""
        if not self._pending_rows:
            return
        # A signal handler calling finish() runs on the thread it interrupted.
        # If that thread was inside log(), it holds one of these locks and never
        # will release it: give up on the held rows rather than hang (#2025
        # review). `_steps_lock` first, so rows are only taken once both are free.
        if not self._steps_lock.acquire(timeout=_CLOSE_LOCK_WAIT_SECONDS):
            self._warn_rows_not_flushed()
            return
        self._steps_lock.release()
        if not self._pending_lock.acquire(timeout=_CLOSE_LOCK_WAIT_SECONDS):
            self._warn_rows_not_flushed()
            return
        try:
            rows = list(self._pending_rows.items())
            self._pending_rows.clear()
        finally:
            self._pending_lock.release()
        for kind, row in rows:
            self._flush_row(kind, row)

    def _warn_rows_not_flushed(self) -> None:
        _diagnostics.warn(
            "probe: finish() could not flush the log(commit=False) row(s): a log() call "
            "was interrupted mid-write (finish() called from a signal handler?), so they "
            "were not sent. Everything logged without commit=False is unaffected.",
            stacklevel=4,
        )
from probe.sdk.run.handle import _UNSET  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.run.metrics.values import _log_stamp  # noqa: E402 -- pieces need each other; the front door loads this one first
