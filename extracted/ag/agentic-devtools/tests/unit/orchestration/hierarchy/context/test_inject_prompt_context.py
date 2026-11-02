"""Unit tests for context injection records and trace event_detail serialization."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.context import (
    inject_prompt_context,
    select_epic_context,
)
from agentic_devtools.orchestration.hierarchy.scopes import AgentScopeLevel, make_review_only_scope


def _epic_agent():
    return make_review_only_scope(agent_id="epic-1", scope_level=AgentScopeLevel.EPIC, issue_key="1")


def test_inject_prompt_context_marks_trusted_false() -> None:
    fields = select_epic_context({}, revision="rev1")
    record = inject_prompt_context(_epic_agent(), fields)
    detail = record.to_event_detail()
    assert detail["trusted"] is False
    assert detail["agent_id"] == "epic-1"
    assert set(detail["fields_injected"]) == set(record.field_content_refs.keys())


def test_to_prompt_context_distinguishes_provenance() -> None:
    fields = select_epic_context({}, revision="rev1")
    record = inject_prompt_context(_epic_agent(), fields)
    prompt_ctx = record.to_prompt_context()
    assert all(entry["authoritative"] is False for entry in prompt_ctx.values())


def test_injection_cannot_widen_agent_boundary_or_capabilities() -> None:
    agent = _epic_agent()
    fields = select_epic_context({}, revision="rev1")
    inject_prompt_context(agent, fields)
    # Injection is purely additive; the agent object itself is immutable and unaffected.
    assert agent.file_boundary.is_empty
    assert not agent.can_modify_files
