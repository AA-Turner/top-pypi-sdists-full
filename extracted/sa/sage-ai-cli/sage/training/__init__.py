"""Local model fine-tuning + shared GCS training corpus.

This package adds a real fine-tuning path alongside the existing
Modelfile-baking path in `main._train_ollama_model`. Both ship as `sage train`
subcommands:

    sage train <model>             — Modelfile/system-prompt bake (existing)
    sage finetune <model> [...]    — actual LoRA weights training (new)

Architecture:
    corpus.py    — GCS-backed shared training data; per-project snapshots
    finetune.py  — QLoRA training; MLX on Apple Silicon, Unsloth fallback
    cache.py     — adapter cache (don't retrain if same base+corpus exists)

Cost-control principles:
  - Lazy-by-default: only train when a model is first used in a project
  - Adapter cache keyed on (base_model_hash, corpus_hash) — repeat = free
  - Embedding-based dedup so corpus doesn't grow with copy/paste
  - Per-model --max-steps cap with sensible defaults
"""

from __future__ import annotations

__all__ = ["corpus", "finetune", "cache"]
