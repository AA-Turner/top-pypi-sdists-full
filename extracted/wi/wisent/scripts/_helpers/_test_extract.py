"""Direct test of extractor on a task."""
import sys
from wisent.core.utils.infra_tools.data.loaders.lm_eval.lm_loader import LMEvalDataLoader
from wisent.extractors.lm_eval.registry.lm_extractor_registry import get_extractor

task_name = sys.argv[1]
task_obj = LMEvalDataLoader.load_lm_eval_task(task_name)
if isinstance(task_obj, dict):
    task_obj = list(task_obj.values())[0]
print(f"task obj type: {type(task_obj).__name__}")

ext = get_extractor(task_name)
print(f"extractor type: {type(ext).__name__}")

print(f"task NAME attr: {getattr(task_obj, 'NAME', None)}")
print(f"task config task: {getattr(task_obj.config, 'task', None) if hasattr(task_obj, 'config') else None}")
import inspect
src = inspect.getsource(type(ext).extract_contrastive_pairs)
print("source first 30 lines:")
for i, line in enumerate(src.split('\n')[:30]):
    print(f"  {line}")
pairs = ext.extract_contrastive_pairs(task_obj, limit=5, train_ratio=0.5)
print(f"got {len(pairs)} pairs")
if pairs:
    print(f"first: {pairs[0]}")
