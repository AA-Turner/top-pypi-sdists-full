"""Tests for get_pr_checks_status orchestration function."""

import json
import subprocess
from unittest.mock import patch

import pytest

from agentic_devtools.cli.github.pr_checks_status import get_pr_checks_status

_REPO = "swai-factory/agentic-devtools"
_HEAD = "c4870fc0018a5bbb80da69505126e864c3567d32"
_REQUIRED = [
    ("Workflow Tests ✅", 122380957400),
    ("Smart Module Tests ✅", 122384266756),
    ("Targeted Checks ✅", 122378220001),
]


def _run(run_id, name, conclusion="success"):
    return {
        "id": run_id,
        "name": name,
        "app": {"id": 15368},
        "head_sha": _HEAD,
        "status": "completed",
        "conclusion": conclusion,
    }


class TestGetPrChecksStatus:
    """Tests for native current-head status resolution."""

    def test_required_runs_pass_without_check_suite_requests(self):
        runs = [_run(i, f"optional-{i}", "skipped") for i in range(1, 40)]
        runs.extend(_run(run_id, name) for name, run_id in _REQUIRED)
        evidence = {
            "complete": True,
            "ready": True,
            "checkRuns": runs,
            "requiredChecks": [{"name": name, "app": {"id": 15368}, "id": run_id} for name, run_id in _REQUIRED],
            "diagnostics": [],
        }
        checks = [{"name": f"check-{i}", "bucket": "pass" if i < 20 else "skipping"} for i in range(42)]
        with (
            patch(
                "agentic_devtools.cli.github.pr_checks_status.run_safe",
                return_value=subprocess.CompletedProcess([], 0, json.dumps(checks), ""),
            ) as fetch_checks,
            patch(
                "agentic_devtools.cli.github.pr_checks_status._resolve_required_checks",
                return_value=evidence,
            ) as resolve_required_checks,
            patch("agentic_devtools.cli.github.pr_checks_status.set_value"),
        ):
            result = get_pr_checks_status(4705, _REPO, _HEAD, "main")

        assert result["status"] == "all-pass"
        assert result["requiredChecksDiagnostics"] == []
        resolve_required_checks.assert_called_once_with(_REPO, "main", _HEAD)
        assert result["totalChecks"] == 42
        assert result["passed"] == 20
        assert result["skipped"] == 22
        fetch_checks.assert_called_once()

    def test_non_required_failure_is_blocking_and_visible(self):
        evidence = {
            "complete": True,
            "ready": False,
            "checkRuns": [_run(1, "optional", "failure")],
            "diagnostics": ["Blocking check 'optional'"],
        }
        with (
            patch(
                "agentic_devtools.cli.github.pr_checks_status._fetch_pr_checks",
                return_value=[{"name": "build", "bucket": "pass"}],
            ),
            patch(
                "agentic_devtools.cli.github.pr_checks_status._resolve_required_checks",
                return_value=evidence,
            ),
            patch("agentic_devtools.cli.github.pr_checks_status.set_value"),
        ):
            result = get_pr_checks_status(42, "owner/repo", _HEAD, "main")

        assert result["status"] == "failed"
        assert result["requiredChecksDiagnostics"] == ["Blocking check 'optional'"]

    @pytest.mark.parametrize(
        "requested_head,resolved_head,expected_status",
        [(_HEAD, _HEAD, "all-pass"), (None, _HEAD, "all-pass"), ("d" * 40, "", "pending")],
    )
    def test_direct_call_resolves_current_base_and_rejects_stale_head(
        self, requested_head, resolved_head, expected_status
    ):
        ready = bool(resolved_head)
        with (
            patch(
                "agentic_devtools.cli.github.pr_checks_status._fetch_pr_checks",
                return_value=[{"name": "build", "bucket": "pass"}],
            ),
            patch(
                "agentic_devtools.cli.github.pr_checks_status.get_pr_state",
                return_value={"baseRefName": "main", "headRefOid": _HEAD},
            ) as get_pr_state,
            patch(
                "agentic_devtools.cli.github.pr_checks_status._resolve_required_checks",
                return_value={
                    "complete": ready,
                    "ready": ready,
                    "checkRuns": [],
                    "diagnostics": [] if ready else ["Missing or invalid full head SHA"],
                },
            ) as resolve,
            patch("agentic_devtools.cli.github.pr_checks_status.set_value"),
        ):
            result = get_pr_checks_status(42, "owner/repo", requested_head)

        get_pr_state.assert_called_once_with(42, "owner/repo")
        resolve.assert_called_once_with("owner/repo", "main", resolved_head)
        assert result["status"] == expected_status

    def test_state_keys_written(self):
        with (
            patch(
                "agentic_devtools.cli.github.pr_checks_status._fetch_pr_checks",
                return_value=[
                    {"name": "build", "bucket": "pass"},
                    {"name": "lint", "bucket": "fail"},
                ],
            ),
            patch(
                "agentic_devtools.cli.github.pr_checks_status._resolve_required_checks",
                return_value={"complete": True, "ready": True, "checkRuns": [], "diagnostics": []},
            ),
            patch("agentic_devtools.cli.github.pr_checks_status.set_value") as mock_set_value,
        ):
            get_pr_checks_status(42, "owner/repo", _HEAD, "main")

        calls = {call.args[0]: call.args[1] for call in mock_set_value.call_args_list}
        assert calls["github.pr_checks_status"] == "failed"
        assert calls["github.pr_checks_failed"] == ["lint"]
        assert calls["github.pr_checks_pending"] == []

    def test_repo_trailing_git_stripped(self):
        with (
            patch(
                "agentic_devtools.cli.github.pr_checks_status._fetch_pr_checks",
                return_value=[],
            ),
            patch(
                "agentic_devtools.cli.github.pr_checks_status._resolve_required_checks",
                return_value={"complete": True, "ready": True, "checkRuns": [], "diagnostics": []},
            ),
            patch("agentic_devtools.cli.github.pr_checks_status.set_value"),
        ):
            result = get_pr_checks_status(42, "owner/repo.git", _HEAD, "main")
        assert result["repo"] == "owner/repo"

    def test_malformed_repo_no_slash(self):
        with pytest.raises(SystemExit) as exc_info:
            get_pr_checks_status(42, "noslash", _HEAD, "main")
        assert exc_info.value.code == 1

    def test_malformed_repo_multiple_slashes(self):
        with pytest.raises(SystemExit) as exc_info:
            get_pr_checks_status(42, "a/b/c", _HEAD, "main")
        assert exc_info.value.code == 1
