"""Tests for filesystem path containment helpers and tool functions."""

from __future__ import annotations

import pathlib
import subprocess
from unittest.mock import patch

from agentic_devtools.orchestration.tools.builtins import (
    _get_allowed_roots,
    _get_cached_git_root,
    _resolve_contained_path,
    register_all_builtins,
)
from agentic_devtools.orchestration.tools.registry import ConcreteToolRegistry


class TestResolveContainedPath:
    """Tests for _resolve_contained_path()."""

    def test_path_inside_root_is_accepted(self, tmp_path):
        """A path inside an allowed root resolves to an absolute Path."""
        target = tmp_path / "subdir" / "file.txt"
        result = _resolve_contained_path(str(target), [tmp_path])
        assert result is not None
        assert result.is_relative_to(tmp_path)

    def test_path_outside_root_returns_none(self, tmp_path):
        """A path outside the allowed root returns None."""
        allowed = tmp_path / "workspace"
        allowed.mkdir()
        outside = tmp_path / "other" / "secret.txt"
        result = _resolve_contained_path(str(outside), [allowed])
        assert result is None

    def test_dotdot_traversal_returns_none(self, tmp_path):
        """Path traversal via '../' that escapes the root returns None."""
        allowed = tmp_path / "workspace"
        allowed.mkdir()
        traversal = str(allowed / ".." / ".." / "etc" / "passwd")
        result = _resolve_contained_path(traversal, [allowed])
        assert result is None

    def test_symlink_escaping_root_returns_none(self, tmp_path):
        """A symlink that resolves outside the allowed root returns None."""
        allowed = tmp_path / "workspace"
        allowed.mkdir()
        outside = tmp_path / "secret.txt"
        outside.write_text("secret")
        link = allowed / "link.txt"
        link.symlink_to(outside)
        result = _resolve_contained_path(str(link), [allowed])
        assert result is None

    def test_root_itself_is_accepted(self, tmp_path):
        """The root directory itself is within the allowed root."""
        result = _resolve_contained_path(str(tmp_path), [tmp_path])
        assert result is not None

    def test_multiple_roots_any_match_accepted(self, tmp_path):
        """A path contained by any of the allowed roots is accepted."""
        root1 = tmp_path / "a"
        root1.mkdir()
        root2 = tmp_path / "b"
        root2.mkdir()
        target = root2 / "file.txt"
        result = _resolve_contained_path(str(target), [root1, root2])
        assert result is not None
        assert result.is_relative_to(root2)

    def test_resolve_raises_returns_none(self, tmp_path):
        """Returns None when Path.resolve() raises unexpectedly."""
        with patch.object(pathlib.Path, "resolve", side_effect=OSError("resolve failed")):
            result = _resolve_contained_path(str(tmp_path / "file.txt"), [tmp_path])
        assert result is None

    def test_is_relative_to_raises_returns_none(self, tmp_path):
        """Returns None when is_relative_to() raises for every root."""
        with patch.object(pathlib.Path, "is_relative_to", side_effect=TypeError("unexpected")):
            result = _resolve_contained_path(str(tmp_path / "file.txt"), [tmp_path])
        assert result is None


class TestGetAllowedRoots:
    """Tests for _get_allowed_roots()."""

    def setup_method(self):
        """Reset git-root cache between tests for deterministic behavior."""
        _get_cached_git_root.cache_clear()

    def test_returns_at_least_one_root(self):
        """_get_allowed_roots always returns at least one root."""
        roots = _get_allowed_roots()
        assert len(roots) >= 1

    def test_roots_are_resolved_paths(self):
        """All returned roots are absolute resolved Path objects."""
        for root in _get_allowed_roots():
            assert isinstance(root, pathlib.Path)
            assert root.is_absolute()

    def test_state_dir_fallback_when_git_unavailable(self, tmp_path):
        """Falls back to AGDT state dir when git rev-parse fails."""
        fake_result = subprocess.CompletedProcess(args=[], returncode=128, stdout="", stderr="not a git repo")
        state_dir = tmp_path / "state"
        state_dir.mkdir()
        with patch(
            "agentic_devtools.orchestration.tools.builtins.subprocess.run",
            return_value=fake_result,
        ):
            with patch("agentic_devtools.state.get_state_dir", return_value=str(state_dir)):
                roots = _get_allowed_roots()
        assert state_dir.resolve() in roots
        assert tmp_path.resolve() not in roots

    def test_cwd_fallback_when_subprocess_raises(self, tmp_path):
        """Returns empty list (fail-closed) when git and state dir are both unavailable."""
        with patch(
            "agentic_devtools.orchestration.tools.builtins.subprocess.run",
            side_effect=FileNotFoundError("git not found"),
        ):
            with patch(
                "agentic_devtools.state.get_state_dir",
                side_effect=RuntimeError("state dir unavailable"),
            ):
                roots = _get_allowed_roots()
        # Fail-closed: CWD must NOT be added when no authoritative root is found.
        assert roots == []

    def test_state_dir_outside_repo_is_appended_to_roots(self, tmp_path):
        """State dir outside the git root is added as an extra allowed root."""
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        external_state_dir = tmp_path / "external-state"
        external_state_dir.mkdir()

        fake_result = subprocess.CompletedProcess(args=[], returncode=0, stdout=str(repo_root), stderr="")
        with patch(
            "agentic_devtools.orchestration.tools.builtins.subprocess.run",
            return_value=fake_result,
        ):
            with patch(
                "agentic_devtools.state.get_state_dir",
                return_value=str(external_state_dir),
            ):
                roots = _get_allowed_roots()

        assert repo_root.resolve() in roots
        assert external_state_dir.resolve() in roots

    def test_state_dir_exception_still_returns_roots(self, tmp_path):
        """get_state_dir raising returns empty list when git is also unavailable."""
        with patch(
            "agentic_devtools.orchestration.tools.builtins.subprocess.run",
            side_effect=FileNotFoundError("git not found"),
        ):
            with patch(
                "agentic_devtools.state.get_state_dir",
                side_effect=RuntimeError("state dir unavailable"),
            ):
                roots = _get_allowed_roots()
        # Fail-closed: both sources failed → no roots, no CWD fallback.
        assert roots == []

    def test_git_root_lookup_is_cached(self, tmp_path):
        """Successful git root lookup is reused across repeated calls."""
        repo_root = tmp_path / "repo"
        repo_root.mkdir()
        fake_result = subprocess.CompletedProcess(args=[], returncode=0, stdout=str(repo_root), stderr="")
        with patch(
            "agentic_devtools.orchestration.tools.builtins.subprocess.run",
            return_value=fake_result,
        ) as mock_run:
            with patch("agentic_devtools.state.get_state_dir", return_value=str(repo_root)):
                first_roots = _get_allowed_roots()
                second_roots = _get_allowed_roots()

        assert repo_root.resolve() in first_roots
        assert repo_root.resolve() in second_roots
        assert mock_run.call_count == 1

    def test_git_lookup_failure_is_cached(self):
        """Failed git root lookup is cached and does not retry subprocess."""
        with patch(
            "agentic_devtools.orchestration.tools.builtins.subprocess.run",
            side_effect=FileNotFoundError("git not found"),
        ) as mock_run:
            first_root = _get_cached_git_root()
            second_root = _get_cached_git_root()

        assert first_root is None
        assert second_root is None
        assert mock_run.call_count == 1


class TestFilesystemToolsContainment:
    """Integration tests: filesystem builtins reject out-of-root paths."""

    def _make_registry(self):
        registry = ConcreteToolRegistry()
        register_all_builtins(registry)
        return registry

    def _with_root(self, tmp_path):
        """Context: patch _get_allowed_roots to only allow tmp_path."""
        return patch(
            "agentic_devtools.orchestration.tools.builtins._get_allowed_roots",
            return_value=[tmp_path.resolve()],
        )

    def test_read_file_inside_root_succeeds(self, tmp_path):
        """filesystem_read_file reads a file inside the allowed root."""
        f = tmp_path / "hello.txt"
        f.write_text("world")
        registry = self._make_registry()
        fn = registry.get_function("filesystem_read_file")
        with self._with_root(tmp_path):
            result = fn(path=str(f))
        assert result["success"] is True
        assert result["content"] == "world"

    def test_read_file_outside_root_fails(self, tmp_path):
        """filesystem_read_file rejects paths outside the allowed root."""
        allowed = tmp_path / "workspace"
        allowed.mkdir()
        outside = tmp_path / "outside.txt"
        outside.write_text("secret")
        registry = self._make_registry()
        fn = registry.get_function("filesystem_read_file")
        with patch(
            "agentic_devtools.orchestration.tools.builtins._get_allowed_roots",
            return_value=[allowed.resolve()],
        ):
            result = fn(path=str(outside))
        assert result["success"] is False
        assert "allowed roots" in result["error"]

    def test_write_file_inside_root_succeeds(self, tmp_path):
        """filesystem_write_file writes a file inside the allowed root."""
        target = tmp_path / "out.txt"
        registry = self._make_registry()
        fn = registry.get_function("filesystem_write_file")
        with self._with_root(tmp_path):
            result = fn(path=str(target), content="hello")
        assert result["success"] is True
        assert target.read_text() == "hello"

    def test_write_file_outside_root_fails(self, tmp_path):
        """filesystem_write_file rejects paths outside the allowed root."""
        allowed = tmp_path / "workspace"
        allowed.mkdir()
        outside = tmp_path / "sensitive.txt"
        registry = self._make_registry()
        fn = registry.get_function("filesystem_write_file")
        with patch(
            "agentic_devtools.orchestration.tools.builtins._get_allowed_roots",
            return_value=[allowed.resolve()],
        ):
            result = fn(path=str(outside), content="bad")
        assert result["success"] is False
        assert "allowed roots" in result["error"]
        assert not outside.exists()

    def test_list_directory_inside_root_succeeds(self, tmp_path):
        """filesystem_list_directory lists a directory inside the allowed root."""
        (tmp_path / "a.txt").write_text("a")
        (tmp_path / "b.txt").write_text("b")
        registry = self._make_registry()
        fn = registry.get_function("filesystem_list_directory")
        with self._with_root(tmp_path):
            result = fn(path=str(tmp_path))
        assert result["success"] is True
        names = [e["name"] for e in result["entries"]]
        assert "a.txt" in names

    def test_list_directory_outside_root_fails(self, tmp_path):
        """filesystem_list_directory rejects directories outside the allowed root."""
        allowed = tmp_path / "workspace"
        allowed.mkdir()
        registry = self._make_registry()
        fn = registry.get_function("filesystem_list_directory")
        with patch(
            "agentic_devtools.orchestration.tools.builtins._get_allowed_roots",
            return_value=[allowed.resolve()],
        ):
            result = fn(path=str(tmp_path))
        assert result["success"] is False
        assert "allowed roots" in result["error"]

    def test_symlink_escaping_root_is_rejected_on_read(self, tmp_path):
        """Symlink pointing outside the workspace root is rejected."""
        workspace = tmp_path / "workspace"
        workspace.mkdir()
        outside = tmp_path / "secret.txt"
        outside.write_text("secret")
        link = workspace / "link.txt"
        link.symlink_to(outside)
        registry = self._make_registry()
        fn = registry.get_function("filesystem_read_file")
        with patch(
            "agentic_devtools.orchestration.tools.builtins._get_allowed_roots",
            return_value=[workspace.resolve()],
        ):
            result = fn(path=str(link))
        assert result["success"] is False
        assert "allowed roots" in result["error"]
