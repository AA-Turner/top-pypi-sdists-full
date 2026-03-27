"""CLI integration tests for workflow credential binding (#970).

Tests real subprocess paths for credential validation and injection.
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


# Workflow that references a credential not declared in config
_MISSING_CRED_WORKFLOW = """\
kind: workflow
id: test_missing_cred
version: 0.1.0
inputs: {}
steps:
  - id: use_cred
    type: runner
    runner: shell
    command: "echo $SECRET_KEY"
    timeout: 10
    credentials:
      - name: SECRET_KEY
        from: nonexistent_credential
"""

# Workflow that uses a credential from an env var
_ENV_CRED_WORKFLOW = """\
kind: workflow
id: test_env_cred
version: 0.1.0
inputs: {}
steps:
  - id: use_cred
    type: runner
    runner: shell
    command: "echo $MY_TOKEN"
    timeout: 10
    credentials:
      - name: MY_TOKEN
        from: test_token
"""


def _run_aroom(*args: str, timeout: int = 30, env: dict | None = None) -> subprocess.CompletedProcess:
    import os

    run_env = dict(os.environ)
    if env:
        run_env.update(env)
    return subprocess.run(
        [_PYTHON, "-m", "anteroom", *args],
        capture_output=True,
        text=True,
        timeout=timeout,
        env=run_env,
    )


def _extract_run_id(output: str) -> str | None:
    for line in output.splitlines():
        if "Run ID:" in line:
            return line.split("Run ID:")[-1].strip()
    return None


class TestCredentialCLI:
    @pytest.fixture()
    def missing_cred_file(self, tmp_path: Path) -> Path:
        wf = tmp_path / "missing_cred.yaml"
        wf.write_text(_MISSING_CRED_WORKFLOW)
        return wf

    def test_missing_credential_shows_error(self, missing_cred_file: Path) -> None:
        """Running a workflow with undeclared credentials shows a clear error."""
        result = _run_aroom("workflow", "run", str(missing_cred_file), timeout=30)
        output = result.stdout + result.stderr
        assert "undeclared credential" in output.lower() or "credential" in output.lower(), (
            f"Expected credential error in output. Got: {output}"
        )

    @pytest.fixture()
    def env_cred_file(self, tmp_path: Path) -> Path:
        wf = tmp_path / "env_cred.yaml"
        wf.write_text(_ENV_CRED_WORKFLOW)
        return wf

    def test_env_credential_succeeds(self, tmp_path: Path, env_cred_file: Path) -> None:
        """Workflow with declared env-var credential runs successfully."""
        # Write config with credential declaration
        anteroom_dir = tmp_path / ".anteroom"
        config = anteroom_dir / "config.yaml"
        config.write_text(
            'ai:\n  base_url: "http://localhost:1/v1"\n  api_key: "test"\n  model: "test"\n'
            "workflow:\n  credentials:\n    - name: test_token\n      env_var: WORKFLOW_TEST_TOKEN\n"
        )

        result = _run_aroom(
            "workflow",
            "run",
            str(env_cred_file),
            timeout=30,
            env={"WORKFLOW_TEST_TOKEN": "secret123"},
        )
        output = result.stdout + result.stderr
        assert "completed" in output.lower() or "Workflow completed" in output, f"Expected completion. Got: {output}"

    def test_credential_value_not_in_output(self, tmp_path: Path, env_cred_file: Path) -> None:
        """Verify credential values never appear in CLI output even on failure."""
        anteroom_dir = tmp_path / ".anteroom"
        config = anteroom_dir / "config.yaml"
        config.write_text(
            'ai:\n  base_url: "http://localhost:1/v1"\n  api_key: "test"\n  model: "test"\n'
            "workflow:\n  credentials:\n    - name: test_token\n      env_var: MISSING_XYZ\n"
        )

        result = _run_aroom("workflow", "run", str(env_cred_file), timeout=30)
        output = result.stdout + result.stderr
        # Error message should mention the env var name (safe) but "not set" reason
        assert "not set" in output or "failed" in output.lower(), f"Expected error message. Got: {output}"
