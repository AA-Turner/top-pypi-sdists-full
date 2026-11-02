"""Tests for _print_console_checklist."""

from agentic_devtools.cli.azure_devops.review_prompt_formatting import _print_console_checklist


def test_prints_review_steps(capsys) -> None:
    _print_console_checklist()

    output = capsys.readouterr().out
    assert "CONSOLE CHECKLIST (for each file)" in output
    assert "Verify repository conventions" in output
    assert "Post the review" in output
