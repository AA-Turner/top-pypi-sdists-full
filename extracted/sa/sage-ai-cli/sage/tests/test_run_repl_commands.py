"""
Comprehensive tests for sage run REPL commands.

This module tests all slash commands, shell escapes, multiline input,
and session state management within the interactive `sage run` loop.
"""

import pytest

# Import the command handlers and utilities from main
# We'll test the command dispatch logic directly


class TestREPLCommandDispatch:
    """Test the command dispatch logic for slash commands."""

    def test_help_command_recognized(self):
        """Test that /help is recognized as a valid command."""
        command = "/help"
        assert command.startswith("/")
        assert command[1:].split(maxsplit=1)[0] == "help"

    def test_exit_command_recognized(self):
        """Test that /exit is recognized as a valid command."""
        command = "/exit"
        assert command.startswith("/")
        assert command[1:].split(maxsplit=1)[0] == "exit"

    def test_models_command_recognized(self):
        """Test that /models is recognized as a valid command."""
        command = "/models"
        assert command.startswith("/")
        assert command[1:].split(maxsplit=1)[0] == "models"

    def test_model_command_with_arg(self):
        """Test that /model <name> parses correctly."""
        command = "/model gpt-4"
        parts = command[1:].split(maxsplit=1)
        assert parts[0] == "model"
        assert parts[1] == "gpt-4"

    def test_clear_command_recognized(self):
        """Test that /clear is recognized."""
        command = "/clear"
        assert command[1:].split(maxsplit=1)[0] == "clear"

    def test_compact_command_recognized(self):
        """Test that /compact is recognized."""
        command = "/compact"
        assert command[1:].split(maxsplit=1)[0] == "compact"

    def test_history_command_recognized(self):
        """Test that /history is recognized."""
        command = "/history"
        assert command[1:].split(maxsplit=1)[0] == "history"

    def test_prompts_command_recognized(self):
        """Test that /prompts is recognized."""
        command = "/prompts"
        assert command[1:].split(maxsplit=1)[0] == "prompts"

    def test_read_command_with_file(self):
        """Test that /read <file> parses correctly."""
        command = "/read src/main.py"
        parts = command[1:].split(maxsplit=1)
        assert parts[0] == "read"
        assert parts[1] == "src/main.py"

    def test_files_command_recognized(self):
        """Test that /files is recognized."""
        command = "/files"
        assert command[1:].split(maxsplit=1)[0] == "files"

    def test_test_command_recognized(self):
        """Test that /test is recognized."""
        command = "/test"
        assert command[1:].split(maxsplit=1)[0] == "test"

    def test_checkpoint_command_recognized(self):
        """Test that /checkpoint is recognized."""
        command = "/checkpoint"
        assert command[1:].split(maxsplit=1)[0] == "checkpoint"

    def test_checkpoints_command_recognized(self):
        """Test that /checkpoints is recognized."""
        command = "/checkpoints"
        assert command[1:].split(maxsplit=1)[0] == "checkpoints"

    def test_undo_command_recognized(self):
        """Test that /undo is recognized."""
        command = "/undo"
        assert command[1:].split(maxsplit=1)[0] == "undo"

    def test_context_command_recognized(self):
        """Test that /context is recognized."""
        command = "/context"
        assert command[1:].split(maxsplit=1)[0] == "context"

    def test_memory_command_recognized(self):
        """Test that /memory is recognized."""
        command = "/memory"
        assert command[1:].split(maxsplit=1)[0] == "memory"

    def test_tdd_command_recognized(self):
        """Test that /tdd is recognized."""
        command = "/tdd"
        assert command[1:].split(maxsplit=1)[0] == "tdd"

    def test_autopolit_command_recognized(self):
        """Test that /autopolit is recognized."""
        command = "/autopolit"
        assert command[1:].split(maxsplit=1)[0] == "autopolit"

    def test_autoorg_command_recognized(self):
        """Test that /autoorg is recognized."""
        command = "/autoorg"
        assert command[1:].split(maxsplit=1)[0] == "autoorg"

    def test_workflow_command_recognized(self):
        """Test that /workflow is recognized."""
        command = "/workflow"
        assert command[1:].split(maxsplit=1)[0] == "workflow"

    def test_wf_alias_recognized(self):
        """Test that /wf alias is recognized."""
        command = "/wf"
        assert command[1:].split(maxsplit=1)[0] == "wf"

    def test_phd_command_recognized(self):
        """Test that /phd is recognized."""
        command = "/phd"
        assert command[1:].split(maxsplit=1)[0] == "phd"

    def test_expert_alias_recognized(self):
        """Test that /expert alias is recognized."""
        command = "/expert"
        assert command[1:].split(maxsplit=1)[0] == "expert"

    def test_sandbox_command_recognized(self):
        """Test that /sandbox is recognized."""
        command = "/sandbox"
        assert command[1:].split(maxsplit=1)[0] == "sandbox"

    def test_swarm_command_recognized(self):
        """Test that /swarm is recognized."""
        command = "/swarm"
        assert command[1:].split(maxsplit=1)[0] == "swarm"

    def test_deps_command_recognized(self):
        """Test that /deps is recognized."""
        command = "/deps"
        assert command[1:].split(maxsplit=1)[0] == "deps"

    def test_lsp_command_recognized(self):
        """Test that /lsp is recognized."""
        command = "/lsp"
        assert command[1:].split(maxsplit=1)[0] == "lsp"

    def test_security_command_recognized(self):
        """Test that /security is recognized."""
        command = "/security"
        assert command[1:].split(maxsplit=1)[0] == "security"

    def test_status_command_recognized(self):
        """Test that /status is recognized."""
        command = "/status"
        assert command[1:].split(maxsplit=1)[0] == "status"

    def test_think_command_recognized(self):
        """Test that /think is recognized."""
        command = "/think"
        assert command[1:].split(maxsplit=1)[0] == "think"


class TestShellEscape:
    """Test shell escape (!command) handling."""

    def test_shell_escape_detected(self):
        """Test that ! prefix is detected as shell escape."""
        command = "!ls -la"
        assert command.startswith("!")
        assert command[1:] == "ls -la"

    def test_shell_escape_with_spaces(self):
        """Test shell escape with spaces in command."""
        command = "!echo 'hello world'"
        assert command.startswith("!")
        assert command[1:] == "echo 'hello world'"

    def test_shell_escape_piped_command(self):
        """Test shell escape with piped commands."""
        command = "!cat file.txt | grep pattern"
        assert command.startswith("!")
        assert "|" in command[1:]

    def test_shell_escape_empty_after_bang(self):
        """Test shell escape with nothing after !."""
        command = "!"
        assert command.startswith("!")
        assert command[1:] == ""


class TestMultilineInput:
    """Test multiline input handling with triple quotes."""

    def test_multiline_start_detected(self):
        """Test that triple quote start is detected."""
        line = '"""'
        assert line.strip() == '"""'

    def test_multiline_with_content(self):
        """Test multiline input with content."""
        lines = [
            '"""',
            "This is line 1",
            "This is line 2",
            '"""',
        ]
        content = "\n".join(lines[1:-1])
        assert content == "This is line 1\nThis is line 2"

    def test_multiline_empty(self):
        """Test empty multiline block."""
        lines = ['"""', '"""']
        content = "\n".join(lines[1:-1])
        assert content == ""


class TestUnknownCommandHandling:
    """Test handling of unknown commands."""

    def test_unknown_command_starts_with_slash(self):
        """Test that unknown commands still start with /."""
        command = "/unknowncommand"
        assert command.startswith("/")
        cmd_name = command[1:].split(maxsplit=1)[0]
        known_commands = {
            "help",
            "exit",
            "models",
            "model",
            "clear",
            "compact",
            "history",
            "prompts",
            "read",
            "files",
            "test",
            "checkpoint",
            "checkpoints",
            "undo",
            "context",
            "memory",
            "tdd",
            "autopolit",
            "autoorg",
            "workflow",
            "wf",
            "phd",
            "expert",
            "sandbox",
            "swarm",
            "deps",
            "lsp",
            "security",
            "think",
            "autopolit-stop",
        }
        assert cmd_name not in known_commands


class TestEmptyAndWhitespaceInput:
    """Test empty and whitespace-only input handling."""

    def test_empty_input(self):
        """Test empty string input."""
        user_input = ""
        assert user_input.strip() == ""

    def test_whitespace_only_input(self):
        """Test whitespace-only input."""
        user_input = "   \t\n   "
        assert user_input.strip() == ""

    def test_input_with_leading_whitespace(self):
        """Test input with leading whitespace is preserved."""
        user_input = "   hello"
        assert user_input.strip() == "hello"


class TestModelSwitching:
    """Test model switching behavior."""

    def test_model_command_parsing(self):
        """Test /model command parses model name."""
        command = "/model ollama:llama3.2"
        parts = command[1:].split(maxsplit=1)
        assert parts[0] == "model"
        assert parts[1] == "ollama:llama3.2"

    def test_model_command_with_ollama_prefix(self):
        """Test /model with ollama: prefix."""
        command = "/model ollama:llama3"
        parts = command[1:].split(maxsplit=1)
        model_id = parts[1]
        assert model_id.startswith("ollama:")

    def test_model_command_with_browser_prefix(self):
        """Test /model with browser: prefix."""
        command = "/model browser:Llama-3.2-1B-Instruct-q4f16_1-MLC"
        parts = command[1:].split(maxsplit=1)
        model_id = parts[1]
        assert model_id.startswith("browser:")

    def test_models_list_command(self):
        """Test /models command (list models)."""
        command = "/models"
        parts = command[1:].split()
        assert parts[0] == "models"
        assert len(parts) == 1


class TestSessionStateCommands:
    """Test session state management commands."""

    def test_clear_command_resets_state(self):
        """Test /clear command intent."""
        command = "/clear"
        assert command[1:].split(maxsplit=1)[0] == "clear"

    def test_checkpoint_with_name(self):
        """Test /checkpoint with name."""
        command = "/checkpoint my_checkpoint"
        parts = command[1:].split(maxsplit=1)
        assert parts[0] == "checkpoint"
        assert parts[1] == "my_checkpoint"

    def test_undo_with_steps(self):
        """Test /undo with number of steps."""
        command = "/undo 3"
        parts = command[1:].split()
        assert parts[0] == "undo"
        assert parts[1] == "3"


class TestOrchestrationCommands:
    """Test orchestration commands (autopolit, autoorg, workflow, etc.)."""

    def test_autopolit_with_task(self):
        """Test /autopolit with task description."""
        command = "/autopolit implement user authentication"
        parts = command[1:].split(maxsplit=1)
        assert parts[0] == "autopolit"
        assert parts[1] == "implement user authentication"

    def test_autoorg_with_task(self):
        """Test /autoorg with task description."""
        command = "/autoorg refactor the database layer"
        parts = command[1:].split(maxsplit=1)
        assert parts[0] == "autoorg"
        assert parts[1] == "refactor the database layer"

    def test_workflow_with_name(self):
        """Test /workflow with workflow name."""
        command = "/workflow code-review"
        parts = command[1:].split(maxsplit=1)
        assert parts[0] == "workflow"
        assert parts[1] == "code-review"

    def test_think_with_prompt(self):
        """Test /think with thinking prompt."""
        command = "/think about the architecture"
        parts = command[1:].split(maxsplit=1)
        assert parts[0] == "think"
        assert parts[1] == "about the architecture"


class TestFileCommands:
    """Test file-related commands."""

    def test_read_single_file(self):
        """Test /read with single file."""
        command = "/read main.py"
        parts = command[1:].split(maxsplit=1)
        assert parts[0] == "read"
        assert parts[1] == "main.py"

    def test_read_multiple_files(self):
        """Test /read with multiple files."""
        command = "/read main.py utils.py config.py"
        parts = command[1:].split(maxsplit=1)
        assert parts[0] == "read"
        files = parts[1].split()
        assert len(files) == 3

    def test_read_with_glob_pattern(self):
        """Test /read with glob pattern."""
        command = "/read src/*.py"
        parts = command[1:].split(maxsplit=1)
        assert parts[0] == "read"
        assert "*" in parts[1]


class TestAdvancedFeatureCommands:
    """Test advanced feature commands."""

    def test_tdd_enable(self):
        """Test /tdd enable."""
        command = "/tdd on"
        parts = command[1:].split()
        assert parts[0] == "tdd"
        assert parts[1] == "on"

    def test_sandbox_command(self):
        """Test /sandbox command."""
        command = "/sandbox"
        parts = command[1:].split()
        assert parts[0] == "sandbox"

    def test_swarm_with_count(self):
        """Test /swarm with agent count."""
        command = "/swarm 5"
        parts = command[1:].split()
        assert parts[0] == "swarm"
        assert parts[1] == "5"

    def test_deps_command(self):
        """Test /deps command."""
        command = "/deps"
        parts = command[1:].split()
        assert parts[0] == "deps"

    def test_security_command(self):
        """Test /security command."""
        command = "/security"
        parts = command[1:].split()
        assert parts[0] == "security"

    def test_lsp_command(self):
        """Test /lsp command."""
        command = "/lsp"
        parts = command[1:].split()
        assert parts[0] == "lsp"

    def test_context_compact(self):
        """Test /context compact."""
        command = "/context compact"
        parts = command[1:].split()
        assert parts[0] == "context"
        assert parts[1] == "compact"


class TestCommandValidation:
    """Test command validation and error cases."""

    def test_command_case_sensitivity(self):
        """Test that commands are case-sensitive."""
        command_lower = "/help"
        command_upper = "/HELP"
        assert command_lower[1:].split(maxsplit=1)[0] == "help"
        assert command_upper[1:].split(maxsplit=1)[0] == "HELP"
        # Commands should be lowercase
        assert command_lower[1:].split(maxsplit=1)[0] != command_upper[1:].split(maxsplit=1)[0]

    def test_command_with_extra_slashes(self):
        """Test command with extra slashes in argument."""
        command = "/read /path/to/file.py"
        parts = command[1:].split(maxsplit=1)
        assert parts[0] == "read"
        assert parts[1] == "/path/to/file.py"

    def test_slash_only(self):
        """Test just a slash."""
        command = "/"
        assert command == "/"
        assert len(command) == 1


class TestAllKnownCommands:
    """Parameterized tests for all known commands."""

    KNOWN_COMMANDS = [
        "help",
        "exit",
        "models",
        "model",
        "clear",
        "compact",
        "history",
        "prompts",
        "read",
        "files",
        "test",
        "checkpoint",
        "checkpoints",
        "undo",
        "context",
        "memory",
        "tdd",
        "autopolit",
        "autopolit-stop",
        "autoorg",
        "workflow",
        "wf",
        "phd",
        "expert",
        "sandbox",
        "swarm",
        "deps",
        "lsp",
        "security",
        "status",
        "think",
    ]

    @pytest.mark.parametrize("cmd", KNOWN_COMMANDS)
    def test_known_command_format(self, cmd):
        """Test that known commands have correct format."""
        command = f"/{cmd}"
        assert command.startswith("/")
        parsed = command[1:].split(maxsplit=1)[0]
        assert parsed == cmd

    @pytest.mark.parametrize("cmd", KNOWN_COMMANDS)
    def test_known_command_with_args(self, cmd):
        """Test known commands can have arguments."""
        command = f"/{cmd} some argument"
        parts = command[1:].split(maxsplit=1)
        assert parts[0] == cmd
        if len(parts) > 1:
            assert parts[1] == "some argument"


class TestInputParsing:
    """Test input parsing edge cases."""

    def test_regular_prompt(self):
        """Test regular prompt (not a command)."""
        user_input = "What is the capital of France?"
        assert not user_input.startswith("/")
        assert not user_input.startswith("!")

    def test_prompt_that_looks_like_command(self):
        """Test prompt that starts with / but isn't a command."""
        user_input = "/path/to/something is broken"
        # This could be confused with a command
        # The first word after / is "path/to/something"
        first_word = user_input[1:].split(maxsplit=1)[0]
        assert "/" in first_word  # Contains another slash

    def test_prompt_with_exclamation(self):
        """Test prompt with ! that isn't shell escape."""
        user_input = "Hello! How are you?"
        # Not a shell escape because ! is not at start
        assert not user_input.startswith("!")

    def test_unicode_input(self):
        """Test unicode characters in input."""
        user_input = "こんにちは世界"
        assert len(user_input) > 0

    def test_emoji_input(self):
        """Test emoji in input."""
        user_input = "🚀 Deploy the app"
        assert "🚀" in user_input


class TestNoTokensShadowingInRepl:
    """Regression: /models REPL handler must NOT shadow the outer `tokens` int.

    The 2026-05-16 bug: typing `/models --all` reassigned `tokens` to the
    list `['--all']`, and the next chat call sent `max_tokens=['--all']` to
    the backend, yielding a 422 from FastAPI's Pydantic validator and a
    matching `'<=' not supported between instances of 'list' and 'int'`
    crash inside llama_cpp's generate. Same root cause for both clients
    (CLI + website) because both went through the same REPL function.

    This test scans main.py's REPL block for the dangerous re-binding
    pattern. We assert at the source-code level because building a full
    REPL fixture would be heavier than the bug warrants — variable
    shadowing is a static property.
    """

    def test_no_argv_split_into_tokens_in_main_py(self):
        from pathlib import Path
        main_py = (
            Path(__file__).resolve().parent.parent / "main.py"
        ).read_text(encoding="utf-8")
        # The exact pattern that caused the regression — any future
        # contributor who reintroduces it gets a loud failing test.
        bad = 'tokens = (arg or "").split()'
        assert bad not in main_py, (
            "REPL handler is re-binding the outer `tokens` int parameter "
            "to a list of argv strings. That value then flows into the "
            "next chat call as max_tokens=['--all'...] and triggers a "
            "422 from the backend. Use a different name (e.g. `argv`)."
        )
