"""Smoke test for the bucketing/distribution math in
generate_pairs_from_task.execute_generate_pairs_from_task.

Runs the IDENTICAL logic on synthetic in-memory pair caches without
importing the rest of wisent (which has external deps the test box
doesn't need). Confirms:

  1. >limit cache with multi-subtask metadata.source_task buckets and
     distributes evenly (the 0.11.33 fix).
  2. <limit cache with multiple subtasks triggers the fall-through
     branch (the 0.11.34 fix).
  3. <limit cache with a single subtask is treated as an intrinsic
     small leaf and kept verbatim.
"""

from __future__ import annotations


def _grp_key(p: dict) -> str:
    md = p.get("metadata") if isinstance(p, dict) else None
    if not isinstance(md, dict):
        md = {}
    return (
        p.get("trait_label")
        or p.get("task_name")
        or p.get("subtask")
        or md.get("source_task")
        or md.get("task")
        or md.get("subtask")
        or ""
    )


def simulate(num_pairs: int, n_subtasks: int, limit: int):
    pairs = [
        {"prompt": f"q{i}", "metadata": {"source_task": f"sub_{i % n_subtasks}"}}
        for i in range(num_pairs)
    ]
    n = len(pairs)
    if n == 0:
        return {"action": "fresh_build_zero"}
    if limit > 0 and n < limit:
        unique = set(_grp_key(p) for p in pairs if _grp_key(p))
        if len(unique) > 1:
            return {"action": "fresh_build_small_group", "n": n, "unique": len(unique)}
        return {"action": "verbatim_small_leaf", "n": n}
    if limit > 0 and n > limit:
        by_grp: dict[str, list] = {}
        for p in pairs:
            by_grp.setdefault(_grp_key(p), []).append(p)
        picked: list = []
        if len(by_grp) > 1:
            per_grp = max(1, limit // len(by_grp))
            for _, gp in by_grp.items():
                picked.extend(gp[:per_grp])
                if len(picked) >= limit:
                    break
            picked = picked[:limit]
        else:
            picked = pairs[:limit]
        counts: dict[str, int] = {}
        for p in picked:
            k = _grp_key(p)
            counts[k] = counts.get(k, 0) + 1
        return {
            "action": "distribute",
            "written_total": len(picked),
            "n_groups": len(by_grp),
            "per_group_counts": counts,
        }
    return {"action": "verbatim_at_limit", "n": n}


def main() -> None:
    print("=== big multi-subtask cache, distribute ===")
    print(simulate(4000, n_subtasks=8, limit=500))
    print()
    print("=== bigbench-style: 10 pairs across 5 subtasks, limit=500 ===")
    print(simulate(10, n_subtasks=5, limit=500))
    print()
    print("=== single-subtask leaf with 100 pairs, limit=500 ===")
    print(simulate(100, n_subtasks=1, limit=500))
    print()
    print("=== 286-subtask group, 100k pairs, limit=500 (bigbench-shaped) ===")
    print(simulate(100000, n_subtasks=286, limit=500))


if __name__ == "__main__":
    main()
