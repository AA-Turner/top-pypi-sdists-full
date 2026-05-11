"""Batch-test multiple benchmarks. Outputs PASS/FAIL/ERROR per task."""
import sys
import subprocess
import os

tasks = sys.argv[1:]
results = {}

for task in tasks:
    out_path = f"scripts/_test_outputs/_test_{task.replace('/', '_').replace('-', '_')}.json"
    proc = subprocess.run(
        [
            sys.executable, "-m", "wisent.core.primitives.model_interface.core.main",
            "generate-pairs-from-task", task,
            "--output", out_path,
            "--limit", "5",
            "--allow-subtasks",
        ],
        capture_output=True,
        text=True,
    )
    out = proc.stdout + proc.stderr
    if any(f"Saved {n} pairs" in out for n in (1, 2, 3, 4, 5)):
        results[task] = "PASS"
    elif "Saved 0 pairs" in out:
        results[task] = "FAIL_0_PAIRS"
    else:
        # Find error
        err_lines = [l for l in out.split('\n') if 'Error' in l or 'error' in l]
        results[task] = f"ERROR: {err_lines[-1][:140] if err_lines else 'unknown'}"

for task, result in results.items():
    print(f"{task}: {result}")

passed = sum(1 for r in results.values() if r == "PASS")
print(f"\nTotal: {passed}/{len(tasks)} passed")
