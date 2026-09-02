"""Tests for agentic_devtools.orchestration.nodes.commit._retry_unpublished_push."""

from unittest.mock import MagicMock, patch

from agentic_devtools.models.git_results import BlockedState, CommitResult
from agentic_devtools.orchestration.nodes import commit as commit_mod

_MOD = "agentic_devtools.orchestration.nodes.commit"


def _proc(stdout: str = "", returncode: int = 0, stderr: str = ""):
    return MagicMock(returncode=returncode, stdout=stdout, stderr=stderr)


class TestRetryUnpublishedPush:
    def test_returns_none_when_previous_result_is_not_retryable(self):
        assert commit_mod._retry_unpublished_push(CommitResult(push_succeeded=True), "/wt") is None

    def test_returns_blocked_result_when_head_changes_and_remote_lacks_current_head(self):
        prior = CommitResult(
            commit_sha="deadbeef",
            push_succeeded=False,
            error=BlockedState(category="transient", message="net"),
        )

        def capture(args, cwd=None):
            if args == ["rev-parse", "--short", "HEAD"]:
                return _proc(stdout="otherhead")
            if args[:2] == ["rev-parse", "--abbrev-ref"]:
                return _proc(stdout="feature/42/x")
            if args == ["rev-parse", "HEAD"]:
                return _proc(stdout="otherheaddeadbeefdeadbeefdeadbeefdeadbeef")
            if args[:2] == ["ls-remote", "--heads"]:
                return _proc(stdout="")
            return _proc()

        with patch(f"{_MOD}.run_git_capture", side_effect=capture):
            result = commit_mod._retry_unpublished_push(prior, "/wt")

        assert result is not None
        assert result.error is not None
        assert result.error.category == "transient"
        assert "no longer matches HEAD" in result.error.message

    def test_returns_none_when_head_changes_but_remote_already_has_current_head(self):
        prior = CommitResult(
            commit_sha="deadbeef",
            push_succeeded=False,
            error=BlockedState(category="transient", message="net"),
        )
        head_full = "otherheaddeadbeefdeadbeefdeadbeefdeadbeef"

        def capture(args, cwd=None):
            if args == ["rev-parse", "--short", "HEAD"]:
                return _proc(stdout="otherhead")
            if args[:2] == ["rev-parse", "--abbrev-ref"]:
                return _proc(stdout="feature/42/x")
            if args == ["rev-parse", "HEAD"]:
                return _proc(stdout=head_full)
            if args[:2] == ["ls-remote", "--heads"]:
                return _proc(stdout=f"{head_full}\trefs/heads/feature/42/x\n")
            return _proc()

        with patch(f"{_MOD}.run_git_capture", side_effect=capture):
            assert commit_mod._retry_unpublished_push(prior, "/wt") is None

    def test_returns_none_when_remote_already_has_head(self):
        prior = {
            "commit_sha": "deadbeef",
            "push_succeeded": False,
            "no_op": False,
            "is_amend": False,
            "error": {"category": "transient"},
        }
        head_full = "deadbeefdeadbeefdeadbeefdeadbeefdeadbeef"

        def capture(args, cwd=None):
            if args == ["rev-parse", "--short", "HEAD"]:
                return _proc(stdout="deadbeef")
            if args[:2] == ["rev-parse", "--abbrev-ref"]:
                return _proc(stdout="feature/42/x")
            if args == ["rev-parse", "HEAD"]:
                return _proc(stdout=head_full)
            if args[:2] == ["ls-remote", "--heads"]:
                return _proc(stdout=f"{head_full}\trefs/heads/feature/42/x\n")
            return _proc()

        with patch(f"{_MOD}.run_git_capture", side_effect=capture):
            assert commit_mod._retry_unpublished_push(prior, "/wt") is None

    def test_returns_blocked_result_when_retry_push_fails(self):
        prior = CommitResult(
            commit_sha="deadbeef",
            commit_message_title="feat(#42): add workflow",
            is_amend=False,
            push_succeeded=False,
            error=BlockedState(category="transient", message="net"),
        )

        def capture(args, cwd=None):
            if args == ["rev-parse", "--short", "HEAD"]:
                return _proc(stdout="deadbeef")
            if args[:2] == ["rev-parse", "--abbrev-ref"]:
                return _proc(stdout="feature/42/x")
            if args == ["rev-parse", "HEAD"]:
                return _proc(stdout="deadbeefdeadbeefdeadbeefdeadbeefdeadbeef")
            if args[:2] == ["ls-remote", "--heads"]:
                return _proc(stdout="")
            return _proc()

        with (
            patch(f"{_MOD}.run_git_capture", side_effect=capture),
            patch(f"{_MOD}._push", return_value=BlockedState(category="auth", message="auth failed")),
        ):
            result = commit_mod._retry_unpublished_push(prior, "/wt")
        assert result is not None
        assert result.error.category == "auth"

    def test_returns_blocked_result_when_head_sha_probe_fails(self):
        prior = CommitResult(
            commit_sha="deadbeef",
            push_succeeded=False,
            error=BlockedState(category="transient", message="net"),
        )

        with patch(f"{_MOD}.run_git_capture", return_value=_proc(returncode=128, stdout="")):
            result = commit_mod._retry_unpublished_push(prior, "/wt")

        assert result is not None
        assert result.error is not None
        assert result.error.category == "transient"
        assert result.commit_sha == "deadbeef"

    def test_returns_blocked_result_when_head_sha_probe_returns_empty_stdout(self):
        prior = CommitResult(
            commit_sha="deadbeef",
            push_succeeded=False,
            error=BlockedState(category="transient", message="net"),
        )

        with patch(f"{_MOD}.run_git_capture", return_value=_proc(returncode=0, stdout="")):
            result = commit_mod._retry_unpublished_push(prior, "/wt")

        assert result is not None
        assert result.error is not None
        assert result.error.category == "transient"

    def test_returns_blocked_result_when_prior_error_has_no_sha(self):
        prior = CommitResult(
            commit_sha=None,
            push_succeeded=False,
            error=BlockedState(category="transient", message="commit failed before SHA recorded"),
        )
        result = commit_mod._retry_unpublished_push(prior, "/wt")
        assert result is not None
        assert result.error is not None
        assert result.error.category == "transient"
        assert "no recorded SHA" in result.error.message
