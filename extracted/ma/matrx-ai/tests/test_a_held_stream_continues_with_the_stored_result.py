"""THE HELD STREAM AT THE DISPATCH (RESUME-AND-RECOVERY section 1a): a saved run whose client keeps reading
waits in its stream for a client-run tool; a client that did not say so is parked exactly as before.

The wait itself (leases, races) is proven in ``test_a_held_call_is_taken_or_released_never_both.py``; here
the dispatch is: opt-in and knob gate the hold, the event says the stream stays open, a taken result is the
stored row's own model-facing content, and a given-up hold announces itself and parks.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from matrx_connect import AppContext
from matrx_connect.context.app_context import clear_app_context, set_app_context

from matrx_ai.db._conversation_rebuild_impl import _rebuild_tool_result_content
from matrx_ai.tools import delegated_hold as hold
from matrx_ai.tools.executor import ToolExecutor
from matrx_ai.tools.models import ToolContext, ToolDefinition

CONV = "11111111-1111-1111-1111-111111111111"


def _hooks(**over) -> hold.HoldHooks:
    base = dict(
        hold_ms=lambda _reason="client_tool": 20_000, poll_ms=lambda: 50, may_hold=lambda: True, lease_ms=lambda: 30_000,
        slow_poll_ms=lambda: 2000, fast_window_ms=lambda: 10_000, max_hold_ms=lambda _reason="client_tool": 55 * 60_000,
    )
    return hold.HoldHooks(**{**base, **over})


def _stored_row(*, is_error: bool = False) -> SimpleNamespace:
    return SimpleNamespace(
        id="tool-row", call_id="call-page", tool_name="get_page_text", tool_name_as_called="get_page_text",
        output="" if is_error else '{"text": "Example Domain"}', output_type="json", is_error=is_error,
        error_type="client_tool_error" if is_error else None,
        error_message="The tab was closed." if is_error else None,
        output_chars=0 if is_error else 26, output_preview=None, model_stub_at=None, metadata={},
        status="error" if is_error else "completed", held_until="lease",
    )


class _Run:
    """One delegated dispatch of a saved run, with the durable park and the wait doubled at their seams."""

    def __init__(self, monkeypatch: pytest.MonkeyPatch, *, reads: list[str], outcome: hold.HoldOutcome | None,
                 claimed: bool = True, hooks: hold.HoldHooks | None = None) -> None:
        self.events: list = []
        self.infos: list = []
        self.claims: list[str] = []
        self.waits: list[float] = []
        run = self

        class Emitter:
            async def send_tool_event(self, event):
                run.events.append(event)

            async def send_info(self, info):
                run.infos.append(info)

        class Logger:
            async def delegate_durably(self, row_id, **kwargs):
                return None

            def _desktop_target_instance_id(self):
                return None

        async def assistant(**kwargs):
            return [SimpleNamespace(role="assistant", status="active",
                                    content=[{"type": "tool_call", "call_id": "call-page"}])]

        async def claim(row_id, *, conversation_id, hold):
            run.claims.append(row_id)
            return claimed

        async def wait(row_id, *, conversation_id, call_id, hold, stop_reason=None):
            run.waits.append(hold.seconds)
            assert outcome is not None, "this dispatch must not wait"
            return outcome

        from matrx_ai.db import cxm

        monkeypatch.setattr(cxm.message, "filter_items", assistant)
        monkeypatch.setattr(hold, "_hooks", hooks if hooks is not None else _hooks())
        monkeypatch.setattr(hold, "claim", claim)
        monkeypatch.setattr(hold, "wait_for_result", wait)
        self.emitter = Emitter()
        self.logger = Logger()
        self.metadata = {"client_reads": reads} if reads else {}

    async def dispatch(self, tool: ToolDefinition | None = None):
        async def checkpoint():
            return "assistant-row"

        token = set_app_context(AppContext(emitter=self.emitter, store=True, metadata=self.metadata))
        try:
            executor = ToolExecutor(
                registry=SimpleNamespace(bindings_for_tool=lambda _name: []), execution_logger=self.logger
            )
            return await executor._execute_delegated(
                tool or ToolDefinition(name="get_page_text"), {"tab": 1},
                ToolContext(call_id="call-page", tool_name="get_page_text", conversation_id=CONV,
                            emitter=self.emitter, assistant_checkpoint=checkpoint),
                row_id="tool-row",
            )
        finally:
            clear_app_context(token)

    @property
    def delegated(self):
        return next(e for e in self.events if e.event == "tool_delegated")


@pytest.mark.asyncio
async def test_a_client_that_did_not_opt_in_is_parked_exactly_as_before(monkeypatch) -> None:
    run = _Run(monkeypatch, reads=["blocks-v1"], outcome=None)
    result = await run.dispatch()
    assert result.delegated_pending is True and result.client_resolved_content is None
    assert run.claims == [] and run.waits == []
    assert "hold" not in run.delegated.data
    assert run.delegated.data == {"arguments": {"tab": 1}}, "the event is byte-for-byte the old one"


@pytest.mark.asyncio
async def test_an_opted_in_client_gets_the_stored_result_in_the_same_stream(monkeypatch) -> None:
    row = _stored_row()
    run = _Run(monkeypatch, reads=[hold.HOLD_READ], outcome=hold.HoldOutcome(taken=True, row=row, waited_ms=412))
    result = await run.dispatch()
    assert run.claims == ["tool-row"] and run.waits == [20.0]
    assert "until" in run.delegated.data["hold"], "the client is told the stream stays open"
    assert result.delegated_pending is False and result.success is True
    assert result.client_resolved_content == _rebuild_tool_result_content([row])[0], (
        "the model sees exactly what a reload of the stored row gives"
    )
    done = run.events[-1]
    assert done.event == "tool_completed" and done.call_id == "call-page"
    assert done.data["held"] is True and done.data["waited_ms"] == 412
    assert run.infos == []


@pytest.mark.asyncio
async def test_a_client_failure_under_the_hold_reaches_the_model_as_the_stored_error(monkeypatch) -> None:
    row = _stored_row(is_error=True)
    run = _Run(monkeypatch, reads=[hold.HOLD_READ], outcome=hold.HoldOutcome(taken=True, row=row, waited_ms=90))
    result = await run.dispatch()
    assert result.success is False
    assert result.client_resolved_content["is_error"] is True
    assert "The tab was closed." in str(result.client_resolved_content["content"])
    assert run.events[-1].event == "tool_error" and run.events[-1].data["error_type"] == "client_tool_error"


@pytest.mark.asyncio
async def test_a_given_up_hold_says_so_and_parks(monkeypatch) -> None:
    run = _Run(monkeypatch, reads=[hold.HOLD_READ],
               outcome=hold.HoldOutcome(taken=False, reason="timeout", waited_ms=20_000))
    result = await run.dispatch()
    assert result.delegated_pending is True and result.client_resolved_content is None
    (info,) = run.infos
    assert info.code == "delegated_hold_released"
    assert info.metadata["reason"] == "timeout" and info.metadata["call_id"] == "call-page"


@pytest.mark.asyncio
async def test_a_hold_that_cannot_take_its_lease_is_not_announced(monkeypatch) -> None:
    run = _Run(monkeypatch, reads=[hold.HOLD_READ], outcome=None, claimed=False)
    result = await run.dispatch()
    assert result.delegated_pending is True
    assert "hold" not in run.delegated.data and run.waits == []


@pytest.mark.asyncio
@pytest.mark.parametrize("hooks", [_hooks(hold_ms=lambda _reason="client_tool": 0), _hooks(may_hold=lambda: False)])
async def test_the_knob_at_zero_or_a_draining_process_never_holds(monkeypatch, hooks) -> None:
    run = _Run(monkeypatch, reads=[hold.HOLD_READ], outcome=None, hooks=hooks)
    result = await run.dispatch()
    assert result.delegated_pending is True and run.claims == []


@pytest.mark.asyncio
async def test_a_tools_own_deadline_caps_the_hold(monkeypatch) -> None:
    run = _Run(monkeypatch, reads=[hold.HOLD_READ],
               outcome=hold.HoldOutcome(taken=False, reason="timeout", waited_ms=5000))
    await run.dispatch(ToolDefinition(name="get_page_text", max_client_wait_seconds=5))
    assert run.waits == [5.0]
