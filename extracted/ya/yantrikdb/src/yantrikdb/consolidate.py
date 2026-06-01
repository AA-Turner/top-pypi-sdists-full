"""YantrikDB Consolidation — re-exported from Rust engine."""

from yantrikdb._yantrikdb_rust import (
    _cosine_similarity,
    _extractive_summary,
    _find_clusters,
    consolidate,
    find_consolidation_candidates,
)

__all__ = [
    "consolidate",
    "find_consolidation_candidates",
    "_cosine_similarity",
    "_extractive_summary",
    "_find_clusters",
]
