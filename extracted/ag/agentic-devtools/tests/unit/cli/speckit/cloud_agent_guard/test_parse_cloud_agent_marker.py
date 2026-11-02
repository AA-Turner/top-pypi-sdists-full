"""Tests for Cloud Agent correlation marker parsing."""

from __future__ import annotations

from agentic_devtools.cli.speckit.cloud_agent_guard import parse_cloud_agent_marker


def test_parses_canonical_marker() -> None:
    marker = (
        "<!--  speckit:agent-assigned schema_version=1 engine=cloud-agent "
        "issue=7 phase=2 hierarchy=Feature correlation_id=123E4567-E89B-12D3-A456-426614174000  -->"
    )
    assert parse_cloud_agent_marker(marker) == {
        "issue": 7,
        "phase": 2,
        "hierarchy": "feature",
        "correlation_id": "123e4567-e89b-12d3-a456-426614174000",
    }


def test_ignores_malformed_or_missing_marker() -> None:
    invalid_marker = (
        "<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent "
        "issue=7 phase=2 hierarchy=Feature correlation_id=deadbeef -->"
    )
    assert parse_cloud_agent_marker(invalid_marker) is None
    invalid_hierarchy_marker = (
        "<!-- speckit:agent-assigned schema_version=1 engine=cloud-agent "
        "issue=7 phase=2 hierarchy=invalid correlation_id=123e4567-e89b-12d3-a456-426614174000 -->"
    )
    assert parse_cloud_agent_marker(invalid_hierarchy_marker) is None
    assert parse_cloud_agent_marker("speckit:agent-fallback") is None
    assert parse_cloud_agent_marker(None) is None
