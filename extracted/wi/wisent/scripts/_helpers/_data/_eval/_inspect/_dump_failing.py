"""Dump all locally-cached failing benchmark names to a list file."""
import json
from pathlib import Path

CACHE = Path.home() / ".cache/huggingface/hub/datasets--wisent-ai--activations/snapshots"

seen = {}
for snap in sorted(CACHE.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
    tr = snap / "test_results"
    if not tr.exists():
        continue
    for f in tr.glob("*.json"):
        if f.stem not in seen:
            seen[f.stem] = f

failing = []
for name, f in seen.items():
    try:
        with open(f) as fp:
            data = json.load(fp)
    except Exception:
        continue
    ext = (data.get("extraction") or {}).get("status")
    evl = (data.get("evaluator") or {}).get("status")
    if ext == "FAIL" or evl == "FAIL":
        failing.append(name)

with open("/tmp/failing_list.txt", "w") as f:
    for n in sorted(failing):
        f.write(n + "\n")
print(f"Wrote {len(failing)} names to /tmp/failing_list.txt")
