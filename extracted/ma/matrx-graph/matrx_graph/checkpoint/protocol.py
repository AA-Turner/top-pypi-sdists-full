from __future__ import annotations

from datetime import UTC, datetime
from typing import Any, Literal, Protocol, runtime_checkable

from pydantic import BaseModel, ConfigDict, Field

from matrx_graph.types.send import Send


class PendingEdgeBinding(BaseModel):
    """One inbound edge's resolution within a target node's pending firing.

    ENGINE_SPEC §2/§3.8: an edge either DELIVERED a mapped payload fragment
    into the join buffer, or was PRUNED (handle not emitted, CONDITIONAL
    predicate false, edge in skip_edge_ids, or upstream firing pruned
    transitively). Unsatisfied edges are represented by ABSENCE from
    ``PendingBinding.edges``. ``source_step`` locates the proving
    ``workflow.node_outcome`` row.

    Fan-out correlation (ENGINE_SPEC §4.4): a delivery from a fanned source
    invocation carries its ``(dispatch_id, item_index)`` and is keyed in
    ``PendingBinding.edges`` as ``"<edge_id>@@<item_index>"`` — one entry per
    item — so the fanned edge resolves as ONE logical upstream only when all
    items of the dispatch resolved. ``item_status`` distinguishes a real
    per-item result (``succeeded``) from a user-skip hole (``skipped``) or a
    failed item recorded under ``on_item_failure='hole'`` (``failed`` — Node
    Result System); ``None`` for ordinary non-fanned deliveries. ``error``
    carries the structured NodeError dump (``{code, message, details}``) for
    ``failed`` items and ERROR-edge deliveries.
    """

    state: Literal["delivered", "pruned"]
    payload: dict[str, Any] = Field(default_factory=dict)
    source_node_id: str
    source_step: int
    dispatch_id: str = ""
    item_index: int = 0
    item_status: Literal["succeeded", "skipped", "failed"] | None = None
    error: dict[str, Any] | None = None
    # Run once per key: a succeeded fanned item whose step reused a stored result
    # (outcome ``source="reused"``) instead of running — ``control.gather`` lists it
    # in ``reused_indexes``.
    reused: bool = False
    # §4.4a: this prune came from a For Each that fanned out ZERO items (not a
    # dead branch). It propagates through the emptied subtree so the gather
    # closing it FIRES with ``items: []`` instead of pruning.
    empty_dispatch: bool = False
    # This prune came from a step that FAILED (its failure caught by an ERROR
    # connection; not ``optional``, not a fanned item) — the id of that step.
    # Not a branch not taken: a join holding such a prune does not fire on its
    # other inputs (a check stops what depends on it), and the mark travels
    # through every step it prunes (2026-10-27).
    failed_upstream: str = ""
    # This prune came from an OPTIONAL step that failed (``data.optional``, not a fanned
    # item), directly or through the steps it pruned — the id of that step. A join that
    # fires on its other inputs still receives every field this connection maps, as
    # ``None`` (the step is absent), so a consumer can test ``inputs['x'] is None``
    # instead of raising ``KeyError`` (2026-10-28, Smart Add Identify parent).
    absent_from: str = ""


class PendingBinding(BaseModel):
    """A target node's partial inbound bindings, buffered across super-steps.

    ENGINE_SPEC §3.8: keyed by target node_id in ``Checkpoint.pending_bindings``.
    The node fires when its required set (all inbound DATA / CONDITIONAL /
    CONTROL edges) is fully resolved per its join_policy; the entry is then
    consumed and dropped from subsequent checkpoints (historical checkpoints
    keep it — time-travel intact). ``firing`` is the monotonic per-node firing
    counter; ``loop_stack`` is the engine-carried §9 loop state inherited from
    the delivering source invocation (correlation inheritance, §4.3) — the
    firing this entry produces carries it forward.
    ``expected_items`` (§4.4 aggregated-dispatch fan-in) is the dispatcher's
    recorded send count for the fanned edge group buffered on this entry —
    persisted so a crash-resume can still tell when the group is complete.
    """

    firing: int = 1
    loop_stack: list[dict[str, Any]] = Field(default_factory=list)
    edges: dict[str, PendingEdgeBinding] = Field(default_factory=dict)
    expected_items: int | None = None


class Checkpoint(BaseModel):
    """Durable snapshot of workflow state taken between super-steps.

    A checkpoint captures the full reducible state of a run at one instant:
    channel values AFTER the step's reductions, the partial inbound bindings
    of every still-Blocked join target (``pending_bindings``, ENGINE_SPEC
    §3.8), and the list of node invocations scheduled for the next step
    (including Sends emitted during this step).

    `parent_checkpoint_id` forms a linked list back to the run's origin,
    enabling time-travel (pick any checkpoint as the starting point of a new
    fork run). Forking creates a new run_id that references the parent's
    checkpoint as its first ancestor.
    """

    model_config = ConfigDict(frozen=True)

    checkpoint_id: str
    run_id: str
    thread_id: str
    parent_checkpoint_id: str | None = None
    step: int
    channel_values: dict[str, Any]
    pending_bindings: dict[str, PendingBinding] = Field(default_factory=dict)
    next_invocations: list[NextInvocation] = Field(default_factory=list)
    interrupt_payload: dict[str, Any] | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class NextInvocation(BaseModel):
    """A node invocation scheduled for the next super-step.

    Explicit rather than derived so Sends (dynamic fanout) round-trip through
    checkpoints cleanly. Each invocation carries its correlation identity
    ``(dispatch_id, item_index)`` plus ``attempt`` (ENGINE_SPEC §4.1) so
    fan-out items stay individually addressable and retry counters survive
    resume. Defaults ``''``/``0`` are the ordinary non-fanned identity —
    historical checkpoint rows read correctly.

    ``config_override`` (Phase 5.3) lets the recovery API stash a tweaked
    config that the scheduler merges over the node's authored config at
    execute time — without saving the draft. Used by "Retry without
    saving": user edits a node's config (e.g. bumps max_tokens after a
    token-cap error), clicks Retry, the recovery endpoint stuffs the
    edited config here, the scheduler picks it up on resume, and the
    workflow definition itself stays clean.
    """

    model_config = ConfigDict(frozen=True)

    node_id: str
    inputs: dict[str, Any] = Field(default_factory=dict)
    attempt: int = 1
    dispatch_id: str = ""
    item_index: int = 0
    triggered_by_send: bool = False
    config_override: dict[str, Any] | None = None
    # Durable work-set correlation (matrx_graph.workset): the claimed
    # workflow.work_item id this invocation is processing, so a park/crash
    # frontier still settles its item on resume. '' = ordinary invocation;
    # old rows read correctly.
    work_item_id: str = ""
    # Blocked-join park marker (ENGINE_SPEC §3.4 Amendment D2b). A join
    # deadlock park saves ONE addressable invocation per blocked node,
    # carrying the currently-merged partial inputs, flagged here. The
    # recovery endpoints locate it like any pending invocation (skip /
    # manual-result record an outcome at its correlation key; retry bumps
    # ``attempt``); ``Scheduler.resume`` runs it ONLY when the user acted
    # (outcome exists or attempt > 1) — an unchanged blocked invocation is
    # filtered out and stays represented by ``pending_bindings``. Old rows
    # read as False (ordinary invocations).
    blocked_join: bool = False
    # Monotonic per-node firing number of the join firing that produced this
    # invocation (ENGINE_SPEC §3.8); 0 for invocations that did not come out
    # of the join accumulator (entry seeds, Sends). Resume restores the
    # per-node firing counter from the max over history so firing ids never
    # restart after a park (F5).
    firing: int = 0
    # Interrupt marker (ENGINE_SPEC §6.2). True on the invocation whose
    # GraphInterrupt payload the checkpoint surfaces — resume records
    # ``resume_value`` at THIS invocation's correlation key instead of
    # blindly ``next_invocations[0]`` (the frontier now also carries
    # completed siblings' routed downstream + deferred/errored siblings —
    # nothing is amputated). A second interrupted sibling in the same step
    # rides the frontier UNMARKED and simply re-raises on resume. Old rows
    # read as False.
    is_interrupted: bool = False
    # Engine-carried loop state (ENGINE_SPEC §9): a stack of LoopFrame dicts
    # ``{origin_node_id, iteration}`` pushed by control.loop's body Send and
    # popped when a delivery returns to the frame's origin (the engine then
    # injects ``iteration`` into the delivered payload). Nested loops
    # compose. Persisted so the round-trip never depends on the body echoing
    # orchestration counters (Temporal precedent). Old rows read as [].
    loop_stack: list[dict[str, Any]] = Field(default_factory=list)
    # The super-step this invocation is SCHEDULED to run at — part of its
    # correlation key. An end-of-step checkpoint saved at step N carries the
    # step-N+1 frontier; an interrupt checkpoint mixes the interrupted
    # invocation (step N) with its siblings' routed successors (step N+1).
    # Resume runs each invocation at THIS step, so a node that already ran
    # (or ran ahead) finds its recorded outcome instead of running twice.
    # None (old rows) = run at the checkpoint's own step.
    step: int | None = None
    # Run once per key (``data.once``): the person asked for a FRESH result on this
    # invocation (Retry / Re-run from with "Use saved results" off) — the scheduler ignores
    # any stored result for its key, runs the step, and the new success replaces the row.
    # Persisted so the choice survives the park → resume path recovery uses. Old rows: False.
    bypass_once: bool = False


OutcomeSource = Literal["executor", "user_skip", "user_manual", "retry", "mocked", "reused"]


class NodeOutcome(BaseModel):
    """Persisted record of a completed node invocation. Keyed by idempotency.

    The checkpointer uses this to avoid double-invoking side-effectful nodes on
    resume: before calling execute(), the scheduler asks the checkpointer for
    the outcome at the full correlation key
    ``(run_id, step, node_id, dispatch_id, item_index, attempt)`` — ENGINE_SPEC
    §4.2. If found, it reuses the recorded output instead of re-running the
    node. ``attempt`` is a retry counter WITHIN one correlation key, so
    sibling fan-out items can never replay or overwrite each other's rows
    (the audit-E2 corruption class). ``emissions`` (§5) persists the
    ``ctx.emit`` handle payloads so replay routes handle-keyed edges
    byte-identically (the audit-E3 vanishing-branch class).

    ``source`` tags how the outcome was produced:
      - executor: the normal path — the node's executor ran and returned
      - user_skip: user clicked Skip on a failed node; output is empty {} or
        a user-supplied placeholder. ``error`` is cleared.
      - user_manual: user clicked "Provide manual result"; output is the
        user-supplied value, validated against the node's output_schema.
      - retry: reserved; today retry creates a child checkpoint and runs at
        a new attempt rather than writing a retry-tagged outcome.
      - reused: the step is marked ``data.once`` and a stored success for its
        key and input digest was reused instead of running it;
        ``metadata.reused_from`` names the origin run, step and time.
    """

    model_config = ConfigDict(frozen=True)

    run_id: str
    step: int
    node_id: str
    attempt: int
    dispatch_id: str = ""
    item_index: int = 0
    output: dict[str, Any]
    # Engine-plane facts about this occurrence that are not data: today
    # ``warning_count`` — how many warnings the invocation recorded through
    # ``ctx.warn`` (rows in ``workflow.run_log``), so a surface can badge a
    # step without reading the log. None = nothing to say.
    metadata: dict[str, Any] | None = None
    # The EXACT fully-resolved arguments this invocation was called with:
    # static_inputs authored on the node merged with the edge-routed payload,
    # validated through the spec's input_schema (defaults applied, types
    # coerced) — the same dict NodeStartedEvent carries.
    #
    # 🚨 WHY IT LIVES ON THE OUTCOME (contract C-30): the platform could always
    # say what a step PRODUCED and never, durably, what it was GIVEN. The inputs
    # were computed, streamed as an event, and dropped — so a replay of one node
    # had no starting point, the drill-down walk hit a wall at the first
    # workflow node, and a per-node reviewer could not be enrolled at all. Both
    # halves of one occurrence share one correlation key and one lifetime, so
    # they share one row; a sibling table would let them disagree about which
    # attempt they describe.
    #
    # None = not captured, and that is HONEST, never "no inputs": a user_skip /
    # user_manual outcome had no executor invocation, and rows written before
    # C-30 have nothing to say.
    inputs: dict[str, Any] | None = None
    #: Content-IR kind the input conformed to, when the node declares one.
    #: Deliberately has no `input_ok` twin — the input contract is FATAL at the
    #: binding, so a stored input is by construction one that passed, and a
    #: column that can only ever be true is a lie waiting to happen.
    input_kind: str | None = None
    channel_writes: list[tuple[str, Any]] = Field(default_factory=list)
    sends: list[Send] = Field(default_factory=list)
    emissions: dict[str, Any] = Field(default_factory=dict)
    duration_ms: int = 0
    error: dict[str, Any] | None = None
    source: OutcomeSource = "executor"
    # Platform kind (content_ir.kind_definition slug) the recorded output
    # conforms to — the node's compiled output_kind at execution time.
    # Persisted to workflow.node_outcome.output_kind so stored outputs are
    # Shape-addressable (typed rendering, resume kind-match checks). None for
    # kind-less outcomes (failures, skips, dynamic inline shapes).
    output_kind: str | None = None
    # Shape-verification truth (Content-IR Studio spec §5), persisted so a
    # reloaded run shows the same verified/drift badge as a live one.
    # True = validated against the kind's registered schema; False = drift
    # (per-field strings in output_kind_errors); None = no kind declared or
    # the kind lookup loud-skipped — neutral, never a pass.
    output_kind_ok: bool | None = None
    output_kind_errors: list[str] | None = None
    # Version of the registry kind the verdict was computed against
    # (content_ir.kind_definition.version at resolution). None = kind-less or
    # never-resolved. Persisted (capability-gated until the DB column lands —
    # see PostgresCheckpointer.record_outcome) so stored verdicts are
    # version-addressable.
    output_kind_version: int | None = None
    # Named degraded mode (matrx_graph.kinds.KindDegradedReason slug) when the
    # output kind check loud-skipped. None = check ran or no kind declared.
    # Persisted so "skipped" is queryable and never renderable as "passed".
    output_kind_degraded: str | None = None
    # Timezone-AWARE, matching Checkpoint.created_at — a naive utcnow here
    # gets re-interpreted by TIMESTAMPTZ as server-local time (audit P3-4).
    completed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


@runtime_checkable
class Checkpointer(Protocol):
    """Durable store for workflow state.

    The scheduler writes one checkpoint per super-step (after reductions) and
    one NodeOutcome per completed invocation. Reads happen on run start
    (latest checkpoint), on resume (by id), and on idempotency check (by the
    invocation key).

    Phase 1: MemoryCheckpointer for tests + in-process single-server use.
    Phase 2: PostgresCheckpointer (via matrx-orm) for durability + multi-worker.
    """

    async def save_checkpoint(self, checkpoint: Checkpoint) -> None: ...

    async def load_checkpoint(self, checkpoint_id: str) -> Checkpoint | None: ...

    async def latest_checkpoint(self, run_id: str) -> Checkpoint | None: ...

    async def list_checkpoints(self, run_id: str) -> list[Checkpoint]: ...

    async def record_outcome(self, outcome: NodeOutcome) -> None: ...

    async def get_outcome(
        self,
        run_id: str,
        step: int,
        node_id: str,
        attempt: int,
        dispatch_id: str = "",
        item_index: int = 0,
    ) -> NodeOutcome | None: ...


def step_history_from_outcomes(
    outcomes: list[tuple[str, dict[str, Any] | None]],
) -> tuple[set[str], dict[str, dict[str, str]]]:
    """``(succeeded step ids, {failed step id: {message, cause}})`` from a run's
    ``(node_id, error)`` outcome pairs. A step with any success row succeeded (a retry that
    worked); one with only error rows failed. Read by the scheduler's run-end result check on a
    resumed run, whose own ``last_outputs`` holds only its leg."""
    succeeded: set[str] = set()
    failed: dict[str, dict[str, str]] = {}
    for node_id, error in outcomes:
        if error:
            failed.setdefault(
                node_id,
                {"message": str(error.get("message") or ""), "cause": str(error.get("cause") or "")},
            )
        else:
            succeeded.add(node_id)
    return succeeded, {nid: info for nid, info in failed.items() if nid not in succeeded}


OutcomeKey = tuple[int, str, int, int]
"""``(step, dispatch_id, item_index, attempt)`` — where one step's outcome row sits in a run."""


def latest_settled_keys(
    outcomes: list[tuple[str, OutcomeKey, dict[str, Any] | None]],
    node_ids: set[str],
    up_to_step: int | None = None,
) -> dict[str, OutcomeKey]:
    """For each of ``node_ids``, the key of its LATEST successful outcome, from a run's
    ``(node_id, key, error)`` rows (later step, then item, then attempt wins — the same one a live
    leg's ``last_outputs`` ends on), counting only steps at or before ``up_to_step`` (the resumed
    checkpoint's step: a resume from an older checkpoint never takes a later leg's output as
    "earlier"). Read by the scheduler when a resumed leg completes: its own ``last_outputs`` holds
    only the steps IT ran, so the run's result is completed with what earlier legs settled
    (``settled_outputs``)."""
    latest: dict[str, OutcomeKey] = {}
    for node_id, key, error in outcomes:
        if node_id not in node_ids or error or (up_to_step is not None and key[0] > up_to_step):
            continue
        held = latest.get(node_id)
        if held is None or (key[0], key[2], key[3]) > (held[0], held[2], held[3]):
            latest[node_id] = key
    return latest
