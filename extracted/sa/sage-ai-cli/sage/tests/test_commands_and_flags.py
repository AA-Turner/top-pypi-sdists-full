import pytest
from typer.testing import CliRunner
from sage.cli_core import app as sage_app

@pytest.fixture
def runner(tmp_path, monkeypatch):
    from pathlib import Path
    monkeypatch.setattr(Path, "home", lambda: tmp_path)
    monkeypatch.setattr(Path, "cwd", lambda: tmp_path)
    import sage.config
    import sage.models.catalog
    monkeypatch.setattr(sage.config, "CONFIG_PATH", tmp_path / "config.json")
    monkeypatch.setattr(sage.config, "SAGE_DIR", tmp_path)
    monkeypatch.setattr(sage.models.catalog, "_CACHE_DIR", tmp_path / "cache")
    monkeypatch.setattr(sage.models.catalog, "_CACHE_FILE", tmp_path / "cache" / "catalog.json")
    return CliRunner()

def test_models_command(runner):
    """Test that the 'models' command works without throwing an error."""
    result = runner.invoke(sage_app, ["models"], catch_exceptions=False)
    assert result.exit_code == 0
    assert "Available Models" in result.output or "Local Models" in result.output or "Cloud Models" in result.output

def test_config_show_command(runner):
    """Test that 'config show' works."""
    result = runner.invoke(sage_app, ["config", "show"])
    assert result.exit_code == 0
    assert "Current Configuration" in result.output or "config" in result.output.lower()

def test_ask_command_with_flags(runner, monkeypatch):
    """Test the ask command with various flags."""
    import sage.cli_core
    
    # Mock the router to avoid real network calls
    class DummyRouter:
        def stream(self, messages, model_id, temp, tokens):
            yield "Mocked response"
        def generate(self, messages, model_id, temp, tokens):
            return "Mocked response"
            
    monkeypatch.setattr(sage.cli_core, "_build_router", lambda cfg: DummyRouter())
    # Note: _auto_upgrade_model_if_possible also uses the router, so we need to mock it if it tries to list models
    monkeypatch.setattr(sage.cli_core, "_auto_upgrade_model_if_possible", lambda r, c, m, **kw: m)
    monkeypatch.setattr(sage.cli_core, "_prepare_model_for_use", lambda c, m: (c, m))
    
    result = runner.invoke(sage_app, [
        "ask", "Create a responsive advertising dashboard using React and Tailwind.", 
        "--raw", 
        "--max-tokens", "100"
    ], catch_exceptions=False)
    assert result.exit_code == 0
    assert "Mocked response" in result.output

@pytest.mark.timeout(15)
def test_repl_slash_exit_commands(runner, monkeypatch):
    """Test that REPL exit commands like /exit, /quit, /q work."""
    import prompt_toolkit
    import sage.cli_core
    
    # Mock the router and model prep to avoid real network calls during agent initialization
    class DummyRouter:
        def stream(self, messages, model_id, temp, tokens):
            yield "Mocked response"
        def generate(self, messages, model_id, temp, tokens):
            return "Mocked response"
            
    monkeypatch.setattr(sage.cli_core, "_build_router", lambda cfg: DummyRouter())
    monkeypatch.setattr(sage.cli_core, "_auto_upgrade_model_if_possible", lambda r, c, m, **kw: m)
    monkeypatch.setattr(sage.cli_core, "_prepare_model_for_use", lambda c, m: (c, m))
    import sage.core.cli_auth
    monkeypatch.setattr(sage.core.cli_auth, "check_token_quota", lambda auth=None: None)
    monkeypatch.setattr(sage.core.cli_auth, "check_cli_access", lambda: None)
    monkeypatch.setattr(sage.cli_core, "_scan_project_context", lambda *args, **kwargs: "Dummy context")
    import sage.core.ai_orchestration
    from sage.core.plugin_system import PluginRegistry
    monkeypatch.setattr(sage.core.ai_orchestration, "build_default_plugin_registry", lambda *args, **kwargs: PluginRegistry())
    monkeypatch.setattr(sage.cli_core, "_build_session_protected_files", lambda *args: set())
    
    for cmd in ["/exit", "/quit", "/q"]:
        call_count = 0
        class DummyPromptSession:
            def __init__(self, **kwargs):
                class DummyLayout:
                    class DummyContainer:
                        def __init__(self):
                            self.children = []
                    def __init__(self):
                        self.container = DummyLayout.DummyContainer()
                self.layout = DummyLayout()
            async def prompt_async(self, *args, **kwargs):
                nonlocal call_count
                call_count += 1
                if call_count > 1:
                    raise EOFError()  # Safety: force exit if called more than once
                return cmd
        monkeypatch.setattr(prompt_toolkit, "PromptSession", DummyPromptSession)
        import sage.core.repl
        monkeypatch.setattr(sage.core.repl, "PromptSession", DummyPromptSession)
        result = runner.invoke(sage_app, ["run"])
        assert result.exit_code == 0

def test_mode_violation_false_positives():
    """Test that conversational lists matching FILE: do not trigger false positive violations."""
    from sage.cli_core import _extract_and_write_files
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
