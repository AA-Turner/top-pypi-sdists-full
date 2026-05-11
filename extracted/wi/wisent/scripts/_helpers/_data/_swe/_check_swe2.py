from huggingface_hub import hf_hub_download
import json
import os
path = hf_hub_download(repo_id="ByteDance-Seed/Multi-SWE-bench", filename="python/multi_swe_bench_python.jsonl", repo_type="dataset")
print(f"path: {path}")
print(f"size: {os.path.getsize(path)}")
with open(path, "r") as f:
    head = f.read(2000)
print(f"head: {head[:1000]}")
