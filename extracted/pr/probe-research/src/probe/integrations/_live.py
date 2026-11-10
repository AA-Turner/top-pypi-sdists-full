"""Live samples for ART, SkyRL, verl and TRL (rl-next W37): each rollout's start, progress and end through
`run.samples`, bounded and fail-open. None of them takes a live command (the W30 spike): their plan says why."""

from __future__ import annotations

import threading
from collections.abc import Iterable, Mapping
from typing import Any

from probe.generated.samples import AttemptOutcome
from probe.generated.samples.result import DEFAULT_REWARD_MAX

#: Open samples one adapter remembers; past it a new start is skipped and counted, so memory stays bounded.
MAX_OPEN = 100_000
#: The live sample commands (`CommandKind`'s sample kinds); none of the four adapters does one safely.
SAMPLE_COMMANDS = ("cancel", "retry", "watch")


def refuse_commands(samples: Any, why: str) -> None:
    """``samples``' producer takes no live command: each kind is refused at once in ``why``, the W30 spike's words
    (`run.samples.refuse`, the plan's `refusals`); it declares no capability. Never raises."""
    for kind in SAMPLE_COMMANDS:
        samples.refuse(kind, why)


def get_outcome(reward: Any, *, reward_max: float | None = None, is_error: bool = False) -> AttemptOutcome:
    """How a rollout ended: `error` when it broke; `passed` / `failed` by its reward against the full reward;
    `ungraded` when it ended unbroken with no reward yet (its sample's `result` says how well, once graded)."""
    if is_error:
        return AttemptOutcome.ERROR
    if isinstance(reward, bool) or not isinstance(reward, (int, float)) or reward != reward:
        return AttemptOutcome.UNGRADED
    full = DEFAULT_REWARD_MAX if reward_max is None else reward_max
    return AttemptOutcome.PASSED if reward >= full else AttemptOutcome.FAILED


class LiveAttempts:
    """One producer's running samples: which keys are open, their start, progress and end. Starts and ends of one
    batch go in one write (`attempt_start_many`). Never raises; ``failures`` and ``skipped`` count what was lost."""

    def __init__(self, samples: Any, *, reward_max: float | None = None) -> None:
        self.samples = samples
        self.reward_max = reward_max
        self.failures = 0
        self.skipped = 0
        self._open: dict[str, None] = {}
        self._lock = threading.Lock()

    def start(self, starts: Iterable[Mapping[str, Any]]) -> list[str]:
        """These samples began (each `key`, `task_key` and its `attempt_start` fields). Returns the keys started."""
        try:
            fresh: list[dict] = []
            with self._lock:
                for start in starts:
                    key = str(start["key"])
                    if key in self._open:
                        continue
                    if len(self._open) >= MAX_OPEN:
                        self.skipped += 1
                        continue
                    self._open[key] = None
                    fresh.append(dict(start))
            if fresh:
                self.samples.attempt_start_many(fresh)
            return [start["key"] for start in fresh]
        except Exception:  # noqa: BLE001 -- fail open: a rollout Probe cannot start still trains
            self.failures += 1
            return []

    def send_progress(self, keys: Iterable[str], **snapshot: Any) -> None:
        """How these open samples are going (`phase`, `turns`, `tokens`, `activity`): a change is real progress."""
        try:
            with self._lock:
                found = [key for key in keys if key in self._open]
            for key in found:
                self.samples.attempt_progress(key, **snapshot)
        except Exception:  # noqa: BLE001 -- fail open
            self.failures += 1

    def end(self, ends: Iterable[Mapping[str, Any]]) -> list[str]:
        """These samples ended (each `key`, `outcome` and its `attempt_end` fields); a key not open is skipped.
        Returns the keys ended."""
        try:
            found: list[dict] = []
            with self._lock:
                for end in ends:
                    if self._open.pop(str(end["key"]), _GONE) is not _GONE:
                        found.append(dict(end))
            if found:
                self.samples.attempt_end_many(found)
            return [end["key"] for end in found]
        except Exception:  # noqa: BLE001 -- fail open: the sample then reads hung, then abandoned
            self.failures += 1
            return []

    def end_error(self, keys: Iterable[str], error: BaseException) -> list[str]:
        """These samples broke with ``error`` (the framework raised)."""
        message = f"{type(error).__name__}: {error}"[:1024]
        return self.end({"key": key, "outcome": AttemptOutcome.ERROR, "error_reason": "unknown",
                         "error_message": message} for key in keys)

    def is_open(self, key: str) -> bool:
        with self._lock:
            return key in self._open

    def get_outcome(self, reward: Any, *, is_error: bool = False) -> AttemptOutcome:
        return get_outcome(reward, reward_max=self.reward_max, is_error=is_error)


_GONE = object()
