"""Boundary Attack (Brendel et al. 2018): decision-based numeric evasion.

Find any adversarial point by growing Gaussian noise, then binary-search back
toward the original to minimise the L2/Linf perturbation while staying
misclassified. Uses only the hard label (decision-based).
"""

import typing as t

from dreadnode.airt.evasion._base import ModelEvasionAttack, _dist
from dreadnode.airt.targets.prediction import PredictionTargetSpec, QueryInput


async def run(attack: ModelEvasionAttack) -> t.Any:
    base = await attack._predict([attack.original])
    x0, orig_label, orig_cls = attack._numeric_setup(base)
    base_conf = attack._orig_confidence(base[0], orig_cls)

    adv, adv_label = await attack._find_adversarial(x0, orig_label)
    if adv is None:
        return attack._numeric_result(
            x0, x0, orig_label, None, [], success=False, residual=base_conf
        )

    # Binary search toward the original to shrink the perturbation.
    best = adv
    lo, hi = 0.0, 1.0
    curve: list[tuple[int, float]] = []
    for it in range(30):
        if attack._over_budget():
            break
        mid = (lo + hi) / 2
        cand = x0 + mid * (adv - x0)
        p = (await attack._predict([cand]))[0]
        if attack._label(p) != orig_label:
            best, adv_label = cand, attack._label(p)
            hi = mid
        else:
            lo = mid
        dist = _dist(x0, best, attack.norm)
        curve.append((attack._query_count, dist))
        attack._trace_step(
            it,
            input=attack._preview_vec(best),
            output=attack._pred_summary(p),
            metrics={"distance": round(dist, 6), "queries": attack._query_count},
        )
    return attack._numeric_result(x0, best, orig_label, adv_label, curve, success=True)


def boundary_evasion(
    target: PredictionTargetSpec, original: QueryInput, **kwargs: t.Any
) -> ModelEvasionAttack:
    """Boundary Attack (Brendel et al. 2018): decision-based black-box evasion for
    numeric inputs. Finds an adversarial point, then minimises the L2/Linf
    perturbation while keeping the prediction flipped."""
    return ModelEvasionAttack(strategy="boundary", target=target, original=original, **kwargs)
