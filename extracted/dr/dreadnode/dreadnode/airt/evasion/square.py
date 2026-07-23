"""Square Attack (Andriushchenko et al. 2020): Linf-bounded random search.

Flip a random contiguous block of features to +/-eps, keeping the change whenever
it lowers the original-class confidence. A strong score-based attack that needs
no gradient estimate.
"""

import typing as t

from dreadnode.airt.evasion._base import ModelEvasionAttack, _dist
from dreadnode.airt.targets.prediction import PredictionTargetSpec, QueryInput


async def run(attack: ModelEvasionAttack) -> t.Any:
    import numpy as np

    base = await attack._predict([attack.original])
    x0, orig_label, orig_cls = attack._numeric_setup(base)
    n = x0.size
    # Linf radius: a bounded perturbation by design, sized to the input's scale so
    # the search is effective on both high-dim (image) and low-dim tabular inputs.
    eps = 1.5 * (float(np.abs(x0).mean()) + 1e-6)
    cur = x0 + attack.rng.choice([-eps, eps], size=n)
    p = (await attack._predict([cur]))[0]
    if attack._label(p) != orig_label:
        return attack._numeric_result(
            x0,
            cur,
            orig_label,
            attack._label(p),
            [(attack._query_count, _dist(x0, cur, attack.norm))],
            success=True,
        )
    cur_conf = attack._orig_confidence(p, orig_cls)
    curve: list[tuple[int, float]] = []
    blk = max(1, n // 8)
    for it in range(attack.max_iterations * 8):
        if attack._over_budget():
            break
        start = int(attack.rng.integers(0, max(1, n - blk)))
        cand = cur.copy()
        width = len(cand[start : start + blk])
        cand[start : start + blk] = x0[start : start + blk] + attack.rng.choice(
            [-eps, eps], size=width
        )
        cand = np.clip(cand, x0 - eps, x0 + eps)
        p = (await attack._predict([cand]))[0]
        if attack._label(p) != orig_label:
            curve.append((attack._query_count, _dist(x0, cand, attack.norm)))
            return attack._numeric_result(
                x0, cand, orig_label, attack._label(p), curve, success=True
            )
        conf = attack._orig_confidence(p, orig_cls)
        if conf < cur_conf:
            cur, cur_conf = cand, conf
            curve.append((attack._query_count, conf))
            attack._trace_step(
                it,
                input=attack._preview_vec(cur),
                output=attack._pred_summary(p),
                metrics={"confidence": round(conf, 4), "queries": attack._query_count},
            )
    return attack._numeric_result(
        x0, cur, orig_label, None, curve, success=False, residual=cur_conf
    )


def square_evasion(
    target: PredictionTargetSpec, original: QueryInput, **kwargs: t.Any
) -> ModelEvasionAttack:
    """Square Attack (Andriushchenko et al. 2020): Linf-bounded random search that
    flips contiguous blocks of features, keeping confidence-reducing changes."""
    return ModelEvasionAttack(strategy="square", target=target, original=original, **kwargs)
