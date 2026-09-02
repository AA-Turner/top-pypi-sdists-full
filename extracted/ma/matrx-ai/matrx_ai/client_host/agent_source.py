"""Canonical executable-agent boundary for ORM-less matrx-ai hosts."""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Any, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator

from matrx_ai._ext import get_ext, has_ext
from matrx_ai.agents.types import AgentConfig
from matrx_ai.agents.variables import AgentVariable
from matrx_ai.config.unified_config import UnifiedConfig

EXECUTION_AGENT_SOURCE_KEY = "execution_agent_source"


@dataclass(frozen=True)
class _AgentDefinitionErrorInfo:
    error_type: str
    message: str
    user_message: str
    status_code: int = 422


class InvalidExecutionAgentDefinition(ValueError):
    """Raised when an authoritative/cached agent is unsafe to execute."""

    def __init__(self, message: str) -> None:
        super().__init__(message)
        self.error_info = _AgentDefinitionErrorInfo(
            error_type="agent_definition_invalid",
            message=message,
            user_message=(
                "This saved agent's executable definition is incomplete or invalid. "
                "Open the agent, correct its model/instructions, and try again."
            ),
        )


class ExecutionAgentDefinition(BaseModel):
    """Complete, portable agent definition consumed by every execution host."""

    model_config = ConfigDict(extra="forbid")

    definition_id: str
    agent_id: str
    is_version: bool = False
    version_number: int | None = None
    revision: str | None = None
    definition_hash: str | None = None

    name: str = ""
    model_id: str
    messages: list[Any] = Field(min_length=1)
    settings: dict[str, Any] = Field(default_factory=dict)
    tools: list[str] = Field(default_factory=list)
    custom_tools: list[Any] = Field(default_factory=list)
    mcp_servers: list[str] = Field(default_factory=list)
    variable_definitions: list[dict[str, Any]] = Field(default_factory=list)
    context_policies: list[dict[str, Any]] = Field(default_factory=list)
    # The context kill switch is a first-class COLUMN on agent.definition (unlike
    # auto_tools_disabled, which rides inside tool_config) — so it is versioned by
    # trg_agx_agent_snapshot_version and diffable in the agent UI like any other
    # authored field.
    auto_context_disabled: bool = False
    tool_config: dict[str, Any] = Field(default_factory=dict)
    output_schema: dict[str, Any] | None = None
    matrx_actions: dict[str, Any] | None = Field(default=None, title="Matrx Directives")
    skill_config: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def _execution_safety_gate(self) -> ExecutionAgentDefinition:
        if not self.model_id.strip():
            raise InvalidExecutionAgentDefinition(
                f"Agent {self.definition_id!r} has no model_id; refusing execution."
            )
        if not self.messages:
            raise InvalidExecutionAgentDefinition(
                f"Agent {self.definition_id!r} has no authored messages; refusing execution."
            )
        return self

    def content_hash(self) -> str:
        payload = self.model_dump_json(
            exclude={"definition_hash"},
            exclude_none=False,
        ).encode("utf-8")
        return hashlib.sha256(payload).hexdigest()

    def with_content_hash(self) -> ExecutionAgentDefinition:
        return self.model_copy(update={"definition_hash": self.content_hash()})


@runtime_checkable
class ExecutionAgentSource(Protocol):
    """Host seam that returns a complete executable agent definition."""

    async def load_for_execution(
        self,
        agent_id: str,
        *,
        is_version: bool = False,
    ) -> ExecutionAgentDefinition | dict[str, Any]: ...


def missing_execution_agent_source_methods(candidate: Any) -> list[str]:
    return [
        name for name in ("load_for_execution",) if not callable(getattr(candidate, name, None))
    ]


def validate_execution_agent_definition(raw: Any) -> ExecutionAgentDefinition:
    try:
        return ExecutionAgentDefinition.model_validate(raw)
    except ValidationError as exc:
        raise InvalidExecutionAgentDefinition(str(exc)) from exc


def get_execution_agent_source() -> ExecutionAgentSource | None:
    if not has_ext(EXECUTION_AGENT_SOURCE_KEY):
        return None
    return get_ext(EXECUTION_AGENT_SOURCE_KEY)


async def try_load_from_execution_source(
    resolved_id: str,
    *,
    is_version: bool = False,
) -> AgentConfig | None:
    """Return an AgentConfig from the host seam, or None when no source is configured."""
    source = get_execution_agent_source()
    if source is None:
        return None
    raw = await source.load_for_execution(resolved_id, is_version=is_version)
    definition = validate_execution_agent_definition(raw)
    if definition.definition_id != resolved_id:
        raise ValueError(
            "ExecutionAgentSource returned the wrong definition: "
            f"requested {resolved_id!r}, received {definition.definition_id!r}."
        )
    if definition.is_version != is_version:
        raise ValueError(
            "ExecutionAgentSource returned the wrong definition kind: "
            f"requested is_version={is_version}, received "
            f"is_version={definition.is_version}."
        )
    return definition_to_agent_config(definition)


def definition_from_row(row: Any, *, is_version: bool) -> ExecutionAgentDefinition:
    """Project an ORM-compatible row into the portable canonical definition."""

    definition_id = str(row.id)
    agent_id = str(row.agent_id) if is_version else definition_id
    revision_raw = (
        getattr(row, "changed_at", None) if is_version else getattr(row, "updated_at", None)
    )
    revision = (
        revision_raw.isoformat()
        if hasattr(revision_raw, "isoformat")
        else (str(revision_raw) if revision_raw else None)
    )
    model_id = str(row.model_id) if getattr(row, "model_id", None) else ""
    definition = validate_execution_agent_definition(
        {
            "definition_id": definition_id,
            "agent_id": agent_id,
            "is_version": is_version,
            "version_number": (
                int(row.version_number or 0) if is_version else int(getattr(row, "version", 0) or 0)
            ),
            "revision": revision,
            "name": str(getattr(row, "name", "") or ""),
            "model_id": model_id,
            "messages": list(getattr(row, "messages", None) or []),
            "settings": dict(getattr(row, "settings", None) or {}),
            "tools": [str(value) for value in (getattr(row, "tools", None) or [])],
            "custom_tools": list(getattr(row, "custom_tools", None) or []),
            "mcp_servers": [str(value) for value in (getattr(row, "mcp_servers", None) or [])],
            "variable_definitions": list(getattr(row, "variable_definitions", None) or []),
            "context_policies": list(getattr(row, "context_policies", None) or []),
            "auto_context_disabled": bool(getattr(row, "auto_context_disabled", False)),
            "tool_config": dict(getattr(row, "tool_config", None) or {}),
            "output_schema": (
                dict(row.output_schema)
                if isinstance(getattr(row, "output_schema", None), dict)
                else None
            ),
            "matrx_actions": (
                dict(row.matrx_actions)
                if isinstance(getattr(row, "matrx_actions", None), dict) and row.matrx_actions
                else None
            ),
            "skill_config": dict(getattr(row, "skill_config", None) or {}),
        }
    )
    return definition.with_content_hash()


def definition_to_agent_config(definition: ExecutionAgentDefinition) -> AgentConfig:
    """The one canonical definition -> AgentConfig -> UnifiedConfig mapper."""

    config_dict: dict[str, Any] = {
        **definition.settings,
        "messages": definition.messages,
        "model": definition.model_id,
        "tools": definition.tools,
        "custom_tools": definition.custom_tools,
        "mcp_servers": definition.mcp_servers,
    }
    config = UnifiedConfig.from_dict(config_dict)
    if definition.output_schema and config.response_format is None:
        config.response_format = {
            "type": "json_schema",
            "json_schema": definition.output_schema,
        }

    excluded_raw = definition.tool_config.get("excluded_tools")
    excluded_tools = (
        [str(value) for value in excluded_raw if isinstance(value, str)]
        if isinstance(excluded_raw, list)
        else []
    )

    from matrx_ai.skills.models import SkillConfig

    try:
        skill_config_obj = SkillConfig.from_jsonb(definition.skill_config)
    except Exception as exc:
        # Preserve the ORM mapper's long-standing defensive posture: a bad
        # optional skill-visibility blob must not make an otherwise valid
        # agent definition unexecutable.
        from matrx_utils import vcprint

        vcprint(
            {
                "raw": definition.skill_config,
                "error": str(exc),
                "agent_id": definition.definition_id,
            },
            "[agent_source] Invalid skill_config; using defaults",
            color="yellow",
        )
        skill_config_obj = SkillConfig()

    return AgentConfig(
        name=definition.name,
        config=config,
        variable_defaults=AgentVariable.from_list(definition.variable_definitions),
        context_policies=definition.context_policies,
        excluded_tools=excluded_tools,
        auto_tools_disabled=bool(definition.tool_config.get("auto_tools_disabled", False)),
        auto_context_disabled=definition.auto_context_disabled,
        output_schema=definition.output_schema,
        matrx_actions=definition.matrx_actions,
        skill_config=skill_config_obj,
    )


__all__ = [
    "ExecutionAgentDefinition",
    "ExecutionAgentSource",
    "InvalidExecutionAgentDefinition",
    "definition_from_row",
    "definition_to_agent_config",
    "get_execution_agent_source",
    "missing_execution_agent_source_methods",
    "try_load_from_execution_source",
    "validate_execution_agent_definition",
]
