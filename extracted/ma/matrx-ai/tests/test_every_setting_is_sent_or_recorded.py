"""PB-03 defects 52 + 53 (L23): every setting is sent, or a settings_adjusted record says why.

Defect 52: ``store`` and ``parallel_tool_calls`` were dropped for Haiku and Gemini and
appeared in no record — the canonical pass (``canonical_settings_from_config``) never
carried them, so the rules gate could neither send nor record them. Defect 53: Gemini's
offering marks ``internal_web_search`` supported, but on Gemini 2.5-class models the
translator cannot ride a built-in tool beside the agent's function tools, and skipped the
search without a word.

Per provider, through the real chokepoint (``translate_request``: capability gates + rules
gate + translator), a kitchen-sink UnifiedConfig must, for EVERY key it sets, either put the
key's MEANING on the wire (``wire_meaning.meaning_paths``) or publish an Adjustment naming it.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.catalog.wire_meaning import meaning_paths
from matrx_ai.config import TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.providers import outbound_params
from matrx_ai.providers.snapshot import wire_json
from matrx_ai.providers.unified_client import UnifiedAIClient
from matrx_ai.testing.profile_factory import make_profile

CAPS = {
    "input": ["text"],
    "output": ["text"],
    "features": ["function_calling", "web_search", "url_context"],
    "interaction": "turn",
}
WIRES = {
    "anthropic_chat": "claude-haiku-5-5",
    "openai_chat": "gpt-5-nano",
    "google_chat": "gemini-flash-lite-latest",
}
DROP = {"drop": True, "why": "this api's models take no such setting"}
FN_TOOL = {
    "name": "lookup",
    "description": "look something up",
    "parameters": {"type": "object", "properties": {"q": {"type": "string"}}},
}

# Every key we ask for, and whether we expect its MEANING on the wire when supported.
SET_KEYS = ("store", "parallel_tool_calls", "internal_web_search")


def _rules(wire: str) -> dict[str, Any]:
    rules: dict[str, Any] = {"temperature": {}, "max_output_tokens": {}}
    for key in SET_KEYS:
        # openai takes store/parallel/search; anthropic + google drop store/parallel
        if wire != "openai_chat" and key in ("store", "parallel_tool_calls"):
            rules[key] = DROP
        else:
            rules[key] = {"supported": True} if key == "internal_web_search" else {}
    return rules


def _config(model: str, *, tools: bool) -> UnifiedConfig:
    return UnifiedConfig(
        model=model,
        messages=[UnifiedMessage(role="user", content=[TextContent(text="hi")])],
        store=True,
        parallel_tool_calls=False,
        internal_web_search=True,
    )


async def _run(monkeypatch, wire: str, *, tools: bool):
    import matrx_ai.catalog.resolve as resolve_mod

    profile = make_profile(
        model_name=WIRES[wire], wire_format=wire, capabilities=dict(CAPS), rules=_rules(wire)
    )

    async def _resolve(*_a: Any, **_k: Any):
        return profile

    monkeypatch.setattr(resolve_mod, "resolve_call_profile", _resolve)
    published: list[Any] = []
    real = outbound_params.publish_settings_adjustments

    def _spy(adjustments, **kw):
        published.extend(adjustments)
        return real(adjustments, **kw)

    monkeypatch.setattr(outbound_params, "publish_settings_adjustments", _spy)
    cfg = _config(WIRES[wire], tools=tools)
    out = await UnifiedAIClient().translate_request(SimpleNamespace(config=cfg, debug=False))
    return wire_json(out), published


@pytest.mark.asyncio
@pytest.mark.parametrize("wire", sorted(WIRES))
async def test_store_and_parallel_tool_calls_are_sent_or_recorded(monkeypatch, wire: str) -> None:
    payload, published = await _run(monkeypatch, wire, tools=False)
    named = {a.key for a in published}
    for key in ("store", "parallel_tool_calls"):
        if key in named:
            continue
        assert meaning_paths(payload, key), (
            f"{wire}: {key} neither on the wire nor in any settings_adjusted record"
        )
    if wire != "openai_chat":
        assert {"store", "parallel_tool_calls"} <= named, f"{wire}: dropped without a record: {named}"


# --- defect 53: Gemini 2.5-class search beside function tools -------------------------
def _google_profile(variant_key: str):
    from test_chat_param_golden import load_golden

    payload = load_golden(variant_key)
    return make_profile(
        model_name=payload["model"],
        wire_format=payload["wire_format"],
        rules=payload["rules"],
        value_orders=payload["value_orders"],
    )


_FAKE_FN = {"name": "ctx_get", "description": "get", "parameters": {"type": "object", "properties": {}}}


def _gcfg(**kw) -> UnifiedConfig:
    from matrx_ai.config import MessageList

    return UnifiedConfig(
        model="gemini-flash-lite-latest",
        messages=MessageList(_messages=[UnifiedMessage(role="user", content=[TextContent(text="hi")])]),
        **kw,
    )


def _search_on_wire(tools: Any) -> bool:
    return any(getattr(t, "google_search", None) is not None for t in (tools or []))


@pytest.mark.parametrize("flag", ["internal_web_search", "internal_url_context"])
def test_google_builtin_tool_skipped_beside_function_tools_is_recorded(monkeypatch, flag: str) -> None:
    """The either/or on Gemini 2.5-class models is real (400 otherwise) — but never silent."""
    from matrx_ai.providers.google.translator import GoogleTranslator

    tr = GoogleTranslator()
    monkeypatch.setattr(tr, "build_provider_tools", lambda config, provider: [_FAKE_FN])
    published: list[Any] = []
    monkeypatch.setattr(
        outbound_params,
        "publish_settings_adjustments",
        lambda adjustments, **kw: published.extend(adjustments),
    )
    cfg = tr.to_google(_gcfg(**{flag: True}), _google_profile("google_thinking"))["config"]
    on_wire = _search_on_wire(cfg.tools) if flag == "internal_web_search" else any(
        getattr(t, "url_context", None) is not None for t in (cfg.tools or [])
    )
    named = [a for a in published if a.key == flag]
    assert on_wire or named, f"{flag} neither sent nor recorded"
    if not on_wire:
        assert named[0].action == "dropped" and "function" in named[0].reason


def test_google_gemini3_search_beside_function_tools_is_sent_and_not_recorded_as_dropped(monkeypatch) -> None:
    from matrx_ai.providers.google.translator import GoogleTranslator

    tr = GoogleTranslator()
    monkeypatch.setattr(tr, "build_provider_tools", lambda config, provider: [_FAKE_FN])
    published: list[Any] = []
    monkeypatch.setattr(
        outbound_params, "publish_settings_adjustments", lambda adjustments, **kw: published.extend(adjustments)
    )
    cfg = tr.to_google(_gcfg(internal_web_search=True), _google_profile("google_thinking_3__flash"))["config"]
    assert _search_on_wire(cfg.tools)
    assert not [a for a in published if a.key == "internal_web_search"]
