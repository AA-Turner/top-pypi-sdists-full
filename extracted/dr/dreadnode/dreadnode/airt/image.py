"""Adversarial attack wrappers for image and tabular data.

Convenience functions that combine adversarial samplers with Study for easy use.
All attacks accept either ``Image`` or ``np.ndarray`` inputs — pass a numpy array
for tabular/numeric data, or an ``Image`` for pixel-based attacks.

For more control, use the samplers directly from ``dreadnode.samplers``.
"""

import typing as t

import numpy as np

from dreadnode.optimization import Study
from dreadnode.samplers import (
    HopSkipJumpSampler,
    NESSampler,
    SimBASampler,
    ZOOSampler,
)
from dreadnode.samplers.image import ArrayInput

if t.TYPE_CHECKING:
    from dreadnode.core.scorer import ScorersLike
    from dreadnode.core.types import Image
    from dreadnode.scorers.image import Norm


def _detect_modality(original: ArrayInput) -> str:
    """Infer input_modality from the input type."""
    from dreadnode.core.types import Image

    if isinstance(original, Image):
        return "image"
    arr = np.asarray(original)
    if arr.ndim <= 2 and arr.shape[-1] < 100:
        return "tabular"
    return "image"


def simba_attack(
    original: "Image | np.ndarray",
    objective: "ScorersLike[t.Any]",
    *,
    theta: float = 0.1,
    num_masks: int = 500,
    norm: "Norm" = "l2",
    max_iterations: int = 10_000,
    seed: int | None = None,
    airt_assessment_id: str | None = None,
    airt_goal_category: str | None = None,
    airt_target_model: str | None = None,
) -> "Study[t.Any]":
    """
    Create a SimBA (Simple Black-box Attack) study.

    Iteratively perturbs the input using random noise masks and retains
    perturbations that improve the adversarial objective.
    Works with both image and tabular (numpy array) inputs.

    See: https://arxiv.org/abs/1805.12317

    Args:
        original: The original input to perturb (Image or ndarray).
        objective: Scorer(s) to evaluate adversarial success.
        theta: Perturbation step size.
        num_masks: Number of random masks to pre-generate.
        norm: Distance metric ('l2', 'l1', or 'linf').
        max_iterations: Maximum attack iterations.
        seed: Random seed for reproducibility.

    Returns:
        A configured Study instance.

    Example:
        ```python
        from dreadnode.airt import simba_attack
        from dreadnode.scorers import target_class

        study = simba_attack(
            original=my_image,
            objective=target_class(model, target_label=5),
            max_iterations=1000,
        )
        result = await study.run()
        ```
    """
    sampler = SimBASampler(
        original,
        theta=theta,
        num_masks=num_masks,
        norm=norm,
        max_iterations=max_iterations,
        seed=seed,
    )

    return Study(
        sampler=sampler,
        objective=objective,
        direction="maximize",
        n_iterations=max_iterations,
        max_trials=max_iterations,
        tags=["airt"],
        airt_attack_domain="adversarial_ml",
        airt_attack_name="simba_attack",
        airt_distance_norm=norm,
        airt_input_modality=_detect_modality(original),
        airt_assessment_id=airt_assessment_id,
        airt_goal_category=airt_goal_category,
        airt_target_model=airt_target_model,
    )


def nes_attack(
    original: "Image | np.ndarray",
    objective: "ScorersLike[t.Any]",
    *,
    learning_rate: float = 0.01,
    num_samples: int = 64,
    sigma: float = 0.001,
    max_iterations: int = 100,
    seed: int | None = None,
    airt_assessment_id: str | None = None,
    airt_goal_category: str | None = None,
    airt_target_model: str | None = None,
) -> "Study[t.Any]":
    """
    Create a NES (Natural Evolution Strategies) attack study.

    Estimates gradients by probing with random perturbations and uses
    Adam optimizer for updates.
    Works with both image and tabular (numpy array) inputs.

    Args:
        original: The original input to perturb (Image or ndarray).
        objective: Scorer(s) to evaluate adversarial success.
        learning_rate: Adam optimizer learning rate.
        num_samples: Number of samples for gradient estimation.
        sigma: Noise scale for gradient estimation.
        max_iterations: Maximum attack iterations.
        seed: Random seed for reproducibility.

    Returns:
        A configured Study instance.

    Example:
        ```python
        from dreadnode.airt import nes_attack
        from dreadnode.scorers import target_class

        study = nes_attack(
            original=my_image,
            objective=target_class(model, target_label=5),
            max_iterations=100,
        )
        result = await study.run()
        ```
    """
    sampler = NESSampler(
        original,
        learning_rate=learning_rate,
        num_samples=num_samples,
        sigma=sigma,
        max_iterations=max_iterations,
        seed=seed,
    )

    return Study(
        sampler=sampler,
        objective=objective,
        direction="maximize",
        n_iterations=max_iterations,
        max_trials=max_iterations,
        tags=["airt"],
        airt_attack_domain="adversarial_ml",
        airt_attack_name="nes_attack",
        airt_distance_norm="l2",
        airt_input_modality=_detect_modality(original),
        airt_assessment_id=airt_assessment_id,
        airt_goal_category=airt_goal_category,
        airt_target_model=airt_target_model,
    )


def zoo_attack(
    original: "Image | np.ndarray",
    objective: "ScorersLike[t.Any]",
    *,
    learning_rate: float = 0.01,
    num_samples: int = 128,
    epsilon: float = 0.01,
    max_iterations: int = 1000,
    seed: int | None = None,
    airt_assessment_id: str | None = None,
    airt_goal_category: str | None = None,
    airt_target_model: str | None = None,
) -> "Study[t.Any]":
    """
    Create a ZOO (Zeroth-Order Optimization) attack study.

    Uses coordinate-wise gradient estimation with Adam optimizer.
    Works with both image and tabular (numpy array) inputs.

    See: https://arxiv.org/abs/1708.03999

    Args:
        original: The original input to perturb (Image or ndarray).
        objective: Scorer(s) to evaluate adversarial success.
        learning_rate: Adam optimizer learning rate.
        num_samples: Number of coordinates to sample per iteration.
        epsilon: Step size for finite difference gradient estimation.
        max_iterations: Maximum attack iterations.
        seed: Random seed for reproducibility.

    Returns:
        A configured Study instance.

    Example:
        ```python
        from dreadnode.airt import zoo_attack
        from dreadnode.scorers import target_class

        study = zoo_attack(
            original=my_image,
            objective=target_class(model, target_label=5),
            max_iterations=500,
        )
        result = await study.run()
        ```
    """
    sampler = ZOOSampler(
        original,
        learning_rate=learning_rate,
        num_samples=num_samples,
        epsilon=epsilon,
        max_iterations=max_iterations,
        seed=seed,
    )

    return Study(
        sampler=sampler,
        objective=objective,
        direction="maximize",
        n_iterations=max_iterations,
        max_trials=max_iterations,
        tags=["airt"],
        airt_attack_domain="adversarial_ml",
        airt_attack_name="zoo_attack",
        airt_distance_norm="l2",
        airt_input_modality=_detect_modality(original),
        airt_assessment_id=airt_assessment_id,
        airt_goal_category=airt_goal_category,
        airt_target_model=airt_target_model,
    )


def hopskipjump_attack(
    source: "Image | np.ndarray",
    objective: "ScorersLike[t.Any]",
    *,
    adversarial: "Image | np.ndarray | None" = None,
    adversarial_threshold: float = 0.0,
    norm: "Norm" = "l2",
    theta: float = 0.01,
    max_iterations: int = 1000,
    seed: int | None = None,
    airt_assessment_id: str | None = None,
    airt_goal_category: str | None = None,
    airt_target_model: str | None = None,
) -> "Study[t.Any]":
    """
    Create a HopSkipJump attack study.

    A decision-based attack that uses binary search to find the decision
    boundary and gradient estimation to minimize the perturbation distance.
    Works with both image and tabular (numpy array) inputs.

    See: https://arxiv.org/abs/1904.02144

    Args:
        source: The original, unperturbed input (Image or ndarray).
        objective: Scorer(s) to evaluate adversarial success.
        adversarial: Optional initial adversarial example.
        adversarial_threshold: Score threshold for adversarial classification.
        norm: Distance metric ('l2', 'l1', or 'linf').
        theta: Relative size of perturbation for gradient estimation.
        max_iterations: Maximum attack iterations.
        seed: Random seed for reproducibility.

    Returns:
        A configured Study instance.

    Example:
        ```python
        from dreadnode.airt import hopskipjump_attack
        import numpy as np

        # Image attack
        study = hopskipjump_attack(source=my_image, objective=scorer)

        # Tabular attack (e.g. fraud detection with 30 features)
        features = np.array([0.1, 0.5, ...])  # 30 floats
        study = hopskipjump_attack(source=features, objective=scorer)
        result = await study.run()
        ```
    """
    sampler = HopSkipJumpSampler(
        source,
        adversarial=adversarial,
        adversarial_threshold=adversarial_threshold,
        norm=norm,
        theta=theta,
        max_iterations=max_iterations,
        seed=seed,
    )

    return Study(
        sampler=sampler,
        objective=objective,
        direction="maximize",
        n_iterations=max_iterations,
        max_trials=max_iterations,
        tags=["airt"],
        airt_attack_domain="adversarial_ml",
        airt_attack_name="hopskipjump_attack",
        airt_distance_norm=norm,
        airt_input_modality=_detect_modality(source),
        airt_assessment_id=airt_assessment_id,
        airt_goal_category=airt_goal_category,
        airt_target_model=airt_target_model,
    )
