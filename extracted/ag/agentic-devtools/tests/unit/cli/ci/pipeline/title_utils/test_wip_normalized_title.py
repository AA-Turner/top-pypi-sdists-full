"""Tests for wip_normalized_title."""

from agentic_devtools.cli.ci.pipeline.title_utils import wip_normalized_title


def test_strips_wip_prefix_and_whitespace() -> None:
    assert wip_normalized_title("[WIP] completed work") == "completed work"
    assert wip_normalized_title("[wip]   completed work") == "completed work"


def test_returns_empty_string_for_non_wip_title() -> None:
    assert wip_normalized_title("feat: add feature") == ""


def test_returns_empty_string_when_no_title_text_remains() -> None:
    assert wip_normalized_title("[WIP]") == ""
    assert wip_normalized_title("[WIP]   ") == ""
