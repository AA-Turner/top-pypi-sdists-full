"""Download and pretty-print one failing test_result to understand the structure."""
import json
import sys
from huggingface_hub import hf_hub_download

REPO = "wisent-ai/activations"
name = sys.argv[1] if len(sys.argv) > 1 else "advanced_ai_risk"
path = hf_hub_download(REPO, f"test_results/{name}.json", repo_type="dataset")
with open(path) as f:
    data = json.load(f)
print(json.dumps(data, indent=2)[:5000])
