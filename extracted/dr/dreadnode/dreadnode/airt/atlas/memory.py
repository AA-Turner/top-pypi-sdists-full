"""ATLAS structural memory — cross-attack learning with the Hedge algorithm.

Tracks what works per ``(category, defense_level)`` and adjusts routing via
multiplicative-weights (Hedge) updates with exponential decay, plus a
quality-diversity archive of successful attack content keyed by failure type.
Ported faithfully from the ATLAS reference implementation.
"""

import math
import typing as t
from collections import defaultdict

from dreadnode.airt.atlas.failure import NearMissDecomposition


class StructuralMemory:
    """Cross-attack learning state with exponential decay and Hedge weights."""

    def __init__(self, decay_rate: float = 0.95, learning_rate: float = 0.3) -> None:
        self.decay_rate = decay_rate
        self.learning_rate = learning_rate  # Hedge learning rate

        self._mode_successes: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
        self._mode_attempts: dict[str, dict[str, float]] = defaultdict(lambda: defaultdict(float))
        self._hedge_weights: dict[str, dict[str, float]] = {}
        self._corrections: dict[str, str] = {}
        self._best_strategy: dict[str, str] = {}
        self._history: list[dict[str, t.Any]] = []
        # Quality-diversity archive: "category::failure_type" -> best attack template
        self._qd_archive: dict[str, dict[str, t.Any]] = {}

    def _key(self, category: str, defense_level: str) -> str:
        return f"{category}::{defense_level}"

    def record(
        self,
        category: str,
        defense_level: str,
        attack_mode: str,
        success: bool,
        score: float,
    ) -> None:
        """Record an attack outcome and update Hedge weights (w *= exp(-eta*loss))."""
        key = self._key(category, defense_level)

        # Decay historical counts (non-stationary adaptation)
        for mode in self._mode_successes[key]:
            self._mode_successes[key][mode] *= self.decay_rate
            self._mode_attempts[key][mode] *= self.decay_rate

        self._mode_attempts[key][attack_mode] += 1.0
        if success:
            self._mode_successes[key][attack_mode] += 1.0

        if key not in self._hedge_weights:
            self._hedge_weights[key] = {}
        if attack_mode not in self._hedge_weights[key]:
            self._hedge_weights[key][attack_mode] = 1.0

        loss = 1.0 - score
        self._hedge_weights[key][attack_mode] *= math.exp(-self.learning_rate * loss)

        cat_successes: dict[str, float] = defaultdict(float)
        cat_attempts: dict[str, float] = defaultdict(float)
        for k, modes in self._mode_successes.items():
            if k.startswith(f"{category}::"):
                for mode, count in modes.items():
                    cat_successes[mode] += count
                    cat_attempts[mode] += self._mode_attempts[k].get(mode, 0)

        if cat_successes:
            best = max(cat_successes, key=lambda m: cat_successes[m] / max(cat_attempts[m], 1))
            self._best_strategy[category] = best

        self._history.append(
            {
                "category": category,
                "defense_level": defense_level,
                "mode": attack_mode,
                "success": success,
                "score": score,
            }
        )

    def get_mode_override(self, category: str, defense_level: str) -> "str | None":
        """Hedge-optimal mode for a routing key, or None if insufficient evidence."""
        key = self._key(category, defense_level)
        weights = self._hedge_weights.get(key, {})
        if not weights or sum(self._mode_attempts[key].values()) < 3:
            return None
        return max(weights, key=lambda m: weights[m])

    def get_near_miss_correction(self, objective_id: str) -> "str | None":
        return self._corrections.get(objective_id)

    def register_near_miss(self, decomposition: NearMissDecomposition) -> None:
        self._corrections[decomposition.objective_id] = decomposition.suggested_correction

    def get_best_strategy(self, category: str) -> "str | None":
        return self._best_strategy.get(category)

    def get_hedge_distribution(self, category: str, defense_level: str) -> dict[str, float]:
        """Normalized Hedge weight distribution (probability simplex)."""
        key = self._key(category, defense_level)
        weights = self._hedge_weights.get(key, {})
        if not weights:
            return {}
        total = sum(weights.values())
        if total < 1e-10:
            return {m: 1.0 / len(weights) for m in weights}
        return {m: w / total for m, w in weights.items()}

    def archive_success(
        self,
        category: str,
        failure_type: str,
        goal_text: str,
        mode_name: str,
        surface: str,
        score: float,
    ) -> None:
        """Store a successful attack in the QD archive (keeps the highest-scoring per cell)."""
        key = f"{category}::{failure_type}"
        existing = self._qd_archive.get(key)
        if not existing or score > existing.get("score", 0):
            self._qd_archive[key] = {
                "goal": goal_text,
                "mode": mode_name,
                "surface": surface,
                "score": score,
            }

    def get_archive_template(self, category: str, failure_type: str) -> "dict[str, t.Any] | None":
        return self._qd_archive.get(f"{category}::{failure_type}")

    def to_dict(self) -> dict[str, t.Any]:
        return {
            "corrections": dict(self._corrections),
            "best_strategy_per_category": dict(self._best_strategy),
            "hedge_weights": {k: dict(v) for k, v in self._hedge_weights.items()},
            "total_records": len(self._history),
            "qd_archive_size": len(self._qd_archive),
            "qd_archive_cells": list(self._qd_archive.keys()),
        }
