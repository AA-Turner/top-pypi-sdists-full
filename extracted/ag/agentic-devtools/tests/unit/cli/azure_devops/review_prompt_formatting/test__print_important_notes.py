"""Tests for _print_important_notes."""

from agentic_devtools.cli.azure_devops.review_prompt_formatting import _print_important_notes


def test_warns_when_no_prompts_were_generated(capsys) -> None:
    _print_important_notes(0)

    output = capsys.readouterr().out
    assert "WARNING: No prompts were generated" in output


def test_confirms_review_queue_is_ready(capsys) -> None:
    _print_important_notes(1)

    output = capsys.readouterr().out
    assert "Ready to begin review" in output
    assert "WARNING: No prompts were generated" not in output
