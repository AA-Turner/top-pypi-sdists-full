from __future__ import annotations

import asyncio
import bisect
import dataclasses
import inspect
import logging
from collections.abc import Sequence
from contextlib import ExitStack
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any, Literal
from uuid import NAMESPACE_URL, uuid4, uuid5

from matrx_orm.core.session_context import declaring_workflow_chain, workflow_chain_for_run
from matrx_utils import raw_capture
from matrx_utils.ctx import public_media_scope
from pydantic import BaseModel

from matrx_graph.checkpoint.protocol import (
    Checkpoint,
    Checkpointer,
    NextInvocation,
    NodeOutcome,
    PendingBinding,
    PendingEdgeBinding,
)
from matrx_graph.decisions import (
    DECISION_KEY,
    DecisionAuthority,
    DecisionProvenance,
    sanitize_decision_value,
    stamp_decision,
)
from matrx_graph.errors import (
    ChannelError,
    EdgeRoutingError,
    ExecutionError,
    FanOutAllItemsFailedError,
    GraphInterrupt,
    NodeFailureError,
    NodeInputValidationError,
    NodeTimeoutError,
    ResumeCannotFinishError,
    forwards_answer,
)
from matrx_graph.mapping_sources import (
    WHOLE_PAYLOAD,
    unknown_sigil,
    unknown_sigil_message,
)
from matrx_graph.failure import (
    TECHNICAL_TEXT_LIMIT,
    Cause,
    RunFailure,
    build_failure,
    cause_from_text,
    client_error_text,
    client_message_for_exception,
    failure_from_exception,
)
from matrx_graph.failure import _refusal_failure, gate_failure
from matrx_graph.content_ir.envelope import stamp_kind_marker
from matrx_graph.executor._retry import compute_backoff_ms, should_retry
from matrx_graph.executor.answered_park import park_was_answered
from matrx_graph.executor.channels import ChannelManager, resolve_reducer
from matrx_graph.executor.introspect import resolve_invocation_inputs
from matrx_graph.executor.json_dump import model_dump_json
from matrx_graph.executor.registry import NodeRegistry, default_registry
from matrx_graph.executor.review_flags import ReviewFlag, ReviewFlagger, occurrence_key
from matrx_graph.executor.once_step import OnceSlot
from matrx_graph.executor.once_step import decide as once_decide
from matrx_graph.executor.once_step import finish as once_finish
from matrx_graph.executor.once_step import not_saved_reason as once_not_saved_reason
from matrx_graph.executor.once_step import settle as once_settle
from matrx_graph.executor.one_at_a_time_step import TurnSlot
from matrx_graph.executor.one_at_a_time_step import end_turn as one_at_a_time_end
from matrx_graph.executor.one_at_a_time_step import take_turn as one_at_a_time_take
from matrx_graph.executor.resume_preflight import (
    JOINABLE_KINDS,
    launch_is_declared,
    record_undeclared_launch,
    required_edge_ids,
    resume_preflight_problems,
)
from matrx_graph.decision_spec import (
    DecisionDefaultError,
    default_decision_answer,
    object_default_from_text,
    resolve_decision,
)
from matrx_graph.executor.client_payload import fold_undeclared_into_extras
from matrx_graph.executor.schema_validation import resume_value_validation_errors, validate_instance
from matrx_graph.paths import resolve_path
from matrx_graph.shape_probe import model_json_schema, path_problem
from matrx_graph.observability import record_exception, set_attributes, span
from matrx_graph.types.compiled import CompiledGraph, CompiledNode
from matrx_graph.types.context import ChannelView, NodeExecutionContext, ResumeAnswer
from matrx_graph.types.identity_inputs import identity_input_fields
from matrx_graph.types.events import (
    CheckpointSavedEvent,
    NodeCompletedEvent,
    NodeFailedEvent,
    NodeRetryScheduledEvent,
    NodeSkippedEvent,
    NodeStartedEvent,
    RunCancelledEvent,
    RunCompletedEvent,
    RunErroredEvent,
    RunFailedEvent,
    RunInterruptedEvent,
    RunPausedEvent,
    RunResumedEvent,
    RunStartedEvent,
    NodeCostEvent,
    WorkflowEvent,
    node_cost_from_output,
)
from matrx_graph.content_ir.edge_routing import (
    EdgeKindRouting,
    fan_out_items,
    select_instances,
)
from matrx_graph.content_ir.envelope import RESERVED_MARKER_KEYS
from matrx_graph.content_ir.subscriptions import KindSubscription, SubscriptionMatcher
from matrx_graph.types.primitives import ActionTier, EdgeKind, NodeCategory, RunStatus
from matrx_graph.types.result import Failure, FieldProblem, NodeError, Success
from matrx_graph.spend_gate import (
    InterruptedAttempt,
    close_invocation_spend,
    is_caller_refusal,
    is_cost_bearing,
    open_invocation_spend,
    tally_totals,
)
from matrx_graph.types.send import Send
from matrx_graph.step_settings import when_gate_owner

if TYPE_CHECKING:
    from matrx_connect.context.app_context import AppContext

logger = logging.getLogger(__name__)

#: (step type, workflow id) pairs whose deprecated-step ``system_error`` this process
#: already wrote — one row per pair, not one per run.
_DEPRECATION_CAPTURED: set[tuple[str, str]] = set()

# Deterministic contract failures: retrying re-executes the node's side
# effects for a guaranteed-identical failure (the output will violate its
# declared kind exactly the same way), so these error codes never enter the
# retry ladder — even under a retry-anything policy. Checked at both
# should_retry sites (live failure + crash-replay walk-forward).
# TurnNotTaken: a step that ended its wait for its turn (cancelled, max wait, self-wait) —
# retrying would only wait again (data.one_at_a_time).
_NON_RETRYABLE_ERROR_TYPES: frozenset[str] = frozenset({"KindContractViolation", "TurnNotTaken"})


class _NodeGate:
    """The live-invocation bound of ONE node (ENGINE_SPEC §4.6 + the ``workflow.fan_out`` knobs).

    ``cap`` invocations run at once; the rest queue. A cost-bearing fanned node starts at
    ``first_wave`` permits and opens to ``cap`` only when its first invocation settles — so a
    200-item map of paid steps never launches before the run knows what one item costs."""

    __slots__ = ("cap", "first_wave", "live", "peak", "_ramped", "_sem")

    def __init__(self, cap: int, first_wave: int | None = None) -> None:
        self.cap = max(1, int(cap))
        self.first_wave = max(1, min(self.cap, int(first_wave or self.cap)))
        self._sem = asyncio.Semaphore(self.first_wave)
        self._ramped = self.first_wave >= self.cap
        self.live = 0
        self.peak = 0

    async def __aenter__(self) -> None:
        await self._sem.acquire()
        self.live += 1
        self.peak = max(self.peak, self.live)

    async def __aexit__(self, *exc: object) -> None:
        self.live -= 1
        self._sem.release()
        if not self._ramped:
            self._ramped = True
            for _ in range(self.cap - self.first_wave):
                self._sem.release()


def _workflow_invocation_conversation_id(
    *,
    run_id: str,
    step: int,
    invocation: Invocation,
) -> str:
    """Return the stable durable conversation identity for one invocation.

    A workflow run keeps one request identity for cost rollup, but each node
    invocation is its own provider/persistence boundary.  In particular,
    parallel invocations must not share provider cache-guard state or race to
    create the same ``cx_conversation`` row.  Retries intentionally retain the
    same identity, so ``attempt`` is not part of this key.
    """

    dispatch_id = invocation.dispatch_id or "root"
    key = (
        f"matrx-workflow-invocation:{run_id}:{step}:{invocation.node_id}:"
        f"{dispatch_id}:{invocation.item_index}:{invocation.firing}"
    )
    return str(uuid5(NAMESPACE_URL, key))


def _merge_structured_failure(
    node_error: NodeError, structured: RunFailure, *, err_type: str
) -> NodeError:
    """Fold the structured failure onto the ``node_error`` kind instance.

    ONE shape for one failure (plan §10d-B3). Before this, the scheduler built
    a loose superset dict for the ``error`` column while the ERROR edge carried
    a three-field NodeError dump — the same failure in two shapes, neither of
    them self-describing. The merge rule is byte-preserved from that dict
    build: ``type``/``message``/``code``/``details`` on the node plane are
    authoritative (a node's own wording beats a generated sentence), and a
    structured value only fills a field the node left empty.
    """
    columns = structured.to_column()
    update: dict[str, Any] = {
        # A node's own wording is authoritative — but never its terminal
        # render: a returned Failure built from ``str(exc)`` carries the ORM
        # banner with SQL and bound args (live 2026-09-17, Save Table Row).
        "message": client_error_text(node_error.message) or structured.message,
        "type": err_type,
    }
    for field_name in (
        "cause",
        "step_id",
        "step_label",
        "field",
        "expected",
        "got",
        "error_type",
        "technical",
    ):
        value = columns.get(field_name)
        if value is not None and getattr(node_error, field_name) is None:
            update[field_name] = value
    if columns.get("fields") and not node_error.fields:
        update["fields"] = [FieldProblem.model_validate(f) for f in columns["fields"]]
    return node_error.model_copy(update=update)


# Run-wide invocation budget (width guard). max_steps bounds depth; this
# bounds the TOTAL number of node invocations one drive segment may schedule,
# so dynamic fan-out (Sends, waves, work queues) stays finite even when every
# per-dispatch cap is individually satisfied. A CAPS default — hosts may
# override per run via Scheduler.run/resume(max_total_invocations=...).
# 25k, NOT 10k: control.map legally dispatches up to 10_000 items in ONE
# step (its own le=10_000 ceiling) — the run-wide budget must sit comfortably
# above the largest single legal dispatch plus its surrounding graph, or a
# previously-legal max-size map regresses to FAILED.
DEFAULT_MAX_TOTAL_INVOCATIONS = 25_000


#: Attributes ``failure_from_exception`` reads as its richest evidence — the
#: node's own stable code first, then the engine's per-field list. They must
#: cross any re-wrap.
_EVIDENCE_ATTRS = ("node_error", "node_id", "person_message", "field_errors")


def append_failure_notes(err: BaseException, notes: list[str]) -> BaseException:
    """Add the step's honest partial-success notes WITHOUT losing the structure.

    A wide fan-out step that mostly succeeded must say so ("1 of 2 invocations …
    completed and are preserved"), which means re-wrapping the first error's
    text. Re-wrapping in a bare ``ExecutionError`` dropped ``node_error`` — the
    node's own stable code — so ``failure_from_exception`` fell all the way to
    its prose ladder and every fan-out failure was classified from its sentence.
    Live 2026-09-12, run ``6fa6ad90`` node ``n_check``: a stalled tool loop
    persisted as ``engine_error`` → "stopped partway through".

    Returns ``err`` unchanged when there is nothing to add.
    """
    if not notes:
        return err
    wrapped = ExecutionError(f"{type(err).__name__}: {err} " + " ".join(notes))
    for attr in _EVIDENCE_ATTRS:
        value = getattr(err, attr, None)
        if value is None:
            continue
        try:
            setattr(wrapped, attr, value)
        except Exception:  # noqa: BLE001 — describing a failure must never become one
            logger.warning("could not carry %s across the fan-out note wrap", attr)
    wrapped.__cause__ = err
    return wrapped


def _install_app_context(ctx: AppContext | None) -> Any:
    """Install ``ctx`` as the ambient AppContext for the current task.

    Returns a token to pass to :func:`_reset_app_context`, or ``None`` when
    there is no context to install (console/standalone use without
    matrx-connect, or a None app). matrx-connect is a hard dependency of
    matrx-graph, but we import lazily + tolerate its absence so the engine
    still runs in a minimal environment.
    """
    if ctx is None:
        return None
    try:
        from matrx_connect.context.app_context import set_app_context
    except ImportError:
        return None
    return set_app_context(ctx)


async def _execute_in_organization(
    executor: Any, ctx: Any, inputs_model: Any, config_model: Any, organization_id: str | None
) -> Any:
    """The executor call, inside the step's admitted organization when ``data.in_organization`` names one."""
    if organization_id is None:
        return await executor.execute(ctx, inputs_model, config_model)
    from matrx_graph.in_organization import in_organization

    async with in_organization(ctx, organization_id):
        return await executor.execute(ctx, inputs_model, config_model)


def _reset_app_context(token: Any) -> None:
    if token is None:
        return
    try:
        from matrx_connect.context.app_context import clear_app_context
    except ImportError:
        return
    try:
        clear_app_context(token)
    except (ValueError, LookupError):
        # Token created in a different context (shouldn't happen — each
        # invocation runs in its own gather task — but resetting across
        # contexts raises; swallow rather than mask the real node result).
        pass


def elided_output_marker(node_id: str, step: int) -> dict[str, Any]:
    """What ``workflow.run.output`` holds for a step that keeps its output out of the run row.

    A plain pointer, not content: ``output_elided`` is the discriminator (no ``__kind`` — it is not a
    registered kind, Content IR rule 28).
    """
    return {"output_elided": True, "node_id": node_id, "step": step,
            "where": "workflow.node_outcome"}


@dataclass(slots=True)
class Invocation:
    """One scheduled call to a node executor within a super-step.

    `inputs` is the JSON payload that becomes the executor's validated
    `inputs` model argument. Edge-driven invocations come from routing a
    predecessor's output; Send-driven invocations come from `ctx.send()`.

    ``(dispatch_id, item_index)`` is the fan-out correlation identity
    (ENGINE_SPEC §4.1): ``''``/``0`` for ordinary invocations; a Send-driven
    invocation carries its Send's minted identity. ``attempt`` is a retry
    counter WITHIN one correlation key (§4.2), never a sibling separator.

    ``config_override`` (Phase 5.3) — optional dict merged OVER the node's
    authored config at execute time. Used by "Retry without saving" so a
    one-off config tweak doesn't have to be committed to the draft.
    """

    node_id: str
    inputs: dict[str, Any]
    attempt: int = 1
    dispatch_id: str = ""
    item_index: int = 0
    config_override: dict[str, Any] | None = None
    # Durable work-set correlation: the claimed workflow.work_item id this
    # invocation processes ('' = none). Settled complete/fail at
    # outcome-record time; round-trips through NextInvocation.
    work_item_id: str = ""
    # Blocked-join park marker (ENGINE_SPEC §3.4 Amendment D2b): this
    # invocation represents a deadlocked join target, addressable by the
    # recovery API. See NextInvocation.blocked_join.
    blocked_join: bool = False
    # Monotonic per-node firing number for accumulator-fired invocations
    # (ENGINE_SPEC §3.8); 0 for entry seeds and Sends.
    firing: int = 0
    # Engine-carried loop state (ENGINE_SPEC §9): [{origin_node_id,
    # iteration}, ...] — pushed by control.loop's body Send, inherited
    # through the body chain (§4.3), popped (+ ``iteration`` injected) when
    # a delivery returns to the frame's origin. See NextInvocation.loop_stack.
    loop_stack: list[dict[str, Any]] = field(default_factory=list)
    # The step this invocation is scheduled for, when it came off a checkpoint
    # frontier (NextInvocation.step). None = the step the loop is on. The loop
    # holds an invocation scheduled for a LATER step until that step, so a
    # resumed run keys every node exactly as the original run did.
    step: int | None = None
    # Run once per key: ignore any stored result for this invocation's key (the person
    # asked for a fresh result). See NextInvocation.bypass_once.
    bypass_once: bool = False


def _record_escaped_fault(task: asyncio.Task[None], result: _StepResult, *, run_stopping: bool = False) -> None:
    """An exception that escaped an invocation task becomes that step's error (the run parks
    ERRORED with the sentence), never a dropped task exception and a silently COMPLETED run.
    A task cancelled while the RUN is stopping (cancel, pause, lost lease / deploy drain) is not
    a fault — the caller stops the run as before; a step that cancelled ITSELF is one. An error
    the invocation already recorded wins."""
    if not task.done():
        return
    if task.cancelled():
        if run_stopping or result.error is not None or result.interrupt is not None:
            return
        result.error = ExecutionError(
            f"Step '{result.invocation.node_id}' stopped itself with a cancellation while the run "
            "was not being cancelled, paused or drained, so it has no result."
        )
        logger.error("[wf node=%s] invocation cancelled itself outside a run stop", result.invocation.node_id)
        return
    exc = task.exception()
    if exc is None or result.error is not None or result.interrupt is not None:
        return
    if isinstance(exc, Exception):
        if isinstance(exc, ExecutionError):
            result.error = exc
        else:
            err = ExecutionError(
                f"Step '{result.invocation.node_id}' stopped on an engine fault: {type(exc).__name__}: {exc}"
            )
            err.__cause__ = exc
            result.error = err
        logger.error("[wf node=%s] invocation task raised outside its step: %r", result.invocation.node_id, exc)


@dataclass(slots=True)
class _StepResult:
    invocation: Invocation
    output: BaseModel | None
    channel_writes: list[tuple[str, Any]] = field(default_factory=list)
    sends: list[Send] = field(default_factory=list)
    emissions: dict[str, Any] = field(default_factory=dict)
    error: Exception | None = None
    interrupt: GraphInterrupt | None = None
    # True when this result came from a user_skip (pre-emptive skip or a
    # replayed user_skip outcome) — join targets consult their
    # on_skipped_upstream policy for it (ENGINE_SPEC §3.4).
    user_skipped: bool = False
    # Node Result System: a ROUTABLE node failure — the node returned a
    # Failure envelope (or raised) after exhausting retries, and the failure
    # is handled by topology instead of parking the run: either an outgoing
    # ERROR edge (delivered the NodeError dump; every normal edge prunes) or
    # a fanned item under on_item_failure='hole' (recorded as an explicit
    # failed item in the aggregated dispatch). Mutually exclusive with
    # ``error`` (which parks) and ``output`` (success).
    failure: NodeError | None = None
    # THE SETTLED DUMP (adversarial round-1 F2): the json-safe dict settlement
    # produced — kind verdict computed, ``__kind`` stamped where lawful. Edge
    # routing, the subscription broadcast, and last_outputs MUST use this
    # instead of re-dumping ``output``, or the stamp dies at the first hop
    # (a legacy ``extra="forbid"`` model cannot carry the marker through a
    # model round-trip) and "self-describing everywhere it travels" is a lie
    # one edge deep. ``None`` for paths that never settled (mock/skip/error).
    settled_dump: dict[str, Any] | None = None
    # RUN ONCE PER KEY: True when this output is a stored result reused instead of running
    # the step (outcome ``source="reused"``, live or replayed). A fanned item carries it to
    # its aggregated delivery, so ``control.gather`` reports ``reused_indexes``.
    reused: bool = False
    # RUN-AHEAD: True once this result was offered to ``_expand_run_ahead``
    # (whether or not anything launched) — it is expanded at most once.
    expanded: bool = False


@dataclass
class RunResult:
    run_id: str
    thread_id: str
    status: RunStatus
    steps_executed: int
    channel_values: dict[str, Any]
    last_outputs: dict[str, Any]
    interrupt: dict[str, Any] | None = None
    error: str | None = None
    # THE structured failure (matrx_graph.failure). Built where the engine
    # still holds the step, the field and the expectation — before any of it
    # gets flattened into ``error``'s one line. ``error`` is kept as the raw
    # technical string every existing log/test reads; ``failure`` is what the
    # host persists into ``workflow.run.error`` so readers branch on a stable
    # ``cause`` instead of regexing English. None on a clean finish.
    failure: RunFailure | None = None
    # Mandate-candidate containment (matrx_graph.candidate): the §2.1
    # ``stopped_at`` record when a candidate run reached a node it may not run.
    # The run's status is CANCELED (the workflow.run CHECK has no candidate
    # value); THIS field is what says why. Also recorded in the shared ledger.
    candidate_stopped: dict[str, Any] | None = None
    # A COMPLETED run that stopped early because a step declared why (a condition step
    # that said no, its conditional edge pruned): ``{reason, says, step}``. The run store
    # writes it to ``workflow.run.metadata.stopped``. See ``executor/run_stop.py``.
    stopped: dict[str, Any] | None = None


#: Why a TEST run did not invoke a step listed in its ``sample_steps`` — on the outcome's
#: ``metadata.reason`` and the ``node_skipped`` event's ``reason``.
SAMPLED_STEP_REASON = "test run: answered from the step's declared sample, not run"


def _stamp_mock_dump(dump: dict[str, Any], output_kind: str | None) -> dict[str, Any]:
    """Round-1 F10: mocked outcomes carry the same root stamp as real ones."""
    if (
        output_kind is not None
        and output_kind != "json"
        and isinstance(dump, dict)
        and "__kind" not in dump
    ):
        dump["__kind"] = output_kind
    return dump


_INPUT_SCHEMA_JSON_CACHE: dict[type, dict[str, Any]] = {}


def _kind_contract_inputs(spec: Any, inputs: Any) -> Any:
    """The part of a step's inputs its declared input kind governs.

    A step whose input model allows extra values (``data.filter`` / ``data.check_items``: every value delivered
    beside the list is the predicate's ``$in`` namespace) declares its kind over its DECLARED fields; the extras are
    the step's documented free namespace and never part of the kind's closed contract. Every other step is checked
    whole, as before. The declared fields are still checked."""
    schema = getattr(spec, "input_schema", None)
    if not isinstance(inputs, dict) or schema is None or not schema.model_fields:
        return inputs
    if schema.model_config.get("extra") != "allow":
        return inputs
    declared = {"__kind"}
    for name, info in schema.model_fields.items():
        declared.add(name)
        if info.alias:
            declared.add(info.alias)
    return {k: v for k, v in inputs.items() if k in declared}


def _input_schema_json(model_cls: type[BaseModel]) -> dict[str, Any]:
    """Cached ``model_json_schema()`` for the ingestion gate.

    The gate runs per invocation; deriving the schema is pure but not cheap,
    and node input models are a small, stable set per process.
    """
    cached = _INPUT_SCHEMA_JSON_CACHE.get(model_cls)
    if cached is None:
        cached = model_cls.model_json_schema()
        _INPUT_SCHEMA_JSON_CACHE[model_cls] = cached
    return cached


def _coerce_replayed_output(model_cls: type[BaseModel], value: Any) -> BaseModel:
    """Use the canonical ingestion gate for saved outputs, retaining the caller's tagged dump.

    Closed legacy models need a validation view; routing and settlement keep the
    original payload, including its nested kind identities.
    """
    from matrx_graph.content_ir.markers import reduce_for_ingestion

    if isinstance(value, dict):
        value = reduce_for_ingestion(value, _input_schema_json(model_cls))
    return model_cls.model_validate(value)


class Scheduler:
    """Pregel super-step executor for a CompiledGraph.

    One super-step = one wave of parallel node invocations. The step loop:
        1. Snapshot channel state — every invocation in this step sees the same view.
        2. Run all invocations in an asyncio.TaskGroup. Executors may:
           - Return an OutputT (routed to outgoing edges).
           - Call ctx.emit(handle_id, payload) (routed only to that handle).
           - Call ctx.send(target, payload) (scheduled as a distinct invocation
             next step).
           - Call ctx.channels.write(name, value) (reduced between steps).
           - Raise GraphInterrupt (halts the run with a payload).
        3. Reduce channel writes via ChannelManager.
        4. Route outputs + Sends into next-step invocations.
        5. Save a checkpoint.
        6. Loop.

    Idempotency: before executing, the scheduler checks the checkpointer for a
    recorded outcome at (run_id, step, node_id, attempt). If present with no
    error, the recorded output is replayed without re-invoking the node —
    this is what makes resume after crash safe for side-effectful nodes.

    Interrupts: GraphInterrupt raised by a node is captured; the scheduler
    persists a checkpoint marked with the interrupt payload and returns with
    status=INTERRUPTED. Call `resume()` to continue from that checkpoint.
    """

    def __init__(
        self,
        graph: CompiledGraph,
        checkpointer: Checkpointer,
        app_context: AppContext,
        registry: NodeRegistry | None = None,
        cancel_check: Any = None,
        pause_check: Any = None,
        skip_node_ids: set[str] | None = None,
        control_check: Any = None,
        control_check_reads_own_row: bool = False,
        fresh_history: bool = False,
        skip_edge_ids: set[str] | None = None,
        step_concurrency: int | None = None,
        definition_version_id: str | None = None,
        definition_id: str | None = None,
        surface_inputs: dict[str, Any] | None = None,
        input_provenance: dict[str, str] | None = None,
        sampled_outputs: dict[str, Any] | None = None,
    ) -> None:
        """
        sampled_outputs: a TEST run's answered steps — node_id → that step's declared sample
            (the host resolves and validates them at start and refuses a non-test run). Each
            listed step is never invoked: every invocation of it (each fan-out item too)
            outputs the sample through the mock seam, recorded ``source="mocked"`` with
            ``metadata.sampled`` and announced on ``node_skipped`` (``sampled=True``). Never
            stored for ``data.once``, never billed. None / {} = every step runs for real.
        surface_inputs: the run's landed INPUT-SURFACE values (name → value,
            precedence already resolved by the start seam and persisted on
            ``wf_run.metadata._settings.input_values``). Resolves every
            ``{"$input": name}`` reference, seeds io.user_input nodes, and
            feeds the park-not-die gate. None/{} = legacy start (the $var /
            node_inputs compatibility path).
        input_provenance: name → source stamp ('pinned'/'human'/'caller'/
            'mandate'/'default') for the landed values. The 'ask' sourcing
            rule is satisfied only by 'human'-stamped values; stamps are
            written by the start seam under the source=human invariant —
            never client-authored here.
        cancel_check: optional async callable ``() -> bool`` that returns True
            if the run should abort before the next super-step. Polled between
            steps. Router wires this to a wf_run.status check; workers do the
            same. None = never cancel (default).
        pause_check: optional async callable ``() -> bool`` that returns True
            if the run should suspend before the next super-step. Polled
            between steps. On True, the scheduler saves a checkpoint, emits
            RunPausedEvent, and returns with status=PAUSED. Resume re-enters
            the loop at the saved checkpoint. None = never pause (default).
            Pause takes priority over cancel — if both signals are set, the
            user wanted to pause first.
        control_check: optional async callable ``() -> str | None`` returning
            the run's current status. When given, ONE call answers both the
            pause and the cancel poll at a super-step boundary ('pausing' /
            'cancelling'); ``pause_check``/``cancel_check`` stay the fallback.
        control_check_reads_own_row: True ONLY when ``control_check`` reads
            nothing but this run's own ``wf_run.status`` — the column the
            checkpoint save already read back. Then that saved status stands in
            for the boundary poll (no round trip). Default False: a check that
            reads anything else (a called workflow's check also reads its
            PARENT's cancel) is called at every boundary, or a parent's Cancel
            never reaches a running child.
        fresh_history: True when the host KNOWS this run has no recorded node
            outcomes — it created the run row moments ago in this process and
            this is the run's first and only leg. A fresh ``run()`` then skips
            the per-invocation idempotency lookup (always empty for such a run;
            a database read before every node starts). Every other leg — resume,
            a queued worker that may be re-delivering a crashed start — leaves
            it False and keeps the lookup.
        skip_node_ids: optional set of node_ids the caller wants the scheduler
            to short-circuit. Each such node emits a ``node_skipped`` event,
            records a ``user_skip`` outcome with output ``{}`` (or the
            schema's empty model when validate({}) fails), and lets downstream
            edges route the empty payload. Useful for "run this workflow but
            skip the slow LLM call" or "skip the external API" during
            iteration. None / empty = no preemptive skips (default).
        skip_edge_ids: optional set of edge ids the scheduler should NOT
            route along (Phase 5.2). When a source node completes, any
            outgoing edges in this set are silently dropped — downstream
            targets receive no payload from them. Useful for "what if
            branch X didn't fire?" testing without editing the graph.
            Downstream nodes that depend on the skipped edge may fail;
            that's the explicit trade-off and the failure is recoverable
            like any other.
        definition_version_id: optional id of the workflow definition VERSION
            this run is pinned to (``workflow.run.definition_version_id``).
            Stamped once onto the run's AppContext here so every forked
            step/agent context carries it and any provider call made inside the
            run records which workflow version produced it
            (``chat.request_snapshot.workflow_definition_version`` — the config
            half of Level-1 wire replay). None is the honest value for a run
            started from a FLOATING definition, which pins no version row.
        definition_id: optional id of the workflow this run belongs to
            (``workflow.run.definition_id``). WHICH WORKFLOW is half of the
            packet the UI receives — it rides ``run_started.definition_id`` and
            the ``node_outcome`` wrapper on every completion. The compiler
            cannot supply it (a CompiledGraph is compiled from a Definition,
            which carries no row id — ``source_metadata`` is left empty), so
            the caller that loaded the row passes it here. None only when the
            graph genuinely has no definition row (an in-code graph).
        """
        self.graph = graph
        self.checkpointer = checkpointer
        # WHICH WORKFLOW — explicit from the caller, else whatever the graph's
        # source metadata carries (empty in practice: see the docstring).
        self.definition_id = (
            str(definition_id)
            if definition_id
            else (graph.source_metadata.get("definition_id") or "")
        )
        # One stamp, at the top of the run — forks inherit it via
        # dataclasses.replace, so nothing downstream has to thread it through.
        if definition_version_id and hasattr(app_context, "workflow_definition_version_id"):
            app_context = dataclasses.replace(
                app_context, workflow_definition_version_id=str(definition_version_id)
            )
        self.app = app_context
        self.registry = registry or default_registry()
        self.channels = ChannelManager(graph.channels, strict=graph.strict_channels)
        self._cancel_check = cancel_check
        self._pause_check = pause_check
        self._control_check = control_check
        self._control_check_reads_own_row = bool(control_check_reads_own_row)
        self._fresh_history = bool(fresh_history)
        # Set for the duration of a fresh ``run()`` leg only (never resume).
        self._history_known_empty = False
        # The run status the last main-loop checkpoint save read (pop_run_status),
        # consumed by the next boundary poll; None = read it at the boundary.
        self._status_at_boundary: str | None = None
        self._skip_node_ids: set[str] = set(skip_node_ids or ())
        self._sampled_outputs: dict[str, Any] = dict(sampled_outputs or {})
        self._skip_edge_ids: set[str] = set(skip_edge_ids or ())
        # Degraded-kind warning throttle: (run_id, kind slug) pairs already
        # warned about. The kind catalog screams once per PROCESS per slug;
        # this keeps the run-scoped context line to once per (run, slug)
        # instead of once per node execution — the verdict fields on every
        # event/outcome still carry the degraded reason per occurrence.
        self._kind_degraded_warned: set[tuple[str, str]] = set()
        # Run variables — the values behind every {'$var': name} reference
        # authored in node static_inputs. Carried on the AppContext as
        # initial_variables (the studio Start sheet / API caller's
        # name→value pairs) for run, resume, queued, and step-mode alike.
        # Resolved per invocation in resolve_invocation_inputs; a reference
        # with no value and no default raises UnresolvedVariableError and
        # parks the run on that node — never a silent empty string.
        self._run_variables: dict[str, Any] = dict(
            getattr(app_context, "initial_variables", None) or {}
        )
        # THE INPUT SURFACE's landed values + provenance stamps (INPUT-
        # SURFACE.md). Resolved once at run start by the host's start seam
        # (precedence: pinned > human > caller > mandate default > declared
        # default) and handed here for {'$input': name} resolution, entry
        # seeding, and the park-not-die gate.
        self._run_inputs: dict[str, Any] = dict(surface_inputs or {})
        # Keys each step named BESIDE its kind (``ctx.declare_beside_kind``) on its last
        # completion — mapping paths into them are never judged against the kind.
        self._beside_kind: dict[str, frozenset[str]] = {}
        # The run being executed, for {"$run": ...} references (set per invocation).
        self._run_facts: dict[str, Any] = {}
        # READINESS ON RUN FACTS (``data.ready_when``): a node whose declared facts are absent
        # from this run's variables is skipped for the run through the pre-emptive skip path —
        # never invoked, never billed, its NodeSkippedEvent naming what was missing.
        # Facts are read from the run variables and the landed input surface (a surface value wins).
        self._not_ready: dict[str, str] = unready_nodes(graph, {**self._run_variables, **self._run_inputs})
        self._skip_node_ids.update(self._not_ready)
        self._input_provenance: dict[str, str] = dict(input_provenance or {})
        # Bounded step parallelism (BS-6): when set, at most N invocations
        # of one super-step execute concurrently — the rest queue on this
        # semaphore. Rate-limited fan-outs (research analysis, TTS,
        # scraping) express their throttle here declaratively instead of
        # hand-rolled per-action semaphores. None = unbounded (legacy).
        self._step_sem: asyncio.Semaphore | None = (
            asyncio.Semaphore(step_concurrency)
            if step_concurrency and step_concurrency > 0
            else None
        )
        # RUN-AHEAD (``run_ahead_blockers``): nodes made Ready while a step
        # waits on an unrelated slow member start at once, filed under the step
        # key the barrier will give them. ``_run_ahead`` holds the launches not
        # yet adopted by their step; ``_run_ahead_unexpanded`` the ones whose
        # own result has not yet been offered for further run-ahead.
        self._run_ahead_allowed: bool = RUN_AHEAD_ENABLED and not run_ahead_blockers(graph)
        self._run_ahead_on: bool = False
        # START WHEN READY (``Definition.metadata['start_when_ready']``): run-ahead becomes dataflow — every
        # finished result the barrier has not routed yet is routed, in step order, whenever a new
        # fact arrives, so a step starts when its last input lands (``_expand_eager``).
        self._eager_ahead: bool = bool(getattr(graph, "start_when_ready", False))
        # The step the drive loop is running (its barrier not yet passed); a launch keyed later is
        # a run-ahead launch.
        self._loop_step: int | None = None
        self._run_ahead_step_limit: int = 0
        # Invocations run-ahead may still launch this drive — the remainder of
        # max_total_invocations, refreshed at every step boundary.
        self._run_ahead_budget: int = 0
        # A pause/cancel seen mid-step (where run-ahead polls before launching)
        # stays seen, so the step-boundary poll acts on it even when the host's
        # check answers only once.
        self._pause_latched: bool = False
        self._cancel_latched: bool = False
        self._last_stop_poll: float = float("-inf")
        # While a step waits with run-ahead on: how a NEW run-ahead launch gets
        # its completion delivered to that wait.
        self._run_ahead_deliver: Any = None
        self._run_ahead: dict[tuple[int, str, str, int], tuple[asyncio.Task[None], _StepResult]] = {}
        self._run_ahead_unexpanded: dict[asyncio.Task[None], tuple[_StepResult, int]] = {}
        # True only while ``_expand_run_ahead`` routes a SUBSET of a step on a
        # throwaway copy of the join state. Every routing rule that reads
        # run-wide state the FULL routing builds (the dispatch registry behind
        # the empty-map prune and fan-in completeness, kind subscriptions) is
        # deferred to the barrier while it is set: a partial routing may make
        # a node Ready only where the full routing provably makes it Ready
        # with the same inputs (``_verify_run_ahead_at_barrier`` checks it).
        self._partial_routing: bool = False
        # PURE-STEP OUTCOMES RIDE THE CHECKPOINT (2026-10-29). While a super-step whose every
        # member is PURE runs, each successful outcome (and its node_completed event) waits
        # here instead of paying its own transaction; the step's checkpoint save lands them
        # in ITS transaction, then emits the events (``_save_checkpoint``). A pure step was
        # ~9 database round trips (outcome: 4, checkpoint: 5); now ~6.
        # Steps that hold a non-PURE member: nothing of theirs waits (a run-ahead launch can
        # finish before its step's members are all known, so the test is made per step at
        # its start and anything already held for it is written then).
        self._no_defer_steps: set[int] = set()
        self._deferred_outcomes: list[tuple[NodeOutcome, NodeCompletedEvent]] = []
        # REVIEW FLAGS (0117): author marks (data.review) + engine auto-flags. One awaited
        # run_log write each, never raising; edge flags queue during canonical routing.
        self._review = ReviewFlagger(
            organization_id=getattr(app_context, "organization_id", None),
            user_id=(str(app_context.user_id) if getattr(app_context, "user_id", None) else None),
        )
        # Failures an ERROR connection caught this run, first per step: ``{node_id: {code, message}}``.
        # At completion ``declared_run_stop`` turns one whose normal next steps never ran into the
        # run-level stop record, so a run that ended at a failed check never reads plain completed.
        self._caught_failures: dict[str, dict[str, str]] = {}
        # Every step that FAILED while the run went on (an ERROR connection caught it, or it is
        # ``optional``): ``{node_id: {message, cause}}``. With ``_error_gate_drops`` it is how the run-end
        # deliverable check tells a result step lost to a failure from a branch not taken.
        self._failed_steps: dict[str, dict[str, str]] = {}
        # Steps the error-handler gate dropped although a normal input DID arrive (only their
        # error connection stayed silent): ``{node_id: error-source node id}``.
        self._error_gate_drops: dict[str, str] = {}
        # Run-end residue: joins dropped with required connections that NEVER resolved (no data
        # buffered, but the step neither ran nor was ruled out) — ``(node_id, [edge ids])``, each
        # raised as an ``engine.join_never_resolved`` review flag before the run completes.
        self._never_resolved_joins: list[tuple[str, list[str]]] = []
        # Joins a FAILED upstream stopped this routing pass: (step id, failed step id),
        # reported as node_skipped once the pass is accepted (_report_failure_blocked).
        self._failure_blocked: list[tuple[str, str]] = []
        # Join accumulator (ENGINE_SPEC §3.8): partial inbound bindings per
        # target node, buffered ACROSS super-steps and persisted on every
        # checkpoint. A target fires only when its required inbound-edge set
        # resolves per its join_policy; the entry is then consumed. Loaded
        # from the checkpoint on resume; reset on a fresh run().
        self._pending_bindings: dict[str, PendingBinding] = {}
        # Monotonic per-node firing counter behind PendingBinding.firing.
        self._firing_seq: dict[str, int] = {}
        # Fan-out dispatch registry (ENGINE_SPEC §4.4): how many Sends of one
        # dispatch target one node — (dispatch_id, target_node_id) → count.
        # Filled when a dispatcher's Sends are routed (idempotent overwrite,
        # so replay refills identical values); seeded on resume from the
        # checkpoint (persisted PendingBinding.expected_items + the frontier's
        # fanned invocations). This is what tells a fan-in edge group that
        # ALL items of its dispatch have resolved.
        self._dispatch_expected: dict[tuple[str, str], int] = {}
        # Per-node concurrency caps (ENGINE_SPEC §4.6): node_id → semaphore,
        # created lazily from CompiledNode.concurrency. Nested INSIDE the
        # run-level step semaphore.
        self._node_sems: dict[str, _NodeGate] = {}
        # The ``workflow.fan_out`` bounds, read once per drive (lazily, at the first bounded launch).
        self._fan_out_policy: Any = None
        # The host's spend refusal (matrx_graph.spend_gate), latched for the rest of the drive:
        # once one cost-bearing launch is refused, no further one is dispatched.
        self._spend_refusal: Any = None
        # resume(): the answer to a relayed question, keyed by the invocation that relayed it.
        self._forwarded_answers: dict[tuple[str, str, int], ResumeAnswer] = {}
        # node_cost already emitted per invocation (node, dispatch, item, firing) → (usd, in, out),
        # so the tally settles only the remainder (matrx_graph.spend_gate § the tally).
        self._cost_emitted: dict[tuple[str, str, int, int], tuple[float, int, int]] = {}
        # Cycle back-edge firings collected during one routing pass (F13,
        # ENGINE_SPEC §3.2): a delivery over a compile-classified back-edge
        # bypasses the join accumulator and opens a NEW firing directly —
        # join_policy='any' semantics for the delivery. Reset per
        # _route_outputs pass.
        self._back_edge_fires: list[Invocation] = []
        # Kind-filtered-edge fan-out (KINDS_EVERYWHERE_PLAN §7.4): an edge in
        # ``each`` mode dispatches ONE Send per instance instead of resolving a
        # join, riding the same machinery ``control.map`` uses. Collected
        # during one routing pass, drained beside the executors' own Sends.
        self._edge_fanout_sends: list[tuple[str, Send]] = []
        # dispatch_id -> the loop frame stack fanned children inherit.
        self._edge_fanout_loop_stacks: dict[str, list[dict[str, Any]]] = {}
        # Kind subscriptions (§7.7c) — the purpose-blind matcher that fires
        # kind-triggered nodes (and, when directive kinds land, mutates the
        # graph under the apply-policy). Built once from the compiled graph:
        # a run with no triggered node carries an empty matcher and pays
        # nothing, because ``observe`` returns immediately on no subscriptions.
        self._subscriptions = SubscriptionMatcher(
            [
                KindSubscription(
                    subscriber_id=node_id,
                    kind=node.trigger_kind,
                    mode=node.trigger_mode,
                    fire_once=node.trigger_fire_once,
                    debounce_steps=node.trigger_debounce_steps,
                    purpose="node_trigger",
                )
                for node_id, node in self.graph.nodes.items()
                if node.trigger_kind
            ]
        )

    def _replay_is_stale(
        self, prior: NodeOutcome, node: Any, spec: Any, invocation: Invocation
    ) -> bool:
        """True when ``prior`` (an executor outcome at this exact key) was
        produced from arguments different from the ones this invocation would
        run with now — the SAME resolution ``node_started`` records as
        ``inputs``. Outcomes without recorded inputs (old rows, skip, manual
        result, an answered pause) are never stale; neither is anything whose
        arguments cannot be resolved here (the fresh run would surface that)."""
        if prior.source not in ("executor", "reused") or not prior.inputs:
            return False
        from matrx_graph.content_ir.markers import reduce_for_ingestion

        try:
            merged = resolve_invocation_inputs(
                node,
                self._with_declared_defaults(invocation.node_id, spec, invocation.inputs),
                run_variables=self._run_variables,
                declared_variables=self.graph.variables,
                run_inputs=self._run_inputs,
                input_surface=self.graph.input_surface,
                run_facts={
                    "id": getattr(prior, "run_id", None) or self._run_facts.get("id"),
                    "workflow_id": self.definition_id,
                    "step_id": node.node_id,
                    "organization_id": self.app.organization_id,
                    "user_id": self.app.user_id,
                },
            )
            merged = reduce_for_ingestion(merged, _input_schema_json(spec.input_schema))
            try:
                current = model_dump_json(
                    spec.input_schema.model_validate(merged),
                    context=f"[wf node={invocation.node_id}] replay inputs",
                )
            except Exception:  # noqa: BLE001 — node_started falls back the same way
                current = dict(merged)
        except Exception:  # noqa: BLE001
            return False
        return current != prior.inputs

    def _candidate_may_run(self, inv: Invocation) -> bool:
        """Side-effect-free twin of ``_candidate_node_gate`` for ONE invocation:
        False when a mandate-candidate run may not execute this node."""
        from matrx_graph.candidate import CANDIDATE_ALLOWED_NODE_TYPES, candidate_ledger
        from matrx_graph.types.primitives import ActionTier

        if candidate_ledger(self.app) is None:
            return True
        spec = self.registry.get(self.graph.nodes[inv.node_id].spec_type).spec
        return (
            spec.determinism == ActionTier.PURE
            or spec.category in (NodeCategory.AGENT, NodeCategory.LLM)
            or spec.node_type in CANDIDATE_ALLOWED_NODE_TYPES
        )

    def _candidate_node_gate(self, invocations: list[Invocation]) -> dict[str, Any] | None:
        """The candidate stop for this step's frontier, or None to run it.

        Off (None) unless the run's AppContext carries the mandate-candidate
        marker. A node may run when its spec is ``ActionTier.PURE``, it is an
        agent / LLM step (its tool calls go through matrx-ai's containment), or
        its type is on the named ``CANDIDATE_ALLOWED_NODE_TYPES`` list.
        Every other node — a side effect, an idempotent write, a
        non-deterministic ``tool.call`` — stops the run; the first such node in
        frontier order is recorded in the shared ledger as the stop.
        """
        from matrx_graph.candidate import (
            CANDIDATE_ALLOWED_NODE_TYPES,
            CandidateStop,
            ToolDisposition,
            args_digest,
            candidate_ledger,
            next_seq,
            record_disposition,
            record_stop,
        )
        from matrx_graph.types.primitives import ActionTier

        ledger = candidate_ledger(self.app)
        if ledger is None:
            return None
        for inv in invocations:
            node = self.graph.nodes[inv.node_id]
            spec = self.registry.get(node.spec_type).spec
            if (
                spec.determinism == ActionTier.PURE
                or spec.category in (NodeCategory.AGENT, NodeCategory.LLM)
                or spec.node_type in CANDIDATE_ALLOWED_NODE_TYPES
            ):
                continue
            seq = next_seq(ledger)
            node_class = f"workflow_node:{spec.determinism.value}"
            reason = (
                f"workflow node '{inv.node_id}' ({node.spec_type}, {spec.category.value}, "
                f"{spec.determinism.value}) is neither PURE, an agent step, nor on the "
                "candidate allow-list"
            )
            record_disposition(
                ledger,
                ToolDisposition(
                    seq=seq,
                    tool=node.spec_type,
                    side_effect_class=node_class,
                    disposition="stopped",
                    args_digest=args_digest(inv.inputs),
                    stopped_reason=reason,
                ),
            )
            stop = CandidateStop(
                step=seq,
                tool=node.spec_type,
                args={"node_id": inv.node_id, "inputs": inv.inputs},
                class_=node_class,
                reason=reason,
            )
            record_stop(ledger, stop)
            logger.warning("[wf candidate] STOPPED at %s", reason)
            return stop.as_record()
        return None

    async def run(
        self,
        run_id: str,
        thread_id: str | None = None,
        inputs: dict[str, Any] | None = None,
        # SAFETY CEILING, NOT A KNOB (census 2026-09-26): bounds super-step DEPTH so a
        # cyclic graph can never spin forever; every run route already lets the caller
        # pass its own (le=100_000). How long an agent inside a step may think is the
        # org knob workflow.run_limits/agent_max_iterations — never this number.
        max_steps: int = 1000,
        node_inputs: dict[str, dict[str, Any]] | None = None,
        max_total_invocations: int = DEFAULT_MAX_TOTAL_INVOCATIONS,
        restarted_after: Literal["server_restart"] | None = None,
        interrupted_attempts: Sequence[InterruptedAttempt] = (),
    ) -> RunResult:
        """Execute a fresh run from the graph's entry nodes.

        ``restarted_after`` / ``interrupted_attempts``: as on :meth:`resume`, for the
        recovery lane restarting a run from its inputs (its server stopped before the
        first checkpoint) — ``run_started`` says why, and the cut-off first steps' spend
        is settled on them.

        ``inputs`` is broadcast to every entry node (legacy / escape-hatch).
        ``node_inputs`` carries per-node payloads keyed by node_id (what the
        generated run form submits — one section per io.user_input node); each
        is merged on top of the broadcast for its addressed entry node.
        """
        thread_id = thread_id or run_id
        # Run once per key: what this run was started with (its subject) — a miss is explained
        # only against earlier answers of runs started with the same inputs (once_step).
        self._once_run_inputs = {"inputs": inputs or {}, "node_inputs": node_inputs or {}}
        await self._resolve_system_context_inputs()
        # ── PARK-NOT-DIE (INPUT-SURFACE.md) ─────────────────────────────────
        # A start missing a require/ask input NEVER crashes: the run parks
        # ``awaiting_input`` — durable, screaming through the normal status
        # announce, resumable the moment anyone supplies the value. This gate
        # runs on EVERY lane (inline, queued worker, detached, subgraph
        # child, trigger) because they all enter here.
        gaps = self._unsatisfied_surface_inputs(inputs, node_inputs)
        if gaps:
            logger.warning(
                "[wf:%s] PARKED awaiting_input — %d required input(s) missing: %s",
                run_id[:8],
                len(gaps),
                ", ".join(g.name for g in gaps),
            )
            return _awaiting_input_result(run_id, thread_id, gaps)
        # A declared variable naming a structured kind is judged against the kind (gap 8): a
        # wrong shape parks the run asking for it again, each problem named — never a step
        # failing later on "{} is not of type 'string'".
        wrong = await self._wrong_shaped_variables(inputs)
        if wrong:
            logger.warning(
                "[wf:%s] PARKED awaiting_input — %d input(s) do not fit their kind: %s",
                run_id[:8],
                len(wrong),
                "; ".join(p for _, problems in wrong for p in problems),
            )
            return _awaiting_input_result(run_id, thread_id, [g for g, _ in wrong], dict(
                (g.name, problems) for g, problems in wrong
            ))
        # Kind-binding admission gate (default OFF — enforcement flags).
        # When workflow_io enforcement is ON, every kind bound by a compiled
        # node must resolve to a live, active, schema-valid registry row
        # BEFORE the run starts: an unknown/inactive kind at binding is fatal
        # at admission. catalog_unreachable stays loudly degraded (an infra
        # outage must never masquerade as validation success OR take down
        # execution — the per-node gates keep the run observable instead).
        await self._enforce_kind_admission(run_id)
        with span(
            "workflow.run",
            run_id=run_id,
            thread_id=thread_id,
            definition_hash=self.graph.definition_hash,
            entry_node_count=len(self.graph.entry_node_ids),
        ) as sp:
            restarted = list(self.graph.entry_node_ids) if restarted_after else []
            await self._emit(
                RunStartedEvent(
                    run_id=run_id,
                    thread_id=thread_id,
                    definition_id=self.definition_id,
                    definition_hash=self.graph.definition_hash,
                    reason=restarted_after,
                    restarted_node_ids=restarted,
                )
            )
            # Fresh run — no buffered joins yet (resume() loads them instead).
            self._pending_bindings = {}
            self._firing_seq = {}
            self._dispatch_expected = {}
            self._node_sems = {}
            self._spend_refusal = None
            self._back_edge_fires = []
            surface_seed = self._surface_node_seed()
            initial = [
                Invocation(
                    node_id=nid,
                    inputs={
                        **self._entry_broadcast(nid, inputs or {}),
                        **surface_seed.get(nid, {}),
                        **(node_inputs or {}).get(nid, {}),
                    },
                )
                for nid in self.graph.entry_node_ids
            ]
            await self._settle_interrupted_attempts(run_id, 0, initial, restarted, interrupted_attempts)
            # THE WORKFLOW CHAIN (lane CHAIR-RECORD-CHANGED): every store write a step makes
            # carries this run id — one level below the record change that started the run,
            # when one did — so a record-changed consumer can cap a chain and see a loop.
            chain = workflow_chain_for_run(
                run_id, ((inputs or {}).get("trigger") or {}).get("chain")
                if isinstance((inputs or {}).get("trigger"), dict) else None
            )
            from matrx_graph.executor.execution import Execution, executing

            self._history_known_empty = self._fresh_history
            try:
                # THE LEG IN MEMORY (lane 11 round 5): a FRESH leg on THIS compiled graph.
                with declaring_workflow_chain(chain), executing(
                    Execution(run_id=run_id, definition_hash=str(self.graph.definition_hash),
                              graph=self.graph, fresh=True)
                ):
                    result = await self._drive(
                        run_id=run_id,
                        thread_id=thread_id,
                        pending=initial,
                        start_step=0,
                        parent_checkpoint_id=None,
                        max_steps=max_steps,
                        max_total_invocations=max_total_invocations,
                    )
            except Exception as e:
                record_exception(sp, e)
                raise
            finally:
                self._history_known_empty = False
            set_attributes(
                sp,
                **{
                    "workflow.status": result.status.value,
                    "workflow.steps_executed": result.steps_executed,
                },
            )
            return result

    def _entry_broadcast(self, node_id: str, inputs: dict[str, Any]) -> dict[str, Any]:
        """The part of the run's ``inputs`` an ENTRY step is handed as its payload.

        A name that is one of the workflow's DECLARED VARIABLES is a run-level value, not
        an argument of every entry step: it is handed to an entry step only when that step TAKES
        the name (``_entry_takes``: a declared input, or an extra its model says it reads — Find
        Records' ``match`` reading ``$in.<name>``); an open step that does not say which extras
        it reads (a transform reading ``inputs['audience']``) gets it as before. Otherwise it stays
        where it belongs — a run input any step reads with ``{"$input": name}`` /
        ``{"$var": name}``. Every start door (API, MCP, triggers, ``subgraph.call``,
        mandate holder, plan resolver) enters through ``run()``, so they all get this.

        Live defect 2026-10-27: "Choose pages to read" started over MCP with
        ``{"brand_id", "kinds_first", "max_pages"}`` died at its entry step
        ``web.stored_pages.read`` (``extra="forbid"``) because ``kinds_first`` and
        ``max_pages`` — read by later steps — were copied into it; the Studio form
        (``initial_variables``) worked. A name that is NOT a declared variable keeps
        today's behaviour (broadcast), so a strict step still refuses a typo.
        """
        declared = {
            name for name, s in self.graph.input_surface.items()
            if getattr(s, "origin", None) == "variable"
        } | set(self.graph.variables)
        if not inputs or not declared.intersection(inputs):
            return inputs
        try:
            spec = self.registry.get(self.graph.nodes[node_id].spec_type).spec
        except Exception:  # noqa: BLE001 — unknown type fails loudly at dispatch, not here
            return inputs
        takes = self._entry_takes(node_id, getattr(spec, "input_schema", None))
        if takes is None:
            # An open step (a transform reading inputs[...]) may read any run input
            # from its payload — unchanged.
            return inputs
        handed: dict[str, Any] = {}
        for name, value in inputs.items():
            if name in declared and name not in takes:
                # Still a run input: {"$input": name} on any step resolves it.
                if self._run_inputs.get(name) is None and value is not None:
                    self._run_inputs[name] = value
                continue
            handed[name] = value
        return handed

    def _entry_takes(self, node_id: str, schema: Any) -> set[str] | None:
        """The input names an entry step takes in its payload; None when it takes any name.

        Its declared fields, plus the extras its input model says it reads from the step's
        authored inputs (``matrx_graph.nodes._template.extras_read`` — the same rule the model's
        own typo refusal applies). Live defect 2026-10-28: Find Records (open only for what
        ``match`` reads as ``$in.<name>``) as a workflow's first step was handed every declared
        setting and refused them all as misspelled settings."""
        # An 'Only when' gate (``<step>~when``) stands in for its step at the start of the run:
        # it receives what the STEP takes and forwards it to the step, so it takes exactly
        # the step's names — an open gate handed every declared run input forwarded them
        # into a closed step, which refused them (2026-10-28). The condition still reads the
        # run inputs (``_only_when_view``).
        owner = when_gate_owner(node_id)
        if owner is not None and owner in self.graph.nodes:
            try:
                schema = self.registry.get(self.graph.nodes[owner].spec_type).spec.input_schema
            except Exception:  # noqa: BLE001 — unknown type fails loudly at dispatch, not here
                return None
            node_id = owner
        if schema is None:
            return None
        from matrx_graph.nodes._template import extras_read

        reads = extras_read(schema, self.graph.nodes[node_id].static_inputs or {})
        if reads is None:
            return None
        return set(getattr(schema, "model_fields", {}) or {}) | reads

    def _only_when_view(self, source_id: str, payload: Any) -> Any:
        """What an 'Only when' condition reads: the step's inputs, over the run's inputs.

        The gate carries what the step receives (its connections and its own authored inputs,
        ``{"$input": name}`` included). A closed step does not take every run input, so the
        gate cannot carry those; the condition still reads them here — the payload wins on a
        name both hold. Any other conditional connection reads only its source's output."""
        if when_gate_owner(source_id) is None or not isinstance(payload, dict):
            return payload
        run_inputs = {k: v for k, v in self._run_inputs.items() if v is not None}
        if not run_inputs:
            return payload
        return {**run_inputs, **payload}

    def _with_declared_defaults(
        self, node_id: str, spec: Any, inputs: dict[str, Any]
    ) -> dict[str, Any]:
        """An ENTRY step's run inputs with every declared input the caller left out filled.

        Entry steps receive the run's inputs as their payload, so a declared input's default
        (``definition.variables``) must be in that payload exactly as if the caller had sent
        it — on every door: a top-level start, a ``subgraph.call`` child called by name
        without the argument, and a resume/retry that replays the entry invocation (the
        fill happens at resolution, not only at the first dispatch). Live defect
        2026-10-27: "Structure material into an outline" declared ``audience`` default
        ``"general"``, a caller omitted it, and the entry transform died on
        ``KeyError: 'audience'``. A value the caller DID send wins; a landed surface value
        (pinned / mandate default) wins over the declared default; a name the step itself
        authors in ``static_inputs`` is left to that authored value. A step that says which
        names it takes (``_entry_takes``) only gets those, so a default never turns into an
        "extra input" refusal.
        """
        if node_id not in self.graph.entry_node_ids:
            return inputs
        takes = self._entry_takes(node_id, getattr(spec, "input_schema", None))
        authored = self.graph.nodes[node_id].static_inputs or {}
        filled: dict[str, Any] | None = None
        for name, surface in self.graph.input_surface.items():
            if getattr(surface, "origin", None) != "variable":
                continue
            if inputs.get(name) is not None or (takes is not None and name not in takes):
                continue
            # The payload overlays authored static inputs, so a fill here would beat the
            # step's own `{"$var": name, "default": ...}` (or literal) for the same name.
            if name in authored:
                continue
            landed = self._run_inputs.get(name)
            value = landed if landed is not None else getattr(surface, "default", None)
            if value is None:
                continue
            if filled is None:
                filled = dict(inputs)
            filled[name] = value
        return inputs if filled is None else filled

    async def _wrong_shaped_variables(self, inputs: dict[str, Any] | None) -> list[tuple[Any, list[str]]]:
        """Each declared variable naming a structured kind whose landed value misses it, with
        the problems (``kinds.input_kind_problems``). A plain-valued kind is never judged here."""
        from matrx_graph.kinds import input_kind_problems, structured_kind_schema
        from matrx_graph.types.input_surface import missing_value, structured_input_kind

        declared = self.graph.variables
        wrong: list[tuple[Any, list[str]]] = []
        for name, spec in self.graph.input_surface.items():
            var = declared.get(name)
            if spec.origin != "variable" or var is None:
                continue
            slug = structured_input_kind(var.kind, var.effective_type())
            if slug is None:
                continue
            value = next(
                (
                    v
                    for v in (self._run_inputs.get(name), self._run_variables.get(name), (inputs or {}).get(name))
                    if not missing_value(v)
                ),
                None,
            )
            if value is None or await structured_kind_schema(slug) is None:
                continue
            problems = await input_kind_problems(name, value, slug, multiple=var.multiple)
            if problems:
                wrong.append((spec, problems))
        return wrong

    def _surface_node_seed(self) -> dict[str, dict[str, Any]]:
        """Per-node seed payloads derived from the landed surface values —
        {node_id: {field_key: value}} for every origin='field' surface entry
        with a landed value. What lets a caller address the ONE surface
        (name → value) while the engine keeps seeding io.user_input nodes
        exactly as before."""
        seed: dict[str, dict[str, Any]] = {}
        if not self._run_inputs:
            return seed
        for name, spec in self.graph.input_surface.items():
            if spec.node_id is None or spec.field_key is None:
                continue
            if name in self._run_inputs and self._run_inputs[name] is not None:
                seed.setdefault(spec.node_id, {})[spec.field_key] = self._run_inputs[name]
        return seed

    def _unsatisfied_surface_inputs(
        self,
        inputs: dict[str, Any] | None,
        node_inputs: dict[str, dict[str, Any]] | None,
    ) -> list[Any]:
        """The require/ask surface entries this start cannot satisfy.

        Values are gathered from every channel a start can land them on:
        the resolved surface values, the legacy broadcast ``inputs``, the
        legacy per-node ``node_inputs``, and (for folded variables) the run
        variables. Provenance comes from the start seam's stamps; legacy
        channels carry no stamp and so never satisfy an ``ask`` (a human
        answers every time — through the stamped path)."""
        from matrx_graph.types.input_surface import unsatisfied_inputs

        surface = self.graph.input_surface
        if not surface:
            return []
        values: dict[str, Any] = {}
        for name, spec in surface.items():
            candidates = (
                self._run_inputs.get(name),
                ((node_inputs or {}).get(spec.node_id or "", {}) or {}).get(spec.field_key or ""),
                (inputs or {}).get(name),
                self._run_variables.get(name) if spec.origin == "variable" else None,
            )
            for candidate in candidates:
                if candidate is not None and candidate != "":
                    values[name] = candidate
                    break
        return unsatisfied_inputs(surface, values, self._input_provenance)

    async def _enforce_kind_admission(self, run_id: str) -> None:
        """Fatal kind-binding admission (enforcement flags, default OFF).

        No-op unless ``KIND_ENFORCEMENT["workflow_io"]`` is True. When ON,
        resolves every distinct ``input_kind``/``output_kind`` bound across
        the compiled graph and raises ``ExecutionError`` naming EVERY fatal
        binding (unregistered / inactive / missing or malformed schema) —
        per the documented matrix, ``catalog_unreachable`` never blocks
        admission: it logs loudly and the run proceeds in named degraded
        mode (the per-node gates keep the skip visible, never a pass).
        """
        from matrx_graph.kinds import (
            KindDegradedReason,
            degraded_escalation,
            kind_enforcement_enabled,
            resolve_kind,
        )

        if not kind_enforcement_enabled("workflow_io"):
            return
        bound: dict[str, list[str]] = {}
        for node in self.graph.nodes.values():
            for slug in (node.input_kind, node.output_kind):
                if slug is not None:
                    bound.setdefault(slug, []).append(node.node_id)
        fatal: list[str] = []
        for slug, node_ids in sorted(bound.items()):
            entry, reason = await resolve_kind(slug)
            if reason is KindDegradedReason.CATALOG_UNREACHABLE:
                logger.error(
                    "[wf:%s] kind admission: catalog unreachable while "
                    "resolving '%s' (nodes: %s) — run proceeds in DEGRADED "
                    "mode (degraded_reason=%s); an infra outage never blocks "
                    "admission and never counts as a pass.",
                    run_id[:8],
                    slug,
                    ", ".join(node_ids),
                    reason.value,
                )
                continue
            if reason is not None and degraded_escalation(reason) == "fatal":
                fatal.append(
                    f"'{slug}' (nodes: {', '.join(node_ids)}): degraded_reason={reason.value}"
                )
            # NO `is_active` GATE. The engine ignores the frontend's dual-gate
            # flag in every mode (Arman, 2026-08-25 — see
            # `matrx_graph.kinds.degraded_escalation` note 1). Enforcing it
            # here would have made turning enforcement on start honoring a
            # flag the engine has never honored.
        if fatal:
            raise ExecutionError(
                "Kind enforcement (workflow_io) is ON and this run's kind "
                "bindings failed admission:\n  - " + "\n  - ".join(fatal)
            )

    def _fold_client_payload(
        self,
        next_invocations: Sequence[Any],
        recorded_value: dict[str, Any],
    ) -> dict[str, Any]:
        """Put client-authored keys in the interrupted node's ``extras`` map.

        No-op unless the node's output model declares ``extras`` — see
        ``matrx_graph.executor.client_payload``.
        """
        if not next_invocations:
            return recorded_value
        interrupted = next(
            (ni for ni in next_invocations if ni.is_interrupted), next_invocations[0]
        )
        node = self.graph.nodes.get(interrupted.node_id)
        if node is None:
            return recorded_value
        try:
            output_model = self.registry.get(node.spec_type).spec.output_schema
        except Exception:  # noqa: BLE001 — an unknown spec must never kill a resume
            return recorded_value
        return fold_undeclared_into_extras(
            recorded_value, output_model, reserved=frozenset({DECISION_KEY, "decision"})
        )

    async def _resolve_system_context_inputs(self) -> None:
        """Replace every ``{"$system_context": key}`` input value with the item's current value
        (``matrx_graph.system_values``), for the run's organization. Runs before the first step of a
        fresh run and of every resume, so a default always reads the item as it is now."""
        from matrx_graph.system_values import is_system_context_ref, resolve_system_context_values

        # A pointer default nobody landed (a lane that skipped the start seam) lands here, so no
        # step ever falls back to the pointer itself.
        for name, spec in self.graph.input_surface.items():
            if is_system_context_ref(getattr(spec, "default", None)) and self._run_inputs.get(name) is None:
                self._run_inputs[name] = spec.default
        organization_id = getattr(self.app, "organization_id", None)
        self._run_inputs = await resolve_system_context_values(
            self._run_inputs, organization_id=organization_id
        )
        self._run_variables = await resolve_system_context_values(
            self._run_variables, organization_id=organization_id
        )

    async def resume(
        self,
        run_id: str,
        checkpoint_id: str,
        resume_value: dict[str, Any] | None = None,
        max_steps: int = 1000,
        stop_after_steps: int | None = None,
        select_node_ids: set[str] | None = None,
        max_total_invocations: int = DEFAULT_MAX_TOTAL_INVOCATIONS,
        decision: DecisionProvenance | None = None,
        restarted_after: Literal["server_restart"] | None = None,
        interrupted_attempts: Sequence[InterruptedAttempt] = (),
    ) -> RunResult:
        """Resume a run from a previous checkpoint.

        ``restarted_after`` (the host's recovery lane only): the server running this leg
        stopped mid-step, so the steps at the checkpoint's frontier were cut off and start
        again. The resume announces that on ``run_resumed`` and settles each of
        ``interrupted_attempts`` — the dead attempts' ledger spend — as that step's
        ``interrupted`` node_cost, so neither the reason nor the money is lost.

        If the checkpoint has `interrupt_payload`, resume_value is recorded as
        the output of the interrupted node (so downstream routing proceeds as
        though the user had answered in-place). Otherwise resume_value is
        ignored and we re-enter the super-step loop at `next_invocations`.

        ``decision`` is WHO authored this answer, supplied by the authenticated
        admission seam (the HTTP route knows the signed-in human; the
        escalation worker knows the agent). It is stamped onto the recorded
        output under ``matrx_decision`` and any caller-supplied stamp is
        discarded — provenance is never client-authored. Omitted, any stamp in
        the value is stripped: the queued lane's trusted stamp rides the job
        row (``enqueue(decision=...)``) and arrives here as ``decision``.

        ``stop_after_steps`` (step-mode): park the run as PAUSED after this many
        super-steps instead of running to completion — e.g. ``1`` executes a
        single super-step then parks at the resulting frontier. ``select_node_ids``
        (step-mode): on the FIRST super-step only, run just these frontier nodes
        and defer the rest, merging the deferred siblings back into the next
        frontier. Together they power "run exactly this one node, persist its
        result, and stop" without a second execution path.
        """
        await self._resolve_system_context_inputs()
        # Same kind-binding admission gate as run() (idempotent, no-op unless
        # workflow_io enforcement is ON) — without this, a parked run that
        # resumes would bypass fatal binding admission entirely.
        await self._enforce_kind_admission(run_id)
        checkpoint = await self.checkpointer.load_checkpoint(checkpoint_id)
        if checkpoint is None:
            raise ExecutionError(f"Checkpoint '{checkpoint_id}' not found for resume.")
        if checkpoint.run_id != run_id:
            raise ExecutionError(
                f"Checkpoint '{checkpoint_id}' belongs to run "
                f"'{checkpoint.run_id}', not '{run_id}'."
            )
        # RESUME PRE-FLIGHT (executor/resume_preflight.py): a checkpoint that
        # can PROVABLY never finish on this graph (an edge added behind a step
        # that will not run again) is refused before any step runs, instead of
        # doing the remaining work and parking in a join deadlock. Refuses only
        # on proof; every launch mechanism the engine has counts as "can run".
        problems = resume_preflight_problems(self.graph, checkpoint, self.registry)
        if problems:
            raise ResumeCannotFinishError(problems)
        # The reserved provenance key is ENGINE state, never part of the
        # author's answer schema — a schema with additionalProperties:false
        # would otherwise reject every stamped resume.
        # A polling park (``re_execute`` in its sleep marker, nodes/flow/sleep.py)
        # is never answered by a value: every wake — timed, "resume now", the
        # recovery sweep — RE-RUNS the parked step, which asks the world again
        # and either returns or parks anew. No outcome is recorded for it here,
        # so its invocation (already on the frontier, at this step) executes
        # fresh instead of replaying a value from park time.
        from matrx_graph.nodes.flow.sleep import re_executes_on_wake

        re_execute = re_executes_on_wake(checkpoint.interrupt_payload)
        resume_value = _settle_default_on_decision_gate(
            checkpoint.interrupt_payload, resume_value, decision
        )
        # A QUESTION THAT WAS ALREADY ANSWERED is resumed with NO value by recovery
        # (a server died after the person answered, before the next checkpoint):
        # the latest checkpoint is still the question's, but the answer exists. For
        # a step's own question it is the recorded outcome, replayed below; for a
        # relayed question (a called workflow asked) the step runs again with no
        # answer and its child decides — it continues, or the step asks again.
        # Never validated as an empty answer (that burned the run), never recorded
        # over the real one. A person's resume always carries a value.
        no_value = not resume_value and decision is None and bool(checkpoint.interrupt_payload)
        rerun_without_answer = no_value and forwards_answer(checkpoint.interrupt_payload)
        answered_already = (
            no_value
            and not re_execute
            and not rerun_without_answer
            and await park_was_answered(self.checkpointer, checkpoint)
        )
        validation_target = {k: v for k, v in (resume_value or {}).items() if k != DECISION_KEY}
        resume_errors = [] if (re_execute or rerun_without_answer or answered_already) else (
            resume_value_validation_errors(checkpoint.interrupt_payload, validation_target)
        )
        if resume_errors:
            raise ExecutionError(
                "Resume value does not satisfy the interrupted node's schema:\n  - "
                + "\n  - ".join(resume_errors)
            )

        self.channels.load_values(checkpoint.channel_values)

        # Reload the join accumulator (ENGINE_SPEC §3.8): partial inbound
        # bindings buffered at park time resume filling exactly where they
        # left off. Deep-copied — the loaded checkpoint stays immutable
        # history while the live accumulator mutates.
        self._pending_bindings = {
            node_id: binding.model_copy(deep=True)
            for node_id, binding in checkpoint.pending_bindings.items()
        }
        # Firing counters MUST stay monotonic across resume (ENGINE_SPEC
        # §3.8 / F5). Pending entries alone are not enough — a firing whose
        # entry was consumed (and possibly already executed) before the park
        # would reset its node's counter to 0 and the next firing would
        # REUSE its number. Restore from the max observed anywhere durable:
        # this checkpoint's entries + every historical checkpoint's entries
        # and frontier invocations (each accumulator-fired NextInvocation
        # carries its firing number).
        self._firing_seq = {
            node_id: binding.firing for node_id, binding in checkpoint.pending_bindings.items()
        }
        for ni in checkpoint.next_invocations:
            if ni.firing > self._firing_seq.get(ni.node_id, 0):
                self._firing_seq[ni.node_id] = ni.firing
        try:
            history = await self.checkpointer.list_checkpoints(run_id)
        except Exception:  # noqa: BLE001 — history is a monotonicity aid, never fatal
            logger.warning(
                "[wf:%s] list_checkpoints failed on resume — firing counters "
                "restored from the resume checkpoint only",
                run_id[:8],
                exc_info=True,
            )
            history = []
        for cp in history:
            for node_id, binding in cp.pending_bindings.items():
                if binding.firing > self._firing_seq.get(node_id, 0):
                    self._firing_seq[node_id] = binding.firing
            for ni in cp.next_invocations:
                if ni.firing > self._firing_seq.get(ni.node_id, 0):
                    self._firing_seq[ni.node_id] = ni.firing
        self._node_sems = {}
        self._spend_refusal = None
        self._back_edge_fires = []

        # Rebuild the fan-out dispatch registry (§4.4) from durable state:
        # (a) a partially-delivered fan-in group persisted its expected count
        # on the binding entry; (b) a dispatch whose items are all still on
        # the frontier (park before any delivery) is counted from the
        # frontier's fanned invocations. An unknown group can never resolve —
        # the end-of-run join-deadlock guard screams rather than completing
        # silently (§12.8).
        self._dispatch_expected = {}
        for binding in checkpoint.pending_bindings.values():
            if not binding.expected_items:
                continue
            for eb in binding.edges.values():
                if eb.dispatch_id:
                    self._dispatch_expected.setdefault(
                        (eb.dispatch_id, eb.source_node_id), binding.expected_items
                    )
        frontier_counts: dict[tuple[str, str], int] = {}
        for ni in checkpoint.next_invocations:
            if ni.dispatch_id:
                key = (ni.dispatch_id, ni.node_id)
                frontier_counts[key] = frontier_counts.get(key, 0) + 1
        for key, count in frontier_counts.items():
            self._dispatch_expected.setdefault(key, count)

        self._forwarded_answers = {}
        if checkpoint.interrupt_payload and forwards_answer(checkpoint.interrupt_payload):
            # The question belongs to a run this step is waiting on (a called
            # workflow). The answer is HANDED to the step when it runs again —
            # never recorded as its output — so the step re-executes (no outcome
            # exists at its key) and passes it to the run that asked. Validation
            # above already held it to the relayed question's schema; WHO decided
            # travels with it untouched, for the asking run to stamp.
            interrupted = next(
                (ni for ni in checkpoint.next_invocations if ni.is_interrupted),
                checkpoint.next_invocations[0] if checkpoint.next_invocations else None,
            )
            if interrupted is not None and not rerun_without_answer:
                self._forwarded_answers[
                    (interrupted.node_id, interrupted.dispatch_id, interrupted.item_index)
                ] = ResumeAnswer(value=None if re_execute else resume_value, decision=decision)
        elif checkpoint.interrupt_payload and not re_execute and not answered_already:
            # WHO decided is recorded in the same row as WHAT was decided —
            # provenance that cannot drift from its answer.
            recorded_value = (
                stamp_decision(resume_value, decision)
                if decision is not None
                else sanitize_decision_value(resume_value)
            )
            # A CLIENT-authored resume payload may carry keys the node never
            # declared. They belong in the node's declared ``extras`` map, not
            # at the root where nothing can know to look for them (Arman's
            # ruling, 2026-08-21) — that root spread is what stopped these
            # nodes from ever declaring an honest output kind. Opt-in: nodes
            # without an ``extras`` field are returned untouched.
            # THE HUMAN GATE (decision preset): the engine — never the client —
            # joins the DURABLE spec with the answers, so every write target
            # downstream is the author's, and a client-sent ``decision`` key is
            # discarded rather than trusted.
            client_decision = recorded_value.pop("decision", None)
            gate_spec = checkpoint.interrupt_payload.get("decision")
            if isinstance(gate_spec, dict):
                recorded_value["decision"] = resolve_decision(gate_spec, recorded_value)
            elif client_decision is not None:
                # Not a gate: a client key that happens to be named "decision"
                # is kept, one level down, like any other undeclared key.
                extras = recorded_value.get("extras")
                extras = dict(extras) if isinstance(extras, dict) else {}
                extras.setdefault("decision", client_decision)
                recorded_value["extras"] = extras
            if checkpoint.interrupt_payload.get("preset") == "list" and "answer" in recorded_value:
                # The list preset: the person edited lines; the step's answer is the list.
                from matrx_graph.nodes.control.human_input import list_answer

                recorded_value["answer"] = list_answer(recorded_value["answer"])
            recorded_value = self._fold_client_payload(checkpoint.next_invocations, recorded_value)
            # The interrupted node needs to appear "as if completed" so
            # downstream edges fire with resume_value as its output. We record
            # the outcome now; the pending invocations list already reflects
            # what should fire next. The frontier carries MORE than the
            # interrupted node (§6.2 — completed siblings' routed downstream,
            # deferred/errored siblings), so the marked invocation is
            # authoritative; ``next_invocations[0]`` is only the pre-§6.2
            # checkpoint fallback (old rows never marked, but also only ever
            # stored the interrupted invocation, first).
            if checkpoint.next_invocations:
                interrupted = next(
                    (ni for ni in checkpoint.next_invocations if ni.is_interrupted),
                    checkpoint.next_invocations[0],
                )
                await self.checkpointer.record_outcome(
                    NodeOutcome(
                        run_id=run_id,
                        step=checkpoint.step,
                        node_id=interrupted.node_id,
                        attempt=interrupted.attempt,
                        dispatch_id=interrupted.dispatch_id,
                        item_index=interrupted.item_index,
                        output=recorded_value,
                    )
                )

        pending = []
        for ni in checkpoint.next_invocations:
            if ni.blocked_join:
                # Blocked-join park invocation (ENGINE_SPEC §3.4 Amendment
                # D2b). It runs ONLY when the user acted on it since the
                # park: skip / manual-result recorded an outcome at its
                # correlation key, or retry bumped its attempt. Untouched,
                # it stays represented by pending_bindings (filtered out
                # here) and the end-of-run deadlock guard re-parks the SAME
                # state — resume of an unchanged deadlock is a no-progress
                # no-op, never a partial fire.
                acted = ni.attempt > 1
                if not acted:
                    prior = await self.checkpointer.get_outcome(
                        run_id=run_id,
                        step=checkpoint.step,
                        node_id=ni.node_id,
                        attempt=ni.attempt,
                        dispatch_id=ni.dispatch_id,
                        item_index=ni.item_index,
                    )
                    acted = prior is not None
                    if acted:
                        from matrx_graph.executor.execution import note_replayed

                        note_replayed(run_id, ni.node_id)
                if not acted:
                    continue
                # The user resolved the deadlock through THIS invocation —
                # it is now authoritative for the blocked firing; consume
                # the buffered entry so the deadlock guard stands down.
                self._pending_bindings.pop(ni.node_id, None)
            pending.append(
                Invocation(
                    node_id=ni.node_id,
                    inputs=ni.inputs,
                    attempt=ni.attempt,
                    dispatch_id=ni.dispatch_id,
                    item_index=ni.item_index,
                    config_override=ni.config_override,
                    blocked_join=ni.blocked_join,
                    firing=ni.firing,
                    loop_stack=[dict(f) for f in ni.loop_stack],
                    work_item_id=ni.work_item_id,
                    step=ni.step if ni.step is not None else checkpoint.step,
                    bypass_once=ni.bypass_once,
                )
            )
        # On interrupt-resume, the recorded outcome lives at the SAME step as
        # the interrupt checkpoint, because we're "completing" the interrupted
        # node virtually via the user's resume value. Start at checkpoint.step
        # so the idempotency check finds it; on non-interrupt resume, the
        # next_invocations are already keyed to run at checkpoint.step as the
        # next super-step.
        # Each frontier invocation carries the step it is scheduled for
        # (NextInvocation.step); the run restarts at the earliest of them and
        # the loop holds the rest until their step — an end-of-step checkpoint
        # (saved at N, frontier for N+1) resumes at N+1, exactly where the
        # original run keyed those nodes, so finished work replays.
        start_step = min((inv.step for inv in pending if inv.step is not None), default=checkpoint.step)
        if select_node_ids:
            # Step-mode runs the SELECTED nodes on the first step — start at
            # their step, or a node scheduled for N+1 (an interrupt's routed
            # successor) would be held and the step would run empty. The
            # unselected keep their own steps and run later at those keys.
            selected_steps = [
                inv.step
                for inv in pending
                if inv.node_id in select_node_ids and inv.step is not None
            ]
            if selected_steps:
                start_step = min(selected_steps)
        with span(
            "workflow.resume",
            run_id=run_id,
            thread_id=checkpoint.thread_id,
            checkpoint_id=checkpoint.checkpoint_id,
            from_step=start_step,
        ) as sp:
            # THE resumed-status transition on the run's OWN event stream.
            # Every other lifecycle transition announces itself here
            # (run_started / run_paused / run_interrupted / run_errored /
            # run_completed / run_failed / run_cancelled); paused→running
            # announced nothing, so a client folding this stream held the
            # pre-resume status — "PAUSED" — for the whole resumed leg while
            # its nodes visibly executed, and only a reload showed truth.
            # Emitted at the ONE seam every resume lane funnels through
            # (resume-paused, interrupt-resume, the recovery legs, the queued
            # worker, subgraph children), after the checkpoint has validated
            # so a rejected resume never announces one.
            #
            # ``mode`` is what this seam can honestly know: the checkpoint
            # carries an interrupt payload or it does not. The recovery
            # entry points (skip / manual / retry) resume from an errored
            # park and so report "pause" — cosmetic copy only; nothing keys
            # behavior off it.
            # The steps that start AGAIN: the frontier due on the first resumed step. A
            # frontier invocation held for a later step had not started when the server
            # stopped, so it is not restarting.
            restarted = (
                list(dict.fromkeys(inv.node_id for inv in pending if inv.step == start_step))
                if restarted_after
                else []
            )
            await self._emit(
                RunResumedEvent(
                    run_id=run_id,
                    from_checkpoint_id=checkpoint.checkpoint_id,
                    mode="interrupt" if checkpoint.interrupt_payload else "pause",
                    reason=restarted_after,
                    restarted_node_ids=restarted,
                )
            )
            await self._settle_interrupted_attempts(
                run_id, start_step, pending, restarted, interrupted_attempts
            )
            from matrx_graph.executor.execution import Execution, executing
            from matrx_graph.executor.resume_chain import resumed_chain_cause

            try:
                # A resumed leg's chain comes from the change that started the run, read by
                # the host from the store's outbox (configure_resume_chain_resolver) — never
                # a fresh root, which reset the loop depth (lane 11 round 5). And the leg is
                # recorded in memory as NOT fresh: it was loaded from a checkpoint.
                caused_by = await resumed_chain_cause(run_id)
                with declaring_workflow_chain(workflow_chain_for_run(run_id, caused_by)), executing(
                    Execution(run_id=run_id, definition_hash=str(self.graph.definition_hash),
                              graph=self.graph, fresh=False)
                ):
                    result = await self._drive(
                        run_id=run_id,
                        thread_id=checkpoint.thread_id,
                        pending=pending,
                        start_step=start_step,
                        parent_checkpoint_id=checkpoint.checkpoint_id,
                        max_steps=max_steps,
                        stop_after_steps=stop_after_steps,
                        select_node_ids=select_node_ids,
                        max_total_invocations=max_total_invocations,
                        resumed_from_step=checkpoint.step,
                    )
            except Exception as e:
                record_exception(sp, e)
                raise
            set_attributes(
                sp,
                **{
                    "workflow.status": result.status.value,
                    "workflow.steps_executed": result.steps_executed,
                },
            )
            return result

    async def _park_paused(
        self,
        *,
        run_id: str,
        thread_id: str,
        step: int,
        start_step: int,
        parent_checkpoint_id: str | None,
        pending: list[Invocation],
        last_outputs: dict[str, Any],
    ) -> RunResult:
        """Save the current frontier as a checkpoint and return PAUSED.

        The shared park path for an explicit user pause AND for the step-mode
        ``stop_after_steps`` budget. Resume-from-pause re-enters ``_drive`` at
        this checkpoint's ``next_invocations``.
        """
        cp_id = await self._save_checkpoint(
            run_id=run_id,
            thread_id=thread_id,
            step=step,
            parent_checkpoint_id=parent_checkpoint_id,
            next_invocations=_as_next_invocations(pending, step),
        )
        await self._emit(
            RunPausedEvent(
                run_id=run_id,
                steps_executed=step - start_step,
                checkpoint_id=cp_id,
            )
        )
        return RunResult(
            run_id=run_id,
            thread_id=thread_id,
            status=RunStatus.PAUSED,
            steps_executed=step - start_step,
            channel_values=self.channels.snapshot(),
            last_outputs=last_outputs,
        )

    async def _drive(
        self,
        run_id: str,
        thread_id: str,
        pending: list[Invocation],
        start_step: int,
        parent_checkpoint_id: str | None,
        max_steps: int,
        stop_after_steps: int | None = None,
        select_node_ids: set[str] | None = None,
        max_total_invocations: int = DEFAULT_MAX_TOTAL_INVOCATIONS,
        resumed_from_step: int | None = None,
    ) -> RunResult:
        # ``resumed_from_step``: the step of the checkpoint a RESUMED leg starts from (None on a
        # fresh run). That leg's ``last_outputs`` holds only its own steps, so its completion adds
        # what earlier legs settled at or before that step (``_with_earlier_outputs``).
        #
        # THE PUBLISHED-MEDIA SCOPE. Both entry points (`run` and `resume`)
        # funnel through here, so declaring it once covers the whole graph —
        # every node, every resume segment, and (ContextVar semantics) every
        # task those nodes create.
        #
        # A workflow whose output is published needs its media born PUBLIC. A
        # personal image's only URL is a signed grant that expires, and a node
        # output is written to `workflow.node_outcome` and read back days
        # later, so persisting private-then-publishing leaves a dead link in
        # the durable record. Podcast W7 shipped exactly that defect: 51
        # outcome rows carrying `…&AWSAccessKeyId=…&Signature=…`, because a
        # published workflow had no way to say what a published Python
        # pipeline says with `public_media_scope()`. This is that way.
        with ExitStack() as media_scope:
            if self.graph.public_media:
                media_scope.enter_context(public_media_scope())
            # Step-mode keeps the plain barrier: "run exactly this node and
            # stop" must never start what comes after it.
            self._run_ahead_on = (
                self._run_ahead_allowed and stop_after_steps is None and select_node_ids is None
            )
            self._run_ahead_step_limit = start_step + max_steps
            self._pause_latched = False
            self._cancel_latched = False
            self._last_stop_poll = float("-inf")
            try:
                return await self._drive_inner(
                    run_id,
                    thread_id,
                    pending,
                    start_step,
                    parent_checkpoint_id,
                    max_steps,
                    stop_after_steps,
                    select_node_ids,
                    max_total_invocations,
                    resumed_from_step,
                )
            finally:
                # Completion adopts every launch; anything left belongs to a
                # run that stopped (park, cancel, failure) — cancel it, never
                # make the stop wait for it. Whatever finished is recorded and
                # replays when the step runs; the rest runs then.
                await self._cancel_run_ahead(run_id)
                if self._deferred_outcomes:
                    await self._flush_deferred_outcomes()

    async def _drive_inner(
        self,
        run_id: str,
        thread_id: str,
        pending: list[Invocation],
        start_step: int,
        parent_checkpoint_id: str | None,
        max_steps: int,
        stop_after_steps: int | None = None,
        select_node_ids: set[str] | None = None,
        max_total_invocations: int = DEFAULT_MAX_TOTAL_INVOCATIONS,
        resumed_from_step: int | None = None,
    ) -> RunResult:
        step = start_step
        last_outputs: dict[str, Any] = {}
        # Width guard: max_steps bounds DEPTH (super-steps) only — one map of
        # 10k items is a single step. This counter bounds total node
        # invocations across the drive segment so a Send-amplifying graph
        # (waves, loops, work queues) cannot fan out unbounded. Counted per
        # drive segment (each resume gets a fresh budget — history is not
        # replayed to reconstruct it); terminal FAILED like max_steps.
        total_invocations = 0

        try:
            while pending:
                if step - start_step >= max_steps:
                    raise ExecutionError(
                        f"Run '{run_id}' exceeded max_steps={max_steps}. "
                        f"Suspected infinite loop in graph."
                    )
                total_invocations += len(pending)
                self._run_ahead_budget = max_total_invocations - total_invocations
                if total_invocations > max_total_invocations:
                    raise ExecutionError(
                        f"Run '{run_id}' exceeded max_total_invocations="
                        f"{max_total_invocations} ({total_invocations} node "
                        "invocations scheduled this session). A dispatcher is "
                        "fanning out more work than the run-wide budget allows "
                        "— raise the cap deliberately on the run request, or "
                        "bound the fan-out at its source (max_dispatches / "
                        "max_iterations / work-queue batch size)."
                    )

                # Step-mode budget (NEW). Park as PAUSED once the requested
                # number of super-steps has run, instead of continuing to
                # completion. max_steps can NOT do this — it raises and goes
                # terminal FAILED; the pause convention is the correct park so
                # resume-paused re-enters cleanly.
                if stop_after_steps is not None and (step - start_step) >= stop_after_steps:
                    return await self._park_paused(
                        run_id=run_id,
                        thread_id=thread_id,
                        step=step,
                        start_step=start_step,
                        parent_checkpoint_id=parent_checkpoint_id,
                        pending=pending,
                        last_outputs=last_outputs,
                    )

                # Pause poll (NEW). Takes priority over cancel — the user
                # explicitly requested suspension. On pause, the run keeps
                # state intact and resume-from-pause re-enters this loop at
                # the saved checkpoint.
                # The FIRST boundary of a host-vouched fresh leg is the start
                # itself: the run row was committed moments ago by this process,
                # so there is no earlier pause/cancel to find — the first node
                # starts without a status read. (Every later boundary polls; an
                # immediate stop cancels the task outright.)
                if self._history_known_empty and step == start_step:
                    pause_now, cancel_now = False, False
                else:
                    # The checkpoint saved at the end of the previous super-step
                    # read the run's status in its own statement; that answer is
                    # this boundary's poll (one fewer round trip per step).
                    known, self._status_at_boundary = self._status_at_boundary, None
                    pause_now, cancel_now = await self._poll_controls(known_status=known)
                if pause_now:
                    return await self._park_paused(
                        run_id=run_id,
                        thread_id=thread_id,
                        step=step,
                        start_step=start_step,
                        parent_checkpoint_id=parent_checkpoint_id,
                        pending=pending,
                        last_outputs=last_outputs,
                    )

                # Cooperative cancellation between super-steps. Placed here
                # (before the step runs) so long LLM calls inside a step
                # complete normally — we stop AT the boundary, not mid-node.
                if cancel_now:
                    await self._save_checkpoint(
                        run_id=run_id,
                        thread_id=thread_id,
                        step=step,
                        parent_checkpoint_id=parent_checkpoint_id,
                        next_invocations=_as_next_invocations(pending, step),
                    )
                    await self._emit(
                        RunCancelledEvent(
                            run_id=run_id,
                            steps_executed=step - start_step,
                            reason="graceful",
                        )
                    )
                    return RunResult(
                        run_id=run_id,
                        thread_id=thread_id,
                        status=RunStatus.CANCELLED,
                        steps_executed=step - start_step,
                        channel_values=self.channels.snapshot(),
                        last_outputs=last_outputs,
                    )

                # Snapshot the channel state BEFORE the step runs. If any
                # node fails this step, we save the errored checkpoint with
                # this pre-step snapshot — successful siblings' channel
                # writes are NOT committed yet, so on resume the whole step
                # re-runs (successful nodes replay from cached outcomes,
                # failed nodes re-execute or use user-supplied recovery
                # outputs). This keeps the channel reducer math correct.
                pre_step_snapshot = self.channels.snapshot()

                # Step-mode node selection (NEW). On the FIRST super-step only,
                # run just the selected frontier nodes and defer the rest; the
                # deferred siblings are merged back into the next frontier after
                # routing so they run on a later step / hand-off. On error or
                # interrupt the FULL frontier (`pending`) is parked, so a
                # deferred sibling is never lost.
                if select_node_ids is not None and step == start_step:
                    to_run = [inv for inv in pending if inv.node_id in select_node_ids]
                    deferred = [inv for inv in pending if inv.node_id not in select_node_ids]
                else:
                    to_run = pending
                    deferred = []
                # A resumed frontier can mix steps (an interrupt checkpoint:
                # the interrupted node at N, its siblings' successors at N+1).
                # Hold the later ones; they rejoin the next frontier.
                held = [inv for inv in to_run if inv.step is not None and inv.step > step]
                if held:
                    to_run = [inv for inv in to_run if inv.step is None or inv.step <= step]
                    deferred = [*deferred, *held]

                # MANDATE-CANDIDATE GATE — before any node of this step runs.
                # Under the candidate marker only PURE nodes and agent/LLM
                # nodes (whose tool calls are contained one by one) may run;
                # any other node ends the run TERMINALLY, at the boundary,
                # exactly like a cancel — never a failure the retry ladder or an
                # ERROR edge could route around.
                candidate_stop = self._candidate_node_gate(to_run)
                if candidate_stop is not None:
                    await self._save_checkpoint(
                        run_id=run_id,
                        thread_id=thread_id,
                        step=step,
                        parent_checkpoint_id=parent_checkpoint_id,
                        next_invocations=_as_next_invocations(pending, step),
                    )
                    await self._emit(
                        RunCancelledEvent(
                            run_id=run_id,
                            steps_executed=step - start_step,
                            reason="candidate_stopped",
                        )
                    )
                    return RunResult(
                        run_id=run_id,
                        thread_id=thread_id,
                        status=RunStatus.CANCELLED,
                        steps_executed=step - start_step,
                        channel_values=self.channels.snapshot(),
                        last_outputs=last_outputs,
                        candidate_stopped=candidate_stop,
                    )

                if not self._step_defers_outcomes(to_run):
                    self._no_defer_steps.add(step)
                    if self._deferred_outcomes:
                        await self._flush_deferred_outcomes()
                self._loop_step = step
                results, interrupt = await self._run_step(run_id, thread_id, step, to_run)
                # A fan-out whose EVERY item failed fails loudly (parks below), never a
                # silent prune that ends the run "completed" (2026-10-22, run 87452569).
                self._escalate_all_failed_fan_outs(results)

                # Capture outputs for return value
                for r in results:
                    if r.output is not None:
                        if not self._output_in_run_row(r.invocation.node_id):
                            last_outputs[r.invocation.node_id] = elided_output_marker(
                                r.invocation.node_id, step
                            )
                            continue
                        last_outputs[r.invocation.node_id] = (
                            r.settled_dump
                            if r.settled_dump is not None
                            else model_dump_json(
                                r.output,
                                context=(
                                    f"[wf:{run_id[:8]} node={r.invocation.node_id}] last_outputs"
                                ),
                            )
                        )

                # Recoverable node failure (NEW). If any node raised, park
                # the run at this step's boundary with status=ERRORED. The
                # user can retry / skip / provide a manual result for the
                # failed node, then resume.
                error_results = [r for r in results if r.error is not None]
                # A REFUSAL LEADS (matrx_graph.spend_gate): when a gate refused any item of the
                # step, the run reports THAT — the one thing a person must act on (approve, then
                # retry) — never a sibling's timeout or "something went wrong on our side".
                error_results.sort(key=lambda r: 0 if is_caller_refusal(exc=r.error) else 1)
                first_error_result = error_results[0] if error_results else None
                if first_error_result is not None and interrupt is None:
                    err = first_error_result.error
                    assert err is not None  # for type narrowing
                    # HONEST PARTIAL FAILURE: a wide fan-out step that mostly
                    # SUCCEEDED must say so. "3 auditors failed" reads as a dead
                    # run; "22 of 25 completed and are preserved" is the truth —
                    # their outcomes are already recorded and a retry re-runs
                    # only the failed invocations.
                    notes: list[str] = []
                    if len(error_results) > 1:
                        # Multi-failure step (audit P1-19): every node got its
                        # own node_failed event already; name the siblings in
                        # the run-level error so nobody is invisible, and log it.
                        # Items sharing the first error (an escalated all-failed
                        # fan-out) are already counted in its one summary.
                        others = [
                            r.invocation.node_id for r in error_results[1:] if r.error is not err
                        ]
                        # Grouped by step: a fan-out's failed items name their step once.
                        named: dict[str, int] = {}
                        for other in others:
                            named[other] = named.get(other, 0) + 1
                        if others:
                            notes.append(
                                f"(+{len(others)} more invocation(s) failed in the "
                                f"same step: "
                                + ", ".join(
                                    f"{nid} ×{n}" if n > 1 else nid for nid, n in named.items()
                                )
                                + ")"
                            )
                        logger.warning(
                            "[wf:%s step=%d] %d nodes failed in one step: %s",
                            run_id[:8],
                            step,
                            len(error_results),
                            [r.invocation.node_id for r in error_results],
                        )
                    if len(results) > 1:
                        done = len(results) - len(error_results)
                        notes.append(
                            f"[{done} of {len(results)} invocations in this step "
                            f"completed and are preserved; retry re-runs only "
                            f"the failed one(s)]"
                        )
                    # The note is added by the ONE primitive that also carries
                    # the node's structured evidence across the wrap.
                    err = append_failure_notes(err, notes)
                    # A CANCEL WINS OVER THE FAILURE IT CAUSED. A person who
                    # cancelled while a step was in flight (a sub-workflow
                    # stopping on its parent's cancel fails its call step) gets a
                    # cancelled run, never an errored one inviting a retry.
                    _pause, cancel_now = await self._poll_controls()
                    if cancel_now:
                        await self._emit(
                            RunCancelledEvent(
                                run_id=run_id,
                                steps_executed=step - start_step,
                                reason="graceful",
                            )
                        )
                        return RunResult(
                            run_id=run_id,
                            thread_id=thread_id,
                            status=RunStatus.CANCELLED,
                            steps_executed=step - start_step,
                            channel_values=self.channels.snapshot(),
                            last_outputs=last_outputs,
                        )
                    return await self._park_errored(
                        run_id=run_id,
                        thread_id=thread_id,
                        step=step,
                        start_step=start_step,
                        parent_checkpoint_id=parent_checkpoint_id,
                        pending=pending,
                        pre_step_snapshot=pre_step_snapshot,
                        last_outputs=last_outputs,
                        node_id=first_error_result.invocation.node_id,
                        attempt=first_error_result.invocation.attempt,
                        err=err,
                    )

                if interrupt is not None:
                    # ENGINE_SPEC §6.2 — nothing is amputated. An interrupt is
                    # NOT a failure: the step's normal completion phases run
                    # for every NON-interrupted result FIRST, so completed
                    # siblings' channel writes COMMIT and their outputs ROUTE
                    # (through the §3 accumulator) before the interrupt
                    # checkpoint is saved. The checkpoint then carries the
                    # FULL remaining frontier: the interrupted invocation(s)
                    # (surfaced one marked ``is_interrupted``), every
                    # invocation made Ready by sibling routing, errored
                    # siblings (their failed outcomes are already recorded —
                    # resume walks their retry ladder), and step-mode
                    # deferred siblings. Temporal precedent: completed
                    # activity results persist in history while the workflow
                    # awaits a signal.
                    completed = [r for r in results if r.error is None and r.interrupt is None]
                    for r in completed:
                        if not r.channel_writes:
                            continue
                        try:
                            self.channels.commit(r.channel_writes)
                        except ChannelError as ce:
                            return await self._park_errored(
                                run_id=run_id,
                                thread_id=thread_id,
                                step=step,
                                start_step=start_step,
                                parent_checkpoint_id=parent_checkpoint_id,
                                pending=pending,
                                pre_step_snapshot=pre_step_snapshot,
                                last_outputs=last_outputs,
                                node_id=r.invocation.node_id,
                                attempt=r.invocation.attempt,
                                err=ce,
                            )
                    await self._settle_work_items(run_id, results)
                    pre_route_bindings = self._snapshot_bindings()
                    try:
                        routed = self._route_outputs(completed, step)
                        if deferred:
                            routed = self._merge_frontier(routed, deferred)
                    except EdgeRoutingError as re_err:
                        self._pending_bindings = pre_route_bindings
                        self._review.discard_pending()
                        return await self._park_errored(
                            run_id=run_id,
                            thread_id=thread_id,
                            step=step,
                            start_step=start_step,
                            parent_checkpoint_id=parent_checkpoint_id,
                            pending=pending,
                            pre_step_snapshot=pre_step_snapshot,
                            last_outputs=last_outputs,
                            node_id=re_err.node_id,
                            attempt=next(
                                (
                                    r.invocation.attempt
                                    for r in results
                                    if r.invocation.node_id == re_err.node_id
                                ),
                                1,
                            ),
                            err=re_err,
                        )
                    await self._review.flush(run_id)
                    await self._report_failure_blocked(run_id, step)
                    # Frontier order: interrupted invocations first (the
                    # surfaced one — results order — leads and gets the
                    # mark), then errored siblings, then routed/deferred.
                    interrupted_invs = [r.invocation for r in results if r.interrupt is not None]
                    errored_invs = [r.invocation for r in results if r.error is not None]
                    # The interrupted/errored invocations re-run at THIS step;
                    # routed successors belong to the next one.
                    frontier = [
                        *_as_next_invocations([*interrupted_invs, *errored_invs], step),
                        *_as_next_invocations(routed, step + 1),
                    ]
                    frontier[0] = frontier[0].model_copy(update={"is_interrupted": True})
                    cp_id = await self._save_checkpoint(
                        run_id=run_id,
                        thread_id=thread_id,
                        step=step,
                        parent_checkpoint_id=parent_checkpoint_id,
                        next_invocations=frontier,
                        interrupt_payload=interrupt.payload,
                    )
                    await self._emit(
                        RunInterruptedEvent(
                            run_id=run_id,
                            node_id=interrupt.node_id,
                            payload=interrupt.payload,
                            checkpoint_id=cp_id,
                        )
                    )
                    return RunResult(
                        run_id=run_id,
                        thread_id=thread_id,
                        status=RunStatus.INTERRUPTED,
                        steps_executed=step - start_step + 1,
                        channel_values=self.channels.snapshot(),
                        last_outputs=last_outputs,
                        interrupt={
                            "node_id": interrupt.node_id,
                            "payload": interrupt.payload,
                            # The checkpoint the run parked ON — known here and
                            # nowhere else without a query. It rides the result
                            # so the run-row snapshot (RunStore.mark_interrupted)
                            # can answer "resume from where?" in ONE read.
                            "checkpoint_id": cp_id,
                        },
                    )

                # Settle claimed work items BEFORE routing (matrx_graph.workset):
                # the queue's drain check reads counts on its next firing, so a
                # finished worker's item must be settled before that firing can
                # be scheduled. Appends happened during execute(); settle here —
                # the ordering that makes "pending==0 and in_progress==0" prove
                # no more discovery is coming from processing.
                await self._settle_work_items(run_id, results)

                # Reduce channel writes from all invocations this step.
                # Committed PER RESULT (semantically identical to one batch
                # for every reducer — each is an incremental left fold in
                # results order) so a reducer failure is attributable to the
                # node whose write broke it. A ChannelError here PARKS the
                # run as ERRORED instead of killing it: the node itself
                # succeeded, so the user's levers are skip / manual-result
                # on that node (replacing the output that the reducer
                # rejected), then resume. Partial in-memory commit state is
                # fine — the errored checkpoint stores pre_step_snapshot and
                # we return immediately.
                for r in results:
                    if not r.channel_writes:
                        continue
                    try:
                        self.channels.commit(r.channel_writes)
                    except ChannelError as ce:
                        return await self._park_errored(
                            run_id=run_id,
                            thread_id=thread_id,
                            step=step,
                            start_step=start_step,
                            parent_checkpoint_id=parent_checkpoint_id,
                            pending=pending,
                            pre_step_snapshot=pre_step_snapshot,
                            last_outputs=last_outputs,
                            node_id=r.invocation.node_id,
                            attempt=r.invocation.attempt,
                            err=ce,
                        )

                # Route outputs + Sends to build next-step pending list.
                # Edge failures (conditional predicate, explicit mapping
                # miss, multi-writer same-arg) also PARK rather than kill —
                # attributed to the source node whose output was being
                # routed. The accumulator is snapshotted first so the
                # errored checkpoint stores the PRE-routing bindings (like
                # pre_step_snapshot for channels): resume re-runs the whole
                # step and re-routes every result idempotently.
                pre_route_bindings = self._snapshot_bindings()
                try:
                    next_pending = self._route_outputs(results, step)
                    # Step-mode: fold any deferred siblings (frontier nodes
                    # the caller chose NOT to run this step) back into the
                    # next frontier. Inside this try because two DISTINCT
                    # firings of one node colliding on a correlation key is
                    # an EdgeRoutingError park (F4), never a silent
                    # last-writer-wins merge.
                    if deferred:
                        next_pending = self._merge_frontier(next_pending, deferred)
                except EdgeRoutingError as re_err:
                    self._pending_bindings = pre_route_bindings
                    self._review.discard_pending()
                    return await self._park_errored(
                        run_id=run_id,
                        thread_id=thread_id,
                        step=step,
                        start_step=start_step,
                        parent_checkpoint_id=parent_checkpoint_id,
                        pending=pending,
                        pre_step_snapshot=pre_step_snapshot,
                        last_outputs=last_outputs,
                        node_id=re_err.node_id,
                        attempt=next(
                            (
                                r.invocation.attempt
                                for r in results
                                if r.invocation.node_id == re_err.node_id
                            ),
                            1,
                        ),
                        err=re_err,
                    )
                # Connections TAKEN by this routing that carry a review mark.
                await self._review.flush(run_id)
                await self._report_failure_blocked(run_id, step)

                # RUN-AHEAD invariant: everything launched early under the
                # next step's key must be exactly what this routing schedules.
                self._verify_run_ahead_at_barrier(step, next_pending)

                # Save checkpoint BEFORE running next step
                cp_id = await self._save_checkpoint(
                    run_id=run_id,
                    thread_id=thread_id,
                    step=step,
                    parent_checkpoint_id=parent_checkpoint_id,
                    next_invocations=_as_next_invocations(next_pending, step + 1),
                )
                pop_status = getattr(self.checkpointer, "pop_run_status", None)
                self._status_at_boundary = pop_status(run_id) if pop_status is not None else None
                parent_checkpoint_id = cp_id
                step += 1
                pending = next_pending
        except ExecutionError as e:
            # Framework-level failure (max_steps exceeded, scheduler bug
            # surfaced as ExecutionError). Terminal — but NEVER raise:
            # returning a RunResult preserves the partial ``last_outputs``
            # so the host persists what completed instead of nulling
            # ``wf_run.output``. Raising here was the P0-5 output-loss bug.
            await self._emit(
                RunFailedEvent(
                    run_id=run_id,
                    steps_executed=step - start_step,
                    error_type=type(e).__name__,
                    error_message=str(e),
                )
            )
            return RunResult(
                run_id=run_id,
                thread_id=thread_id,
                status=RunStatus.FAILED,
                steps_executed=step - start_step,
                channel_values=self.channels.snapshot(),
                last_outputs=last_outputs,
                error=f"{type(e).__name__}: {client_error_text(str(e))}",
                failure=self._failure_for(e, None),
            )
        except ChannelError as e:
            # Defensive: any ChannelError not already attributed by the
            # per-result commit loop (e.g. raised from a future code path)
            # must still terminate WITH an event + partial outputs, never
            # as an unobserved exception.
            await self._emit(
                RunFailedEvent(
                    run_id=run_id,
                    steps_executed=step - start_step,
                    error_type=type(e).__name__,
                    error_message=str(e),
                )
            )
            return RunResult(
                run_id=run_id,
                thread_id=thread_id,
                status=RunStatus.FAILED,
                steps_executed=step - start_step,
                channel_values=self.channels.snapshot(),
                last_outputs=last_outputs,
                error=f"{type(e).__name__}: {client_error_text(str(e))}",
                failure=self._failure_for(e, None),
            )

        # Join-deadlock guard (ENGINE_SPEC §3.4 + §12.8 "silence is a bug").
        # The frontier drained, but if any node still holds buffered
        # deliveries (a blocked join whose remaining upstream can never
        # resolve — e.g. a user_skip under on_skipped_upstream='block', or
        # an upstream that never fired), completing would silently discard
        # real data. Park ERRORED, loudly naming every blocked node and its
        # unresolved edges; the buffered bindings stay durable on the parked
        # checkpoint so recovery (retry / manual-result on the missing
        # upstream) + resume can still fire the join. Pure-pruned residue
        # (dead-branch leftovers) is dropped with a warning — no data there.
        blocked = self._blocked_join_leftovers(run_id)
        if blocked:
            first_node_id, deadlock_error = blocked
            # ENGINE_SPEC §3.4 Amendment D2b: the park is ADDRESSABLE — one
            # blocked_join invocation per deadlocked node, carrying its
            # currently-merged partial inputs, so the recovery endpoints
            # (skip / manual-result / retry) can act on the blocked node
            # instead of 404ing against an empty frontier.
            return await self._park_errored(
                run_id=run_id,
                thread_id=thread_id,
                step=step,
                start_step=start_step,
                parent_checkpoint_id=parent_checkpoint_id,
                pending=self._blocked_join_invocations(),
                pre_step_snapshot=self.channels.snapshot(),
                last_outputs=last_outputs,
                node_id=first_node_id,
                attempt=1,
                err=deadlock_error,
            )

        await self._flag_never_resolved_joins(run_id, step)
        steps_executed = step - start_step
        channel_values = self.channels.snapshot()
        if resumed_from_step is not None:
            # A resumed leg's result is the run's WHOLE result (2026-10-28, child run 0c33f0f5: it
            # finished every step, its server died before the row said so, and the resume from
            # its last checkpoint ran nothing — "completed" with no result, the caller failed
            # child_result_missing). What earlier legs settled rides beneath what this leg ran.
            last_outputs, read = await self._with_earlier_outputs(run_id, last_outputs, resumed_from_step)
            if not read and not last_outputs and steps_executed == 0:
                # Steps that legitimately return nothing still complete with ``{}``; only results
                # that EXIST in the run's history but could not be read fail the run.
                earlier = await self._earlier_step_history(run_id)
                if earlier is not None and earlier[0]:
                    return await self._resumed_without_result(
                        run_id=run_id, thread_id=thread_id, channel_values=channel_values
                    )
        from matrx_graph.executor.run_stop import declared_run_stop, undelivered_deliverables

        stopped = declared_run_stop(self.graph, last_outputs, caught=self._caught_failures)
        # NOTHING FAILS SILENTLY (2026-10-27): a run whose declared deliverables ALL never ran
        # BECAUSE a step failed (or the error-handler gate dropped a step that had its data) did
        # not complete — it ends FAILED naming what happened. A branch not taken or an end step
        # reached is an ordinary finish and stays "completed"; so does a step that declared why
        # the run stopped (``stopped``). A resumed run judges its WHOLE history: what earlier
        # legs ran and which of their steps failed come from the checkpointer.
        never_ran = None
        deliverables = self._deliverable_ids()
        if (
            not stopped
            and stop_after_steps is None
            and deliverables
            and not any(nid in last_outputs and nid not in self._failed_steps for nid in deliverables)
        ):
            ran, failed = set(last_outputs), dict(self._failed_steps)
            # This leg delivered none of them: judge the run's WHOLE history (a resumed leg's
            # ``last_outputs`` holds only its own steps). One read, only on this path.
            earlier = await self._earlier_step_history(run_id)
            if earlier is not None:
                earlier_ran, earlier_failed = earlier
                ran |= earlier_ran
                for nid, info in earlier_failed.items():
                    if nid not in ran or nid in self._failed_steps:
                        failed.setdefault(nid, info)
            if earlier is not None or start_step == 0:
                never_ran = undelivered_deliverables(
                    self.graph, ran, failed=failed, gate_dropped=self._error_gate_drops,
                    label=self._step_label,
                )
            # else: a resumed leg with no history to judge by — never fail a run on a guess.
        if never_ran:
            first = never_ran[0]
            message = "The run ended without its result: " + " ".join(f["says"] for f in never_ran)
            logger.error("[wf:%s] deliverable_never_ran: %s", run_id[:8], never_ran)
            await self._emit(
                RunFailedEvent(
                    run_id=run_id,
                    steps_executed=steps_executed,
                    error_type="DeliverableNeverRan",
                    error_message=message,
                )
            )
            return RunResult(
                run_id=run_id,
                thread_id=thread_id,
                status=RunStatus.FAILED,
                steps_executed=steps_executed,
                channel_values=channel_values,
                last_outputs=last_outputs,
                error=f"DeliverableNeverRan: {message}",
                stopped={"reason": "deliverable_never_ran", "says": message, "step": first["step"]},
                failure=RunFailure(
                    cause=(
                        Cause.WIRING_BROKEN
                        if first["cause"] == "error_gate"
                        else (failed.get(first["by"], {}).get("cause") or Cause.ENGINE_ERROR)
                    ),
                    message=message,
                    step_id=first["by"],
                    step_label=self._step_label(first["by"]),
                    error_type="DeliverableNeverRan",
                    technical=f"deliverable_never_ran: {never_ran}",
                ),
            )
        await self._emit(
            RunCompletedEvent(
                run_id=run_id,
                steps_executed=steps_executed,
                last_outputs=last_outputs,
                channel_values=channel_values,
                stopped=stopped,
            )
        )

        return RunResult(
            run_id=run_id,
            thread_id=thread_id,
            status=RunStatus.COMPLETED,
            steps_executed=steps_executed,
            channel_values=channel_values,
            last_outputs=last_outputs,
            stopped=stopped,
        )

    def _output_in_run_row(self, node_id: str) -> bool:
        """False when the node's spec keeps its output out of the run row (``NodeSpec.output_in_run_row``)."""
        node = self.graph.nodes.get(node_id)
        if node is None:
            return True
        try:
            return bool(getattr(self.registry.get(node.spec_type).spec, "output_in_run_row", True))
        except Exception:  # noqa: BLE001 — an unknown spec keeps today's behavior
            return True

    async def _run_step(
        self,
        run_id: str,
        thread_id: str,
        step: int,
        pending: list[Invocation],
    ) -> tuple[list[_StepResult], GraphInterrupt | None]:
        """Run all pending invocations in parallel; return their results.

        Interrupts and normal exceptions are captured per-invocation so one
        failing node doesn't cancel the others mid-step via TaskGroup.
        """
        with span(
            "workflow.super_step",
            run_id=run_id,
            step=step,
            pending_count=len(pending),
            pending_node_ids=[inv.node_id for inv in pending],
        ):
            return await self._run_step_body(run_id, thread_id, step, pending)

    async def _run_step_body(
        self,
        run_id: str,
        thread_id: str,
        step: int,
        pending: list[Invocation],
    ) -> tuple[list[_StepResult], GraphInterrupt | None]:
        snapshot = self.channels.snapshot()
        # IMPORTANT: each parallel invocation in this super-step MUST get its
        # own AppContext.  Forking once at the step level and sharing the
        # result across asyncio.gather() tasks was the root cause of the
        # "duplicate key value violates unique constraint cx_request_pkey"
        # bug — concurrent agents all mutated the same metadata dict (and
        # before that, the same reserved_*_ids), so later writers stomped on
        # earlier writers' reserved IDs.  Forking per invocation gives each
        # task an independent AppContext + independent mutable collections,
        # which restores the per-task isolation asyncio's ContextVar already
        # promises but a shared object silently breaks.
        invocation_counts = _invocation_counts(pending)
        # RUN-AHEAD: a node this step's routing would schedule here may already
        # be running (or done) — launched early, under THIS step's key, while
        # an earlier step waited on a slow sibling. Adopt those FIRST: a broken
        # adoption raises before this step has started anything.
        adoptions = await self._adopt_run_ahead_all(step, pending)
        results: list[_StepResult] = []
        tasks: dict[asyncio.Task[None], _StepResult] = {}
        for inv, adopted in zip(pending, adoptions, strict=True):
            if adopted is not None:
                task, result = adopted
            else:
                result = _StepResult(invocation=inv, output=None)
                task = asyncio.create_task(
                    self._run_invocation(
                        run_id=run_id,
                        thread_id=thread_id,
                        # A resumed frontier entry runs at the step it was
                        # scheduled for (its key); everything else at this one.
                        step=_scheduled_step(inv, step),
                        result=result,
                        snapshot=snapshot,
                        invocation_count=invocation_counts[inv.node_id],
                    )
                )
            results.append(result)
            tasks[task] = result

        # Not using TaskGroup: one node failing would cancel siblings mid-step,
        # which is wrong for multi-node super-steps. Per-invocation errors are
        # captured on each result and handled after the step boundary.
        try:
            await self._await_step(run_id, thread_id, step, tasks)
        except BaseException:
            for task in tasks:
                task.cancel()
            await asyncio.gather(*tasks, return_exceptions=True)
            raise

        # Surface the first interrupt (if any). Per-node errors are NO
        # LONGER raised here — they propagate to `_drive` via the StepResult
        # objects so the run can transition to the recoverable ERRORED state
        # with a checkpoint instead of dying. The failure outcome has
        # already been recorded in `_execute_invocation_body`'s except
        # clause, so retry/skip/manual-result can find it.
        return results, _first_interrupt(results)

    async def _await_step(
        self,
        run_id: str,
        thread_id: str,
        step: int,
        tasks: dict[asyncio.Task[None], _StepResult],
    ) -> None:
        """Wait until every member of this step has finished.

        With run-ahead on, every member (and every earlier run-ahead launch)
        that finishes while the step is still waiting is offered to
        ``_expand_run_ahead`` — so a node that needs only finished work starts
        now instead of at the barrier (podcast W0, 2026-10-07: images waited
        6.5 min for an audio render they never read).

        Run-ahead stops for the rest of the drive the moment a member of the
        step fails or interrupts (the step will park), or a pause/cancel is
        requested (polled before launching, at most once per
        ``RUN_AHEAD_STOP_POLL_SECONDS``, and latched for the boundary poll).
        """
        if not self._run_ahead_on:
            await asyncio.gather(*tasks, return_exceptions=True)
            self._settle_escaped(tasks, tasks)
            return
        if self._eager_ahead:
            await self._await_step_eager(run_id, thread_id, step, tasks)
            return
        open_members: set[asyncio.Task[None]] = {t for t in tasks if not t.done()}
        if not open_members:
            return
        done_queue: asyncio.Queue[tuple[asyncio.Task[None], _StepResult, int]] = asyncio.Queue()

        def _deliver(task: asyncio.Task[None], result: _StepResult, result_step: int) -> None:
            task.add_done_callback(lambda t: done_queue.put_nowait((t, result, result_step)))

        for task, result in tasks.items():
            _deliver(task, result, _scheduled_step(result.invocation, step))
        for task, (result, result_step) in list(self._run_ahead_unexpanded.items()):
            if task not in tasks:
                _deliver(task, result, result_step)
        self._run_ahead_deliver = _deliver
        # This step's members in frontier order — the order the barrier routes them in. A finished member is
        # routed TOGETHER with every member of the same step that already finished, so a join whose inputs all
        # came from this step starts the moment its last input lands (Smart Add run 363ea8bb, 2026-10-14: the
        # first-data capture point joined two quick steps and waited 25 s for an unrelated screenshot step).
        member_order = {id(r): i for i, r in enumerate(tasks.values())}
        finished_members: list[_StepResult] = []
        try:
            while open_members:
                task, result, result_step = await done_queue.get()
                if task.cancelled() and _job_lease().lost():
                    # A member stopped because this copy lost its job lease (``JobLeaseLost`` is a cancellation):
                    # the whole copy stops here, never routing or checkpointing on (lane K1b, B2).
                    lease = _job_lease().current()
                    raise _job_lease().JobLeaseLost(f"job lease lost: {lease.why if lease else ''}")
                if id(result) in member_order and result_step == step:
                    # Kept in frontier order by insertion — O(log n) search per finished member, never a re-sort.
                    bisect.insort(finished_members, result, key=lambda r: member_order[id(r)])
                open_members.discard(task)
                self._run_ahead_unexpanded.pop(task, None)
                _record_escaped_fault(task, result, run_stopping=self._run_is_stopping())
                if result.expanded:
                    continue
                if result.error is not None or result.interrupt is not None or result.channel_writes:
                    # The step will park (or a channel write the graph never
                    # declared appeared): nothing more runs ahead this drive.
                    self._run_ahead_on = False
                if self._run_ahead_on and open_members and await self._stop_requested():
                    self._run_ahead_on = False
                if not self._run_ahead_on or not open_members:
                    result.expanded = True
                    if not self._run_ahead_on:
                        break
                    continue
                self._expand_run_ahead(
                    run_id, thread_id, result, result_step,
                    siblings=finished_members if result_step == step and id(result) in member_order else None,
                )
        finally:
            self._run_ahead_deliver = None
        if open_members:
            await asyncio.gather(*open_members, return_exceptions=True)
            self._settle_escaped(tasks, open_members)

    async def _await_step_eager(
        self,
        run_id: str,
        thread_id: str,
        step: int,
        tasks: dict[asyncio.Task[None], _StepResult],
    ) -> None:
        """``_await_step`` for a START WHEN READY graph (executor/FEATURE.md).

        The step begins with one recomputation of the speculative frontier (the barrier just routed
        the previous step, so results that finished earlier may now complete a join), and every
        later batch of routable completions — members or launches for any later step — triggers
        another. The stop rules are run-ahead's: a failed / interrupted / channel-writing result or
        a latched pause/cancel ends launching for the drive."""
        open_members: set[asyncio.Task[None]] = {t for t in tasks if not t.done()}
        if not open_members:
            return
        done_queue: asyncio.Queue[tuple[asyncio.Task[None], _StepResult, int]] = asyncio.Queue()

        def _deliver(task: asyncio.Task[None], result: _StepResult, result_step: int) -> None:
            task.add_done_callback(lambda t: done_queue.put_nowait((t, result, result_step)))

        for task, result in tasks.items():
            if not task.done():
                _deliver(task, result, step)
        for (ahead_step, *_rest), (task, result) in list(self._run_ahead.items()):
            if task not in tasks and not task.done():
                _deliver(task, result, ahead_step)
        self._run_ahead_deliver = _deliver
        fresh = True
        try:
            while open_members:
                if fresh:
                    fresh = False
                    if await self._stop_requested():
                        self._run_ahead_on = False
                        break
                    self._expand_eager(run_id, thread_id, step, tasks)
                batch = [await done_queue.get()]
                while not done_queue.empty():
                    batch.append(done_queue.get_nowait())
                for task, result, _result_step in batch:
                    if task.cancelled() and _job_lease().lost():
                        lease = _job_lease().current()
                        raise _job_lease().JobLeaseLost(f"job lease lost: {lease.why if lease else ''}")
                    open_members.discard(task)
                    self._run_ahead_unexpanded.pop(task, None)
                    result.expanded = True
                    _record_escaped_fault(task, result, run_stopping=self._run_is_stopping())
                    if result.error is not None or result.interrupt is not None or result.channel_writes:
                        # The step will park (or a channel write the graph never declared
                        # appeared): nothing more runs ahead this drive.
                        self._run_ahead_on = False
                    elif _routable_ahead(result):
                        fresh = True
                if not self._run_ahead_on:
                    break
        finally:
            self._run_ahead_deliver = None
        if open_members:
            await asyncio.gather(*open_members, return_exceptions=True)
            self._settle_escaped(tasks, open_members)

    def _expand_eager(
        self,
        run_id: str,
        thread_id: str,
        step: int,
        tasks: dict[asyncio.Task[None], _StepResult],
    ) -> None:
        """Launch every node the FINISHED, not-yet-barrier-routed results make Ready.

        On a throwaway copy of the barrier's join state, route — exactly as the barriers will —
        this step's finished routable members (frontier order), then each later step's finished
        routable launches, one ``_route_outputs(group, k)`` per step ``k`` in step order. A node
        that routing makes Ready under ``k`` launches under the key ``k + 1`` the barrier will
        give it, unless already launched. Recomputed from scratch each time, so a result that
        finished before the state advanced is routed again with everything finished since."""
        groups: list[tuple[int, list[_StepResult]]] = []
        members = [r for t, r in tasks.items() if t.done() and not t.cancelled() and _routable_ahead(r)]
        if members:
            groups.append((step, members))
        later: dict[int, list[_StepResult]] = {}
        for (ahead_step, *_rest), (task, ahead) in self._run_ahead.items():
            if ahead_step > step and task.done() and not task.cancelled() and _routable_ahead(ahead):
                later.setdefault(ahead_step, []).append(ahead)
        groups.extend(sorted(later.items()))
        if not groups:
            return
        launches: list[tuple[int, Invocation]] = []
        saved = self._snapshot_routing_state()
        self._partial_routing = True
        try:
            for group_step, group in groups:
                if group_step + 1 >= self._run_ahead_step_limit:
                    break
                launches.extend(
                    (group_step + 1, inv) for inv in self._route_outputs(group, group_step)
                )
        except Exception:  # noqa: BLE001 — the barrier's own routing reports it
            return
        finally:
            self._partial_routing = False
            self._restore_routing_state(saved)
        snapshot = self.channels.snapshot()
        for next_step, inv in launches:
            if inv.dispatch_id or inv.blocked_join:
                continue
            key = _run_ahead_key(next_step, inv)
            if (
                key in self._run_ahead
                or self._run_ahead_budget <= 0
                or not self._candidate_may_run(inv)
            ):
                continue
            self._run_ahead_budget -= 1
            ahead = _StepResult(invocation=inv, output=None)
            task = asyncio.create_task(
                self._run_invocation(
                    run_id=run_id,
                    thread_id=thread_id,
                    step=next_step,
                    result=ahead,
                    snapshot=snapshot,
                    invocation_count=1,
                )
            )
            self._run_ahead[key] = (task, ahead)
            self._run_ahead_unexpanded[task] = (ahead, next_step)
            if self._run_ahead_deliver is not None:
                self._run_ahead_deliver(task, ahead, next_step)

    def _run_is_stopping(self) -> bool:
        """The run itself is being stopped — a cancel or pause latched, this copy's job lease lost,
        or this drive's own task being cancelled (a deploy drain)."""
        current = asyncio.current_task()
        return bool(
            self._cancel_latched
            or self._pause_latched
            or _job_lease().lost()
            or (current is not None and current.cancelling())
        )

    def _settle_escaped(
        self, tasks: dict[asyncio.Task[None], _StepResult], members: Any
    ) -> None:
        """After a ``return_exceptions`` gather: a member cancelled because the run is stopping
        stops the step as a cancellation (exactly as the plain gather did); every other escaped
        fault, a step's own cancellation included, becomes that step's error."""
        stopping = self._run_is_stopping()
        for task, result in tasks.items():
            if task not in members:
                continue
            if task.done() and task.cancelled() and stopping:
                if _job_lease().lost():
                    lease = _job_lease().current()
                    raise _job_lease().JobLeaseLost(f"job lease lost: {lease.why if lease else ''}")
                raise asyncio.CancelledError(f"step member '{result.invocation.node_id}' cancelled by a run stop")
            _record_escaped_fault(task, result, run_stopping=stopping)

    async def _stop_requested(self) -> bool:
        """Pause/cancel poll for run-ahead launches — throttled, because a
        fan-out can finish hundreds of members a second and each poll is a
        status read. A latched answer is free."""
        if self._pause_latched or self._cancel_latched:
            return True
        now = asyncio.get_running_loop().time()
        if now - self._last_stop_poll < RUN_AHEAD_STOP_POLL_SECONDS:
            return False
        self._last_stop_poll = now
        pause_now, cancel_now = await self._poll_controls()
        return cancel_now or pause_now

    def _expand_run_ahead(
        self,
        run_id: str,
        thread_id: str,
        result: _StepResult,
        result_step: int,
        *,
        siblings: list[_StepResult] | None = None,
    ) -> None:
        """Launch every node that ``result`` makes Ready, under the step
        key the barrier will give it (``result_step + 1``).

        ``siblings``: the members of ``result``'s step that already finished
        (``result`` among them), in the barrier's routing order. They are routed
        together, so a JOIN fed only by finished members of this step is Ready
        here; without them only ``result`` alone is routed.

        Routing runs on a throwaway copy of the join state, so the canonical
        step-end routing is untouched; a target that still waits on any other
        unfinished delivery is simply not Ready here and runs at its step as
        always. Fan-out items, Sends, failures and interrupts never run ahead.
        ``_partial_routing`` defers every rule that reads run-wide state the
        full routing builds, so this routing never resolves an edge differently
        from the barrier's.
        """
        if result.expanded:
            return
        result.expanded = True
        if (
            result.error is not None
            or result.interrupt is not None
            or result.sends
            or result.channel_writes
            or result.invocation.dispatch_id
            or (result.output is None and result.failure is None)
        ):
            return
        next_step = result_step + 1
        if next_step >= self._run_ahead_step_limit:
            return
        routed = [result]
        if siblings:
            routed = [r for r in siblings if r is result or _routable_ahead(r)]
        saved = self._snapshot_routing_state()
        self._partial_routing = True
        try:
            derived = self._route_outputs(routed, result_step)
        except Exception:  # noqa: BLE001 — the barrier's own routing reports it
            return
        finally:
            self._partial_routing = False
            self._restore_routing_state(saved)
        snapshot = self.channels.snapshot()
        for inv in derived:
            if inv.dispatch_id or inv.blocked_join:
                continue
            key = _run_ahead_key(next_step, inv)
            if (
                key in self._run_ahead
                or self._run_ahead_budget <= 0
                or not self._candidate_may_run(inv)
            ):
                continue
            self._run_ahead_budget -= 1
            ahead = _StepResult(invocation=inv, output=None)
            task = asyncio.create_task(
                self._run_invocation(
                    run_id=run_id,
                    thread_id=thread_id,
                    step=next_step,
                    result=ahead,
                    snapshot=snapshot,
                    invocation_count=1,
                )
            )
            self._run_ahead[key] = (task, ahead)
            self._run_ahead_unexpanded[task] = (ahead, next_step)
            if self._run_ahead_deliver is not None:
                self._run_ahead_deliver(task, ahead, next_step)

    async def _adopt_run_ahead_all(
        self, step: int, pending: list[Invocation]
    ) -> list[tuple[asyncio.Task[None], _StepResult] | None]:
        """The run-ahead launch for each invocation of this step (None where
        there is none), checked for the WHOLE step before anything launches.

        Same correlation key means the same firing; the inputs MUST match — a
        launch already recorded its outcome at this key, so a mismatch would
        replay the wrong output. That is an engine defect: every launch taken
        here is canceled and awaited, and the run fails loudly."""
        adoptions: list[tuple[asyncio.Task[None], _StepResult] | None] = []
        mismatch: str | None = None
        for inv in pending:
            entry = self._run_ahead.pop(_run_ahead_key(_scheduled_step(inv, step), inv), None)
            adoptions.append(entry)
            if entry is None:
                continue
            self._run_ahead_unexpanded.pop(entry[0], None)
            ran = entry[1].invocation
            if mismatch is None and (ran.inputs != inv.inputs or ran.attempt != inv.attempt):
                mismatch = (
                    f"run-ahead invariant broken at step {step}: node '{inv.node_id}' was "
                    f"launched early with inputs {sorted(ran.inputs)} (attempt "
                    f"{ran.attempt}) but the step scheduled it with inputs "
                    f"{sorted(inv.inputs)} (attempt {inv.attempt}). Its outcome at this "
                    "key cannot be trusted — the run stops instead of replaying it."
                )
        if mismatch is None:
            return adoptions
        taken = [entry[0] for entry in adoptions if entry is not None]
        for task in taken:
            task.cancel()
        await asyncio.gather(*taken, return_exceptions=True)
        raise ExecutionError(mismatch)

    def _verify_run_ahead_at_barrier(self, step: int, next_pending: list[Invocation]) -> None:
        """The barrier's routing of ``step`` is the truth; every run-ahead
        launch filed at or before ``step + 1`` must match it.

        Run-ahead launches a node under the key the barrier WILL give it. Two
        ways that can be wrong, both an engine defect that used to pass
        silently (the node ran twice, first on wrong inputs, and the run said
        COMPLETED):

        * an ORPHAN — a launch filed at ``step + 1`` (or earlier) that this
          routing does not schedule there with the same inputs and attempt;
        * a DOUBLE — this routing schedules a node whose launch is filed under
          a DIFFERENT step's key, so the step would run it again.

        Raises ``ExecutionError`` (the run fails loudly); the drive's cleanup
        cancels every open launch."""
        if not self._run_ahead:
            return
        next_step = step + 1
        scheduled: dict[tuple[int, str, str, int], Invocation] = {
            _run_ahead_key(_scheduled_step(inv, next_step), inv): inv for inv in next_pending
        }
        identities = {(k[1], k[2], k[3]): k for k in self._run_ahead}
        problems: list[str] = []
        for key, (_task, ahead) in self._run_ahead.items():
            if key[0] > next_step:
                continue
            inv = scheduled.get(key)
            ran = ahead.invocation
            if inv is None:
                problems.append(
                    f"node '{key[1]}' was launched early for step {key[0]} but the barrier "
                    f"after step {step} does not schedule it there"
                )
            elif ran.inputs != inv.inputs or ran.attempt != inv.attempt:
                problems.append(
                    f"node '{key[1]}' was launched early with inputs {sorted(ran.inputs)} "
                    f"(attempt {ran.attempt}) but the barrier schedules it with inputs "
                    f"{sorted(inv.inputs)} (attempt {inv.attempt})"
                )
        for key, inv in scheduled.items():
            other = identities.get((key[1], key[2], key[3]))
            if other is not None and other != key:
                problems.append(
                    f"node '{inv.node_id}' is scheduled for step {key[0]} but already "
                    f"launched early for step {other[0]} — it would run twice"
                )
        if problems:
            raise ExecutionError(
                "run-ahead invariant broken: " + "; ".join(problems)
                + ". The early launch cannot be trusted — the run stops instead of running "
                "the node twice."
            )

    async def _cancel_run_ahead(self, run_id: str) -> None:
        """Cancel every run-ahead launch no step adopted; wait only for the
        cancellations to land. A launch that already finished recorded its
        outcome (its step replays it); one cut off runs again at its step."""
        pending = [task for task, _ in self._run_ahead.values() if not task.done()]
        self._run_ahead = {}
        self._run_ahead_unexpanded = {}
        if not pending:
            return
        logger.info(
            "[wf:%s] canceling %d run-ahead invocation(s) — the run stopped before their step",
            run_id[:8],
            len(pending),
        )
        for task in pending:
            task.cancel()
        await asyncio.gather(*pending, return_exceptions=True)

    def _snapshot_routing_state(
        self,
    ) -> tuple[dict[str, PendingBinding], dict[str, int], dict[tuple[str, str], int]]:
        """Everything ``_route_outputs`` mutates in a run-ahead-eligible graph."""
        return (
            self._snapshot_bindings(),
            dict(self._firing_seq),
            dict(self._dispatch_expected),
        )

    def _restore_routing_state(
        self,
        state: tuple[dict[str, PendingBinding], dict[str, int], dict[tuple[str, str], int]],
    ) -> None:
        bindings, firing_seq, dispatch_expected = state
        self._pending_bindings = bindings
        self._firing_seq = firing_seq
        self._dispatch_expected = dispatch_expected

    async def _run_invocation(
        self,
        *,
        run_id: str,
        thread_id: str,
        step: int,
        result: _StepResult,
        snapshot: dict[str, Any],
        invocation_count: int,
    ) -> None:
        """Run ONE invocation into ``result`` (a super-step member, or a
        run-ahead launch keyed to the step it belongs to).

        Captures GraphInterrupt / exceptions on the result so one failing node
        never cancels its siblings; applies the run-level and per-node
        concurrency caps."""
        inv = result.invocation
        invocation_app_ctx = self.app.fork_for_workflow_step(
            _workflow_invocation_conversation_id(
                run_id=run_id,
                step=step,
                invocation=inv,
            )
        )
        # Per-INVOCATION stream attribution: hand this invocation its own
        # scoped emitter so that when several invocations stream
        # concurrently in one super-step, each one's tokens land in a
        # distinct live buffer (the FE renders one floating panel per
        # invocation). The identity is (node_id, dispatch_id, item_index)
        # — the same fan-out correlation every durable event carries — so
        # a 50-item fan-out is 50 separable streams, not one interleaved
        # mess. Opt-in via the emitter's ``for_invocation`` hook — host
        # emitters implement it; the console/standalone fallback emitter
        # doesn't and is left as-is.
        base_emitter = getattr(invocation_app_ctx, "emitter", None)
        if base_emitter is not None and hasattr(base_emitter, "for_invocation"):
            try:
                # ``step``/``attempt`` complete the invocation's DURABLE
                # coordinates, so an emitter that receives countable
                # progress from deep inside a provider call (the agent
                # loop's tool iterations) can build a well-formed
                # NodeProgressEvent instead of guessing. Keyword-only and
                # optional: an emitter still on the three-positional
                # signature keeps working, unchanged.
                try:
                    scoped_emitter = base_emitter.for_invocation(
                        inv.node_id,
                        inv.dispatch_id,
                        inv.item_index,
                        step=step,
                        attempt=inv.attempt,
                    )
                except TypeError:
                    scoped_emitter = base_emitter.for_invocation(
                        inv.node_id, inv.dispatch_id, inv.item_index
                    )
            except Exception:  # noqa: BLE001 — never let this kill a run
                scoped_emitter = None
            if scoped_emitter is not None:
                invocation_app_ctx = dataclasses.replace(
                    invocation_app_ctx, emitter=scoped_emitter
                )

        async def _invoke() -> None:
            # Install the per-invocation context as the AMBIENT context for
            # this node. Forking alone is not enough: the fork only reaches
            # code that takes `ctx.app` explicitly, but matrx-ai (and any
            # tool / sub-agent it spawns) reads `get_app_context()` off the
            # ContextVar. Without installing it, an LLM node saw the
            # RUN-LEVEL context — whose conversation_id can be "" — and its
            # cx_* persistence crashed with `invalid input syntax for type
            # uuid: ""`, parking the whole run. Each _run_one runs in its
            # own asyncio task (gather copies the ContextVar map), so this
            # set is task-local; the token reset below keeps it tidy.
            _ctx_token = _install_app_context(invocation_app_ctx)
            # Watch AI raw capture (matrx_utils.raw_capture): what this step's outside calls returned
            # (a vendor body as received) lands on this step's scope; a tool call inside an AI step
            # opens its own nested scope. Delivered to the host's sink, which indexes it on the
            # step's workflow.node_outcome row (metadata.raw_capture).
            _capture = raw_capture.capture_scope(
                {
                    "target": "node_outcome",
                    "run_id": run_id,
                    "step": step,
                    "node_id": inv.node_id,
                    "dispatch_id": inv.dispatch_id,
                    "item_index": inv.item_index,
                    # Carried verbatim, never defaulted: an empty organization is
                    # refused BY NAME at the sink (it files nothing), not stored as None.
                    "organization_id": str(getattr(invocation_app_ctx, "organization_id", "") or ""),
                    "user_id": str(getattr(invocation_app_ctx, "user_id", "") or "") or None,
                }
            )
            _scope = _capture.__enter__()
            # THE INVOCATION SPEND TALLY (matrx_graph.spend_gate): every paid request row this
            # step writes is noted here, so its cost settles however the step ends.
            _tally, _tally_token = open_invocation_spend()
            try:
                await self._execute_invocation(
                    run_id=run_id,
                    thread_id=thread_id,
                    step=step,
                    invocation=inv,
                    result=result,
                    channel_snapshot=snapshot,
                    step_app_ctx=invocation_app_ctx,
                    invocation_count=invocation_count,
                )
            except GraphInterrupt as gi:
                result.interrupt = gi
            except Exception as e:
                result.error = e
            finally:
                close_invocation_spend(_tally_token)
                # Shielded: a cancelled step still settles what it already paid for.
                await asyncio.shield(self._settle_invocation_spend(run_id, step, inv, _tally))
                _capture.__exit__(None, None, None)
                if _scope.items or _scope.cuts:
                    _scope.target["attempt"] = inv.attempt
                    raw_capture.deliver(_scope)
                _reset_app_context(_ctx_token)

        # Per-node concurrency cap (ENGINE_SPEC §4.6): at most
        # NodeDef.data.concurrency live invocations of THIS node inside
        # the step, nested INSIDE the run-level step semaphore so both
        # bounds hold simultaneously ("one Node B per item, max 5").
        try:
            node_sem = await self._node_gate(inv)
        except ExecutionError as e:
            # A "how many at once" read from the run's inputs that is not a valid cap: the step
            # fails with the plain sentence, never runs unbounded or at a guessed bound.
            result.error = e
            return
        except Exception as e:  # noqa: BLE001 — any other gate fault fails the step in words
            result.error = ExecutionError(f"Step '{inv.node_id}' could not start: {type(e).__name__}: {e}")
            result.error.__cause__ = e
            return

        async def _invoke_bounded(node_sem: _NodeGate | None = node_sem) -> None:
            if node_sem is not None:
                async with node_sem:
                    await _invoke()
            else:
                await _invoke()

        if self._step_sem is not None:
            # Bounded step parallelism (BS-6): the semaphore wraps the
            # WHOLE invocation (including retries/timeouts) so at most
            # step_concurrency nodes are live at once.
            async with self._step_sem:
                await _invoke_bounded()
        else:
            await _invoke_bounded()

    def _note_cost_emitted(self, invocation: Invocation, event: NodeCostEvent) -> None:
        key = (invocation.node_id, invocation.dispatch_id, invocation.item_index, invocation.firing)
        cost, tok_in, tok_out = self._cost_emitted.get(key, (0.0, 0, 0))
        self._cost_emitted[key] = (
            cost + float(event.cost_usd or 0.0),
            tok_in + int(event.input_tokens or 0),
            tok_out + int(event.output_tokens or 0),
        )

    async def _settle_interrupted_attempts(
        self,
        run_id: str,
        start_step: int,
        pending: list[Invocation],
        restarted: list[str],
        attempts: Sequence[InterruptedAttempt],
    ) -> None:
        """Settle each restart-cut attempt's ledger spend as its step's ``interrupted``
        node_cost. Deliberately NOT noted in ``_cost_emitted``: that map is what the NEW
        attempt's own tally is netted against, and the new attempt owes every cent it
        spends itself. Never raises — a cost tick never breaks a run; it screams."""
        for attempt in attempts:
            try:
                # Only a step that is starting again owns a cut-off attempt: a finished
                # sibling replays its recorded outcome and already settled its own cost.
                node_id = attempt.node_id
                if node_id is None or node_id not in restarted or node_id not in self.graph.nodes:
                    logger.error(
                        "[wf:%s] interrupted attempt %s names no step this run restarts "
                        "(node=%r, restarted=%s); its $%.6f is in the request ledger but "
                        "not on any step's cost",
                        run_id[:8], attempt.request_id, attempt.node_id, restarted,
                        attempt.cost_usd,
                    )
                    continue
                if attempt.cost_usd <= 0 and attempt.input_tokens <= 0 and attempt.output_tokens <= 0:
                    continue
                inv = next((i for i in pending if i.node_id == node_id), None)
                node = self.graph.nodes[node_id]
                await self._emit(
                    NodeCostEvent(
                        run_id=run_id,
                        step=inv.step if inv is not None and inv.step is not None else start_step,
                        node_id=node_id,
                        spec_type=getattr(node, "spec_type", None),
                        attempt=inv.attempt if inv is not None else 1,
                        dispatch_id=inv.dispatch_id if inv is not None else "",
                        item_index=inv.item_index if inv is not None else 0,
                        cost_usd=max(0.0, float(attempt.cost_usd)),
                        input_tokens=max(0, int(attempt.input_tokens)),
                        output_tokens=max(0, int(attempt.output_tokens)),
                        total_tokens=max(0, int(attempt.input_tokens)) + max(0, int(attempt.output_tokens)),
                        model=attempt.model,
                        models=[attempt.model] if attempt.model else [],
                        request_id=attempt.request_id,
                        interrupted=True,
                    )
                )
            except Exception:  # noqa: BLE001
                logger.exception(
                    "[wf:%s] settling interrupted attempt %s FAILED — the step's cost "
                    "under-reports its ledger spend",
                    run_id[:8],
                    attempt.request_id,
                )

    async def _settle_invocation_spend(
        self, run_id: str, step: int, inv: Invocation, tally: dict[str, Any]
    ) -> None:
        """Settle what this invocation's tally holds beyond its node_cost events — the spend of a
        step that raised or was cancelled after paying. Never raises."""
        try:
            if not tally:
                return
            cost, tok_in, tok_out = tally_totals(tally)
            key = (inv.node_id, inv.dispatch_id, inv.item_index, inv.firing)
            done_cost, done_in, done_out = self._cost_emitted.get(key, (0.0, 0, 0))
            rest = round(cost - done_cost, 6)
            rest_in = max(0, tok_in - done_in)
            rest_out = max(0, tok_out - done_out)
            if rest <= 0 and rest_in <= 0 and rest_out <= 0:
                return
            node = self.graph.nodes.get(inv.node_id)
            event = NodeCostEvent(
                run_id=run_id,
                step=step,
                node_id=inv.node_id,
                spec_type=getattr(node, "spec_type", None),
                attempt=inv.attempt,
                dispatch_id=inv.dispatch_id,
                item_index=inv.item_index,
                cost_usd=max(0.0, rest),
                input_tokens=rest_in,
                output_tokens=rest_out,
                total_tokens=rest_in + rest_out,
            )
            await self._emit(event)
            self._note_cost_emitted(inv, event)
        except Exception:  # noqa: BLE001 — a cost tick never breaks a run; it screams
            logger.exception(
                "[wf:%s node=%s] invocation spend settlement FAILED — node_cost under-reports "
                "this step's ledger spend",
                run_id[:8],
                inv.node_id,
            )

    async def _node_gate(self, inv: Invocation) -> _NodeGate | None:
        """The bound one invocation queues on: the node's own ``data.concurrency``, and for a
        FANNED invocation (it came from a Send) never more than the ``workflow.fan_out`` ceiling —
        the knob's default when the step declares nothing. A cost-bearing fanned node opens with
        ``paid_first_wave`` permits until its first item settles. None = unbounded (a plain,
        un-fanned node with no declared cap, exactly as before)."""
        node = self.graph.nodes[inv.node_id]
        declared = node.concurrency
        fanned = bool(inv.dispatch_id)
        if not declared and not fanned and not node.concurrency_input_ref:
            return None
        gate = self._node_sems.get(inv.node_id)
        if gate is not None:
            return gate
        if node.concurrency_input_ref:
            declared = self._concurrency_from_inputs(inv.node_id, node.concurrency_input_ref)
        if not fanned:
            return self._node_sems.setdefault(inv.node_id, _NodeGate(int(declared or 1)))
        if self._fan_out_policy is None:
            from matrx_graph.knobs import fan_out_policy

            self._fan_out_policy = await fan_out_policy()
        policy = self._fan_out_policy
        cap = min(int(declared or policy.default_item_concurrency), policy.max_item_concurrency)
        if declared and declared > cap:
            logger.warning(
                "[wf] step '%s' asks for %d items at once; the platform ceiling "
                "(workflow.fan_out max_item_concurrency) holds it at %d",
                inv.node_id,
                declared,
                cap,
            )
        from matrx_graph.spend_gate import is_cost_bearing

        spec = self.registry.get(node.spec_type).spec
        first_wave = policy.paid_first_wave if is_cost_bearing(spec) else cap
        return self._node_sems.setdefault(inv.node_id, _NodeGate(cap, first_wave))

    def _concurrency_from_inputs(self, node_id: str, ref: dict[str, Any]) -> int:
        """``data.concurrency`` as ``{"$input": name}``: this run's "how many at once", bound
        once per drive (the run's inputs do not change mid-run). The ``workflow.fan_out``
        ceiling still applies to it in ``_node_gate``. Not a whole number >= 1 → ExecutionError."""
        from matrx_graph.errors import UnresolvedInputError
        from matrx_graph.types.variables import resolve_var_refs
        from matrx_graph.validation import concurrency_cap

        try:
            value = resolve_var_refs(
                dict(ref),
                run_variables=self._run_variables,
                declared=self.graph.variables,
                node_id=node_id,
                run_inputs=self._run_inputs,
                input_surface=self.graph.input_surface,
            )
        except UnresolvedInputError as e:
            raise ExecutionError(str(e)) from e
        cap = concurrency_cap(value)
        if cap is None:
            raise ExecutionError(
                f"Step '{node_id}' reads how many to run at once from input '{ref['$input']}', "
                f"which is {value!r}. It must be a whole number of 1 or more."
            )
        return cap

    async def _spend_check(
        self, *, run_id: str, invocation: Invocation, spec: Any, app_ctx: Any
    ) -> Any:
        """The host's per-run spend answer for a cost-bearing launch (``spend_gate``), latched.

        Never raises: a gate that breaks is logged loudly and the launch proceeds (the provider
        boundary's own gate still stands behind it)."""
        from matrx_graph.spend_gate import SpendQuery, is_cost_bearing, spend_gate

        if not is_cost_bearing(spec):
            return None
        if self._spend_refusal is not None:
            return self._spend_refusal
        gate = spend_gate()
        if gate is None:
            return None
        try:
            refusal = await gate(
                SpendQuery(
                    run_id=run_id,
                    node_id=invocation.node_id,
                    spec_type=spec.node_type,
                    app=app_ctx,
                    definition_id=self.definition_id,
                )
            )
        except Exception:  # noqa: BLE001 — a broken check never blocks; it screams
            logger.exception(
                "[wf:%s node=%s] spend gate raised — launching without the per-run check",
                run_id[:8],
                invocation.node_id,
            )
            return None
        if refusal is not None:
            self._spend_refusal = refusal
            logger.warning(
                "[wf:%s node=%s] spend gate refused (%s) — no further paid step of this run "
                "is dispatched: %s",
                run_id[:8],
                invocation.node_id,
                refusal.code,
                refusal.approval_url or "",
            )
        return refusal

    async def _execute_invocation(
        self,
        run_id: str,
        thread_id: str,
        step: int,
        invocation: Invocation,
        result: _StepResult,
        channel_snapshot: dict[str, Any],
        step_app_ctx: AppContext,
        invocation_count: int,
    ) -> None:
        node = self.graph.nodes[invocation.node_id]
        executor = self.registry.get(node.spec_type)
        spec = executor.spec

        with span(
            "workflow.node",
            run_id=run_id,
            step=step,
            node_id=invocation.node_id,
            spec_type=spec.node_type,
            attempt=invocation.attempt,
            dispatch_id=invocation.dispatch_id,
            item_index=invocation.item_index,
            determinism=spec.determinism.value,
        ) as node_span:
            # Run once per key (data.once): the claim this invocation may take is released in
            # ``finally`` unless a success was stored under it — a failure, interrupt, cancel or
            # routable failure never leaves a key claimed.
            once_slot = OnceSlot()
            # One at a time per key (data.one_at_a_time): the turn this invocation may hold is
            # always given back here, however the step ends.
            turn_slot = TurnSlot()
            try:
                await self._execute_invocation_body(
                    run_id=run_id,
                    thread_id=thread_id,
                    step=step,
                    invocation=invocation,
                    result=result,
                    channel_snapshot=channel_snapshot,
                    step_app_ctx=step_app_ctx,
                    invocation_count=invocation_count,
                    node_span=node_span,
                    once_slot=once_slot,
                    turn_slot=turn_slot,
                )
            finally:
                # Nested, so a second cancel landing while the turn is given back can never
                # skip releasing the once claim.
                try:
                    await one_at_a_time_end(turn_slot)
                finally:
                    await once_finish(once_slot)

    async def _execute_invocation_body(
        self,
        *,
        run_id: str,
        thread_id: str,
        step: int,
        invocation: Invocation,
        result: _StepResult,
        channel_snapshot: dict[str, Any],
        step_app_ctx: AppContext,
        node_span: Any,
        invocation_count: int,
        once_slot: OnceSlot | None = None,
        turn_slot: TurnSlot | None = None,
    ) -> None:
        once_slot = once_slot if once_slot is not None else OnceSlot()
        turn_slot = turn_slot if turn_slot is not None else TurnSlot()
        node = self.graph.nodes[invocation.node_id]
        executor = self.registry.get(node.spec_type)
        spec = executor.spec

        # Pre-emptive skip: caller requested this node be short-circuited for
        # the run (e.g. "skip the slow LLM step while I'm iterating on the
        # rest of the graph"). Synthesize an empty output, record a
        # user_skip outcome, emit NodeSkippedEvent, return. Downstream edges
        # see an empty payload.
        if invocation.node_id in self._skip_node_ids:
            try:
                skipped_output = spec.output_schema.model_validate({})
            except Exception:  # noqa: BLE001
                # Schema has required fields — fall back to model_construct
                # which skips validation. Downstream nodes may break if they
                # depend on the missing fields, but that's the user's
                # explicit choice.
                skipped_output = spec.output_schema.model_construct()
            result.output = skipped_output
            result.channel_writes = []
            result.sends = []
            result.user_skipped = True
            set_attributes(node_span, **{"workflow.node.outcome": "user_skipped"})
            try:
                await self.checkpointer.record_outcome(
                    NodeOutcome(
                        run_id=run_id,
                        step=step,
                        node_id=invocation.node_id,
                        attempt=invocation.attempt,
                        dispatch_id=invocation.dispatch_id,
                        item_index=invocation.item_index,
                        output=model_dump_json(
                            skipped_output,
                            context=(f"[wf:{run_id[:8]} node={invocation.node_id}] node_skipped"),
                        ),
                        source="user_skip",
                    )
                )
            except Exception as outcome_err:  # noqa: BLE001
                record_exception(node_span, outcome_err)
                logger.warning(
                    "[wf:%s step=%d node=%s] user_skip outcome write failed "
                    "— replay integrity at risk: %s",
                    run_id[:8],
                    step,
                    invocation.node_id,
                    outcome_err,
                )
            await self._emit(
                NodeSkippedEvent(
                    run_id=run_id,
                    step=step,
                    node_id=invocation.node_id,
                    spec_type=spec.node_type,
                    attempt=invocation.attempt,
                    dispatch_id=invocation.dispatch_id,
                    item_index=invocation.item_index,
                    invocation_count=invocation_count,
                    output=model_dump_json(
                        skipped_output,
                        context=f"[wf:{run_id[:8]} node={invocation.node_id}] node_skipped",
                    ),
                    source="user_skip",
                    reason=self._not_ready.get(invocation.node_id),
                )
            )
            return

        # Phase 6.2 — per-node mock mode. If the user configured this
        # node with mock_response.enabled=true, we synthesise the
        # specified output instead of invoking the executor. Useful
        # for fast iteration (skip an LLM call) or dev-without-API-keys
        # (substitute a deterministic placeholder for a side-effectful
        # node). The mock output is validated against the node's
        # output_schema so a malformed mock fails loudly here rather
        # than corrupting downstream channel state.
        sampled = invocation.node_id in self._sampled_outputs
        # A SAMPLED step still runs its executor's pre-send checks (``sample_preflight``): the
        # inputs are resolved exactly as a live step resolves them, and a refusal (a missing
        # upstream, a request firewall hit) fails the step as the live call would — nothing is
        # sent. Executors without the hook are answered from the sample as before.
        preflight_record: Any = None
        if sampled and getattr(executor, "sample_preflight", None) is not None:
            try:
                preflight_record = await self._run_sample_preflight(
                    executor, node, spec, invocation, run_id, thread_id, step, channel_snapshot, step_app_ctx
                )
            except GraphInterrupt:
                raise
            except Exception as e:  # noqa: BLE001 — the live failure ladder, one attempt
                from matrx_graph.types.primitives import RetryPolicy

                await self._fail_attempt(
                    run_id=run_id,
                    step=step,
                    invocation=invocation,
                    node=node,
                    spec=spec,
                    policy=RetryPolicy(max_attempts=1),
                    attempt=invocation.attempt,
                    elapsed_ms=0,
                    err_type=type(e).__name__,
                    node_error=NodeError(
                        code=type(e).__name__,
                        message=client_message_for_exception(
                            e, step_label=self._step_label(invocation.node_id)
                        ),
                        details={
                            "sampled": True,
                            "technical_message": client_error_text(str(e), limit=TECHNICAL_TEXT_LIMIT),
                        },
                    ),
                    result=result,
                    node_span=node_span,
                    invocation_count=invocation_count,
                    exc=e,
                )
                return
        if sampled or node.mock_response is not None:
            # A mock is usually a SETTLED payload — a recording of what this node
            # really emitted, which by law carries ``__kind`` (proof-run replay
            # feeds exactly these back in). A closed legacy output_schema would
            # reject its own past output on the marker alone, so the mock takes
            # the SAME ingestion shim the checkpoint-replay path takes below:
            # the marker is reduced ONLY where this schema would fatally reject
            # it, never stripped from anything stored or forwarded.
            # A TEST run's answered step (``sampled_outputs``) takes the same seam with its
            # declared sample — announced as sampled everywhere, never as a real answer.
            mock_value: Any = (
                self._sampled_outputs[invocation.node_id] if sampled else node.mock_response
            )
            sampled_meta = (
                {"sampled": True, "reason": SAMPLED_STEP_REASON} if sampled else None
            )
            if sampled_meta is not None and preflight_record is not None:
                sampled_meta["preflight"] = preflight_record
            if isinstance(mock_value, dict):
                from matrx_graph.content_ir.markers import reduce_for_ingestion

                mock_value = reduce_for_ingestion(
                    mock_value, _input_schema_json(spec.output_schema)
                )
            try:
                mock_output = spec.output_schema.model_validate(mock_value)
            except Exception as e:  # noqa: BLE001
                raise ExecutionError(
                    f"the declared sample for step '{invocation.node_id}' does not fit its "
                    f"output: {e}"
                    if sampled
                    else f"mock_response invalid for node '{invocation.node_id}': {e}"
                ) from e
            result.output = mock_output
            # A mocked node still honors its output_channel binding —
            # otherwise every fan-in test/dev-run with mocks sees an empty
            # channel while the real run doesn't (divergent behavior). The
            # write is recorded on the outcome so crash-replay reproduces it.
            result.channel_writes = (
                [
                    (
                        node.output_channel,
                        model_dump_json(
                            mock_output,
                            context=f"[wf:{run_id[:8]} node={invocation.node_id}] mock channel_write",
                        ),
                    )
                ]
                if node.output_channel
                else []
            )
            result.sends = []
            set_attributes(
                node_span, **{"workflow.node.outcome": "sampled" if sampled else "mocked"}
            )
            # Round-1 F10: a mocked declared node must match the real run's
            # wire shape in exactly the dimension mocks promise not to diverge
            # — the mock dump gets the same root stamp settlement would apply,
            # and it is what routes (live) and what is recorded (replay routes
            # it back byte-identically).
            mock_dump = _stamp_mock_dump(
                model_dump_json(
                    mock_output,
                    context=f"[wf:{run_id[:8]} node={invocation.node_id}] mock outcome",
                ),
                node.output_kind,
            )
            result.settled_dump = mock_dump
            try:
                await self.checkpointer.record_outcome(
                    NodeOutcome(
                        run_id=run_id,
                        step=step,
                        node_id=invocation.node_id,
                        attempt=invocation.attempt,
                        dispatch_id=invocation.dispatch_id,
                        item_index=invocation.item_index,
                        output=mock_dump,
                        channel_writes=result.channel_writes,
                        source="mocked",
                        output_kind=node.output_kind,
                        metadata=sampled_meta,
                    )
                )
            except Exception as outcome_err:  # noqa: BLE001
                record_exception(node_span, outcome_err)
                logger.warning(
                    "[wf:%s step=%d node=%s] mocked outcome write failed — "
                    "replay integrity at risk: %s",
                    run_id[:8],
                    step,
                    invocation.node_id,
                    outcome_err,
                )
            # Mocked nodes emit a NodeSkippedEvent (the FE renders them
            # identically to user_skip — same "ghost" visual, plus the
            # cached output so downstream nodes see real data).
            await self._emit(
                NodeSkippedEvent(
                    run_id=run_id,
                    step=step,
                    node_id=invocation.node_id,
                    spec_type=spec.node_type,
                    attempt=invocation.attempt,
                    dispatch_id=invocation.dispatch_id,
                    item_index=invocation.item_index,
                    invocation_count=invocation_count,
                    output=model_dump_json(
                        mock_output,
                        context=f"[wf:{run_id[:8]} node={invocation.node_id}] mock outcome",
                    ),
                    source="mocked",
                    sampled=sampled,
                    reason=SAMPLED_STEP_REASON if sampled else None,
                )
            )
            invocation.attempt = invocation.attempt
            return

        # Retry loop. Each iteration is one attempt. We start at the
        # invocation's current attempt number (1 for fresh invocations, or
        # whatever the recovery API bumped it to). On a failed attempt with
        # retries remaining, we record a `source="retry"` outcome, emit
        # NodeRetryScheduledEvent, sleep, and loop. On a failed attempt with
        # no retries left, we record a normal outcome (source="executor")
        # and raise — _drive parks the run as ERRORED. On crash-and-resume,
        # the idempotency lookup recognizes prior retry-attempts and walks
        # forward through them without re-paying the backoff sleep.
        #
        # Phase 6.1 — per-node retry override. If the user set a
        # retry_policy on this node (via the inspector), it wins over the
        # registered NodeSpec's class-level default.
        policy = node.retry_policy or spec.retry
        attempt = invocation.attempt

        while True:
            # Idempotency: if a prior outcome exists for THIS attempt, either
            # replay it (success) or walk forward (failed retry, or exhausted
            # failure). Nodes that declare re_execute_on_resume SKIP this
            # check — the author has decided correctness requires re-running
            # fresh on every resume (timestamps, rate-limited calls mid-
            # backoff, notification side-effects, etc).
            prior = None
            # A fresh leg the host vouched for (``fresh_history``) has no
            # recorded outcome to find — skip the read before the node starts.
            if not spec.re_execute_on_resume and not self._history_known_empty:
                # Idempotency lookup at the FULL correlation key (ENGINE_SPEC
                # §4.2): (run_id, step, node_id, dispatch_id, item_index,
                # attempt). Sibling fan-out items can never find — let alone
                # replay — each other's outcomes (the audit-E2 corruption).
                prior = await self.checkpointer.get_outcome(
                    run_id=run_id,
                    step=step,
                    node_id=invocation.node_id,
                    attempt=attempt,
                    dispatch_id=invocation.dispatch_id,
                    item_index=invocation.item_index,
                )
                if prior is not None and self._replay_is_stale(prior, node, spec, invocation):
                    # Same key, different arguments: an upstream re-ran
                    # ("re-run from this step") and this node must see its
                    # NEW output — replaying the old one would be stale.
                    logger.info(
                        "[wf:%s step=%d node=%s] recorded outcome was produced from "
                        "different inputs — running fresh instead of replaying it",
                        run_id[:8],
                        step,
                        invocation.node_id,
                    )
                    prior = None

            if prior is not None:
                # ANY stored outcome steers this leg — a success replayed, or a failure walked
                # forward / routed down an ERROR edge (lane 11 rounds 5 and 7: node_outcome rows
                # are owner-writable). Remembered in memory so nothing downstream can count this
                # step as executed here.
                from matrx_graph.executor.execution import note_replayed

                note_replayed(run_id, invocation.node_id)

            if prior is not None and prior.error is None:
                # Successful replay — short-circuit without invoking executor.
                # Round-1 F3: recorded outcomes are SETTLED dumps — station 1
                # stamped ``__kind`` into them, and a closed legacy model
                # would reject its own history at replay, shunting every
                # stamped node through the LEGACY-REPLAY salvage below (an
                # error-level log on data the CURRENT code wrote, and an
                # unstamped resumed leg). Same gate as live ingestion: reduce
                # the marker only where this schema would fatally reject it.
                replay_value = prior.output
                salvaged = False
                try:
                    result.output = _coerce_replayed_output(spec.output_schema, replay_value)
                except Exception:  # noqa: BLE001
                    salvaged = True
                    if isinstance(replay_value, dict):
                        from matrx_graph.content_ir.markers import reduce_for_ingestion

                        replay_value = reduce_for_ingestion(
                            replay_value, _input_schema_json(spec.output_schema)
                        )
                    # LEGACY-REPLAY (Node Result System migration window): a
                    # run parked BEFORE a node's payload migration may hold
                    # outcome rows in the node's OLD shape (e.g. an http
                    # outcome with the removed ok/error fields, rejected by
                    # extra="forbid"). Re-validate with unknown keys stripped
                    # — LOUDLY — instead of re-parking a run on a node that
                    # actually succeeded (retry would re-execute a
                    # side-effectful call). Delete at ratchet zero.
                    filtered = {
                        k: v
                        for k, v in dict(replay_value).items()
                        if k in spec.output_schema.model_fields
                    }
                    result.output = spec.output_schema.model_validate(filtered)
                    logger.error(
                        "[wf:%s step=%d node=%s] LEGACY-REPLAY: recorded outcome "
                        "did not validate against the migrated %s — replayed with "
                        "unknown keys stripped (%s dropped). Pre-migration run "
                        "history; safe, but downstream consumers of the dropped "
                        "keys will miss them.",
                        run_id[:8],
                        step,
                        invocation.node_id,
                        spec.output_schema.__name__,
                        sorted(set(prior.output) - set(filtered)),
                    )
                # THE REPLAY WIRE IS THE RECORDED WIRE. A scheduler-written
                # outcome stores the SETTLED dump (``__kind`` stamped,
                # archetype intact); routing must carry exactly that, as the
                # live run did — never a re-dump of the model rebuilt above,
                # which for a closed legacy schema has the marker reduced
                # away. Re-dumping stripped it, so every downstream node's
                # inputs stopped matching its recorded ones and it RAN AGAIN on
                # each resume (a podcast child's audio, re-bought). Outcomes the
                # scheduler did NOT settle — skip / manual result, an answered
                # pause's resume value (executor-sourced but with no recorded
                # inputs), old rows — have no live wire and keep routing the
                # validated model — and so does a LEGACY-REPLAY salvage: the
                # recorded dump still holds the keys the salvage dropped, and
                # routing it would hand them to every downstream node.
                settled_here = not salvaged and (prior.source == "mocked" or (
                    prior.source in ("executor", "reused") and prior.inputs is not None
                ))
                if settled_here and isinstance(prior.output, dict):
                    result.settled_dump = prior.output
                result.channel_writes = list(prior.channel_writes)
                result.sends = list(prior.sends)
                # A replayed user_skip keeps its §3.4 join treatment on
                # resume — on_skipped_upstream must not silently flip to
                # propagate just because the run was parked and resumed.
                result.user_skipped = prior.source == "user_skip"
                result.reused = prior.source == "reused"
                # ENGINE_SPEC §5: restore the recorded ctx.emit payloads so
                # handle-keyed edge routing is byte-identical on replay. The
                # old "prior outcomes don't carry emissions" hole silently
                # pruned every branch/loop decision on errored-park resume,
                # crash replay, and step-mode replay (audit E3).
                result.emissions = dict(prior.emissions)
                set_attributes(node_span, **{"workflow.node.outcome": "skipped"})
                await self._emit(
                    NodeSkippedEvent(
                        run_id=run_id,
                        step=step,
                        node_id=invocation.node_id,
                        spec_type=spec.node_type,
                        attempt=attempt,
                        dispatch_id=invocation.dispatch_id,
                        item_index=invocation.item_index,
                        invocation_count=invocation_count,
                        output=prior.output,
                        # An answered pause / an approved held write replays as an
                        # executor outcome — the screen reads it as done, not skipped.
                        source=prior.source,
                    )
                )
                invocation.attempt = attempt
                return

            if prior is not None and prior.error is not None:
                # This attempt was tried + failed in a prior run (crash).
                # Walk forward through historic retries without re-paying
                # the sleep. If retries are exhausted, raise the final
                # failure so _drive parks at ERRORED.
                err_type = str(prior.error.get("type", "Exception"))
                err_message = str(prior.error.get("message", ""))
                prior_refused = is_caller_refusal(error=prior.error)
                if (
                    not prior_refused
                    and err_type not in _NON_RETRYABLE_ERROR_TYPES
                    and should_retry(policy, attempt, err_type)
                ):
                    await self._emit(
                        NodeRetryScheduledEvent(
                            run_id=run_id,
                            step=step,
                            node_id=invocation.node_id,
                            spec_type=spec.node_type,
                            attempt=attempt,
                            dispatch_id=invocation.dispatch_id,
                            item_index=invocation.item_index,
                            invocation_count=invocation_count,
                            next_attempt=attempt + 1,
                            delay_ms=0,
                            error_type=err_type,
                            error_message=err_message,
                        )
                    )
                    attempt += 1
                    continue
                # Exhausted on replay — emit the final NodeFailedEvent, then
                # park OR route exactly like a fresh exhausted failure. The
                # prior outcome already represents the failure; no need to
                # record another row. Routable dispositions (ERROR edge /
                # on_item_failure='hole') replay the ROUTE, not a park —
                # otherwise a crash between record and route would flip a
                # handled failure into a dead run.
                set_attributes(node_span, **{"workflow.node.outcome": "failed"})
                invocation.attempt = attempt
                await self._emit(
                    NodeFailedEvent(
                        run_id=run_id,
                        step=step,
                        node_id=invocation.node_id,
                        spec_type=spec.node_type,
                        attempt=attempt,
                        dispatch_id=invocation.dispatch_id,
                        item_index=invocation.item_index,
                        invocation_count=invocation_count,
                        error_type=err_type,
                        error_message=err_message,
                        error=dict(prior.error),
                    )
                )
                if self._failure_is_routable(node, invocation):
                    result.failure = NodeError(
                        code=str(prior.error.get("code", err_type)),
                        message=client_error_text(err_message),
                        details=(
                            prior.error.get("details")
                            if isinstance(prior.error.get("details"), dict)
                            else None
                        ),
                    )
                    return
                if prior_refused:
                    # A replayed REFUSAL stays the refusal — its structured error (code, sentence,
                    # approval link) reaches the run, never "exhausted retries".
                    raise NodeFailureError(
                        invocation.node_id,
                        NodeError(
                            code=str(prior.error.get("code") or err_type),
                            message=client_error_text(err_message),
                            details=(
                                prior.error.get("details")
                                if isinstance(prior.error.get("details"), dict)
                                else None
                            ),
                        ),
                    )
                raise ExecutionError(
                    f"Node '{invocation.node_id}' exhausted retries at "
                    f"attempt {attempt} (replayed): {err_type}: {err_message}"
                )

            # No prior outcome at this attempt — run the executor fresh.
            view = ChannelView(_values=dict(channel_snapshot), _pending_writes=[])
            ctx = NodeExecutionContext(
                app=step_app_ctx,
                run_id=run_id,
                thread_id=thread_id,
                node_id=invocation.node_id,
                step=step,
                attempt=attempt,
                channels=view,
                checkpointer=self.checkpointer,
                dispatch_id=invocation.dispatch_id,
                item_index=invocation.item_index,
                firing=invocation.firing,
                registry=self.registry,
                # The node's own kind declaration, handed to the executor. A
                # node that can SHAPE its output (ai.agent.produce binds the
                # model's response_format to the kind's schema) honors it;
                # every other node ignores it. Same slug the verdict below is
                # computed against — one declaration, not two.
                output_kind=node.output_kind,
                workflow_id=self.definition_id or None,
                # A relayed question's answer, handed once to the step that relayed it.
                resume_answer=self._forwarded_answers.pop(
                    (invocation.node_id, invocation.dispatch_id, invocation.item_index), None
                ),
            )
            # {"$run": "id"}: the run this invocation belongs to (a write can say who wrote it).
            self._run_facts = ctx.run_facts
            merged_inputs = resolve_invocation_inputs(
                node,
                self._with_declared_defaults(invocation.node_id, spec, invocation.inputs),
                run_variables=self._run_variables,
                declared_variables=self.graph.variables,
                run_inputs=self._run_inputs,
                input_surface=self.graph.input_surface,
                run_facts=self._run_facts,
            )
            # MKT-167 part 2: a value an upstream step HELD ON THE SERVER
            # (value_store.hold_on_server — a provision snapshot) travels through
            # channels, checkpoints and events as a reference only. The executor
            # gets the full value, resolved here; node_started and the outcome keep
            # the reference (restored below), so no event ever carries it inline.
            # Only whole ARGUMENTS resolve: a fan-out step handed a list of held
            # values passes the references on, and each target resolves its own.
            from matrx_graph.checkpoint.value_store import held_hash, resolve_step_inputs

            held_refs = {k: v for k, v in merged_inputs.items() if held_hash(v)}
            if held_refs:

                merged_inputs = {**merged_inputs, **(await resolve_step_inputs(run_id, held_refs))}
            # THE INGESTION GATE (plan §4, workflow design station 3 — the
            # audit's hard problem 2). Upstream payloads are self-described
            # (__kind in the data, by declaration or settlement propagation).
            # Identity TRAVELS by default: the marker is removed only at
            # positions where the receiving schema would fatally reject it —
            # an explicitly closed object (extra="forbid") that does not
            # declare the discriminator, i.e. the legacy shim. Open dict
            # args, unions, and KindModel args all keep it. One gate for
            # every value, before coercion, so the strip-order bug class
            # (validation stripped, coercion did not) is closed by
            # construction and the marker can never fatal a run at the next
            # node's door.
            from matrx_graph.content_ir.markers import reduce_for_ingestion

            merged_inputs = reduce_for_ingestion(
                merged_inputs, _input_schema_json(spec.input_schema)
            )
            # 2026-09-11 (expert-book challenge W28): this parse used to sit
            # OUTSIDE the routable-failure try below, so a node fed a value
            # its input schema refuses (an empty date, a text where named
            # values are required) parked the whole run even when the author
            # had wired an ERROR edge for exactly that case. The parse still
            # happens here (node_started wants the resolved arguments), but
            # its failure is raised inside the try, where every other failure
            # of this node is routable.
            input_gate_error: Exception | None = None
            # RUN IN ANOTHER ORGANIZATION (matrx_graph.in_organization): the target comes from the
            # step's resolved inputs or its setting, read here; the host admits the run's person
            # around the executor call below. A missing target refuses the step (routable), never
            # falls back to the run's organization.
            in_org_target: str | None = None
            if node.in_organization is not None:
                from matrx_graph.in_organization import (
                    admit_organization,
                    consume_setting_input,
                    target_organization,
                )

                try:
                    in_org_target = target_organization(node.in_organization, merged_inputs)
                    # ADMIT NOW, before run once per key can hand out a result saved in that
                    # organization: a reuse never reaches the executor call the switch wraps.
                    await admit_organization(ctx, in_org_target)
                except Exception as e:  # noqa: BLE001 — re-raised inside the routable try
                    input_gate_error = e
                merged_inputs = consume_setting_input(node.in_organization, merged_inputs, spec.input_schema)
            inputs_model: BaseModel | None
            try:
                inputs_model = spec.input_schema.model_validate(merged_inputs)
            except Exception as e:  # noqa: BLE001 — re-raised inside the routable try
                inputs_model = None
                input_gate_error = input_gate_error or e
            # Phase 5.3 — apply a one-shot config_override (set by the
            # "Retry without saving" recovery path) over the authored
            # config. Override values are merged on top of the compiled
            # config model's fields, then re-validated through the
            # spec's config_schema so type mistakes blow up here rather
            # than inside the executor.
            # SETTINGS FROM RUN INPUTS: a setting authored as {"$input": name} takes the
            # run's value (same resolution as a static input: run value → ref default →
            # declared default), re-validated through config_schema for THIS invocation.
            node_config = node.config
            if node.config_input_refs:
                from matrx_graph.types.variables import resolve_var_refs

                bound = model_dump_json(
                    node.config, context=f"[wf:{run_id[:8]} node={invocation.node_id}] setting refs"
                )
                resolved = resolve_var_refs(
                    dict(node.config_input_refs),
                    run_variables=self._run_variables,
                    declared=self.graph.variables,
                    node_id=invocation.node_id,
                    run_inputs=self._run_inputs,
                    input_surface=self.graph.input_surface,
                )
                for path, setting_value in resolved.items():
                    # "escalation.after_seconds": a number inside a settings object.
                    head, _, sub = path.partition(".")
                    if sub:
                        holder = bound.get(head)
                        bound[head] = {**(holder if isinstance(holder, dict) else {}), sub: setting_value}
                    else:
                        bound[path] = setting_value
                try:
                    node_config = spec.config_schema.model_validate(bound)
                except Exception as e:  # noqa: BLE001
                    raise ExecutionError(
                        f"node '{invocation.node_id}': a setting read from the run's inputs is not "
                        f"valid for this step: {e}"
                    ) from e
            if invocation.config_override:
                base = (
                    model_dump_json(
                        node_config,
                        context=(
                            f"[wf:{run_id[:8]} node={invocation.node_id}] config_override base"
                        ),
                    )
                    if isinstance(node_config, BaseModel)
                    else {}
                )
                base.update(invocation.config_override)
                try:
                    config_model = spec.config_schema.model_validate(base)
                except Exception as e:  # noqa: BLE001
                    raise ExecutionError(
                        f"config_override invalid for node '{invocation.node_id}': {e}"
                    ) from e
            else:
                config_model = node_config

            # Emit the FULLY RESOLVED arguments the executor actually
            # receives — static_inputs (authored on the node) merged with
            # the edge-routed payload, then validated through the spec's
            # input_schema. Emitting only ``invocation.inputs`` showed just
            # the edge payload and hid the node-authored params, so the
            # inspector's Run panel looked empty for nodes whose arguments
            # came from their own config. ``model_dump`` mirrors exactly
            # what the node was called with (defaults applied, types coerced).
            try:
                started_inputs = (
                    model_dump_json(
                        inputs_model,
                        context=f"[wf:{run_id[:8]} node={invocation.node_id}] node_started inputs",
                    )
                    if inputs_model is not None
                    else dict(merged_inputs)
                )
            except Exception:  # noqa: BLE001 — never let serialization kill a run
                started_inputs = dict(merged_inputs)
            if held_refs:
                started_inputs = {**started_inputs, **held_refs}
            if (
                node.once is not None
                and not once_slot.decided
                and input_gate_error is None
                and inputs_model is not None
            ):
                # RUN ONCE PER KEY — decided before paying, on the resolved arguments (held
                # values resolved, never their per-run references) and the effective config.
                if await once_decide(
                    self,
                    once_slot,
                    run_id=run_id,
                    step=step,
                    attempt=attempt,
                    invocation=invocation,
                    node=node,
                    spec=spec,
                    executor=executor,
                    ctx=ctx,
                    inputs_model=inputs_model,
                    digest_inputs=model_dump_json(
                        inputs_model,
                        context=f"[wf:{run_id[:8]} node={invocation.node_id}] once key",
                    ),
                    config_model=config_model,
                    config_dump=(
                        model_dump_json(
                            config_model,
                            context=f"[wf:{run_id[:8]} node={invocation.node_id}] once digest",
                        )
                        if isinstance(config_model, BaseModel)
                        else {}
                    ),
                    started_inputs=started_inputs,
                    result=result,
                    invocation_count=invocation_count,
                    # A step set to run in another organization saves and reuses its result THERE.
                    organization_id=in_org_target,
                ):
                    set_attributes(node_span, **{"workflow.node.outcome": "reused"})
                    invocation.attempt = attempt
                    return
            # THE PER-RUN SPEND CHECK (matrx_graph.spend_gate): a cost-bearing step asks the host
            # before it launches — after the items ahead of it in the fan-out settled. A refusal
            # ends this item with a typed refusal outcome (never retried) and latches, so no
            # further paid item of the run is dispatched; the run parks with the approval link.
            async def _end_as_spend_refusal(
                refusal: Any, elapsed_ms: int, at_attempt: int
            ) -> None:
                set_attributes(node_span, **{"workflow.node.outcome": "refused"})
                await self._fail_attempt(
                    run_id=run_id,
                    step=step,
                    invocation=invocation,
                    node=node,
                    spec=spec,
                    policy=policy,
                    attempt=at_attempt,
                    elapsed_ms=elapsed_ms,
                    err_type=refusal.code,
                    node_error=NodeError(
                        code=refusal.code,
                        message=refusal.message,
                        details=refusal.node_error_details(),
                    ),
                    result=result,
                    node_span=node_span,
                    invocation_count=invocation_count,
                    exc=None,
                )

            spend_refusal = await self._spend_check(
                run_id=run_id, invocation=invocation, spec=spec, app_ctx=step_app_ctx
            )
            if spend_refusal is not None:
                await _end_as_spend_refusal(spend_refusal, 0, attempt)
                return
            await self._emit(
                NodeStartedEvent(
                    run_id=run_id,
                    step=step,
                    node_id=invocation.node_id,
                    spec_type=spec.node_type,
                    attempt=attempt,
                    dispatch_id=invocation.dispatch_id,
                    item_index=invocation.item_index,
                    invocation_count=invocation_count,
                    inputs=started_inputs,
                    # The node's declared effective kind (compile-time
                    # resolution: spec.output_kind overridden by
                    # data.output_kind) — the SAME value settlement starts
                    # from (effective_output_kind = node.output_kind).
                    # Announced at start so the UI shows the kind's loading
                    # silhouette while the node streams.
                    output_kind=node.output_kind,
                )
            )
            step_mark = getattr(node, "review", None)
            if step_mark is not None:
                # Author mark "review if this runs": one flag per attempt that STARTS
                # (a replayed outcome never reaches here).
                await self._raise_review(
                    run_id,
                    invocation,
                    step=step,
                    attempt=attempt,
                    label=step_mark.label or f"flagged_step.{invocation.node_id}",
                    message=step_mark.reason,
                    category=step_mark.category,
                    source="flagged_step",
                )
            # DEPRECATED STEP (matrx_graph.deprecations): screams on every fresh run of it.
            await self._scream_deprecated_step(run_id, invocation, spec, step=step, attempt=attempt)
            if (
                node.one_at_a_time is not None
                and not turn_slot.decided
                and input_gate_error is None
                and inputs_model is not None
            ):
                # ONE AT A TIME PER KEY — wait (saying so on the step) while another invocation
                # holds this key's turn, then hold it for every attempt of this invocation.
                await one_at_a_time_take(
                    self,
                    turn_slot,
                    run_id=run_id,
                    step=step,
                    attempt=attempt,
                    invocation=invocation,
                    node=node,
                    ctx=ctx,
                    inputs=model_dump_json(
                        inputs_model,
                        context=f"[wf:{run_id[:8]} node={invocation.node_id}] one-at-a-time key",
                    ),
                )

            started = datetime.now(UTC)
            try:
                if input_gate_error is not None:
                    # The input-shape refusal, raised where it is routable
                    # (ERROR edge / fan-out hole) like any other failure.
                    raise input_gate_error
                if turn_slot.error is not None:
                    # data.one_at_a_time ended its wait without the turn: fail loudly, never
                    # run unguarded (a cancel then wins over this failure at the boundary).
                    raise turn_slot.error
                # Strict input contract. A dynamic-output SOURCE node
                # (io.user_input) carries the compiled JSON Schema its run form
                # is generated from, and its inputs ARE the run-form-seeded
                # values (no incoming edges). The permissive spec.input_schema
                # (extra="allow", zero fields) can't enforce the author's field
                # types/enums/required-ness, so a wrong-typed or out-of-enum
                # value would slip through and fail, confusingly, two steps
                # downstream. Validate against the real schema BEFORE the node
                # runs — inside this try so it parks the run on THIS node with a
                # per-field message, exactly like an executor failure. Non-source
                # / non-dynamic nodes have effective_output_schema=None and keep
                # their normal Pydantic validation — strictness by position.
                if spec.is_source and node.effective_output_schema is not None:
                    field_errors = await _source_input_problems(node, merged_inputs)
                    if field_errors:
                        raise NodeInputValidationError(
                            f"The values for '{invocation.node_id}' don't match "
                            "what this step asks for:\n  - " + "\n  - ".join(field_errors),
                            node_id=invocation.node_id,
                            field_errors=field_errors,
                        )
                # Kind-declared input contract (Shape system). When the node
                # (spec default or authored data.input_kind) names a platform
                # kind, the merged inputs must conform to that kind's
                # registered JSON Schema — same fatal, per-field posture as
                # the dynamic-source check above. A broken registration
                # (unregistered / no schema / malformed schema / unreachable
                # catalog) is a NAMED degraded outcome — loud inside
                # check_against_kind (platform defect, not user input),
                # non-blocking by default. With the workflow_io enforcement
                # flag ON, fatal-escalating degraded reasons and inactive
                # kinds park the run HERE, at the binding — only
                # catalog_unreachable stays degraded-but-not-fatal (an infra
                # outage must never masquerade as validation success OR take
                # down execution).
                if node.input_kind is not None:
                    from matrx_graph.kinds import (
                        check_against_kind,
                        degraded_escalation,
                        kind_enforcement_enabled,
                    )

                    # THE DECLARATION SUPPLIES THE IDENTITY (schema-law
                    # companion, 2026-08-23): kind schemas now DECLARE __kind
                    # (aidream e04b0d3cb), so a plain edge payload
                    # ({"text": ...} from a transform or regex node) would
                    # fail its own declared input kind for lacking a marker
                    # it has no author to supply — the first live casualty
                    # was Agent Foundry run 72ca63ab at extract_slug. The
                    # node's input_kind IS the identity claim; inject the
                    # root marker (copy-on-write) when the payload does not
                    # carry one. A payload that DOES carry a marker is
                    # validated as-is — a wrong self-identification must
                    # still fail loudly.
                    kind_inputs = _kind_contract_inputs(spec, merged_inputs)
                    if isinstance(kind_inputs, dict) and "__kind" not in kind_inputs:
                        kind_inputs = {"__kind": node.input_kind, **kind_inputs}
                    kind_check = await check_against_kind(kind_inputs, node.input_kind)
                    if kind_check.errors:
                        raise NodeInputValidationError(
                            f"The values for '{invocation.node_id}' don't match "
                            f"the '{node.input_kind}' kind it declares:\n  - "
                            + "\n  - ".join(kind_check.errors),
                            node_id=invocation.node_id,
                            field_errors=kind_check.errors,
                        )
                    if kind_enforcement_enabled("workflow_io"):
                        reason = kind_check.degraded_reason
                        if reason is not None and degraded_escalation(reason) == "fatal":
                            raise NodeInputValidationError(
                                f"Kind enforcement (workflow_io) is ON and the "
                                f"input kind '{node.input_kind}' declared by "
                                f"'{invocation.node_id}' cannot be validated: "
                                f"degraded_reason={reason.value}. Fix the kind "
                                f"registration or unbind the kind.",
                                node_id=invocation.node_id,
                                field_errors=[f"degraded_reason={reason.value}"],
                            )
                        # NO `is_active` GATE -- see the admission gate.
                # 🚨 THE STEP WALL CLOCK — every node attempt is bounded, always.
                # An authored ``NodeSpec.timeout_ms`` wins; a node that declares
                # none gets the platform ceiling (``workflow.step_clock``
                # ``default_step_seconds``, a row an admin turns, NOT a constant).
                # There is no third branch: an unbounded ``await
                # executor.execute(...)`` is the defect this closes — live
                # Masterwork run e991e70e node ``chief`` held one provider call
                # for 18m08s (chat.request 401262dc, api_duration_ms 1,087,650)
                # against ~82s for the identical node on two interactive runs,
                # while the run's streaming heartbeat kept beating. See
                # ``matrx_graph.knobs`` § THE STEP WALL CLOCK.
                from matrx_graph.knobs import step_timeout_seconds

                clock_seconds, clock_source = await step_timeout_seconds(
                    spec.timeout_ms, node_clock=node.step_clock
                )
                # THE LATCH HOLDS TO THE LAST INSTANT (matrx_graph.spend_gate): this launch was
                # admitted above, but every await since (started event, review flag, input
                # checks, the clock knob) let a sibling item ask the gate and be refused. A paid
                # call never STARTS after the run's refusal latched — re-read the latch with no
                # await between it and the call. (CI run 40455895731: two items admitted before
                # the refusal started their paid call after it.)
                if self._spend_refusal is not None and is_cost_bearing(spec):
                    await _end_as_spend_refusal(
                        self._spend_refusal,
                        int((datetime.now(UTC) - started).total_seconds() * 1000),
                        attempt,
                    )
                    return
                try:
                    try:
                        output = await asyncio.wait_for(
                            _execute_in_organization(
                                executor, ctx, inputs_model, config_model, in_org_target
                            ),
                            timeout=clock_seconds,
                        )
                    except TimeoutError:
                        raise NodeTimeoutError(
                            invocation.node_id,
                            int(clock_seconds * 1000),
                            attempt,
                            source=clock_source,
                        ) from None
                except Exception:
                    # Raised, timed out, or interrupted: whatever the node
                    # streamed before it stopped still lands before the
                    # node_failed / retry / interrupt event this unwinds into.
                    # (CancelledError is not Exception — a canceled run is
                    # never held open for its live wire.)
                    await self._settle_node_emitter(step_app_ctx, run_id, invocation)
                    raise
                await self._settle_node_emitter(step_app_ctx, run_id, invocation)
            except GraphInterrupt as gi:
                set_attributes(node_span, **{"workflow.node.outcome": "interrupted"})
                record_exception(node_span, gi)
                invocation.attempt = attempt
                raise
            except Exception as e:
                elapsed_ms = int((datetime.now(UTC) - started).total_seconds() * 1000)
                # Node Result System: a raised exception is synthesized into
                # the SAME structured failure shape as a returned Failure —
                # one namespace (``code`` == exception class name, exactly
                # what RetryPolicy.retry_on matches), one ladder.
                err_type = type(e).__name__
                # Input-gate structured errors: NodeInputValidationError
                # carries per-field messages — put them on the structured
                # error's details so the wire (node_failed.error.details.
                # field_errors + node_outcome.error) gets the list, not just
                # the joined message string.
                field_errors = getattr(e, "field_errors", None)
                details = (
                    {"field_errors": list(field_errors)}
                    if isinstance(field_errors, list) and field_errors
                    else None
                )
                # Structured refusals (duck-typed `e.error_info`, the same
                # contract matrx-connect's stream-crash handler reads — e.g.
                # aidream's EducationConsentRequiredError) carry a
                # `user_message` written for the person and an `error_type`
                # the client keys recovery on. The run-level error is what the
                # user SEES, so prefer the human line; keep the technical
                # message (which may name ids) in details for operators.
                error_info = getattr(e, "error_info", None)
                user_message = getattr(error_info, "user_message", None)
                # NEVER ``str(e)`` as the client message: a matrx-orm error
                # renders a terminal banner with the statement and its bound
                # args. The full render goes to the log; the client gets one
                # sentence (the exception's own person_message when it has one).
                message = client_message_for_exception(
                    e, step_label=self._step_label(invocation.node_id)
                )
                technical = client_error_text(str(e), limit=TECHNICAL_TEXT_LIMIT)
                if message != technical:
                    logger.warning(
                        "[wf:%s step=%d node=%s attempt=%d] node raised %s — client "
                        "message redacted; full diagnostic follows:\n%s",
                        run_id[:8],
                        step,
                        invocation.node_id,
                        attempt,
                        err_type,
                        e,
                    )
                # Duck-typed structured context a host attached to the exception
                # on its way out (e.g. aidream's request ledger: the calls the
                # step made before it raised) lands on the failure's details.
                extra_details = getattr(e, "node_error_details", None)
                if isinstance(extra_details, dict) and extra_details:
                    details = {**extra_details, **(details or {})}
                if isinstance(user_message, str) and user_message.strip():
                    details = dict(details or {})
                    details["technical_message"] = technical
                    error_type = getattr(error_info, "error_type", None)
                    if isinstance(error_type, str) and error_type:
                        details["error_type"] = error_type
                node_error = NodeError(code=err_type, message=message, details=details)
                disposition = await self._fail_attempt(
                    run_id=run_id,
                    step=step,
                    invocation=invocation,
                    node=node,
                    spec=spec,
                    policy=policy,
                    attempt=attempt,
                    elapsed_ms=elapsed_ms,
                    err_type=err_type,
                    node_error=node_error,
                    result=result,
                    node_span=node_span,
                    invocation_count=invocation_count,
                    exc=e,
                )
                if disposition == "retry":
                    attempt += 1
                    continue
                # "handled": the failure routes (ERROR edge / fan-out hole);
                # result.failure carries it to _route_outputs.
                return

            elapsed_ms = int((datetime.now(UTC) - started).total_seconds() * 1000)

            # Node Result System (Layer 1): the executor returned the
            # NodeResult envelope. The scheduler is the ONLY consumer of the
            # envelope — a Success unwraps HERE and the bare payload T flows
            # downstream exactly as before (mappings, predicates, channels,
            # outcome.output, events all see T); a returned Failure goes
            # through the SAME retry/route/park ladder as a raised exception.
            if isinstance(output, Failure):
                node_error = output.error
                disposition = await self._fail_attempt(
                    run_id=run_id,
                    step=step,
                    invocation=invocation,
                    node=node,
                    spec=spec,
                    policy=policy,
                    attempt=attempt,
                    elapsed_ms=elapsed_ms,
                    err_type=node_error.code,
                    node_error=node_error,
                    result=result,
                    node_span=node_span,
                    invocation_count=invocation_count,
                    exc=None,
                )
                if disposition == "retry":
                    attempt += 1
                    continue
                return

            if isinstance(output, Success):
                payload = output.result
                if not isinstance(payload, spec.output_schema):
                    # Pydantic parametrized generics are exact classes —
                    # Value(value=1) / Value[int](value=1) are NOT instances
                    # of Value[Any]. Accept a payload whose class shares the
                    # schema's generic ORIGIN before declaring drift.
                    origin = (
                        getattr(spec.output_schema, "__pydantic_generic_metadata__", None) or {}
                    ).get("origin")
                    if origin is None or not isinstance(payload, origin):
                        # Author-drift guard: the envelope's T must be the
                        # node's declared output_schema — this replaces (and
                        # sharpens) the old bare isinstance(BaseModel) check.
                        raise ExecutionError(
                            f"Node '{invocation.node_id}' ({spec.node_type}) "
                            f"returned Success[{type(payload).__name__}]; its "
                            f"declared output_schema is "
                            f"{spec.output_schema.__name__}."
                        )
                output = payload
            else:
                # Anything that is not a Success/Failure — including a bare
                # BaseModel payload (the pre-envelope legacy form, deleted at
                # ratchet zero) — is an author defect.
                raise ExecutionError(
                    f"Node '{invocation.node_id}' ({spec.node_type}) returned "
                    f"{type(output).__name__}; expected NodeResult["
                    f"{spec.output_schema.__name__}] — wrap the payload with "
                    f"success(...)."
                )

            result.output = output
            result.channel_writes = view.drain()
            ctx_channel_writes = len(result.channel_writes)
            if node.output_channel:
                # Per-node binding: the node's whole output participates in
                # reducer-based fan-in (the only aggregation that survives
                # send-driven parallelism — edge routing merges per-target
                # last-writer-wins).
                result.channel_writes.append(
                    (
                        node.output_channel,
                        model_dump_json(
                            output,
                            context=(f"[wf:{run_id[:8]} node={invocation.node_id}] channel_write"),
                        ),
                    )
                )
            result.sends = ctx.drain_sends()
            result.emissions = ctx.drain_emissions()
            beside_fields = ctx.beside_kind_fields() if hasattr(ctx, "beside_kind_fields") else frozenset()
            if beside_fields:
                self._beside_kind[invocation.node_id] = frozenset(beside_fields)

            set_attributes(
                node_span,
                **{
                    "workflow.node.outcome": "completed",
                    "workflow.node.duration_ms": elapsed_ms,
                    "workflow.node.sends_emitted": len(result.sends),
                    "workflow.node.channels_written": len(result.channel_writes),
                },
            )
            output_dump = model_dump_json(
                output,
                context=f"[wf:{run_id[:8]} node={invocation.node_id}] node_completed",
            )
            # Shape-verification truth (Content-IR Studio spec §5) — computed
            # once, carried on BOTH the node_completed event and the persisted
            # outcome row. None = no kind declared or the catalog loud-skipped
            # (fail-open platform defect) — neutral, never rendered as a pass.
            output_kind_ok: bool | None = None
            output_kind_errors: list[str] | None = None
            output_kind_version: int | None = None
            output_kind_degraded: str | None = None
            # Runtime kind propagation — the missing primitive the audit named,
            # made nearly free by discriminator-as-data (plan §4.1/§7): when a
            # node declares no output kind (pass-throughs: data.transform,
            # pipe.step, subgraph.call, tool.call...), the payload's OWN
            # declaration is the effective kind — "output kind = the kind of
            # what actually flowed". It gets the SAME registry verification as
            # a declared kind, so a payload lying about itself screams exactly
            # like author drift; a payload carrying no __kind changes nothing
            # (kind stays None — today's behavior, the honest answer).
            effective_output_kind = node.output_kind
            output_kind_declared = node.output_kind is not None
            if effective_output_kind is None:
                from matrx_graph.content_ir.model import kind_of

                effective_output_kind = kind_of(output_dump)
                if effective_output_kind == "json":
                    # 'json' is a format word, never an identity (round-1 F7)
                    # — refuse to adopt it from a payload just as specs no
                    # longer declare it.
                    effective_output_kind = None
            if effective_output_kind is not None:
                # Shape-system output contract. A mismatch here is the NODE
                # AUTHOR's defect (the executor produced something its declared
                # kind doesn't describe), not user input — so it never fails
                # the run by default, but it must scream (mirrors
                # validate_instance's malformed-schema posture). The outcome
                # still records the declared kind (+ version + named degraded
                # reason) so drift AND skips are inspectable — a skipped check
                # is never renderable as a pass. With the workflow_io
                # enforcement flag ON, a violation (or a fatal-escalating
                # degraded reason / inactive kind) becomes an execution
                # failure through the unified _fail_attempt ladder instead of
                # a logged verdict; catalog_unreachable stays loudly degraded
                # even when enforced.
                from matrx_graph.kinds import (
                    check_against_kind,
                    degraded_escalation,
                    kind_enforcement_enabled,
                )

                # Validate the CANDIDATE SETTLEMENT, not the raw dump. The
                # SCHEMA LAW (2026-08-23) makes every emitted_json_schema
                # require the root `__kind`; a deterministic node's payload is
                # a pydantic dump with no marker field, and STATION 1 below is
                # what stamps it. Checking the pre-stamp dump therefore failed
                # every plain declared node with "'__kind' is a required
                # property" — and the failed verdict then blocked the very
                # stamp that would have satisfied it (feedback 77069e51).
                # So the check sees the dump AS SETTLEMENT WILL SHIP IT: a
                # local copy with the root marker, mirroring _stamp_mock_dump.
                # Root only — nested markers are the payload's own to carry
                # (a kind whose schema requires nested `__kind` that a
                # deterministic producer never emits is a modeling error, and
                # it still fails here loudly, which is the honest verdict).
                # output_dump itself is untouched: STATION 1 below remains the
                # single stamping site, honesty guard included.
                check_value: dict[str, Any] | Any = output_dump
                # Keys the step declared BESIDE its kind (ctx.declare_beside_kind:
                # a typed agent also handing over its run facts) are not the kind's.
                beside = ctx.beside_kind_fields() if hasattr(ctx, "beside_kind_fields") else frozenset()
                if beside and isinstance(check_value, dict):
                    check_value = {k: v for k, v in check_value.items() if k not in beside}
                if (
                    effective_output_kind != "json"
                    and isinstance(output_dump, dict)
                    and "__kind" not in output_dump
                ):
                    check_value = {**check_value, "__kind": effective_output_kind}
                kind_check = await check_against_kind(check_value, effective_output_kind)
                if (
                    not output_kind_declared
                    and kind_check.degraded_reason is not None
                    and kind_check.degraded_reason.value == "kind_not_registered"
                ):
                    # Round-1 F6: a SELF-DESCRIBED slug is arbitrary payload
                    # content (user JSON through a pass-through can carry any
                    # `__kind`). An unregistered slug from that path is not a
                    # platform defect and not an identity — treating it as a
                    # declaration let user data fatal a run under enforcement
                    # and pollute the output_kind column. Unknown + undeclared
                    # = NO kind: neutral verdict, no stamp, no escalation.
                    # (A DECLARED-but-unregistered kind keeps today's loud
                    # degraded posture — that one IS a platform defect.)
                    effective_output_kind = None
                    kind_check = None  # type: ignore[assignment]
                if kind_check is None:
                    output_kind_version = None
                else:
                    output_kind_version = kind_check.kind_version
                if kind_check is None:
                    pass  # F6: no kind — verdict stays neutral end to end
                elif kind_check.checked:
                    output_kind_ok = not kind_check.errors
                    output_kind_errors = kind_check.errors or None
                elif kind_check.degraded_reason is not None:
                    output_kind_degraded = kind_check.degraded_reason.value
                    # Run-scoped context log, throttled to once per
                    # (run, slug) — the catalog already screamed once per
                    # process per slug at error level, and every
                    # event/outcome carries the degraded reason anyway, so
                    # per-step repetition on the hot path is pure noise.
                    throttle_key = (run_id, effective_output_kind)
                    if throttle_key not in self._kind_degraded_warned:
                        self._kind_degraded_warned.add(throttle_key)
                        logger.warning(
                            "[wf:%s step=%d node=%s] output kind '%s' check "
                            "DEGRADED (degraded_reason=%s) — verdict is "
                            "neutral, NOT a pass. (Logged once per run per "
                            "kind; every affected outcome row carries the "
                            "reason.)",
                            run_id[:8],
                            step,
                            invocation.node_id,
                            effective_output_kind,
                            output_kind_degraded,
                        )
                if kind_check is not None and kind_check.errors:
                    logger.error(
                        "[wf:%s step=%d node=%s] output does NOT match its "
                        "declared kind '%s' — node-author defect%s. "
                        "Errors:\n  - %s",
                        run_id[:8],
                        step,
                        invocation.node_id,
                        effective_output_kind,
                        (
                            ", FATAL (workflow_io enforcement ON)"
                            if kind_enforcement_enabled("workflow_io")
                            else ", run continues"
                        ),
                        "\n  - ".join(kind_check.errors),
                    )
                if kind_check is not None and not kind_enforcement_enabled("workflow_io") and (
                    kind_check.errors
                    or (
                        output_kind_declared
                        and kind_check.degraded_reason is not None
                        # an unreachable catalog is infrastructure, not this workflow
                        and kind_check.degraded_reason.value != "catalog_unreachable"
                    )
                ):
                    # The run goes on with an output its kind could not vouch for — a
                    # review flag (enforced, the same case fails the step instead).
                    await self._raise_review(
                        run_id,
                        invocation,
                        step=step,
                        attempt=attempt,
                        label="engine.output_shape",
                        message=(
                            f"Output does not match its kind '{effective_output_kind}'"
                            if kind_check.errors
                            else f"Output kind '{effective_output_kind}' could not be checked "
                            f"({kind_check.degraded_reason.value})"  # type: ignore[union-attr]
                        ),
                        category="degraded_output",
                        payload={
                            "kind": effective_output_kind,
                            "errors": list(kind_check.errors or [])[:10],
                            "degraded_reason": (
                                kind_check.degraded_reason.value
                                if kind_check.degraded_reason is not None
                                else None
                            ),
                        },
                    )
                if kind_check is not None and kind_enforcement_enabled("workflow_io"):
                    # "declared" = the node author's contract; "self-described"
                    # = the payload's own __kind, propagated at settlement — a
                    # violation there means the payload LIES about itself
                    # (upstream's defect), and the message must say which.
                    kind_word = "declared" if output_kind_declared else "self-described"
                    fatal_message: str | None = None
                    if kind_check.errors:
                        fatal_message = (
                            f"Output of '{invocation.node_id}' violates its "
                            f"{kind_word} kind '{effective_output_kind}' and "
                            f"workflow_io kind enforcement is ON:\n  - "
                            + "\n  - ".join(kind_check.errors)
                        )
                    elif (
                        kind_check.degraded_reason is not None
                        and degraded_escalation(kind_check.degraded_reason) == "fatal"
                    ):
                        fatal_message = (
                            f"Output kind '{effective_output_kind}' {kind_word} by "
                            f"'{invocation.node_id}' cannot be validated "
                            f"(degraded_reason={kind_check.degraded_reason.value}) "
                            f"and workflow_io kind enforcement is ON. Fix the "
                            f"kind registration or unbind the kind."
                        )
                    # NO `is_active` GATE -- see the admission gate.
                    if fatal_message is not None:
                        # Route through the unified failure ladder so the
                        # violation is a structured, recoverable execution
                        # failure — and the invalid typed output is NEVER
                        # stored as a successful outcome. _StepResult.failure
                        # is mutually exclusive with output/success, so the
                        # already-captured output and its side-channel writes
                        # are discarded before failing the attempt.
                        result.output = None
                        result.channel_writes = []
                        result.sends = []
                        result.emissions = {}
                        exc = ExecutionError(fatal_message)
                        node_error = NodeError(
                            code="KindContractViolation",
                            message=fatal_message,
                            details={
                                "output_kind": effective_output_kind,
                                "output_kind_version": output_kind_version,
                                "degraded_reason": output_kind_degraded,
                                "field_errors": kind_check.errors or None,
                            },
                        )
                        disposition = await self._fail_attempt(
                            run_id=run_id,
                            step=step,
                            invocation=invocation,
                            node=node,
                            spec=spec,
                            policy=policy,
                            attempt=attempt,
                            elapsed_ms=elapsed_ms,
                            err_type="KindContractViolation",
                            node_error=node_error,
                            result=result,
                            node_span=node_span,
                            invocation_count=invocation_count,
                            exc=exc,
                        )
                        if disposition == "retry":
                            attempt += 1
                            continue
                        return
            # Content IR envelope hand-off (Studio spec §6 P3 / D2): a
            # VERIFIED output (checked=True, no errors) ships a canonical
            # CanonicalBlockIR at metadata.__ir so consumers (the Studio's
            # readEnvelope/sanitizeInboundEnvelopeMetadata trusted path)
            # render it without re-parsing. Verified-only — drift, degraded,
            # or kind-less outputs get NO envelope (the verdict fields above
            # already carry that truth; an envelope IS a rendered pass).
            # Wire shape: root.value is ELIDED (value_ref="output" marks it)
            # because the same dict rides the event's own `output` field —
            # the consumer's ingest gate rehydrates it, so nothing is
            # serialized twice per event / per wf_node_events row.
            # Loud fail-open: assembly is pure metadata and must never fail
            # the run — a stamping bug screams and the event ships bare.
            # STATION 1 — SETTLEMENT STAMPING (plan §4.2; workflow design
            # station 1). The one law: a payload SAYS what it is. KindModel
            # outputs already carry the discriminator as declared data; a
            # DECLARED node whose (legacy) pydantic model predates KindModel
            # gets the root marker injected here, so every settled payload is
            # self-describing on the wire, in the outcome row, and everywhere
            # it travels afterwards. The stamping ITSELF lives in
            # ``stamp_kind_marker`` (content_ir.envelope) because settlement
            # is not the only boundary a node payload crosses — the isolated
            # node-test path and tool.call's inner dispatch dump payloads the
            # scheduler never sees, and they were shipping unstamped (live
            # 2026-09-09: the Text to Data Test Step sample failed the
            # Studio's structural check for a missing root `__kind`).
            # Honesty guard, and it stays HERE because only settlement holds
            # the verdict: never stamp on a FAILED verdict (output_kind_ok is
            # False) — stamping a payload with a kind it measurably violates
            # would make the data lie; the column + verdict fields still
            # record the declared kind and the drift. Neutral (no check ran /
            # loud-skip) stamps: declared intent is the best truth available,
            # same posture as the output_kind column itself.
            if output_kind_ok is not False:
                stamp_kind_marker(output_dump, effective_output_kind)
            # Round-1 F2: hand the settled dump to routing/broadcast/
            # last_outputs — the wire carries what settlement produced.
            result.settled_dump = output_dump if isinstance(output_dump, dict) else None
            output_ir_metadata: dict[str, Any] | None = None
            if output_kind_ok is True:
                # output_kind_ok=True implies effective_output_kind was
                # resolved (declared OR self-described/propagated), so the
                # slug is present by construction.
                try:
                    from matrx_graph.content_ir.envelope import (
                        ir_metadata_for_verified_output,
                    )

                    output_ir_metadata = ir_metadata_for_verified_output(
                        output_dump, effective_output_kind
                    )
                except Exception:  # noqa: BLE001 — never load-bearing (law 3)
                    logger.error(
                        "[wf:%s step=%d node=%s] Content IR envelope stamping "
                        "FAILED for verified kind '%s' — node_completed ships "
                        "WITHOUT metadata.__ir (consumers fall back to their "
                        "own classification). This is a platform defect.",
                        run_id[:8],
                        step,
                        invocation.node_id,
                        effective_output_kind,
                        exc_info=True,
                    )
            # THE PACKET (plan §10b item 8): the same completion as a
            # self-describing ``node_outcome`` runtime-wrapper kind instance.
            # Payload ELIDED — ``output_ref="output"`` names this event's own
            # ``output`` field (the ``__ir`` value_ref rule, same reason: never
            # serialize the same dict twice per event / per persisted row).
            # Additive: every column above is untouched and consumers migrate
            # at their own pace. Loud fail-open — a defect here screams and the
            # event ships without the wrapper; it never fails a run.
            outcome_wrapper: dict[str, Any] | None = None
            try:
                from matrx_graph.content_ir.runtime_view import (
                    OUTPUT_REF_OUTPUT,
                    node_outcome_view,
                )

                outcome_wrapper = node_outcome_view(
                    run_id=run_id,
                    node_id=invocation.node_id,
                    workflow_id=self.definition_id or None,
                    step=step,
                    attempt=attempt,
                    status="completed",
                    output_kind=effective_output_kind,
                    output_kind_ok=output_kind_ok,
                    output_kind_errors=output_kind_errors,
                    duration_ms=elapsed_ms,
                    started_at=started.isoformat(),
                    ended_at=datetime.now(UTC).isoformat(),
                    output_ref=OUTPUT_REF_OUTPUT,
                )
            except Exception:  # noqa: BLE001 — never load-bearing
                logger.error(
                    "[wf:%s step=%d node=%s] node_outcome wrapper assembly "
                    "FAILED — node_completed ships WITHOUT the runtime wrapper "
                    "(consumers fall back to the flat columns). This is a "
                    "platform defect.",
                    run_id[:8],
                    step,
                    invocation.node_id,
                    exc_info=True,
                )
            # The outcome lands BEFORE the completion event: record_outcome writes the
            # step's large output values and the row in ONE transaction, and the event
            # that follows finds those values already stored (no transaction of its own).
            # Run once per key: a result that will not be saved for reuse says why ON the
            # outcome (degraded, topology) — never only in a log.
            once_not_saved = once_not_saved_reason(
                once_slot, result=result, output_dump=output_dump, ctx_channel_writes=ctx_channel_writes,
                warning_count=ctx.warning_count, output_kind_ok=output_kind_ok,
                output_kind_degraded=output_kind_degraded,
            )
            outcome_metadata: dict[str, Any] | None = (
                {"warning_count": ctx.warning_count} if ctx.warning_count else None
            )
            if once_not_saved:
                outcome_metadata = {**(outcome_metadata or {}), "once_not_saved": once_not_saved}
            completed_outcome = NodeOutcome(
                    run_id=run_id,
                    step=step,
                    node_id=invocation.node_id,
                    attempt=attempt,
                    dispatch_id=invocation.dispatch_id,
                    item_index=invocation.item_index,
                    output=output_dump,
                    # C-30: the INPUT half of this occurrence, persisted on the
                    # same row as the output. `started_inputs` is the exact dict
                    # the executor was called with — already computed above for
                    # NodeStartedEvent, which until now was the ONLY place it
                    # existed, and an event stream is a narration, not a
                    # per-occurrence record a replay can start from.
                    inputs=started_inputs,
                    input_kind=node.input_kind,
                    # ctx.warn count — the step worked but missed something
                    # (rows in workflow.run_log); surfaces badge from this.
                    metadata=outcome_metadata,
                    channel_writes=result.channel_writes,
                    sends=result.sends,
                    # ENGINE_SPEC §5: emissions persist alongside sends /
                    # channel_writes so replay restores handle routing.
                    emissions=result.emissions,
                    duration_ms=elapsed_ms,
                    output_kind=effective_output_kind,
                    output_kind_ok=output_kind_ok,
                    output_kind_errors=output_kind_errors,
                    output_kind_version=output_kind_version,
                    output_kind_degraded=output_kind_degraded,
            )
            completed_event = NodeCompletedEvent(
                    run_id=run_id,
                    step=step,
                    node_id=invocation.node_id,
                    spec_type=spec.node_type,
                    attempt=attempt,
                    dispatch_id=invocation.dispatch_id,
                    item_index=invocation.item_index,
                    invocation_count=invocation_count,
                    duration_ms=elapsed_ms,
                    output=output_dump,
                    output_kind=effective_output_kind,
                    output_kind_ok=output_kind_ok,
                    output_kind_errors=output_kind_errors,
                    output_kind_version=output_kind_version,
                    output_kind_degraded=output_kind_degraded,
                    metadata=output_ir_metadata,
                    wrapper=outcome_wrapper,
            )
            if (
                DEFER_PURE_STEP_OUTCOMES
                and step not in self._no_defer_steps
                # START WHEN READY: a launch for a LATER step writes at once — held for the
                # current step's checkpoint it would sit behind the slow member it overtook.
                and not (self._eager_ahead and self._loop_step is not None and step > self._loop_step)
                and getattr(self.checkpointer, "save_checkpoint_with_outcomes", None) is not None
                and spec.determinism == ActionTier.PURE
                and spec.category not in (NodeCategory.AGENT, NodeCategory.LLM)
                and once_slot.claim is None
                and turn_slot.claim is None
                and not invocation.work_item_id
            ):
                # Lands with the step's checkpoint (``_save_checkpoint``), event after it.
                self._deferred_outcomes.append((completed_outcome, completed_event))
            else:
                await self.checkpointer.record_outcome(completed_outcome)
                await self._emit(completed_event)
            # Cost settlement (the live spend ticker). An AGENT/LLM node whose
            # output carries the canonical AI usage block (the
            # AiExecutionResult ``usage`` shape) settles its billed cost as a
            # typed node_cost event — one per invocation, durable via the
            # host's event recorder. The category gate matters: pass-through
            # nodes (output.to_frontend, data shapers) forward the upstream
            # payload VERBATIM, usage block included — sniffing every output
            # double-counted the same spend once per hop (seen live
            # 2026-07-06). Every AI cost producer declares AGENT or LLM.
            if spec.category in (NodeCategory.AGENT, NodeCategory.LLM):
                # Preferred: the executor DECLARED its spend on the engine
                # plane (ctx.record_billed_usage). Required for any node whose
                # payload is a platform kind — a strict kind has nowhere to
                # carry a usage block, so sniffing the payload would silently
                # lose the tick. Falls back to the payload for every node that
                # still returns the AiExecutionResult envelope.
                cost_source = ctx.drain_billed_usage() or output_dump
                cost_event = node_cost_from_output(
                    cost_source,
                    run_id=run_id,
                    step=step,
                    node_id=invocation.node_id,
                    spec_type=spec.node_type,
                    attempt=attempt,
                    dispatch_id=invocation.dispatch_id,
                    item_index=invocation.item_index,
                )
                if cost_event is not None:
                    await self._emit(cost_event)
                    self._note_cost_emitted(invocation, cost_event)
            if once_slot.claim is not None:
                await once_settle(
                    once_slot,
                    self,
                    run_id=run_id,
                    step=step,
                    attempt=attempt,
                    invocation=invocation,
                    node=node,
                    result=result,
                    output_dump=output_dump,
                    verdict={
                        "output_kind_ok": output_kind_ok,
                        "output_kind_errors": output_kind_errors,
                        "output_kind_version": output_kind_version,
                        "output_kind_degraded": output_kind_degraded,
                    },
                    output_kind=effective_output_kind,
                    not_saved=once_not_saved,
                )
            invocation.attempt = attempt
            return

    def _failure_is_routable(self, node: Any, invocation: Invocation) -> bool:
        """Whether an exhausted node failure is handled by topology instead of
        parking the run (Node Result System).

        Precedence: a FANNED invocation under ``on_item_failure='hole'``
        becomes an explicit failed item in the aggregated dispatch (§4.4) —
        the hole IS the handling, ERROR edges prune. Otherwise (fanned or
        not) ≥1 outgoing ERROR edge routes the failure (try/catch topology;
        every Send-driven invocation — loop bodies, map items — carries a
        dispatch_id, so ERROR edges MUST work for them too: a loop body's
        ERROR back-edge is the retry-topology case). No hole, no ERROR edge
        → park, today's behavior.
        """
        if invocation.dispatch_id and node.on_item_failure == "hole":
            return True
        # A fail-soft step (data.optional): the failure is recorded on the step, its normal
        # edges prune like a branch not taken, and the run goes on (2026-10-14).
        if getattr(node, "optional", False):
            return True
        return any(self.graph.edges[eid].kind is EdgeKind.ERROR for eid in node.outgoing_edge_ids)

    def _escalate_all_failed_fan_outs(self, results: list[_StepResult]) -> None:
        """Turn an optional fan-out whose EVERY item failed into a parking error (2026-10-22).

        ``data.optional`` routes a failed fanned item so the run goes on — right when SOME
        items fail. When every item failed, the stage did nothing: each item's normal edges
        prune, the collector and everything after it prune, and the run used to end
        ``completed`` with no error (live: Brand discovery run 87452569, 16/16 curate calls
        failed).

        Judged PER TARGET NODE across every dispatch of it in this step (nested maps: one
        all-failed inner group beside successful siblings is a partial failure, review F2),
        counting items of the same dispatch that settled in an EARLIER step from the
        accumulator (items split by a human-input gate and a resume, F4). Escalates only when
        every dispatch is complete and not one item of any of them succeeded (or is still
        interrupted). Never escalated — something reaches the steps after it, or another
        mechanism owns the failure:
          * ``on_item_failure='hole'`` — gather receives the holes (F1);
          * an ERROR connection out of the step — author-handled;
          * ``work_item_id`` invocations — ``control.work_queue`` counts failed / dead-letter
            items in its own tally, and its items are settled before routing (F3);
          * a ``control.loop`` body after its first iteration — an earlier iteration already
            delivered (F3).
        Each failed item's result becomes the same ``FanOutAllItemsFailedError``, so the
        ordinary park path errors the run on that step and a retry re-runs the items.
        """
        by_target: dict[str, list[_StepResult]] = {}
        for r in results:
            inv = r.invocation
            if inv.dispatch_id and not inv.work_item_id:
                by_target.setdefault(inv.node_id, []).append(r)
        for target, rs in by_target.items():
            node = self.graph.nodes[target]
            if not getattr(node, "optional", False) or node.on_item_failure == "hole":
                continue
            if any(self.graph.edges[eid].kind is EdgeKind.ERROR for eid in node.outgoing_edge_ids):
                continue
            if any(r.failure is None for r in rs):
                continue  # an item succeeded, was skipped, or is still interrupted
            if any(self._later_loop_iteration(r.invocation) for r in rs):
                continue
            by_dispatch: dict[str, set[int]] = {}
            for r in rs:
                by_dispatch.setdefault(r.invocation.dispatch_id, set()).add(r.invocation.item_index)
            earlier_errors: list[object] = []
            complete = True
            for dispatch_id, indexes in by_dispatch.items():
                expected = self._dispatch_expected.get((dispatch_id, target))
                earlier_failed, earlier_ok = self._earlier_item_outcomes(target, dispatch_id)
                if earlier_ok - indexes:
                    complete = False  # an item of this dispatch already delivered
                    break
                settled = indexes | set(earlier_failed)
                if not expected or len(settled) < expected:
                    complete = False  # never guessed: the group is not all in
                    break
                earlier_errors.extend(
                    err for idx, err in sorted(earlier_failed.items()) if idx not in indexes
                )
            if not complete:
                continue
            err = FanOutAllItemsFailedError(
                node_id=target,
                label=self._step_label(target),
                errors=[*earlier_errors, *(r.failure for r in rs)],
            )
            logger.warning(
                "[wf step] fan-out to '%s' (%d dispatch(es)): all %d item(s) failed — "
                "parking the run ERRORED",
                target,
                len(by_dispatch),
                len(rs) + len(earlier_errors),
            )
            for r in rs:
                r.error = err
                r.failure = None

    def _later_loop_iteration(self, invocation: Invocation) -> bool:
        """True for a ``control.loop`` body invocation past the loop's first iteration."""
        if not invocation.loop_stack:
            return False
        frame = invocation.loop_stack[-1]
        origin = self.graph.nodes.get(str(frame.get("origin_node_id") or ""))
        if origin is None or origin.spec_type != "control.loop":
            return False
        if getattr(origin.config, "target_node_id", None) != invocation.node_id:
            return False
        iteration = frame.get("iteration")
        return isinstance(iteration, int) and not isinstance(iteration, bool) and iteration > 1

    def _earlier_item_outcomes(
        self, target: str, dispatch_id: str
    ) -> tuple[dict[int, object], set[int]]:
        """Items of ``dispatch_id`` that ``target`` already settled in an earlier step, read
        from the accumulator its outgoing edges feed: ``(failed index -> error, ok indexes)``.
        A failed optional item is recorded pruned with ``item_status='failed'``; any delivery
        is an item that reached the next step."""
        failed: dict[int, object] = {}
        ok: set[int] = set()
        for eid in self.graph.nodes[target].outgoing_edge_ids:
            entry = self._pending_bindings.get(self.graph.edges[eid].target_node_id)
            if entry is None:
                continue
            for b in entry.edges.values():
                if b.dispatch_id != dispatch_id or b.source_node_id != target:
                    continue
                if b.state == "delivered":
                    ok.add(b.item_index)
                elif b.item_status == "failed":
                    failed.setdefault(b.item_index, b.error or {"code": "error", "message": "failed"})
        for idx in ok:
            failed.pop(idx, None)
        return failed, ok

    async def _run_sample_preflight(
        self,
        executor: Any,
        node: Any,
        spec: Any,
        invocation: Invocation,
        run_id: str,
        thread_id: str,
        step: int,
        channel_snapshot: dict[str, Any],
        step_app_ctx: AppContext,
    ) -> Any:
        """A sampled step's pre-send checks: its inputs resolved as the live leg resolves them
        (static + routed + declared defaults, run inputs, held values, the ingestion gate, the
        input schema), then ``executor.sample_preflight(ctx, inputs, config)``. Reads only; what
        it returns is recorded on the sampled outcome as ``metadata.preflight``."""
        from matrx_graph.checkpoint.value_store import held_hash, resolve_step_inputs
        from matrx_graph.content_ir.markers import reduce_for_ingestion

        ctx = NodeExecutionContext(
            app=step_app_ctx,
            run_id=run_id,
            thread_id=thread_id,
            node_id=invocation.node_id,
            step=step,
            attempt=invocation.attempt,
            channels=ChannelView(_values=dict(channel_snapshot), _pending_writes=[]),
            checkpointer=self.checkpointer,
            dispatch_id=invocation.dispatch_id,
            item_index=invocation.item_index,
            firing=invocation.firing,
            registry=self.registry,
            output_kind=node.output_kind,
            workflow_id=self.definition_id or None,
        )
        merged = resolve_invocation_inputs(
            node,
            self._with_declared_defaults(invocation.node_id, spec, invocation.inputs),
            run_variables=self._run_variables,
            declared_variables=self.graph.variables,
            run_inputs=self._run_inputs,
            input_surface=self.graph.input_surface,
            run_facts=ctx.run_facts,
        )
        held = {k: v for k, v in merged.items() if held_hash(v)}
        if held:
            merged = {**merged, **(await resolve_step_inputs(run_id, held))}
        merged = reduce_for_ingestion(merged, _input_schema_json(spec.input_schema))
        inputs_model = spec.input_schema.model_validate(merged)
        return await executor.sample_preflight(ctx, inputs_model, node.config)

    async def _fail_attempt(
        self,
        *,
        run_id: str,
        step: int,
        invocation: Invocation,
        node: Any,
        spec: Any,
        policy: Any,
        attempt: int,
        elapsed_ms: int,
        err_type: str,
        node_error: NodeError,
        result: _StepResult,
        node_span: Any,
        invocation_count: int,
        exc: Exception | None,
    ) -> str:
        """One failed attempt through the unified ladder — raised exceptions
        and returned Failure envelopes share this path exactly.

        Returns ``"retry"`` (caller bumps attempt and loops) or ``"handled"``
        (the failure routes — ``result.failure`` is set for _route_outputs).
        Raises (the original exception, or NodeFailureError for a returned
        Failure) when the failure must PARK the run — unchanged behavior.

        The persisted error dict is the SUPERSET shape
        ``{type, message, code, details}`` PLUS the structured failure fields
        (``cause``/``step_id``/``step_label``/``field``/``expected``/``got``/
        ``technical``): ``type`` keeps every existing consumer (agent_plans,
        checkpoint preview, replay walk-forward) working; ``code``/``details``
        carry the structured NodeError; the failure fields let a step-level
        surface explain itself from data instead of regexing the message.
        Strictly additive — nothing was removed.
        """
        # The structured half. Derived from the exception when there is one
        # (a pydantic ValidationError names the field and the expectation
        # outright); otherwise from the NodeError's already-stable ``code``.
        # ``message`` is NOT overwritten — the node's own wording is better
        # than a generated sentence when the node bothered to write one.
        node_id = invocation.node_id
        if exc is not None:
            structured = self._failure_for(exc, node_id)
        elif (
            refusal := _refusal_failure(
                node_error,
                code=node_error.code,
                node_message=node_error.message,
                technical=f"{err_type}: {node_error.message}",
                step_id=node_id,
                step_label=self._step_label(node_id),
            )
        ) is not None:
            # A RETURNED caller refusal (``ai.mandate.start`` on a declined approval returns
            # ``ai_turn_failed`` + ``details.caller_refusal``) is classified by the refusal it
            # carries, never by its code: the hole a fan-out keeps reads ``spend_approval_required``,
            # not ``engine_error`` (live run 5c5db16c, 2026-10-27, 29 holes).
            structured = refusal
        elif (
            gated := gate_failure(
                node_error,
                technical=f"{err_type}: {node_error.message}",
                step_id=node_id,
                step_label=self._step_label(node_id),
            )
        ) is not None:
            # A returned code that IS a gate cause (a called workflow stopped by the usage limit,
            # ``subgraph.call``) is the step's cause, exactly as on the run (2026-10-27 review).
            structured = gated
        else:
            structured = build_failure(
                cause=cause_from_text(
                    f"{node_error.code} {node_error.message}", error_type=err_type
                ),
                technical=f"{err_type}: {node_error.message}",
                step_id=node_id,
                step_label=self._step_label(node_id),
                error_type=err_type,
                message=node_error.message,
            )
        # ERRORS ARE KINDS (plan §10d-B3). The structured half is merged ONTO
        # the NodeError rather than into a loose dict beside it, so the
        # persisted column, ``NodeFailedEvent.error``, and the ERROR-edge
        # payload are all the SAME self-describing ``node_error`` instance
        # instead of three dialects of one failure. Merge rule is unchanged:
        # message/type/code/details on the node plane are authoritative, and
        # a structured value only fills a field the node left empty.
        node_error = _merge_structured_failure(node_error, structured, err_type=err_type)
        error_dict: dict[str, Any] = node_error.to_column()

        # A CALLER REFUSAL IS FINAL (matrx_graph.spend_gate): a gate that said no before anything
        # was spent says no again on every retry — retrying it pays for nothing and re-files it.
        refused = is_caller_refusal(exc=exc, node_error=node_error)
        if (
            not refused
            and err_type not in _NON_RETRYABLE_ERROR_TYPES
            and should_retry(policy, attempt, err_type)
        ):
            # Record the retry-attempt outcome so a crash mid-backoff
            # survives resume: on the next boot, the loop walks past
            # this row instead of re-running this attempt.
            try:
                await self.checkpointer.record_outcome(
                    NodeOutcome(
                        run_id=run_id,
                        step=step,
                        node_id=invocation.node_id,
                        attempt=attempt,
                        dispatch_id=invocation.dispatch_id,
                        item_index=invocation.item_index,
                        output={},
                        error=error_dict,
                        duration_ms=elapsed_ms,
                        source="retry",
                    )
                )
            except Exception as outcome_err:  # noqa: BLE001
                record_exception(node_span, outcome_err)
                logger.warning(
                    "[wf:%s step=%d node=%s attempt=%d] retry outcome write failed: %s",
                    run_id[:8],
                    step,
                    invocation.node_id,
                    attempt,
                    outcome_err,
                )

            delay_ms = compute_backoff_ms(policy, attempt)
            await self._emit(
                NodeRetryScheduledEvent(
                    run_id=run_id,
                    step=step,
                    node_id=invocation.node_id,
                    spec_type=spec.node_type,
                    attempt=attempt,
                    dispatch_id=invocation.dispatch_id,
                    item_index=invocation.item_index,
                    invocation_count=invocation_count,
                    next_attempt=attempt + 1,
                    delay_ms=delay_ms,
                    error_type=err_type,
                    error_message=node_error.message,
                )
            )
            await self._raise_review(
                run_id,
                invocation,
                step=step,
                attempt=attempt,
                label="engine.retry",
                message=f"Attempt {attempt} failed and was retried: {node_error.message}"[:500],
                category="retry",
                payload={"error_type": err_type, "code": node_error.code, "next_attempt": attempt + 1},
            )
            if delay_ms > 0:
                await asyncio.sleep(delay_ms / 1000)
            return "retry"

        # Final failure (no retries left OR error not retryable).
        set_attributes(node_span, **{"workflow.node.outcome": "failed"})
        if exc is not None:
            record_exception(node_span, exc)
        try:
            await self.checkpointer.record_outcome(
                NodeOutcome(
                    run_id=run_id,
                    step=step,
                    node_id=invocation.node_id,
                    attempt=attempt,
                    dispatch_id=invocation.dispatch_id,
                    item_index=invocation.item_index,
                    output={},
                    error=error_dict,
                    duration_ms=elapsed_ms,
                )
            )
        except Exception as outcome_err:  # noqa: BLE001
            record_exception(node_span, outcome_err)
            logger.warning(
                "[wf:%s step=%d node=%s attempt=%d] FAILED outcome "
                "write failed — recovery may re-execute or "
                "mis-replay this node: %s",
                run_id[:8],
                step,
                invocation.node_id,
                attempt,
                outcome_err,
            )
        invocation.attempt = attempt
        # THE PACKET, FAILURE SIDE (plan §10d-B3). Same assembly and the same
        # loud fail-open posture as the completed path — a failure ships as a
        # ``node_outcome`` wrapper with the ``node_error`` kind nested, so a
        # consumer has ONE rendering path for both outcomes.
        failure_wrapper: dict[str, Any] | None = None
        try:
            from matrx_graph.content_ir.runtime_view import node_outcome_view

            failure_wrapper = node_outcome_view(
                run_id=run_id,
                node_id=invocation.node_id,
                workflow_id=self.definition_id or None,
                step=step,
                attempt=attempt,
                status="failed",
                duration_ms=elapsed_ms,
                error=node_error,
            )
        except Exception:  # noqa: BLE001 — never load-bearing
            logger.error(
                "[wf:%s step=%d node=%s] node_outcome wrapper assembly FAILED "
                "on the failure path — node_failed ships WITHOUT the runtime "
                "wrapper (consumers fall back to the flat error dict). This is "
                "a platform defect.",
                run_id[:8],
                step,
                invocation.node_id,
                exc_info=True,
            )
        await self._emit(
            NodeFailedEvent(
                run_id=run_id,
                step=step,
                node_id=invocation.node_id,
                spec_type=spec.node_type,
                attempt=attempt,
                dispatch_id=invocation.dispatch_id,
                item_index=invocation.item_index,
                invocation_count=invocation_count,
                error_type=err_type,
                error_message=node_error.message,
                error=error_dict,
                wrapper=failure_wrapper,
            )
        )
        # Cost settlement survives failure (Node Result System): a paid call
        # that failed carries its billed usage under NodeError.details.usage
        # (documented convention) — settle it exactly like the success path.
        # Unlike the success-path gate (category-restricted to avoid
        # double-counting a pass-through node forwarding an upstream
        # payload's usage block VERBATIM), a failure never forwards another
        # node's payload — NodeError.details is always this node's own
        # error, so the presence of usage here IS the signal money was
        # spent by THIS node. Settle on presence, regardless of category —
        # this also covers IO-category paid actions (e.g. page_extraction)
        # that fail after already billing (2026-07-09).
        if isinstance(node_error.details, dict) and isinstance(
            node_error.details.get("usage"), dict
        ):
            cost_event = node_cost_from_output(
                node_error.details,
                run_id=run_id,
                step=step,
                node_id=invocation.node_id,
                spec_type=spec.node_type,
                attempt=attempt,
                dispatch_id=invocation.dispatch_id,
                item_index=invocation.item_index,
            )
            if cost_event is not None:
                await self._emit(cost_event)
                self._note_cost_emitted(invocation, cost_event)

        if self._failure_is_routable(node, invocation):
            result.failure = node_error
            await self._flag_handled_failure(
                run_id, invocation, node, step=step, attempt=attempt, node_error=node_error,
                err_type=err_type,
            )
            return "handled"
        if exc is not None:
            raise exc
        raise NodeFailureError(invocation.node_id, node_error)

    async def _scream_deprecated_step(
        self,
        run_id: str,
        invocation: Invocation,
        spec: Any,
        *,
        step: int,
        attempt: int,
    ) -> None:
        """A deprecated step is running: log WARNING (every attempt), one review flag per
        run per step, one ``system_error`` per (step type, workflow) per process. Never raises."""
        try:
            from matrx_graph.deprecations import (
                DEPRECATED_STEP_ERROR_KIND,
                DEPRECATED_STEP_FLAG_LABEL,
                deprecation_for,
                deprecation_message,
            )

            dep = deprecation_for(spec.node_type)
            if dep is None:
                return
            workflow_id = self.definition_id or ""
            message = deprecation_message(
                dep,
                display_name=spec.display_name,
                node_id=invocation.node_id,
                workflow_name=str(self.graph.source_metadata.get("name") or ""),
                workflow_id=workflow_id,
            )
            logger.warning("[wf:%s] %s", run_id[:8], message)
            await self._review.raise_flag(
                run_id,
                ReviewFlag(
                    node_id=invocation.node_id,
                    step=0,
                    attempt=0,
                    label=DEPRECATED_STEP_FLAG_LABEL,
                    message=message,
                    category="other",
                    source="engine",
                    payload={"step_type": dep.step_type, "replacement": dep.replacement},
                    # Once per run per step: no step/attempt/item in the key.
                    occurrence_key=f"{DEPRECATED_STEP_FLAG_LABEL}|{invocation.node_id}",
                ),
            )
            signature = (dep.step_type, workflow_id)
            if signature in _DEPRECATION_CAPTURED:
                return
            from matrx_utils import capture_error

            await capture_error(
                RuntimeError(message),
                kind=DEPRECATED_STEP_ERROR_KIND,
                error_type=DEPRECATED_STEP_ERROR_KIND,
                error_text=message,
                organization_id=self._review.organization_id,
                context={
                    "step_type": dep.step_type,
                    "workflow_id": workflow_id,
                    "node_id": invocation.node_id,
                    "run_id": run_id,
                    "replacement": dep.replacement,
                },
            )
            # Marked only once the error row landed, so a failed capture is retried next time.
            _DEPRECATION_CAPTURED.add(signature)
        except Exception:  # noqa: BLE001 — a scream never fails the run
            logger.exception("[wf:%s] deprecated-step scream failed", run_id[:8])

    async def _raise_review(
        self,
        run_id: str,
        invocation: Invocation,
        *,
        step: int,
        attempt: int,
        label: str,
        message: str,
        category: str,
        source: str = "engine",
        payload: dict[str, Any] | None = None,
    ) -> None:
        """Raise one review flag for this invocation's attempt. Never raises."""
        await self._review.raise_flag(
            run_id,
            ReviewFlag(
                node_id=invocation.node_id,
                step=step,
                attempt=attempt,
                label=label,
                message=message,
                category=category,
                source=source,
                payload=payload,
                occurrence_key=occurrence_key(
                    node_id=invocation.node_id,
                    step=step,
                    attempt=attempt,
                    dispatch_id=invocation.dispatch_id,
                    item_index=invocation.item_index,
                    firing=invocation.firing,
                    label=label,
                ),
            ),
        )

    async def _flag_handled_failure(
        self,
        run_id: str,
        invocation: Invocation,
        node: Any,
        *,
        step: int,
        attempt: int,
        node_error: NodeError,
        err_type: str,
    ) -> None:
        """A failure the topology handled and the run survives — which one, by the same
        precedence routing applies: a fan-out hole, then an ERROR connection, then optional."""
        payload = {"error_type": err_type, "code": node_error.code}
        if invocation.dispatch_id and node.on_item_failure == "hole":
            label, category = "engine.item_skipped", "skipped_item"
            message = f"Item {invocation.item_index} failed and was skipped: {node_error.message}"
            details = node_error.details if isinstance(node_error.details, dict) else {}
            if details.get("caller_refusal") is True:
                # A refused item is final (never retried or re-asked): the flag says so and names
                # where a person acts on it, so the hole is never a dead end.
                approval_url = details.get("approval_url")
                payload.update(
                    cause=node_error.cause,
                    approval_id=details.get("approval_id"),
                    approval_url=approval_url,
                )
                message = (
                    f"Item {invocation.item_index} was refused and skipped: {node_error.message}"
                    + (f" Approve it here: {approval_url}" if approval_url else "")
                )
        elif any(self.graph.edges[eid].kind is EdgeKind.ERROR for eid in node.outgoing_edge_ids):
            self._failed_steps.setdefault(
                invocation.node_id,
                {"message": node_error.message, "cause": str(getattr(node_error, "cause", "") or "")},
            )
            label, category = "engine.caught_failure", "recovered_error"
            self._caught_failures.setdefault(
                invocation.node_id, {"code": node_error.code, "message": node_error.message}
            )
            message = f"Failed and was handled by its error path: {node_error.message}"
        elif getattr(node, "optional", False):
            self._failed_steps.setdefault(
                invocation.node_id,
                {"message": node_error.message, "cause": str(getattr(node_error, "cause", "") or "")},
            )
            label, category = "engine.optional_step_failed", "recovered_error"
            message = f"Optional step failed; the run went on without it: {node_error.message}"
        else:
            return
        await self._raise_review(
            run_id, invocation, step=step, attempt=attempt, label=label,
            message=message[:500], category=category, payload=payload,
        )

    def _queue_edge_taken(
        self,
        edge: Any,
        *,
        source_id: str,
        step: int,
        dispatch_id: str = "",
        item_index: int = 0,
    ) -> None:
        """A connection carrying ``data.review`` was TAKEN (payload delivered): queue its flag,
        flushed after this canonical routing pass. A run-ahead (partial) pass never queues —
        the barrier's routing is the one that counts."""
        mark = getattr(edge, "review", None)
        if mark is None or self._partial_routing:
            return
        label = mark.label or f"flagged_path.{edge.edge_id}"
        self._review.queue(
            ReviewFlag(
                node_id=edge.target_node_id,
                step=step,
                attempt=1,
                label=label,
                message=mark.reason,
                category=mark.category,
                source="flagged_path",
                edge_id=edge.edge_id,
                payload={"from_step": source_id},
                occurrence_key=occurrence_key(
                    node_id=edge.target_node_id,
                    step=step,
                    attempt=1,
                    dispatch_id=f"{source_id}#{dispatch_id}",
                    item_index=item_index,
                    edge_id=edge.edge_id,
                    label=label,
                ),
            )
        )

    def _step_label(self, node_id: str | None) -> str | None:
        """The AUTHOR's name for a node, or None.

        Never falls back to the node_id: a failure that says "n-l4fuKvk13v
        needs a topic" names nothing the reader recognizes. The client decides
        what to say when there is no label.
        """
        if not node_id:
            return None
        node = self.graph.nodes.get(node_id)
        label = getattr(node, "label", None) if node is not None else None
        return label if isinstance(label, str) and label.strip() else None

    def _failure_for(self, err: BaseException, node_id: str | None) -> RunFailure:
        """Derive the structured failure with this run's step identity attached."""
        return failure_from_exception(err, step_id=node_id, step_label=self._step_label(node_id))

    async def _park_errored(
        self,
        *,
        run_id: str,
        thread_id: str,
        step: int,
        start_step: int,
        parent_checkpoint_id: str | None,
        pending: list[Invocation],
        pre_step_snapshot: dict[str, Any],
        last_outputs: dict[str, Any],
        node_id: str,
        attempt: int,
        err: Exception,
    ) -> RunResult:
        """Park the run as ERRORED at this step's boundary — the recoverable path.

        Shared by all three failure classes: node-executor exceptions,
        channel-reducer failures on commit, and edge-routing failures
        (conditional predicate / mapping miss). The checkpoint stores the
        PRE-step channel snapshot with the full pending list, so resume
        re-runs the whole step — successful siblings replay from cached
        outcomes, the recovered node re-executes (or uses the user-supplied
        skip/manual output) — and channel reducer math stays correct.
        """
        cp_id = await self._save_checkpoint(
            run_id=run_id,
            thread_id=thread_id,
            step=step,
            parent_checkpoint_id=parent_checkpoint_id,
            next_invocations=_as_next_invocations(pending, step),
            channel_values_override=pre_step_snapshot,
        )
        await self._emit(
            RunErroredEvent(
                run_id=run_id,
                steps_executed=step - start_step,
                node_id=node_id,
                step=step,
                attempt=attempt,
                error_type=type(err).__name__,
                error_message=str(err),
                checkpoint_id=cp_id,
            )
        )
        return RunResult(
            run_id=run_id,
            thread_id=thread_id,
            status=RunStatus.ERRORED,
            steps_executed=step - start_step,
            channel_values=pre_step_snapshot,
            last_outputs=last_outputs,
            error=f"{type(err).__name__}: {client_error_text(str(err))}",
            failure=self._failure_for(err, node_id),
        )

    def _merge_frontier(
        self, routed: list[Invocation], deferred: list[Invocation]
    ) -> list[Invocation]:
        """Fold step-mode deferred siblings into the routed next-frontier.

        Keyed by the FULL correlation ``(node_id, dispatch_id, item_index)``
        (§4.1 — a plain node_id key would collapse fanned siblings into one
        invocation). A key collision is legitimate ONLY when the two
        invocations carry IDENTICAL inputs — the idempotent re-route case
        (an errored-park resume re-delivers the same payloads to a node
        already on the parked frontier); they collapse to one invocation
        with ``attempt`` = max. Two DISTINCT firings of one node (edge-driven
        multi-fire, e.g. join_policy='any' firing again while an earlier
        firing sits deferred) colliding on one correlation key is an
        EdgeRoutingError park (F4 / §3.1, §3.7): merging them was silent
        last-writer-wins data loss, and running both in one super-step would
        collide on the outcome idempotency key. Recovery: resume without
        node selection — the full parked frontier runs the firings on
        separate steps. A deferred invocation absent from the routed set is
        carried through untouched. Routed order is preserved, then
        deferred-only invocations are appended.
        """
        by_id: dict[tuple[str, str, int], Invocation] = {}
        for inv in deferred:
            by_id[(inv.node_id, inv.dispatch_id, inv.item_index)] = Invocation(
                node_id=inv.node_id,
                inputs=dict(inv.inputs),
                attempt=inv.attempt,
                dispatch_id=inv.dispatch_id,
                item_index=inv.item_index,
                config_override=inv.config_override,
                blocked_join=inv.blocked_join,
                firing=inv.firing,
                loop_stack=[dict(f) for f in inv.loop_stack],
                work_item_id=inv.work_item_id,
                # A resumed entry keeps the step it is keyed at (an answered
                # interrupt's recorded value lives there).
                step=inv.step,
                bypass_once=inv.bypass_once,
            )
        for inv in routed:
            key = (inv.node_id, inv.dispatch_id, inv.item_index)
            existing = by_id.get(key)
            if existing is None:
                by_id[key] = inv
            elif existing.inputs == inv.inputs:
                by_id[key] = Invocation(
                    node_id=inv.node_id,
                    inputs=dict(inv.inputs),
                    attempt=max(existing.attempt, inv.attempt),
                    dispatch_id=inv.dispatch_id,
                    item_index=inv.item_index,
                    config_override=inv.config_override or existing.config_override,
                    firing=max(existing.firing, inv.firing),
                    loop_stack=[dict(f) for f in (inv.loop_stack or existing.loop_stack)],
                    work_item_id=inv.work_item_id or existing.work_item_id,
                    step=existing.step,
                    bypass_once=inv.bypass_once or existing.bypass_once,
                )
            else:
                raise EdgeRoutingError(
                    f"step-mode cannot merge two DISTINCT firings of node "
                    f"'{inv.node_id}' (correlation dispatch_id="
                    f"{inv.dispatch_id!r}, item_index={inv.item_index}): a "
                    f"deferred invocation holds inputs "
                    f"{sorted(existing.inputs)} while this step's routing "
                    f"fired it again with inputs {sorted(inv.inputs)}. "
                    f"Collapsing them would silently drop one firing's "
                    f"payload (ENGINE_SPEC §3.1/§3.7). Resume WITHOUT node "
                    f"selection so the firings run on separate steps.",
                    node_id=inv.node_id,
                    edge_id="",
                )

        ordered: list[Invocation] = []
        seen: set[tuple[str, str, int]] = set()
        for inv in routed:
            key = (inv.node_id, inv.dispatch_id, inv.item_index)
            if key not in seen:
                ordered.append(by_id[key])
                seen.add(key)
        for inv in deferred:
            key = (inv.node_id, inv.dispatch_id, inv.item_index)
            if key not in seen:
                ordered.append(by_id[key])
                seen.add(key)
        return ordered

    # Edge kinds that participate in join readiness (ENGINE_SPEC §3.2):
    # DATA and CONDITIONAL bind payload; CONTROL counts toward the join but
    # binds NO payload (audit U5). ERROR (Node Result System) joins too:
    # on source SUCCESS it resolves PRUNED (the handler branch dies via
    # §3.3 transitive prune); on a routable source FAILURE it DELIVERS the
    # structured NodeError dump while every normal edge prunes. STREAM
    # never join-counts (unimplemented).
    # ONE definition, shared with the resume pre-flight.
    _JOINABLE_KINDS = JOINABLE_KINDS

    async def _settle_work_items(self, run_id: str, results: list[_StepResult]) -> None:
        """Settle claimed work items for invocations that FINISHED this step.

        The engine half of matrx_graph.workset: an invocation carrying a
        ``work_item_id`` (dispatched by ``control.work_queue``) settles its
        item ``succeeded`` on success / user-skip / mock, ``failed`` on a
        routable failure or park-bound error. An interrupted invocation is
        NOT finished — its item stays leased and settles when it completes
        after resume. Settlement is best-effort: a store hiccup is logged
        loudly and the lease-reclaim path recovers the item; it must never
        kill the run.
        """
        relevant = [r for r in results if r.invocation.work_item_id]
        if not relevant:
            return
        from matrx_graph.workset import get_work_set_store

        store = get_work_set_store()
        for r in relevant:
            if r.interrupt is not None:
                continue
            try:
                if r.failure is not None:
                    await store.fail(
                        r.invocation.work_item_id,
                        run_id=run_id,
                        error=r.failure.model_dump(mode="json"),
                    )
                elif r.error is not None:
                    await store.fail(
                        r.invocation.work_item_id,
                        run_id=run_id,
                        error={"code": type(r.error).__name__, "message": str(r.error)},
                    )
                else:
                    await store.complete(r.invocation.work_item_id, run_id=run_id)
            except Exception:  # noqa: BLE001 — reclaim covers; never kill the run
                logger.warning(
                    "[wf:%s node=%s] work-item settle failed (item=%s) — "
                    "lease reclaim will recover it",
                    run_id[:8],
                    r.invocation.node_id,
                    r.invocation.work_item_id,
                    exc_info=True,
                )

    def _route_outputs(self, results: list[_StepResult], step: int) -> list[Invocation]:
        """Translate this step's outputs + emissions + Sends into next-step invocations.

        Edge-routed deliveries ALWAYS pass through the binding accumulator
        (ENGINE_SPEC §3.6) — each completed source resolves every joinable
        outgoing edge as delivered (buffered mapped fragment) or pruned; a
        target becomes Ready only when its required inbound-edge set is
        fully resolved per its join_policy (§3.1–§3.3). Single-input nodes
        complete their required set immediately, so behavior is identical
        to the pre-join engine with one bookkeeping hop.

        Sends are distinct invocations that BYPASS the accumulator — each
        Send produces its own Invocation, even multiple Sends to the same
        target (dynamic fanout).
        """
        # Insertion-ordered (dict-as-ordered-set): join firings must be
        # deterministic across runs/replays, so drain order follows
        # delivery order, never set-hash order.
        touched: dict[str, None] = {}
        # Back-edge firings (F13) collected by _resolve_source_edges during
        # this pass — reset here so a parked pass's leftovers never leak.
        self._back_edge_fires = []
        if not self._partial_routing:
            self._failure_blocked = []
        self._edge_fanout_sends = []
        self._edge_fanout_loop_stacks = {}

        for r in results:
            if r.failure is not None:
                # Node Result System: a routable node failure — deliver the
                # structured NodeError over ERROR edges (or record an explicit
                # fan-out hole under on_item_failure='hole'); every normal
                # outgoing edge prunes.
                failed_node = self.graph.nodes[r.invocation.node_id]
                self._resolve_failure_edges(
                    source_id=r.invocation.node_id,
                    node_error=r.failure,
                    step=step,
                    touched=touched,
                    source_dispatch_id=r.invocation.dispatch_id,
                    source_item_index=r.invocation.item_index,
                    as_hole=(
                        bool(r.invocation.dispatch_id) and failed_node.on_item_failure == "hole"
                    ),
                    source_loop_stack=r.invocation.loop_stack,
                )
                continue
            if r.output is None:
                continue
            # run_id for the dump-context label comes from the result's own
            # invocation scope (this method has no run_id parameter; an
            # in-flight refactor referenced a bare `run_id` here — NameError
            # on every routed output).
            run_label = f"[wf:{r.invocation.node_id}] broadcast"
            # Round-1 F2: the settled (stamped, verdicted) dump IS the wire
            # value; re-dumping the model would strip the stamp at hop 1.
            broadcast_payload = (
                r.settled_dump
                if r.settled_dump is not None
                else model_dump_json(r.output, context=run_label)
            )
            # Kind subscriptions (§7.7c): every completed output is offered to
            # the matcher BEFORE edges route, so a trigger sees a kind no edge
            # was ever wired to carry. Deduped by occurrence identity, so a
            # value passed along step after step fires exactly once.
            if not self._partial_routing:
                self._subscriptions.observe(
                    broadcast_payload,
                    source_node_id=r.invocation.node_id,
                    step=step,
                    scope=(
                        f"{r.invocation.node_id}#{r.invocation.dispatch_id}:{r.invocation.item_index}"
                        if r.invocation.dispatch_id
                        else r.invocation.node_id
                    ),
                )
            self._resolve_source_edges(
                source_id=r.invocation.node_id,
                broadcast_payload=broadcast_payload,
                emissions=r.emissions,
                user_skipped=r.user_skipped,
                step=step,
                touched=touched,
                source_dispatch_id=r.invocation.dispatch_id,
                source_item_index=r.invocation.item_index,
                source_loop_stack=r.invocation.loop_stack,
                source_reused=r.reused,
            )

        # Register this pass's dispatches BEFORE draining joins: same-step
        # deliveries from an earlier wave's items may complete a fan-in group
        # whose expected count comes from these counts. Overwrite (never
        # increment) — a replayed dispatcher re-drains identical Sends, so
        # registration is idempotent (ENGINE_SPEC §4.4).
        pass_counts: dict[tuple[str, str], int] = {}
        for r in results:
            for send in r.sends:
                if send.dispatch_id:
                    key = (send.dispatch_id, send.target_node_id)
                    pass_counts[key] = pass_counts.get(key, 0) + 1
        # Edge fan-out (§7.4) mints Sends during routing, not from an
        # executor — they need the same registration or a downstream fan-in
        # group would never learn how many items to expect.
        for _source_id, send in self._edge_fanout_sends:
            if send.dispatch_id:
                key = (send.dispatch_id, send.target_node_id)
                pass_counts[key] = pass_counts.get(key, 0) + 1
        self._dispatch_expected.update(pass_counts)

        # §4.4a EMPTY DISPATCH (2026-08-29): a ``control.map`` that fired
        # successfully with ZERO items emits no Sends, so its configured
        # target — a Send-only node — can never activate: the target's
        # fan-in edges never resolve and the run used to end in a join
        # deadlock ("frontier empty but N node(s) still hold partial
        # inbound bindings"). An explicitly empty fan-out is a DEAD branch,
        # and it resolves like one: the target's outgoing edges prune
        # transitively (§3.3), so a downstream gather prunes and any join
        # that also holds a real delivery still fires ('all' fires on
        # resolved-with-≥1-delivery). Scoped deliberately:
        #   * ``control.map`` only — ``control.work_queue`` legitimately
        #     claims zero items in a wave while work is still in flight,
        #     and ``control.loop``/``control.send`` own their completion
        #     semantics; widening needs its own proof.
        #   * only when NO dispatch anywhere in this run has ever targeted
        #     the node (``_dispatch_expected``) — a sibling dispatcher's
        #     in-flight items are never disturbed.
        # An author who wants to REACT to emptiness branches on the map's
        # own output (``dispatched == 0``) — this rule only keeps an empty
        # list from strangling the run.
        #
        # A PARTIAL routing (run-ahead) never applies it: "no dispatch has
        # targeted the node" is only true once the full step is routed — a
        # sibling still running, or one that finished with Sends (never routed
        # ahead), registers its dispatch at the barrier. Pruning here launched
        # a join without the gather's values, then again with them.
        for r in [] if self._partial_routing else results:
            if r.error is not None or r.interrupt is not None:
                continue
            fired_node = self.graph.nodes.get(r.invocation.node_id)
            if fired_node is None or fired_node.spec_type != "control.map":
                continue
            empty_target = getattr(fired_node.config, "target_node_id", None)
            if not empty_target or empty_target not in self.graph.nodes:
                continue
            if any(s.target_node_id == empty_target for s in r.sends):
                continue
            if any(t == empty_target for (_d, t) in self._dispatch_expected):
                continue
            logger.info(
                "[wf step=%d] control.map '%s' dispatched 0 items — "
                "resolving target '%s' subtree as a pruned (empty) branch",
                step,
                r.invocation.node_id,
                empty_target,
            )
            self._resolve_source_edges(
                source_id=empty_target,
                broadcast_payload={},
                emissions={},
                user_skipped=False,
                step=step,
                touched=touched,
                pruned_firing=True,
                source_loop_stack=r.invocation.loop_stack,
                empty_dispatch=True,
            )

        next_invs = self._drain_completed_joins(touched, step)

        # Process Sends — dynamic fanout. Each Send is its own invocation
        # carrying its correlation identity (ENGINE_SPEC §4.1); attempt
        # ALWAYS starts at 1 — the old per-target attempt bump made sibling
        # items share the retry keyspace and replay each other's outcomes
        # (audit E2). Loop state (§9): the child inherits the dispatcher's
        # loop_stack; a control.loop dispatch additionally pushes its frame
        # (engine-carried iteration — replay re-drains identical Sends, so
        # the frame is deterministic across crash/park replays).
        for r in results:
            for send in r.sends:
                # An unknown Send target used to surface as a bare KeyError
                # deep in _execute_invocation — crash-shaped, unattributed.
                # Fail HERE with the dispatching node named, as a framework
                # ExecutionError (terminal FAILED with partial outputs
                # preserved, like max_steps).
                if send.target_node_id not in self.graph.nodes:
                    raise ExecutionError(
                        f"Node '{r.invocation.node_id}' dispatched work to "
                        f"'{send.target_node_id}', which is not a step on "
                        "this workflow. Check the dispatcher's target "
                        "(config.target_node_id or ctx.send) against the "
                        "canvas node ids."
                    )
                # THE LAUNCH DECLARATION is enforced where Sends are applied:
                # the resume pre-flight's model of "who can launch what" must
                # not go stale (executor/resume_preflight.py).
                if not launch_is_declared(
                    self.graph, self.registry, r.invocation.node_id, send.target_node_id
                ):
                    record_undeclared_launch(
                        self.graph.nodes[r.invocation.node_id].spec_type
                        if r.invocation.node_id in self.graph.nodes
                        else "?",
                        r.invocation.node_id,
                        send.target_node_id,
                    )
                next_invs.append(
                    Invocation(
                        node_id=send.target_node_id,
                        inputs=dict(send.payload),
                        attempt=1,
                        dispatch_id=send.dispatch_id,
                        item_index=send.item_index,
                        loop_stack=self._send_loop_stack(r, send),
                        work_item_id=send.work_item_id,
                    )
                )

        # Back-edge firings (F13): each delivery over a cycle back-edge
        # opens a NEW firing of its target directly — Pregel-heritage
        # re-fire-per-delivery, outside the join accumulator.
        next_invs.extend(self._back_edge_fires)
        self._back_edge_fires = []

        # Kind-filtered edge fan-out (§7.4 ``each``): one invocation per
        # instance, over the same Send machinery control.map uses — the edge
        # was excluded from its target's required join set, so these ARE the
        # target's firings for this delivery.
        for _source_id, send in self._edge_fanout_sends:
            next_invs.append(
                Invocation(
                    node_id=send.target_node_id,
                    inputs=dict(send.payload),
                    attempt=1,
                    dispatch_id=send.dispatch_id,
                    item_index=send.item_index,
                    loop_stack=[
                        dict(f) for f in self._edge_fanout_loop_stacks.get(send.dispatch_id, [])
                    ],
                )
            )
        self._edge_fanout_sends = []
        self._edge_fanout_loop_stacks = {}

        # Kind-triggered nodes (§7.7c): drain every subscription whose
        # debounce window closed and open its firing. A triggered node is
        # wired to nothing, so this is the ONLY way it ever runs. Draining
        # mutates the matcher, which a partial routing never touches.
        if not self._partial_routing:
            next_invs.extend(self._trigger_invocations(step))

        return next_invs

    def _trigger_invocations(self, step: int) -> list[Invocation]:
        """Turn drained kind-subscription firings into node invocations.

        Only ``node_trigger`` firings become invocations here. A ``directive``
        firing (§7.5) is deliberately NOT handled: mutating the graph belongs
        behind the apply-policy cascade, in a consumer that can record what it
        changed and why, never inside the router. The matcher is shared; the
        meaning of a firing is not.
        """
        invocations: list[Invocation] = []
        by_subscription: dict[str, list[Any]] = {}
        for firing in self._subscriptions.drain(step):
            if firing.subscription.purpose != "node_trigger":
                continue
            by_subscription.setdefault(
                f"{firing.subscription.subscriber_id}::{firing.subscription.kind}", []
            ).append(firing)

        for key, firings in by_subscription.items():
            subscription = firings[0].subscription
            node = self.graph.nodes.get(subscription.subscriber_id)
            if node is None:
                continue
            # ``each`` produces SIBLING firings of one node in one super-step,
            # which is a fan-out — so it needs fan-out IDENTITY. Without it
            # every sibling shares (node_id, attempt=1, dispatch_id='',
            # item_index=0), collide in the engine's per-invocation keyspace,
            # and only the first one ever runs. The id is derived (never
            # uuid4) because trigger firings are recomputed during routing and
            # a replay must mint them identically. ``all`` is a single firing
            # and stays plain — no dispatch, no fan-in bookkeeping.
            fanned = len(firings) > 1
            dispatch_id = f"trigger:{key}:{step}" if fanned else ""
            if fanned:
                self._dispatch_expected[(dispatch_id, subscription.subscriber_id)] = len(firings)
            for index, firing in enumerate(firings):
                values = firing.values
                payload: Any = values[0] if subscription.mode == "each" else values
                invocations.append(
                    Invocation(
                        node_id=subscription.subscriber_id,
                        inputs={
                            node.trigger_item_key: payload,
                            # Provenance: a node wired to nothing must still be
                            # able to answer "where did this come from?", and
                            # its executor may legitimately need the accessor
                            # path (a persistence node recording where it saw
                            # the value).
                            "trigger_kind": subscription.kind,
                            "trigger_source_node_ids": list(firing.source_node_ids),
                            "trigger_paths": [o.path for o in firing.occurrences],
                        },
                        attempt=1,
                        dispatch_id=dispatch_id,
                        item_index=index if fanned else 0,
                    )
                )
        return invocations

    def _send_loop_stack(self, result: _StepResult, send: Send) -> list[dict[str, Any]]:
        """The loop_stack a Send-driven child invocation carries (§9).

        Inherit the dispatcher's stack; when the dispatcher is a
        ``control.loop``, push its frame ``{origin_node_id, iteration}`` —
        the iteration the loop stamped into its body Send payload (engine
        vocabulary: the loop node is platform-owned; the BODY never needs to
        echo). Fallback for a payload without the key: the loop invocation's
        own engine-injected iteration + 1.
        """
        stack = [dict(f) for f in result.invocation.loop_stack]
        node = self.graph.nodes[result.invocation.node_id]
        if node.spec_type == "control.loop":
            raw_iter = send.payload.get("iteration")
            if not isinstance(raw_iter, int) or isinstance(raw_iter, bool):
                base = result.invocation.inputs.get("iteration")
                raw_iter = (base if isinstance(base, int) and not isinstance(base, bool) else 0) + 1
            stack.append({"origin_node_id": result.invocation.node_id, "iteration": raw_iter})
        return stack

    def _resolve_source_edges(
        self,
        *,
        source_id: str,
        broadcast_payload: dict[str, Any],
        emissions: dict[str, Any],
        user_skipped: bool,
        step: int,
        touched: dict[str, None],
        pruned_firing: bool = False,
        source_dispatch_id: str = "",
        source_item_index: int = 0,
        source_loop_stack: list[dict[str, Any]] | None = None,
        empty_dispatch: bool = False,
        source_reused: bool = False,
        failed_upstream: str = "",
        absent_from: str = "",
    ) -> None:
        """Resolve every joinable outgoing edge of a completed (or pruned)
        source firing into its target's binding accumulator.

        Each edge lands as DELIVERED (with its mapped payload fragment) or
        PRUNED (skip_edge_ids, CONDITIONAL predicate false, handle not
        emitted, or the whole source firing pruned — ``pruned_firing=True``
        propagates a dead branch, §3.3). A user_skip source consults the
        TARGET's on_skipped_upstream policy per edge (§3.4).

        Fan-out correlation (§4.4): when the source invocation is fanned
        (``source_dispatch_id`` non-empty), every resolution — delivered,
        skipped-hole, or pruned — lands as a PER-ITEM entry keyed
        ``"<edge_id>@@<item_index>"``, so the fanned edge behaves as ONE
        logical upstream that resolves only when all items of the dispatch
        resolved. A pruned/skipped item must still be RECORDED (as a hole),
        never dropped — a silently absent item would deadlock the group.

        Loop state (§9): the source's ``source_loop_stack`` propagates onto
        every delivered binding (correlation inheritance). When an edge
        targets the TOP frame's ``origin_node_id`` — the loop return — the
        engine pops the frame, injects ``iteration`` into the delivered
        fragment, and (when the return edge has no explicit mappings) wraps
        the body output as ``{"accumulator": <full payload>}``. The body
        never needs to know it is in a loop.
        """
        source = self.graph.nodes[source_id]
        stack = [dict(f) for f in (source_loop_stack or [])]
        if pruned_firing and not source_dispatch_id and source.spec_type == "control.map":
            # A PRUNED map never fires, so it never Sends: its target is reached by nothing, and without this the
            # target's outgoing edges (its gather and everything after) stay unresolved for ever — a join downstream
            # deadlocks (aidream brand_foundation run ffcbb913, 2026-10-24). Resolve the target subtree as pruned,
            # exactly as a map that fired with 0 items does (_route_results). Not for a map that some other live
            # dispatcher also feeds: that target still has a firing coming.
            target = getattr(source.config, "target_node_id", None)
            if (
                target
                and target != source_id
                and target in self.graph.nodes
                and not any(t == target for (_d, t) in self._dispatch_expected)
            ):
                self._resolve_source_edges(
                    source_id=target,
                    broadcast_payload={},
                    emissions={},
                    user_skipped=False,
                    step=step,
                    touched=touched,
                    pruned_firing=True,
                    source_loop_stack=source_loop_stack,
                    failed_upstream=failed_upstream,
                    absent_from=absent_from,
                )
        for edge_id in source.outgoing_edge_ids:
            edge = self.graph.edges[edge_id]
            if edge.kind not in self._JOINABLE_KINDS:
                continue  # STREAM edges neither join-count nor route

            if edge.kind is EdgeKind.ERROR:
                # Source succeeded (or was pruned) — the error-handler branch
                # was not taken: PRUNE, so the handler's subtree resolves dead
                # (§3.3). Failure deliveries go through
                # _resolve_failure_edges, never here. An ERROR back-edge
                # simply does not re-fire.
                if not edge.is_back_edge:
                    self._record_edge_resolution(
                        edge,
                        PendingEdgeBinding(
                            state="pruned",
                            source_node_id=source_id,
                            source_step=step,
                            dispatch_id=source_dispatch_id,
                            item_index=source_item_index,
                        ),
                        touched,
                    )
                continue

            # §9 loop return: this edge delivers back to the innermost open
            # loop frame's origin.
            is_loop_return = bool(stack) and stack[-1].get("origin_node_id") == edge.target_node_id
            binding_stack = stack[:-1] if is_loop_return else stack

            if edge.is_back_edge:
                # Cycle back-edge (F13, §3.2): excluded from the target's
                # required set; a delivery opens a NEW firing directly.
                if not pruned_firing:
                    self._resolve_back_edge(
                        edge,
                        source_id=source_id,
                        broadcast_payload=broadcast_payload,
                        emissions=emissions,
                        source_loop_stack=stack,
                        step=step,
                        source_dispatch_id=source_dispatch_id,
                        source_item_index=source_item_index,
                        user_skipped=user_skipped,
                    )
                continue

            if pruned_firing:
                self._record_edge_resolution(
                    edge,
                    PendingEdgeBinding(
                        state="pruned",
                        source_node_id=source_id,
                        source_step=step,
                        dispatch_id=source_dispatch_id,
                        item_index=source_item_index,
                        empty_dispatch=empty_dispatch,
                        failed_upstream=failed_upstream,
                        absent_from=absent_from,
                    ),
                    touched,
                )
                continue

            # Phase 5.2 — pre-emptive edge skip. The caller flagged this
            # edge to NOT carry its source's output downstream ("what if
            # branch X didn't fire?"). Under join semantics that is a PRUNE
            # (ENGINE_SPEC §2): the edge leaves the target's required set
            # instead of blocking it forever.
            if edge_id in self._skip_edge_ids:
                self._record_edge_resolution(
                    edge,
                    PendingEdgeBinding(
                        state="pruned",
                        source_node_id=source_id,
                        source_step=step,
                        dispatch_id=source_dispatch_id,
                        item_index=source_item_index,
                    ),
                    touched,
                )
                continue

            # Phase 6.5 — conditional edge predicate. When the edge is
            # CONDITIONAL and carries a `condition` expression, evaluate
            # it against the source node's output (exposed as `inputs`
            # in the sandbox). The edge delivers only when the predicate is
            # truthy; false is a PRUNE. A predicate error fails closed
            # (edge doesn't deliver) AND surfaces as EdgeRoutingError — the
            # _drive loop catches it and PARKS the run as ERRORED attributed
            # to the source node (recoverable via skip/manual-result),
            # instead of the old terminal-FAILED death.
            if edge.kind is EdgeKind.CONDITIONAL and edge.condition:
                from matrx_graph.nodes._sandbox import bind_item, safe_eval

                try:
                    # bind_item refuses a bare-`inputs` condition over a
                    # wrapped scalar payload — the inert-predicate class (W58).
                    predicate_input = bind_item(
                        edge.condition,
                        self._only_when_view(source_id, broadcast_payload),
                        where=f"conditional edge '{edge_id}'",
                    )
                    passed = bool(safe_eval(edge.condition, predicate_input))
                except Exception as e:  # noqa: BLE001
                    raise EdgeRoutingError(
                        f"conditional edge '{edge_id}' predicate failed: {edge.condition!r}: {e}",
                        node_id=source_id,
                        edge_id=edge_id,
                    ) from e
                if not passed:
                    self._record_edge_resolution(
                        edge,
                        PendingEdgeBinding(
                            state="pruned",
                            source_node_id=source_id,
                            source_step=step,
                            dispatch_id=source_dispatch_id,
                            item_index=source_item_index,
                        ),
                        touched,
                    )
                    continue

            if edge.source_handle is not None and edge.source_handle not in emissions:
                # Handle-specific edge the node didn't emit on — the branch
                # was not taken: PRUNE (§2).
                self._record_binding(
                    edge.target_node_id,
                    edge_id,
                    PendingEdgeBinding(state="pruned", source_node_id=source_id, source_step=step),
                    touched,
                )
                continue

            # DELIVERED. CONTROL edges count toward the join but bind NO
            # payload (§3.2 — this makes the documented "no payload" promise
            # true, audit U5). A LOOP RETURN is a control transfer, not a
            # fan-in: the body Send's dispatch correlation is STRIPPED here
            # (§9) so the delivery merges as a plain edge payload — the §4.4
            # aggregated-dispatch wrap would bury the injected iteration
            # inside an {"items": [...]} list and re-open the E7 spin.
            # Kind routing (§7.3/§7.4). A CONTROL edge binds no payload, so
            # a kind filter on it is meaningless and is skipped rather than
            # silently pruning the control transfer.
            routing = EdgeKindRouting(
                kind_filter=edge.kind_filter, fan_out=edge.fan_out, item_key=edge.item_key
            )
            if routing.is_active and edge.kind is not EdgeKind.CONTROL:
                routed_payload: Any = (
                    emissions[edge.source_handle]
                    if edge.source_handle is not None
                    else broadcast_payload
                )
                handled = self._resolve_kind_routed_edge(
                    edge,
                    routing=routing,
                    payload=routed_payload,
                    source_id=source_id,
                    step=step,
                    touched=touched,
                    source_dispatch_id=source_dispatch_id,
                    source_item_index=source_item_index,
                    loop_stack=binding_stack,
                )
                if handled is None:
                    continue  # pruned (no instances) or fanned out via Sends
                # ``all`` mode: the selected instances ARE this edge's payload
                # (a dict keyed by ``item_key``), and flow through the normal
                # mapping path below so explicit ``mappings`` still apply.
                edge_payload_override: Any = handled
            else:
                edge_payload_override = None

            binding_dispatch_id = "" if is_loop_return else source_dispatch_id
            binding_item_index = 0 if is_loop_return else source_item_index
            item_status: str | None = "succeeded" if binding_dispatch_id else None
            if edge.kind is EdgeKind.CONTROL:
                fragment: dict[str, Any] = {}
            else:
                payload: Any = (
                    edge_payload_override
                    if edge_payload_override is not None
                    else emissions[edge.source_handle]
                    if edge.source_handle is not None
                    else broadcast_payload
                )
                target = self.graph.nodes[edge.target_node_id]
                if user_skipped and target.on_skipped_upstream == "block":
                    # §3.4 block: the edge stays Unsatisfied — the node stays
                    # Blocked until recovery provides real data. The entry is
                    # materialized (empty is fine) so Blocked is durable and
                    # the end-of-run deadlock guard can scream.
                    self._ensure_binding_entry(edge.target_node_id)
                    touched[edge.target_node_id] = None
                    continue
                if user_skipped and target.on_skipped_upstream == "default_value":
                    fragment = self._skip_default_fragment(edge, target, source_id)
                elif user_skipped and binding_dispatch_id:
                    # §4.4: a user-skipped fan-out item becomes an EXPLICIT
                    # hole in the aggregated delivery — never routed through
                    # edge mappings (a mapped key can't resolve against the
                    # empty skip output; that's not an authoring error here,
                    # it's the definition of a hole).
                    fragment = {}
                    item_status = "skipped"
                elif is_loop_return and edge.mappings is None:
                    # §9: a return edge with no explicit mappings wraps the
                    # body's WHOLE output as the accumulator (with mappings,
                    # the author binds `accumulator` explicitly).
                    fragment = {"accumulator": payload}
                else:
                    # propagate_empty (default) — deliver the (empty) payload
                    # as-is, exactly like a normal completion (§3.4).
                    fragment = self._map_edge_payload(
                        edge, payload, source_id, step=step, flag_misses=not user_skipped
                    )
                if is_loop_return and item_status != "skipped":
                    # §9: iteration is ENGINE truth — injected from the popped
                    # frame, never trusted from a body echo.
                    fragment["iteration"] = int(stack[-1]["iteration"])

            self._record_edge_resolution(
                edge,
                PendingEdgeBinding(
                    state="delivered",
                    payload=fragment,
                    source_node_id=source_id,
                    source_step=step,
                    dispatch_id=binding_dispatch_id,
                    item_index=binding_item_index,
                    item_status=item_status,  # type: ignore[arg-type]
                    # A fanned item whose step reused a stored result says so (§4.4).
                    reused=source_reused and item_status == "succeeded",
                ),
                touched,
                loop_stack=binding_stack,
            )

    def _resolve_kind_routed_edge(
        self,
        edge: Any,
        *,
        routing: EdgeKindRouting,
        payload: Any,
        source_id: str,
        step: int,
        touched: dict[str, None],
        source_dispatch_id: str,
        source_item_index: int,
        loop_stack: list[dict[str, Any]],
    ) -> dict[str, Any] | None:
        """Apply an edge's kind filter and fan-out mode (§7.3/§7.4).

        Returns the payload the edge should deliver in ``all`` mode, or
        ``None`` when the edge produced no join delivery at all — either
        because it PRUNED (its kind never appeared: the zero-code conditional
        path) or because it fanned out into Sends, which open their own
        firings and never touch the accumulator.
        """
        if routing.fans_out:
            items = fan_out_items(payload, routing)
            if items is None:
                # An ``each`` edge that cannot see a list is an authoring
                # problem the run must not paper over: delivering the whole
                # payload once would silently contradict what the author
                # asked for, and doing nothing would look like a prune.
                raise EdgeRoutingError(
                    f"edge '{edge.edge_id}' fans out per item, but "
                    f"'{source_id}' produced nothing it can iterate. Name a "
                    "kind filter on the edge (carry instances of one kind), "
                    "or point the edge at a step that outputs a list.",
                    node_id=source_id,
                    edge_id=edge.edge_id,
                )
            if not items:
                self._record_edge_resolution(
                    edge,
                    PendingEdgeBinding(
                        state="pruned",
                        source_node_id=source_id,
                        source_step=step,
                        dispatch_id=source_dispatch_id,
                        item_index=source_item_index,
                    ),
                    touched,
                )
                return None
            # Deterministic dispatch identity: the same routing pass on the
            # same recorded outcomes must mint the SAME ids, or a replay would
            # re-fan under fresh correlation and the fan-in group would never
            # close. ``ctx.send``'s uuid4 is fine for an executor (its Sends
            # are persisted in the outcome and replayed verbatim); an edge
            # fan-out is recomputed during routing, so it must be derived.
            dispatch_id = f"edge:{edge.edge_id}:{source_dispatch_id}:{source_item_index}"
            if items:
                self._queue_edge_taken(
                    edge,
                    source_id=source_id,
                    step=step,
                    dispatch_id=source_dispatch_id,
                    item_index=source_item_index,
                )
            for index, item in enumerate(items):
                self._edge_fanout_sends.append(
                    (
                        source_id,
                        Send.create(
                            edge.target_node_id,
                            {routing.item_key: item},
                            dispatch_id=dispatch_id,
                            item_index=index,
                        ),
                    )
                )
            self._edge_fanout_loop_stacks[dispatch_id] = [dict(f) for f in loop_stack]
            return None

        # ``all`` — the whole selection to ONE invocation (the ratified
        # default). Only reached with a kind filter set: an edge with neither a
        # filter nor ``each`` never enters this function.
        selection = select_instances(payload, routing.kind_filter or "")
        if not selection.instances:
            # "An edge whose kind never appears doesn't fire." The PRUNE is
            # the feature: the target's join set releases instead of blocking,
            # and a branch that depended solely on this edge resolves dead.
            self._record_edge_resolution(
                edge,
                PendingEdgeBinding(
                    state="pruned",
                    source_node_id=source_id,
                    source_step=step,
                    dispatch_id=source_dispatch_id,
                    item_index=source_item_index,
                ),
                touched,
            )
            return None
        return {routing.item_key: selection.instances}

    def _resolve_back_edge(
        self,
        edge: Any,
        *,
        source_id: str,
        broadcast_payload: dict[str, Any],
        emissions: dict[str, Any],
        source_loop_stack: list[dict[str, Any]] | None = None,
        step: int = 0,
        source_dispatch_id: str = "",
        source_item_index: int = 0,
        user_skipped: bool = False,
    ) -> None:
        """Route one completed source firing over a cycle back-edge (F13).

        Back-edges bypass the join accumulator: a delivery opens a NEW
        firing of the target immediately (join_policy='any' semantics for
        the delivery; the node's static inputs merge in at execute time via
        ``resolve_invocation_inputs``) — the pre-join engine's
        re-fire-per-delivery behavior that legacy feedback loops rely on. A
        prune (skip_edge_ids, predicate false, handle not emitted) simply
        does NOT re-fire — cycle termination. ``on_skipped_upstream`` is not
        consulted (there is no blocked join to police); a skipped source
        just delivers its empty output, exactly like the pre-join engine.
        Termination stays bounded by ``max_steps``.
        """
        if edge.edge_id in self._skip_edge_ids:
            return
        if edge.kind is EdgeKind.CONDITIONAL and edge.condition:
            from matrx_graph.nodes._sandbox import bind_item, safe_eval

            try:
                # bind_item refuses a bare-`inputs` condition over a wrapped
                # scalar payload — the inert-predicate class (W58).
                predicate_input = bind_item(
                    edge.condition,
                    broadcast_payload,
                    where=f"conditional back-edge '{edge.edge_id}'",
                )
                passed = bool(safe_eval(edge.condition, predicate_input))
            except Exception as e:  # noqa: BLE001
                raise EdgeRoutingError(
                    f"conditional back-edge '{edge.edge_id}' predicate failed: "
                    f"{edge.condition!r}: {e}",
                    node_id=source_id,
                    edge_id=edge.edge_id,
                ) from e
            if not passed:
                return
        if edge.source_handle is not None and edge.source_handle not in emissions:
            return  # branch not taken — the loop does not re-fire
        stack = [dict(f) for f in (source_loop_stack or [])]
        is_loop_return = bool(stack) and stack[-1].get("origin_node_id") == edge.target_node_id
        if edge.kind is EdgeKind.CONTROL:
            fragment: dict[str, Any] = {}
        else:
            payload: Any = (
                emissions[edge.source_handle]
                if edge.source_handle is not None
                else broadcast_payload
            )
            if is_loop_return and edge.mappings is None:
                fragment = {"accumulator": payload}  # §9 accumulator wrap
            else:
                fragment = self._map_edge_payload(
                    edge, payload, source_id, step=step, flag_misses=not user_skipped
                )
            if is_loop_return:
                # §9: iteration is ENGINE truth on the return delivery.
                fragment["iteration"] = int(stack[-1]["iteration"])
        if is_loop_return:
            stack = stack[:-1]
        target_id = edge.target_node_id
        firing = self._firing_seq.get(target_id, 0) + 1
        self._firing_seq[target_id] = firing
        self._queue_edge_taken(
            edge,
            source_id=source_id,
            step=step,
            dispatch_id=source_dispatch_id,
            item_index=source_item_index,
        )
        self._back_edge_fires.append(
            Invocation(
                node_id=target_id, inputs=fragment, attempt=1, firing=firing, loop_stack=stack
            )
        )

    def _resolve_failure_edges(
        self,
        *,
        source_id: str,
        node_error: NodeError,
        step: int,
        touched: dict[str, None],
        source_dispatch_id: str = "",
        source_item_index: int = 0,
        as_hole: bool = False,
        source_loop_stack: list[dict[str, Any]] | None = None,
    ) -> None:
        """Resolve a routable node FAILURE into the accumulator (Node Result
        System).

        ``as_hole=False`` (ERROR-edge topology): each outgoing ERROR edge
        DELIVERS the structured ``NodeError`` dump (through the edge's
        mappings — ``code``/``message``/``details`` are addressable source
        keys); every other joinable edge PRUNES, so the success subtree dies
        transitively (§3.3). An ERROR back-edge fires its target directly
        (retry-topology), like any back-edge delivery.

        ``as_hole=True`` (fanned item under ``on_item_failure='hole'``): every
        DATA/CONDITIONAL edge records the item as an explicit FAILED entry in
        its dispatch group — state ``delivered`` with ``item_status='failed'``
        and the error attached — so the aggregated §4.4 delivery reports it as
        a hole with its error instead of deadlocking or parking; CONTROL edges
        keep gating; ERROR edges prune (the hole IS the handling).
        """
        source = self.graph.nodes[source_id]
        error_payload = node_error.model_dump(mode="json")
        # §9 loop state threads through failure routing exactly like the
        # success path — a handler downstream of a loop body inherits the
        # stack, so its eventual loop return still pops/injects correctly.
        stack = [dict(f) for f in (source_loop_stack or [])]
        for edge_id in source.outgoing_edge_ids:
            edge = self.graph.edges[edge_id]
            if edge.kind not in self._JOINABLE_KINDS:
                continue

            if as_hole:
                if edge.is_back_edge:
                    continue  # a failed item never re-fires a cycle
                if edge.kind in (EdgeKind.ERROR, EdgeKind.CONTROL):
                    # ERROR: the hole is the handling. CONTROL: gates the
                    # join but a failed item still counts as resolved.
                    state: str = "pruned" if edge.kind is EdgeKind.ERROR else "delivered"
                    self._record_edge_resolution(
                        edge,
                        PendingEdgeBinding(
                            state=state,  # type: ignore[arg-type]
                            source_node_id=source_id,
                            source_step=step,
                            dispatch_id=source_dispatch_id,
                            item_index=source_item_index,
                            item_status=("failed" if edge.kind is EdgeKind.CONTROL else None),
                        ),
                        touched,
                    )
                    continue
                self._record_edge_resolution(
                    edge,
                    PendingEdgeBinding(
                        state="delivered",
                        payload={},
                        source_node_id=source_id,
                        source_step=step,
                        dispatch_id=source_dispatch_id,
                        item_index=source_item_index,
                        item_status="failed",
                        error=error_payload,
                    ),
                    touched,
                )
                continue

            if edge.kind is EdgeKind.ERROR:
                # The failure record is not the step's output: its paths are never
                # judged against the success output schema, and a mapping that reads
                # nothing from it is not flagged (it legitimately has no output).
                fragment = self._map_edge_payload(
                    edge, error_payload, source_id, flag_misses=False, failure_record=True
                )
                if edge.is_back_edge:
                    # Retry-topology: an ERROR back-edge re-fires its target
                    # directly with the error payload (Pregel re-fire). The
                    # loop frame pops if this IS the loop return.
                    is_loop_return = (
                        bool(stack) and stack[-1].get("origin_node_id") == edge.target_node_id
                    )
                    fire_stack = stack[:-1] if is_loop_return else stack
                    if is_loop_return:
                        fragment["iteration"] = int(stack[-1]["iteration"])
                    target_id = edge.target_node_id
                    firing = self._firing_seq.get(target_id, 0) + 1
                    self._firing_seq[target_id] = firing
                    self._queue_edge_taken(
                        edge,
                        source_id=source_id,
                        step=step,
                        dispatch_id=source_dispatch_id,
                        item_index=source_item_index,
                    )
                    self._back_edge_fires.append(
                        Invocation(
                            node_id=target_id,
                            inputs=fragment,
                            attempt=1,
                            firing=firing,
                            loop_stack=[dict(f) for f in fire_stack],
                        )
                    )
                    continue
                self._record_edge_resolution(
                    edge,
                    PendingEdgeBinding(
                        state="delivered",
                        payload=fragment,
                        source_node_id=source_id,
                        source_step=step,
                        dispatch_id=source_dispatch_id,
                        item_index=source_item_index,
                        item_status="failed" if source_dispatch_id else None,
                        error=error_payload,
                    ),
                    touched,
                    loop_stack=stack,
                )
                continue

            # Normal edge from a failed source — the success branch was not
            # taken: PRUNE (a back-edge simply does not re-fire). A fanned item
            # is marked ``failed`` with its error so a group that completes in a
            # later step (resume) can still be judged all-failed (2026-10-22).
            if edge.is_back_edge:
                continue
            self._record_edge_resolution(
                edge,
                PendingEdgeBinding(
                    state="pruned",
                    source_node_id=source_id,
                    source_step=step,
                    dispatch_id=source_dispatch_id,
                    item_index=source_item_index,
                    item_status="failed" if source_dispatch_id else None,
                    error=error_payload if source_dispatch_id else None,
                    # A caught failure is not a branch not taken: what depends on
                    # this step does not run on its other inputs. An optional
                    # step declared its dependents tolerate it; a fanned item is
                    # its For Each's business (2026-10-27).
                    failed_upstream=(
                        "" if source_dispatch_id or getattr(source, "optional", False) else source_id
                    ),
                    # An optional step that failed is ABSENT: the join it feeds still
                    # receives this connection's fields, as None (2026-10-28).
                    absent_from=(
                        source_id if not source_dispatch_id and getattr(source, "optional", False) else ""
                    ),
                ),
                touched,
            )

    def _map_edge_payload(
        self,
        edge: Any,
        payload: Any,
        source_id: str,
        *,
        step: int = 0,
        flag_misses: bool = True,
        failure_record: bool = False,
    ) -> dict[str, Any]:
        """Shape one edge's payload into the target-arg fragment it delivers.

        Same contract as the pre-join router: explicit mappings pass ONLY the
        mapped fields; no mappings broadcasts the whole dict; a non-dict
        payload lands under the ``value`` key. A mapped path the declared
        output can never have is an EdgeRoutingError; one this output simply
        lacks arrives absent and raises ``engine.mapping_read_nothing``
        (``_queue_mapping_miss``) unless ``flag_misses`` is False — a skipped
        source or a failure record legitimately carries no output.
        ``failure_record`` (an ERROR connection): the payload is the failure
        record, not the step's output, so the success output schema never rules
        a path out — a miss arrives absent, like save-time validation, which
        skips ERROR connections' source paths too.
        """
        edge_id = edge.edge_id
        if not isinstance(payload, dict):
            return {"value": payload}
        if edge.mappings is None:
            # Default behavior: pass entire output payload — MINUS the target's
            # identity inputs, which never bind from a broadcast (see
            # ``matrx_graph.types.identity_inputs``).
            return self._withhold_identity_inputs(edge, payload, source_id)

        target_payload: dict[str, Any] = {}
        for target_key, source_key in edge.mappings.items():
            # Dot-paths are only meaningful on the SOURCE side.
            # A dotted TARGET key would be written verbatim into
            # the downstream node's inputs — a literal input key
            # named e.g. "variables.count", not a nested field —
            # and then silently do nothing. Reject it loudly.
            if "." in target_key:
                raise EdgeRoutingError(
                    f"edge '{edge_id}' mapping has a dotted "
                    f"TARGET key {target_key!r} (mapped from "
                    f"{source_key!r}). Target keys must be "
                    f"plain top-level input field names — a "
                    f"dotted target creates a literal input "
                    f"key named {target_key!r}, not a nested "
                    f"field. Dot-notation is only supported "
                    f"on the SOURCE side of a mapping; use "
                    f"e.g. {target_key.rsplit('.', 1)[-1]!r} "
                    f"as the target key instead.",
                    node_id=source_id,
                    edge_id=edge_id,
                )
            if source_key == WHOLE_PAYLOAD:
                target_payload[target_key] = payload
                continue

            # An unsupported '$' token never reaches a key lookup: say what it
            # IS (a reserved token the engine does not have) rather than
            # letting it read as a missing field of the upstream's output.
            bad_sigil = unknown_sigil(source_key)
            if bad_sigil is not None:
                raise EdgeRoutingError(
                    unknown_sigil_message(str(target_key), bad_sigil, edge_id=str(edge_id)),
                    node_id=source_id,
                    edge_id=edge_id,
                )

            # SELECT A FIELD. The source side is a path —
            # `structured_output.entries`, `items[0].x`,
            # `values.0.final_text` — resolved by THE ONE
            # resolver (``matrx_graph.paths``) that display
            # steps and ``text.json_path`` use.
            #
            # A MISS has two meanings, and the source's declared
            # output schema tells them apart (the same probe the
            # save-time validation and the dry run use):
            #   * the schema PROVABLY lacks the path (a closed level
            #     with no such field) — a real wiring error; validation
            #     refuses it at save, and a run that still meets it
            #     parks ERRORED attributed to the source.
            #   * the schema allows it but THIS output does not carry it
            #   (``first`` is null, an optional key was left out, a
            #   list is shorter) — data, not wiring. The edge delivers
            #   the arg ABSENT; the target's own input check decides
            #   (a required input fails there, naming the input; an
            #   optional one takes its default).
            found, val = resolve_path(payload, source_key)
            if not found:
                problem = (
                    None if failure_record else self._source_path_problem(source_id, source_key)
                )
                if problem is not None:
                    raise EdgeRoutingError(
                        f"edge '{edge_id}' mapping "
                        f"'{target_key}' <- '{source_key}' can never "
                        f"resolve against the output of node "
                        f"'{source_id}': {problem}. Available keys: "
                        f"{sorted(payload.keys())}",
                        node_id=source_id,
                        edge_id=edge_id,
                    )
                logger.info(
                    "[edge %s] %s -> %s: '%s' <- '%s' is not in this output "
                    "(a null or missing value); the input arrives absent and "
                    "the step's own input check decides.",
                    edge_id,
                    source_id,
                    edge.target_node_id,
                    target_key,
                    source_key,
                )
                if flag_misses:
                    self._queue_mapping_miss(
                        edge, source_id=source_id, target_key=str(target_key),
                        source_key=str(source_key), step=step,
                    )
                continue
            target_payload[target_key] = val
        return target_payload

    def _queue_mapping_miss(
        self, edge: Any, *, source_id: str, target_key: str, source_key: str, step: int
    ) -> None:
        """A mapped path read NOTHING from this output (2026-10-27): the input arrives absent,
        and a run that goes on to "complete" with empty results must still say so. Queue ONE
        ``engine.mapping_read_nothing`` review flag per (run, edge, path) — every fan-out item
        and loop firing of the same edge shares the occurrence key — flushed with the routing
        pass. Never fails the run. A run-ahead (partial) routing never queues.

        Not raised (nothing was misread): a branch not taken (a pruned edge never maps), a
        skipped source or an ERROR connection's failure record (``flag_misses=False``), and a
        ``[*]`` path over an EMPTY list (the resolver finds it: an empty fan-out reads ``[]``).
        """
        if self._partial_routing:
            return
        label = "engine.mapping_read_nothing"
        source_name = self._step_label(source_id) or source_id
        self._review.queue(
            ReviewFlag(
                node_id=edge.target_node_id,
                step=step,
                attempt=1,
                label=label,
                message=(
                    f"Input '{target_key}' got nothing: '{source_key}' is not in the output of "
                    f"'{source_name}', so it arrived empty."
                ),
                category="unexpected_path",
                source="engine",
                edge_id=edge.edge_id,
                payload={
                    "from_step": source_id,
                    "path": source_key,
                    "input": target_key,
                },
                occurrence_key=f"{label}|{edge.edge_id}|{source_key}",
            )
        )

    def _source_path_problem(self, source_id: str, source_key: str) -> str | None:
        """Why ``source_key`` can NEVER resolve against ``source_id``'s output.

        None when the declared output (the compiled effective schema, else
        the step type's output schema) cannot rule the path out — dynamic
        outputs, open levels and nullable unions are all unprovable.
        """
        node = self.graph.nodes.get(source_id)
        if node is None:
            return None
        schema = node.effective_output_schema
        if schema is None:
            try:
                spec = self.registry.get(node.spec_type).spec
            except Exception:  # noqa: BLE001 — routing never dies on a registry miss
                return None
            if not spec.dynamic_output:
                schema = model_json_schema(spec.output_schema)
        problem = path_problem(schema, source_key) if schema else None
        if problem is None:
            problem = self._kind_path_problem(node, source_key)
        return problem

    def _kind_path_problem(self, node: Any, source_key: str) -> str | None:
        """Why ``source_key`` can never resolve against the step's DECLARED OUTPUT KIND — or None.

        A step whose output is the kind it declares (Run Typed Agent's answer IS the kind; its
        step type's output schema is open) used to route a path the kind rules out — e.g.
        ``structured_output`` off a typed agent — as an ABSENT input, so the next step got
        ``{}`` and nothing said so (2026-10-28). Keys the step hands BESIDE its kind
        (``run_envelope``, or what it named with ``ctx.declare_beside_kind``) are not the
        kind's and are never judged — per ``??`` alternative, the save gate's own judgment
        (``shape_probe.kind_path_problem``). ``node.output_kind`` is compile's
        ``declared_output_kind`` (authored, else the step type's own) — the save gate's too."""
        from matrx_graph.kinds import cached_kind_schema
        from matrx_graph.shape_probe import kind_path_problem

        slug = getattr(node, "output_kind", None)
        kind_schema = cached_kind_schema(slug)
        if not kind_schema:
            return None
        beside = {str(f) for f in (getattr(getattr(node, "config", None), "run_envelope", None) or ())}
        beside |= self._beside_kind.get(getattr(node, "node_id", None) or "", frozenset())
        return kind_path_problem(
            kind_schema, source_key, beside=beside, origin=f"the declared output kind '{slug}'"
        )

    def _withhold_identity_inputs(
        self, edge: Any, payload: dict[str, Any], source_id: str
    ) -> dict[str, Any]:
        """Strip the target's identity inputs from an UNMAPPED edge payload.

        An edge with no ``mappings`` broadcasts the whole upstream dict. For
        ordinary data that is the right default; for a field that names a
        durable resource somebody else owns (a conversation, a session, a
        thread) it silently re-points the step's identity — the live
        ``conversation_binding_mismatch`` class this closes
        (``matrx_graph.types.identity_inputs``). The author's explicit
        mapping still passes the key; an accident never does.

        Withholding is ANNOUNCED with the remedy, never silent.
        """
        target = self.graph.nodes.get(edge.target_node_id)
        if target is None:
            return dict(payload)
        try:
            input_schema = self.registry.get(target.spec_type).spec.input_schema
        except Exception:  # noqa: BLE001 — routing never dies on a registry miss
            return dict(payload)
        protected = identity_input_fields(input_schema)
        if not protected:
            return dict(payload)
        withheld = sorted(k for k in payload if k in protected)
        if not withheld:
            return dict(payload)
        logger.warning(
            "[edge %s] %s -> %s: withheld %s from this edge's broadcast. "
            "Those fields name a resource this step would have taken over "
            "(they arrived because the edge passes the whole upstream "
            "payload, not because anyone wired them). '%s' starts its own "
            "instead. If you really meant to continue the upstream one, map "
            "it explicitly on the edge (mappings: {'%s': '%s'}).",
            edge.edge_id,
            source_id,
            edge.target_node_id,
            withheld,
            edge.target_node_id,
            withheld[0],
            withheld[0],
        )
        return {k: v for k, v in payload.items() if k not in protected}

    def _skip_default_fragment(self, edge: Any, target: Any, source_id: str) -> dict[str, Any]:
        """§3.4 default_value: substitute skip_defaults for each arg the edge
        maps (validation guarantees completeness; a hole here is a loud
        engine-contract violation, not a silent empty)."""
        if edge.mappings is None:
            return dict(target.skip_defaults)
        fragment: dict[str, Any] = {}
        for target_key in edge.mappings:
            if target_key not in target.skip_defaults:
                raise EdgeRoutingError(
                    f"edge '{edge.edge_id}' maps arg '{target_key}' into node "
                    f"'{target.node_id}' (on_skipped_upstream='default_value') "
                    f"but skip_defaults has no '{target_key}' entry — "
                    f"validate_definition should have rejected this "
                    f"definition (ENGINE_SPEC §3.4).",
                    node_id=source_id,
                    edge_id=edge.edge_id,
                )
            fragment[target_key] = target.skip_defaults[target_key]
        return fragment

    def _record_binding(
        self,
        target_node_id: str,
        edge_id: str,
        binding: PendingEdgeBinding,
        touched: dict[str, None],
        loop_stack: list[dict[str, Any]] | None = None,
    ) -> None:
        """Write one edge resolution into the target's accumulator entry.

        A re-delivery on the SAME key (a later firing of the source, an
        idempotent re-route after an errored-park resume, or a retried item
        redelivering its own index) REPLACES the buffered binding — one key
        holds exactly one latest payload (§2). A delivered binding's
        ``loop_stack`` (§9, post-pop) is stamped onto the entry so the firing
        it produces inherits the loop state (correlation inheritance, §4.3).
        """
        entry = self._ensure_binding_entry(target_node_id)
        entry.edges[edge_id] = binding
        if loop_stack is not None and binding.state == "delivered":
            entry.loop_stack = [dict(f) for f in loop_stack]
        touched[target_node_id] = None

    # Separator inside the per-item accumulator keys
    # ("<edge_id>@@<dispatch_id>@@<item_index>", §4.4). The dispatch_id is
    # load-bearing: two INDEPENDENT dispatches (two sibling maps, or nested
    # maps) delivering over the SAME edge carry equal item_index values, so a
    # key without the dispatch_id would COLLIDE and one dispatch's items would
    # silently overwrite the other's. Recovery of the logical edge_id strips
    # the known "@@<dispatch_id>@@<item_index>" suffix (both taken from the
    # binding, not parsed), so an edge id that itself contains "@@" stays
    # unambiguous; a legacy two-part key ("<edge_id>@@<item_index>", pre-fix
    # checkpoints) falls back to a right rsplit.
    _ITEM_KEY_SEP = "@@"

    def _item_key(self, edge_id: str, binding: PendingEdgeBinding) -> str:
        return (
            f"{edge_id}{self._ITEM_KEY_SEP}{binding.dispatch_id}"
            f"{self._ITEM_KEY_SEP}{binding.item_index}"
        )

    def _logical_edge_id(self, key: str, binding: PendingEdgeBinding) -> str:
        """Recover the logical edge_id from a per-item accumulator key by
        stripping the binding's own ``@@<dispatch_id>@@<item_index>`` suffix.
        Falls back to a right rsplit for a legacy two-part key."""
        suffix = (
            f"{self._ITEM_KEY_SEP}{binding.dispatch_id}{self._ITEM_KEY_SEP}{binding.item_index}"
        )
        if key.endswith(suffix):
            return key[: -len(suffix)]
        return key.rsplit(self._ITEM_KEY_SEP, 1)[0]

    def _record_edge_resolution(
        self,
        edge: Any,
        binding: PendingEdgeBinding,
        touched: dict[str, None],
        loop_stack: list[dict[str, Any]] | None = None,
    ) -> None:
        """Route one resolution to its accumulator key.

        Ordinary (non-fanned) resolutions keep the plain edge_id key. A
        fanned item's resolution (§4.4) gets its own per-item key and stamps
        the entry's ``expected_items`` from the dispatch registry so the
        group's completeness survives a crash (persisted on every
        checkpoint).
        """
        if binding.state == "delivered" and (
            edge.kind is EdgeKind.ERROR or binding.item_status not in ("skipped", "failed")
        ):
            self._queue_edge_taken(
                edge,
                source_id=binding.source_node_id,
                step=binding.source_step,
                dispatch_id=binding.dispatch_id,
                item_index=binding.item_index,
            )
        if not binding.dispatch_id:
            self._record_binding(
                edge.target_node_id, edge.edge_id, binding, touched, loop_stack=loop_stack
            )
            return
        key = self._item_key(edge.edge_id, binding)
        self._record_binding(edge.target_node_id, key, binding, touched, loop_stack=loop_stack)
        expected = self._dispatch_expected.get((binding.dispatch_id, binding.source_node_id))
        if expected is not None:
            self._pending_bindings[edge.target_node_id].expected_items = expected

    def _split_edge_entries(
        self, entry: PendingBinding
    ) -> tuple[
        dict[str, PendingEdgeBinding],
        dict[tuple[str, str], dict[int, PendingEdgeBinding]],
    ]:
        """Partition an entry's edges into (plain, groups).

        ``plain`` is keyed by edge_id; ``groups`` maps ``(logical_edge_id,
        dispatch_id)`` to that dispatch's per-item bindings keyed by item_index
        (§4.4). The dispatch_id is part of the group key so two INDEPENDENT
        dispatches over one physical edge (two sibling maps / nested maps into
        one fan-in) resolve as SEPARATE logical arrivals instead of colliding
        on equal item_index values. Group membership is decided by the
        binding's own ``dispatch_id`` — never by parsing the key alone.
        """
        plain: dict[str, PendingEdgeBinding] = {}
        groups: dict[tuple[str, str], dict[int, PendingEdgeBinding]] = {}
        for key, binding in entry.edges.items():
            if binding.dispatch_id and self._ITEM_KEY_SEP in key:
                logical_id = self._logical_edge_id(key, binding)
                groups.setdefault((logical_id, binding.dispatch_id), {})[binding.item_index] = (
                    binding
                )
            else:
                plain[key] = binding
        return plain, groups

    def _group_expected(
        self, entry: PendingBinding, group: dict[int, PendingEdgeBinding]
    ) -> int | None:
        """How many items this fanned edge group waits for — the dispatcher's
        recorded send count for (dispatch_id, fanned node). In-memory registry
        first (filled at Send-routing time, replay-idempotent), persisted
        ``expected_items`` as the crash-resume fallback. ``None`` = unknown:
        the group can never resolve and the end-of-run deadlock guard screams
        instead of completing silently (§12.8)."""
        any_binding = next(iter(group.values()))
        expected = self._dispatch_expected.get(
            (any_binding.dispatch_id, any_binding.source_node_id)
        )
        return expected if expected is not None else entry.expected_items

    def _edge_resolution(self, entry: PendingBinding) -> tuple[set[str], bool]:
        """Compute (resolved logical edge ids, any-delivery flag) for a
        target's accumulator entry, group-aware (§4.4): a fanned edge group
        resolves only when ALL expected items resolved; it counts as a
        delivery when ≥1 of its items actually delivered."""
        plain, groups = self._split_edge_entries(entry)
        resolved: set[str] = set()
        delivered = False
        for edge_id, binding in plain.items():
            resolved.add(edge_id)
            if binding.state == "delivered":
                delivered = True
        # A physical edge may carry SEVERAL dispatch groups (two sibling maps
        # / nested maps into one fan-in). It resolves only when EVERY buffered
        # group of it is complete — the groups aggregate into one gather
        # firing (§4.4), so a half-filled second group must not let the edge
        # fire early and drop the rest.
        by_edge: dict[str, list[dict[int, PendingEdgeBinding]]] = {}
        for (logical_id, _dispatch_id), group in groups.items():
            by_edge.setdefault(logical_id, []).append(group)
        for logical_id, group_list in by_edge.items():
            # Fan-in completeness reads the run-wide dispatch registry, which
            # only the FULL routing of a step fills: a partial (run-ahead)
            # routing treats every fanned group as still open.
            if self._partial_routing:
                continue
            all_complete = True
            any_delivered = False
            for group in group_list:
                expected = self._group_expected(entry, group)
                if expected is None or len(group) < expected:
                    all_complete = False
                    break
                if any(b.state == "delivered" for b in group.values()):
                    any_delivered = True
            if all_complete:
                resolved.add(logical_id)
                if any_delivered:
                    delivered = True
        return resolved, delivered

    def _ensure_binding_entry(self, target_node_id: str) -> PendingBinding:
        entry = self._pending_bindings.get(target_node_id)
        if entry is None:
            firing = self._firing_seq.get(target_node_id, 0) + 1
            self._firing_seq[target_node_id] = firing
            entry = PendingBinding(firing=firing)
            self._pending_bindings[target_node_id] = entry
        return entry

    def _required_edge_ids(self, node_id: str) -> set[str]:
        """The required inbound set (§3.2): all DATA/CONDITIONAL/CONTROL
        inbound edges — CompiledNode.incoming_edge_ids, finally load-bearing.
        Cycle back-edges are EXCLUDED (F13): requiring one would deadlock
        every run containing a feedback loop; their deliveries open a new
        firing directly instead (``_resolve_back_edge``)."""
        # ONE definition, shared with the resume pre-flight
        # (executor/resume_preflight.py). A fan-out edge (§7.4 ``each``) is a
        # DISPATCHER, exactly like a back-edge: it opens one firing per
        # instance instead of resolving a join, so requiring it would deadlock
        # a target that also has an ordinary inbound edge.
        return required_edge_ids(self.graph, node_id)

    def _drain_completed_joins(self, touched: dict[str, None], step: int) -> list[Invocation]:
        """Fire every target whose required set completed; propagate prunes.

        join_policy 'all' (default): fire when every required edge resolved
        with ≥1 delivery; all-pruned prunes the firing itself, and the dead
        node's own outgoing edges prune transitively (worklist) — this is
        how a dead branch's whole subtree resolves (§3.3). 'any': fire at
        each boundary with ≥1 delivery (explicit multi-fire).
        """
        ready: list[Invocation] = []
        worklist = list(touched)
        while worklist:
            target_id = worklist.pop(0)
            entry = self._pending_bindings.get(target_id)
            if entry is None:
                continue  # already consumed this boundary
            node = self.graph.nodes[target_id]
            required = self._required_edge_ids(target_id)
            resolved_ids, delivered = self._edge_resolution(entry)
            resolved = required <= resolved_ids

            if node.join_policy == "any":
                fire = delivered
                prune = not delivered and resolved
            else:  # "all" (default)
                fire = resolved and delivered
                prune = resolved and not delivered

            # Node Result System: inbound ERROR edges GATE the firing (like
            # CONTROL gates the join). A handler wired A --error--> H,
            # B --data--> H must NOT fire on A's success just because B
            # delivered — the error handler runs only when an error actually
            # arrived. All-ERROR-pruned + fully resolved → the handler
            # subtree dies (§3.3).
            #
            # Two error connections are INPUTS, never gates (2026-10-27, run f2735de2: the
            # result step had a data AND an error connection from one optional side step;
            # the side step succeeded, its error connection pruned, the gate dropped the
            # result step, and the run read "completed" with no result):
            # * one whose source's SUCCESS path reaches this step (directly or through later
            #   steps, ``_success_path_reaches``) — a convergence: exactly one of the success
            #   path and the error connection delivers (run b0e3f868: two hops, dropped);
            # * any error connection into a declared deliverable (THE deliverable rule: an
            #   ``output.*`` step by default, ``data.deliverable`` either way) — the result step
            #   runs whether its side steps failed or not.
            error_required = self._gating_error_edges(target_id, required)
            if error_required and fire:
                plain, groups = self._split_edge_entries(entry)
                error_delivered = any(
                    b.state == "delivered"
                    for eid in error_required
                    for b in ([plain[eid]] if eid in plain else [])
                ) or any(
                    b.state == "delivered"
                    for (logical_id, _d), group in groups.items()
                    if logical_id in error_required
                    for b in group.values()
                )
                if not error_delivered:
                    fire = False
                    prune = resolved
                    if resolved and not self._partial_routing:
                        silent = sorted(self.graph.edges[eid].source_node_id for eid in error_required)
                        self._error_gate_drops.setdefault(target_id, silent[0])

            # A FAILED upstream (caught by its ERROR connection) is not a branch not
            # taken: a join holding its prune does not fire on its other inputs —
            # unless the failure's own error path leads here (the author wired the
            # recovery to rejoin). join_policy 'any' fires per delivery, by declaration.
            failed_upstream = next(
                (b.failed_upstream for b in entry.edges.values() if b.failed_upstream), ""
            )
            if (
                fire
                and failed_upstream
                and node.join_policy != "any"
                and not self._failure_rejoins(failed_upstream, entry)
            ):
                fire = False
                prune = True
                if not self._partial_routing:
                    self._failure_blocked.append((target_id, failed_upstream))

            if fire:
                inputs = self._merge_join_payload(target_id, entry)
                ready.append(
                    Invocation(
                        node_id=target_id,
                        inputs=inputs,
                        attempt=1,
                        firing=entry.firing,
                        # §9/§4.3: the firing inherits the loop state its
                        # deliveries carried (post-pop for a loop return).
                        loop_stack=[dict(f) for f in entry.loop_stack],
                    )
                )
                del self._pending_bindings[target_id]
                # join_policy 'any' can fire while a fanned group is still
                # filling — retain the incomplete group's buffered items for
                # the next firing instead of silently discarding them.
                if node.join_policy == "any":
                    _plain, groups = self._split_edge_entries(entry)
                    leftover: dict[str, PendingEdgeBinding] = {}
                    for (logical_id, _dispatch_id), group in groups.items():
                        expected = self._group_expected(entry, group)
                        if expected is None or len(group) < expected:
                            for b in group.values():
                                leftover[self._item_key(logical_id, b)] = b
                    if leftover:
                        retained = self._ensure_binding_entry(target_id)
                        retained.edges.update(leftover)
                        retained.expected_items = entry.expected_items
            elif prune:
                del self._pending_bindings[target_id]
                # §4.4a: a subtree emptied by a For Each that fanned out ZERO
                # items is "no results", not a dead branch. The gather that
                # closes it FIRES once with an empty aggregated delivery
                # (values [] / count 0) so the steps after it run; every node
                # in between prunes and carries the mark forward.
                from_empty_dispatch = any(
                    b.state == "pruned" and b.empty_dispatch for b in entry.edges.values()
                )
                if from_empty_dispatch and not failed_upstream and node.spec_type == "control.gather":
                    logger.info(
                        "[wf step=%d] gather '%s' closes an empty For Each — firing with no values",
                        step,
                        target_id,
                    )
                    ready.append(
                        Invocation(
                            node_id=target_id,
                            inputs={"items": []},
                            attempt=1,
                            firing=entry.firing,
                            loop_stack=[dict(f) for f in entry.loop_stack],
                        )
                    )
                    continue
                # The firing itself is pruned — the node does not run and
                # its outgoing edges prune transitively (§3.3).
                pruned_touched: dict[str, None] = {}
                self._resolve_source_edges(
                    source_id=target_id,
                    broadcast_payload={},
                    emissions={},
                    user_skipped=False,
                    step=step,
                    touched=pruned_touched,
                    pruned_firing=True,
                    source_loop_stack=entry.loop_stack,
                    empty_dispatch=from_empty_dispatch,
                    failed_upstream=failed_upstream,
                    absent_from=next(
                        (b.absent_from for b in entry.edges.values() if b.absent_from), ""
                    ),
                )
                worklist.extend(pruned_touched)
        return ready

    async def _with_earlier_outputs(
        self, run_id: str, last_outputs: dict[str, Any], up_to_step: int
    ) -> tuple[dict[str, Any], bool]:
        """``last_outputs`` completed with what EARLIER legs of this run settled at or before
        ``up_to_step`` (the resumed checkpoint's step), for the steps this leg did not run (this leg
        wins), and whether the store could be read. A step that keeps its output out of the run row
        is not read (the row never holds it). A store without ``settled_outputs``, or a read that
        fails, leaves ``last_outputs`` as it is (logged) and reports False."""
        missing = {
            nid for nid in self.graph.nodes if nid not in last_outputs and self._output_in_run_row(nid)
        }
        if not missing:
            return last_outputs, True
        settled = getattr(self.checkpointer, "settled_outputs", None)
        if settled is None:
            logger.error(
                "[wf:%s] resumed leg: the checkpointer cannot read earlier legs' outputs "
                "(no settled_outputs) — the run's result holds only this leg's steps",
                run_id[:8],
            )
            return last_outputs, False
        try:
            earlier = await settled(run_id, missing, up_to_step)
        except Exception:  # noqa: BLE001 — reported False: the caller fails the run when results existed
            logger.exception("[wf:%s] resumed leg: earlier legs' outputs could not be read", run_id[:8])
            return last_outputs, False
        merged = {nid: out for nid, out in earlier.items() if nid in missing and out is not None}
        merged.update(last_outputs)
        return merged, True

    async def _resumed_without_result(
        self, *, run_id: str, thread_id: str, channel_values: dict[str, Any]
    ) -> RunResult:
        """A resumed leg that ran nothing, whose earlier steps succeeded but whose results could not
        be read, ends FAILED saying so — never "completed" with nothing (2026-10-28, run 0c33f0f5)."""
        message = (
            "The run was continued from where it stopped, but it had no steps left to run and the "
            "results of the steps it had already run could not be read, so it has no result to hand "
            "back. Re-run it to start fresh."
        )
        logger.error("[wf:%s] resumed_without_result: %s", run_id[:8], message)
        await self._emit(
            RunFailedEvent(
                run_id=run_id,
                steps_executed=0,
                error_type="ResumedWithoutResult",
                error_message=message,
            )
        )
        return RunResult(
            run_id=run_id,
            thread_id=thread_id,
            status=RunStatus.FAILED,
            steps_executed=0,
            channel_values=channel_values,
            last_outputs={},
            error=f"ResumedWithoutResult: {message}",
            failure=RunFailure(
                cause=Cause.ENGINE_ERROR,
                message=message,
                error_type="ResumedWithoutResult",
                technical="resumed_without_result: earlier results exist but settled_outputs was unreadable",
            ),
        )

    async def _earlier_step_history(
        self, run_id: str
    ) -> tuple[set[str], dict[str, dict[str, str]]] | None:
        """Every step of this run that has a recorded outcome, across ALL legs (a resumed run's
        ``last_outputs`` holds only its own leg): ``(succeeded ids, {failed id: {message, cause}})``.
        None when the checkpointer cannot say — the caller then never fails a resumed run on a
        guess."""
        history = getattr(self.checkpointer, "step_history", None)
        if history is None:
            return None
        try:
            return await history(run_id)
        except Exception:  # noqa: BLE001 — a history miss never fails a run; it is logged
            logger.exception("[wf:%s] step history unavailable for the result check", run_id[:8])
            return None

    def _deliverable_ids(self) -> frozenset[str]:
        """THE deliverable set of this graph (``types.deliverables.deliverable_node_ids``), once."""
        cached = getattr(self, "_deliverable_ids_cache", None)
        if cached is None:
            from matrx_graph.types.deliverables import deliverable_node_ids

            cached = frozenset(deliverable_node_ids(self.graph))
            self._deliverable_ids_cache = cached
        return cached

    def _gating_error_edges(self, target_id: str, required: set[str]) -> set[str]:
        """The required ERROR connections into ``target_id`` that gate its firing (see the
        join drain): a pure error handler's inbound error connections. Empty for a declared
        deliverable (THE deliverable rule — ``output.*`` steps by default, ``data.deliverable``
        either way); an error connection whose source also feeds the target normally is an
        input alternative, not a gate."""
        if target_id in self._deliverable_ids():
            return set()
        edges = self.graph.edges
        return {
            eid
            for eid in required
            if edges[eid].kind is EdgeKind.ERROR
            and not self._success_path_reaches(edges[eid].source_node_id, target_id)
        }

    def _success_path_reaches(self, source_id: str, target_id: str) -> bool:
        """Whether ``source_id``'s SUCCESS path (its normal — non-ERROR, forward — connections,
        followed transitively) leads into ``target_id``.

        When it does, ``source --error--> target`` is a CONVERGENCE, not a handler: the step is
        reached on success by the normal path and on failure by the error connection, so the error
        connection is an input alternative and never gates the firing. Run b0e3f868 (wrap-up
        f3ff47f8, 2026-10-27): ``record → … → done → wu_state`` plus ``record --error--> wu_state``;
        the direct-source exemption missed the two-hop path, ``record`` succeeded, its error
        connection pruned, the gate dropped ``wu_state`` and its whole subtree, and the run read
        "completed". A pure handler (the source's success path goes elsewhere) still gates."""
        edges = self.graph.edges
        seen: set[str] = {source_id}
        frontier = [source_id]
        found = False
        while frontier and not found:
            current = frontier.pop()
            for eid in self.graph.nodes[current].outgoing_edge_ids:
                edge = edges.get(eid)
                if edge is None or edge.kind is EdgeKind.ERROR or edge.is_back_edge:
                    continue
                nxt = edge.target_node_id
                if nxt == target_id:
                    found = True
                    break
                if nxt not in seen and nxt in self.graph.nodes:
                    seen.add(nxt)
                    frontier.append(nxt)
        return found

    def _failure_rejoins(self, failed_id: str, entry: PendingBinding) -> bool:
        """Whether a delivery into this join came along ``failed_id``'s ERROR path —
        the failure delivered here directly, or a step its error path leads to did."""
        edges = self.graph.edges.values()
        region: set[str] = set()
        frontier = [
            e.target_node_id
            for e in edges
            if e.source_node_id == failed_id and e.kind is EdgeKind.ERROR
        ]
        while frontier:
            current = frontier.pop()
            if current in region or current == failed_id:
                continue
            region.add(current)
            frontier.extend(e.target_node_id for e in edges if e.source_node_id == current)
        return any(
            b.state == "delivered" and (b.source_node_id == failed_id or b.source_node_id in region)
            for b in entry.edges.values()
        )

    async def _report_failure_blocked(self, run_id: str, step: int) -> None:
        """Say why each join a failed upstream stopped did not run (Law 4): a
        ``node_skipped`` with the reason, never a silent absence."""
        blocked, self._failure_blocked = self._failure_blocked, []
        for node_id, failed_id in blocked:
            failed_label = self._step_label(failed_id) or failed_id
            failure = self._caught_failures.get(failed_id) or {}
            reason = f"'{failed_label}' failed, so this step did not run" + (
                f": {failure['message']}" if failure.get("message") else ""
            )
            logger.warning("[wf:%s step=%d] '%s' not run — %s", run_id[:8], step, node_id, reason)
            await self._emit(
                NodeSkippedEvent(
                    run_id=run_id,
                    step=step,
                    node_id=node_id,
                    spec_type=self.graph.nodes[node_id].spec_type,
                    attempt=1,
                    reason=reason[:500],
                )
            )

    def _merge_join_payload(self, target_id: str, entry: PendingBinding) -> dict[str, Any]:
        """Merge the delivered edge fragments into ONE invocation payload.

        Deterministic edge-id order. Two edges writing the same target key is
        an EdgeRoutingError attributed to the second writer's source — never
        silent last-writer-wins (§3.7) — unless the target declares an
        arg_merge reducer for that key (channel reducer vocabulary). Engine
        markers (``RESERVED_MARKER_KEYS``) are exempt: they are metadata the
        platform stamps, not author data args, so two typed upstreams both
        carrying ``__kind`` is normal fan-in, never a collision.

        A COMPLETE fanned edge group (§4.4) contributes ONE fragment:
        ``{"items": [{item_index, status, value, error, reused}, ...]}`` — ALWAYS
        ordered by item_index, gaps impossible (the group only resolves when
        every expected item resolved), holes explicit (a user-skipped item is
        ``status="skipped"``, a per-item prune ``status="pruned"``, both with
        ``value={}``). CONTROL-kind fanned edges keep their "no payload"
        promise — they gate the join but contribute nothing.
        """
        node = self.graph.nodes[target_id]
        plain, groups = self._split_edge_entries(entry)

        # (deterministic-order key, attributed source, fragment) triples.
        fragments: list[tuple[str, str, dict[str, Any]]] = []
        for edge_id in sorted(plain):
            binding = plain[edge_id]
            if binding.state != "delivered":
                continue
            fragments.append((edge_id, binding.source_node_id, binding.payload))
        # A physical edge may carry SEVERAL dispatch groups. They aggregate
        # into ONE ordered "items" fragment (§4.4 one-logical-upstream): each
        # group's items stay contiguous and internally index-ordered, the
        # groups concatenate in a deterministic arrival order (min source_step,
        # then dispatch_id), and the whole list is RE-INDEXED 0..N-1 so a
        # downstream item_index sort keeps per-group order (never interleaved).
        by_edge: dict[str, list[tuple[str, dict[int, PendingEdgeBinding]]]] = {}
        for (logical_id, dispatch_id), group in groups.items():
            by_edge.setdefault(logical_id, []).append((dispatch_id, group))
        for logical_id in sorted(by_edge):
            edge = self.graph.edges.get(logical_id)
            if edge is not None and edge.kind is EdgeKind.CONTROL:
                continue  # gates the join, binds NO payload (§3.2)
            dispatch_groups = sorted(
                by_edge[logical_id],
                key=lambda dg: (
                    min(b.source_step for b in dg[1].values()),
                    dg[0],
                ),
            )
            items: list[dict[str, Any]] = []
            source_for_attr: str | None = None
            seq = 0
            for _dispatch_id, group in dispatch_groups:
                if not any(b.state == "delivered" for b in group.values()):
                    continue  # all-pruned group — resolved but delivers nothing
                for idx in sorted(group):
                    b = group[idx]
                    if source_for_attr is None:
                        source_for_attr = b.source_node_id
                    if b.state == "pruned":
                        status = "pruned"
                    elif b.item_status in ("skipped", "failed"):
                        status = b.item_status
                    else:
                        status = "succeeded"
                    items.append(
                        {
                            "item_index": seq,
                            "status": status,
                            "value": b.payload if status == "succeeded" else {},
                            # Node Result System: a 'failed' hole carries its
                            # structured NodeError so gather reports WHY.
                            "error": b.error if status == "failed" else None,
                            # Run once per key: this item's step reused a stored result.
                            "reused": status == "succeeded" and b.reused,
                        }
                    )
                    seq += 1
            if source_for_attr is None:
                continue  # every dispatch group all-pruned — delivers nothing
            fragments.append((logical_id, source_for_attr, {"items": items}))

        merged: dict[str, Any] = {}
        first_writer: dict[str, tuple[str, str]] = {}
        merge_pool: dict[str, list[Any]] = {}

        # A join of TWO OR MORE fragments produces a payload with no single
        # author: the target's arg dict is the union of what several upstreams
        # mapped in, which is not any one of their kinds even when they agree
        # (identical kinds fanning in still merge into a wider, different
        # shape). So the engine markers are carried through ONLY on a
        # single-fragment delivery — that payload IS its upstream's payload and
        # keeps its identity, the common typed hop — and DROPPED on a real
        # merge, rather than mislabeling the merged shape with the first
        # writer's kind. Same honesty guard settlement uses at station 1:
        # never stamp a payload with a kind it does not satisfy. The target's
        # own declared ``input_kind`` is what settles a joined payload's
        # identity downstream (the ingestion gate re-stamps it for the check).
        markers_survive = len(fragments) == 1

        for edge_id, source_node_id, payload in fragments:
            for key, value in payload.items():
                if key in RESERVED_MARKER_KEYS:
                    # Engine plane — never an author data arg, so §3.7's
                    # multi-writer error (and arg_merge, which only speaks
                    # about data args) does not apply to it.
                    if markers_survive:
                        merged[key] = value
                    continue
                if key in node.arg_merge:
                    merge_pool.setdefault(key, []).append(value)
                    continue
                if key in first_writer:
                    prev_edge, prev_source = first_writer[key]
                    raise EdgeRoutingError(
                        f"join for node '{target_id}' received input key "
                        f"'{key}' from TWO edges: '{prev_edge}' (source "
                        f"'{prev_source}') and '{edge_id}' (source "
                        f"'{source_node_id}'). Multi-writer same-arg "
                        f"is an error by default — declare "
                        f"data.arg_merge = {{'{key}': 'append' | 'merge' | "
                        f"'replace' | 'sum'}} on '{target_id}' to merge "
                        f"them (ENGINE_SPEC §3.7).",
                        node_id=source_node_id,
                        edge_id=edge_id,
                    )
                first_writer[key] = (edge_id, source_node_id)
                merged[key] = value

        # An optional step that failed is ABSENT, never missing: every field its pruned
        # connection maps arrives as None, so the step it feeds can say "no answer"
        # (2026-10-28). A field another connection delivered keeps that value.
        for edge_id in sorted(plain):
            binding = plain[edge_id]
            if binding.state != "pruned" or not binding.absent_from:
                continue
            edge = self.graph.edges.get(edge_id)
            if edge is None or edge.kind is EdgeKind.CONTROL:
                continue
            for key in edge.mappings or {}:
                if key not in merged and key not in merge_pool and key not in RESERVED_MARKER_KEYS:
                    merged[key] = None

        for key, values in merge_pool.items():
            reducer_name = node.arg_merge[key]
            try:
                reducer_fn = resolve_reducer(reducer_name)
                merged[key] = reducer_fn(None, values)
            except Exception as e:  # noqa: BLE001 — F1: a reducer failure is a
                # ROUTING failure (recoverable ERRORED park with checkpoint),
                # never a terminal ChannelError that kills the run with zero
                # durable state. Attributed to the TARGET node + arg + every
                # contributing edge/source so the user knows exactly which
                # join broke and what fed it.
                writers = [
                    (edge_id, source_node_id)
                    for edge_id, source_node_id, payload in fragments
                    if key in payload
                ]
                writer_desc = (
                    ", ".join(f"'{eid}' (source '{src}')" for eid, src in writers)
                    or "<no contributing edges>"
                )
                raise EdgeRoutingError(
                    f"join for node '{target_id}': arg_merge reducer "
                    f"'{reducer_name}' failed for arg '{key}' merging values "
                    f"from {writer_desc}: {type(e).__name__}: {e}. Fix the "
                    f"reducer choice on '{target_id}' (data.arg_merge) or "
                    f"the upstream outputs, then resume.",
                    node_id=target_id,
                    edge_id=writers[-1][0] if writers else "",
                ) from e
        if (
            node.spec_type == "control.gather"
            and "items" not in merged
            and any(b.state == "pruned" and b.empty_dispatch for b in entry.edges.values())
        ):
            # §4.4a with a plain connection beside the emptied For Each (``items_from``):
            # the join fires on the plain edge, and the empty dispatch still says "no
            # values" rather than leaving the gather with nothing to gather.
            merged["items"] = []
        return merged

    def _snapshot_bindings(self) -> dict[str, PendingBinding]:
        # Structural copy only (MKT-111): the live accumulator mutates each
        # entry's ``edges`` dict, ``expected_items`` and ``loop_stack`` — never a
        # delivered PendingEdgeBinding (an edge is replaced, never edited) or its payload — so the payloads
        # are shared, not deep-copied once per checkpoint. A fan-in of nine
        # targets over one 300 KB value used to copy it nine times per step. A
        # checkpointer that KEEPS the object (MemoryCheckpointer) snapshots it
        # itself; Postgres serializes it before the next step runs.
        return {
            node_id: binding.model_copy(
                update={
                    "edges": dict(binding.edges),
                    "loop_stack": [dict(frame) for frame in binding.loop_stack],
                }
            )
            for node_id, binding in self._pending_bindings.items()
        }

    def _blocked_join_leftovers(self, run_id: str) -> tuple[str, ExecutionError] | None:
        """End-of-run accumulator audit (§3.4 / §12.8).

        Entries holding a real delivery, or ANY 'block'-policy placeholder
        (a block-policy node with unresolved required edges — the skipped
        upstream deliberately recorded nothing, F3), are blocked joins whose
        data/contract would be silently lost on COMPLETED — return the loud
        deadlock error to park on. A pruned sibling edge NEVER launders a
        block placeholder into droppable residue. Pure-pruned residue on
        non-block nodes (dead-branch leftovers) carries no data and is
        dropped with a warning.
        """
        blocked: list[str] = []
        for node_id in sorted(self._pending_bindings):
            entry = self._pending_bindings[node_id]
            has_delivery = any(b.state == "delivered" for b in entry.edges.values())
            resolved_ids, _ = self._edge_resolution(entry)
            has_block_placeholder = self.graph.nodes[
                node_id
            ].on_skipped_upstream == "block" and bool(
                self._required_edge_ids(node_id) - resolved_ids
            )
            if has_delivery or not entry.edges or has_block_placeholder:
                blocked.append(node_id)
            else:
                # No data is lost, but a required connection NEVER resolved: its source neither
                # ran nor was pruned, so this step was never run and never ruled out. Not silent
                # (Law 4): named in the log at ERROR and returned for the run-end review flag.
                unresolved = sorted(self._required_edge_ids(node_id) - resolved_ids)
                logger.error(
                    "[wf:%s] join never resolved: step '%s' did not run — connections %s never "
                    "resolved (resolved: %s); no data was buffered",
                    run_id[:8],
                    node_id,
                    unresolved,
                    sorted(entry.edges),
                )
                self._never_resolved_joins.append((node_id, unresolved))
                del self._pending_bindings[node_id]
        if not blocked:
            return None

        lines: list[str] = []
        for node_id in blocked:
            entry = self._pending_bindings[node_id]
            required = self._required_edge_ids(node_id)
            delivered = sorted(
                f"{eid} (from '{entry.edges[eid].source_node_id}')"
                for eid in entry.edges
                if entry.edges[eid].state == "delivered"
            )
            unresolved = sorted(
                f"{eid} (from '{self.graph.edges[eid].source_node_id}')"
                for eid in required - set(entry.edges)
            )
            lines.append(
                f"  - '{node_id}': delivered=[{', '.join(delivered)}], "
                f"unresolved=[{', '.join(unresolved)}]"
            )
        message = (
            f"Join deadlock: the run frontier is empty but {len(blocked)} "
            f"node(s) still hold partial inbound bindings and can never "
            f"fire:\n" + "\n".join(lines) + "\n"
            "Completing would silently discard the buffered data "
            "(ENGINE_SPEC §3.4/§12.8) — the run is parked ERRORED instead. "
            "Provide the missing upstream data (retry or manual-result the "
            "skipped/unresolved source) and resume."
        )
        logger.error("[wf:%s] %s", run_id[:8], message)
        return blocked[0], ExecutionError(message)

    async def _flag_never_resolved_joins(self, run_id: str, step: int) -> None:
        """RUN-END INVARIANT: a run never reads plain "completed" while a step's join was left
        with a connection that never resolved. Each such step gets one
        ``engine.join_never_resolved`` review flag naming the step and the connections; the run
        keeps its status (no data was lost) but carries the flag for review. Never raises."""
        residue, self._never_resolved_joins = self._never_resolved_joins, []
        for node_id, unresolved in residue:
            sources = sorted(
                {self.graph.edges[eid].source_node_id for eid in unresolved if eid in self.graph.edges}
            )
            names = ", ".join(f"'{self._step_label(s) or s}'" for s in sources) or "an earlier step"
            await self._review.raise_flag(
                run_id,
                ReviewFlag(
                    node_id=node_id,
                    step=step,
                    attempt=1,
                    label="engine.join_never_resolved",
                    message=(
                        f"'{self._step_label(node_id) or node_id}' never ran: it waits on {names}, "
                        "which never finished or was ruled out."
                    )[:500],
                    category="unexpected_path",
                    source="engine",
                    severity="error",
                    occurrence_key=occurrence_key(
                        node_id=node_id, step=step, attempt=1, label="engine.join_never_resolved"
                    ),
                    payload={"unresolved_connections": unresolved, "waits_on": sources},
                ),
            )

    def _blocked_join_invocations(self) -> list[Invocation]:
        """Build the ADDRESSABLE frontier for a join-deadlock park
        (ENGINE_SPEC §3.4 Amendment D2b).

        One ``blocked_join``-flagged invocation per deadlocked node, carrying
        the currently-merged partial inputs (best-effort: a merge failure —
        e.g. an un-reduced multi-writer among the delivered fragments — falls
        back to first-writer-wins so the park itself can never fail). The
        recovery endpoints address the blocked node through it; ``resume``
        runs it only once the user acted (see ``NextInvocation.blocked_join``).
        The pending_bindings entries stay in place — the checkpoint persists
        BOTH the buffered data and its addressable handle.
        """
        invocations: list[Invocation] = []
        for node_id in sorted(self._pending_bindings):
            entry = self._pending_bindings[node_id]
            try:
                partial = self._merge_join_payload(node_id, entry)
            except Exception:  # noqa: BLE001 — park must never fail on a merge error
                partial = {}
                for key in sorted(entry.edges):
                    binding = entry.edges[key]
                    if binding.state == "delivered":
                        for arg, value in binding.payload.items():
                            partial.setdefault(arg, value)
            invocations.append(
                Invocation(
                    node_id=node_id,
                    inputs=partial,
                    attempt=1,
                    blocked_join=True,
                    firing=entry.firing,
                    loop_stack=[dict(f) for f in entry.loop_stack],
                )
            )
        return invocations

    async def _save_checkpoint(
        self,
        run_id: str,
        thread_id: str,
        step: int,
        parent_checkpoint_id: str | None,
        next_invocations: list[NextInvocation],
        interrupt_payload: dict[str, Any] | None = None,
        channel_values_override: dict[str, Any] | None = None,
    ) -> str:
        """Save a checkpoint.

        ``channel_values_override`` lets the errored-state save use a
        pre-step snapshot instead of the current (post-step) snapshot.
        That keeps the channel reducer math correct on resume: the whole
        super-step re-runs (replays cached outcomes for successful
        siblings, re-executes recovered nodes) and channel writes commit
        together at the end. Default ``None`` preserves the existing
        behavior — snapshot is the current channel state.

        Every checkpoint also persists the join accumulator
        (``pending_bindings``, ENGINE_SPEC §3.8) — deep-copied so this
        checkpoint stays immutable history while the live accumulator keeps
        mutating. Consumed firings were already dropped from the live dict,
        so they naturally vanish from subsequent checkpoints while
        historical ones retain them (time-travel intact).
        """
        checkpoint_id = str(uuid4())
        checkpoint = Checkpoint(
            checkpoint_id=checkpoint_id,
            run_id=run_id,
            thread_id=thread_id,
            parent_checkpoint_id=parent_checkpoint_id,
            step=step,
            channel_values=channel_values_override
            if channel_values_override is not None
            else self.channels.snapshot(),
            pending_bindings=self._snapshot_bindings(),
            next_invocations=next_invocations,
            interrupt_payload=interrupt_payload,
        )
        deferred, self._deferred_outcomes = self._deferred_outcomes, []
        together = getattr(self.checkpointer, "save_checkpoint_with_outcomes", None)
        if deferred and together is not None:
            try:
                await together(checkpoint, [outcome for outcome, _ in deferred])
            except Exception:  # noqa: BLE001 — the outcomes and the checkpoint still land, apart
                logger.warning(
                    "[wf:%s step=%d] saving %d pure-step outcome(s) with the checkpoint failed — "
                    "writing each on its own, then the checkpoint",
                    run_id[:8],
                    step,
                    len(deferred),
                    exc_info=True,
                )
                for outcome, _ in deferred:
                    await self.checkpointer.record_outcome(outcome)
                await self.checkpointer.save_checkpoint(checkpoint)
        else:
            for outcome, _ in deferred:
                await self.checkpointer.record_outcome(outcome)
            await self.checkpointer.save_checkpoint(checkpoint)
        for _, completed in deferred:
            await self._emit(completed)
        await self._emit(
            CheckpointSavedEvent(
                run_id=run_id,
                checkpoint_id=checkpoint_id,
                step=step,
                parent_checkpoint_id=parent_checkpoint_id,
            )
        )
        return checkpoint_id

    def _step_defers_outcomes(self, to_run: list[Invocation]) -> bool:
        """Whether this super-step's outcomes wait for its checkpoint: every member is a PURE
        step (milliseconds of work), so holding a completion event until the barrier never
        hides a finished step behind a slow sibling, and the checkpointer can write both
        in one transaction."""
        if not DEFER_PURE_STEP_OUTCOMES or not to_run:
            return False
        if getattr(self.checkpointer, "save_checkpoint_with_outcomes", None) is None:
            return False
        for inv in to_run:
            node = self.graph.nodes.get(inv.node_id)
            if node is None or node.once is not None or node.one_at_a_time is not None:
                return False
            try:
                spec = self.registry.get(node.spec_type).spec
            except Exception:  # noqa: BLE001 — the step itself reports an unknown type
                return False
            if spec.determinism != ActionTier.PURE or spec.category in (NodeCategory.AGENT, NodeCategory.LLM):
                return False
        return True

    async def _flush_deferred_outcomes(self) -> None:
        """Write any held pure-step outcomes on their own (a run that stops without the step's
        checkpoint) and emit their completion events — never lost, never silent."""
        deferred, self._deferred_outcomes = self._deferred_outcomes, []
        for outcome, completed in deferred:
            try:
                await self.checkpointer.record_outcome(outcome)
            except Exception:  # noqa: BLE001 — same posture as a run-ending write: loud
                logger.error(
                    "[wf:%s step=%d node=%s] a held pure-step outcome could not be written",
                    outcome.run_id[:8],
                    outcome.step,
                    outcome.node_id,
                    exc_info=True,
                )
                continue
            await self._emit(completed)

    async def _poll_controls(self, known_status: str | None = None) -> tuple[bool, bool]:
        """``(pause, cancel)`` at a super-step boundary.

        With a host ``control_check`` (one read of the run's status) BOTH
        signals come from that single read — the boundary costs one round
        trip, not two. ``known_status`` is that same column as the checkpoint
        saved just before this boundary read it (``pop_run_status``): when the
        host declared ``control_check_reads_own_row`` it stands in for the read,
        so the boundary costs no round trip at all; any other check is called. Without a
        ``control_check``, the separate checks run exactly as before: pause
        first, cancel only when not pausing."""
        if self._control_check is None or self._pause_latched or self._cancel_latched:
            if await self._should_pause():
                return True, False
            return False, await self._should_cancel()
        # The saved status answers the poll only when the host's check reads
        # nothing beyond that same column; otherwise the check itself runs.
        if known_status is not None and self._control_check_reads_own_row:
            self._pause_latched = known_status == "pausing"
            self._cancel_latched = known_status == "cancelling"
            return self._pause_latched, self._cancel_latched
        try:
            status = await self._control_check()
        except Exception:  # noqa: BLE001
            logger.warning(
                "control_check failed — a pending pause/cancel request may be "
                "delayed one super-step",
                exc_info=True,
            )
            return False, False
        self._pause_latched = status == "pausing"
        self._cancel_latched = status == "cancelling"
        return self._pause_latched, self._cancel_latched

    async def _should_cancel(self) -> bool:
        """Poll the cancel_check. Failures in the check are swallowed — a
        cancellation-query failure should NEVER terminate a real run."""
        if self._cancel_latched:
            return True
        if self._cancel_check is None:
            return False
        try:
            self._cancel_latched = bool(await self._cancel_check())
            return self._cancel_latched
        except Exception:  # noqa: BLE001
            # A failed status poll means a user's Cancel may be IGNORED
            # this step — never silent (audit A6/P1-17).
            logger.warning(
                "cancel_check failed — a pending cancel request may be delayed one super-step",
                exc_info=True,
            )
            return False

    async def _should_pause(self) -> bool:
        """Poll the pause_check. Same swallow-on-failure policy as
        ``_should_cancel`` — a transient lookup failure must never
        unexpectedly suspend a real run."""
        if self._pause_latched:
            return True
        if self._pause_check is None:
            return False
        try:
            self._pause_latched = bool(await self._pause_check())
            return self._pause_latched
        except Exception:  # noqa: BLE001
            logger.warning(
                "pause_check failed — a pending pause request may be delayed one super-step",
                exc_info=True,
            )
            return False

    #: Ceiling on how long a finished invocation waits for its emitter's
    #: ``settle()``. NOT a tuning knob: it is the engine's structural guarantee
    #: that a wedged live wire never holds a node's outcome (or the run) open.
    #: The tunable bound is the HOST's own settle (aidream: the knob
    #: ``runtime.workflow_live_wire_settle_ms``, capped at 15 s), which must stay
    #: below this ceiling.
    node_emitter_settle_timeout_s: float = 20.0

    async def _settle_node_emitter(
        self, app_ctx: AppContext, run_id: str, invocation: Invocation
    ) -> None:
        # THE NODE-EMITTER SETTLE HOOK — optional, duck-typed, bounded.
        #
        # A host emitter may publish live frames (token deltas, live media, its
        # streaming heartbeat) off the critical path: the producer enqueues and
        # returns, a drain task does the I/O. ``node_completed`` / ``node_failed``
        # leave through the RUN-level emitter, so nothing orders them after the
        # invocation emitter's queue — a node's last chunks, its audio, and its
        # final heartbeat could reach the client after the node's outcome, or
        # after the run ended. An emitter that exposes ``async settle()`` is
        # awaited here, after every attempt ends and before its outcome is
        # published. One without it is untouched. A settle that hangs is cut off
        # at ``node_emitter_settle_timeout_s`` and one that raises is logged; the
        # live wire is never load-bearing for the run.
        emitter = getattr(app_ctx, "emitter", None)
        settle = getattr(emitter, "settle", None)
        if not callable(settle):
            return
        try:
            pending = settle()
            if not inspect.isawaitable(pending):
                return
            await asyncio.wait_for(pending, timeout=self.node_emitter_settle_timeout_s)
        except TimeoutError:
            logger.error(
                "[wf:%s node=%s item=%s] node emitter did not settle within %.0fs — "
                "its last live frames may reach the client after the node's outcome",
                run_id[:8],
                invocation.node_id,
                invocation.item_index,
                self.node_emitter_settle_timeout_s,
            )
        except Exception:  # noqa: BLE001 — the live wire never fails the run
            logger.warning(
                "[wf:%s node=%s item=%s] node emitter settle raised — run continues",
                run_id[:8],
                invocation.node_id,
                invocation.item_index,
                exc_info=True,
            )

    async def _emit(self, event: WorkflowEvent) -> None:
        """Best-effort event emission via the AppContext emitter.

        Failures to emit are swallowed: a broken stream must not kill the run.
        All events flow as a single `data` envelope with the typed payload so
        the UI narrows on `data.event`.

        The TYPED model is passed through — serialization (`model_dump`)
        happens at the wire edge (the host's emitter), never here. Emitters
        that need a dict do ``model_dump_json(...)`` (see
        ``matrx_graph.executor.json_dump``) themselves.
        """
        if self._deferred_outcomes and isinstance(event, _RUN_STOP_EVENTS):
            # A held pure-step outcome lands (and says so) before the run says it stopped.
            await self._flush_deferred_outcomes()
        emitter = getattr(self.app, "emitter", None)
        if emitter is None:
            return
        try:
            await emitter.send_data(event)
        except Exception:  # pragma: no cover — defensive only
            logger.warning(
                "event emit failed (event=%s) — stream/UI will miss it; run continues",
                getattr(event, "event", type(event).__name__),
                exc_info=True,
            )


def _invocation_counts(pending: list[Invocation]) -> dict[str, int]:
    counts: dict[str, int] = {}
    for inv in pending:
        counts[inv.node_id] = counts.get(inv.node_id, 0) + 1
    return counts


def _first_interrupt(results: list[_StepResult]) -> GraphInterrupt | None:
    for r in results:
        if r.interrupt is not None:
            return r.interrupt
    return None


# Run-ahead asks "was pause/cancel requested?" before launching, at most this
# often (seconds). An engine pacing constant, not an organization's choice.
RUN_AHEAD_STOP_POLL_SECONDS = 1.0


def _scheduled_step(inv: Invocation, loop_step: int) -> int:
    """The step ``inv`` runs (and is keyed) at: its checkpoint-scheduled step
    when it came off a resumed frontier, else the step the loop is on."""
    return inv.step if inv.step is not None else loop_step


def _routable_ahead(result: _StepResult) -> bool:
    """A finished member whose output may be routed early (the same test ``_expand_run_ahead`` puts ``result``
    to): no failure, interrupt, Send, channel write or fan-out item, and something to route."""
    return not (
        result.error is not None
        or result.interrupt is not None
        or result.sends
        or result.channel_writes
        or result.invocation.dispatch_id
        or (result.output is None and result.failure is None)
    )


def _run_ahead_key(step: int, inv: Invocation) -> tuple[int, str, str, int]:
    """The correlation key (ENGINE_SPEC §4.1) a run-ahead launch is filed under."""
    return (step, inv.node_id, inv.dispatch_id, inv.item_index)


# Kill switch for run-ahead (off = the plain super-step barrier everywhere).
RUN_AHEAD_ENABLED = True

# A super-step of only PURE members lands its outcomes in its checkpoint's transaction
# (``Scheduler._step_defers_outcomes``). Off = one transaction per outcome, as before.
DEFER_PURE_STEP_OUTCOMES = True

# Events after which no held outcome may still be waiting (``Scheduler._emit``).
_RUN_STOP_EVENTS = (
    RunCompletedEvent,
    RunFailedEvent,
    RunCancelledEvent,
    RunInterruptedEvent,
    RunPausedEvent,
    RunErroredEvent,
)


def run_ahead_blockers(graph: CompiledGraph) -> list[str]:
    """Why this graph may not RUN AHEAD of the super-step barrier ([] = it may).

    RUN-AHEAD (2026-10-07; same-step joins 2026-10-14): while a super-step waits
    on a slow member, a member that already finished is routed on a throwaway
    copy of the join state — together with every member of its step that
    already finished, in the barrier's order (a later step's launch is routed
    alone). Every node that partial routing makes Ready is launched at once
    under the step key the barrier would give it, and that step adopts the task
    instead of starting the node again. Step numbers, checkpoints, the park
    frontier and replay keys are exactly the barrier's.

    Graph-level eligibility is these blockers. Per routing, the rules that read
    run-wide state only a FULL routing builds (the empty-map prune, fan-in
    completeness, kind subscriptions) are deferred to the barrier while
    ``Scheduler._partial_routing`` is set, and ``_verify_run_ahead_at_barrier``
    fails the run loudly if a launch ever disagrees with the barrier. It is only
    sound where a node's inputs are fixed by its edges, and each node fires once:

    * channels — a node reads the step-start snapshot, so it could miss a write
      a still-running sibling commits at the barrier;
    * kind-triggered nodes — subscriptions observe at routing time, per step;
    * cycle back-edges and join_policy='any' — a node can fire again, so an
      early launch could take a later firing's place.
    """
    blockers: list[str] = []
    if graph.channels:
        blockers.append("declares channels")
    for node_id, node in graph.nodes.items():
        if node.reads_channels or node.writes_channels or node.output_channel:
            blockers.append(f"node '{node_id}' reads or writes channels")
        elif getattr(node.config, "channel", None):
            blockers.append(f"node '{node_id}' drains a channel")
        if node.trigger_kind:
            blockers.append(f"node '{node_id}' is kind-triggered")
        if node.join_policy == "any":
            blockers.append(f"node '{node_id}' fires on any input")
    for edge_id, edge in graph.edges.items():
        if edge.is_back_edge:
            blockers.append(f"edge '{edge_id}' closes a cycle")
    return blockers


def _as_next_invocations(pending: list[Invocation], step: int) -> list[NextInvocation]:
    """Frontier → checkpoint shape, carrying the FULL correlation identity
    (ENGINE_SPEC §4.1) — dropping (dispatch_id, item_index) here would
    collapse fanned siblings back onto one idempotency key on resume.

    ``step`` is the super-step these invocations are scheduled for (an
    invocation already holding a later step keeps it)."""
    return [
        NextInvocation(
            node_id=inv.node_id,
            inputs=inv.inputs,
            attempt=inv.attempt,
            dispatch_id=inv.dispatch_id,
            item_index=inv.item_index,
            config_override=inv.config_override,
            blocked_join=inv.blocked_join,
            firing=inv.firing,
            loop_stack=[dict(f) for f in inv.loop_stack],
            work_item_id=inv.work_item_id,
            step=inv.step if inv.step is not None else step,
            bypass_once=inv.bypass_once,
        )
        for inv in pending
    ]


def _fact_at(variables: dict[str, Any], path: str) -> Any:
    """The run-variable value at a dotted path (``"confirmed.name"``), or None."""
    current: Any = variables
    for part in path.split("."):
        if not isinstance(current, dict):
            return None
        current = current.get(part)
    return current


def unready_nodes(graph: Any, variables: dict[str, Any]) -> dict[str, str]:
    """{node_id: reason} for every node whose ``ready_when`` facts are not all present.

    Present = non-empty (``matrx_graph.emptiness.is_zero_value`` is the one definition of
    empty, except that a numeric 0 / False fact is still a fact a person stated)."""
    from matrx_graph.emptiness import is_zero_value

    out: dict[str, str] = {}
    for node_id, node in getattr(graph, "nodes", {}).items():
        paths = list(getattr(node, "ready_when", None) or [])
        missing = [
            p for p in paths
            if (v := _fact_at(variables, p)) is None
            or (not isinstance(v, bool | int | float) and is_zero_value(v))
        ]
        if missing:
            out[node_id] = "not ready: " + ", ".join(missing) + (" is" if len(missing) == 1 else " are") + " missing"
    return out


def _settle_default_on_decision_gate(
    interrupt_payload: dict[str, Any] | None,
    resume_value: dict[str, Any] | None,
    decision: DecisionProvenance | None,
) -> dict[str, Any] | None:
    """A DEFAULT-authored resume of a ``decision`` gate carries the author's one
    default value; the gate's schema wants per-item answers. Translate it here,
    at the engine's one resume seam, from the DURABLE spec — so every decision
    gate can time out to its default whoever settles it (the escalation sweeper,
    a host, a test). Any other authority, or an already-shaped answer, passes
    through untouched; an untranslatable default raises a named ExecutionError.

    A form / approval gate (an object ``schema_hint``) whose default is JSON-object
    TEXT resumes with that object, whoever settles it — ``{"answer": "<json>"}``
    never satisfies a schema that wants ``{"decision": ...}``."""
    if decision is None or decision.authority != DecisionAuthority.DEFAULT:
        return resume_value
    block = (interrupt_payload or {}).get("decision")
    if not isinstance(block, dict):
        answer = (resume_value or {}).get("answer")
        as_object = object_default_from_text((interrupt_payload or {}).get("schema_hint"), answer)
        if as_object is None:
            return resume_value
        kept = {k: v for k, v in (resume_value or {}).items() if k == DECISION_KEY}
        return {**as_object, **kept}
    value = dict(resume_value or {})
    answer = value.get("answer")
    if isinstance(answer, dict) and isinstance(answer.get("answers"), dict):
        return resume_value
    raw = answer if answer not in (None, "") else (interrupt_payload or {}).get("default_answer")
    try:
        shaped = default_decision_answer(block, raw)
    except DecisionDefaultError as exc:
        raise ExecutionError(f"The decision gate cannot time out to its default: {exc}") from exc
    logger.info("decision gate settled by its default %r → %s", raw, shaped["answer"])
    value["answer"] = shaped["answer"]
    return value


def _job_lease():
    """``matrx_graph.workers.job_lease``, imported on use (the workers package imports the executor)."""
    from matrx_graph.workers import job_lease

    return job_lease


async def _source_input_problems(node: CompiledNode, values: dict[str, Any]) -> list[str]:
    """What a dynamic-output source step's landed values miss in its compiled contract.

    A field naming a STRUCTURED kind is judged against the kind itself, resolved now (gap 8):
    a cold kind cache at compile leaves that field's compiled fragment the plain type, which
    must never refuse a real object. Every other field keeps the compiled schema's check."""
    from matrx_graph.nodes.io.user_input import UserInputConfig, user_input_kind_problems

    schema = node.effective_output_schema or {}
    kind_problems: list[str] = []
    if isinstance(node.config, UserInputConfig):
        judged, kind_problems = await user_input_kind_problems(node.config, values)
        if judged:
            props = dict(schema.get("properties") or {})
            for key in judged:
                props[key] = {}
            schema = {**schema, "properties": props}
    return validate_instance(schema, values) + kind_problems


def _awaiting_input_result(
    run_id: str, thread_id: str, gaps: list[Any], problems: dict[str, list[str]] | None = None
) -> RunResult:
    """A start parked ``awaiting_input`` on ``gaps`` (PARK-NOT-DIE, INPUT-SURFACE.md); an entry
    whose landed value missed its kind carries ``problems``."""
    missing: list[dict[str, Any]] = []
    for g in gaps:
        entry: dict[str, Any] = {
            "name": g.name,
            "kind": g.kind,
            "sourcing": g.sourcing,
            "variant": g.variant,
            "label": g.label,
            "help": g.help,
            "placeholder": g.placeholder,
            "options": list(g.options),
            "json_schema": dict(g.json_schema),
        }
        if problems and g.name in problems:
            entry["problems"] = list(problems[g.name])
        missing.append(entry)
    return RunResult(
        run_id=run_id,
        thread_id=thread_id,
        status=RunStatus.AWAITING_INPUT,
        steps_executed=0,
        channel_values={},
        last_outputs={},
        interrupt={"kind": "awaiting_input", "missing": missing},
    )
