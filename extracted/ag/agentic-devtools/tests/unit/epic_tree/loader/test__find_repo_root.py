"""Tests for _find_repo_root helper function."""

from pathlib import Path

from agentic_devtools.epic_tree.loader import _find_repo_root


class TestFindRepoRoot:
    """Tests for _find_repo_root."""

    def test_finds_git_marker(self, tmp_path):
        """Returns the directory that contains a .git entry."""
        (tmp_path / ".git").mkdir()
        nested = tmp_path / "subdir" / "nested"
        nested.mkdir(parents=True)
        assert _find_repo_root(nested) == tmp_path

    def test_finds_agdt_config_marker(self, tmp_path):
        """Returns the directory that contains .github/agdt-config.json."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir()
        (github_dir / "agdt-config.json").write_text("{}", encoding="utf-8")
        nested = tmp_path / "subdir"
        nested.mkdir()
        assert _find_repo_root(nested) == tmp_path

    def test_start_is_file(self, tmp_path):
        """When start is a file its parent directory is used as the initial candidate."""
        (tmp_path / ".git").mkdir()
        f = tmp_path / "epic.json"
        f.write_text("{}", encoding="utf-8")
        assert _find_repo_root(f) == tmp_path

    def test_start_dir_is_repo_root(self, tmp_path):
        """Returns start immediately when it contains .git."""
        (tmp_path / ".git").mkdir()
        assert _find_repo_root(tmp_path) == tmp_path

    def test_returns_none_when_no_marker(self, tmp_path, monkeypatch):
        """Returns None when no .git or .github/agdt-config.json marker is found."""
        nested = tmp_path / "a" / "b" / "c"
        nested.mkdir(parents=True)
        # Patch Path.exists to always return False so the traversal never finds a
        # marker, regardless of how the CI filesystem is structured above tmp_path.
        monkeypatch.setattr(Path, "exists", lambda self: False)
        assert _find_repo_root(nested) is None

    def test_deeply_nested_reaches_ancestor(self, tmp_path):
        """Walks multiple levels of nesting to find the repo root."""
        (tmp_path / ".git").mkdir()
        deep = tmp_path / "a" / "b" / "c" / "d"
        deep.mkdir(parents=True)
        assert _find_repo_root(deep) == tmp_path

    def test_git_file_marker(self, tmp_path):
        """Treats a .git *file* (worktree case) as a valid repo root marker."""
        (tmp_path / ".git").write_text("gitdir: ../.git/worktrees/branch", encoding="utf-8")
        nested = tmp_path / "sub"
        nested.mkdir()
        assert _find_repo_root(nested) == tmp_path
