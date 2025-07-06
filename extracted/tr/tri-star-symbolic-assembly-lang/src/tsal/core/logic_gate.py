"""Dynamic logic gate with self-locking and plasticity."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import List

from tsal.utils.error_dignity import ERROR_DIR

@dataclass
class DynamicLogicGate:
    """A simple adaptive logic gate."""

    threshold_a: float = 0.5
    threshold_b: float = 0.5
    unlock_sequence: List[int] = field(default_factory=list)
    history: List[int] = field(default_factory=list)
    locked: bool = False

    def process(
        self, value: float, reward: float = 0.0, simulate: bool = False
    ) -> int:
        """Process a value, optionally updating thresholds if not in simulate mode."""
        try:
            polarity = 1 if value >= 0 else -1
            threshold = self.threshold_a if polarity > 0 else self.threshold_b
            result = 1 if abs(value) >= threshold else 0
            if not simulate and not self.locked:
                if polarity > 0:
                    self.threshold_a += reward * 0.1
                else:
                    self.threshold_b += reward * 0.1
            self._check_sequence(result)
            return result
        except Exception as e:  # pragma: no cover - unexpected failures
            ERROR_DIR.mkdir(exist_ok=True)
            with open(ERROR_DIR / "logic_gate.log", "a") as f:
                f.write(str(e) + "\n")
            # treat error as lateral learning by relaxing thresholds
            self.threshold_a *= 0.9
            self.threshold_b *= 0.9
            return 0

    def _check_sequence(self, value: int) -> None:
        self.history.append(value)
        if len(self.unlock_sequence) <= len(self.history):
            if (
                self.history[-len(self.unlock_sequence) :]
                == self.unlock_sequence
            ):
                self.locked = not self.locked
                self.history.clear()
