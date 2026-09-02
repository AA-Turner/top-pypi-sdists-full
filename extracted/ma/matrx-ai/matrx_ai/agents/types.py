"""
Shared types for the prompts/agent system.

This module contains dataclasses and type definitions used across
the prompts and agent modules to avoid circular imports.
"""

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from matrx_ai.agents.variables import AgentVariable
from matrx_ai.config.unified_config import UnifiedConfig

if TYPE_CHECKING:
    from matrx_ai.skills.models import SkillConfig


@dataclass
class AgentConfig:
    """
    Configuration for creating an Agent instance.

    This is the return type from manager.to_config() methods.
    Contains all necessary components to initialize an Agent.

    Attributes:
        name: Display name for the agent
        config: UnifiedConfig instance with messages, model settings, etc.
        variable_defaults: Dictionary of variable definitions (name -> AgentVariable)
        context_policies: Agent-defined deferred context policy descriptors (from prompts.context_policies).
        excluded_tools: Per-agent deny list — names filtered out of the resolved
            tool set regardless of source (capability, request, agent's own
            definition, dynamic injection). Phase C of TOOL_INJECTION_REFACTOR.md.
        auto_tools_disabled: Kill switch — when True, automatic tool injection
            paths are short-circuited (capabilities, request-side adds, editable
            tools). The agent's own explicitly-declared tools still apply.
            Phase C of TOOL_INJECTION_REFACTOR.md.
        auto_context_disabled: The EXACT mirror of auto_tools_disabled, for the
            context channel (``agent.definition.auto_context_disabled``). When
            True, ONLY the agent's explicitly-declared Context Policies deliver
            — every undeclared key the surface offers is dropped before the
            model sees it. The switch stops AUTOMATIC injection; the agent's own
            declarations still apply. Default False = today's behaviour
            (undeclared context flows), now a named, visible setting rather than
            an unexamined default. See
            common-docs/systems/mandates/FEATURE.md § "Context Policy — and the
            kill switch".
        output_schema: Declared structured-output envelope from the DB record
            (OpenAI ``response_format`` shape: ``{name, schema, strict}``).
            Read by ``parse_agent_output`` so any consumer of the agent's text
            output gets schema-aware JSON extraction for free.
    """

    name: str
    config: UnifiedConfig
    variable_defaults: dict[str, AgentVariable]
    context_policies: list[dict[str, Any]] = field(default_factory=list)
    excluded_tools: list[str] = field(default_factory=list)
    auto_tools_disabled: bool = False
    auto_context_disabled: bool = False
    output_schema: dict[str, Any] | None = None
    # Opaque host-interpreted apply config from the ``agx_agent.matrx_actions``
    # column. matrx-ai never reads its contents — it only carries it so the host's
    # output-apply dispatcher can declare a directive ON the agent (the agent
    # emits a plain payload; the host wraps + applies it). ``None`` = not declared.
    matrx_actions: dict[str, Any] | None = None
    # Per-agent skill visibility config (skill.definition tiering). Loaded from
    # ``agx_agent.skill_config`` JSONB. ``None`` = column absent (defensive);
    # an explicit empty SkillConfig() means "no opinions, default tiers apply."
    # See ``matrx_ai.skills.models.SkillConfig``.
    skill_config: "SkillConfig | None" = None
