from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from agentic_devtools.orchestration.safety.exceptions import WorktreeIsolationError
from agentic_devtools.orchestration.safety.isolation import WorktreeIsolationGuard


class TestWorktreeIsolationGuardErrorPaths:
    """Tests for WorktreeIsolationGuard helper and error branches."""

    @patch("agentic_devtools.orchestration.tools.builtins._get_allowed_roots")
    def test_resolve_allowed_roots_uses_builtins_helper(self, mock_get_allowed_roots) -> None:
        expected = [Path("/repo")]
        mock_get_allowed_roots.return_value = expected
        guard = WorktreeIsolationGuard()

        assert guard._resolve_allowed_roots() == expected

    @patch("agentic_devtools.orchestration.safety.isolation.pathlib.Path.resolve", side_effect=OSError("bad path"))
    def test_path_resolution_error_raises_worktree_isolation_error(self, _mock_resolve, tmp_path: Path) -> None:
        guard = WorktreeIsolationGuard(allowed_roots=[tmp_path])

        with pytest.raises(WorktreeIsolationError) as exc_info:
            guard.check("filesystem_write_file", {"path": "bad-path"})

        assert "bad-path" in str(exc_info.value)
        assert str(tmp_path) in str(exc_info.value)

    @patch("agentic_devtools.orchestration.safety.isolation.pathlib.Path", side_effect=TypeError("invalid path"))
    def test_non_pathlike_input_raises_worktree_isolation_error(self, _mock_path, tmp_path: Path) -> None:
        guard = WorktreeIsolationGuard(allowed_roots=[tmp_path])

        with pytest.raises(WorktreeIsolationError) as exc_info:
            guard.check("filesystem_write_file", {"path": object()})

        assert "outside allowed roots" in str(exc_info.value)
        assert str(tmp_path) in str(exc_info.value)

    def test_is_relative_to_error_continues_to_next_root(self, tmp_path: Path) -> None:
        root_one = tmp_path / "root-one"
        root_two = tmp_path / "root-two"
        resolved = MagicMock()
        resolved.is_relative_to.side_effect = [TypeError("bad root"), True]
        guard = WorktreeIsolationGuard(allowed_roots=[root_one, root_two])

        with patch(
            "agentic_devtools.orchestration.safety.isolation.pathlib.Path.resolve",
            return_value=resolved,
        ):
            guard.check("filesystem_write_file", {"path": str(root_two / "file.txt")})

        assert resolved.is_relative_to.call_count == 2
