"""PB-03 defect 45 (L16): a setting the rules DROP removes every wire effect.

``internal_web_search`` / ``internal_url_context`` are not request params; the translators
read them off the config and append the provider's hosted tool. A declared drop in the
offering rules used to clear nothing but the (absent) settings key, so the stored request
still carried the tool. Per provider, through the real chokepoint (``translate_request``:
capability gates + rules gate + translator), the payload must carry no hosted tool the
rules drop — judged BY MEANING (``wire_meaning.meaning_paths``) so every shape counts —
and the drop must be recorded for ``settings_adjusted``.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.catalog.wire_meaning import meaning_paths
from matrx_ai.config import TextContent, UnifiedConfig, UnifiedMessage
from matrx_ai.providers import unified_client
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
DROP = {"drop": True, "why": "this offering takes no hosted tool for it"}


def _config(model: str) -> UnifiedConfig:
    return UnifiedConfig(
        model=model,
        messages=[UnifiedMessage(role="user", content=[TextContent(text="hi")])],
        internal_web_search=True,
        internal_url_context=True,
    )


async def _payload(monkeypatch, wire: str, rules: dict[str, Any]) -> dict[str, Any]:
    import matrx_ai.catalog.resolve as resolve_mod

    profile = make_profile(
        model_name=WIRES[wire], wire_format=wire, capabilities=dict(CAPS), rules=rules
    )

    async def _resolve(*_a: Any, **_k: Any):
        return profile

    monkeypatch.setattr(resolve_mod, "resolve_call_profile", _resolve)
    out = await UnifiedAIClient().translate_request(
        SimpleNamespace(config=_config(WIRES[wire]), debug=False)
    )
    return wire_json(out)


@pytest.mark.asyncio
@pytest.mark.parametrize("wire", sorted(WIRES))
async def test_dropped_hosted_tools_are_absent_from_the_wire(monkeypatch, wire: str) -> None:
    rules = {"temperature": {}, "internal_web_search": DROP, "internal_url_context": DROP}
    payload = await _payload(monkeypatch, wire, rules)
    for key in ("internal_web_search", "internal_url_context"):
        assert meaning_paths(payload, key) == [], f"{wire}: {key} dropped but the tool is on the wire"


@pytest.mark.asyncio
@pytest.mark.parametrize("wire", sorted(WIRES))
async def test_declared_hosted_tools_still_ride(monkeypatch, wire: str) -> None:
    """The other half: supported (or undeclared) means the tool is sent — nothing is lost."""
    rules = {"temperature": {}, "internal_web_search": {"supported": True}}
    payload = await _payload(monkeypatch, wire, rules)
    assert meaning_paths(payload, "internal_web_search"), f"{wire}: supported search not sent"


def test_the_rules_gate_records_each_drop_and_leaves_the_rest() -> None:
    controls = make_profile(
        rules={"temperature": {}, "internal_web_search": DROP, "internal_url_context": {"supported": True}}
    ).controls
    config = _config("m")
    adjustments = unified_client.strip_hosted_tools_the_rules_drop(config, controls)
    assert [(a.key, a.action) for a in adjustments] == [("internal_web_search", "dropped")]
    assert config.internal_web_search is None and config.internal_url_context is True


def test_a_passthrough_profile_keeps_everything() -> None:
    config = _config("m")
    assert unified_client.strip_hosted_tools_the_rules_drop(config, make_profile(rules={}).controls) == []
    assert config.internal_web_search is True


# --- wire_meaning covers hosted tools in every provider's shape -------------------------
@pytest.mark.parametrize(
    ("key", "payload"),
    [
        ("internal_web_search", {"tools": [{"type": "web_search_20250305", "name": "web_search"}]}),
        ("internal_web_search", {"tools": [{"type": "web_search_preview"}]}),
        ("internal_web_search", {"tools": [{"type": "web_search"}]}),
        ("internal_web_search", {"config": {"tools": [{"google_search": {}}]}}),
        ("internal_web_search", {"config": {"tools": [{"googleSearch": {}}]}}),
        ("internal_url_context", {"config": {"tools": [{"url_context": {}}]}}),
        ("internal_url_context", {"tools": [{"type": "web_fetch_20250910", "name": "web_fetch"}]}),
        ("internal_x_search", {"tools": [{"type": "x_search"}]}),
        ("code_execution", {"config": {"tools": [{"code_execution": {}}]}}),
        ("code_execution", {"tools": [{"type": "code_interpreter"}]}),
    ],
)
def test_wire_meaning_sees_hosted_tools(key: str, payload: dict[str, Any]) -> None:
    assert meaning_paths(payload, key)


def test_wire_meaning_ignores_local_function_tools() -> None:
    payload = {"tools": [{"type": "function", "name": "web_search"}, {"name": "web_search", "input_schema": {}}]}
    assert meaning_paths(payload, "internal_web_search") == []
