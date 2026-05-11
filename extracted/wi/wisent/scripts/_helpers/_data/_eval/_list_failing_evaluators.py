"""List ALL failing benchmarks from HF test_results/ cache.

Test results are stored at test_results/{benchmark}.json with structure:
  {"task": ..., "extraction": {"status": ...}, "evaluator": {"status": ..., "detail": ...}}

Categorize all failures so we can attack each one.
"""
import json
import sys
from huggingface_hub import HfApi, hf_hub_download
from concurrent.futures import ThreadPoolExecutor, as_completed

REPO = "wisent-ai/activations"

api = HfApi()
print("Listing test_results/ ...", flush=True)
files = api.list_repo_files(REPO, repo_type="dataset")
test_files = sorted([f for f in files if f.startswith("test_results/") and f.endswith(".json")])
print(f"Found {len(test_files)} test_results files", flush=True)

def fetch(path):
    name = path[len("test_results/"):-len(".json")]
    try:
        local = hf_hub_download(REPO, path, repo_type="dataset")
        with open(local) as f:
            data = json.load(f)
        ext = (data.get("extraction") or {}).get("status")
        evl_obj = data.get("evaluator") or {}
        evl = evl_obj.get("status")
        detail = (evl_obj.get("detail") or "")[:300]
        return name, ext, evl, detail
    except Exception as e:
        return name, "ERR", "ERR", str(e)[:300]

ext_pass_evl_fail = []
ext_fail = []
both_pass = []
ext_pass_evl_skip = []
others = []

print("Fetching results in parallel ...", flush=True)
with ThreadPoolExecutor(max_workers=24) as ex:
    futures = {ex.submit(fetch, p): p for p in test_files}
    for i, fut in enumerate(as_completed(futures)):
        name, ext, evl, detail = fut.result()
        if ext == "PASS" and evl == "PASS":
            both_pass.append(name)
        elif ext == "PASS" and evl == "FAIL":
            ext_pass_evl_fail.append((name, detail))
        elif ext == "FAIL":
            ext_fail.append(name)
        elif ext == "PASS" and evl in ("SKIP", "SKIP_NO_MODEL"):
            ext_pass_evl_skip.append((name, evl))
        else:
            others.append((name, ext, evl))
        if (i + 1) % 200 == 0:
            print(f"  [{i+1}/{len(test_files)}]", flush=True)

print(f"\n=== Summary ===")
print(f"Total test_results: {len(test_files)}")
print(f"BOTH PASS:           {len(both_pass)}")
print(f"ext PASS, evl FAIL:  {len(ext_pass_evl_fail)}")
print(f"ext PASS, evl SKIP:  {len(ext_pass_evl_skip)}")
print(f"ext FAIL:            {len(ext_fail)}")
print(f"OTHER:               {len(others)}")

# Break down OTHER
print(f"\n=== OTHER breakdown ===")
from collections import Counter
other_combos = Counter()
for name, ext, evl in others:
    other_combos[(ext, evl)] += 1
for (ext, evl), n in other_combos.most_common():
    print(f"  ext={ext} evl={evl}: {n}")
print(f"\nSample 'OTHER' names:")
for name, ext, evl in others[:10]:
    print(f"  {name} (ext={ext} evl={evl})")

# Group failing evaluators by error message
from collections import Counter
err_buckets = Counter()
for name, detail in ext_pass_evl_fail:
    # Take first non-empty line
    key = next((l for l in detail.split("\n") if l.strip()), "")[:200]
    err_buckets[key] += 1
print(f"\n=== Top failure messages ===")
for msg, n in err_buckets.most_common(30):
    print(f"  {n:>5}  {msg}")

# Save failing names
with open("/tmp/failing_evaluators.json", "w") as f:
    json.dump({
        "ext_pass_evl_fail": [n for n, _ in ext_pass_evl_fail],
        "ext_fail": ext_fail,
    }, f, indent=2)
print(f"\nSaved /tmp/failing_evaluators.json")
