"""Confidence / entropy / loss thresholding membership inference (Yeom et al. CSF'18).

Query the target once per record and score each by the chosen output signal
(confidence, negative entropy, or negative loss); members score higher because an
over-fit model is more confident on its own training rows. No training - purely
query based. The named ``entropy`` and ``loss`` variants reuse ``run`` here with
their signal pinned.
"""

import typing as t

import numpy as np

from dreadnode.airt.membership._base import (
    MembershipInferenceAttack,
    MembershipResult,
    _preds_to_proba,
    membership_auc,
    membership_scores,
)
from dreadnode.airt.targets.prediction import Prediction, PredictionTargetSpec, QueryInput

#: Emit at most this many per-record step traces so a large campaign does not
#: explode the trace tree (``_trace_step`` also caps internally).
_TRACE_STRIDE_TARGET = 40


def _maybe_art_scores(
    attack: MembershipInferenceAttack, preds: list[Prediction]
) -> np.ndarray | None:
    """ART rule-based black-box membership scores (Yeom et al.), used when ART
    is installed, ``engine`` allows it, the modality is numeric (records are
    already feature vectors), and per-record labels are available. Falls back
    to ``None`` otherwise so the caller uses the native signal."""
    # ART's rule-based attack yields a *binary* per-record verdict (Yeom
    # baseline). The native confidence signal is continuous and gives a
    # smoother ROC, so ART membership is opt-in (engine='art') rather than
    # the 'auto' default. It maps onto the 'confidence' signal only and needs
    # numeric records + per-record labels.
    if attack.engine != "art" or attack.modality == "text":
        return None
    if attack.signal != "confidence":
        return None
    if attack.member_labels is None or attack.nonmember_labels is None:
        return None
    from dreadnode.airt.art_engine import art_membership_scores

    nb_classes = attack.num_classes
    if nb_classes is None:
        vec = next((p.vector for p in preds if p.vector is not None), None)
        nb_classes = len(vec) if vec else int(max(p.hard_label for p in preds)) + 1
    proba = _preds_to_proba(preds, nb_classes)
    n_mem = len(attack.members)
    try:
        members_x = np.asarray([np.asarray(r, dtype=np.float64).ravel() for r in attack.members])
        nonmembers_x = np.asarray(
            [np.asarray(r, dtype=np.float64).ravel() for r in attack.nonmembers]
        )
    except (ValueError, TypeError):
        return None
    return art_membership_scores(
        attack.method,
        members_x,
        nonmembers_x,
        proba[:n_mem],
        proba[n_mem:],
        np.asarray(attack.member_labels),
        np.asarray(attack.nonmember_labels),
        nb_classes,
    )


async def _threshold_scores(
    attack: MembershipInferenceAttack,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    records = attack.members + attack.nonmembers
    labels = None
    if attack.signal == "loss":
        if attack.member_labels is None or attack.nonmember_labels is None:
            raise ValueError("signal='loss' requires member_labels and nonmember_labels")
        labels = attack.member_labels + attack.nonmember_labels
    preds = await attack._query(records)
    is_member = np.array([1] * len(attack.members) + [0] * len(attack.nonmembers))
    true_labels = np.array(labels) if labels is not None else np.array([-1] * len(records))

    art_scores = _maybe_art_scores(attack, preds)
    if art_scores is not None:
        return art_scores, is_member, true_labels

    scores = membership_scores(preds, attack.signal, labels)
    return scores, is_member, true_labels


def _trace_scores(
    attack: MembershipInferenceAttack,
    scores: np.ndarray,
    is_member: np.ndarray,
    records: t.Sequence[QueryInput],
) -> None:
    """Emit per-record step traces of the intermediate membership signal so the
    Traces tab shows the actual scored record and the verdict, not just an index."""
    from dreadnode.airt._base import sample_input_preview

    n = len(scores)
    if n == 0:
        return
    stride = max(1, n // _TRACE_STRIDE_TARGET)
    lo, hi = float(scores.min()), float(scores.max())
    span = (hi - lo) or 1.0
    running_auc = 0.0
    for it, i in enumerate(range(0, n, stride)):
        seen = np.arange(i + 1)
        if len(np.unique(is_member[seen])) >= 2:
            running_auc = membership_auc(scores[seen], is_member[seen])
        member_prob = float((scores[i] - lo) / span)
        attack._trace_step(
            it,
            input={
                "record": sample_input_preview(records[i]) if i < len(records) else None,
                "signal": attack.signal,
            },
            output={
                "member_score": round(float(scores[i]), 6),
                "predicted_member": int(member_prob >= 0.5),
                "true_member": int(is_member[i]),
            },
            metrics={"auc": round(running_auc, 4), "queries": attack._query_count},
        )


async def run(attack: MembershipInferenceAttack) -> MembershipResult:
    scores, is_member, true_labels = await _threshold_scores(attack)
    records = list(attack.members) + list(attack.nonmembers)
    _trace_scores(attack, scores, is_member, records)
    return attack._build_result(scores, is_member, true_labels, records=records)


def threshold_membership(
    target: PredictionTargetSpec,
    members: t.Sequence[QueryInput],
    nonmembers: t.Sequence[QueryInput],
    **kwargs: t.Any,
) -> MembershipInferenceAttack:
    """Confidence/entropy/loss-threshold membership inference (Yeom et al.). No
    training - queries the target and thresholds its output signal."""
    return MembershipInferenceAttack(
        method="threshold", target=target, members=members, nonmembers=nonmembers, **kwargs
    )
