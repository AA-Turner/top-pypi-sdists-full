"""Label-only membership inference (Choquette-Choo et al., arXiv 2007.14321).

Membership score = fraction of noisy augmentations of a record still classified as
the record's true label. Members are more robust to perturbation, so they score
higher. Uses only the hard label, so it works against endpoints that return no
probabilities.
"""

import typing as t

import numpy as np

from dreadnode.airt._base import sample_input_preview
from dreadnode.airt.membership._base import (
    MembershipInferenceAttack,
    MembershipResult,
    membership_auc,
)
from dreadnode.airt.targets.prediction import PredictionTargetSpec, QueryInput


async def _label_only_scores(
    attack: MembershipInferenceAttack,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Membership score = fraction of noisy augmentations still classified as the
    record's true label. Members are more robust. Uses only the hard label. Emits a
    per-record step trace of the robustness signal as records are scored."""
    if attack.member_labels is None or attack.nonmember_labels is None:
        raise ValueError("label_only membership requires true labels for all records")
    if attack.modality == "text":
        # Label-only robustness augments each record with Gaussian noise, which
        # only defines a numeric feature vector. For text targets use a
        # signal-based method (threshold / entropy / loss / shadow_model).
        raise ValueError(
            "label_only membership requires numeric records; for text targets use "
            "threshold_membership, entropy_membership, or shadow_model_membership"
        )
    records = attack.members + attack.nonmembers
    labels = np.array(attack.member_labels + attack.nonmember_labels)
    is_member = np.array([1] * len(attack.members) + [0] * len(attack.nonmembers))
    scores = np.zeros(len(records))
    for i, rec in enumerate(records):
        base = np.asarray(rec, dtype=np.float64).ravel()
        noised = [base] + [
            base + attack.rng.normal(0, attack.augment_sigma, base.shape)
            for _ in range(attack.n_augment)
        ]
        preds = await attack._query(noised)
        pred_labels = np.array([p.hard_label for p in preds])
        scores[i] = float(np.mean(pred_labels == labels[i]))
        seen = np.arange(i + 1)
        running_auc = (
            membership_auc(scores[seen], is_member[seen])
            if len(np.unique(is_member[seen])) >= 2
            else 0.0
        )
        attack._trace_step(
            i,
            input={"record": sample_input_preview(rec), "augmentations": attack.n_augment},
            output={
                "member_score": round(float(scores[i]), 6),
                "predicted_member": int(scores[i] >= 0.5),
                "true_member": int(is_member[i]),
            },
            metrics={"auc": round(running_auc, 4), "queries": attack._query_count},
        )
    return scores, is_member, labels


async def run(attack: MembershipInferenceAttack) -> MembershipResult:
    scores, is_member, true_labels = await _label_only_scores(attack)
    records = list(attack.members) + list(attack.nonmembers)
    return attack._build_result(scores, is_member, true_labels, records=records)


def label_only_membership(
    target: PredictionTargetSpec,
    members: t.Sequence[QueryInput],
    nonmembers: t.Sequence[QueryInput],
    **kwargs: t.Any,
) -> MembershipInferenceAttack:
    """Label-only membership inference via robustness to input perturbation
    (Choquette-Choo et al.). Works against endpoints that return only a hard label."""
    return MembershipInferenceAttack(
        method="label_only", target=target, members=members, nonmembers=nonmembers, **kwargs
    )
