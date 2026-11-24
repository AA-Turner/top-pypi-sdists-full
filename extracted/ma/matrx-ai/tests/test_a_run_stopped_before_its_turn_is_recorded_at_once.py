"""A run a Stop ended while preparing is recorded at once, never queued behind the request lane (P1-CHAT 1116d).

Live 2026-11-16: a Stop 0.2-0.6 s after Send ended the run before its turn row and nothing recorded it, so the take-back
door answered "no run found". ``record_stopped_before_run`` writes a ``cancelled`` request row marked
``stopped_before_run``. Inside a request lane an ordinary request row is QUEUED and lands only when the lane drains (after
the stream ends) — too late for the door, which is asked at the cancel. This row is written directly.
"""

from __future__ import annotations

import contextlib
from typing import Any

import pytest

from matrx_ai.db import conversation_gate as gate

RID = "a81b3898-e4e8-4272-b021-56e41aaab9c7"


@pytest.fixture
def world(monkeypatch: pytest.MonkeyPatch) -> dict[str, Any]:
    import matrx_orm

    state: dict[str, Any] = {"created": [], "queued": []}

    class UserRequests:
        model = object()

        async def filter_user_requests(self, **_kw: Any) -> list[Any]:
            return []

        async def create_user_request(self, **kw: Any) -> None:
            state["created"].append(kw)

    class Cxm:
        user_request = UserRequests()

    class Session:
        async def __aenter__(self) -> Session:
            return self

        async def __aexit__(self, *_a: Any) -> None:
            return None

    async def lineage(*_a: Any, **_k: Any) -> None:
        return None

    monkeypatch.setattr(gate, "_cxm", lambda: Cxm())
    monkeypatch.setattr(gate, "_get_active_lane_coordinator", lambda: object())  # a request lane IS open
    monkeypatch.setattr(gate, "_queue_user_request_create", lambda **kw: state["queued"].append(kw))
    monkeypatch.setattr(gate, "_stamp_lineage", lineage)
    monkeypatch.setattr(gate, "_refuse_person_request_in_platform_tenant", lambda *_a, **_k: None)
    monkeypatch.setattr(matrx_orm, "Session", Session)
    monkeypatch.setattr(matrx_orm, "allow_direct_coordinator_write", lambda *_a, **_k: contextlib.nullcontext())
    return state


async def test_the_stopped_run_is_written_now_cancelled_and_marked(world: dict[str, Any]) -> None:
    assert await gate.record_stopped_before_run(RID, where="the run's bindings", conversation_id="c-1") is True
    assert world["queued"] == [], "never queued behind the lane (it drains after the stream ends)"
    [row] = world["created"]
    assert row["id"] == RID and row["status"] == "cancelled" and row["completed_at"] is not None
    assert row["metadata"][gate.STOPPED_BEFORE_RUN_KEY] == {"where": "the run's bindings", "conversation_id": "c-1"}


async def test_an_ordinary_request_row_in_a_lane_is_still_queued(world: dict[str, Any]) -> None:
    assert await gate._create_user_request(request_id=RID, user_id=None) is True
    assert world["created"] == [] and len(world["queued"]) == 1
    assert gate.STOPPED_BEFORE_RUN_KEY not in world["queued"][0]["metadata"]
