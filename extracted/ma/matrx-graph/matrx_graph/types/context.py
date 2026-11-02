from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, NoReturn
from uuid import uuid4

from pydantic import BaseModel

from matrx_graph.errors import GraphInterrupt
from matrx_graph.types.channel import coerce_to_json
from matrx_graph.types.send import Send

if TYPE_CHECKING:
    from matrx_connect.context.app_context import AppContext
    from matrx_connect.context.emitter_protocol import Emitter

    from matrx_graph.checkpoint.protocol import Checkpointer


#: Floor between two ``NodeProgressEvent`` frames from ONE invocation
#: (SPEC-workflow-ui-contract §5.1). Durable events are cheap individually and
#: ruinous in a tight loop; 500 ms is faster than a human reads and slower than
#: any loop can flood.
PROGRESS_MIN_INTERVAL_S: float = 0.5


@dataclass(frozen=True, slots=True)
class ResumeAnswer:
    """A person's answer handed to the step that relayed the question
    (``forwards_answer`` interrupt): the value exactly as the resume carried it
    and WHO decided (``DecisionProvenance``; None = the value's own stamp, if any)."""

    value: dict[str, Any] | None
    decision: Any = None


@dataclass(slots=True)
class ChannelView:
    """Read-only snapshot of channel values for a node invocation.

    The scheduler captures channel state at the start of each super-step and
    hands every node in that step an identical view. Writes go through the
    explicit `write()` API, which queues updates for reduction between steps
    rather than applying them immediately.
    """

    _values: dict[str, Any]
    _pending_writes: list[tuple[str, Any]]

    def get(self, name: str, default: Any = None) -> Any:
        return self._values.get(name, default)

    def has(self, name: str) -> bool:
        return name in self._values

    def snapshot(self) -> dict[str, Any]:
        return dict(self._values)

    def write(self, channel: str, value: Any) -> None:
        """Queue a write. Applied between super-steps by the channel manager.

        Pydantic models are dumped to JSON-safe form; all other values are
        validated as JSON-serializable immediately (raises ChannelError if not).
        """
        if isinstance(value, BaseModel):
            normalized = value.model_dump(mode="json")
        else:
            normalized = coerce_to_json(value)
        self._pending_writes.append((channel, normalized))

    def drain(self) -> list[tuple[str, Any]]:
        writes = list(self._pending_writes)
        self._pending_writes.clear()
        return writes


@dataclass(slots=True)
class NodeExecutionContext:
    """Per-invocation context handed to a node executor.

    Wraps AppContext via COMPOSITION (not subclassing). This preserves
    dataclasses.replace() semantics on AppContext and keeps graph execution
    testable without registering ContextVars. The scheduler constructs one of
    these per node invocation and passes it explicitly — do not put this type
    in a ContextVar.

    `app` carries user/org/emitter/conversation identity, already forked for
    this workflow step via AppContext.fork_for_workflow_step().

    `(run_id, thread_id, node_id, step, attempt)` form the idempotency key used
    by the checkpointer to dedupe retried invocations of side-effectful nodes.
    """

    app: AppContext
    run_id: str
    thread_id: str
    node_id: str
    step: int
    attempt: int
    channels: ChannelView
    checkpointer: Checkpointer
    dispatch_id: str = ""
    item_index: int = 0
    firing: int = 0
    # The registry this run was scheduled with. A node that DELEGATES to
    # another node type (pipe.step's code pipe) must resolve the delegate
    # from the same registry the scheduler is using, never from the process
    # global — otherwise a run scheduled with a custom registry silently
    # dispatches against a different catalog. None = fall back to the
    # default registry (direct-execute paths that construct a ctx by hand).
    registry: Any = None
    # The kind slug this node INSTANCE is declared to produce — the compiled
    # ``output_kind`` (``NodeSpec.output_kind``, overridden per node by
    # ``data.output_kind``), the very value the scheduler validates this
    # invocation's output against and stamps on the outcome row.
    #
    # A node executor that can SHAPE what it produces reads this and honors it:
    # ``ai.agent.produce`` binds the model's ``response_format`` to this kind's
    # schema, so the agent answers IN the declared shape instead of emitting
    # prose that a downstream projection node has to reconstruct (Arman's
    # ruling, 2026-08-20 — the seven Study Pack projection nodes existed only
    # because the agent never saw its own declaration). Never a second
    # authority: it is the SAME slug the verdict is computed against, handed to
    # the executor instead of being kept from it.
    output_kind: str | None = None
    # The workflow this run executes (the scheduler's ``definition_id``); None for a run of an
    # unsaved definition or a hand-built context. Read through ``run_facts``.
    workflow_id: str | None = None
    # Set only on the invocation that relayed a question (``forwards_answer``)
    # when the run resumes with the person's answer: the step hands it on
    # (``subgraph.call`` resumes its waiting child with it). None otherwise.
    resume_answer: ResumeAnswer | None = None
    _sends: list[Send] = field(default_factory=list)
    _emissions: dict[str, Any] = field(default_factory=dict)
    # Fan-out correlation (ENGINE_SPEC §4.1): ONE dispatch_id minted lazily
    # per invocation-execution on the first ctx.send(); every Send of this
    # invocation shares it, with item_index auto-incremented. Persisted in
    # the dispatcher's NodeOutcome.sends → crash-replay reuses the SAME ids.
    _dispatch_id: str = ""
    # Billed AI usage this invocation actually spent, recorded by the executor
    # (see ``record_billed_usage``). Engine-plane, never data-plane.
    _billed_usage: dict[str, Any] | None = None
    # Top-level payload keys this invocation hands over BESIDE its kind (see
    # ``declare_beside_kind``). Engine-plane: the kind check ignores them.
    _beside_kind: frozenset[str] = frozenset()
    # ``progress`` throttle clock (SPEC §5.1: at most one NodeProgressEvent per
    # 500 ms per node, PER INVOCATION). The context IS the invocation — it is
    # minted once per (node_id, dispatch_id, item_index) — so instance state is
    # exactly the required key, with no shared registry to leak across a
    # fan-out or across runs.
    _last_progress_monotonic: float = 0.0
    # Warnings this invocation recorded through ``warn`` — the scheduler stamps
    # the count on the outcome row (``node_outcome.metadata.warning_count``).
    _warning_count: int = 0

    @property
    def emitter(self) -> Emitter:
        return self.app.emitter

    @property
    def user_id(self) -> str:
        return self.app.user_id

    @property
    def organization_id(self) -> str | None:
        return self.app.organization_id

    @property
    def project_id(self) -> str | None:
        return self.app.project_id

    @property
    def conversation_id(self) -> str:
        return self.app.conversation_id

    @property
    def request_id(self) -> str:
        return self.app.request_id

    @property
    def api_keys(self) -> dict[str, str]:
        return self.app.api_keys

    @property
    def run_facts(self) -> dict[str, str | None]:
        """The run's own identity, as ``{"$run": name}`` reads it (``RUN_REF_FIELDS``)."""
        return {
            "id": self.run_id,
            "workflow_id": self.workflow_id,
            "step_id": self.node_id,
            # The run's carried context (AppContext) — never resolved from a default.
            "organization_id": self.organization_id,
            "user_id": self.user_id,
        }

    @property
    def idempotency_key(self) -> str:
        return f"{self.run_id}:{self.step}:{self.node_id}:{self.attempt}"

    @property
    def stable_idempotency_key(self) -> str:
        """Identity for work that must survive a workflow-node retry.

        ``attempt`` is deliberately excluded. Fan-out correlation and the
        monotonic firing number distinguish multiple logical invocations of
        the same node without creating a second durable session on retry.
        """
        dispatch = self.dispatch_id or "root"
        return (
            f"{self.run_id}:{self.step}:{self.node_id}:{dispatch}:{self.item_index}:{self.firing}"
        )

    def record_billed_usage(
        self,
        usage: dict[str, Any],
        *,
        conversation_id: str | None = None,
        request_id: str | None = None,
    ) -> None:
        """Declare what this invocation SPENT, independent of what it returns.

        Cost settlement used to sniff the node's payload for a top-level
        ``usage`` block — which silently ties "did we bill this?" to the SHAPE
        of the data the node hands downstream. A node whose payload is a
        platform kind (``ai.agent.produce`` returns the kind, not the run
        envelope) has nowhere to put a usage block, and additionalProperties:
        false kinds forbid inventing one. So spend is DECLARED here, on the
        engine plane, and the scheduler settles from this when present and
        falls back to payload sniffing for every node that has not migrated.

        Shape: the canonical ``AiExecutionResult.usage`` block
        (``cost_usd`` / ``input_tokens`` / ``output_tokens`` / ``models``).
        """
        self._billed_usage = {
            "usage": dict(usage),
            "conversation_id": conversation_id,
            "request_id": request_id,
        }

    def declare_beside_kind(self, fields: list[str] | tuple[str, ...] | set[str]) -> None:
        """Declare top-level payload keys that ride BESIDE the kind, not inside it.

        A kind-answering step (``ai.agent.produce``) may also hand downstream the
        run's own facts (``final_text``, ``messages``, ``usage``…) so a step that
        read them keeps every door. Those keys are not the kind's: the output
        kind check validates the payload WITHOUT them; the payload itself (what
        edges read and what is stored) keeps them.
        """
        self._beside_kind = frozenset(str(f) for f in fields if f and str(f) != "__kind")

    def beside_kind_fields(self) -> frozenset[str]:
        """The keys :meth:`declare_beside_kind` named (scheduler-only)."""
        return self._beside_kind

    def drain_billed_usage(self) -> dict[str, Any] | None:
        """Take the declared spend (scheduler-only), clearing it."""
        recorded, self._billed_usage = self._billed_usage, None
        return recorded

    async def progress(
        self,
        message: str = "",
        *,
        fraction: float | None = None,
        current: int | None = None,
        total: int | None = None,
    ) -> None:
        """Emit a best-effort mid-node progress signal (BS-6).

        Long executors call this between units of work ("3/10 sources
        analyzed") so the canvas shows movement instead of a minutes-long
        black box. NEVER load-bearing: emission failures are swallowed
        with a log — losing a progress tick must not affect execution.

        THROTTLED to at most one frame per ``PROGRESS_MIN_INTERVAL_S`` per
        invocation (SPEC §5.1). A tight loop over 5 000 items would otherwise
        write 5 000 durable ``wf_node_events`` rows for a bar that can only
        move 60 times a second. Two classes always pass:

        - the TERMINAL tick (``current >= total``, or ``fraction >= 1.0``) —
          dropping it leaves the bar parked at 998/1000 forever;
        - the FIRST tick of the invocation — "1 of 500" must appear at once,
          not half a second later.
        """
        import time

        from matrx_graph.types.events import NodeProgressEvent

        now = time.monotonic()
        terminal = (current is not None and total is not None and current >= total) or (
            fraction is not None and fraction >= 1.0
        )
        if (
            not terminal
            and self._last_progress_monotonic
            and (now - self._last_progress_monotonic) < PROGRESS_MIN_INTERVAL_S
        ):
            return
        self._last_progress_monotonic = now

        try:
            await self.app.emitter.send_data(
                NodeProgressEvent(
                    run_id=self.run_id,
                    step=self.step,
                    node_id=self.node_id,
                    attempt=self.attempt,
                    dispatch_id=self.dispatch_id,
                    item_index=self.item_index,
                    message=message,
                    fraction=fraction,
                    current=current,
                    total=total,
                )
            )
        except Exception:  # noqa: BLE001 — progress is best-effort
            import logging

            logging.getLogger(__name__).warning(
                "node progress emit failed (run=%s node=%s) — UI tick lost",
                self.run_id[:8],
                self.node_id,
                exc_info=True,
            )

    async def phase(self, phase: str) -> None:
        """Announce WHAT THIS STEP IS DOING, from the closed vocabulary.

        The liveness twin of :meth:`progress`: ``progress`` carries countable
        work, ``phase`` carries the named moment. The label is folded onto
        :data:`~matrx_graph.types.events.AGENT_STEP_PHASES` here, so no caller
        can widen the vocabulary by accident (an unknown label still reaches
        the screen — see ``map_agent_step_phase`` — but it screams in the log).

        Best-effort by contract, exactly like ``progress``: an emitter that
        does not implement ``send_phase`` (or one that throws) costs a debug
        line and nothing else. Liveness is never load-bearing.
        """
        from matrx_graph.types.events import map_agent_step_phase

        label = map_agent_step_phase(phase)
        if label is None:
            return
        send_phase = getattr(self.app.emitter, "send_phase", None)
        if send_phase is None:
            return
        try:
            await send_phase(label)
        except Exception:  # noqa: BLE001 — liveness is never load-bearing
            import logging

            logging.getLogger(__name__).debug(
                "node phase emit failed (run=%s node=%s phase=%s)",
                self.run_id[:8],
                self.node_id,
                label,
                exc_info=True,
            )

    def send(
        self,
        target_node_id: str,
        payload: dict[str, Any] | BaseModel | None = None,
        *,
        work_item_id: str = "",
    ) -> None:
        """Queue a Send directive. Applied by the scheduler after execute() returns.

        Creates a new invocation of `target_node_id` in the next super-step
        with `payload` as its inputs. Each Send carries its own correlation
        identity `(dispatch_id, item_index)` (ENGINE_SPEC §4.1) — minted once
        per calling invocation, item_index auto-incremented — so dynamic
        fanout is idempotent under replay and retries stay per-item.
        """
        if not self._dispatch_id:
            self._dispatch_id = str(uuid4())
        self._sends.append(
            Send.create(
                target_node_id=target_node_id,
                payload=payload,
                dispatch_id=self._dispatch_id,
                item_index=len(self._sends),
                work_item_id=work_item_id,
            )
        )

    async def warn(
        self,
        label: str,
        message: str,
        *,
        payload: Any = None,
        payload_kind: str | None = None,
    ) -> bool:
        """Record that this step WORKED but missed something. Never fails the run.

        THE WARNINGS CHANNEL (response-checks DESIGN §7.1). The row lands in
        ``workflow.run_log`` through the ONE writer (``matrx_graph.run_log``),
        immediately — a warning is durable even if the worker dies a moment
        later — and the scheduler stamps the count on the outcome row. Returns
        whether the row landed. ``label`` is a stable key from a closed
        vocabulary (``response_check.revised`` …); ``message`` the sentence.
        """
        from matrx_graph.run_log import write_run_log

        entry = await write_run_log(
            run_id=self.run_id,
            node_id=self.node_id,
            step=self.step,
            attempt=self.attempt,
            label=label,
            message=message,
            severity="warning",
            payload=coerce_to_json(payload) if payload is not None else None,
            payload_kind=payload_kind,
            organization_id=self.organization_id,
            user_id=str(self.user_id) if self.user_id else None,
        )
        self._warning_count += 1
        return entry.recorded

    async def flag_for_review(
        self,
        label: str,
        message: str,
        *,
        category: str = "other",
        payload: Any = None,
        payload_kind: str | None = None,
        severity: str = "warning",
        source: str = "step_code",
        edge_id: str | None = None,
    ) -> bool:
        """Flag this workflow for review: the run carries on and SUCCEEDS, but what just
        happened (a recovery, a redo, a fallback, extra work) should never have been needed.

        THE REVIEW-FLAG CHANNEL (0117). Same one writer as :meth:`warn`, with
        ``needs_review`` set: the database groups it into one review issue per
        (workflow, step, connection, ``label``), counts it on the run, and the host's
        notifier hears about a new or returning issue. ``label`` is a STABLE key (never
        embed an id or a time); ``category`` is one of ``matrx_graph.run_log.CATEGORIES``.
        Returns whether the row landed. Never fails the run.
        """
        from matrx_graph.run_log import write_run_log

        entry = await write_run_log(
            run_id=self.run_id,
            node_id=self.node_id,
            step=self.step,
            attempt=self.attempt,
            label=label,
            message=message,
            severity=severity,
            payload=coerce_to_json(payload) if payload is not None else None,
            payload_kind=payload_kind,
            organization_id=self.organization_id,
            user_id=str(self.user_id) if self.user_id else None,
            needs_review=True,
            category=category,
            source=source,
            edge_id=edge_id,
        )
        self._warning_count += 1
        return entry.recorded

    @property
    def warning_count(self) -> int:
        return self._warning_count

    def drain_sends(self) -> list[Send]:
        sends = list(self._sends)
        self._sends.clear()
        return sends

    def emit(self, handle_id: str, payload: dict[str, Any] | BaseModel | None = None) -> None:
        """Emit `payload` on output handle `handle_id`.

        The scheduler routes handle-keyed emissions only to outgoing edges whose
        `source_handle` matches `handle_id`. Edges without a `source_handle`
        receive the executor's return value, not emissions. This is how
        branching nodes route to exactly one of several downstream targets
        (e.g. `control.branch` emits on 'true' or 'false').
        """
        if payload is None:
            normalized: Any = {}
        elif isinstance(payload, BaseModel):
            normalized = payload.model_dump(mode="json")
        else:
            normalized = coerce_to_json(payload)
        self._emissions[handle_id] = normalized

    def drain_emissions(self) -> dict[str, Any]:
        emitted = dict(self._emissions)
        self._emissions.clear()
        return emitted

    def interrupt(self, payload: dict[str, Any]) -> NoReturn:
        """Pause the run and surface `payload` to the UI.

        Raises `GraphInterrupt`. The scheduler catches this, persists an
        interrupt checkpoint containing `payload`, and halts the super-step
        loop. Resuming via `POST /runs/:id/resume` replays from the interrupt
        checkpoint with the user's response as the node's effective output.
        """
        _ = coerce_to_json(payload)  # fail fast if not JSON-serializable
        raise GraphInterrupt(node_id=self.node_id, payload=payload)
