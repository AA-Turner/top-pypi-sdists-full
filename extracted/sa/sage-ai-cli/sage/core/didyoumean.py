"""Item #9 — Did you mean? Tool-error recovery."""

from __future__ import annotations

import difflib
import os
from pathlib import Path

__all__ = ["suggest_filenames"]


def suggest_filenames(target: str, root: Path, *, max_results: int = 3) -> list[str]:
    target_path = root / target
    if target_path.exists():
        return []

    target_basename = os.path.basename(target)
    candidates: list[str] = []

    for dirpath, dirnames, filenames in os.walk(root):
        # Skip noise
        dirnames[:] = [d for d in dirnames if not d.startswith(".")
                       and d not in {"node_modules", "__pycache__", "dist", "build"}]
        for name in filenames:
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)
            candidates.append(rel)

    if not candidates:
        return []

    matches = difflib.get_close_matches(
        target, candidates, n=max_results, cutoff=0.6,
    )
    if matches:
        return matches

    # Also try matching by basename only
    basename_matches = difflib.get_close_matches(
        target_basename, [os.path.basename(c) for c in candidates],
        n=max_results, cutoff=0.6,
    )
    return [c for c in candidates if os.path.basename(c) in basename_matches][:max_results]
