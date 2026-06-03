import sys
from wisent.core.utils.infra_tools.data.loaders.lm_eval.lm_loader import LMEvalDataLoader

task_name = sys.argv[1]
try:
    task = LMEvalDataLoader.load_lm_eval_task(task_name)
    if isinstance(task, dict):
        for k, v in task.items():
            print(f'subtask: {k}')
            task = v
            break
    print('LOAD OK')
    if task.has_test_docs():
        docs = list(task.test_docs())[:2]
    elif task.has_validation_docs():
        docs = list(task.validation_docs())[:2]
    else:
        docs = list(task.training_docs())[:2]
    print(f'docs: {len(docs)}')
    for d in docs[:1]:
        print('keys:', list(d.keys()))
        print('doc:', d)
except Exception as e:
    import traceback
    traceback.print_exc()
    print(f'FAIL: {type(e).__name__}: {e}')
