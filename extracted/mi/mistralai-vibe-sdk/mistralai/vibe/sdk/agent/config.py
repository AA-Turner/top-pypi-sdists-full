"""Agent configuration model."""

import copy
import os
from typing import Any

from pydantic import BaseModel, Field, SerializeAsAny, model_validator

from mistralai.vibe.sdk.agent.skills import SkillDefinition
from mistralai.vibe.sdk.agent.system_prompt import render_system_prompt
from mistralai.vibe.sdk.agent.tasks.agent_task import AgentTaskConfig
from mistralai.vibe.sdk.agent.tasks.core import TaskCallback
from mistralai.vibe.sdk.agent.tasks.runtime import TaskConfigBase
from mistralai.vibe.sdk.capabilities.authoring import ClientToolDefinition, ToolDefinition
from mistralai.vibe.sdk.capabilities.compiler import CompiledAgentTools, compile_agent_tools
from mistralai.vibe.sdk.capabilities.mcp.config import McpConfigBase
from mistralai.vibe.sdk.capabilities.registry import ClientToolRegistry
from mistralai.vibe.sdk.providers.completion.config import CompletionConfig

type SdkToolDefinition = ToolDefinition[Any, Any] | ClientToolDefinition[Any]


def get_from_env(*key_names: str) -> str | None:
    """Return the first non-empty environment value from ``key_names``."""
    for key_name in key_names:
        value = os.environ.get(key_name, "").strip()
        if value:
            return value
    return None


class AgentConfig(BaseModel):
    """Configuration for creating an SDK Agent."""

    completion: SerializeAsAny[CompletionConfig]
    name: str = "sdk_agent"
    system_prompt: str | None = None
    max_iterations: int | None = None
    enabled_tools: list[str] | None = None
    disabled_tools: list[str] | None = None
    tools: dict[str, SdkToolDefinition] = Field(default_factory=dict)
    skills: list[SkillDefinition] = Field(default_factory=list)
    mcps: dict[str, SerializeAsAny[McpConfigBase]] = Field(default_factory=dict)
    model_config = {"extra": "forbid", "arbitrary_types_allowed": True}

    @model_validator(mode="after")
    def _validate_skills(self) -> "AgentConfig":
        if "skill" in self.tools:
            raise ValueError(
                "The 'skill' tool is auto-injected when skills are configured. "
                "Remove it from tools."
            )

        seen: set[str] = set()
        for skill in self.skills:
            if skill.name in seen:
                raise ValueError(f"Duplicate skill name: {skill.name!r}")
            seen.add(skill.name)
        return self

    @property
    def tasks(self) -> dict[str, TaskConfigBase]:
        """Protocol task configs derived from SDK tool definitions."""
        return self._compiled_tools().tasks

    def to_task_config(self) -> AgentTaskConfig:
        """Compile this SDK config into the protocol agent task config."""
        compiled_tools = self._compiled_tools()
        return AgentTaskConfig(
            completion=self.completion,
            name=self.name,
            system_prompt=render_system_prompt(
                system_prompt=self.system_prompt,
                skills=self.skills,
            ),
            max_iterations=self.max_iterations,
            tasks=compiled_tools.tasks,
            direct_callbacks=compiled_tools.direct_callbacks,
            mcps=self.mcps,
        )

    def client_tool_registry(self) -> ClientToolRegistry:
        """Build a registry for client-handled tools with bound host handlers."""
        return compile_agent_tools(self.tools).client_tool_registry

    def _direct_callbacks(self) -> list[TaskCallback]:
        """Protocol callback declarations derived from client-handled tools."""
        return compile_agent_tools(self.tools).direct_callbacks

    def clone(self) -> "AgentConfig":
        """Create a new AgentConfig from the existing one."""
        completion = self.completion.model_copy(deep=True)
        mcps = {key: mcp.model_copy(deep=True) for key, mcp in self.mcps.items()}
        return self.model_copy(
            update={
                "completion": completion,
                "tools": dict(self.tools),
                "skills": list(self.skills),
                "mcps": mcps,
            }
        )

    def _compiled_tools(self) -> CompiledAgentTools:
        """Compile tools, injecting the builtin skill tool when skills are configured."""
        tools = self.tools
        if self.skills:
            from mistralai.vibe.sdk.capabilities.builtins.skill_tool import SkillToolContext
            from mistralai.vibe.sdk.capabilities.builtins.skill_tool import skill as _skill_tool

            skill_tool = copy.copy(_skill_tool)
            skill_tool.ctx = SkillToolContext(skills={skill.name: skill for skill in self.skills})
            tools = {**tools, "skill": skill_tool}
        return compile_agent_tools(tools)
