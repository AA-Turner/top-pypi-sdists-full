"""The runtime host — executes a compiled workflow in-process.

A thin loop around two pure functions::

    state   = fold(facts)
    actions = next_actions(topology, state)
    for action in actions:
        facts += await execute(action)     # the only impure part

Everything that decides *what happens next* lives in
``dreadnode-workflow-core`` and is shared with the platform, so the two hosts
cannot disagree about control flow. This module owns only the *doing*: running
step bodies, calling agents, assigning ``seq``, and shipping facts.

Release 1 executes here, in the capability runtime, beside workers. Facts are
retried in memory until the platform acknowledges them, but a dead runtime still
marks its runs ``lost``; they do not resume. Durability is a separate, deferred
host that reuses this same scheduler.
"""

import asyncio
import contextlib
import inspect
import tempfile
import typing as t
from datetime import UTC, datetime
from pathlib import Path

from dreadnode_workflow_core import (
    Collect,
    CompleteRun,
    Fact,
    FailRun,
    MaterializeFanOut,
    NodeFailure,
    ReadyNode,
    RequestApproval,
    RunState,
    SkipNode,
    Topology,
    UnitKey,
    check_min_success,
    fold,
    next_actions,
)
from loguru import logger
from pydantic import BaseModel

from dreadnode.workflows.context import AgentResult
from dreadnode.workflows.workflow import StepDef, Workflow

__all__ = [
    "FactSink",
    "MemoryFactSink",
    "PlatformFactSink",
    "RunResult",
    "WorkflowHost",
    "WorkflowRunCancelled",
]

DEFAULT_MAX_TURNS = 10_000
"""Loop guard. The scheduler is a DAG advance, so it terminates by construction;
this only bounds a bug, and is deliberately far above any real workflow."""
DEFAULT_HEARTBEAT_INTERVAL = 10.0
DEFAULT_FACT_RETRY_INITIAL = 0.25
DEFAULT_FACT_RETRY_MAX = 5.0
DEFAULT_FACT_RETRY_TIMEOUT = 60.0
MAX_FACT_BATCH_SIZE = 500


class WorkflowRunCancelled(Exception):  # noqa: N818 - a signal, not an error
    """Raised inside a step body when the run has been cancelled."""


class FactDeliveryError(RuntimeError):
    """Raised when the platform cannot accept a host's ordered fact batch."""


class FactSink(t.Protocol):
    """Where facts go once produced.

    The runtime host retries transient failures in sequence and keeps its own
    authoritative copy in memory until the sink acknowledges the batch.
    """

    async def emit(self, facts: list[Fact]) -> None: ...


class MemoryFactSink:
    """Collects facts locally. The default when there is no platform to talk to."""

    def __init__(self) -> None:
        self.facts: list[Fact] = []

    async def emit(self, facts: list[Fact]) -> None:
        self.facts.extend(facts)


class PlatformFactSink:
    """Ships facts to the platform so the run page can render them.

    Batches are sent in ``seq`` order. The host retries the exact batch after a
    failure, and the platform's idempotent ``(run, seq)`` append makes a timeout
    after a successful write safe to redeliver.
    """

    def __init__(
        self,
        api: t.Any,
        org: str,
        workspace: str,
        run_id: str,
        execution_id: str,
    ) -> None:
        self.api = api
        self.org = org
        self.workspace = workspace
        self.run_id = run_id
        self.execution_id = execution_id
        self.shipped = 0
        self.failures = 0

    async def emit(self, facts: list[Fact]) -> None:
        payload = [
            {
                "seq": fact.seq,
                "kind": fact.kind,
                "unit_key": fact.unit_key,
                "attempt": fact.attempt,
                "payload": fact.payload,
                "occurred_at": fact.occurred_at.isoformat() if fact.occurred_at else None,
            }
            for fact in facts
        ]
        for offset in range(0, len(payload), MAX_FACT_BATCH_SIZE):
            chunk = payload[offset : offset + MAX_FACT_BATCH_SIZE]
            try:
                result = await asyncio.to_thread(
                    self.api.append_workflow_facts,
                    self.org,
                    self.workspace,
                    self.run_id,
                    chunk,
                    execution_id=self.execution_id,
                )
            except Exception:
                self.failures += 1
                raise
            self.shipped += len(chunk)
            if result.get("buffered"):
                logger.debug(
                    "platform is holding {} facts behind a gap | run={}",
                    result["buffered"],
                    self.run_id,
                )

    async def heartbeat(self) -> None:
        """Liveness, so a dead runtime's run is marked ``lost`` rather than
        displayed as running forever."""
        with contextlib.suppress(Exception):
            await asyncio.to_thread(
                self.api.heartbeat_workflow_run,
                self.org,
                self.workspace,
                self.run_id,
                execution_id=self.execution_id,
            )


class RunResult(t.NamedTuple):
    state: RunState
    facts: list[Fact]

    @property
    def status(self) -> str:
        return self.state.status

    @property
    def result(self) -> t.Any:
        return self.state.result


class _Ctx:
    """The handle a step body receives. Implements the ``Ctx`` protocol."""

    def __init__(
        self,
        host: "WorkflowHost",
        unit: UnitKey,
        step: StepDef,
    ) -> None:
        self._host = host
        self._unit = unit
        self._step = step

    @property
    def input(self) -> t.Any:
        return self._host.input

    @property
    def workspace(self) -> Path:
        return self._host.workspace

    def result(self, step: "StepDef | str") -> t.Any:
        key = step.key if isinstance(step, StepDef) else step
        return self._host.result_of(key)

    async def agent(
        self,
        name: str,
        prompt: str,
        *,
        model: str | None = None,
        max_steps: int | None = None,
        labels: dict[str, str] | None = None,
    ) -> AgentResult:
        return await self._host.run_agent(
            self._unit,
            name,
            prompt,
            model=model,
            max_steps=max_steps,
            labels=labels,
        )

    def log(self, message: str, **fields: t.Any) -> None:
        logger.info("workflow step | {} | {} | {}", self._unit, message, fields)
        self._host.append("node_log", unit=self._unit, message=message, fields=_jsonable(fields))

    def publish_runtime_event(self, kind: str, payload: dict[str, t.Any]) -> None:
        self._host.publish_runtime_event(kind, payload)


class _AgentResult:
    """Concrete ``AgentResult`` built from a ``turn.completed`` payload."""

    __slots__ = ("_payload", "output", "session_id", "tool_calls")

    def __init__(self, payload: dict[str, t.Any], session_id: str) -> None:
        self._payload = payload
        self.output: str = str(payload.get("response_text") or "").strip()
        raw_calls = payload.get("tool_calls")
        self.tool_calls: list[t.Any] = raw_calls if isinstance(raw_calls, list) else []
        self.session_id = session_id

    def parse(self, model: type[t.Any]) -> t.Any:
        return model.model_validate_json(self.output)


class WorkflowHost:
    """Executes one run of one workflow, in this process."""

    def __init__(
        self,
        workflow: Workflow,
        topology: Topology,
        *,
        client: t.Any = None,
        sink: FactSink | None = None,
        workspace: Path | None = None,
        capability: str | None = None,
        run_label: str = "",
        run_id: str | None = None,
        session_group_id: str | None = None,
        heartbeat_interval: float = DEFAULT_HEARTBEAT_INTERVAL,
        fact_retry_initial: float = DEFAULT_FACT_RETRY_INITIAL,
        fact_retry_max: float = DEFAULT_FACT_RETRY_MAX,
        fact_retry_timeout: float = DEFAULT_FACT_RETRY_TIMEOUT,
    ) -> None:
        self.workflow = workflow
        self.topology = topology
        self.client = client
        self.sink = sink or MemoryFactSink()
        self.capability = capability
        self.run_label = run_label
        self.run_id = run_id
        self.heartbeat_interval = heartbeat_interval
        self.fact_retry_initial = fact_retry_initial
        self.fact_retry_max = fact_retry_max
        self.fact_retry_timeout = fact_retry_timeout
        """Stamped onto every agent session, so the spans an agent emits can be
        filtered back to this run. The runtime never learns it any other way."""
        self.session_group_id = session_group_id
        """The run's session group. Every agent session joins it, which is what
        makes node-to-transcript click-through and per-run findings work."""

        self.facts: list[Fact] = []
        self.input: t.Any = None
        self._seq = 0
        self._pending: list[Fact] = []
        self._facts_available = asyncio.Event()
        self._workspace = workspace
        self._workspace_tmp: tempfile.TemporaryDirectory[str] | None = None
        self._event_types = _event_registry(workflow)
        self._deadline: float | None = None

    # ── Workspace ────────────────────────────────────────────────────────

    @property
    def workspace(self) -> Path:
        """A run-scoped directory shared across steps.

        Local to this process. A pipeline that passes filesystem paths between
        steps is therefore runtime-host-only until the shared workspace lands.
        """
        if self._workspace is None:
            self._workspace_tmp = tempfile.TemporaryDirectory(prefix="dn-workflow-")
            self._workspace = Path(self._workspace_tmp.name)
        return self._workspace

    # ── Facts ────────────────────────────────────────────────────────────

    def append(
        self,
        kind: str,
        *,
        unit: UnitKey | None = None,
        attempt: int = 1,
        **payload: t.Any,
    ) -> Fact:
        """Assign the next ``seq`` and record a fact.

        The host assigns ``seq`` because it is the only party that knows
        execution order. Callers must hold no assumptions about ordering across
        concurrent steps beyond what this method guarantees.
        """
        self._seq += 1
        fact = Fact(
            seq=self._seq,
            kind=kind,
            unit_key=str(unit) if unit is not None else None,
            attempt=attempt,
            payload=_jsonable(payload),
            occurred_at=datetime.now(UTC),
        )
        self.facts.append(fact)
        self._pending.append(fact)
        self._facts_available.set()
        return fact

    async def flush(self) -> None:
        """Ship the next ordered batch, retrying until it is acknowledged."""
        if not self._pending:
            return
        batch, self._pending = self._pending, []
        delay = self.fact_retry_initial
        deadline = asyncio.get_running_loop().time() + self.fact_retry_timeout
        try:
            while True:
                try:
                    await self.sink.emit(batch)
                except Exception as exc:
                    if _is_permanent_sink_error(exc):
                        self._pending = batch + self._pending
                        raise FactDeliveryError(
                            "platform rejected workflow facts permanently"
                        ) from exc
                    if asyncio.get_running_loop().time() >= deadline:
                        self._pending = batch + self._pending
                        raise FactDeliveryError(
                            "platform did not acknowledge workflow facts within "
                            f"{self.fact_retry_timeout}s"
                        ) from exc
                    logger.opt(exception=True).warning(
                        "workflow fact shipping failed; retrying in {}s | facts={}",
                        delay,
                        len(batch),
                    )
                    await asyncio.sleep(delay)
                    delay = min(
                        max(delay * 2, self.fact_retry_initial),
                        self.fact_retry_max,
                    )
                else:
                    return
        except asyncio.CancelledError:
            self._pending = batch + self._pending
            raise

    # ── The loop ─────────────────────────────────────────────────────────

    async def run(
        self, input_data: t.Any = None, *, max_turns: int = DEFAULT_MAX_TURNS
    ) -> RunResult:
        """Drive the workflow to a terminal state."""
        self.input = _coerce_input(self.workflow, input_data)
        if self.topology.config.timeout_sec is not None:
            self._deadline = asyncio.get_running_loop().time() + self.topology.config.timeout_sec
        self.append("run_started", input=_jsonable(self.input))
        heartbeat = getattr(self.sink, "heartbeat", None)
        heartbeat_task = (
            asyncio.create_task(self._heartbeat_loop(heartbeat)) if callable(heartbeat) else None
        )
        delivery_failed = False

        try:
            await self.flush()
            for _ in range(max_turns):
                if (
                    self._deadline is not None
                    and asyncio.get_running_loop().time() >= self._deadline
                ):
                    self.append(
                        "run_failed",
                        error=(f"workflow exceeded {self.topology.config.timeout_sec}s timeout"),
                    )
                    break
                state = fold(self.facts)
                if state.is_terminal():
                    break
                actions = next_actions(self.topology, state)
                if not actions:
                    break
                await self._execute_all(actions)
                await self.flush()
            else:
                self.append("run_failed", error=f"workflow did not converge in {max_turns} turns")
        except FactDeliveryError:
            delivery_failed = True
            raise
        finally:
            if heartbeat_task is not None:
                heartbeat_task.cancel()
                with contextlib.suppress(asyncio.CancelledError):
                    await heartbeat_task
            if not delivery_failed:
                await self.flush()
            self._deadline = None
            if self._workspace_tmp is not None:
                with contextlib.suppress(Exception):
                    self._workspace_tmp.cleanup()

        return RunResult(fold(self.facts), list(self.facts))

    async def _heartbeat_loop(self, heartbeat: t.Callable[[], t.Awaitable[None]]) -> None:
        while True:
            await heartbeat()
            await asyncio.sleep(self.heartbeat_interval)

    async def _execute_all(self, actions: list[t.Any]) -> None:
        """Run one scheduler turn.

        Bookkeeping actions apply first and in order; ``ReadyNode`` actions run
        concurrently, because the scheduler has already bounded them by
        ``max_concurrency``.
        """
        runnable: list[ReadyNode] = []
        for action in actions:
            if isinstance(action, ReadyNode):
                runnable.append(action)
            elif isinstance(action, MaterializeFanOut):
                self.append(
                    "fan_out_materialized",
                    unit=UnitKey(action.node_key),
                    node_key=action.node_key,
                    count=action.count,
                )
            elif isinstance(action, SkipNode):
                self.append("node_skipped", unit=action.unit, reason=action.reason)
            elif isinstance(action, RequestApproval):
                self.append(
                    "approval_requested",
                    unit=action.unit,
                    summary=action.summary,
                    payload=action.payload,
                )
            elif isinstance(action, CompleteRun):
                self.append("run_completed", result=_jsonable(action.result))
            elif isinstance(action, FailRun):
                self.append("run_failed", error=action.error)

        if runnable:
            execution = asyncio.gather(*(self._run_node(a) for a in runnable))
            execution.add_done_callback(lambda _: self._facts_available.set())
            try:
                while not execution.done():
                    self._facts_available.clear()
                    await self.flush()
                    if not execution.done():
                        await self._facts_available.wait()
                await execution
            finally:
                # A permanent delivery failure must stop the active bodies,
                # and cancellation must not leave orphan steps running.
                execution.cancel()
                await asyncio.gather(execution, return_exceptions=True)

    async def _run_node(self, action: ReadyNode) -> None:
        step = self.workflow.steps.get(action.unit.node_key)
        if step is None:
            self.append(
                "node_failed",
                unit=action.unit,
                failure_class="error",
                error=f"no step named {action.unit.node_key!r}",
            )
            return

        node = self.topology.node(action.unit.node_key)

        # A join's declared minimum is checked before the body runs, so nobody
        # ships a degraded result by accident.
        if node.consumes.collect:
            breach = check_min_success(
                self.topology,
                node.key,
                collected=len(action.input.get("collected") or []),
                failed=len(action.input.get("failed") or []),
            )
            if breach is not None:
                self.append("node_failed", unit=action.unit, failure_class="error", error=breach)
                self.append("run_failed", error=breach)
                return

        self.append("node_ready", unit=action.unit, input=_jsonable(action.input))
        max_attempts = max(1, int(node.config.effective_max_attempts))
        for attempt in range(1, max_attempts + 1):
            self.append("node_started", unit=action.unit, attempt=attempt)
            try:
                argument = self._build_argument(node, action)
                ctx = _Ctx(self, action.unit, step)
                coro = step.fn(ctx, argument)
                timeout = step.timeout_sec
                if self._deadline is not None:
                    remaining = max(0.0, self._deadline - asyncio.get_running_loop().time())
                    timeout = min(timeout, remaining) if timeout is not None else remaining
                emitted = await (asyncio.wait_for(coro, timeout) if timeout is not None else coro)
            except TimeoutError:
                error = (
                    f"step exceeded {step.timeout_sec}s"
                    if step.timeout_sec is not None
                    else (f"workflow exceeded {self.topology.config.timeout_sec}s timeout")
                )
                self.append(
                    "node_failed",
                    unit=action.unit,
                    attempt=attempt,
                    failure_class="timeout",
                    error=error,
                )
                if (
                    self._deadline is not None
                    and asyncio.get_running_loop().time() >= self._deadline
                ):
                    self.append("run_failed", error=error)
                    return
            except WorkflowRunCancelled:
                self.append(
                    "node_failed",
                    unit=action.unit,
                    attempt=attempt,
                    failure_class="cancelled",
                    error="cancelled",
                )
                return
            except Exception as exc:
                logger.opt(exception=True).warning(
                    "workflow step failed | unit={} attempt={}",
                    action.unit,
                    attempt,
                )
                self.append(
                    "node_failed",
                    unit=action.unit,
                    attempt=attempt,
                    failure_class="error",
                    error=f"{type(exc).__name__}: {exc}",
                )
            else:
                self._emit_output(action.unit, emitted, attempt=attempt)
                return

    def _emit_output(self, unit: UnitKey, emitted: t.Any, *, attempt: int = 1) -> None:
        """Turn a step's return value into ``event_emitted`` + ``node_output``."""
        events = _normalize_emitted(emitted)
        if not events:
            self.append("node_output", unit=unit, attempt=attempt, event_type="", data={})
            return

        for index, event in enumerate(events):
            self.append(
                "event_emitted",
                unit=unit,
                attempt=attempt,
                event_type=_event_name_of(event),
                data=_jsonable(event),
                index=index,
            )
        primary = events[0]
        self.append(
            "node_output",
            unit=unit,
            attempt=attempt,
            event_type=_event_name_of(primary),
            data=_jsonable(primary),
        )

    # ── Step input ───────────────────────────────────────────────────────

    def _build_argument(self, node: t.Any, action: ReadyNode) -> t.Any:
        """Reconstruct the typed object a step body expects.

        Facts carry JSON; step signatures want events. The event classes come
        from the authored module, which is why the host holds the ``Workflow``
        and not just the compiled topology.
        """
        if node.consumes.collect:
            ok = []
            for item in action.input.get("collected") or []:
                if "event_type" in item and "data" in item:
                    ok.append(self._rehydrate(item["event_type"], item["data"]))
                else:
                    # Backward-compatible with facts produced before event tags
                    # were retained in join inputs.
                    ok.append(self._rehydrate_any(node.consumes.events, item))
            failed = [
                NodeFailure(
                    node=item.get("node", ""),
                    ordinal=int(item.get("ordinal", 0)),
                    failure_class=item.get("failure_class", "error"),
                    error=item.get("error"),
                )
                for item in action.input.get("failed") or []
            ]
            return Collect(ok, failed)

        if node.kind == "entry" or "input" in action.input:
            start_type = self._event_types.get(node.consumes.events[0])
            if start_type is not None:
                return start_type(input=self.input)
            return _Start(self.input)

        return self._rehydrate(action.input.get("event_type"), action.input.get("event") or {})

    def _rehydrate(self, event_type: str | None, data: dict[str, t.Any]) -> t.Any:
        cls = self._event_types.get(event_type or "")
        if cls is None:
            return data
        try:
            return cls.model_validate(data)
        except Exception:
            logger.warning("could not rehydrate {} from stored payload", event_type)
            return data

    def _rehydrate_any(self, candidates: list[str], data: dict[str, t.Any]) -> t.Any:
        """Read legacy collected payloads that predate explicit event tags."""
        for name in candidates:
            cls = self._event_types.get(name)
            if cls is None:
                continue
            try:
                return cls.model_validate(data)
            except Exception:  # noqa: S112
                continue
        return data

    def result_of(self, node_key: str) -> t.Any:
        """The event emitted by the most recently completed run of ``node_key``.

        Deliberately "most recently completed" rather than "the" output — a DAG
        has one, bounded loops would have several, and defining it loosely now
        avoids a silent meaning change later.
        """
        state = fold(self.facts)
        completed = [
            n
            for n in state.nodes.values()
            if n.unit.node_key == node_key and n.status == "completed"
        ]
        if not completed:
            return None
        latest = max(completed, key=lambda n: n.last_fact_seq)
        return self._rehydrate(latest.output_event_type, latest.output or {})

    # ── Agents ───────────────────────────────────────────────────────────

    async def run_agent(
        self,
        unit: UnitKey,
        name: str,
        prompt: str,
        *,
        model: str | None = None,
        max_steps: int | None = None,
        labels: dict[str, str] | None = None,
    ) -> AgentResult:
        """Run one agent turn as a sub-unit of a step."""
        if self.client is None:
            raise RuntimeError("this workflow calls ctx.agent() but the host has no runtime client")

        session_labels: dict[str, list[str]] = {
            "workflow": [self.workflow.name],
            "workflow_node": [unit.node_key],
            # The full unit, because `workflow_node` cannot distinguish one
            # fan-out instance from another — five specialists all carry
            # `specialist`. The platform stamps items with whichever of these it
            # finds, so this is what makes item attribution exact rather than
            # per-step.
            "workflow_unit": [str(unit)],
        }
        if self.run_id:
            session_labels["workflow_run"] = [self.run_id]
        for key, value in (labels or {}).items():
            session_labels[key] = [value]

        session = await self.client.create_session(
            capability=_bare_capability(self.capability),
            agent=name,
            model=model,
            policy={"name": "headless", **({"max_steps": max_steps} if max_steps else {})},
            labels=session_labels,
            group_id=self.session_group_id,
        )
        session_id = str(getattr(session, "session_id", session))

        # Recorded at agent *start*, so a node that fails or times out mid-agent
        # still links to its partial transcript.
        self.append("agent_session_started", unit=unit, session_id=session_id, agent=name)

        payload = await self.client.run_turn(
            session_id=session_id, message=prompt, agent=name, model=model, reset=True
        )
        return t.cast("AgentResult", _AgentResult(payload or {}, session_id))

    def publish_runtime_event(self, kind: str, payload: dict[str, t.Any]) -> None:
        """Put a runtime-bus event on the wire for external reactors.

        Distinct from *returning* a workflow event, which advances the graph.
        """
        if self.client is None:
            return
        publish = getattr(self.client, "publish", None)
        if publish is None:
            return
        task = asyncio.create_task(publish(kind, payload))
        self._bus_tasks.add(task)
        task.add_done_callback(self._bus_tasks.discard)

    _bus_tasks: t.ClassVar[set[asyncio.Task[t.Any]]] = set()


# ── Helpers ──────────────────────────────────────────────────────────────


class _Start:
    """Fallback ``StartEvent`` stand-in when the real class cannot be resolved."""

    def __init__(self, value: t.Any) -> None:
        self.input = value


def _bare_capability(capability: str | None) -> str | None:
    """Drop the org prefix from a capability ref.

    The platform stores a definition's capability org-qualified
    (``dreadnode/source-code-analysis``), because that is how it is published.
    A runtime resolves what is *installed on it*, which is a flat namespace —
    so it only ever knows the bare name, and hands back a 409 for the qualified
    one. Normalizing here keeps the run from failing on every agent step.
    """
    if capability is None:
        return None
    return capability.rsplit("/", 1)[-1]


def _event_registry(workflow: Workflow) -> dict[str, type[BaseModel]]:
    """Map event-type name → class, from the authored step signatures."""
    registry: dict[str, type[BaseModel]] = {}
    for step in workflow.steps.values():
        try:
            hints = t.get_type_hints(step.fn)
        except Exception:  # noqa: S112 - compile already reported this
            continue
        for annotation in hints.values():
            for candidate in _unpack(annotation):
                if isinstance(candidate, type) and issubclass(candidate, BaseModel):
                    registry.setdefault(_type_name(candidate), candidate)
    return registry


def _unpack(annotation: t.Any) -> t.Iterator[t.Any]:
    yield annotation
    for arg in t.get_args(annotation):
        yield from _unpack(arg)


def _type_name(cls: type) -> str:
    metadata = getattr(cls, "__pydantic_generic_metadata__", None)
    if metadata and metadata.get("origin") is not None:
        args = metadata.get("args") or ()
        inner = args[0].__name__ if args and isinstance(args[0], type) else "Any"
        return f"{metadata['origin'].__name__}[{inner}]"
    return cls.__name__


def _event_name_of(event: t.Any) -> str:
    return _type_name(type(event)) if not isinstance(event, dict) else ""


def _normalize_emitted(emitted: t.Any) -> list[t.Any]:
    """A step may return one event, a list (fan-out), or a tuple (fork)."""
    if emitted is None:
        return []
    if isinstance(emitted, (list, tuple)):
        return list(emitted)
    return [emitted]


def _coerce_input(workflow: Workflow, value: t.Any) -> t.Any:
    if value is None:
        return workflow.input() if _constructible(workflow.input) else {}
    if isinstance(value, workflow.input):
        return value
    if isinstance(value, dict):
        return workflow.input.model_validate(value)
    return value


def _constructible(model: type) -> bool:
    try:
        inspect.signature(model).bind()
    except TypeError:
        return False
    return True


def _jsonable(value: t.Any) -> t.Any:
    """Everything crossing the fact boundary is JSON.

    This is one of the two compatibility constraints that cannot be retrofitted
    without breaking authors, so it is enforced at the boundary rather than
    trusted.
    """
    if isinstance(value, BaseModel):
        return value.model_dump(mode="json")
    if isinstance(value, dict):
        return {str(k): _jsonable(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_jsonable(v) for v in value]
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def _is_permanent_sink_error(error: Exception) -> bool:
    """Classify non-retryable 4xx responses without coupling to httpx."""
    current: BaseException | None = error
    while current is not None:
        response = getattr(current, "response", None)
        status_code = getattr(response, "status_code", None)
        if isinstance(status_code, int):
            return 400 <= status_code < 500 and status_code not in {408, 429}
        current = current.__cause__
    return False
