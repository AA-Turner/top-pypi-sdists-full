"""Tests for URL and numeric target pull-artifact aliases."""

from agentic_devtools.cli.ci.agent_task_lifecycle_raw_evidence import _artifact_url_matches


def test_compares_pull_urls_and_numeric_target_ids() -> None:
    assert _artifact_url_matches("https://github.com/o/r/pull/42?plain=1", 42, pull_artifact=False)
    assert not _artifact_url_matches("https://github.com/o/r/pull/43", 42, pull_artifact=False)
    assert _artifact_url_matches("42", 42, pull_artifact=True)
    assert not _artifact_url_matches("43", 42, pull_artifact=True)


def test_ignores_non_pull_numbers_and_invalid_values() -> None:
    assert _artifact_url_matches("43", 42, pull_artifact=False)
    assert _artifact_url_matches("not a pull URL", 42, pull_artifact=True)
    assert _artifact_url_matches(None, 42, pull_artifact=True)
    assert _artifact_url_matches("²", 42, pull_artifact=True)
    assert _artifact_url_matches("https://github.com/o/r/pull/٤٣", 42, pull_artifact=True)
