"""Inspect a few ext PASS evl FAIL test_results from local cache."""
import json
import os
from pathlib import Path

CACHE = Path.home() / ".cache/huggingface/hub/datasets--wisent-ai--activations/snapshots"

# Find latest test_results dir per benchmark
seen = {}
for snap in sorted(CACHE.iterdir(), key=lambda p: p.stat().st_mtime, reverse=True):
    tr_dir = snap / "test_results"
    if not tr_dir.exists():
        continue
    for f in tr_dir.glob("*.json"):
        name = f.stem
        if name not in seen:
            seen[name] = f

print(f"Found {len(seen)} unique benchmarks in local cache")

# Categorize
pass_pass = []
ext_pass_evl_fail = []
ext_fail = []
other = []

for name, f in seen.items():
    try:
        with open(f) as fp:
            data = json.load(fp)
        ext = (data.get("extraction") or {}).get("status")
        evl_obj = data.get("evaluator") or {}
        evl = evl_obj.get("status")
        detail = (evl_obj.get("detail") or "")
        if ext == "PASS" and evl == "PASS":
            pass_pass.append(name)
        elif ext == "PASS" and evl == "FAIL":
            ext_pass_evl_fail.append((name, detail))
        elif ext == "FAIL":
            ext_fail.append((name, (data.get("extraction") or {}).get("detail", "")))
        else:
            other.append((name, ext, evl))
    except Exception as e:
        pass

print(f"\nPASS+PASS: {len(pass_pass)}")
print(f"ext PASS evl FAIL: {len(ext_pass_evl_fail)}")
print(f"ext FAIL: {len(ext_fail)}")
print(f"OTHER: {len(other)}")

print(f"\n=== ext PASS, evl FAIL details (first 5 unique-by-tail) ===")
seen_tails = set()
shown = 0
for name, detail in ext_pass_evl_fail:
    tail = detail[-500:] if len(detail) > 500 else detail
    if tail in seen_tails:
        continue
    seen_tails.add(tail)
    print(f"\n--- {name} ---")
    print(detail[-1500:])
    shown += 1
    if shown >= 5:
        break

print(f"\n=== ext FAIL details (first 3 unique) ===")
seen_tails = set()
shown = 0
for name, detail in ext_fail:
    tail = detail[-300:] if detail else ""
    if tail in seen_tails:
        continue
    seen_tails.add(tail)
    print(f"\n--- {name} ---")
    print(detail[-800:] if detail else "(empty)")
    shown += 1
    if shown >= 3:
        break
