"""Re-test the failing benchmarks list, report new pass/fail counts.

Usage: python3 _batch_retest.py [START] [COUNT]
  default: 0 100

Reads /tmp/failing_list.txt, runs test_single_benchmark on each in sequence
(skipping cache so we re-extract), and reports pass / fail / skip counts.
"""
import json
import os
import subprocess
import sys
import tempfile
from collections import Counter

LIST_FILE = "/tmp/failing_list.txt"
start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
count = int(sys.argv[2]) if len(sys.argv) > 2 else 100

with open(LIST_FILE) as f:
    names = [l.strip() for l in f if l.strip()]
batch = names[start : start + count]

print(f"Re-testing {len(batch)} benchmarks (offset {start})", flush=True)

results = Counter()
new_fail_names = []
new_pass_names = []

for i, name in enumerate(batch):
    proc = subprocess.run(
        [
            sys.executable, "-m",
            "wisent.support.examples.scripts.discovery.validation.test_single_benchmark",
            name, "--skip-cache",
        ],
        capture_output=True, text=True,
    )
    out = proc.stdout
    # Parse "extraction=X  evaluator=Y" line
    ext_status = "?"
    evl_status = "?"
    for line in out.split("\n"):
        if line.startswith("Result: extraction="):
            parts = line.replace("Result: ", "").split()
            for p in parts:
                if p.startswith("extraction="):
                    ext_status = p.split("=", 1)[1]
                elif p.startswith("evaluator="):
                    evl_status = p.split("=", 1)[1]
    if ext_status == "PASS" and (evl_status == "PASS" or evl_status.startswith("SKIP")):
        results["PASS"] += 1
        new_pass_names.append(name)
    elif ext_status == "FAIL" or evl_status == "FAIL":
        results["FAIL"] += 1
        new_fail_names.append(f"{name}  ext={ext_status} evl={evl_status}")
    else:
        results["OTHER"] += 1
        new_fail_names.append(f"{name}  ext={ext_status} evl={evl_status}")
    if (i + 1) % 10 == 0:
        print(f"  [{i+1}/{len(batch)}] PASS={results['PASS']} FAIL={results['FAIL']}", flush=True)

print(f"\n=== Final ===")
print(f"PASS: {results['PASS']}")
print(f"FAIL: {results['FAIL']}")
print(f"OTHER: {results['OTHER']}")
print(f"\nFirst 30 still-failing:")
for n in new_fail_names[:30]:
    print(f"  {n}")
