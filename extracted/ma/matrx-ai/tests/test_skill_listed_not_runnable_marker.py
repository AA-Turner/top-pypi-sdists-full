"""A Listed skill whose tooling does not exist here says so in the line the model sees.

An agent with a skill on the LISTED tier sees only ``- <skill_id> — <description>``
until it chooses to load the body — and the "not yet runnable here" banner lives
in the body. So a row with ``config.tooling_not_runnable`` must carry its marker
in the listed line itself, or the model picks a skill whose steps it cannot run.

This drives the real path: DB-shaped row → ``_row_to_body`` (provider) →
``resolve_skills_for_agent`` → ``render_preamble``.
"""

from __future__ import annotations

from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.skills.models import SkillConfig, not_runnable_marker, not_runnable_tooling
from matrx_ai.skills.preamble import render_preamble
from matrx_ai.skills.providers import _row_to_body, _row_to_hint
from matrx_ai.skills.resolver import resolve_skills_for_agent

TOOLING = ["the pack's own command-line tool", "Medialyst (the authors' commercial PR data service)"]


def _row(skill_id: str, config: dict) -> SimpleNamespace:
    return SimpleNamespace(
        id=uuid4(),
        skill_id=skill_id,
        label=skill_id.title(),
        description=f"What {skill_id} does.",
        skill_type="reference",
        body="# body",
        allowed_tools=[],
        trigger_patterns=[],
        disable_auto_invocation=False,
        version=1,
        config=config,
    )


class _Provider:
    def __init__(self, rows):
        self._rows = {r.id: r for r in rows}

    async def category_overview(self, *, user_id=None):
        return []

    async def get_by_id(self, skill_uuid, *, user_id=None):
        row = self._rows.get(skill_uuid)
        return _row_to_body(row, []) if row else None


@pytest.mark.asyncio
async def test_listed_line_carries_the_not_runnable_marker():
    needs = _row("news-search", {"tooling_not_runnable": TOOLING})
    plain = _row("meanest-editor", {"ingested_from": "outside_pack"})
    agent = SimpleNamespace(skill_config=SkillConfig(listed=[needs.id, plain.id]))

    resolved = await resolve_skills_for_agent(agent, _Provider([needs, plain]))
    text = render_preamble(resolved.preamble)

    assert (
        "- news-search — What news-search does. (needs tooling not in AI Matrx yet: "
        "the pack's own command-line tool; Medialyst (the authors' commercial PR data service))"
    ) in text
    # An ordinary row's line is byte-identical to before (prompt-cache stability).
    assert "- meanest-editor — What meanest-editor does.\n" in text


def test_hints_from_list_and_search_carry_the_flag_too():
    hint = _row_to_hint(_row("pr-calendar", {"tooling_not_runnable": TOOLING}), [])
    assert hint.not_runnable == TOOLING
    assert hint.model_dump(mode="json")["not_runnable"] == TOOLING


def test_shared_reader_tolerates_bad_shapes():
    assert not_runnable_tooling(None) == []
    assert not_runnable_tooling({"tooling_not_runnable": "cron"}) == []
    assert not_runnable_tooling({"tooling_not_runnable": ["", " cron ", 3]}) == ["cron"]
    assert not_runnable_marker([]) == ""
