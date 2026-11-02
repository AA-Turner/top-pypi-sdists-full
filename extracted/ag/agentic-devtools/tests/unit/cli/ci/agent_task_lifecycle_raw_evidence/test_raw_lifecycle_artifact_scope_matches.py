"""Tests for pull-artifact lifecycle scope validation."""

from agentic_devtools.cli.ci.agent_task_lifecycle_raw_evidence import raw_lifecycle_artifact_scope_matches


def test_rejects_conflicting_pull_artifact_number_and_url_aliases() -> None:
    assert not raw_lifecycle_artifact_scope_matches(
        {"artifacts": [{"type": "pull", "data": {"number": 43}}]},
        42,
    )
    assert not raw_lifecycle_artifact_scope_matches(
        {"artifacts": [{"type": "pull", "url": "https://github.com/o/r/pull/43"}]},
        42,
    )
    assert not raw_lifecycle_artifact_scope_matches(
        {
            "artifacts": [
                {"type": "pull", "data": {"number": 42}, "url": "https://github.com/o/r/pull/43"},
            ],
        },
        42,
    )


def test_accepts_matching_and_invalid_pull_artifact_aliases() -> None:
    assert raw_lifecycle_artifact_scope_matches({}, 42)
    assert raw_lifecycle_artifact_scope_matches(
        {
            "artifacts": [
                {"type": "pull", "data": {"number": 42}},
                {"type": "pull", "url": "https://github.com/o/r/pull/42?plain=1"},
                {"type": "issue", "data": {"number": 43}},
                "malformed",
            ],
        },
        42,
    )
    assert raw_lifecycle_artifact_scope_matches(
        {"artifacts": [{"type": "pull", "data": {"number": True}, "url": "not a pull URL"}]},
        42,
    )


def test_validates_repository_identity_in_pull_artifact_urls() -> None:
    assert not raw_lifecycle_artifact_scope_matches(
        {"artifacts": [{"type": "pull", "url": "https://github.com/other/repo/pull/42"}]},
        42,
        repository="owner/repo",
    )
    assert raw_lifecycle_artifact_scope_matches(
        {"artifacts": [{"type": "pull", "data": {"html_url": "https://github.com/owner/repo/pull/42"}}]},
        42,
        repository="owner/repo",
    )
    assert raw_lifecycle_artifact_scope_matches(
        {"artifacts": [{"type": "pull", "url": "https://[invalid/pull/42"}]},
        42,
        repository="owner/repo",
    )
