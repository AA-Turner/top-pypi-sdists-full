"""Tests for agentic_devtools.orchestration.nodes.commit._find_stash_commit."""

from unittest.mock import MagicMock, patch

from agentic_devtools.orchestration.nodes import commit as commit_mod

_MOD = "agentic_devtools.orchestration.nodes.commit"


def _proc(stdout: str = "", returncode: int = 0, stderr: str = ""):
    return MagicMock(returncode=returncode, stdout=stdout, stderr=stderr)


class TestFindStashCommit:
    def test_returns_none_when_token_is_none(self):
        result = commit_mod._find_stash_commit(None, "/wt")
        assert result is None

    def test_returns_sha_for_matching_token(self):
        sha = "abc1234" * 5
        list_output = f"other\x00On main: something else\n{sha}\x00On feature/42/x: agdt-rebase-stash:token-123\n"
        with patch(f"{_MOD}.run_git_capture", return_value=_proc(stdout=list_output)):
            found_sha = commit_mod._find_stash_commit("agdt-rebase-stash:token-123", "/wt")
        assert found_sha == sha

    def test_returns_none_when_token_not_in_list(self):
        output = "abc\x00On feature/42/x: agdt-rebase-stash:other-token\n"
        with patch(f"{_MOD}.run_git_capture", return_value=_proc(stdout=output)):
            found_sha = commit_mod._find_stash_commit("agdt-rebase-stash:token-123", "/wt")
        assert found_sha is None

    def test_returns_none_when_stash_list_command_fails(self):
        with patch(f"{_MOD}.run_git_capture", return_value=_proc(returncode=1)):
            found_sha = commit_mod._find_stash_commit("agdt-rebase-stash:token-123", "/wt")
        assert found_sha is None
