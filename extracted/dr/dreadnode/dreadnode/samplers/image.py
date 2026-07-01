"""Adversarial attack samplers for image and tabular data.

All samplers accept either ``Image`` or raw ``np.ndarray`` inputs.
When an ``Image`` is provided, outputs are clipped to [0, 1] and wrapped
back in ``Image``.  Raw arrays are returned unclipped so tabular features
with arbitrary ranges work out of the box.
"""

import typing as t
from abc import abstractmethod
from enum import Enum, auto

import numpy as np
from loguru import logger

from dreadnode.core.types import Image
from dreadnode.optimization.sampler import Sample, Sampler
from dreadnode.optimization.trial import Trial
from dreadnode.scorers.image import Norm

#: Input type accepted by all adversarial samplers.
ArrayInput = Image | np.ndarray


def _to_array(x: ArrayInput) -> np.ndarray:
    """Extract a float32 numpy array from *x*."""
    if isinstance(x, Image):
        return x.to_numpy()
    return np.asarray(x, dtype=np.float32)


def _wrap(arr: np.ndarray, *, like_image: bool) -> ArrayInput:
    """Wrap *arr* back to the caller's input type."""
    if like_image:
        return Image(clip(arr, 0, 1))
    return arr


def clip(arr: np.ndarray, min_val: float, max_val: float) -> np.ndarray:
    """Clip array values to a range."""
    return np.clip(arr, min_val, max_val)


def get_random(shape: tuple, norm: Norm, seed: int | None = None) -> np.ndarray:
    """Generate random noise with specified norm.

    Args:
        shape: Shape of the output array.
        norm: Type of norm ('l2', 'l1', or 'linf').
        seed: Random seed for reproducibility.

    Returns:
        Random noise array normalized according to the specified norm.
    """
    rng = np.random.default_rng(seed)
    noise = rng.standard_normal(shape).astype(np.float32)

    if norm == "l2":
        # Normalize to unit L2 norm
        flat = noise.reshape(shape[0], -1) if len(shape) > 1 else noise.reshape(1, -1)
        norms = np.linalg.norm(flat, axis=1, keepdims=True)
        norms = np.maximum(norms, 1e-10)
        flat = flat / norms
        return flat.reshape(shape)
    if norm == "l1":
        # Normalize to unit L1 norm
        flat = noise.reshape(shape[0], -1) if len(shape) > 1 else noise.reshape(1, -1)
        norms = np.sum(np.abs(flat), axis=1, keepdims=True)
        norms = np.maximum(norms, 1e-10)
        flat = flat / norms
        return flat.reshape(shape)
    # linf - Normalize to [-1, 1] range
    return np.sign(noise)


class _Phase(Enum):
    """Internal phase tracking for multi-phase algorithms."""

    INIT = auto()
    PROBING = auto()
    UPDATING = auto()
    DONE = auto()


class _HSJPhase(Enum):
    """Internal phase tracking for HopSkipJump algorithm."""

    BOOTSTRAP = auto()  # Finding initial adversarial
    BOUNDARY_SEARCH = auto()  # Binary search to boundary
    GRADIENT_ESTIMATION = auto()  # Estimating gradient direction
    LINE_SEARCH = auto()  # Stepping along gradient
    PROJECTION = auto()  # Projecting back to boundary
    DONE = auto()


class ImageSampler(Sampler[t.Any]):
    """Base class for adversarial samplers (image and tabular)."""

    def __init__(
        self,
        original: ArrayInput,
        *,
        objective: str | None = None,
        max_iterations: int = 1000,
        seed: int | None = None,
    ):
        self.original = original
        self.objective = objective
        self.max_iterations = max_iterations
        self.seed = seed
        self._is_image = isinstance(original, Image)

        self._rng = np.random.default_rng(seed)
        self._iteration = 0
        self._best_score = -float("inf")
        self._best_candidate: ArrayInput | None = None
        self._phase = _Phase.INIT
        self._exhausted = False

    def _wrap(self, arr: np.ndarray) -> ArrayInput:
        """Wrap array back to caller's input type."""
        return _wrap(arr, like_image=self._is_image)

    @abstractmethod
    def _generate_samples(self) -> list[Sample[t.Any]]:
        """Generate next batch of samples. Override in subclasses."""
        ...

    @abstractmethod
    def _process_results(self, trials: list[Trial[t.Any]]) -> None:
        """Process trial results. Override in subclasses."""
        ...

    def sample(self, history: list[Trial[t.Any]]) -> list[Sample[t.Any]]:  # noqa: ARG002
        """Generate next batch of candidates."""
        if self._exhausted:
            return []
        return self._generate_samples()

    def tell(self, trials: list[Trial[t.Any]]) -> None:
        """Process completed trials."""
        if not trials:
            return
        self._process_results(trials)

    @property
    def exhausted(self) -> bool:
        return self._exhausted

    def reset(self) -> None:
        """Reset sampler state."""
        self._rng = np.random.default_rng(self.seed)
        self._iteration = 0
        self._best_score = -float("inf")
        self._best_candidate = None
        self._phase = _Phase.INIT
        self._exhausted = False


class SimBASampler(ImageSampler):
    """
    SimBA (Simple Black-box Attack) sampler.

    Iteratively perturbs the image using random noise masks and retains
    perturbations that improve the adversarial objective.

    See: SimBA - https://arxiv.org/abs/1805.12317
    """

    def __init__(
        self,
        original: ArrayInput,
        *,
        objective: str | None = None,
        theta: float = 0.1,
        num_masks: int = 500,
        norm: Norm = "l2",
        max_iterations: int = 10_000,
        seed: int | None = None,
    ):
        super().__init__(original, objective=objective, max_iterations=max_iterations, seed=seed)
        self.theta = theta
        self.num_masks = num_masks
        self.norm = norm

        self._original_array = _to_array(original)
        # Pre-generate mask collection
        mask_shape = (num_masks, *list(self._original_array.shape))
        self._mask_collection = get_random(mask_shape, norm, seed=seed) * theta
        self._current_mask = np.zeros_like(self._original_array)

        logger.info(
            f"SimBASampler initialized: theta={theta}, num_masks={num_masks}, "
            f"norm={norm}, max_iterations={max_iterations}"
        )

    def _generate_samples(self) -> list[Sample[t.Any]]:
        # First iteration - evaluate original
        if self._phase == _Phase.INIT:
            self._phase = _Phase.UPDATING
            return [Sample(self.original)]

        if self._iteration >= self.max_iterations:
            self._exhausted = True
            return []

        # Generate next perturbation
        mask_idx = self._rng.choice(self._mask_collection.shape[0])
        new_mask = self._mask_collection[mask_idx]

        masked_array = self._original_array + self._current_mask + new_mask
        self._pending_mask = new_mask

        return [Sample(self._wrap(masked_array))]

    def _process_results(self, trials: list[Trial[t.Any]]) -> None:
        for trial in trials:
            if trial.status != "finished":
                continue

            new_score = trial.get_directional_score(self.objective)

            # First trial sets baseline
            if self._phase == _Phase.UPDATING and self._best_candidate is None:
                self._best_score = new_score
                self._best_candidate = trial.candidate
                self._iteration = 1
                logger.info(f"SimBA baseline: score={new_score:.5f}")
                continue

            self._iteration += 1
            is_better = new_score > self._best_score

            logger.debug(
                f"SimBA [{self._iteration}/{self.max_iterations}]: "
                f"score={new_score:.5f}, best={self._best_score:.5f}, better={is_better}"
            )

            if is_better:
                self._best_score = new_score
                self._best_candidate = trial.candidate
                self._current_mask = self._current_mask + self._pending_mask

    def reset(self) -> None:
        super().reset()
        self._current_mask = np.zeros_like(_to_array(self.original))
        self._pending_mask = None


class NESSampler(ImageSampler):
    """
    Natural Evolution Strategies (NES) sampler.

    Estimates gradients by probing with random perturbations in positive
    and negative directions, then uses Adam optimizer for updates.

    See: NES - Natural Evolution Strategies
    """

    def __init__(
        self,
        original: ArrayInput,
        *,
        objective: str | None = None,
        max_iterations: int = 100,
        learning_rate: float = 0.01,
        num_samples: int = 64,
        sigma: float = 0.001,
        adam_beta1: float = 0.9,
        adam_beta2: float = 0.999,
        adam_epsilon: float = 1e-8,
        seed: int | None = None,
    ):
        super().__init__(original, objective=objective, max_iterations=max_iterations, seed=seed)
        self.learning_rate = learning_rate
        self.num_samples = num_samples
        self.sigma = sigma
        self.adam_beta1 = adam_beta1
        self.adam_beta2 = adam_beta2
        self.adam_epsilon = adam_epsilon

        self._original_array = _to_array(original)
        self._current_best_array = self._original_array.copy()
        self._adam_m = np.zeros_like(self._original_array, dtype=np.float32)
        self._adam_v = np.zeros_like(self._original_array, dtype=np.float32)

        # State for probe management
        self._perturbation_vectors: np.ndarray | None = None

        logger.info(
            f"NESSampler initialized: lr={learning_rate}, num_samples={num_samples}, "
            f"sigma={sigma}, max_iterations={max_iterations}"
        )

    def _generate_samples(self) -> list[Sample[t.Any]]:
        # First - evaluate original
        if self._phase == _Phase.INIT:
            self._phase = _Phase.UPDATING
            return [Sample(self.original)]

        if self._iteration >= self.max_iterations:
            self._exhausted = True
            return []

        # Generate probes for gradient estimation
        if self._phase == _Phase.UPDATING:
            self._perturbation_vectors = self._rng.standard_normal(
                (self.num_samples, *self._original_array.shape)
            )

            samples: list[Sample[t.Any]] = []
            for p_vec in self._perturbation_vectors:
                perturbed_p = self._current_best_array + self.sigma * p_vec
                samples.append(Sample(self._wrap(perturbed_p)))

                perturbed_n = self._current_best_array - self.sigma * p_vec
                samples.append(Sample(self._wrap(perturbed_n)))

            self._phase = _Phase.PROBING
            self._num_probes_expected = len(samples)
            return samples

        return []

    def _process_results(self, trials: list[Trial[t.Any]]) -> None:
        # Process initial trial
        if self._phase == _Phase.UPDATING and self._best_candidate is None:
            for trial in trials:
                if trial.status == "finished":
                    self._best_score = trial.get_directional_score(self.objective)
                    self._best_candidate = trial.candidate
                    logger.info(f"NES baseline: score={self._best_score:.5f}")
            return

        # Process probe results
        if self._phase == _Phase.PROBING:
            # Separate positive and negative probes (alternating in batch)
            finished = [t for t in trials if t.status == "finished"]
            probes_p = finished[::2]  # Even indices (positive perturbations)
            probes_n = finished[1::2]  # Odd indices (negative perturbations)

            if len(probes_p) != self.num_samples or len(probes_n) != self.num_samples:
                # Not all results received yet
                return

            scores_p = np.array([t.get_directional_score(self.objective) for t in probes_p])
            scores_n = np.array([t.get_directional_score(self.objective) for t in probes_n])
            score_diffs = scores_p - scores_n

            # Estimate gradient
            weights = score_diffs.reshape(self.num_samples, *([1] * self._original_array.ndim))
            estimated_gradient = np.mean(weights * self._perturbation_vectors, axis=0)

            # Adam update
            self._iteration += 1
            self._adam_m = (
                self.adam_beta1 * self._adam_m + (1 - self.adam_beta1) * estimated_gradient
            )
            self._adam_v = self.adam_beta2 * self._adam_v + (1 - self.adam_beta2) * (
                estimated_gradient**2
            )
            m_hat = self._adam_m / (1 - self.adam_beta1**self._iteration)
            v_hat = self._adam_v / (1 - self.adam_beta2**self._iteration)

            update_step = self.learning_rate * m_hat / (np.sqrt(v_hat) + self.adam_epsilon)
            new_array = self._current_best_array + update_step
            perturbation = new_array - self._original_array
            final_array = self._original_array + perturbation
            if self._is_image:
                final_array = clip(final_array, 0, 1)

            # Update best
            self._current_best_array = final_array
            self._phase = _Phase.UPDATING

            logger.info(
                f"NES [{self._iteration}/{self.max_iterations}]: "
                f"gradient_norm={np.linalg.norm(estimated_gradient):.5f}"
            )


class ZOOSampler(ImageSampler):
    """
    Zeroth-Order Optimization (ZOO) sampler.

    Uses coordinate-wise gradient estimation with Adam optimizer.

    See: ZOO - https://arxiv.org/abs/1708.03999
    """

    def __init__(
        self,
        original: ArrayInput,
        *,
        objective: str | None = None,
        max_iterations: int = 1000,
        learning_rate: float = 0.01,
        num_samples: int = 128,
        epsilon: float = 0.01,
        adam_beta1: float = 0.9,
        adam_beta2: float = 0.999,
        adam_epsilon: float = 1e-8,
        seed: int | None = None,
    ):
        super().__init__(original, objective=objective, max_iterations=max_iterations, seed=seed)
        self.learning_rate = learning_rate
        self.num_samples = num_samples
        self.epsilon = epsilon
        self.adam_beta1 = adam_beta1
        self.adam_beta2 = adam_beta2
        self.adam_epsilon = adam_epsilon

        self._original_array = _to_array(original)
        self._current_perturbation = np.zeros_like(self._original_array, dtype=np.float32)
        self._adam_m = np.zeros_like(self._current_perturbation)
        self._adam_v = np.zeros_like(self._current_perturbation)

        self._num_features = int(np.prod(self._original_array.shape))
        self._sample_indices: list[tuple[int, ...]] = []

        logger.info(
            f"ZOOSampler initialized: lr={learning_rate}, num_samples={num_samples}, "
            f"epsilon={epsilon}, max_iterations={max_iterations}"
        )

    def _generate_samples(self) -> list[Sample[t.Any]]:
        # First - evaluate original
        if self._phase == _Phase.INIT:
            self._phase = _Phase.UPDATING
            return [Sample(self.original)]

        if self._iteration >= self.max_iterations:
            self._exhausted = True
            return []

        # Generate coordinate probes
        if self._phase == _Phase.UPDATING:
            sample_indices_flat = self._rng.choice(
                self._num_features, min(self.num_samples, self._num_features), replace=False
            )
            self._sample_indices = [
                np.unravel_index(idx, self._original_array.shape) for idx in sample_indices_flat
            ]

            samples: list[Sample[t.Any]] = []
            for idx_nd in self._sample_indices:
                basis_vector = np.zeros(self._original_array.shape, dtype=np.float32)
                basis_vector[idx_nd] = 1.0

                perturbed_p = (
                    self._original_array + self._current_perturbation + self.epsilon * basis_vector
                )
                samples.append(Sample(self._wrap(perturbed_p)))

                perturbed_n = (
                    self._original_array + self._current_perturbation - self.epsilon * basis_vector
                )
                samples.append(Sample(self._wrap(perturbed_n)))

            self._phase = _Phase.PROBING
            return samples

        return []

    def _process_results(self, trials: list[Trial[t.Any]]) -> None:
        # Process initial trial
        if self._phase == _Phase.UPDATING and self._best_candidate is None:
            for trial in trials:
                if trial.status == "finished":
                    self._best_score = trial.get_directional_score(self.objective)
                    self._best_candidate = trial.candidate
                    logger.info(f"ZOO baseline: score={self._best_score:.5f}")
            return

        # Process probe results
        if self._phase == _Phase.PROBING:
            finished = [t for t in trials if t.status == "finished"]
            probes_p = finished[::2]  # Even indices (positive perturbations)
            probes_n = finished[1::2]  # Odd indices (negative perturbations)

            if len(probes_p) != len(self._sample_indices):
                return

            # Estimate gradient for sampled coordinates
            estimated_gradient = np.zeros_like(self._current_perturbation)
            for i, idx_nd in enumerate(self._sample_indices):
                score_p = probes_p[i].get_directional_score(self.objective)
                score_n = probes_n[i].get_directional_score(self.objective)
                estimated_gradient[idx_nd] = (score_p - score_n) / (2 * self.epsilon)

            # Adam update
            self._iteration += 1
            self._adam_m = (
                self.adam_beta1 * self._adam_m + (1 - self.adam_beta1) * estimated_gradient
            )
            self._adam_v = self.adam_beta2 * self._adam_v + (1 - self.adam_beta2) * (
                estimated_gradient**2
            )
            m_hat = self._adam_m / (1 - self.adam_beta1**self._iteration)
            v_hat = self._adam_v / (1 - self.adam_beta2**self._iteration)

            update_step = self.learning_rate * m_hat / (np.sqrt(v_hat) + self.adam_epsilon)
            self._current_perturbation += update_step

            self._phase = _Phase.UPDATING

            logger.info(
                f"ZOO [{self._iteration}/{self.max_iterations}]: "
                f"update_norm={np.linalg.norm(update_step):.5f}"
            )


class HopSkipJumpSampler(Sampler[t.Any]):
    """
    HopSkipJump attack sampler for black-box adversarial attacks.

    A decision-based attack that uses binary search to find the decision
    boundary and gradient estimation to minimize the perturbation distance.
    Works with both image (``Image``) and tabular (``np.ndarray``) inputs.

    See: HopSkipJumpAttack - https://arxiv.org/abs/1904.02144

    Args:
        source: The original, unperturbed input (Image or ndarray).
        adversarial: An optional initial adversarial example.
        objective: The name of the score to use for adversarial decisions.
        adversarial_threshold: Score threshold for adversarial classification.
        norm: Distance metric ('l2', 'l1', or 'linf').
        theta: Relative size of perturbation for gradient estimation.
        boundary_tolerance: Tolerance for binary search (default: theta/10).
        step_size: Initial step size ratio (default: theta).
        min_evaluations: Minimum probes per gradient estimation.
        max_evaluations: Maximum probes per gradient estimation.
        max_iterations: Maximum main iterations.
        seed: Random seed for reproducibility.
    """

    def __init__(
        self,
        source: ArrayInput,
        adversarial: ArrayInput | None = None,
        *,
        objective: str | None = None,
        adversarial_threshold: float = 0.0,
        norm: Norm = "l2",
        theta: float = 0.01,
        boundary_tolerance: float | None = None,
        step_size: float | None = None,
        min_evaluations: int = 50,
        max_evaluations: int = 100,
        max_iterations: int = 1_000,
        seed: int | None = None,
    ):
        self.source = source
        self.adversarial = adversarial
        self.objective = objective
        self.adversarial_threshold = adversarial_threshold
        self.norm = norm
        self.theta = theta
        self.boundary_tolerance = boundary_tolerance or theta / 10
        self.step_size = step_size or theta
        self.min_evaluations = min_evaluations
        self.max_evaluations = max_evaluations
        self.max_iterations = max_iterations
        self.seed = seed

        self._is_image = isinstance(source, Image)
        self._rng = np.random.default_rng(seed)
        self._source_array = _to_array(source)
        self._current_best: ArrayInput | None = adversarial
        self._current_best_array: np.ndarray | None = (
            _to_array(adversarial) if adversarial is not None else None
        )
        self._iteration = 0
        self._exhausted = False

        # Phase tracking
        self._phase = _HSJPhase.BOUNDARY_SEARCH if adversarial is not None else _HSJPhase.BOOTSTRAP

        # Sub-phase state
        self._bootstrap_attempts = 0
        self._bisection_low: float = 0.0
        self._bisection_high: float = 1.0
        self._bisection_target: np.ndarray | None = None
        self._gradient_probes: list[np.ndarray] = []
        self._gradient_noise: np.ndarray | None = None
        self._line_search_epsilon: float = 0.0
        self._line_search_attempts = 0

        logger.info(
            f"HopSkipJumpSampler initialized: theta={theta}, norm={norm}, "
            f"max_iterations={max_iterations}, input_type={'image' if self._is_image else 'array'}"
        )

    def _wrap_output(self, arr: np.ndarray) -> ArrayInput:
        """Wrap array back to caller's input type."""
        return _wrap(arr, like_image=self._is_image)

    def _is_adversarial(self, trial: "Trial[t.Any]") -> bool:
        """Check if trial is adversarial based on score threshold."""
        return trial.get_directional_score(self.objective) > self.adversarial_threshold

    def _compute_distance(self, arr: np.ndarray) -> float:
        """Compute distance from source."""
        diff = arr.flatten() - self._source_array.flatten()
        if self.norm == "l2":
            return float(np.linalg.norm(diff))
        if self.norm == "l1":
            return float(np.sum(np.abs(diff)))
        # linf
        return float(np.max(np.abs(diff)))

    def sample(self, history: "list[Trial[t.Any]]") -> "list[Sample[t.Any]]":  # noqa: ARG002
        """Generate next batch of samples."""
        if self._exhausted:
            return []

        # Bootstrap phase - random search for initial adversarial
        if self._phase == _HSJPhase.BOOTSTRAP:
            if self._is_image:
                random_arr = self._rng.random(self._source_array.shape).astype(np.float32)
            else:
                # For tabular: random in range [min-range, max+range] of source features
                spread = np.abs(self._source_array).max() + 1.0
                random_arr = self._rng.uniform(-spread, spread, self._source_array.shape).astype(
                    np.float32
                )
            self._bootstrap_attempts += 1
            return [Sample(self._wrap_output(random_arr))]

        # Boundary search - binary search between source and adversarial
        if self._phase == _HSJPhase.BOUNDARY_SEARCH:
            if self._bisection_target is None:
                self._bisection_target = self._current_best_array
                self._bisection_low = 0.0
                self._bisection_high = 1.0

            alpha = (self._bisection_low + self._bisection_high) / 2
            assert self._bisection_target is not None
            interpolated = (1 - alpha) * self._source_array + alpha * self._bisection_target
            return [Sample(self._wrap_output(interpolated))]

        # Gradient estimation - probe with random perturbations
        if self._phase == _HSJPhase.GRADIENT_ESTIMATION:
            distance = self._compute_distance(self._current_best_array)
            delta = self.theta * distance
            num_evals = min(
                int(self.min_evaluations * np.sqrt(self._iteration + 1)),
                self.max_evaluations,
            )

            self._gradient_noise = get_random(
                (num_evals, *self._source_array.shape), self.norm, seed=self.seed
            )
            noise_norms = np.linalg.norm(
                self._gradient_noise.reshape(num_evals, -1), axis=1
            ).reshape(num_evals, *((1,) * len(self._source_array.shape)))
            self._gradient_noise = self._gradient_noise / noise_norms

            samples = []
            for noise in self._gradient_noise:
                perturbed = self._current_best_array + delta * noise
                samples.append(Sample(self._wrap_output(perturbed)))

            return samples

        # Line search - step along gradient
        if self._phase == _HSJPhase.LINE_SEARCH:
            perturbed = (
                self._current_best_array + self._line_search_epsilon * self._estimated_gradient
            )
            return [Sample(self._wrap_output(perturbed))]

        # Projection - binary search back to boundary
        if self._phase == _HSJPhase.PROJECTION:
            alpha = (self._bisection_low + self._bisection_high) / 2
            assert self._bisection_target is not None
            interpolated = (1 - alpha) * self._source_array + alpha * self._bisection_target
            return [Sample(self._wrap_output(interpolated))]

        return []

    def tell(self, trials: "list[Trial[t.Any]]") -> None:
        """Process completed trials."""
        if not trials:
            return

        for trial in trials:
            if trial.status != "finished":
                continue

            # Bootstrap phase
            if self._phase == _HSJPhase.BOOTSTRAP:
                if self._is_adversarial(trial):
                    self._current_best = trial.candidate
                    self._current_best_array = _to_array(trial.candidate)
                    self._phase = _HSJPhase.BOUNDARY_SEARCH
                    logger.info(
                        f"HSJ: Found initial adversarial after {self._bootstrap_attempts} attempts"
                    )
                elif self._bootstrap_attempts > 1000:
                    logger.error("HSJ: Failed to find initial adversarial")
                    self._exhausted = True
                return

            # Boundary search
            if self._phase == _HSJPhase.BOUNDARY_SEARCH:
                is_adv = self._is_adversarial(trial)
                if is_adv:
                    self._bisection_high = (self._bisection_low + self._bisection_high) / 2
                else:
                    self._bisection_low = (self._bisection_low + self._bisection_high) / 2

                if self._bisection_high - self._bisection_low < self.boundary_tolerance:
                    # Boundary found
                    alpha = self._bisection_high
                    assert self._bisection_target is not None
                    boundary_arr = (1 - alpha) * self._source_array + alpha * self._bisection_target
                    if self._is_image:
                        boundary_arr = clip(boundary_arr, 0, 1)
                    self._current_best_array = boundary_arr
                    self._current_best = self._wrap_output(self._current_best_array)
                    self._bisection_target = None
                    self._iteration += 1

                    if self._iteration >= self.max_iterations:
                        self._exhausted = True
                        logger.info(f"HSJ: Completed {self.max_iterations} iterations")
                    else:
                        self._phase = _HSJPhase.GRADIENT_ESTIMATION
                        logger.info(
                            f"HSJ [{self._iteration}/{self.max_iterations}]: "
                            f"distance={self._compute_distance(self._current_best_array):.5f}"
                        )
                return

            # Gradient estimation
            if self._phase == _HSJPhase.GRADIENT_ESTIMATION:
                # Collect all results
                finished = [t for t in trials if t.status == "finished"]
                if len(finished) != len(self._gradient_noise):
                    return  # Wait for all results

                satisfied = np.array([self._is_adversarial(p) for p in finished], dtype=np.float32)
                f_val = 2 * satisfied - 1

                crossing_ratio = np.mean(satisfied)
                assert self._gradient_noise is not None
                if crossing_ratio in [0.0, 1.0]:
                    gradient = np.mean(self._gradient_noise, axis=0) * (2 * crossing_ratio - 1)
                else:
                    f_val = f_val - f_val.mean()
                    f_val_reshaped = f_val.reshape(
                        len(finished), *((1,) * len(self._source_array.shape))
                    )
                    gradient = np.mean(f_val_reshaped * self._gradient_noise, axis=0)

                if self.norm == "l2":
                    gradient = gradient / (np.linalg.norm(gradient) + 1e-10)
                else:
                    gradient = np.sign(gradient)

                self._estimated_gradient = gradient
                distance = self._compute_distance(self._current_best_array)
                self._line_search_epsilon = (self.step_size * distance) / np.sqrt(self._iteration)
                self._line_search_attempts = 0
                self._phase = _HSJPhase.LINE_SEARCH
                return

            # Line search
            if self._phase == _HSJPhase.LINE_SEARCH:
                self._line_search_attempts += 1
                if self._is_adversarial(trial):
                    self._current_best = trial.candidate
                    self._current_best_array = _to_array(trial.candidate)
                    # Move to projection
                    self._bisection_target = self._current_best_array.copy()
                    self._bisection_low = 0.0
                    self._bisection_high = 1.0
                    self._phase = _HSJPhase.PROJECTION
                else:
                    self._line_search_epsilon /= 2.0
                    if self._line_search_attempts > 15:
                        # Failed line search, skip to projection with current best
                        assert self._current_best_array is not None
                        self._bisection_target = self._current_best_array.copy()
                        self._bisection_low = 0.0
                        self._bisection_high = 1.0
                        self._phase = _HSJPhase.PROJECTION
                return

            # Projection
            if self._phase == _HSJPhase.PROJECTION:
                is_adv = self._is_adversarial(trial)
                if is_adv:
                    self._bisection_high = (self._bisection_low + self._bisection_high) / 2
                else:
                    self._bisection_low = (self._bisection_low + self._bisection_high) / 2

                if self._bisection_high - self._bisection_low < self.boundary_tolerance:
                    alpha = self._bisection_high
                    assert self._bisection_target is not None
                    boundary_arr = (1 - alpha) * self._source_array + alpha * self._bisection_target
                    if self._is_image:
                        boundary_arr = clip(boundary_arr, 0, 1)
                    self._current_best_array = boundary_arr
                    self._current_best = self._wrap_output(self._current_best_array)
                    self._bisection_target = None

                    # Yield result and start next iteration
                    self._iteration += 1
                    if self._iteration >= self.max_iterations:
                        self._exhausted = True
                    else:
                        self._phase = _HSJPhase.GRADIENT_ESTIMATION

    @property
    def exhausted(self) -> bool:
        return self._exhausted

    def reset(self) -> None:
        """Reset sampler state."""
        self._rng = np.random.default_rng(self.seed)
        self._current_best = self.adversarial
        self._current_best_array = (
            _to_array(self.adversarial) if self.adversarial is not None else None
        )
        self._iteration = 0
        self._exhausted = False
        self._phase = (
            _HSJPhase.BOUNDARY_SEARCH if self.adversarial is not None else _HSJPhase.BOOTSTRAP
        )
        self._bootstrap_attempts = 0
        self._bisection_low = 0.0
        self._bisection_high = 1.0
        self._bisection_target = None
