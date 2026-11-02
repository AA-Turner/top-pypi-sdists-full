"""Tests for render_table in record_discovery_baseline."""

from __future__ import annotations

from tests.scripts.record_discovery_baseline import baseline


def test_table_carries_a_header_and_one_row_per_unit():
    """The rendered table starts with a header and lists every unit once."""
    units = [
        baseline.Unit("agent", "agdt.set", ".github/agents/agdt.set.agent.md"),
        baseline.Unit("prompt", "/agdt.set", ".github/prompts/agdt.set.prompt.md"),
    ]
    lines = baseline.render_table(units).splitlines()
    assert lines[0] == "| Surface | Invocation name | Backing file |"
    assert lines[1] == "|---|---|---|"
    assert lines[2:] == [
        "| agent | `agdt.set` | `.github/agents/agdt.set.agent.md` |",
        "| prompt | `/agdt.set` | `.github/prompts/agdt.set.prompt.md` |",
    ]


def test_empty_unit_list_renders_header_only():
    """An empty corpus still renders a valid Markdown table."""
    assert baseline.render_table([]).splitlines() == [
        "| Surface | Invocation name | Backing file |",
        "|---|---|---|",
    ]
