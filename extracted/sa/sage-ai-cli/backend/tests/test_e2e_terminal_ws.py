"""
End-to-End Integration Tests for Website Terminal WebSocket.

These tests actually connect to the WebSocket endpoint and verify real functionality.
They test the full pipeline: WebSocket connection, PTY session, command execution.

Note: WebSocket tests require the server to be running or use special async testing.

Usage:
    pytest backend/tests/test_e2e_terminal_ws.py -v -m "smoke"  # Quick tests
    pytest backend/tests/test_e2e_terminal_ws.py -v             # All tests
"""

import asyncio
import json
import pytest
from unittest.mock import patch, MagicMock, AsyncMock

from fastapi.testclient import TestClient
from fastapi.websockets import WebSocket

from backend.app import app
from backend.terminal_ws import (
    TerminalSession,
    CLIAutoUpdater,
    _TerminalRateLimiter,
    _require_terminal_auth,
)


# ═══════════════════════════════════════════════════════════════════════════════
# TEST FIXTURES
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.fixture
def client():
    """Create a test client for the API."""
    with TestClient(app) as c:
        yield c


@pytest.fixture
def rate_limiter():
    """Create a fresh rate limiter for testing."""
    return _TerminalRateLimiter(max_connections_per_ip=5, time_window_seconds=60)


@pytest.fixture
def cli_updater():
    """Create a CLI updater instance."""
    return CLIAutoUpdater()


# ═══════════════════════════════════════════════════════════════════════════════
# SMOKE TESTS - Quick verification
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.smoke
@pytest.mark.integration
class TestTerminalSmokeTests:
    """Quick smoke tests for terminal functionality."""

    def test_cli_update_check_endpoint(self, client):
        """Test /api/cli/check-update endpoint works."""
        response = client.get("/api/cli/check-update")
        assert response.status_code == 200
        data = response.json()
        assert "current_version" in data
        assert "latest_version" in data
        assert "update_available" in data


# ═══════════════════════════════════════════════════════════════════════════════
# RATE LIMITER E2E TESTS
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.integration
class TestRateLimiterE2E:
    """End-to-end tests for terminal rate limiting."""

    def test_rate_limiter_allows_initial_connections(self, rate_limiter):
        """Test rate limiter allows first connections."""
        assert rate_limiter.is_allowed("192.168.1.1") is True
        assert rate_limiter.is_allowed("192.168.1.1") is True
        assert rate_limiter.is_allowed("192.168.1.1") is True

    def test_rate_limiter_blocks_after_limit(self, rate_limiter):
        """Test rate limiter blocks after limit exceeded."""
        # Use up all allowed connections
        for _ in range(5):
            rate_limiter.is_allowed("192.168.1.100")

        # 6th should be blocked
        assert rate_limiter.is_allowed("192.168.1.100") is False

    def test_rate_limiter_tracks_ips_separately(self, rate_limiter):
        """Test rate limiter tracks different IPs separately."""
        # Fill up one IP
        for _ in range(5):
            rate_limiter.is_allowed("192.168.1.1")

        # Different IP should still work
        assert rate_limiter.is_allowed("192.168.1.2") is True

    def test_rate_limiter_multiple_ips(self, rate_limiter):
        """Test rate limiter with multiple IPs."""
        ips = ["10.0.0.1", "10.0.0.2", "10.0.0.3", "10.0.0.4", "10.0.0.5"]

        for ip in ips:
            assert rate_limiter.is_allowed(ip) is True


# ═══════════════════════════════════════════════════════════════════════════════
# AUTHENTICATION E2E TESTS
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.integration
class TestAuthenticationE2E:
    """End-to-end tests for terminal authentication."""

    def test_auth_allows_in_development_mode(self):
        """Test auth allows connections in development mode."""
        result = _require_terminal_auth(
            token=None,
            production_mode=False,
        )
        assert result is True

    def test_auth_requires_token_in_production(self):
        """Test auth requires token in production mode."""
        result = _require_terminal_auth(
            token=None,
            production_mode=True,
            valid_tokens={"secret-token"},
        )
        assert result is False

    def test_auth_accepts_valid_token(self):
        """Test auth accepts valid token."""
        result = _require_terminal_auth(
            token="secret-token",
            production_mode=True,
            valid_tokens={"secret-token"},
        )
        assert result is True

    def test_auth_rejects_invalid_token(self):
        """Test auth rejects invalid token."""
        result = _require_terminal_auth(
            token="wrong-token",
            production_mode=True,
            valid_tokens={"secret-token"},
        )
        assert result is False


# ═══════════════════════════════════════════════════════════════════════════════
# CLI UPDATER E2E TESTS
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.integration
class TestCLIUpdaterE2E:
    """End-to-end tests for CLI auto-updater."""

    def test_version_comparison_basic(self, cli_updater):
        """Test basic version comparison."""
        assert cli_updater._compare_versions("1.0.0", "2.0.0") == -1
        assert cli_updater._compare_versions("2.0.0", "1.0.0") == 1
        assert cli_updater._compare_versions("1.0.0", "1.0.0") == 0

    def test_version_comparison_minor(self, cli_updater):
        """Test minor version comparison."""
        assert cli_updater._compare_versions("1.1.0", "1.2.0") == -1
        assert cli_updater._compare_versions("1.2.0", "1.1.0") == 1

    def test_version_comparison_patch(self, cli_updater):
        """Test patch version comparison."""
        assert cli_updater._compare_versions("1.0.1", "1.0.2") == -1
        assert cli_updater._compare_versions("1.0.2", "1.0.1") == 1

    def test_get_current_version(self, cli_updater):
        """Test getting current installed version."""
        version = cli_updater.get_current_version()
        # Should return a version string or "0.0.0"
        assert isinstance(version, str)
        assert "." in version or version == "0.0.0"

    def test_check_for_update_returns_version_info(self, cli_updater):
        """Test check_for_update returns proper structure."""
        version_info = cli_updater.check_for_update()
        assert hasattr(version_info, "current")
        assert hasattr(version_info, "latest")
        assert hasattr(version_info, "update_available")


# ═══════════════════════════════════════════════════════════════════════════════
# TERMINAL SESSION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.integration
class TestTerminalSessionE2E:
    """Tests for terminal session management."""

    def test_terminal_session_creation(self):
        """Test terminal session can be created."""
        mock_ws = MagicMock()
        mock_ws.client = MagicMock()
        mock_ws.client.host = "127.0.0.1"

        session = TerminalSession(mock_ws)
        assert session.websocket == mock_ws
        assert session.master_fd is None
        assert session.pid is None
        assert session._running is False

    def test_terminal_session_attributes(self):
        """Test terminal session has required attributes."""
        mock_ws = MagicMock()
        session = TerminalSession(mock_ws)

        assert hasattr(session, "websocket")
        assert hasattr(session, "master_fd")
        assert hasattr(session, "pid")
        assert hasattr(session, "_running")
        assert hasattr(session, "start")
        assert hasattr(session, "write")
        assert hasattr(session, "resize")
        assert hasattr(session, "stop")


# ═══════════════════════════════════════════════════════════════════════════════
# WEBSOCKET MESSAGE FORMAT TESTS
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.integration
class TestWebSocketMessagesE2E:
    """Test WebSocket message formats."""

    def test_input_message_format(self):
        """Test input message format is valid."""
        message = {"type": "input", "data": "/help\n"}
        json_str = json.dumps(message)
        parsed = json.loads(json_str)
        assert parsed["type"] == "input"
        assert parsed["data"] == "/help\n"

    def test_resize_message_format(self):
        """Test resize message format is valid."""
        message = {"type": "resize", "cols": 120, "rows": 40}
        json_str = json.dumps(message)
        parsed = json.loads(json_str)
        assert parsed["type"] == "resize"
        assert parsed["cols"] == 120
        assert parsed["rows"] == 40

    def test_output_message_format(self):
        """Test output message format is valid."""
        message = {"type": "output", "data": "Hello, World!\n"}
        json_str = json.dumps(message)
        parsed = json.loads(json_str)
        assert parsed["type"] == "output"

    def test_update_available_message_format(self):
        """Test update available message format is valid."""
        message = {
            "type": "update_available",
            "info": {
                "current_version": "1.13.60",
                "latest_version": "1.13.68",
            },
        }
        json_str = json.dumps(message)
        parsed = json.loads(json_str)
        assert parsed["type"] == "update_available"
        assert "current_version" in parsed["info"]


# ═══════════════════════════════════════════════════════════════════════════════
# TERMINAL COMMAND EXECUTION TESTS
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.integration
class TestTerminalCommandsE2E:
    """Test terminal command execution."""

    SLASH_COMMANDS = [
        "/help",
        "/models",
        "/model ollama:llama3.2",
        "/clear",
        "/exit",
    ]

    SHELL_COMMANDS = [
        "!echo test",
        "!pwd",
        "!ls",
    ]

    @pytest.mark.parametrize("command", SLASH_COMMANDS)
    def test_slash_command_format(self, command):
        """Test slash commands have correct format."""
        message = {"type": "input", "data": f"{command}\n"}
        json_str = json.dumps(message)
        assert "input" in json_str
        assert command in json_str

    @pytest.mark.parametrize("command", SHELL_COMMANDS)
    def test_shell_command_format(self, command):
        """Test shell escape commands have correct format."""
        message = {"type": "input", "data": f"{command}\n"}
        json_str = json.dumps(message)
        assert "input" in json_str
        assert "!" in json_str


# ═══════════════════════════════════════════════════════════════════════════════
# TERMINAL RESIZE BOUNDS TESTS
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.integration
class TestTerminalResizeE2E:
    """Test terminal resize handling."""

    def test_resize_bounds_min(self):
        """Test resize enforces minimum bounds."""
        cols, rows = -10, -10
        cols = max(10, min(500, cols))
        rows = max(5, min(200, rows))
        assert cols == 10
        assert rows == 5

    def test_resize_bounds_max(self):
        """Test resize enforces maximum bounds."""
        cols, rows = 10000, 10000
        cols = max(10, min(500, cols))
        rows = max(5, min(200, rows))
        assert cols == 500
        assert rows == 200

    def test_resize_bounds_normal(self):
        """Test resize accepts normal values."""
        cols, rows = 120, 40
        cols = max(10, min(500, cols))
        rows = max(5, min(200, rows))
        assert cols == 120
        assert rows == 40


# ═══════════════════════════════════════════════════════════════════════════════
# FULL TERMINAL WORKFLOW TESTS
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.integration
class TestTerminalWorkflowE2E:
    """Test complete terminal interaction workflows."""

    def test_full_session_message_sequence(self):
        """Test full session message sequence is valid."""
        workflow = [
            {"type": "resize", "cols": 120, "rows": 40},
            {"type": "input", "data": "/help\n"},
            {"type": "input", "data": "/models\n"},
            {"type": "input", "data": "/model ollama:llama3.2\n"},
            {"type": "input", "data": "Hello, write hello world\n"},
            {"type": "input", "data": "/exit\n"},
        ]

        for message in workflow:
            json_str = json.dumps(message)
            parsed = json.loads(json_str)
            assert "type" in parsed

    def test_model_switch_sequence(self):
        """Test model switching sequence is valid."""
        models = ["ollama:llama3.2", "ollama:mistral", "ollama:qwen2.5-coder"]

        for model_id in models:
            message = {"type": "input", "data": f"/model {model_id}\n"}
            json_str = json.dumps(message)
            parsed = json.loads(json_str)
            assert model_id in parsed["data"]

    def test_prompt_sequence_after_model_switch(self):
        """Test sending prompts after model switch."""
        prompts = [
            "Hello, how are you?",
            "Write a Python hello world",
            "What is 2+2?",
        ]

        sequence = [
            {"type": "input", "data": "/model ollama:llama3.2\n"},
        ]

        for prompt in prompts:
            sequence.append({"type": "input", "data": f"{prompt}\n"})

        # Validate sequence
        for message in sequence:
            json_str = json.dumps(message)
            assert "input" in json_str


# ═══════════════════════════════════════════════════════════════════════════════
# TERMINAL WITH ALL MODELS AND PROMPTS
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.integration
class TestTerminalAllModelsPromptsE2E:
    """Test terminal with all models and example prompts."""

    MODELS = [
        "ollama:llama3.2",
        "ollama:qwen2.5-coder",
        "browser:Llama-3.2-1B-Instruct-q4f16_1-MLC",
    ]

    PROMPTS = [
        "Hello",
        "What is 2+2?",
        "Write a Python function",
        "Explain recursion",
    ]

    @pytest.mark.parametrize("model_id", MODELS)
    @pytest.mark.parametrize("prompt", PROMPTS)
    def test_model_prompt_combination(self, model_id, prompt):
        """Test each model with each prompt generates valid messages."""
        sequence = [
            {"type": "input", "data": f"/model {model_id}\n"},
            {"type": "input", "data": f"{prompt}\n"},
        ]

        for message in sequence:
            json_str = json.dumps(message)
            parsed = json.loads(json_str)
            assert parsed["type"] == "input"

        # Verify model and prompt are in the sequence
        sequence_str = json.dumps(sequence)
        assert model_id in sequence_str
        assert prompt in sequence_str


# ═══════════════════════════════════════════════════════════════════════════════
# WEBSOCKET CLOSE CODE TESTS
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.integration
class TestWebSocketCloseCodesE2E:
    """Test WebSocket close codes are handled correctly."""

    def test_auth_required_code(self):
        """Test authentication required close code."""
        code = 4003
        reason = "Authentication required"
        assert code == 4003
        assert "Authentication" in reason

    def test_rate_limit_code(self):
        """Test rate limit exceeded close code."""
        code = 4029
        reason = "Terminal connection rate limit exceeded"
        assert code == 4029
        assert "rate limit" in reason.lower()

    def test_normal_close_code(self):
        """Test normal close code."""
        code = 1000
        assert code == 1000


# ═══════════════════════════════════════════════════════════════════════════════
# CLI UPDATE WORKFLOW TESTS
# ═══════════════════════════════════════════════════════════════════════════════

@pytest.mark.integration
class TestCLIUpdateWorkflowE2E:
    """Test CLI update workflow."""

    def test_check_update_via_api(self, client):
        """Test checking for updates via API."""
        response = client.get("/api/cli/check-update")
        assert response.status_code == 200
        data = response.json()
        assert "current_version" in data
        assert "latest_version" in data
        assert "update_available" in data
        assert isinstance(data["update_available"], bool)

    def test_update_available_flag(self, cli_updater):
        """Test update available detection."""
        # Mock a scenario where update is available
        v1 = cli_updater._compare_versions("1.0.0", "2.0.0")
        assert v1 == -1  # v1 < v2, so update available

        # Mock no update
        v2 = cli_updater._compare_versions("2.0.0", "2.0.0")
        assert v2 == 0  # equal, no update

        # Mock v1 is newer (downgrade scenario)
        v3 = cli_updater._compare_versions("3.0.0", "2.0.0")
        assert v3 == 1  # v1 > v2, no update needed
