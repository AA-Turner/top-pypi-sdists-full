"""Generated skills (one per tool, bundle, shape) never change the preamble's skill overview.

The overview ("You have access to N skills across: …") is rendered into the cached system preamble
of every agent with skills. A generated row must leave it byte-identical (chat-agent-skills lane F
review, 2026-11-19: 2,515 coverage rows moved it for 17 agents)."""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from uuid import uuid4

from matrx_ai.skills import providers
from matrx_ai.skills.models import SkillHint
from matrx_ai.skills.resolver import render_overview_lines


def _row(category: str, *, config=None, metadata=None):
    return SimpleNamespace(id=uuid4(), category=category, config=config or {}, metadata=metadata or {})


def _overview(rows) -> str:
    p = providers.DbSkillProvider.__new__(providers.DbSkillProvider)
    cats = [SimpleNamespace(slug=c, name=c, parent_id=None, position=i, metadata={"description": c})
            for i, c in enumerate(["conventions", "tool-guides", "render-blocks"])]

    async def ensure():
        return None

    async def load_cats():
        return cats

    async def hints(**kw):
        return [SkillHint(id=r.id, skill_id=str(r.id), label="x", description="x", skill_type="reference",
                          category_path=[r.category]) for r in rows]

    async def all_rows():
        return rows

    p._ensure_categories, p._load_category_rows, p.list_hints, p._get_all_active_rows = ensure, load_cats, hints, all_rows
    out = asyncio.run(p.category_overview(user_id=None))
    return "\n".join(render_overview_lines(out)) + f"\nTOTAL {sum(c for _, _, c in out)}"


BASE = [_row("conventions"), _row("conventions"), _row("render-blocks", metadata={"created_via": "kind_create_skill"})]
COVERAGE = _row("tool-guides", config={"ingested_from": "skill_coverage"})
#: a family skill (one per cluster of near-identical tools): a coverage row like the rest
FAMILY = _row("tool-guides", config={"ingested_from": "skill_coverage", "skill_coverage": {"family": "tool_family"}})
NEW_SHAPE = _row("render-blocks", metadata={"created_via": "kind_create_skill", "in_skill_overview": False})


def test_generated_rows_leave_the_overview_bytes_identical():
    before = _overview(BASE)
    assert _overview([*BASE, COVERAGE, NEW_SHAPE]) == before
    assert "TOTAL 3" in before  # an existing shape skill keeps counting: today's bytes are kept


def test_family_skills_leave_the_overview_bytes_identical():
    before = _overview(BASE)
    assert _overview([*BASE, FAMILY, FAMILY, COVERAGE]) == before


def test_the_check_can_fail(monkeypatch):
    """Without the exclusion the same rows DO move the bytes — the guard above is not vacuous."""
    monkeypatch.setattr(providers, "counts_in_overview", lambda row: True)
    assert _overview([*BASE, COVERAGE, NEW_SHAPE]) != _overview(BASE)
    assert _overview([*BASE, FAMILY]) != _overview(BASE)
