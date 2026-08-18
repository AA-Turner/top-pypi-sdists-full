"""Transport-neutral agent configuration accepted by Session procedures."""

from typing import Annotated, Literal, Self

from pydantic import Field, JsonValue, model_validator

from .base import JsonSchema, SessionModel
from .common import AbsolutePath, ToolKind

type HookType = Literal[
    "pre_agent_turn",
    "post_agent_turn",
    "pre_llm_call",
    "post_llm_call",
    "pre_mcp_tool_call",
    "post_mcp_tool_call",
    "pre_client_tool_call",
    "post_client_tool_call",
    "pre_tool_call",
    "post_tool_call",
]


class ToolDefinition(SessionModel):
    """Client-owned callable exposed to a Runtime through a callback."""

    type: Literal["client_tool"] = "client_tool"
    name: str
    description: str = ""
    input_schema: JsonSchema = Field(default_factory=dict)
    output_schema: JsonSchema = Field(default_factory=dict)


class RuntimeToolDefinition(SessionModel):
    """Server-owned callable resolved by the Session Runtime."""

    type: Literal["runtime_tool"] = "runtime_tool"
    name: str
    description: str = ""
    input_schema: JsonSchema = Field(default_factory=dict)
    output_schema: JsonSchema = Field(default_factory=dict)
    tool_kind: ToolKind = "local"
    snapshot_type: str | None = None
    handler_path: str | None = None
    handler_context: JsonValue = None


type AgentToolDefinition = Annotated[
    ToolDefinition | RuntimeToolDefinition,
    Field(discriminator="type"),
]


class HookDefinition(SessionModel):
    type: HookType
    name: str
    matcher: dict[str, JsonValue] = Field(default_factory=dict)


class SandboxConfig(SessionModel):
    type: Literal["local", "managed"] = "local"
    image: str | None = None
    size: str | None = None
    network_access: bool | None = None
    env: dict[str, str] = Field(default_factory=dict)
    options: dict[str, JsonValue] = Field(default_factory=dict)


class SkillDefinition(SessionModel):
    name: str
    description: str
    content: str
    license: str | None = None
    compatibility: str | None = None
    metadata: dict[str, JsonValue] = Field(default_factory=dict)
    allowed_tools: list[str] = Field(default_factory=list)


class AgentConfig(SessionModel):
    """Serializable configuration shared by local and remote Session Runtimes."""

    completion: dict[str, JsonValue] = Field(
        default_factory=lambda: {"type": "mistral", "model": "mistral-small-latest"}
    )
    name: str = "sdk_agent"
    max_iterations: int | None = None
    enabled_tools: list[str] | None = None
    disabled_tools: list[str] | None = None
    sandbox: SandboxConfig | None = None
    instructions: str = ""
    auto_compact_threshold: int = Field(default=0, ge=0)
    compaction_prompt: str | None = None
    workdir: AbsolutePath | None = None
    tools: list[AgentToolDefinition] = Field(default_factory=list)
    skills: list[SkillDefinition] = Field(default_factory=list)
    mcps: dict[str, dict[str, JsonValue]] = Field(default_factory=dict)
    hooks: list[HookDefinition] = Field(default_factory=list)

    @model_validator(mode="after")
    def validate_skills(self) -> Self:
        if self.skills and any(
            isinstance(tool, ToolDefinition) and tool.name == "skill" for tool in self.tools
        ):
            raise ValueError("The 'skill' tool is added when skills are configured")
        skill_names = [skill.name for skill in self.skills]
        if len(skill_names) != len(set(skill_names)):
            raise ValueError("Agent configuration contains duplicate skill names")
        return self
