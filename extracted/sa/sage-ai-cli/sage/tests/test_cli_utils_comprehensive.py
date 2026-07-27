"""Comprehensive tests for sage/core/cli_utils.py to achieve 100% coverage."""

import json
import tempfile
from pathlib import Path
from unittest.mock import MagicMock, patch

from sage.core.cli_utils import (
    AnalyticsDashboard,
    CommandHelp,
    CommandSuggester,
    ConfigWizard,
    HelpSystem,
    HistoryBrowser,
    ModelSelector,
    MultiSelect,
    OutputConfig,
    OutputHandler,
    OutputMode,
    OutputPager,
    UsageStats,
    VerbosityLevel,
)


class TestOutputMode:
    """Tests for OutputMode enum."""

    def test_all_modes_exist(self):
        """Test all output modes are defined."""
        assert OutputMode.RICH.value == "rich"
        assert OutputMode.PLAIN.value == "plain"
        assert OutputMode.JSON.value == "json"
        assert OutputMode.CSV.value == "csv"
        assert OutputMode.MARKDOWN.value == "markdown"


class TestVerbosityLevel:
    """Tests for VerbosityLevel enum."""

    def test_verbosity_levels(self):
        """Test verbosity levels have correct values."""
        assert VerbosityLevel.QUIET.value == 0
        assert VerbosityLevel.NORMAL.value == 1
        assert VerbosityLevel.VERBOSE.value == 2
        assert VerbosityLevel.DEBUG.value == 3


class TestOutputConfig:
    """Tests for OutputConfig dataclass."""

    def test_default_config(self):
        """Test default configuration."""
        config = OutputConfig()
        assert config.mode == OutputMode.RICH
        assert config.verbosity == VerbosityLevel.NORMAL
        assert config.color is True
        assert config.pager is False
        assert config.width is None

    def test_custom_config(self):
        """Test custom configuration."""
        config = OutputConfig(
            mode=OutputMode.JSON,
            verbosity=VerbosityLevel.DEBUG,
            color=False,
            pager=True,
            width=80,
        )
        assert config.mode == OutputMode.JSON
        assert config.verbosity == VerbosityLevel.DEBUG
        assert config.color is False
        assert config.pager is True
        assert config.width == 80


class TestOutputHandler:
    """Tests for OutputHandler class."""

    def test_default_handler(self):
        """Test default handler initialization."""
        handler = OutputHandler()
        assert handler.config.mode == OutputMode.RICH
        assert handler._console is None

    def test_custom_config_handler(self):
        """Test handler with custom config."""
        config = OutputConfig(mode=OutputMode.PLAIN, color=False)
        handler = OutputHandler(config)
        assert handler.config.mode == OutputMode.PLAIN
        assert handler.config.color is False

    def test_console_property(self):
        """Test console property creates console."""
        handler = OutputHandler()
        console = handler.console
        assert console is not None
        # Same console returned on second call
        assert handler.console is console

    def test_print_normal_verbosity(self, capsys):
        """Test print with normal verbosity."""
        config = OutputConfig(mode=OutputMode.PLAIN)
        handler = OutputHandler(config)
        handler.print("test message")
        captured = capsys.readouterr()
        assert "test message" in captured.out

    def test_print_skipped_high_verbosity(self, capsys):
        """Test print skipped when verbosity too high."""
        config = OutputConfig(verbosity=VerbosityLevel.QUIET)
        handler = OutputHandler(config)
        handler.print("test message", level=VerbosityLevel.VERBOSE)
        captured = capsys.readouterr()
        assert captured.out == ""

    def test_print_json_mode(self, capsys):
        """Test print in JSON mode."""
        config = OutputConfig(mode=OutputMode.JSON)
        handler = OutputHandler(config)
        handler.print("test message")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["message"] == "test message"

    def test_print_plain_mode_strips_markup(self, capsys):
        """Test plain mode strips rich markup."""
        config = OutputConfig(mode=OutputMode.PLAIN)
        handler = OutputHandler(config)
        handler.print("[bold]test[/bold] [red]message[/red]")
        captured = capsys.readouterr()
        assert "[bold]" not in captured.out
        assert "test message" in captured.out

    def test_print_data_json(self, capsys):
        """Test print_data in JSON mode."""
        config = OutputConfig(mode=OutputMode.JSON)
        handler = OutputHandler(config)
        handler.print_data({"key": "value"})
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["key"] == "value"

    def test_print_data_csv_list_of_dicts(self, capsys):
        """Test print_data in CSV mode with list of dicts."""
        config = OutputConfig(mode=OutputMode.CSV)
        handler = OutputHandler(config)
        handler.print_data([{"a": 1, "b": 2}, {"a": 3, "b": 4}])
        captured = capsys.readouterr()
        assert "a,b" in captured.out
        assert "1,2" in captured.out

    def test_print_data_csv_list_of_values(self, capsys):
        """Test print_data in CSV mode with simple list."""
        config = OutputConfig(mode=OutputMode.CSV)
        handler = OutputHandler(config)
        handler.print_data(["value1", "value2"])
        captured = capsys.readouterr()
        assert "value1" in captured.out

    def test_print_data_csv_list_of_tuples(self, capsys):
        """Test print_data in CSV mode with list of tuples."""
        config = OutputConfig(mode=OutputMode.CSV)
        handler = OutputHandler(config)
        handler.print_data([("a", "b"), ("c", "d")])
        captured = capsys.readouterr()
        assert "a,b" in captured.out

    def test_print_data_markdown_with_title(self, capsys):
        """Test print_data in markdown mode with title."""
        config = OutputConfig(mode=OutputMode.MARKDOWN)
        handler = OutputHandler(config)
        handler.print_data({"key": "value"}, title="Test Title")
        captured = capsys.readouterr()
        assert "# Test Title" in captured.out
        assert "**key**" in captured.out

    def test_print_data_markdown_list_of_dicts(self, capsys):
        """Test print_data in markdown mode with table."""
        config = OutputConfig(mode=OutputMode.MARKDOWN)
        handler = OutputHandler(config)
        handler.print_data([{"col1": "val1", "col2": "val2"}])
        captured = capsys.readouterr()
        assert "| col1 | col2 |" in captured.out
        assert "| --- | --- |" in captured.out

    def test_print_data_markdown_simple_value(self, capsys):
        """Test print_data in markdown mode with simple value."""
        config = OutputConfig(mode=OutputMode.MARKDOWN)
        handler = OutputHandler(config)
        handler.print_data("simple string", title=None)
        captured = capsys.readouterr()
        assert "simple string" in captured.out

    def test_print_table_empty_data(self):
        """Test _print_table with empty data."""
        handler = OutputHandler()
        # Should not raise
        handler._print_table([], None)

    def test_print_dict(self):
        """Test _print_dict."""
        handler = OutputHandler()
        # Should not raise
        handler._print_dict({"key": "value"}, "Test")

    def test_print_data_rich_list_of_dicts(self):
        """Test print_data with rich output for list of dicts."""
        handler = OutputHandler()
        # Should not raise
        handler.print_data([{"a": 1}], "Test")

    def test_print_data_rich_simple_value(self):
        """Test print_data with rich output for simple value."""
        handler = OutputHandler()
        # Should not raise
        handler.print_data("simple value")


class TestCommandHelp:
    """Tests for CommandHelp dataclass."""

    def test_basic_command_help(self):
        """Test basic command help creation."""
        cmd = CommandHelp(
            name="test",
            description="Test command",
            usage="sage test [options]",
        )
        assert cmd.name == "test"
        assert cmd.examples == []
        assert cmd.options == []
        assert cmd.related == []

    def test_full_command_help(self):
        """Test command help with all fields."""
        cmd = CommandHelp(
            name="run",
            description="Run agent",
            usage="sage run",
            examples=["sage run", "sage run --model gpt-4"],
            options=[("-m", "Model to use")],
            related=["chat", "ask"],
        )
        assert len(cmd.examples) == 2
        assert len(cmd.options) == 1
        assert len(cmd.related) == 2


class TestHelpSystem:
    """Tests for HelpSystem class."""

    def test_register_and_show_command(self, capsys):
        """Test registering and showing command help."""
        help_sys = HelpSystem()
        cmd = CommandHelp(
            name="test",
            description="Test command",
            usage="sage test",
            examples=["sage test"],
            options=[("-v", "Verbose")],
            related=["other"],
        )
        help_sys.register(cmd)
        help_sys.show("test")
        captured = capsys.readouterr()
        assert "test" in captured.out
        assert "Test command" in captured.out

    def test_show_unknown_command(self, capsys):
        """Test showing help for unknown command."""
        help_sys = HelpSystem()
        help_sys.register(CommandHelp("test", "Test", "sage test"))
        help_sys.show("unknown")
        captured = capsys.readouterr()
        assert "Unknown command" in captured.out

    def test_show_all_commands(self, capsys):
        """Test showing all commands."""
        help_sys = HelpSystem()
        help_sys.register(CommandHelp("cmd1", "First", "sage cmd1"))
        help_sys.register(CommandHelp("cmd2", "Second", "sage cmd2"))
        help_sys.show()
        captured = capsys.readouterr()
        assert "cmd1" in captured.out
        assert "cmd2" in captured.out

    def test_suggest_similar_commands(self, capsys):
        """Test suggesting similar commands."""
        help_sys = HelpSystem()
        help_sys.register(CommandHelp("test", "Test", "sage test"))
        help_sys.show("tets")  # typo
        captured = capsys.readouterr()
        assert "Did you mean" in captured.out


class TestCommandSuggester:
    """Tests for CommandSuggester class."""

    def test_suggest_for_typo(self):
        """Test typo suggestions."""
        suggester = CommandSuggester(["run", "test", "chat", "models"])
        suggestions = suggester.suggest_for_typo("rnu")
        assert "run" in suggestions

    def test_set_context(self):
        """Test setting context."""
        suggester = CommandSuggester(["test"])
        suggester.set_context("has_tests", True)
        assert suggester._context["has_tests"] is True

    def test_record_command(self):
        """Test recording commands."""
        suggester = CommandSuggester(["test"])
        suggester.record_command("run")
        assert "run" in suggester._history

    def test_suggest_next_after_run(self):
        """Test suggestions after run command."""
        suggester = CommandSuggester(["test", "lint", "build"])
        suggester.record_command("run")
        suggestions = suggester.suggest_next()
        assert "test" in suggestions

    def test_suggest_next_after_test(self):
        """Test suggestions after test command."""
        suggester = CommandSuggester(["fix", "run"])
        suggester.record_command("test")
        suggestions = suggester.suggest_next()
        assert "fix" in suggestions

    def test_suggest_next_with_context(self):
        """Test suggestions based on context."""
        suggester = CommandSuggester(["test", "fix"])
        suggester.set_context("has_tests", True)
        suggester.set_context("has_errors", True)
        suggestions = suggester.suggest_next()
        assert "test" in suggestions
        assert "fix" in suggestions


class TestConfigWizard:
    """Tests for ConfigWizard class."""

    @patch("sage.core.cli_utils.Prompt.ask")
    @patch("sage.core.cli_utils.Confirm.ask")
    def test_run_wizard_basic(self, mock_confirm, mock_prompt):
        """Test running basic wizard flow."""
        mock_prompt.side_effect = ["1", "0.3", "8192"]
        mock_confirm.side_effect = [False, True]  # No API key, Yes save
        wizard = ConfigWizard()
        config = wizard.run()
        assert config["default_model"] == "ollama:llama3.2"
        assert config["temperature"] == 0.3
        assert config["max_tokens"] == 8192

    @patch("sage.core.cli_utils.Prompt.ask")
    @patch("sage.core.cli_utils.Confirm.ask")
    def test_run_wizard_with_api_key(self, mock_confirm, mock_prompt):
        """Test wizard with API key configuration."""
        mock_prompt.side_effect = ["2", "test-api-key", "0.5", "4096"]
        mock_confirm.side_effect = [True, True]  # Yes API key, Yes save
        wizard = ConfigWizard()
        config = wizard.run()
        assert config["default_model"] == "gemini:gemini-2.0-flash"
        assert "api_keys" in config

    @patch("sage.core.cli_utils.Prompt.ask")
    @patch("sage.core.cli_utils.Confirm.ask")
    def test_run_wizard_cancelled(self, mock_confirm, mock_prompt):
        """Test wizard when user cancels."""
        mock_prompt.side_effect = ["1", "0.2", "16384"]
        mock_confirm.side_effect = [False, False]  # No API key, No save
        wizard = ConfigWizard()
        config = wizard.run()
        assert config == {}

    def test_validate_config_valid(self):
        """Test validation with valid config."""
        wizard = ConfigWizard()
        config = {"default_model": "test", "temperature": 0.5, "max_tokens": 4096}
        issues = wizard.validate(config)
        assert len(issues) == 0

    def test_validate_config_missing_model(self):
        """Test validation with missing model."""
        wizard = ConfigWizard()
        issues = wizard.validate({})
        assert any("default_model" in i[0] for i in issues)

    def test_validate_config_bad_temperature(self):
        """Test validation with out-of-range temperature."""
        wizard = ConfigWizard()
        config = {"default_model": "test", "temperature": 3.0}
        issues = wizard.validate(config)
        assert any("temperature" in i[0] for i in issues)

    def test_validate_config_low_tokens(self):
        """Test validation with low max_tokens."""
        wizard = ConfigWizard()
        config = {"default_model": "test", "max_tokens": 10}
        issues = wizard.validate(config)
        assert any("max_tokens" in i[0] for i in issues)

    def test_load_project_config_sagecrc(self):
        """Test loading .sagecrc config."""
        with tempfile.TemporaryDirectory() as tmpdir:
            project = Path(tmpdir)
            config_file = project / ".sagecrc"
            config_file.write_text('{"model": "test"}')
            wizard = ConfigWizard()
            config = wizard.load_project_config(project)
            assert config["model"] == "test"

    def test_load_project_config_none(self):
        """Test loading config when none exists."""
        with tempfile.TemporaryDirectory() as tmpdir:
            wizard = ConfigWizard()
            config = wizard.load_project_config(Path(tmpdir))
            assert config == {}


class TestModelSelector:
    """Tests for ModelSelector class."""

    @patch("sage.core.cli_utils.Prompt.ask")
    def test_select_model(self, mock_prompt):
        """Test selecting a model."""
        mock_prompt.return_value = "1"
        models = [{"name": "model1", "provider": "test", "size": "7B"}]
        selector = ModelSelector(models)
        result = selector.select()
        assert result == "model1"

    @patch("sage.core.cli_utils.Prompt.ask")
    def test_select_model_cancelled(self, mock_prompt):
        """Test cancelling model selection."""
        mock_prompt.return_value = "q"
        models = [{"name": "model1"}]
        selector = ModelSelector(models)
        result = selector.select()
        assert result is None

    @patch("sage.core.cli_utils.Prompt.ask")
    def test_select_model_invalid(self, mock_prompt):
        """Test invalid model selection."""
        mock_prompt.return_value = "invalid"
        models = [{"name": "model1"}]
        selector = ModelSelector(models)
        result = selector.select()
        assert result is None

    def test_select_no_models(self, capsys):
        """Test selection with no models."""
        selector = ModelSelector([])
        result = selector.select()
        assert result is None
        captured = capsys.readouterr()
        assert "No models found" in captured.out

    def test_filter_models(self):
        """Test model filtering."""
        models = [
            {"name": "llama-7b", "provider": "ollama"},
            {"name": "gpt-4", "provider": "openai"},
        ]
        selector = ModelSelector(models)
        filtered = selector._filter_models("llama")
        assert len(filtered) == 1
        assert filtered[0]["name"] == "llama-7b"

    @patch("sage.core.cli_utils.Prompt.ask")
    def test_select_with_filter(self, mock_prompt):
        """Test selection with filter."""
        mock_prompt.return_value = "1"
        models = [
            {"name": "llama-7b", "provider": "ollama"},
            {"name": "gpt-4", "provider": "openai"},
        ]
        selector = ModelSelector(models)
        result = selector.select(filter_text="llama")
        assert result == "llama-7b"


class TestHistoryBrowser:
    """Tests for HistoryBrowser class."""

    def test_add_and_search(self):
        """Test adding and searching history."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history_file = Path(tmpdir) / "history"
            browser = HistoryBrowser(history_file)
            browser.add("sage run")
            browser.add("sage test")
            results = browser.search("run")
            assert "sage run" in results

    def test_recent(self):
        """Test getting recent commands."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history_file = Path(tmpdir) / "history"
            browser = HistoryBrowser(history_file)
            browser.add("cmd1")
            browser.add("cmd2")
            browser.add("cmd3")
            recent = browser.recent(2)
            assert len(recent) == 2
            assert "cmd3" in recent

    def test_load_existing_history(self):
        """Test loading existing history file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history_file = Path(tmpdir) / "history"
            # Create history file
            history_file.write_text("1234567890.0|cmd1\n1234567891.0|cmd2\n")
            browser = HistoryBrowser(history_file)
            assert len(browser._history) == 2

    def test_load_invalid_history_lines(self):
        """Test loading history with invalid lines."""
        with tempfile.TemporaryDirectory() as tmpdir:
            history_file = Path(tmpdir) / "history"
            history_file.write_text("invalid line\n1234567890.0|valid\n")
            browser = HistoryBrowser(history_file)
            assert len(browser._history) == 1


class TestUsageStats:
    """Tests for UsageStats dataclass."""

    def test_default_stats(self):
        """Test default stats."""
        stats = UsageStats()
        assert stats.command_counts == {}
        assert stats.success_counts == {}
        assert stats.error_counts == {}
        assert stats.total_duration == 0.0
        assert stats.session_count == 0


class TestAnalyticsDashboard:
    """Tests for AnalyticsDashboard class."""

    def test_record_command_success(self):
        """Test recording successful command."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = Path(tmpdir) / "analytics.json"
            dashboard = AnalyticsDashboard(storage)
            dashboard.record_command("test", success=True, duration=1.5)
            assert dashboard.stats.command_counts["test"] == 1
            assert dashboard.stats.success_counts["test"] == 1
            assert dashboard.stats.total_duration == 1.5

    def test_record_command_failure(self):
        """Test recording failed command."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = Path(tmpdir) / "analytics.json"
            dashboard = AnalyticsDashboard(storage)
            dashboard.record_command("test", success=False, duration=0.5)
            assert dashboard.stats.error_counts["test"] == 1

    def test_start_session(self):
        """Test recording session start."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = Path(tmpdir) / "analytics.json"
            dashboard = AnalyticsDashboard(storage)
            dashboard.start_session()
            assert dashboard.stats.session_count == 1

    def test_render_dashboard(self, capsys):
        """Test rendering dashboard."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = Path(tmpdir) / "analytics.json"
            dashboard = AnalyticsDashboard(storage)
            dashboard.record_command("cmd1", True, 1.0)
            dashboard.record_command("cmd1", True, 0.5)
            dashboard.record_command("cmd2", False, 0.3)
            dashboard.render()
            captured = capsys.readouterr()
            assert "Analytics Dashboard" in captured.out
            assert "cmd1" in captured.out

    def test_load_existing_stats(self):
        """Test loading existing stats."""
        with tempfile.TemporaryDirectory() as tmpdir:
            storage = Path(tmpdir) / "analytics.json"
            storage.write_text(
                json.dumps(
                    {
                        "command_counts": {"test": 5},
                        "success_counts": {"test": 4},
                        "error_counts": {"test": 1},
                        "total_duration": 10.0,
                        "session_count": 3,
                    }
                )
            )
            dashboard = AnalyticsDashboard(storage)
            assert dashboard.stats.command_counts["test"] == 5


class TestOutputPager:
    """Tests for OutputPager class."""

    def test_page_short_content(self, capsys):
        """Test paging short content (no paging needed)."""
        pager = OutputPager()
        pager.page("short content", title="Test")
        captured = capsys.readouterr()
        assert "Test" in captured.out
        assert "short content" in captured.out

    @patch("shutil.get_terminal_size")
    @patch("builtins.input")
    def test_page_long_content(self, mock_input, mock_terminal_size, capsys):
        """Test paging long content."""
        mock_terminal_size.return_value = MagicMock(lines=5)
        mock_input.return_value = "q"  # Quit after first page
        pager = OutputPager()
        long_content = "\n".join([f"line {i}" for i in range(20)])
        pager.page(long_content, title="Test")
        captured = capsys.readouterr()
        # Should show some content
        assert "line" in captured.out

    @patch("shutil.get_terminal_size")
    @patch("builtins.input")
    def test_page_next_page(self, mock_input, mock_terminal_size, capsys):
        """Test going to next page."""
        mock_terminal_size.return_value = MagicMock(lines=5)
        mock_input.side_effect = ["", "q"]  # Next page, then quit
        pager = OutputPager()
        long_content = "\n".join([f"line {i}" for i in range(20)])
        pager.page(long_content)


class TestMultiSelect:
    """Tests for MultiSelect class."""

    @patch("sage.core.cli_utils.Prompt.ask")
    def test_select_single(self, mock_prompt):
        """Test selecting single item."""
        mock_prompt.return_value = "1"
        ms = MultiSelect()
        result = ms.select(["opt1", "opt2", "opt3"])
        assert result == ["opt1"]

    @patch("sage.core.cli_utils.Prompt.ask")
    def test_select_multiple(self, mock_prompt):
        """Test selecting multiple items."""
        mock_prompt.return_value = "1, 3"
        ms = MultiSelect()
        result = ms.select(["opt1", "opt2", "opt3"])
        assert "opt1" in result
        assert "opt3" in result
        assert "opt2" not in result

    @patch("sage.core.cli_utils.Prompt.ask")
    def test_select_all(self, mock_prompt):
        """Test selecting all items."""
        mock_prompt.return_value = "a"
        ms = MultiSelect()
        result = ms.select(["opt1", "opt2"])
        assert result == ["opt1", "opt2"]

    @patch("sage.core.cli_utils.Prompt.ask")
    def test_select_min_not_met(self, mock_prompt, capsys):
        """Test selection when minimum not met."""
        mock_prompt.side_effect = ["", "1, 2"]  # First empty, then valid
        ms = MultiSelect()
        result = ms.select(["opt1", "opt2"], min_selections=2)
        assert len(result) == 2

    @patch("sage.core.cli_utils.Prompt.ask")
    def test_select_max_exceeded(self, mock_prompt, capsys):
        """Test selection when maximum exceeded."""
        mock_prompt.side_effect = ["1, 2, 3", "1"]  # Too many, then valid
        ms = MultiSelect()
        result = ms.select(["opt1", "opt2", "opt3"], max_selections=1)
        assert len(result) == 1

    @patch("sage.core.cli_utils.Prompt.ask")
    def test_select_invalid_input(self, mock_prompt, capsys):
        """Test invalid input handling."""
        mock_prompt.side_effect = ["abc", "1"]  # Invalid, then valid
        ms = MultiSelect()
        result = ms.select(["opt1", "opt2"])
        assert result == ["opt1"]
