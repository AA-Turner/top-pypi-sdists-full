"""MetricsMixin, Run's methods: run.log -- one step's points in one POST, the step counter, flatten
warnings, hardware metrics."""

from __future__ import annotations
from collections.abc import Mapping
import os
from typing import Any

from ....foundation.safe_warn import safe_warn as _diagnostics
from ..launch import preempt as _preempt
from ..context import context as unit_context
# What a metric point's step and key must fit (review of #2053): see
# `unstorable.drop_unstorable_points`, the choke point every metrics POST
# passes; `Run.log` checks first only to warn with the step and key it saw.
from ...values.unstorable import MAX_METRIC_KEY_BYTES
from ...values.unstorable import STEP_MAX as _STEP_MAX
from ...values.unstorable import STEP_MIN as _STEP_MIN
from ...values.unstorable import key_too_long as _key_too_long
from ....models import MetricPointIn
from probe.sdk.run.handle import _UNSET
from probe.sdk.run.metrics.values import (
    _FLATTEN_MAX_DEPTH,
    _NESTED_KEY_BUDGET,
    _NESTED_KEY_MAX_CHARS,
    _as_metric_value,
    _flatten,
    _is_omegaconf,
    _json_safe,
    _log_stamp,
)
from probe.sdk.routes import WriteOp, path_for

#: How many distinct flattening warnings one run remembers (#2009 review).
_FLATTEN_WARNINGS_REMEMBERED = 256

#: Why a mapping was kept whole, as a warning names it.
_KEPT_WHOLE_REASONS = {
    "depth": f"nested past {_FLATTEN_MAX_DEPTH} levels",
    "cycle": "a dict that contains itself",
    "unreadable": "a mapping that could not be read",
    "length": f"a flattened key would pass {_NESTED_KEY_MAX_CHARS} characters",
    "budget": (
        f"this run already has {_NESTED_KEY_BUDGET} distinct keys from nested dicts; "
        "a dict keyed by data (example ids, file names) would mint a series per key -- "
        "log it as a list or an artifact instead"
    ),
}


#: Plan (f): how many recent steps ``Run.log`` remembers the sent step-record
#: attributes of, so a repeat write to one of them sends the union.
_STEP_ATTRIBUTES_REMEMBERED = 64


class MetricsMixin:
    """Part of Run: its methods run with `self` the Run; compose() folds them into Run."""

    def _next_step(self, kind: str) -> int:
        with self._steps_lock:
            # The hardware rail never consults the resume floor: its steps
            # are epoch-derived, not counted, and stay invisible to the
            # training rails' resume machinery.
            floor = 0 if kind == "hardware" else self._auto_step_floor
            step = self._steps.get(kind, floor)
            self._steps[kind] = step + 1
            return step

    def _note_step(self, kind: str, step: int) -> None:
        """Move the auto counter past an explicitly-given step.

        Without this, mixing ``log(step=i)`` with a bare ``log()`` would restart
        the auto sequence at 0 and stack a second set of points on steps the loop
        already used."""
        with self._steps_lock:
            self._steps[kind] = max(self._steps.get(kind, 0), step + 1)

    # -- metrics ------------------------------------------------------------
    def log(
        self,
        metrics: dict[str, Any],
        *,
        step: int | None = _UNSET,
        kind: str = "model",
        wall_clock: str | None = None,
        dimensions: dict[str, Any] | None = None,
        labels: dict[str, Any] | None = None,
        span_id: str | None = None,
        agg: str | None = None,
        strict: bool | None = None,
        commit: bool | None = None,
    ):
        """Append metric points. Fail-open by default (spools on failure).

        DECIDE THE SHAPE BEFORE YOU CALL THIS. Series identity is
        ``(run,kind,key,dims_hash)``, so every distinct ``dimensions`` combination
        is a SEPARATE series — and a series holding one point has nothing to plot,
        so it renders as a scalar tile rather than a graph. Each metric is one of
        three shapes:

        * **curve** (loss, lr, reward over time) — one series, many points,
          distinguished by ``step``. ONLY ``step`` makes a curve; spreading values
          across a dimension does not.
        * **headline scalar** (final accuracy) — one series, one point, 0-2
          low-cardinality dims.
        * **breakdown** (accuracy by category) — one series per category value.

        Budget it at the write: series ≈ the PRODUCT of your dimension
        cardinalities. Past ~50 you have designed a wall of tiles. That failure is
        silent — every call succeeds, the values are correct, the data stays fully
        queryable, and the only symptom is an unreadable run page — so assert the
        count after the first run instead of eyeballing the dashboard::

            series = client.run_series(run.id)     # one row per series
            assert len(series) < 50, f"{len(series)} series — a wall of tiles"

        ``dimensions`` is a bounded flat label map (<=8 keys) of the LOW-CARDINALITY
        axes you actually intend to group by — split, seed, rank, difficulty,
        category. Never an identifier: ``example_id``, a row id, a uuid, a
        filename, a per-field name each mint their own one-point series (500
        examples logged with ``example_id`` as a dimension = 500 series = 500
        tiles and zero graphs). Per-sample identity goes in ``labels`` instead
        (<=32 keys, POINT identity only — it does NOT widen the series), and
        per-item detail belongs in an artifact, which is where analysis code reads
        it from anyway. Metrics are for what a human should see; artifacts are for
        what code reads. ``span_id`` is an optional exemplar pointer to the span
        the value was produced under. Both maps merge over the ambient
        :meth:`unit` context (the explicit call site wins per key); a key in both
        maps raises ``ValueError``. Dimension-less points stay byte-identical.
        Built through the generated ``MetricBatch``/``MetricPointIn``, so schema
        drift fails here, not as a server 422.

        The headline number must be exactly ONE series: a computed view resolves a
        key and REFUSES one carrying several dimension variants ("series X has N
        dimension variants"). So never log a headline scalar and a per-item cloud
        under the same key — use two (``accuracy`` and ``accuracy_per_example``),
        and put the high-cardinality one under its own ``kind`` so the run page
        shows the handful of numbers that matter while the detail stays queryable.

        ``agg`` DECLARES the key's reduce fn (mean|sum|min|max|count) so a later
        grouped read can omit its own (server 0062: an omitted read-side ``agg``
        resolves to the declared one, else mean; conflicting declarations 422).
        The producer knows whether a count sums or a loss averages; declaring it
        at the write is what saves every reader from guessing.

        ``wall_clock`` defaults to the time of THIS call (strictly increasing
        within the process), so a point the outbox holds through an outage
        keeps the time it was logged; pass it only for an event that happened
        earlier. ``log_derived*`` sends none, and the server then stamps arrival.

        Nested dicts flatten to ``/`` keys, the separator the run page sections
        panels by: ``log({"eval": {"acc": 0.9, "note": "ok"}})`` writes the point
        ``eval/acc`` and puts ``eval/note`` in the step record, all at ONE step.
        Any ``Mapping`` flattens (an OmegaConf ``DictConfig`` too); lists do not,
        and an empty mapping writes nothing. An explicit ``"a/b"`` beside a nested
        ``{"a": {"b": ...}}`` wins, with a warning once per key per run. A mapping
        nested past 16 levels, or one that contains itself, stays one step
        attribute. ``dimensions`` and ``labels`` are never flattened (they must
        stay flat maps). W&B's own history uses ``.`` for nesting, so a run
        brought in with ``probe import wandb`` keeps ``a.b`` keys: a different
        series from ``a/b``.

        ``commit`` (W&B's spelling): ``commit=False`` holds this call's values in
        a pending row for its step instead of writing them. The next call
        without ``commit=False`` at the same step, or with ``step`` omitted,
        merges into that row and writes it once (last value per key wins); a
        call at a different step writes the pending row first. ``finish()`` --
        and so the ``with`` block and the exit hook -- writes a row still
        pending; a crash before that loses it, as in W&B. Pending rows are per
        ``kind``. One difference from W&B: a bare ``log()`` after
        ``log(step=5)`` lands at 6 here (W&B: 5), because an explicit step
        always moves the counter past itself.

        Non-numeric values logged twice at one step keep the first call's keys
        too (new wins per key): the server replaces a step record whole, so the
        SDK sends the union for the steps it wrote recently."""
        # A SIGTERM handler installed since `probe.init` that runs ours only
        # after its own (Lightning's) gets ours put first (`preempt.run_first`).
        _preempt.run_first()
        # Resume guard (research-os#364): a step at or below the resume point is a retry (DESIGN.md).
        if (
            kind != "hardware"
            and self._resume_from_step is not None
            and step is not _UNSET
            and step is not None
            and step <= self._resume_from_step
        ):
            return self._drop_below_resume(step, strict=strict)
        # Plan (d): only a Mapping value (and any DictConfig) flattens to `/` keys (DESIGN.md).
        if _is_omegaconf(metrics) or any(isinstance(value, Mapping) for value in metrics.values()):
            metrics = self._flatten_metrics(metrics)
        numeric: dict[str, float] = {}
        other: dict[str, Any] = {}
        for key, value in metrics.items():
            as_number = _as_metric_value(value)
            if as_number is None:
                other[key] = _json_safe(key, value)
            else:
                numeric[key] = as_number

        # Plan (f): `commit=False`, or a row pending for this kind, takes the buffered path.
        if commit is False or kind in self._pending_rows:
            return self._log_pending(
                kind, step, numeric, other, dimensions, labels, span_id, agg,
                wall_clock, strict, commit,
            )

        # Split BEFORE drawing a step: a call with nothing to write consumes no index (DESIGN.md).
        if not numeric and not other:
            return None

        if step is _UNSET:
            step = self._next_step(kind)
        elif step is not None:
            step = int(step)
            self._note_step(kind, step)
        if self._resume_drops and kind != "hardware" and step is not None:
            self._note_resumed(step)

        dims, labs = unit_context.merged(dimensions, labels)
        if numeric and wall_clock is None:
            # Plan 1.4: stamp when the loop LOGGED the points, frozen into the journaled body (DESIGN.md).
            wall_clock = _log_stamp()
        points = [(key, value, dims, labs, span_id, agg) for key, value in numeric.items()]
        return self._write_row(kind, step, points, other, wall_clock, strict, stacklevel=3)

    def _write_row(
        self,
        kind: str,
        step: int | None,
        points: list[tuple],
        other: dict[str, Any],
        wall_clock: str | None,
        strict: bool | None,
        *,
        stacklevel: int,
    ):
        """Write one step's row: every numeric point in ONE metrics POST, the
        rest as the step record. ``points`` are ``(key, value, dimensions,
        labels, span_id, agg)``; ``stacklevel`` makes a warning name the
        caller's ``log()`` line, however deep this was reached from. Warnings
        go through ``_diagnostics.warn``: this also runs inside ``finish()``,
        where a warning raised by ``-W error`` would read as a lost row."""
        if os.getpid() != self._opened_pid:
            self._note_forked_writer()
        if kind != "hardware":
            self._progress.bump()  # 2.8: one user row is one unit of progress
        result = None
        # What the server cannot store, dropped here with a warning rather than
        # queued: it answered a step past int64 or a key past its index row
        # size with a 500, which the outbox retries for 24 h and which held
        # the run's later writes behind it (review of #2053).
        if step is not None and not (_STEP_MIN <= step <= _STEP_MAX):
            if not getattr(self, "_step_range_warned", False):
                self._step_range_warned = True
                _diagnostics.warn(
                    f"probe: dropped the metrics of step {step}: a step must fit in a "
                    "64-bit signed integer. Later steps out of range are dropped "
                    "silently.",
                    stacklevel=stacklevel,
                )
            return None
        kept = [point for point in points if not _key_too_long(point[0])]
        if len(kept) != len(points):
            warned = self.__dict__.setdefault("_long_keys_warned", set())
            for point in points:
                key = point[0]
                if _key_too_long(key) and key not in warned:
                    warned.add(key)
                    _diagnostics.warn(
                        f"probe: dropped metric {key[:60]!r}...: a key may be at most "
                        f"{MAX_METRIC_KEY_BYTES} bytes ({len(key.encode('utf-8', 'surrogatepass'))} given).",
                        stacklevel=stacklevel,
                    )
            points = kept
            if not points and not other:
                return None
        if points:
            body = _metric_batch_body(
                [
                    MetricPointIn(
                        key=key,
                        kind=kind,
                        value=value,
                        step_index=step,
                        wall_clock=wall_clock,
                        dimensions=dims,
                        labels=labs or None,
                        span_id=span_id,
                        agg=agg,
                    )
                    for key, value, dims, labs, span_id, agg in points
                ]
            )
            # Returned even when a step record is also written: callers key off
            # this to tell "confirmed" from "spooled" (connectors/harbor.py).
            result = self._client.write(
                "POST", path_for(WriteOp.METRICS, self.id), self._stamp_writer(body), strict=strict
            )

        if other:
            if step is None:
                _diagnostics.warn(
                    f"dropped non-numeric {sorted(other)} — a step record needs a step "
                    "index, and step=None was passed explicitly to mean no step axis. "
                    "Omit step= to auto-increment, or pass one.",
                    stacklevel=stacklevel,
                )
            elif kind != "model":
                # StepCreate has no `kind` — a step record is keyed on
                # (run, step_index) alone. So a hardware value at hardware-step 3
                # would merge into the model loop's record at step 3. Numeric
                # hardware metrics are unaffected: those are metric points, where
                # kind IS part of the series identity.
                _diagnostics.warn(
                    f"dropped non-numeric {sorted(other)} from a {kind!r} log — step "
                    "records are keyed by step index alone, with no kind, so these "
                    "would overwrite the model loop's record at the same step.",
                    stacklevel=stacklevel,
                )
            else:
                name, attributes = self._union_step_record(step, other)
                step_result = self.step(step, name=name, attributes=attributes, strict=strict)
                # Only stand in when there was NOTHING numeric to write. A
                # successful step record must never mask a metrics write that
                # spooled: harbor.py reads None as "spooled".
                if not points:
                    result = step_result
        return result

    def _union_step_record(
        self, step: int, other: dict[str, Any]
    ) -> tuple[str | None, dict[str, Any]]:
        """``(name, other plus the attributes)`` this handle already sent to
        ``step``'s record, by :meth:`log` or :meth:`step`.

        The server REPLACES a step record's name and attributes on upsert
        (``app/telemetry/spans_router.py``), so ``log({"phase": "eval"},
        step=3)`` then ``log({"note": "x"}, step=3)`` used to leave only
        ``note``, and a ``step(3, name="warmup")`` lost its name to the next
        ``log(..., step=3)``. :meth:`step` remembers what it sent for the last
        ``_STEP_ATTRIBUTES_REMEMBERED`` steps, so memory stays flat over a long
        run. A first write to a step sends ``other`` unchanged. Never waits
        long on the lock (a signal handler may hold it): without it, no union."""
        if not self._pending_lock.acquire(timeout=_CLOSE_LOCK_WAIT_SECONDS):
            return None, other
        try:
            name, sent = self._step_records_sent.get(step, (None, {}))
        finally:
            self._pending_lock.release()
        return name, {**sent, **other}

    def _remember_step_record(self, step: int, name: str | None, attributes: Any) -> None:
        if not isinstance(attributes, dict):
            attributes = {}
        if not self._pending_lock.acquire(timeout=_CLOSE_LOCK_WAIT_SECONDS):
            return
        try:
            sent = self._step_records_sent
            sent.pop(step, None)
            sent[step] = (name, dict(attributes))
            if len(sent) > _STEP_ATTRIBUTES_REMEMBERED:
                del sent[next(iter(sent))]
        finally:
            self._pending_lock.release()

    def _peek_step(self, kind: str) -> int:
        """The step the next omitted-step call would draw, without drawing it."""
        with self._steps_lock:
            floor = 0 if kind == "hardware" else self._auto_step_floor
            return self._steps.get(kind, floor)

    def _claim_step(self, kind: str, step: int | None) -> None:
        """Move the counter past a pending row's step as it is written, and
        tell plan 2.4's resume guard, exactly as the ordinary path in
        :meth:`log` does."""
        if step is not None:
            self._note_step(kind, step)
            if self._resume_drops and kind != "hardware":
                self._note_resumed(step)

    def _flatten_metrics(self, metrics: Mapping[Any, Any]) -> dict[str, Any]:
        """``_flatten`` plus its warnings, each once per key per run: a loop logs
        the same structure every step, and a warning per step is noise.
        ``_diagnostics.warn`` because a plain warning raises under ``-W error``."""
        flat, collided, kept_whole = _flatten(metrics, known=self._nested_keys)
        for key, _top in collided:
            self._warn_flatten_once(
                ("collided", str(key)),
                f"probe.log: {key!r} was given twice, as an explicit key and through "
                "a nested dict; kept the explicit (least nested) one. Warned once per "
                "key per run.",
            )
        for key, reason, top in kept_whole:
            # Once per reason per TOP-LEVEL key: a dict keyed by data would
            # otherwise warn once per id.
            self._warn_flatten_once(
                (reason, top),
                f"probe.log: {key!r} was not flattened ({_KEPT_WHOLE_REASONS[reason]}); "
                f"recorded whole in the step record. Warned once per reason under {top!r} "
                "per run.",
            )
        return flat

    def _warn_flatten_once(self, token: tuple[str, str], message: str) -> None:
        """One warning per ``token`` per run, from a set bounded at
        ``_FLATTEN_WARNINGS_REMEMBERED``: past it, flattening goes quiet rather
        than growing without bound on a pathological structure."""
        warned = self._flatten_warned
        if token in warned or len(warned) >= _FLATTEN_WARNINGS_REMEMBERED:
            return
        warned.add(token)
        # 4 frames: warn <- here <- _flatten_metrics <- log <- the caller's line.
        _diagnostics.warn(message, stacklevel=4)

    def log_hw(
        self,
        metrics: dict[str, Any],
        *,
        step: int | None = _UNSET,
        wall_clock: str | None = None,
        strict: bool | None = None,
        **dims: Any,
    ):
        """Log hardware metrics with real dimensions (host/rank/device, fold #9).

        ``run.log_hw({"gpu_temp": 88}, device=3, host="n1")`` sends
        ``dimensions={"device": 3, "host": "n1"}``, kind=hardware."""
        return self.log(
            metrics,
            step=step,
            kind="hardware",
            wall_clock=wall_clock,
            dimensions=dims or None,
            strict=strict,
        )
from probe.sdk.run.metrics.derived import _metric_batch_body  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.run.metrics.pending import _CLOSE_LOCK_WAIT_SECONDS  # noqa: E402 -- pieces need each other; the front door loads this one first
