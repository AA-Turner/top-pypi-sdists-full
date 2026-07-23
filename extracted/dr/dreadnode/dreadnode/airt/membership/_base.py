"""Shared base for the membership-inference attacks.

Given records known to be members (in the target's training set) and non-members,
these attacks decide membership from the target's outputs and report how well
members separate from non-members - the concrete training-data privacy leak.

Each concrete method lives in its own module under this package (``threshold``,
``label_only``, ``lira``, ``shadow_model``, ``entropy``, ``loss``) as a
``run(attack)`` coroutine plus a public factory function. Each module scores every
record, then hands off to :meth:`MembershipInferenceAttack._build_result` for the
shared metric roll-up (AUC, TPR at fixed FPR, advantage, ROC, distributions).
:class:`MembershipInferenceAttack` holds the shared state (query counting, shadow
plumbing, per-step tracing, the result builder) and dispatches to the selected
module's ``run``.
"""

import typing as t
from dataclasses import dataclass, field

import numpy as np

from dreadnode.airt._base import BlackBoxAttack, sample_input_preview
from dreadnode.airt.targets.prediction import (
    Prediction,
    PredictionTargetSpec,
    QueryInput,
)

MembershipMethod = t.Literal["threshold", "label_only", "lira", "shadow_model", "entropy", "loss"]
MembershipSignal = t.Literal["confidence", "entropy", "loss"]


def _preds_to_proba(preds: t.Sequence[Prediction], num_classes: int) -> np.ndarray:
    """Stack predictions into an ``(n, num_classes)`` probability matrix, one-hotting
    hard labels when a prediction carries no soft vector."""
    rows: list[list[float]] = []
    for p in preds:
        vec = p.vector
        if vec is not None and len(vec) == num_classes:
            rows.append([float(v) for v in vec])
        else:
            one_hot = [0.0] * num_classes
            label = p.hard_label
            if isinstance(label, (int, np.integer)) and 0 <= int(label) < num_classes:
                one_hot[int(label)] = 1.0
            rows.append(one_hot)
    return np.asarray(rows, dtype=np.float64)


# --------------------------------------------------------------------------- #
# Pure metric helpers
# --------------------------------------------------------------------------- #
def membership_auc(scores: np.ndarray, is_member: np.ndarray) -> float:
    """ROC AUC of membership scores (higher score = more member-like)."""
    from sklearn.metrics import roc_auc_score

    if len(np.unique(is_member)) < 2:
        return 0.5
    return float(roc_auc_score(is_member, scores))


def tpr_at_fpr(scores: np.ndarray, is_member: np.ndarray, target_fpr: float) -> float:
    """True-positive rate at the largest achievable FPR <= ``target_fpr``."""
    from sklearn.metrics import roc_curve

    if len(np.unique(is_member)) < 2:
        return 0.0
    fpr, tpr, _ = roc_curve(is_member, scores)
    allowed = fpr <= target_fpr
    return float(np.max(tpr[allowed])) if allowed.any() else 0.0


def membership_advantage(scores: np.ndarray, is_member: np.ndarray) -> tuple[float, float]:
    """Yeom membership advantage = max_threshold (TPR - FPR), plus that threshold."""
    from sklearn.metrics import roc_curve

    if len(np.unique(is_member)) < 2:
        return 0.0, 0.0
    fpr, tpr, thr = roc_curve(is_member, scores)
    idx = int(np.argmax(tpr - fpr))
    return float(tpr[idx] - fpr[idx]), float(thr[idx])


def _subsample(values: np.ndarray, n: int = 200) -> list[float]:
    """Up to *n* values (evenly strided) as plain floats, for a distribution chart."""
    if len(values) <= n:
        return [float(v) for v in values]
    idx = np.linspace(0, len(values) - 1, n).astype(int)
    return [float(v) for v in values[idx]]


def roc_points(
    scores: np.ndarray, is_member: np.ndarray, max_points: int = 100
) -> list[list[float]]:
    """Sub-sampled ROC curve as ``[[fpr, tpr], ...]`` for charting."""
    from sklearn.metrics import roc_curve

    if len(np.unique(is_member)) < 2:
        return []
    fpr, tpr, _ = roc_curve(is_member, scores)
    if len(fpr) > max_points:
        idx = np.linspace(0, len(fpr) - 1, max_points).astype(int)
        fpr, tpr = fpr[idx], tpr[idx]
    return [[float(f), float(t)] for f, t in zip(fpr, tpr, strict=True)]


# --------------------------------------------------------------------------- #
# Signal extraction
# --------------------------------------------------------------------------- #
def _confidence(pred: Prediction) -> float:
    vec = pred.vector
    return float(np.max(vec)) if vec else 0.0


def _neg_entropy(pred: Prediction) -> float:
    vec = pred.vector
    if not vec:
        return 0.0
    p = np.clip(np.asarray(vec), 1e-12, 1.0)
    return float(np.sum(p * np.log(p)))  # = -entropy; higher (less negative) = confident


def _neg_loss(pred: Prediction, true_label: int) -> float:
    vec = pred.vector
    if not vec or true_label >= len(vec):
        return 0.0
    return float(np.log(np.clip(vec[true_label], 1e-12, 1.0)))  # -cross-entropy loss


def membership_scores(
    preds: t.Sequence[Prediction], signal: MembershipSignal, labels: t.Sequence[int] | None
) -> np.ndarray:
    """Per-record membership score (higher = more member-like)."""
    if signal == "confidence":
        return np.array([_confidence(p) for p in preds])
    if signal == "entropy":
        return np.array([_neg_entropy(p) for p in preds])
    if labels is None:
        raise ValueError("signal='loss' requires per-record true labels")
    return np.array([_neg_loss(p, int(y)) for p, y in zip(preds, labels, strict=True)])


# --------------------------------------------------------------------------- #
# Result
# --------------------------------------------------------------------------- #
@dataclass
class MembershipResult:
    method: str
    signal: str
    auc: float
    tpr_at_1pct_fpr: float
    tpr_at_01pct_fpr: float
    advantage: float
    balanced_accuracy: float
    #: Member/non-member classification quality at the advantage-optimal threshold.
    attack_accuracy: float
    attack_precision: float
    attack_recall: float
    records_reidentified: int
    query_count: int
    per_class_auc: dict[str, float]
    roc: list[list[float]]
    #: {"members": [...scores], "nonmembers": [...scores]} for the distribution histogram.
    score_distribution: dict[str, list[float]]
    #: Top-N most-confidently-flagged records: {rank, member_prob, true_member}.
    leaked_records: list[dict[str, t.Any]]
    #: A sample of real (input -> prediction) pairs from the query campaign.
    query_samples: list[dict[str, t.Any]] = field(default_factory=list)

    @property
    def metrics_detail(self) -> dict[str, t.Any]:
        return {
            "per_class_auc": self.per_class_auc,
            "roc": self.roc,
            "score_distribution": self.score_distribution,
            "leaked_records": self.leaked_records,
            "advantage": round(self.advantage, 4),
            "balanced_accuracy": round(self.balanced_accuracy, 4),
            "attack_accuracy": round(self.attack_accuracy, 4),
            "attack_precision": round(self.attack_precision, 4),
            "attack_recall": round(self.attack_recall, 4),
            "query_samples": self.query_samples,
        }


# --------------------------------------------------------------------------- #
# Attack
# --------------------------------------------------------------------------- #
class MembershipInferenceAttack(BlackBoxAttack):
    """A configured membership-inference run. ``await attack.run()`` queries the
    target on members + non-members and returns a :class:`MembershipResult`."""

    attack_domain = "membership_inference"
    default_goal = "Determine whether records were in the model's training set"
    default_goal_category = "membership_inference"

    def __init__(
        self,
        *,
        target: PredictionTargetSpec,
        method: MembershipMethod,
        members: t.Sequence[QueryInput],
        nonmembers: t.Sequence[QueryInput],
        member_labels: t.Sequence[int] | None = None,
        nonmember_labels: t.Sequence[int] | None = None,
        signal: MembershipSignal = "confidence",
        n_augment: int = 8,
        augment_sigma: float = 0.05,
        n_shadow: int = 8,
        modality: str = "tabular",
        engine: str = "auto",
        num_classes: int | None = None,
        seed: int | None = None,
        airt_assessment_id: str | None = None,
        airt_target_model: str | None = None,
        airt_goal: str | None = None,
        airt_goal_category: str | None = None,
    ) -> None:
        super().__init__(
            target=target,
            modality=modality,
            seed=seed,
            airt_assessment_id=airt_assessment_id,
            airt_target_model=airt_target_model,
            airt_goal=airt_goal,
            airt_goal_category=airt_goal_category,
        )
        self.method = method
        self.members = list(members)
        self.nonmembers = list(nonmembers)
        self.member_labels = list(member_labels) if member_labels is not None else None
        self.nonmember_labels = list(nonmember_labels) if nonmember_labels is not None else None
        # entropy / loss are named threshold variants - pin the signal to match.
        self.signal = "entropy" if method == "entropy" else "loss" if method == "loss" else signal
        self.n_augment = n_augment
        self.augment_sigma = augment_sigma
        self.n_shadow = n_shadow
        self.engine = engine
        self.num_classes = num_classes

    # -- shadow-model plumbing shared by lira / shadow_model --------------- #
    def _feat(self, records: t.Sequence[t.Any]) -> np.ndarray:
        """Feature matrix for training shadow models: raw vectors for numeric
        records, a TF-IDF embedding for text."""
        if self.modality == "text":
            from sklearn.feature_extraction.text import TfidfVectorizer

            corpus = [str(r) for r in (self.members + self.nonmembers)]
            vec = TfidfVectorizer(max_features=1000).fit(corpus)
            return np.asarray(vec.transform([str(r) for r in records]).toarray(), dtype=np.float64)
        return np.asarray([np.asarray(r, dtype=np.float64).ravel() for r in records])

    def _fit_shadow(self, x: np.ndarray, y: np.ndarray) -> t.Any:
        from sklearn.linear_model import LogisticRegression

        return LogisticRegression(max_iter=500).fit(x, y)

    async def _target_setup(self) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Query the target once for every record and return (features, true
        labels, target confidence on the true label, is_member) - the shared basis
        for the shadow-model attacks. Requires per-record labels."""
        if self.member_labels is None or self.nonmember_labels is None:
            raise ValueError("shadow-model membership requires true labels for all records")
        records = self.members + self.nonmembers
        y = np.array(self.member_labels + self.nonmember_labels)
        is_member = np.array([1] * len(self.members) + [0] * len(self.nonmembers))
        preds = await self._query(records)
        nb = self.num_classes or (
            len(next((p.vector for p in preds if p.vector is not None), [0, 0]))
        )
        proba = _preds_to_proba(preds, nb)
        target_conf = np.array([proba[i, y[i]] for i in range(len(records))])
        return self._feat(records), y, target_conf, is_member

    # -- result roll-up ---------------------------------------------------- #
    def _build_result(
        self,
        scores: np.ndarray,
        is_member: np.ndarray,
        true_labels: np.ndarray,
        records: t.Sequence[QueryInput] | None = None,
    ) -> MembershipResult:
        """Turn per-record membership scores into the shared metric roll-up (AUC,
        TPR at fixed FPR, advantage, per-class AUC, ROC, score distribution, and
        the top-N leaked records). ``records`` (in score order) lets each leaked
        row carry the actual record and a correct/false-positive outcome."""
        auc = membership_auc(scores, is_member)
        adv, best_thr = membership_advantage(scores, is_member)
        # Balanced accuracy at the advantage-optimal threshold.
        pred_member = (scores >= best_thr).astype(int)
        tp = int(np.sum((pred_member == 1) & (is_member == 1)))
        tn = int(np.sum((pred_member == 0) & (is_member == 0)))
        n_pos, n_neg = int(np.sum(is_member == 1)), int(np.sum(is_member == 0))
        balanced_acc = 0.5 * (tp / max(n_pos, 1) + tn / max(n_neg, 1))
        # Member/non-member classification quality at the same operating point.
        fp = int(np.sum((pred_member == 1) & (is_member == 0)))
        attack_accuracy = (tp + tn) / max(n_pos + n_neg, 1)
        attack_precision = tp / max(tp + fp, 1)
        attack_recall = tp / max(n_pos, 1)
        tpr_1 = tpr_at_fpr(scores, is_member, 0.01)
        # records re-identified = members caught at the 1%-FPR operating point.
        records_reid = round(tpr_1 * n_pos)

        per_class_auc: dict[str, float] = {}
        if (true_labels >= 0).any():
            for c in np.unique(true_labels[true_labels >= 0]):
                mask = true_labels == c
                if len(np.unique(is_member[mask])) == 2:
                    per_class_auc[str(int(c))] = membership_auc(scores[mask], is_member[mask])

        # Member vs non-member score distribution (sub-sampled for the histogram).
        score_distribution = {
            "members": _subsample(scores[is_member == 1]),
            "nonmembers": _subsample(scores[is_member == 0]),
        }
        # Top-N most-confidently-flagged records (min-max normalised membership
        # prob). Each row carries the attack's verdict (predicted_member at the
        # advantage-optimal threshold) and an outcome so a highly-scored
        # non-member reads as a false positive, not a re-identification.
        lo, hi = float(scores.min()), float(scores.max())
        span = (hi - lo) or 1.0
        order = np.argsort(scores)[::-1][:20]
        leaked_records = []
        for rank, i in enumerate(order):
            pred_member = int(scores[i] >= best_thr)
            true_m = int(is_member[i])
            if pred_member and true_m:
                outcome = "re-identified"
            elif pred_member and not true_m:
                outcome = "false positive"
            elif not pred_member and true_m:
                outcome = "missed member"
            else:
                outcome = "correct rejection"
            row: dict[str, t.Any] = {
                "rank": rank + 1,
                "member_prob": round(float((scores[i] - lo) / span), 4),
                "predicted_member": pred_member,
                "true_member": true_m,
                "outcome": outcome,
            }
            if records is not None and i < len(records):
                # Longer preview than the default so text records are readable
                # rather than cut at 60 chars.
                row["record"] = sample_input_preview(records[i], n=240)
            leaked_records.append(row)

        return MembershipResult(
            method=self.method,
            signal=self.signal if self.method == "threshold" else "label_only",
            auc=auc,
            tpr_at_1pct_fpr=tpr_1,
            tpr_at_01pct_fpr=tpr_at_fpr(scores, is_member, 0.001),
            advantage=adv,
            balanced_accuracy=balanced_acc,
            attack_accuracy=attack_accuracy,
            attack_precision=attack_precision,
            attack_recall=attack_recall,
            records_reidentified=records_reid,
            query_count=self._query_count,
            per_class_auc=per_class_auc,
            roc=roc_points(scores, is_member),
            score_distribution=score_distribution,
            leaked_records=leaked_records,
            query_samples=self._query_samples,
        )

    # -- run scaffold ------------------------------------------------------ #
    @property
    def _attack_name(self) -> str:
        return f"{self.method}_membership"

    def _span_attributes(self, result: MembershipResult) -> dict[str, t.Any]:
        from dreadnode.tracing.constants import (
            AIRT_ATTRIBUTE_BEST_SCORE,
            AIRT_ATTRIBUTE_MEMBERSHIP_ADVANTAGE,
            AIRT_ATTRIBUTE_MEMBERSHIP_AUC,
            AIRT_ATTRIBUTE_MEMBERSHIP_BALANCED_ACC,
            AIRT_ATTRIBUTE_MEMBERSHIP_METHOD,
            AIRT_ATTRIBUTE_MEMBERSHIP_TPR_AT_01FPR,
            AIRT_ATTRIBUTE_MEMBERSHIP_TPR_AT_1FPR,
            AIRT_ATTRIBUTE_QUERY_COUNT,
            AIRT_ATTRIBUTE_RECORDS_REIDENTIFIED,
        )

        return {
            AIRT_ATTRIBUTE_BEST_SCORE: result.auc,
            AIRT_ATTRIBUTE_MEMBERSHIP_AUC: result.auc,
            AIRT_ATTRIBUTE_MEMBERSHIP_TPR_AT_1FPR: result.tpr_at_1pct_fpr,
            AIRT_ATTRIBUTE_MEMBERSHIP_TPR_AT_01FPR: result.tpr_at_01pct_fpr,
            AIRT_ATTRIBUTE_MEMBERSHIP_ADVANTAGE: result.advantage,
            AIRT_ATTRIBUTE_MEMBERSHIP_BALANCED_ACC: result.balanced_accuracy,
            AIRT_ATTRIBUTE_RECORDS_REIDENTIFIED: result.records_reidentified,
            AIRT_ATTRIBUTE_MEMBERSHIP_METHOD: result.method,
            AIRT_ATTRIBUTE_QUERY_COUNT: result.query_count,
        }

    #: method -> the module under this package that implements it.
    _STRATEGY_MODULES: t.ClassVar[dict[str, str]] = {
        "threshold": "threshold",
        "entropy": "entropy",
        "loss": "loss",
        "label_only": "label_only",
        "lira": "lira",
        "shadow_model": "shadow_model",
    }

    async def _execute(self) -> MembershipResult:
        import importlib

        n_records = len(self.members) + len(self.nonmembers)
        with self._phase("query target + score records", records=n_records, method=self.method):
            module = importlib.import_module(
                f"dreadnode.airt.membership.{self._STRATEGY_MODULES[self.method]}"
            )
            return await module.run(self)
