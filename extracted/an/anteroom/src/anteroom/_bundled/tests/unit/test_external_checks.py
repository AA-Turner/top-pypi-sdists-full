"""Unit tests for external_checks module (#1306)."""

from __future__ import annotations

import json
import subprocess
from unittest.mock import patch

from anteroom.services.external_checks import (
    check_closing_prs,
    check_external_completion,
    check_issue_closed,
)


def _completed_process(stdout: str = "", returncode: int = 0) -> subprocess.CompletedProcess[str]:
    return subprocess.CompletedProcess(args=[], returncode=returncode, stdout=stdout, stderr="")


# ---------------------------------------------------------------------------
# check_issue_closed
# ---------------------------------------------------------------------------


class TestCheckIssueClosed:
    @patch("anteroom.services.external_checks.subprocess.run")
    def test_returns_true_for_closed_state(self, mock_run: object) -> None:
        mock_run.return_value = _completed_process("CLOSED\n")  # type: ignore[attr-defined]
        assert check_issue_closed(42) is True

    @patch("anteroom.services.external_checks.subprocess.run")
    def test_returns_false_for_open_state(self, mock_run: object) -> None:
        mock_run.return_value = _completed_process("OPEN\n")  # type: ignore[attr-defined]
        assert check_issue_closed(42) is False

    @patch("anteroom.services.external_checks.subprocess.run")
    def test_fails_closed_on_subprocess_error(self, mock_run: object) -> None:
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="gh", timeout=10)  # type: ignore[attr-defined]
        assert check_issue_closed(42) is False

    @patch("anteroom.services.external_checks.subprocess.run")
    def test_fails_closed_on_nonzero_exit(self, mock_run: object) -> None:
        mock_run.return_value = _completed_process("", returncode=1)  # type: ignore[attr-defined]
        assert check_issue_closed(42) is False

    @patch("anteroom.services.external_checks.subprocess.run")
    def test_passes_repo_flag(self, mock_run: object) -> None:
        mock_run.return_value = _completed_process("CLOSED\n")  # type: ignore[attr-defined]
        assert check_issue_closed(42, repo="owner/repo") is True
        args = mock_run.call_args[0][0]  # type: ignore[attr-defined]
        assert "--repo" in args
        assert "owner/repo" in args

    def test_rejects_invalid_repo_pattern(self) -> None:
        assert check_issue_closed(42, repo="--hostname evil.example.com") is False


# ---------------------------------------------------------------------------
# check_closing_prs
# ---------------------------------------------------------------------------


class TestCheckClosingPrs:
    @patch("anteroom.services.external_checks._resolve_repo")
    @patch("anteroom.services.external_checks.subprocess.run")
    def test_returns_merged_pr_numbers(self, mock_run: object, mock_resolve: object) -> None:
        mock_resolve.return_value = ("owner", "repo")  # type: ignore[attr-defined]
        graphql_response = {
            "data": {
                "repository": {
                    "issue": {
                        "closedByPullRequestsReferences": {
                            "nodes": [
                                {"number": 1305, "merged": True},
                                {"number": 1310, "merged": False},
                            ]
                        }
                    }
                }
            }
        }
        mock_run.return_value = _completed_process(json.dumps(graphql_response))  # type: ignore[attr-defined]
        assert check_closing_prs(1180) == [1305]

    @patch("anteroom.services.external_checks._resolve_repo")
    @patch("anteroom.services.external_checks.subprocess.run")
    def test_excludes_unmerged_prs(self, mock_run: object, mock_resolve: object) -> None:
        mock_resolve.return_value = ("owner", "repo")  # type: ignore[attr-defined]
        graphql_response = {
            "data": {
                "repository": {
                    "issue": {"closedByPullRequestsReferences": {"nodes": [{"number": 99, "merged": False}]}}
                }
            }
        }
        mock_run.return_value = _completed_process(json.dumps(graphql_response))  # type: ignore[attr-defined]
        assert check_closing_prs(42) == []

    @patch("anteroom.services.external_checks._resolve_repo")
    @patch("anteroom.services.external_checks.subprocess.run")
    def test_fails_closed_on_graphql_error(self, mock_run: object, mock_resolve: object) -> None:
        mock_resolve.return_value = ("owner", "repo")  # type: ignore[attr-defined]
        mock_run.return_value = _completed_process("", returncode=1)  # type: ignore[attr-defined]
        assert check_closing_prs(42) == []

    @patch("anteroom.services.external_checks._resolve_repo")
    def test_fails_closed_when_repo_unresolvable(self, mock_resolve: object) -> None:
        mock_resolve.return_value = None  # type: ignore[attr-defined]
        assert check_closing_prs(42) == []


# ---------------------------------------------------------------------------
# check_external_completion
# ---------------------------------------------------------------------------


class TestCheckExternalCompletion:
    @patch("anteroom.services.external_checks.check_closing_prs")
    @patch("anteroom.services.external_checks.check_issue_closed")
    def test_returns_reason_with_pr_numbers(self, mock_closed: object, mock_prs: object) -> None:
        mock_closed.return_value = True  # type: ignore[attr-defined]
        mock_prs.return_value = [1305]  # type: ignore[attr-defined]
        ok, reason = check_external_completion(1180)
        assert ok is True
        assert reason == "Issue #1180 closed; merged closing PR(s): #1305"

    @patch("anteroom.services.external_checks.check_closing_prs")
    @patch("anteroom.services.external_checks.check_issue_closed")
    def test_returns_degraded_reason_when_no_prs(self, mock_closed: object, mock_prs: object) -> None:
        mock_closed.return_value = True  # type: ignore[attr-defined]
        mock_prs.return_value = []  # type: ignore[attr-defined]
        ok, reason = check_external_completion(42)
        assert ok is True
        assert reason == "Issue #42 closed externally"

    @patch("anteroom.services.external_checks.check_issue_closed")
    def test_returns_false_when_issue_open(self, mock_closed: object) -> None:
        mock_closed.return_value = False  # type: ignore[attr-defined]
        ok, reason = check_external_completion(42)
        assert ok is False
        assert reason is None

    @patch("anteroom.services.external_checks.check_issue_closed")
    def test_fails_closed_on_issue_check_error(self, mock_closed: object) -> None:
        mock_closed.return_value = False  # type: ignore[attr-defined]
        ok, reason = check_external_completion(42)
        assert ok is False
        assert reason is None
