"""Tests for _normalize_summary_for_comparison."""

from agentic_devtools.cli.ci.pipeline.summary import _normalize_summary_for_comparison


def test_strips_terminal_label_before_comparing_summary_bodies() -> None:
    body = "#### 🤖 AI PR Loop Run — [View Logs](run)\n\n🤖 AI PR Loop ·"

    assert _normalize_summary_for_comparison(body) == "#### 🤖 AI PR Loop Run"


def test_keeps_malformed_terminal_label_in_comparison_body() -> None:
    body = "#### 🤖 AI PR Loop Run — [View Logs](run)\n🤖 AI PR Loop ·"

    assert _normalize_summary_for_comparison(body) == "#### 🤖 AI PR Loop Run\n🤖 AI PR Loop ·"
