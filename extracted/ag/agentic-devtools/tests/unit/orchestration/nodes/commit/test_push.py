"""Tests for agentic_devtools.orchestration.nodes.commit._push."""

from unittest.mock import MagicMock, patch

from agentic_devtools.orchestration.nodes import commit as commit_mod

_MOD = "agentic_devtools.orchestration.nodes.commit"


def _proc(stdout: str = "", returncode: int = 0, stderr: str = ""):
    return MagicMock(returncode=returncode, stdout=stdout, stderr=stderr)


class TestPush:
    def test_amend_force_pushes(self):
        def capture(args, cwd=None):
            if args[:2] == ["rev-parse", "--abbrev-ref"]:
                return _proc(stdout="feature/42/x")
            return _proc(returncode=0)

        with patch(f"{_MOD}.run_git_capture", side_effect=capture) as cap:
            assert commit_mod._push("/wt", is_amend=True) is None
        push_args = [c.args[0] for c in cap.call_args_list if c.args[0][0] == "push"][0]
        assert "--force-with-lease" in push_args

    def test_new_publish_sets_upstream(self):
        def capture(args, cwd=None):
            if args[:2] == ["rev-parse", "--abbrev-ref"]:
                return _proc(stdout="feature/42/x")
            return _proc(returncode=0)

        with patch(f"{_MOD}.run_git_capture", side_effect=capture) as cap:
            assert commit_mod._push("/wt", is_amend=False) is None
        push_args = [c.args[0] for c in cap.call_args_list if c.args[0][0] == "push"][0]
        assert "--set-upstream" in push_args

    def test_push_rejection_returns_block(self):
        def capture(args, cwd=None):
            if args[:2] == ["rev-parse", "--abbrev-ref"]:
                return _proc(stdout="feature/42/x")
            return _proc(returncode=1, stderr="Protected branch")

        with patch(f"{_MOD}.run_git_capture", side_effect=capture):
            blocked = commit_mod._push("/wt", is_amend=False)
        assert blocked.category == "protection"
