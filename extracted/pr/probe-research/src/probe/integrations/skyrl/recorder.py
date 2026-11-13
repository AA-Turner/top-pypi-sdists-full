"""What the SkyRL hooks write to `run.samples` (RL plan §6.3): every generation's rows, which rows a step trained on
or dropped, commits, weight versions and the seals that keep capture whole. Pure: the hooks (`hooks.py`)
call it with SkyRL's objects. Line refs are `NovaSky-AI/SkyRL@d87004689e3a`. Why: DESIGN.md."""

from __future__ import annotations

import itertools
import threading
from collections.abc import Iterable, Mapping, Sequence
from datetime import datetime, timezone
from typing import Any

from .outputs import CallVersions, OutputMapper, get_trajectories

#: A row whose loss mask is all zero did not train: zero variance when SkyRL's filter is on
#: (`trainer.py:1186-1201`), else another filter's mask.
MASKED_DROP = "filter:loss_mask"


def _make_locked(method):
    """Run ``method`` under the recorder's lock."""

    def call_locked(self, *args, **kwargs):
        with self._lock:
            return method(self, *args, **kwargs)

    call_locked.__name__ = method.__name__
    call_locked.__doc__ = method.__doc__
    return call_locked


class SkyrlRecorder:
    """One SkyRL training process's samples. ``samples`` is `run.samples` as this producer; ``mapper`` maps a
    generate call; ``is_zero_variance_filter`` says what an all-zero loss mask means."""

    def __init__(
        self, samples: Any, mapper: OutputMapper, *, is_zero_variance_filter: bool = False, floor: int = 0
    ) -> None:
        self._samples = samples
        self._mapper = mapper
        self._is_zero_variance_filter = is_zero_variance_filter
        self._calls = itertools.count()
        #: The fully async trainer converts a batch in a worker thread while generations land on the loop.
        self._lock = threading.RLock()
        #: id(train response_ids row) -> (the row, its key): the row object rides from generate to training.
        self._rows: dict[int, tuple[Any, str]] = {}
        #: Steps parts were stamped with, and not sealed since.
        self._stamped: set[int] = set()
        #: Train keys generated since the last consumption, by TrajectoryID (a merged step-wise row is new).
        self._pending: dict[tuple[str, int], list[str]] = {}
        #: A pending train key's TrajectoryID (a Harbor trial's key does not spell it).
        self._trajectory_of: dict[str, tuple[str, int]] = {}
        #: The step whose seal is next: every part sent before `seal(N)` is stamped <= N.
        self.cursor = 0
        self._sealed: set[int] = set()
        #: The first step this write epoch owns (R after a resume): no empty seal below it.
        self._floor = floor
        self._consumed_at: dict[int, datetime] = {}
        self._drops: dict[int, dict[str, int]] = {}
        #: (global_step, weight-sync count) at train start: a count maps to a policy version.
        self._version_base: tuple[int, int] | None = None

    @property
    def samples(self) -> Any:
        """`run.samples` as this producer."""
        return self._samples

    # -- versions ----------------------------------------------------------------------------------------
    @_make_locked
    def start(self, global_step: int, weight_version: int | None) -> None:
        """At `on_train_start`, after SkyRL's first weight sync (`trainer.py:318-329`): the version the
        engines serve is `global_step` (updates applied), and later syncs count up from there."""
        self.cursor = max(self.cursor, global_step)
        if isinstance(weight_version, int):
            self._version_base = (global_step, weight_version)

    def get_version(self, weight_version: int | None, *, fallback: int | None) -> int | None:
        """The policy version for an engine weight-sync count (`remote_inference_client.py:551-560`)."""
        if self._version_base is not None and isinstance(weight_version, int):
            step, count = self._version_base
            return step + (weight_version - count)
        return fallback

    # -- generation --------------------------------------------------------------------------------------
    def take_call(self) -> int:
        """The next generate call's ordinal (taken as the call starts: its live samples are keyed by it)."""
        return next(self._calls)

    @_make_locked
    def record_generation(self, inputs: Mapping[str, Any], output: Mapping[str, Any], versions: CallVersions,
                          harbor: Mapping[int, Any] | None = None, scheduled_step: int | None = None,
                          call_id: int | None = None) -> list[dict]:
        """One `generate()` call: its rows as generator parts, stamped with the step whose seal is next, returned.
        ``harbor``: the Harbor trials that ran its trajectories (`harbor.HarborJoin.take`); ``scheduled_step``:
        the step the call was scheduled at, when the trainer knows it better than the call's metadata; ``call_id``:
        the ordinal `take_call` gave the call (else the next one)."""
        call_id = self.take_call() if call_id is None else call_id
        parts = self._mapper.map_call(inputs, output, call_id=call_id, versions=versions, harbor=harbor,
                                      scheduled_step=scheduled_step)
        for row, part, trajectory in zip(output.get("response_ids") or [], parts, get_trajectories(inputs, output)):
            if part.get("split") == "train":
                self._rows[id(row)] = (row, part["key"])
                self._trajectory_of[part["key"]] = trajectory
                self._pending.setdefault(trajectory, []).append(part["key"])
        self._send(parts)
        return parts

    @_make_locked
    def record_parts(self, parts: Iterable[Mapping[str, Any]], step: int | None = None) -> int:
        """Parts the other side of an attempt wrote (a Harbor trial's `harbor` parts), stamped like the rows.
        ``step`` is ignored: they count toward the step whose seal is next. Shaped as `run.samples.log`."""
        found = [dict(part) for part in parts]
        self._send(found)
        return len(found)

    log = record_parts

    # -- training ----------------------------------------------------------------------------------------
    @_make_locked
    def record_batch(self, step: int, output: Mapping[str, Any], *, dropped: Iterable[Mapping[str, Any]] = (),
                     should_drop_leftovers: bool = False) -> list[list[str]]:
        """Rows a step is about to train on, before it trains: consumed by ``step`` at version ``step - 1``
        (the updates applied before it), or dropped when their loss mask is all zero. ``dropped`` outputs
        are groups the trainer threw away (zero variance, `fully_async_trainer.py:832-850`). With
        ``should_drop_leftovers`` (the synchronous trainer), train rows generated this step and missing from
        the batch were filtered out (dynamic sampling). Returns each training row's sample keys, in order."""
        self._consumed_at[step] = datetime.now(timezone.utc)
        parts: list[dict] = []
        row_keys: list[list[str]] = []
        masks = output.get("loss_masks") or []
        for row_index, row in enumerate(output.get("response_ids") or []):
            mask = masks[row_index] if row_index < len(masks) else None
            keys = self._take_keys(row, output, row_index)
            row_keys.append(keys)
            drop = None if mask is None or any(mask) else ("zero_variance" if self._is_zero_variance_filter else MASKED_DROP)
            parts.extend(self._make_trainer_part(key, step, drop) for key in keys)
        parts.extend(self._drop_groups(step, dropped, "zero_variance"))
        if should_drop_leftovers:
            for keys in self._pending.values():
                parts.extend(self._make_trainer_part(key, step, "filter:dynamic_sampling") for key in keys)
            self._pending.clear()
            self._trajectory_of.clear()
            self._rows.clear()  # every train row of the step is now consumed or dropped
        self._send(parts)
        return row_keys

    @_make_locked
    def record_discarded(self, step: int, groups: Iterable[Mapping[str, Any]], reason: str) -> None:
        """Groups collected and then thrown away untrained (a partial batch at epoch end, zero-variance
        groups dropped while collecting it)."""
        self._send(self._drop_groups(step, groups, reason))

    @_make_locked
    def commit(self, step: int) -> None:
        """`on_step_end`: the optimizer step succeeded; its consumed rows read `trained`. Its weights go live."""
        self._samples.commit(step, consumed_at=self._consumed_at.pop(step, None))
        self._samples.weights(step, after_step=step)

    @_make_locked
    def record_checkpoint(self, step: int, ref: Mapping[str, Any] | None) -> None:
        """`on_save`: the weight version ``step`` gains its checkpoint (the server fills it in)."""
        self._samples.weights(step, after_step=step, checkpoint=dict(ref) if ref else None)

    @_make_locked
    def record_phases(self, step: int, phases: list[dict]) -> None:
        """SkyRL's timed blocks of ``step`` as `phase` spans (`phases.py`)."""
        self._samples.record_phases(step, phases)

    @_make_locked
    def add_drop(self, step: int, reason: str, count: int) -> None:
        if count > 0:
            drops = self._drops.setdefault(step, {})
            drops[reason] = drops.get(reason, 0) + count

    # -- seals -------------------------------------------------------------------------------------------
    @_make_locked
    def send_seals(self, step: int) -> None:
        """`on_log` at ``step``, the end of a step (or of the eval before training): seal every step from the
        cursor to ``step`` that has parts or drops, and every step at or past the run's floor this producer
        had nothing at (an empty seal, so capture's 0..N finds one). The cursor moves past ``step``."""
        for current in range(min(self.cursor, step), step + 1):
            has_news = current in self._stamped or current in self._drops
            if not has_news and (current < self._floor or current in self._sealed):
                continue
            self._samples.seal(current, dropped=self._drops.pop(current, None))
            self._sealed.add(current)
            self._stamped.discard(current)
        self.cursor = max(self.cursor, step + 1)

    @_make_locked
    def close(self) -> int | None:
        """At the end: seal what was stamped after the last step's seal (a late generation, the final eval).
        Returns the last sealed step, the terminal manifest's `final_step`."""
        late = self._stamped | set(self._drops)
        if late:
            self.send_seals(max(late))
        return max(self._sealed) if self._sealed else None

    # -- inside ------------------------------------------------------------------------------------------
    def _take_keys(self, row: Any, output: Mapping[str, Any], row_index: int) -> list[str]:
        """The sample keys behind a training row: the generated row itself, else (a merged step-wise row)
        every pending segment of its TrajectoryID."""
        found = self._rows.pop(id(row), None)
        if found is not None and found[0] is row:
            key = found[1]
            trajectory = self._trajectory_of.pop(key, None)
            pending = self._pending.get(trajectory) if trajectory is not None else None
            if pending is not None and key in pending:
                pending.remove(key)
                if not pending:
                    del self._pending[trajectory]
            return [key]
        trajectory_ids: Sequence[Any] = output.get("trajectory_ids") or []
        trajectory = trajectory_ids[row_index] if row_index < len(trajectory_ids) else None
        instance = getattr(trajectory, "instance_id", None)
        if instance is None:
            return []
        keys = self._pending.pop((str(instance), int(getattr(trajectory, "repetition_id", 0) or 0)), [])
        for key in keys:
            self._trajectory_of.pop(key, None)
        return keys

    def _send(self, parts: list[dict]) -> None:
        if parts:
            self._samples.log(parts, step=self.cursor)
            self._stamped.add(self.cursor)

    def _drop_groups(self, step: int, groups: Iterable[Mapping[str, Any]], reason: str) -> list[dict]:
        """Trainer drop parts for each group's stored rows; a group nothing stored is a seal count (one per
        group, as SkyRL counts `async/num_groups_dropped`), never both."""
        parts: list[dict] = []
        for group in groups:
            keys = [
                key
                for row_index, row in enumerate(group.get("response_ids") or [])
                for key in self._take_keys(row, group, row_index)
            ]
            if keys:
                parts.extend(self._make_trainer_part(key, step, reason) for key in keys)
            else:
                self.add_drop(step, reason, 1)
        return parts

    @staticmethod
    def _make_trainer_part(key: str, step: int, drop: str | None) -> dict:
        part: dict[str, Any] = {"key": key, "role": "trainer"}
        if drop is None:
            part.update(consumed_step=step, consumed_version=max(step - 1, 0))
        else:
            part["drop_reason"] = drop
        return part

