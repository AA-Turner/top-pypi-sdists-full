from __future__ import annotations
import portalocker
import fasteners
import os
# ---- Enforce full offline mode and disable parallel tokenizer forks ----
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")
os.environ.setdefault("TRANSFORMERS_NO_ADVISORY_WARNINGS", "1")
# Optional: Hugging Face local cache directory for safety
os.environ.setdefault("HF_HOME", "/mnt/24T/hugging_face/cache")
