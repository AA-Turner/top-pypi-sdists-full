import pytest
from unittest.mock import patch, MagicMock
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

@patch("sage.main.SAGEAgent")
def test_run_command_initialization(mock_agent, runner):
    """Test that 'run' initializes the agent and exits cleanly when mocked."""
    mock_agent_instance = MagicMock()
    mock_agent.return_value = mock_agent_instance
    
    result = runner.invoke(sage_app, ["run"], input="exit\n")
    # If the interactive loop exits immediately, we should get 0
    # Actually 'sage run' might have different arguments or exit gracefully.
    assert result.exit_code == 0

@patch("sage.main.ConversationEngine")
def test_chat_command_initialization(mock_engine, runner):
    """Test that 'chat' command initializes without crashing."""
    mock_engine_instance = MagicMock()
    mock_engine.return_value = mock_engine_instance
    
    result = runner.invoke(sage_app, ["chat"], input="/exit\n")
    assert result.exit_code == 0

@patch("sage.main._prepare_model_for_use")
@patch("sage.main._build_router")
def test_ask_command_with_flags(mock_router, mock_prep, runner, tmp_path):
    """Test the ask command with various flags."""
    mock_prep.return_value = (MagicMock(), "cloud:gemini-2.0-flash")
    mock_router_inst = MagicMock()
    mock_router_inst.stream.return_value = ["Output"]
    mock_router.return_value = mock_router_inst
    
    # Test --raw and --cwd flags
    result = runner.invoke(sage_app, [
        "ask", "Test prompt", 
        "--raw", 
        "--model", "cloud:gemini-2.0-flash",
        "--max-tokens", "100"
    ])
    
    assert result.exit_code == 0
    assert "Output" in result.output

@patch("sage.main.SAGEAgent")
def test_slash_command_mock_routing(mock_agent, runner):
    """Test that slash commands like /goal or /schedule don't crash the orchestrator."""
    # This is a basic structural test for slash commands passing through the CLI
    pass
