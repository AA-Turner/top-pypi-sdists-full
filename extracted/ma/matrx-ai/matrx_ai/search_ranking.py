"""Pre-read source ranking — the ONE search-result prioritization algorithm.

Which search results deserve a fetch, best first: rank prominence (a curve over
the engine's position) x a small top-rank boost x a cross-query BREADTH bonus x
a capped AUTHORITY prior, normalized to a true 0-100. Pure and config-driven —
no I/O. Moved here from aidream ``research/source_scoring.py`` (2026-10-09) so
the research code path and the ``ai.search.rank_sources`` workflow node rank
with the same code; ``research/source_scoring.py`` keeps the persistence shell.
"""

from __future__ import annotations

from dataclasses import dataclass

from pydantic import BaseModel

# ===========================================================================
# CONFIG — tune these and re-run. This is the whole knob panel.
# ===========================================================================


@dataclass(frozen=True)
class PreReadConfig:
    # --- Authority prior: a noisy pre-read signal that REFINES, never dominates.
    authority_boost: float = 0.30  # max +30% from authority
    min_authority_prior: float = 0.90
    max_authority_prior: float = 1.30
    spam_authority_threshold: int = 20  # authority < this → prior pinned to min

    # --- Rank prominence blend: avg rewards consistency, best rewards one strong
    #     query. avg weighted higher so a single lucky #1 doesn't dominate.
    rank_blend_average: float = 0.65
    rank_blend_best: float = 0.35

    # --- Top-rank "respect" boost (small; breaks close calls, doesn't overpower).
    top_rank_boost_1: float = 1.20
    top_rank_boost_2_3: float = 1.15
    top_rank_boost_4_5: float = 1.10
    top_rank_boost_6_10: float = 1.03
    top_rank_boost_default: float = 1.00

    # --- Breadth: a BONUS for covering more of the topic, never a divisor.
    #
    # This replaced `coverage = matched / total_topic_keywords` (see the module
    # docstring). One keyword match is the baseline (multiplier 1.0); the bonus
    # scales to its maximum at `breadth_full_at` matched keywords and stops.
    # Nothing here reads the topic's keyword COUNT, which is what makes the
    # score scale-free and stable when a keyword is added.
    breadth_boost: float = 0.60  # a fully-broad source is worth 1.6x a single-keyword one
    breadth_full_at: float = 5.0  # matched keyword weight at which the bonus maxes out

    # --- Small-site protection: a niche site that ranks well across the topic
    #     must not be buried by a merely-medium authority prior.
    protect_breadth_min: float = 2.0  # matched keyword weight, was a coverage fraction
    protect_rank_prominence_min: float = 0.60
    protect_authority_min: int = 35
    protect_authority_prior_floor: float = 1.05


DEFAULT_PRE_READ_CONFIG = PreReadConfig()


def _max_score_product(cfg: PreReadConfig) -> float:
    """The best product any source can achieve under ``cfg`` — the normalizer.

    Every factor's maximum is reachable together: a source ranked #1 for
    ``breadth_full_at`` keywords with authority 100 scores exactly 100. That
    matters — a scale whose top is unreachable reads as broken.
    """
    # The authority prior's real ceiling is what the FORMULA can produce, not the
    # clamp bound: `1 + authority_boost` at authority 100, clamped, and possibly
    # lifted by the small-site protection floor. Using `max_authority_prior`
    # directly looks right only because the two coincide at the default 1.30 —
    # raise the clamp without raising the boost and every score silently shrinks,
    # putting 100 out of reach again.
    max_authority_prior = max(
        _clamp(1.0 + cfg.authority_boost, cfg.min_authority_prior, cfg.max_authority_prior),
        cfg.protect_authority_prior_floor,
    )
    return (
        1.0  # rank_prominence: best + average both at rank 1
        * cfg.top_rank_boost_1
        * (1.0 + cfg.breadth_boost)
        * max_authority_prior
    )


# Google rank → 0-1 prominence. Steep early (top-3 matter a lot), long flat tail.
# A list of (max_rank_inclusive, score) so it's data, not branches — easy to tune.
RANK_CURVE: tuple[tuple[int, float], ...] = (
    (1, 1.00),
    (2, 0.90),
    (3, 0.84),
    (5, 0.75),
    (10, 0.60),
    (20, 0.40),
    (50, 0.20),
    (100, 0.08),
)
RANK_CURVE_TAIL = 0.03  # rank > 100


def rank_to_score(rank: int) -> float:
    for max_rank, score in RANK_CURVE:
        if rank <= max_rank:
            return score
    return RANK_CURVE_TAIL


# ===========================================================================
# Inputs / outputs
# ===========================================================================


@dataclass(frozen=True)
class KeywordRanking:
    """One (keyword, weight, google_rank) row for a source — i.e. the source
    appeared at ``google_rank`` for ``keyword`` (weight defaults to 1.0)."""

    keyword: str
    keyword_weight: float
    google_rank: int


class PreReadScoreBreakdown(BaseModel):
    """The full, inspectable decomposition — persisted so the algorithm is
    auditable per-source (every multiplier is visible)."""

    pre_read_score: float  # NORMALIZED 0-100 — the sort key AND the displayed value
    pre_read_score_display: int  # round(pre_read_score); never exceeds 100
    raw_product: float  # the un-normalized product, for auditing the factors
    breadth_multiplier: float  # replaced keyword_coverage_score as the score input
    rank_prominence_score: float
    top_rank_boost: float
    authority_prior: float
    authority_score: int
    matched_keyword_count: int
    matched_keyword_weight: float
    best_google_rank: int
    average_google_rank: float
    # DISPLAY ONLY — "this source covers 3 of the topic's 8 keywords". Kept
    # because it is genuinely useful to a human reading the table, but it is NOT
    # an input to the score any more: dividing by the topic's keyword count is
    # exactly what made the old score un-normalizable and unstable.
    keyword_coverage_score: float
    topic_keyword_weight: float


def _clamp(v: float, lo: float, hi: float) -> float:
    return max(lo, min(hi, v))


def _top_rank_boost(best_google_rank: int, cfg: PreReadConfig) -> float:
    # best_google_rank <= 0 means "no ranking data" → no boost.
    if best_google_rank == 1:
        return cfg.top_rank_boost_1
    if 2 <= best_google_rank <= 3:
        return cfg.top_rank_boost_2_3
    if 4 <= best_google_rank <= 5:
        return cfg.top_rank_boost_4_5
    if 6 <= best_google_rank <= 10:
        return cfg.top_rank_boost_6_10
    return cfg.top_rank_boost_default


def compute_pre_read_score(
    keyword_rankings: list[KeywordRanking],
    total_keyword_weight: float,
    authority_score: int | None,
    config: PreReadConfig = DEFAULT_PRE_READ_CONFIG,
) -> PreReadScoreBreakdown:
    """Pre-read priority for ONE source.

    ``total_keyword_weight`` is the sum of weights over ALL of the topic's
    keywords (the breadth denominator) — pass it in so coverage is a true
    fraction of the topic, robust to any keyword count.
    """
    cfg = config
    auth = int(authority_score) if authority_score is not None else 0

    # --- Step 1: breadth BONUS (absolute, never a fraction of the topic) ------
    # `total_keyword_weight` is used ONLY to report the coverage statistic; it
    # must never re-enter the score. See the module docstring for why.
    matched_weight = sum(kr.keyword_weight for kr in keyword_rankings)
    breadth_span = max(cfg.breadth_full_at - 1.0, 1e-9)
    breadth = 1.0 + cfg.breadth_boost * _clamp((matched_weight - 1.0) / breadth_span, 0.0, 1.0)

    # --- Step 2: rank prominence (weighted avg + best blend) ------------------
    if keyword_rankings:
        scored = [(rank_to_score(kr.google_rank), kr.keyword_weight) for kr in keyword_rankings]
        wsum = sum(w for _, w in scored) or 1.0
        avg_rank_score = sum(s * w for s, w in scored) / wsum
        best_rank_score = max(s for s, _ in scored)
        best_google_rank = min(kr.google_rank for kr in keyword_rankings)
        average_google_rank = sum(kr.google_rank for kr in keyword_rankings) / len(keyword_rankings)
    else:
        avg_rank_score = best_rank_score = 0.0
        best_google_rank = 0
        average_google_rank = 0.0
    rank_prominence = (
        cfg.rank_blend_average * avg_rank_score + cfg.rank_blend_best * best_rank_score
    )

    # --- Step 3: top-rank boost (small) --------------------------------------
    top_boost = _top_rank_boost(best_google_rank, cfg)

    # --- Step 4: capped authority prior --------------------------------------
    authority_prior = 1.0 + cfg.authority_boost * (auth / 100.0)
    authority_prior = _clamp(authority_prior, cfg.min_authority_prior, cfg.max_authority_prior)
    if auth < cfg.spam_authority_threshold:
        authority_prior = cfg.min_authority_prior  # spam / low-quality penalty

    # --- Step 5: small-site protection ---------------------------------------
    # Gated on ABSOLUTE matched weight now, not a coverage fraction: "ranks well
    # across several of the topic's keywords" means the same thing whether the
    # topic has 3 keywords or 30.
    if (
        matched_weight >= cfg.protect_breadth_min
        and rank_prominence >= cfg.protect_rank_prominence_min
        and auth >= cfg.protect_authority_min
    ):
        authority_prior = max(authority_prior, cfg.protect_authority_prior_floor)

    # --- Final: normalize to a true 0-100 ------------------------------------
    raw_product = rank_prominence * top_boost * breadth * authority_prior
    pre_read = _clamp(raw_product / _max_score_product(cfg) * 100.0, 0.0, 100.0)

    # Reported for humans only — NOT an input. A source with no keyword links
    # has no coverage to report rather than a fabricated zero-denominator value.
    denom = total_keyword_weight if total_keyword_weight > 0 else 1.0
    coverage = _clamp(matched_weight / denom, 0.0, 1.0)

    return PreReadScoreBreakdown(
        pre_read_score=pre_read,
        pre_read_score_display=round(pre_read),
        raw_product=round(raw_product, 6),
        breadth_multiplier=round(breadth, 4),
        rank_prominence_score=round(rank_prominence, 4),
        top_rank_boost=top_boost,
        authority_prior=round(authority_prior, 4),
        authority_score=auth,
        matched_keyword_count=len(keyword_rankings),
        matched_keyword_weight=round(matched_weight, 4),
        best_google_rank=best_google_rank,
        average_google_rank=round(average_google_rank, 2),
        keyword_coverage_score=round(coverage, 4),
        topic_keyword_weight=round(float(total_keyword_weight), 4),
    )
