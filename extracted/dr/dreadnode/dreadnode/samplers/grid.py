"""Grid search sampler - exhaustive search over all parameter combinations."""

import itertools
import random
import typing as t

from loguru import logger

from dreadnode.optimization.sampler import Sample, Sampler
from dreadnode.optimization.trial import Trial


class GridSampler(Sampler[dict[str, t.Any]]):
    """
    Exhaustive grid search over all parameter combinations.

    Evaluates every combination of parameter values exactly once.

    Example:
        sampler = GridSampler({
            "model": ["gpt-4", "claude-3"],
            "temperature": [0.3, 0.7, 1.0],
        })
        # Yields 2 * 3 = 6 candidates

    Args:
        grid: Dictionary mapping parameter names to lists of values.
        shuffle: If True, randomize the order of combinations.
        seed: Random seed for shuffling (only used if shuffle=True).
    """

    def __init__(
        self,
        grid: dict[str, list[t.Any]],
        *,
        shuffle: bool = False,
        seed: int | None = None,
    ):
        if not grid:
            raise ValueError("Grid search space cannot be empty")

        self.grid = grid
        self.keys = list(grid.keys())

        # Generate all combinations
        value_lists = [grid[k] for k in self.keys]
        self.combinations = list(itertools.product(*value_lists))

        if shuffle:
            rng = random.Random(seed)
            rng.shuffle(self.combinations)

        self.index = 0

        logger.info(
            f"GridSampler initialized: "
            f"parameters={self.keys}, "
            f"total_combinations={len(self.combinations)}, "
            f"shuffle={shuffle}"
        )

    def sample(self, history: list[Trial[dict]]) -> list[Sample[dict]]:  # noqa: ARG002
        """Return the next grid combination."""
        if self.exhausted:
            return []

        values = self.combinations[self.index]
        candidate = dict(zip(self.keys, values, strict=False))
        self.index += 1

        logger.debug(f"GridSampler [{self.index}/{len(self.combinations)}]: {candidate}")

        return [Sample(candidate)]

    @property
    def exhausted(self) -> bool:
        """True when all combinations have been sampled."""
        return self.index >= len(self.combinations)

    def reset(self) -> None:
        """Reset to start from the beginning."""
        self.index = 0
