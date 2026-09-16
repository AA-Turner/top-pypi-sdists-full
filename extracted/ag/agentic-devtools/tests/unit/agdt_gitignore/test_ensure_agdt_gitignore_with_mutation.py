"""Tests for agentic_devtools.agdt_gitignore.ensure_agdt_gitignore_with_mutation."""

from unittest.mock import patch

from agentic_devtools.agdt_gitignore import ensure_agdt_gitignore_with_mutation


class TestEnsureAgdtGitignoreWithMutation:
    """Tests for the mutation-aware ensure_agdt_gitignore function."""

    def test_returns_mutated_when_creating_file(self, tmp_path):
        """Returns success and mutation when creating the managed file."""
        assert ensure_agdt_gitignore_with_mutation(tmp_path) == (True, True)

    def test_returns_unmutated_for_canonical_file(self, tmp_path):
        """Returns success without mutation when the file is already canonical."""
        ensure_agdt_gitignore_with_mutation(tmp_path)

        assert ensure_agdt_gitignore_with_mutation(tmp_path) == (True, False)

    def test_returns_mutated_when_overwriting_file(self, tmp_path):
        """Returns success and mutation when replacing non-canonical content."""
        gitignore_path = tmp_path / ".agdt" / ".gitignore"
        gitignore_path.parent.mkdir()
        gitignore_path.write_text("stale content\n", encoding="utf-8")

        assert ensure_agdt_gitignore_with_mutation(tmp_path) == (True, True)

    def test_returns_false_without_git_root(self):
        """Returns failure without mutation when no git root is provided."""
        assert ensure_agdt_gitignore_with_mutation(None) == (False, False)

    def test_returns_false_on_write_error(self, tmp_path):
        """Returns failure without mutation when writing fails."""
        with patch("pathlib.Path.write_bytes", side_effect=OSError("permission denied")):
            assert ensure_agdt_gitignore_with_mutation(tmp_path) == (False, False)

    def test_returns_false_on_read_error(self, tmp_path):
        """Returns failure without mutation when reading fails."""
        ensure_agdt_gitignore_with_mutation(tmp_path)

        with patch("pathlib.Path.read_bytes", side_effect=PermissionError("permission denied")):
            assert ensure_agdt_gitignore_with_mutation(tmp_path) == (False, False)
