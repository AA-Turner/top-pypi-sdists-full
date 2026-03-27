"""CLI integration tests for workflow checkpoint and idempotency visibility (#977, #979).

Tests that `aroom workflow status` and `aroom workflow history` display
checkpoint information and idempotency keys when present.
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


_TEST_WORKFLOW_YAML = """\
kind: workflow
id: test_checkpoint_cli
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


class TestCheckpointCLIVisibility:
    @pytest.fixture()
    def workflow_file(self, tmp_path: Path) -> Path:
        wf = tmp_path / "test_checkpoint.yaml"
        wf.write_text(_TEST_WORKFLOW_YAML)
        return wf

    def test_status_shows_checkpoint_count(self, workflow_file: Path) -> None:
        """After running a workflow, `status` output includes checkpoint count."""
        run_result = _run_aroom("workflow", "run", str(workflow_file), timeout=30)
        run_output = run_result.stdout + run_result.stderr
        run_id = _extract_run_id(run_output)
        assert run_id is not None, f"Could not extract run ID from output: {run_output}"

        status_result = _run_aroom("workflow", "status", run_id)
        status_output = status_result.stdout
        assert status_result.returncode == 0
        assert "Checkpoint" in status_output, f"'Checkpoint' not found in status output: {status_output}"

    def test_history_shows_checkpoints(self, workflow_file: Path) -> None:
        """After running a workflow, `history` output lists checkpoint labels."""
        run_result = _run_aroom("workflow", "run", str(workflow_file), timeout=30)
        run_output = run_result.stdout + run_result.stderr
        run_id = _extract_run_id(run_output)
        assert run_id is not None, f"Could not extract run ID from output: {run_output}"

        history_result = _run_aroom("workflow", "history", run_id)
        history_output = history_result.stdout
        assert history_result.returncode == 0
        assert "after:" in history_output, f"'after:' checkpoint label not found in history output: {history_output}"

    def test_history_shows_idempotency_key_for_publish(self, tmp_path: Path) -> None:
        """After a workflow with a publish step, `history` shows idempotency key."""
        output_file = tmp_path / "published.txt"
        wf_yaml = f"""\
kind: workflow
id: test_idem_cli
version: 0.1.0
inputs: {{}}
steps:
  - id: make_content
    type: runner
    runner: shell
    command: "echo hello"
    timeout: 10
  - id: publish_file
    type: publish
    destination:
      adapter: file
      path: "{output_file}"
    context_from:
      - step: make_content
        field: result_summary
"""
        wf_file = tmp_path / "test_idem.yaml"
        wf_file.write_text(wf_yaml)

        run_result = _run_aroom("workflow", "run", str(wf_file), timeout=30)
        run_output = run_result.stdout + run_result.stderr
        run_id = _extract_run_id(run_output)
        assert run_id is not None, f"Could not extract run ID from output: {run_output}"

        history_result = _run_aroom("workflow", "history", run_id)
        history_output = history_result.stdout
        assert history_result.returncode == 0, f"history failed: {history_result.stderr}"
        # The idempotency key is run_id:step_id by default
        assert "publish_file" in history_output, f"publish step not in history: {history_output}"
        # The Idem. Key column shows the key (may be truncated by Rich table)
        # Check that the key prefix (first 5 chars of run_id) appears in the output
        key_prefix = run_id[:5]
        assert key_prefix in history_output, (
            f"Idempotency key prefix '{key_prefix}' not found in history output: {history_output}"
        )
        # Also verify the "Idem." column header is present
        assert "Idem." in history_output, f"'Idem.' column header not in history: {history_output}"
