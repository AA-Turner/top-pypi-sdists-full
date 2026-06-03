from datasets import load_dataset
ds = load_dataset("MediaTek-Research/TCEval-v2", "tmmluplus-accounting", split="test")
print(f"len: {len(ds)}")
print(f"first: {ds[0]}")
