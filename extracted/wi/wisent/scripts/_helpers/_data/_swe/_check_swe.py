from huggingface_hub import HfApi
api = HfApi()
files = api.list_repo_files("ByteDance-Seed/Multi-SWE-bench", repo_type="dataset")
print(f"total: {len(files)}")
for f in files[:30]:
    print(f"  {f}")
