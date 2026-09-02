"""Request-time skill resolution.

Reads ``AgentConfig.skill_config`` (already parsed by ``_row_to_config``),
calls the provider to fetch the right bodies/hints, and returns a
``ResolvedSkills`` envelope the request-prep layer hands to the preamble
renderer + tool merger.

Hot rule: this resolver runs ONCE per request, BEFORE the agent's first
provider call (cache stability — A1). Mid-flight ``skill_get`` calls
bypass this resolver entirely.
"""
from __future__ import annotations

from typing import TYPE_CHECKING
from uuid import UUID

from matrx_ai.skills.models import (
    ResolvedSkills,
    SkillConfig,
    SkillHint,
    SkillPreamble,
    SkillTier,
)
from matrx_ai.skills.preamble import render_overview_lines

if TYPE_CHECKING:
    from matrx_ai.agents.types import AgentConfig
    from matrx_ai.skills.providers import SkillProvider


async def resolve_skills_for_agent(
    agent_config: "AgentConfig",
    provider: "SkillProvider",
    *,
    user_id: UUID | None = None,
) -> ResolvedSkills:
    """Build the request-time skill envelope from the agent's config.

    Returns:
        ResolvedSkills with the preamble (overview + listed + included)
        and the list of tool UUIDs to merge into the request's tool surface.

    Behavior:
        * ``disabled=True`` short-circuits — empty preamble, no tools.
        * Forbidden ids are stripped from every output.
        * Included skills with ``disable_auto_invocation=True`` do NOT
          contribute to ``tools_to_inject`` (SK-R8 / agent stays in control).
        * The overview is generated even when no skills are pre-configured,
          so the agent always knows the library exists and how to search.
    """
    cfg: SkillConfig = agent_config.skill_config or SkillConfig()

    if cfg.disabled:
        return ResolvedSkills(
            preamble=SkillPreamble(),
            tools_to_inject=[],
            config=cfg,
            disabled=True,
        )

    # 1. Category overview — always rendered; this is the "hint that skills
    #    exist" the agent sees by default.
    overview_rows = await provider.category_overview(user_id=user_id)
    overview_lines = render_overview_lines(overview_rows)
    total_active = sum(count for _, _, count in overview_rows)

    # 2. Listed skills — name + description only.
    listed_skills: list[SkillHint] = []
    for skill_uuid in cfg.listed:
        if cfg.is_forbidden(skill_uuid):
            continue
        body = await provider.get_by_id(skill_uuid, user_id=user_id)
        if body is None:
            continue
        listed_skills.append(
            SkillHint(
                id=body.id,
                skill_id=body.skill_id,
                label=body.label,
                description=body.description,
                skill_type=body.skill_type,
                category_path=body.category_path,
                has_resources=False,
                has_allowed_tools=bool(body.allowed_tools),
                tier=SkillTier.LISTED,
            )
        )

    # 3. Included skills — full body. Resolve in declaration order.
    included_skills = []
    tools_to_inject: list[UUID] = []
    seen_tools: set[UUID] = set()
    for skill_uuid in cfg.included:
        if cfg.is_forbidden(skill_uuid):
            continue
        body = await provider.get_by_id(skill_uuid, user_id=user_id)
        if body is None:
            continue
        included_skills.append(body)
        if not body.disable_auto_invocation:
            for tool_uuid in body.allowed_tools:
                if tool_uuid in seen_tools:
                    continue
                seen_tools.add(tool_uuid)
                tools_to_inject.append(tool_uuid)

    preamble = SkillPreamble(
        overview_lines=overview_lines,
        listed_skills=listed_skills,
        included_skills=included_skills,
        total_active_count=total_active,
    )

    return ResolvedSkills(
        preamble=preamble,
        tools_to_inject=tools_to_inject,
        config=cfg,
        disabled=False,
    )
