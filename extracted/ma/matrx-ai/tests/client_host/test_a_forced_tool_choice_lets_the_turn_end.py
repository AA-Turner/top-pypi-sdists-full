"""A saved ``tool_choice: required`` forces ONE tool call, then the run can end.

THE DEFECT (2026-10-23). An agent whose settings carry ``tool_choice: required``
kept it on EVERY iteration of the tool loop, so after its tool call returned the
provider was forced to call a tool again, and again: the run could never end
with text, ran to its iteration ceiling, and re-paid its tool each round (a paid
image generation per round for the "GPT Image all-in-one" agent).

What the test is FOR: delete the RESET TOOL CHOICE block in
``execute_until_complete`` and the second provider call is sent ``required``
again, the tool runs on every round, and the run hits the ceiling.

The mock provider behaves like a real model under a forced choice: it calls the
tool when (and only when) the request says ``required``, otherwise it answers.
"""

from __future__ import annotations

import pytest

pytestmark = pytest.mark.usefixtures("client_host_sandbox")

from test_the_iteration_ceiling_ends_with_an_answer import (  # noqa: E402
    TOOL,
    WRAP_UP_TEXT,
    _config,
    _configure,
    _set_context,
    _text_of,
    _tool_calls_in,
    probe_tool,  # noqa: F401  (fixture)
)


def _obeys_tool_choice(monkeypatch) -> list[str | None]:
    from matrx_ai.providers.mock.mock_api import MockChat

    sent: list[str | None] = []
    original_raw_spec = MockChat._raw_spec
    monkeypatch.setattr(
        MockChat, "_history_has_tool_result", staticmethod(lambda unified_config: False)
    )

    def _raw_spec(unified_config):
        raw = dict(original_raw_spec(unified_config) or {})
        sent.append(unified_config.tool_choice)
        if unified_config.tool_choice == "required":
            raw["tool_calls"] = [{"name": TOOL, "arguments": {"path": f"file-{len(sent)}"}}]
        else:
            raw["tool_calls"] = []
        return raw

    monkeypatch.setattr(MockChat, "_raw_spec", staticmethod(_raw_spec))
    return sent


@pytest.mark.asyncio
async def test_required_tool_choice_applies_until_the_first_tool_call(probe_tool, monkeypatch):  # noqa: F811
    from matrx_ai.orchestrator.executor import execute_ai_request

    sent = _obeys_tool_choice(monkeypatch)
    _configure()
    _set_context(sub_agent=False)

    config = _config()
    config.tool_choice = "required"
    completed = await execute_ai_request(config, max_iterations=5)

    assert sent == ["required", "auto"], f"tool_choice sent per provider call: {sent}"
    assert len(probe_tool) == 1, f"the forced tool ran {len(probe_tool)} times"
    assert (completed.metadata or {}).get("status") != "max_iterations_exceeded"
    last = list(completed.request.config.messages)[-1]
    assert last.role == "assistant"
    assert _tool_calls_in(last) == 0
    assert _text_of(last) == WRAP_UP_TEXT


def test_the_definition_mapper_carries_tool_choice_and_parallel_tool_calls():
    """The saved settings reach UnifiedConfig (live 2026-10-23: the runs carried an
    older row's settings; this pins that the mapper itself is not the drop)."""
    from matrx_ai.client_host.agent_source import (
        definition_to_agent_config,
        validate_execution_agent_definition,
    )

    definition = validate_execution_agent_definition(
        {
            "definition_id": "6bc1d330-40b5-49f8-8895-e5b55ec95ae9",
            "agent_id": "6bc1d330-40b5-49f8-8895-e5b55ec95ae9",
            "is_version": False,
            "version_number": 1,
            "name": "probe",
            "model_id": "mock-model",
            "messages": [{"role": "system", "content": "call the tool"}],
            "settings": {"tool_choice": "required", "parallel_tool_calls": True},
            "tools": [TOOL],
        }
    )
    config = definition_to_agent_config(definition).config
    assert config.tool_choice == "required"
    assert config.parallel_tool_calls is True
