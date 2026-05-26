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
def test_repl_slash_exit_commands(mock_agent, runner):
    """Test that REPL exit commands like /exit, /quit, /q work."""
    mock_agent_instance = MagicMock()
    mock_agent.return_value = mock_agent_instance
    
    for cmd in ["/exit", "/quit", "/q"]:
        result = runner.invoke(sage_app, ["run"], input=f"{cmd}\n")
        assert result.exit_code == 0

@patch("sage.main.SAGEAgent")
def test_repl_slash_command_routing(mock_agent, runner):
    """Test that slash commands are handled by the REPL handler and not sent to agent's LLM loop."""
    mock_agent_instance = MagicMock()
    mock_agent.return_value = mock_agent_instance
    
    # Mock print_agent_help on renderer
    mock_agent_instance.renderer = MagicMock()
    
    # We patch run_repl so we can capture _repl_execute and call it directly
    with patch("sage.core.repl.run_repl") as mock_run_repl:
        # Run command inside runner to trigger run()
        runner.invoke(sage_app, ["run"])
        
        assert mock_run_repl.called
        agent_passed, repl_exec = mock_run_repl.call_args[0]
        
        # Test /help
        repl_exec("/help")
        # Ensure it calls print_agent_help instead of execute_task_prompt
        assert mock_agent_instance.renderer.print_agent_help.called
        assert not mock_agent_instance.execute_task_prompt.called

        # Reset mocks
        mock_agent_instance.renderer.print_agent_help.reset_mock()
        mock_agent_instance.execute_task_prompt.reset_mock()

        # Test /clear
        repl_exec("/clear")
        assert mock_agent_instance.engine.clear.called
        assert not mock_agent_instance.execute_task_prompt.called

        # Test /context
        mock_stats = MagicMock()
        mock_stats.message_count = 10
        mock_stats.turn_count = 5
        mock_stats.system_prompt_tokens = 100
        mock_stats.history_tokens = 500
        mock_stats.estimated_tokens = 600
        mock_stats.max_tokens = 100000
        mock_stats.usage_percent = 0.6
        mock_agent_instance.engine.get_context_stats.return_value = mock_stats

        repl_exec("/context")
        assert mock_agent_instance.engine.get_context_stats.called

        # Test /tdd
        from sage.core.tdd import get_tdd_enforcer
        enforcer = get_tdd_enforcer()
        original_status = enforcer.enabled
        repl_exec("/tdd")
        assert enforcer.enabled != original_status
        repl_exec("/tdd off")
        assert not enforcer.enabled
        repl_exec("/tdd on")
        assert enforcer.enabled
        enforcer.enabled = original_status # restore

        # Test /expert
        mock_agent_instance.send_to_model.return_value = "Expert analysis text"
        repl_exec("/expert Security Engineering")
        assert mock_agent_instance.send_to_model.called

        # Test /swarm
        mock_agent_instance.send_to_model.reset_mock()
        repl_exec("/swarm")
        assert mock_agent_instance.send_to_model.called

        # Test /sandbox
        mock_sandbox = MagicMock()
        mock_sandbox.is_available.return_value = True
        mock_sandbox.execute.return_value = MagicMock(stdout="Line count: 123", stderr="", exit_code=0)
        mock_agent_instance.tdd_gate = MagicMock()
        mock_agent_instance.tdd_gate.sandbox = mock_sandbox

        repl_exec("/sandbox")
        assert mock_sandbox.execute.called

        # Test /phd
        mock_phd = MagicMock()
        mock_phd.solver.solve_complete.return_value = {"sub_problems": ["Sub-task 1"], "solutions": {0: "Solution 1"}}
        mock_agent_instance.phd_agent = mock_phd
        repl_exec("/phd Quantum Computing")
        assert mock_phd.solver.solve_complete.called

        # Test /rag (with mock RAGIndex)
        with patch("sage.core.rag.RAGIndex") as mock_rag_index_cls:
            mock_index_inst = MagicMock()
            mock_index_inst.query.return_value = []
            mock_index_inst.reindex.return_value = {"files_seen": 2, "chunks_added": 5}
            mock_rag_index_cls.return_value = mock_index_inst

            repl_exec("/rag status")
            assert mock_rag_index_cls.called

            mock_rag_index_cls.reset_mock()
            repl_exec("/rag query Test")
            assert mock_rag_index_cls.called
            assert mock_index_inst.query.called

            mock_rag_index_cls.reset_mock()
            repl_exec("/rag index")
            assert mock_rag_index_cls.called
            assert mock_index_inst.reindex.called


@patch("sage.main._get_current_classification")
@patch("sage.main.renderer")
def test_mode_violation_false_positives(mock_renderer, mock_get_class):
    """Test that conversational lists matching FILE: do not trigger false positive MODE VIOLATIONs."""
    from sage.main import _extract_and_write_files, _RequestType
    from pathlib import Path

    # Mock read-only analysis classification
    mock_class = MagicMock()
    mock_class.read_only = True
    mock_class.request_type = _RequestType.ANALYSIS
    mock_get_class.return_value = mock_class

    # Output containing conversational lists with 'FILE:'
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
    # It should not call renderer.error for mode violations
    assert not mock_renderer.error.called


