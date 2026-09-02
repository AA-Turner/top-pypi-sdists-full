"""Tests for agentic_devtools.skill_injector._ensure_github_gitignore_unignores_agdt."""

from pathlib import Path
from unittest.mock import patch

import pytest

from agentic_devtools.skill_injector import _ensure_github_gitignore_unignores_agdt


class TestEnsureGithubGitignoreUnignoresAgdt:
    """Tests for the helper that manages .github/.gitignore un-ignore rules."""

    def test_returns_without_raising_when_existing_gitignore_read_fails(self, tmp_path: Path):
        """Read errors should be ignored to keep injection best-effort."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir(parents=True)
        github_gitignore = github_dir / ".gitignore"
        original = "existing content\n"
        github_gitignore.write_text(original, encoding="utf-8")

        with patch("pathlib.Path.read_text", side_effect=OSError("cannot read")):
            with pytest.warns(RuntimeWarning, match="failed to read"):
                _ensure_github_gitignore_unignores_agdt(tmp_path)

        assert github_gitignore.read_text(encoding="utf-8") == original

    def test_returns_without_raising_when_gitignore_write_fails(self, tmp_path: Path):
        """Write errors should be ignored to keep injection best-effort."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir(parents=True)
        github_gitignore = github_dir / ".gitignore"

        with patch("pathlib.Path.write_text", side_effect=OSError("cannot write")):
            with pytest.warns(RuntimeWarning, match="failed to write"):
                _ensure_github_gitignore_unignores_agdt(tmp_path)

        assert not github_gitignore.exists()

    def test_skips_write_when_all_lines_already_present(self, tmp_path: Path):
        """No write occurs when all desired lines are already in the file."""
        github_dir = tmp_path / ".github"
        github_dir.mkdir(parents=True)
        github_gitignore = github_dir / ".gitignore"
        # Pre-populate with all desired lines
        desired_lines = [
            "# Managed by agentic-devtools: ensure injected skills under .github are tracked.",
            "!agents/.agdt/",
            "!agents/.agdt/**",
            "!prompts/.agdt/",
            "!prompts/.agdt/**",
        ]
        original_content = "\n".join(desired_lines) + "\n"
        github_gitignore.write_text(original_content, encoding="utf-8")

        with patch("pathlib.Path.write_text") as mock_write:
            _ensure_github_gitignore_unignores_agdt(tmp_path)

        mock_write.assert_not_called()
        # File content should remain unchanged
        assert github_gitignore.read_text(encoding="utf-8") == original_content
