import sys
from wisent.extractors.lm_eval.registry.lm_extractor_registry import get_extractor

task = sys.argv[1]
ext = get_extractor(task)
print(f"Task: {task}")
print(f"Extractor: {type(ext).__name__}")
print(f"Module: {type(ext).__module__}")
import inspect
print(f"File: {inspect.getfile(type(ext))}")
