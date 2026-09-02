"""Scoring Engine (FEAT-190).

Pure numpy scoring engine (spec Module 3). ``ScoringEngine.score()`` takes a
pre-built feature matrix and a frozen ``ScoringPolicy`` and produces a
deterministic, byte-identical ``ScoreResult`` for identical inputs (spec D1,
AC1). No I/O, no RNG, no clock — the engine does NOT call extractors; it
only aggregates already-extracted raw feature values.

Only ``hashlib`` and ``numpy`` are imported here (plus the contract types
from ``models.py``) — no scipy, no h3 (spec AC11).
"""
import hashlib
from typing import Any, Optional

import numpy as np

from .models import Direction, ScoringPolicy, ScoreResult, ValueFunction

# Small epsilon to keep weighted_geomean numerically stable when a
# criterion's utility is exactly 0 (spec: "Float precision" gotcha).
_GEOMEAN_EPS = 1e-10


class ScoringEngine:
    """Pure numpy scoring engine. No I/O, no RNG, no clock."""

    def score(
        self,
        feature_matrix: np.ndarray,
        policy: ScoringPolicy,
        filter_matrix: Optional[np.ndarray] = None,
        candidate_ids: Optional[list[str]] = None,
    ) -> ScoreResult:
        """Score every candidate against the policy.

        Args:
            feature_matrix: Raw feature values, shape ``(N, len(policy.criteria))``.
                Column ``i`` holds the raw value for ``policy.criteria[i]``.
            policy: Frozen scoring policy.
            filter_matrix: Raw feature values for hard filters, shape
                ``(N, len(policy.filters))``. Column ``i`` holds the raw value
                for ``policy.filters[i]``. May be ``None`` if the policy has
                no filters.
            candidate_ids: Optional candidate identifiers, carried through to
                the result unchanged.

        Returns:
            A ``ScoreResult`` with per-candidate total scores, per-criterion
            breakdown, the hard-filter mask, and the policy provenance hash.
        Raises:
            ValueError: if ``policy.criteria`` is empty, criteria weights sum
                to a non-positive value, or ``feature_matrix``/``filter_matrix``
                shapes are inconsistent with the policy. Callers going through
                ``SweetSpotScorer`` never hit these (the facade always builds
                consistent matrices); they guard direct ``ScoringEngine`` API
                use against opaque numpy broadcasting/indexing errors.
        """
        if not policy.criteria:
            raise ValueError(
                "ScoringPolicy.criteria is empty — cannot compute a score "
                "with zero criteria."
            )

        n_candidates = feature_matrix.shape[0]
        if feature_matrix.shape[1] != len(policy.criteria):
            raise ValueError(
                f"feature_matrix has {feature_matrix.shape[1]} columns but "
                f"policy has {len(policy.criteria)} criteria — columns must "
                "align 1:1 with policy.criteria, in order."
            )
        if policy.filters:
            if filter_matrix is None:
                raise ValueError(
                    f"policy has {len(policy.filters)} hard filter(s) but "
                    "filter_matrix=None was passed — filter feature values "
                    "must be supplied when a policy declares filters."
                )
            if filter_matrix.shape[0] != n_candidates:
                raise ValueError(
                    f"filter_matrix has {filter_matrix.shape[0]} rows but "
                    f"feature_matrix has {n_candidates} — both must have one "
                    "row per candidate."
                )
            if filter_matrix.shape[1] != len(policy.filters):
                raise ValueError(
                    f"filter_matrix has {filter_matrix.shape[1]} columns but "
                    f"policy has {len(policy.filters)} filters — columns must "
                    "align 1:1 with policy.filters, in order."
                )

        # 1. Hard filters — boolean mask applied BEFORE scoring (spec D5, AC4).
        filtered_out = self._apply_hard_filters(filter_matrix, policy, n_candidates)

        # 2. Value functions → utility matrix, one column per criterion.
        utilities = np.zeros_like(feature_matrix, dtype=float)
        for col_idx, criterion in enumerate(policy.criteria):
            raw_col = feature_matrix[:, col_idx]
            utilities[:, col_idx] = self._apply_value_function(
                raw_col, criterion.value_fn, criterion.direction
            )

        # 3. Normalize weights to sum=1 (spec D12).
        raw_weights = np.array([c.weight for c in policy.criteria], dtype=float)
        weight_sum = raw_weights.sum()
        if weight_sum <= 0:
            raise ValueError(
                "Criteria weights must sum to a positive value; got "
                f"weights={raw_weights.tolist()} (sum={weight_sum}). "
                "A zero/negative weight sum would silently divide by zero "
                "and produce NaN scores for every candidate."
            )
        weights = raw_weights / weight_sum

        # 4-5. Aggregate.
        if policy.aggregation == "weighted_mean":
            scores = self._weighted_mean(utilities, weights)
        else:
            scores = self._weighted_geomean(utilities, weights)

        # Hard-filtered candidates are excluded from ranking regardless of
        # their other criteria (spec D5, AC4).
        scores = np.array(scores, dtype=float)
        scores[filtered_out] = 0.0

        # 6. Per-criterion breakdown for auditability.
        breakdown = self._build_breakdown(
            feature_matrix, utilities, weights, policy, filtered_out
        )

        # 7. Policy provenance hash (spec D15, OQ5→YES, AC10).
        policy_hash = hashlib.sha256(
            policy.model_dump_json().encode()
        ).hexdigest()

        return ScoreResult(
            scores=scores,
            breakdown=breakdown,
            filtered_out=filtered_out,
            policy_hash=policy_hash,
            candidate_ids=candidate_ids,
        )

    def _apply_value_function(
        self, raw: np.ndarray, vf: ValueFunction, direction: Direction
    ) -> np.ndarray:
        """Map a raw feature column to utility in [0,100].

        ``threshold`` and ``gaussian_decay`` are self-describing (their
        shape already encodes "which direction is good" via the configured
        bands/center), so ``direction`` is not applied to them. ``linear``
        and ``sigmoid`` are inverted when ``direction == "lower_better"``.
        """
        raw = np.asarray(raw, dtype=float)

        if vf.kind == "threshold":
            return self._threshold(raw, vf)
        if vf.kind == "linear":
            utility = np.clip(raw, 0.0, 100.0)
            if direction == "lower_better":
                utility = 100.0 - utility
            return utility
        if vf.kind == "sigmoid":
            center = vf.center if vf.center is not None else 0.0
            steepness = vf.steepness if vf.steepness is not None else 1.0
            utility = 100.0 / (1.0 + np.exp(-steepness * (raw - center)))
            if direction == "lower_better":
                utility = 100.0 - utility
            return utility
        if vf.kind == "gaussian_decay":
            return self._gaussian_decay(raw, vf)
        if vf.kind == "quantile":
            return self._quantile(raw, direction)
        raise ValueError(f"Unknown ValueFunction kind: {vf.kind!r}")

    @staticmethod
    def _threshold(raw: np.ndarray, vf: ValueFunction) -> np.ndarray:
        """Non-monotone threshold-band value function (spec D3/AC3).

        ``bands`` is ``[(upper_bound, utility), ...]`` sorted ascending by
        ``upper_bound``. For each raw value, use the utility of the first
        (smallest) band whose ``upper_bound >= raw``. If ``raw`` exceeds
        every band's ``upper_bound``, utility is 0.
        """
        bands = vf.bands or []
        sorted_bands = sorted(bands, key=lambda b: b[0])
        utility = np.zeros_like(raw, dtype=float)
        for i, value in np.ndenumerate(raw):
            band_utility = 0.0
            for upper_bound, band_value in sorted_bands:
                if value <= upper_bound:
                    band_utility = band_value
                    break
            utility[i] = band_utility
        return utility

    @staticmethod
    def _gaussian_decay(raw: np.ndarray, vf: ValueFunction) -> np.ndarray:
        """Gaussian decay value function, peak at ``center``, width ``steepness``."""
        center = vf.center if vf.center is not None else 0.0
        steepness = vf.steepness if vf.steepness is not None else 1.0
        utility = 100.0 * np.exp(-((raw - center) ** 2) / (2.0 * steepness ** 2))
        return np.clip(utility, 0.0, 100.0)

    @staticmethod
    def _quantile(raw: np.ndarray, direction: Direction) -> np.ndarray:
        """Percentile-rank value function scaled to [0,100] across candidates."""
        n = raw.shape[0]
        if n <= 1:
            return np.full_like(raw, 100.0, dtype=float)
        ranks = raw.argsort().argsort().astype(float)
        utility = ranks / (n - 1) * 100.0
        if direction == "lower_better":
            utility = 100.0 - utility
        return utility

    @staticmethod
    def _apply_hard_filters(
        filter_matrix: Optional[np.ndarray],
        policy: ScoringPolicy,
        n_candidates: int,
    ) -> np.ndarray:
        """Boolean mask: True where a candidate fails ANY hard filter (spec D5)."""
        if not policy.filters:
            return np.zeros(n_candidates, dtype=bool)

        filtered_out = np.zeros(n_candidates, dtype=bool)
        for idx, hard_filter in enumerate(policy.filters):
            raw_col = filter_matrix[:, idx]
            if hard_filter.op == "lte":
                passes = raw_col <= hard_filter.value
            else:  # "gte"
                passes = raw_col >= hard_filter.value
            filtered_out |= ~passes
        return filtered_out

    @staticmethod
    def _weighted_mean(utilities: np.ndarray, weights: np.ndarray) -> np.ndarray:
        """Weighted arithmetic mean of per-criterion utilities (spec D4)."""
        return np.average(utilities, axis=1, weights=weights)

    @staticmethod
    def _weighted_geomean(utilities: np.ndarray, weights: np.ndarray) -> np.ndarray:
        """Weighted geometric mean of per-criterion utilities (spec D4).

        Computed in log-space for numerical stability. A single criterion at
        utility 0 collapses the geomean toward 0 (spec AC5), unlike the
        arithmetic mean.
        """
        log_utilities = np.log(utilities + _GEOMEAN_EPS)
        weighted_log_sum = np.sum(weights[np.newaxis, :] * log_utilities, axis=1)
        return np.exp(weighted_log_sum)

    @staticmethod
    def _build_breakdown(
        feature_matrix: np.ndarray,
        utilities: np.ndarray,
        weights: np.ndarray,
        policy: ScoringPolicy,
        filtered_out: np.ndarray,
    ) -> list[dict[str, Any]]:
        """Build a per-candidate, per-criterion breakdown for auditability.

        ``contribution = normalized_weight * utility`` so that, for
        ``weighted_mean``, ``sum(contribution for all criteria) == total``
        (spec AC6) — including for hard-filtered candidates, whose
        ``contribution`` is zeroed here to stay consistent with
        ``scores[filtered_out] = 0.0``. ``raw``/``utility`` are still
        reported (not zeroed) for filtered candidates so an auditor can see
        what values led to the veto; only ``contribution`` (which feeds the
        AC6 reconstruction check) is forced to 0.
        """
        n_candidates = utilities.shape[0]
        breakdown: list[dict[str, Any]] = []
        for row in range(n_candidates):
            row_is_filtered = bool(filtered_out[row])
            row_breakdown: dict[str, Any] = {}
            for col_idx, criterion in enumerate(policy.criteria):
                raw = float(feature_matrix[row, col_idx])
                utility = float(utilities[row, col_idx])
                weight = float(weights[col_idx])
                contribution = 0.0 if row_is_filtered else weight * utility
                row_breakdown[criterion.name] = {
                    "raw": raw,
                    "utility": utility,
                    "weight": weight,
                    "contribution": contribution,
                }
            breakdown.append(row_breakdown)
        return breakdown
