import sys
import importlib

# Trigger the __init__.py
import wisent.extractors.lm_eval.registry.lm_task_extractors

print(f"__path__ has {len(wisent.extractors.lm_eval.registry.lm_task_extractors.__path__)} entries")
for p in wisent.extractors.lm_eval.registry.lm_task_extractors.__path__[:5]:
    print(f"  {p}")

try:
    mod = importlib.import_module("wisent.extractors.lm_eval.registry.lm_task_extractors.ifeval")
    print(f"OK: {mod}")
    print(f"  IFEvalExtractor: {hasattr(mod, 'IFEvalExtractor')}")
except Exception as e:
    print(f"FAIL: {type(e).__name__}: {e}")
