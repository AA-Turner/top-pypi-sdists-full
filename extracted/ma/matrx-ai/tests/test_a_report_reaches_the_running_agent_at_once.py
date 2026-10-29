"""A helper's report reaches its running parent at the next boundary, not at the end of the run.

Arman, 2026-10-28: "Subagent results need to go to the agent immediately as they finish."
Conversation 12313527 (2026-10-26): eight helpers finished while the parent was idle and wakes
were held; when the person wrote "Great. It looks like they're done.", the parent answered
"none of the 8 results have actually been shown to me yet" and messaged finished helpers for
answers that were already waiting — reports were taken only at a run's FINAL boundary.
"""

from __future__ import annotations

from types import SimpleNamespace

from matrx_ai.db._cx_managers_impl import LIVE_REPORT_SOURCES, CxPendingInjectionManager


def _row(rid: str, *, source: str, kind: str = "system_message", seq: int = 1, by: str | None = None):
    return SimpleNamespace(
        id=rid,
        source=source,
        kind=kind,
        status="pending",
        enqueued_seq=seq,
        metadata={"enqueued_by_request_id": by},
    )


def _fake(rows):
    async def filter_items(**kwargs):
        return [r for r in rows if r.status == kwargs.get("status")]

    async def update_where(where, **fields):
        hit = [r for r in rows if r.id == where["id"] and r.status == where["status"]]
        for r in hit:
            r.status = fields["status"]
        return SimpleNamespace(updated_rows=hit)

    return SimpleNamespace(filter_items=filter_items, update_where=update_where)


async def test_every_waiting_report_is_taken_at_any_boundary():
    rows = [
        _row("report-a", source="deferred_tool", seq=1),
        _row("person-1", source="user", kind="user_message", seq=2),
        _row("report-b", source="deferred_tool", seq=3),
        _row("wake-1", source="scheduled_wake", seq=4),
        _row("hold-note", source="wake_guard", seq=5),
        _row("collab", source="agent_collab", seq=6),
    ]
    claimed = await CxPendingInjectionManager.claim_reports_now(_fake(rows), "c", request_id="r")
    assert [r.id for r in claimed] == ["report-a", "report-b", "wake-1"]
    # The person's queued message keeps its one-per-turn queue; a hold note and a write-back wait.
    assert {r.id for r in rows if r.status == "pending"} == {"person-1", "hold-note", "collab"}


async def test_a_run_never_takes_a_row_it_enqueued_itself():
    rows = [_row("own", source="agent_message", by="r"), _row("theirs", source="agent_message", by="x")]
    claimed = await CxPendingInjectionManager.claim_reports_now(_fake(rows), "c", request_id="r")
    assert [r.id for r in claimed] == ["theirs"]


def test_the_live_sources_are_the_news_sources():
    assert LIVE_REPORT_SOURCES == {
        "deferred_tool",
        "agent_message",
        "background_run",
        "scheduled_wake",
        "agent_steer_returned",
    }


async def test_the_mid_run_drain_takes_reports(monkeypatch):
    """The per-iteration drain (not only the final boundary) asks for reports."""
    from matrx_ai.config.message_config import MessageList
    from matrx_ai.db import cx_managers as cxm_mod
    from matrx_ai.tools import dynamic_drain

    report = SimpleNamespace(
        id="report-a",
        source="deferred_tool",
        kind="system_message",
        content={"text": "<task-notification>done</task-notification>"},
        enqueued_seq=1,
        is_visible_to_user=True,
    )
    asked: list[str] = []

    async def claim_pending(_cid, *, request_id=None):
        return []

    async def claim_reports_now(cid, *, request_id=None):
        asked.append(cid)
        return [report]

    monkeypatch.setattr(
        cxm_mod.cxm,
        "pending_injection",
        SimpleNamespace(claim_pending=claim_pending, claim_reports_now=claim_reports_now),
    )
    config = SimpleNamespace(messages=MessageList())
    ctx = SimpleNamespace(conversation_id="c", request_id="r", emitter=None, metadata={}, store=True)
    monkeypatch.setattr(
        "matrx_ai.agents.conversation_type.is_internal_conversation", lambda _ctx: False
    )
    await dynamic_drain.drain_pending_injections(config, ctx)
    assert asked == ["c"]
    assert config.messages[-1].metadata.get("injection_source") == "deferred_tool"
