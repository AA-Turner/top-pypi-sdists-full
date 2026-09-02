"""Forcing-function: request_snapshot must not write when store=False.

Ephemeral runs assign a real conversation UUID but create no parent row.
The failure-path snapshot writer used to queue anyway → permanent
``request_snapshot_conversation_id_fkey`` orphans in system_write_failure
(seen 2026-07-10: 6 rows across 2 ephemeral provider failures).

Gut check: if the store gate is removed from ``_write_request_snapshot``,
this test fails — the queue helper must never be called for store=False.
"""

from __future__ import annotations

import ast
import inspect
from types import SimpleNamespace
from uuid import uuid4

import pytest

from matrx_ai.orchestrator import executor as executor_mod
from matrx_ai.orchestrator.execution_state import ExecutionState

_FAKE_COORD = object()  # in-lane sentinel: the writer must route through the queue


def test_success_path_awaits_snapshot_writer_before_losing_request_lane() -> None:
    """The call site must queue into the parent conversation's Coordinator."""
    tree = ast.parse(inspect.getsource(executor_mod._execute_until_complete_inner))
    awaited_snapshot_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Await)
        and isinstance(node.value, ast.Call)
        and getattr(node.value.func, "id", None) == "_write_request_snapshot"
    ]
    assert awaited_snapshot_calls, (
        "success snapshot capture must be awaited in-lane; detaching it clears "
        "the Coordinator and races its FK parent commit"
    )


def _with_lane(monkeypatch):
    """Pretend a WriteCoordinator/lane is active so the queue path is taken."""
    monkeypatch.setattr(
        "matrx_ai.persistence.queue_helpers.get_coordinator", lambda: _FAKE_COORD
    )


@pytest.mark.asyncio
async def test_write_request_snapshot_skips_when_store_false(monkeypatch):
    queued: list[dict] = []

    monkeypatch.setattr(
        "matrx_ai.persistence.queue_helpers.queue_request_snapshot_create",
        lambda **kwargs: queued.append(kwargs) or "op",
    )

    exec_ctx = SimpleNamespace(
        store=False,
        conversation_id=str(uuid4()),
        request_id=str(uuid4()),
    )
    state = ExecutionState()

    await executor_mod._write_request_snapshot(
        exec_ctx=exec_ctx,
        iteration=1,
        api_response=None,
        request_payload={"messages": []},
        unified_payload={"config": {"store": False}},
        trigger_position=0,
        first_assistant_position=1,
        state_snapshot=state.snapshot(),
        error_payload={"outcome": "error"},
        provider="openai",
        model="gpt-test",
    )

    assert queued == [], (
        f"ephemeral store=False must never queue request_snapshot — got {len(queued)} queue call(s)"
    )


@pytest.mark.asyncio
async def test_write_request_snapshot_queues_when_store_true(monkeypatch):
    queued: list[dict] = []

    _with_lane(monkeypatch)
    monkeypatch.setattr(
        "matrx_ai.persistence.queue_helpers.queue_request_snapshot_create",
        lambda **kwargs: queued.append(kwargs) or "op",
    )

    conversation_id = str(uuid4())
    request_id = str(uuid4())
    exec_ctx = SimpleNamespace(
        store=True,
        conversation_id=conversation_id,
        request_id=request_id,
    )
    state = ExecutionState()

    await executor_mod._write_request_snapshot(
        exec_ctx=exec_ctx,
        iteration=1,
        api_response=None,
        request_payload={"messages": [{"role": "user", "content": "hi"}]},
        unified_payload={"config": {"store": True}},
        trigger_position=0,
        first_assistant_position=1,
        state_snapshot=state.snapshot(),
        error_payload={"outcome": "error"},
        provider="openai",
        model="gpt-test",
    )

    assert len(queued) == 1
    assert queued[0]["conversation_id"] == conversation_id
    assert queued[0]["user_request_id"] == request_id


@pytest.mark.asyncio
async def test_write_request_snapshot_stamps_organization_from_request_metadata(monkeypatch):
    queued: list[dict] = []
    _with_lane(monkeypatch)
    monkeypatch.setattr(
        "matrx_ai.persistence.queue_helpers.queue_request_snapshot_create",
        lambda **kwargs: queued.append(kwargs) or "op",
    )

    organization_id = str(uuid4())
    await executor_mod._write_request_snapshot(
        exec_ctx=SimpleNamespace(
            store=True,
            conversation_id=str(uuid4()),
            request_id=str(uuid4()),
            metadata={"organization_id": organization_id},
        ),
        iteration=1,
        api_response=None,
        request_payload={"messages": [{"role": "user", "content": "hi"}]},
        unified_payload={"config": {"store": True}},
        trigger_position=0,
        first_assistant_position=1,
        state_snapshot=ExecutionState().snapshot(),
        error_payload={"outcome": "error"},
        provider="anthropic",
        model="claude-sonnet-5",
    )

    assert queued[0]["organization_id"] == organization_id


@pytest.mark.asyncio
async def test_write_request_snapshot_prefers_typed_request_organization(monkeypatch):
    queued: list[dict] = []
    _with_lane(monkeypatch)
    monkeypatch.setattr(
        "matrx_ai.persistence.queue_helpers.queue_request_snapshot_create",
        lambda **kwargs: queued.append(kwargs) or "op",
    )

    organization_id = str(uuid4())
    await executor_mod._write_request_snapshot(
        exec_ctx=SimpleNamespace(
            store=True,
            conversation_id=str(uuid4()),
            request_id=str(uuid4()),
            organization_id=organization_id,
            metadata={"organization_id": str(uuid4())},
        ),
        iteration=1,
        api_response=None,
        request_payload={"messages": [{"role": "user", "content": "hi"}]},
        unified_payload=None,
        trigger_position=0,
        first_assistant_position=1,
        state_snapshot=ExecutionState().snapshot(),
        error_payload={"outcome": "error"},
        provider="anthropic",
        model="claude-sonnet-5",
    )

    assert queued[0]["organization_id"] == organization_id


# ── The always-on gate (D-33, 2026-08-15) ───────────────────────────────────
# Capture is ON by default; the per-request flag survives only as an override.
# These pin the three cells that matter — the default, the explicit opt-out,
# and the ephemeral invariant that no override may ever defeat.


def test_capture_default_is_on() -> None:
    assert executor_mod.REQUEST_SNAPSHOT_CAPTURE_DEFAULT is True, (
        "snapshot capture is always-on (D-33); a snapshot you have to remember "
        "to ask for is a regression case you don't have"
    )


def test_snapshot_enabled_defaults_on_when_request_says_nothing() -> None:
    assert executor_mod._request_snapshot_enabled(SimpleNamespace(store=True, snapshot=None))
    # A caller that never set the attribute at all (e.g. a bare context object)
    # gets the default too — absence is not opt-out.
    assert executor_mod._request_snapshot_enabled(SimpleNamespace(store=True))


def test_explicit_false_is_honored_as_opt_out() -> None:
    assert not executor_mod._request_snapshot_enabled(SimpleNamespace(store=True, snapshot=False))


def test_explicit_true_still_forces_capture() -> None:
    assert executor_mod._request_snapshot_enabled(SimpleNamespace(store=True, snapshot=True))


@pytest.mark.parametrize("flag", [None, True, False])
def test_ephemeral_never_captures_whatever_the_override_says(flag) -> None:
    assert not executor_mod._request_snapshot_enabled(
        SimpleNamespace(store=False, snapshot=flag)
    ), "store=False is a hard invariant, not a volume knob — no override may defeat it"


# ── Row identity: a snapshot must say WHICH model/provider produced it ──────
# A row that can't name its model is a weak replay input ("re-execute with the
# config that ran it" needs the config). Measured 2026-08-16 on the live table:
# 2,004 of 2,600 rows carried provider='unknown', model=NULL, because the writer
# read bare "provider"/"model" keys off UnifiedResponse.metadata and nothing
# stamps those. Invisible at 2 rows/day; every row once capture went always-on.


async def _capture_queued(monkeypatch, **kwargs):
    queued: list[dict] = []
    _with_lane(monkeypatch)
    monkeypatch.setattr(
        "matrx_ai.persistence.queue_helpers.queue_request_snapshot_create",
        lambda **kw: queued.append(kw) or "op",
    )
    await executor_mod._write_request_snapshot(
        exec_ctx=SimpleNamespace(store=True, conversation_id=str(uuid4()), request_id=str(uuid4())),
        iteration=1,
        request_payload={"messages": []},
        unified_payload=None,
        trigger_position=0,
        first_assistant_position=1,
        state_snapshot=ExecutionState().snapshot(),
        **kwargs,
    )
    return queued


@pytest.mark.asyncio
async def test_explicit_provider_and_model_are_recorded(monkeypatch):
    queued = await _capture_queued(
        monkeypatch,
        api_response=None,
        error_payload={"outcome": "error"},
        provider="anthropic",
        model="claude-sonnet-5",
    )
    assert queued[0]["provider"] == "anthropic"
    assert queued[0]["model"] == "claude-sonnet-5", (
        "the model the request ran with must reach the row — it is what replay re-executes"
    )


@pytest.mark.asyncio
async def test_model_falls_back_to_the_providers_own_metadata_vocabulary(monkeypatch):
    # Nobody stamps a bare "model"; providers stamp matrx_model_name.
    api_response = SimpleNamespace(
        metadata={"matrx_model_name": "gpt-4o-mini", "provider_model_name": "gpt-4o-mini-2024"},
        to_dict=lambda: {"ok": True},
    )
    queued = await _capture_queued(monkeypatch, api_response=api_response)
    assert queued[0]["model"] == "gpt-4o-mini"


# ── Out-of-lane fallback (2026-08-17) ───────────────────────────────────────
# A mandated agent / NamedAgent.run in a background pipeline has NO RequestLane,
# so the queue helper log+DROPs the write. That silently produced ZERO snapshots
# for every podcast/mandated run (runs 6c2f768f + 34e2d7f4: 15 child
# conversations, 0 rows, 0 failure alarms) while always-on capture (D-33)
# claimed coverage. Out of lane the writer must fall back to a DIRECT insert.
# Gut check: revert the fallback and these fail.


class _FakeSnapshotModel:
    def __init__(self) -> None:
        self.created: list[dict] = []

    async def create(self, **kwargs):
        self.created.append(kwargs)
        return SimpleNamespace(id=kwargs.get("id"))


def _without_lane(monkeypatch) -> _FakeSnapshotModel:
    monkeypatch.setattr("matrx_ai.persistence.queue_helpers.get_coordinator", lambda: None)
    fake_model = _FakeSnapshotModel()
    fake_cxm = SimpleNamespace(request_snapshot=SimpleNamespace(model=fake_model))
    monkeypatch.setattr("matrx_ai.db.cx_managers.cxm", fake_cxm)
    return fake_model


@pytest.mark.asyncio
async def test_out_of_lane_write_falls_back_to_direct_insert(monkeypatch):
    queued: list[dict] = []
    monkeypatch.setattr(
        "matrx_ai.persistence.queue_helpers.queue_request_snapshot_create",
        lambda **kw: queued.append(kw) or "",
    )
    fake_model = _without_lane(monkeypatch)

    conversation_id = str(uuid4())
    request_id = str(uuid4())
    user_id = str(uuid4())
    await executor_mod._write_request_snapshot(
        exec_ctx=SimpleNamespace(
            store=True,
            conversation_id=conversation_id,
            request_id=request_id,
            user_id=user_id,
            organization_id=None,
        ),
        iteration=1,
        api_response=None,
        request_payload={"messages": [{"role": "user", "content": "hi"}]},
        unified_payload={"config": {"store": True}},
        trigger_position=0,
        first_assistant_position=1,
        state_snapshot=ExecutionState().snapshot(),
        error_payload={"outcome": "error"},
        provider="anthropic",
        model="claude-sonnet-5",
    )

    assert queued == [], "no lane → the queue path must not be attempted (it would drop the op)"
    assert len(fake_model.created) == 1, (
        "out-of-lane snapshot must land via a direct insert — dropping it is how every "
        "podcast/mandated run recorded zero snapshots"
    )
    row = fake_model.created[0]
    assert row["conversation_id"] == conversation_id
    assert row["user_request_id"] == request_id
    assert row["created_by"] == user_id
    assert row["provider"] == "anthropic"


@pytest.mark.asyncio
async def test_out_of_lane_session_report_reaches_structured_capture(monkeypatch):
    _without_lane(monkeypatch)
    captured: list[tuple[BaseException, dict]] = []

    class _FailedSession:
        async def __aenter__(self):
            return self

        async def __aexit__(self, *_args):
            return False

        async def flush(self, **_kwargs):
            return SimpleNamespace(error="forced snapshot FK failure")

    monkeypatch.setattr("matrx_orm.Session", _FailedSession)

    async def _capture(exc, context):
        captured.append((exc, context))

    monkeypatch.setattr(
        executor_mod,
        "_record_snapshot_capture_failure",
        _capture,
    )

    await executor_mod._write_request_snapshot(
        exec_ctx=SimpleNamespace(
            store=True,
            conversation_id=str(uuid4()),
            request_id=str(uuid4()),
            user_id=str(uuid4()),
            organization_id=str(uuid4()),
        ),
        iteration=1,
        api_response=None,
        request_payload={"messages": []},
        unified_payload={"config": {"store": True}},
        trigger_position=0,
        first_assistant_position=1,
        state_snapshot=ExecutionState().snapshot(),
        error_payload={"outcome": "error"},
        provider="openai",
        model="gpt-test",
    )

    assert len(captured) == 1
    assert captured[0][1]["path"] == "success"
    assert "forced snapshot FK failure" in str(captured[0][0])


@pytest.mark.asyncio
async def test_snapshot_failure_uses_canonical_system_error_kind(monkeypatch):
    calls: list[dict] = []

    async def _record_error(_exc, **fields):
        calls.append(fields)

    monkeypatch.setattr("matrx_ai._ext.get_ext", lambda _key: _record_error)
    await executor_mod._record_snapshot_capture_failure(
        RuntimeError("forced capture proof"), {"path": "forced_test"}
    )

    assert calls[0]["kind"] == executor_mod.REQUEST_SNAPSHOT_CAPTURE_FAILURE_KIND
    assert calls[0]["route"] == "request_snapshot_capture"


@pytest.mark.asyncio
async def test_out_of_lane_ephemeral_still_never_writes(monkeypatch):
    fake_model = _without_lane(monkeypatch)
    await executor_mod._write_request_snapshot(
        exec_ctx=SimpleNamespace(store=False, conversation_id=str(uuid4()), request_id=str(uuid4())),
        iteration=1,
        api_response=None,
        request_payload={"messages": []},
        unified_payload=None,
        trigger_position=0,
        first_assistant_position=1,
        state_snapshot=ExecutionState().snapshot(),
        error_payload={"outcome": "error"},
        provider="openai",
        model="gpt-test",
    )
    assert fake_model.created == []


@pytest.mark.asyncio
async def test_out_of_lane_client_host_skips_direct_insert(monkeypatch):
    fake_model = _without_lane(monkeypatch)
    monkeypatch.setattr(
        "matrx_ai.client_host.get_conversation_store", lambda: object()
    )
    await executor_mod._write_request_snapshot(
        exec_ctx=SimpleNamespace(store=True, conversation_id=str(uuid4()), request_id=str(uuid4())),
        iteration=1,
        api_response=None,
        request_payload={"messages": []},
        unified_payload=None,
        trigger_position=0,
        first_assistant_position=1,
        state_snapshot=ExecutionState().snapshot(),
        error_payload={"outcome": "error"},
        provider="openai",
        model="gpt-test",
    )
    assert fake_model.created == [], (
        "a CLIENT host cannot reach chat.request_snapshot — the fallback must not fire there"
    )


@pytest.mark.asyncio
async def test_provider_resolves_from_the_catalog_when_nothing_stamped_it(monkeypatch):
    async def _vendor(model: str) -> str:
        assert model == "some-model"
        return "together"

    monkeypatch.setattr(executor_mod, "_catalog_vendor_for_model", _vendor)
    api_response = SimpleNamespace(
        metadata={"matrx_model_name": "some-model"}, to_dict=lambda: {"ok": True}
    )
    queued = await _capture_queued(monkeypatch, api_response=api_response)
    assert queued[0]["provider"] == "together"
