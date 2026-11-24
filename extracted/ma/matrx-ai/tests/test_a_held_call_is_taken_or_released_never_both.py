"""THE HELD STREAM'S WAIT (RESUME-AND-RECOVERY section 1a): a turn waiting in its open stream for a
client-run tool either TAKES the result or RELEASES the call, decided by the row, never both and never
neither.

The store here is a small in-memory row with the two real predicates (the claim/renew/release update and
the result POST's two-step compare-and-set), so every interleaving below is driven on purpose. The same
statements against real Postgres are proven by
``aidream/api/live_tests/test_held_stream_race_live.py``.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest

from matrx_ai.tools import delegated_hold as hold


def _hooks(**over) -> hold.HoldHooks:
    base = dict(
        hold_ms=lambda _reason="client_tool": 60_000, poll_ms=lambda: 50, may_hold=lambda: True, lease_ms=lambda: 30_000,
        slow_poll_ms=lambda: 2000, fast_window_ms=lambda: 10_000, max_hold_ms=lambda _reason="client_tool": 55 * 60_000,
    )
    return hold.HoldHooks(**{**base, **over})


class Row:
    """One chat.tool_call row and the only two writers that touch it while it is held."""

    def __init__(self) -> None:
        self.status = "delegated"
        self.resolved_at = None
        self.held_until: datetime | None = None
        self.is_error = False
        self.writes: list[str] = []

    def view(self) -> SimpleNamespace:
        return SimpleNamespace(
            id="row-1", status=self.status, resolved_at=self.resolved_at, held_until=self.held_until,
            is_error=self.is_error,
        )

    async def holder_write(self, row_id: str, *, conversation_id: str, held_until, renew: bool) -> int:
        if self.status != "delegated" or self.resolved_at is not None:
            return 0
        if (renew or held_until is None) and self.held_until is None:
            return 0
        self.held_until = held_until
        self.writes.append("release" if held_until is None else ("renew" if renew else "claim"))
        return 1

    def client_post(self) -> bool:
        """The result POST's compare-and-set. True when the waiting turn was told it continues (held)."""
        assert self.status == "delegated", "a second POST is a duplicate, not a resolution"
        held = self.held_until is not None and self.held_until > datetime.now(UTC)
        self.status, self.resolved_at = "completed", datetime.now(UTC)
        if not held:
            self.held_until = None  # the plain compare-and-set clears the lease
        return held


@pytest.fixture
def row(monkeypatch: pytest.MonkeyPatch) -> Row:
    row = Row()

    async def read(_row_id: str):
        return row.view()

    monkeypatch.setattr(hold, "_read_row", read)
    monkeypatch.setattr(hold, "_write", row.holder_write)
    monkeypatch.setattr(hold, "_hooks", _hooks())
    return row


async def _held(row: Row, **kw) -> asyncio.Task[hold.HoldOutcome]:
    found = hold.settings(cap_seconds=kw.pop("seconds", 30))
    assert found is not None
    assert await hold.claim("row-1", conversation_id="conv", hold=found)
    task = asyncio.create_task(hold.wait_for_result("row-1", conversation_id="conv", call_id="call", hold=found, **kw))
    await asyncio.sleep(0)
    return task


@pytest.mark.asyncio
async def test_a_result_that_lands_while_held_is_taken_by_the_waiting_turn(row: Row) -> None:
    task = await _held(row)
    assert row.client_post() is True, "the POST must be told the open stream continues"
    assert hold.wake("conv", "call") is True
    outcome = await asyncio.wait_for(task, 1)
    assert outcome.taken and outcome.row.status == "completed"
    assert "release" not in row.writes


@pytest.mark.asyncio
async def test_a_lost_wake_costs_one_poll_never_the_result(row: Row) -> None:
    task = await _held(row)
    row.client_post()  # no wake at all: the NOTIFY was dropped
    outcome = await asyncio.wait_for(task, 1)
    assert outcome.taken


@pytest.mark.asyncio
async def test_the_limit_releases_the_call_and_a_later_post_is_told_to_resume(row: Row) -> None:
    task = await _held(row, seconds=0.1)
    outcome = await asyncio.wait_for(task, 1)
    assert not outcome.taken and outcome.reason == "timeout"
    assert row.held_until is None and row.status == "delegated", "the call stays parked, with no lease"
    assert row.client_post() is False, "a result after the release is continued by /resume"


@pytest.mark.asyncio
async def test_a_result_that_beats_the_release_at_the_limit_is_taken_not_lost(row: Row) -> None:
    """The exact late race: the limit passes, the POST commits under the lease, THEN the release runs."""
    real_write = row.holder_write

    async def post_lands_just_before_the_release(row_id, *, conversation_id, held_until, renew):
        if held_until is None:
            assert row.client_post() is True
        return await real_write(row_id, conversation_id=conversation_id, held_until=held_until, renew=renew)

    task = await _held(row, seconds=0.1)
    row.holder_write = post_lands_just_before_the_release  # type: ignore[method-assign]
    import matrx_ai.tools.delegated_hold as module

    module._write = post_lands_just_before_the_release  # the fixture's monkeypatch restores it
    outcome = await asyncio.wait_for(task, 1)
    assert outcome.taken, "the POST was told held=True, so this turn MUST continue with the result"


@pytest.mark.asyncio
async def test_a_result_resolved_without_the_lease_is_never_continued_twice(row: Row) -> None:
    """The lease lapsed (a stalled holder): the POST cleared it and told the client to resume."""
    task = await _held(row)
    row.held_until = datetime.now(UTC) - timedelta(seconds=1)
    assert row.client_post() is False
    hold.wake("conv", "call")
    outcome = await asyncio.wait_for(task, 1)
    assert not outcome.taken and outcome.reason == "answered_elsewhere"


@pytest.mark.asyncio
async def test_a_draining_process_gives_the_hold_up(row: Row, monkeypatch: pytest.MonkeyPatch) -> None:
    draining = {"now": False}
    monkeypatch.setattr(hold, "_hooks", _hooks(may_hold=lambda: not draining["now"]))
    task = await _held(row)
    draining["now"] = True
    outcome = await asyncio.wait_for(task, 1)
    assert not outcome.taken and outcome.reason == "shutdown" and row.held_until is None
    assert hold.hold_seconds() == 0.0, "no new hold starts while draining"


@pytest.mark.asyncio
async def test_a_stop_gives_the_hold_up_and_leaves_the_call_parked(row: Row) -> None:
    stopped = {"now": False}

    async def stop_reason():
        return ("stopped", "the person stopped the turn") if stopped["now"] else None

    task = await _held(row, stop_reason=stop_reason)
    stopped["now"] = True
    outcome = await asyncio.wait_for(task, 1)
    assert not outcome.taken and outcome.reason == "stopped"
    assert row.status == "delegated" and row.held_until is None


@pytest.mark.asyncio
async def test_a_cancelled_wait_releases_its_lease(row: Row) -> None:
    task = await _held(row)
    await asyncio.sleep(0.01)
    task.cancel()
    with pytest.raises(asyncio.CancelledError):
        await task
    assert row.held_until is None and row.status == "delegated"
    assert hold.waiting_count() == 0


@pytest.mark.asyncio
async def test_a_long_wait_keeps_its_lease_alive(row: Row, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(hold, "_hooks", _hooks(lease_ms=lambda: 150, slow_poll_ms=lambda: 50))
    task = await _held(row)
    await asyncio.sleep(0.3)
    assert "renew" in row.writes
    row.client_post()
    hold.wake("conv", "call")
    assert (await asyncio.wait_for(task, 1)).taken


def test_an_unbound_package_never_holds(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(hold, "_hooks", None)
    assert hold.hold_seconds() == 0.0


def test_the_wait_never_outlives_the_dispatch_backstop(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(hold, "_hooks", _hooks(hold_ms=lambda _reason="client_tool": 10**9, max_hold_ms=lambda _reason="client_tool": 55 * 60_000))
    assert hold.hold_seconds() == 55 * 60.0


def test_an_unreadable_limit_means_no_hold_never_an_error_mid_wait(monkeypatch: pytest.MonkeyPatch) -> None:
    def unreadable() -> int:
        raise RuntimeError("feature knobs for 'runtime' were never loaded in this process")

    monkeypatch.setattr(hold, "_hooks", _hooks(lease_ms=unreadable))
    assert hold.settings() is None and hold.hold_seconds() == 0.0


@pytest.mark.asyncio
async def test_a_database_blip_mid_wait_never_becomes_a_failed_tool(row: Row, monkeypatch: pytest.MonkeyPatch) -> None:
    """The client may be running the call: an error reading the row must not escape the wait."""
    blips = {"left": 3}

    async def flaky_read(_row_id: str):
        if blips["left"]:
            blips["left"] -= 1
            raise ConnectionError("pool: connection reset")
        return row.view()

    async def quiet(*_a, **_k) -> None:
        return None

    monkeypatch.setattr(hold, "_report", quiet)
    task = await _held(row)
    monkeypatch.setattr(hold, "_read_row", flaky_read)
    row.client_post()
    outcome = await asyncio.wait_for(task, 2)
    assert outcome.taken and blips["left"] == 0


@pytest.mark.asyncio
async def test_a_database_down_for_a_whole_lease_parks_the_call_without_raising(
    row: Row, monkeypatch: pytest.MonkeyPatch
) -> None:
    async def down(*_a, **_k):
        raise ConnectionError("database unreachable")

    async def quiet(*_a, **_k) -> None:
        return None

    monkeypatch.setattr(hold, "_report", quiet)
    monkeypatch.setattr(hold, "_hooks", _hooks(lease_ms=lambda: 200, slow_poll_ms=lambda: 50))
    task = await _held(row)
    monkeypatch.setattr(hold, "_read_row", down)
    monkeypatch.setattr(hold, "_write", down)
    outcome = await asyncio.wait_for(task, 3)
    assert not outcome.taken and outcome.reason == "database"


def test_a_lease_shorter_than_three_polls_is_raised_and_said(monkeypatch: pytest.MonkeyPatch, capsys) -> None:
    monkeypatch.setattr(hold, "_hooks", _hooks(lease_ms=lambda: 5000, slow_poll_ms=lambda: 30_000))
    found = hold.settings()
    assert found is not None and found.lease_seconds == 90.0


@pytest.mark.asyncio
async def test_a_pending_call_answered_meanwhile_is_taken_at_the_batchs_end(monkeypatch: pytest.MonkeyPatch) -> None:
    """Two client-run calls in one reply: A's wait was given up, A was answered, B was taken under its
    hold. Nobody was told to resume, so the batch itself must take A's stored result."""
    from matrx_ai.db import cxm

    rows = {
        "call-a": SimpleNamespace(
            id="row-a", call_id="call-a", tool_name="get_page_text", tool_name_as_called="get_page_text",
            status="completed", resolved_at=datetime.now(UTC), is_error=False, is_client_delegated=True,
            output='{"text": "A"}', output_type="json", output_chars=13, output_preview=None,
            model_stub_at=None, metadata={}, error_type=None, error_message=None,
        ),
        "call-c": SimpleNamespace(id="row-c", call_id="call-c", status="delegated", resolved_at=None,
                                  is_client_delegated=True),
    }

    async def read(**kw):
        return [rows[kw["call_id"]]] if kw["call_id"] in rows else []

    monkeypatch.setattr(cxm.tool_call, "filter_items", read)
    taken = await hold.answered_meanwhile("conv", ["call-a", "call-c", "call-missing"])
    assert list(taken) == ["call-a"], "only an ANSWERED call is taken; an open one stays pending"
    assert taken["call-a"]["call_id"] == "call-a" and taken["call-a"]["is_error"] is False
