"""Tests for atomic Phase 3 artifact writes."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.run_phase3_gates import _write_atomically


def test_replaces_destination_with_complete_contents(tmp_path: Path) -> None:
    destination = tmp_path / "generated" / "result.json"

    _write_atomically(destination, '{"ok": true}\n')

    assert destination.read_text(encoding="utf-8") == '{"ok": true}\n'
    assert list(destination.parent.iterdir()) == [destination]


def test_cleans_up_temporary_file_when_replace_fails(tmp_path: Path) -> None:
    destination = tmp_path / "result.json"
    destination.write_text("old", encoding="utf-8")

    with patch("agentic_devtools.cli.speckit.run_phase3_gates.os.replace", side_effect=OSError("replace failed")):
        with pytest.raises(OSError, match="replace failed"):
            _write_atomically(destination, "new")

    assert destination.read_text(encoding="utf-8") == "old"
    assert list(tmp_path.iterdir()) == [destination]


def test_preserves_directory_when_temporary_file_creation_fails(tmp_path: Path) -> None:
    destination = tmp_path / "result.json"

    with patch(
        "agentic_devtools.cli.speckit.run_phase3_gates.tempfile.NamedTemporaryFile",
        side_effect=OSError("open failed"),
    ):
        with pytest.raises(OSError, match="open failed"):
            _write_atomically(destination, "new")

    assert list(tmp_path.iterdir()) == []
