"""Tests for _read_repo_file()."""

import pytest

from agentic_devtools.cli.ci.github_provider import _read_repo_file


class TestReadRepoFile:
    """Tests for reading repo-root-relative files with graceful degradation."""

    def test_reads_file_from_github_workspace(self, tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
        (tmp_path / ".github").mkdir()
        (tmp_path / ".github" / "agent.md").write_text("agent content", encoding="utf-8")
        monkeypatch.setenv("GITHUB_WORKSPACE", str(tmp_path))
        assert _read_repo_file(".github/agent.md") == "agent content"

    def test_missing_file_returns_empty(self, tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GITHUB_WORKSPACE", str(tmp_path))
        assert _read_repo_file(".github/missing.md") == ""

    def test_falls_back_to_cwd_when_workspace_unset(self, tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.delenv("GITHUB_WORKSPACE", raising=False)
        monkeypatch.chdir(tmp_path)
        (tmp_path / "file.md").write_text("from cwd", encoding="utf-8")
        assert _read_repo_file("file.md") == "from cwd"

    def test_truncates_oversize_file(self, tmp_path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.setenv("GITHUB_WORKSPACE", str(tmp_path))
        (tmp_path / "big.md").write_text("A" * 100, encoding="utf-8")
        result = _read_repo_file("big.md", max_bytes=10)
        assert result.startswith("A" * 10)
        assert result.endswith("[… file truncated …]")
        assert len(result) < 100
