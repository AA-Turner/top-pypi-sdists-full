"""Tests for _print_shared_context."""

from agentic_devtools.cli.azure_devops.review_prompt_formatting import _print_shared_context


def test_describes_shared_review_artifacts(capsys) -> None:
    _print_shared_context()

    output = capsys.readouterr().out
    assert "pull-request-files.json" in output
    assert "pull-request-threads.json" in output
    assert "pull-request-jira-issue.json" in output
