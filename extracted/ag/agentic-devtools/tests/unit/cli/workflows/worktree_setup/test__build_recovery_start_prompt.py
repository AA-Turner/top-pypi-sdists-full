"""Tests for the recovery start prompt builder."""

from unittest.mock import patch

from agentic_devtools.cli.workflows.worktree_setup import (
    _WORKFLOW_AGNOSTIC_FALLBACK_PROMPT,
    _build_recovery_start_prompt,
)


class TestBuildRecoveryStartPrompt:
    """Tests for _build_recovery_start_prompt."""

    def test_uses_workflow_agnostic_fallback_without_command(self):
        """A missing command keeps the generic recovery prompt available."""
        assert _build_recovery_start_prompt() == _WORKFLOW_AGNOSTIC_FALLBACK_PROMPT

    def test_includes_exact_command_and_model(self):
        """A recovery prompt includes every nested command argument."""
        command = [
            "agdt-initiate-pull-request-review-workflow",
            "--pull-request-id",
            "30779",
            "--model",
            "gemini-3.7-flash",
            "--skip-copilot-session",
        ]

        prompt = _build_recovery_start_prompt(command)

        assert "\n" not in prompt
        assert "--model" in prompt
        assert "gemini-3.7-flash" in prompt

    def test_windows_prefixes_command_with_call_operator(self):
        """Windows prompts use a runnable command form for quoted executables."""
        command = ["C:/Program Files/Agentic Devtools/agdt.cmd", "--skip-copilot-session"]

        with patch("agentic_devtools.cli.workflows.worktree_setup.platform.system", return_value="Windows"):
            prompt = _build_recovery_start_prompt(command)

        assert "Please rerun this exact command now: & " in prompt
        assert "--skip-copilot-session." not in prompt

    def test_posix_does_not_prefix_command_with_call_operator(self):
        """POSIX prompts use the quoted command without a Windows call operator."""
        command = ["/opt/agentic-devtools/agdt", "--skip-copilot-session"]

        with patch("agentic_devtools.cli.workflows.worktree_setup.platform.system", return_value="Linux"):
            prompt = _build_recovery_start_prompt(command)

        assert "Please rerun this exact command now: & " not in prompt
        assert "Please rerun this exact command now: /opt/agentic-devtools/agdt" in prompt
