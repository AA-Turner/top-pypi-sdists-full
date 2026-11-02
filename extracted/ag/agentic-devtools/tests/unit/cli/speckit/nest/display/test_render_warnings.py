"""Unit tests for :func:`render_warnings`."""

from __future__ import annotations

from agentic_devtools.cli.speckit.nest.display import render_warnings


class TestRenderWarnings:
    """Behavior of the warning block renderer."""

    def test_returns_empty_string_for_no_warnings(self) -> None:
        """An empty warning list renders nothing at all."""
        assert render_warnings([]) == ""

    def test_renders_header_and_bulleted_warnings(self) -> None:
        """Each warning is rendered on its own labeled line under a header."""
        output = render_warnings(["issue #42 not found", "cycle detected"])

        lines = output.splitlines()
        assert lines[0] == "Warnings:"
        assert lines[2] == "  ⚠ issue #42 not found"
        assert lines[3] == "  ⚠ cycle detected"

    def test_preserves_input_order(self) -> None:
        """Warnings are rendered in the order supplied by the caller."""
        output = render_warnings(["first", "second", "third"])

        assert output.index("first") < output.index("second") < output.index("third")
