"""Resolve an agent's DECLARED prompt blocks once, on the first turn.

Ladder (owner ruling R1, 2026-10-10): personal (only when the runner is the agent's creator and the
run organization's ``prompt_blocks/personal_rung`` knob is on) > the run's organization > system.
A declared block with no row at any rung — or a skill-linked block whose skill is gone — refuses the
run (:class:`PromptBlocksMissing`) before any provider call. Block text is a value: never filled.
"""

from __future__ import annotations

import logging
from typing import Any

from matrx_ai.prompt_blocks.conditions import matches
from matrx_ai.prompt_blocks.errors import PromptBlocksMissing, PromptBlockSourceUnavailable
from matrx_ai.prompt_blocks.models import LEVEL_ORDER, BlockRow, ModelFacts, ResolvedBlock
from matrx_ai.prompt_blocks.source import BlockSource, get_block_source

logger = logging.getLogger(__name__)

#: A tool-bound block whose tool the run does not carry: it sends "", and says so.
OFF_TOOL_NOT_IN_RUN = "tool not in run"


def declared_names(raw: Any) -> list[str]:
    """``[{"name": "x"}]`` (or bare strings) -> ordered, deduped names."""
    names: list[str] = []
    for item in raw or []:
        name = item.get("name") if isinstance(item, dict) else item
        if isinstance(name, str) and name.strip() and name.strip() not in names:
            names.append(name.strip())
    return names


def _run_tool_names(config: Any) -> set[str]:
    raw = [t for t in (getattr(config, "tools", None) or []) if isinstance(t, str)]
    names = set(raw)
    try:
        from matrx_ai.tools.merge import canonical_tool_names

        names.update(n for n in canonical_tool_names(raw) if isinstance(n, str))
    except Exception:
        pass
    for tool in getattr(config, "custom_tools", None) or []:
        name = getattr(tool, "name", None) or (tool.get("name") if isinstance(tool, dict) else None)
        if name:
            names.add(str(name))
    return names


def _pick(rows: list[BlockRow], allow_personal: bool) -> dict[str, BlockRow]:
    chosen: dict[str, BlockRow] = {}
    for level in LEVEL_ORDER:
        if level == "personal" and not allow_personal:
            continue
        for row in rows:
            if row.level == level and row.name not in chosen:
                chosen[row.name] = row
    return chosen


async def resolve_declared_blocks(
    config: Any,
    *,
    runner_id: str | None,
    organization_id: str | None,
    source: BlockSource | None = None,
) -> list[ResolvedBlock]:
    """Fill ``config.prompt_block_texts`` / ``prompt_block_report`` / ``prompt_block_tool_ids``.

    Idempotent: a config already resolved is left as it is (frozen with the conversation)."""
    names = declared_names(getattr(config, "prompt_blocks", None))
    if getattr(config, "prompt_block_texts", None) is not None:
        return []
    if not names:
        config.prompt_block_texts = {}
        return []
    source = source or get_block_source()
    if source is None:
        raise PromptBlockSourceUnavailable()

    creator = getattr(config, "prompt_block_creator", None)
    allow_personal = bool(
        runner_id and creator and str(runner_id) == str(creator)
        and await source.personal_rung_enabled(organization_id)
    )
    rows = await source.candidates(
        names,
        organization_id=organization_id,
        personal_user_id=str(runner_id) if allow_personal else None,
    )
    chosen = _pick(rows, allow_personal)
    missing = [n for n in names if n not in chosen]

    facts: ModelFacts | None = None
    facts_loaded = False
    reasoning_raw = getattr(config, "reasoning_effort", None)
    reasoning = None if reasoning_raw is None else str(getattr(reasoning_raw, "value", reasoning_raw))
    run_tools = _run_tool_names(config)

    resolved: list[ResolvedBlock] = []
    tool_ids: list[str] = []
    for name in names:
        row = chosen.get(name)
        if row is None:
            continue
        if row.bound_tool and row.bound_tool not in run_tools:
            logger.info(
                "prompt block %r is off: its tool %r is not in this run (tools: %s)",
                name, row.bound_tool, sorted(run_tools) or "none",
            )
            resolved.append(
                ResolvedBlock(
                    name, "", row.level, row.id, None, row.source_kind, row.bound_tool,
                    off=OFF_TOOL_NOT_IN_RUN,
                )
            )
            continue
        variant = None
        if row.variants:
            if not facts_loaded:
                facts = await source.model_facts(str(getattr(config, "model", "") or ""))
                facts_loaded = True
            for candidate in sorted(row.variants, key=lambda v: v.sort_order):
                if matches(candidate.condition, facts, reasoning):
                    variant = candidate
                    break
        skill_id = None
        if row.source_kind == "skill":
            skill = await source.skill(row.source_ref or "")
            if skill is None:
                missing.append(name)
                continue
            skill_id = skill.skill_id
            text = variant.content if variant else skill.body
            if not skill.disable_auto_invocation:
                tool_ids.extend(str(t) for t in skill.allowed_tools)
        else:
            text = variant.content if variant else row.content
        resolved.append(
            ResolvedBlock(
                name, text, row.level, row.id, variant.id if variant else None,
                row.source_kind, row.bound_tool, skill_id,
            )
        )

    if missing:
        raise PromptBlocksMissing(missing)

    config.prompt_block_texts = {b.name: b.text for b in resolved}
    config.prompt_block_report = [b.report() for b in resolved]
    config.prompt_block_tool_ids = list(dict.fromkeys(tool_ids))
    if tool_ids:
        add_block_tools(config)
    return resolved


def add_block_tools(config: Any) -> None:
    """Skill-linked blocks' tools join the run (canonical names, deduped)."""
    ids = list(getattr(config, "prompt_block_tool_ids", None) or [])
    if not ids:
        return
    try:
        from matrx_ai.tools.merge import canonical_tool_names

        names = canonical_tool_names(ids)
    except Exception:
        names = ids
    existing = {str(t) for t in (config.tools or [])}
    added = [n for n in names if isinstance(n, str) and n not in existing]
    if added:
        config.tools = list(config.tools or []) + added
