#  -*- coding: utf-8 -*-
#
#  Copyright (c) 2023-2026 Featrix, Inc, All Rights Reserved
#
#  Proprietary and Confidential.  Unauthorized use, copying or dissemination
#  of these materials is strictly prohibited.
#

"""
Label similarity utilities for discovering and collapsing near-duplicate class labels.

These functions use BERT sentence embeddings (via the Featrix string server) to
compute semantic similarity between label strings, then group or merge them.

Two modes:
  - **threshold mode**: Merge pairs whose cosine similarity exceeds a threshold
    (e.g., "Unsafe & Dangerous" ↔ "Unsafe and Dangerous" at 0.96).
  - **desired_label_count mode**: Agglomerative clustering to reduce labels to
    exactly N groups.

Both modes can be combined: first collapse synonyms, then cluster to target count.

Usage in a notebook::

    from featrixsphere import find_similar_labels, collapse_similar_labels

    # Discover synonym groups
    info = find_similar_labels(df['violation_type'], threshold=0.90)

    # Collapse in-place and get mapping
    df, info = collapse_similar_labels(df, 'violation_type', threshold=0.85)

    # Cluster into 5 groups
    df, info = collapse_similar_labels(df, 'violation_type', desired_label_count=5)
"""
import logging
from typing import Any, Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd

logger = logging.getLogger(__name__)


def _get_bert_embeddings(class_names: List[str]) -> Optional[np.ndarray]:
    """Get BERT embeddings for a list of strings via the Featrix string server.

    Returns an (N, 384) numpy array, or None on failure.
    """
    try:
        import sys
        import os

        # Try the installed neural lib first, fall back to src/lib path
        try:
            from featrix.neural.simple_string_cache import SimpleStringCache
        except ImportError:
            # Running from repo root — add src/lib to path
            repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            for subdir in ("src/lib", "src"):
                p = os.path.join(repo_root, subdir)
                if p not in sys.path:
                    sys.path.insert(0, p)
            from featrix.neural.simple_string_cache import SimpleStringCache

        import torch

        cache = SimpleStringCache(initial_values=class_names, debugName="label_utils")
        raw = cache.get_embeddings_batch(class_names)

        vectors = []
        for emb in raw:
            if emb is None:
                return None
            if isinstance(emb, torch.Tensor):
                emb = emb.cpu().numpy()
            elif isinstance(emb, list):
                emb = np.array(emb, dtype=np.float32)
            vectors.append(emb)

        return np.array(vectors, dtype=np.float32)
    except Exception as exc:
        logger.warning("Could not fetch BERT embeddings: %s", exc)
        return None


def _cosine_similarity_matrix(embeddings: np.ndarray) -> np.ndarray:
    """Compute NxN cosine-similarity matrix."""
    from scipy.spatial.distance import cdist
    return 1.0 - cdist(embeddings, embeddings, metric="cosine")


def _union_find_groups(pairs: List[Tuple[str, str]], all_items: List[str]) -> Dict[str, List[str]]:
    """Build connected components from synonym pairs via union-find."""
    parent: Dict[str, str] = {item: item for item in all_items}

    def find(x: str) -> str:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: str, b: str) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    for a, b in pairs:
        union(a, b)

    from collections import defaultdict
    groups: Dict[str, List[str]] = defaultdict(list)
    for item in all_items:
        groups[find(item)].append(item)
    return dict(groups)


def _agglomerative_cluster(sim_matrix: np.ndarray, class_names: List[str],
                           desired_count: int, value_counts: Dict[str, int]) -> Dict[str, List[str]]:
    """Agglomerative clustering on similarity matrix until desired_count groups remain."""
    n = len(class_names)
    if desired_count >= n:
        return {c: [c] for c in class_names}

    # Start with each class in its own group
    # group_id -> list of class indices
    groups: Dict[int, List[int]] = {i: [i] for i in range(n)}

    # Build a max-heap of inter-group similarities
    # We'll use a simple greedy approach: repeatedly merge the two most similar groups
    while len(groups) > desired_count:
        best_sim = -1.0
        best_pair = (-1, -1)
        group_ids = list(groups.keys())
        for ii in range(len(group_ids)):
            for jj in range(ii + 1, len(group_ids)):
                gi, gj = group_ids[ii], group_ids[jj]
                # Average linkage: mean similarity between all pairs across groups
                sims = []
                for a in groups[gi]:
                    for b in groups[gj]:
                        sims.append(sim_matrix[a, b])
                avg_sim = np.mean(sims)
                if avg_sim > best_sim:
                    best_sim = avg_sim
                    best_pair = (gi, gj)

        # Merge
        gi, gj = best_pair
        groups[gi].extend(groups[gj])
        del groups[gj]

    # Convert index groups to name groups, canonical = most frequent
    result: Dict[str, List[str]] = {}
    for members_idx in groups.values():
        members = [class_names[i] for i in members_idx]
        members_sorted = sorted(members, key=lambda m: value_counts.get(m, 0), reverse=True)
        canonical = members_sorted[0]
        result[canonical] = members_sorted
    return result


def _build_result(groups: Dict[str, List[str]], value_counts: Dict[str, int],
                  original_n: int, sim_stats: Dict[str, float],
                  threshold: Optional[float], desired_label_count: Optional[int],
                  source: str) -> Dict[str, Any]:
    """Build the standard result dict from groups."""
    reduced_to_full: Dict[str, List[str]] = {}
    full_to_reduced: Dict[str, str] = {}

    for canonical, members in groups.items():
        reduced_to_full[canonical] = members
        for m in members:
            full_to_reduced[m] = canonical

    collapsed_n = len(reduced_to_full)

    # Build per-group info
    groups_info = []
    for canonical, members in groups.items():
        if len(members) > 1:
            synonyms = [m for m in members if m != canonical]
            groups_info.append({
                "canonical": canonical,
                "synonyms": synonyms,
                "counts": {m: int(value_counts.get(m, 0)) for m in members},
            })

    # New collapsed counts
    collapsed_counts: Dict[str, int] = {}
    for canonical, members in groups.items():
        collapsed_counts[canonical] = sum(int(value_counts.get(m, 0)) for m in members)

    return {
        "original_n_classes": original_n,
        "collapsed_n_classes": collapsed_n,
        "threshold": threshold,
        "desired_label_count": desired_label_count,
        "source": source,
        "reduced_to_full": reduced_to_full,
        "full_to_reduced": full_to_reduced,
        "class_counts": collapsed_counts,
        "similarity_stats": sim_stats,
        "groups": groups_info,
    }


# ──────────────────────────────────────────────────────────────────────
# Public API
# ──────────────────────────────────────────────────────────────────────

def find_similar_labels(
    values: Union[pd.Series, List[str]],
    threshold: Optional[float] = 0.90,
    desired_label_count: Optional[int] = None,
) -> Dict[str, Any]:
    """Discover groups of similar labels using BERT embedding similarity.

    Pure discovery — does not modify any data.

    Args:
        values: A pandas Series or list of label strings to analyze.
        threshold: Cosine similarity threshold for synonym detection.
            Pairs above this are grouped together. Set to ``None`` to
            disable threshold-based grouping (use *desired_label_count*
            instead).
        desired_label_count: Target number of label groups. Uses
            agglomerative clustering to merge labels until this count
            is reached. Can be combined with *threshold* (synonyms are
            collapsed first, then clustered to target).

    Returns:
        dict with keys:

        - **reduced_to_full** — ``{canonical: [canonical, synonym1, ...]}``
        - **full_to_reduced** — ``{original_label: canonical_label}``
        - **class_counts** — ``{canonical: total_count}``
        - **groups** — list of dicts with ``canonical``, ``synonyms``, ``counts``
        - **similarity_stats** — ``{min, q1, median, q3, max, mean}``
        - **original_n_classes**, **collapsed_n_classes** — before/after counts

    Example::

        info = find_similar_labels(df['violation_type'], threshold=0.85)
        for g in info['groups']:
            print(f"{g['canonical']} <- {g['synonyms']}")
    """
    if isinstance(values, pd.Series):
        unique_classes = sorted(values.dropna().unique().tolist())
        value_counts = values.value_counts().to_dict()
    else:
        unique_classes = sorted(set(str(v) for v in values if v is not None and str(v) != 'nan'))
        from collections import Counter
        value_counts = dict(Counter(str(v) for v in values))

    n_original = len(unique_classes)
    if n_original < 2:
        return _build_result(
            groups={c: [c] for c in unique_classes},
            value_counts=value_counts, original_n=n_original,
            sim_stats={}, threshold=threshold,
            desired_label_count=desired_label_count, source="skipped",
        )

    # Get BERT embeddings
    embeddings = _get_bert_embeddings(unique_classes)
    if embeddings is None:
        raise RuntimeError(
            "Could not get BERT embeddings from string server. "
            "Ensure the Featrix string server is reachable."
        )

    sim_matrix = _cosine_similarity_matrix(embeddings)

    # Stats on upper triangle
    n = len(unique_classes)
    upper_tri = [sim_matrix[i, j] for i in range(n) for j in range(i + 1, n)]
    upper_tri_arr = np.array(upper_tri) if upper_tri else np.array([0.0])
    sim_stats = {
        "min": float(np.min(upper_tri_arr)),
        "q1": float(np.percentile(upper_tri_arr, 25)),
        "median": float(np.median(upper_tri_arr)),
        "q3": float(np.percentile(upper_tri_arr, 75)),
        "max": float(np.max(upper_tri_arr)),
        "mean": float(np.mean(upper_tri_arr)),
    }

    # Step 1: Threshold-based synonym collapse
    if threshold is not None:
        synonym_pairs = []
        for i in range(n):
            for j in range(i + 1, n):
                if sim_matrix[i, j] >= threshold:
                    synonym_pairs.append((unique_classes[i], unique_classes[j]))
        groups = _union_find_groups(synonym_pairs, unique_classes)
    else:
        groups = {c: [c] for c in unique_classes}

    # Pick canonical per group (most frequent)
    canonical_groups: Dict[str, List[str]] = {}
    for _, members in groups.items():
        members_sorted = sorted(members, key=lambda m: value_counts.get(m, 0), reverse=True)
        canonical_groups[members_sorted[0]] = members_sorted

    # Step 2: Agglomerative clustering to desired count
    if desired_label_count is not None and len(canonical_groups) > desired_label_count:
        # Build new sim matrix for the canonical labels
        canonical_names = list(canonical_groups.keys())
        canonical_indices = [unique_classes.index(c) for c in canonical_names]
        sub_sim = sim_matrix[np.ix_(canonical_indices, canonical_indices)]

        # Aggregate value counts per canonical group
        agg_counts = {c: sum(value_counts.get(m, 0) for m in members)
                      for c, members in canonical_groups.items()}

        clustered = _agglomerative_cluster(sub_sim, canonical_names, desired_label_count, agg_counts)

        # Expand: each clustered group's members include all original synonyms
        final_groups: Dict[str, List[str]] = {}
        for new_canonical, old_canonicals in clustered.items():
            all_members = []
            for oc in old_canonicals:
                all_members.extend(canonical_groups[oc])
            # Re-sort by frequency, pick new canonical
            all_members_sorted = sorted(all_members, key=lambda m: value_counts.get(m, 0), reverse=True)
            final_groups[all_members_sorted[0]] = all_members_sorted
        canonical_groups = final_groups

    source = "threshold" if desired_label_count is None else (
        "desired_label_count" if threshold is None else "threshold+desired_label_count"
    )
    return _build_result(
        groups=canonical_groups, value_counts=value_counts,
        original_n=n_original, sim_stats=sim_stats,
        threshold=threshold, desired_label_count=desired_label_count,
        source=source,
    )


def collapse_similar_labels(
    df: pd.DataFrame,
    column: str,
    threshold: Optional[float] = 0.90,
    desired_label_count: Optional[int] = None,
    mapping: Optional[Dict[str, str]] = None,
    inplace: bool = False,
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """Discover and apply label collapsing to a DataFrame column.

    Combines discovery and application in one call. The DataFrame is
    modified **in-place** by default (set ``inplace=False`` to get a copy).

    Args:
        df: DataFrame containing the label column.
        column: Column name to collapse.
        threshold: Cosine similarity threshold for synonym detection
            (default 0.90). Set to ``None`` to skip threshold-based merging.
        desired_label_count: Target number of distinct labels. Uses
            agglomerative clustering after synonym collapse.
        mapping: Explicit ``{old_label: new_label}`` dict. If provided,
            applied directly — auto-detection is skipped.
        inplace: If True, modify *df* in place. If False (default),
            operate on a copy.

    Returns:
        ``(df, info)`` where *df* is the (possibly modified) DataFrame
        and *info* is the same dict returned by :func:`find_similar_labels`,
        plus the ``full_to_reduced`` mapping that was applied.

    Example::

        # Auto-detect and collapse synonyms
        df, info = collapse_similar_labels(df, 'violation_type')

        # Cluster into 3 groups
        df, info = collapse_similar_labels(df, 'violation_type',
                                           desired_label_count=3)

        # Explicit mapping
        df, info = collapse_similar_labels(df, 'violation_type',
            mapping={"Unsafe & Dangerous": "Unsafe and Dangerous"})
    """
    if not inplace:
        df = df.copy()

    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found in DataFrame. Available: {list(df.columns)}")

    if mapping is not None:
        # Explicit mapping — apply directly
        original_unique = sorted(df[column].dropna().unique().tolist())
        df[column] = df[column].map(lambda v: mapping.get(v, v))
        new_unique = sorted(df[column].dropna().unique().tolist())
        new_counts = df[column].value_counts().to_dict()

        reduced_to_full: Dict[str, List[str]] = {}
        for old, new in mapping.items():
            reduced_to_full.setdefault(new, []).append(old)
        for cls in new_unique:
            if cls not in reduced_to_full:
                reduced_to_full[cls] = [cls]
            elif cls not in reduced_to_full[cls]:
                reduced_to_full[cls].insert(0, cls)

        info = {
            "original_n_classes": len(original_unique),
            "collapsed_n_classes": len(new_unique),
            "threshold": None,
            "desired_label_count": None,
            "source": "explicit_mapping",
            "reduced_to_full": reduced_to_full,
            "full_to_reduced": dict(mapping),
            "class_counts": {k: int(v) for k, v in new_counts.items()},
            "similarity_stats": {},
            "groups": [],
        }
        return df, info

    # Auto-detect
    info = find_similar_labels(
        values=df[column],
        threshold=threshold,
        desired_label_count=desired_label_count,
    )

    # Apply the mapping
    full_to_reduced = info["full_to_reduced"]
    df[column] = df[column].map(lambda v: full_to_reduced.get(v, v))

    # Update counts after application
    info["class_counts"] = {k: int(v) for k, v in df[column].value_counts().to_dict().items()}

    return df, info
