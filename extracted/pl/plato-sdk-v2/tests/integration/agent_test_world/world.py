"""Minimal test world that exposes MCP tools and validates agent behaviour.

Exposes two MCP tools via ToolServer:
  - get_secret_value(key) → returns a predefined secret value
  - add_numbers(a, b)     → returns a + b

The world gives the agent a structured prompt asking it to call both tools
and write results to /workspace/result.json.  After the agent finishes the
world reads that file and reports pass/fail.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Annotated, ClassVar

from pydantic import BaseModel, Field

from plato.tools import ToolDefinition
from plato.tools.server import ToolServer
from plato.worlds import (
    Agent,
    AgentConfig,
    BaseWorld,
    Observation,
    RunConfig,
    StepResult,
    Workspace,
    register_world,
)

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
# MCP Tools
# --------------------------------------------------------------------------- #

SECRET_VALUES = {
    "alpha": "platypus-42",
    "beta": "octopus-99",
    "gamma": "seahorse-7",
}


class GetSecretInput(BaseModel):
    key: str = Field(description="Secret key to look up (alpha, beta, or gamma)")


class AddNumbersInput(BaseModel):
    a: int = Field(description="First number")
    b: int = Field(description="Second number")


class TestToolServer(ToolServer):
    """Minimal MCP tool server for integration testing."""

    def build_tools(self) -> list[ToolDefinition]:
        return [
            ToolDefinition(
                name="get_secret_value",
                description="Look up a secret value by key. Valid keys: alpha, beta, gamma.",
                input_model=GetSecretInput,
                handler=self._get_secret,
            ),
            ToolDefinition(
                name="add_numbers",
                description="Add two integers and return the sum.",
                input_model=AddNumbersInput,
                handler=self._add_numbers,
            ),
        ]

    def _get_secret(self, inp: GetSecretInput) -> dict:
        value = SECRET_VALUES.get(inp.key)
        if value is None:
            return {"error": f"Unknown key: {inp.key}. Valid keys: {list(SECRET_VALUES.keys())}"}
        return {"key": inp.key, "value": value}

    def _add_numbers(self, inp: AddNumbersInput) -> dict:
        return {"a": inp.a, "b": inp.b, "sum": inp.a + inp.b}


# --------------------------------------------------------------------------- #
# World
# --------------------------------------------------------------------------- #

AGENT_INSTRUCTION = """\
You have access to MCP tools. Complete these tasks:

1. Call the `get_secret_value` tool with key="alpha" and note the returned value.
2. Call the `add_numbers` tool with a=17 and b=25 and note the returned sum.
3. Write a JSON file at /workspace/result.json with exactly this structure:

```json
{
  "secret_value": "<value from step 1>",
  "sum": <number from step 2>,
  "agent_message": "integration test passed"
}
```

Do NOT include any extra keys. Write ONLY valid JSON (no markdown fences) to the file.
"""


class AgentTestWorldConfig(RunConfig):
    agent: Annotated[AgentConfig, Agent(description="Agent under test")]
    tools_port: int = 8765
    code: Annotated[
        Path,
        Workspace(description="Agent workspace", tracked=False, mount_path="/workspace"),
    ] = Path("/workspace")


@register_world("plato-world-agent-test")
class AgentTestWorld(BaseWorld[AgentTestWorldConfig]):
    name: ClassVar[str] = "agent-test"
    description: ClassVar[str] = "Integration test world for agent MCP + ATIF validation"

    _tool_server: TestToolServer | None = None

    async def reset(self) -> Observation:
        self.logger.info("AgentTestWorld reset")
        return Observation(data={"status": "ready"})

    async def step(self) -> StepResult:
        port = self.config.tools_port
        self._tool_server = TestToolServer(name="agent-test-tools", port=port)
        await self._tool_server.start()
        self.logger.info(f"MCP tool server started on port {port}")

        try:
            mcp_url = f"http://runtime.plato.internal:{port}/mcp"
            agent_cfg = self.config.agent
            agent_cfg.config["mcp_server_url"] = mcp_url
            agent_cfg.config["mcp_server_name"] = "agent-test-tools"

            self.logger.info(f"Running agent with MCP URL: {mcp_url}")
            code_ws = self.workspace("code")
            await self.agent(agent_cfg, workspaces=[code_ws]).run(
                AGENT_INSTRUCTION,
            )
        finally:
            await self._tool_server.close()
            self.logger.info("MCP tool server stopped")

        # Validate result
        code_ws = self.workspace("code")
        result_path = Path(code_ws.path) / "result.json"
        if not result_path.exists():
            raise RuntimeError("Agent did not create /workspace/result.json")

        result = json.loads(result_path.read_text())
        errors = []
        if result.get("secret_value") != SECRET_VALUES["alpha"]:
            errors.append(f"secret_value: expected {SECRET_VALUES['alpha']!r}, got {result.get('secret_value')!r}")
        if result.get("sum") != 42:
            errors.append(f"sum: expected 42, got {result.get('sum')!r}")

        if errors:
            raise RuntimeError(f"Validation failed: {'; '.join(errors)}")

        self.logger.info("All validations passed!")
        return StepResult(
            observation=Observation(data={"status": "passed", "result": result}),
            done=True,
        )
