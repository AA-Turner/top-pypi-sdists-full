"""A recovered capability fact is one row per (class, model, UTC day) across every process.

The per-process guard on anthropic.streaming_required (addc8bcd8dd) still let the same fact land every
10-20 minutes on 2026-11-13 (claude-haiku-5-5, max_tokens 128000): short-lived workers each start with an
empty set. ``once_per_day`` asks the database, so a new process cannot repeat what one already filed today.
"""

from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_ai.ops import issue_capture, issue_registry


def _wire(monkeypatch: pytest.MonkeyPatch, rows: list[dict[str, Any]]) -> list[Any]:
    detached: list[Any] = []

    class _OpsIssueEvent:
        @classmethod
        async def create(cls, **payload: Any) -> None:
            rows.append(payload)

        @classmethod
        async def exists(cls, **filters: Any) -> bool:
            return bool(await cls.get_many(**filters))

        @classmethod
        async def get_many(cls, **filters: Any) -> list[Any]:
            since = filters["occurred_at__gte"]
            return [
                SimpleNamespace(**r)
                for r in rows
                if r["issue_class_id"] == filters["issue_class_id"]
                and r["model"] == filters["model"]
                and r["occurred_at"] >= since
            ]

    async def _get_issue_class(_key: str) -> dict[str, Any]:
        return {"id": "issue-class-id", "is_active": True}

    def _track_detached(coro: Any, *, name: str) -> None:
        detached.append(coro)

    monkeypatch.setattr(issue_capture, "get_model", lambda _name: _OpsIssueEvent)
    monkeypatch.setattr(issue_registry, "get_issue_class", _get_issue_class)
    monkeypatch.setattr("matrx_utils.detached_task", _track_detached)
    return detached


async def _capture(detached: list[Any], model: str, *, once_per_day: bool) -> None:
    await issue_capture.capture_issue(
        "anthropic.streaming_required",
        error_type="streaming_required",
        provider="anthropic",
        model=model,
        organization_id="organization-id",
        was_recovered=True,
        once_per_day=once_per_day,
    )
    await detached.pop()


@pytest.mark.asyncio
async def test_once_per_day_files_one_row_per_model(monkeypatch: pytest.MonkeyPatch) -> None:
    rows: list[dict[str, Any]] = []
    detached = _wire(monkeypatch, rows)

    for _ in range(5):
        await _capture(detached, "claude-haiku-5-5", once_per_day=True)
    await _capture(detached, "claude-sonnet-5-5", once_per_day=True)

    assert [r["model"] for r in rows] == ["claude-haiku-5-5", "claude-sonnet-5-5"]


@pytest.mark.asyncio
async def test_without_the_flag_every_event_is_recorded(monkeypatch: pytest.MonkeyPatch) -> None:
    rows: list[dict[str, Any]] = []
    detached = _wire(monkeypatch, rows)

    for _ in range(3):
        await _capture(detached, "claude-haiku-5-5", once_per_day=False)

    assert len(rows) == 3


async def _capture_keyed(detached: list[Any], agent: str, schema: str) -> None:
    await issue_capture.capture_issue(
        "structured_output.enforcement_dropped",
        error_type="enforcement_dropped",
        provider="anthropic",
        model="claude-opus-5-5",
        organization_id="organization-id",
        was_recovered=True,
        detail={"agent_name": agent},
        once_per_day=True,
        day_key=(agent, schema),
    )
    await detached.pop()


@pytest.mark.asyncio
async def test_day_key_files_one_row_per_agent_and_schema(monkeypatch: pytest.MonkeyPatch) -> None:
    rows: list[dict[str, Any]] = []
    detached = _wire(monkeypatch, rows)

    for _ in range(4):
        await _capture_keyed(detached, "Agent A", "SchemaX")
    await _capture_keyed(detached, "Agent B", "SchemaX")
    await _capture_keyed(detached, "Agent A", "SchemaY")

    assert [r["detail"]["day_key"] for r in rows] == [
        ["Agent A", "SchemaX"],
        ["Agent B", "SchemaX"],
        ["Agent A", "SchemaY"],
    ]


@pytest.mark.asyncio
async def test_recovered_structured_output_finding_asks_for_a_day_key(monkeypatch: pytest.MonkeyPatch) -> None:
    from matrx_ai.providers import structured_output_findings as sof

    calls: list[dict[str, Any]] = []

    async def _fake_capture(key: str, **kw: Any) -> None:
        calls.append({"key": key, **kw})

    monkeypatch.setattr(issue_capture, "capture_issue", _fake_capture)
    sof.forget_recorded_facts()
    detail = {"agent_name": "Agent A", "schema_name": "SchemaX", "action": "x"}
    await sof.record_structured_output_finding(
        sof.ENFORCEMENT_DROPPED, provider="anthropic", model="m", detail=detail
    )
    await sof.record_structured_output_finding(
        sof.ANSWER_OFF_CONTRACT, provider="anthropic", model="m", detail=detail, was_recovered=False
    )
    sof.forget_recorded_facts()

    assert calls[0]["once_per_day"] is True
    assert calls[0]["day_key"][0] == "Agent A"
    assert calls[1]["once_per_day"] is False and calls[1]["day_key"] is None
