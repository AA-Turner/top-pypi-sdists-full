"""CLI integration tests for approve, deny, and respond commands."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

_PYTHON = sys.executable

_HUMAN_GATE_WORKFLOW = """\
kind: workflow
id: test_hitl
version: 0.1.0
inputs: {}
steps:
  - id: prepare
    type: runner
    runner: shell
    command: "echo prepared"
    timeout: 10
  - id: review_gate
    type: human_gate
    prompt: "Approve the prepared output?"
    options:
      - id: approve
        label: Approve
        outcome: continue
      - id: reject
        label: Reject
        outcome: stop
        stop_reason: operator_rejected
  - id: finalize
    type: runner
    runner: shell
    command: "echo finalized"
    timeout: 10
"""

# Helper to set run status via DB
_SET_STATUS_SCRIPT = """\
import sys
from anteroom.config import _resolve_data_dir
from anteroom.db import get_db
from anteroom.services.workflow_storage import update_workflow_run
db = get_db(_resolve_data_dir() / "chat.db")
run_id = sys.argv[1]
status = sys.argv[2]
update_workflow_run(db, run_id, status=status)
print(f"SET:{run_id}:{status}")
"""


@pytest.fixture(autouse=True)
def _isolated_home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch):
    anteroom_dir = tmp_path / ".anteroom"
    anteroom_dir.mkdir()
    config_file = anteroom_dir / "config.yaml"
    # Identity block is required post-#1441 so `aroom workflow respond`
    # can derive the bearer token that routes the decision through the
    # local server (#1444).  PEM strings here are placeholders — they
    # act as HMAC key material, never parsed as real keys.
    config_file.write_text(
        "ai:\n"
        '  base_url: "http://localhost:1/v1"\n'
        '  api_key: "test"\n'
        '  model: "test"\n'
        "identity:\n"
        '  user_id: "00000000-0000-4000-8000-000000000000"\n'
        '  display_name: "Test User"\n'
        '  public_key: "-----BEGIN PUBLIC KEY-----\\ntest-public-key\\n-----END PUBLIC KEY-----\\n"\n'
        '  private_key: "-----BEGIN PRIVATE KEY-----\\ntest-private-key\\n-----END PRIVATE KEY-----\\n"\n'
    )
    monkeypatch.setenv("HOME", str(tmp_path))
    yield


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


class TestApproveDenyHelp:
    def test_approve_help(self) -> None:
        result = _run_aroom("workflow", "approve", "--help")
        assert result.returncode == 0
        assert "run_id" in result.stdout

    def test_deny_help(self) -> None:
        result = _run_aroom("workflow", "deny", "--help")
        assert result.returncode == 0
        assert "--reason" in result.stdout

    def test_respond_help(self) -> None:
        result = _run_aroom("workflow", "respond", "--help")
        assert result.returncode == 0
        assert "--option" in result.stdout


class TestApproveDenyErrors:
    def test_approve_nonexistent(self) -> None:
        result = _run_aroom("workflow", "approve", "nonexistent-id")
        output = result.stdout + result.stderr
        assert "not found" in output.lower() or "Error" in output

    def test_deny_nonexistent(self) -> None:
        result = _run_aroom("workflow", "deny", "nonexistent-id")
        output = result.stdout + result.stderr
        assert "not found" in output.lower() or "Error" in output

    def test_respond_nonexistent(self) -> None:
        result = _run_aroom("workflow", "respond", "nonexistent-id")
        output = result.stdout + result.stderr
        assert "not found" in output.lower() or "Error" in output


class TestRespondSuccessPath:
    """Real human_gate workflow: run → pauses → respond → resume → completes."""

    @pytest.fixture()
    def workflow_file(self, tmp_path: Path) -> Path:
        wf = tmp_path / "test_hitl.yaml"
        wf.write_text(_HUMAN_GATE_WORKFLOW)
        return wf

    def test_respond_approve_then_resume_completes(self, workflow_file: Path) -> None:
        """Run → human_gate pauses → respond approve → resume → completed."""
        # 1. Run the workflow (should pause at human_gate)
        run_result = _run_aroom("workflow", "run", str(workflow_file), timeout=30)
        output = run_result.stdout + run_result.stderr
        run_id = _extract_run_id(output)
        assert run_id, f"No run ID: {output}"
        assert "waiting_for_input" in output.lower() or "human decision" in output.lower()

        # 2. Respond with approve option
        respond_result = _run_aroom("workflow", "respond", run_id, "--option", "approve")
        respond_output = respond_result.stdout + respond_result.stderr
        assert "Decision recorded" in respond_output or "approve" in respond_output.lower()

        # 3. Resume
        resume_result = _run_aroom(
            "workflow",
            "resume",
            run_id,
            "--definition",
            str(workflow_file),
            timeout=30,
        )
        resume_output = resume_result.stdout + resume_result.stderr
        assert "completed" in resume_output.lower()

    def test_respond_reject_then_resume_cancelled(self, workflow_file: Path) -> None:
        """Run → human_gate pauses → respond reject → resume → cancelled."""
        run_result = _run_aroom("workflow", "run", str(workflow_file), timeout=30)
        output = run_result.stdout + run_result.stderr
        run_id = _extract_run_id(output)
        assert run_id

        # Respond with reject
        _run_aroom("workflow", "respond", run_id, "--option", "reject")

        # Resume — should be cancelled
        resume_result = _run_aroom(
            "workflow",
            "resume",
            run_id,
            "--definition",
            str(workflow_file),
            timeout=30,
        )
        resume_output = resume_result.stdout + resume_result.stderr
        assert "cancelled" in resume_output.lower() or "operator_rejected" in resume_output.lower()


# Helper script that simulates a tool-approval pause:
# runs a shell workflow, then marks it as waiting_for_approval with a
# pending approval request, simulating what happens when an agent runner
# step triggers a tool approval gate.
_SIMULATE_APPROVAL_PAUSE = """\
import sys, json
from anteroom.config import _resolve_data_dir
from anteroom.db import get_db
from anteroom.services.workflow_storage import (
    update_workflow_run, create_approval_request,
    list_workflow_steps, update_workflow_step,
)
db = get_db(_resolve_data_dir() / "chat.db")
run_id = sys.argv[1]
# Mark run as waiting_for_approval
update_workflow_run(db, run_id, status="waiting_for_approval", stop_reason="Paused for approval")
# Find the last step and create an approval request for it
steps = list_workflow_steps(db, run_id)
if steps:
    step = steps[-1]
    req = create_approval_request(
        db, run_id=run_id, step_id=step["step_id"],
        tool_name="write_file", tool_args={"path": "/src/foo.py"},
        risk_tier="WRITE",
    )
    update_workflow_step(db, step["id"], approval_request_id=req["id"])
    print(f"APPROVAL_PAUSED:{run_id}:{req['id']}")
else:
    print(f"NO_STEPS:{run_id}")
"""

_SIMPLE_WORKFLOW = """\
kind: workflow
id: test_approval_cli
version: 0.1.0
inputs: {}
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo step one"
    timeout: 10
  - id: step_two
    type: runner
    runner: shell
    command: "echo step two"
    timeout: 10
"""


class TestApproveSuccessPath:
    """Simulated tool approval: run → simulate pause → approve → resume → completes."""

    @pytest.fixture()
    def simple_workflow(self, tmp_path: Path) -> Path:
        wf = tmp_path / "test_approval.yaml"
        wf.write_text(_SIMPLE_WORKFLOW)
        return wf

    def test_approve_then_resume_completes(self, simple_workflow: Path) -> None:
        """Run → simulate approval pause → approve → resume → completed."""
        # 1. Run the workflow (completes normally with shell steps)
        run_result = _run_aroom("workflow", "run", str(simple_workflow), timeout=30)
        output = run_result.stdout + run_result.stderr
        run_id = _extract_run_id(output)
        assert run_id, f"No run ID: {output}"

        # 2. Simulate approval pause via DB helper
        pause_result = _run_script(_SIMULATE_APPROVAL_PAUSE, run_id)
        assert f"APPROVAL_PAUSED:{run_id}" in pause_result.stdout, (
            f"Pause failed: {pause_result.stdout} {pause_result.stderr}"
        )

        # 3. Verify status shows waiting_for_approval
        status_result = _run_aroom("workflow", "status", run_id)
        assert "waiting_for_approval" in status_result.stdout.lower()

        # 4. Approve via real CLI
        approve_result = _run_aroom("workflow", "approve", run_id)
        approve_output = approve_result.stdout + approve_result.stderr
        assert "Approved" in approve_output or "approved" in approve_output.lower()

        # 5. Resume via real CLI
        resume_result = _run_aroom(
            "workflow",
            "resume",
            run_id,
            "--definition",
            str(simple_workflow),
            timeout=30,
        )
        resume_output = resume_result.stdout + resume_result.stderr
        assert "completed" in resume_output.lower(), f"Expected completed: {resume_output}"

    def test_deny_moves_to_paused(self, simple_workflow: Path) -> None:
        """Run → simulate approval pause → deny → run moves to paused."""
        run_result = _run_aroom("workflow", "run", str(simple_workflow), timeout=30)
        output = run_result.stdout + run_result.stderr
        run_id = _extract_run_id(output)
        assert run_id

        _run_script(_SIMULATE_APPROVAL_PAUSE, run_id)

        # Deny
        deny_result = _run_aroom("workflow", "deny", run_id)
        deny_output = deny_result.stdout + deny_result.stderr
        assert "Denied" in deny_output or "denied" in deny_output.lower()

        # Verify status shows paused (deny moves from waiting_for_approval to paused)
        status_result = _run_aroom("workflow", "status", run_id)
        assert "paused" in status_result.stdout.lower()
