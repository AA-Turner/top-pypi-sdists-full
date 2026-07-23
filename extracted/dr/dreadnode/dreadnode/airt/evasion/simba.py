"""SimBA (Guo et al. 2019): score-based numeric evasion.

Walk one random coordinate at a time, keeping a +/- step whenever it lowers the
target's confidence in the original class, until the label flips.
"""

import typing as t

from dreadnode.airt.evasion._base import ModelEvasionAttack, _dist
from dreadnode.airt.targets.prediction import PredictionTargetSpec, QueryInput


async def run(attack: ModelEvasionAttack) -> t.Any:
    import numpy as np

    base = await attack._predict([attack.original])
    x0, orig_label, orig_cls = attack._numeric_setup(base)
    cur = x0.copy()
    cur_conf = attack._orig_confidence(base[0], orig_cls)
    eps = 0.2 * (np.linalg.norm(x0) / np.sqrt(x0.size) + 1e-6)
    curve: list[tuple[int, float]] = []
    it = 0
    # Repeated epochs over the coordinate set: one pass rarely flips a confident
    # victim, so keep sweeping (accepting any confidence-reducing step) until the
    # label flips, the budget is spent, or an epoch stalls.
    while not attack._over_budget():
        progressed = False
        for idx in attack.rng.permutation(x0.size):
            if attack._over_budget():
                break
            for sign in (1.0, -1.0):
                if attack._over_budget():
                    break
                cand = cur.copy()
                cand[idx] += sign * eps
                p = (await attack._predict([cand]))[0]
                if attack._label(p) != orig_label:
                    curve.append((attack._query_count, _dist(x0, cand, attack.norm)))
                    return attack._numeric_result(
                        x0, cand, orig_label, attack._label(p), curve, success=True
                    )
                conf = attack._orig_confidence(p, orig_cls)
                if conf < cur_conf:
                    cur, cur_conf, progressed = cand, conf, True
                    break
            it += 1
            if it % 8 == 0:
                curve.append((attack._query_count, _dist(x0, cur, attack.norm)))
                attack._trace_step(
                    it,
                    input=attack._preview_vec(cur),
                    output={"predicted_label": orig_label, "confidence": round(cur_conf, 4)},
                    metrics={"confidence": round(cur_conf, 4), "queries": attack._query_count},
                )
        if not progressed:
            break
    return attack._numeric_result(
        x0, cur, orig_label, None, curve, success=False, residual=cur_conf
    )


def simba_evasion(
    target: PredictionTargetSpec, original: QueryInput, **kwargs: t.Any
) -> ModelEvasionAttack:
    """SimBA (Guo et al. 2019): score-based evasion that perturbs one random
    coordinate at a time, keeping steps that lower the original-class confidence."""
    return ModelEvasionAttack(strategy="simba", target=target, original=original, **kwargs)
