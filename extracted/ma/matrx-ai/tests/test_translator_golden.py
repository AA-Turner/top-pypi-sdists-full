"""Translator-level golden check for the flipped (DB-driven) chat translators.

The engine test (``test_chat_param_golden``) holds ``canonicalize -> outbound``
byte-identical to the frozen legacy output. THIS test closes the remaining gap
— the merge of those params into the actual provider request inside each
flipped translator: for every golden case it builds a real ``UnifiedConfig``,
runs the REAL translator with a profile compiled from the fixture's rules, and
asserts the extracted param subset equals the golden byte-for-byte.

A family appears in ``_FLIPPED`` the commit its translator flips; when the last
one lands, this file covers every chat family permanently.
"""

from __future__ import annotations

import json
from typing import Any

import pytest

from matrx_ai.catalog.controls import flatten_dotted
from matrx_ai.config import TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.testing.profile_factory import make_profile

from test_chat_param_golden import FIXTURE_DIR, load_golden

# Structural request keys per wire shape — everything else is a param the
# golden freezes. Mirrors scripts/dump_chat_param_golden.py (the dump-time
# extractors); the two must stay in sync when a new structural key appears.
_STRUCTURAL_OPENAI = {
    "model", "input", "tools", "text", "tool_choice",
    "parallel_tool_calls", "include", "store", "stream",
}
_STRUCTURAL_CHAT = {
    "model", "messages", "stream", "tools", "tool_choice",
    "response_format", "parallel_tool_calls",
}
_STRUCTURAL_XAI = {"model", "messages", "tools", "tool_choice", "response_format",
                   "parallel_tool_calls"}
_STRUCTURAL_ANTHROPIC = {"model", "messages", "system", "tools", "tool_choice", "stream"}


def _extract_openai(req: dict[str, Any]) -> dict[str, Any]:
    return flatten_dotted({k: v for k, v in req.items() if k not in _STRUCTURAL_OPENAI})


def _extract_chat(req: dict[str, Any]) -> dict[str, Any]:
    return flatten_dotted({k: v for k, v in req.items() if k not in _STRUCTURAL_CHAT})


def _extract_xai(req: dict[str, Any]) -> dict[str, Any]:
    return flatten_dotted({k: v for k, v in req.items() if k not in _STRUCTURAL_XAI})


def _extract_anthropic(req: dict[str, Any]) -> dict[str, Any]:
    return flatten_dotted({k: v for k, v in req.items() if k not in _STRUCTURAL_ANTHROPIC})


def _extract_google(result: Any) -> dict[str, Any]:
    cfg = result["config"]
    out: dict[str, Any] = {}
    for key in ("temperature", "max_output_tokens", "top_p", "top_k"):
        value = getattr(cfg, key, None)
        if value is not None:
            out[key] = value
    tc = getattr(cfg, "thinking_config", None)
    if tc is not None:
        for key in ("include_thoughts", "thinking_budget", "thinking_level"):
            value = getattr(tc, key, None)
            enum_value = getattr(value, "value", None)
            if isinstance(enum_value, str):
                value = enum_value.lower()
            if value is not None:
                out[f"thinking_config.{key}"] = value
    return out


def _translator_for(family: str):
    """(translator instance, extractor) for a FLIPPED family — None if that
    family's translator has not flipped yet."""
    if family.startswith("openai"):
        from matrx_ai.providers.openai.translator import OpenAITranslator

        return OpenAITranslator(), _extract_openai
    if family.startswith("groq"):
        from matrx_ai.providers.groq.translator import GroqTranslator

        return GroqTranslator(), _extract_chat
    if family.startswith("cerebras"):
        from matrx_ai.providers.cerebras.translator import CerebrasTranslator

        return CerebrasTranslator(), _extract_chat
    if family.startswith("xai"):
        from matrx_ai.providers.xai.translator import XAITranslator

        return XAITranslator(), _extract_xai
    if family.startswith("google"):
        from matrx_ai.providers.google.translator import GoogleTranslator

        return GoogleTranslator(), _extract_google
    if family.startswith("anthropic"):
        from matrx_ai.providers.anthropic.translator import AnthropicTranslator

        return AnthropicTranslator(), _extract_anthropic
    if family.startswith("together"):
        from matrx_ai.providers.together.translator import TogetherTranslator

        return TogetherTranslator(), _extract_chat
    from matrx_ai.providers.generic_openai.translator import GenericOpenAITranslator

    return GenericOpenAITranslator(), _extract_chat


# Families whose translator has flipped onto profile.controls. Grows per flip
# commit; ends as every golden variant.
_FLIPPED: tuple[str, ...] = (
    "openai_standard",
    "openai_reasoning",
    "openai_reasoning_minimal",
    "openai_reasoning_xhigh",
    "groq_standard",
    "groq_reasoning",
    "groq_reasoning_toggle",
    "cerebras_standard",
    "cerebras_reasoning",
    "cerebras_reasoning_toggle",
    "xai_standard",
    "xai_reasoning",
    "google_thinking",
    "google_thinking_3",
    "anthropic_standard",
    "anthropic_adaptive",
    "together_text_standard",
    "huggingface_standard",
    "generic_openai_standard",
)


def _flipped_variant_keys() -> list[str]:
    keys = []
    for path in sorted(FIXTURE_DIR.glob("*.json")):
        payload = json.loads(path.read_text())
        if payload["family"] in _FLIPPED:
            keys.append(path.stem)
    return keys


@pytest.mark.parametrize("variant_key", _flipped_variant_keys())
def test_flipped_translator_reproduces_golden(variant_key: str) -> None:
    payload = load_golden(variant_key)
    profile = make_profile(
        model_name=payload["model"],
        wire_format=payload["wire_format"],
        rules=payload["rules"],
        value_orders=payload["value_orders"],
    )
    translator, extract = _translator_for(payload["family"])

    failures: list[str] = []
    for case in payload["cases"]:
        config = UnifiedConfig(
            model=payload["model"],
            messages=[UnifiedMessage(role="user", content=[TextContent(text="hi")])],
            **case["config"],
        )
        request = translator.build_request(config, profile)
        got = extract(request)
        if got != case["params"]:
            failures.append(
                f"config={json.dumps(case['config'], sort_keys=True)}\n"
                f"  golden    : {json.dumps(case['params'], sort_keys=True)}\n"
                f"  translator: {json.dumps(got, sort_keys=True, default=str)}"
            )
    if failures:
        pytest.fail(
            f"{variant_key}: {len(failures)}/{len(payload['cases'])} translator "
            f"outputs diverge from the golden:\n" + "\n".join(failures[:8])
        )
