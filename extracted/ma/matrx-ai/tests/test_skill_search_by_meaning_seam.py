"""The ``skill`` tool's search ranks by meaning through the host's ``skill_search`` seam, never widening access.

``DbSkillProvider.search`` hands the seam only the skills the caller may read; the seam's ranking is
taken in its order, any id it returns that the caller cannot read is dropped, an exact skill id still
comes first, and a failing or absent seam leaves the keyword scoring answering (chat-agent-skills lane D).
"""

from __future__ import annotations

from uuid import UUID

import pytest

from matrx_ai import _ext
from matrx_ai.skills import providers
from matrx_ai.skills.models import SkillHint
from matrx_ai.skills.providers import DbSkillProvider


def _hint(n: int, skill_id: str, label: str, description: str) -> SkillHint:
    return SkillHint(
        id=UUID(f"00000000-0000-4000-8000-{n:012d}"),
        skill_id=skill_id,
        label=label,
        description=description,
        skill_type="reference",
    )


READABLE = [
    _hint(1, "forms-and-capture", "Forms and capture", "Send something in by link."),
    _hint(2, "slide-decks", "Presentations", "Build a deck of slides from an outline."),
    _hint(3, "spaces-and-pages", "Spaces and pages", "A wiki or handbook."),
]
NOT_READABLE = "00000000-0000-4000-8000-000000000099"


@pytest.fixture
def provider(monkeypatch: pytest.MonkeyPatch) -> DbSkillProvider:
    p = DbSkillProvider()

    async def fake_hints(**_kwargs: object) -> list[SkillHint]:
        return list(READABLE)

    async def no_body(*_args: object, **_kwargs: object) -> None:
        return None

    monkeypatch.setattr(p, "list_hints", fake_hints)
    monkeypatch.setattr(p, "get_by_id", no_body)
    return p


@pytest.mark.asyncio
async def test_the_seam_ranks_only_readable_skills(provider: DbSkillProvider, monkeypatch: pytest.MonkeyPatch) -> None:
    seen: list[list[str]] = []

    async def seam(query: str, skills: list[SkillHint], *, limit: int) -> list[str]:
        seen.append([str(s.id) for s in skills])
        return [NOT_READABLE, str(READABLE[1].id), str(READABLE[0].id)]

    monkeypatch.setitem(_ext._registry, "skill_search", seam)
    hits = await provider.search("make a pitch for investors", limit=5)
    assert seen == [[str(h.id) for h in READABLE]], "the seam was handed something other than the readable skills"
    assert [h.skill_id for h in hits] == ["slide-decks", "forms-and-capture"]
    assert NOT_READABLE not in {str(h.id) for h in hits}, "a skill the caller cannot read was returned"


@pytest.mark.asyncio
async def test_an_exact_skill_id_still_comes_first(provider: DbSkillProvider, monkeypatch: pytest.MonkeyPatch) -> None:
    async def seam(query: str, skills: list[SkillHint], *, limit: int) -> list[str]:
        return [str(READABLE[1].id), str(READABLE[2].id)]

    monkeypatch.setitem(_ext._registry, "skill_search", seam)
    hits = await provider.search("Spaces-And-Pages", limit=5)
    assert hits[0].skill_id == "spaces-and-pages"


@pytest.mark.asyncio
async def test_a_failing_seam_falls_back_to_keywords(provider: DbSkillProvider, monkeypatch: pytest.MonkeyPatch) -> None:
    async def seam(query: str, skills: list[SkillHint], *, limit: int) -> list[str]:
        raise RuntimeError("embedding provider down")

    monkeypatch.setitem(_ext._registry, "skill_search", seam)
    monkeypatch.setattr(providers, "_meaning_failure_announced", False)
    hits = await provider.search("wiki", limit=5)
    assert [h.skill_id for h in hits] == ["spaces-and-pages"]


@pytest.mark.asyncio
async def test_no_seam_means_keyword_scoring(provider: DbSkillProvider, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delitem(_ext._registry, "skill_search", raising=False)
    hits = await provider.search("wiki", limit=5)
    assert [h.skill_id for h in hits] == ["spaces-and-pages"]
