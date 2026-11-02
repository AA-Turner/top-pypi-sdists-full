"""Tests for _print_delegation_instructions."""

from agentic_devtools.cli.azure_devops.review_prompt_formatting import _print_delegation_instructions


def test_prints_file_review_handoff_command(capsys) -> None:
    _print_delegation_instructions()

    output = capsys.readouterr().out
    assert "NEXT STEP: FILE REVIEW DELEGATION" in output
    assert "agdt-file-review-write --file-key" in output
