import importlib.util
import os
import subprocess
import sys
import tomllib

from pathlib import Path
from unittest import mock

import pytest


PYPROJECT_PATH = Path(__file__).resolve().parents[2] / "pyproject.toml"
INSTALL_SCRIPT_PATH = Path(__file__).resolve().parents[2] / "scripts" / "install_universal_driver.py"

_spec = importlib.util.spec_from_file_location("install_universal_driver", INSTALL_SCRIPT_PATH)
if _spec is None or _spec.loader is None:
    raise ImportError(f"Could not load module spec from {INSTALL_SCRIPT_PATH}")
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

install_universal_driver = _mod.install_universal_driver
main = _mod.main
validate_ref = _mod.validate_ref


def test_pyproject_toml_no_env_interpolation_in_ud():
    """Verify pyproject.toml does not use unsafe {env:...} interpolation in the ud environment."""
    with open(PYPROJECT_PATH, "rb") as f:
        config = tomllib.load(f)

    ud_scripts = config["tool"]["hatch"]["envs"]["ud"]["scripts"]["check"]
    assert "python scripts/install_universal_driver.py" in ud_scripts
    for script in ud_scripts:
        assert "{env:UD_BRANCH" not in script, (
            f"Vulnerable {{env:UD_BRANCH}} found in Hatch ud script: {script!r}. "
            "Branch names must be safely processed without shell interpolation."
        )


@pytest.mark.parametrize(
    "valid_ref",
    [
        "main",
        "master",
        "develop",
        "v1.0.0",
        "1.2.3",
        "release/2.0.0",
        "feature/add-support_123",
        "bugfix/fix-issue.patch",
        "refs/heads/main",
        "refs/tags/v1.0.0",
        "a",
        "0",
        "_branch",
        "branch-name",
        "4b825dc642cb6eb9a060e54bf8d69288fbee4904",
        "e788d971",
    ],
)
def test_validate_ref_valid(valid_ref: str):
    """Ensure safe and well-formed git references are accepted."""
    assert validate_ref(valid_ref) == valid_ref


@pytest.mark.parametrize(
    "invalid_ref",
    [
        # Shell injection / command chaining
        'main"; echo INJECTED; #',
        "main'; echo INJECTED; #",
        "main && id",
        "main || whoami",
        "main; uname -a",
        "main | cat /etc/passwd",
        "main > /tmp/pwn",
        "main < /dev/null",
        "main$(id)",
        "main`id`",
        "main${IFS}id",
        "main\nid",
        "main\r\nid",
        # Option / flag injection
        "-b",
        "--upload-pack=exploit",
        "--config=core.gitProxy=exploit",
        # Path traversal / invalid git ref format
        "/root/escape",
        "./relative",
        ".hidden",
        "feature/../../evil",
        "..",
        "feature//branch",
        "feature/",
        "branch.",
        "v1.0.",
        "branch.lock",
        "refs/heads/main.lock",
        # Disallowed characters
        "main*wildcard",
        "main?query",
        "main[0-9]",
        "main~1",
        "main^2",
        "main:branch",
        "main@{1}",
        "main branch",
        # Empty / whitespace
        "",
        "   ",
        # Excessively long
        "a" * 256,
    ],
)
def test_validate_ref_invalid(invalid_ref: str):
    """Ensure malicious or malformed git references are strictly rejected."""
    with pytest.raises(ValueError):
        validate_ref(invalid_ref)


def test_validate_ref_non_string():
    """Ensure non-string types raise ValueError."""
    with pytest.raises(ValueError):
        validate_ref(None)  # type: ignore[arg-type]
    with pytest.raises(ValueError):
        validate_ref(123)  # type: ignore[arg-type]


def test_install_universal_driver_default():
    """Verify default installation uses 'main' branch when UD_BRANCH is not set."""
    with mock.patch("os.environ.get", return_value=""), mock.patch("subprocess.run") as mock_run:
        install_universal_driver()
        mock_run.assert_called_once_with(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "git+https://github.com/snowflakedb/drivers@main#subdirectory=python",
            ],
            check=True,
        )


def test_install_universal_driver_explicit_ref():
    """Verify installation with an explicitly passed ref."""
    with mock.patch("subprocess.run") as mock_run:
        install_universal_driver("feature/test-branch")
        mock_run.assert_called_once_with(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "git+https://github.com/snowflakedb/drivers@feature/test-branch#subdirectory=python",
            ],
            check=True,
        )


def test_install_universal_driver_env_var(monkeypatch):
    """Verify installation reads UD_BRANCH environment variable."""
    monkeypatch.setenv("UD_BRANCH", "v1.2.3")
    with mock.patch("subprocess.run") as mock_run:
        install_universal_driver()
        mock_run.assert_called_once_with(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "git+https://github.com/snowflakedb/drivers@v1.2.3#subdirectory=python",
            ],
            check=True,
        )


def test_install_universal_driver_injection_blocked(monkeypatch):
    """Verify command injection in UD_BRANCH raises ValueError without calling subprocess.run."""
    monkeypatch.setenv("UD_BRANCH", 'main"; echo INJECTED; #')
    with mock.patch("subprocess.run") as mock_run:
        with pytest.raises(ValueError, match="Invalid git ref name"):
            install_universal_driver()
        mock_run.assert_not_called()


def test_install_universal_driver_main_cli(monkeypatch):
    """Verify CLI main entrypoint."""
    monkeypatch.setattr(sys, "argv", ["install_universal_driver.py", "custom/ref"])
    with mock.patch("subprocess.run") as mock_run:
        main()
        mock_run.assert_called_once_with(
            [
                sys.executable,
                "-m",
                "pip",
                "install",
                "git+https://github.com/snowflakedb/drivers@custom/ref#subdirectory=python",
            ],
            check=True,
        )


def test_script_execution_as_subprocess():
    """Verify running the script as a separate process blocks command injection."""
    env = dict(os.environ)
    env["UD_BRANCH"] = 'main"; echo CANARY_EXPLOIT; #'
    result = subprocess.run(
        [sys.executable, str(INSTALL_SCRIPT_PATH)],
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode != 0
    assert "Invalid git ref name" in result.stderr
    assert "CANARY_EXPLOIT" not in result.stdout
