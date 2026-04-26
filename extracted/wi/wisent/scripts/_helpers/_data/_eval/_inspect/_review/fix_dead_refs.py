"""Remove dead references to `lm_eval_task_data` in HF extractors that load via
self.load_dataset (HF path) but copied an unused warning line from the lm-eval template.
"""
from pathlib import Path
import re

REPO = Path("/Users/zuzannadykiert/Desktop/Wisent/backends/wisent-open-source")

candidates = [
    "wisent/extractors/hf/registry/hf_task_extractors/specialized/language/text_translation/wmt14/wmt14_en_fr.py",
    "wisent/extractors/hf/registry/hf_task_extractors/specialized/language/text_translation/wmt16/wmt16_en_ro.py",
    "wisent/extractors/hf/registry/hf_task_extractors/specialized/language/text_translation/wmt16/wmt16_de_en.py",
    "wisent/extractors/hf/registry/hf_task_extractors/specialized/language/text_translation/wmt16/wmt16_en_de.py",
    "wisent/extractors/hf/registry/hf_task_extractors/specialized/language/text_translation/wmt16/wmt_ro_en_t5_prompt.py",
    "wisent/extractors/hf/registry/hf_task_extractors/specialized/language/text_translation/wmt16/wmt16_ro_en.py",
]

pattern = re.compile(
    r"(\s*)task_name = getattr\(lm_eval_task_data, \"NAME\", type\(lm_eval_task_data\)\.__name__\)\n"
    r"(\s*)log\.warning\(\"No valid pairs extracted\", extra=\{\"task\": task_name\}\)",
)

for rel in candidates:
    path = REPO / rel
    text = path.read_text()
    new = pattern.sub(
        r'\2log.warning("No valid pairs extracted")',
        text,
    )
    if new != text:
        path.write_text(new)
        print(f"fixed {rel}")
    else:
        print(f"NO-CHANGE {rel}")
