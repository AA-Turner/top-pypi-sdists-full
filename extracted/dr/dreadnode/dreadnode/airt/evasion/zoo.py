"""ZOO (Chen et al. 2017): zeroth-order-optimization numeric evasion.

Estimate the gradient of the original-class confidence by symmetric finite
differences over a sampled coordinate subset, then descend it. Score-based; needs
per-class confidences from the target.
"""

import typing as t

from dreadnode.airt.evasion._base import ModelEvasionAttack, _dist
from dreadnode.airt.targets.prediction import PredictionTargetSpec, QueryInput


async def run(attack: ModelEvasionAttack) -> t.Any:
    import numpy as np

    base = await attack._predict([attack.original])
    x0, orig_label, orig_cls = attack._numeric_setup(base)
    n = x0.size
    cur = x0.copy()
    h = 0.01 * (np.linalg.norm(x0) / np.sqrt(n) + 1e-6)
    # Fixed-size step along the NORMALISED gradient direction (sign-SGD style): a
    # saturated victim yields a tiny-magnitude but correctly-signed finite-diff
    # gradient, so descending the raw gradient stalls - normalising keeps every
    # step effective.
    step = 0.5 * (np.linalg.norm(x0) / np.sqrt(n) + 1e-6)
    curve: list[tuple[int, float]] = []
    for it in range(attack.max_iterations * 4):
        if attack._over_budget():
            break
        k = min(n, max(2, attack._budget_left() // 2))
        coords = attack.rng.choice(n, size=k, replace=False)
        grad = np.zeros(n)
        for c in coords:
            if attack._over_budget():
                break
            ep, en = cur.copy(), cur.copy()
            ep[c] += h
            en[c] -= h
            pp, pn = await attack._predict([ep, en])
            grad[c] = (
                attack._orig_confidence(pp, orig_cls) - attack._orig_confidence(pn, orig_cls)
            ) / (2 * h)
        gnorm = float(np.linalg.norm(grad))
        if gnorm < 1e-15:
            grad = attack.rng.normal(0, 1, n)
            gnorm = float(np.linalg.norm(grad)) + 1e-12
        cur = cur - step * grad / gnorm
        p = (await attack._predict([cur]))[0]
        dist = _dist(x0, cur, attack.norm)
        curve.append((attack._query_count, dist))
        attack._trace_step(
            it,
            input=attack._preview_vec(cur),
            output=attack._pred_summary(p),
            metrics={
                "confidence": round(attack._orig_confidence(p, orig_cls), 4),
                "distance": round(dist, 6),
                "queries": attack._query_count,
            },
        )
        if attack._label(p) != orig_label:
            return attack._numeric_result(
                x0, cur, orig_label, attack._label(p), curve, success=True
            )
    p = (await attack._predict([cur]))[0]
    return attack._numeric_result(
        x0,
        cur,
        orig_label,
        None,
        curve,
        success=False,
        residual=attack._orig_confidence(p, orig_cls),
    )


def zoo_evasion(
    target: PredictionTargetSpec, original: QueryInput, **kwargs: t.Any
) -> ModelEvasionAttack:
    """ZOO (Chen et al. 2017): zeroth-order evasion that estimates the gradient of
    the original-class confidence via finite differences and descends it."""
    return ModelEvasionAttack(strategy="zoo", target=target, original=original, **kwargs)
