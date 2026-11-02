"""Tests for _find_outside_code()."""

from agentic_devtools.cli.ci.evaluator.snapshot_comment_sanitization import _find_outside_code


def test_finds_unmasked_occurrence_after_masked_match() -> None:
    """Skips a Markdown-code occurrence and returns a later visible marker."""
    body = "<!-- code --> <!-- visible -->"
    mask = [False] * len(body)
    first = body.find("<!--")
    mask[first : first + 4] = [True] * 4

    assert _find_outside_code(body, mask, "<!--", 0) == body.rfind("<!--")


def test_returns_minus_one_when_no_visible_occurrence_exists() -> None:
    """Returns -1 when every matching marker is inside Markdown code."""
    body = "<!-- code -->"

    assert _find_outside_code(body, [True] * len(body), "<!--", 0) == -1
