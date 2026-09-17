from __future__ import annotations

from agentic_devtools.adapters.pull_request_draft import PullRequestDraftResult


def test_defaults_error_to_empty_string() -> None:
    result = PullRequestDraftResult(True, "github", "updated")
    assert result.error == ""


def test_preserves_explicit_error() -> None:
    result = PullRequestDraftResult(False, "azure_devops", "failed", "permission denied")
    assert result.error == "permission denied"
