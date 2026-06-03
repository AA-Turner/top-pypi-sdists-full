"""Check afridiacritics and adr lm-eval task loading."""
import sys, os
sys.path.insert(0, '/Users/zuzannadykiert/Desktop/Wisent/backends/wisent-open-source')
os.environ['HF_DATASETS_TRUST_REMOTE_CODE'] = '1'

from wisent.core.utils.infra_tools.data.loaders.lm_eval.lm_loader import LMEvalDataLoader

loader = LMEvalDataLoader()

# Test: load afridiacritics via loader (now should map to adr)
try:
    task_obj = loader.load_lm_eval_task('afridiacritics')
    print('load_lm_eval_task afridiacritics result type:', type(task_obj).__name__)
    if isinstance(task_obj, dict):
        print('  subtasks:', list(task_obj.keys())[:5])
        print('  count:', len(task_obj))
except Exception as e:
    print('load_lm_eval_task afridiacritics error:', e)
    import traceback
    traceback.print_exc()
