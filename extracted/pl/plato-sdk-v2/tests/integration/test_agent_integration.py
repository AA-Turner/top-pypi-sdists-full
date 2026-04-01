"""Agent integration tests — spins up real Chronos VMs and runs agents.

Validates:
  - Remote MCP tools are discovered and callable
  - Agent produces correct structured output via tool results
  - ATIF spans are emitted (agent steps, system/tool steps, token usage)
  - Trajectory API returns structured agent trace data

Requires real API keys:
  PLATO_API_KEY            — Plato + Chronos API access
  ANTHROPIC_API_KEY        — For claude-code agent tests
  OPENAI_API_KEY           — For codex agent tests

Run with:
  pytest tests/integration/test_agent_integration.py -m integration -v
"""

from __future__ import annotations

import asyncio
import logging
import os
import shutil
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

CONFIGS_DIR = Path(__file__).resolve().parent / "configs"
CLAUDE_CODE_CONFIG = CONFIGS_DIR / "agent-claude-code-test.json"
CODEX_CONFIG = CONFIGS_DIR / "agent-codex-test.json"


def _build_fuse_dir(tmp_path: Path) -> Path:
    """Build plato-fuse binary and return a directory containing it."""
    from .conftest import build_plato_fuse_binary

    binary = build_plato_fuse_binary((2, 34))
    fuse_dir = tmp_path / "plato-fuse"
    fuse_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(binary, fuse_dir / "plato-fuse")
    return fuse_dir


def _run_agent_test(config_path: Path, tmp_path: Path) -> tuple[int, str]:
    """Run an agent test via TestRunner, return (exit_code, session_id)."""
    fuse_dir = _build_fuse_dir(tmp_path)
    config = TestConfig.from_file(config_path)
    config = config.model_copy(update={"dev": config.dev.model_copy(update={"extra_sync": {"plato-fuse": fuse_dir}})})
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
    return exit_code, runner.session_id


def _get_atif_step_spans(chronos_client, session_id: str):
    traces = chronos_client.get_traces(session_id)
    return [span for span in traces.spans if span.attributes and span.attributes.get("atif.step.source")]


def _get_session_root_spans(chronos_client, session_id: str):
    traces = chronos_client.get_traces(session_id)
    return [
        span for span in traces.spans if span.attributes and span.attributes.get("atif.agent.turn_count") is not None
    ]


@pytest.fixture(scope="module")
def chronos_client():
    from plato.chronos.sdk import Chronos

    client = Chronos()
    yield client
    client.close()


class TestClaudeCodeAgent:
    """Integration tests for the claude-code agent with MCP tools."""

    @skip_no_anthropic
    def test_mcp_tools_and_atif(self, tmp_path: Path, chronos_client):
        """Claude Code connects to MCP tools, calls them correctly, emits ATIF spans."""
        exit_code, session_id = _run_agent_test(CLAUDE_CODE_CONFIG, tmp_path)
        assert exit_code == 0, f"Agent test world failed (exit {exit_code})"

        atif_spans = _get_atif_step_spans(chronos_client, session_id)
        assert len(atif_spans) > 0, "No ATIF step spans emitted"

        agent_steps = [s for s in atif_spans if s.attributes.get("atif.step.source") == "agent"]
        system_steps = [s for s in atif_spans if s.attributes.get("atif.step.source") == "system"]
        tool_call_steps = [s for s in agent_steps if s.attributes.get("atif.step.tool_calls")]

        assert len(agent_steps) > 0, "No agent steps in ATIF spans"
        assert len(system_steps) > 0, "No system steps — agent didn't produce tool results"
        assert len(tool_call_steps) > 0, "No tool_calls — agent didn't invoke MCP tools"

        root_spans = _get_session_root_spans(chronos_client, session_id)
        assert len(root_spans) > 0, "No root span with turn_count"
        attrs = root_spans[0].attributes
        assert attrs.get("atif.agent.turn_count", 0) > 0
        assert attrs.get("atif.agent.prompt_tokens", 0) > 0
        assert attrs.get("atif.agent.completion_tokens", 0) > 0

        logger.info(
            "Claude Code: %d agent, %d system, %d tool_call steps | turns=%s prompt=%s completion=%s",
            len(agent_steps),
            len(system_steps),
            len(tool_call_steps),
            attrs.get("atif.agent.turn_count"),
            attrs.get("atif.agent.prompt_tokens"),
            attrs.get("atif.agent.completion_tokens"),
        )

    @skip_no_anthropic
    def test_trajectory_api(self, tmp_path: Path, chronos_client):
        """Trajectory API returns structured agent trace with valid steps."""
        exit_code, session_id = _run_agent_test(CLAUDE_CODE_CONFIG, tmp_path)
        assert exit_code == 0, f"Agent test world failed (exit {exit_code})"

        trajectory = chronos_client.get_trajectory(session_id)
        assert trajectory.session_id == session_id

        if trajectory.agents:
            agent_trace = trajectory.agents[0]
            steps = agent_trace.trajectory.steps or []
            assert len(steps) > 0, "Agent trajectory has no steps"

            sources = {s.source for s in steps}
            assert "agent" in sources, "No agent-source steps in trajectory"

            for step in steps:
                assert step.source in ("agent", "system", "user")
                assert step.step_id > 0

            logger.info("Trajectory: %d steps, sources=%s", len(steps), sources)


class TestCodexAgent:
    """Integration tests for the codex agent with MCP tools."""

    @skip_no_openai
    def test_mcp_tools_and_atif(self, tmp_path: Path, chronos_client):
        """Codex connects to MCP tools, calls them correctly, emits ATIF spans."""
        exit_code, session_id = _run_agent_test(CODEX_CONFIG, tmp_path)
        assert exit_code == 0, f"Agent test world failed (exit {exit_code})"

        atif_spans = _get_atif_step_spans(chronos_client, session_id)
        assert len(atif_spans) > 0, "No ATIF step spans emitted"

        agent_steps = [s for s in atif_spans if s.attributes.get("atif.step.source") == "agent"]
        system_steps = [s for s in atif_spans if s.attributes.get("atif.step.source") == "system"]
        tool_call_steps = [s for s in agent_steps if s.attributes.get("atif.step.tool_calls")]

        assert len(agent_steps) > 0, "No agent steps in ATIF spans"
        assert len(system_steps) > 0, "No system steps — agent didn't produce tool results"
        assert len(tool_call_steps) > 0, "No tool_calls — agent didn't invoke MCP tools"

        root_spans = _get_session_root_spans(chronos_client, session_id)
        assert len(root_spans) > 0, "No root span with turn_count"
        attrs = root_spans[0].attributes
        assert attrs.get("atif.agent.turn_count", 0) > 0
        assert attrs.get("atif.agent.prompt_tokens", 0) > 0

        cost = attrs.get("atif.agent.cost_usd")
        assert cost is not None and cost > 0, f"No cost_usd on root span (got {cost})"

        logger.info(
            "Codex: %d agent, %d system, %d tool_call steps | turns=%s cost=$%.6f",
            len(agent_steps),
            len(system_steps),
            len(tool_call_steps),
            attrs.get("atif.agent.turn_count"),
            cost,
        )

    @skip_no_openai
    def test_trajectory_api(self, tmp_path: Path, chronos_client):
        """Trajectory API returns structured agent trace with valid steps."""
        exit_code, session_id = _run_agent_test(CODEX_CONFIG, tmp_path)
        assert exit_code == 0, f"Agent test world failed (exit {exit_code})"

        trajectory = chronos_client.get_trajectory(session_id)
        assert trajectory.session_id == session_id

        if trajectory.agents:
            agent_trace = trajectory.agents[0]
            steps = agent_trace.trajectory.steps or []
            assert len(steps) > 0, "Agent trajectory has no steps"

            sources = {s.source for s in steps}
            assert "agent" in sources

            for step in steps:
                assert step.source in ("agent", "system", "user")
                assert step.step_id > 0

            logger.info("Trajectory: %d steps, sources=%s", len(steps), sources)
