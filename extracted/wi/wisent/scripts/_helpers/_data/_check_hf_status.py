"""Check status of pair_texts/ uploads in wisent-ai/activations HF repo.

Lists files in pair_texts/, downloads each, counts pairs, reports:
- total uploaded benchmarks
- benchmarks with 0 pairs (failing)
- benchmarks with >=1 pairs (passing)
"""
import json
import sys
from huggingface_hub import HfApi, hf_hub_download

REPO = "wisent-ai/activations"

api = HfApi()
print(f"Listing files in {REPO}/pair_texts/ ...", flush=True)
all_files = api.list_repo_files(REPO, repo_type="dataset")
pair_files = sorted([f for f in all_files if f.startswith("pair_texts/") and f.endswith(".json")])
print(f"Found {len(pair_files)} pair_texts files", flush=True)

passing = []
failing = []
errors = []

for i, path in enumerate(pair_files):
    name = path[len("pair_texts/"):-len(".json")]
    if i % 50 == 0:
        print(f"  [{i}/{len(pair_files)}] checking {name}...", flush=True)
    try:
        local = hf_hub_download(REPO, path, repo_type="dataset")
        with open(local, "r") as f:
            data = json.load(f)
        if isinstance(data, dict):
            n = len(data)
        elif isinstance(data, list):
            n = len(data)
        else:
            n = 0
        if n >= 1:
            passing.append((name, n))
        else:
            failing.append(name)
    except Exception as e:
        errors.append((name, str(e)[:80]))

print(f"\n=== Summary ===")
print(f"PASS (>=1 pair): {len(passing)}")
print(f"FAIL (0 pairs):  {len(failing)}")
print(f"ERROR (load):    {len(errors)}")
print(f"\nFAILING benchmarks ({len(failing)}):")
for name in failing[:200]:
    print(f"  {name}")
if len(failing) > 200:
    print(f"  ... +{len(failing)-200} more")
print(f"\nERRORS ({len(errors)}):")
for name, err in errors[:30]:
    print(f"  {name}: {err}")
