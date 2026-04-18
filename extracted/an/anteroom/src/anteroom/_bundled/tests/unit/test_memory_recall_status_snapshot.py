"""Visual snapshot tests for CLI memory recall status rendering (#921).

Mirrors tests/unit/test_rag_status_snapshot.py. Uses captured terminal output
rather than Syrupy's snapshot fixture so the output diff is reviewable as
plain assertions (same approach as test_rag_status_snapshot.py).
"""

from __future__ import annotations

from io import StringIO

from rich.console import Console


class TestMemoryRecallStatusSnapshot:
    """Verify render_memory_recall_status produces expected terminal output."""

    def _capture(self, status: str, **kwargs) -> str:
        from anteroom.cli import renderer

        buf = StringIO()
        test_console = Console(file=buf, width=120, force_terminal=False, no_color=True)
        original = renderer.console
        renderer.console = test_console
        try:
            renderer.render_memory_recall_status(status, **kwargs)
        finally:
            renderer.console = original
        return buf.getvalue()

    # -- gated off --

    def test_gated_off_produces_no_output(self) -> None:
        from anteroom.cli import renderer

        renderer.set_memory_recall_status_visible(False)
        try:
            assert self._capture("ok", count=3) == ""
        finally:
            renderer.set_memory_recall_status_visible(True)

    # -- COMPACT mode --

    def test_compact_ok_suppressed(self) -> None:
        from anteroom.cli import renderer
        from anteroom.cli.renderer import Verbosity

        renderer._verbosity = Verbosity.COMPACT
        output = self._capture("ok", count=3)
        assert output == ""

    def test_compact_failed_shows_softened(self) -> None:
        from anteroom.cli import renderer
        from anteroom.cli.renderer import Verbosity

        renderer._verbosity = Verbosity.COMPACT
        output = self._capture("failed")
        assert "Memory recall unavailable" in output

    def test_compact_no_vec_support_shows_softened(self) -> None:
        from anteroom.cli import renderer
        from anteroom.cli.renderer import Verbosity

        renderer._verbosity = Verbosity.COMPACT
        output = self._capture("no_vec_support")
        assert "Memory recall not configured" in output

    # -- DETAILED mode --

    def test_detailed_ok_shows_count(self) -> None:
        from anteroom.cli import renderer
        from anteroom.cli.renderer import Verbosity

        renderer._verbosity = Verbosity.DETAILED
        output = self._capture("ok", count=2)
        assert "Memory: 2 memory(ies) recalled" in output

    def test_detailed_ok_zero_count_suppressed(self) -> None:
        from anteroom.cli import renderer
        from anteroom.cli.renderer import Verbosity

        renderer._verbosity = Verbosity.DETAILED
        output = self._capture("ok", count=0)
        assert output == ""

    def test_detailed_no_results_with_reason(self) -> None:
        from anteroom.cli import renderer
        from anteroom.cli.renderer import Verbosity

        renderer._verbosity = Verbosity.DETAILED
        output = self._capture("no_results", reason="no_embeddings_yet")
        assert "Memory: no results" in output
        assert "no_embeddings_yet" in output

    def test_detailed_failed(self) -> None:
        from anteroom.cli import renderer
        from anteroom.cli.renderer import Verbosity

        renderer._verbosity = Verbosity.DETAILED
        output = self._capture("failed")
        assert "Memory: recall failed" in output

    def test_detailed_no_vec_support(self) -> None:
        from anteroom.cli import renderer
        from anteroom.cli.renderer import Verbosity

        renderer._verbosity = Verbosity.DETAILED
        output = self._capture("no_vec_support")
        assert "Memory: embedding service unavailable" in output
