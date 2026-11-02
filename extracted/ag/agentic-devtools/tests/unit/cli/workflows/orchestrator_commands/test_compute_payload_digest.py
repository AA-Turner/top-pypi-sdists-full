"""Tests for _compute_payload_digest."""

from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

from agentic_devtools.cli.workflows.orchestrator_commands import _compute_payload_digest


def test_compute_payload_digest_is_stable_for_nested_directories(tmp_path) -> None:
    root = tmp_path / "scratch"
    (root / "nested" / "deeper").mkdir(parents=True)
    (root / "nested" / "file.txt").write_text("payload", encoding="utf-8")

    assert _compute_payload_digest(root) == _compute_payload_digest(root)


def test_compute_payload_digest_changes_when_executable_bit_changes(tmp_path) -> None:
    root = tmp_path / "scratch"
    root.mkdir()
    script = root / "run.sh"
    script.write_text("#!/bin/sh\necho hi\n", encoding="utf-8")

    original_stat = Path.stat
    executable = False

    def stat(path: Path, *, follow_symlinks: bool = True):
        result = original_stat(path, follow_symlinks=follow_symlinks)
        if path == script:
            mode = result.st_mode | (0o111 if executable else 0)
            return SimpleNamespace(st_mode=mode, st_size=result.st_size)
        return result

    with patch("pathlib.Path.stat", stat):
        non_executable_digest = _compute_payload_digest(root)
        executable = True

        assert _compute_payload_digest(root) != non_executable_digest


def test_compute_payload_digest_rejects_symlinks(tmp_path) -> None:
    root = tmp_path / "scratch"
    root.mkdir()
    target = tmp_path / "outside.txt"
    target.write_text("secret", encoding="utf-8")
    (root / "linked.txt").symlink_to(target)

    with pytest.raises(ValueError, match="contains symlink"):
        _compute_payload_digest(root)


def test_compute_payload_digest_rejects_unsupported_path_types(tmp_path) -> None:
    root = tmp_path / "scratch"
    root.mkdir()
    unsupported_path = root / "named-pipe"
    unsupported_path.touch()
    original_is_file = Path.is_file

    def is_file(path: Path) -> bool:
        return False if path == unsupported_path else original_is_file(path)

    with patch.object(Path, "is_file", is_file):
        with pytest.raises(ValueError, match="unsupported path type"):
            _compute_payload_digest(root)
