"""Guest minting is bounded and race-safe (2026-09-29 verifier findings).

DEFECT 1 — any X-Fingerprint-Id minted a new anonymous auth user (+ its signup
organization) with no format check and no per-client limit.
DEFECT 2 — concurrent first requests for one fingerprint minted two users and,
on the "row exists, auth_user_id null" branch, returned BOTH (a returning
visitor's data split across two identities).

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
    """users.guest_executions: unique fingerprint, conditional updates, counts."""

    def __init__(self) -> None:
        self.rows: dict[str, SimpleNamespace] = {}
        self._ids = itertools.count(1)
        self.minted_rows_from_ip: dict[str | None, int] = {}

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

    async def count(self, **filters: Any) -> int:
        self.last_count_filters = filters
        return self.minted_rows_from_ip.get(filters.get("ip_address"), 0)


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
def ceiling(monkeypatch: pytest.MonkeyPatch) -> dict[str, int]:
    limits = {"ceiling": 30, "window": 60}

    async def reader() -> tuple[int, int]:
        return limits["ceiling"], limits["window"]

    monkeypatch.setitem(_ext._registry, "guest_mint_limit_reader", reader)
    return limits


@pytest.fixture
def recorded(monkeypatch: pytest.MonkeyPatch) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []

    async def record_error(exc: BaseException, **kw: Any) -> None:
        rows.append(kw)

    monkeypatch.setitem(_ext._registry, "record_error", record_error)
    return rows


# ── DEFECT 1a: format ────────────────────────────────────────────────────────


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "fingerprint",
    [
        pytest.param("", id="empty"),
        pytest.param("short123", id="too_short"),
        pytest.param("a" * 201, id="too_long"),
        pytest.param("x' OR 1=1 --padding-xx", id="sql_shape"),
        pytest.param("ab cd ef gh ij kl mn op", id="spaces"),
        pytest.param("../../../../etc/passwd00", id="path"),
    ],
)
async def test_malformed_fingerprint_is_refused_before_lookup_or_mint(
    table: _Table, gotrue: _GoTrue, ceiling: dict[str, int], fingerprint: str
) -> None:
    with pytest.raises(guest_registry.GuestFingerprintMalformedError):
        await guest_registry.resolve_guest_uuid(fingerprint, ip_address="203.0.113.9")
    assert gotrue.minted == []
    assert table.rows == {}


@pytest.mark.parametrize(
    "fingerprint",
    [
        pytest.param("3f9a1c0b7d2e4f6a8b0c1d2e3f4a5b6c", id="web_randomuuid_hex"),
        pytest.param("a" * 64, id="extension_sha256_hex"),
        pytest.param("VisitorId0123456789AbCdEf", id="acquisition_visitor_cookie"),
        pytest.param("temp_1727640000_abcdef", id="legacy_web_temp_id"),
    ],
)
def test_every_real_client_fingerprint_shape_is_admitted(fingerprint: str) -> None:
    assert guest_registry.looks_like_guest_fingerprint(fingerprint)


# ── DEFECT 1b: per-IP ceiling on NEW identities ──────────────────────────────


@pytest.mark.asyncio
async def test_new_identity_past_the_ip_ceiling_is_refused_before_gotrue(
    table: _Table, gotrue: _GoTrue, ceiling: dict[str, int]
) -> None:
    ceiling["ceiling"] = 20
    table.minted_rows_from_ip["203.0.113.9"] = 20

    with pytest.raises(guest_registry.GuestMintRateLimitedError) as exc_info:
        await guest_registry.resolve_guest_uuid(FP, ip_address="203.0.113.9")

    assert not isinstance(exc_info.value, guest_registry.GuestIdentityUnavailableError)
    assert exc_info.value.retry_after_seconds == 60 * 60
    assert gotrue.minted == []
    assert table.rows == {}
    # Only rows that hold an identity, from THIS address, inside the window.
    assert table.last_count_filters["ip_address"] == "203.0.113.9"
    assert table.last_count_filters["auth_user_id__isnull"] is False
    assert "created_at__gte" in table.last_count_filters


@pytest.mark.asyncio
async def test_backfill_mint_is_also_ceiling_checked(
    table: _Table, gotrue: _GoTrue, ceiling: dict[str, int]
) -> None:
    table.add(fingerprint=FP)  # acquisition first-touch row, no identity yet
    table.minted_rows_from_ip["203.0.113.9"] = 30

    with pytest.raises(guest_registry.GuestMintRateLimitedError):
        await guest_registry.resolve_guest_uuid(FP, ip_address="203.0.113.9")
    assert gotrue.minted == []


@pytest.mark.asyncio
async def test_returning_guest_is_never_affected_by_the_ceiling(
    table: _Table, gotrue: _GoTrue, ceiling: dict[str, int]
) -> None:
    table.add(fingerprint=FP, auth_user_id="1f8d19c8-fdb8-49f1-b658-3cdab32d0c6e")
    table.minted_rows_from_ip["203.0.113.9"] = 10_000

    resolved = await guest_registry.resolve_guest_uuid(FP, ip_address="203.0.113.9")

    assert resolved == "1f8d19c8-fdb8-49f1-b658-3cdab32d0c6e"
    assert gotrue.minted == []


@pytest.mark.asyncio
async def test_under_the_ceiling_mints_normally(
    table: _Table, gotrue: _GoTrue, ceiling: dict[str, int]
) -> None:
    table.minted_rows_from_ip["203.0.113.9"] = 29
    resolved = await guest_registry.resolve_guest_uuid(FP, ip_address="203.0.113.9")
    assert resolved == gotrue.minted[0]


@pytest.mark.asyncio
async def test_unbound_limit_reader_refuses_to_mint_never_unlimited(
    table: _Table, gotrue: _GoTrue, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.delitem(_ext._registry, "guest_mint_limit_reader", raising=False)

    with pytest.raises(guest_registry.GuestIdentityUnavailableError) as exc_info:
        await guest_registry.resolve_guest_uuid(FP, ip_address="203.0.113.9")

    assert "guest_mint_limit_reader" in str(exc_info.value.__cause__)
    assert gotrue.minted == []


# ── DEFECT 2: exactly one identity per fingerprint ───────────────────────────


@pytest.mark.asyncio
async def test_concurrent_backfill_returns_one_identity_and_records_the_loser(
    table: _Table, gotrue: _GoTrue, ceiling: dict[str, int], recorded: list[dict[str, Any]]
) -> None:
    row = table.add(fingerprint=FP)  # one of the 168,888 identity-less rows

    a, b = await asyncio.gather(
        guest_registry.resolve_guest_uuid(FP, ip_address="203.0.113.9"),
        guest_registry.resolve_guest_uuid(FP, ip_address="203.0.113.9"),
    )

    assert len(gotrue.minted) == 2  # both raced into GoTrue
    assert a == b == row.auth_user_id  # …but only the winner is ever served
    loser = next(u for u in gotrue.minted if u != a)
    assert [r["kind"] for r in recorded] == ["guest_identity_race_loser"]
    assert recorded[0]["payload"]["orphan_auth_user_id"] == loser
    assert recorded[0]["payload"]["winner_auth_user_id"] == a


@pytest.mark.asyncio
async def test_concurrent_first_visits_return_one_identity_and_record_the_loser(
    table: _Table, gotrue: _GoTrue, ceiling: dict[str, int], recorded: list[dict[str, Any]]
) -> None:
    a, b = await asyncio.gather(
        guest_registry.resolve_guest_uuid(FP, ip_address="203.0.113.9"),
        guest_registry.resolve_guest_uuid(FP, ip_address="203.0.113.9"),
    )

    (row,) = table.rows.values()
    assert a == b == row.auth_user_id
    assert len(gotrue.minted) == 2
    assert [r["kind"] for r in recorded] == ["guest_identity_race_loser"]
    assert recorded[0]["payload"]["orphan_auth_user_id"] != a


@pytest.mark.asyncio
async def test_first_visit_racing_an_identity_less_row_claims_it(
    table: _Table, gotrue: _GoTrue, ceiling: dict[str, int], monkeypatch: pytest.MonkeyPatch
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

    resolved = await guest_registry.resolve_guest_uuid(FP, ip_address="203.0.113.9")

    (row,) = table.rows.values()
    assert resolved == gotrue.minted[0] == row.auth_user_id
