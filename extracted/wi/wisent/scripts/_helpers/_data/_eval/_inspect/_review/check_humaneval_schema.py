from datasets import load_dataset

ds = load_dataset(
    "loubnabnl/humaneval_infilling",
    "HumanEval-SingleLineInfilling",
    split="test",
    trust_remote_code=True,
)
print("KEYS:", list(ds[0].keys()))
print()
print("SAMPLE:")
for k, v in ds[0].items():
    val = str(v)
    if len(val) > 200:
        val = val[:200] + "..."
    print(f"  {k!r}: {val!r}")
