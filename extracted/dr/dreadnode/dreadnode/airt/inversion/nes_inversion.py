"""NES model inversion: confidence-maximizing reconstruction via Natural
Evolution Strategies (Wierstra et al. 2014; Ilyas et al. 2018 for the black-box
query setting).

Same objective as MI-Face (maximize the target's confidence for a class) but the
ascent direction is estimated from a Gaussian population of antithetic
perturbations weighted by the confidence each achieves, then a step is taken along
that weighted mean. More query-efficient than coordinate hill-climbing in higher
dimensions. Purely query based - no gradients from the model.
"""

import typing as t

import numpy as np

from dreadnode.airt.inversion._base import (
    InversionResult,
    ModelInversionAttack,
    build_inversion_result,
)
from dreadnode.airt.targets.prediction import PredictionTargetSpec

#: NES population (antithetic pairs) and step size per iteration.
_POPULATION = 6
_LEARNING_RATE = 0.5


async def _invert_class(
    attack: ModelInversionAttack, cls: int, curve: list[tuple[int, float]]
) -> dict[str, t.Any]:
    """Estimate an NES ascent direction per iteration and step the reconstruction."""
    cur = attack._neutral_input(cls)
    base = (await attack._query([cur]))[0]
    best = cur.copy()
    best_conf = attack._class_confidence(base.vector, cls)
    dim = cur.size
    sigma = max(0.5, 0.2 * float(np.linalg.norm(cur)) / np.sqrt(dim))
    for it in range(attack.max_iterations):
        # Need the whole antithetic population plus a probe of the stepped point.
        if attack._budget_left() < 2 * _POPULATION + 1:
            break
        # Antithetic sampling: +noise and -noise share a draw for lower variance.
        noises = [attack.rng.normal(0.0, 1.0, cur.shape) for _ in range(_POPULATION)]
        candidates = [cur + sigma * n for n in noises] + [cur - sigma * n for n in noises]
        preds = await attack._query(candidates)
        confs = np.array([attack._class_confidence(p.vector, cls) for p in preds])
        # Standardize the rewards so the step is scale-free.
        weights = confs - confs.mean()
        std = float(confs.std())
        if std > 1e-8:
            weights = weights / std
        grad = np.zeros_like(cur)
        for k, n in enumerate(noises):
            grad += (weights[k] - weights[k + _POPULATION]) * n
        grad /= 2 * _POPULATION * sigma
        cur = cur + _LEARNING_RATE * sigma * grad

        pred = (await attack._query([cur]))[0]
        conf = attack._class_confidence(pred.vector, cls)
        if conf > best_conf:
            best, best_conf = cur.copy(), conf
        curve.append((attack._query_count, best_conf))
        attack._trace_step(
            it,
            input=attack._preview(cur),
            output={"target_class": cls, "confidence": round(conf, 4)},
            metrics={"confidence": round(best_conf, 4), "queries": attack._query_count},
            target_class=cls,
        )
        if best_conf >= 0.999:
            break

    return {
        "class": int(cls),
        "achieved_confidence": round(float(best_conf), 4),
        "queries": attack._query_count,
        "reconstruction_preview": attack._preview(best),
        "reconstruction_image": attack._reconstruction_image(best),
        "reference_similarity": attack._reference_similarity(best, cls),
    }


async def run(attack: ModelInversionAttack) -> InversionResult:
    per_class: list[dict[str, t.Any]] = []
    curve: list[tuple[int, float]] = []
    for cls in attack.target_classes:
        if attack._over_budget():
            break
        per_class.append(await _invert_class(attack, cls, curve))
    return build_inversion_result(attack, per_class, curve)


def nes_inversion(
    target: PredictionTargetSpec, num_classes: int, **kwargs: t.Any
) -> ModelInversionAttack:
    """NES model inversion: reconstruct a representative input per class by
    estimating a confidence-ascent direction from a Gaussian population of
    perturbations and stepping along the weighted mean. Query-efficient in higher
    dimensions."""
    return ModelInversionAttack(strategy="nes", target=target, num_classes=num_classes, **kwargs)
