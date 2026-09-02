"""Regression: Google native search (googleSearch grounding / url_context) must be
sent ALONGSIDE function tools on Gemini 3, not dropped.

The bug: the translator used an either/or — when the request carried ANY function
tool (e.g. context tools auto-injected for an agent), the built-in Google tools were
silently skipped, so an agent with context lost Google's native web search. Gemini 3
supports mixing built-in + function tools in one request; Gemini 2.5/earlier 400 on
it, so those keep the either/or.
"""

from __future__ import annotations

import pytest
from test_chat_param_golden import load_golden

from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.providers.google.translator import GoogleTranslator
from matrx_ai.testing.profile_factory import make_profile


def _google_profile(variant_key: str):
    payload = load_golden(variant_key)
    return make_profile(
        model_name=payload["model"],
        wire_format=payload["wire_format"],
        rules=payload["rules"],
        value_orders=payload["value_orders"],
    )


_GEMINI_3 = _google_profile("google_thinking_3__flash")
_GEMINI_25 = _google_profile("google_thinking")

_FAKE_FN = {
    "name": "ctx_get",
    "description": "get context",
    "parameters": {"type": "object", "properties": {}},
}


def _config(**kw) -> UnifiedConfig:
    return UnifiedConfig(
        model="gemini-3.1-flash-lite-preview",
        messages=MessageList(_messages=[UnifiedMessage(role="user", content=[TextContent(text="hi")])]),
        **kw,
    )


_JSON_SCHEMA_FORMAT = {
    "type": "json_schema",
    "json_schema": {
        "name": "answer",
        "strict": True,
        "schema": {
            "type": "object",
            "properties": {"answer": {"type": "string"}},
            "required": ["answer"],
            "additionalProperties": False,
        },
    },
}


def _has_function_tool(tools) -> bool:
    return any(getattr(t, "function_declarations", None) for t in (tools or []))


def _has_google_search(tools) -> bool:
    return any(getattr(t, "google_search", None) is not None for t in (tools or []))


def test_gemini3_sends_search_alongside_function_tools(monkeypatch):
    tr = GoogleTranslator()
    monkeypatch.setattr(tr, "build_provider_tools", lambda config, provider: [_FAKE_FN])
    cfg = tr.to_google(_config(internal_web_search=True), _GEMINI_3)["config"]
    tools = cfg.tools
    # The fix: BOTH the function tool AND googleSearch ride the same request.
    assert _has_function_tool(tools), "function tools missing"
    assert _has_google_search(tools), "Google native search was dropped (the bug)"
    # Gemini REQUIRES this flag when built-in tools mix with function calling,
    # else it 400s ("Please enable tool_config.include_server_side_tool_invocations").
    assert cfg.tool_config is not None
    assert cfg.tool_config.include_server_side_tool_invocations is True


def test_no_server_side_flag_when_search_alone(monkeypatch):
    # No function tools → no mixing → the flag isn't needed.
    tr = GoogleTranslator()
    monkeypatch.setattr(tr, "build_provider_tools", lambda config, provider: [])
    cfg = tr.to_google(_config(internal_web_search=True), _GEMINI_3)["config"]
    tc = cfg.tool_config
    assert tc is None or not getattr(tc, "include_server_side_tool_invocations", False)


def test_gemini3_search_still_works_without_function_tools(monkeypatch):
    tr = GoogleTranslator()
    monkeypatch.setattr(tr, "build_provider_tools", lambda config, provider: [])
    out = tr.to_google(_config(internal_web_search=True), _GEMINI_3)
    assert _has_google_search(out["config"].tools)


def test_grounded_json_keeps_search_and_provider_native_schema(monkeypatch):
    tr = GoogleTranslator()
    monkeypatch.setattr(tr, "build_provider_tools", lambda config, provider: [])

    out = tr.to_google(
        _config(internal_web_search=True, response_format=_JSON_SCHEMA_FORMAT),
        _GEMINI_3,
    )
    cfg = out["config"]

    assert _has_google_search(cfg.tools)
    assert cfg.response_mime_type == "application/json"
    assert cfg.response_json_schema is not None
    assert cfg.response_json_schema["required"] == ["answer"]
    assert cfg.system_instruction is None


def test_json_without_search_keeps_provider_native_schema(monkeypatch):
    tr = GoogleTranslator()
    monkeypatch.setattr(tr, "build_provider_tools", lambda config, provider: [])

    cfg = tr.to_google(_config(response_format=_JSON_SCHEMA_FORMAT), _GEMINI_3)["config"]

    assert cfg.response_mime_type == "application/json"
    assert cfg.response_json_schema is not None
    assert cfg.system_instruction is None


def test_older_gemini_keeps_safe_either_or(monkeypatch):
    # Gemini 2.5/earlier (google_thinking) can't mix → with function tools present,
    # the built-in search is NOT added (it would 400). This is the safe fallback.
    tr = GoogleTranslator()
    monkeypatch.setattr(tr, "build_provider_tools", lambda config, provider: [_FAKE_FN])
    out = tr.to_google(_config(internal_web_search=True), _GEMINI_25)
    tools = out["config"].tools
    assert _has_function_tool(tools)
    assert not _has_google_search(tools)  # dropped on purpose for non-mixing models


def test_older_gemini_search_alone_still_works(monkeypatch):
    tr = GoogleTranslator()
    monkeypatch.setattr(tr, "build_provider_tools", lambda config, provider: [])
    out = tr.to_google(_config(internal_web_search=True), _GEMINI_25)
    assert _has_google_search(out["config"].tools)


def test_initially_empty_gemini_request_fails_before_sdk_with_actionable_error():
    config = UnifiedConfig(
        model="gemini-3.1-flash-lite-preview",
        messages=MessageList([]),
    )

    with pytest.raises(ValueError, match="request-construction bug"):
        GoogleTranslator().to_google(config, _GEMINI_3)
