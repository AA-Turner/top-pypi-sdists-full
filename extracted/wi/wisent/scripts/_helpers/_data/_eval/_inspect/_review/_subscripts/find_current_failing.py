"""Walk every test_result JSON across all snapshots, picking the most recent
status per benchmark, and emit the names that are currently FAIL on either
extraction or evaluator.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

CACHE_ROOT = Path.home() / ".cache" / "huggingface" / "hub" / "datasets--wisent-ai--activations" / "snapshots"

# benchmark_name -> (mtime, status_str)
latest: dict[str, tuple[float, str]] = {}

for snap in CACHE_ROOT.iterdir():
    tr_dir = snap / "test_results"
    if not tr_dir.is_dir():
        continue
    for jf in tr_dir.iterdir():
        if not jf.name.endswith(".json"):
            continue
        try:
            mtime = jf.stat().st_mtime
        except OSError:
            continue
        name = jf.name[:-5]
        cur = latest.get(name)
        if cur is not None and cur[0] >= mtime:
            continue
        try:
            data = json.loads(jf.read_text())
        except Exception:
            continue
        ext = data.get("extraction", {}).get("status", "?")
        evl = data.get("evaluator", {}).get("status", "?")
        latest[name] = (mtime, f"{ext}/{evl}")

failing = sorted(
    name for name, (_mtime, status) in latest.items()
    if "FAIL" in status
)
print(f"TOTAL: {len(latest)} unique benchmarks")
print(f"FAILING: {len(failing)}")
out_path = Path(__file__).parent / "current_failing.txt"
out_path.write_text("\n".join(failing) + "\n")
print(f"Wrote {out_path}")
