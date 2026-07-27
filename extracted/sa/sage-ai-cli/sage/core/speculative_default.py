"""Item #10 — Speculative decoding on by default."""

from __future__ import annotations

from pathlib import Path

__all__ = ["enable_if_available"]


def enable_if_available() -> str:
    """Set cfg.speculative_draft_model if a small draft is locally installed
    and the user hasn't already configured one. Returns the id set, or ''."""
    from sage.config import load_config, save_config

    cfg = load_config()
    if cfg.speculative_draft_model:
        return ""  # respect user choice

    models_dir = Path.home() / ".sage" / "models"
    if not models_dir.is_dir():
        return ""

    # Look for any small draft model
    candidates = ("llama3.2-1b", "tinyllama-1.1b", "qwen2.5-coder-0.5b")
    for name in candidates:
        if (models_dir / f"{name}.gguf").is_file():
            cfg.speculative_draft_model = f"llama_cpp:{name}"
            save_config(cfg)
            return cfg.speculative_draft_model
    return ""
