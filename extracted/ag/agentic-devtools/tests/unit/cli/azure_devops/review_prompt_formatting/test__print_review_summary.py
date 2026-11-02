"""Tests for _print_review_summary."""

from agentic_devtools.cli.azure_devops.review_prompt_formatting import _print_review_summary


def test_prints_review_counts_and_skipped_files(tmp_path, capsys) -> None:
    _print_review_summary(42, tmp_path, 3, 2)

    output = capsys.readouterr().out
    assert "PR ID: 42" in output
    assert "Prompts generated: 3" in output
    assert "Skipped (not on branch, from merged PRs): 2" in output
