"""Tests for determine_agent."""

from pathlib import Path
from unittest.mock import patch

import pytest

from detect_agent import (
    DEVIN_LOCAL_PATH,
    KNOWN_AGENTS,
    determine_agent,
)

# Env vars we reset so tests don't leak into each other
_AGENT_ENV_VARS = (
    "AI_AGENT",
    "PI_CODING_AGENT",
    "CURSOR_AGENT",
    "CURSOR_EXTENSION_HOST_ROLE",
    "GEMINI_CLI",
    "CODEX_SANDBOX",
    "CODEX_CI",
    "CODEX_THREAD_ID",
    "ANTIGRAVITY_AGENT",
    "AUGMENT_AGENT",
    "OPENCODE_CLIENT",
    "CLAUDECODE",
    "CLAUDE_CODE",
    "CLAUDE_CODE_IS_COWORK",
    "REPL_ID",
    "COPILOT_MODEL",
    "COPILOT_ALLOW_ALL",
    "COPILOT_GITHUB_TOKEN",
)


@pytest.fixture(autouse=True)
def _clear_agent_env(monkeypatch):
    for key in _AGENT_ENV_VARS:
        monkeypatch.delenv(key, raising=False)
    yield
    for key in _AGENT_ENV_VARS:
        monkeypatch.delenv(key, raising=False)


class TestCustomAgentFromAI_AGENT:
    """Custom agent detection from AI_AGENT."""

    def test_ai_agent_not_set_returns_no_agent(self):
        result = determine_agent()
        assert result == {"is_agent": False, "agent": None}

    def test_ai_agent_set_detects_custom_agent(self, monkeypatch):
        monkeypatch.setenv("AI_AGENT", "custom-agent")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": "custom-agent"}}


class TestGitHubCopilotDetection:
    """GitHub Copilot detection."""

    def test_pi_coding_agent_set_detects_pi(self, monkeypatch):
        monkeypatch.setenv("PI_CODING_AGENT", "1")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["PI"]}}

    def test_from_ai_agent_github_copilot(self, monkeypatch):
        monkeypatch.setenv("AI_AGENT", "github-copilot")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["GITHUB_COPILOT"]}}

    def test_from_ai_agent_github_copilot_cli(self, monkeypatch):
        monkeypatch.setenv("AI_AGENT", "github-copilot-cli")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["GITHUB_COPILOT"]}}

    def test_from_copilot_model(self, monkeypatch):
        monkeypatch.setenv("COPILOT_MODEL", "gpt-5")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["GITHUB_COPILOT"]}}

    def test_from_copilot_allow_all(self, monkeypatch):
        monkeypatch.setenv("COPILOT_ALLOW_ALL", "true")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["GITHUB_COPILOT"]}}

    def test_from_copilot_github_token(self, monkeypatch):
        monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "ghp_xxx")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["GITHUB_COPILOT"]}}


class TestCursorDetection:
    """Cursor detection."""

    def test_cursor_agent_set_detects_cursor(self, monkeypatch):
        monkeypatch.setenv("CURSOR_AGENT", "1")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["CURSOR"]}}


class TestCursorCliDetection:
    """Cursor CLI detection."""

    def test_cursor_agent_not_set_returns_no_agent(self):
        result = determine_agent()
        assert result == {"is_agent": False, "agent": None}

    def test_cursor_agent_set_detects_cursor_cli(self, monkeypatch):
        monkeypatch.setenv("CURSOR_AGENT", "1")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["CURSOR"]}}

    def test_cursor_extension_host_role_agent_exec_detects_cursor_cli(self, monkeypatch):
        monkeypatch.setenv("CURSOR_EXTENSION_HOST_ROLE", "agent-exec")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["CURSOR_CLI"]}}

    def test_cursor_extension_host_role_other_value_returns_no_agent(self, monkeypatch):
        monkeypatch.setenv("CURSOR_EXTENSION_HOST_ROLE", "something-else")
        result = determine_agent()
        assert result == {"is_agent": False, "agent": None}


class TestGeminiDetection:
    """Gemini detection."""

    def test_gemini_cli_not_set_returns_no_agent(self):
        result = determine_agent()
        assert result == {"is_agent": False, "agent": None}

    def test_gemini_cli_set_detects_gemini(self, monkeypatch):
        monkeypatch.setenv("GEMINI_CLI", "1")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["GEMINI"]}}


class TestCodexDetection:
    """Codex detection."""

    def test_codex_sandbox_not_set_returns_no_agent(self):
        result = determine_agent()
        assert result == {"is_agent": False, "agent": None}

    def test_codex_sandbox_set_detects_codex(self, monkeypatch):
        monkeypatch.setenv("CODEX_SANDBOX", "seatbelt")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["CODEX"]}}

    def test_codex_ci_set_detects_codex(self, monkeypatch):
        monkeypatch.setenv("CODEX_CI", "1")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["CODEX"]}}

    def test_codex_thread_id_set_detects_codex(self, monkeypatch):
        monkeypatch.setenv("CODEX_THREAD_ID", "thread-123")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["CODEX"]}}


class TestAntigravityDetection:
    """Antigravity detection."""

    def test_antigravity_agent_not_set_returns_no_agent(self):
        result = determine_agent()
        assert result == {"is_agent": False, "agent": None}

    def test_antigravity_agent_set_detects_antigravity(self, monkeypatch):
        monkeypatch.setenv("ANTIGRAVITY_AGENT", "1")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["ANTIGRAVITY"]}}


class TestAugmentCliDetection:
    """Augment CLI detection."""

    def test_augment_agent_not_set_returns_no_agent(self):
        result = determine_agent()
        assert result == {"is_agent": False, "agent": None}

    def test_augment_agent_set_detects_augment_cli(self, monkeypatch):
        monkeypatch.setenv("AUGMENT_AGENT", "1")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["AUGMENT_CLI"]}}


class TestOpencodeDetection:
    """Opencode detection."""

    def test_opencode_client_not_set_returns_no_agent(self):
        result = determine_agent()
        assert result == {"is_agent": False, "agent": None}

    def test_opencode_client_set_detects_opencode(self, monkeypatch):
        monkeypatch.setenv("OPENCODE_CLIENT", "opencode")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["OPENCODE"]}}


class TestClaudeDetection:
    """Claude detection."""

    def test_claude_code_not_set_returns_no_agent(self):
        result = determine_agent()
        assert result == {"is_agent": False, "agent": None}

    def test_claude_code_set_detects_claude(self, monkeypatch):
        monkeypatch.setenv("CLAUDE_CODE", "1")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["CLAUDE"]}}

    def test_claudecode_set_detects_claude(self, monkeypatch):
        monkeypatch.setenv("CLAUDECODE", "1")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["CLAUDE"]}}


class TestCoworkDetection:
    """Cowork detection."""

    def test_claude_code_is_cowork_not_set_detects_claude(self, monkeypatch):
        monkeypatch.setenv("CLAUDECODE", "1")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["CLAUDE"]}}

    def test_claude_code_is_cowork_set_with_claudecode_detects_cowork(self, monkeypatch):
        monkeypatch.setenv("CLAUDECODE", "1")
        monkeypatch.setenv("CLAUDE_CODE_IS_COWORK", "1")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["COWORK"]}}

    def test_claude_code_is_cowork_set_with_claude_code_detects_cowork(self, monkeypatch):
        monkeypatch.setenv("CLAUDE_CODE", "1")
        monkeypatch.setenv("CLAUDE_CODE_IS_COWORK", "1")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["COWORK"]}}

    def test_claude_code_is_cowork_set_without_claudecode_or_claude_code_returns_no_agent(
        self, monkeypatch
    ):
        monkeypatch.setenv("CLAUDE_CODE_IS_COWORK", "1")
        result = determine_agent()
        assert result == {"is_agent": False, "agent": None}


class TestDevinDetection:
    """Devin detection."""

    def test_devin_path_does_not_exist_returns_no_agent(self):
        with patch.object(Path, "exists", return_value=False):
            result = determine_agent()
        assert result == {"is_agent": False, "agent": None}

    def test_devin_path_exists_detects_devin(self):
        with patch.object(Path, "exists", return_value=True):
            result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["DEVIN"]}}


class TestReplitDetection:
    """Replit detection."""

    def test_repl_id_not_set_returns_no_agent(self):
        result = determine_agent()
        assert result == {"is_agent": False, "agent": None}

    def test_repl_id_set_detects_replit(self, monkeypatch):
        monkeypatch.setenv("REPL_ID", "1")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["REPLIT"]}}


class TestPriorityOrderDetection:
    """Priority order detection."""

    def test_ai_agent_takes_highest_priority(self, monkeypatch):
        monkeypatch.setenv("AI_AGENT", "custom-priority")
        monkeypatch.setenv("CURSOR_AGENT", "1")
        monkeypatch.setenv("GEMINI_CLI", "1")
        monkeypatch.setenv("CODEX_SANDBOX", "seatbelt")
        monkeypatch.setenv("ANTIGRAVITY_AGENT", "1")
        monkeypatch.setenv("AUGMENT_AGENT", "1")
        monkeypatch.setenv("OPENCODE_CLIENT", "opencode")
        monkeypatch.setenv("CLAUDE_CODE", "1")
        monkeypatch.setenv("REPL_ID", "1")
        monkeypatch.setenv("COPILOT_MODEL", "gpt-5")
        monkeypatch.setenv("COPILOT_ALLOW_ALL", "true")
        monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "ghp_xxx")
        with patch.object(Path, "exists") as mock_exists:
            mock_exists.side_effect = lambda self: str(self) == DEVIN_LOCAL_PATH
            result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": "custom-priority"}}

    def test_cursor_agent_takes_priority_over_remaining_agents(self, monkeypatch):
        monkeypatch.setenv("CURSOR_AGENT", "1")
        monkeypatch.setenv("GEMINI_CLI", "1")
        monkeypatch.setenv("CODEX_SANDBOX", "seatbelt")
        monkeypatch.setenv("ANTIGRAVITY_AGENT", "1")
        monkeypatch.setenv("AUGMENT_AGENT", "1")
        monkeypatch.setenv("OPENCODE_CLIENT", "opencode")
        monkeypatch.setenv("CLAUDE_CODE", "1")
        monkeypatch.setenv("REPL_ID", "1")
        monkeypatch.setenv("COPILOT_MODEL", "gpt-5")
        monkeypatch.setenv("COPILOT_ALLOW_ALL", "true")
        monkeypatch.setenv("COPILOT_GITHUB_TOKEN", "ghp_xxx")
        with patch.object(Path, "exists") as mock_exists:
            mock_exists.side_effect = lambda self: str(self) == DEVIN_LOCAL_PATH
            result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": KNOWN_AGENTS["CURSOR"]}}


class TestEdgeCases:
    """Edge cases."""

    def test_empty_string_env_vars(self, monkeypatch):
        monkeypatch.setenv("AI_AGENT", "")
        result = determine_agent()
        assert result == {"is_agent": False, "agent": None}

    def test_whitespace_only_ai_agent(self, monkeypatch):
        monkeypatch.setenv("AI_AGENT", "   ")
        result = determine_agent()
        assert result == {"is_agent": False, "agent": None}

    def test_special_characters_in_ai_agent(self, monkeypatch):
        monkeypatch.setenv("AI_AGENT", "my-custom-agent@v1.0")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": "my-custom-agent@v1.0"}}

    def test_trims_whitespace_from_ai_agent(self, monkeypatch):
        monkeypatch.setenv("AI_AGENT", "  custom-agent  ")
        result = determine_agent()
        assert result == {"is_agent": True, "agent": {"name": "custom-agent"}}

    def test_devin_path_not_accessible_returns_no_agent(self):
        with patch.object(Path, "exists", return_value=False):
            result = determine_agent()
        assert result == {"is_agent": False, "agent": None}


class TestConvenienceMethods:
    """Convenience methods."""

    def test_is_agent_boolean(self, monkeypatch):
        monkeypatch.setenv("AI_AGENT", "test-agent")
        result = determine_agent()
        assert result["is_agent"] is True

    def test_agent_details_when_detected(self, monkeypatch):
        monkeypatch.setenv("CURSOR_AGENT", "1")
        result = determine_agent()
        assert result["is_agent"] is True
        assert result.get("agent") is not None
        assert result["agent"]["name"] == KNOWN_AGENTS["CURSOR"]

    def test_no_agent_details_when_not_detected(self):
        result = determine_agent()
        assert result["is_agent"] is False
        assert result.get("agent") is None
