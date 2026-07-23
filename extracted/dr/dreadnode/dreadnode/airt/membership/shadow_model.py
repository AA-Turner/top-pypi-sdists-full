"""Shadow-model membership inference (Shokri et al. 2017).

Train a shadow classifier on half the records, learn an in/out attack classifier
from the shadow's confidence on its train (in) vs held-out (out) records, then
score the target's confidences with it. Ensembled over several random splits.
"""

import typing as t

import numpy as np

from dreadnode.airt.membership._base import (
    MembershipInferenceAttack,
    MembershipResult,
    membership_auc,
)
from dreadnode.airt.targets.prediction import PredictionTargetSpec, QueryInput


async def _shadow_model_scores(
    attack: MembershipInferenceAttack,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Shadow-model attack (Shokri et al. 2017): train a shadow classifier on
    half the records, learn an in/out attack classifier from the shadow's
    confidence on its train (in) vs held-out (out) records, then score the
    target's confidences with it. Emits a per-split step trace."""
    feat, y, target_conf, is_member = await attack._target_setup()
    n = len(y)
    half = max(2, n // 2)
    # Ensemble over several random shadow splits and average the attack
    # scores. A single split is high-variance - the 1D in/out classifier can
    # invert on an unlucky split (AUC < 0.5) - so we only keep splits where
    # the shadow's train (in) records are more confident than its held-out
    # (out) ones, which is the memorisation signal the attack relies on.
    agg = np.zeros(n)
    votes = 0
    for split in range(attack.n_shadow):
        idx = attack.rng.permutation(n)
        tr, out = idx[:half], idx[half:]
        if len(tr) < 2 or len(out) < 2:
            continue
        shadow = attack._fit_shadow(feat[tr], y[tr])
        conf_in = shadow.predict_proba(feat[tr])[np.arange(len(tr)), y[tr]]
        conf_out = shadow.predict_proba(feat[out])[np.arange(len(out)), y[out]]
        if float(conf_in.mean()) <= float(conf_out.mean()):
            continue  # degenerate / inverted shadow - would flip the direction
        attack_x = np.concatenate([conf_in, conf_out]).reshape(-1, 1)
        attack_y = np.array([1] * len(tr) + [0] * len(out))
        clf = attack._fit_shadow(attack_x, attack_y)
        agg += clf.predict_proba(target_conf.reshape(-1, 1))[:, 1]
        votes += 1
        cur = agg / votes
        running_auc = membership_auc(cur, is_member) if len(np.unique(is_member)) >= 2 else 0.0
        attack._trace_step(
            split,
            input={"shadow_split": int(split), "train_size": len(tr)},
            output={
                "conf_in_mean": round(float(conf_in.mean()), 6),
                "conf_out_mean": round(float(conf_out.mean()), 6),
                "kept_splits": votes,
            },
            metrics={"auc": round(running_auc, 4), "queries": attack._query_count},
        )
    scores = agg / votes if votes else target_conf
    return scores, is_member, y


async def run(attack: MembershipInferenceAttack) -> MembershipResult:
    scores, is_member, true_labels = await _shadow_model_scores(attack)
    records = list(attack.members) + list(attack.nonmembers)
    return attack._build_result(scores, is_member, true_labels, records=records)


def shadow_model_membership(
    target: PredictionTargetSpec,
    members: t.Sequence[QueryInput],
    nonmembers: t.Sequence[QueryInput],
    **kwargs: t.Any,
) -> MembershipInferenceAttack:
    """Shadow-model membership inference (Shokri et al. 2017). Trains a shadow
    classifier and an in/out attack classifier on shadow confidences, then applies
    it to the target's outputs. Needs per-record labels."""
    return MembershipInferenceAttack(
        method="shadow_model", target=target, members=members, nonmembers=nonmembers, **kwargs
    )
