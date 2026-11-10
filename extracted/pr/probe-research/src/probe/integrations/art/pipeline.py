"""A `PipelineTrainer`'s facts ART keeps out of its own log (RL plan §6.2): stale groups dropped as counts, the
zero-variance groups past the 50 it logs, its `checkpoint/*` rows and its queue depth. Line refs are
`OpenPipe/ART@414acc5` `src/art/pipeline_trainer/trainer.py`."""

from __future__ import annotations

import functools
import math
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .art import ArtTracker

#: `_log_zero_variance_groups` logs at most this many discarded groups per step and drops the rest (`:874`).
ZERO_VARIANCE_LOGGED_MAX = 50


class PipelineHooks:
    """Wraps one trainer's instance methods for ``tracker``. Every hook fails open."""

    def __init__(self, tracker: ArtTracker, trainer: Any) -> None:
        self._tracker = tracker
        self._trainer = trainer
        tracker.queue_depth = self.get_queue_depth
        collect = trainer._collect_batch
        log_zero_variance = trainer._log_zero_variance_groups
        log_history = trainer._log_checkpoint_history

        @functools.wraps(collect)
        async def collect_batch(current_step: int) -> Any:
            result = await collect(current_step)
            tracker.guard.call("stale groups", self._record_stale_drops, current_step, result)
            return result

        @functools.wraps(log_zero_variance)
        async def log_zero_variance_groups(step: int) -> Any:
            tracker.guard.call("zero-variance groups", self._record_zero_variance_overflow, step)
            return await log_zero_variance(step)

        @functools.wraps(log_history)
        def log_checkpoint_history(step: int, metrics: dict) -> Any:
            result = log_history(step, metrics)
            tracker.guard.call("checkpoint rows", self._send_checkpoint_rows, step, metrics)
            return result

        tracker.install(trainer, "_collect_batch", collect_batch)
        tracker.install(trainer, "_log_zero_variance_groups", log_zero_variance_groups)
        tracker.install(trainer, "_log_checkpoint_history", log_checkpoint_history)

    def get_queue_depth(self) -> int | None:
        """Finished groups waiting for the trainer (ART prints it, `status.py`; never logs it)."""
        queue = getattr(self._trainer, "_output_queue", None)
        return queue.qsize() if queue is not None else None

    def _record_stale_drops(self, current_step: int, result: Any) -> None:
        """Stale groups `_collect_batch` threw away (`:637`, `:656`) are drops of the step this batch trains,
        `current_step + 1` (`:514`). A collapse stops training with the zero-variance queue unlogged
        (`:641`, `:660`): those count too."""
        batch, discarded, _saw_sentinel = result
        consuming = current_step + 1
        self._tracker.add_drops(consuming, "stale", int(discarded or 0))
        trainer = self._trainer
        if not batch and getattr(trainer, "_collapse_triggered", False):
            self._tracker.add_drops(consuming, "zero_variance", len(getattr(trainer, "_discard_queue", ()) or ()))

    def _record_zero_variance_overflow(self, step: int) -> None:
        """The zero-variance groups past the 50 ART logs as `split="discarded"` samples are counts only, so
        a group is either stored or counted, never both (RL plan §3.4)."""
        overflow = len(getattr(self._trainer, "_discard_queue", ()) or ()) - ZERO_VARIANCE_LOGGED_MAX
        self._tracker.add_drops(step, "zero_variance", overflow)

    def _send_checkpoint_rows(self, step: int, metrics: dict) -> None:
        """The rows ART writes straight to `history.jsonl`, skipping `_log_metrics` (`:930-945`)."""
        row = {
            (key if key.startswith("checkpoint/") else f"checkpoint/{key}"): float(value)
            for key, value in metrics.items()
            if isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)
        }
        if row:
            self._tracker.log_metrics(row, step)
