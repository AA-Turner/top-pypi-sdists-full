"""Tests for suppressed_reaper.render_verdict_table()."""

from __future__ import annotations

from agentic_devtools.cli.ci.suppressed_reaper import parse_verdict_rows, render_verdict_table
from tests.unit.cli.ci.suppressed_reaper._fixtures import TABLE


class TestRenderVerdictTable:
    """The table posted to the issue is rebuilt from parsed cells only."""

    def test_round_trips_the_documented_table(self) -> None:
        """Rendering the parsed rows reproduces the table verbatim."""
        assert render_verdict_table(parse_verdict_rows(TABLE)) == TABLE

    def test_renders_the_fixed_header_for_no_rows(self) -> None:
        """An empty row list still yields a well-formed (empty) table."""
        rendered = render_verdict_table([])
        assert rendered.splitlines() == [
            "| # | Location | Verdict | Justification |",
            "| - | -------- | ------- | ------------- |",
        ]
