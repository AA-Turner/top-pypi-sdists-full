current = set(["name", "age", "city"])
expected = set(["name", "age","another"])

print(expected.issubset(current))
print(f"missing: {expected - current}")