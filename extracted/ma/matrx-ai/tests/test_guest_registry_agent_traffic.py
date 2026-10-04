"""The agent-traffic marker labels a guest our own agent minted (2026-10-03).

Break it would catch: the marker is read but the mint stamp still says ``bot``/``browser`` (the
Accounts roster keeps guessing), or the host's expiry tagger is never called (the account is
never swept), or a tagger failure fails the guest's request (a label must never gate).
Table and GoTrue doubles are shared with the mint-ceiling suite.
"""

from __future__ import annotations

from typing import Any

import pytest
import test_guest_registry_mint_ceiling as ceiling_suite
from test_guest_registry_mint_ceiling import _GoTrue, _Table

from matrx_ai.agent_traffic import MATRX_AGENT_TRAFFIC, agent_traffic_headers, agent_traffic_of
from matrx_ai.db import _guest_registry_impl as guest_registry

# The shared doubles, re-bound here so this file's tests name them as fixtures.
table = pytest.fixture(ceiling_suite.table.__wrapped__)
gotrue = pytest.fixture(ceiling_suite.gotrue.__wrapped__)
knobs = pytest.fixture(ceiling_suite.knobs.__wrapped__)

IP = "203.0.113.9"
CHROME = "Mozilla/5.0 (Macintosh) AppleWebKit/537.36 Chrome/141.0 Safari/537.36"


async def _resolve(fp: str, **kw: Any) -> str:
    return await guest_registry.resolve_guest_uuid(
        fp, ip_address=IP, user_agent=CHROME, minted_route="POST /x", **kw
    )


@pytest.mark.asyncio
async def test_marked_mint_is_agent_and_tagged(table: _Table, gotrue: _GoTrue, knobs: dict[str, Any]) -> None:
    tagged: list[tuple[str, str]] = []

    async def tagger(user_id: str, tool: str) -> None:
        tagged.append((user_id, tool))

    uid = await _resolve("fp-agent", agent_traffic="playwright:walk", on_agent_minted=tagger)
    row = (await table.filter_all_guest_executions(fingerprint="fp-agent"))[0]
    # A real Chrome user agent: the heuristic alone would have said "browser".
    assert row.metadata["traffic_kind"] == "agent"
    assert row.metadata["agent_tool"] == "playwright:walk"
    assert row.metadata["ua_family"] == "chrome"
    assert tagged == [(uid, "playwright:walk")]


@pytest.mark.asyncio
async def test_returning_agent_guest_is_not_retagged(
    table: _Table, gotrue: _GoTrue, knobs: dict[str, Any]
) -> None:
    tagged: list[str] = []

    async def tagger(user_id: str, tool: str) -> None:
        tagged.append(user_id)

    first = await _resolve("fp-again", agent_traffic="curl", on_agent_minted=tagger)
    second = await _resolve("fp-again", agent_traffic="curl", on_agent_minted=tagger)
    assert first == second and tagged == [first]


@pytest.mark.asyncio
async def test_unmarked_mint_keeps_the_heuristic(
    table: _Table, gotrue: _GoTrue, knobs: dict[str, Any]
) -> None:
    called: list[str] = []

    async def tagger(user_id: str, tool: str) -> None:
        called.append(user_id)

    await _resolve("fp-person", on_agent_minted=tagger)
    row = (await table.filter_all_guest_executions(fingerprint="fp-person"))[0]
    assert row.metadata["traffic_kind"] == "browser"
    assert "agent_tool" not in row.metadata
    assert called == []


@pytest.mark.asyncio
async def test_tagger_failure_never_fails_the_request(
    table: _Table, gotrue: _GoTrue, knobs: dict[str, Any]
) -> None:
    async def broken(user_id: str, tool: str) -> None:
        raise RuntimeError("GoTrue down")

    uid = await _resolve("fp-broken", agent_traffic="node", on_agent_minted=broken)
    assert uid == gotrue.minted[-1]


def test_marker_reads_header_any_case_then_cookie() -> None:
    assert agent_traffic_of({"x-matrx-agent-traffic": "smoke"}) == "smoke"
    assert agent_traffic_of(agent_traffic_headers("py client")) == "py-client"
    assert agent_traffic_of({}, {MATRX_AGENT_TRAFFIC["cookie"]: "local-preview"}) == "local-preview"
    assert agent_traffic_of({"x-matrx-agent-traffic": "  "}) is None
    assert agent_traffic_of(None) is None


@pytest.mark.asyncio
async def test_race_loser_is_tagged_too(table: _Table, gotrue: _GoTrue, knobs: dict[str, Any]) -> None:
    """An orphan our agent minted is still ours: it must expire, or nothing ever removes it."""
    tagged: list[str] = []

    async def tagger(user_id: str, tool: str) -> None:
        tagged.append(user_id)

    table.add(fingerprint="fp-race", auth_user_id=None)
    real_update = table.update_where

    async def racer_wins(filters: dict[str, Any], **updates: Any) -> Any:
        table.rows[filters["id"]].auth_user_id = "winner-0000"
        return await real_update(filters, **updates)

    table.update_where = racer_wins  # type: ignore[method-assign]
    uid = await _resolve("fp-race", agent_traffic="walk", on_agent_minted=tagger)
    assert uid == "winner-0000"
    assert tagged == [gotrue.minted[-1]]
