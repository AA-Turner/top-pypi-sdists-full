"""``ai.agent.start`` input hygiene (FOUND_DEFECTS agent-node #4).

The host ``AgentStartRequest`` burned the legacy ``client_tools`` /
``custom_tools`` fields (unified injection: ``tools`` / ``tools_replace``).
The node's ``AgentStartInput`` must mirror that — declare the unified fields,
never the burned ones. Empty legacy values from stale saved workflows are
stripped silently; non-empty values fail loudly (they would have folded into
agent VARIABLES via ``extra="allow"``).
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_ai import _ext
from matrx_ai.graph_nodes import agent_action
from matrx_ai.graph_nodes.agent_action import (
    AgentStartInput,
    _strip_inert_burned_tool_fields,
    agent_start,
)


def test_unified_tool_fields_declared_and_legacy_burned() -> None:
    fields = set(AgentStartInput.model_fields)
    assert {"tools", "tools_replace"} <= fields
    assert not {"client_tools", "custom_tools"} & fields


@pytest.mark.parametrize("legacy_field", ["client_tools", "custom_tools"])
async def test_burned_legacy_tool_field_rejected_loudly(legacy_field: str) -> None:
    # Minimal exts so the entry guard passes; the burned-field check fires
    # before either ext is actually used.
    injected = {"agent_runner": object(), "AgentStartRequest": object()}
    preexisting = {k for k in injected if _ext.has_ext(k)}
    _ext.configure_ext(**{k: v for k, v in injected.items() if k not in preexisting})
    try:
        inputs = AgentStartInput.model_validate(
            {"agent_id": "00000000-0000-0000-0000-000000000000", legacy_field: ["x"]}
        )
        with pytest.raises(ValueError, match="tools_replace"):
            await agent_start(None, inputs)  # type: ignore[arg-type]
    finally:
        for k in injected:
            if k not in preexisting:
                _ext._registry.pop(k, None)


@pytest.mark.parametrize("legacy_field", ["client_tools", "custom_tools"])
@pytest.mark.parametrize("inert_value", [None, [], {}])
def test_empty_burned_legacy_tool_field_stripped(legacy_field: str, inert_value: object) -> None:
    """Stale workflows often persist empty legacy arrays from old JSON Schema defaults."""
    extra = {"topic": "Pizza", legacy_field: inert_value}
    _strip_inert_burned_tool_fields(extra)
    assert legacy_field not in extra
    assert extra["topic"] == "Pizza"


def test_non_empty_burned_legacy_tool_field_not_stripped() -> None:
    extra = {"client_tools": ["browser-dom"]}
    _strip_inert_burned_tool_fields(extra)
    assert extra["client_tools"] == ["browser-dom"]


@pytest.mark.asyncio
async def test_workflow_file_variable_reaches_canonical_agent_runner(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A workflow edge needs only provide the file id as the agent variable."""
    file_id = "550e8400-e29b-41d4-a716-446655440000"
    agent_id = "4185e955-0f4e-4faa-b63c-704bb876c85f"
    captured: dict[str, object] = {}

    class FakeAgentStartRequest:
        @classmethod
        def model_validate(cls, payload):
            captured["payload"] = payload
            return payload

    async def fake_agent_runner(received_agent_id, request, app_ctx):
        captured["agent_id"] = received_agent_id
        captured["request"] = request
        captured["app_ctx"] = app_ctx
        return "completed"

    monkeypatch.setitem(_ext._registry, "agent_runner", fake_agent_runner)
    monkeypatch.setitem(_ext._registry, "AgentStartRequest", FakeAgentStartRequest)
    monkeypatch.setattr(agent_action, "normalize_completed_result", lambda value: value)

    app_ctx = SimpleNamespace()
    inputs = AgentStartInput.model_validate(
        {
            "agent_id": agent_id,
            "user_input": "Inspect the document",
            "pdf_file": file_id,
        }
    )
    step_ctx = SimpleNamespace(app=app_ctx, node_id="agent_step", organization_id="8fd3a0e1-0000-4000-8000-000000000001")
    result = await agent_start(step_ctx, inputs)  # type: ignore[arg-type]

    assert result == "completed"
    assert captured["agent_id"] == agent_id
    assert captured["app_ctx"] is app_ctx
    assert captured["payload"]["variables"] == {"pdf_file": file_id}


# ---------------------------------------------------------------------------
# Run-scope config layering (F-19 / C-32)
# ---------------------------------------------------------------------------
#
# A workflow step's authored config is STATIC — it is part of the saved
# definition. `runtime_config_overrides` is the per-run layer an upstream step
# delivers on an edge (the podcast challenger's W6 voice map, computed from the
# run's cast). Precedence, lowest → highest: mandate → authored → runtime,
# mirroring `resolve_mandate`'s own ladder where run-scope is the top.


def _capture_request(monkeypatch: pytest.MonkeyPatch) -> dict[str, object]:
    captured: dict[str, object] = {}

    class FakeAgentStartRequest:
        @classmethod
        def model_validate(cls, payload):
            captured["payload"] = payload
            # A real request object, not the dict — the node stamps
            # ``_mandate_key`` on it for provenance.
            return SimpleNamespace()

    async def fake_agent_runner(agent_id, request, app_ctx):
        captured["agent_id"] = agent_id
        return "completed"

    monkeypatch.setitem(_ext._registry, "agent_runner", fake_agent_runner)
    monkeypatch.setitem(_ext._registry, "AgentStartRequest", FakeAgentStartRequest)
    monkeypatch.setattr(agent_action, "normalize_completed_result", lambda value: value)
    return captured


def _step_ctx():
    return SimpleNamespace(
        app=SimpleNamespace(),
        node_id="audio_step",
        organization_id="8fd3a0e1-0000-4000-8000-000000000001",
    )


@pytest.mark.asyncio
async def test_runtime_config_overrides_merge_over_authored_config(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captured = _capture_request(monkeypatch)
    inputs = AgentStartInput.model_validate(
        {
            "agent_id": "4185e955-0f4e-4faa-b63c-704bb876c85f",
            "config_overrides": {"temperature": 0.2, "tts_voice": "Zephyr"},
            "runtime_config_overrides": {
                "tts_voice": [{"name": "Ava", "voice": "Kore"}]
            },
        }
    )
    await agent_start(_step_ctx(), inputs)  # type: ignore[arg-type]

    payload = captured["payload"]
    # The runtime layer wins on the contested key and leaves the rest alone —
    # a MERGE, never the whole-dict replacement a plain edge-delivered
    # config_overrides would produce.
    assert payload["config_overrides"] == {
        "temperature": 0.2,
        "tts_voice": [{"name": "Ava", "voice": "Kore"}],
    }
    # It is a workflow-only field: it never reaches the host request itself.
    assert "runtime_config_overrides" not in payload
    # ...and it must never be mistaken for an agent VARIABLE.
    assert "runtime_config_overrides" not in (payload.get("variables") or {})


@pytest.mark.asyncio
async def test_config_precedence_is_mandate_then_authored_then_runtime(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_ai import mandates as mandates_mod
    from matrx_ai.agents.named import AgentRecordSource

    resolved_agent_id = "a3f9c1d2-0000-4000-8000-000000000042"

    async def fake_resolver(mandate_key: str):
        return mandates_mod.MandateResolution(
            source=AgentRecordSource(agent_id=resolved_agent_id, is_version=False),
            config_overrides={
                "model": "from-mandate",
                "temperature": 0.9,
                "tts_voice": "MandateVoice",
            },
        )

    previous = mandates_mod.get_mandate_resolver()
    mandates_mod.set_mandate_resolver(fake_resolver)
    try:
        captured = _capture_request(monkeypatch)
        inputs = AgentStartInput.model_validate(
            {
                "mandate_key": "podcast.audio_english",
                "config_overrides": {"temperature": 0.1, "tts_voice": "AuthoredVoice"},
                "runtime_config_overrides": {"tts_voice": "RuntimeVoice"},
            }
        )
        await agent_start(_step_ctx(), inputs)  # type: ignore[arg-type]
    finally:
        if previous is None:
            mandates_mod._MANDATE_RESOLVER = None
        else:
            mandates_mod.set_mandate_resolver(previous)

    # The Holder the mandate resolved to is what ran — never the authored id.
    assert captured["agent_id"] == resolved_agent_id
    assert captured["payload"]["config_overrides"] == {
        # only the mandate names it → the mandate's value stands
        "model": "from-mandate",
        # mandate + author → the author (the step's own choice) wins
        "temperature": 0.1,
        # all three name it → the run's computed value wins
        "tts_voice": "RuntimeVoice",
    }


@pytest.mark.asyncio
async def test_no_runtime_layer_leaves_the_authored_config_untouched(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """The seam is additive — a step that delivers nothing behaves as before."""
    captured = _capture_request(monkeypatch)
    inputs = AgentStartInput.model_validate(
        {
            "agent_id": "4185e955-0f4e-4faa-b63c-704bb876c85f",
            "config_overrides": {"temperature": 0.2},
        }
    )
    await agent_start(_step_ctx(), inputs)  # type: ignore[arg-type]
    assert captured["payload"]["config_overrides"] == {"temperature": 0.2}


@pytest.mark.asyncio
async def test_empty_runtime_layer_never_invents_a_config(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """`{}` (W6's no-cast answer) must not add a config_overrides key at all."""
    captured = _capture_request(monkeypatch)
    inputs = AgentStartInput.model_validate(
        {
            "agent_id": "4185e955-0f4e-4faa-b63c-704bb876c85f",
            "runtime_config_overrides": {},
        }
    )
    await agent_start(_step_ctx(), inputs)  # type: ignore[arg-type]
    assert "config_overrides" not in captured["payload"]
