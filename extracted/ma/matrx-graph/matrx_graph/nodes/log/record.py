"""``log.record`` — the workflow's own diagnostic record.

ARMAN, 2026-08-23, on the Agent Foundry failure that produced this node:

    "we need to trigger some sort of node that is going to write to a
     persistent place and render a very loud error… we need to give users a
     way to be able to track their own internal logs and problems… a place
     where you can pass it whatever thing you want, and then it will write to
     the database in a table that can later be used to diagnose problems that
     happened within a workflow that you were able to work around, but should
     never have happened."

Nothing on the platform could do this. A workflow that hit a serious problem
and recovered from it had exactly two options — fail the whole run, or say
nothing at all. The Foundry took the second: both Component Artisans refused
to build a component, each for a correct and well-argued reason, and the run
reported `completed` with no component and no trace of why. The diagnosis was
sitting in an agent's prose and nothing was ever going to read it.

WHY THIS IS NOT `system_error`
------------------------------
Workflows are authored by USERS. A node that wrote into the platform's own
error queue would let any author inject rows into our operational alarm
surface — noise at best, a channel for abuse at worst. `workflow.run_log` is
the user's own diagnostic table: org-scoped, readable by the run's owner
(`ledger` RLS variant), written only by the server. Genuine PLATFORM defects
still go to `system_error` through the server's own paths; this is for
"something happened inside MY workflow that shouldn't have."

WHAT MAKES IT USEFUL RATHER THAN A SHRUG
----------------------------------------
* **`label` is a stable key, `message` is the sentence.** Grouping "this
  happened 40 times" needs a key that does not embed a run id or a timestamp;
  explaining it to a human needs a sentence. Asking one field to be both gives
  a table you cannot query and prose you cannot read.
* **`payload` takes whatever you have** — and `payload_kind` records what that
  was, when it is a registered kind. A diagnostic that throws away the
  evidence is a log line, not a record.
* **The node never fails the run.** It exists for the case where the workflow
  DID work around the problem. A recorder that can break the run it is
  reporting on would make authors stop reaching for it, which is the only way
  this node can truly fail.
* **It returns a typed receipt** (`run_log_entry`), not prose — so a
  downstream step can branch on `recorded` and the run can prove it told
  somebody.
"""

from __future__ import annotations

import logging
from typing import Any, ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from matrx_graph.types.usl import field_extras

from matrx_graph.run_log import SEVERITIES, RunLogEntry, write_run_log

log = logging.getLogger(__name__)

Severity = Literal["debug", "info", "warning", "error", "critical"]
Category = Literal[
    "recovered_error", "retry", "rework", "fallback", "validation_failed",
    "unexpected_path", "extra_cost", "degraded_output", "skipped_item",
    "human_handoff", "stall_recovery", "other",
]

__all__ = ["SEVERITIES", "RecordIssueExecutor", "RunLogEntry"]


class RecordIssueInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # Optional at run time: the step's configured label (config.label) is the
    # fallback, so a step that sets its label in config never fails validation
    # for leaving the input blank (Agent Foundry record_no_component, 3b90681b).
    label: str = Field(
        default="",
        max_length=200,
        description=(
            "A short, STABLE name for this problem — the same words every time "
            "it happens (e.g. 'component_not_written'). This is what lets you "
            "ask 'how often does this happen?' later."
        ),
        json_schema_extra=field_extras(widget="text", placeholder="component_not_written"),
    )
    message: str = Field(
        default="",
        description=(
            "What happened, in a sentence a person can read. Defaults to the "
            "label when you have nothing more to say."
        ),
        json_schema_extra=field_extras(widget="textarea", multiline_rows=2),
    )
    # NULLABLE ON PURPOSE. A non-null default here is indistinguishable from
    # the author choosing "warning", so `inputs.severity or config.severity`
    # made the step's own configured severity unreachable — caught on the
    # first live run, which recorded a 'warning' for a step configured
    # 'error'. Absence must be representable wherever a config can override.
    severity: Severity | None = Field(
        default=None,
        description=(
            "How bad it is. 'warning' = the workflow carried on but something "
            "was wrong; 'error'/'critical' = the result is compromised even "
            "though the run continued. Falls back to the step's configured "
            "severity."
        ),
        json_schema_extra=field_extras(widget="select"),
    )
    payload: JsonValue = Field(
        default=None,
        description=(
            "Anything you want kept as evidence — the agent's own answer, the "
            "value that failed, the step's inputs. Stored verbatim."
        ),
        json_schema_extra=field_extras(widget="json"),
    )
    payload_kind: str | None = Field(
        default=None,
        description=(
            "The registered Shape of the evidence, when it has one — so the "
            "record renders through that Shape's component later instead of a "
            "key/value dump."
        ),
    )


class RecordIssueConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    label: str = Field(
        default="",
        description=(
            "Author-time label, used when the step is not given one at run "
            "time. The input wins when both are present."
        ),
        json_schema_extra=field_extras(widget="text"),
    )
    severity: Severity = Field(
        default="warning",
        json_schema_extra=field_extras(widget="select"),
    )
    needs_review: bool = Field(
        default=True,
        description=(
            "Flag the workflow for review each time this records — the run still "
            "succeeds, but the problem is grouped into one issue the owner is told about."
        ),
        json_schema_extra=field_extras(widget="toggle"),
    )
    category: Category = Field(
        default="other",
        description="Why it is worth reviewing: a recovered error, a redo, a fallback, extra work…",
        json_schema_extra=field_extras(widget="select"),
    )


class RecordIssueExecutor:
    """Write one diagnostic row. Never fails the run."""

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="log.record",
        category=NodeCategory.DATA,
        display_name="Record a Problem",
        description=(
            "Write down something that went wrong, with whatever evidence you "
            "have, so you can find it later. The workflow keeps going."
        ),
        input_schema=RecordIssueInput,
        output_schema=RunLogEntry,
        config_schema=RecordIssueConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT, required=False),
        ),
        determinism=ActionTier.SIDE_EFFECT,
        icon="clipboard-alert",
        output_kind="run_log_entry",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: RecordIssueInput,
        config: RecordIssueConfig,
    ) -> NodeResult[RunLogEntry]:
        # THE ONE WRITER (matrx_graph.run_log) — shared with ctx.warn; the per-run
        # cap is counted from durable rows there, never from process memory.
        return success(
            await write_run_log(
                run_id=ctx.run_id,
                node_id=ctx.node_id,
                step=ctx.step,
                attempt=ctx.attempt,
                label=inputs.label or config.label or "unlabeled",
                message=inputs.message,
                severity=inputs.severity or config.severity or "warning",
                payload=inputs.payload,
                payload_kind=inputs.payload_kind,
                organization_id=ctx.organization_id,
                user_id=str(ctx.user_id) if ctx.user_id else None,
                needs_review=config.needs_review,
                category=config.category,
                source="record_step",
            )
        )
