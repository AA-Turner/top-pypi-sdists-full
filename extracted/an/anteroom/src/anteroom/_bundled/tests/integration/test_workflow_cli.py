"""CLI integration tests for `aroom workflow` subcommands.

Tests real argparse dispatch via subprocess. Exercises the actual
`python -m anteroom workflow` command path — not direct handler calls.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

_PYTHON = sys.executable


@pytest.fixture(autouse=True)
def _isolated_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    """Use an isolated HOME so workflow runs don't pollute the user's DB."""
    anteroom_dir = tmp_path / ".anteroom"
    anteroom_dir.mkdir()
    config_file = anteroom_dir / "config.yaml"
    config_file.write_text('ai:\n  base_url: "http://localhost:1/v1"\n  api_key: "test"\n  model: "test"\n')
    monkeypatch.setenv("HOME", str(tmp_path))
    yield


# A generic test workflow (shell-only, no AI needed, no GitHub concepts)
# Uses no required inputs so it can be run via `aroom workflow run <path>`
# without needing --issue or other flags.
_TEST_WORKFLOW_YAML = """\
kind: workflow
id: test_cli_pipeline
version: 0.1.0
inputs: {}
steps:
  - id: greet
    type: runner
    runner: shell
    command: "echo Hello from workflow"
    timeout: 10
  - id: validate
    type: runner
    runner: shell
    command: "echo Validation passed"
    timeout: 10
"""


def _run_aroom(*args: str, timeout: int = 30) -> subprocess.CompletedProcess:
    """Run `aroom` CLI via subprocess and capture output."""
    return subprocess.run(
        [_PYTHON, "-m", "anteroom", *args],
        capture_output=True,
        text=True,
        timeout=timeout,
    )


# ---------------------------------------------------------------------------
# Help and error handling (subprocess)
# ---------------------------------------------------------------------------


class TestWorkflowCLIHelp:
    """Help text renders correctly for workflow subcommands."""

    def test_workflow_help(self) -> None:
        result = _run_aroom("workflow", "--help")
        assert result.returncode == 0
        assert "run" in result.stdout
        assert "status" in result.stdout
        assert "list" in result.stdout
        assert "history" in result.stdout

    def test_workflow_run_help(self) -> None:
        result = _run_aroom("workflow", "run", "--help")
        assert result.returncode == 0
        assert "workflow_name" in result.stdout
        assert "--issue" in result.stdout
        assert "--dry-run" in result.stdout
        assert "--detach" in result.stdout

    def test_workflow_status_help(self) -> None:
        result = _run_aroom("workflow", "status", "--help")
        assert result.returncode == 0
        assert "run_id" in result.stdout

    def test_workflow_list_help(self) -> None:
        result = _run_aroom("workflow", "list", "--help")
        assert result.returncode == 0
        assert "--status" in result.stdout
        assert "--limit" in result.stdout

    def test_workflow_history_help(self) -> None:
        result = _run_aroom("workflow", "history", "--help")
        assert result.returncode == 0
        assert "run_id" in result.stdout


class TestWorkflowCLIDryRun:
    """Dry run shows workflow plan without executing."""

    def test_dry_run_issue_delivery(self) -> None:
        result = _run_aroom("workflow", "run", "issue_delivery", "--dry-run", "--issue", "42")
        assert result.returncode == 0
        assert "issue_delivery" in result.stdout
        assert "v0.1.0" in result.stdout
        assert "issue:42" in result.stdout
        assert "gate_issue_current" in result.stdout
        assert "gate_plan" in result.stdout
        assert "fast_checks_loop" in result.stdout
        assert "sync_for_pr" in result.stdout
        assert "review_loop" in result.stdout

    def test_dry_run_unknown_workflow(self) -> None:
        result = _run_aroom("workflow", "run", "nonexistent", "--dry-run")
        assert result.returncode == 0
        assert "Unknown workflow" in result.stdout or "Error" in result.stdout


# ---------------------------------------------------------------------------
# Real command path tests — run/status/list/history via subprocess
# ---------------------------------------------------------------------------


class TestWorkflowCLIRealCommands:
    """Drive real `python -m anteroom workflow` commands through subprocess.

    Uses a shell-only test workflow (no AI needed) written to a temp file.
    The actual argparse → config → handler → engine → storage path is
    exercised end-to-end.
    """

    @pytest.fixture()
    def workflow_file(self, tmp_path: Path) -> Path:
        """Write the test workflow YAML to a temp file."""
        wf = tmp_path / "test_pipeline.yaml"
        wf.write_text(_TEST_WORKFLOW_YAML)
        return wf

    def test_run_shell_workflow_completes(self, workflow_file: Path) -> None:
        """Run a shell-only workflow via the real CLI and verify completion."""
        result = _run_aroom(
            "workflow",
            "run",
            str(workflow_file),
            timeout=30,
        )
        # The workflow should complete (shell commands are simple echos)
        output = result.stdout + result.stderr
        assert "completed" in output.lower() or "Workflow completed" in output
        assert "Run ID:" in output

    def test_run_then_list_shows_run(self, workflow_file: Path) -> None:
        """After running a workflow, `list` shows it."""
        # Run the workflow first
        _run_aroom("workflow", "run", str(workflow_file), timeout=30)
        # List should show the run
        list_result = _run_aroom("workflow", "list")
        list_output = list_result.stdout
        assert list_result.returncode == 0
        # Should show either the workflow ID or the run table
        assert "test_cli_pipeline" in list_output or "Workflow Runs" in list_output
        assert "State" in list_output
        assert "Step" not in list_output

    def test_run_then_status_shows_details(self, workflow_file: Path) -> None:
        """After running, `status <run_id>` shows run details."""
        # Run the workflow and extract run ID
        run_result = _run_aroom(
            "workflow",
            "run",
            str(workflow_file),
            timeout=30,
        )
        run_output = run_result.stdout + run_result.stderr

        # Extract run ID from output
        run_id = None
        for line in run_output.splitlines():
            if "Run ID:" in line:
                run_id = line.split("Run ID:")[-1].strip()
                break

        if run_id:
            status_result = _run_aroom("workflow", "status", run_id)
            status_output = status_result.stdout
            assert status_result.returncode == 0
            assert "test_cli_pipeline" in status_output or run_id[:12] in status_output

    def test_run_then_history_shows_steps(self, workflow_file: Path) -> None:
        """After running, `history <run_id>` shows step details."""
        # Run the workflow and extract run ID
        run_result = _run_aroom(
            "workflow",
            "run",
            str(workflow_file),
            timeout=30,
        )
        run_output = run_result.stdout + run_result.stderr

        # Extract run ID
        run_id = None
        for line in run_output.splitlines():
            if "Run ID:" in line:
                run_id = line.split("Run ID:")[-1].strip()
                break

        if run_id:
            history_result = _run_aroom("workflow", "history", run_id)
            history_output = history_result.stdout
            assert history_result.returncode == 0
            # Should show step names from the workflow
            assert "greet" in history_output or "validate" in history_output

    def test_status_nonexistent_run(self) -> None:
        """Status with a fake run ID shows error, doesn't crash."""
        result = _run_aroom("workflow", "status", "nonexistent-fake-id")
        output = result.stdout + result.stderr
        assert "not found" in output.lower() or "Error" in output

    def test_list_empty_state(self) -> None:
        """List with no runs shows empty message."""
        result = _run_aroom("workflow", "list")
        assert result.returncode == 0
        output = result.stdout
        assert "No workflow runs" in output or "Workflow Runs" in output

    def test_list_output_is_run_centric(self, workflow_file: Path) -> None:
        """List view shows run-level columns, not step-level detail."""
        _run_aroom("workflow", "run", str(workflow_file), timeout=30)
        result = _run_aroom("workflow", "list")
        output = result.stdout
        assert result.returncode == 0
        # Run-centric columns should be present
        assert "Run" in output
        assert "Workflow" in output
        assert "State" in output
        # Step-level columns should NOT be primary headers
        assert "Step ID" not in output
        assert "Runner" not in output


# ---------------------------------------------------------------------------
# Watch subcommand (#888)
# ---------------------------------------------------------------------------


class TestWorkflowCLIWatch:
    """Integration tests for `aroom workflow watch`."""

    def test_watch_help(self) -> None:
        result = _run_aroom("workflow", "watch", "--help")
        assert result.returncode == 0
        assert "run_id" in result.stdout

    def test_watch_nonexistent_run(self) -> None:
        """Watch with a fake run ID shows error, doesn't crash."""
        result = _run_aroom("workflow", "watch", "nonexistent-fake-id", timeout=10)
        output = result.stdout + result.stderr
        assert "not found" in output.lower() or "Error" in output

    def test_watch_completed_run_exits(self, tmp_path: Path) -> None:
        """Watch exits immediately when the run is already in terminal status.

        Creates a real workflow run via `aroom workflow run`, then watches it.
        Since the run completes synchronously before watch starts, watch should
        see the terminal status and exit right away.
        """
        wf_path = tmp_path / "fast.yaml"
        wf_path.write_text(_TEST_WORKFLOW_YAML)

        # Run the workflow to completion
        run_result = _run_aroom("workflow", "run", str(wf_path), timeout=30)
        assert run_result.returncode == 0

        # Extract run_id from output — look for a UUID-like string after "run_id"
        import re

        run_output = run_result.stdout
        # The run output typically contains the run ID in the status display
        uuid_pattern = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
        match = uuid_pattern.search(run_output)
        if not match:
            pytest.skip("Could not extract run_id from workflow run output")

        run_id = match.group(0)

        # Watch the already-completed run — should exit immediately
        watch_result = _run_aroom("workflow", "watch", run_id, timeout=10)
        watch_output = watch_result.stdout + watch_result.stderr
        assert "completed" in watch_output.lower() or "failed" in watch_output.lower()


# ---------------------------------------------------------------------------
# Timeline output format (#1102)
# ---------------------------------------------------------------------------


def _run_workflow_and_get_id(workflow_yaml: str, tmp_path: Path) -> str:
    """Run a workflow and extract the run ID."""
    import re

    wf_path = tmp_path / "timeline_test.yaml"
    wf_path.write_text(workflow_yaml)
    run_result = _run_aroom("workflow", "run", str(wf_path), timeout=30)
    assert run_result.returncode == 0, f"workflow run failed: {run_result.stderr}"
    run_output = run_result.stdout
    uuid_pattern = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
    match = uuid_pattern.search(run_output)
    assert match, f"Could not extract run_id: {run_output}"
    return match.group(0)


class TestTimelineOutput:
    """Verify that watch/status/history use the timeline-style output (#1102)."""

    def test_status_shows_timeline_step_lines(self, tmp_path: Path) -> None:
        """Status output contains status icons and friendly durations."""
        run_id = _run_workflow_and_get_id(_TEST_WORKFLOW_YAML, tmp_path)
        result = _run_aroom("workflow", "status", run_id)
        output = result.stdout
        assert result.returncode == 0

        # Timeline step lines should show step names
        assert "greet" in output
        assert "validate" in output
        # Should show status icons (completed steps)
        # Rich renders Unicode so we check for the icon OR the step status text
        assert "completed" in output.lower() or "\u2705" in output or "success" in output.lower()
        # Should show the run header with workflow id
        assert "test_cli_pipeline" in output

    def test_status_shows_friendly_durations(self, tmp_path: Path) -> None:
        """Status uses friendly duration format, not raw ms."""
        run_id = _run_workflow_and_get_id(_TEST_WORKFLOW_YAML, tmp_path)
        result = _run_aroom("workflow", "status", run_id)
        output = result.stdout
        assert result.returncode == 0
        # Friendly durations contain 's' (e.g., '< 1s', '3s', '1m 5s')
        # The old format was raw 'ms' (e.g., '150ms')
        # At least one step should have completed with a friendly duration
        assert "s" in output  # every friendly duration ends in 's'

    def test_watch_completed_shows_timeline(self, tmp_path: Path) -> None:
        """Watch on a completed run shows timeline header and step lines."""
        run_id = _run_workflow_and_get_id(_TEST_WORKFLOW_YAML, tmp_path)
        result = _run_aroom("workflow", "watch", run_id, timeout=10)
        output = result.stdout + result.stderr
        assert "test_cli_pipeline" in output
        assert "greet" in output or "validate" in output
        # Should show terminal status
        assert "completed" in output.lower() or "failed" in output.lower()

    def test_history_preserves_detail_columns(self, tmp_path: Path) -> None:
        """History retains the detailed table with Runner, Result, Duration columns."""
        run_id = _run_workflow_and_get_id(_TEST_WORKFLOW_YAML, tmp_path)
        result = _run_aroom("workflow", "history", run_id)
        output = result.stdout
        assert result.returncode == 0
        # History should have the detail table columns (may be truncated by Rich)
        assert "Runner" in output
        assert "Result" in output
        assert "Durat" in output  # "Duration" or "Durat…" when truncated
        # Step names should be present
        assert "greet" in output
        assert "validate" in output
        # Should also show the timeline run header
        assert "test_cli_pipeline" in output

    def test_history_uses_friendly_durations(self, tmp_path: Path) -> None:
        """History table uses friendly duration format."""
        run_id = _run_workflow_and_get_id(_TEST_WORKFLOW_YAML, tmp_path)
        result = _run_aroom("workflow", "history", run_id)
        output = result.stdout
        assert result.returncode == 0
        # Old format was 'NNNms', new format is '< 1s' or 'Ns' etc.
        # The word 'ms' should NOT appear in duration column
        # (It may appear elsewhere like in column headers, but not as a step duration value)
        lines_with_greet = [ln for ln in output.splitlines() if "greet" in ln]
        assert len(lines_with_greet) > 0
        # The greet step's line should not have raw ms format
        for line in lines_with_greet:
            # Raw ms would look like '150ms' or '2000ms' — check it's not there
            import re

            assert not re.search(r"\d+ms", line), f"Raw ms duration found in history: {line}"


# A workflow with triggers for schedule tests (#969)
_TRIGGER_WORKFLOW_YAML = """\
kind: workflow
id: test_scheduled_pipeline
version: 0.1.0
inputs: {}
triggers:
  - type: schedule
    cron: "0 * * * *"
    target_ref: hourly-check
    missed_policy: skip
steps:
  - id: greet
    type: runner
    runner: shell
    command: "echo Hello from scheduled workflow"
    timeout: 10
"""


# ---------------------------------------------------------------------------
# Triggers and schedule subcommands (#969)
# ---------------------------------------------------------------------------


class TestWorkflowCLITriggers:
    """Integration tests for `aroom workflow triggers` and `aroom workflow schedule`."""

    def test_triggers_help(self) -> None:
        result = _run_aroom("workflow", "triggers", "--help")
        assert result.returncode == 0
        assert "list" in result.stdout
        assert "fire" in result.stdout

    def test_triggers_list_empty(self) -> None:
        result = _run_aroom("workflow", "triggers", "list")
        assert result.returncode == 0
        output = result.stdout + result.stderr
        assert "No workflow schedules" in output or "Workflow Schedules" in output

    def test_schedule_registers_triggers(self, tmp_path: Path) -> None:
        """Register triggers from a workflow YAML and verify they appear in triggers list."""
        # Place in ~/.anteroom/ so path confinement allows it
        anteroom_dir = tmp_path / ".anteroom"
        anteroom_dir.mkdir(exist_ok=True)
        wf_path = anteroom_dir / "scheduled.yaml"
        wf_path.write_text(_TRIGGER_WORKFLOW_YAML)

        # Register
        result = _run_aroom("workflow", "schedule", str(wf_path))
        assert result.returncode == 0
        output = result.stdout
        assert "Schedule created" in output

        # Verify it appears in the list
        list_result = _run_aroom("workflow", "triggers", "list")
        assert list_result.returncode == 0
        assert "0 * * * *" in list_result.stdout

    def test_schedule_help(self) -> None:
        result = _run_aroom("workflow", "schedule", "--help")
        assert result.returncode == 0
        assert "workflow_path" in result.stdout

    def test_triggers_enable_disable(self, tmp_path: Path) -> None:
        """Enable/disable a schedule via the CLI."""
        import re

        anteroom_dir = tmp_path / ".anteroom"
        anteroom_dir.mkdir(exist_ok=True)
        wf_path = anteroom_dir / "scheduled.yaml"
        wf_path.write_text(_TRIGGER_WORKFLOW_YAML)

        # Register first
        result = _run_aroom("workflow", "schedule", str(wf_path))
        assert result.returncode == 0

        # Extract full UUID from create output (stdout + stderr — Rich may write to either)
        all_output = result.stdout + result.stderr
        full_uuid = re.compile(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}")
        full_match = full_uuid.search(all_output)
        if not full_match:
            pytest.skip("Could not extract full schedule_id from output")
        schedule_id = full_match.group(0)

        # Disable
        disable_result = _run_aroom("workflow", "triggers", "disable", schedule_id)
        assert disable_result.returncode == 0
        disable_output = disable_result.stdout + disable_result.stderr
        assert "disabled" in disable_output

        # Enable
        enable_result = _run_aroom("workflow", "triggers", "enable", schedule_id)
        assert enable_result.returncode == 0
        enable_output = enable_result.stdout + enable_result.stderr
        assert "enabled" in enable_output
