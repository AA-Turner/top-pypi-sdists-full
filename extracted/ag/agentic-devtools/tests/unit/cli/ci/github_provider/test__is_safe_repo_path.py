"""Tests for the _is_safe_repo_path() helper."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.ci.github_provider import _is_safe_repo_path


class TestIsSafeRepoPath:
    """Tests for the guard applied to file paths taken from an untrusted PR body."""

    @pytest.mark.parametrize(
        "path",
        [
            "a.py",
            "src/module.py",
            "docs/my file.md",
            "a/b/c/d.txt",
            ".github/workflows/ci.yml",
            "src/C++/parser(test).cc",
            "docs/@notes[final].md",
            # ? and : are percent-encoded by urllib.parse.quote before use in API endpoints
            "docs/why?.md",
            "a?ref=x",
            "path:file.txt",
        ],
    )
    def test_accepts_plain_repository_relative_paths(self, path: str) -> None:
        assert _is_safe_repo_path(path) is True

    @pytest.mark.parametrize(
        "path",
        [
            "",
            "/absolute.py",
            "src/",
            "a//b",
            "../secret",
            "./secret",
            "src/./module.py",
            "src/../../etc/passwd",
            "-flag",
            "https://example.com/x",
            "a\nb",
        ],
    )
    def test_rejects_unsafe_paths(self, path: str) -> None:
        assert _is_safe_repo_path(path) is False
