"""Item #22 — Shell-history mining."""

from __future__ import annotations

import math
import re
import time
from collections import defaultdict
from pathlib import Path

__all__ = ["extract_top_commands", "score_command"]


_ZSH_HISTORY_RE = re.compile(r"^:\s*(\d+):\d+;(.+?)\s*$", re.MULTILINE)


def score_command(*, count: int, last_seen_ts: float) -> float:
    """Higher score = more relevant. More recent timestamps weight higher.

    The formula combines raw count with a normalized recency factor so that
    given equal counts, the more recent command always scores higher.
    """
    # Normalize timestamp into a recency component: scaled by 1e10 so that
    # even tiny ts differences produce visible score differences but the
    # count term still dominates.
    recency_factor = last_seen_ts / 1e10
    return float(count) + recency_factor


def extract_top_commands(history_file: Path, *, n: int = 5) -> list[tuple[str, int]]:
    if not history_file.exists():
        return []
    try:
        text = history_file.read_text("utf-8", errors="replace")
    except OSError:
        return []
    counts: dict[str, int] = defaultdict(int)
    timestamps: dict[str, float] = {}
    for m in _ZSH_HISTORY_RE.finditer(text):
        ts = float(m.group(1))
        cmd = m.group(2).strip()
        counts[cmd] += 1
        if ts > timestamps.get(cmd, 0):
            timestamps[cmd] = ts
    if not counts:
        # Fallback: try plain bash history (one cmd per line)
        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            counts[line] += 1
    sorted_cmds = sorted(counts.items(), key=lambda t: t[1], reverse=True)
    return sorted_cmds[:n]
