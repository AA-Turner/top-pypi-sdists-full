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

from collections.abc import Sequence
from typing import TYPE_CHECKING
from uuid import UUID

from matrx_ai.skills.models import (
    ResolvedSkills,
    SkillBody,
    SkillConfig,
    SkillHint,
    SkillPreamble,
    SkillTier,
)
from matrx_ai.skills.knobs import outline_min_chars, set_max_depth, skill_bodies_budget
from matrx_ai.skills.preamble import render_overview_lines
from matrx_ai.skills.sections import compact_outline

if TYPE_CHECKING:
    from matrx_ai.agents.types import AgentConfig
    from matrx_ai.skills.providers import SkillProvider


# Sets may nest; deeper than agents.context.skill_set_max_depth is treated as a loop and stops.
# A listed REFERENCE skill longer than agents.context.skill_outline_min_chars gets its heading
# outline on its preamble line (the same size as one ``skill get`` page). Both: skills/knobs.py.


async def expand_skill_sets(
    cfg: SkillConfig,
    provider: "SkillProvider",
    *,
    user_id: UUID | None = None,
    bodies: dict[UUID, SkillBody | None] | None = None,
) -> SkillConfig:
    """Replace every skill SET id in each tier with its members, in order, at run time.

    A set placed in ``included`` includes all its members, in ``listed`` lists them, in
    ``forbidden`` forbids them. Sets may nest (loop-safe). Order is declaration order with
    the first occurrence kept; a skill both included and listed stays included. The set
    rows themselves never reach the preamble — only their members do. ``bodies`` (when
    given) is filled with every row fetched so the caller never loads one twice.
    """
    cache: dict[UUID, SkillBody | None] = bodies if bodies is not None else {}

    async def load(uid: UUID) -> SkillBody | None:
        if uid not in cache:
            cache[uid] = await provider.get_by_id(uid, user_id=user_id)
        return cache[uid]

    max_depth = set_max_depth()

    async def expand(ids: list[UUID]) -> list[UUID]:
        out: list[UUID] = []

        async def walk(uid: UUID, trail: tuple[UUID, ...]) -> None:
            if uid in trail or len(trail) > max_depth:
                return
            body = await load(uid)
            if body is not None and body.is_set:
                for member in body.set_members:
                    await walk(member, (*trail, uid))
                return
            if uid not in out:
                out.append(uid)

        for uid in ids:
            await walk(uid, ())
        return out

    if not (cfg.included or cfg.listed or cfg.forbidden):
        return cfg
    included = await expand(cfg.included)
    listed = [u for u in await expand(cfg.listed) if u not in included]
    forbidden = await expand(cfg.forbidden)
    return SkillConfig(
        included=included, listed=listed, forbidden=forbidden, disabled=cfg.disabled
    )


async def resolve_skills_for_agent(
    agent_config: "AgentConfig",
    provider: "SkillProvider",
    *,
    user_id: UUID | None = None,
    carried: Sequence[SkillBody] = (),
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
        * ``carried`` — skills attached because the run's tool set includes a
          tool they declare in ``config.attach_with_tools`` (the third input,
          MODULE_README "two-input rule"). Appended to the included tier after
          the agent's own, deduped by id, never when the agent forbids them.
    """
    raw_cfg: SkillConfig = agent_config.skill_config or SkillConfig()

    if raw_cfg.disabled:
        return ResolvedSkills(
            preamble=SkillPreamble(),
            tools_to_inject=[],
            config=raw_cfg,
            disabled=True,
        )

    # 0. Skill SETS resolve to their members now — adding a doc to a set reaches every
    #    agent that attaches it. The returned ``config`` is the EXPANDED one, so the
    #    ``skill`` tool's forbidden check sees members of a forbidden set.
    bodies: dict[UUID, SkillBody | None] = {}
    cfg = await expand_skill_sets(raw_cfg, provider, user_id=user_id, bodies=bodies)

    async def load(uid: UUID) -> SkillBody | None:
        if uid not in bodies:
            bodies[uid] = await provider.get_by_id(uid, user_id=user_id)
        return bodies[uid]

    # 1. Category overview — always rendered; this is the "hint that skills
    #    exist" the agent sees by default.
    overview_rows = await provider.category_overview(user_id=user_id)
    overview_lines = render_overview_lines(overview_rows)
    total_active = sum(count for _, _, count in overview_rows)

    def hint_for(body: SkillBody, tier: SkillTier) -> SkillHint:
        long_reference = body.skill_type == "reference" and len(body.body) > outline_min_chars()
        return SkillHint(
            id=body.id,
            skill_id=body.skill_id,
            label=body.label,
            description=body.description,
            skill_type=body.skill_type,
            category_path=body.category_path,
            has_resources=False,
            has_allowed_tools=bool(body.allowed_tools),
            tier=tier,
            not_runnable=body.not_runnable,
            outline=compact_outline(body.body) if long_reference else "",
            total_chars=len(body.body) if long_reference else None,
        )

    # 2. Listed skills — name + description only.
    listed_skills: list[SkillHint] = []
    for skill_uuid in cfg.listed:
        if cfg.is_forbidden(skill_uuid):
            continue
        body = await load(skill_uuid)
        if body is None:
            continue
        listed_skills.append(hint_for(body, SkillTier.LISTED))

    # 3. Included skills — full body. Resolve in declaration order.
    included_skills = []
    tools_to_inject: list[UUID] = []
    seen_tools: set[UUID] = set()
    for skill_uuid in cfg.included:
        if cfg.is_forbidden(skill_uuid):
            continue
        body = await load(skill_uuid)
        if body is None:
            continue
        included_skills.append(body)
        if not body.disable_auto_invocation:
            for tool_uuid in body.allowed_tools:
                if tool_uuid in seen_tools:
                    continue
                seen_tools.add(tool_uuid)
                tools_to_inject.append(tool_uuid)

    # 4. Tool-carried skills — the platform attaches them wherever their tools are.
    included_ids = {b.id for b in included_skills}
    for body in carried:
        if body.id in included_ids or cfg.is_forbidden(body.id):
            continue
        included_ids.add(body.id)
        included_skills.append(body)
        if not body.disable_auto_invocation:
            for tool_uuid in body.allowed_tools:
                if tool_uuid in seen_tools:
                    continue
                seen_tools.add(tool_uuid)
                tools_to_inject.append(tool_uuid)

    # 5. Every automatic block is bounded: whole bodies up to the attach budget (the same
    #    knob a continuation turn uses), the overflow is LISTED instead (hint + section outline),
    #    on every turn including the first, and the preamble says so in one line. Order is kept:
    #    the skills the author put first keep their bodies.
    budget = skill_bodies_budget()
    kept: list[SkillBody] = []
    demoted: list[SkillBody] = []
    used = 0
    for body in included_skills:
        if used + len(body.body) <= budget:
            kept.append(body)
            used += len(body.body)
        else:
            demoted.append(body)
    for body in demoted:
        listed_skills.append(hint_for(body, SkillTier.LISTED))

    preamble = SkillPreamble(
        overview_lines=overview_lines,
        listed_skills=listed_skills,
        included_skills=kept,
        total_active_count=total_active,
        demoted_count=len(demoted),
        demoted_chars=sum(len(b.body) for b in demoted),
        body_budget_chars=budget,
    )

    return ResolvedSkills(
        preamble=preamble,
        tools_to_inject=tools_to_inject,
        config=cfg,
        disabled=False,
    )
