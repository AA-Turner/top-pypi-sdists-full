"""THE REPEAT GUARD's predicate, proven against the shapes that caused it.

Every case here is a real 2026-08-14 live scheduler row shape, not an invention:
the GA4 dispatcher (4/4 failed, one cause — must escalate), the backlink
dispatcher (fails on individual URLs between successful runs — must NOT
escalate), and the agent tasks that failed 103 times and were then repaired
(a success resets the streak to zero).
"""

from __future__ import annotations

import pytest

from matrx_scheduler import repeat_guard
from matrx_scheduler.repeat_guard import (
    MAX_CONSECUTIVE_FAILURES,
    check_task_failure_streak,
    failure_signature,
)


class _FakeQuery:
    def __init__(self, rows: list[dict]) -> None:
        self._rows = rows

    def order_by(self, *_a: str) -> _FakeQuery:
        return self

    def limit(self, *_a: int) -> _FakeQuery:
        return self

    async def values(self, *_fields: str) -> list[dict]:
        return self._rows


class _FakeModel:
    """Honors ``status__in`` so the "has it EVER succeeded?" read is real —
    without it the never-worked ceiling would silently never be exercised."""

    rows: list[dict] = []
    task_rows: list[dict] = []
    trigger_rows: list[dict] = []

    @classmethod
    def filter(cls, **kw: object) -> _FakeQuery:
        wanted = kw.get("status__in")
        if wanted is not None:
            allowed = {str(s).lower() for s in wanted}  # type: ignore[union-attr]
            return _FakeQuery(
                [r for r in cls.rows if str(r.get("status") or "").lower() in allowed]
            )
        return _FakeQuery(cls.rows)


class _UpdateResult:
    def __init__(self, updated: bool) -> None:
        self.updated_rows = [{}] if updated else []


class _TaskModel:
    rows: list[dict] = []

    @classmethod
    def filter(cls, **kw: object) -> _FakeQuery:
        return _FakeQuery([r for r in cls.rows if all(r.get(k) == v for k, v in kw.items())])

    @classmethod
    async def update_where(cls, filters: dict, **updates: object) -> _UpdateResult:
        matched = [r for r in cls.rows if all(r.get(k) == v for k, v in filters.items())]
        for row in matched:
            row.update(updates)
        return _UpdateResult(bool(matched))


class _TriggerModel(_TaskModel):
    pass


@pytest.fixture
def ledger(monkeypatch):
    def _install(rows: list[dict]) -> None:
        _FakeModel.rows = rows
        monkeypatch.setattr(repeat_guard, "get_db_model", lambda _n: _FakeModel)

    return _install


def _failed(msg: str) -> dict:
    return {"status": "failed", "error_message": msg}


def _ok() -> dict:
    return {"status": "success", "error_message": None}


@pytest.mark.asyncio
async def test_threshold_auto_suspends_task_and_trigger_once(monkeypatch) -> None:
    task_id = "task"
    _FakeModel.rows = [_failed(GA4_ERROR)] * MAX_CONSECUTIVE_FAILURES
    _TaskModel.rows = [{"id": task_id, "enabled": True, "metadata": {}}]
    _TriggerModel.rows = [{"id": "trigger", "task_id": task_id, "enabled": True, "metadata": {}}]
    alarms = []

    def models(name: str):
        return {"SchRun": _FakeModel, "SchTask": _TaskModel, "SchTrigger": _TriggerModel}[name]

    async def sink(alarm) -> None:
        alarms.append(alarm)

    monkeypatch.setattr(repeat_guard, "get_db_model", models)
    monkeypatch.setattr(
        repeat_guard,
        "get_optional_ext",
        lambda name: sink if name == "escalation_sink" else None,
    )

    await repeat_guard.note_failed_run("run", task_id=task_id)
    await repeat_guard.note_failed_run("run", task_id=task_id)

    assert _TaskModel.rows[0]["enabled"] is False
    assert _TriggerModel.rows[0]["enabled"] is False
    assert _TaskModel.rows[0]["metadata"]["auto_suspended"]["run_id"] == "run"
    # The sink fires on EVERY escalating failure, not only the one that won the
    # disable race — gating it on the suspension is how an already-disabled
    # task never raised its chip. Dedupe is the host sink's contract (assists
    # dedupe_key); the package hands over the streak and says whether THIS call
    # suspended.
    assert len(alarms) == 2
    assert alarms[0].suspended is True
    assert alarms[1].suspended is False
    assert alarms[0].approval is None
    assert "overriding_approval" not in _TaskModel.rows[0]["metadata"]["auto_suspended"]


def _productive_failed(msg: str, units: int) -> dict:
    """A run stamped failed whose ledger row says it committed work — the exact
    shape of scheduler run 78c5de02 on 2026-08-26 (839 keywords, then a blip)."""
    return {"status": "failed", "error_message": msg, "result_metadata": {"units_done": units}}


TRANSPORT_BLIP = (
    "MandateError: Mandate 'seo.keyword_classifier': agent 5ca54dd9 failed: Google "
    "rejected the request: Response payload is not completed: <TransferEncodingError: "
    "400, message='Not enough data to satisfy transfer length header.'>."
)
MANDATE_BUG = "AttributeError: 'NoneType' object has no attribute 'context_entries'"


@pytest.mark.asyncio
async def test_the_real_2026_08_26_ledger_does_not_read_as_never_succeeded(ledger) -> None:
    """The five rows the guard disabled an approved schedule on: three fixed-bug
    failures, one blank failure, and — newest — a run that classified 839
    keywords before a transport blip. Work landed; the schedule works."""
    ledger(
        [
            _productive_failed(TRANSPORT_BLIP, 839),
            _failed(""),
            _failed(MANDATE_BUG),
            _failed(MANDATE_BUG),
            _failed(MANDATE_BUG),
        ]
    )
    streak = await check_task_failure_streak("task")
    assert streak is None or streak.escalate is False, streak


@pytest.mark.asyncio
async def test_a_productive_run_ends_the_streak_like_a_success(ledger) -> None:
    ledger([_failed(GA4_ERROR), _failed(GA4_ERROR), _productive_failed(GA4_ERROR, 20)]
           + [_failed(GA4_ERROR)] * 10)
    streak = await check_task_failure_streak("task")
    assert streak is not None
    assert streak.escalate is False
    assert streak.consecutive_failures == 2


@pytest.mark.asyncio
async def test_unmeasured_metadata_never_reads_as_productive(ledger) -> None:
    rows = [_failed(GA4_ERROR) for _ in range(4)]
    rows[0]["result_metadata"] = {"classified": 839}  # a handler's own key, not the contract
    rows[1]["result_metadata"] = {"units_done": "lots"}
    rows[2]["result_metadata"] = None
    ledger(rows)
    streak = await check_task_failure_streak("task")
    assert streak is not None and streak.escalate is True


@pytest.mark.asyncio
async def test_suspending_an_approved_task_says_so_and_keeps_the_approval(monkeypatch) -> None:
    task_id = "approved-task"
    _FakeModel.rows = [_failed(GA4_ERROR)] * MAX_CONSECUTIVE_FAILURES
    approval_fields = {
        "approval": "Approved: seo_keyword_facet_backfill, daily 04:20 UTC, ≤4,000 keywords/day",
        "approved_by": "arman",
        "approved_at": "2026-08-22",
    }
    _TaskModel.rows = [{"id": task_id, "enabled": True, "metadata": dict(approval_fields)}]
    _TriggerModel.rows = [{"id": "trigger", "task_id": task_id, "enabled": True, "metadata": {}}]
    alarms = []

    def models(name: str):
        return {"SchRun": _FakeModel, "SchTask": _TaskModel, "SchTrigger": _TriggerModel}[name]

    async def sink(alarm) -> None:
        alarms.append(alarm)

    monkeypatch.setattr(repeat_guard, "get_db_model", models)
    monkeypatch.setattr(
        repeat_guard, "get_optional_ext", lambda name: sink if name == "escalation_sink" else None
    )

    await repeat_guard.note_failed_run("run-1", task_id=task_id)

    meta = _TaskModel.rows[0]["metadata"]
    assert _TaskModel.rows[0]["enabled"] is False
    for key, value in approval_fields.items():
        assert meta[key] == value, f"approval field {key} was altered"
    block = meta["auto_suspended"]
    assert "arman" in block["overriding_approval"]
    assert "OVERRIDING" in block["override_notice"]
    assert "restores" in block["override_notice"].lower()
    assert _TriggerModel.rows[0]["metadata"]["auto_suspended"]["overriding_approval"] == block["overriding_approval"]
    assert len(alarms) == 1
    assert alarms[0].suspended is True
    assert "arman" in alarms[0].approval

    # A second suspension keeps the first as history instead of overwriting it.
    _TaskModel.rows[0]["enabled"] = True
    _TriggerModel.rows[0]["enabled"] = True
    await repeat_guard.note_failed_run("run-2", task_id=task_id)
    meta = _TaskModel.rows[0]["metadata"]
    assert meta["auto_suspended"]["run_id"] == "run-2"
    assert [h["run_id"] for h in meta["auto_suspended_history"]] == ["run-1"]


@pytest.mark.asyncio
async def test_an_already_disabled_task_still_escalates(monkeypatch) -> None:
    task_id = "already-off"
    _FakeModel.rows = [_failed(GA4_ERROR)] * MAX_CONSECUTIVE_FAILURES
    _TaskModel.rows = [{"id": task_id, "enabled": False, "metadata": {}}]
    _TriggerModel.rows = []
    alarms = []

    def models(name: str):
        return {"SchRun": _FakeModel, "SchTask": _TaskModel, "SchTrigger": _TriggerModel}[name]

    async def sink(alarm) -> None:
        alarms.append(alarm)

    monkeypatch.setattr(repeat_guard, "get_db_model", models)
    monkeypatch.setattr(
        repeat_guard, "get_optional_ext", lambda name: sink if name == "escalation_sink" else None
    )
    await repeat_guard.note_failed_run("run", task_id=task_id)
    assert len(alarms) == 1 and alarms[0].suspended is False
    assert "auto_suspended" not in _TaskModel.rows[0]["metadata"]


# Genuinely different diagnoses — not one cause wearing different ids. This is
# the GA4 shape: each partial repair replaced the error with a new one.
_NINE_DISTINCT_CAUSES = [
    "3 site syncs failed",
    "ResourceBindingError: the analytics_property was never discovered",
    "GA4 Data API PERMISSION_DENIED: the API is disabled for this project",
    "the connection has no refresh token",
    "scraper-service returned an unprocessable entity",
    "permission denied for table backlink",
    "no agent_id on task",
    "the provider timed out while streaming",
    "the storage bucket vanished",
]

GA4_ERROR = (
    "site 38eff4c9-b021-451a-b995-7d9b3d17db5e: ProviderResponseError: 1 GA4 request "
    "or pagination failure(s): GA4 Data API PERMISSION_DENIED: Google Analytics Data "
    "API has not been used in project 34576215171 before or it is disabled."
)


@pytest.mark.asyncio
async def test_same_cause_every_run_escalates(ledger) -> None:
    """The GA4 dispatcher: 4 of 4 failed, one cause, no success ever."""
    ledger([_failed(GA4_ERROR)] * 4)

    streak = await check_task_failure_streak("ga4-task")

    assert streak is not None
    assert streak.escalate is True
    assert streak.consecutive_failures == 4


@pytest.mark.asyncio
async def test_a_success_resets_the_streak(ledger) -> None:
    """The repaired agent tasks: 103 failures behind 21 successes must be quiet."""
    ledger([_ok()] * 3 + [_failed("no agent_id on task")] * 103)

    streak = await check_task_failure_streak("repaired-task")

    assert streak is None or streak.escalate is False


@pytest.mark.asyncio
async def test_different_ids_same_cause_still_counts(ledger) -> None:
    """A dispatcher naming a different row each run is still ONE stuck cause."""
    ledger(
        [
            _failed("site 57711943-0c42-4281-bc1d-f045df8700a4: quota exhausted at 14:02:01"),
            _failed("site d0aff5b6-0710-4848-8304-164db3c80ab7: quota exhausted at 13:02:00"),
            _failed("site 38eff4c9-b021-451a-b995-7d9b3d17db5e: quota exhausted at 12:02:09"),
        ]
    )

    streak = await check_task_failure_streak("dispatcher")

    assert streak is not None and streak.escalate is True


@pytest.mark.asyncio
async def test_a_changed_cause_breaks_the_same_way_streak(ledger) -> None:
    """Failing a NEW way is not the same stuck schedule. Given a task that HAS
    worked before, six mixed failures stay under every ceiling."""
    ledger([_failed("scraper returned 422")] + [_failed(GA4_ERROR)] * 5 + [_ok()])

    streak = await check_task_failure_streak("changed")

    assert streak is not None
    assert streak.consecutive_failures == 1
    assert streak.escalate is False


@pytest.mark.asyncio
async def test_never_succeeding_escalates_even_when_the_cause_keeps_changing(
    ledger,
) -> None:
    """THE GA4 CASE. Same-signature counting alone stayed silent on a task that
    has never once succeeded, because each partial repair changed the error."""
    ledger([_failed(m) for m in _NINE_DISTINCT_CAUSES])

    streak = await check_task_failure_streak("never-worked")

    assert streak is not None
    assert streak.escalate is True
    assert streak.consecutive_failures == 9
    assert streak.signature == repeat_guard.ANY_CAUSE_SIGNATURE


@pytest.mark.asyncio
async def test_the_real_ga4_ledger_escalates_at_four(ledger) -> None:
    """THE EXACT LIVE CASE, 2026-08-14: four runs, four failures, three different
    causes as partial repairs landed, zero successes ever. Under same-signature
    counting this task was silent; it must not be."""
    ledger(
        [
            _failed("GA4 Data API PERMISSION_DENIED: the API is disabled for this project"),
            _failed("ResourceBindingError: the analytics_property was never discovered"),
            _failed("3 site syncs failed"),
            _failed("3 site syncs failed"),
        ]
    )

    streak = await check_task_failure_streak("ga4")

    assert streak is not None
    assert streak.escalate is True
    assert streak.signature == repeat_guard.ANY_CAUSE_SIGNATURE
    assert "NEVER succeeded" in (streak.reason or "")


@pytest.mark.asyncio
async def test_a_task_that_has_worked_before_gets_the_higher_bar(ledger) -> None:
    """Same four mixed failures, but a success exists in history — that is a
    regression to watch, not a task nobody has seen work. Stay quiet at four."""
    ledger(
        [
            _failed("GA4 Data API PERMISSION_DENIED: the API is disabled"),
            _failed("ResourceBindingError: the property was never discovered"),
            _failed("3 site syncs failed"),
            _failed("the provider timed out"),
            _ok(),
        ]
    )

    streak = await check_task_failure_streak("used-to-work")

    assert streak is not None and streak.escalate is False


@pytest.mark.asyncio
async def test_never_succeeding_chip_is_deduped_across_changing_errors(ledger) -> None:
    """A task failing a new way every run must raise ONE chip, not one per run."""
    ledger([_failed(m) for m in _NINE_DISTINCT_CAUSES])
    first = await check_task_failure_streak("t")
    ledger([_failed("the storage bucket vanished")] + [_failed(m) for m in _NINE_DISTINCT_CAUSES])
    second = await check_task_failure_streak("t")

    assert first is not None and second is not None
    assert first.signature == second.signature  # same dedupe_key => one chip


@pytest.mark.asyncio
async def test_below_the_ceiling_is_silent(ledger) -> None:
    """One failure is noise, two can be a deploy. Only the third is a pattern."""
    ledger([_failed(GA4_ERROR)] * (MAX_CONSECUTIVE_FAILURES - 1))

    streak = await check_task_failure_streak("noisy")

    assert streak is not None and streak.escalate is False


@pytest.mark.asyncio
async def test_running_rows_do_not_break_the_streak(ledger) -> None:
    """A run in flight is not a verdict — it must not reset the count."""
    ledger(
        [{"status": "running", "error_message": None}]
        + [_failed(GA4_ERROR)] * MAX_CONSECUTIVE_FAILURES
    )

    streak = await check_task_failure_streak("inflight")

    assert streak is not None and streak.escalate is True


@pytest.mark.asyncio
async def test_an_unreadable_ledger_never_raises(monkeypatch) -> None:
    """Fail OPEN: the guard must never become a new way for a run to die."""

    class _Broken:
        @classmethod
        def filter(cls, **_kw: object):
            raise RuntimeError("ledger is down")

    monkeypatch.setattr(repeat_guard, "get_db_model", lambda _n: _Broken)

    assert await check_task_failure_streak("any") is None


def test_signature_ignores_volatile_detail_but_not_the_cause() -> None:
    a = "site 57711943-0c42-4281-bc1d-f045df8700a4: quota exhausted at 2026-08-14 21:37:01+00"
    b = "site d0aff5b6-0710-4848-8304-164db3c80ab7: quota exhausted at 2026-08-14 22:37:44+00"
    assert failure_signature(a) == failure_signature(b)
    assert failure_signature(a) != failure_signature("permission denied for table backlink")


def test_a_silent_failure_still_gets_a_signature() -> None:
    """A task failing with no message at all is exactly what must not stay quiet."""
    assert failure_signature(None) == failure_signature("")
