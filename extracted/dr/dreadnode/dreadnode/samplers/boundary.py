"""Boundary sampler - binary search between two points to find decision boundary."""

import typing as t

import numpy as np
from loguru import logger

from dreadnode.core.types import Image
from dreadnode.optimization.sampler import Sample, Sampler
from dreadnode.optimization.trial import Trial

CandidateT = t.TypeVar("CandidateT")


class BoundarySampler(Sampler[Image]):
    """
    Binary search sampler to find decision boundary between two images.

    Performs binary search along the line between a source image and a target
    image to find the decision boundary. Useful for understanding model
    sensitivity or finding minimal perturbations.

    The sampler iteratively narrows the search interval based on whether
    midpoint samples are adversarial (above threshold) or not.

    Example:
        sampler = BoundarySampler(
            source=clean_image,
            target=adversarial_image,
            objective="confidence",
            threshold=0.5,
        )

    Args:
        source: The starting point (typically non-adversarial).
        target: The ending point (typically adversarial).
        objective: Name of the score to use for boundary decisions.
        threshold: Score threshold for classifying as adversarial.
        tolerance: Stop when interval is smaller than this (default: 1e-4).
        max_iterations: Maximum number of binary search steps.
    """

    def __init__(
        self,
        source: Image,
        target: Image,
        *,
        objective: str | None = None,
        threshold: float = 0.0,
        tolerance: float = 1e-4,
        max_iterations: int = 50,
    ):
        self.source = source
        self.target = target
        self.objective = objective
        self.threshold = threshold
        self.tolerance = tolerance
        self.max_iterations = max_iterations

        self._source_array = source.to_numpy()
        self._target_array = target.to_numpy()

        # Binary search state
        self._low: float = 0.0  # Source end
        self._high: float = 1.0  # Target end
        self._iteration = 0
        self._exhausted = False
        self._boundary_found: Image | None = None

        logger.info(
            f"BoundarySampler initialized: "
            f"threshold={threshold}, tolerance={tolerance}, max_iterations={max_iterations}"
        )

    def _interpolate(self, alpha: float) -> np.ndarray:
        """Interpolate between source and target at alpha in [0, 1]."""
        return (1 - alpha) * self._source_array + alpha * self._target_array

    def sample(self, history: list[Trial[Image]]) -> list[Sample[Image]]:  # noqa: ARG002
        """Return the midpoint sample for binary search."""
        if self._exhausted:
            return []

        alpha = (self._low + self._high) / 2
        interpolated = np.clip(self._interpolate(alpha), 0, 1).astype(np.float32)
        return [Sample(Image(interpolated))]

    def tell(self, trials: list[Trial[Image]]) -> None:
        """Update binary search bounds based on trial result."""
        if not trials or self._exhausted:
            return

        for trial in trials:
            if trial.status != "finished":
                continue

            self._iteration += 1
            score = trial.get_directional_score(self.objective)
            is_adversarial = score > self.threshold

            # Update bounds based on adversarial classification
            if is_adversarial:
                # Midpoint is adversarial, search lower half
                self._high = (self._low + self._high) / 2
            else:
                # Midpoint is not adversarial, search upper half
                self._low = (self._low + self._high) / 2

            logger.debug(
                f"Boundary [{self._iteration}/{self.max_iterations}]: "
                f"score={score:.5f}, adversarial={is_adversarial}, "
                f"interval=[{self._low:.6f}, {self._high:.6f}]"
            )

            # Check convergence
            if self._high - self._low < self.tolerance:
                self._exhausted = True
                alpha = self._high  # Use adversarial side of boundary
                boundary = np.clip(self._interpolate(alpha), 0, 1).astype(np.float32)
                self._boundary_found = Image(boundary)
                logger.info(f"BoundarySampler converged after {self._iteration} iterations")

            if self._iteration >= self.max_iterations:
                self._exhausted = True
                logger.info(f"BoundarySampler reached max iterations ({self.max_iterations})")

    @property
    def exhausted(self) -> bool:
        """Return True when boundary search is complete."""
        return self._exhausted

    @property
    def boundary(self) -> Image | None:
        """Return the found boundary image, if available."""
        return self._boundary_found

    def reset(self) -> None:
        """Reset binary search state."""
        self._low = 0.0
        self._high = 1.0
        self._iteration = 0
        self._exhausted = False
        self._boundary_found = None
