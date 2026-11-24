"""A scrape retry-queue item is seen, claimed, completed and failed only inside its own organization.

THE FINDING (CASA 3.1.4, 2026-11-10). ``scraper.scrape_retry_queue`` rows carried no owner and no
organization, and ``/queue/pending``, ``/queue/claim``, ``/queue/submit`` and ``/queue/fail`` asked
nothing beyond a signed-in identity: any person could list which pages another organization's scrapes
failed on, claim them, and mark them failed or "completed" without doing the work. The helpers are
matrx-local's desktop app and the extension, running as a signed-in person, and what a helper saves
lands in ITS OWN organization's cache, so a helper of another organization never helped the row's
owner. Now the enqueue stamps the failing scrape's organization (``request_context.organization_id``)
and every queue route acts only on rows of the request's organization.

The fake queue evaluates the real lookups the routes send (``id``, ``status``, ``tier``,
``claim_expires_at__lt``, ``request_context__json_key``); an unknown lookup raises, so a route that
drops its scope cannot pass by accident.
"""

from __future__ import annotations

import asyncio
import sys
from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any

import pytest

pytest.importorskip("fastapi", reason="server extra not installed")

import matrx_scraper.api.ext_router  # noqa: E402, F401

ext_router = sys.modules["matrx_scraper.api.ext_router"]

ORG_A = "aaaaaaaa-aaaa-4aaa-8aaa-aaaaaaaaaaaa"
ORG_B = "bbbbbbbb-bbbb-4bbb-8bbb-bbbbbbbbbbbb"
ITEM = "11111111-1111-4111-8111-111111111111"


def _matches(row: dict[str, Any], filters: dict[str, Any]) -> bool:
    for key, want in filters.items():
        if key == "request_context__json_key":
            name, value = want
            if (row.get("request_context") or {}).get(name) != value:
                return False
        elif key == "claim_expires_at__lt":
            if row.get("claim_expires_at") is None or not row["claim_expires_at"] < want:
                return False
        elif key in {"id", "status", "tier"}:
            if row.get(key) != want:
                return False
        else:  # a lookup this fake does not know is a test defect, never a silent pass
            raise AssertionError(f"unexpected lookup {key!r}")
    return True


class _Query:
    def __init__(self, rows: list[dict[str, Any]], filters: dict[str, Any]):
        self._rows, self._filters = rows, dict(filters)

    def filter(self, **more: Any) -> _Query:
        return _Query(self._rows, {**self._filters, **more})

    def order_by(self, *_: Any) -> _Query:
        return self

    def limit(self, _: int) -> _Query:
        return self

    async def values(self, *cols: str) -> list[dict[str, Any]]:
        return [{c: r.get(c) for c in cols} for r in self._rows if _matches(r, self._filters)]


class _FakeQueue:
    def __init__(self, rows: list[dict[str, Any]]):
        self.rows = rows

    def filter(self, **filters: Any) -> _Query:
        return _Query(self.rows, filters)

    async def count(self, **filters: Any) -> int:
        return sum(1 for r in self.rows if _matches(r, filters))

    async def update_where(self, filters: dict[str, Any], **updates: Any) -> SimpleNamespace:
        hit = [r for r in self.rows if _matches(r, filters)]
        for r in hit:
            r.update({k: v for k, v in updates.items() if k != "attempt_count"})
        return SimpleNamespace(rows_affected=len(hit))


def _row(status: str) -> dict[str, Any]:
    return {
        "id": ITEM,
        "target_url": "https://example.com/private-report",
        "domain_name": "example.com",
        "failure_reason": "blocked",
        "tier": "desktop",
        "status": status,
        "created_at": datetime.now(UTC),
        "claim_expires_at": None,
        "request_context": {"organization_id": ORG_A},
    }


def _ctx(org: str) -> SimpleNamespace:
    return SimpleNamespace(organization_id=org, user_id="22222222-2222-4222-8222-222222222222")


@pytest.fixture
def queue(monkeypatch: pytest.MonkeyPatch):
    def install(status: str) -> _FakeQueue:
        fake = _FakeQueue([_row(status)])
        monkeypatch.setattr(ext_router, "ScrapeRetryQueue", fake)
        return fake

    return install


def test_another_organization_does_not_see_the_item(queue) -> None:
    queue("pending")
    out = asyncio.run(ext_router.queue_pending(tier="desktop", limit=10, domain=None, ctx=_ctx(ORG_B)))
    assert out["items"] == [] and out["total_pending"] == 0


def test_another_organization_cannot_claim_the_item(queue) -> None:
    fake = queue("pending")
    req = ext_router.RetryClaimRequest(item_ids=[ITEM], client_id="stranger-desktop")
    out = asyncio.run(ext_router.queue_claim(req, ctx=_ctx(ORG_B)))
    assert out["claimed"] == [] and fake.rows[0]["status"] == "pending"


def test_another_organization_cannot_complete_the_item(queue) -> None:
    fake = queue("claimed")
    out = asyncio.run(ext_router.queue_submit(ext_router.RetrySubmitRequest(queue_item_id=ITEM), ctx=_ctx(ORG_B)))
    assert out == {"success": False} and fake.rows[0]["status"] == "claimed"


def test_another_organization_cannot_fail_the_item(queue) -> None:
    fake = queue("claimed")
    req = ext_router.RetryFailRequest(queue_item_id=ITEM, error="x", promote_to_extension=False)
    out = asyncio.run(ext_router.queue_fail(req, ctx=_ctx(ORG_B)))
    assert out == {"success": False} and fake.rows[0]["status"] == "claimed"


def test_the_items_own_organization_still_works_it(queue) -> None:
    fake = queue("pending")
    assert asyncio.run(ext_router.queue_pending(tier="desktop", limit=10, domain=None, ctx=_ctx(ORG_A)))["total_pending"] == 1
    req = ext_router.RetryClaimRequest(item_ids=[ITEM], client_id="own-desktop")
    assert asyncio.run(ext_router.queue_claim(req, ctx=_ctx(ORG_A)))["claimed"] == [ITEM]
    out = asyncio.run(ext_router.queue_submit(ext_router.RetrySubmitRequest(queue_item_id=ITEM), ctx=_ctx(ORG_A)))
    assert out == {"success": True} and fake.rows[0]["status"] == "completed"
