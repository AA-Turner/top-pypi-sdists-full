"""Add http_timeout default value (60) to extractor __init__ methods that
require it as a positional arg. The registry _instantiate passes no kwargs,
so any required positional after self blocks instantiation.
"""
from pathlib import Path
import re

REPO = Path("/Users/zuzannadykiert/Desktop/Wisent/backends/wisent-open-source")

candidates = [
    "wisent/extractors/hf/registry/hf_task_extractors/applied/agents/tool_use/tau_bench.py",
    "wisent/extractors/hf/registry/hf_task_extractors/applied/agents/tool_use/toolemu.py",
    "wisent/extractors/hf/registry/hf_task_extractors/applied/coding/multilang_benchmarks/swe_bench/nl2bash_scicode.py",
    "wisent/extractors/hf/registry/hf_task_extractors/applied/coding/code_tasks/code_analysis/recode.py",
    "wisent/extractors/hf/registry/hf_task_extractors/evaluation/hallucination/grounding/faithbench.py",
    "wisent/extractors/hf/registry/hf_task_extractors/evaluation/reasoning/benchmarks/tag.py",
]

# Pattern: `http_timeout: int` (without default) -> `http_timeout: int = 60`
pattern = re.compile(r"http_timeout: int(?!\s*=)")

for rel in candidates:
    path = REPO / rel
    text = path.read_text()
    new = pattern.sub("http_timeout: int = 60", text)
    if new != text:
        path.write_text(new)
        print(f"fixed {rel}")
    else:
        print(f"no-change {rel}")
