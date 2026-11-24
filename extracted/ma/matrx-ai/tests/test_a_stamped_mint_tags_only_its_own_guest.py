"""``on_minted`` runs for an identity THIS call minted, never for one that already existed (CGU-M3 W4, 2026-11-04).

The host uses it to make a guest minted by a test-stamped request a fixture of that run. Both directions:
a fresh mint is handed over (before the request goes on), a returning guest is never touched, and a hook
failure never fails the guest's request.
"""

from __future__ import annotations

from typing import Any

import pytest
import test_guest_registry_mint_ceiling as ceiling_suite
from test_guest_registry_mint_ceiling import _GoTrue, _Table

from matrx_ai.db import _guest_registry_impl as guest_registry

table = pytest.fixture(ceiling_suite.table.__wrapped__)
gotrue = pytest.fixture(ceiling_suite.gotrue.__wrapped__)
knobs = pytest.fixture(ceiling_suite.knobs.__wrapped__)


async def _resolve(fp: str, **kw: Any) -> str:
    return await guest_registry.resolve_guest_uuid(fp, ip_address="203.0.113.7", user_agent="ua", **kw)


@pytest.mark.asyncio
async def test_a_fresh_mint_is_handed_to_the_hook(table: _Table, gotrue: _GoTrue, knobs: dict[str, Any]) -> None:
    seen: list[str] = []

    async def hook(user_id: str) -> None:
        seen.append(user_id)

    uid = await _resolve("fp-new", on_minted=hook)
    assert seen == [uid]


@pytest.mark.asyncio
async def test_an_existing_guest_is_never_handed_over(table: _Table, gotrue: _GoTrue, knobs: dict[str, Any]) -> None:
    table.add(fingerprint="fp-old", auth_user_id="existing-guest-0001")
    seen: list[str] = []

    async def hook(user_id: str) -> None:
        seen.append(user_id)

    assert await _resolve("fp-old", on_minted=hook) == "existing-guest-0001"
    assert seen == [] and gotrue.minted == []


@pytest.mark.asyncio
async def test_a_backfilled_row_mints_and_is_handed_over(table: _Table, gotrue: _GoTrue, knobs: dict[str, Any]) -> None:
    table.add(fingerprint="fp-first-touch", auth_user_id=None)
    seen: list[str] = []

    async def hook(user_id: str) -> None:
        seen.append(user_id)

    uid = await _resolve("fp-first-touch", on_minted=hook)
    assert seen == [uid] == gotrue.minted


@pytest.mark.asyncio
async def test_a_hook_failure_never_fails_the_request(table: _Table, gotrue: _GoTrue, knobs: dict[str, Any]) -> None:
    async def broken(user_id: str) -> None:
        raise RuntimeError("GoTrue down")

    assert await _resolve("fp-broken", on_minted=broken) == gotrue.minted[-1]
