"""
SweetSpotScore.

DAG component for spatial and/or column-value suitability (site-selection)
scoring: DataFrame(s) in, enriched DataFrame out (``sweetspot_score``,
``sweetspot_rank``, ``sweetspot_filtered``, and optional per-criterion
breakdown columns). Wraps ``flowtask.interfaces.scoring.SweetSpotScorer``
and/or ``ScoringEngine``. No LLM, no agent dependency — the scoring policy
comes from inline YAML component config or an external policy file
(FEAT-190, FEAT-191).
"""
from .component import SweetSpotScore

__all__ = ["SweetSpotScore"]
