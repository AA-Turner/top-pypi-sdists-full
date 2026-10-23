"""A SERP re-collection replaces the provider's own fields and nothing else.

``seo.serp_mention.extras`` holds the provider's result fields (rank_group,
breadcrumb, timestamp …) WHOLE under ``serp_result``, beside other writers' keys
(the link check's ``link_check`` / ``broken_links``). A re-collection must replace
that sub-key exactly — a field the provider stopped sending goes — drop the
pre-sub-key top-level copies, and keep every other key. The double applies the SQL
expressions the way Postgres does, so it holds what the database would.
"""

from __future__ import annotations

from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any

import pytest
from matrx_orm import JsonbMerge, JsonbRemoveKeys

import matrx_seo.orm_repository as repo
from matrx_seo.db import models_seo as m


def _apply(current: dict[str, Any], expr: Any) -> dict[str, Any]:
    """Evaluate a JsonbMerge / JsonbRemoveKeys over ``current`` as Postgres would."""
    if isinstance(expr, JsonbRemoveKeys):
        return {k: v for k, v in current.items() if k not in expr.keys}
    if isinstance(expr, JsonbMerge):
        inner = expr.args[0]
        base = current if isinstance(inner, str) else _apply(current, inner)
        return {**base, **expr.value}
    return expr  # a whole value


class _Mention:
    def __init__(self, extras: dict[str, Any]) -> None:
        self.extras = extras
        self.rank = 3
        self.query = "q"
        self.variant = "v"

    async def update(self, **kw: Any) -> _Mention:
        self.extras = _apply(self.extras, kw["extras"])
        return self


class _Q:
    def __init__(self, rows: list[Any]) -> None:
        self.rows = rows

    async def first(self) -> Any:
        return self.rows[0] if self.rows else None

    async def all(self) -> list[Any]:
        return self.rows


@pytest.mark.asyncio
async def test_a_recollection_replaces_only_the_provider_s_own_fields(monkeypatch: pytest.MonkeyPatch) -> None:
    row = _Mention(
        {
            "rank_group": 7, "breadcrumb": "old > crumb", "timestamp": "2026-09-01",  # pre-sub-key copies
            "serp_result": {"rank_group": 7, "is_featured_snippet": True},          # a field no longer sent
            "link_check": {"version": 3, "dead_count": 1},
            "broken_links": [{"dead_url": "https://x"}],
        }
    )

    class _Opp:
        id = "opp-1"

        async def update(self, **_kw: Any) -> Any:
            return self

    monkeypatch.setattr(m.SerpOpportunity, "filter", staticmethod(lambda **_kw: _Q([_Opp()])))

    async def get_or_create(**_kw: Any) -> tuple[_Mention, bool]:
        return row, False

    monkeypatch.setattr(m.SerpMention, "get_or_create", staticmethod(get_or_create))
    monkeypatch.setattr(m.SerpMention, "filter", staticmethod(lambda **_kw: _Q([row])))
    now = datetime.now(UTC)
    mention = SimpleNamespace(variant="v", seed_keyword="s", title="t", snippet="sn", rank=2, result_type="organic",
                              query="q", url="https://a.example/p", extras={"rank_group": 2, "breadcrumb": "a > p"})
    domain = SimpleNamespace(normalized_domain="a.example", display_domain="a.example", mentions=[mention])
    observation = SimpleNamespace(site_id="site-1", observed_at=now, domains=[domain])
    run = SimpleNamespace(id="run-1", request=SimpleNamespace(site_id="site-1", organization_id="o", created_by="u"))
    await repo.OrmSeoRepository._persist_serp_prospects(SimpleNamespace(), run, [observation])  # type: ignore[arg-type]
    assert row.extras == {
        "serp_result": {"rank_group": 2, "breadcrumb": "a > p"},  # replaced whole: the stale field is gone
        "link_check": {"version": 3, "dead_count": 1},              # other writers' keys survive
        "broken_links": [{"dead_url": "https://x"}],
    }
