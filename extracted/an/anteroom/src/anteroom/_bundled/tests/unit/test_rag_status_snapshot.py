"""Snapshot tests for CLI RAG status and source badge rendering (#854).

Captures Rich console output to verify the exact format of RAG status
messages and source badge labels shown to the user.

Tests cover both COMPACT (default) and DETAILED verbosity modes (#1053).
"""

from __future__ import annotations

from io import StringIO
from types import SimpleNamespace

from rich.console import Console


class TestRagStatusSnapshot:
    """Verify render_rag_status produces expected terminal output."""

    def _capture_rag_status(self, status: str, **kwargs) -> str:
        from anteroom.cli import renderer

        buf = StringIO()
        test_console = Console(file=buf, width=120, force_terminal=False, no_color=True)
        original = renderer.console
        renderer.console = test_console
        try:
            renderer.render_rag_status(status, **kwargs)
        finally:
            renderer.console = original
        return buf.getvalue()

    # -- COMPACT mode (default) — suppresses low-value diagnostics (#1053) --

    def test_compact_ok_suppressed(self) -> None:
        from anteroom.cli import renderer
        from anteroom.cli.renderer import Verbosity

        renderer._verbosity = Verbosity.COMPACT
        output = self._capture_rag_status("ok", chunk_count=5)
        assert output == ""

    def test_compact_no_results_suppressed(self) -> None:
        from anteroom.cli import renderer
        from anteroom.cli.renderer import Verbosity

        renderer._verbosity = Verbosity.COMPACT
        output = self._capture_rag_status("no_results", reason="too short")
        assert output == ""

    def test_compact_failed_shows_softened_message(self) -> None:
        from anteroom.cli import renderer
        from anteroom.cli.renderer import Verbosity

        renderer._verbosity = Verbosity.COMPACT
        output = self._capture_rag_status("failed")
        assert "Knowledge search unavailable" in output
        assert "RAG" not in output

    def test_compact_no_vec_support_shows_softened_message(self) -> None:
        from anteroom.cli import renderer
        from anteroom.cli.renderer import Verbosity

        renderer._verbosity = Verbosity.COMPACT
        output = self._capture_rag_status("no_vec_support")
        assert "Knowledge search not configured" in output
        assert "RAG" not in output

    # -- DETAILED mode — full diagnostic output --

    def test_detailed_ok_status_shows_chunk_count(self) -> None:
        from anteroom.cli import renderer
        from anteroom.cli.renderer import Verbosity

        renderer._verbosity = Verbosity.DETAILED
        output = self._capture_rag_status("ok", chunk_count=5)
        assert "RAG: 5 relevant chunk(s) retrieved" in output

    def test_ok_status_zero_chunks_no_output(self) -> None:
        from anteroom.cli import renderer
        from anteroom.cli.renderer import Verbosity

        renderer._verbosity = Verbosity.DETAILED
        output = self._capture_rag_status("ok", chunk_count=0)
        assert output == ""

    def test_detailed_no_results_without_reason(self) -> None:
        from anteroom.cli import renderer
        from anteroom.cli.renderer import Verbosity

        renderer._verbosity = Verbosity.DETAILED
        output = self._capture_rag_status("no_results")
        assert "RAG: no results" in output
        assert " — " not in output

    def test_detailed_no_results_with_reason(self) -> None:
        from anteroom.cli import renderer
        from anteroom.cli.renderer import Verbosity

        renderer._verbosity = Verbosity.DETAILED
        output = self._capture_rag_status("no_results", reason="no matching content")
        assert "RAG: no results" in output
        assert "no matching content" in output

    def test_detailed_failed_status(self) -> None:
        from anteroom.cli import renderer
        from anteroom.cli.renderer import Verbosity

        renderer._verbosity = Verbosity.DETAILED
        output = self._capture_rag_status("failed")
        assert "RAG: retrieval failed" in output

    def test_detailed_no_vec_support_status(self) -> None:
        from anteroom.cli import renderer
        from anteroom.cli.renderer import Verbosity

        renderer._verbosity = Verbosity.DETAILED
        output = self._capture_rag_status("no_vec_support")
        assert "RAG: embedding service unavailable" in output

    def test_silent_statuses_produce_no_output(self) -> None:
        for status in ("disabled", "no_config", "skipped_plan_mode", "skipped"):
            output = self._capture_rag_status(status)
            assert output == "", f"Status '{status}' should produce no output, got: {output!r}"


class TestRagSourceBadgeSnapshot:
    """Verify render_rag_sources badge labels in captured output."""

    def _capture_rag_sources(self, chunks: list) -> str:
        from anteroom.cli import renderer

        buf = StringIO()
        test_console = Console(file=buf, width=120, force_terminal=False, no_color=True)
        original = renderer.console
        renderer.console = test_console
        try:
            renderer.render_rag_sources(chunks)
        finally:
            renderer.console = original
        return buf.getvalue()

    def test_knowledge_badge_for_source_chunk(self) -> None:
        chunk = SimpleNamespace(source_label="Q3 Report", source_type="source_chunk")
        output = self._capture_rag_sources([chunk])
        assert "knowledge" in output
        assert "Q3 Report" in output

    def test_conversation_badge_for_message(self) -> None:
        chunk = SimpleNamespace(source_label="Prior Chat", source_type="message")
        output = self._capture_rag_sources([chunk])
        assert "conversation" in output
        assert "Prior Chat" in output

    def test_dedup_same_label(self) -> None:
        chunks = [
            SimpleNamespace(source_label="Report", source_type="source_chunk"),
            SimpleNamespace(source_label="Report", source_type="source_chunk"),
        ]
        output = self._capture_rag_sources(chunks)
        assert output.count("Report") == 1

    def test_empty_chunks_no_output(self) -> None:
        output = self._capture_rag_sources([])
        assert output == ""

    def test_unknown_type_fallback(self) -> None:
        chunk = SimpleNamespace(source_label="Mystery", source_type="unknown_type")
        output = self._capture_rag_sources([chunk])
        assert "Mystery" in output
