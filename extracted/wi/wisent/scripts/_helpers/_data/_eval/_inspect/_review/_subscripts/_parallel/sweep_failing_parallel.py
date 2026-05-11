"""Parallel sweep through current_failing.txt. Runs N test_single_benchmark
processes concurrently and records each result to sweep_results.jsonl.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

HERE = Path(__file__).parent.parent
NAMES_FILE = HERE / "current_failing.txt"
RESULTS_FILE = HERE / "sweep_results.jsonl"

WORKERS = int(os.environ.get("SWEEP_WORKERS", "8"))
def run_one(name: str) -> dict:
    try:
        proc = subprocess.run(
            [sys.executable, "-m",
             "wisent.support.examples.scripts.discovery.validation.test_single_benchmark",
             name, "--skip-cache"],
            capture_output=True, text=True,
        )
        ext_status = "?"
        evl_status = "?"
        for line in proc.stdout.splitlines():
            if line.strip().startswith("Result:"):
                for p in line.split():
                    if p.startswith("extraction="):
                        ext_status = p.split("=", 1)[1]
                    elif p.startswith("evaluator="):
                        evl_status = p.split("=", 1)[1]
                break
        return {
            "benchmark": name,
            "extraction": ext_status,
            "evaluator": evl_status,
            "rc": proc.returncode,
        }
    except Exception as e:
        return {"benchmark": name, "extraction": "ERROR", "evaluator": "SKIP", "rc": -2, "error": str(e)}


def main() -> None:
    done: set[str] = set()
    if RESULTS_FILE.exists():
        for line in RESULTS_FILE.read_text().splitlines():
            try:
                done.add(json.loads(line)["benchmark"])
            except Exception:
                pass

    names = [n for n in NAMES_FILE.read_text().splitlines() if n.strip() and n not in done]
    print(f"Total: {len(names)} remaining; workers={WORKERS}")

    completed = 0
    with RESULTS_FILE.open("a") as f, ProcessPoolExecutor(max_workers=WORKERS) as pool:
        futures = {pool.submit(run_one, n): n for n in names}
        for future in as_completed(futures):
            entry = future.result()
            f.write(json.dumps(entry) + "\n")
            f.flush()
            completed += 1
            if completed % 20 == 0:
                print(f"[{completed}/{len(names)}] {entry['benchmark']}: ext={entry['extraction']} eval={entry['evaluator']}")


if __name__ == "__main__":
    main()
