"""Find the correct HuggingFace dataset name for AIME 2025."""
import sys
sys.path.insert(0, '/Users/zuzannadykiert/Desktop/Wisent/backends/wisent-open-source')
from datasets import load_dataset

candidates = [
    ('HuggingFaceH4/aime_2025', 'train'),
    ('HuggingFaceH4/aime_2025', None),
    ('MathArena/aime_2025', 'train'),
    ('MathArena/aime_2025', None),
    ('Maxwell-Jia/AIME_2025', 'train'),
    ('Maxwell-Jia/AIME_2025', None),
    ('di-dimitrov/aime-2025', 'train'),
    ('di-dimitrov/aime-2025', None),
]

for name, split in candidates:
    try:
        if split:
            ds = load_dataset(name, split=split)
        else:
            ds = load_dataset(name)
        print(f'SUCCESS: {name} (split={split})')
        if hasattr(ds, 'features'):
            print(f'  Features: {list(ds.features.keys())}')
            if len(ds) > 0:
                print(f'  First row: {ds[0]}')
        elif hasattr(ds, 'keys'):
            print(f'  Splits: {list(ds.keys())}')
            for sp in ds.keys():
                print(f'  Split {sp} columns: {ds[sp].column_names}')
                if len(ds[sp]) > 0:
                    print(f'  First row in {sp}: {ds[sp][0]}')
    except Exception as e:
        print(f'FAIL: {name} (split={split}): {e}')
