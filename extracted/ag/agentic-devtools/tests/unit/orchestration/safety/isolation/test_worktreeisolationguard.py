"""Tests for WorktreeIsolationGuard — FR-008."""

from __future__ import annotations

import pathlib

import pytest

from agentic_devtools.orchestration.safety.exceptions import WorktreeIsolationError
from agentic_devtools.orchestration.safety.isolation import WorktreeIsolationGuard


class TestWorktreeIsolationGuard:
    """Tests for worktree isolation enforcement."""

    def test_non_file_writing_tool_passes(self, tmp_path: pathlib.Path) -> None:
        guard = WorktreeIsolationGuard(allowed_roots=[tmp_path])
        guard.check("filesystem_read_file", {"path": "/etc/passwd"})

    def test_write_within_root_passes(self, tmp_path: pathlib.Path) -> None:
        target = tmp_path / "subdir" / "file.txt"
        guard = WorktreeIsolationGuard(allowed_roots=[tmp_path])
        guard.check("filesystem_write_file", {"path": str(target)})

    def test_write_outside_root_raises(self, tmp_path: pathlib.Path) -> None:
        guard = WorktreeIsolationGuard(allowed_roots=[tmp_path])
        with pytest.raises(WorktreeIsolationError):
            guard.check("filesystem_write_file", {"path": "/etc/evil.txt"})

    def test_no_allowed_roots_rejects_all(self) -> None:
        guard = WorktreeIsolationGuard(allowed_roots=[])
        with pytest.raises(WorktreeIsolationError):
            guard.check("filesystem_write_file", {"path": "/any/path"})

    def test_multiple_roots_any_match_passes(self, tmp_path: pathlib.Path) -> None:
        root1 = tmp_path / "root1"
        root2 = tmp_path / "root2"
        root1.mkdir()
        root2.mkdir()
        guard = WorktreeIsolationGuard(allowed_roots=[root1, root2])
        guard.check("filesystem_write_file", {"path": str(root2 / "file.txt")})

    def test_no_path_in_inputs_passes(self, tmp_path: pathlib.Path) -> None:
        guard = WorktreeIsolationGuard(allowed_roots=[tmp_path])
        guard.check("filesystem_write_file", {"content": "data"})

    def test_none_inputs_passes(self, tmp_path: pathlib.Path) -> None:
        guard = WorktreeIsolationGuard(allowed_roots=[tmp_path])
        guard.check("filesystem_write_file", None)
