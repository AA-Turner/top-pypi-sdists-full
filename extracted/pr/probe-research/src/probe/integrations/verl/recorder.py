"""What the verl hooks write to `run.samples` (RL plan §6.5): each training batch before it trains, its commit after
`update_actor`, critic-warmup batches, validation passes, weight versions, checkpoints, counted drops (stale, DAPO,
failed), and the seals capture reads. Pure: the trainer wraps (`trainers.py`) hand it rows. Why: DESIGN.md."""

from __future__ import annotations

import threading
from collections.abc import Mapping, Sequence
from datetime import datetime, timezone
from typing import Any

from .rows import RowMapper, VerlRow

#: A fully async rollout group the message queue refused for staleness (`fully_async_rollouter.py:1007-1014`).
STALE_DROP = "stale"


class VerlRecorder:
    """One verl process's samples. ``samples`` is `run.samples` as this producer; ``floor`` is the first step this
    write epoch owns (R after a resume): no empty seal below it. ``is_eval_only``: the fully async rollouter, which
    only validates: it seals just the steps it wrote at and never speaks for the run's last step."""

    def __init__(self, samples: Any, *, floor: int = 0, is_eval_only: bool = False) -> None:
        self._samples = samples
        self._floor = floor
        self._is_eval_only = is_eval_only
        self._lock = threading.RLock()
        self.mapper: RowMapper | None = None
        self._consumed_at: dict[int, datetime] = {}
        self._sealed: set[int] = set()
        #: Steps whose record failed: never sealed, so capture answers "no" for them.
        self._failed: set[int] = set()
        self._drops: dict[int, dict[str, int]] = {}
        self._stale_seen: int | None = None
        self._has_plan_steps = False
        #: Training batches the samples door took (not merely read): the end-to-end proof the hooks run.
        self.accepted_batches = 0

    def set_mapper(self, mapper: RowMapper) -> None:
        with self._lock:
            if self.mapper is None:
                self.mapper = mapper

    def plan_steps(self, total_steps: int | None) -> None:
        """The run's step count, once (verl knows it only after building its dataloader)."""
        with self._lock:
            if self._has_plan_steps or not isinstance(total_steps, int) or total_steps <= 0:
                return
            self._has_plan_steps = True
        self._samples.plan(expected_steps=total_steps)

    def mark_failed(self, step: int) -> None:
        """A record for ``step`` failed before it was sent: the step is never sealed (capture answers "no"), and no
        later step's seal stands in for it."""
        with self._lock:
            self._failed.add(step)

    # -- training ----------------------------------------------------------------------------------------
    def record_train(self, step: int, rows: Sequence[VerlRow]) -> list[str]:
        """Rows ``step`` is about to train on, before it trains: consumed by ``step`` (RL plan §3.3). Returns each
        row's sample key, in order (the per-sample metrics name their rows with them)."""
        with self._lock:
            self._consumed_at.setdefault(step, datetime.now(timezone.utc))
            try:
                parts = self._get_mapper().map_train(rows, step)
                taken = self._samples.log(parts, step=step)
            except Exception:
                self._failed.add(step)
                raise
            if taken:
                self.accepted_batches += 1
        return [part["key"] for part in parts if part.get("role") == "trainer"]

    def commit(self, step: int, *, is_pushing_weights: bool = True) -> None:
        """`update_actor` succeeded: the step's consumed samples read `trained`, the weights it made go live (verl
        pushes version ``step`` right after, `ray_trainer.py:1715`), and the step is sealed."""
        with self._lock:
            self._samples.commit(step, consumed_at=self._consumed_at.get(step))
            if is_pushing_weights:
                self._samples.weights(step, after_step=step)
            self._send_seals_through(step)

    def record_dropped(self, step: int, rows: Sequence[VerlRow], reason: str) -> None:
        """Rows ``step`` generated and did not train the actor on (critic warmup): stored as drops, then the step is
        sealed (no commit: the actor did not change)."""
        with self._lock:
            try:
                parts = self._get_mapper().map_dropped(rows, step, reason)
                self._samples.log(parts, step=step)
            except Exception:
                self._failed.add(step)
                raise
            self._send_seals_through(step)

    def add_stale_drops(self, step: int, total_dropped: Any) -> None:
        """The rollouter's running count of groups it dropped as stale (`fully_async/count/dropped_stale_samples`):
        what is new since the last batch counts toward ``step``'s seal. A smaller count is a restarted rollouter."""
        if isinstance(total_dropped, bool) or not isinstance(total_dropped, (int, float)):
            return
        total = int(total_dropped)
        with self._lock:
            seen = self._stale_seen
            self._stale_seen = total
            new = total if seen is None or total < seen else total - seen
        self.add_drops(step, STALE_DROP, new)

    def add_drops(self, step: int, reason: str, count: Any) -> None:
        """``count`` groups verl threw away for ``reason`` before they could train (a `DropReason`): counted in
        ``step``'s seal, never stored (a group is stored or counted, never both). A step already sealed is sealed
        again with them (the SDK adds them to its totals)."""
        if isinstance(count, bool) or not isinstance(count, (int, float)) or int(count) <= 0:
            return
        with self._lock:
            drops = self._drops.setdefault(step, {})
            drops[reason] = drops.get(reason, 0) + int(count)
            if step in self._sealed and step not in self._failed:
                self._samples.seal(step, dropped=self._drops.pop(step))

    # -- validation and checkpoints ----------------------------------------------------------------------
    def record_eval(self, step: int, rows: Sequence[VerlRow]) -> None:
        """A validation pass at ``step`` (0 before training): eval samples, then the step re-sealed with them."""
        with self._lock:
            try:
                parts = self._get_mapper().map_eval(rows, step)
                self._samples.log(parts, step=step)
            except Exception:
                self._failed.add(step)
                raise
            self._send_seals_through(step)

    def record_checkpoint(self, step: int, ref: Mapping[str, Any]) -> None:
        """A checkpoint saved after ``step``: weight version ``step`` gains it (the server fills it in)."""
        with self._lock:
            self._samples.weights(step, after_step=step, checkpoint=dict(ref))

    # -- the end -----------------------------------------------------------------------------------------
    def close(self) -> int | None:
        """Journal what is still held; returns the last sealed step, the terminal manifest's `final_step`."""
        with self._lock:
            pending = sorted(set(self._drops) - self._failed)
            if pending:
                self._send_seals_through(pending[-1])
            self._samples.close()
            return max(self._sealed) if self._sealed else None

    # -- inside ------------------------------------------------------------------------------------------
    def _get_mapper(self) -> RowMapper:
        if self.mapper is None:
            self.mapper = RowMapper()
        return self.mapper

    def _send_seals_through(self, step: int) -> None:
        """Seal ``step`` (again, when an eval pass lands on a sealed step: the SDK declares totals so far) and
        every earlier step from the floor nothing was recorded at, so capture's 0..N finds a seal. A step whose
        record failed is never sealed. The run's last step so far goes in the plan: a killed actor never
        reaches its finish. The rollouter seals only ``step``: it is not a producer of the training steps."""
        if self._is_eval_only:
            if step not in self._failed:
                self._samples.seal(step, dropped=self._drops.pop(step, None))
                self._sealed.add(step)
            return
        for current in range(min(self._floor, step), step + 1):
            if current in self._failed:
                continue
            if current != step and (current < self._floor or current in self._sealed):
                continue
            self._samples.seal(current, dropped=self._drops.pop(current, None))
            self._sealed.add(current)
        if self._sealed:
            self._samples.plan(final_step=max(self._sealed))
