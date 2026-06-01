"""Framework-agnostic helpers for extracting LLM metadata from LangChain-style
callback arguments. Used by framework bindings (LangGraph today; LangChain
in a follow-up) when they receive on_llm_start / on_chat_model_start.

Pure functions only — no I/O, no global state.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ModelInfo:
    display_name: str
    model_id: str | None  # canonical identifier suitable for cost-tracking lookups


_GENERIC_CLASS_NAME_PREFIXES = ("Chat", "LLM")
_GENERIC_CLASS_NAME_EXACT = frozenset({"LLM Call"})


_MODEL_KEYS = ("model", "model_name", "model_id")


def _probe_model(source: dict[str, Any] | None) -> str | None:
    """Pull the canonical model identifier from a dict using known key names.

    OpenAI uses ``model_name``; Anthropic and Google use ``model``; Bedrock
    (langchain_aws ChatBedrockConverse) exposes ``model_id``. Probing all
    three lets a single resolver handle every provider.
    """
    if not source:
        return None
    for key in _MODEL_KEYS:
        value = source.get(key)
        if value:
            return str(value)
    return None


def _resolve_from_serialized(
    serialized: dict[str, Any],
) -> tuple[str, str | None]:
    """Return (display_name, model_id) from a serialized LLM dump.

    Walks the legacy LangChain serialization shape: a ``name`` field plus an
    ``id`` that's either a dotted path list or a string. When ``name`` is
    absent, the last element of the ``id`` list becomes the display name.
    """
    llm_id = serialized.get("id")
    if isinstance(llm_id, list) and llm_id:
        joined = ".".join(str(x) for x in llm_id)
        name = serialized.get("name") or (llm_id[-1] if len(llm_id) > 1 else llm_id[0])
        return str(name), joined
    if llm_id:
        return str(serialized.get("name") or llm_id), str(llm_id)
    return str(serialized.get("name") or "LLM Call"), None


def extract_model_info(
    serialized: dict[str, Any] | None,
    invocation_params: dict[str, Any] | None,
    metadata: dict[str, Any] | None = None,
) -> ModelInfo:
    """Resolve a display name + canonical model identifier.

    Priority:
      1. serialized["kwargs"][model | model_name | model_id]   (LangChain LLM class kwargs)
      2. invocation_params[model | model_name | model_id]      (per-call override)
      3. metadata["ls_model_name"]                              (LangSmith hint; populated by langchain_aws etc.)
      4. serialized["name"]                                     (LangChain class name)
      5. serialized["id"]                                       (qualified class path)
      6. fallback "LLM Call"

    When the class name from (4) is generic (e.g. "ChatOpenAI",
    "ChatBedrockConverse") AND a real model is found from (1)–(3), the real
    model id becomes the display name.
    """
    if serialized:
        display_name, model_id = _resolve_from_serialized(serialized)
        actual_model = _probe_model(serialized.get("kwargs"))
    else:
        display_name, model_id, actual_model = "LLM Call", None, None

    if not actual_model:
        actual_model = _probe_model(invocation_params)
    if not actual_model and metadata:
        actual_model = metadata.get("ls_model_name") or None

    if actual_model:
        if _is_generic_class_name(display_name):
            display_name = actual_model
        model_id = actual_model

    return ModelInfo(display_name=display_name, model_id=model_id)


def _is_generic_class_name(name: str) -> bool:
    if name in _GENERIC_CLASS_NAME_EXACT:
        return True
    return any(prefix in name for prefix in _GENERIC_CLASS_NAME_PREFIXES)


def extract_prompt_content(  # noqa: PLR0915 — message normalization across 3 input shapes
    prompts: list[Any] | None,
) -> tuple[str | None, list[dict[str, Any]]]:
    """Split a LangChain prompts list into (system_prompt, messages[]).

    Accepts plain strings, LangChain Message objects (anything with a
    ``type`` and ``content`` attribute), or {"role","content"} dicts.
    System messages are returned separately; everything else lands in the
    messages list with role defaulted to "user".
    """
    if not prompts:
        return None, []
    system_prompt: str | None = None
    messages: list[dict[str, Any]] = []
    for prompt in prompts:
        if isinstance(prompt, str):
            messages.append({"role": "user", "content": prompt})
            continue
        if hasattr(prompt, "content"):
            role = getattr(prompt, "type", "user")
            content = prompt.content
            if isinstance(role, str) and role.lower() == "system":
                system_prompt = content
            else:
                messages.append({"role": role, "content": content})
            continue
        if isinstance(prompt, dict):
            role = prompt.get("role", "user")
            content = prompt.get("content", str(prompt))
            if isinstance(role, str) and role.lower() == "system":
                system_prompt = content
            else:
                messages.append({"role": role, "content": content})
    return system_prompt, messages


_LLM_PARAM_KEYS = (
    "temperature",
    "top_p",
    "top_k",
    "frequency_penalty",
    "presence_penalty",
    "logprobs",
    "logit_bias",
)
_LLM_PARAM_ALIASES = {
    "max_tokens": ("max_tokens", "max_tokens_to_sample"),  # Anthropic uses *_to_sample
    "stop": ("stop", "stop_sequences"),
}


def extract_llm_params(
    invocation_params: dict[str, Any] | None,
    kwargs: dict[str, Any] | None,
) -> dict[str, Any]:
    """Extract canonical LLM sampling parameters.

    Pulls from invocation_params first (LangChain canonical), falls back to
    kwargs for older LangChain versions. Normalizes Anthropic's
    ``max_tokens_to_sample`` to ``max_tokens`` and ``stop_sequences`` to ``stop``.
    Drops keys whose value is None.
    """
    source = invocation_params if invocation_params else (kwargs or {})
    out: dict[str, Any] = {}
    for key in _LLM_PARAM_KEYS:
        value = source.get(key)
        if value is not None:
            out[key] = value
    for canonical, aliases in _LLM_PARAM_ALIASES.items():
        for alias in aliases:
            if source.get(alias) is not None:
                out[canonical] = source[alias]
                break
    return out
