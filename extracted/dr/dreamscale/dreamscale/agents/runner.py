"""The same local decision loop runs every qualified robot adapter."""

import asyncio
import time
from typing import Protocol
from uuid import uuid4

from dreamscale_transport.llm import (
    MAX_CALLS,
    MAX_SECONDS,
    Observation,
    RobotProfile,
    ToolCall,
    ToolReceipt,
    TurnRequest,
)

from .display import AgentDisplay, action_lines, clean
from .journal import Journal


class ExecutionInterrupted(asyncio.CancelledError):
    """Cancellation carrying the adapter's best known physical execution receipt."""

    def __init__(self, receipt: ToolReceipt):
        super().__init__("Robot execution interrupted")
        self.receipt = receipt


class RobotAdapter(Protocol):
    def describe(self) -> RobotProfile: ...
    async def observe(self) -> Observation: ...
    async def execute(self, call: ToolCall) -> ToolReceipt: ...
    async def stop(self) -> None: ...
    async def close(self) -> None: ...


async def run(adapter: RobotAdapter, gateway, sid, journal_path, *, print_fn=print):
    journal = None
    receipt = None
    executing = None
    interrupted_receipt = None
    total_credits = None
    started = time.monotonic()
    display = AgentDisplay(print_fn=print_fn)
    emit = display.info

    try:
        journal = Journal(journal_path)
        profile = adapter.describe()
        async with asyncio.timeout(MAX_SECONDS):
            for index in range(MAX_CALLS):
                observation = await adapter.observe()
                turn = TurnRequest(id=str(uuid4()), observation=observation, receipt=receipt)
                with display.thinking(index + 1):
                    result = await gateway.turn(sid, turn)
                total_credits = result.total_credits
                # Cancellation is checked again even if an HTTP callback suppressed it.
                if asyncio.current_task().cancelling() or time.monotonic() - started >= MAX_SECONDS:
                    raise asyncio.CancelledError
                if result.id != turn.id:
                    raise RuntimeError("Decision does not match the submitted observation.")
                if result.outcome or result.status != "completed":
                    label = (
                        "Model reports completion"
                        if result.outcome == "model_reports_completion"
                        else f"Stopped: {result.outcome or result.status}"
                    )
                    emit(f"{label}.")
                    display.summary(result.message)
                    return result
                if len(result.calls) != 1 or result.calls[0].name not in {
                    t.name for t in profile.tools
                }:
                    raise RuntimeError("Invalid robot tool decision.")
                call = result.calls[0]
                journal.begin(call.id, call=call)
                executing = call
                display.summary(result.message)
                for line in action_lines(adapter, call, observation):
                    display.motion(line)
                receipt = await adapter.execute(call)
                if receipt.call_id != call.id:
                    raise RuntimeError("Execution receipt does not match the motion identity.")
                journal.finish(receipt)
                executing = None
                if receipt.status == "rejected":
                    display.warning(f"Rejected: {clean(receipt.detail)}")
                elif receipt.status == "completed" and receipt.measured.get("arrived") is False:
                    display.warning("Arrival not confirmed by measured feedback.")
                if receipt.status in {"partial", "unknown"}:
                    display.warning(
                        "Stopped: physical execution is uncertain; start a fresh attended run."
                    )
                    return receipt
            emit("Stopped: provider call limit reached.")
    except ExecutionInterrupted as exc:
        interrupted_receipt = exc.receipt
        raise
    finally:
        # Hardware stop precedes all network/disk cleanup, including on camera loss.
        try:
            await adapter.stop()
        finally:
            try:
                if executing is not None and journal is not None:
                    journal.finish(
                        interrupted_receipt
                        or ToolReceipt(
                            call_id=executing.id,
                            status="unknown",
                            requested=executing.arguments,
                            detail=(
                                "Execution interrupted; physical outcome is uncertain. "
                                "Never replay."
                            ),
                        )
                    )
            finally:
                try:
                    async with asyncio.timeout(10):
                        await gateway.close(sid)
                finally:
                    try:
                        await adapter.close()
                    finally:
                        if journal:
                            journal.close()
                        if total_credits is not None:
                            emit(f"Usage: {total_credits} credits")
                        display.close()
                        emit("Stopped")
