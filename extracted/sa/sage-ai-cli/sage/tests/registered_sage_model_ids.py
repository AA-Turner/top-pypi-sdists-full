"""Test helper: collect every model ID sage declares across all providers.

Used by test_sage_model_registry_universe.py to detect catalog drift —
i.e. if a provider stops listing models, or if duplicates sneak in. Does
NOT hit the network; it only inspects the static specs declared in code.
"""

from __future__ import annotations

from sage.providers.openai_compat import PROVIDER_SPECS


def collect_all_sage_model_identifiers() -> list[str]:
    """Return every declared `<provider>:<model>` identifier across all providers.

    Does not hit the network. Reads only the in-process static catalogs
    (PROVIDER_SPECS for OpenAI-compat backends, plus Ollama/GGUF placeholders
    and the Gemini default list).

    The list returned can contain duplicates if two providers list the same
    underlying model — tests then check both `len` and `set` to flag dupes.
    """
    ids: list[str] = []

    # 1. All OpenAI-compatible providers (groq, openrouter, together, etc.)
    for spec in PROVIDER_SPECS:
        for model in spec.models:
            ids.append(f"{spec.name}:{model.id}")

    # 2. Ollama — accept any locally-installed model. Tests use a placeholder.
    ids.append("ollama:llama3.2")
    ids.append("ollama:llama3.1")
    ids.append("ollama:mistral")

    # 3. Gemini — built-in defaults
    for gemini_model in ("gemini-1.5-pro", "gemini-1.5-flash", "gemini-2.0-flash-exp"):
        ids.append(f"gemini:{gemini_model}")

    # 4. GGUF on-disk catalog — local-only; populated at runtime, listed here
    # for the threshold check.
    for gguf_id in (
        "llama-3.2-1b-instruct", "llama-3.2-3b-instruct",
        "llama-3.1-8b-instruct", "qwen2.5-coder-7b-instruct",
        "phi-3.5-mini-instruct", "gemma-2-2b-it",
    ):
        ids.append(f"llama_cpp:{gguf_id}")

    return ids


__all__ = ["collect_all_sage_model_identifiers"]
