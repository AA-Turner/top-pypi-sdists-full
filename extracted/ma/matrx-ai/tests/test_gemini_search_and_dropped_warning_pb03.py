"""PB-03 t (2026-11-09), defects 4 and 6.

Defect 4: ``internal_web_search`` is ``supported: true`` on gemini-flash-lite-latest (it runs as
gemini-3.5-flash-lite, which accepts Google Search beside function tools), yet the tool was dropped
because the translator read the Gemini 3 dialect ONLY from the ``reasoning_effort`` cell's processor,
and that offering's cell carries none. The model id is now the second witness.

Defect 6: ``setting_not_supported`` fired once per loop iteration of a run; it now fires once per request.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from test_chat_param_golden import load_golden

from matrx_ai.catalog.gemini_mode_truth import is_gemini_3_dialect
from matrx_ai.config import MessageList, TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.providers import outbound_params as op
from matrx_ai.providers.google.translator import GoogleTranslator
from matrx_ai.testing.profile_factory import make_profile

_FAKE_FN = {"name": "ctx_get", "description": "get", "parameters": {"type": "object", "properties": {}}}


def _profile(provider_model_id: str):
    # The live gap: the offering's reasoning_effort cell carries NO google_thinking processor (no mode).
    # A real 2.5 id keeps the legacy-mode golden, as its catalog cell does.
    import copy

    payload = load_golden("google_thinking")
    rules = copy.deepcopy(payload["rules"])
    if not provider_model_id.startswith("gemini-2.5"):
        for key in ("processor", "processor_config"):
            rules["reasoning_effort"].pop(key, None)
    return make_profile(
        model_name=provider_model_id,
        provider_model_id=provider_model_id,
        wire_format=payload["wire_format"],
        rules=rules,
        value_orders=payload["value_orders"],
    )


def _config() -> UnifiedConfig:
    return UnifiedConfig(
        model="gemini-flash-lite-latest",
        messages=MessageList(_messages=[UnifiedMessage(role="user", content=[TextContent(text="hi")])]),
        internal_web_search=True,
    )


def _search_sent(provider_model_id: str, monkeypatch) -> bool:
    tr = GoogleTranslator()
    monkeypatch.setattr(tr, "build_provider_tools", lambda config, provider: [_FAKE_FN])
    tools = tr.to_google(_config(), _profile(provider_model_id))["config"].tools
    return any(getattr(t, "google_search", None) is not None for t in (tools or []))


@pytest.mark.parametrize(
    "pid",
    ["gemini-flash-lite-latest", "gemini-pro-latest", "gemini-3-flash-preview",
     "gemini-3.1-flash-lite", "gemini-3.1-pro-preview"],
)
def test_supported_search_is_sent_on_every_gemini_3_id_even_without_a_processor_mode(pid, monkeypatch):
    assert _search_sent(pid, monkeypatch), f"{pid}: web search is supported:true but was dropped"


def test_a_real_gemini_25_still_drops_and_says_so(monkeypatch):
    published: list = []
    monkeypatch.setattr(op, "publish_settings_adjustments", lambda adj, **kw: published.extend(adj))
    assert not _search_sent("gemini-2.5-flash", monkeypatch)
    assert any(a.key == "internal_web_search" and a.action == "dropped" for a in published)


def test_dialect_helper():
    assert is_gemini_3_dialect("gemini_3", "gemini-2.5-flash")
    assert is_gemini_3_dialect(None, "gemini-flash-lite-latest")
    assert not is_gemini_3_dialect("legacy", "gemini-2.5-flash")
    assert not is_gemini_3_dialect(None, None)


def _adj(key="clear_thinking", value=True, reason="r"):
    return SimpleNamespace(action="dropped", expected=False, key=key, reason=reason, canonical_value=value)


def _in_request(monkeypatch, request_id):
    import matrx_connect.context.app_context as ac

    monkeypatch.setattr(ac, "try_get_app_context", lambda: SimpleNamespace(request_id=request_id, metadata={}))


def test_setting_not_supported_warns_once_per_request(monkeypatch):
    sent: list = []
    monkeypatch.setattr(op, "send_client_warning", lambda payload, name: sent.append(payload))
    _in_request(monkeypatch, "req-A")
    for _ in range(3):  # three loop iterations of one run
        op.warn_client_about_dropped_settings([_adj()], model="m")
    assert len(sent) == 1
    # a different dropped key in the same request is still new information
    op.warn_client_about_dropped_settings([_adj("top_k", 3)], model="m")
    assert len(sent) == 2
    # a CHANGED value of the same key warns again (the key carries values and reasons)
    op.warn_client_about_dropped_settings([_adj(value=False)], model="m")
    assert len(sent) == 3
    # a NEW request warns again
    _in_request(monkeypatch, "req-B")
    op.warn_client_about_dropped_settings([_adj()], model="m")
    assert len(sent) == 4


def test_the_memory_survives_a_context_rebuild_mid_run(monkeypatch):
    # tools/merge.py + dynamic_drain.py rebuild ctx.metadata with with_overrides: a memory kept ON the
    # metadata dict is lost; this one is keyed by the request id.
    import matrx_connect.context.app_context as ac

    sent: list = []
    monkeypatch.setattr(op, "send_client_warning", lambda payload, name: sent.append(payload))
    for metadata in ({}, {"rebuilt": 1}, {}):
        monkeypatch.setattr(ac, "try_get_app_context", lambda m=metadata: SimpleNamespace(request_id="req-C", metadata=m))
        op.warn_client_about_dropped_settings([_adj()], model="m")
    assert len(sent) == 1


def test_a_context_less_call_does_not_warn_every_time(monkeypatch):
    import matrx_connect.context.app_context as ac

    sent: list = []
    monkeypatch.setattr(op, "send_client_warning", lambda payload, name: sent.append(payload))
    monkeypatch.setattr(ac, "try_get_app_context", lambda: None)
    op._SAID_NO_CONTEXT.set(None)
    for _ in range(3):
        op.warn_client_about_dropped_settings([_adj()], model="m")
    assert len(sent) == 1


def test_an_unplaceable_gemini_id_that_loses_search_warns_the_client(monkeypatch):
    warned: list = []
    monkeypatch.setattr(op, "send_client_warning", lambda payload, name: warned.append(payload))
    _in_request(monkeypatch, "req-D")
    assert not _search_sent("gemini-zz-mystery", monkeypatch)  # cannot be placed: dropped...
    assert warned, "...and the client must be told (not an expected silent drop)"
    warned.clear()
    _in_request(monkeypatch, "req-E")
    assert not _search_sent("gemini-2.5-flash", monkeypatch)  # a known older model: the declared, expected drop
    assert not warned


def test_the_fallback_names_itself_when_it_decides(caplog):
    from matrx_ai.catalog import gemini_mode_truth as g

    g.FALLBACK_DECIDED.discard("gemini-3.1-pro-preview")
    with caplog.at_level("WARNING"):
        assert g.is_gemini_3_dialect(None, "gemini-3.1-pro-preview")
    assert any("gemini-dialect-fallback" in r.message and "gemini-3.1-pro-preview" in r.message for r in caplog.records)
    # a catalog mode decides without any fallback line
    caplog.clear()
    assert g.is_gemini_3_dialect("gemini_3", "gemini-3.1-pro-preview")
    assert not caplog.records


def test_retired_fallback_trusts_only_the_catalog(monkeypatch):
    from matrx_ai.catalog import gemini_mode_truth as g

    monkeypatch.setattr(g, "MODEL_ID_FALLBACK_IN_USE", False)
    assert not g.is_gemini_3_dialect(None, "gemini-3.1-pro-preview")
    assert g.is_gemini_3_dialect("gemini_3", "anything")


_BIG_ENOUGH_SCHEMA = {
    "type": "json_schema",
    "json_schema": {"name": "a", "strict": True, "schema": {
        "type": "object", "properties": {"answer": {"type": "string"}}, "required": ["answer"], "additionalProperties": False}},
}


def _schema_config():
    c = _config()
    c.internal_web_search = False
    c.response_format = _BIG_ENOUGH_SCHEMA
    return c


def test_gemini_3x_without_a_catalog_mode_keeps_native_schema_beside_small_tools(monkeypatch):
    """_native_schema_tool_conflict: only Gemini BEFORE 3 refuses function calling with a JSON schema
    (measured 2026-09-22); Gemini 3 refuses only oversize declarations. These ids ARE 3.x."""
    tr = GoogleTranslator()
    monkeypatch.setattr(tr, "build_provider_tools", lambda config, provider: [_FAKE_FN])
    cfg = tr.to_google(_schema_config(), _profile("gemini-flash-lite-latest"))["config"]
    assert cfg.response_mime_type == "application/json" and cfg.response_json_schema is not None
    old = tr.to_google(_schema_config(), _profile("gemini-2.5-flash"))["config"]
    assert old.response_json_schema is None  # a real 2.5 still gets the text contract
    assert "JSON" in str(old.system_instruction)
