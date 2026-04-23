"""Visual snapshot tests for ``render_attribution_footer`` (#1473).

Captures what the user sees in three scenarios and pins the output with
Syrupy so any unintended rendering drift is caught as a diff. All
snapshots are generated with NO_COLOR to keep the .ambr files readable.

Run to (re-)generate::

    .venv/bin/python -m pytest tests/unit/test_attribution_footer_snapshot.py --snapshot-update -v

Three cases:
  (A) Normal counts: tools=2, turns=3, memory=0, sources=1, packs=0, instructions=1
  (B) Truncated-count display: tools=30 (SECTION_CAP+10), asserting the footer
      reads "30 tools" with the canonical count field present
  (C) Legacy fallback: a dict shaped like a pre-#1473 persisted snapshot
      (no ``<section>_count`` fields, ``tools`` list ends in
      ``{"truncated": 10}`` sentinel)
"""

from __future__ import annotations

import io
import re

import pytest
from rich.console import Console
from syrupy import SnapshotAssertion

from anteroom.cli import renderer
from anteroom.services.attribution import SECTION_CAP, build_attribution

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


@pytest.fixture(autouse=True)
def _no_color(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NO_COLOR", "1")


@pytest.fixture(autouse=True)
def _restore_midnight(monkeypatch: pytest.MonkeyPatch) -> None:
    from anteroom.cli.themes import CliTheme

    renderer.set_theme(CliTheme.load("midnight"))
    yield  # type: ignore[misc]
    renderer.set_theme(CliTheme.load("midnight"))


def _capture_footer(snapshot: object) -> str:
    """Render the footer into a fixed-width no-colour console and return plain text."""
    buf = io.StringIO()
    con = Console(file=buf, width=80, force_terminal=False, no_color=True)
    original = renderer.console
    renderer.console = con
    try:
        renderer.render_attribution_footer(snapshot)
    finally:
        renderer.console = original
    return _ANSI_RE.sub("", buf.getvalue())


# ---------------------------------------------------------------------------
# Case A — Normal counts
# ---------------------------------------------------------------------------


class TestNormalCountsSnapshot:
    def test_footer_normal_counts(self, snapshot: SnapshotAssertion) -> None:
        """tools=2, turns=3, memory=0, sources=1, packs=0, instructions=1."""
        turn_tcs = [{"id": f"tc-{i}", "tool_name": f"tool_{i}"} for i in range(2)]
        pm = {
            "context_turns": [{"id": f"m-{i}", "role": "user"} for i in range(3)],
            "rag_sources": [{"label": "README.md", "type": "source_chunk", "source_id": "s1"}],
            "memory_recall_items": [],
            "pack_attachments": [],
            "instruction_files": [{"path": "/repo/ANTEROOM.md", "scope": "project", "estimated_tokens": 500}],
        }
        snap = build_attribution(
            pm, {"id": "msg-1", "role": "assistant", "tool_calls": []}, [], turn_tool_calls=turn_tcs
        )
        out = _capture_footer(snap)
        assert out == snapshot


# ---------------------------------------------------------------------------
# Case B — Truncated-count display
# ---------------------------------------------------------------------------


class TestTruncatedCountSnapshot:
    def test_footer_truncated_tools_shows_real_count(self, snapshot: SnapshotAssertion) -> None:
        """30 items → canonical tools_count=30; footer must read '30 tools'."""
        turn_tcs = [{"id": f"tc-{i}", "tool_name": f"tool_{i}"} for i in range(SECTION_CAP + 10)]
        pm = {
            "context_turns": [],
            "rag_sources": [],
            "memory_recall_items": [],
            "pack_attachments": [],
            "instruction_files": [],
        }
        snap = build_attribution(
            pm, {"id": "msg-1", "role": "assistant", "tool_calls": []}, [], turn_tool_calls=turn_tcs
        )
        assert snap.tools_count == SECTION_CAP + 10
        out = _capture_footer(snap)
        assert "30 tools" in out, f"Expected '30 tools' in footer, got: {out!r}"
        assert "21 tools" not in out
        assert out == snapshot


# ---------------------------------------------------------------------------
# Case C — Legacy fallback (no <section>_count fields)
# ---------------------------------------------------------------------------


class TestLegacyFallbackSnapshot:
    def test_footer_legacy_dict_with_truncation_sentinel(self, snapshot: SnapshotAssertion) -> None:
        """Pre-#1473 persisted snapshot: tools list ends in sentinel, no count field.

        The footer must compute the correct count (30) from the sentinel,
        not from raw len (21).
        """
        tools_list = [{"id": f"tc-{i}", "name": f"tool_{i}"} for i in range(20)]
        tools_list.append({"truncated": 10})
        legacy_dict = {
            "turns": [{"message_id": "m-1", "role": "user"}],
            "memory": [],
            "sources": [],
            "tools": tools_list,
            "packs": [],
            "instructions": [],
            "dlp_match_count": 0,
            "output_filter_match_count": 0,
            # Deliberately no <section>_count fields — legacy shape.
        }
        out = _capture_footer(legacy_dict)
        assert "30 tools" in out, f"Expected '30 tools' in footer, got: {out!r}"
        assert out == snapshot
