"""Tests for render_markdown."""

from __future__ import annotations

from agentic_devtools.cli.checks.benchmark import render_markdown


class TestRenderMarkdown:
    """Tests for benchmark table formatting."""

    def test_renders_scenarios_as_markdown_table(self):
        result = render_markdown(
            [
                ("Typical small change", 1.25, "passed"),
                ("Giant-file change", 12.5, "passed"),
                ("Full suite", 45.0, "passed"),
            ],
            hardware="Windows, 8 logical CPUs",
        )

        assert "| Scenario | Seconds | Result |" in result
        assert "| Typical small change | 1.25 | passed |" in result
        assert "| Giant-file change | 12.50 | passed |" in result
        assert "| Full suite | 45.00 | passed |" in result
        assert "Windows, 8 logical CPUs" in result
