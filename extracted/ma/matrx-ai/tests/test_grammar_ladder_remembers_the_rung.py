"""The Anthropic grammar-budget ladder remembers the rung that served.

Live 2026-11-12: every Applet Builder call paid a refused provider round trip
("The compiled grammar is too large") before the ladder found the rung that
serves, because nothing remembered it. The refusal is a fact about (model,
schema, tool set), so the second call of the same shape must make ONE provider
request, starting at the remembered rung; a changed schema, tool set or model
must miss; a remembered rung that is later refused falls down the ladder and
the rung that served replaces it.
"""

from __future__ import annotations

import asyncio
import contextlib
import io
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.providers.anthropic import anthropic_api
from matrx_ai.providers.anthropic.anthropic_api import AnthropicChat

REFUSAL = "The compiled grammar is too large, which would cause performance issues."


class _Emitter:
    def __init__(self) -> None:
        self.warnings: list[str] = []

    async def send_warning(self, warning: Any) -> None:
        self.warnings.append(getattr(warning, "code", str(warning)))

    def __getattr__(self, name: str) -> Any:  # any other emitter call is a no-op
        async def _noop(*_a: Any, **_k: Any) -> None:
            return None

        return _noop


def _payload(model: str = "claude-sonnet-5", unions: int = 3, tool_count: int = 2) -> dict[str, Any]:
    props = {f"f{i}": {"type": ["string", "null"]} for i in range(unions)}
    props["title"] = {"type": "string"}
    schema = {"type": "object", "properties": props, "required": list(props), "additionalProperties": False}
    return {
        "model": model,
        "messages": [],
        "max_tokens": 1000,
        "output_config": {"format": {"type": "json_schema", "schema": schema}},
        "tools": [
            {"name": f"tool_{i}", "input_schema": {"type": "object", "properties": {}}}
            for i in range(tool_count)
        ],
    }


@pytest.fixture(autouse=True)
def _clean(monkeypatch: pytest.MonkeyPatch):
    from matrx_ai.providers import structured_output_findings as sof

    anthropic_api.forget_grammar_rungs()
    sof.forget_recorded_facts()
    token = sof._GATE_PENDING.set(None)
    recorded: list[str] = []

    async def fake_capture(key: str, **_kwargs: Any) -> None:
        recorded.append(key)

    import matrx_ai.ops.issue_capture as issue_capture

    monkeypatch.setattr(issue_capture, "capture_issue", fake_capture)
    yield recorded
    sof._GATE_PENDING.reset(token)
    anthropic_api.forget_grammar_rungs()


def _harness(monkeypatch: pytest.MonkeyPatch, accept: Any):
    """Drive the REAL ``AnthropicChat.execute`` with the wire replaced by ``accept``."""
    sent: list[dict[str, Any]] = []
    emitter = _Emitter()
    state: dict[str, Any] = {"payload": _payload()}

    chat = AnthropicChat.__new__(AnthropicChat)
    chat.translator = SimpleNamespace(debug=False)
    chat.debug = False
    monkeypatch.setattr(chat, "to_provider_config", lambda *_a, **_k: dict(state["payload"]), raising=False)

    async def fake_wire(payload: dict[str, Any], _emitter: Any, _model: str) -> str:
        sent.append(payload)
        if accept(payload):
            return "served"
        raise RuntimeError(REFUSAL)

    monkeypatch.setattr(chat, "_execute_non_streaming", fake_wire, raising=False)
    monkeypatch.setattr(anthropic_api, "capture_request_payload", lambda *a, **k: None)
    monkeypatch.setattr(anthropic_api, "stamp_call_meta", lambda **k: None)
    import matrx_ai.context.app_context as app_context

    monkeypatch.setattr(app_context, "get_app_context", lambda: SimpleNamespace(emitter=emitter))

    def call() -> Any:
        cfg = SimpleNamespace(
            model=state["payload"]["model"],
            stream=False,
            response_format={"type": "json_schema", "json_schema": {"name": "probe", "schema": {}}},
        )
        with contextlib.redirect_stdout(io.StringIO()):
            return asyncio.run(chat.execute(cfg, SimpleNamespace(wire_format="anthropic_chat")))

    return call, sent, state


def _tools_shed_fits(p: dict[str, Any]) -> bool:
    return bool((p.get("output_config") or {}).get("format")) and not p.get("tools")


def test_second_call_makes_one_provider_request(monkeypatch, _clean) -> None:
    call, sent, _ = _harness(monkeypatch, _tools_shed_fits)
    assert call() == "served"
    first = len(sent)
    assert first == 3, "first call: refused original, refused narrowing, served tool shed"
    sent.clear()
    assert call() == "served"
    assert len(sent) == 1, f"the second call re-paid the refused attempts: {len(sent)} requests"
    assert _tools_shed_fits(sent[0])
    # The compromise is still recorded (once per process, unchanged rule).
    assert _clean.count("structured_output.tools_shed") == 1


@pytest.mark.parametrize("change", ["schema", "tools", "model"])
def test_a_changed_shape_misses_the_memory(monkeypatch, change) -> None:
    call, sent, state = _harness(monkeypatch, _tools_shed_fits)
    call()
    sent.clear()
    if change == "schema":
        state["payload"] = _payload(unions=4)
    elif change == "tools":
        state["payload"] = _payload(tool_count=3)
    else:
        state["payload"] = _payload(model="claude-opus-5-5")
    call()
    assert len(sent) == 3, "a different shape must be sent as configured first"
    assert sent[0].get("tools"), "the first request of a new shape was not the original"


def test_a_remembered_rung_that_is_refused_falls_down_and_updates(monkeypatch) -> None:
    rule = {"accept": _tools_shed_fits}
    call, sent, _ = _harness(monkeypatch, lambda p: rule["accept"](p))
    call()
    # The provider's budget tightens: now only the prompt-guided rung serves.
    rule["accept"] = lambda p: not (p.get("output_config") or {}).get("format")
    sent.clear()
    assert call() == "served"
    assert len(sent) == 2, "remembered rung refused, next rung served; the original was not re-sent"
    assert sent[0].get("tools") == [] or not sent[0].get("tools")
    sent.clear()
    call()
    assert len(sent) == 1, "the rung that served must replace the remembered one"
    assert not (sent[0].get("output_config") or {}).get("format")


def test_memory_is_bounded() -> None:
    for i in range(anthropic_api._GRAMMAR_RUNG_MEMORY_MAX + 50):
        anthropic_api._remember_grammar_rung((f"m{i}", "s", "t"), "x")
    assert len(anthropic_api._GRAMMAR_RUNG_MEMORY) == anthropic_api._GRAMMAR_RUNG_MEMORY_MAX
    assert ("m0", "s", "t") not in anthropic_api._GRAMMAR_RUNG_MEMORY
