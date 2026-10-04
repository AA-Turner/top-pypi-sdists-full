"""The usage gate: the paid-call seam answers from MEMORY, before money is spent.

SUT: ``UnifiedAIClient._dispatch_with_billing_net`` — the one seam every paid
provider call passes — and the gate it calls,
``matrx_ai.providers.usage_gate.admit_paid_call`` (plus the request-boundary
twin ``precheck_usage`` inside ``conversation_gate.ensure_user_request_exists``).

Doubles: the host's verdict resolver (a plain dict lookup — the shape of the
host's process memory, and a call counter so a test can prove what was asked),
an emitter that records ``info`` events, and the provider dispatch itself (a
coroutine that records that it ran — the stand-in for "money was spent").

Breaks named (USAGE-GATE.md):
* a cached-over person reaches the provider (money spent after the limit);
* a cache miss refuses, waits or fetches instead of being honored;
* over with enforcement OFF refuses;
* near proceeds silently (the client is never told);
* a request that crossed the line mid-run is cut off at its next paid call;
* machine work (system/scheduled) pays out of a person's allowance;
* the refusal's code or numbers drift from the envelope the client parses;
* an over person's new turn is stored before being refused.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace
from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context
from matrx_connect.emitters.silent_emitter import SilentEmitter

from matrx_ai.providers import usage_gate as gate
from matrx_ai.providers.unified_client import UnifiedAIClient

USER = "0f0e0d0c-0b0a-4908-8706-050403020100"
GUEST = "6b1f6f8e-2d0c-4a55-9b7e-1c2d3e4f5a6b"
PROFILE = SimpleNamespace(
    vendor="openai",
    model_name="gpt-test",
    endpoint_id="openai-test",
    base_url=None,
    offering_metadata={},
)


def _usage(state: str, plan: str = "free") -> dict[str, Any]:
    return {
        "scope": "user",
        "subject_id": USER,
        "plan_key": plan,
        "plan_name": plan.title(),
        "required_tier": "personal-entry" if plan == "free" else "free",
        "state": state,
        "near_ratio": 0.8,
        "binding_period": "week",
        "resets_at": "2026-10-05T00:00:00+00:00",
        "windows": [
            {"period": "week", "limit": 7500, "used": 7600 if state == "over" else 6500,
             "remaining": 0, "resets_at": "2026-10-05T00:00:00+00:00", "state": state},
        ],
        "computed_at": "2026-10-04T01:50:14+00:00",
    }


class _Memory:
    """The host's process memory: user_id -> verdict, and who was asked."""

    def __init__(self) -> None:
        self.verdicts: dict[str, gate.UsageVerdict] = {}
        self.asked: list[str] = []

    def put(self, user_id: str, state: str, *, enforced: bool, plan: str = "free") -> None:
        self.verdicts[user_id] = gate.UsageVerdict(
            state=state,  # type: ignore[arg-type]
            refuse=(state == "over" and enforced),
            enforced=enforced,
            usage=_usage(state, plan),
        )

    def __call__(self, user_id: str) -> gate.UsageVerdict | None:
        self.asked.append(user_id)
        return self.verdicts.get(user_id)


class _Recording(SilentEmitter):
    def __init__(self) -> None:
        super().__init__()
        self.infos: list[Any] = []

    async def send_info(self, payload: Any) -> None:  # type: ignore[override]
        self.infos.append(payload)


@pytest.fixture
def memory() -> _Memory:
    mem = _Memory()
    gate.set_usage_verdict_resolver(mem)
    gate.reset_usage_gate_state()
    yield mem
    gate.set_usage_verdict_resolver(None)
    gate.reset_usage_gate_state()


def _rid(n: int) -> str:
    return f"00000000-0000-4000-8000-{n:012d}"


def _ctx(request_id: str, *, user_id: str = USER, emitter: Any = None, **kw: Any) -> AppContext:
    return AppContext(
        emitter=emitter or SilentEmitter(),
        user_id=user_id,
        auth_type="token",
        is_authenticated=True,
        request_id=request_id,
        **kw,
    )


async def _paid_call(ctx: AppContext, spent: list[str]) -> Any:
    token = set_app_context(ctx)
    try:

        async def _provider() -> str:
            spent.append(ctx.request_id)
            return "ok"

        return await UnifiedAIClient._dispatch_with_billing_net(_provider, profile=PROFILE)
    finally:
        clear_app_context(token)


async def _refused(ctx: AppContext, spent: list[str]) -> BaseException | None:
    try:
        await _paid_call(ctx, spent)
    except BaseException as exc:  # noqa: BLE001
        return exc
    return None


def test_cached_over_and_enforced_is_refused_before_the_provider(memory: _Memory) -> None:
    memory.put(USER, "over", enforced=True)
    spent: list[str] = []
    refused = asyncio.run(_refused(_ctx(_rid(1)), spent))
    assert isinstance(refused, gate.UsageLimitReachedError)
    assert spent == [], "a cached-over person reached the provider"
    env = refused.envelope()
    assert env["error"] == "usage_limit_reached"
    assert env["fix_action"] == "upgrade_plan"
    assert env["required_tier"] == "personal-entry"
    assert (env["plan_key"], env["state"], env["binding_period"]) == ("free", "over", "week")
    assert (env["limit"], env["used"]) == (7500, 7600)
    assert env["resets_at"] == "2026-10-05T00:00:00+00:00"
    assert env["usage"] == _usage("over")
    # The stream contract: executor + stream crash handler read error_info.
    assert refused.error_info.error_type == "usage_limit_reached"
    assert refused.error_info.status_code == 402
    assert refused.error_info.is_retryable is False
    assert refused.error_info.details["required_tier"] == "personal-entry"
    assert refused.is_caller_refusal is True


def test_a_guest_keeps_the_sign_up_reminder_code(memory: _Memory) -> None:
    memory.put(GUEST, "over", enforced=True, plan="guest")
    ctx = AppContext(
        emitter=SilentEmitter(), user_id=GUEST, auth_type="fingerprint",
        is_authenticated=False, fingerprint_id="fp", request_id=_rid(2),
    )
    spent: list[str] = []
    refused = asyncio.run(_refused(ctx, spent))
    assert isinstance(refused, gate.UsageLimitReachedError)
    assert refused.envelope()["error"] == "guest_ai_allowance_used"
    assert refused.envelope()["required_tier"] == "free"
    assert spent == []


def test_cache_miss_is_honored_without_waiting(memory: _Memory) -> None:
    spent: list[str] = []
    assert asyncio.run(_paid_call(_ctx(_rid(3)), spent)) == "ok"
    assert spent == [_rid(3)]
    assert memory.asked == [USER], "the seam must ask memory, and only memory"


def test_over_but_not_enforced_proceeds_and_tells_the_client(memory: _Memory) -> None:
    memory.put(USER, "over", enforced=False)
    emitter = _Recording()
    spent: list[str] = []
    asyncio.run(_paid_call(_ctx(_rid(4), emitter=emitter), spent))
    assert spent == [_rid(4)]
    assert [i.code for i in emitter.infos] == ["usage_state"]
    assert emitter.infos[0].metadata == {"usage": _usage("over"), "enforced": False}


def test_near_proceeds_and_notifies_once_per_request(memory: _Memory) -> None:
    memory.put(USER, "near", enforced=True)
    emitter = _Recording()
    spent: list[str] = []

    async def _run() -> None:
        ctx = _ctx(_rid(5), emitter=emitter)
        for _ in range(3):  # tool-loop iterations of one request
            await _paid_call(ctx, spent)

    asyncio.run(_run())
    assert len(spent) == 3
    assert [i.code for i in emitter.infos] == ["usage_state"]
    assert emitter.infos[0].metadata["usage"]["state"] == "near"


def test_crossing_the_line_mid_request_never_stops_it(memory: _Memory) -> None:
    spent: list[str] = []

    async def _run() -> BaseException | None:
        ctx = _ctx(_rid(6))
        child = ctx.fork_for_child_agent(new_conversation_id="11111111-1111-4111-8111-111111111111")
        assert child.request_id == ctx.request_id
        await _paid_call(ctx, spent)  # admitted while ok
        memory.put(USER, "over", enforced=True)  # a settle mid-run flips the cache
        await asyncio.gather(_paid_call(ctx, spent), _paid_call(child, spent))
        return await _refused(_ctx(_rid(7)), spent)  # the NEXT request is stopped

    refused = asyncio.run(_run())
    assert spent == [_rid(6)] * 3, "the running request was cut off"
    assert isinstance(refused, gate.UsageLimitReachedError)


def test_a_resume_on_another_process_is_never_refused(memory: _Memory) -> None:
    """Rule 5 across processes: the memo is per process; a request paused for
    input resumes (same request id) on another task or after a restart. The
    resume path carries ``usage_admitted`` on the context; the gate honors it,
    at the paid call AND at the request boundary, and every fork inherits it."""
    spent: list[str] = []

    async def _run() -> BaseException | None:
        await _paid_call(_ctx(_rid(20)), spent)  # admitted while ok, process A
        gate.reset_usage_gate_state()  # the resume lands on process B
        memory.put(USER, "over", enforced=True)
        resumed = _ctx(_rid(20)).with_overrides(usage_admitted=True)
        child = resumed.fork_for_child_agent(new_conversation_id="22222222-2222-4222-8222-222222222222")
        await asyncio.gather(_paid_call(resumed, spent), _paid_call(child, spent))
        token = set_app_context(resumed)
        try:
            gate.precheck_usage()  # ensure_user_request_exists on the resume
        finally:
            clear_app_context(token)
        # Without the carried fact, process B re-judges it — the bug.
        return await _refused(_ctx(_rid(20)), spent)

    refused = asyncio.run(_run())
    assert spent == [_rid(20)] * 3, "a resumed request was refused on another process"
    assert isinstance(refused, gate.UsageLimitReachedError)


def test_an_internal_step_inherits_its_parents_admission(memory: _Memory) -> None:
    """One user operation = one admission: a step that mints its own request id
    (Knowledge Ask's answer step) inherits the parent's admission; a parent
    never admitted gives the step nothing to inherit, and it is judged."""
    spent: list[str] = []

    async def _run() -> tuple[bool, BaseException | None]:
        parent = _ctx(_rid(21))
        await _paid_call(parent, spent)  # retrieval, admitted
        memory.put(USER, "over", enforced=True)  # retrieval's settle flips the cache
        step = parent.with_overrides(request_id=_rid(22), usage_admitted=gate.admission_of(parent))
        await _paid_call(step, spent)
        fresh = _ctx(_rid(23))
        orphan = fresh.with_overrides(request_id=_rid(24), usage_admitted=gate.admission_of(fresh))
        return gate.admission_of(fresh), await _refused(orphan, spent)

    fresh_admitted, refused = asyncio.run(_run())
    assert spent == [_rid(21), _rid(22)], "the answer step was refused after retrieval was paid"
    assert fresh_admitted is False
    assert isinstance(refused, gate.UsageLimitReachedError)


def test_machine_work_is_not_gated(memory: _Memory) -> None:
    memory.put(USER, "over", enforced=True)
    spent: list[str] = []
    for n, origin in ((8, "system"), (9, "scheduled")):
        asyncio.run(_paid_call(_ctx(_rid(n), origin_class=origin), spent))
    assert spent == [_rid(8), _rid(9)]
    assert memory.asked == []


def test_no_resolver_means_nothing_is_gated() -> None:
    gate.set_usage_verdict_resolver(None)
    gate.reset_usage_gate_state()
    spent: list[str] = []
    asyncio.run(_paid_call(_ctx(_rid(10)), spent))
    assert spent == [_rid(10)]


def test_a_raising_resolver_honors_the_request(memory: _Memory) -> None:
    def _broken(_uid: str) -> None:
        raise RuntimeError("memory torn")

    gate.set_usage_verdict_resolver(_broken)
    spent: list[str] = []
    asyncio.run(_paid_call(_ctx(_rid(11)), spent))
    assert spent == [_rid(11)]


# --- the executor's stream path ----------------------------------------------


@pytest.mark.asyncio
async def test_executor_streams_the_refusal_code_and_files_no_incident(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from test_provider_out_of_credit_terminal import _run

    import matrx_ai.orchestrator.executor as executor_mod

    terminal: list[Any] = []

    async def _terminal(*a: Any, **k: Any) -> None:
        terminal.append((a, k))

    monkeypatch.setattr(executor_mod, "_capture_terminal_provider_failure", _terminal)
    run = await _run(monkeypatch, gate.UsageLimitReachedError(_usage("over")))

    assert run["client"].calls == 1, "a caller refusal was retried"
    assert len(run["errors"]) == 1, run["errors"]
    event = run["errors"][0]
    assert event["error_type"] == "usage_limit_reached"
    assert event["code"] == "usage_limit_reached"
    assert event["details"]["fix_action"] == "upgrade_plan"
    assert event["details"]["resets_at"] == "2026-10-05T00:00:00+00:00"
    assert event["user_message"] == gate.USAGE_LIMIT_MESSAGE
    assert terminal == [], "an expected refusal was filed as a provider failure"
    assert run["captured"] == [], "an expected refusal wrote a system_error"


# --- the request-boundary pre-check -------------------------------------------


def test_ensure_user_request_refuses_before_the_request_row_is_created(
    memory: _Memory, monkeypatch: pytest.MonkeyPatch
) -> None:
    from matrx_ai.db import conversation_gate

    memory.put(USER, "over", enforced=True)
    created: list[str] = []

    async def _create(*, request_id: str, user_id: str | None) -> None:
        created.append(request_id)

    async def _no_rows(**_: Any) -> list[Any]:
        return []

    async def _no_store(*_: Any) -> bool:
        return False

    monkeypatch.setattr(conversation_gate, "_store_pending_user_request", _no_store)
    monkeypatch.setattr(conversation_gate, "_create_user_request", _create)
    monkeypatch.setattr(
        conversation_gate,
        "_cxm",
        lambda: SimpleNamespace(user_request=SimpleNamespace(filter_user_requests=_no_rows)),
    )
    monkeypatch.setattr(conversation_gate, "_require_persistence_actor", lambda uid, _c: uid)

    async def _in(ctx: AppContext, rid: str) -> BaseException | None:
        token = set_app_context(ctx)
        try:
            await conversation_gate.ensure_user_request_exists(rid, USER)
        except BaseException as exc:  # noqa: BLE001
            return exc
        finally:
            clear_app_context(token)
        return None

    assert isinstance(asyncio.run(_in(_ctx(_rid(700)), _rid(700))), gate.UsageLimitReachedError)
    assert created == [], "the request row was created for a refused action"

    memory.put(USER, "near", enforced=True)
    assert asyncio.run(_in(_ctx(_rid(701)), _rid(701))) is None
    assert created == [_rid(701)]
