"""Chunk buffer with temporal ensembling.

Ported from sandbox/sdk/python/dropbear/action_buffer.py (stale-chunk
rejection, stats, underrun semantics) and
sandbox/experiments/sagemaker-libero/src/sagemaker_libero/ensemble.py
(uniform-weight averaging across overlapping predictions). See the plan's
Task 7 header for the adaptation list.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from dreamscale.constants import MAX_PREDICTIONS, STALE_ACTION_S


@dataclass
class BufferStats:
    consumed_count: int = 0
    underrun_count: int = 0
    stale_chunk_count: int = 0
    accepted_chunk_count: int = 0


@dataclass(frozen=True)
class Prediction:
    chunk_id: int
    observation_id: int
    start_tick: int
    actions: tuple[tuple[float, ...], ...]
    received_ns: int


@dataclass
class EnsembleBuffer:
    max_predictions: int = MAX_PREDICTIONS
    _predictions: list[Prediction] = field(default_factory=list, init=False, repr=False)
    _latest_observation_id: int = field(default=-1, init=False, repr=False)
    _last_chunk_received_ns: int | None = field(default=None, init=False, repr=False)
    stats: BufferStats = field(default_factory=BufferStats, init=False)

    def add_chunk(self, *, chunk_id: int, observation_id: int,
                  actions: list[list[float]], current_tick: int, now_ns: int) -> bool:
        if observation_id < self._latest_observation_id:
            self.stats.stale_chunk_count += 1
            return False
        self._predictions.append(Prediction(
            chunk_id=chunk_id,
            observation_id=observation_id,
            start_tick=current_tick + 1,
            actions=tuple(tuple(action) for action in actions),
            received_ns=now_ns,
        ))
        self._predictions = self._predictions[-self.max_predictions:]
        self._latest_observation_id = observation_id
        self._last_chunk_received_ns = now_ns
        self.stats.accepted_chunk_count += 1
        return True

    def consume(self, tick: int, now_ns: int) -> list[float] | None:
        stale_ns = int(STALE_ACTION_S * 1e9)
        self._predictions = [
            p for p in self._predictions if now_ns - p.received_ns <= stale_ns
        ]
        covering = [
            p.actions[tick - p.start_tick]
            for p in self._predictions
            if 0 <= tick - p.start_tick < len(p.actions)
        ]
        if not covering:
            self.stats.underrun_count += 1
            return None
        self.stats.consumed_count += 1
        dims = len(covering[0])
        return [sum(action[d] for action in covering) / len(covering) for d in range(dims)]

    def actions_remaining(self, tick: int) -> int:
        remaining = 0
        for p in self._predictions:
            end_tick = p.start_tick + len(p.actions)
            remaining = max(remaining, end_tick - max(tick, p.start_tick))
        return max(0, remaining)

    def last_chunk_age_ns(self, now_ns: int) -> int | None:
        if self._last_chunk_received_ns is None:
            return None
        return now_ns - self._last_chunk_received_ns

    @property
    def has_chunks(self) -> bool:
        return self.stats.accepted_chunk_count > 0
