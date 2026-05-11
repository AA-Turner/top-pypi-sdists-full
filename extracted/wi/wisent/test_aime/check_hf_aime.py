"""Check HuggingFaceH4/aime_2024 dataset details."""
import sys
sys.path.insert(0, '/Users/zuzannadykiert/Desktop/Wisent/backends/wisent-open-source')
from datasets import load_dataset

ds = load_dataset('HuggingFaceH4/aime_2024', split='train')
print(f"Total rows: {len(ds)}")
print(f"Columns: {ds.column_names}")
print(f"Years: {set(ds['year'])}")
print(f"First row: {ds[0]}")
print(f"Second row: {ds[1]}")
print()
# Check answer types
for i in range(min(5, len(ds))):
    row = ds[i]
    print(f"Row {i}: answer={repr(row['answer'])} type={type(row['answer']).__name__}")
