"""MI-Face-style confidence-maximizing model inversion (Fredrikson et al. 2015).

For each target class, start from a neutral reconstruction (zeros, or the mean of
that class's reference inputs) and hill-climb: perturb with Gaussian noise via the
attack rng and keep any perturbation that raises the target's confidence for the
class. Purely query based - no gradients from the model.
"""

import typing as t

import numpy as np

from dreadnode.airt.inversion._base import (
    InversionResult,
    ModelInversionAttack,
    build_inversion_result,
)
from dreadnode.airt.targets.prediction import PredictionTargetSpec


async def _invert_class(
    attack: ModelInversionAttack, cls: int, curve: list[tuple[int, float]]
) -> dict[str, t.Any]:
    """Hill-climb a reconstruction for a single class and return its result row."""
    cur = attack._neutral_input(cls)
    base = (await attack._query([cur]))[0]
    best_conf = attack._class_confidence(base.vector, cls)
    dim = cur.size
    # Perturbation scale relative to the current reconstruction magnitude, with a
    # unit floor so a zero start still explores meaningfully.
    sigma = max(0.5, 0.2 * float(np.linalg.norm(cur)) / np.sqrt(dim))
    for it in range(attack.max_iterations):
        if attack._over_budget():
            break
        cand = cur + attack.rng.normal(0.0, sigma, cur.shape)
        pred = (await attack._query([cand]))[0]
        conf = attack._class_confidence(pred.vector, cls)
        if conf > best_conf:
            cur, best_conf = cand, conf
        curve.append((attack._query_count, best_conf))
        attack._trace_step(
            it,
            input=attack._preview(cur),
            output={"target_class": cls, "confidence": round(best_conf, 4)},
            metrics={"confidence": round(best_conf, 4), "queries": attack._query_count},
            target_class=cls,
        )
        # Saturated - the class is fully recovered, no gain from more steps.
        if best_conf >= 0.999:
            break

    return {
        "class": int(cls),
        "achieved_confidence": round(float(best_conf), 4),
        "queries": attack._query_count,
        "reconstruction_preview": attack._preview(cur),
        "reconstruction_image": attack._reconstruction_image(cur),
        "reference_similarity": attack._reference_similarity(cur, cls),
    }


async def run(attack: ModelInversionAttack) -> InversionResult:
    per_class: list[dict[str, t.Any]] = []
    curve: list[tuple[int, float]] = []
    for cls in attack.target_classes:
        if attack._over_budget():
            break
        per_class.append(await _invert_class(attack, cls, curve))
    return build_inversion_result(attack, per_class, curve)


def confidence_inversion(
    target: PredictionTargetSpec, num_classes: int, **kwargs: t.Any
) -> ModelInversionAttack:
    """MI-Face-style confidence-maximizing model inversion (Fredrikson et al. 2015):
    per class, hill-climb a reconstruction by keeping Gaussian perturbations that
    raise the target's confidence for that class."""
    return ModelInversionAttack(
        strategy="confidence", target=target, num_classes=num_classes, **kwargs
    )
