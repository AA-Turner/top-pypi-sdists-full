"""Behavioural unit tests for ``render_attribution_footer`` (#1473).

Verifies that the footer renders counts correctly in four scenarios:

1. Normal counts — tools=2 shows "2 tools"
2. Truncated section — 30 items shows "30 tools" not "21 tools"
3. Legacy persisted dict (no ``<section>_count`` fields) falls back correctly
4. Zero-state — shows "0 tools"
"""

from __future__ import annotations

import io
import re

from rich.console import Console

from anteroom.cli import renderer
from anteroom.services.attribution import (
    SECTION_CAP,
    AttributionSnapshot,
    build_attribution,
)

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def _capture_footer(snapshot: object) -> str:
    """Capture ``render_attribution_footer`` output as plain text."""
    buf = io.StringIO()
    con = Console(file=buf, width=120, force_terminal=False, no_color=True)
    original = renderer.console
    renderer.console = con
    try:
        renderer.render_attribution_footer(snapshot)
    finally:
        renderer.console = original
    return _ANSI_RE.sub("", buf.getvalue())


# ---------------------------------------------------------------------------
# Test helpers
# ---------------------------------------------------------------------------


def _make_snap(
    tools: int = 0,
    turns: int = 0,
    memory: int = 0,
    sources: int = 0,
    packs: int = 0,
    instructions: int = 0,
) -> AttributionSnapshot:
    """Build a snapshot with the specified counts (small, no truncation)."""
    turn_tcs = [{"id": f"tc-{i}", "tool_name": f"tool_{i}"} for i in range(tools)]
    context_turns = [{"id": f"m-{i}", "role": "user"} for i in range(turns)]
    memory_items = [
        {"fqn": f"@user/memory/m{i}", "scope": "user", "category": "pref", "distance": 0.1} for i in range(memory)
    ]
    rag_sources = [{"label": f"src-{i}", "type": "source_chunk", "source_id": f"s{i}"} for i in range(sources)]
    instruction_files = [
        {"path": f"/path/ANTEROOM_{i}.md", "scope": "project", "estimated_tokens": 100} for i in range(instructions)
    ]
    pack_list = [{"namespace": f"ns{i}", "name": f"pack{i}"} for i in range(packs)]
    pack_attachments = [{"namespace": f"ns{i}", "name": f"pack{i}", "scope": "global"} for i in range(packs)]

    pm = {
        "context_turns": context_turns,
        "rag_sources": rag_sources,
        "memory_recall_items": memory_items,
        "pack_attachments": pack_attachments,
        "instruction_files": instruction_files,
    }

    return build_attribution(
        pm, {"id": "msg-1", "role": "assistant", "tool_calls": []}, pack_list, turn_tool_calls=turn_tcs
    )


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestNormalCounts:
    def test_tools_count_renders_correctly(self) -> None:
        snap = _make_snap(tools=2)
        out = _capture_footer(snap)
        assert "2 tools" in out

    def test_turns_count_renders_correctly(self) -> None:
        snap = _make_snap(turns=3)
        out = _capture_footer(snap)
        assert "3 turns" in out

    def test_memory_count_renders_correctly(self) -> None:
        snap = _make_snap(memory=5)
        out = _capture_footer(snap)
        assert "5 memories" in out

    def test_sources_count_renders_correctly(self) -> None:
        snap = _make_snap(sources=1)
        out = _capture_footer(snap)
        assert "1 sources" in out

    def test_instructions_renders_singular_noun(self) -> None:
        snap = _make_snap(instructions=1)
        out = _capture_footer(snap)
        assert "1 instruction file" in out

    def test_instructions_renders_plural_noun(self) -> None:
        snap = _make_snap(instructions=2)
        out = _capture_footer(snap)
        assert "2 instruction files" in out

    def test_footer_contains_attribution_hint(self) -> None:
        snap = _make_snap(tools=1)
        out = _capture_footer(snap)
        assert "/attribution" in out


class TestTruncatedCount:
    def test_30_tools_shows_30_not_21(self) -> None:
        """SECTION_CAP=20; 30 items → list len 21 (cap+sentinel).
        Footer must display 30 tools, not 21.
        """
        turn_tcs = [{"id": f"tc-{i}", "tool_name": f"tool_{i}"} for i in range(30)]
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
        assert snap.tools_count == 30
        out = _capture_footer(snap)
        assert "30 tools" in out
        assert "21 tools" not in out

    def test_truncated_memory_shows_real_count(self) -> None:
        """SECTION_CAP=20; 25 memories → memory_count=25 on footer."""
        memory_items = [
            {"fqn": f"@user/memory/m{i}", "scope": "user", "category": "pref", "distance": 0.1}
            for i in range(SECTION_CAP + 5)
        ]
        pm = {
            "context_turns": [],
            "rag_sources": [],
            "memory_recall_items": memory_items,
            "pack_attachments": [],
            "instruction_files": [],
        }
        snap = build_attribution(pm, {"id": "msg-1", "role": "assistant", "tool_calls": []}, [])
        out = _capture_footer(snap)
        assert "25 memories" in out
        assert "21 memories" not in out


class TestLegacyFallback:
    def test_older_persisted_dict_without_count_fields_falls_back(self) -> None:
        """Pre-#1473 snapshots lack ``<section>_count`` fields. The footer
        must still render a correct count using the truncation-aware fallback.
        """
        # 3 real tools, no truncation — fallback reads len(items)
        legacy_dict = {
            "turns": [{"message_id": "m-1", "role": "user"}],
            "memory": [],
            "sources": [],
            "tools": [
                {"id": "tc-1", "name": "read_file"},
                {"id": "tc-2", "name": "grep"},
                {"id": "tc-3", "name": "write_file"},
            ],
            "packs": [],
            "instructions": [],
            "dlp_match_count": 0,
            "output_filter_match_count": 0,
            # No <section>_count fields — this is the legacy shape.
        }
        out = _capture_footer(legacy_dict)
        assert "3 tools" in out

    def test_legacy_truncated_dict_fallback_computes_correct_count(self) -> None:
        """Pre-#1473 dict with truncation sentinel — fallback correctly
        computes real count from sentinel rather than raw len.
        """
        tools_list = [{"id": f"tc-{i}", "name": f"tool_{i}"} for i in range(20)]
        tools_list.append({"truncated": 10})
        legacy_dict = {
            "turns": [],
            "memory": [],
            "sources": [],
            "tools": tools_list,
            "packs": [],
            "instructions": [],
            "dlp_match_count": 0,
            "output_filter_match_count": 0,
            # No count fields — legacy.
        }
        out = _capture_footer(legacy_dict)
        assert "30 tools" in out
        assert "21 tools" not in out


class TestZeroState:
    def test_zero_tools_renders_0_tools(self) -> None:
        snap = build_attribution(
            {
                "context_turns": [],
                "rag_sources": [],
                "memory_recall_items": [],
                "pack_attachments": [],
                "instruction_files": [],
            },
            {"id": "msg-1", "role": "assistant", "tool_calls": []},
            [],
            turn_tool_calls=[],
        )
        out = _capture_footer(snap)
        assert "0 tools" in out

    def test_none_snapshot_renders_nothing(self) -> None:
        out = _capture_footer(None)
        assert out.strip() == ""

    def test_snap_with_turns_key_required(self) -> None:
        """Structural guard: dict without 'turns' key renders nothing."""
        out = _capture_footer({"memory": []})
        assert out.strip() == ""
