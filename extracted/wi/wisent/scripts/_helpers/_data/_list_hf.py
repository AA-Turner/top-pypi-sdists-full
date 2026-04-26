"""Verify what is in the wisent-ai/activations repo."""
from huggingface_hub import HfApi

REPO = "wisent-ai/activations"
api = HfApi()

print("Method 1: list_repo_files")
files = api.list_repo_files(REPO, repo_type="dataset")
print(f"  total files: {len(files)}")
prefixes = {}
for f in files:
    p = f.split("/")[0] if "/" in f else f
    prefixes[p] = prefixes.get(p, 0) + 1
for p, c in sorted(prefixes.items(), key=lambda x: -x[1])[:20]:
    print(f"  {p}: {c}")

print("\nMethod 2: dataset_info siblings")
info = api.dataset_info(REPO, files_metadata=True)
print(f"  siblings count: {len(info.siblings)}")
for s in info.siblings[:10]:
    print(f"  {s.rfilename} size={s.size}")
