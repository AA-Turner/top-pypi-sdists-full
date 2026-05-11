"""Fast check: use list_repo_tree to get file sizes without downloading."""
from huggingface_hub import HfApi

REPO = "wisent-ai/activations"
api = HfApi()

print(f"Listing {REPO}/pair_texts/ ...", flush=True)
pair_files = []
for entry in api.list_repo_tree(REPO, repo_type="dataset", path_in_repo="pair_texts", recursive=False):
    if entry.path.endswith(".json"):
        pair_files.append((entry.path, getattr(entry, "size", None)))
print(f"Found {len(pair_files)} files", flush=True)

# Empty JSON ('{}') = 2 bytes; with whitespace/newline ~3-4 bytes
# Anything < 50 bytes is essentially empty
EMPTY_THRESHOLD = 50

empty = [(f, s) for f, s in pair_files if s is not None and s < EMPTY_THRESHOLD]
non_empty = [(f, s) for f, s in pair_files if s is not None and s >= EMPTY_THRESHOLD]
unknown_size = [f for f, s in pair_files if s is None]

print(f"\n=== Summary ===")
print(f"Total pair_texts files: {len(pair_files)}")
print(f"PASS (size >= {EMPTY_THRESHOLD} bytes): {len(non_empty)}")
print(f"FAIL (empty/tiny):       {len(empty)}")
print(f"UNKNOWN size:            {len(unknown_size)}")

print(f"\nFAILING benchmarks ({len(empty)}):")
for path, size in sorted(empty)[:300]:
    name = path[len("pair_texts/"):-len(".json")]
    print(f"  {name} ({size} bytes)")
if len(empty) > 300:
    print(f"  ... +{len(empty) - 300} more")
