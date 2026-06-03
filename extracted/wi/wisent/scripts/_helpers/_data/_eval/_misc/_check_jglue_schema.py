from datasets import load_dataset
ds = load_dataset("shunk031/JGLUE", "JCommonsenseQA", split="validation", trust_remote_code=True)
print(f"len: {len(ds)}")
print(f"first: {ds[0]}")
