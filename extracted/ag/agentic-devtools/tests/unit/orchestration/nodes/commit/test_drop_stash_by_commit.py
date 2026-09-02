"""Tests for agentic_devtools.orchestration.nodes.commit._drop_stash_by_commit."""

from unittest.mock import MagicMock, patch

from agentic_devtools.orchestration.nodes import commit as commit_mod

_MOD = "agentic_devtools.orchestration.nodes.commit"


def _proc(stdout: str = "", returncode: int = 0, stderr: str = ""):
    return MagicMock(returncode=returncode, stdout=stdout, stderr=stderr)


class TestDropStashByCommit:
    def test_returns_false_when_sha_is_none(self):
        assert commit_mod._drop_stash_by_commit(None, "/wt") is False

    def test_drops_matching_ref_after_reverification(self):
        sha = "feedface" * 5

        def capture(args, cwd=None):
            if args[:2] == ["stash", "list"]:
                return _proc(stdout=f"{sha}\x00stash@{{0}}\n")
            if args == ["rev-parse", "stash@{0}"]:
                return _proc(stdout=sha)
            if args[:2] == ["stash", "drop"]:
                return _proc(returncode=0)
            return _proc()

        with patch(f"{_MOD}.run_git_capture", side_effect=capture):
            assert commit_mod._drop_stash_by_commit(sha, "/wt") is True

    def test_returns_false_when_reverification_changes(self):
        sha = "feedface" * 5

        def capture(args, cwd=None):
            if args[:2] == ["stash", "list"]:
                return _proc(stdout=f"{sha}\x00stash@{{0}}\n")
            if args == ["rev-parse", "stash@{0}"]:
                return _proc(stdout="different")
            return _proc()

        with patch(f"{_MOD}.run_git_capture", side_effect=capture):
            assert commit_mod._drop_stash_by_commit(sha, "/wt") is False

    def test_returns_false_when_stash_list_command_fails(self):
        with patch(f"{_MOD}.run_git_capture", return_value=_proc(returncode=1)):
            assert commit_mod._drop_stash_by_commit("feedface", "/wt") is False

    def test_skips_non_matching_entries_until_match(self):
        sha = "feedface" * 5

        def capture(args, cwd=None):
            if args[:2] == ["stash", "list"]:
                return _proc(stdout=f"other\x00stash@{{1}}\n{sha}\x00stash@{{0}}\n")
            if args == ["rev-parse", "stash@{0}"]:
                return _proc(stdout=sha)
            if args[:2] == ["stash", "drop"]:
                return _proc(returncode=0)
            return _proc()

        with patch(f"{_MOD}.run_git_capture", side_effect=capture):
            assert commit_mod._drop_stash_by_commit(sha, "/wt") is True

    def test_returns_false_when_sha_is_absent(self):
        with patch(f"{_MOD}.run_git_capture", return_value=_proc(stdout="other\x00stash@{0}\n")):
            assert commit_mod._drop_stash_by_commit("feedface", "/wt") is False
