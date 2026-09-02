"""Pure PageRank Link Score algorithm.

Standalone — no DB, no host coupling. Hosts (e.g. aidream) wrap this in a
function that pulls nodes/edges out of their persistence layer, calls
`compute_link_scores`, then writes the results back.

Algorithm: standard iterative PageRank with damping factor d=0.85, dangling-
mass teleport, capped iterations, converges to 1e-6. Output is a 0..100 score
per node where the most-linked-to page is 100 and the least is ~0.

Used for Screaming-Frog-style "Link Score" — the single best at-a-glance
signal of which pages on a site matter most.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from collections.abc import Iterable

logger = logging.getLogger(__name__)


DAMPING = 0.85
MAX_ITERATIONS = 60
CONVERGENCE_DELTA = 1e-6


@dataclass
class Edge:
    """A directed link in the page graph. `target_url` is matched against the
    URL→id map computed by `compute_link_scores`."""

    source_id: str
    target_url: str


def compute_link_scores(
    nodes: list[tuple[str, str, str | None]],
    edges: Iterable[Edge],
) -> dict[str, float]:
    """Compute link scores for the given graph.

    Args:
        nodes: list of (id, url, canonical_url|None) tuples — one per page.
            canonical_url lets a link to a redirected URL resolve to the
            canonical page (so we don't double-count or drop edges).
        edges: iterable of Edge(source_id, target_url). Edges whose target
            isn't a known node are silently skipped.

    Returns:
        dict mapping each node id to its 0..100 link score. If `nodes` is
        empty, returns {}.
    """
    page_ids = [pid for pid, _, _ in nodes]
    n = len(page_ids)
    if n == 0:
        return {}

    # URL → id index that handles both `url` and `canonical_url` so internal
    # links to a redirected page still resolve to a known node.
    url_to_id: dict[str, str] = {}
    for pid, url, canonical_url in nodes:
        url_to_id[url] = pid
        if canonical_url and canonical_url != url:
            url_to_id[canonical_url] = pid

    # Build outbound edge map: source_id -> {target_id, …} with dedup.
    out_edges: dict[str, set[str]] = {pid: set() for pid in page_ids}
    for e in edges:
        tgt = url_to_id.get(e.target_url)
        if tgt and e.source_id in out_edges:
            out_edges[e.source_id].add(tgt)

    # Iterative PageRank — standard formulation with dangling-mass teleport.
    score = {pid: 1.0 / n for pid in page_ids}
    for it in range(MAX_ITERATIONS):
        new_score = {pid: (1.0 - DAMPING) / n for pid in page_ids}
        dangling_mass = sum(score[pid] for pid in page_ids if not out_edges[pid])
        if dangling_mass > 0:
            even = DAMPING * dangling_mass / n
            for pid in page_ids:
                new_score[pid] += even
        for pid, targets in out_edges.items():
            if not targets:
                continue
            share = DAMPING * score[pid] / len(targets)
            for tgt in targets:
                new_score[tgt] = new_score.get(tgt, 0.0) + share
        delta = sum(abs(new_score[p] - score[p]) for p in page_ids)
        score = new_score
        if delta < CONVERGENCE_DELTA:
            logger.info("PageRank converged after %d iterations (n=%d)", it + 1, n)
            break

    # Rescale to 0..100. If everyone has the same score (no edges at all)
    # default to 50 so the column is populated and visually neutral.
    max_v = max(score.values())
    min_v = min(score.values())
    spread = max_v - min_v
    if spread <= 0:
        return {pid: 50.0 for pid in page_ids}
    return {pid: ((score[pid] - min_v) / spread) * 100.0 for pid in page_ids}


__all__ = ["Edge", "compute_link_scores", "DAMPING", "MAX_ITERATIONS"]
