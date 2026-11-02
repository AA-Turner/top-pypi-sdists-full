"""Tests for suppressed_reaper.parse_verdict_rows()."""

from __future__ import annotations

from agentic_devtools.cli.ci.suppressed_reaper import parse_verdict_rows
from tests.unit.cli.ci.suppressed_reaper._fixtures import TABLE


class TestParseVerdictRows:
    """Only data rows are parsed; the header and separator are skipped."""

    def test_parses_every_data_row_in_order(self) -> None:
        """Each row yields its index, citation, verdict and justification."""
        rows = parse_verdict_rows(TABLE)
        assert [row.index for row in rows] == [1, 2]
        assert rows[0].location == "specs/spec.md:42"
        assert rows[0].verdict == "valid-no-action"
        assert rows[0].justification == "AS-4 on line 51 already states this."
        assert rows[1].location == "stale"

    def test_skips_header_and_separator_rows(self) -> None:
        """The fixed header lines never appear as data rows."""
        assert len(parse_verdict_rows(TABLE)) == 2

    def test_returns_empty_for_a_body_without_a_table(self) -> None:
        """Prose without a table yields no rows."""
        assert parse_verdict_rows("no table here") == []

    def test_returns_empty_for_isolated_row_shaped_lines(self) -> None:
        """Row text without the fixed header is not accepted as a verdict table."""
        body = "| 1 | `specs/spec.md:42` | `valid-no-action` | Already covered. |"
        assert parse_verdict_rows(body) == []

    def test_returns_empty_for_a_header_without_the_fixed_separator(self) -> None:
        """The contract header must include both required lines."""
        body = (
            "| # | Location | Verdict | Justification |\n"
            "| 1 | `specs/spec.md:42` | `valid-no-action` | Already covered. |"
        )
        assert parse_verdict_rows(body) == []

    def test_returns_empty_for_a_header_without_data_rows(self) -> None:
        """A table start with no contiguous data rows is rejected."""
        body = "| # | Location | Verdict | Justification |\n| - | -------- | ------- | ------------- |"
        assert parse_verdict_rows(body) == []

    def test_returns_empty_for_a_fenced_example_table(self) -> None:
        """A contract example inside a fenced block is not treated as the live verdict table."""
        body = f"```\n{TABLE}\n```"
        assert parse_verdict_rows(body) == []

    def test_returns_empty_for_a_tilde_fenced_example_table(self) -> None:
        """A tilde-fenced contract example is not treated as the live verdict table."""
        body = f"~~~markdown\n{TABLE}\n~~~"
        assert parse_verdict_rows(body) == []

    def test_returns_empty_for_multiple_tables(self) -> None:
        """Exactly one contiguous verdict table is accepted."""
        body = f"{TABLE}\n\n{TABLE}"
        assert parse_verdict_rows(body) == []

    def test_returns_empty_for_empty_body(self) -> None:
        """An empty body is handled without raising."""
        assert parse_verdict_rows("") == []
