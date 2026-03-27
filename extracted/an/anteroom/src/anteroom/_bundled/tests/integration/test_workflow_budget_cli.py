"""CLI integration tests for workflow budget enforcement (#967).

Tests real subprocess paths for:
- workflow run renders budget-exceeded output
- workflow status shows budget usage
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


# Workflow with max_steps: 1 but 2 steps — second step should trigger budget exceeded.
_BUDGET_EXCEEDED_WORKFLOW = """\
kind: workflow
id: test_budget_cli
version: 0.1.0
inputs: {}
policies:
  budget:
    max_steps: 1
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo step one"
    timeout: 10
  - id: step_two
    type: runner
    runner: shell
    command: "echo step two should not run"
    timeout: 10
"""

# Workflow with a generous budget that completes normally.
_BUDGET_OK_WORKFLOW = """\
kind: workflow
id: test_budget_ok
version: 0.1.0
inputs: {}
policies:
  budget:
    max_steps: 10
    max_tokens: 100000
steps:
  - id: step_one
    type: runner
    runner: shell
    command: "echo step one"
    timeout: 10
"""


def _run_aroom(*args: str, timeout: int = 30) -> subprocess.CompletedProcess:
    return subprocess.run(
        [_PYTHON, "-m", "anteroom", *args],
        capture_output=True,
        text=True,
        timeout=timeout,
    )


def _extract_run_id(output: str) -> str | None:
    for line in output.splitlines():
        if "Run ID:" in line:
            return line.split("Run ID:")[-1].strip()
    return None


class TestBudgetExceededCLI:
    @pytest.fixture()
    def budget_exceeded_file(self, tmp_path: Path) -> Path:
        wf = tmp_path / "budget_exceeded.yaml"
        wf.write_text(_BUDGET_EXCEEDED_WORKFLOW)
        return wf

    def test_run_renders_budget_exceeded(self, budget_exceeded_file: Path) -> None:
        """Running a workflow that exceeds step budget shows budget-exceeded output."""
        result = _run_aroom("workflow", "run", str(budget_exceeded_file), timeout=30)
        output = result.stdout + result.stderr
        # The CLI should show budget exceeded in the progress output
        assert "budget" in output.lower() or "Budget exceeded" in output, (
            f"Expected budget-exceeded message in output. Got: {output}"
        )

    def test_status_shows_budget_exceeded_reason(self, budget_exceeded_file: Path) -> None:
        """After budget exceeded, status shows the stop reason."""
        run_result = _run_aroom("workflow", "run", str(budget_exceeded_file), timeout=30)
        output = run_result.stdout + run_result.stderr
        run_id = _extract_run_id(output)
        assert run_id, f"No run ID found: {output}"

        status_result = _run_aroom("workflow", "status", run_id)
        status_output = status_result.stdout
        assert "budget_exceeded" in status_output, (
            f"Expected 'budget_exceeded' in status stop_reason. Got: {status_output}"
        )


class TestBudgetDisplayCLI:
    @pytest.fixture()
    def budget_ok_file(self, tmp_path: Path) -> Path:
        wf = tmp_path / "budget_ok.yaml"
        wf.write_text(_BUDGET_OK_WORKFLOW)
        return wf

    def test_status_shows_budget_usage(self, budget_ok_file: Path) -> None:
        """After a successful run with budget, status shows budget usage."""
        run_result = _run_aroom("workflow", "run", str(budget_ok_file), timeout=30)
        output = run_result.stdout + run_result.stderr
        run_id = _extract_run_id(output)
        assert run_id, f"No run ID found: {output}"

        status_result = _run_aroom("workflow", "status", run_id)
        status_output = status_result.stdout
        assert "Budget:" in status_output, f"Expected 'Budget:' in status output. Got: {status_output}"
        # Should show step count usage
        assert "steps" in status_output.lower(), f"Expected step count in budget display. Got: {status_output}"
