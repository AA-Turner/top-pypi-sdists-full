import pytest
from typer.testing import CliRunner
from sage.main import app as sage_app

@pytest.fixture
def runner():
    return CliRunner()

def test_models_command(runner):
    """Test that the 'models' command works without throwing an error."""
    result = runner.invoke(sage_app, ["models"])
    assert result.exit_code == 0
    assert "Available Models" in result.output or "Local Models" in result.output or "Cloud Models" in result.output

def test_config_show_command(runner):
    """Test that 'config show' works."""
    result = runner.invoke(sage_app, ["config", "show"])
    assert result.exit_code == 0
    assert "Current Configuration" in result.output or "config" in result.output.lower()

def test_ask_command_with_flags(runner):
    """Test the ask command with various flags."""
    # SAGE CLI will execute functionally using our session test server
    result = runner.invoke(sage_app, [
        "ask", "Create a responsive advertising dashboard using React and Tailwind.", 
        "--raw", 
        "--max-tokens", "100"
    ])
    assert result.exit_code == 0

def test_repl_slash_exit_commands(runner):
    """Test that REPL exit commands like /exit, /quit, /q work."""
    for cmd in ["/exit", "/quit", "/q"]:
        result = runner.invoke(sage_app, ["run"], input=f"{cmd}\n")
        assert result.exit_code == 0

def test_mode_violation_false_positives():
    """Test that conversational lists matching FILE: do not trigger false positive violations."""
    from sage.main import _extract_and_write_files
    from pathlib import Path

    conversational_output = (
        "Analysis Plan:\n"
        "1. FILE: models/predict.py - This is the main prediction file\n"
        "2. FILE: models/config.py - Config files\n"
        "\n"
        "Some details: FILE: models/utils.py contains helpers.\n"
    )

    written = _extract_and_write_files(conversational_output, Path("."))
    # It should not write any files
    assert not written
