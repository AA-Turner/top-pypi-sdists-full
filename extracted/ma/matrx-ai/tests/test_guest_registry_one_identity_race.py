"""One guest identity per fingerprint, even under concurrent first requests
(2026-09-29 verifier finding).

Concurrent first requests for one fingerprint minted two anonymous users and,
on the "row exists, auth_user_id null" branch, returned BOTH — a returning
visitor's data split across two identities.

GoTrue (``_create_anon_auth_user``) is the only external dependency doubled
here; the registry double below behaves like the table: a unique fingerprint,
and ``update_where`` honouring ``auth_user_id__isnull`` atomically.
"""

from __future__ import annotations

import asyncio
import itertools
from datetime import UTC, datetime
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai import _ext
from matrx_ai.db import _guest_registry_impl as guest_registry

FP = "3f9a1c0b7d2e4f6a8b0c1d2e3f4a5b6c"  # crypto.randomUUID hex — what the web client sends


class _Table:
    """users.guest_executions: unique fingerprint, conditional updates."""

    def __init__(self) -> None:
        self.rows: dict[str, SimpleNamespace] = {}
        self._ids = itertools.count(1)

    def add(self, **cols: Any) -> SimpleNamespace:
        row = SimpleNamespace(
            **{
                "id": f"row-{next(self._ids)}",
                "auth_user_id": None,
                "is_blocked": False,
                "blocked_until": None,
                "total_executions": 0,
                "first_execution_at": None,
                "created_at": datetime.now(UTC),
                **cols,
            }
        )
        self.rows[row.id] = row
        return row

    async def filter_all_guest_executions(self, **kw: Any) -> list[SimpleNamespace]:
        await asyncio.sleep(0)
        return [r for r in self.rows.values() if all(getattr(r, k) == v for k, v in kw.items())]

    async def create_guest_executions(self, **data: Any) -> SimpleNamespace:
        await asyncio.sleep(0)
        if any(r.fingerprint == data["fingerprint"] for r in self.rows.values()):
            raise RuntimeError("duplicate key value violates unique constraint guest_executions_fingerprint_key")
        return self.add(**data)

    async def update_guest_executions(self, row_id: str, **updates: Any) -> None:
        for k, v in updates.items():
            setattr(self.rows[row_id], k, v)

    async def update_where(self, filters: dict[str, Any], **updates: Any) -> SimpleNamespace:
        # One statement: the check and the write cannot interleave.
        row = self.rows.get(filters["id"])
        if row is None or (filters.get("auth_user_id__isnull") and row.auth_user_id is not None):
            return SimpleNamespace(rows_affected=0, updated_rows=[])
        for k, v in updates.items():
            setattr(row, k, v)
        return SimpleNamespace(rows_affected=1, updated_rows=[vars(row)])


class _GoTrue:
    """Mints a distinct anonymous user per call, yielding mid-call like the network."""

    def __init__(self) -> None:
        self.minted: list[str] = []

    async def __call__(self) -> str:
        await asyncio.sleep(0)
        uid = f"anon-{len(self.minted) + 1:04d}-0000-4000-8000-000000000000"
        self.minted.append(uid)
        await asyncio.sleep(0)
        return uid


@pytest.fixture
def table(monkeypatch: pytest.MonkeyPatch) -> _Table:
    t = _Table()
    monkeypatch.setattr(guest_registry, "_gm", t)
    return t


@pytest.fixture
def gotrue(monkeypatch: pytest.MonkeyPatch) -> _GoTrue:
    g = _GoTrue()
    monkeypatch.setattr(guest_registry, "_create_anon_auth_user", g)
    return g


@pytest.fixture
def recorded(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    async def record_error(exc: BaseException, **kw: Any) -> None:
        rows.append(kw)

    monkeypatch.setitem(_ext._registry, "record_error", record_error)
    return rows


# ── exactly one identity per fingerprint ─────────────────────────────────────


@pytest.mark.asyncio
async def test_concurrent_backfill_returns_one_identity_and_records_the_loser(
    table: _Table, gotrue: _GoTrue, recorded: list[dict[str, Any]]
) -> None:
    row = table.add(fingerprint=FP)  # one of the 168,888 identity-less rows

    a, b = await asyncio.gather(
        guest_registry.resolve_guest_uuid(FP),
        guest_registry.resolve_guest_uuid(FP),
    )

    assert len(gotrue.minted) == 2  # both raced into GoTrue
    assert a == b == row.auth_user_id  # …but only the winner is ever served
    loser = next(u for u in gotrue.minted if u != a)
    assert [r["kind"] for r in recorded] == ["guest_identity_race_loser"]
    assert recorded[0]["payload"]["orphan_auth_user_id"] == loser
    assert recorded[0]["payload"]["winner_auth_user_id"] == a


@pytest.mark.asyncio
async def test_concurrent_first_visits_return_one_identity_and_record_the_loser(
    table: _Table, gotrue: _GoTrue, recorded: list[dict[str, Any]]
) -> None:
    a, b = await asyncio.gather(
        guest_registry.resolve_guest_uuid(FP),
        guest_registry.resolve_guest_uuid(FP),
    )

    (row,) = table.rows.values()
    assert a == b == row.auth_user_id
    assert len(gotrue.minted) == 2
    assert [r["kind"] for r in recorded] == ["guest_identity_race_loser"]
    assert recorded[0]["payload"]["orphan_auth_user_id"] != a


@pytest.mark.asyncio
async def test_first_visit_racing_an_identity_less_row_claims_it(
    table: _Table, gotrue: _GoTrue, monkeypatch: pytest.MonkeyPatch
) -> None:
    # The acquisition first-touch door inserts the fingerprint row (no identity)
    # while this request is minting: the insert collides, the row must be
    # CLAIMED with our identity — not refused as unavailable, not left empty.
    real_create = table.create_guest_executions

    async def create_after_first_touch(**data: Any) -> SimpleNamespace:
        if not table.rows:
            table.add(fingerprint=data["fingerprint"])
        return await real_create(**data)

    monkeypatch.setattr(table, "create_guest_executions", create_after_first_touch)

    resolved = await guest_registry.resolve_guest_uuid(FP)

    (row,) = table.rows.values()
    assert resolved == gotrue.minted[0] == row.auth_user_id
