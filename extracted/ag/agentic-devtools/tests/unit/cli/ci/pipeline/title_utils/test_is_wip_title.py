"""Tests for is_wip_title."""

from agentic_devtools.cli.ci.pipeline.title_utils import is_wip_title


def test_detects_wip_prefix_case_insensitively() -> None:
    assert is_wip_title("[WIP] work")
    assert is_wip_title("[wip] work")
    assert not is_wip_title("WIP without brackets")
    assert not is_wip_title("A [WIP] title")
