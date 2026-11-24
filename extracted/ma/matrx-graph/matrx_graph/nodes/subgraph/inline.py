"""A called workflow that runs INSIDE its caller's step — no run of its own (L-SPEED 6d, 2026-11-09).

A workflow is "just Python running code" (Arman, research VISION 2026-11-09): calling one should cost a
function call, not a durable run (run row, setup, terminal write, hand-back, value copy). A workflow that
declares ``metadata.runs_as = "inline"`` (set with the ``set_workflow_setting`` patch op) is run by Run
Workflow as a nested :class:`~matrx_graph.Scheduler` inside the calling step's leg:

- **One run.** The nested scheduler runs under the CALLER's run id: its paid requests land in the caller's
  ledger and the caller's spend gate answers its launches; no child run row exists.
- **Its own identities.** Every identity an executor derives from ``ctx.dispatch_id`` (a deeper child run,
  idempotency keys, a step's request conversation) carries the call's namespace (:func:`inline_namespace`),
  so two inline children of one run (a For each over an inline child) never share one.
- **Its steps under the calling step.** Its events stream on the caller's stream with the step path
  ``<calling step>/<child step>`` (:func:`inline_node_prefix`); its run-level events (started, completed,
  checkpoint saved) are dropped — the calling step is what starts and ends.
- **Resume = the calling step runs the child again.** Checkpoints live in memory. A step that re-runs
  safely (``step_reruns_safely``: pure/idempotent, spends nothing) and sent no work records nothing; every other
  step's outcome (a loop or For each that sent work included) is recorded under the caller's run (node id = its step path, dispatch id namespaced), so the re-run
  REPLAYS it instead of paying or writing twice.

A child that pauses (a question, a timer) cannot run inline — the host refuses that loudly.
"""

from __future__ import annotations

from typing import Any

from matrx_graph.checkpoint.memory import MemoryCheckpointer
from matrx_graph.checkpoint.protocol import Checkpoint, NodeOutcome

#: ``Definition.metadata["runs_as"]`` value: the workflow runs inside its caller's step (this module).
RUNS_INLINE = "inline"

#: Run-level events of the nested scheduler: the calling step starts and ends, never the child.
_RUN_LEVEL_EVENTS = frozenset({
    "run_started", "run_completed", "run_failed", "run_cancelled", "run_paused", "run_resumed",
    "run_errored", "run_interrupted", "checkpoint_saved",
})


def runs_inline(metadata: Any) -> bool:
    """True when a workflow's definition metadata asks to run inside its caller's step."""
    return isinstance(metadata, dict) and metadata.get("runs_as") == RUNS_INLINE


def inline_namespace(ctx: Any) -> str:
    """The calling invocation's identity prefix for its inline child: unique per (dispatch, step, item,
    firing) and nested (``ctx.dispatch_id`` of a step inside an inline child already carries its own)."""
    return f"{ctx.dispatch_id or 'root'}>{ctx.node_id}#{ctx.item_index}.{ctx.firing}/"


def inline_node_prefix(ctx: Any) -> str:
    """The step path the child's steps are shown under: ``<calling step>/`` (nested: ``a/b/``)."""
    emitter = getattr(getattr(ctx, "app", None), "emitter", None)
    # Only an inline child's own emitter names an outer path (read off the instance: a proxy emitter's
    # ``__getattr__`` answers any name with something that is not one).
    outer = vars(emitter).get("inline_node_prefix") if emitter is not None and hasattr(emitter, "__dict__") else None
    return f"{outer if isinstance(outer, str) else ''}{ctx.node_id}/"


def inline_depth(ctx: Any) -> int:
    """How many inline children deep the calling step ``ctx`` runs (0 = a step of a run of its own).

    An inline child has no run row, so a chain of calls counted by run rows alone never sees it; the
    Run Workflow depth limit adds this (``workflow.run_workflow.max_depth``)."""
    emitter = getattr(getattr(ctx, "app", None), "emitter", None)
    depth = vars(emitter).get("inline_depth") if emitter is not None and hasattr(emitter, "__dict__") else None
    return depth if isinstance(depth, int) else 0


class InlineChildEmitter:
    """The caller's emitter, seen from an inline child: step events renamed to the child's step path and
    namespaced dispatch, run-level events dropped, the stream's end kept for the caller."""

    def __init__(self, base: Any, *, node_prefix: str, namespace: str, depth: int = 1) -> None:
        self._base = base
        self.inline_node_prefix = node_prefix
        self._namespace = namespace
        #: How many inline children deep this child runs (read by :func:`inline_depth`).
        self.inline_depth = depth

    def _node(self, node_id: Any) -> Any:
        if not isinstance(node_id, str) or node_id.startswith(self.inline_node_prefix):
            return node_id
        return self.inline_node_prefix + node_id

    def _dispatch(self, dispatch_id: Any) -> Any:
        if not isinstance(dispatch_id, str) or dispatch_id.startswith(self._namespace):
            return dispatch_id
        return self._namespace + dispatch_id

    def _rewrite(self, payload: Any) -> Any:
        event = payload.get("event") if isinstance(payload, dict) else getattr(payload, "event", None)
        if event in _RUN_LEVEL_EVENTS:
            return None
        if isinstance(payload, dict):
            out = dict(payload)
            if "node_id" in out:
                out["node_id"] = self._node(out["node_id"])
            if "dispatch_id" in out:
                out["dispatch_id"] = self._dispatch(out["dispatch_id"])
            return out
        fields = getattr(type(payload), "model_fields", None)
        if not fields:
            return payload
        update: dict[str, Any] = {}
        if "node_id" in fields:
            update["node_id"] = self._node(payload.node_id)
        if "dispatch_id" in fields:
            update["dispatch_id"] = self._dispatch(payload.dispatch_id)
        return payload.model_copy(update=update) if update else payload

    async def send_data(self, payload: Any) -> None:
        payload = self._rewrite(payload)
        if payload is not None:
            await self._base.send_data(payload)

    async def send_end(self, *args: Any, **kwargs: Any) -> None:
        """The child ending is not the caller's stream ending."""

    def for_invocation(
        self, node_id: str, dispatch_id: str = "", item_index: int = 0, *, step: int | None = None, attempt: int = 1
    ) -> InlineChildEmitter:
        scope = getattr(self._base, "for_invocation", None)
        if scope is None:
            return self
        try:
            scoped = scope(self._node(node_id), self._dispatch(dispatch_id), item_index, step=step, attempt=attempt)
        except TypeError:
            scoped = scope(self._node(node_id), self._dispatch(dispatch_id), item_index)
        return InlineChildEmitter(
            scoped, node_prefix=self.inline_node_prefix, namespace=self._namespace, depth=self.inline_depth
        )

    def __getattr__(self, name: str) -> Any:
        return getattr(self._base, name)


class InlineChildCheckpointer:
    """Checkpoints in memory; outcomes of steps that must not run twice recorded under the CALLER's run.

    ``base`` is the caller's checkpointer. Recorded rows carry ``node_id = <step path><child step>`` and
    ``dispatch_id = <namespace><child dispatch>``, so nothing keyed by the caller's own step ids (its
    resume, its settled outputs, its step history) ever reads them as the caller's."""

    def __init__(
        self, base: Any, *, run_id: str, namespace: str, node_prefix: str, graph: Any, registry: Any
    ) -> None:
        self._base = base
        self._run_id = run_id
        self._namespace = namespace
        self._prefix = node_prefix
        self._graph = graph
        self._registry = registry
        # Only the latest checkpoint: nothing reads an inline child's history back (it never resumes — a re-run
        # of the calling step runs it again), and a kept history deep-copied every super-step of the child for
        # the whole call: ~150 MB at the peak of one 92-page research keyword (lane M1, 2026-11-17).
        self._memory = MemoryCheckpointer(keep_history=False)
        #: Keys of outcomes an earlier leg recorded for this call: ``None`` = unknown (ask the base each time).
        self.recorded: set[tuple[int, str, str, int, int]] | None = None

    async def load_recorded(self) -> None:
        """One read: which outcomes an earlier run of this call recorded (none on a first run)."""
        reader = getattr(self._base, "outcome_keys", None)
        if reader is None:
            return
        self.recorded = set(await reader(self._run_id, self._namespace))

    def _reruns_safely(self, node_id: str) -> bool:
        from matrx_graph.executor.scheduler import step_reruns_safely

        return step_reruns_safely(self._graph.nodes.get(node_id), self._registry)

    def _outward(self, outcome: NodeOutcome) -> NodeOutcome:
        return outcome.model_copy(update={
            "run_id": self._run_id,
            "node_id": self._prefix + outcome.node_id,
            "dispatch_id": self._namespace + outcome.dispatch_id,
        })

    def must_record(self, outcome: NodeOutcome) -> bool:
        """An outcome a re-run cannot rebuild: a step that is not safe to run again, or ANY step that sent work
        (a loop, a For each): its sends carry a fresh dispatch id per execution, so re-running it would orphan
        every recorded outcome downstream and run that work again (review C1, 2026-11-10)."""
        return bool(outcome.sends) or self._emits(outcome.node_id) or not self._reruns_safely(outcome.node_id)

    def _emits(self, node_id: str) -> bool:
        """A step whose only effect is a stream emission (Show on Screen): safe to run again for the DATA, but a
        re-run would show it twice — recorded, the re-run replays it silently (review M4)."""
        node = self._graph.nodes.get(node_id)
        try:
            spec = self._registry.get(node.spec_type).spec if node is not None else None
        except Exception:  # noqa: BLE001 — an unknown type reports itself when it runs
            return False
        return bool(getattr(spec, "emits_only", False))

    async def record_outcome(self, outcome: NodeOutcome) -> None:
        await self._memory.record_outcome(outcome)
        if self.must_record(outcome):
            await self._base.record_outcome(self._outward(outcome))

    async def get_outcome(
        self, run_id: str, step: int, node_id: str, attempt: int, dispatch_id: str = "", item_index: int = 0
    ) -> NodeOutcome | None:
        held = await self._memory.get_outcome(run_id, step, node_id, attempt, dispatch_id, item_index)
        if held is not None:
            return held
        key = (step, self._prefix + node_id, self._namespace + dispatch_id, item_index, attempt)
        if self.recorded is not None and key not in self.recorded:
            return None
        found = await self._base.get_outcome(
            run_id=self._run_id, step=step, node_id=key[1], attempt=attempt, dispatch_id=key[2], item_index=item_index
        )
        if found is None:
            return None
        return found.model_copy(update={"node_id": node_id, "dispatch_id": dispatch_id})

    async def save_checkpoint(self, checkpoint: Checkpoint) -> None:
        await self._memory.save_checkpoint(checkpoint)

    async def save_checkpoint_with_outcomes(self, checkpoint: Checkpoint, outcomes: list[NodeOutcome]) -> None:
        for outcome in outcomes:
            await self.record_outcome(outcome)
        await self._memory.save_checkpoint(checkpoint)

    async def save_checkpoint_chain(self, items: list[tuple[Checkpoint, list[NodeOutcome]]]) -> None:
        for checkpoint, outcomes in items:
            await self.save_checkpoint_with_outcomes(checkpoint, outcomes)

    async def load_checkpoint(self, checkpoint_id: str) -> Checkpoint | None:
        return await self._memory.load_checkpoint(checkpoint_id)

    async def latest_checkpoint(self, run_id: str) -> Checkpoint | None:
        return await self._memory.latest_checkpoint(run_id)

    async def list_checkpoints(self, run_id: str) -> list[Checkpoint]:
        return await self._memory.list_checkpoints(run_id)

    async def step_history(self, run_id: str) -> tuple[set[str], dict[str, dict[str, str]]]:
        return await self._memory.step_history(run_id)

    async def settled_outputs(self, run_id: str, node_ids: set[str], up_to_step: int | None = None) -> dict[str, Any]:
        return await self._memory.settled_outputs(run_id, node_ids, up_to_step)


def inline_refusal(graph: Any, registry: Any) -> str | None:
    """Why ``graph`` cannot run inside a step, or None: a step that may stop to WAIT (a question, a timer) needs
    a run of its own to wait in (review M1: refused before its first step, never after its side effects). A
    nested Run Workflow is judged when it runs (its own child decides)."""
    waiting: list[str] = []
    for node_id, node in graph.nodes.items():
        try:
            spec = registry.get(node.spec_type).spec
        except Exception:  # noqa: BLE001
            continue
        if getattr(spec, "can_interrupt", False) and spec.node_type != "subgraph.call":
            waiting.append(node_id)
    if not waiting:
        return None
    return (
        "it has steps that can stop and wait (" + ", ".join(sorted(waiting)) + "), which a workflow run inside a "
        "step cannot do. Set its runs_as to 'step' so it runs as its own run."
    )


#: The step path suffix of the outcome that pins WHICH workflow version a call runs inline (review I3).
_PIN_STEP = "~call"


async def inline_call_pin(checkpointer: Any, ctx: Any) -> tuple[dict[str, Any] | None, set[tuple[int, str, str, int, int]] | None]:
    """What an earlier leg of THIS calling-step invocation pinned (``record_inline_call_pin``) and the keys it
    recorded — one read (two when a pin exists). ``(None, keys)`` on a first run; keys ``None`` = the store
    cannot list them. A pinned call keeps its version and mode however the child is republished meanwhile."""
    reader = getattr(checkpointer, "outcome_keys", None)
    if reader is None:
        return None, None
    namespace = inline_namespace(ctx)
    keys = set(await reader(ctx.run_id, namespace))
    pin_node = inline_node_prefix(ctx) + _PIN_STEP
    for step, node_id, dispatch_id, item_index, attempt in keys:
        if node_id == pin_node and dispatch_id == namespace:
            found = await checkpointer.get_outcome(
                run_id=ctx.run_id, step=step, node_id=node_id, attempt=attempt, dispatch_id=dispatch_id,
                item_index=item_index,
            )
            if found is not None and isinstance(found.output, dict):
                return dict(found.output), keys
    return None, keys


async def record_inline_call_pin(checkpointer: Any, ctx: Any, pin: dict[str, Any]) -> None:
    """Record, before the child's first step, which workflow version this call runs inline (``pin``: the
    host's facts, e.g. definition id + version number), so a re-run of the calling step runs that same version
    inline even after the child was republished or its ``runs_as`` flipped (review I3)."""
    await checkpointer.record_outcome(NodeOutcome(
        run_id=ctx.run_id, step=0, node_id=inline_node_prefix(ctx) + _PIN_STEP, attempt=1,
        dispatch_id=inline_namespace(ctx), item_index=0, output=dict(pin),
    ))


async def run_inline_child(
    ctx: Any,
    graph: Any,
    *,
    checkpointer: Any,
    registry: Any,
    inputs: dict[str, Any] | None,
    app: Any = None,
    definition_id: str | None = None,
    definition_version_id: str | None = None,
    control_check: Any = None,
    surface_inputs: dict[str, Any] | None = None,
    input_provenance: dict[str, str] | None = None,
    sampled_outputs: dict[str, Any] | None = None,
    max_steps: int = 1000,
    recorded: set[tuple[int, str, str, int, int]] | None = None,
) -> Any:
    """Run ``graph`` inside the calling step ``ctx``: a nested Scheduler under the caller's run id.

    ``checkpointer`` is the caller's (durable) checkpointer, ``app`` the context the child runs as
    (default ``ctx.app``). Returns the nested scheduler's ``RunResult``; the host turns it into the
    step's answer (and refuses a child that paused: its checkpoints do not outlive this step)."""
    from matrx_graph.executor.scheduler import Scheduler

    namespace = inline_namespace(ctx)
    prefix = inline_node_prefix(ctx)
    store = InlineChildCheckpointer(
        checkpointer, run_id=ctx.run_id, namespace=namespace, node_prefix=prefix, graph=graph, registry=registry
    )
    if recorded is not None:
        store.recorded = set(recorded)
    else:
        await store.load_recorded()
    base_app = app if app is not None else ctx.app
    child_app = base_app.with_overrides(
        emitter=InlineChildEmitter(
            base_app.emitter, node_prefix=prefix, namespace=namespace, depth=inline_depth(ctx) + 1
        )
    )
    scheduler = Scheduler(
        graph=graph,
        checkpointer=store,
        app_context=child_app,
        registry=registry,
        definition_id=definition_id,
        control_check=control_check,
        # A first run of this call has nothing recorded: no outcome read before each step.
        fresh_history=store.recorded is not None and not store.recorded,
        definition_version_id=definition_version_id,
        surface_inputs=surface_inputs,
        input_provenance=input_provenance,
        sampled_outputs=sampled_outputs,
        invocation_namespace=namespace,
    )
    return await scheduler.run(
        run_id=ctx.run_id, thread_id=getattr(ctx, "thread_id", None) or ctx.run_id, inputs=inputs, max_steps=max_steps
    )


__all__ = [
    "RUNS_INLINE",
    "InlineChildCheckpointer",
    "InlineChildEmitter",
    "inline_call_pin",
    "inline_depth",
    "inline_refusal",
    "inline_namespace",
    "inline_node_prefix",
    "record_inline_call_pin",
    "run_inline_child",
    "runs_inline",
]
