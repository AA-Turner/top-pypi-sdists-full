from __future__ import annotations

from uuid import UUID

import pytest

from matrx_ai.skills.providers import DbSkillProvider


@pytest.mark.asyncio
async def test_owned_scope_never_loads_the_public_skill_catalog(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    provider = DbSkillProvider()
    user_id = UUID("33333333-3333-4333-8333-333333333333")
    owned = type("SkillRow", (), {"id": "owned", "category_id": None})()

    async def fake_owned(actual_user_id: UUID) -> list[object]:
        assert actual_user_id == user_id
        return [owned]

    async def fail_public() -> list[object]:
        raise AssertionError("owned scope must not load public skills")

    monkeypatch.setattr(provider, "_get_user_rows", fake_owned)
    monkeypatch.setattr(provider, "_get_system_public_rows", fail_public)

    rows = await provider._fetch_visible(user_id=user_id, scope="owned")

    assert rows == [owned]


@pytest.mark.asyncio
async def test_visible_scope_unions_public_and_owned_skills(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    provider = DbSkillProvider()
    user_id = UUID("33333333-3333-4333-8333-333333333333")
    public = type("SkillRow", (), {"id": "public", "category_id": None})()
    owned = type("SkillRow", (), {"id": "owned", "category_id": None})()

    async def fake_owned(_user_id: UUID) -> list[object]:
        return [owned]

    async def fake_public() -> list[object]:
        return [public]

    monkeypatch.setattr(provider, "_get_user_rows", fake_owned)
    monkeypatch.setattr(provider, "_get_system_public_rows", fake_public)

    rows = await provider._fetch_visible(user_id=user_id, scope="visible")

    assert rows == [public, owned]
