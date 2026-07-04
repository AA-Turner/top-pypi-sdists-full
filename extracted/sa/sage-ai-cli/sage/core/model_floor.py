"""T1 — Hard model-capability floor.

Refuses to run agentic tasks when the loaded model is too small to follow
the SAGE protocol reliably. Empirically, 3B models hallucinate the
protocol on multi-step coding tasks (the Novellia incident).

Conservative bias: unknown models default to passing the floor (don't
block users running custom or unrecognized weights). Known small models
get blocked with an actionable suggestion.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

__all__ = [
    "AGENTIC_FLOOR_B",
    "estimate_params_b",
    "passes_floor",
    "check_capability",
    "CapabilityResult",
]


AGENTIC_FLOOR_B = 7.0    # billion params — empirical floor for protocol compliance


# Known model name → param-count (in billions). Includes Ollama-style and
# bare names. Tag suffixes (`:latest`, etc.) are stripped before lookup.
_KNOWN_MODELS: dict[str, float] = {
    # Llama family
    "llama3.2-1b": 1.0, "llama3.2-3b": 3.0, "llama3.2": 3.0,
    "llama3.1-8b": 8.0, "llama3.1": 8.0,
    "llama3.3": 70.0, "llama3.3-70b": 70.0,
    # Qwen2.5-coder
    "qwen2.5-coder-0.5b": 0.5, "qwen2.5-coder-1.5b": 1.5,
    "qwen2.5-coder-3b": 3.0, "qwen2.5-coder-7b": 7.0,
    "qwen2.5-coder-14b": 14.0, "qwen2.5-coder-32b": 32.0,
    # Qwen3
    "qwen3-coder-next": 30.0,                 # cloud-tier coder, treat as ≥30B
    # DeepSeek
    "deepseek-coder-v2": 16.0, "deepseek-r1-7b": 7.0, "deepseek-r1": 7.0,
    "deepseek-r1-32b": 32.0, "deepseek-r1-70b": 70.0,
    # Gemma
    "gemma2:2b": 2.0, "gemma2-2b": 2.0,
    "gemma2:9b": 9.0, "gemma2-9b": 9.0,
    "gemma2:27b": 27.0, "gemma2-27b": 27.0,
    "gemma4": 12.0,
    # Mistral
    "mistral-7b": 7.0, "mistral-nemo": 12.0,
    "mixtral-8x7b": 47.0, "mixtral-8x22b": 141.0,
    # Phi
    "phi-3-mini": 3.8, "phi-3-medium": 14.0, "phi-4": 14.0,
    # CodeLlama
    "codellama:7b": 7.0, "codellama-7b": 7.0,
    "codellama:13b": 13.0, "codellama-13b": 13.0,
    "codellama:34b": 34.0, "codellama-34b": 34.0,
    # StarCoder
    "starcoder2-3b": 3.0, "starcoder2-7b": 7.0, "starcoder2-15b": 15.0,
    # TinyLlama
    "tinyllama-1.1b": 1.1, "tinyllama": 1.1,
}


_PARAM_SIZE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*[bB](?![a-zA-Z])")


def _strip_prefix_and_tag(name: str) -> str:
    """`ollama:llama3.2:latest` → `llama3.2`. `llama_cpp:qwen2.5-coder-7b` → `qwen2.5-coder-7b`."""
    bare = name
    # Strip provider prefix
    for prefix in ("ollama:", "llama_cpp:", "openai:", "anthropic:", "gemini:"):
        if bare.startswith(prefix):
            bare = bare[len(prefix):]
            break
    # Strip Ollama tag (`:latest`, `:8b`, etc.)
    if ":" in bare and not bare.startswith("/"):
        bare = bare.split(":", 1)[0]
    return bare.lower()


def estimate_params_b(model_name: str) -> float | None:
    """Return param count in billions. None if unknown."""
    bare = _strip_prefix_and_tag(model_name)
    if bare in _KNOWN_MODELS:
        return _KNOWN_MODELS[bare]
    # Try to extract a "<num>b" suffix from the name
    m = _PARAM_SIZE_RE.search(bare)
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            return None
    return None


def passes_floor(model_name: str, *, floor_b: float = AGENTIC_FLOOR_B) -> bool:
    """Return True iff the model is at or above the agentic floor.

    Unknown models pass (we don't block users on weights we don't recognize).
    """
    estimated = estimate_params_b(model_name)
    if estimated is None:
        return True
    return estimated >= floor_b


@dataclass
class CapabilityResult:
    ok: bool
    model: str
    detail: str = ""
    suggestion: str = ""


def check_capability(model_name: str, *, task_kind: str = "agentic") -> CapabilityResult:
    """Decide whether `model_name` is capable enough for `task_kind`.

    task_kind ∈ {"agentic", "chat"}.
        agentic — uses tools, follows protocol; needs ≥AGENTIC_FLOOR_B
        chat    — pure conversation; small models are fine
    """
    if task_kind == "chat":
        return CapabilityResult(ok=True, model=model_name)
    estimated = estimate_params_b(model_name)
    if estimated is None:
        return CapabilityResult(
            ok=True, model=model_name,
            detail="param count unknown; allowing run",
        )
    if estimated >= AGENTIC_FLOOR_B:
        return CapabilityResult(
            ok=True, model=model_name,
            detail=f"~{estimated:g}B params (above {AGENTIC_FLOOR_B:g}B floor)",
        )
    return CapabilityResult(
        ok=False, model=model_name,
        detail=f"~{estimated:g}B params (below {AGENTIC_FLOOR_B:g}B agentic floor)",
        suggestion=(
            "Agentic tasks need a stronger model. Try:\n"
            "    sage pull qwen2.5-coder-7b\n"
            "    sage use qwen2.5-coder-7b\n"
            "Or pull an Ollama coder:\n"
            "    sage pull ollama:qwen3-coder-next\n"
            "    sage use ollama:qwen3-coder-next"
        ),
    )
