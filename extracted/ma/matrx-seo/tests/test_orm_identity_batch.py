from __future__ import annotations

from typing import Any

import pytest

from matrx_seo import ResolvedSeoIdentity, SeoIdentityRequest
from matrx_seo.orm_identity import OrmSeoIdentityResolver, upsert_keywords


@pytest.mark.asyncio
async def test_upsert_keywords_uses_one_ordered_batch(monkeypatch) -> None:
    calls: list[tuple[Any, ...]] = []

    async def fake_call_db_function(*args: Any) -> list[dict[str, Any]]:
        calls.append(args)
        return [
            {"input_index": 1, "o_id": "second-id", "o_created": False},
            {"input_index": 0, "o_id": "first-id", "o_created": True},
        ]

    monkeypatch.setattr(
        "matrx_seo.orm_identity.call_db_function",
        fake_call_db_function,
    )

    result = await upsert_keywords([(" First keyword ", "en"), ("Second keyword", "es")])

    assert result == [("first-id", True), ("second-id", False)]
    assert len(calls) == 1
    assert calls[0][1] == "seo.fn_upsert_keywords"
    assert calls[0][2] == [
        {"phrase": " First keyword ", "language": "en"},
        {"phrase": "Second keyword", "language": "es"},
    ]


@pytest.mark.asyncio
async def test_resolve_many_preserves_batch_keyword_mapping(monkeypatch) -> None:
    resolver = OrmSeoIdentityResolver()

    async def fake_upsert_keywords(
        _items: list[tuple[str, str]],
    ) -> list[tuple[str, bool]]:
        return [("first-id", True), ("second-id", False)]

    async def fake_resolve_with_keyword_id(
        _request: Any,
        _identity: SeoIdentityRequest,
        keyword_id: str,
    ) -> ResolvedSeoIdentity:
        return ResolvedSeoIdentity(keyword_id=keyword_id)

    monkeypatch.setattr(
        "matrx_seo.orm_identity.upsert_keywords",
        fake_upsert_keywords,
    )
    monkeypatch.setattr(
        resolver,
        "_resolve_with_keyword_id",
        fake_resolve_with_keyword_id,
    )

    identities = [
        SeoIdentityRequest(keyword="first"),
        SeoIdentityRequest(keyword="second"),
    ]
    resolved = await resolver.resolve_many(object(), identities)  # type: ignore[arg-type]

    assert [item.keyword_id for item in resolved] == ["first-id", "second-id"]


@pytest.mark.asyncio
async def test_upsert_keywords_rejects_incomplete_results(monkeypatch) -> None:
    async def fake_call_db_function(*_args: Any) -> list[dict[str, Any]]:
        return [{"input_index": 0, "o_id": "first-id", "o_created": True}]

    monkeypatch.setattr(
        "matrx_seo.orm_identity.call_db_function",
        fake_call_db_function,
    )

    with pytest.raises(RuntimeError, match="returned 1 rows for 2 inputs"):
        await upsert_keywords([("first", "en"), ("second", "en")])
