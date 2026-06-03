from huggingface_hub import HfApi
api = HfApi()
for repo in ["Rakuten/JGLUE", "shunk031/JGLUE", "nlp-waseda/JGLUE", "leemeng/JGLUE", "yahoojapan/JGLUE"]:
    try:
        files = api.list_repo_files(repo, repo_type="dataset")
        print(f"{repo} OK: {len(files)} files")
    except Exception as e:
        print(f"{repo} FAIL: {type(e).__name__}")
