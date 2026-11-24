"""A skill is found by its exact name.

2026-11-03: an in-chat agent searched ``dashboards-and-kpis`` (the skill's own
skill_id, the name every skill link carries) and got 0 hints — search scored
only the label and description, split on spaces, so a hyphenated id matched
nothing and the skill turned up only under other keywords.
"""

from __future__ import annotations

from uuid import UUID

import pytest

from matrx_ai.skills.models import SkillHint
from matrx_ai.skills.providers import DbSkillProvider


def _hint(n: int, skill_id: str, label: str, description: str) -> SkillHint:
    return SkillHint(
        id=UUID(f"00000000-0000-4000-8000-{n:012d}"),
        skill_id=skill_id,
        label=label,
        description=description,
        skill_type="reference",
        category_path=[],
        has_resources=False,
        has_allowed_tools=False,
    )


HINTS = [
    _hint(1, "forms-and-capture", "Forms and capture", "Send something in by link."),
    _hint(2, "dashboards-and-kpis", "Dashboards and KPIs on live tables", "How are we doing."),
    _hint(3, "spaces-and-pages", "Spaces and pages", "A wiki or handbook."),
]


@pytest.fixture
def provider(monkeypatch: pytest.MonkeyPatch) -> DbSkillProvider:
    p = DbSkillProvider()

    async def fake_hints(**_kwargs: object) -> list[SkillHint]:
        return list(HINTS)

    async def no_body(*_args: object, **_kwargs: object) -> None:
        return None

    monkeypatch.setattr(p, "list_hints", fake_hints)
    monkeypatch.setattr(p, "get_by_id", no_body)
    return p


@pytest.mark.asyncio
@pytest.mark.parametrize("query", ["dashboards-and-kpis", "Dashboards-And-KPIs", " dashboards-and-kpis "])
async def test_search_by_exact_skill_id_answers_that_skill_first(provider: DbSkillProvider, query: str) -> None:
    hits = await provider.search(query, limit=5)
    assert hits, f"search({query!r}) found nothing"
    assert hits[0].skill_id == "dashboards-and-kpis"


@pytest.mark.asyncio
async def test_every_skill_is_reachable_by_its_own_skill_id(provider: DbSkillProvider) -> None:
    for h in HINTS:
        hits = await provider.search(h.skill_id, limit=5)
        assert hits and hits[0].skill_id == h.skill_id, h.skill_id


@pytest.mark.parametrize(
    "raw",
    ["dashboards-and-kpis", "/skills/dashboards-and-kpis/SKILL.md", "skills/dashboards-and-kpis/SKILL.md",
     "common-docs/skills/dashboards-and-kpis/SKILL.md", "dashboards-and-kpis/SKILL.md"],
)
def test_a_skill_link_names_its_skill_id(raw: str) -> None:
    from matrx_ai.tools.implementations.skill import skill_key_from_reference

    assert skill_key_from_reference(raw) == "dashboards-and-kpis"
