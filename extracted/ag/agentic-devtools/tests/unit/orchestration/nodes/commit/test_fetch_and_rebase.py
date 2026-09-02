"""Tests for agentic_devtools.orchestration.nodes.commit._fetch_and_rebase."""

from unittest.mock import MagicMock, patch

from agentic_devtools.cli.git.core import GitError
from agentic_devtools.orchestration.nodes import commit as commit_mod

_MOD = "agentic_devtools.orchestration.nodes.commit"


def _proc(stdout: str = "", returncode: int = 0, stderr: str = ""):
    return MagicMock(returncode=returncode, stdout=stdout, stderr=stderr)


class TestFetchAndRebase:
    def test_skip_rebase_fetch_success(self):
        with patch(f"{_MOD}.run_git_safe", return_value=_proc()) as safe:
            fresh, blocked = commit_mod._fetch_and_rebase("/wt", skip_rebase=True)
        assert fresh is True and blocked is None
        safe.assert_called_once()

    def test_fetch_failure_no_issue_key_blocks_transient(self):
        """Fetch failure without an issue_key returns a transient BlockedState (fail closed)."""
        with (
            patch(f"{_MOD}.run_git_safe", side_effect=GitError(1, "net", ["fetch"])),
            patch(f"{_MOD}.run_git_capture", return_value=_proc(stdout="unrelated commit\n")) as cap,
        ):
            fresh, blocked = commit_mod._fetch_and_rebase("/wt", skip_rebase=True)
        assert fresh is False
        assert blocked is not None
        assert blocked.category == "transient"
        assert "stale refs" in blocked.message
        cap.assert_called_once_with(["log", "-1", "--format=%B"], cwd="/wt")

    def test_fetch_failure_head_not_issue_commit_blocks_transient(self):
        """Fetch failure when HEAD is not the issue commit returns a transient BlockedState."""
        with (
            patch(f"{_MOD}.run_git_safe", side_effect=GitError(1, "net", ["fetch"])),
            patch(f"{_MOD}.run_git_capture", return_value=_proc(stdout="unrelated commit\n")),
        ):
            fresh, blocked = commit_mod._fetch_and_rebase("/wt", skip_rebase=False, issue_key="42")
        assert fresh is False
        assert blocked is not None
        assert blocked.category == "transient"
        assert "stale refs" in blocked.message

    def test_fetch_failure_head_contains_bare_digit_blocks_transient(self):
        """Fetch failure: a commit message containing '42' as a bare number must NOT pass.

        The old substring test (``'42' in msg``) would incorrectly allow amend here.
        The new precise match requires the exact scope ``(#42)`` or footer ``#42``.
        """
        with (
            patch(f"{_MOD}.run_git_safe", side_effect=GitError(1, "net", ["fetch"])),
            patch(f"{_MOD}.run_git_capture", return_value=_proc(stdout="fix: bump version to v42.0\n")),
        ):
            fresh, blocked = commit_mod._fetch_and_rebase("/wt", skip_rebase=False, issue_key="42")
        assert fresh is False
        assert blocked is not None
        assert blocked.category == "transient"
        assert "stale refs" in blocked.message

    def test_fetch_failure_head_is_issue_commit_allows_stale_amend(self):
        """Fetch failure when HEAD already contains the issue key returns (False, None)."""
        with (
            patch(f"{_MOD}.run_git_safe", side_effect=GitError(1, "net", ["fetch"])),
            patch(f"{_MOD}.run_git_capture", return_value=_proc(stdout="feat(#42): implement\n\n#42\n")),
        ):
            fresh, blocked = commit_mod._fetch_and_rebase("/wt", skip_rebase=False, issue_key="42")
        assert fresh is False and blocked is None

    def test_fetch_failure_head_probe_failure_blocks_transient(self):
        """Fetch failure where the log probe also fails returns a transient BlockedState."""
        with (
            patch(f"{_MOD}.run_git_safe", side_effect=GitError(1, "net", ["fetch"])),
            patch(f"{_MOD}.run_git_capture", return_value=_proc(returncode=128, stdout="")),
        ):
            fresh, blocked = commit_mod._fetch_and_rebase("/wt", skip_rebase=False, issue_key="42")
        assert fresh is False
        assert blocked is not None
        assert blocked.category == "transient"

    def test_no_ref_to_rebase_is_noop(self):
        with (
            patch(f"{_MOD}.run_git_safe", return_value=_proc()),
            patch(f"{_MOD}.run_git_capture", return_value=_proc(returncode=1)),
        ):
            fresh, blocked = commit_mod._fetch_and_rebase("/wt", skip_rebase=False)
        assert fresh is True and blocked is None

    def test_clean_worktree_rebase_success_no_stash(self):
        capture_calls = []

        def capture(args, cwd=None):
            capture_calls.append(args)
            if args[:2] == ["rev-parse", "--verify"]:
                return _proc(returncode=0)
            if args[0] == "rebase":
                return _proc(returncode=0)
            return _proc()

        with (
            patch(f"{_MOD}.run_git_safe", return_value=_proc()) as safe,
            patch(f"{_MOD}._has_pending_changes", return_value=False),
            patch(f"{_MOD}.run_git_capture", side_effect=capture),
        ):
            fresh, blocked = commit_mod._fetch_and_rebase("/wt", skip_rebase=False)
        assert blocked is None
        assert safe.call_count == 1
        assert not any(a[0] == "stash" for a in capture_calls)

    def test_dirty_worktree_stash_and_pop_success(self):
        stash_sha = "aabbccdd11223344aabbccdd11223344aabbccdd"
        token = "agdt-rebase-stash:token-123"

        def capture(args, cwd=None):
            if args[:2] == ["rev-parse", "--verify"]:
                return _proc(returncode=0)
            if args[:2] == ["stash", "list"] and "%gs" in args[-1]:
                return _proc(stdout=f"{stash_sha}\x00On feature/42/x: {token}\n")
            if args[:2] == ["stash", "list"] and "%gd" in args[-1]:
                return _proc(stdout=f"{stash_sha}\x00stash@{{0}}\n")
            if args[0] == "rebase":
                return _proc(returncode=0)
            if args[:2] == ["stash", "apply"]:
                return _proc(returncode=0)
            if args == ["rev-parse", "stash@{0}"]:
                return _proc(stdout=stash_sha)
            if args[:2] == ["stash", "drop"]:
                return _proc(returncode=0)
            return _proc()

        with (
            patch(f"{_MOD}.run_git_safe", return_value=_proc()) as safe,
            patch(f"{_MOD}._has_pending_changes", return_value=True),
            patch(f"{_MOD}.uuid4", return_value=MagicMock(hex="token-123")),
            patch(f"{_MOD}.run_git_capture", side_effect=capture) as cap,
        ):
            fresh, blocked = commit_mod._fetch_and_rebase("/wt", skip_rebase=False)
        assert blocked is None
        assert any(c.args[0][:2] == ["stash", "push"] for c in safe.call_args_list)
        stash_push = next(c.args[0] for c in safe.call_args_list if c.args[0][:2] == ["stash", "push"])
        assert stash_push[-1] == token
        apply_calls = [c.args[0] for c in cap.call_args_list if c.args[0][:2] == ["stash", "apply"]]
        assert apply_calls and apply_calls[0] == ["stash", "apply", "--index", stash_sha]

    def test_stash_push_failure_blocks_transient(self):
        def safe(args, cwd=None):
            if args[:2] == ["stash", "push"]:
                raise GitError(1, "cannot stash", ["stash", "push"])
            return _proc()

        with (
            patch(f"{_MOD}.run_git_safe", side_effect=safe),
            patch(f"{_MOD}._has_pending_changes", return_value=True),
            patch(f"{_MOD}.run_git_capture", return_value=_proc(returncode=0)),
        ):
            fresh, blocked = commit_mod._fetch_and_rebase("/wt", skip_rebase=False)
        assert blocked.category == "transient"

    def test_rebase_conflict_aborts_and_restores(self):
        stash_sha = "deadbeef1122334455deadbeef1122334455dead"
        restored = []
        token = "agdt-rebase-stash:token-123"

        def capture(args, cwd=None):
            if args[:2] == ["rev-parse", "--verify"]:
                return _proc(returncode=0)
            if args[:2] == ["stash", "list"] and "%gs" in args[-1]:
                return _proc(stdout=f"{stash_sha}\x00On feature/42/x: {token}\n")
            if args[:2] == ["stash", "list"] and "%gd" in args[-1]:
                return _proc(stdout=f"{stash_sha}\x00stash@{{0}}\n")
            if args == ["rebase", "origin/main"]:
                return _proc(returncode=1)
            if args[:2] == ["diff", "--name-only"]:
                return _proc(stdout="conflict.py\n")
            if args == ["rebase", "--abort"]:
                return _proc(returncode=0)
            if args[:2] == ["stash", "apply"]:
                restored.append(args)
                return _proc(returncode=0)
            if args == ["rev-parse", "stash@{0}"]:
                return _proc(stdout=stash_sha)
            if args[:2] == ["stash", "drop"]:
                return _proc(returncode=0)
            return _proc()

        with (
            patch(f"{_MOD}.run_git_safe", return_value=_proc()),
            patch(f"{_MOD}._has_pending_changes", return_value=True),
            patch(f"{_MOD}.uuid4", return_value=MagicMock(hex="token-123")),
            patch(f"{_MOD}.run_git_capture", side_effect=capture),
        ):
            fresh, blocked = commit_mod._fetch_and_rebase("/wt", skip_rebase=False)
        assert blocked.category == "conflict"
        assert blocked.details == ["conflict.py"]
        assert restored
        assert restored[0][2] == "--index"
        assert restored[0][3] == stash_sha

    def test_rebase_conflict_clean_worktree_no_restore(self):
        def capture(args, cwd=None):
            if args[:2] == ["rev-parse", "--verify"]:
                return _proc(returncode=0)
            if args == ["rebase", "origin/main"]:
                return _proc(returncode=1)
            if args[:2] == ["diff", "--name-only"]:
                return _proc(stdout="")
            if args == ["rebase", "--abort"]:
                return _proc(returncode=0)
            return _proc()

        with (
            patch(f"{_MOD}.run_git_safe", return_value=_proc()),
            patch(f"{_MOD}._has_pending_changes", return_value=False),
            patch(f"{_MOD}.run_git_capture", side_effect=capture) as cap,
        ):
            fresh, blocked = commit_mod._fetch_and_rebase("/wt", skip_rebase=False)
        assert blocked.category == "conflict"
        assert not any(c.args[0][:2] == ["stash", "pop"] for c in cap.call_args_list)

    def test_rebase_abort_failure_blocks_corruption(self):
        stash_sha = "aaaa1111bbbb2222cccc3333dddd4444eeee5555"
        restored = []
        token = "agdt-rebase-stash:token-123"

        def capture(args, cwd=None):
            if args[:2] == ["rev-parse", "--verify"]:
                return _proc(returncode=0)
            if args[:2] == ["stash", "list"] and "%gs" in args[-1]:
                return _proc(stdout=f"{stash_sha}\x00On feature/42/x: {token}\n")
            if args == ["rebase", "origin/main"]:
                return _proc(returncode=1)
            if args[:2] == ["diff", "--name-only"]:
                return _proc(stdout="conflict.py\n")
            if args == ["rebase", "--abort"]:
                return _proc(returncode=1, stderr="abort failed: no active rebase")
            if args[:2] == ["stash", "apply"]:
                restored.append(args)
                return _proc(returncode=0)
            return _proc()

        with (
            patch(f"{_MOD}.run_git_safe", return_value=_proc()),
            patch(f"{_MOD}._has_pending_changes", return_value=True),
            patch(f"{_MOD}.uuid4", return_value=MagicMock(hex="token-123")),
            patch(f"{_MOD}.run_git_capture", side_effect=capture),
        ):
            fresh, blocked = commit_mod._fetch_and_rebase("/wt", skip_rebase=False)
        assert blocked.category == "corruption"
        assert "abort also failed" in blocked.message or "abort" in blocked.message.lower()
        assert not restored

    def test_rebase_abort_ok_but_restore_fails_blocks_transient(self):
        stash_sha = "bbbb2222cccc3333dddd4444eeee5555ffff6666"
        token = "agdt-rebase-stash:token-123"

        def capture(args, cwd=None):
            if args[:2] == ["rev-parse", "--verify"]:
                return _proc(returncode=0)
            if args[:2] == ["stash", "list"] and "%gs" in args[-1]:
                return _proc(stdout=f"{stash_sha}\x00On feature/42/x: {token}\n")
            if args == ["rebase", "origin/main"]:
                return _proc(returncode=1)
            if args[:2] == ["diff", "--name-only"]:
                return _proc(stdout="conflict.py\n")
            if args == ["rebase", "--abort"]:
                return _proc(returncode=0)
            if args[:2] == ["stash", "apply"]:
                return _proc(returncode=1, stderr="apply failed: conflict")
            return _proc()

        with (
            patch(f"{_MOD}.run_git_safe", return_value=_proc()),
            patch(f"{_MOD}._has_pending_changes", return_value=True),
            patch(f"{_MOD}.uuid4", return_value=MagicMock(hex="token-123")),
            patch(f"{_MOD}.run_git_capture", side_effect=capture),
        ):
            fresh, blocked = commit_mod._fetch_and_rebase("/wt", skip_rebase=False)
        assert blocked.category == "transient"
        assert "aborted successfully" in blocked.message or "restore" in blocked.message.lower()

    def test_stash_restore_failure_after_success_blocks_without_abort(self):
        stash_sha = "1234567890abcdef1234567890abcdef12345678"
        aborted = []
        token = "agdt-rebase-stash:token-123"

        def capture(args, cwd=None):
            if args[:2] == ["rev-parse", "--verify"]:
                return _proc(returncode=0)
            if args[:2] == ["stash", "list"] and "%gs" in args[-1]:
                return _proc(stdout=f"{stash_sha}\x00On feature/42/x: {token}\n")
            if args[0] == "rebase" and args == ["rebase", "--abort"]:
                aborted.append(args)
                return _proc(returncode=0)
            if args[0] == "rebase":
                return _proc(returncode=0)
            if args[:2] == ["stash", "apply"]:
                return _proc(returncode=1, stderr="apply conflict")
            return _proc()

        with (
            patch(f"{_MOD}.run_git_safe", return_value=_proc()),
            patch(f"{_MOD}._has_pending_changes", return_value=True),
            patch(f"{_MOD}.uuid4", return_value=MagicMock(hex="token-123")),
            patch(f"{_MOD}.run_git_capture", side_effect=capture),
        ):
            fresh, blocked = commit_mod._fetch_and_rebase("/wt", skip_rebase=False)
        assert blocked.category == "conflict"
        assert "restoring stashed changes failed" in blocked.message
        assert not aborted

    def test_unresolvable_stash_after_conflict_blocks_for_manual_recovery(self):
        def capture(args, cwd=None):
            if args[:2] == ["rev-parse", "--verify"]:
                return _proc(returncode=0)
            if args[:2] == ["stash", "list"] and "%gs" in args[-1]:
                return _proc(stdout="")
            if args == ["rebase", "origin/main"]:
                return _proc(returncode=1)
            if args[:2] == ["diff", "--name-only"]:
                return _proc(stdout="")
            if args == ["rebase", "--abort"]:
                return _proc(returncode=0)
            return _proc()

        with (
            patch(f"{_MOD}.run_git_safe", return_value=_proc()),
            patch(f"{_MOD}._has_pending_changes", return_value=True),
            patch(f"{_MOD}.uuid4", return_value=MagicMock(hex="token-123")),
            patch(f"{_MOD}.run_git_capture", side_effect=capture),
        ):
            fresh, blocked = commit_mod._fetch_and_rebase("/wt", skip_rebase=False)
        assert blocked is not None
        assert blocked.category == "transient"
        assert "stash identity could not be resolved" in blocked.message
        assert "Manual stash recovery" in blocked.message

    def test_unresolvable_stash_after_success_blocks_transient(self):
        def capture(args, cwd=None):
            if args[:2] == ["rev-parse", "--verify"]:
                return _proc(returncode=0)
            if args[:2] == ["stash", "list"] and "%gs" in args[-1]:
                return _proc(stdout="")
            if args[0] == "rebase":
                return _proc(returncode=0)
            return _proc()

        with (
            patch(f"{_MOD}.run_git_safe", return_value=_proc()),
            patch(f"{_MOD}._has_pending_changes", return_value=True),
            patch(f"{_MOD}.uuid4", return_value=MagicMock(hex="token-123")),
            patch(f"{_MOD}.run_git_capture", side_effect=capture),
        ):
            fresh, blocked = commit_mod._fetch_and_rebase("/wt", skip_rebase=False)
        assert blocked is not None
        assert blocked.category == "transient"
        assert "stash SHA could not be resolved" in blocked.message

    def test_drop_failure_after_conflict_restore_does_not_block(self):
        stash_sha = "cab005eecab005eecab005eecab005eecab005ee"
        token = "agdt-rebase-stash:token-123"

        def capture(args, cwd=None):
            if args[:2] == ["rev-parse", "--verify"]:
                return _proc(returncode=0)
            if args[:2] == ["stash", "list"] and "%gs" in args[-1]:
                return _proc(stdout=f"{stash_sha}\x00On feature/42/x: {token}\n")
            if args == ["rebase", "origin/main"]:
                return _proc(returncode=1)
            if args[:2] == ["diff", "--name-only"]:
                return _proc(stdout="conflict.py\n")
            if args == ["rebase", "--abort"]:
                return _proc(returncode=0)
            if args[:2] == ["stash", "apply"]:
                return _proc(returncode=0)
            return _proc()

        with (
            patch(f"{_MOD}.run_git_safe", return_value=_proc()),
            patch(f"{_MOD}._has_pending_changes", return_value=True),
            patch(f"{_MOD}.uuid4", return_value=MagicMock(hex="token-123")),
            patch(f"{_MOD}._drop_stash_by_commit", return_value=False),
            patch(f"{_MOD}.run_git_capture", side_effect=capture),
        ):
            fresh, blocked = commit_mod._fetch_and_rebase("/wt", skip_rebase=False)
        assert blocked is not None
        assert blocked.category == "conflict"

    def test_drop_failure_after_success_does_not_block(self):
        stash_sha = "cab005eecab005eecab005eecab005eecab005ee"
        token = "agdt-rebase-stash:token-123"

        def capture(args, cwd=None):
            if args[:2] == ["rev-parse", "--verify"]:
                return _proc(returncode=0)
            if args[:2] == ["stash", "list"] and "%gs" in args[-1]:
                return _proc(stdout=f"{stash_sha}\x00On feature/42/x: {token}\n")
            if args[0] == "rebase":
                return _proc(returncode=0)
            if args[:2] == ["stash", "apply"]:
                return _proc(returncode=0)
            return _proc()

        with (
            patch(f"{_MOD}.run_git_safe", return_value=_proc()),
            patch(f"{_MOD}._has_pending_changes", return_value=True),
            patch(f"{_MOD}.uuid4", return_value=MagicMock(hex="token-123")),
            patch(f"{_MOD}._drop_stash_by_commit", return_value=False),
            patch(f"{_MOD}.run_git_capture", side_effect=capture),
        ):
            fresh, blocked = commit_mod._fetch_and_rebase("/wt", skip_rebase=False)
        assert blocked is None
