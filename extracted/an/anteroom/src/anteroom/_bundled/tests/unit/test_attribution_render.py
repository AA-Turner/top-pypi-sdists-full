"""Rendering tests for attribution footer + detail (#923).

Uses the same capture pattern as test_rag_status_snapshot.py. No external
Syrupy dependency — the assertions pin the human-meaningful substrings so
the tests are stable across Rich version bumps.
"""

from __future__ import annotations

from io import StringIO
from typing import Any

from rich.console import Console

from anteroom.services.attribution import AttributionSnapshot


def _capture_footer(snapshot: Any) -> str:
    """Capture ``render_attribution_footer`` output via the module console."""
    from anteroom.cli import renderer

    buf = StringIO()
    test_console = Console(file=buf, width=120, force_terminal=False, no_color=True)
    original = renderer.console
    renderer.console = test_console
    try:
        renderer.render_attribution_footer(snapshot)
    finally:
        renderer.console = original
    return buf.getvalue()


def _capture_detail(snapshot: Any) -> str:
    from anteroom.cli.attribution_render import render_attribution_detail

    buf = StringIO()
    test_console = Console(file=buf, width=120, force_terminal=False, no_color=True)
    render_attribution_detail(test_console, snapshot)
    return buf.getvalue()


def _sample_snapshot() -> AttributionSnapshot:
    return AttributionSnapshot(
        turns=[{"message_id": "m-1", "role": "user"}, {"message_id": "m-2", "role": "assistant"}],
        memory=[{"fqn": "@user/memory/pref", "scope": "user", "category": "preference", "distance": 0.12}],
        sources=[{"label": "README.md", "type": "source_chunk", "source_id": "s-1"}],
        tools=[{"id": "tc-1", "name": "read_file"}],
        packs=[{"namespace": "core", "name": "alpha", "scope": "global"}],
        dlp_match_count=0,
        output_filter_match_count=0,
    )


# ---------------------------------------------------------------------------
# Footer snapshot cases
# ---------------------------------------------------------------------------


class TestAttributionFooter:
    def test_none_snapshot_renders_nothing(self) -> None:
        assert _capture_footer(None) == ""

    def test_empty_snapshot(self) -> None:
        out = _capture_footer(AttributionSnapshot())
        assert "[ctx]" in out
        assert "0 turns" in out
        assert "0 memories" in out
        assert "/attribution for detail" in out

    def test_typical_counts(self) -> None:
        out = _capture_footer(_sample_snapshot())
        assert "[ctx]" in out
        assert "2 turns" in out
        assert "1 memories" in out
        assert "1 sources" in out
        assert "1 tools" in out
        assert "1 packs" in out
        assert "DLP:" not in out  # no redactions in sample
        assert "OF:" not in out

    def test_dlp_and_of_counters_surface_when_nonzero(self) -> None:
        snap = AttributionSnapshot(dlp_match_count=2, output_filter_match_count=1)
        out = _capture_footer(snap)
        assert "DLP:2" in out
        assert "OF:1" in out

    def test_bad_snapshot_renders_without_crashing(self) -> None:
        # Passing a plain object with missing attrs should render nothing and not raise.
        class _Bad:
            pass

        assert _capture_footer(_Bad()) == ""


# ---------------------------------------------------------------------------
# Detail rendering
# ---------------------------------------------------------------------------


class TestAttributionDetail:
    def test_empty_snapshot_shows_none_per_section(self) -> None:
        out = _capture_detail(AttributionSnapshot())
        assert "Recent turns" in out
        assert "Recalled memories" in out
        assert "RAG sources" in out
        assert "Tool calls" in out
        assert "Attached packs" in out
        assert out.count("(none)") >= 5

    def test_typical_snapshot_renders_all_sections(self) -> None:
        out = _capture_detail(_sample_snapshot())
        assert "Recent turns" in out
        assert "m-1" in out
        assert "@user/memory/pref" in out
        assert "README.md" in out
        assert "read_file" in out
        assert "core" in out

    def test_accepts_dict_from_persisted_metadata(self) -> None:
        """On conversation reload, attribution comes back as a plain dict."""
        persisted = {
            "turns": [{"message_id": "m-1", "role": "user"}],
            "memory": [],
            "sources": [],
            "tools": [],
            "packs": [],
            "dlp_match_count": 0,
            "output_filter_match_count": 0,
        }
        out = _capture_detail(persisted)
        assert "Recent turns" in out
        assert "m-1" in out

    def test_truncated_marker_renders_as_more_row(self) -> None:
        snap = AttributionSnapshot(
            tools=[{"id": f"tc-{i}", "name": f"tool{i}"} for i in range(5)] + [{"truncated": 12}]
        )
        out = _capture_detail(snap)
        assert "+12 more" in out

    def test_none_input_safe(self) -> None:
        out = _capture_detail(None)
        assert "No attribution recorded" in out
