"""Reclassify HF extractor classes that mistakenly inherit HuggingFaceBenchmarkExtractor
but use the LMEvalBenchmarkExtractor method signature (lm_eval_task_data positional).

This script does NOT touch the body of _extract_pair_from_doc — it only:
1. Replaces the import `from wisent.extractors.hf.atoms import HuggingFaceBenchmarkExtractor`
   with `from wisent.extractors.lm_eval.atoms import LMEvalBenchmarkExtractor`.
2. Replaces `(HuggingFaceBenchmarkExtractor)` in the class declaration with
   `(LMEvalBenchmarkExtractor)`.
3. Adds `*, train_ratio: float,` to extract_contrastive_pairs signatures that take
   lm_eval_task_data but don't yet pass train_ratio through.
4. Adds `train_ratio=train_ratio` to the load_docs() call inside.

Run from the repo root.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

REPO = Path("/Users/zuzannadykiert/Desktop/Wisent/backends/wisent-open-source")

# Find all HF extractors that use lm_eval_task_data
out = subprocess.run(
    ["grep", "-rln", "class .*HuggingFaceBenchmarkExtractor",
     str(REPO / "wisent/extractors/hf"), "--include=*.py"],
    capture_output=True, text=True,
)
candidates = [Path(line) for line in out.stdout.splitlines() if line]

results = []
for path in candidates:
    text = path.read_text()
    if "lm_eval_task_data" not in text:
        continue
    if "self.load_docs(lm_eval_task_data" not in text:
        # Doesn't actually use the lm-eval load path; skip.
        results.append((str(path.relative_to(REPO)), "skipped (no load_docs call)"))
        continue

    new = text
    # 1. Imports
    new = new.replace(
        "from wisent.extractors.hf.atoms import HuggingFaceBenchmarkExtractor",
        "from wisent.extractors.lm_eval.atoms import LMEvalBenchmarkExtractor",
    )
    # 2. Class base
    new = re.sub(
        r"\(HuggingFaceBenchmarkExtractor\)",
        "(LMEvalBenchmarkExtractor)",
        new,
    )
    # 3. extract_contrastive_pairs signature: add `*, train_ratio: float,`
    #    after the last positional/optional arg before the closing paren.
    #    We look for the pattern:
    #        def extract_contrastive_pairs(
    #            self,
    #            lm_eval_task_data: ConfigurableTask,
    #            limit: int | None = None,
    #            preferred_doc: str | None = None,
    #        ) -> ...
    sig_pattern = re.compile(
        r"(def extract_contrastive_pairs\(\s*self,\s*lm_eval_task_data:[^)]*?preferred_doc:[^)]*?,)\s*(\)\s*->\s*list\[ContrastivePair\]:)",
        re.DOTALL,
    )
    if "train_ratio" not in new:
        new = sig_pattern.sub(r"\1\n        *,\n        train_ratio: float,\n    \2", new)

    # 4. load_docs call: add train_ratio=train_ratio if not present
    load_pat = re.compile(
        r"self\.load_docs\(lm_eval_task_data,\s*max_items,\s*preferred_doc=preferred_doc\)"
    )
    new = load_pat.sub(
        "self.load_docs(lm_eval_task_data, max_items, preferred_doc=preferred_doc, train_ratio=train_ratio)",
        new,
    )

    if new != text:
        path.write_text(new)
        results.append((str(path.relative_to(REPO)), "fixed"))
    else:
        results.append((str(path.relative_to(REPO)), "no-change"))

for p, status in results:
    print(f"{status:12s} {p}")
