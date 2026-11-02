"""Tests for ``_atomic_write_json``."""

import json
from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.scaffold_new_feature import _atomic_write_json


class TestAtomicWriteJson:
    """_atomic_write_json writes JSON atomically and rejects symlinks."""

    def test_writes_json_to_file(self, tmp_path: Path) -> None:
        target = tmp_path / "out.json"
        _atomic_write_json(target, {"key": "value"})
        data = json.loads(target.read_text(encoding="utf-8"))
        assert data == {"key": "value"}

    def test_rejects_symlink_target(self, tmp_path: Path) -> None:
        real_file = tmp_path / "real.json"
        real_file.write_text("{}", encoding="utf-8")
        link = tmp_path / "link.json"
        with patch.object(Path, "is_symlink", return_value=True), pytest.raises(ValueError, match="symlinked"):
            _atomic_write_json(link, {"x": 1})

    def test_cleans_up_temp_file_on_write_error(self, tmp_path: Path) -> None:
        target = tmp_path / "out.json"
        with patch("os.replace", side_effect=OSError("disk full")):
            with pytest.raises(OSError, match="disk full"):
                _atomic_write_json(target, {"key": "value"})
        # No stale temp files should remain
        tmp_files = list(tmp_path.glob(".out.json.*.tmp"))
        assert tmp_files == []

    def test_tolerates_missing_temp_file_during_cleanup(self, tmp_path: Path) -> None:
        target = tmp_path / "out.json"
        with (
            patch("os.replace", side_effect=OSError("disk full")),
            patch("os.unlink", side_effect=OSError("already gone")),
        ):
            with pytest.raises(OSError, match="disk full"):
                _atomic_write_json(target, {"key": "value"})

    def test_closes_fd_when_fdopen_raises(self, tmp_path: Path) -> None:
        target = tmp_path / "out.json"
        with patch("os.fdopen", side_effect=OSError("bad fd")):
            with pytest.raises(OSError, match="bad fd"):
                _atomic_write_json(target, {"key": "value"})
        # No stale temp files should remain
        tmp_files = list(tmp_path.glob(".out.json.*.tmp"))
        assert tmp_files == []

    def test_handles_unlink_failure_after_fdopen_error(self, tmp_path: Path) -> None:
        target = tmp_path / "out.json"
        with (
            patch("os.fdopen", side_effect=OSError("bad fd")),
            patch("os.unlink", side_effect=OSError("unlink failed")),
        ):
            with pytest.raises(OSError, match="bad fd"):
                _atomic_write_json(target, {"key": "value"})
