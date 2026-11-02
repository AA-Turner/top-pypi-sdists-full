"""``flow.sleep`` + ``flow.wait_until`` — durable timers (the Temporal way).

A long sleep must NOT be an ``asyncio.sleep`` holding a worker slot: the run
PARKS (GraphInterrupt → INTERRUPTED checkpoint, exactly like Pause & Ask) and
a wake job is enqueued on the durable ``workflow.job`` queue with
``visible_at = wake_at`` (``matrx_graph.workers.sleep_wake``, called from the
one ``RunStore.apply_result`` funnel every execution lane already uses). The
job row is Postgres truth, so a worker restart mid-sleep loses nothing and the
claim fencing + ``claim_for_resume`` CAS guarantee the wake fires once — the
same chaos-tested machinery every queued run rides.

Short sleeps (≤ ``INLINE_SLEEP_CEILING_SECONDS``) run inline instead: a park +
checkpoint + queue round-trip costs more than the wait itself. Crash-safety is
unchanged — a worker that dies mid-inline-sleep re-runs the step from the last
checkpoint and simply re-waits; it can never lose or double the payload.

The interrupt payload carries:

* ``SLEEP_MARKER`` (``matrx_sleep``) — ``{"wake_at": iso, "duration_seconds",
  "node_id"}``. This marker is what ``schedule_sleep_wake`` keys on; it is the
  durable contract between the node and the wake scheduler.
* ``resume_output`` — the node's exact input payload. The wake job passes it
  as ``resume_value``, so the engine records it as this node's output and the
  payload flows downstream unchanged (pass-through posture).
* ``prompt`` — so the studio's ordinary interrupt UI shows what the run is
  waiting for, and "resume now" doubles as wake-early for free.
"""

from __future__ import annotations

import asyncio
from datetime import UTC, datetime, timedelta
from typing import ClassVar

from pydantic import BaseModel, ConfigDict, Field

from matrx_graph.nodes._template import render_template_string
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success

#: The interrupt-payload key that marks "this park is a timer, wake me".
#: Read by ``matrx_graph.workers.sleep_wake.schedule_sleep_wake``.
SLEEP_MARKER = "matrx_sleep"

#: In the sleep marker: ``True`` means a wake RE-RUNS the parked step instead of
#: recording ``resume_output`` as its output. A polling node (re-count, re-check)
#: parks with it so EVERY way the park ends — the timed wake, "resume now", the
#: recovery sweep's resume of an orphaned leg — asks the world again; a stale
#: value from park time is never taken as the answer. The node then either
#: returns (the run moves on) or parks again with a fresh marker and wake.
RE_EXECUTE_ON_WAKE = "re_execute"


def re_executes_on_wake(interrupt_payload: object) -> bool:
    """True when a park asked to be re-run on wake (either interrupt shape:
    the run-row ``{"node_id", "payload"}`` envelope or the bare node payload)."""
    if not isinstance(interrupt_payload, dict):
        return False
    inner = interrupt_payload.get("payload")
    payload = inner if isinstance(inner, dict) else interrupt_payload
    marker = payload.get(SLEEP_MARKER)
    return isinstance(marker, dict) and marker.get(RE_EXECUTE_ON_WAKE) is True


#: At or below this many seconds the node waits inline instead of parking —
#: a checkpoint + queue round-trip (~1s worker poll) is worse than just
#: waiting. Crash-safe either way (step replay re-waits).
INLINE_SLEEP_CEILING_SECONDS = 30.0

#: Schema ceiling on one sleep: 90 days. Max-duration POLICY (should this be
#: an admin knob? per-plan?) is an open Arman decision recorded in
#: KINDS_EVERYWHERE_PLAN §10b — this bound just keeps a typo from parking a
#: run for a millennium.
MAX_SLEEP_SECONDS = 90 * 24 * 3600


class _PassThroughInput(BaseModel):
    """Whatever flows in, flows out — the payload is not this node's business."""

    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "x-contract-dynamic": "pass-through pacing node; the payload flows unchanged"
        },
    )


class _PassThroughOutput(BaseModel):
    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "x-contract-dynamic": "pass-through pacing node; the payload flows unchanged"
        },
    )


class SleepConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    duration_seconds: float = Field(
        gt=0,
        le=MAX_SLEEP_SECONDS,
        description=(
            "How long to wait before continuing. Short waits happen in place; "
            "longer ones park the run durably and wake it on time even across "
            "server restarts."
        ),
    )


def _interrupt_for_wake(
    ctx: NodeExecutionContext,
    inputs: BaseModel,
    wake_at: datetime,
    duration_seconds: float,
) -> None:
    payload = inputs.model_dump(mode="json")
    ctx.interrupt(
        {
            "prompt": (
                f"Waiting until {wake_at.isoformat(timespec='seconds')} — "
                "resume now to skip the remaining wait."
            ),
            SLEEP_MARKER: {
                "wake_at": wake_at.isoformat(),
                "duration_seconds": duration_seconds,
                "node_id": ctx.node_id,
            },
            "resume_output": payload,
        }
    )


class SleepExecutor:
    """Durable relative delay. Parks the run; the wake job is Postgres truth."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="flow.sleep",
        category=NodeCategory.CONTROL,
        display_name="Wait",
        description=(
            "Pause here for a set amount of time, then continue automatically. "
            "Survives restarts — the wake-up is stored, not held in memory."
        ),
        input_schema=_PassThroughInput,
        output_schema=_PassThroughOutput,
        config_schema=SleepConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT, required=False),
        ),
        # PASS-THROUGH BY DESIGN — the payload flows through unchanged (see
        # module docstring). Declared dynamic (GAP 2, KINDS_EVERYWHERE_PLAN
        # §10g) so runtime __kind propagation is the recorded posture rather
        # than an undeclared NULL.
        dynamic_output=True,
        determinism=ActionTier.NON_DETERMINISTIC,
        can_interrupt=True,
        icon="clock",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: _PassThroughInput,
        config: SleepConfig,
    ) -> NodeResult[_PassThroughOutput]:
        duration = float(config.duration_seconds)
        if duration <= INLINE_SLEEP_CEILING_SECONDS:
            await asyncio.sleep(duration)
            return success(_PassThroughOutput(**inputs.model_dump(mode="json")))
        wake_at = datetime.now(UTC) + timedelta(seconds=duration)
        _interrupt_for_wake(ctx, inputs, wake_at, duration)
        raise AssertionError("unreachable — ctx.interrupt() raises")


class WaitUntilConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    timestamp: str = Field(
        min_length=1,
        description=(
            "Absolute moment to continue at, ISO-8601 (e.g. "
            "'2026-09-01T09:00:00Z'). '{dot.path}' placeholders interpolate "
            "values from this node's inputs, so an upstream step can supply "
            "the moment. A time already in the past continues immediately."
        ),
    )


def _parse_timestamp(raw: str) -> datetime | None:
    text = raw.strip()
    if text.endswith(("Z", "z")):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None
    return parsed if parsed.tzinfo else parsed.replace(tzinfo=UTC)


class WaitUntilExecutor:
    """Durable absolute-time gate — same wake machinery as ``flow.sleep``."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="flow.wait_until",
        category=NodeCategory.CONTROL,
        display_name="Wait Until",
        description=(
            "Pause here until a specific date and time, then continue "
            "automatically. Survives restarts."
        ),
        input_schema=_PassThroughInput,
        output_schema=_PassThroughOutput,
        config_schema=WaitUntilConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT, required=False),
        ),
        # PASS-THROUGH BY DESIGN — the payload flows through unchanged (see
        # module docstring). Declared dynamic (GAP 2, KINDS_EVERYWHERE_PLAN
        # §10g) so runtime __kind propagation is the recorded posture rather
        # than an undeclared NULL.
        dynamic_output=True,
        determinism=ActionTier.NON_DETERMINISTIC,
        can_interrupt=True,
        icon="calendar-clock",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: _PassThroughInput,
        config: WaitUntilConfig,
    ) -> NodeResult[_PassThroughOutput]:
        namespace = inputs.model_dump(mode="json")
        rendered, _ = render_template_string(config.timestamp, namespace, whole_key="inputs")
        wake_at = _parse_timestamp(rendered)
        if wake_at is None:
            return failure(
                "invalid_timestamp",
                f"'{rendered}' is not an ISO-8601 timestamp (e.g. 2026-09-01T09:00:00Z).",
            )
        remaining = (wake_at - datetime.now(UTC)).total_seconds()
        if remaining <= 0:
            return success(_PassThroughOutput(**namespace))
        if remaining <= INLINE_SLEEP_CEILING_SECONDS:
            await asyncio.sleep(remaining)
            return success(_PassThroughOutput(**namespace))
        if remaining > MAX_SLEEP_SECONDS:
            return failure(
                "wait_too_long",
                f"'{rendered}' is more than 90 days away — this gate refuses "
                "to park a run that far out (open policy question; see "
                "flow.sleep's ceiling).",
            )
        _interrupt_for_wake(ctx, inputs, wake_at, remaining)
        raise AssertionError("unreachable — ctx.interrupt() raises")
