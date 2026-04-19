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
        assert out.count("(none)") >= 5

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
