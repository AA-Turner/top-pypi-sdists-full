"""The ``auth.guest_identity`` per-client-IP ceiling bounds guest minting (2026-10-03).

Live finding (feedback feafe3ce): the knobs ``new_identities_per_ip`` = 30 and
``new_identities_window_minutes`` = 60 existed, but ``resolve_guest_uuid`` minted
an anonymous auth user for every new fingerprint without reading them.

The table double below EVALUATES the seed filters against its rows (ip,
identity present, mint stamp present, created_at window) the way Postgres would,
so window expiry and the exclusion of pre-stamp Cloudflare-edge rows are real
behaviour, not a canned number. GoTrue is the only other double.

Since 2026-10-03 (USAGE-GATE.md rule 1) the mint path reads NO table: the count
is an in-process per-IP log seeded in the background. A test that plants rows
in the table therefore lets the seed land (``_seeded``) before it asserts.
"""

from __future__ import annotations

import asyncio
import itertools
import time
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai import _ext
from matrx_ai.db import _guest_registry_impl as guest_registry

IP = "203.0.113.7"
UA = "Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/141.0 Safari/537.36"


class _Table:
    def __init__(self) -> None:
        self.rows: dict[str, SimpleNamespace] = {}
        self._ids = itertools.count(1)
        self.count_calls: list[dict[str, Any]] = []

    def add(self, **cols: Any) -> SimpleNamespace:
        row = SimpleNamespace(
            **{
                "id": f"row-{next(self._ids)}",
                "fingerprint": f"seeded-{len(self.rows)}",
                "auth_user_id": None,
                "ip_address": None,
                "metadata": {},
                "is_blocked": False,
                "blocked_until": None,
                "created_at": datetime.now(UTC),
                **cols,
            }
        )
        self.rows[row.id] = row
        return row

    async def filter_all_guest_executions(self, **kw: Any) -> list[SimpleNamespace]:
        await asyncio.sleep(0)
        if "created_at__gte" in kw:  # the background seed's query
            self.count_calls.append(kw)
            assert set(kw) == {
                "ip_address",
                "auth_user_id__isnull",
                "metadata__json_has_key",
                "created_at__gte",
                "created_at__lt",
            }, kw
            return [
                r
                for r in self.rows.values()
                if r.ip_address == kw["ip_address"]
                and (r.auth_user_id is not None) is (kw["auth_user_id__isnull"] is False)
                and kw["metadata__json_has_key"] in (r.metadata or {})
                and r.created_at >= kw["created_at__gte"]
                and r.created_at < kw["created_at__lt"]
            ]
        return [r for r in self.rows.values() if all(getattr(r, k) == v for k, v in kw.items())]

    async def create_guest_executions(self, **data: Any) -> SimpleNamespace:
        if any(r.fingerprint == data["fingerprint"] for r in self.rows.values()):
            raise RuntimeError("duplicate key value violates unique constraint")
        return self.add(**data)

    async def update_where(self, filters: dict[str, Any], **updates: Any) -> SimpleNamespace:
        row = self.rows.get(filters["id"])
        if row is None or (filters.get("auth_user_id__isnull") and row.auth_user_id is not None):
            return SimpleNamespace(rows_affected=0)
        for k, v in updates.items():
            setattr(row, k, v)
        return SimpleNamespace(rows_affected=1)


class _GoTrue:
    def __init__(self) -> None:
        self.minted: list[str] = []

    async def __call__(self) -> str:
        uid = f"anon-{len(self.minted) + 1:04d}-0000-4000-8000-000000000000"
        self.minted.append(uid)
        return uid


@pytest.fixture
def table(monkeypatch: pytest.MonkeyPatch) -> _Table:
    t = _Table()
    monkeypatch.setattr(guest_registry, "_gm", t)
    guest_registry.reset_mint_ceiling_state()
    yield t
    guest_registry.reset_mint_ceiling_state()


async def _seeded(ip: str = IP, window: int = 60) -> None:
    """Let the background seed land, as it would between two real requests."""
    started = time.time()
    guest_registry._seeded_at[ip] = started
    await guest_registry._seed_mint_log(ip, window, started)


@pytest.fixture
def gotrue(monkeypatch: pytest.MonkeyPatch) -> _GoTrue:
    g = _GoTrue()
    monkeypatch.setattr(guest_registry, "_create_anon_auth_user", g)
    return g


@pytest.fixture
def knobs(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    """The host reader: knob values for countable addresses, None otherwise."""
    state: dict[str, Any] = {"ceiling": 3, "window": 60, "uncountable": set()}

    async def reader(ip_address: str | None) -> tuple[int, int] | None:
        if ip_address is None or ip_address in state["uncountable"]:
            return None
        return state["ceiling"], state["window"]

    monkeypatch.setitem(_ext._registry, "guest_mint_limit_reader", reader)
    return state


def _minted_row(table: _Table, *, ip: str, minutes_ago: float, stamped: bool = True) -> None:
    table.add(
        auth_user_id=f"prior-{len(table.rows)}",
        ip_address=ip,
        created_at=datetime.now(UTC) - timedelta(minutes=minutes_ago),
        metadata={"minted_at": "x", "traffic_kind": "bot"} if stamped else {},
    )


async def _resolve(fp: str, ip: str | None = IP) -> str:
    return await guest_registry.resolve_guest_uuid(fp, ip_address=ip, user_agent=UA, minted_route="POST /x")


@pytest.mark.asyncio
async def test_ceiling_reached_mints_nothing(table: _Table, gotrue: _GoTrue, knobs: dict[str, Any]) -> None:
    for i in range(3):
        await _resolve(f"fp-new-{i}")
    assert len(gotrue.minted) == 3

    with pytest.raises(guest_registry.GuestMintRateLimitedError) as info:
        await _resolve("fp-new-3")
    assert len(gotrue.minted) == 3, "GoTrue must not be called at the ceiling"
    assert info.value.ceiling == 3 and info.value.window_minutes == 60
    assert info.value.retry_after_seconds == 3600
    assert not await table.filter_all_guest_executions(fingerprint="fp-new-3")


@pytest.mark.asyncio
async def test_rate_limit_is_not_reported_as_an_outage(
    table: _Table, gotrue: _GoTrue, knobs: dict[str, Any]
) -> None:
    knobs["ceiling"] = 1
    _minted_row(table, ip=IP, minutes_ago=1)
    await _seeded()
    with pytest.raises(guest_registry.GuestMintRateLimitedError):
        await _resolve("fp-a")
    assert not issubclass(
        guest_registry.GuestMintRateLimitedError, guest_registry.GuestIdentityUnavailableError
    )


@pytest.mark.asyncio
async def test_window_expiry_mints_again(table: _Table, gotrue: _GoTrue, knobs: dict[str, Any]) -> None:
    for _ in range(3):
        _minted_row(table, ip=IP, minutes_ago=61)
    await _seeded()
    assert await _resolve("fp-after-window")
    assert len(gotrue.minted) == 1


@pytest.mark.asyncio
async def test_knob_change_is_respected(table: _Table, gotrue: _GoTrue, knobs: dict[str, Any]) -> None:
    for _ in range(3):
        _minted_row(table, ip=IP, minutes_ago=5)
    await _seeded()
    with pytest.raises(guest_registry.GuestMintRateLimitedError):
        await _resolve("fp-1")
    knobs["ceiling"] = 4
    await _resolve("fp-1")
    assert len(gotrue.minted) == 1
    knobs["window"] = 3  # the 3 old rows fall out of a 3-minute window
    knobs["ceiling"] = 1
    with pytest.raises(guest_registry.GuestMintRateLimitedError):
        await _resolve("fp-2")  # the fresh fp-1 mint still counts
    knobs["ceiling"] = 2
    await _resolve("fp-2")


@pytest.mark.asyncio
async def test_pre_stamp_cloudflare_edge_rows_are_not_counted(
    table: _Table, gotrue: _GoTrue, knobs: dict[str, Any]
) -> None:
    # Historic rows: thousands of strangers recorded under one Cloudflare edge,
    # minted before the stamp existed. They must not fill a real client's bucket,
    # and a request that still arrives with an edge address is not counted.
    edge = "172.70.1.1"
    for _ in range(50):
        _minted_row(table, ip=edge, minutes_ago=2, stamped=False)
        _minted_row(table, ip=IP, minutes_ago=2, stamped=False)
    knobs["uncountable"].add(edge)

    await _seeded()
    await _resolve("fp-real-ip", ip=IP)
    await _resolve("fp-edge-ip", ip=edge)
    assert len(gotrue.minted) == 2
    assert table.count_calls and all(c["ip_address"] == IP for c in table.count_calls)


@pytest.mark.asyncio
async def test_bots_count_toward_the_ceiling(table: _Table, gotrue: _GoTrue, knobs: dict[str, Any]) -> None:
    knobs["ceiling"] = 2
    for i in range(2):
        await guest_registry.resolve_guest_uuid(
            f"bot-{i}", ip_address=IP, user_agent="HeadlessChrome/141", minted_route="POST /x"
        )
    with pytest.raises(guest_registry.GuestMintRateLimitedError):
        await guest_registry.resolve_guest_uuid(
            "browser-1", ip_address=IP, user_agent=UA, minted_route="POST /x"
        )
    stamps = [r.metadata for r in table.rows.values()]
    assert all(s["traffic_kind"] == "bot" and s["minted_ip"] == IP for s in stamps)


@pytest.mark.asyncio
async def test_returning_guest_never_reaches_the_ceiling(
    table: _Table, gotrue: _GoTrue, knobs: dict[str, Any]
) -> None:
    knobs["ceiling"] = 1
    _minted_row(table, ip=IP, minutes_ago=1)
    table.add(fingerprint="returning", auth_user_id="known-user", ip_address=IP)
    assert await _resolve("returning") == "known-user"
    assert table.count_calls == []


@pytest.mark.asyncio
async def test_backfill_branch_is_ceiling_checked(
    table: _Table, gotrue: _GoTrue, knobs: dict[str, Any]
) -> None:
    knobs["ceiling"] = 1
    _minted_row(table, ip=IP, minutes_ago=1)
    table.add(fingerprint="first-touch", ip_address=IP)  # acquisition row, no identity
    await _seeded()
    with pytest.raises(guest_registry.GuestMintRateLimitedError):
        await _resolve("first-touch")
    assert gotrue.minted == []


@pytest.mark.asyncio
async def test_unbound_reader_refuses_to_mint(table: _Table, gotrue: _GoTrue, monkeypatch) -> None:
    monkeypatch.delitem(_ext._registry, "guest_mint_limit_reader", raising=False)
    with pytest.raises(guest_registry.GuestIdentityUnavailableError):
        await _resolve("fp-x")
    assert gotrue.minted == []


@pytest.mark.asyncio
async def test_the_mint_path_reads_no_table_and_seeds_in_the_background(
    table: _Table, gotrue: _GoTrue, knobs: dict[str, Any], monkeypatch: pytest.MonkeyPatch
) -> None:
    """Break named: a per-request count on the mint path (USAGE-GATE.md rule 1).

    An IP this process has never seen mints on what it knows (nothing), while the
    seed runs detached; once the seed has landed, the table's mints count.
    """
    knobs["ceiling"] = 1
    _minted_row(table, ip=IP, minutes_ago=1)
    gate = asyncio.Event()
    real_seed = guest_registry._seed_mint_log

    async def _slow_seed(*a: Any, **k: Any) -> None:
        await gate.wait()
        await real_seed(*a, **k)

    monkeypatch.setattr(guest_registry, "_seed_mint_log", _slow_seed)
    assert await _resolve("fp-unseen-ip")  # not refused, not waiting on the seed
    assert table.count_calls == [], "the mint path waited on a table read"
    gate.set()
    for _ in range(20):
        await asyncio.sleep(0)
        if table.count_calls and not guest_registry._seed_tasks:
            break
    assert table.count_calls, "no background seed was scheduled"
    with pytest.raises(guest_registry.GuestMintRateLimitedError):
        await _resolve("fp-next")
