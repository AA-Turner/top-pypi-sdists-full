"""Engines — HOW an Action runs. ONE router (``run_action``) sends every call to its engine.

Arman, 2026-10-29: an Action is a unique name, a typed input, an execution ENGINE and a
typed output. Engines are how it runs, not different kinds of thing; every door (step,
tool, directive, mcp — and later button, schedule, API) calls :func:`run_action`, never
an engine directly.

The engine set is closed (``ENGINES``):

- ``code``         — the in-process work function ``async (app, input) -> output``
                     (``declare_action``). Registered here; the only engine this
                     package runs itself.
- ``record_write`` — a generated create/update/delete of one record.
- ``record_tree``  — a record with its children, in one transaction.
- ``workflow``     — a workflow definition run (every saved workflow is an Action).
- ``agent``        — an agent run (every typed agent is an Action; through its Mandate).
- ``client``       — the person's browser / extension / desktop runs it. The runner here
                     answers :class:`ActionOnClient` ("run this on the client") — the
                     typed hand-off a door returns; the client's one runner does the work.
- ``outside``      — a provider or MCP server.

Every engine but ``code`` and ``client`` is a plug-in the HOST registers (``register_engine``):
matrx-graph never imports the host. An Action whose engine is not registered refuses
loudly at call time, naming the engine.

A long-running engine returns :class:`ActionStarted` — a handle on the host's ONE
operations contract (the request id a client follows) — instead of the output. The
typed result of every call is therefore ``output_schema | ActionStarted | ActionQueued``.

An Action whose registered rule answered ``ask`` and whose ask router QUEUED the call for a
person returns :class:`ActionQueued` — a RESULT, never a failure: nothing ran, and the exact
change waits on the approval queue as ``approval_id``. A plain ``ask`` with nothing queued
stays a refusal (``ActionFailed("needs_approval")``).
"""

from __future__ import annotations

import logging
import uuid
from collections.abc import Awaitable, Callable, Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

from matrx_graph.actions import runs as _runs

_logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from matrx_graph.actions.registry import ActionRegistry
    from matrx_graph.actions.spec import ActionSpec

ActionEngine = Literal["code", "record_write", "record_tree", "workflow", "agent", "client", "outside"]
ENGINES: frozenset[str] = frozenset(
    {"code", "record_write", "record_tree", "workflow", "agent", "client", "outside"}
)
#: Engines that change stored records by their nature — the apply policy always gates them.
WRITING_ENGINES: frozenset[str] = frozenset({"record_write", "record_tree"})


#: The host's ONE operations contract (aidream ``services/runtime/reconnect.py``:
#: ``GET /runtime/operations/{request_id}`` identifies, ``…/rejoin`` follows live). A
#: started Action's paths are DERIVED from its request id with these, never typed by an
#: engine; aidream's ``test_action_started_follows_the_operations_contract`` pins them to
#: ``reconnect.rejoin_path_for``.
OPERATION_PATH = "/runtime/operations/{request_id}"
OPERATION_REJOIN_PATH = "/runtime/operations/{request_id}/rejoin"


class ActionStarted(BaseModel):
    """A long-running engine's answer: the work started; follow it here.

    ``request_id`` is the spine request id (``runtime.global_request``) of the
    operations contract. ``follow`` (status) and ``rejoin`` (live delivery) are that
    contract's paths for it — derived, so no engine can hand back a second route.
    ``link_kind``/``link_id`` point at the feature's own record (a workflow run, …) —
    the source of truth for the result.
    """

    model_config = ConfigDict(extra="forbid")

    status: Literal["started"] = "started"
    action: str
    request_id: UUID
    follow: str = Field(default="", description="GET this for the operation's status (derived).")
    rejoin: str = Field(default="", description="POST this to rejoin live delivery (derived).")
    link_kind: str | None = None
    link_id: str | None = None

    @model_validator(mode="after")
    def _derive_paths(self) -> ActionStarted:
        want = OPERATION_PATH.format(request_id=self.request_id)
        want_rejoin = OPERATION_REJOIN_PATH.format(request_id=self.request_id)
        if self.follow not in ("", want) or self.rejoin not in ("", want_rejoin):
            raise ValueError(
                f"ActionStarted paths are derived from the request id: follow={want!r}, "
                f"rejoin={want_rejoin!r} (got {self.follow!r}, {self.rejoin!r})."
            )
        self.follow, self.rejoin = want, want_rejoin
        return self


class ActionQueued(BaseModel):
    """The call was put in front of a person instead of running: NOTHING ran.

    Returned by ``run_action`` when the host's apply gate answered ``ask`` and its ask router
    queued the call (one approval-queue item, ``approval_id``). ``output`` is what a door
    hands its caller — the Action's own preview plus where the change waits (Google's
    ``awaiting_approval`` answer, for one). Every door answers it as a success: a step
    succeeds with it, the api door answers 202, a tool or mcp call returns it.
    """

    model_config = ConfigDict(extra="forbid")

    status: Literal["queued"] = "queued"
    action: str
    approval_id: str = Field(min_length=1)
    output: dict[str, Any] = Field(default_factory=dict)


class ActionOnClient(BaseModel):
    """A ``client``-engine Action's answer on the server: run it on the person's client.

    Nothing ran on the server. ``input`` is the call's validated input; the client's ONE
    runner (alchemy ``runSurfaceAction``, ``runs: "client"``) runs ``action`` by the same
    name in the browser, and answers with the Action's ``output_schema``. An agent reaches
    one the way directives do: as a directive in its answer, run on the person's press.
    """

    model_config = ConfigDict(extra="forbid")

    status: Literal["client"] = "client"
    action: str
    input: dict[str, Any] = Field(default_factory=dict)


#: ``async (spec, app, input, *, idempotency_key) -> output | ActionStarted``
EngineRunner = Callable[..., Awaitable[BaseModel]]

_ENGINES: dict[str, EngineRunner] = {}

#: WHO is calling carries the authority to run an Action automatically (Arman,
#: 2026-10-29: "the thing that calls the action tells the system if it is authorized to
#: automatically trigger it or not … When you call an action from a workflow, everything
#: carries the authority to always just do it"):
#:
#: - ``workflow`` — a workflow step: the workflow carries the authority; always ``auto``.
#: - ``person``   — a person clicking, an API call, an mcp call as the signed-in person: ``auto``.
#: - ``agent``    — an agent's tool call: its own config (``matrx_actions``) decides.
#: - ``None``     — a caller with no authority of its own: the Action's REGISTERED rule
#:                  (``ActionSpec.declared_apply_rule``) decides.
#:
#: - ``approved`` — a person's RECORDED approval of this exact call (an approval-queue item
#:                  they accepted is replayed): the ask has been answered, so the Action's
#:                  registered rule is not asked again.
#:
#: A person's or organization's explicit ``off`` wins over every authority (the host gate).
Authority = Literal["workflow", "person", "agent", "approved"]
AUTHORITIES: frozenset[str] = frozenset({"workflow", "person", "agent", "approved"})
#: The authority a door carries when its caller does not name one.
DOOR_AUTHORITY: dict[str, str] = {
    "step": "workflow",
    "api": "person",
    "mcp": "person",
    "tool": "agent",
    "binding": "agent",
    # The schedule door runs from an enabled schedule row, which IS the recorded approval
    # (no-unapproved-schedules): the registered rule is not asked again on every tick.
    "schedule": "approved",
    # The service door is one of our servers, admitted by the shared server secret, calling an
    # Action that DECLARED the door (its declaration is the standing approval of that call).
    "service": "approved",
    # The trigger door runs from a workflow.trigger row its bound actor created: a standing
    # automation, carrying the authority a workflow step carries (Triggers PLAN Rule 4). NOT
    # ``approved`` — no person approved THIS call — so the host gate still runs the Action's
    # registered rule resolver (an organization rule that asks queues the fire for a person) and
    # the person's own ``off`` still wins.
    "trigger": "workflow",
    # The visitor door runs from an embed token an organization admin issued for exactly this Action
    # on exact origins (its issue is the standing decision): authority ``workflow``, NOT ``approved`` —
    # the host gate still runs the Action's registered rule resolver (an organization rule that asks
    # queues the press for a person) and an explicit ``off`` still wins.
    "visitor": "workflow",
}
#: The authority that runs even where no host gate exists to read a person's ``off`` —
#: a step inside a standalone graph (the workflow carries the authority), and a call that
#: carries a person's RECORDED approval (an approved schedule's fire, an accepted queue item):
#: the ask was already answered, and with no gate there is no ``off`` to read.
SELF_AUTHORIZING: frozenset[str] = frozenset({"workflow", "approved"})
#: Doors whose own dispatcher already resolved the apply policy for this exact call (the
#: directive dispatcher asks agent → surface → user, and the person may have clicked
#: Accept); the router does not ask twice.
SELF_RESOLVED_DOORS: frozenset[str] = frozenset({"directive"})
#: Kept for readers of the old name: the doors whose caller is not a self-authorizing one.
POLICY_DOORS: frozenset[str] = frozenset({"tool", "mcp"})

#: ``async (spec, app, input, *, door, authority) -> ActionQueued | None`` — the host's apply
#: policy: the ONE resolution of the Action's registered rule, the caller's authority and the
#: person's / organization's explicit settings. Returns ``None`` to let the call run, an
#: :class:`ActionQueued` when it put the call in front of a person (the call does not run and
#: ``run_action`` returns it); raises ``ActionFailed`` (``needs_approval`` / ``apply_off``) to
#: refuse it.
ApplyGate = Callable[..., Awaitable["ActionQueued | None"]]
_GATE: list[ApplyGate] = []


def configure_apply_gate(gate: ApplyGate | None) -> None:
    """The host plugs in its apply-policy resolver (aidream: output_directives.policy)."""
    _GATE.clear()
    if gate is not None:
        _GATE.append(gate)


#: Doors whose own caller already holds the ONE dedupe for this call. The directive
#: dispatcher claims the directive's content key in the host ledger before it reaches
#: ``run_action``; a second claim here would be a second key for the same write. The
#: schedule door's run row (``sch_run``, one per fire, claim-token fenced) is its dedupe.
SELF_LEDGERED_DOORS: frozenset[str] = frozenset({"directive", "schedule"})

#: ``async (spec, app, input, *, door, idempotency_key, run) -> output | ActionStarted``
#: — the host's idempotency ledger. ``run()`` runs the engine once; the ledger claims the
#: door's key first and, on a repeat of the same key, returns the first call's output
#: instead of calling ``run`` again.
ActionLedger = Callable[..., Awaitable[BaseModel]]
_LEDGER: list[ActionLedger] = []
_DURABLE_LEDGER: list[ActionLedger] = []


def configure_action_ledger(
    ledger: ActionLedger | None, *, durable_ledger: ActionLedger | None = None
) -> None:
    """The host plugs in its ONE idempotency ledger (aidream: platform.matrx_action_ledger).

    Every gated Action (it writes or spends) called through any door but the directive
    door — which ledgers the directive's own content key itself — runs under it, keyed by
    the door's stable idempotency key, so a retried step, tool call or mcp call never
    writes twice. With no ledger configured the call runs undeduped (a standalone graph)."""
    _LEDGER.clear()
    _DURABLE_LEDGER.clear()
    if durable_ledger is not None:
        _DURABLE_LEDGER.append(durable_ledger)
    if ledger is not None:
        _LEDGER.append(ledger)


#: Whether the LAST ``run_action`` in this context was answered from the idempotency
#: ledger (a repeat of the same key) instead of running. Set by ``run_action`` just before
#: it returns; every door reads it with :func:`last_run_replayed` and says so in its reply —
#: a replay is never silent.
_REPLAYED: ContextVar[bool] = ContextVar("action_last_run_replayed", default=False)
#: The run id of the call that just returned (the OUTERMOST call's, since it finishes last), read by
#: the api door with :func:`last_run_id` so a client can name the run to ``run.undo``.
_LAST_RUN_ID: ContextVar[str | None] = ContextVar("action_last_run_id", default=None)


@dataclass(frozen=True)
class ActionCall:
    """WHO is calling the Action now: its door and the authority it carries. The router sets it
    around the engine, so the work learns its caller from the call itself (the tool door is an agent
    acting for the person, the api door is the person) instead of from which function was called."""

    action: str
    door: str
    authority: str | None
    #: The RUN this call belongs to. Minted once, by the OUTERMOST ``run_action``, and inherited by
    #: every Action that call runs inside itself, so one press or one tool call is one run however
    #: many Actions and rows it touches. The host says it to the database (every row version the
    #: run writes carries it), which is what lets a whole run be listed and undone as one change.
    run_id: str | None = None
    #: The outermost call's Action and door: what the person or agent actually asked for.
    run_action: str | None = None
    run_door: str | None = None


_CALL: ContextVar[ActionCall | None] = ContextVar("action_current_call", default=None)


def current_action_call() -> ActionCall | None:
    """The call the running Action's work belongs to; ``None`` outside ``run_action``."""
    return _CALL.get()


def current_action_run_id() -> str | None:
    """The run the running Action's work belongs to; ``None`` outside ``run_action``."""
    call = _CALL.get()
    return call.run_id if call else None


def _call_in_run(action: str, door: str, authority: str | None) -> ActionCall:
    """This call, placed in its run: the enclosing call's run, else a new one."""
    outer = _CALL.get()
    if outer is not None and outer.run_id:
        return ActionCall(
            action=action, door=door, authority=authority,
            run_id=outer.run_id, run_action=outer.run_action, run_door=outer.run_door,
        )
    return ActionCall(
        action=action, door=door, authority=authority,
        run_id=uuid.uuid4().hex, run_action=action, run_door=door,
    )

REPLAY_MESSAGE = (
    "This is the first call's result, returned again because the same idempotency key was "
    "sent; nothing ran a second time. To run it again on purpose, send a new key."
)


def last_run_id() -> str | None:
    """The run id of the ``run_action`` that just returned in this context (the outermost call's)."""
    return _LAST_RUN_ID.get()


def last_run_replayed() -> bool:
    """True when the ``run_action`` that just returned in this context replayed a prior result."""
    return _REPLAYED.get()


@dataclass
class ActionBodyWatch:
    """Whether a watched ``run_action`` reached its Action's BODY (the engine runner was called).
    False after a refusal the router raises before the body — engine not registered, schedule only,
    not runnable, admin only, no organization, apply policy off, durable claim unavailable, its input
    refused — and after a call the apply gate queued for a person."""

    started: bool = False


_BODY_WATCH: ContextVar[ActionBodyWatch | None] = ContextVar("action_body_watch", default=None)


@contextmanager
def watch_action_body() -> Iterator[ActionBodyWatch]:
    """``with watch_action_body() as watch: await run_action(...)`` — then ``watch.started`` says
    whether the Action's body ran (a failure after it is "ran and failed", before it "didn't start").
    A nested ``run_action`` inside the body only ever marks the same watch started."""
    watch = ActionBodyWatch()
    token = _BODY_WATCH.set(watch)
    try:
        yield watch
    finally:
        _BODY_WATCH.reset(token)


def register_engine(engine: str, runner: EngineRunner, *, overwrite: bool = False) -> None:
    """The host plugs an engine in. Re-registering the same runner is a no-op."""
    if engine not in ENGINES:
        raise ValueError(f"Unknown engine {engine!r}; the engines are {sorted(ENGINES)}.")
    existing = _ENGINES.get(engine)
    if existing is not None and existing is not runner and not overwrite:
        raise ValueError(f"Engine {engine!r} is already registered by {existing!r}.")
    _ENGINES[engine] = runner


def registered_engines() -> frozenset[str]:
    return frozenset(_ENGINES)


def validate_engine(name: str, engine: str) -> str:
    if engine not in ENGINES:
        raise ValueError(
            f"Action {name!r} names unknown engine {engine!r}; the engines are {sorted(ENGINES)}."
        )
    return engine


async def _resolve(action: str | ActionSpec, registry: ActionRegistry | None, app: Any) -> ActionSpec:
    if isinstance(action, str):
        from matrx_graph.actions.registry import default_action_registry

        return await (registry or default_action_registry()).resolve(action, app=app)
    return action


def caller_authority(door: str, authority: str | None) -> str | None:
    """The authority this call carries: the caller's own, else its door's."""
    if authority is not None and authority not in AUTHORITIES:
        raise ValueError(f"Unknown authority {authority!r}; the authorities are {sorted(AUTHORITIES)}.")
    return authority or DOOR_AUTHORITY.get(door)


async def run_action(
    action: str | ActionSpec,
    payload: BaseModel | dict[str, Any],
    *,
    app: Any,
    idempotency_key: str | None = None,
    door: str = "step",
    authority: str | None = None,
    registry: ActionRegistry | None = None,
) -> BaseModel:
    """Run an Action through its configured engine and host policy."""
    return await _run_action(
        action, payload, app=app, idempotency_key=idempotency_key,
        door=door, authority=authority, registry=registry,
    )


async def _run_action(
    action: str | ActionSpec,
    payload: BaseModel | dict[str, Any],
    *,
    app: Any,
    idempotency_key: str | None = None,
    door: str = "step",
    step_run_id: str | None = None,
    node_context: Any | None = None,
    receipt_only: bool = False,
    authority: str | None = None,
    registry: ActionRegistry | None = None,
) -> BaseModel:
    """THE one entry point: run an Action by name (or spec) on its engine.

    ``payload`` is validated against the Action's ``input_schema`` here, once, for every
    engine. ``name`` resolves through the registry's declared Actions and then its lazy
    sources (generated workflow / agent Actions). Unless the door already resolved the
    policy itself (``SELF_RESOLVED_DOORS``), an Action that is gated or whose registered
    rule is not ``auto`` asks the host's apply gate with the call's ``authority`` (the
    caller's, else its door's — ``DOOR_AUTHORITY``); with no gate configured only a
    self-authorizing caller (a workflow) runs it — anyone else is REFUSED, never
    run unasked. A gated Action then runs under the host's idempotency
    ledger (``configure_action_ledger``) on every door but the directive door, so a
    repeat of the same door key returns the first output and writes nothing. The return is an ``output_schema`` instance, an
    :class:`ActionStarted` handle, or :class:`ActionQueued` (the gate put the call in front of a
    person; nothing ran); anything else is a defect of the engine and raises.
    """
    from matrx_graph.actions.spec import ActionFailed

    _REPLAYED.set(False)
    watch = _BODY_WATCH.get()

    def body_starts() -> None:
        if watch is not None:
            watch.started = True

    spec = await _resolve(action, registry, app)
    if receipt_only and not spec.requires_action_claim:
        raise ActionFailed(
            "action_claim_unavailable", "This step has no durable Action receipt.",
            error_type="refused",
        )
    if spec.takes_node_context and (door != "step" or node_context is None):
        raise ActionFailed("node_context_required", "This action requires its actual workflow node context.", error_type="refused")
    who = caller_authority(door, authority)
    runner = _ENGINES.get(spec.engine)
    if runner is None:
        raise ActionFailed(
            "engine_not_registered",
            f"Action {spec.name!r} runs on engine {spec.engine!r}, and no runner for it is "
            f"registered in this process (registered: {sorted(_ENGINES)}).",
            error_type="refused",
            suggested_action="Run it from a process that has this engine, or pick another Action.",
            details={"engine": spec.engine},
        )
    if spec.schedule_only and door != "schedule":
        raise ActionFailed(
            "schedule_only",
            f"{spec.name} runs only from its schedule; it cannot be run from the {door} door.",
            error_type="refused",
            suggested_action="Use \"Run now\" on its schedule, which queues a scheduled run.",
            details={"door": door},
        )
    if spec.engine == "code" and spec.work is None:
        raise ActionFailed(
            "action_not_runnable",
            f"Action {spec.name!r} is a step-only node; only its workflow step door can run it.",
            error_type="refused",
            suggested_action="Use it as a step in a workflow, or call an Action that has a tool / api / mcp door.",
            details={"door": door},
        )
    data = (
        payload
        if isinstance(payload, spec.input_schema)
        else spec.input_schema.model_validate(
            payload.model_dump() if isinstance(payload, BaseModel) else payload
        )
    )
    if spec.admin_only and not bool(getattr(app, "is_admin", False)):
        # EVERY door, not only the step adapter: an admin-only Action (admin SQL, dev
        # tools) reached by a tool call, a directive in an agent's answer, or the mcp
        # door refuses a non-admin caller here, before any policy or engine runs.
        from matrx_graph.actions.spec import ActionFailed

        raise ActionFailed(
            "admin_only",
            f"Only a platform admin can run “{getattr(getattr(spec, 'node_spec', None), 'display_name', None) or spec.name}”.",
            error_type="refused",
            details={"door": door},
        )
    if spec.engine in WRITING_ENGINES and not getattr(app, "organization_id", None):
        # A record is always saved INTO an organization; the router refuses a write that
        # carries none, on every door, before any engine runs (the server never picks one).
        from matrx_graph.actions.spec import ActionFailed

        raise ActionFailed(
            "no_organization",
            f"{spec.name} saves a record, and this call carries no organization to save it in.",
            error_type="refused",
            details={"door": door},
        )
    asks = door not in SELF_RESOLVED_DOORS and (spec.gated or spec.declared_apply_rule != "auto")

    async def apply_gate() -> ActionQueued | None:
        # The apply gate, then the engine. A gate that QUEUED the call for a person hands
        # back ActionQueued: that is the call's result and the engine does not run.
        if asks:
            if _GATE:
                queued = await _GATE[0](spec, app, data, door=door, authority=who)
                if queued is not None:
                    if not isinstance(queued, ActionQueued):
                        raise TypeError(
                            f"The apply gate returned {type(queued).__name__} for {spec.name!r}; "
                            "it returns None (run) or ActionQueued (queued for a person)."
                        )
                    return queued
            elif who not in SELF_AUTHORIZING:
                from matrx_graph.actions.spec import ActionFailed

                raise ActionFailed(
                    "apply_off",
                    f"{spec.name} writes or spends, and this process has no apply policy to ask.",
                    error_type="refused",
                )
        return None

    async def gate_then_run() -> BaseModel:
        queued = await apply_gate()
        if queued is not None:
            return queued
        body_starts()
        return await runner(spec, app, data, idempotency_key=idempotency_key, **({"node_context": node_context} if spec.takes_node_context else {}))

    outer_call = _CALL.get()
    call = _call_in_run(spec.name, door, who)
    # THE RUN'S WAY BACK: this call collects what the Actions it runs inside itself would undo,
    # and hands its own Part to the call that ran it. The OUTERMOST call reports the whole run
    # to the host's recorder (``runs.configure_run_recorder``), which writes the one envelope.
    recorder = _runs.run_recorder() if outer_call is None or not outer_call.run_id else None
    mark: Any = None
    if recorder is not None:
        # Awaited BEFORE this call marks the context: a cancellation here leaves no mark behind
        # for the task's next run to mistake for an enclosing one.
        try:
            mark = await recorder.begin(spec, app, call.run_id or "")
        except Exception as exc:  # noqa: BLE001 - recording a run never stops the run; it says so
            _logger.warning("action run %s (%s): the recorder could not begin (%s: %s); this run is not recorded.",
                            call.run_id, spec.name, type(exc).__name__, exc)
            recorder = None
    call_token = _CALL.set(call)
    parts, parts_token = _runs.open_parts()
    out: Any = None
    replayed = False
    failure: BaseException | None = None
    try:
        replayed = False
        if spec.requires_action_claim:
            if (
                door != "step" or not step_run_id or not idempotency_key
                or not _GATE or not _DURABLE_LEDGER
            ):
                raise ActionFailed(
                    "action_claim_unavailable",
                    "This workflow step needs a durable Action claim before it can run.",
                    error_type="refused",
                )
            queued = await apply_gate()
            if queued is not None:
                raise ActionFailed(
                    "action_claim_unavailable",
                    "This workflow step cannot queue approval under a durable Action claim.",
                    error_type="refused",
                )
            dispatched = False

            async def run_claimed() -> BaseModel:
                nonlocal dispatched
                if receipt_only:
                    raise ActionFailed(
                        "action_claim_outcome_unknown", "The previous Action outcome could not be confirmed.",
                        error_type="refused",
                    )
                dispatched = True
                body_starts()
                return await runner(spec, app, data, idempotency_key=idempotency_key, **({"node_context": node_context} if spec.takes_node_context else {}))

            out = await _DURABLE_LEDGER[0](
                spec, app, data, door=door, idempotency_key=idempotency_key,
                step_run_id=step_run_id, run=run_claimed,
                **({"receipt_only": True} if receipt_only else {}),
            )
            replayed = not dispatched
        elif (
            spec.gated
            and idempotency_key
            and _LEDGER
            and door not in SELF_LEDGERED_DOORS
            and not getattr(spec, "owns_idempotency", False)
        ):
            # The gate runs INSIDE the ledger's claim: a retry of the same door key replays the
            # first answer — the output, or the ONE approval item it queued — and never asks
            # (or queues) twice. A refusal raises, which releases the claim (never ledgered).
            ran = False

            async def run_once() -> BaseModel:
                nonlocal ran
                ran = True
                return await gate_then_run()

            out = await _LEDGER[0](
                spec, app, data, door=door, idempotency_key=idempotency_key, run=run_once
            )
            replayed = not ran
        else:
            out = await gate_then_run()
    except BaseException as exc:
        failure = exc
        raise
    finally:
        _runs.close_parts(parts_token)
        # Worked out while this call is still current, so an inverse can name the run it takes back
        # (``current_action_run_id()``); then the caller's call is current again.
        if failure is not None:
            steps, reason = None, f"{spec.name} failed partway ({type(failure).__name__}); what it changed before failing stays."
        elif replayed:
            # A repeat of the same key wrote nothing now; the first call's run owns its change.
            steps, reason = [], None
        else:
            try:
                steps, reason = _runs.inverse_for(spec.name, data, out, parts)
            except Exception as exc:  # noqa: BLE001 - the write already happened: not undoable, never a failure
                steps, reason = None, f"The way to undo {spec.name} could not be worked out ({type(exc).__name__})."
        _CALL.reset(call_token)
        _runs.report_part(_runs.Part(action=spec.name, steps=steps, reason=reason))
        if recorder is not None:
            try:
                await recorder.finish(_runs.RunRecord(
                    run_id=call.run_id or "", action=spec.name, door=door, authority=who, app=app,
                    input=data, output=out if failure is None else None,
                    inverse=steps, not_undoable=[reason] if reason else [], mark=mark, error=failure,
                ))
            except Exception as exc:  # noqa: BLE001 - the run already happened; losing its record is said, never raised
                _logger.warning("action run %s (%s): the recorder could not record it (%s: %s).",
                                call.run_id, spec.name, type(exc).__name__, exc)
    if not isinstance(out, (spec.output_schema, ActionStarted, ActionQueued, ActionOnClient)):
        raise TypeError(
            f"Action {spec.name!r} (engine {spec.engine!r}) returned {type(out).__name__}; "
            f"its declared output is {spec.output_schema.__name__}, ActionStarted or ActionQueued."
        )
    _REPLAYED.set(replayed)
    _LAST_RUN_ID.set(call.run_id)
    return out


async def _run_code(
    spec: ActionSpec, app: Any, data: BaseModel, *, idempotency_key: str | None = None, node_context: Any | None = None
) -> BaseModel:
    """The ``code`` engine: the plain work function, in process."""
    if spec.work is None:
        from matrx_graph.actions.spec import ActionFailed

        raise ActionFailed(
            "action_not_runnable",
            f"Action {spec.name!r} has no plain work function — it is a step-only "
            "register_node; only its step door can run it.",
            error_type="refused",
        )
    kwargs: dict[str, Any] = {}
    if spec.takes_idempotency_key:
        kwargs["idempotency_key"] = idempotency_key
    if spec.takes_node_context:
        kwargs["node_context"] = node_context
    return await spec.work(app, data, **kwargs)


register_engine("code", _run_code)


async def _run_client(
    spec: ActionSpec, app: Any, data: BaseModel, *, idempotency_key: str | None = None
) -> BaseModel:
    """The ``client`` engine: nothing runs here — the answer says "run it on the client"."""
    return ActionOnClient(action=spec.name, input=data.model_dump(mode="json"))


register_engine("client", _run_client)


def dump_result(spec: ActionSpec, out: BaseModel) -> dict[str, Any]:
    """The result as a door hands it on as JSON: the output, the started handle, or — for a
    call queued for a person — its queued answer carrying ``awaiting_approval`` and the
    ``approval_id`` (never a bare success that hides that nothing ran)."""
    if isinstance(out, (ActionStarted, ActionOnClient)):
        return out.model_dump(mode="json")
    if isinstance(out, ActionQueued):
        return {**out.output, "awaiting_approval": True, "approval_id": out.approval_id}
    return spec.dump_output(out)


def restore_result(spec: ActionSpec, stored: dict[str, Any]) -> BaseModel:
    """A stored result (``store_result``) back as the typed one: the started handle, the
    queued answer, or the Action's output."""
    if stored.get("status") == "started" and "request_id" in stored:
        return ActionStarted.model_validate(stored)
    if stored.get("status") == "queued" and "approval_id" in stored and "output" in stored:
        return ActionQueued.model_validate(stored)
    if stored.get("status") == "client" and "action" in stored and set(stored) <= {"status", "action", "input"}:
        return ActionOnClient.model_validate(stored)
    return spec.output_schema.model_validate(stored)


def store_result(spec: ActionSpec, out: BaseModel) -> dict[str, Any]:
    """The result as a ledger stores it, so :func:`restore_result` hands back the same type."""
    if isinstance(out, ActionQueued):
        return out.model_dump(mode="json")
    return dump_result(spec, out)


__all__ = [
    "ActionCall",
    "current_action_call",
    "OPERATION_PATH",
    "OPERATION_REJOIN_PATH",
    "AUTHORITIES",
    "DOOR_AUTHORITY",
    "POLICY_DOORS",
    "SELF_AUTHORIZING",
    "SELF_RESOLVED_DOORS",
    "Authority",
    "caller_authority",
    "SELF_LEDGERED_DOORS",
    "ActionLedger",
    "configure_action_ledger",
    "configure_apply_gate",
    "ENGINES",
    "WRITING_ENGINES",
    "ActionEngine",
    "ActionStarted",
    "ActionQueued",
    "ActionOnClient",
    "REPLAY_MESSAGE",
    "last_run_replayed",
    "last_run_id",
    "ActionBodyWatch",
    "watch_action_body",
    "EngineRunner",
    "dump_result",
    "restore_result",
    "store_result",
    "register_engine",
    "registered_engines",
    "run_action",
    "validate_engine",
]
