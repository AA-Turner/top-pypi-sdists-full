"""LiRA likelihood-ratio membership inference (Carlini et al. 2022), offline variant.

Train several shadow models on random halves; for each record collect the
logit-scaled confidences from the shadows that did NOT train on it (the OUT
distribution), then score the target's confidence by how many standard deviations
it exceeds that OUT mean - a per-record likelihood-ratio test.
"""

import typing as t

import numpy as np

from dreadnode.airt.membership._base import MembershipInferenceAttack, MembershipResult
from dreadnode.airt.targets.prediction import PredictionTargetSpec, QueryInput


def _logit(p: np.ndarray) -> np.ndarray:
    p = np.clip(p, 1e-6, 1 - 1e-6)
    return np.log(p / (1 - p))


async def _lira_scores(
    attack: MembershipInferenceAttack,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """LiRA (Carlini et al. 2022), offline variant. Trains shadow models on random
    halves, models each record's OUT confidence distribution, and scores the
    target's confidence against it. Emits a per-shadow step trace."""
    feat, y, target_conf, is_member = await attack._target_setup()
    n = len(y)
    rows = np.arange(n)
    out_logits: list[list[float]] = [[] for _ in range(n)]
    trained = 0
    for shadow_i in range(attack.n_shadow):
        mask = attack.rng.random(n) < 0.5
        if mask.sum() < 2 or (~mask).sum() < 2:
            continue
        shadow = attack._fit_shadow(feat[mask], y[mask])
        conf = shadow.predict_proba(feat)[rows, y]
        lg = _logit(conf)
        for i in range(n):
            if not mask[i]:
                out_logits[i].append(float(lg[i]))
        trained += 1
        covered = int(sum(1 for logs in out_logits if len(logs) >= 2))
        attack._trace_step(
            shadow_i,
            input={"shadow_index": int(shadow_i), "out_size": int((~mask).sum())},
            output={
                "trained_shadows": trained,
                "records_with_out_dist": covered,
            },
            metrics={"records_covered": covered, "queries": attack._query_count},
        )
    target_lg = _logit(target_conf)
    scores = np.zeros(n)
    for i in range(n):
        if len(out_logits[i]) >= 2:
            mu = float(np.mean(out_logits[i]))
            sd = float(np.std(out_logits[i])) + 1e-6
            scores[i] = (target_lg[i] - mu) / sd
        else:
            scores[i] = target_conf[i]
    return scores, is_member, y


async def run(attack: MembershipInferenceAttack) -> MembershipResult:
    scores, is_member, true_labels = await _lira_scores(attack)
    records = list(attack.members) + list(attack.nonmembers)
    return attack._build_result(scores, is_member, true_labels, records=records)


def lira_membership(
    target: PredictionTargetSpec,
    members: t.Sequence[QueryInput],
    nonmembers: t.Sequence[QueryInput],
    **kwargs: t.Any,
) -> MembershipInferenceAttack:
    """LiRA likelihood-ratio membership inference (Carlini et al. 2022), offline
    variant. Trains shadow models to model each record's OUT confidence
    distribution, then scores the target's confidence against it. Needs labels."""
    return MembershipInferenceAttack(
        method="lira", target=target, members=members, nonmembers=nonmembers, **kwargs
    )
