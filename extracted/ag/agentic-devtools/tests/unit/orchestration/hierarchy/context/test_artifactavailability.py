"""Unit tests for context injection records and trace event_detail serialization."""

from __future__ import annotations

from agentic_devtools.orchestration.hierarchy.context import (
    ArtifactAvailability,
    inject_prompt_context,
    select_epic_context,
)
from agentic_devtools.orchestration.hierarchy.scopes import AgentScopeLevel, make_review_only_scope


def _epic_agent():
    return make_review_only_scope(agent_id="epic-1", scope_level=AgentScopeLevel.EPIC, issue_key="1")


def test_context_injected_field_refs_have_sha256_and_locator_or_snapshot() -> None:
    fields = select_epic_context(
        {"spec.md": ArtifactAvailability(path="specs/x/spec.md", exists=True, content="hello")}, revision="rev1"
    )
    record = inject_prompt_context(_epic_agent(), fields)
    refs = record.field_content_refs
    spec_ref = refs["spec_md"]
    assert len(spec_ref["content_sha256"]) == 64
    assert spec_ref["locator_type"] == "artifact_path"

    plan_ref = refs["plan_md"]
    assert plan_ref["snapshot_ref"] is not None
