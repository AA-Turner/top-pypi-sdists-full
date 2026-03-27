"""CLI integration tests for definition drift detection (#964).

Tests real subprocess paths for:
- resume blocked on definition drift
- resume --force overrides drift block
- status shows definition hash
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

_PYTHON = sys.executable


@pytest.fixture(autouse=True)
def _isolated_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    anteroom_dir = tmp_path / ".anteroom"
    anteroom_dir.mkdir()
    config_file = anteroom_dir / "config.yaml"
    config_file.write_text('ai:\n  base_url: "http://localhost:1/v1"\n  api_key: "test"\n  model: "test"\n')
    monkeypatch.setenv("HOME", str(tmp_path))
    yield


_ORIGINAL_WORKFLOW = """\
kind: workflow
id: test_drift_cli
version: 0.1.0
inputs: {}
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo original step one"
    timeout: 10
  - id: step_two
    type: runner
    runner: shell
    command: "echo original step two"
    timeout: 10
"""

_MODIFIED_WORKFLOW = """\
kind: workflow
id: test_drift_cli
version: 0.1.0
inputs: {}
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo MODIFIED step one"
    timeout: 10
  - id: step_three
    type: runner
    runner: shell
    command: "echo brand new step three"
    timeout: 10
"""

# Helper script: mark a completed run as paused to simulate a crash.
_PAUSE_RUN_SCRIPT = """\
import sys
from anteroom.config import _resolve_data_dir
from anteroom.db import get_db
from anteroom.services.workflow_storage import update_workflow_run

db = get_db(_resolve_data_dir() / "chat.db")
run_id = sys.argv[1]
update_workflow_run(db, run_id, status="paused", stop_reason="test_simulated_crash")
print(f"PAUSED:{run_id}")
"""


def _run_aroom(*args: str, timeout: int = 30) -> subprocess.CompletedProcess:
    return subprocess.run(
        [_PYTHON, "-m", "anteroom", *args],
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def _run_script(script: str, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [_PYTHON, "-c", script, *args],
        capture_output=True,
        text=True,
        timeout=15,
    )


def _extract_run_id(output: str) -> str | None:
    for line in output.splitlines():
        if "Run ID:" in line:
            return line.split("Run ID:")[-1].strip()
    return None


class TestDefinitionDriftCLI:
    @pytest.fixture()
    def original_file(self, tmp_path: Path) -> Path:
        wf = tmp_path / "drift_workflow.yaml"
        wf.write_text(_ORIGINAL_WORKFLOW)
        return wf

    @pytest.fixture()
    def modified_file(self, tmp_path: Path) -> Path:
        wf = tmp_path / "drift_workflow_modified.yaml"
        wf.write_text(_MODIFIED_WORKFLOW)
        return wf

    def test_resume_blocked_on_drift(self, original_file: Path, modified_file: Path) -> None:
        """Run with original → pause → resume with modified definition → blocked."""
        # 1. Run the original workflow
        run_result = _run_aroom("workflow", "run", str(original_file), timeout=30)
        output = run_result.stdout + run_result.stderr
        run_id = _extract_run_id(output)
        assert run_id, f"No run ID found in output: {output}"

        # 2. Mark as paused (simulates crash)
        pause_result = _run_script(_PAUSE_RUN_SCRIPT, run_id)
        assert f"PAUSED:{run_id}" in pause_result.stdout

        # 3. Resume with modified definition — should be blocked
        resume_result = _run_aroom(
            "workflow",
            "resume",
            run_id,
            "--definition",
            str(modified_file),
            timeout=30,
        )
        resume_output = resume_result.stdout + resume_result.stderr
        assert "Definition has changed" in resume_output or "hash mismatch" in resume_output, (
            f"Expected drift block message. Got: {resume_output}"
        )

    def test_resume_force_overrides_drift(self, original_file: Path, modified_file: Path) -> None:
        """Run with original → pause → resume --force with modified → succeeds."""
        # 1. Run the original workflow
        run_result = _run_aroom("workflow", "run", str(original_file), timeout=30)
        output = run_result.stdout + run_result.stderr
        run_id = _extract_run_id(output)
        assert run_id, f"No run ID found in output: {output}"

        # 2. Mark as paused
        pause_result = _run_script(_PAUSE_RUN_SCRIPT, run_id)
        assert f"PAUSED:{run_id}" in pause_result.stdout

        # 3. Resume with --force and modified definition — should succeed
        resume_result = _run_aroom(
            "workflow",
            "resume",
            run_id,
            "--definition",
            str(modified_file),
            "--force",
            timeout=30,
        )
        resume_output = resume_result.stdout + resume_result.stderr
        assert "completed" in resume_output.lower() or "Workflow completed" in resume_output, (
            f"Expected completion after --force. Got: {resume_output}"
        )

    def test_status_shows_definition_hash(self, original_file: Path) -> None:
        """After running, status output includes the definition hash."""
        # Run the workflow
        run_result = _run_aroom("workflow", "run", str(original_file), timeout=30)
        output = run_result.stdout + run_result.stderr
        run_id = _extract_run_id(output)
        assert run_id, f"No run ID found: {output}"

        # Check status output
        status_result = _run_aroom("workflow", "status", run_id)
        status_output = status_result.stdout
        assert "Definition hash:" in status_output, (
            f"Expected 'Definition hash:' in status output. Got: {status_output}"
        )

    def test_resume_help_shows_force_flag(self) -> None:
        """The --force flag appears in resume help text."""
        result = _run_aroom("workflow", "resume", "--help")
        assert "--force" in result.stdout
