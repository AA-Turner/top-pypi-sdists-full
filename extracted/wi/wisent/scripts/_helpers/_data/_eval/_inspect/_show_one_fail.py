"""Show full failure detail for one benchmark."""
import json
import sys
from pathlib import Path

CACHE = Path.home() / ".cache/huggingface/hub/datasets--wisent-ai--activations/snapshots"
target = sys.argv[1]

# Find latest test_result for target
latest = None
latest_mtime = 0
for snap in CACHE.iterdir():
    f = snap / "test_results" / f"{target}.json"
    if f.exists() and f.stat().st_mtime > latest_mtime:
        latest = f
        latest_mtime = f.stat().st_mtime

if not latest:
    print(f"No test_result found for {target}")
    sys.exit(1)

print(f"file: {latest}")
with open(latest) as f:
    data = json.load(f)
print(json.dumps(data, indent=2)[:4000])
