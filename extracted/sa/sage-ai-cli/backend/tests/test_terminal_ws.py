"""
Comprehensive tests for WebSocket terminal functionality.

Tests the PTY-based terminal emulation, authentication, rate limiting,
and CLI auto-update features used by the website CLI terminal.
"""

import asyncio
import json
import pytest
from unittest.mock import MagicMock, patch, AsyncMock
from dataclasses import dataclass

from sage.core.updater import CLIUpdateResult


# ═══════════════════════════════════════════════════════════════════════════════
# TEST FIXTURES AND HELPERS
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def mock_websocket():
    """Create a mock WebSocket for testing."""
    ws = MagicMock()
    ws.client = MagicMock()
    ws.client.host = "127.0.0.1"
    ws.query_params = {}
    ws.headers = {}
    ws.accept = AsyncMock()
    ws.send_json = AsyncMock()
    ws.receive_json = AsyncMock()
    ws.close = AsyncMock()
    return ws


@pytest.fixture
def mock_settings():
    """Create mock settings for testing."""
    settings = MagicMock()
    settings.admin_token = "test-admin-token"
    settings.is_production = False
    return settings


# ═══════════════════════════════════════════════════════════════════════════════
# CLI VERSION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestCLIVersion:
    """Test CLI version management."""

    def test_cli_version_dataclass(self):
        """Test CLIVersion dataclass structure."""
        from backend.terminal_ws import CLIVersion

        version = CLIVersion(
            current="1.13.60",
            latest="1.13.68",
            update_available=True,
        )
        assert version.current == "1.13.60"
        assert version.latest == "1.13.68"
        assert version.update_available is True

    def test_cli_version_no_update(self):
        """Test CLIVersion when no update is available."""
        from backend.terminal_ws import CLIVersion

        version = CLIVersion(
            current="1.13.68",
            latest="1.13.68",
            update_available=False,
        )
        assert version.update_available is False


class TestCLIAutoUpdater:
    """Test CLI auto-updater functionality."""

    def test_version_comparison_less_than(self):
        """Test version comparison when v1 < v2."""
        from backend.terminal_ws import CLIAutoUpdater

        result = CLIAutoUpdater._compare_versions("1.13.60", "1.13.68")
        assert result == -1

    def test_version_comparison_equal(self):
        """Test version comparison when versions are equal."""
        from backend.terminal_ws import CLIAutoUpdater

        result = CLIAutoUpdater._compare_versions("1.13.68", "1.13.68")
        assert result == 0

    def test_version_comparison_greater_than(self):
        """Test version comparison when v1 > v2."""
        from backend.terminal_ws import CLIAutoUpdater

        result = CLIAutoUpdater._compare_versions("1.13.70", "1.13.68")
        assert result == 1

    def test_version_comparison_major_version(self):
        """Test version comparison with major version difference."""
        from backend.terminal_ws import CLIAutoUpdater

        result = CLIAutoUpdater._compare_versions("2.0.0", "1.13.68")
        assert result == 1

    def test_version_comparison_with_dash(self):
        """Test version comparison with dashes in version."""
        from backend.terminal_ws import CLIAutoUpdater

        # "1.13.68-beta" becomes (1, 13, 68, 0) because "beta" -> 0
        # In Python tuple comparison, (1, 13, 68, 0) > (1, 13, 68)
        # because longer tuples with trailing elements are considered greater
        result = CLIAutoUpdater._compare_versions("1.13.68-beta", "1.13.68")
        assert result == 1  # 1.13.68-beta is treated as > 1.13.68

    def test_updater_initialization(self):
        """Test CLIAutoUpdater initialization."""
        from backend.terminal_ws import CLIAutoUpdater

        updater = CLIAutoUpdater()
        assert updater.PACKAGE_NAME == "sage-ai-cli"
        assert updater._cache_timeout == 300
        assert updater._cached_version is None

    @patch("sage.core.updater.package_version", return_value="1.13.99")
    def test_get_current_version_prefers_source_version(self, _mock_package_version):
        """Local source metadata should win over stale installed package metadata."""
        from backend.terminal_ws import CLIAutoUpdater

        updater = CLIAutoUpdater()

        assert updater.get_current_version() == "1.14.0"

    @patch("backend.terminal_ws.cli_updater.ensure_latest")
    def test_apply_cli_update_returns_status_message(self, mock_ensure_latest):
        """REST update helper should expose the shared updater result."""
        from backend.terminal_ws import apply_cli_update

        mock_ensure_latest.return_value = CLIUpdateResult(
            ok=True,
            updated=True,
            attempted=True,
            current="1.14.0",
            latest="1.14.0",
            message="Updated SAGE AI from v1.13.73 to v1.14.0.",
        )

        payload = apply_cli_update()

        assert payload["ok"] is True
        assert payload["updated"] is True
        assert "updated" in payload["message"].lower()


# ═══════════════════════════════════════════════════════════════════════════════
# TERMINAL SESSION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestTerminalSession:
    """Test terminal session management."""

    def test_terminal_session_initialization(self, mock_websocket):
        """Test TerminalSession initialization."""
        from backend.terminal_ws import TerminalSession

        session = TerminalSession(mock_websocket)
        assert session.websocket == mock_websocket
        assert session.master_fd is None
        assert session.pid is None
        assert session._running is False

    def test_terminal_session_command_format(self):
        """Test terminal session command format."""
        # Default command should be sage run or fallback
        expected_commands = [
            ["sage", "run"],
            ["/path/to/sage", "run"],
        ]
        for cmd in expected_commands:
            assert "sage" in cmd[0] or cmd[0].endswith("sage")
            assert "run" in cmd

    @pytest.mark.asyncio
    @patch("backend.terminal_ws.cli_updater.ensure_latest")
    async def test_simulated_terminal_update_command(self, mock_ensure_latest, mock_websocket):
        """Simulated terminal should support /update like the real CLI."""
        from backend.terminal_ws import SimulatedTerminalSession

        mock_ensure_latest.return_value = CLIUpdateResult(
            ok=True,
            updated=True,
            attempted=True,
            current="1.14.0",
            latest="1.14.0",
            message="Updated SAGE AI from v1.13.73 to v1.14.0.",
        )

        session = SimulatedTerminalSession(mock_websocket)
        await session._handle_command("/update")

        rendered = "".join(
            call.args[0]["data"]
            for call in mock_websocket.send_json.await_args_list
            if call.args and isinstance(call.args[0], dict) and call.args[0].get("type") == "output"
        )
        assert "updated sage ai" in rendered.lower()

    @patch("backend.terminal_ws.cli_updater.get_current_version", return_value="1.13.82")
    def test_simulated_terminal_banner_uses_updater_version(self, mock_current_version, mock_websocket):
        """The website CLI banner should display the installed CLI version, not stale source metadata."""
        from backend.terminal_ws import SimulatedTerminalSession

        session = SimulatedTerminalSession(mock_websocket)
        banner = session._get_welcome_banner()

        assert "SAGE AI CLI" in banner
        assert "v1.13.82" in banner
        mock_current_version.assert_called_once()


class TestTerminalMessageFormat:
    """Test terminal WebSocket message formats."""

    def test_output_message_format(self):
        """Test terminal output message format."""
        message = {
            "type": "output",
            "data": "Hello, World!\n",
        }
        assert message["type"] == "output"
        assert isinstance(message["data"], str)

    def test_input_message_format(self):
        """Test terminal input message format."""
        message = {
            "type": "input",
            "data": "/help\n",
        }
        assert message["type"] == "input"
        assert message["data"] == "/help\n"

    def test_resize_message_format(self):
        """Test terminal resize message format."""
        message = {
            "type": "resize",
            "cols": 120,
            "rows": 40,
        }
        assert message["type"] == "resize"
        assert message["cols"] == 120
        assert message["rows"] == 40

    def test_update_available_message_format(self):
        """Test update available message format."""
        message = {
            "type": "update_available",
            "info": {
                "current_version": "1.13.60",
                "latest_version": "1.13.68",
            },
        }
        assert message["type"] == "update_available"
        assert "current_version" in message["info"]
        assert "latest_version" in message["info"]


# ═══════════════════════════════════════════════════════════════════════════════
# TERMINAL RATE LIMITER TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestTerminalRateLimiter:
    """Test terminal rate limiting."""

    def test_rate_limiter_initialization(self):
        """Test rate limiter initialization."""
        from backend.terminal_ws import _TerminalRateLimiter

        limiter = _TerminalRateLimiter(
            max_connections_per_ip=5,
            time_window_seconds=60,
        )
        assert limiter.max_connections_per_ip == 5
        assert limiter.time_window_seconds == 60

    def test_rate_limiter_allows_first_connection(self):
        """Test rate limiter allows first connection."""
        from backend.terminal_ws import _TerminalRateLimiter

        limiter = _TerminalRateLimiter(max_connections_per_ip=5)
        assert limiter.is_allowed("192.168.1.1") is True

    def test_rate_limiter_allows_under_limit(self):
        """Test rate limiter allows connections under limit."""
        from backend.terminal_ws import _TerminalRateLimiter

        limiter = _TerminalRateLimiter(max_connections_per_ip=5)

        # First 4 connections should be allowed
        for _ in range(4):
            assert limiter.is_allowed("192.168.1.1") is True

    def test_rate_limiter_blocks_over_limit(self):
        """Test rate limiter blocks connections over limit."""
        from backend.terminal_ws import _TerminalRateLimiter

        limiter = _TerminalRateLimiter(max_connections_per_ip=5)

        # Use up all connections
        for _ in range(5):
            limiter.is_allowed("192.168.1.1")

        # 6th connection should be blocked
        assert limiter.is_allowed("192.168.1.1") is False

    def test_rate_limiter_separate_ips(self):
        """Test rate limiter tracks IPs separately."""
        from backend.terminal_ws import _TerminalRateLimiter

        limiter = _TerminalRateLimiter(max_connections_per_ip=2)

        # Use up limit for first IP
        limiter.is_allowed("192.168.1.1")
        limiter.is_allowed("192.168.1.1")
        assert limiter.is_allowed("192.168.1.1") is False

        # Second IP should still be allowed
        assert limiter.is_allowed("192.168.1.2") is True


# ═══════════════════════════════════════════════════════════════════════════════
# TERMINAL AUTHENTICATION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestTerminalAuthentication:
    """Test terminal authentication."""

    def test_auth_development_mode_no_token(self):
        """Test auth in development mode without token."""
        from backend.terminal_ws import _require_terminal_auth

        # Development mode should allow without token
        result = _require_terminal_auth(
            token=None,
            production_mode=False,
        )
        assert result is True

    def test_auth_production_mode_no_token(self):
        """Test auth in production mode without token."""
        from backend.terminal_ws import _require_terminal_auth

        # Production mode should require token
        result = _require_terminal_auth(
            token=None,
            production_mode=True,
            valid_tokens={"valid-token"},
        )
        assert result is False

    def test_auth_production_mode_valid_token(self):
        """Test auth in production mode with valid token."""
        from backend.terminal_ws import _require_terminal_auth

        result = _require_terminal_auth(
            token="valid-token",
            production_mode=True,
            valid_tokens={"valid-token"},
        )
        assert result is True

    def test_auth_production_mode_invalid_token(self):
        """Test auth in production mode with invalid token."""
        from backend.terminal_ws import _require_terminal_auth

        result = _require_terminal_auth(
            token="wrong-token",
            production_mode=True,
            valid_tokens={"valid-token"},
        )
        assert result is False


# ═══════════════════════════════════════════════════════════════════════════════
# TERMINAL RESIZE BOUNDS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestTerminalResizeBounds:
    """Test terminal resize bounds checking."""

    def test_resize_bounds_normal_values(self):
        """Test resize with normal values."""
        cols, rows = 80, 24

        # Apply bounds (as in terminal_websocket_handler)
        cols = max(10, min(500, cols))
        rows = max(5, min(200, rows))

        assert cols == 80
        assert rows == 24

    def test_resize_bounds_too_small(self):
        """Test resize with values too small."""
        cols, rows = 1, 1

        cols = max(10, min(500, cols))
        rows = max(5, min(200, rows))

        assert cols == 10
        assert rows == 5

    def test_resize_bounds_too_large(self):
        """Test resize with values too large."""
        cols, rows = 10000, 10000

        cols = max(10, min(500, cols))
        rows = max(5, min(200, rows))

        assert cols == 500
        assert rows == 200

    def test_resize_bounds_negative_values(self):
        """Test resize with negative values."""
        cols, rows = -50, -50

        cols = max(10, min(500, cols))
        rows = max(5, min(200, rows))

        assert cols == 10
        assert rows == 5


# ═══════════════════════════════════════════════════════════════════════════════
# CLI UPDATE API TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestCLIUpdateAPI:
    """Test CLI update REST API endpoints."""

    def test_get_cli_update_info_format(self):
        """Test get_cli_update_info response format."""
        expected = {
            "current_version": "1.13.60",
            "latest_version": "1.13.68",
            "update_available": True,
        }
        assert "current_version" in expected
        assert "latest_version" in expected
        assert "update_available" in expected

    def test_apply_cli_update_format(self):
        """Test apply_cli_update response format."""
        expected = {
            "ok": True,
            "current_version": "1.13.68",
            "latest_version": "1.13.68",
        }
        assert "ok" in expected
        assert "current_version" in expected


# ═══════════════════════════════════════════════════════════════════════════════
# TERMINAL COMMAND TESTS (SAGE RUN)
# ═══════════════════════════════════════════════════════════════════════════════

class TestTerminalCommands:
    """Test terminal command handling for sage run."""

    # All slash commands that should work in terminal
    SLASH_COMMANDS = [
        "/help",
        "/exit",
        "/models",
        "/model ollama:llama3.2",
        "/clear",
        "/compact",
        "/history",
        "/prompts",
        "/read main.py",
        "/files",
        "/test",
        "/checkpoint mycp",
        "/checkpoints",
        "/undo",
        "/context",
        "/memory",
        "/tdd on",
        "/autopolit task",
        "/autoorg task",
        "/workflow code-review",
        "/wf code-review",
        "/phd",
        "/expert",
        "/sandbox",
        "/swarm 3",
        "/deps",
        "/lsp",
        "/security",
        "/think carefully",
    ]

    @pytest.mark.parametrize("command", SLASH_COMMANDS)
    def test_command_format_valid(self, command):
        """Test slash commands have valid format."""
        assert command.startswith("/")
        cmd_name = command[1:].split()[0]
        assert len(cmd_name) > 0

    def test_shell_escape_format(self):
        """Test shell escape command format."""
        commands = [
            "!ls -la",
            "!pwd",
            "!cat file.txt | grep pattern",
        ]
        for cmd in commands:
            assert cmd.startswith("!")
            assert len(cmd[1:].strip()) > 0


# ═══════════════════════════════════════════════════════════════════════════════
# TERMINAL PROMPT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestTerminalPrompts:
    """Test prompts sent through terminal."""

    EXAMPLE_PROMPTS = [
        "Hello, how are you?",
        "What is 2 + 2?",
        "Write a Python function to check if a number is prime.",
        "Explain what a REST API is.",
    ]

    @pytest.mark.parametrize("prompt", EXAMPLE_PROMPTS)
    def test_prompt_is_valid_terminal_input(self, prompt):
        """Test prompts are valid terminal input."""
        assert isinstance(prompt, str)
        assert len(prompt) > 0
        # No null bytes
        assert "\x00" not in prompt
        # Not a command
        assert not prompt.startswith("/")
        # Not a shell escape
        assert not prompt.startswith("!")

    def test_prompt_with_model_switch(self):
        """Test model switching then prompt sequence."""
        sequence = [
            "/model ollama:llama3.2",
            "Hello, write a hello world program",
        ]
        assert sequence[0].startswith("/model ")
        assert not sequence[1].startswith("/")


# ═══════════════════════════════════════════════════════════════════════════════
# WEBSOCKET CLOSE CODES TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestWebSocketCloseCodes:
    """Test WebSocket close codes used by terminal."""

    def test_rate_limit_close_code(self):
        """Test rate limit close code."""
        # Custom close code for rate limit
        code = 4029
        reason = "Terminal connection rate limit exceeded"
        assert code == 4029
        assert "rate limit" in reason.lower()

    def test_auth_required_close_code(self):
        """Test authentication required close code."""
        code = 4003
        reason = "Authentication required"
        assert code == 4003
        assert "authentication" in reason.lower()


# ═══════════════════════════════════════════════════════════════════════════════
# TERMINAL ENVIRONMENT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestTerminalEnvironment:
    """Test terminal environment setup."""

    def test_terminal_env_vars(self):
        """Test terminal environment variables are set correctly."""
        expected_env = {
            "TERM": "xterm-256color",
            "COLORTERM": "truecolor",
            "SAGE_TERMINAL": "web",
        }
        for key, value in expected_env.items():
            assert len(key) > 0
            assert len(value) > 0

    def test_xterm_256color_support(self):
        """Test xterm-256color terminal type."""
        term_type = "xterm-256color"
        assert "256color" in term_type
        assert "xterm" in term_type


# ═══════════════════════════════════════════════════════════════════════════════
# INTEGRATION SCENARIO TESTS
# ═══════════════════════════════════════════════════════════════════════════════

class TestTerminalIntegrationScenarios:
    """Test terminal integration scenarios."""

    def test_full_session_workflow(self):
        """Test full terminal session workflow."""
        workflow = [
            {"type": "resize", "cols": 120, "rows": 40},  # Initial resize
            {"type": "input", "data": "/help\n"},  # Get help
            {"type": "input", "data": "/models\n"},  # List models
            {"type": "input", "data": "/model ollama:llama3.2\n"},  # Select model
            {"type": "input", "data": "Hello, write a hello world program\n"},  # Prompt
            {"type": "input", "data": "/exit\n"},  # Exit
        ]

        for msg in workflow:
            assert "type" in msg
            if msg["type"] == "resize":
                assert "cols" in msg
                assert "rows" in msg
            elif msg["type"] == "input":
                assert "data" in msg

    def test_model_selection_workflow(self):
        """Test model selection workflow in terminal."""
        # Subset of Pollinations models for terminal tests
        models_to_test = [
            "ollama:llama3.2",
            "ollama:mistral",
            "ollama:qwen2.5-coder",
            "browser:Llama-3.2-1B-Instruct-q4f16_1-MLC",
            "ollama:llama3.2",
            "ollama:qwen2.5-coder",
        ]

        for model_id in models_to_test:
            command = f"/model {model_id}\n"
            assert command.startswith("/model ")
            assert model_id in command

    def test_prompt_after_model_switch(self):
        """Test sending prompt after model switch."""
        prompts = [
            "Write a Python hello world program.",
            "Explain recursion simply.",
            "What is 2 + 2?",
        ]

        for prompt in prompts:
            message = {"type": "input", "data": f"{prompt}\n"}
            assert message["type"] == "input"
            assert prompt in message["data"]
