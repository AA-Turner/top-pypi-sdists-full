"""CLI integration tests for workflow progress output.

Tests that `aroom workflow run` shows step-by-step progress with
status indicators and final summary. One-shot commands, not REPL.
"""

from __future__ import annotations

import os
import re
import signal
import subprocess
import sys
import time
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


_TEST_WORKFLOW = """\
kind: workflow
id: test_progress
version: 0.1.0
inputs: {}
steps:
  - id: first_step
    type: runner
    runner: shell
    command: "echo first step output"
    timeout: 10
  - id: second_step
    type: runner
    runner: shell
    command: "echo second step output"
    timeout: 10
"""

_FAILING_WORKFLOW = """\
kind: workflow
id: test_fail_progress
version: 0.1.0
inputs: {}
steps:
  - id: good_step
    type: runner
    runner: shell
    command: "echo good"
    timeout: 10
  - id: bad_step
    type: runner
    runner: shell
    command: "exit 1"
    timeout: 10
"""

_SLOW_WORKFLOW = """\
kind: workflow
id: test_slow_progress
version: 0.1.0
inputs: {}
steps:
  - id: slow_step
    type: runner
    runner: shell
    command: "sleep 2 && echo done"
    timeout: 10
"""


def _run_aroom(*args: str, timeout: int = 30) -> subprocess.CompletedProcess:
    return subprocess.run(
        [_PYTHON, "-m", "anteroom", *args],
        capture_output=True,
        text=True,
        timeout=timeout,
    )


class _MarkerWaiter:
    """Wait for a marker in subprocess stdout without losing output.

    The reader thread collects all lines.  After sending a signal and
    calling ``proc.communicate()``, combine ``self.collected`` with the
    remainder to get the full output.
    """

    def __init__(self, proc: subprocess.Popen, marker: str) -> None:
        import threading

        self.collected: list[str] = []
        self._found = threading.Event()
        self._proc = proc

        def _reader() -> None:
            assert proc.stdout is not None
            for line in proc.stdout:
                self.collected.append(line)
                if marker in line:
                    self._found.set()
                    return

        self._thread = threading.Thread(target=_reader, daemon=True)
        self._thread.start()

    def wait(self, timeout: float = 15.0) -> bool:
        return self._found.wait(timeout=timeout)

    def full_output(self, remainder: str) -> str:
        """Combine pre-signal output with post-communicate remainder."""
        return "".join(self.collected) + (remainder or "")


class TestProgressOutput:
    """Verify `aroom workflow run` shows step progress."""

    @pytest.fixture()
    def workflow_file(self, tmp_path: Path) -> Path:
        wf = tmp_path / "test_progress.yaml"
        wf.write_text(_TEST_WORKFLOW)
        return wf

    @pytest.fixture()
    def failing_workflow(self, tmp_path: Path) -> Path:
        wf = tmp_path / "test_fail.yaml"
        wf.write_text(_FAILING_WORKFLOW)
        return wf

    def test_shows_step_names(self, workflow_file: Path) -> None:
        """Output includes step names from the workflow definition."""
        result = _run_aroom("workflow", "run", str(workflow_file), timeout=30)
        output = result.stdout + result.stderr
        assert "first_step" in output
        assert "second_step" in output

    def test_shows_completion_status(self, workflow_file: Path) -> None:
        """Output includes completion markers for each step."""
        result = _run_aroom("workflow", "run", str(workflow_file), timeout=30)
        output = result.stdout + result.stderr
        assert "done" in output.lower() or "completed" in output.lower()

    def test_shows_final_status(self, workflow_file: Path) -> None:
        """Output ends with the final workflow status."""
        result = _run_aroom("workflow", "run", str(workflow_file), timeout=30)
        output = result.stdout + result.stderr
        assert "Workflow completed" in output or "completed" in output.lower()

    def test_shows_run_id(self, workflow_file: Path) -> None:
        """Output includes the run ID for follow-up commands."""
        result = _run_aroom("workflow", "run", str(workflow_file), timeout=30)
        output = result.stdout + result.stderr
        assert "Run ID:" in output

    def test_failed_workflow_shows_error(self, failing_workflow: Path) -> None:
        """Failed workflow shows error status and the failing step."""
        result = _run_aroom("workflow", "run", str(failing_workflow), timeout=30)
        output = result.stdout + result.stderr
        assert "failed" in output.lower()
        assert "bad_step" in output

    def test_detach_returns_run_id_and_background_run_completes(self, tmp_path: Path) -> None:
        workflow_file = tmp_path / "slow.yaml"
        workflow_file.write_text(_SLOW_WORKFLOW)

        result = _run_aroom("workflow", "run", str(workflow_file), "--detach", timeout=10)
        output = result.stdout + result.stderr
        assert result.returncode == 0
        assert "Detached" in output

        match = re.search(r"Run ID:\s*([0-9a-f-]{36})", output)
        assert match, output
        run_id = match.group(1)

        deadline = time.time() + 15
        final_status = ""
        while time.time() < deadline:
            status_result = _run_aroom("workflow", "status", run_id, timeout=10)
            final_status = status_result.stdout + status_result.stderr
            if "completed" in final_status.lower():
                break
            time.sleep(0.5)

        assert "completed" in final_status.lower(), final_status

    @pytest.mark.skipif(os.name == "nt", reason="SIGINT workflow interruption test is Unix-only")
    def test_ctrl_c_stops_cleanly_without_traceback(self, tmp_path: Path) -> None:
        workflow_file = tmp_path / "interrupt.yaml"
        workflow_file.write_text(_SLOW_WORKFLOW.replace("sleep 2", "sleep 30"))

        proc = subprocess.Popen(
            [_PYTHON, "-m", "anteroom", "workflow", "run", str(workflow_file)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        waiter = _MarkerWaiter(proc, "slow_step")
        assert waiter.wait(), "Timed out waiting for step progress"
        proc.send_signal(signal.SIGINT)
        remainder, _ = proc.communicate(timeout=15)
        output = waiter.full_output(remainder)

        # Asyncio internals on Python 3.13+ may emit teardown tracebacks
        # during SIGINT — filter those out and check for application-level ones.
        app_lines = [ln for ln in output.splitlines() if "anteroom" in ln.lower() or ln.strip().startswith("Traceback")]
        app_tracebacks = [ln for ln in app_lines if ln.strip().startswith("Traceback")]
        # Allow asyncio teardown noise; block application tracebacks
        for tb_line in app_tracebacks:
            idx = output.splitlines().index(tb_line)
            nearby = output.splitlines()[idx : idx + 5]
            assert not any("anteroom" in ln for ln in nearby), (
                f"Application traceback found in output:\n{''.join(nearby)}"
            )
        assert "Workflow interrupted." in output

        match = re.search(r"Run ID:\s*([0-9a-f-]{36})", output)
        assert match, output
        run_id = match.group(1)

        status_result = _run_aroom("workflow", "status", run_id, timeout=10)
        status_output = status_result.stdout + status_result.stderr
        assert "paused" in status_output.lower()

    @pytest.mark.skipif(os.name == "nt", reason="SIGINT workflow interruption test is Unix-only")
    def test_interrupt_shows_resume_guidance(self, tmp_path: Path) -> None:
        """Ctrl-C prints an actionable resume command with the run ID."""
        workflow_file = tmp_path / "interrupt_resume.yaml"
        workflow_file.write_text(_SLOW_WORKFLOW.replace("sleep 2", "sleep 30"))

        proc = subprocess.Popen(
            [_PYTHON, "-m", "anteroom", "workflow", "run", str(workflow_file)],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        waiter = _MarkerWaiter(proc, "slow_step")
        assert waiter.wait(), "Timed out waiting for step progress"
        proc.send_signal(signal.SIGINT)
        remainder, _ = proc.communicate(timeout=15)
        output = waiter.full_output(remainder)

        match = re.search(r"Run ID:\s*([0-9a-f-]{36})", output)
        assert match, f"No Run ID in output: {output}"
        run_id = match.group(1)

        assert f"aroom workflow resume {run_id}" in output

    def test_run_id_printed_before_step_progress(self, tmp_path: Path) -> None:
        """Run ID line appears before any step progress indicators."""
        workflow_file = tmp_path / "ordering.yaml"
        workflow_file.write_text(_SLOW_WORKFLOW)

        result = _run_aroom("workflow", "run", str(workflow_file), timeout=30)
        output = result.stdout + result.stderr

        run_id_match = re.search(r"Run ID:", output)
        assert run_id_match, f"No 'Run ID:' in output: {output}"

        # Step progress uses status icons — find the first one
        step_match = re.search(r"[✅●❌⏭🚫]", output)
        if step_match:
            assert run_id_match.start() < step_match.start(), "Run ID should appear before step progress indicators"
