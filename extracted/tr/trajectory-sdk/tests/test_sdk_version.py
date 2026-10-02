import json
import os
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "sdk_version.py"


@pytest.fixture
def project(tmp_path: Path) -> Path:
  (tmp_path / "scripts").mkdir()
  shutil.copyfile(SCRIPT, tmp_path / "scripts" / SCRIPT.name)
  return tmp_path


def write_project(project: Path, version: str) -> None:
  (project / "pyproject.toml").write_text(
    '[project]\nname = "trajectory-sdk"\n'
    f"version = {json.dumps(version)}\n"
    'requires-python = ">=3.11"\n'
  )


def run(project: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
  return subprocess.run(
    [
      "uv",
      "run",
      "--no-project",
      "--offline",
      "--python",
      sys.executable,
      "python",
      "scripts/sdk_version.py",
      *arguments,
    ],
    cwd=project,
    env={**os.environ, "UV_OFFLINE": "1", "UV_PYTHON_DOWNLOADS": "never"},
    capture_output=True,
    text=True,
    check=False,
  )


@pytest.mark.parametrize("version", ["0.7.21", "0.7.99", "0.8.10", "1.0.10"])
def test_release_check_accepts_actual_two_digit_patch_versions(project: Path, version: str) -> None:
  write_project(project, version)
  result = run(project, "check")
  assert result.returncode == 0
  assert result.stdout.strip() == version
  assert not (project / ".venv").exists()


@pytest.mark.parametrize(
  "version",
  [
    "0.7.2",
    "0.7.0",
    "0.7.100",
    "0.7.02",
    "0.7.011",
    "00.7.11",
    "0.07.11",
    "0.7.11rc1",
    "0.7.11+local",
    "v0.7.11",
    "0.7",
  ],
)
def test_release_check_rejects_padding_and_out_of_policy_versions(
  project: Path, version: str
) -> None:
  write_project(project, version)
  before = (project / "pyproject.toml").read_bytes()
  result = run(project, "check")
  assert result.returncode != 0
  assert "error:" in result.stderr
  assert (project / "pyproject.toml").read_bytes() == before
  assert not (project / "uv.lock").exists()


@pytest.mark.parametrize(
  "version,arguments,expected",
  [
    ("0.7.2", (), "0.7.10"),
    ("0.7.10", (), "0.7.11"),
    ("0.7.98", (), "0.7.99"),
    ("0.7.99", (), "0.8.10"),
    ("9.99.99", (), "9.100.10"),
    ("0.7.21", ("--part", "minor"), "0.8.10"),
    ("0.7.21", ("--part", "major"), "1.0.10"),
  ],
)
def test_bump_updates_real_project_and_lock_without_syncing_environment(
  project: Path, version: str, arguments: tuple[str, ...], expected: str
) -> None:
  write_project(project, version)
  result = run(project, "bump", *arguments)
  assert result.returncode == 0, result.stderr
  metadata = tomllib.loads((project / "pyproject.toml").read_text())
  locked = tomllib.loads((project / "uv.lock").read_text())
  assert metadata["project"]["version"] == expected
  assert [
    package["version"] for package in locked["package"] if package["name"] == "trajectory-sdk"
  ] == [expected]
  assert run(project, "check").stdout.strip() == expected
  assert not (project / ".venv").exists()


@pytest.mark.parametrize("version", ["0.7.100", "0.7.02", "0.7.11rc1"])
def test_bump_rejects_invalid_source_version_before_writing(project: Path, version: str) -> None:
  write_project(project, version)
  before = (project / "pyproject.toml").read_bytes()
  result = run(project, "bump")
  assert result.returncode != 0
  assert (project / "pyproject.toml").read_bytes() == before
  assert not (project / "uv.lock").exists()
