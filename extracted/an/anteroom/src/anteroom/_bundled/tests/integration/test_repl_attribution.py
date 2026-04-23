"""Integration tests for the /attribution REPL command (#923).

Drives ``_handle_attribution_command`` against a real Rich Console so
the round trip (renderer state → detail rendering) is covered. Uses
the same capture pattern as ``test_repl_memory.py``.
"""

from __future__ import annotations

import io
import re

from rich.console import Console

from anteroom.cli import renderer
from anteroom.cli.repl import _handle_attribution_command, _restore_last_attribution_from
from anteroom.services.attribution import AttributionSnapshot

_ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def _capture() -> str:
    buf = io.StringIO()
    console = Console(file=buf, width=120, force_terminal=False, no_color=True)
    original = renderer.console
    renderer.console = console
    try:
        _handle_attribution_command()
    finally:
        renderer.console = original
    return _ANSI_RE.sub("", buf.getvalue())


def _reset_state() -> None:
    renderer.set_last_attribution(None)


class TestAttributionCommand:
    def test_no_snapshot_prints_informational_message(self) -> None:
        _reset_state()
        out = _capture()
        assert "No attribution recorded" in out

    def test_cached_snapshot_renders_all_sections(self) -> None:
        snap = AttributionSnapshot(
            turns=[{"message_id": "m-1", "role": "user"}],
            memory=[{"fqn": "@user/memory/pref", "scope": "user", "category": "preference"}],
            sources=[{"label": "README.md", "type": "source_chunk"}],
            tools=[{"id": "tc-1", "name": "read_file"}],
            packs=[{"namespace": "core", "name": "alpha", "scope": "global"}],
        )
        renderer.set_last_attribution(snap)
        try:
            out = _capture()
        finally:
            _reset_state()
        assert "Recent turns" in out
        assert "Recalled memories" in out
        assert "RAG sources" in out
        assert "Tool calls" in out
        assert "Attached packs" in out
        assert "m-1" in out
        assert "@user/memory/pref" in out
        assert "README.md" in out
        assert "read_file" in out
        assert "core" in out

    def test_cached_empty_snapshot_renders_none_per_section(self) -> None:
        renderer.set_last_attribution(AttributionSnapshot())
        try:
            out = _capture()
        finally:
            _reset_state()
        # Six sections (turns, memory, sources, tools, packs, instructions).
        assert out.count("(none)") >= 6

    def test_snapshot_surfaces_loaded_instructions_both_scopes(self) -> None:
        """`/attribution` detail renders both global + project rows when
        ``_load_instructions_with_trust`` reported them as loaded (#1462)."""
        snap = AttributionSnapshot(
            instructions=[
                {
                    "path": "/home/u/.anteroom/ANTEROOM.md",
                    "scope": "global",
                    "estimated_tokens": 512,
                },
                {
                    "path": "/repo/ANTEROOM.md",
                    "scope": "project",
                    "estimated_tokens": 9894,
                },
            ]
        )
        renderer.set_last_attribution(snap)
        try:
            out = _capture()
        finally:
            _reset_state()
        assert "Project instructions" in out
        # Both rows render.
        assert "/home/u/.anteroom/ANTEROOM.md" in out
        assert "/repo/ANTEROOM.md" in out
        assert "global" in out
        assert "project" in out
        # Header summary counts both files with the plural noun.
        assert "2 instruction files" in out

    def test_snapshot_hides_instructions_when_none_loaded(self) -> None:
        """With no instruction files loaded (``--no-project-context`` or no
        file on disk), the section renders ``(none)`` and the summary omits
        any instructions counter."""
        snap = AttributionSnapshot(
            turns=[{"message_id": "m-1", "role": "user"}],
            instructions=[],
        )
        renderer.set_last_attribution(snap)
        try:
            out = _capture()
        finally:
            _reset_state()
        assert "Project instructions" in out
        # The section header line lives above its "(none)" body.
        assert "instruction file" not in out

    def test_persisted_dict_round_trip(self) -> None:
        """Setter accepts the serialised dict shape (as would arrive on conversation reload)."""
        persisted = {
            "turns": [{"message_id": "m-9", "role": "assistant"}],
            "memory": [],
            "sources": [],
            "tools": [],
            "packs": [],
            "dlp_match_count": 0,
            "output_filter_match_count": 0,
        }
        renderer.set_last_attribution(persisted)
        try:
            out = _capture()
        finally:
            _reset_state()
        assert "Recent turns" in out
        assert "m-9" in out


class TestRestoreLastAttributionFrom:
    """Resume parity: ``/attribution`` must work right after reload (#923)."""

    def _assistant_with_attribution(self, payload: dict | str | None) -> dict:
        metadata: dict | str | None
        if payload is None:
            metadata = None
        elif isinstance(payload, str):
            metadata = payload
        else:
            metadata = {"attribution": payload}
        return {"id": "msg-a", "role": "assistant", "content": "hi", "metadata": metadata}

    def test_restores_from_dict_metadata(self) -> None:
        _reset_state()
        stored = [
            {"id": "u-1", "role": "user", "content": "q", "metadata": None},
            self._assistant_with_attribution(
                {
                    "turns": [{"message_id": "m-1", "role": "user"}],
                    "memory": [],
                    "sources": [],
                    "tools": [],
                    "packs": [],
                    "dlp_match_count": 0,
                    "output_filter_match_count": 0,
                }
            ),
        ]
        _restore_last_attribution_from(stored)
        snap = renderer.get_last_attribution()
        assert isinstance(snap, dict)
        assert snap["turns"] == [{"message_id": "m-1", "role": "user"}]
        _reset_state()

    def test_restores_from_json_string_metadata(self) -> None:
        """Storage can return metadata as raw JSON string — must deserialize."""
        import json as _json

        _reset_state()
        attribution = {
            "turns": [],
            "memory": [],
            "sources": [{"label": "README", "type": "source_chunk"}],
            "tools": [],
            "packs": [],
            "dlp_match_count": 0,
            "output_filter_match_count": 0,
        }
        stored = [
            self._assistant_with_attribution(_json.dumps({"attribution": attribution})),
        ]
        _restore_last_attribution_from(stored)
        snap = renderer.get_last_attribution()
        assert isinstance(snap, dict)
        assert snap["sources"][0]["label"] == "README"
        _reset_state()

    def test_persisted_instructions_field_round_trips(self) -> None:
        """Messages persisted with the #1462 ``instructions`` field must
        survive the reload path and surface in the restored snapshot."""
        _reset_state()
        attribution = {
            "turns": [],
            "memory": [],
            "sources": [],
            "tools": [],
            "packs": [],
            "instructions": [
                {
                    "path": "/repo/ANTEROOM.md",
                    "scope": "project",
                    "estimated_tokens": 9894,
                }
            ],
            "dlp_match_count": 0,
            "output_filter_match_count": 0,
        }
        stored = [self._assistant_with_attribution(attribution)]
        _restore_last_attribution_from(stored)
        snap = renderer.get_last_attribution()
        assert isinstance(snap, dict)
        assert len(snap["instructions"]) == 1
        assert snap["instructions"][0]["scope"] == "project"
        assert snap["instructions"][0]["path"] == "/repo/ANTEROOM.md"
        _reset_state()

    def test_older_persisted_snapshot_without_instructions_key(self) -> None:
        """Backwards compat: a snapshot written before #1462 has no
        ``instructions`` key. The reload path must not crash and the
        renderer must default to an empty list."""
        _reset_state()
        attribution = {
            "turns": [{"message_id": "m-1", "role": "user"}],
            "memory": [],
            "sources": [],
            "tools": [],
            "packs": [],
            "dlp_match_count": 0,
            "output_filter_match_count": 0,
        }
        stored = [self._assistant_with_attribution(attribution)]
        _restore_last_attribution_from(stored)
        snap = renderer.get_last_attribution()
        assert isinstance(snap, dict)
        # The render path must tolerate the absence of the key (the
        # attribution_render `_get` helper returns [] for missing keys).
        try:
            out = _capture()
        finally:
            _reset_state()
        # Pre-#1462 snapshot renders cleanly including the new section.
        assert "Project instructions" in out
        assert "(none)" in out

    def test_no_attribution_key_sets_none(self) -> None:
        _reset_state()
        renderer.set_last_attribution({"turns": []})  # priming garbage
        stored = [self._assistant_with_attribution({"rag_sources": []})]  # metadata with no attribution
        # payload above wraps under 'attribution' key; bypass by constructing directly
        stored = [{"id": "a", "role": "assistant", "content": "x", "metadata": {"rag_sources": []}}]
        _restore_last_attribution_from(stored)
        assert renderer.get_last_attribution() is None

    def test_no_assistant_messages_sets_none(self) -> None:
        _reset_state()
        renderer.set_last_attribution({"turns": [1]})
        stored = [{"id": "u", "role": "user", "content": "x", "metadata": None}]
        _restore_last_attribution_from(stored)
        assert renderer.get_last_attribution() is None

    def test_malformed_json_metadata_safe(self) -> None:
        _reset_state()
        renderer.set_last_attribution({"turns": []})
        stored = [{"id": "a", "role": "assistant", "content": "x", "metadata": "{not-json"}]
        _restore_last_attribution_from(stored)
        assert renderer.get_last_attribution() is None

    def test_picks_last_assistant_when_multiple(self) -> None:
        _reset_state()
        stored = [
            self._assistant_with_attribution(
                {
                    "turns": [{"message_id": "old"}],
                    "memory": [],
                    "sources": [],
                    "tools": [],
                    "packs": [],
                    "dlp_match_count": 0,
                    "output_filter_match_count": 0,
                }
            ),
            {"id": "u", "role": "user", "content": "x", "metadata": None},
            self._assistant_with_attribution(
                {
                    "turns": [{"message_id": "new"}],
                    "memory": [],
                    "sources": [],
                    "tools": [],
                    "packs": [],
                    "dlp_match_count": 0,
                    "output_filter_match_count": 0,
                }
            ),
        ]
        _restore_last_attribution_from(stored)
        snap = renderer.get_last_attribution()
        assert isinstance(snap, dict)
        assert snap["turns"][0]["message_id"] == "new"
        _reset_state()


class TestCliTurnToolCallAggregation:
    """Regression for #1472: CLI multi-iteration turns must aggregate all
    tool calls into the attribution snapshot, even when the final stored
    assistant message has no ``tool_calls`` (the final iteration was
    prose-only).

    Exercises the contract between ``renderer._current_turn_tools``
    (accumulator) and ``services.attribution.build_attribution`` (consumer
    via the new ``turn_tool_calls`` kwarg).
    """

    def test_build_attribution_reflects_renderer_turn_tools_across_iterations(self) -> None:
        from anteroom.services.attribution import build_attribution

        # Simulate the renderer accumulating tools as the agent loop runs
        # across multiple LLM iterations. ``clear_turn_history`` is what
        # the REPL calls at each user turn boundary.
        renderer.clear_turn_history()
        # Iteration 1: read_file
        renderer._current_turn_tools.append(
            {
                "tool_name": "read_file",
                "arguments": {"path": "README.md"},
                "summary": "read README.md",
                "status": "success",
                "output": None,
                "start_time": 0.0,
                "id": "tc-1",
            }
        )
        # Iteration 2: grep
        renderer._current_turn_tools.append(
            {
                "tool_name": "grep",
                "arguments": {"pattern": "foo"},
                "summary": "grep foo",
                "status": "success",
                "output": None,
                "start_time": 0.0,
                "id": "tc-2",
            }
        )
        # Iteration 3: bash
        renderer._current_turn_tools.append(
            {
                "tool_name": "bash",
                "arguments": {"command": "ls"},
                "summary": "bash ls",
                "status": "success",
                "output": None,
                "start_time": 0.0,
                "id": "tc-3",
            }
        )
        # Final iteration: pure prose — the stored assistant message has no tool_calls.
        stored_msg = {"id": "msg-final", "role": "assistant", "tool_calls": []}
        # Build the per-turn list the same way the REPL call site does.
        turn_tcs = [
            {
                "id": entry.get("id") or "",
                "tool_name": entry.get("tool_name", ""),
                "name": entry.get("tool_name", ""),
                "arguments": entry.get("arguments", {}),
                "status": entry.get("status", ""),
            }
            for entry in list(renderer._current_turn_tools)
        ]
        snap = build_attribution(
            {"context_turns": [], "rag_sources": [], "memory_recall_items": [], "pack_attachments": []},
            stored_msg,
            [],
            turn_tool_calls=turn_tcs,
        )
        # Pre-#1472: the stored-message fallback returned 0. The fix
        # surfaces all three tools.
        assert len(snap.tools) == 3
        assert [t["name"] for t in snap.tools] == ["read_file", "grep", "bash"]
        renderer.clear_turn_history()

    def test_attribution_footer_renders_correct_tool_count(self) -> None:
        """End-to-end: build the snapshot, cache it, render ``/attribution``
        detail, assert the ``Tool calls`` section surfaces all tools from the
        turn rather than the ``(none)`` default seen before the fix.
        """
        from anteroom.services.attribution import build_attribution

        renderer.clear_turn_history()
        renderer._current_turn_tools.extend(
            [
                {
                    "tool_name": "read_file",
                    "arguments": {"path": "a.py"},
                    "summary": "",
                    "status": "success",
                    "output": None,
                    "start_time": 0.0,
                    "id": "tc-1",
                },
                {
                    "tool_name": "write_file",
                    "arguments": {"path": "b.py"},
                    "summary": "",
                    "status": "success",
                    "output": None,
                    "start_time": 0.0,
                    "id": "tc-2",
                },
            ]
        )
        turn_tcs = [
            {
                "id": entry["id"],
                "tool_name": entry["tool_name"],
                "name": entry["tool_name"],
                "arguments": entry["arguments"],
                "status": entry["status"],
            }
            for entry in list(renderer._current_turn_tools)
        ]
        snap = build_attribution(
            {"context_turns": [], "rag_sources": [], "memory_recall_items": [], "pack_attachments": []},
            {"id": "msg-prose", "role": "assistant", "tool_calls": []},
            [],
            turn_tool_calls=turn_tcs,
        )
        renderer.set_last_attribution(snap)
        try:
            out = _capture()
        finally:
            _reset_state()
            renderer.clear_turn_history()
        assert "Tool calls" in out
        assert "read_file" in out
        assert "write_file" in out


# ---------------------------------------------------------------------------
# Canonical count field round-trip tests (#1473)
# ---------------------------------------------------------------------------


class TestCanonicalCountRoundTrip:
    """Verify that canonical count fields survive persist → reload → render (#1473)."""

    def _assistant_with_attribution(self, payload: dict) -> dict:
        return {"id": "msg-a", "role": "assistant", "content": "hi", "metadata": {"attribution": payload}}

    def test_reload_parity_all_six_sections(self) -> None:
        """Persist a snapshot with all six sections populated; reload via
        ``_restore_last_attribution_from`` and assert the restored dict
        carries all count fields with the correct values.
        """
        from anteroom.services.attribution import build_attribution, serialize_attribution

        pm = {
            "context_turns": [{"id": f"m-{i}", "role": "user"} for i in range(2)],
            "rag_sources": [{"label": "README.md", "type": "source_chunk", "source_id": "s1"}],
            "memory_recall_items": [
                {"fqn": "@user/memory/pref", "scope": "user", "category": "preference", "distance": 0.1},
                {"fqn": "@user/memory/ctx", "scope": "user", "category": "context", "distance": 0.2},
                {"fqn": "@user/memory/fact", "scope": "user", "category": "fact", "distance": 0.3},
            ],
            "pack_attachments": [],
            "instruction_files": [{"path": "/repo/ANTEROOM.md", "scope": "project", "estimated_tokens": 500}],
        }
        turn_tcs = [{"id": f"tc-{i}", "tool_name": f"tool_{i}"} for i in range(4)]
        snap = build_attribution(
            pm,
            {"id": "msg-1", "role": "assistant", "tool_calls": []},
            [],
            turn_tool_calls=turn_tcs,
        )
        serialized = serialize_attribution(snap)

        # Simulate persist → reload cycle.
        _reset_state()
        stored = [self._assistant_with_attribution(serialized)]
        _restore_last_attribution_from(stored)
        restored = renderer.get_last_attribution()
        assert isinstance(restored, dict)

        # All six canonical count fields must survive the round-trip.
        assert restored["turns_count"] == 2
        assert restored["memory_count"] == 3
        assert restored["sources_count"] == 1
        assert restored["tools_count"] == 4
        assert restored["packs_count"] == 0
        assert restored["instructions_count"] == 1
        _reset_state()

    def test_truncation_round_trip_footer_shows_real_count(self) -> None:
        """Persist a snapshot with tools_count=30; reload and assert the
        footer renders '30 tools' not '21 tools'.
        """
        import io as _io
        import re as _re

        from anteroom.services.attribution import build_attribution, serialize_attribution

        _ansi_re = _re.compile(r"\x1b\[[0-9;]*m")

        pm = {
            "context_turns": [],
            "rag_sources": [],
            "memory_recall_items": [],
            "pack_attachments": [],
            "instruction_files": [],
        }
        turn_tcs = [{"id": f"tc-{i}", "tool_name": f"tool_{i}"} for i in range(30)]
        snap = build_attribution(
            pm, {"id": "msg-1", "role": "assistant", "tool_calls": []}, [], turn_tool_calls=turn_tcs
        )
        assert snap.tools_count == 30
        serialized = serialize_attribution(snap)
        assert serialized["tools_count"] == 30

        # Simulate persist → reload.
        _reset_state()
        stored = [self._assistant_with_attribution(serialized)]
        _restore_last_attribution_from(stored)
        restored = renderer.get_last_attribution()
        assert isinstance(restored, dict)
        assert restored["tools_count"] == 30

        # Render the footer and assert it shows 30, not 21.
        buf = _io.StringIO()
        con = Console(file=buf, width=120, force_terminal=False, no_color=True)
        original = renderer.console
        renderer.console = con
        try:
            renderer.render_attribution_footer(restored)
        finally:
            renderer.console = original
        out = _ansi_re.sub("", buf.getvalue())
        assert "30 tools" in out
        assert "21 tools" not in out
        _reset_state()
