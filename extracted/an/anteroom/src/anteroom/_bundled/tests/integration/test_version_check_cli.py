from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

from anteroom import __version__


def _env_with_config(tmp_path: Path) -> dict[str, str]:
    home = tmp_path / "home"
    anteroom_dir = home / ".anteroom"
    anteroom_dir.mkdir(parents=True)
    (anteroom_dir / "config.yaml").write_text(
        'ai:\n  base_url: "http://127.0.0.1:9"\n  api_key: "test"\n  model: "test"\n',
        encoding="utf-8",
    )
    return {**os.environ, "HOME": str(home)}


def _run_version_check(tmp_path: Path, command: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "anteroom", "version", "check", "--command", command],
        capture_output=True,
        text=True,
        timeout=15,
        env=_env_with_config(tmp_path),
    )


def test_version_check_command_reports_update_available(tmp_path: Path) -> None:
    result = _run_version_check(tmp_path, "printf '999.0.0\\n'")

    assert result.returncode == 0
    assert f"Current version: {__version__}" in result.stdout
    assert "Check source: custom command" in result.stdout
    assert f"Update available: {__version__} -> 999.0.0" in result.stdout


def test_version_check_command_reports_current(tmp_path: Path) -> None:
    result = _run_version_check(tmp_path, f"printf '{__version__}\\n'")

    assert result.returncode == 0
    assert f"Anteroom is up to date: {__version__}" in result.stdout


def test_version_check_command_reports_not_newer(tmp_path: Path) -> None:
    result = _run_version_check(tmp_path, "printf '0.0.1\\n'")

    assert result.returncode == 0
    assert "No newer version available: latest checked version is 0.0.1" in result.stdout


def test_version_check_command_reports_unavailable_for_invalid_output(tmp_path: Path) -> None:
    result = _run_version_check(tmp_path, "printf 'not-a-version\\n'")

    assert result.returncode == 1
    assert "Unable to check for updates" in result.stderr
    assert "up to date" not in result.stdout.lower()


def test_version_check_command_reports_unavailable_for_nonzero_command(tmp_path: Path) -> None:
    result = _run_version_check(tmp_path, "sh -c 'exit 2'")

    assert result.returncode == 1
    assert "checker exited non-zero" in result.stderr
    assert "up to date" not in result.stdout.lower()
