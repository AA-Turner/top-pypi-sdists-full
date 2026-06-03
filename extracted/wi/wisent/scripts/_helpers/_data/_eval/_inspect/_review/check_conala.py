from datasets import load_dataset

try:
    ds = load_dataset("neulab/conala", split="train", trust_remote_code=True)
    print(f"OK len={len(ds)}")
    print(f"keys={list(ds[0].keys())}")
    print(f"sample={ds[0]}")
except Exception as e:
    print(f"FAIL {type(e).__name__}: {e}")
