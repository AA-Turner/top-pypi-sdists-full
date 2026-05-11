"""Item #23 — Live "what-am-I-doing" overlay."""

from __future__ import annotations

import time
from collections import Counter
from dataclasses import dataclass, field

__all__ = ["OverlayState"]


@dataclass
class OverlayState:
    file_modifications: Counter = field(default_factory=Counter)
    test_passes: int = 0
    test_total: int = 0
    recent_signals: Counter = field(default_factory=Counter)
    started_ts: float = field(default_factory=time.time)

    def note_file_modification(self, path: str) -> None:
        self.file_modifications[path] += 1

    def note_test_result(self, *, passed: bool, total: int = 1) -> None:
        if passed:
            self.test_passes += total
        self.test_total += total

    def note_validator_signal(self, signal: str) -> None:
        self.recent_signals[signal] += 1

    def snapshot(self) -> dict:
        return {
            "uptime_s": time.time() - self.started_ts,
            "most_modified": self.file_modifications.most_common(3),
            "test_pass_rate": (self.test_passes / self.test_total
                               if self.test_total else 0.0),
            "recent_signals": dict(self.recent_signals),
        }
