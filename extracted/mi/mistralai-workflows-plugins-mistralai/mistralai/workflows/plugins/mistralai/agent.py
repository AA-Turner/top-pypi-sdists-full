from typing import Any, Generator

from pydantic import BaseModel, model_validator

from mistralai.client import models as mistralai_models

from .connectors.decorator import ConnectorSlot
from .mcp import MCPConfig
from .tool import Tool


class RunResult(BaseModel):
    final_output: Any


class Agent(mistralai_models.CreateAgentRequest):
    # optional remote identifier; when set, runner/session updates this agent
    id: str | None = None

    # override the type of tools to be able to pass activities
    tools: list[Tool] | None = None  # type: ignore[assignment]

    # override the type of handoffs to be able to pass Agent objects
    handoffs: list["Agent"] | None = None  # type: ignore[assignment]

    # MCP configurations to provide external tools
    mcp_clients: list[MCPConfig] | None = None

    # Connector slots to pass to the conversation API
    connectors: list[ConnectorSlot] | None = None

    # default to mistral-medium-latest
    model: str = "mistral-medium-latest"

    @model_validator(mode="after")
    def _reject_credentials_name(self) -> "Agent":
        if self.connectors:
            for slot in self.connectors:
                if slot.credentials_name is not None:
                    raise ValueError(
                        f"Connector '{slot.connector_name}' uses credentials_name which is not "
                        f"supported by the agent SDK. Remove credentials_name or use "
                        f"ToolCallClient for multi-credential connectors."
                    )
        return self

    _mistral_agent: mistralai_models.Agent | None = None
    _conversation_id: str | None = None

    def __hash__(self) -> int:
        return hash(id(self))

    @staticmethod
    def iterate_agents_deeply_in_handoffs(agent: "Agent") -> Generator["Agent", None, None]:
        """
        Deeply iterates over an agent and its handoffs, returning a generator that yields each agent.

        Args:
            agent (Agent): The starting agent to iterate from.

        Yields:
            Agent: Each agent encountered during the deep iteration.
        """
        seen_agents = set()

        def _recursive_iterate(current_agent: "Agent") -> Generator["Agent", None, None]:
            if current_agent in seen_agents:
                return
            seen_agents.add(current_agent)
            yield current_agent
            if current_agent.handoffs:
                for handoff in current_agent.handoffs:
                    yield from _recursive_iterate(handoff)

        yield from _recursive_iterate(agent)
