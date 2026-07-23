"""HopSkipJump (Chen, Jordan, Wainwright 2020): decision-based numeric evasion.

Find an adversarial point, then repeatedly (1) binary-search onto the boundary,
(2) Monte-Carlo estimate the boundary gradient direction from label-only queries,
and (3) take a geometric step, shrinking the perturbation each iteration.
Query-efficient and works when the target returns only a hard label.
"""

import typing as t

import numpy as np

from dreadnode.airt.evasion._base import ModelEvasionAttack, _dist
from dreadnode.airt.targets.prediction import PredictionTargetSpec, QueryInput


async def run(attack: ModelEvasionAttack) -> t.Any:
    x0, orig_label, orig_cls = attack._numeric_setup(await attack._predict([attack.original]))
    base_conf = attack._orig_confidence((await attack._predict([x0]))[0], orig_cls)
    adv, adv_label = await attack._find_adversarial(x0, orig_label)
    if adv is None:
        return attack._numeric_result(
            x0, x0, orig_label, None, [], success=False, residual=base_conf
        )
    best = adv
    curve: list[tuple[int, float]] = []
    for it in range(attack.max_iterations):
        if attack._over_budget():
            break
        lo, hi = 0.0, 1.0
        for _ in range(10):
            if attack._over_budget():
                break
            mid = (lo + hi) / 2
            p = (await attack._predict([x0 + mid * (best - x0)]))[0]
            if attack._label(p) != orig_label:
                hi, adv_label = mid, attack._label(p)
            else:
                lo = mid
        boundary = x0 + hi * (best - x0)
        batch = min(20, max(4, attack._budget_left() // 4))
        if batch <= 0 or attack._over_budget():
            best = boundary
            break
        delta = 0.01 * np.linalg.norm(boundary - x0) + 1e-6
        dirs = attack.rng.normal(0, 1, (batch, x0.size))
        dirs /= np.linalg.norm(dirs, axis=1, keepdims=True) + 1e-12
        preds = await attack._predict([boundary + delta * d for d in dirs])
        signs = np.array([1.0 if attack._label(p) != orig_label else -1.0 for p in preds])
        grad = (signs[:, None] * dirs).mean(axis=0)
        gnorm = float(np.linalg.norm(grad))
        if gnorm < 1e-12:
            best = boundary
            break
        grad /= gnorm
        step = np.linalg.norm(boundary - x0) / np.sqrt(it + 1) + 1e-9
        moved = boundary
        last_pred = None
        for _ in range(6):
            if attack._over_budget():
                break
            p = (await attack._predict([boundary + step * grad]))[0]
            last_pred = p
            if attack._label(p) != orig_label:
                moved, adv_label = boundary + step * grad, attack._label(p)
                break
            step /= 2
        best = moved
        dist = _dist(x0, best, attack.norm)
        curve.append((attack._query_count, dist))
        attack._trace_step(
            it,
            input=attack._preview_vec(best),
            output=attack._pred_summary(last_pred) if last_pred is not None else None,
            metrics={"distance": round(dist, 6), "queries": attack._query_count},
        )
    return attack._numeric_result(x0, best, orig_label, adv_label, curve, success=True)


def hopskipjump_evasion(
    target: PredictionTargetSpec, original: QueryInput, **kwargs: t.Any
) -> ModelEvasionAttack:
    """HopSkipJump (Chen, Jordan, Wainwright 2020): decision-based evasion that
    estimates the boundary gradient from label-only queries and takes geometric
    steps - query-efficient and works when the target returns only a hard label."""
    return ModelEvasionAttack(strategy="hopskipjump", target=target, original=original, **kwargs)
