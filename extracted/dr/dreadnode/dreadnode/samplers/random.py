"""Random samplers - random parameter sampling and random image generation."""

import random
import typing as t

import numpy as np

from dreadnode.core.types import Image
from dreadnode.optimization.sampler import Sample, Sampler
from dreadnode.optimization.search import (
    Categorical,
    Float,
    Int,
    SearchSpace,
)
from dreadnode.optimization.trial import Trial


class RandomSampler(Sampler[dict[str, t.Any]]):
    """
    Random sampling from a search space.

    Continuously samples random parameter combinations until stopped.
    Supports Float, Int, and Categorical distributions.

    Example:
        sampler = RandomSampler({
            "temperature": Float(0.0, 2.0),
            "max_tokens": Int(100, 1000),
            "model": ["gpt-4", "claude-3"],  # shorthand for Categorical
        })

    Args:
        search_space: Dictionary mapping parameter names to distributions.
        seed: Random seed for reproducibility.
    """

    def __init__(
        self,
        search_space: SearchSpace,
        *,
        seed: int | None = None,
    ):
        if not search_space:
            raise ValueError("Search space cannot be empty")

        self.search_space = search_space
        self.rng = random.Random(seed)

    def sample(self, history: list[Trial[dict]]) -> list[Sample[dict]]:  # noqa: ARG002
        """Return a random sample from the search space."""
        candidate: dict[str, t.Any] = {}

        for name, dist in self.search_space.items():
            if isinstance(dist, Float):
                if dist.log:
                    import math

                    log_low = math.log(dist.low)
                    log_high = math.log(dist.high)
                    value = math.exp(self.rng.uniform(log_low, log_high))
                else:
                    value = self.rng.uniform(dist.low, dist.high)

                if dist.step is not None:
                    steps = int((value - dist.low) / dist.step)
                    value = dist.low + steps * dist.step

                candidate[name] = value

            elif isinstance(dist, Int):
                if dist.log:
                    import math

                    log_low = math.log(dist.low)
                    log_high = math.log(dist.high)
                    value = int(math.exp(self.rng.uniform(log_low, log_high)))
                else:
                    value = self.rng.randint(dist.low, dist.high)

                if dist.step != 1:
                    steps = (value - dist.low) // dist.step
                    value = dist.low + steps * dist.step

                candidate[name] = value

            elif isinstance(dist, Categorical):
                candidate[name] = self.rng.choice(dist.choices)

            elif isinstance(dist, list):
                # Shorthand: list of values treated as categorical
                candidate[name] = self.rng.choice(dist)

            else:
                raise TypeError(f"Unsupported distribution type: {type(dist)}")

        return [Sample(candidate)]

    @property
    def exhausted(self) -> bool:
        """Random sampler never exhausts - always returns False."""
        return False

    def reset(self) -> None:
        """No-op for random sampler."""


class RandomImageSampler(Sampler[Image]):
    """
    Generate random noise images.

    Continuously generates random images with pixel values in [0, 1].
    Useful for bootstrapping adversarial attacks or exploring image space.

    Example:
        sampler = RandomImageSampler(shape=(224, 224, 3))

    Args:
        shape: Shape of images to generate (height, width, channels).
        seed: Random seed for reproducibility.
    """

    def __init__(
        self,
        shape: tuple[int, ...],
        *,
        seed: int | None = None,
    ):
        if not shape:
            raise ValueError("Shape cannot be empty")

        self.shape = shape
        self.seed = seed
        self._rng = np.random.default_rng(seed)

    def sample(self, history: list[Trial[Image]]) -> list[Sample[Image]]:  # noqa: ARG002
        """Return a random noise image."""
        noise = self._rng.random(self.shape).astype(np.float32)
        return [Sample(Image(noise))]

    @property
    def exhausted(self) -> bool:
        """Random image sampler never exhausts - always returns False."""
        return False

    def reset(self) -> None:
        """Reset the random number generator."""
        self._rng = np.random.default_rng(self.seed)
