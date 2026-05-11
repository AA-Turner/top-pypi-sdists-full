"""Sweep through current_failing.txt and run test_single_benchmark on each
benchmark, recording the result. Skips entries that already passed in this run.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
NAMES_FILE = HERE / "current_failing.txt"
RESULTS_FILE = HERE / "sweep_results.jsonl"

# Resume support — if RESULTS_FILE exists, skip benchmarks already recorded.
done: set[str] = set()
if RESULTS_FILE.exists():
    for line in RESULTS_FILE.read_text().splitlines():
        try:
            done.add(json.loads(line)["benchmark"])
        except Exception:
            pass

names = [n for n in NAMES_FILE.read_text().splitlines() if n.strip()]
total = len(names)
print(f"Total: {total}, already done: {len(done)}, remaining: {total - len(done)}")

with RESULTS_FILE.open("a") as f:
    for i, name in enumerate(names, 1):
        if name in done:
            continue
        try:
            proc = subprocess.run(
                [sys.executable, "-m",
                 "wisent.support.examples.scripts.discovery.validation.test_single_benchmark",
                 name, "--skip-cache"],
                capture_output=True, text=True, timeout=180,
            )
            output = proc.stdout
            ext_status = "?"
            evl_status = "?"
            for line in output.splitlines():
                if "Extraction:" in line:
                    pass
                elif line.strip().startswith("Result:"):
                    parts = line.split()
                    for p in parts:
                        if p.startswith("extraction="):
                            ext_status = p.split("=", 1)[1]
                        elif p.startswith("evaluator="):
                            evl_status = p.split("=", 1)[1]
                    break
            entry = {
                "benchmark": name,
                "extraction": ext_status,
                "evaluator": evl_status,
                "rc": proc.returncode,
            }
        except subprocess.TimeoutExpired:
            entry = {"benchmark": name, "extraction": "TIMEOUT", "evaluator": "SKIP", "rc": -1}
        except Exception as e:
            entry = {"benchmark": name, "extraction": "ERROR", "evaluator": "SKIP", "rc": -2, "error": str(e)}

        f.write(json.dumps(entry) + "\n")
        f.flush()

        if i % 10 == 0:
            print(f"[{i}/{total}] {name}: ext={entry['extraction']} eval={entry['evaluator']}")
