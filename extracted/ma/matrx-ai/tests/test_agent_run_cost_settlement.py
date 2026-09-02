"""A run that spends money must SAY it spent money.

`chat.agent_run.total_cost` was never written by anything — for the whole life of
the podcast feature every run reported $0.00 while its stages carried real
provider spend in `output.usage.cost_usd` (113 runs, ~$13.50 of unrecorded
charges, found 2026-08-11). These tests pin the settlement contract at the layer
that owns it, so the column can never go quiet again:

1. A terminal transition WRITES the cost — on success AND on failure (a run that
   burned a script agent and two video renders before dying still owes it).
2. Settlement is ADDITIVE across passes: a resumed run settles only the stages it
   actually paid for, on top of what the prior pass already settled. It must
   never overwrite the first pass's spend, and never double-count the replayed
   stages.
3. Each stage stamps its own cost on commit, so the run total always has
   per-stage evidence behind it.

These assert against a fake `arm` that records real writes — the test passes only
if the checkpointer genuinely issues them, never because the harness computed
the number itself.
"""

from __future__ import annotations

from decimal import Decimal
from typing import Any

import pytest

from matrx_ai.agent_runners import _checkpoint as ck
from matrx_ai.agent_runners._checkpoint import RunCheckpointer, stage_cost
from matrx_connect.streaming import error_capture


def _usage(cost: float) -> dict[str, Any]:
    return {
        "input_tokens": 10,
        "output_tokens": 5,
        "total_tokens": 15,
        "cost_usd": cost,
        "models": {},
    }


class _FakeRow:
    def __init__(self, **kw: Any) -> None:
        self.__dict__.update(kw)


class _FakeRuns:
    def __init__(self, run_id: str) -> None:
        self.row = _FakeRow(id=run_id, total_cost=Decimal("0"), status="processing")
        self.updates: list[dict[str, Any]] = []

    async def load_by_id(self, run_id: str) -> _FakeRow:
        return self.row

    async def update_item(self, run_id: str, **updates: Any) -> None:
        self.updates.append(dict(updates))
        for key, value in updates.items():
            setattr(self.row, key, value)


class _FakeStages:
    def __init__(self) -> None:
        self.rows: list[_FakeRow] = []

    async def filter_items(self, **filters: Any) -> list[_FakeRow]:
        return [
            row
            for row in self.rows
            if all(getattr(row, key, None) == value for key, value in filters.items())
        ]

    async def create_item(self, **kw: Any) -> _FakeRow:
        row = _FakeRow(id=f"stage-{len(self.rows)}", **kw)
        self.rows.append(row)
        return row

    async def update_item(self, row_id: str, **updates: Any) -> None:
        for row in self.rows:
            if row.id == row_id:
                row.__dict__.update(updates)


class _FakeArm:
    def __init__(self, run_id: str) -> None:
        self.runs = _FakeRuns(run_id)
        self.stages = _FakeStages()


@pytest.fixture
def arm(monkeypatch: pytest.MonkeyPatch) -> _FakeArm:
    fake = _FakeArm("run-1")
    monkeypatch.setattr(ck, "_arm", lambda: fake)
    return fake


def _ckpt() -> RunCheckpointer:
    return RunCheckpointer(run_id="run-1", completed={}, kind="podcast", user_id="u1")


async def test_finish_writes_the_cost(arm: _FakeArm) -> None:
    await _ckpt().finish({"success": True}, total_cost=1.0175563)

    assert arm.runs.updates[-1]["status"] == "completed"
    assert arm.runs.updates[-1]["total_cost"] == Decimal("1.017556")


async def test_a_paid_run_that_FAILED_still_settles(arm: _FakeArm) -> None:
    """The failure path is the one that matters most: the provider was paid
    whether or not the user got a podcast."""
    await _ckpt().fail("Audio generation failed: boom", total_cost=0.4231)

    assert arm.runs.updates[-1]["status"] == "failed"
    assert arm.runs.updates[-1]["total_cost"] == Decimal("0.423100")


async def test_a_resumed_pass_ADDS_its_delta_and_never_overwrites(arm: _FakeArm) -> None:
    # Pass 1 pays $0.60 and dies on audio.
    await _ckpt().fail("Audio generation failed", total_cost=0.60)
    assert arm.runs.row.total_cost == Decimal("0.600000")

    # Pass 2 replays every completed stage for free (so its settle-safe delta is
    # only the audio it actually re-bought) and finishes.
    await _ckpt().finish({"success": True}, total_cost=0.18)

    assert arm.runs.row.total_cost == Decimal("0.780000"), (
        "a resumed pass must ADD its own spend to the run's lifetime total — "
        "overwriting would erase pass 1's charges"
    )


async def test_terminal_write_failure_is_captured_and_spine_is_not_marked_completed(
    arm: _FakeArm,
) -> None:
    captured: list[tuple[BaseException, str, dict[str, Any]]] = []
    settled: list[tuple[str, str | None]] = []

    async def capture(exc: BaseException, *, kind: str, **fields: Any) -> None:
        captured.append((exc, kind, fields))

    async def broken_update(_run_id: str, **_updates: Any) -> None:
        raise RuntimeError("terminal write unavailable")

    async def settle(status: str, error: str | None = None) -> None:
        settled.append((status, error))

    error_capture.configure_error_capture(capture, allow_in_tests=True)
    try:
        arm.runs.update_item = broken_update  # type: ignore[method-assign]
        checkpointer = _ckpt()
        checkpointer._spine_settle = settle
        await checkpointer.finish({"success": True})
    finally:
        error_capture.configure_error_capture(None)

    assert captured[0][1] == "agent_run_persistence_failed"
    assert captured[0][2]["payload"]["operation"] == "_finish_run"
    assert settled == [("failed", "agent_run terminal persistence failed")]


async def test_no_cost_leaves_the_existing_total_untouched(arm: _FakeArm) -> None:
    """A pass with nothing billable must not stamp a zero over real spend."""
    arm.runs.row.total_cost = Decimal("0.75")
    await _ckpt().finish({"success": True}, total_cost=None)

    assert "total_cost" not in arm.runs.updates[-1]
    assert arm.runs.row.total_cost == Decimal("0.75")


async def test_each_stage_stamps_its_own_cost_on_commit(arm: _FakeArm) -> None:
    ckpt = _ckpt()

    async def _stage() -> dict[str, Any]:
        return {"stage": "create_audio", "success": True, "output": "cdn://a.mp3",
                "usage": _usage(0.18195)}

    await ckpt.stage("create_audio", _stage)

    row = arm.stages.rows[-1]
    assert row.stage_key == "create_audio"
    assert row.cost == Decimal("0.18195"), "the stage's own spend must reach its column"


async def test_stage_cost_reads_nothing_as_None_not_zero() -> None:
    """`None` and `0` mean different things: 'this stage tracked no usage' must
    not become 'this stage was free', or a reconciliation can't tell them apart."""
    assert stage_cost({"success": True, "output": "x"}) is None
    assert stage_cost({"usage": {"cost_usd": None}}) is None
    assert stage_cost({"usage": {"cost_usd": 0.0}}) == Decimal("0.0")
    assert stage_cost({"usage": "not-a-dict"}) is None
    assert stage_cost(None) is None


async def test_a_FRESH_run_settles_what_it_spent_end_to_end(arm: _FakeArm) -> None:
    """The bug this file exists for, at the layer it actually lived on.

    Every stage goes through `ckpt.stage()` -> `_stage_from_payload`, on fresh
    runs as well as replays. When that reconstruction marked fresh stages
    'already settled', `_unsettled_cost` came out empty and `finish()` wrote
    nothing — a run with $0.05 of real charges reported $0.00 (live run 55850645,
    2026-08-11). This drives the real chain: run stages, aggregate, settle.
    """
    from matrx_ai.agent_runners.podcast_generator import _stage_from_payload, _unsettled_cost

    ckpt = _ckpt()
    stage_results = []
    for key, cost in (("create_script", 0.036040), ("create_audio", 0.015580)):
        async def _fn(key: str = key, cost: float = cost) -> dict[str, Any]:
            return {"stage": key, "success": True, "output": "x", "usage": _usage(cost)}

        stage_results.append(_stage_from_payload(key, await ckpt.stage(key, _fn)))

    await ckpt.finish({"success": True}, total_cost=_unsettled_cost(stage_results))

    assert arm.runs.row.total_cost == Decimal("0.051620"), (
        "a fresh run must settle every stage it just paid for"
    )


async def test_a_RESUMED_run_settles_only_the_stages_it_re_bought(arm: _FakeArm) -> None:
    """The other half: replaying a checkpoint must not re-bill it."""
    from matrx_ai.agent_runners.podcast_generator import _stage_from_payload, _unsettled_cost

    # Attempt 1 pays for the script, then dies.
    first = _ckpt()

    async def _script() -> dict[str, Any]:
        return {"stage": "create_script", "success": True, "output": "s", "usage": _usage(0.036040)}

    script_payload = await first.stage("create_script", _script)
    await first.fail("died", total_cost=_unsettled_cost([_stage_from_payload("create_script", script_payload)]))
    assert arm.runs.row.total_cost == Decimal("0.036040")

    # Attempt 2 replays the script for free and buys only the audio.
    second = RunCheckpointer(
        run_id="run-1", completed={"create_script": script_payload}, kind="podcast", user_id="u1"
    )
    replayed = _stage_from_payload("create_script", await second.stage("create_script", _script))

    async def _audio() -> dict[str, Any]:
        return {"stage": "create_audio", "success": True, "output": "a", "usage": _usage(0.015580)}

    audio = _stage_from_payload("create_audio", await second.stage("create_audio", _audio))
    await second.finish({"success": True}, total_cost=_unsettled_cost([replayed, audio]))

    assert arm.runs.row.total_cost == Decimal("0.051620"), (
        "the resumed pass must add ONLY the audio it re-bought — never re-bill the "
        "replayed script, never drop attempt 1's spend"
    )
