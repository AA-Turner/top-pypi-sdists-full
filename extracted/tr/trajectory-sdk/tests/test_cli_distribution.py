from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.mark.skipif(sys.platform != "darwin", reason="Uses the macOS script utility")
@pytest.mark.parametrize("exit_code", [0, 7])
def test_macos_claude_handoff_has_terminal_streams_and_preserves_exit_status(
  tmp_path: Path, exit_code: int
) -> None:
  project = tmp_path / "project with spaces"
  project.mkdir()
  executable = tmp_path / "claude"
  executable.write_text(
    f"#!{sys.executable}\n"
    "import json, os, sys\n"
    "from pathlib import Path\n"
    "Path('invocation.json').write_text(json.dumps({"
    "'tty': [os.isatty(fd) for fd in range(3)], 'args': sys.argv[1:]}))\n"
    f"raise SystemExit({exit_code})\n"
  )
  executable.chmod(0o755)
  environment = dict(os.environ)
  for name in ("TRAJECTORY_API_KEY", "TRAJECTORY_PROFILE", "TRAJECTORY_BASE_URL"):
    environment.pop(name, None)
  environment["TRAJECTORY_CONFIG_HOME"] = str(tmp_path / "auth")
  environment["PATH"] = str(tmp_path) + os.pathsep + environment.get("PATH", "")
  result = subprocess.run(
    [
      sys.executable,
      "-c",
      "from pathlib import Path; from trajectory.lib.cli.assistants import handoff; "
      "result = handoff('claude', Path.cwd(), 'benchmark', "
      "'Literal $(touch unexpected) `touch unexpected`', None, None, True); "
      "raise SystemExit(result['exit_code'])",
    ],
    cwd=project,
    input="",
    capture_output=True,
    text=True,
    env=environment,
    timeout=15,
    check=False,
  )
  assert result.returncode == exit_code, result.stderr
  invocation = json.loads((project / "invocation.json").read_text())
  assert invocation["tty"] == [True, True, True]
  assert len(invocation["args"]) == 1
  assert "Literal $(touch unexpected) `touch unexpected`" in invocation["args"][0]
  assert not (project / "unexpected").exists()


def test_sdk_import_does_not_load_terminal_dependencies(tmp_path: Path) -> None:
  environment = dict(os.environ)
  environment["TRAJECTORY_CONFIG_HOME"] = str(tmp_path)
  result = subprocess.run(
    [sys.executable, "-c", "import sys; import trajectory; assert 'textual' not in sys.modules"],
    capture_output=True,
    text=True,
    env=environment,
    check=False,
  )
  assert result.returncode == 0, result.stderr


@pytest.mark.parametrize("command", ["tj", "trajectory"])
def test_cli_help_works_outside_a_project(tmp_path: Path, command: str) -> None:
  result = subprocess.run(
    [str(Path(sys.executable).parent / command), "--help"],
    cwd=tmp_path,
    capture_output=True,
    text=True,
    check=False,
  )
  assert result.returncode == 0, result.stderr
  assert "usage: tj " in result.stdout
  assert "login" in result.stdout
  assert "training" in result.stdout


def test_cli_schema_is_machine_readable_without_authentication(tmp_path: Path) -> None:
  environment = dict(os.environ)
  environment.pop("TRAJECTORY_API_KEY", None)
  environment["TRAJECTORY_CONFIG_HOME"] = str(tmp_path)
  result = subprocess.run(
    [sys.executable, "-m", "trajectory.lib.cli.main", "schema", "--json"],
    cwd=tmp_path,
    env=environment,
    capture_output=True,
    text=True,
    check=False,
  )
  assert result.returncode == 0, result.stderr
  assert isinstance(json.loads(result.stdout), dict)
  assert "Traceback" not in result.stderr


@pytest.mark.parametrize(
  ("topic", "expected_content"),
  [("onboarding", "tj benchmarks push"), ("skill", "tj whoami --json")],
)
def test_cli_reads_bundled_guides_without_network(
  tmp_path: Path, topic: str, expected_content: str
) -> None:
  result = subprocess.run(
    [sys.executable, "-m", "trajectory.lib.cli.main", "docs", "--topic", topic, "--json"],
    cwd=tmp_path,
    capture_output=True,
    text=True,
    check=False,
  )
  assert result.returncode == 0, result.stderr
  document = json.loads(result.stdout)
  assert Path(document["path"]).is_file()
  assert expected_content in document["content"]


@pytest.mark.parametrize(
  ("arguments", "interactive", "exit_code", "message"),
  [
    (["schema", "--json"], False, 0, '"commands"'),
    (["--help"], False, 0, "usage: tj"),
    (["init"], True, 1, "missing_dependency"),
  ],
)
@pytest.mark.parametrize("missing_package", ["textual", "rich"])
def test_cli_without_optional_terminal_package(
  tmp_path: Path,
  arguments: list[str],
  interactive: bool,
  exit_code: int,
  message: str,
  missing_package: str,
) -> None:
  script = "\n".join(
    [
      "import sys",
      f"sys.modules[{missing_package!r}] = None",
      "from trajectory.lib.cli.main import CLI",
      "from unittest.mock import patch",
      "with patch('sys.stdin.isatty', return_value=" + repr(interactive) + "), "
      "patch('sys.stdout.isatty', return_value=" + repr(interactive) + "), "
      "patch('sys.stderr.isatty', return_value=" + repr(interactive) + "):",
      "  raise SystemExit(CLI.run(" + repr(arguments) + "))",
    ]
  )
  environment = dict(os.environ, TRAJECTORY_API_KEY="test-key")
  result = subprocess.run(
    [sys.executable, "-c", script],
    cwd=tmp_path,
    env=environment,
    capture_output=True,
    text=True,
    check=False,
  )
  assert result.returncode == exit_code, result.stderr
  assert message in result.stdout + result.stderr
  assert "Traceback" not in result.stderr
