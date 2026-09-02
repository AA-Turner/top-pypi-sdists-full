from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import call, patch

import pytest

from agentic_devtools.cli.workflows import commands
from agentic_devtools.cli.workflows.preflight import PreflightResult
from agentic_devtools.orchestration.safety.mode import ExecutionMode, resolve_execution_mode


class TestExecutionModeFlag:
    """Tests for --execution-mode workflow CLI flags."""

    def test_pull_request_review_workflow_persists_execution_mode(self, tmp_path: Path) -> None:
        with patch("agentic_devtools.state.set_value") as mock_set_value:
            with patch("agentic_devtools.state.get_value", return_value=None):
                with patch("agentic_devtools.state.delete_value"):
                    with patch("agentic_devtools.state.delete_pin_file"):
                        with patch("agentic_devtools.state.write_pin_file"):
                            with patch("agentic_devtools.state.get_state_dir", return_value=tmp_path):
                                with patch(
                                    "agentic_devtools.cli.workflows.commands.get_default_copilot_model",
                                    return_value="gpt-4o",
                                ):
                                    with patch(
                                        "agentic_devtools.cli.workflows.commands.clear_state_for_workflow_initiation"
                                    ):
                                        with patch(
                                            "agentic_devtools.cli.workflows.commands._ensure_bootstrap_identity"
                                        ):
                                            with patch(
                                                "agentic_devtools.cli.workflows.commands._ensure_bootstrap_identity_and_scope"
                                            ):
                                                with pytest.raises(SystemExit) as exc_info:
                                                    commands.initiate_pull_request_review_workflow(
                                                        _argv=["--execution-mode", "dry_run"]
                                                    )

        assert exc_info.value.code == 1
        assert call("orchestration.execution_mode", "dry_run") in mock_set_value.call_args_list

    def test_work_on_jira_issue_workflow_persists_non_restricted_execution_mode(self) -> None:
        """dry_run mode must be persisted to state after bootstrap."""
        preflight_result = PreflightResult(
            folder_valid=False,
            branch_valid=False,
            folder_name="wrong-folder",
            branch_name="main",
            issue_key="PROJECT-1234",
        )

        with patch("agentic_devtools.state.set_value") as mock_set_value:
            with patch(
                "agentic_devtools.cli.workflows.commands._ensure_scoped_bootstrap_and_clear",
                return_value="PROJECT-1234",
            ):
                with patch(
                    "agentic_devtools.cli.workflows.commands.get_default_copilot_model",
                    return_value="gpt-4o",
                ):
                    with patch(
                        "agentic_devtools.cli.workflows.commands.check_worktree_and_branch",
                        return_value=preflight_result,
                    ):
                        with patch("agentic_devtools.cli.workflows.preflight.perform_auto_setup", return_value=True):
                            commands.initiate_work_on_jira_issue_workflow(_argv=["--execution-mode", "dry_run"])

        assert call("orchestration.execution_mode", "dry_run") in mock_set_value.call_args_list

    def test_work_on_jira_issue_workflow_persists_effective_mode_when_state_is_stricter(self) -> None:
        """Persist the resolved mode instead of a less restrictive CLI override."""
        preflight_result = PreflightResult(
            folder_valid=False,
            branch_valid=False,
            folder_name="wrong-folder",
            branch_name="main",
            issue_key="PROJECT-1234",
        )

        with patch("agentic_devtools.state.set_value") as mock_set_value:
            with patch(
                "agentic_devtools.cli.workflows.commands._read_scoped_execution_signals",
                return_value=("dry_run", False),
            ):
                with patch(
                    "agentic_devtools.cli.workflows.commands._ensure_scoped_bootstrap_and_clear",
                    return_value="PROJECT-1234",
                ):
                    with patch(
                        "agentic_devtools.cli.workflows.commands.get_default_copilot_model",
                        return_value="gpt-4o",
                    ):
                        with patch(
                            "agentic_devtools.cli.workflows.commands.check_worktree_and_branch",
                            return_value=preflight_result,
                        ):
                            with patch(
                                "agentic_devtools.cli.workflows.preflight.perform_auto_setup",
                                return_value=True,
                            ):
                                commands.initiate_work_on_jira_issue_workflow(
                                    _argv=["--issue-key", "PROJECT-1234", "--execution-mode", "live"]
                                )

        assert call("orchestration.execution_mode", "dry_run") in mock_set_value.call_args_list

    def test_work_on_jira_issue_workflow_rejects_restricted_mode_before_state_writes(self) -> None:
        """restricted mode must exit before any state writes (bootstrap, model, mode)."""
        with patch("agentic_devtools.state.set_value") as mock_set_value:
            with patch("agentic_devtools.cli.workflows.commands._ensure_scoped_bootstrap_and_clear") as mock_bootstrap:
                with patch(
                    "agentic_devtools.cli.workflows.commands.get_default_copilot_model",
                    return_value="gpt-4o",
                ):
                    with pytest.raises(SystemExit) as exc_info:
                        commands.initiate_work_on_jira_issue_workflow(
                            _argv=["--issue-key", "PROJECT-1234", "--execution-mode", "restricted"]
                        )

        assert exc_info.value.code == 1
        # Bootstrap and state writes must NOT have been called
        mock_bootstrap.assert_not_called()
        mock_set_value.assert_not_called()


class TestReadScopedExecutionSignals:
    @pytest.fixture(autouse=True)
    def _clear_state_dir_env(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Keep tests deterministic regardless of inherited AGENTIC_DEVTOOLS_STATE_DIR."""
        monkeypatch.delenv("AGENTIC_DEVTOOLS_STATE_DIR", raising=False)

    def test_reads_scoped_signals_from_issue_scope(self, tmp_path: Path) -> None:
        state_path = tmp_path / ".agdt" / "workflows" / "abc" / "PROJECT-1234" / "state.json"
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(
            '{"orchestration": {"execution_mode": "restricted"}, "dry_run": true}',
            encoding="utf-8",
        )

        with patch("agentic_devtools.state.get_bootstrap_state", return_value={"identity": "abc"}):
            with patch("agentic_devtools.state.is_safe_dir_segment", return_value=True):
                with patch("agentic_devtools.cli.workflows.commands.get_git_repo_root", return_value=str(tmp_path)):
                    mode, dry_run = commands._read_scoped_execution_signals("PROJECT-1234")

        assert mode == "restricted"
        assert dry_run is True

    def test_reads_scoped_signals_from_bootstrap_scope_when_issue_missing(self, tmp_path: Path) -> None:
        state_path = tmp_path / ".agdt" / "workflows" / "abc" / "PROJECT-1234" / "state.json"
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(
            '{"orchestration": {"execution_mode": "dry_run"}, "dry_run": false}',
            encoding="utf-8",
        )

        with patch(
            "agentic_devtools.state.get_bootstrap_state",
            return_value={"identity": "abc", "worktree_key": "PROJECT-1234"},
        ):
            with patch("agentic_devtools.state.is_safe_dir_segment", return_value=True):
                with patch("agentic_devtools.cli.workflows.commands.get_git_repo_root", return_value=str(tmp_path)):
                    mode, dry_run = commands._read_scoped_execution_signals(None)

        assert mode == "dry_run"
        assert dry_run is False

    def test_returns_none_mode_when_persisted_mode_is_not_string(self, tmp_path: Path) -> None:
        state_path = tmp_path / ".agdt" / "workflows" / "abc" / "PROJECT-1234" / "state.json"
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(
            '{"orchestration": {"execution_mode": 1}, "dry_run": "true"}',
            encoding="utf-8",
        )

        with patch("agentic_devtools.state.get_bootstrap_state", return_value={"identity": "abc"}):
            with patch("agentic_devtools.state.is_safe_dir_segment", return_value=True):
                with patch("agentic_devtools.cli.workflows.commands.get_git_repo_root", return_value=str(tmp_path)):
                    mode, dry_run = commands._read_scoped_execution_signals("PROJECT-1234")

        assert mode is None
        assert dry_run == "true"
        assert resolve_execution_mode(state_mode=mode, state_dry_run=dry_run) is ExecutionMode.dry_run

    def test_returns_none_when_worktree_key_cannot_be_resolved(self) -> None:
        with patch("agentic_devtools.state.get_bootstrap_state", return_value={"identity": "abc"}):
            mode, dry_run = commands._read_scoped_execution_signals(None)

        assert mode is None
        assert dry_run is None

    def test_returns_none_when_bootstrap_identity_is_missing(self) -> None:
        with patch("agentic_devtools.state.get_bootstrap_state", return_value={}):
            mode, dry_run = commands._read_scoped_execution_signals("PROJECT-1234")

        assert mode is None
        assert dry_run is None

    def test_returns_none_when_scope_segments_are_unsafe(self) -> None:
        with patch(
            "agentic_devtools.state.get_bootstrap_state",
            return_value={"identity": "abc", "worktree_key": "PROJECT-1234"},
        ):
            with patch("agentic_devtools.state.is_safe_dir_segment", return_value=False):
                mode, dry_run = commands._read_scoped_execution_signals(None)

        assert mode is None
        assert dry_run is None

    def test_returns_none_when_repo_root_is_unavailable(self) -> None:
        with patch(
            "agentic_devtools.state.get_bootstrap_state",
            return_value={"identity": "abc", "worktree_key": "PROJECT-1234"},
        ):
            with patch("agentic_devtools.state.is_safe_dir_segment", return_value=True):
                with patch("agentic_devtools.cli.workflows.commands.get_git_repo_root", return_value=None):
                    mode, dry_run = commands._read_scoped_execution_signals(None)

        assert mode is None
        assert dry_run is None

    def test_returns_none_when_scoped_state_file_is_missing(self, tmp_path: Path) -> None:
        with patch(
            "agentic_devtools.state.get_bootstrap_state",
            return_value={"identity": "abc", "worktree_key": "PROJECT-1234"},
        ):
            with patch("agentic_devtools.state.is_safe_dir_segment", return_value=True):
                with patch("agentic_devtools.cli.workflows.commands.get_git_repo_root", return_value=str(tmp_path)):
                    mode, dry_run = commands._read_scoped_execution_signals(None)

        assert mode is None
        assert dry_run is None

    def test_returns_none_when_scoped_state_json_is_invalid(self, tmp_path: Path) -> None:
        state_path = tmp_path / ".agdt" / "workflows" / "abc" / "PROJECT-1234" / "state.json"
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text("{not-json}", encoding="utf-8")

        with patch("agentic_devtools.state.get_bootstrap_state", return_value={"identity": "abc"}):
            with patch("agentic_devtools.state.is_safe_dir_segment", return_value=True):
                with patch("agentic_devtools.cli.workflows.commands.get_git_repo_root", return_value=str(tmp_path)):
                    mode, dry_run = commands._read_scoped_execution_signals("PROJECT-1234")

        assert mode is None
        assert dry_run is None

    def test_returns_none_when_scoped_state_payload_is_not_object(self, tmp_path: Path) -> None:
        state_path = tmp_path / ".agdt" / "workflows" / "abc" / "PROJECT-1234" / "state.json"
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text("[]", encoding="utf-8")

        with patch("agentic_devtools.state.get_bootstrap_state", return_value={"identity": "abc"}):
            with patch("agentic_devtools.state.is_safe_dir_segment", return_value=True):
                with patch("agentic_devtools.cli.workflows.commands.get_git_repo_root", return_value=str(tmp_path)):
                    mode, dry_run = commands._read_scoped_execution_signals("PROJECT-1234")

        assert mode is None
        assert dry_run is None

    def test_work_on_jira_issue_workflow_rejects_scoped_restricted_mode_before_state_writes(self) -> None:
        """Scoped persisted restricted mode must exit before any state writes."""
        with patch("agentic_devtools.state.set_value") as mock_set_value:
            with patch("agentic_devtools.cli.workflows.commands._ensure_scoped_bootstrap_and_clear") as mock_bootstrap:
                with patch(
                    "agentic_devtools.cli.workflows.commands._read_scoped_execution_signals",
                    return_value=("restricted", None),
                ):
                    with patch(
                        "agentic_devtools.cli.workflows.commands.get_default_copilot_model",
                        return_value="gpt-4o",
                    ):
                        with pytest.raises(SystemExit) as exc_info:
                            commands.initiate_work_on_jira_issue_workflow(_argv=["--issue-key", "PROJECT-1234"])

        assert exc_info.value.code == 1
        # Bootstrap and state writes must NOT have been called
        mock_bootstrap.assert_not_called()
        mock_set_value.assert_not_called()

    def test_reads_scoped_signals_for_github_hash_issue_key(self, tmp_path: Path) -> None:
        """#42 GitHub keys must be canonicalized to 42 before directory lookup."""
        state_path = tmp_path / ".agdt" / "workflows" / "abc" / "42" / "state.json"
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(
            '{"orchestration": {"execution_mode": "restricted"}, "dry_run": false}',
            encoding="utf-8",
        )

        with patch("agentic_devtools.state.get_bootstrap_state", return_value={"identity": "abc"}):
            with patch("agentic_devtools.state.is_safe_dir_segment", return_value=True):
                with patch("agentic_devtools.cli.workflows.commands.get_git_repo_root", return_value=str(tmp_path)):
                    mode, dry_run = commands._read_scoped_execution_signals("#42")

        assert mode == "restricted"
        assert dry_run is False

    def test_reads_signals_from_env_state_dir_without_bootstrap_identity(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """AGENTIC_DEVTOOLS_STATE_DIR must be honored before scoped bootstrap fallback."""
        state_path = tmp_path / "env-state" / "state.json"
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(
            '{"orchestration": {"execution_mode": "restricted"}, "dry_run": true}',
            encoding="utf-8",
        )
        monkeypatch.setenv("AGENTIC_DEVTOOLS_STATE_DIR", str(state_path.parent))

        with patch("agentic_devtools.state.get_bootstrap_state", return_value={}):
            mode, dry_run = commands._read_scoped_execution_signals("PROJECT-1234")

        assert mode == "restricted"
        assert dry_run is True

    def test_reads_signals_from_valid_pin_without_bootstrap_identity(
        self,
        tmp_path: Path,
        monkeypatch: pytest.MonkeyPatch,
    ) -> None:
        """Valid pin-file state dir must be checked before scoped bootstrap fallback."""
        state_dir = tmp_path / ".agdt" / "workflows" / "abc" / "PROJECT-1234"
        state_dir.mkdir(parents=True, exist_ok=True)
        (state_dir / "state.json").write_text(
            '{"orchestration": {"execution_mode": "restricted"}, "dry_run": false}',
            encoding="utf-8",
        )
        (tmp_path / ".agdt" / "pinned-state-dir.json").write_text(
            (
                "{\n"
                f'  "state_dir": {json.dumps(str(state_dir))},\n'
                '  "workflow": "work-on-jira-issue",\n'
                '  "created_utc": "2099-01-01T00:00:00+00:00",\n'
                '  "ttl_hours": 24\n'
                "}"
            ),
            encoding="utf-8",
        )

        with patch("agentic_devtools.cli.workflows.commands.get_git_repo_root", return_value=str(tmp_path)):
            with patch("agentic_devtools.state.get_bootstrap_state", return_value={}):
                mode, dry_run = commands._read_scoped_execution_signals("PROJECT-1234")

        assert mode == "restricted"
        assert dry_run is False

    def test_reads_signals_from_valid_pin_with_float_ttl_hours(
        self,
        tmp_path: Path,
    ) -> None:
        """Float ttl_hours (e.g. 24.0) must be accepted, matching the canonical state.py validator."""
        state_dir = tmp_path / ".agdt" / "workflows" / "abc" / "PROJECT-1234"
        state_dir.mkdir(parents=True, exist_ok=True)
        (state_dir / "state.json").write_text(
            '{"orchestration": {"execution_mode": "restricted"}, "dry_run": false}',
            encoding="utf-8",
        )
        (tmp_path / ".agdt" / "pinned-state-dir.json").write_text(
            (
                "{\n"
                f'  "state_dir": {json.dumps(str(state_dir))},\n'
                '  "workflow": "work-on-jira-issue",\n'
                '  "created_utc": "2099-01-01T00:00:00+00:00",\n'
                '  "ttl_hours": 24.0\n'
                "}"
            ),
            encoding="utf-8",
        )

        with patch("agentic_devtools.cli.workflows.commands.get_git_repo_root", return_value=str(tmp_path)):
            with patch("agentic_devtools.state.get_bootstrap_state", return_value={}):
                mode, dry_run = commands._read_scoped_execution_signals("PROJECT-1234")

        assert mode == "restricted"
        assert dry_run is False

    def test_invalid_pin_metadata_types_are_ignored(self, tmp_path: Path) -> None:
        """Pin metadata must have the expected JSON types before date validation."""
        state_dir = tmp_path / ".agdt" / "workflows" / "abc" / "PROJECT-1234"
        state_dir.mkdir(parents=True, exist_ok=True)
        (tmp_path / ".agdt" / "pinned-state-dir.json").write_text(
            json.dumps(
                {
                    "state_dir": str(state_dir),
                    "workflow": "work-on-jira-issue",
                    "created_utc": 2099,
                    "ttl_hours": 24,
                }
            ),
            encoding="utf-8",
        )

        with patch("agentic_devtools.cli.workflows.commands.get_git_repo_root", return_value=str(tmp_path)):
            with patch("agentic_devtools.state.get_bootstrap_state", return_value={}):
                mode, dry_run = commands._read_scoped_execution_signals("PROJECT-1234")

        assert mode is None
        assert dry_run is None

    def test_malformed_pin_timestamp_is_ignored(self, tmp_path: Path) -> None:
        """Malformed timestamps must be rejected after valid path metadata is read."""
        state_dir = tmp_path / ".agdt" / "workflows" / "abc" / "PROJECT-1234"
        state_dir.mkdir(parents=True, exist_ok=True)
        (tmp_path / ".agdt" / "pinned-state-dir.json").write_text(
            json.dumps(
                {
                    "state_dir": str(state_dir),
                    "workflow": "work-on-jira-issue",
                    "created_utc": "not-a-date",
                    "ttl_hours": 24,
                }
            ),
            encoding="utf-8",
        )

        with patch("agentic_devtools.cli.workflows.commands.get_git_repo_root", return_value=str(tmp_path)):
            with patch("agentic_devtools.state.get_bootstrap_state", return_value={}):
                mode, dry_run = commands._read_scoped_execution_signals("PROJECT-1234")

        assert mode is None
        assert dry_run is None

    @pytest.mark.parametrize(
        ("pin_payload", "expected_mode"),
        [
            ("[]", None),
            (
                (
                    "{\n"
                    '  "state_dir": "/tmp/nowhere",\n'
                    '  "workflow": "unknown-workflow",\n'
                    '  "created_utc": "2099-01-01T00:00:00+00:00",\n'
                    '  "ttl_hours": 24\n'
                    "}"
                ),
                None,
            ),
            (
                (
                    "{\n"
                    '  "state_dir": "   ",\n'
                    '  "workflow": "work-on-jira-issue",\n'
                    '  "created_utc": "2099-01-01T00:00:00+00:00",\n'
                    '  "ttl_hours": 24\n'
                    "}"
                ),
                None,
            ),
            (
                (
                    "{\n"
                    '  "state_dir": "relative/path",\n'
                    '  "workflow": "work-on-jira-issue",\n'
                    '  "created_utc": "2099-01-01T00:00:00+00:00",\n'
                    '  "ttl_hours": 24\n'
                    "}"
                ),
                None,
            ),
            (
                (
                    "{\n"
                    '  "state_dir": "/tmp/nowhere",\n'
                    '  "workflow": "work-on-jira-issue",\n'
                    '  "created_utc": "not-a-date",\n'
                    '  "ttl_hours": 24\n'
                    "}"
                ),
                None,
            ),
            (
                (
                    "{\n"
                    '  "state_dir": "/tmp/nowhere",\n'
                    '  "workflow": "work-on-jira-issue",\n'
                    '  "created_utc": "2099-01-01T00:00:00+00:00",\n'
                    '  "ttl_hours": 0\n'
                    "}"
                ),
                None,
            ),
        ],
    )
    def test_invalid_pin_payloads_fall_back_without_crashing(
        self,
        tmp_path: Path,
        pin_payload: str,
        expected_mode: str | None,
    ) -> None:
        """Invalid pin payload variants must safely fall back to non-pinned resolution."""
        (tmp_path / ".agdt").mkdir(parents=True, exist_ok=True)
        (tmp_path / ".agdt" / "pinned-state-dir.json").write_text(pin_payload, encoding="utf-8")

        with patch("agentic_devtools.cli.workflows.commands.get_git_repo_root", return_value=str(tmp_path)):
            with patch("agentic_devtools.state.get_bootstrap_state", return_value={}):
                mode, dry_run = commands._read_scoped_execution_signals("PROJECT-1234")

        assert mode is expected_mode
        assert dry_run is None

    def test_pin_payload_with_naive_timestamp_is_treated_as_utc(self, tmp_path: Path) -> None:
        """Naive created_utc values should be accepted and interpreted as UTC."""
        state_dir = tmp_path / ".agdt" / "workflows" / "abc" / "PROJECT-1234"
        state_dir.mkdir(parents=True, exist_ok=True)
        (state_dir / "state.json").write_text(
            '{"orchestration": {"execution_mode": "restricted"}, "dry_run": false}',
            encoding="utf-8",
        )
        (tmp_path / ".agdt" / "pinned-state-dir.json").write_text(
            (
                "{\n"
                f'  "state_dir": {json.dumps(str(state_dir))},\n'
                '  "workflow": "work-on-jira-issue",\n'
                '  "created_utc": "2099-01-01T00:00:00",\n'
                '  "ttl_hours": 24\n'
                "}"
            ),
            encoding="utf-8",
        )

        with patch("agentic_devtools.cli.workflows.commands.get_git_repo_root", return_value=str(tmp_path)):
            with patch("agentic_devtools.state.get_bootstrap_state", return_value={}):
                mode, dry_run = commands._read_scoped_execution_signals("PROJECT-1234")

        assert mode == "restricted"
        assert dry_run is False

    def test_expired_pin_payload_is_ignored(self, tmp_path: Path) -> None:
        """Expired pins must be ignored and return no scoped execution signals."""
        state_dir = tmp_path / ".agdt" / "workflows" / "abc" / "PROJECT-1234"
        state_dir.mkdir(parents=True, exist_ok=True)
        (state_dir / "state.json").write_text(
            '{"orchestration": {"execution_mode": "restricted"}, "dry_run": false}',
            encoding="utf-8",
        )
        (tmp_path / ".agdt" / "pinned-state-dir.json").write_text(
            (
                "{\n"
                f'  "state_dir": {json.dumps(str(state_dir))},\n'
                '  "workflow": "work-on-jira-issue",\n'
                '  "created_utc": "2000-01-01T00:00:00+00:00",\n'
                '  "ttl_hours": 1\n'
                "}"
            ),
            encoding="utf-8",
        )

        with patch("agentic_devtools.cli.workflows.commands.get_git_repo_root", return_value=str(tmp_path)):
            with patch("agentic_devtools.state.get_bootstrap_state", return_value={}):
                mode, dry_run = commands._read_scoped_execution_signals("PROJECT-1234")

        assert mode is None
        assert dry_run is None

    def test_pin_payload_outside_workflows_root_is_ignored(self, tmp_path: Path) -> None:
        """Pinned state_dir outside .agdt/workflows must be rejected."""
        outside_state_dir = tmp_path / "outside-scope"
        outside_state_dir.mkdir(parents=True, exist_ok=True)
        (outside_state_dir / "state.json").write_text(
            '{"orchestration": {"execution_mode": "restricted"}, "dry_run": false}',
            encoding="utf-8",
        )
        (tmp_path / ".agdt").mkdir(parents=True, exist_ok=True)
        (tmp_path / ".agdt" / "pinned-state-dir.json").write_text(
            (
                "{\n"
                f'  "state_dir": {json.dumps(str(outside_state_dir))},\n'
                '  "workflow": "work-on-jira-issue",\n'
                '  "created_utc": "2099-01-01T00:00:00+00:00",\n'
                '  "ttl_hours": 24\n'
                "}"
            ),
            encoding="utf-8",
        )

        with patch("agentic_devtools.cli.workflows.commands.get_git_repo_root", return_value=str(tmp_path)):
            with patch("agentic_devtools.state.get_bootstrap_state", return_value={}):
                mode, dry_run = commands._read_scoped_execution_signals("PROJECT-1234")

        assert mode is None
        assert dry_run is None

    def test_orchestration_key_not_dict_returns_none_mode(self, tmp_path: Path) -> None:
        """orchestration value that is not a dict must not raise and must return None mode."""
        state_path = tmp_path / ".agdt" / "workflows" / "abc" / "PROJECT-1234" / "state.json"
        state_path.parent.mkdir(parents=True, exist_ok=True)
        state_path.write_text(
            '{"orchestration": "restricted", "dry_run": true}',
            encoding="utf-8",
        )

        with patch("agentic_devtools.state.get_bootstrap_state", return_value={"identity": "abc"}):
            with patch("agentic_devtools.state.is_safe_dir_segment", return_value=True):
                with patch("agentic_devtools.cli.workflows.commands.get_git_repo_root", return_value=str(tmp_path)):
                    mode, dry_run = commands._read_scoped_execution_signals("PROJECT-1234")

        assert mode is None
        assert dry_run is True
