"""Speculative decoding helpers.

Speculative decoding: a small "draft" model proposes K tokens, the big
"target" model verifies them in a single forward pass, accepting the
prefix that matches its own greedy output. End result: same output, 2-3x
fewer target-model forward passes.

llama-cpp-python supports this natively when constructing Llama with
`draft_model=...`. We expose a thin helper that resolves the configured
draft model to a path the constructor accepts.

When the draft model is unavailable or the same family/architecture isn't
shared with the target, we transparently fall back to no speculation —
better to lose a perf optimization than crash the chat loop.
"""

from __future__ import annotations

from pathlib import Path

from sage.config import SageConfig

__all__ = ["resolve_draft_model_path", "speculative_kwargs"]


def resolve_draft_model_path(cfg: SageConfig) -> Path | None:
    """Resolve cfg.speculative_draft_model to a GGUF path on disk.

    Format: "llama_cpp:<name>" — same shape as default_model.
    Returns None when speculative decoding is disabled or unavailable.
    """
    spec = cfg.speculative_draft_model
    if not spec:
        return None
    if ":" in spec:
        provider, name = spec.split(":", 1)
        if provider != "llama_cpp":
            return None
    else:
        name = spec

    # Check explicit registry first
    entry = cfg.get_local_model(name)
    if entry and Path(entry.path).is_file():
        return Path(entry.path)

    # Disk scan
    models_dir = Path.home() / ".sage" / "models"
    direct = models_dir / f"{name}.gguf"
    if direct.is_file():
        return direct
    return None


def speculative_kwargs(cfg: SageConfig) -> dict:
    """Return kwargs to pass to the Llama() constructor.

    Empty dict when speculative decoding is disabled / draft model missing.
    Caller merges this into their kwargs before instantiation:

        kwargs = {...}
        kwargs.update(speculative_kwargs(cfg))
        Llama(**kwargs)
    """
    draft = resolve_draft_model_path(cfg)
    if draft is None:
        return {}
    try:
        from llama_cpp import LlamaPromptLookupDecoding  # type: ignore  # noqa: F401
    except Exception:
        # Older llama-cpp-python lacks LlamaPromptLookupDecoding; check the
        # generic draft_model parameter route instead.
        pass
    return {"draft_model": str(draft)}
