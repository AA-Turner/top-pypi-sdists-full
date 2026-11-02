"""Tests for validating one raw pull-artifact's scope."""

from agentic_devtools.cli.ci.agent_task_lifecycle_raw_evidence import _artifact_scope_matches


def test_rejects_conflicting_pull_number_and_url_fields() -> None:
    assert not _artifact_scope_matches({"type": "pull", "data": {"number": 43}}, 42)
    assert not _artifact_scope_matches({"type": "pull", "url": "https://github.com/o/r/pull/43"}, 42)


def test_accepts_matching_non_pull_and_malformed_artifacts() -> None:
    assert _artifact_scope_matches({"type": "pull", "data": {"number": 42}}, 42)
    assert _artifact_scope_matches({"type": "issue", "data": {"number": 43}}, 42)
    assert _artifact_scope_matches(None, 42)
