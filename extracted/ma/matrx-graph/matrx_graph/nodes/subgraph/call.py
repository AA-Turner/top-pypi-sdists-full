"""subgraph.call — embed another workflow as a child run.

Phase 4 scope: the executor declares the node shape + typed inputs/outputs.
The actual nested-run dispatch requires a DefinitionStore accessor passed via
host-app wiring (because matrx-graph itself doesn't depend on the Postgres
store). aidream provides the resolver via ``set_subgraph_resolver`` in
``aidream/api/routers/workflow.py`` at app startup.

Node Result System: a missing resolver or a failed child run is a node
``Failure`` (``no_subgraph_resolver`` / ``child_run_failed``) — the old
``success``/``error`` payload fields are gone. A child interrupt still
re-raises ``GraphInterrupt`` to the parent scheduler, marked ``forwards_answer``:
the parent parks carrying the child's question, and the person's answer to the
PARENT is handed back to this step (``ctx.resume_answer``) for the host to resume
the waiting child with — never recorded as this step's output.

CALL BY NAME, READ ONE TYPED RESULT (P4). A step names its child either by
``workflow_key`` — the stable name the child carries (its ``platform:<key>``
tag), run at its latest PUBLISHED version unless ``version_number`` pins one —
or by ``definition_id`` (the draft unless pinned). A child that declares its
result (``output_kind`` + the step marked as the result, the ``set_result``
patch op) answers with ``output`` / ``output_kind`` / ``result_step``; a child
that declares nothing still answers with ``last_outputs`` keyed by its step
ids. A child that declares ``input_kind`` refuses inputs that do not fit it
(``child_input_refused``) before any child run exists. The host resolves the
target through :func:`set_subgraph_target_resolver`; the same answer feeds
``result_version`` so a run-once step reuses only for the same child version.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, Field, JsonValue, field_validator, model_validator

from matrx_graph.errors import FORWARDS_ANSWER_KEY, ExecutionError, GraphInterrupt
from matrx_graph.failure import GATE_CAUSES, OUR_GATE_CAUSES
from matrx_graph.spend_gate import CALLER_REFUSAL_KEY
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success
from matrx_graph.types.usl import field_extras

SubgraphRunner = Callable[
    [NodeExecutionContext, "SubgraphCallConfig", "SubgraphCallInput"],
    Awaitable[dict[str, Any]],
]

_resolver: SubgraphRunner | None = None

#: A workflow's stable name is carried as the tag ``platform:<key>``.
PLATFORM_TAG_PREFIX = "platform:"


#: The Failure code of a step whose child run did not hand back an answer; it is also the step's cause.
CHILD_RUN_FAILED_CODE = "child_run_failed"


class SubgraphCallRefused(Exception):
    """A call the host refuses BEFORE any child run exists — unknown name, no
    access, inputs that do not fit the child's ``input_kind``, a result
    declaration the child's graph contradicts. ``code`` becomes the step's
    Failure code; ``message`` is the sentence a person reads."""

    def __init__(self, code: str, message: str, details: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.details = details or {}


class SubgraphChildFailed(ExecutionError):
    """A child run that ended without an answer, carrying the child's STRUCTURED failure.

    The host raises it with the child's ``RunFailure`` column dict (``cause``, ``message``,
    ``approval_url`` ...). When the child stopped on a gate (:data:`matrx_graph.failure.GATE_CAUSES`)
    the step's Failure code is that cause, so the caller's person reads the real remedy (Open
    Billing, the approval link); anything else is ``child_run_failed`` pointing at the child."""

    def __init__(self, message: str, *, child_run_id: str, failure: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.message = message
        self.child_run_id = child_run_id
        self.failure = dict(failure or {})

    @property
    def code(self) -> str:
        cause = self.failure.get("cause")
        return cause if isinstance(cause, str) and cause in GATE_CAUSES else CHILD_RUN_FAILED_CODE

    def details(self) -> dict[str, Any]:
        details: dict[str, Any] = {"error": self.message, "child_run_id": self.child_run_id}
        cause = self.failure.get("cause")
        if isinstance(cause, str) and cause:
            details["child_cause"] = cause
        if self.code in GATE_CAUSES and self.code not in OUR_GATE_CAUSES:
            # A gate is a caller refusal on this step too: never retried, re-dispatched or resumed.
            details[CALLER_REFUSAL_KEY] = True
            details["refusal_code"] = self.code
        approval_url = self.failure.get("approval_url")
        if isinstance(approval_url, str) and approval_url:
            details["approval_url"] = approval_url
        return details


class SubgraphTarget(BaseModel):
    """The workflow a ``subgraph.call`` step runs, as the host resolved it."""

    model_config = ConfigDict(extra="forbid")

    definition_id: str
    name: str = ""
    version_number: int | None = Field(
        default=None, description="Published version that runs; None = the draft."
    )
    revision: int | None = Field(
        default=None, description="The draft's saved revision when the draft runs."
    )
    input_kind: str | None = None
    output_kind: str | None = None
    result_step: str | None = None
    result_title: str | None = None
    platform: bool = Field(
        default=False, description="True when the platform owns it (callable from every organization)."
    )

    def answer_version(self) -> str:
        """What answers this step, as one string (the run-once digest)."""
        if self.version_number is not None:
            return f"{self.definition_id}@v{self.version_number}"
        return f"{self.definition_id}@draft{self.revision if self.revision is not None else '?'}"


SubgraphTargetResolver = Callable[
    [NodeExecutionContext | None, "SubgraphCallConfig"], Awaitable[SubgraphTarget]
]

_target_resolver: SubgraphTargetResolver | None = None


def set_subgraph_target_resolver(resolver: SubgraphTargetResolver | None) -> None:
    """Register the host function that turns a step's config into the workflow
    it runs (key → latest published version, access, declared I/O)."""
    global _target_resolver
    _target_resolver = resolver


def get_subgraph_target_resolver() -> SubgraphTargetResolver | None:
    return _target_resolver


def set_subgraph_resolver(resolver: SubgraphRunner | None) -> None:
    """Register the host-app resolver that knows how to execute a child workflow.

    The host typically wires this to a DefinitionStore → compile_graph →
    Scheduler.run pipeline. Passing None unregisters (for tests).
    """
    global _resolver
    _resolver = resolver


class SubgraphCallInput(BaseModel):
    """What the child run is seeded with.

    Two ways in, because a workflow step is wired two ways. An author who
    picked ``inputs`` explicitly gets it verbatim. An author who linked
    upstream FIELDS straight onto this step (the studio's normal
    connect-and-map flow, and what workflow EXTRACTION produces) delivers
    them as plain top-level keys — this model is open, and every extra key
    is seeded into the child alongside ``inputs``.

    That second path is what lets a run of steps be extracted into its own
    workflow without touching a single field link: the links already name
    the first step's own input args, and the child broadcasts its seeded
    inputs to exactly that step. An explicit ``inputs`` entry wins over an
    extra of the same name (the author asked for it by name).
    """

    model_config = ConfigDict(extra="allow")

    inputs: dict[str, JsonValue] = Field(
        default_factory=dict,
        description="Inputs seeded into the child workflow's run (keyed by its "
        "Collect-Inputs field ids). Fields linked directly onto this step are "
        "seeded too — you rarely need to fill this in by hand.",
    )

    @property
    def child_inputs(self) -> dict[str, Any]:
        """The seed payload for the child run: linked fields, then ``inputs``.

        ONE canonicalization — the resolver seeds the run row and the child
        scheduler from this single property, never from ``.inputs`` directly,
        so the two can never disagree.
        """
        return {**(self.model_extra or {}), **(self.inputs or {})}


class SubgraphCallOutput(BaseModel):
    """Success payload (Node Result System) — the old ``success``/``error``
    payload fields are gone; a failed child run is this node's own Failure."""

    model_config = ConfigDict(extra="forbid")

    run_id: str = Field(
        description="The child run's id (for looking up its events/checkpoints).",
    )
    output: JsonValue = Field(
        default=None,
        description="The child workflow's declared result — the output of the step "
        "it marks as its result. Empty when the child declares no result.",
    )
    output_kind: str | None = Field(
        default=None,
        description="The kind of the declared result (the child's output_kind).",
    )
    result_step: str | None = Field(
        default=None,
        description="Which step of the child produced the declared result.",
    )
    definition_id: str | None = Field(
        default=None, description="The child workflow that ran."
    )
    version_number: int | None = Field(
        default=None, description="The child's published version that ran; empty = its draft."
    )
    last_outputs: dict[str, JsonValue] = Field(
        default_factory=dict,
        description="For a child that declares no result, or marks its result step "
        "without a kind: every step's output, keyed by the child's step ids. Read "
        "`output` when the child marks a result.",
    )
    channel_values: dict[str, JsonValue] = Field(
        default_factory=dict,
        description="For a child that declares no result, or marks its result step "
        "without a kind: its final shared-state values, keyed by channel name.",
    )


class SubgraphCallConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    workflow_key: str | None = Field(
        default=None,
        description="The stable name of the workflow to run (its 'platform:<name>' "
        "tag). Runs its latest published version, so improving it improves every caller.",
    )
    definition_id: str | None = Field(
        default=None,
        description="ID of the workflow definition to invoke as a child run "
        "(when it has no stable name).",
        json_schema_extra=field_extras(widget="workflow_picker"),
    )
    version_number: int | None = Field(
        default=None,
        description="Specific published version to run. Blank: the latest published "
        "version for a named workflow, the current draft for one picked by id.",
        json_schema_extra=field_extras(widget="number"),
    )
    max_steps: int = Field(
        default=500,
        ge=1,
        le=100_000,
        description="Hard cap on nested super-steps.",
        json_schema_extra=field_extras(widget="number"),
    )

    @field_validator("workflow_key", "definition_id", mode="before")
    @classmethod
    def _blank_is_none(cls, value: Any) -> Any:
        if isinstance(value, str) and not value.strip():
            return None
        return value.strip() if isinstance(value, str) else value

    @field_validator("workflow_key", mode="after")
    @classmethod
    def _key_without_tag_prefix(cls, value: str | None) -> str | None:
        # The name is written both ways — the tag ``platform:<key>`` and the bare
        # ``<key>``; both mean the same workflow, so the tag prefix is dropped here once.
        if value and value.startswith(PLATFORM_TAG_PREFIX):
            return value[len(PLATFORM_TAG_PREFIX) :].strip() or None
        return value

    @model_validator(mode="after")
    def _one_target(self) -> SubgraphCallConfig:
        if not self.workflow_key and not self.definition_id:
            raise ValueError("Choose the workflow to run: its name (workflow_key) or its id.")
        if self.workflow_key and self.definition_id:
            raise ValueError("Name the workflow to run once: by workflow_key or by definition_id, not both.")
        return self


class SubgraphCallExecutor:
    spec: ClassVar[NodeSpec] = NodeSpec(
        type="subgraph.call",
        category=NodeCategory.SUBGRAPH,
        display_name="Run Workflow",
        description="Run another workflow as a step inside this one.",
        input_schema=SubgraphCallInput,
        output_schema=SubgraphCallOutput,
        config_schema=SubgraphCallConfig,
        output_kind="workflow_run_result",
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
        can_interrupt=True,
        icon="workflow",
    )

    async def result_version(
        self,
        ctx: NodeExecutionContext | None,
        inputs: SubgraphCallInput,
        config: SubgraphCallConfig,
    ) -> str | None:
        """Which child version answers — a run-once step reuses its saved result
        only while the same child version would run (a newly published child
        is a miss). Raises when the host cannot say; the step then runs."""
        if _target_resolver is None:
            raise RuntimeError("no subgraph target resolver registered")
        target = await _target_resolver(ctx, config)
        return target.answer_version()

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: SubgraphCallInput,
        config: SubgraphCallConfig,
    ) -> NodeResult[SubgraphCallOutput]:
        if _resolver is None:
            return failure(
                "no_subgraph_resolver",
                "No subgraph resolver registered. Call "
                "matrx_graph.nodes.subgraph.set_subgraph_resolver(fn) at "
                "app startup to enable subgraph.call.",
            )
        try:
            result = await _resolver(ctx, config, inputs)
        except GraphInterrupt as asked:
            # A question deep inside the child (a Pause & Ask, a durable wait)
            # parks the PARENT at this step, carrying the child's question — one
            # place to answer. Marked ``forwards_answer``: the parent's resume
            # hands the person's answer back to this step (``ctx.resume_answer``)
            # and the host resumes the waiting child with it, instead of
            # recording the answer as this step's own output.
            raise GraphInterrupt(
                node_id=getattr(ctx, "node_id", None) or asked.node_id,
                payload={**asked.payload, FORWARDS_ANSWER_KEY: True},
            ) from asked
        except SubgraphCallRefused as refused:
            return failure(refused.code, refused.message, details=refused.details)
        except SubgraphChildFailed as child:
            # The child's gate cause wins over the generic code: a child stopped by the usage limit is
            # ``usage_limit_reached`` on this step too, with the child run id (and approval link).
            return failure(child.code, child.message, details=child.details())
        except Exception as e:  # noqa: BLE001
            # A child run that errored/failed (the aidream resolver raises
            # ExecutionError with the child run id in the message) is this
            # node's OWN Failure — never a soft-error payload. The code IS the
            # cause (``child_run_failed``, failure._TYPE_CAUSES): the scheduler
            # never guesses it from the sentence, which names the child workflow
            # ("Permissions audit" read not_authorized, 2026-10-27).
            return failure(
                CHILD_RUN_FAILED_CODE,
                str(e),
                details={"error": str(e)},
            )
        run_id = result.get("run_id")
        if not run_id:
            return failure(
                CHILD_RUN_FAILED_CODE,
                "subgraph resolver returned no run_id for the child run.",
                details={"error": "missing run_id in resolver result"},
            )
        declared = result.get("result")
        if isinstance(declared, dict):
            # The child declares its one result: that IS the answer, typed —
            # the caller never reaches into the child's step ids.
            return success(
                SubgraphCallOutput(
                    run_id=run_id,
                    output=declared.get("value"),
                    output_kind=declared.get("output_kind"),
                    result_step=declared.get("step"),
                    definition_id=result.get("definition_id"),
                    version_number=result.get("version_number"),
                    # A result marked without a kind also keeps the step outputs.
                    last_outputs=result.get("last_outputs", {}),
                    channel_values=result.get("channel_values", {}),
                )
            )
        return success(
            SubgraphCallOutput(
                run_id=run_id,
                definition_id=result.get("definition_id"),
                version_number=result.get("version_number"),
                last_outputs=result.get("last_outputs", {}),
                channel_values=result.get("channel_values", {}),
            )
        )
