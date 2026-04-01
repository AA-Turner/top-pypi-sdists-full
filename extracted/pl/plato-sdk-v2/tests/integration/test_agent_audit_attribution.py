"""Integration tests for local tool-attributed workspace audit collection."""

from __future__ import annotations

import asyncio
import logging
import os
from pathlib import Path

import pytest

from plato.cli.chronos.test import TestConfig, TestRunner

logger = logging.getLogger(__name__)

pytestmark = [
    pytest.mark.integration,
    pytest.mark.skipif(not os.environ.get("PLATO_API_KEY"), reason="PLATO_API_KEY not set"),
]

skip_no_anthropic = pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set",
)

skip_no_openai = pytest.mark.skipif(
    not os.environ.get("OPENAI_API_KEY"),
    reason="OPENAI_API_KEY not set",
)

skip_no_gemini = pytest.mark.skipif(
    not os.environ.get("GEMINI_API_KEY"),
    reason="GEMINI_API_KEY not set",
)

CONFIGS_DIR = Path(__file__).resolve().parent / "configs"


def _run_agent_audit_test(config_path: Path) -> tuple[int, str]:
    config = TestConfig.from_file(config_path)
    runner = TestRunner(
        config=config,
        config_path=config_path,
        api_key=os.environ["PLATO_API_KEY"],
        phase_filter="all",
        pytest_args=None,
        artifacts_dir=None,
        verbose=True,
    )
    exit_code = asyncio.run(runner.run())
    session_id = runner.session_id
    logger.info(
        "Agent audit test completed: config=%s session=%s exit_code=%d", config_path.name, session_id, exit_code
    )
    return exit_code, session_id


class TestAgentAuditAttribution:
    @skip_no_anthropic
    def test_claude_code_tool_attribution(self) -> None:
        exit_code, session_id = _run_agent_audit_test(
            CONFIGS_DIR / "agent-audit-claude-code-test.json",
        )
        assert exit_code == 0, f"Claude audit attribution test failed: session={session_id}"
        logger.info("Claude Code audit attribution test PASSED: session=%s", session_id)

    @skip_no_anthropic
    def test_claude_code_parallel_tool_attribution(self) -> None:
        """Run 3 agents in parallel and verify Read/Write/Bash all get audit attribution."""
        exit_code, session_id = _run_agent_audit_test(
            CONFIGS_DIR / "agent-audit-parallel-claude-code-test.json",
        )
        assert exit_code == 0, f"Parallel Claude audit attribution test failed: session={session_id}"
        logger.info("Parallel Claude Code audit attribution test PASSED: session=%s", session_id)

    @skip_no_openai
    def test_codex_tool_attribution(self) -> None:
        exit_code, session_id = _run_agent_audit_test(
            CONFIGS_DIR / "agent-audit-codex-test.json",
        )
        assert exit_code == 0, f"Codex audit attribution test failed: session={session_id}"
        logger.info("Codex audit attribution test PASSED: session=%s", session_id)

    @skip_no_gemini
    def test_gemini_cli_tool_attribution(self) -> None:
        exit_code, session_id = _run_agent_audit_test(
            CONFIGS_DIR / "agent-audit-gemini-cli-test.json",
        )
        assert exit_code == 0, f"Gemini CLI audit attribution test failed: session={session_id}"
        logger.info("Gemini CLI audit attribution test PASSED: session=%s", session_id)
