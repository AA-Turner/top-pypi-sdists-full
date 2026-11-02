"""Tests for approve_pr core function."""

from unittest.mock import patch

import pytest

from agentic_devtools.cli.github import pr_approve


def test_uses_explicit_environment_for_all_gh_commands() -> None:
    import subprocess

    env = {"GH_TOKEN": "approver-token", "PATH": "/usr/bin"}
    expected_head = "a" * 40
    results = [
        subprocess.CompletedProcess([], 0, "alice\n", ""),
        subprocess.CompletedProcess([], 0, f"{expected_head}\n", ""),
        subprocess.CompletedProcess([], 0, "", ""),
        subprocess.CompletedProcess([], 0, "", ""),
        subprocess.CompletedProcess(
            [],
            0,
            (
                '{"id": 9, "state": "APPROVED", "submitted_at": "2026-04-07T09:00:00Z", '
                f'"user": {{"login": "alice"}}, "commit_id": "{expected_head}"}}\n'
            ),
            "",
        ),
        subprocess.CompletedProcess([], 0, f"{expected_head}\n", ""),
    ]

    def fake_run_safe(*args: object, **kwargs: object) -> subprocess.CompletedProcess:
        assert kwargs.get("env") is env
        return results.pop(0)

    with (
        patch.object(pr_approve, "_check_gh_available"),
        patch.object(pr_approve, "run_safe", side_effect=fake_run_safe) as mock_run_safe,
        patch.object(pr_approve, "set_value"),
    ):
        result = pr_approve.approve_pr(42, "owner/repo", expected_head=expected_head, env=env)

    assert result["approved"] is True
    assert mock_run_safe.call_count == 6
    assert results == []


class TestApprovePr:
    """Tests for approve_pr."""

    def test_full_success_flow(self):
        """Full success: approval submitted and verified."""
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(pr_approve, "_submit_approval", return_value=(True, "")),
            patch.object(
                pr_approve,
                "_verify_approval",
                return_value=({"id": 999, "submitted_at": "2026-04-07T09:00:00Z"}, 0, True),
            ),
            patch.object(pr_approve, "set_value") as mock_set,
        ):
            result = pr_approve.approve_pr(42, "owner/repo")

        assert result["prNumber"] == 42
        assert result["repo"] == "owner/repo"
        assert result["approved"] is True
        assert result["reviewId"] == 999
        assert result["approver"] == "alice"
        assert result["submittedAt"] == "2026-04-07T09:00:00Z"
        assert result["verified"] is True
        assert result["retries"] == 0
        assert mock_set.called

    def test_full_success_flow_with_retries(self):
        """Success after retries: retries field reflects actual attempts."""
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(pr_approve, "_submit_approval", return_value=(True, "")),
            patch.object(
                pr_approve,
                "_verify_approval",
                return_value=({"id": 999, "submitted_at": "2026-04-07T09:00:00Z"}, 1, True),
            ),
            patch.object(pr_approve, "set_value"),
        ):
            result = pr_approve.approve_pr(42, "owner/repo")

        assert result["verified"] is True
        assert result["retries"] == 1

    def test_approval_submission_failure(self):
        """Approval submission fails: returns approved=False."""
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(
                pr_approve,
                "_submit_approval",
                return_value=(False, "draft state"),
            ),
            patch.object(pr_approve, "set_value") as mock_set,
        ):
            result = pr_approve.approve_pr(42, "owner/repo")

        assert result["approved"] is False
        assert result["error"] == "approval_failed"
        assert result["message"] == "draft state"
        assert result["verified"] is False
        assert mock_set.called

    def test_persist_state_false_suppresses_state_writes_on_submission_failure(self):
        """persist_state=False suppresses set_value calls on a submission failure."""
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(
                pr_approve,
                "_submit_approval",
                return_value=(False, "draft state"),
            ),
            patch.object(pr_approve, "set_value") as mock_set,
        ):
            result = pr_approve.approve_pr(42, "owner/repo", persist_state=False)

        assert result["approved"] is False
        mock_set.assert_not_called()

    def test_verification_exhausted(self):
        """Approval submitted but verification fails."""
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(pr_approve, "_submit_approval", return_value=(True, "")),
            patch.object(pr_approve, "_verify_approval", return_value=(None, 2, True)),
            patch.object(pr_approve, "set_value") as mock_set,
        ):
            result = pr_approve.approve_pr(42, "owner/repo")

        assert result["approved"] is True
        assert result["verified"] is False
        assert result["reviewId"] is None
        assert result["retries"] == 2
        assert mock_set.called

    def test_state_keys_written_on_success(self):
        """State keys written correctly on successful approval."""
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(pr_approve, "_submit_approval", return_value=(True, "")),
            patch.object(
                pr_approve,
                "_verify_approval",
                return_value=({"id": 555, "submitted_at": "2026-01-01T00:00:00Z"}, 0, True),
            ),
            patch.object(pr_approve, "set_value") as mock_set,
        ):
            pr_approve.approve_pr(42, "owner/repo")

        calls = [call.args for call in mock_set.call_args_list]
        assert ("github.pr_approval_verified", True) in calls
        assert ("github.pr_approval_review_id", 555) in calls

    def test_state_keys_written_on_failure(self):
        """State keys written correctly on failed submission."""
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(
                pr_approve,
                "_submit_approval",
                return_value=(False, "error"),
            ),
            patch.object(pr_approve, "set_value") as mock_set,
        ):
            pr_approve.approve_pr(42, "owner/repo")

        calls = [call.args for call in mock_set.call_args_list]
        assert ("github.pr_approval_verified", False) in calls
        assert ("github.pr_approval_review_id", None) in calls

    def test_default_body_used(self):
        """Default body used when body is None."""
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(pr_approve, "_submit_approval", return_value=(True, "")) as mock_submit,
            patch.object(
                pr_approve,
                "_verify_approval",
                return_value=({"id": 1, "submitted_at": "2026-01-01T00:00:00Z"}, 0, True),
            ),
            patch.object(pr_approve, "set_value"),
        ):
            pr_approve.approve_pr(42, "owner/repo", body=None)

        assert mock_submit.call_args[0][2] == "Approved via agdt-gh-pr-approve"

    def test_custom_body_passed_through(self):
        """Custom body is passed through to _submit_approval."""
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(pr_approve, "_submit_approval", return_value=(True, "")) as mock_submit,
            patch.object(
                pr_approve,
                "_verify_approval",
                return_value=({"id": 1, "submitted_at": "2026-01-01T00:00:00Z"}, 0, True),
            ),
            patch.object(pr_approve, "set_value"),
        ):
            pr_approve.approve_pr(42, "owner/repo", body="Custom message")

        assert mock_submit.call_args[0][2] == "Custom message"

    def test_expected_head_is_forwarded_to_submit_and_verify(self):
        """A valid expected_head is propagated through approval submission and verification."""
        expected_head = "a" * 40
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(pr_approve, "_fetch_current_head_sha", return_value=(expected_head, "")),
            patch.object(pr_approve, "_find_existing_approval", return_value=(None, True)) as mock_find_existing,
            patch.object(pr_approve, "_submit_approval", return_value=(True, "")) as mock_submit,
            patch.object(
                pr_approve,
                "_verify_approval",
                return_value=({"id": 1, "submitted_at": "2026-01-01T00:00:00Z"}, 0, True),
            ) as mock_verify,
            patch.object(pr_approve, "set_value"),
        ):
            pr_approve.approve_pr(42, "owner/repo", expected_head=expected_head)

        assert mock_find_existing.call_args.args == (42, "owner/repo", "alice", expected_head)
        assert mock_submit.call_args.args == (42, "owner/repo", pr_approve._DEFAULT_APPROVAL_BODY, expected_head)
        assert mock_verify.call_args.args == (42, "owner/repo", "alice")
        assert mock_verify.call_args.kwargs["expected_head"] == expected_head

    def test_existing_expected_head_approval_is_reused(self):
        """An existing approval on the same head is returned without submitting again."""
        expected_head = "a" * 40
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(pr_approve, "_fetch_current_head_sha", return_value=(expected_head, "")),
            patch.object(
                pr_approve,
                "_find_existing_approval",
                return_value=({"id": 77, "submitted_at": "2026-04-07T09:00:00Z"}, True),
            ),
            patch.object(pr_approve, "_submit_approval") as mock_submit,
            patch.object(pr_approve, "set_value") as mock_set,
        ):
            result = pr_approve.approve_pr(42, "owner/repo", expected_head=expected_head)

        assert result["approved"] is True
        assert result["status"] == "already_approved"
        assert result["reviewId"] == 77
        assert result["verified"] is True
        mock_submit.assert_not_called()
        mock_set.assert_any_call("github.pr_approval_verified", True)
        mock_set.assert_any_call("github.pr_approval_review_id", 77)

    def test_existing_expected_head_approval_skips_state_writes_when_disabled(self):
        """persist_state=False suppresses writes when an existing approval is reused."""
        expected_head = "a" * 40
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(pr_approve, "_fetch_current_head_sha", return_value=(expected_head, "")),
            patch.object(
                pr_approve,
                "_find_existing_approval",
                return_value=({"id": 77, "submitted_at": "2026-04-07T09:00:00Z"}, True),
            ),
            patch.object(pr_approve, "_submit_approval") as mock_submit,
            patch.object(pr_approve, "set_value") as mock_set,
        ):
            result = pr_approve.approve_pr(42, "owner/repo", expected_head=expected_head, persist_state=False)

        assert result["status"] == "already_approved"
        mock_submit.assert_not_called()
        mock_set.assert_not_called()

    def test_lookup_failed_refuses_submission_to_avoid_duplicate(self):
        """A failed preflight lookup refuses to submit rather than risk a duplicate approval."""
        expected_head = "a" * 40
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(pr_approve, "_fetch_current_head_sha", return_value=(expected_head, "")),
            patch.object(pr_approve, "_find_existing_approval", return_value=(None, False)),
            patch.object(pr_approve, "_submit_approval") as mock_submit,
            patch.object(pr_approve, "set_value") as mock_set,
        ):
            result = pr_approve.approve_pr(42, "owner/repo", expected_head=expected_head)

        assert result["approved"] is False
        assert result["error"] == "lookup_failed"
        assert expected_head in result["message"]
        assert result["verified"] is False
        mock_submit.assert_not_called()
        mock_set.assert_any_call("github.pr_approval_verified", False)
        mock_set.assert_any_call("github.pr_approval_review_id", None)

    def test_lookup_failed_does_not_persist_state_when_disabled(self):
        """persist_state=False suppresses set_value calls on a lookup failure."""
        expected_head = "a" * 40
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(pr_approve, "_fetch_current_head_sha", return_value=(expected_head, "")),
            patch.object(pr_approve, "_find_existing_approval", return_value=(None, False)),
            patch.object(pr_approve, "_submit_approval") as mock_submit,
            patch.object(pr_approve, "set_value") as mock_set,
        ):
            result = pr_approve.approve_pr(42, "owner/repo", expected_head=expected_head, persist_state=False)

        assert result["error"] == "lookup_failed"
        mock_submit.assert_not_called()
        mock_set.assert_not_called()

    def test_stale_head_detected_after_existing_approval_reuse(self):
        """The PR head moving between the preflight check and the reuse decision refuses success."""
        expected_head = "a" * 40
        moved_head = "b" * 40
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(
                pr_approve,
                "_fetch_current_head_sha",
                side_effect=[(expected_head, ""), (moved_head, "")],
            ),
            patch.object(
                pr_approve,
                "_find_existing_approval",
                return_value=({"id": 77, "submitted_at": "2026-04-07T09:00:00Z"}, True),
            ),
            patch.object(pr_approve, "_submit_approval") as mock_submit,
            patch.object(pr_approve, "set_value") as mock_set,
        ):
            result = pr_approve.approve_pr(42, "owner/repo", expected_head=expected_head)

        assert result["approved"] is False
        assert result["error"] == "stale_head"
        assert result["reviewId"] == 77
        assert result["verified"] is False
        mock_submit.assert_not_called()
        mock_set.assert_any_call("github.pr_approval_verified", False)
        mock_set.assert_any_call("github.pr_approval_review_id", None)

    def test_stale_head_reuse_recheck_failure_reports_unknown_head(self):
        """A recheck fetch failure after reusing an approval reports the failure detail."""
        expected_head = "a" * 40
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(
                pr_approve,
                "_fetch_current_head_sha",
                side_effect=[(expected_head, ""), (None, "network error")],
            ),
            patch.object(
                pr_approve,
                "_find_existing_approval",
                return_value=({"id": 77, "submitted_at": "2026-04-07T09:00:00Z"}, True),
            ),
            patch.object(pr_approve, "_submit_approval") as mock_submit,
            patch.object(pr_approve, "set_value"),
        ):
            result = pr_approve.approve_pr(42, "owner/repo", expected_head=expected_head)

        assert result["error"] == "stale_head"
        assert "network error" in result["message"]
        mock_submit.assert_not_called()

    def test_stale_head_after_reuse_does_not_persist_state_when_disabled(self):
        """persist_state=False suppresses set_value calls when a reused approval's head goes stale."""
        expected_head = "a" * 40
        moved_head = "b" * 40
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(
                pr_approve,
                "_fetch_current_head_sha",
                side_effect=[(expected_head, ""), (moved_head, "")],
            ),
            patch.object(
                pr_approve,
                "_find_existing_approval",
                return_value=({"id": 77, "submitted_at": "2026-04-07T09:00:00Z"}, True),
            ),
            patch.object(pr_approve, "_submit_approval") as mock_submit,
            patch.object(pr_approve, "set_value") as mock_set,
        ):
            result = pr_approve.approve_pr(42, "owner/repo", expected_head=expected_head, persist_state=False)

        assert result["error"] == "stale_head"
        mock_submit.assert_not_called()
        mock_set.assert_not_called()

    def test_stale_head_detected_after_fresh_submission(self):
        """The PR head moving between submission and the final result refuses success."""
        expected_head = "a" * 40
        moved_head = "b" * 40
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(
                pr_approve,
                "_fetch_current_head_sha",
                side_effect=[(expected_head, ""), (moved_head, "")],
            ),
            patch.object(pr_approve, "_find_existing_approval", return_value=(None, True)),
            patch.object(pr_approve, "_submit_approval", return_value=(True, "")),
            patch.object(
                pr_approve,
                "_verify_approval",
                return_value=({"id": 900, "submitted_at": "2026-04-07T09:00:00Z"}, 0, True),
            ),
            patch.object(pr_approve, "set_value") as mock_set,
        ):
            result = pr_approve.approve_pr(42, "owner/repo", expected_head=expected_head)

        assert result["approved"] is False
        assert result["error"] == "stale_head"
        assert result["reviewId"] == 900
        assert result["verified"] is False
        mock_set.assert_any_call("github.pr_approval_verified", False)
        mock_set.assert_any_call("github.pr_approval_review_id", None)

    def test_stale_head_after_submission_does_not_persist_state_when_disabled(self):
        """persist_state=False suppresses set_value calls when a freshly submitted approval goes stale."""
        expected_head = "a" * 40
        moved_head = "b" * 40
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(
                pr_approve,
                "_fetch_current_head_sha",
                side_effect=[(expected_head, ""), (moved_head, "")],
            ),
            patch.object(pr_approve, "_find_existing_approval", return_value=(None, True)),
            patch.object(pr_approve, "_submit_approval", return_value=(True, "")),
            patch.object(
                pr_approve,
                "_verify_approval",
                return_value=({"id": 900, "submitted_at": "2026-04-07T09:00:00Z"}, 0, True),
            ),
            patch.object(pr_approve, "set_value") as mock_set,
        ):
            result = pr_approve.approve_pr(42, "owner/repo", expected_head=expected_head, persist_state=False)

        assert result["error"] == "stale_head"
        mock_set.assert_not_called()

    def test_expected_head_invalid_raises_value_error(self):
        """Invalid expected_head values are rejected before approval submission."""
        with patch.object(pr_approve, "_check_gh_available"):
            with patch.object(pr_approve, "_resolve_current_user", return_value="alice"):
                with pytest.raises(ValueError, match="40 lowercase hexadecimal characters"):
                    pr_approve.approve_pr(42, "owner/repo", expected_head="abc123")

    def test_stale_head_refuses_approval_without_submitting(self):
        """A mismatched current head refuses to approve and never calls _submit_approval."""
        expected_head = "a" * 40
        current_head = "b" * 40
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(pr_approve, "_fetch_current_head_sha", return_value=(current_head, "")),
            patch.object(pr_approve, "_submit_approval") as mock_submit,
            patch.object(pr_approve, "set_value") as mock_set,
        ):
            result = pr_approve.approve_pr(42, "owner/repo", expected_head=expected_head)

        assert result["approved"] is False
        assert result["error"] == "stale_head"
        assert current_head in result["message"]
        assert expected_head in result["message"]
        assert result["verified"] is False
        mock_submit.assert_not_called()
        mock_set.assert_any_call("github.pr_approval_verified", False)
        mock_set.assert_any_call("github.pr_approval_review_id", None)

    def test_head_check_failure_refuses_approval_without_submitting(self):
        """When the current head cannot be resolved, approval is refused rather than assumed safe."""
        expected_head = "a" * 40
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(pr_approve, "_fetch_current_head_sha", return_value=(None, "network error")),
            patch.object(pr_approve, "_submit_approval") as mock_submit,
            patch.object(pr_approve, "set_value") as mock_set,
        ):
            result = pr_approve.approve_pr(42, "owner/repo", expected_head=expected_head)

        assert result["approved"] is False
        assert result["error"] == "head_check_failed"
        assert "network error" in result["message"]
        assert result["verified"] is False
        mock_submit.assert_not_called()
        mock_set.assert_any_call("github.pr_approval_verified", False)
        mock_set.assert_any_call("github.pr_approval_review_id", None)

    def test_head_check_failure_does_not_persist_state_when_disabled(self):
        """persist_state=False suppresses set_value calls even when the head check itself fails."""
        expected_head = "a" * 40
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(pr_approve, "_fetch_current_head_sha", return_value=(None, "network error")),
            patch.object(pr_approve, "_submit_approval") as mock_submit,
            patch.object(pr_approve, "set_value") as mock_set,
        ):
            result = pr_approve.approve_pr(42, "owner/repo", expected_head=expected_head, persist_state=False)

        assert result["error"] == "head_check_failed"
        mock_submit.assert_not_called()
        mock_set.assert_not_called()

    def test_stale_head_does_not_persist_state_when_disabled(self):
        """persist_state=False suppresses set_value calls even on a stale-head refusal."""
        expected_head = "a" * 40
        current_head = "b" * 40
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(pr_approve, "_fetch_current_head_sha", return_value=(current_head, "")),
            patch.object(pr_approve, "_submit_approval") as mock_submit,
            patch.object(pr_approve, "set_value") as mock_set,
        ):
            result = pr_approve.approve_pr(42, "owner/repo", expected_head=expected_head, persist_state=False)

        assert result["error"] == "stale_head"
        mock_submit.assert_not_called()
        mock_set.assert_not_called()

    def test_persist_state_false_suppresses_state_writes_on_success(self):
        """persist_state=False suppresses set_value calls on a successful approval."""
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(pr_approve, "_submit_approval", return_value=(True, "")),
            patch.object(
                pr_approve,
                "_verify_approval",
                return_value=({"id": 999, "submitted_at": "2026-04-07T09:00:00Z"}, 0, True),
            ),
            patch.object(pr_approve, "set_value") as mock_set,
        ):
            result = pr_approve.approve_pr(42, "owner/repo", persist_state=False)

        assert result["approved"] is True
        mock_set.assert_not_called()

    def test_empty_string_body_preserved(self):
        """Empty string body is preserved, not replaced with default."""
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(pr_approve, "_submit_approval", return_value=(True, "")) as mock_submit,
            patch.object(
                pr_approve,
                "_verify_approval",
                return_value=({"id": 1, "submitted_at": "2026-01-01T00:00:00Z"}, 0, True),
            ),
            patch.object(pr_approve, "set_value"),
        ):
            pr_approve.approve_pr(42, "owner/repo", body="")

        assert mock_submit.call_args[0][2] == ""

    def test_repo_normalized_before_downstream_calls(self):
        """Repo is normalized (stripped, .git removed) before _submit_approval and _verify_approval."""
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(pr_approve, "_submit_approval", return_value=(True, "")) as mock_submit,
            patch.object(
                pr_approve,
                "_verify_approval",
                return_value=({"id": 1, "submitted_at": "2026-01-01T00:00:00Z"}, 0, True),
            ) as mock_verify,
            patch.object(pr_approve, "set_value"),
        ):
            pr_approve.approve_pr(42, "  owner/repo.git  ")

        # Both downstream calls receive the normalized repo
        assert mock_submit.call_args[0][1] == "owner/repo"
        assert mock_verify.call_args[0][1] == "owner/repo"

    def test_repo_in_result_uses_normalized_value(self):
        """Result dict contains the normalized repo, not the raw input."""
        with (
            patch.object(pr_approve, "_check_gh_available"),
            patch.object(pr_approve, "_resolve_current_user", return_value="alice"),
            patch.object(pr_approve, "_submit_approval", return_value=(True, "")),
            patch.object(
                pr_approve,
                "_verify_approval",
                return_value=({"id": 1, "submitted_at": "2026-01-01T00:00:00Z"}, 0, True),
            ),
            patch.object(pr_approve, "set_value"),
        ):
            result = pr_approve.approve_pr(42, "  owner/repo.git  ")

        assert result["repo"] == "owner/repo"
