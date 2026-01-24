"""CLI stories: every invocation a single beat."""

from __future__ import annotations

from collections.abc import Callable

import pytest
from click.testing import CliRunner, Result

from lib_detect_testenv import cli as cli_mod
from lib_detect_testenv import __init__conf__


@pytest.mark.os_agnostic
def test_when_cli_runs_without_arguments_check_is_run(
    cli_runner: CliRunner,
) -> None:
    """When CLI runs without arguments, the check command should run."""
    result = cli_runner.invoke(cli_mod.cli, [])

    # Should run check command (exit code 1 means not in test env in CI context)
    assert result.exit_code in (0, 1)
    # Should show test environment check output
    assert "test environment" in result.output.lower() or "detected" in result.output.lower()


@pytest.mark.os_agnostic
def test_default_shows_traceback(
    capsys: pytest.CaptureFixture[str],
    strip_ansi: Callable[[str], str],
) -> None:
    """By default (no flags), full traceback should appear on errors."""
    # Call main without any flags
    exit_code = cli_mod.main(["fail"])

    # Should return non-zero exit code
    assert exit_code != 0

    # Should show traceback in output (default behavior)
    captured = capsys.readouterr()
    output = captured.out + captured.err
    assert "Traceback" in output


@pytest.mark.os_agnostic
def test_no_traceback_flag_suppresses_traceback(
    capsys: pytest.CaptureFixture[str],
    strip_ansi: Callable[[str], str],
) -> None:
    """When --no-traceback is used, only simple error message should appear."""
    # Call main with --no-traceback flag
    exit_code = cli_mod.main(["--no-traceback", "fail"])

    # Should return non-zero exit code
    assert exit_code != 0

    # Should NOT show full traceback, just simple error
    captured = capsys.readouterr()
    output = captured.out + captured.err
    assert "Error: RuntimeError: I should fail" in output
    assert "Traceback" not in output or output.count("Traceback") == 0


@pytest.mark.os_agnostic
def test_when_hello_is_invoked_the_cli_smiles(cli_runner: CliRunner) -> None:
    """Hello command should output the canonical greeting."""
    result: Result = cli_runner.invoke(cli_mod.cli, ["hello"])

    assert result.exit_code == 0
    assert result.output == "Hello World\n"


@pytest.mark.os_agnostic
def test_when_fail_is_invoked_the_cli_raises(cli_runner: CliRunner) -> None:
    """Fail command should raise RuntimeError."""
    result: Result = cli_runner.invoke(cli_mod.cli, ["fail"])

    assert result.exit_code != 0
    assert isinstance(result.exception, RuntimeError)


@pytest.mark.os_agnostic
def test_when_info_is_invoked_the_metadata_is_displayed(cli_runner: CliRunner) -> None:
    """Info command should display package metadata."""
    result: Result = cli_runner.invoke(cli_mod.cli, ["info"])

    assert result.exit_code == 0
    assert f"Info for {__init__conf__.name}:" in result.output
    assert __init__conf__.version in result.output


@pytest.mark.os_agnostic
def test_when_an_unknown_command_is_used_a_helpful_error_appears(cli_runner: CliRunner) -> None:
    """Unknown commands should produce a helpful error message."""
    result: Result = cli_runner.invoke(cli_mod.cli, ["does-not-exist"])

    assert result.exit_code != 0
    assert "No such command" in result.output


@pytest.mark.os_agnostic
def test_main_returns_zero_on_success() -> None:
    """Main should return 0 for successful commands."""
    exit_code = cli_mod.main(["hello"])
    assert exit_code == 0


@pytest.mark.os_agnostic
def test_main_returns_nonzero_on_failure() -> None:
    """Main should return non-zero for failed commands."""
    exit_code = cli_mod.main(["fail"])
    assert exit_code != 0


@pytest.mark.os_agnostic
def test_version_option_displays_version(cli_runner: CliRunner) -> None:
    """--version should display the package version."""
    result = cli_runner.invoke(cli_mod.cli, ["--version"])

    assert result.exit_code == 0
    assert __init__conf__.version in result.output
    assert __init__conf__.shell_command in result.output


@pytest.mark.os_agnostic
def test_help_option_displays_help(cli_runner: CliRunner) -> None:
    """--help should display usage information."""
    result = cli_runner.invoke(cli_mod.cli, ["--help"])

    assert result.exit_code == 0
    assert "Usage:" in result.output
    assert "--traceback" in result.output


# ============================================================================
# Tests for test environment detection commands
# ============================================================================


@pytest.mark.os_agnostic
def test_check_command_with_pytest_args(cli_runner: CliRunner) -> None:
    """Check command should detect pytest when given pytest args."""
    result = cli_runner.invoke(cli_mod.cli, ["check", "--arg-string", "pytest.py"])

    assert result.exit_code == 0
    assert "detected" in result.output.lower()


@pytest.mark.os_agnostic
def test_check_command_without_test_env(cli_runner: CliRunner) -> None:
    """Check command should return exit code 1 when no test env detected."""
    result = cli_runner.invoke(cli_mod.cli, ["check", "--arg-string", "normal.py"])

    assert result.exit_code == 1
    assert "not detected" in result.output.lower() or "no test" in result.output.lower()


@pytest.mark.os_agnostic
def test_check_command_quiet_mode(cli_runner: CliRunner) -> None:
    """Check command with --quiet should suppress output."""
    result = cli_runner.invoke(cli_mod.cli, ["check", "--quiet", "--arg-string", "pytest.py"])

    assert result.exit_code == 0
    # Quiet mode should have minimal output
    assert result.output == "" or len(result.output.strip()) < 50


@pytest.mark.os_agnostic
def test_pytest_command_detects_pytest(cli_runner: CliRunner) -> None:
    """Pytest command should detect pytest environment."""
    result = cli_runner.invoke(cli_mod.cli, ["pytest", "--arg-string", "pytest.py"])

    assert result.exit_code == 0
    assert "pytest" in result.output.lower()
    assert "detected" in result.output.lower()


@pytest.mark.os_agnostic
def test_pytest_command_without_pytest(cli_runner: CliRunner) -> None:
    """Pytest command should return exit code 1 when pytest not detected."""
    result = cli_runner.invoke(cli_mod.cli, ["pytest", "--arg-string", "normal.py"])

    assert result.exit_code == 1
    assert "not detected" in result.output.lower()


@pytest.mark.os_agnostic
def test_pytest_command_quiet_mode(cli_runner: CliRunner) -> None:
    """Pytest command with --quiet should suppress output."""
    result = cli_runner.invoke(cli_mod.cli, ["pytest", "--quiet", "--arg-string", "pytest.py"])

    assert result.exit_code == 0
    assert result.output == "" or len(result.output.strip()) < 50


@pytest.mark.os_agnostic
def test_doctest_command_detects_doctest(cli_runner: CliRunner) -> None:
    """Doctest command should detect doctest environment."""
    result = cli_runner.invoke(cli_mod.cli, ["doctest", "--arg-string", "docrunner.py"])

    assert result.exit_code == 0
    assert "doctest" in result.output.lower()
    assert "detected" in result.output.lower()


@pytest.mark.os_agnostic
def test_doctest_command_without_doctest(cli_runner: CliRunner) -> None:
    """Doctest command should return exit code 1 when doctest not detected."""
    result = cli_runner.invoke(cli_mod.cli, ["doctest", "--arg-string", "normal.py"])

    assert result.exit_code == 1
    assert "not detected" in result.output.lower()


@pytest.mark.os_agnostic
def test_setup_command_detects_setup(cli_runner: CliRunner) -> None:
    """Setup command should detect setup.py."""
    result = cli_runner.invoke(cli_mod.cli, ["setup", "--arg-string", "setup.py build"])

    assert result.exit_code == 0
    assert "setup" in result.output.lower()
    assert "detected" in result.output.lower()


@pytest.mark.os_agnostic
def test_setup_command_test_only_flag(cli_runner: CliRunner) -> None:
    """Setup command with --test-only should detect only 'setup.py test'."""
    # Should detect setup.py test
    result = cli_runner.invoke(cli_mod.cli, ["setup", "--test-only", "--arg-string", "setup.py test"])
    assert result.exit_code == 0

    # Should NOT detect just setup.py
    result = cli_runner.invoke(cli_mod.cli, ["setup", "--test-only", "--arg-string", "setup.py build"])
    assert result.exit_code == 1


@pytest.mark.os_agnostic
def test_setup_command_without_setup(cli_runner: CliRunner) -> None:
    """Setup command should return exit code 1 when setup.py not detected."""
    result = cli_runner.invoke(cli_mod.cli, ["setup", "--arg-string", "normal.py"])

    assert result.exit_code == 1
    assert "not detected" in result.output.lower()


@pytest.mark.os_agnostic
def test_all_commands_have_help(cli_runner: CliRunner) -> None:
    """All commands should have help text available."""
    commands = ["check", "pytest", "doctest", "setup", "hello", "fail", "info"]

    for cmd in commands:
        result = cli_runner.invoke(cli_mod.cli, [cmd, "--help"])
        assert result.exit_code == 0, f"Command '{cmd}' --help failed"
        assert "Usage:" in result.output, f"Command '{cmd}' help missing Usage"
