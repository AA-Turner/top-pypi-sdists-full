"""Tests for _persist_response."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import patch

from agentic_devtools.orchestration.nodes._issue_retrieval import _persist_response


class TestPersistResponse:
    """Tests for best-effort JSON persistence."""

    def test_writes_data_to_file(self, tmp_path: Path) -> None:
        target = tmp_path / "response.json"
        _persist_response(target, {"key": "value", "num": 42})
        assert target.exists()
        payload = json.loads(target.read_text())
        assert payload == {"key": "value", "num": 42}

    def test_creates_parent_directories(self, tmp_path: Path) -> None:
        target = tmp_path / "a" / "b" / "response.json"
        _persist_response(target, {"x": 1})
        assert target.exists()

    def test_write_failure_is_best_effort(self, tmp_path: Path) -> None:
        target = tmp_path / "response.json"
        with patch("pathlib.Path.write_text", side_effect=OSError("disk full")):
            # Should not raise; failure is logged and silently swallowed
            _persist_response(target, {"data": "value"})

    def test_handles_non_serialisable_values_with_default_str(self, tmp_path: Path) -> None:
        target = tmp_path / "response.json"
        _persist_response(target, {"path": Path("/some/path")})
        payload = json.loads(target.read_text())
        assert payload["path"] == "/some/path"
