"""Auto-instrumentation for the Google Gen AI SDK (``google.genai``).

The client that replaced ``google.generativeai`` (traced by ``gemini_legacy.py``). An
install carrying only this one was traced by nothing at all — a direct Gemini call
produced no trace and no spans, so there was no record to be missing a field from.

Gemini passes the system prompt out of band, on the request config's
``system_instruction`` rather than as a message, so it needs lifting onto the span
explicitly. OpenInference's ``google_genai`` instrumentor reads the same field off the
same config; it flattens it into an input message with role ``system``, where our wire
contract gives the system prompt its own ``system_prompt`` key. OTel's GenAI
semconv has since settled on a dedicated ``gen_ai.system_instructions`` attribute rather
than a message, so a field of its own is the converging shape — the name stays ours.

Covers ``generate_content`` on both the sync and async model classes. ``generate_content_stream``
is left alone, as it was before: a streamed span needs its usage read after the stream is
consumed, which is a separate piece of work from carrying the system prompt.
"""

from __future__ import annotations

import logging
from typing import Any

from aigie._system_prompt import system_prompt_text
from aigie.auto_instrument._gemini_span import (
    PROVIDER,
    TEXT_LIMIT,
    traced,
    traced_async,
)

logger = logging.getLogger(__name__)

_patched = False


def patch_google_genai() -> None:
    """Patch the ``Models`` classes rather than the client, so every client instance is
    covered. Idempotent; silent when the library is absent."""
    global _patched
    try:
        models_module = _models_module()
        if models_module is None or _patched:
            return
        for cls_name, wrap in (("Models", traced), ("AsyncModels", traced_async)):
            _patch_class(getattr(models_module, cls_name, None), wrap)
        _patched = True
        logger.debug("Patched google.genai for auto-instrumentation")
    except Exception as exc:  # noqa: BLE001 - instrumentation must never break the caller
        logger.warning("Failed to patch google.genai: %s", exc)


def _models_module() -> Any:
    try:
        from google.genai import models as genai_models
    except ImportError:
        return None
    return genai_models


def _patch_class(cls: Any, wrap: Any) -> None:
    if cls is None:
        return
    original = getattr(cls, "generate_content", None)
    if original is None or getattr(original, "_aigie_patched", False) is True:
        return
    cls.generate_content = wrap(original, _describe)


def _system_instruction(config: Any) -> str:
    """The system prompt off a ``GenerateContentConfig``, an object or a dict."""
    if config is None:
        return ""
    instruction = (
        config.get("system_instruction")
        if isinstance(config, dict)
        else getattr(config, "system_instruction", None)
    )
    return system_prompt_text(instruction)


def _model_name(kwargs: dict[str, Any]) -> str:
    """The bare model id, however the caller spelled it.

    This client accepts ``models/gemini-x`` and ``gemini-x`` as the same call — its own
    ``t_model`` returns an already-prefixed name unchanged — so without stripping, one
    model reaches the platform under two names and splits in per-model grouping. Same
    unification the legacy client needs for the opposite reason: it *adds* the prefix.
    """
    model = kwargs.get("model")
    if not isinstance(model, str):
        return str(model or PROVIDER)
    return model.removeprefix("models/") or PROVIDER


def _describe(
    _receiver: Any, _args: tuple[Any, ...], kwargs: dict[str, Any]
) -> tuple[str, dict[str, Any]]:
    """The model name and span input for this call.

    ``generate_content`` is keyword-only here (``def generate_content(self, *, model,
    contents, config=None)``), so reading kwargs is complete for any call the client
    accepts, and the receiver is not needed. Positional args are *not* proof of nothing
    to read: the wrapper's own ``*args`` absorbs them, so a positional call reaches us
    and only raises ``TypeError`` from the original further down — leaving a failure span
    with model ``gemini`` and the literal string ``"None"`` as its prompt, for a call that
    never left the process.
    Inherited, and cheap to live with: the client rejects such a call regardless.
    """
    model_name = _model_name(kwargs)
    contents = kwargs.get("contents")
    span_input: dict[str, Any] = {
        "provider": PROVIDER,
        "model": model_name,
        "prompt": (system_prompt_text(contents) or str(contents))[:TEXT_LIMIT],
    }
    instruction = _system_instruction(kwargs.get("config"))
    if instruction:
        span_input["system_prompt"] = instruction
    return model_name, span_input
