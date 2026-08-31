"""Auto-instrumentation for the legacy Google Generative AI client.

``google.generativeai`` is the client Google has since replaced with ``google.genai``
(see ``google_genai.py`` for that one). It is end-of-life and still in service, so it
keeps its tracing.

Lifted out of ``auto_instrument/llm.py`` rather than fixed in place: that file was 1,172
lines against a 500-line policy and carries no exemption, so editing it there would have
failed the length gate. Landing this took the rest of that file with it, leaving ``llm.py``
at 256 lines. Two defects came out with it:

* **The system prompt was never recorded.** This client takes ``system_instruction`` on
  the *model*, not the request — ``GenerativeModel.__init__`` normalizes it to a
  protobuf ``Content`` and keeps it as ``_system_instruction`` — while the patch read
  only ``contents``. The patched method already held ``self``, so it was in reach.
* **The span was never emitted.** The patch constructed a ``SpanContext``, set input and
  output on it, and dropped it. Spans ship exactly once, from ``__aexit__``, so a direct
  Gemini call produced a trace with no spans at all.
"""

from __future__ import annotations

import logging
from typing import Any

from aigie._system_prompt import system_prompt_text
from aigie.auto_instrument._gemini_span import (
    PROVIDER,
    TEXT_LIMIT,
    traced,
)

logger = logging.getLogger(__name__)

_patched = False


def patch_gemini_legacy() -> None:
    """Patch ``GenerativeModel.generate_content``. Idempotent; silent when absent."""
    global _patched
    try:
        model_cls = _generative_model()
        if model_cls is None or _patched:
            return
        original = getattr(model_cls, "generate_content", None)
        if original is None or getattr(original, "_aigie_patched", False) is True:
            return
        model_cls.generate_content = traced(original, _describe)
        _patched = True
        logger.debug("Patched google.generativeai for auto-instrumentation")
    except Exception as exc:  # noqa: BLE001 - instrumentation must never break the caller
        logger.warning("Failed to patch google.generativeai: %s", exc)


def _generative_model() -> Any:
    """The legacy ``GenerativeModel`` class, or None when the client is not installed.

    Importing it emits a ``FutureWarning`` about the package being end-of-life. That is
    the host's own import's business to announce, not ours to repeat on every
    ``initialize()``, so it is suppressed for the duration of this one.
    """
    import warnings

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", FutureWarning)
            import google.generativeai as genai
    except ImportError:
        return None
    return getattr(genai, "GenerativeModel", None)


def _model_name(model: Any) -> str:
    """The model's own name, however this version of the client stores it.

    This client stores it fully qualified — ``GenerativeModel.__init__`` prepends
    ``models/`` — while ``google.genai`` takes the bare id. Left alone, the same model
    reaches the platform under two names depending on which client made the call, which
    splits it in per-model grouping. Pricing is *not* affected: ``normalize_model_name``
    strips the prefix before the rate lookup. Stripping it here is what OpenLLMetry's
    instrumentor does with the same attribute.
    """
    name = getattr(model, "model_name", None) or getattr(model, "_model_name", None)
    if not isinstance(name, str):
        return PROVIDER
    return name.removeprefix("models/") or PROVIDER


def _system_instruction(model: Any) -> str:
    """The model-level system instruction, flattened to text.

    Held as a protobuf ``Content`` whose ``parts`` carry the text — which is why
    ``system_prompt_text`` has to treat a repeated proto field as a sequence of pieces.
    """
    instruction = getattr(model, "system_instruction", None)
    if instruction is None:
        instruction = getattr(model, "_system_instruction", None)
    return system_prompt_text(instruction)


def _describe(
    model: Any, args: tuple[Any, ...], kwargs: dict[str, Any]
) -> tuple[str, dict[str, Any]]:
    """The model name and span input for this call.

    ``contents`` is positional-or-keyword on this client, so both spellings are read.
    The ``prompt`` key and its truncation are inherited unchanged — the user prompt is
    its own defect, tracked separately from the system prompt.
    """
    model_name = _model_name(model)
    contents = args[0] if args else kwargs.get("contents", "")
    prompt = contents if isinstance(contents, str) else str(contents)
    span_input: dict[str, Any] = {
        "provider": PROVIDER,
        "model": model_name,
        "prompt": prompt[:TEXT_LIMIT],
    }
    instruction = _system_instruction(model)
    if instruction:
        span_input["system_prompt"] = instruction
    return model_name, span_input
