"""Tests for write_log in speckit/phase0/observability.py (FR-001)."""

from __future__ import annotations

import json
from pathlib import Path

from agentic_devtools.cli.speckit.phase0.observability import write_log


class TestWriteLog:
    """Tests for the write_log function."""

    def test_writes_valid_utf8_json_document(self, tmp_path: Path) -> None:
        document: dict[str, object] = {
            "schemaVersion": "1.0",
            "terminationCode": None,
            "run": {},
            "events": [],
        }
        destination = tmp_path / ".agdt" / "logs" / "phase0-20260101T000000Z-1-1.json"

        write_log(document, destination)

        assert destination.exists()
        loaded = json.loads(destination.read_text(encoding="utf-8"))
        assert loaded == document

    def test_creates_missing_parent_directories(self, tmp_path: Path) -> None:
        destination = tmp_path / "nested" / "dirs" / "log.json"
        write_log({"a": 1}, destination)
        assert destination.exists()

    def test_preserves_unicode_content(self, tmp_path: Path) -> None:
        destination = tmp_path / "log.json"
        document = {"message": "caf\u00e9"}
        write_log(document, destination)
        raw_text = destination.read_text(encoding="utf-8")
        assert "caf\u00e9" in raw_text
