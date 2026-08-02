"""Compile SDK-authored tools into today's agent runtime structures."""

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any

from mistralai.vibe.sdk.agent.tasks.core import TaskCallback
from mistralai.vibe.sdk.agent.tasks.runtime import TaskConfigBase
from mistralai.vibe.sdk.capabilities.authoring import ClientToolDefinition, ToolDefinition
from mistralai.vibe.sdk.capabilities.registry import ClientToolRegistry

type AgentToolDefinition = ToolDefinition[Any, Any] | ClientToolDefinition[Any]


@dataclass(frozen=True, slots=True)
class CompiledAgentTools:
    tasks: dict[str, TaskConfigBase]
    direct_callbacks: list[TaskCallback]
    client_tool_registry: ClientToolRegistry


def compile_agent_tools(
    tools: Mapping[str, AgentToolDefinition],
) -> CompiledAgentTools:
    tasks: dict[str, TaskConfigBase] = {}
    direct_callbacks: list[TaskCallback] = []
    client_tool_registry = ClientToolRegistry()

    for name, definition in tools.items():
        if isinstance(definition, ToolDefinition):
            tasks[name] = definition.to_config().model_copy(update={"name": name})
            continue

        if isinstance(definition, ClientToolDefinition):
            callback = definition.to_callback()
            direct_callbacks.append(
                callback.model_copy(
                    update={"card": callback.card.model_copy(update={"name": name})}
                )
            )
            if definition.handler is not None:
                client_tool_registry.register(name, definition, definition.handler)

    return CompiledAgentTools(
        tasks=tasks,
        direct_callbacks=direct_callbacks,
        client_tool_registry=client_tool_registry,
    )


__all__ = ["CompiledAgentTools", "compile_agent_tools"]
