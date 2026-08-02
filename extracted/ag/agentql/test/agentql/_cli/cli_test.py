import subprocess

import pytest
from mockito import mock, patch, unstub, verify, when
from typer.testing import CliRunner

from agentql._cli._commands import init_command, new_script_command
from agentql._cli._main import app

# pylint: disable=protected-access


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture(autouse=True)
def clean_mockito():
    # Setup can go here if needed
    yield
    unstub()


def test_init_command(runner):
    """Test the init command."""
    with runner.isolated_filesystem():
        # Mock subprocess for dependency installation
        completed_process_mock = mock({"returncode": 0})
        when(subprocess).run(["playwright", "install", "chromium"], check=True, capture_output=True).thenReturn(
            completed_process_mock
        )

        # Stubbing the API key request, validation, and file writing
        when(init_command)._request_api_key().thenReturn("valid_api_key")
        when(init_command)._check_server_status().thenReturn(True)
        when(init_command)._request_debug_files_path().thenReturn("debug_path")
        when(init_command)._check_api_key("valid_api_key").thenReturn(True)
        patch(init_command._save_config_to_file, lambda api_key, debug_path: None)
        patch(init_command._download_sample_script, lambda: None)

        result = runner.invoke(app, ["init"])

        assert "AgentQL is now installed and ready to use!" in result.output
        assert result.exit_code == 0

        verify(subprocess).run(["playwright", "install", "chromium"], check=True, capture_output=True)
        verify(init_command, times=1)._request_api_key()
        verify(init_command, times=1)._check_server_status()
        verify(init_command, times=1)._check_api_key("valid_api_key")
        verify(init_command, times=1)._request_debug_files_path()
        verify(init_command, times=1)._save_config_to_file(api_key="valid_api_key", debug_path="debug_path")
        verify(init_command, times=1)._download_sample_script()


def test_new_script_sync(runner):
    """Test the new_script command for synchronous template download."""
    with runner.isolated_filesystem():
        when(new_script_command).download_script(any, any).thenReturn(None)
        result = runner.invoke(app, ["new-script", "--type", "sync"], input="sync\n")

        assert "Downloading the template script..." in result.output
        assert result.exit_code == 0

        verify(new_script_command, times=1).download_script(any, any)


def test_new_script_async(runner):
    """Test the new_script command for asynchronous template download."""
    with runner.isolated_filesystem():
        when(new_script_command).download_script(any, any).thenReturn(None)

        result = runner.invoke(app, ["new-script", "--type", "async"], input="async\n")

        assert "Downloading the template script..." in result.output
        assert result.exit_code == 0

        verify(new_script_command, times=1).download_script(any, any)


def test_new_script_invalid_option(runner):
    """Test the new_script command with an invalid option."""
    result = runner.invoke(app, ["new-script", "--type", "invalid"])
    assert result.exit_code == 2


def test_doctor(runner):
    """Test the doctor command."""
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert (
        "In the future, this command will run various checks to ensure your system is ready to run AgentQL. For now, it does nothing."
        in result.output
    )
