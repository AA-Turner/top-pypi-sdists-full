"""Agent integration tests — spins up real Chronos VMs and runs agents.

Validates:
  - Remote MCP tools are discovered and callable
  - Agent produces correct structured output via tool results
  - ATIF spans are emitted (agent steps, system/tool steps, token usage)
  - Trajectory API returns structured data

Requires real API keys:
  PLATO_API_KEY            — Plato + Chronos API access
  ANTHROPIC_API_KEY        — For claude-code agent tests
  OPENAI_API_KEY           — For codex agent tests

Run with:
  pytest tests/integration/test_agent_integration.py -m integration -v
"""

from __future__ import annotations

import asyncio
import base64
import json
import logging
import os
import subprocess
from pathlib import Path

import pytest

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Mark all tests in this module as integration tests
# ---------------------------------------------------------------------------

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

# ---------------------------------------------------------------------------
# Shared config
# ---------------------------------------------------------------------------

# Base tag applied to all Chronos sessions created by integration tests,
# so the backend can filter/identify CI-created sessions.
# Each test class adds its own specific tag (e.g. "agent.claude-code").
CI_SESSION_BASE_TAG = "ci.test"

WORLD_IMAGE = "383806609161.dkr.ecr.us-west-1.amazonaws.com/vm/rootfs/plato-worlds/webclone:0.2.14"
SDK_ROOT = Path(__file__).resolve().parent.parent.parent  # python-sdk/
REPO_ROOT = SDK_ROOT.parent  # plato-client/
AGENT_TEST_WORLD_DIR = Path(__file__).resolve().parent / "agent_test_world"
CHRONOS_URL = "https://chronos.plato.so"

# Agent source directories (synced to world VM for dev-mode agent install)
CLAUDE_CODE_AGENT_DIR = REPO_ROOT / "agents" / "claude-code"
CODEX_AGENT_DIR = REPO_ROOT / "agents" / "codex"

# Agent images — full ECR URLs for VM allocation
ECR_REGISTRY = "383806609161.dkr.ecr.us-west-1.amazonaws.com"
CLAUDE_CODE_IMAGE = f"{ECR_REGISTRY}/vm/rootfs/plato-agents/claude-code:3.0.22"
CODEX_IMAGE = f"{ECR_REGISTRY}/vm/rootfs/plato-agents/codex:3.0.10"


# ---------------------------------------------------------------------------
# VM helper
# ---------------------------------------------------------------------------


def _run_async(coro):
    return asyncio.get_event_loop().run_until_complete(coro)


class _VM:
    """Manages a Plato VM session for testing."""

    def __init__(self):
        self.plato = None
        self.session = None
        self.env = None
        self.chronos_session_id = None

    async def start(self, tags: list[str]):
        import httpx

        from plato.chronos.api.sessions import create_session
        from plato.chronos.models import CreateSessionRequest
        from plato.cli.chronos.dev.ssh import SSHKeyPair
        from plato.v2 import AsyncPlato, Env
        from plato.v2.types import SimConfigCompute

        self.plato = AsyncPlato()
        self.session = await self.plato.sessions.create(
            envs=[
                Env.resource(
                    simulator="agent-integration-test",
                    sim_config=SimConfigCompute(cpus=2, memory=4096, disk=20480),
                    alias="runtime",
                    docker_image_url=WORLD_IMAGE,
                    upload_rootfs=False,
                    rootfs_storage_backend="snapshot-store",
                )
            ],
            timeout=3600,
            connect_network=True,
        )
        self.env = self.session.envs[0]

        # Create Chronos session for OTel trace collection — tagged for CI filtering
        async with httpx.AsyncClient(
            base_url=CHRONOS_URL,
            timeout=30.0,
        ) as client:
            resp = await create_session.asyncio(
                client,
                body=CreateSessionRequest(
                    world_name="plato-world-agent-test",
                    world_config={},
                    tags=tags,
                ),
                x_api_key=os.environ["PLATO_API_KEY"],
            )
        self.chronos_session_id = resp.public_id
        logger.info(f"Chronos session: {self.chronos_session_id} (tags={tags})")

        # Setup SSH key on VM
        self._ssh_key = SSHKeyPair.generate()
        await self.session.add_ssh_key(self._ssh_key.public_key)
        private_key = self._ssh_key.private_key_path.read_text()
        public_key = self._ssh_key.public_key
        escaped_private = private_key.replace("'", "'\\''")
        escaped_public = public_key.replace("'", "'\\''")
        await self.env.execute(
            f"mkdir -p /root/.ssh && "
            f"echo '{escaped_private}' > /root/.ssh/agent_key && chmod 600 /root/.ssh/agent_key && "
            f"echo '{escaped_public}' > /root/.ssh/agent_key.pub && chmod 644 /root/.ssh/agent_key.pub",
            timeout=30,
        )

    async def exec(self, cmd: str, timeout: int = 120) -> tuple[int, str, str]:
        result = await self.env.execute(cmd, timeout=timeout)
        return result.exit_code, result.stdout or "", result.stderr or ""

    async def exec_ok(self, cmd: str, timeout: int = 120) -> str:
        code, out, err = await self.exec(cmd, timeout=timeout)
        assert code == 0, f"Command failed (exit {code}):\ncmd: {cmd}\nstderr: {err}\nstdout: {out}"
        return out

    def rsync_to(self, local_path: str, remote_path: str) -> None:
        from plato.cli.chronos.dev.ssh import build_ssh_command_string

        ssh_str = build_ssh_command_string(self.env.job_id, self._ssh_key.private_key_path)
        host = f"root@{self.env.job_id}.plato"
        cmd = [
            "rsync",
            "-az",
            "--delete",
            "--exclude",
            "__pycache__",
            "--exclude",
            ".git",
            "--exclude",
            "*.pyc",
            "--exclude",
            ".venv",
            "--exclude",
            "node_modules",
            "--exclude",
            "dist",
            "-e",
            ssh_str,
            f"{local_path}/",
            f"{host}:{remote_path}/",
        ]
        proc = subprocess.run(cmd, capture_output=True, timeout=120)
        assert proc.returncode == 0, f"rsync failed: {proc.stderr.decode()}"

    async def close(self):
        if self.session:
            await self.session.close()
        if self.plato:
            await self.plato.close()


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="class")
def vm(request):
    """Spin up a VM per test class, with class-specific Chronos session tags."""
    # Each test class can define session_tags; default to base tag only
    class_tag = getattr(request.cls, "session_tag", None)
    tags = [CI_SESSION_BASE_TAG]
    if class_tag:
        tags.append(class_tag)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    v = _VM()
    try:
        loop.run_until_complete(v.start(tags=tags))
        logger.info(f"VM ready: {v.env.job_id}")

        # Sync SDK + agent test world + agent code
        v.rsync_to(str(SDK_ROOT), "/sdk")
        v.rsync_to(str(AGENT_TEST_WORLD_DIR), "/agent-test-world")

        # Sync agent source code (like chronos dev does for dev mode)
        loop.run_until_complete(v.exec_ok("mkdir -p /agents/claude-code /agents/codex", timeout=10))
        if CLAUDE_CODE_AGENT_DIR.exists():
            v.rsync_to(str(CLAUDE_CODE_AGENT_DIR), "/agents/claude-code")
        if CODEX_AGENT_DIR.exists():
            v.rsync_to(str(CODEX_AGENT_DIR), "/agents/codex")

        # Ensure rsync is available on the VM
        loop.run_until_complete(
            v.exec_ok(
                "which rsync || (apt-get update && apt-get install -y rsync)",
                timeout=60,
            )
        )

        # Install SDK + test world
        loop.run_until_complete(
            v.exec_ok(
                "uv pip install --system -e /sdk -e /agent-test-world 2>&1",
                timeout=300,
            )
        )

        yield v
    finally:
        loop.run_until_complete(v.close())
        loop.close()


@pytest.fixture(scope="class")
def chronos_client():
    """Chronos SDK client for fetching traces/trajectory after tests."""
    from plato.chronos.sdk import Chronos

    client = Chronos()
    yield client
    client.close()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _run_agent_world(
    vm: _VM,
    agent_image: str,
    agent_config: dict,
    timeout: int = 600,
) -> tuple[int, str, str]:
    """Run the agent-test world on the VM with the given agent config."""
    config = {
        "world": {
            "package": "plato-world-agent-test:0.0.1",
            "runtime": {"type": "vm", "vm": {"cpus": 2, "memory": 4096, "disk": 20480}},
            "config": {
                "agent": {
                    "image": agent_image,
                    "config": agent_config,
                },
                "tools_port": 8765,
            },
        },
        "session": {
            "session_id": vm.chronos_session_id,
            "plato_session": vm.session.dump().model_dump(),
            "chronos_url": CHRONOS_URL,
            "otel_url": f"{CHRONOS_URL}/api/otel",
        },
        "dev": {
            "ssh_key_path": "/root/.ssh/agent_key",
        },
    }

    config_b64 = base64.b64encode(json.dumps(config).encode()).decode()
    _run_async(
        vm.exec_ok(
            f"echo '{config_b64}' | base64 -d > /tmp/agent-test-config.json",
            timeout=10,
        )
    )

    env_vars = f"PLATO_API_KEY='{os.environ['PLATO_API_KEY']}'"

    code, stdout, stderr = _run_async(
        vm.exec(
            f"{env_vars} plato-world-runner run --world plato-world-agent-test --config /tmp/agent-test-config.json -v",
            timeout=timeout,
        )
    )

    print(f"STDOUT:\n{stdout}")
    if stderr:
        print(f"STDERR:\n{stderr}")

    return code, stdout, stderr


def _get_atif_step_spans(chronos_client, session_id: str):
    """Fetch ATIF step spans from Chronos traces."""
    traces = chronos_client.get_traces(session_id)
    return [span for span in traces.spans if span.attributes and span.attributes.get("atif.step.source")]


def _get_session_root_spans(chronos_client, session_id: str):
    """Fetch session-level root spans (with aggregate metrics)."""
    traces = chronos_client.get_traces(session_id)
    return [
        span for span in traces.spans if span.attributes and span.attributes.get("atif.agent.turn_count") is not None
    ]


# ---------------------------------------------------------------------------
# Tests — Claude Code
# ---------------------------------------------------------------------------


class TestClaudeCodeAgent:
    """Integration tests for the claude-code agent with MCP tools."""

    session_tag = "agent.claude-code"

    @skip_no_anthropic
    def test_mcp_tools_and_atif(self, vm: _VM, chronos_client):
        """Claude Code connects to MCP tools, calls them correctly, emits ATIF spans."""
        code, stdout, stderr = _run_agent_world(
            vm,
            agent_image=CLAUDE_CODE_IMAGE,
            agent_config={
                "model_name": "anthropic/claude-sonnet-4-20250514",
                "anthropic_api_key": os.environ["ANTHROPIC_API_KEY"],
                "max_turns": 20,
            },
        )

        # World validates result.json internally — exit 0 means all checks passed
        assert code == 0, f"Agent test world failed (exit {code})"

        # Fetch and validate ATIF spans from Chronos
        atif_spans = _get_atif_step_spans(chronos_client, vm.chronos_session_id)
        assert len(atif_spans) > 0, "No ATIF step spans emitted"

        agent_steps = [s for s in atif_spans if s.attributes.get("atif.step.source") == "agent"]
        system_steps = [s for s in atif_spans if s.attributes.get("atif.step.source") == "system"]
        tool_call_steps = [s for s in agent_steps if s.attributes.get("atif.step.tool_calls")]

        assert len(agent_steps) > 0, "No agent steps in ATIF spans"
        assert len(system_steps) > 0, "No system steps — agent didn't produce tool results"
        assert len(tool_call_steps) > 0, "No tool_calls — agent didn't invoke MCP tools"

        # Verify session-level metrics on root span
        root_spans = _get_session_root_spans(chronos_client, vm.chronos_session_id)
        assert len(root_spans) > 0, "No root span with turn_count"
        attrs = root_spans[0].attributes
        assert attrs.get("atif.agent.turn_count", 0) > 0
        assert attrs.get("atif.agent.prompt_tokens", 0) > 0
        assert attrs.get("atif.agent.completion_tokens", 0) > 0

        logger.info(
            f"Claude Code: {len(agent_steps)} agent, {len(system_steps)} system, "
            f"{len(tool_call_steps)} tool_call steps | "
            f"turns={attrs.get('atif.agent.turn_count')} "
            f"prompt={attrs.get('atif.agent.prompt_tokens')} "
            f"completion={attrs.get('atif.agent.completion_tokens')}"
        )

    @skip_no_anthropic
    def test_trajectory_api(self, vm: _VM, chronos_client):
        """Trajectory API returns structured agent trace with valid steps."""
        # Re-use the session from the previous test (spans are already there)
        trajectory = chronos_client.get_trajectory(vm.chronos_session_id)
        assert trajectory.session_id == vm.chronos_session_id

        if trajectory.agents:
            agent_trace = trajectory.agents[0]
            steps = agent_trace.trajectory.steps or []
            assert len(steps) > 0, "Agent trajectory has no steps"

            sources = {s.source for s in steps}
            assert "agent" in sources, "No agent-source steps in trajectory"

            for step in steps:
                assert step.source in ("agent", "system", "user")
                assert step.step_id > 0

            logger.info(f"Trajectory: {len(steps)} steps, sources={sources}")


# ---------------------------------------------------------------------------
# Tests — Codex
# ---------------------------------------------------------------------------


class TestCodexAgent:
    """Integration tests for the codex agent with MCP tools."""

    session_tag = "agent.codex"

    @skip_no_openai
    def test_mcp_tools_and_atif(self, vm: _VM, chronos_client):
        """Codex connects to MCP tools, calls them correctly, emits ATIF spans."""
        code, stdout, stderr = _run_agent_world(
            vm,
            agent_image=CODEX_IMAGE,
            agent_config={
                "model_name": "openai/gpt-5.3-codex",
                "openai_api_key": os.environ["OPENAI_API_KEY"],
                "max_turns": 20,
                "reasoning_effort": "high",
            },
        )

        assert code == 0, f"Agent test world failed (exit {code})"

        atif_spans = _get_atif_step_spans(chronos_client, vm.chronos_session_id)
        assert len(atif_spans) > 0, "No ATIF step spans emitted"

        agent_steps = [s for s in atif_spans if s.attributes.get("atif.step.source") == "agent"]
        system_steps = [s for s in atif_spans if s.attributes.get("atif.step.source") == "system"]
        tool_call_steps = [s for s in agent_steps if s.attributes.get("atif.step.tool_calls")]

        assert len(agent_steps) > 0, "No agent steps in ATIF spans"
        assert len(system_steps) > 0, "No system steps — agent didn't produce tool results"
        assert len(tool_call_steps) > 0, "No tool_calls — agent didn't invoke MCP tools"

        root_spans = _get_session_root_spans(chronos_client, vm.chronos_session_id)
        assert len(root_spans) > 0, "No root span with turn_count"
        attrs = root_spans[0].attributes
        assert attrs.get("atif.agent.turn_count", 0) > 0
        assert attrs.get("atif.agent.prompt_tokens", 0) > 0

        # Verify cost tracking (calculated via litellm from token counts)
        cost = attrs.get("atif.agent.cost_usd")
        assert cost is not None and cost > 0, f"No cost_usd on root span (got {cost})"

        logger.info(
            f"Codex: {len(agent_steps)} agent, {len(system_steps)} system, "
            f"{len(tool_call_steps)} tool_call steps | "
            f"turns={attrs.get('atif.agent.turn_count')} "
            f"cost=${cost:.6f}"
        )

    @skip_no_openai
    def test_trajectory_api(self, vm: _VM, chronos_client):
        """Trajectory API returns structured agent trace with valid steps."""
        trajectory = chronos_client.get_trajectory(vm.chronos_session_id)
        assert trajectory.session_id == vm.chronos_session_id

        if trajectory.agents:
            agent_trace = trajectory.agents[0]
            steps = agent_trace.trajectory.steps or []
            assert len(steps) > 0, "Agent trajectory has no steps"

            sources = {s.source for s in steps}
            assert "agent" in sources

            for step in steps:
                assert step.source in ("agent", "system", "user")
                assert step.step_id > 0
