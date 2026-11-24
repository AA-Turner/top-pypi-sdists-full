"""The runtime meter backstop: an unmetered paid send is FILED (and still sent); a metered one is not (P8-RUNS).

Drives the real seam (``UnifiedAIClient._dispatch_with_billing_net``) and the batch lane's live send with a fake
dispatch / client — nothing reaches a provider.
"""

from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

from matrx_ai.providers import meter_scope
from matrx_ai.providers.unified_client import UnifiedAIClient


@pytest.fixture
def filed():
    records: list[meter_scope.UnmeteredProviderCall] = []
    meter_scope.reset_for_tests()
    meter_scope.configure_meter_probe(None)
    meter_scope.configure_run_meter_probe(None)
    meter_scope.configure_unmetered_call_sink(records.append)
    yield records
    meter_scope.configure_unmetered_call_sink(None)
    meter_scope.configure_meter_probe(None)
    meter_scope.configure_run_meter_probe(None)
    meter_scope.reset_for_tests()


_PROFILE = SimpleNamespace(vendor="openai", model_name="gpt-backstop-test", route_kind=None, offering_id=None)


async def _send() -> object:
    sent: list[bool] = []

    async def dispatch():
        sent.append(True)
        return SimpleNamespace(usage=None)

    result = await UnifiedAIClient._dispatch_with_billing_net(dispatch, profile=_PROFILE, firewall_checked=True)
    assert sent == [True], "the backstop must never block the send"
    return result


def test_an_unmetered_send_is_sent_and_filed(filed) -> None:
    asyncio.run(_send())
    assert len(filed) == 1, filed
    call = filed[0]
    assert (call.entry, call.provider, call.model) == ("unified_client.dispatch", "openai", "gpt-backstop-test")
    assert "test_meter_backstop" in call.caller, call.caller  # the first frame outside the provider layer


def test_a_send_inside_a_direct_spend_scope_is_not_filed(filed) -> None:
    async def run():
        with meter_scope.direct_spend_scope("backstop_test"):
            await _send()

    asyncio.run(run())
    assert filed == []


def test_a_send_inside_a_runtime_execution_is_not_filed(filed) -> None:
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

    async def run():
        token = set_app_context(AppContext(emitter=None, metadata={"runtime_execution_id": "00000000-0000-0000-0000-000000000001"}))
        try:
            await _send()
        finally:
            clear_app_context(token)

    asyncio.run(run())
    assert filed == []


def test_the_host_probe_opens_a_meter(filed) -> None:
    meter_scope.configure_meter_probe(lambda: "spend-scope-1")
    asyncio.run(_send())
    assert filed == []


def test_a_failed_unmetered_send_is_filed_too(filed) -> None:
    async def run():
        async def dispatch():
            raise RuntimeError("provider down")

        with pytest.raises(RuntimeError):
            await UnifiedAIClient._dispatch_with_billing_net(dispatch, profile=_PROFILE, firewall_checked=True)

    asyncio.run(run())
    assert len(filed) == 1 and filed[0].cost_usd is None


def test_the_batch_live_send_is_filed_when_unmetered(filed) -> None:
    from matrx_ai.providers import batch_live

    class _Messages:
        async def create(self, **payload):
            return {"ok": True}

    client = SimpleNamespace(messages=_Messages())
    out = asyncio.run(batch_live.send_live("anthropic", "messages", {"model": "claude-x"}, client=client))
    assert out == {"ok": True}
    assert [(c.entry, c.provider, c.model) for c in filed] == [("batch_live.send_live:messages", "anthropic", "claude-x")]


# --- P8-RUNS cost adversary pass 3 (2026-11-17): the backstop never hides money ---------------------------------


def test_every_repeat_reaches_the_sink_with_the_running_total(filed) -> None:
    """probe_backstop.py: five calls costing $62.75 filed ONE record of $0.50 (repeats never counted). Every repeat
    now reaches the sink as the same finding, carrying the running count and total."""
    for cost in (0.50, 3.00, 7.25, 12.0, 40.0):
        meter_scope.check_send("unified_client.dispatch", provider="openai", model="gpt-image").settle(cost)
    assert [(r.cost_usd, r.repeats) for r in filed] == [(0.5, 1), (3.0, 2), (7.25, 3), (12.0, 4), (40.0, 5)]
    assert filed[-1].total_cost_usd == pytest.approx(62.75)
    assert len({r.finding for r in filed}) == 1 and filed[0].finding


def test_an_unpriced_repeat_is_counted_apart_from_the_total(filed) -> None:
    for cost in (1.0, None, 2.0):
        meter_scope.check_send("unified_client.dispatch", provider="openai", model="m").settle(cost)
    last = filed[-1]
    assert (last.repeats, last.unpriced_repeats, last.total_cost_usd) == (3, 1, pytest.approx(3.0))


def _in_run(coro_fn):
    from matrx_connect.context.app_context import AppContext, clear_app_context, set_app_context

    async def run():
        token = set_app_context(AppContext(emitter=None, metadata={"runtime_execution_id": "00000000-0000-0000-0000-000000000001"}))
        try:
            await coro_fn()
        finally:
            clear_app_context(token)

    asyncio.run(run())


def test_a_run_id_no_recorder_banks_is_not_a_meter(filed) -> None:
    """An agent-as-tool child carried the root's run id while nothing recorded its tools' calls: the backstop read
    "run open" and filed nothing. With the host's run probe wired, a run id alone opens no meter."""
    meter_scope.configure_run_meter_probe(lambda _md: None)
    _in_run(_send)
    assert len(filed) == 1


def test_a_run_the_host_banks_on_is_a_meter(filed) -> None:
    meter_scope.configure_run_meter_probe(lambda md: "child-exec-1")
    _in_run(_send)
    assert filed == []


def test_the_dispatch_prices_the_call_once_and_files_its_amount(filed, monkeypatch) -> None:
    """The backstop's filing read cost from the RAW usage (a second catalog ask): a counters-only usage (STT, media,
    decisions) priced only through the dispatched route filed no amount. The seam now prices ONCE, through the route
    (``note_paid_result``), and the filing reuses that price."""
    import matrx_ai.providers.unified_client as uc
    from matrx_ai.providers import guardrail_gate

    for hook in ("_accrue", "_every_call_accrue", "_every_call_usage", "_every_call_unpriced"):
        monkeypatch.setattr(guardrail_gate, hook, None, raising=False)
    asked: list[object] = []

    async def catalog(usage):
        asked.append(usage)
        return 1.25 if getattr(usage, "matrx_model_name", None) == "gpt-backstop-test" else None

    monkeypatch.setattr(uc, "catalog_cost_or_none", catalog)

    async def run():
        async def dispatch():
            return SimpleNamespace(usage=SimpleNamespace(input_tokens=10, output_tokens=3))

        await UnifiedAIClient._dispatch_with_billing_net(dispatch, profile=_PROFILE, firewall_checked=True)

    asyncio.run(run())
    assert len(asked) == 1, f"the catalog was asked {len(asked)} times for one call"
    assert [(r.cost_usd, r.repeats) for r in filed] == [(1.25, 1)]


def test_a_pass_through_in_processing_never_hides_the_real_caller(filed) -> None:
    """cd62a240: findings named ``processing.audio.stt:execute_stt`` instead of the code that asked for the send."""
    from matrx_ai.providers.meter_scope import _LAYER_MARKERS

    assert "/matrx_ai/processing/" in _LAYER_MARKERS
