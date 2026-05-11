from huggingface_hub import HfApi
api = HfApi()
try:
    files = api.list_repo_files("miulab/tmlu", repo_type="dataset")
    print("miulab/tmlu OK:", len(files))
except Exception as e:
    print(f"miulab/tmlu FAIL: {e}")

# Try alternatives
for repo in ["ikala/tmlu", "miulab/TMLU", "MediaTek-Research/TCEval-v2", "miulab/TaiwanLLM"]:
    try:
        files = api.list_repo_files(repo, repo_type="dataset")
        print(f"{repo} OK:", len(files), "files")
    except Exception as e:
        print(f"{repo} FAIL: {type(e).__name__}: {str(e)[:100]}")
