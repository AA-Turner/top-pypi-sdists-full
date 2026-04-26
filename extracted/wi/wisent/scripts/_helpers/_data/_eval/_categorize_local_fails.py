"""Read all locally-cached test_results, find failing ones, group by error pattern."""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

CACHE = Path.home() / ".cache/huggingface/hub/datasets--wisent-ai--activations/snapshots"

# Latest test_result per benchmark name
seen = {}
for snap in sorted(CACHE.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
    tr = snap / "test_results"
    if not tr.exists():
        continue
    for f in tr.glob("*.json"):
        if f.stem not in seen:
            seen[f.stem] = f

print(f"Found {len(seen)} unique benchmarks")

failing = []
for name, f in seen.items():
    try:
        with open(f) as fp:
            data = json.load(fp)
    except Exception:
        continue
    ext = (data.get("extraction") or {}).get("status")
    evl_obj = data.get("evaluator") or {}
    evl = evl_obj.get("status")
    if ext == "FAIL" or evl == "FAIL":
        detail = (evl_obj.get("detail") if evl == "FAIL" else (data.get("extraction") or {}).get("detail")) or ""
        failing.append((name, ext, evl, detail))

print(f"Total failing: {len(failing)}")

# Bucket by signature of last error line
def signature(detail: str) -> str:
    if not detail:
        return "(empty detail)"
    # Find last meaningful line
    lines = [l.strip() for l in detail.strip().split("\n") if l.strip()]
    if not lines:
        return "(empty)"
    last = lines[-1]
    # Strip task names and numbers
    sig = re.sub(r"'[^']*'", "'X'", last)
    sig = re.sub(r"\d+", "N", sig)
    return sig[:200]

buckets = defaultdict(list)
for name, ext, evl, detail in failing:
    sig = signature(detail)
    buckets[sig].append((name, ext, evl))

print(f"\n=== Top failure signatures ===")
sorted_buckets = sorted(buckets.items(), key=lambda x: -len(x[1]))
for sig, names in sorted_buckets[:30]:
    print(f"\n[{len(names)}] {sig}")
    for name, ext, evl in names[:3]:
        print(f"     - {name}  (ext={ext} evl={evl})")
