from huggingface_hub import HfApi
api = HfApi()
files = api.list_repo_files("MediaTek-Research/TCEval-v2", repo_type="dataset")
for f in files[:30]:
    print(f)
