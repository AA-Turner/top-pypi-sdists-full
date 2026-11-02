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
- ``client``       — the person's extension / desktop / browser executor.
- ``outside``      — a provider or MCP server.

Every engine but ``code`` is a plug-in the HOST registers (``register_engine``):
matrx-graph never imports the host. An Action whose engine is not registered refuses
loudly at call time, naming the engine.

A long-running engine returns :class:`ActionStarted` — a handle on the host's ONE
operations contract (the request id a client follows) — instead of the output. The
typed result of every call is therefore ``output_schema | ActionStarted``.
"""

from __future__ import annotations

from collections.abc import Awaitable, Callable
from contextvars import ContextVar
from typing import TYPE_CHECKING, Any, Literal

from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, model_validator

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
#: A person's or organization's explicit ``off`` wins over every authority (the host gate).
Authority = Literal["workflow", "person", "agent"]
AUTHORITIES: frozenset[str] = frozenset({"workflow", "person", "agent"})
#: The authority a door carries when its caller does not name one.
DOOR_AUTHORITY: dict[str, str] = {"step": "workflow", "api": "person", "mcp": "person", "tool": "agent"}
#: The authority that runs even where no host gate exists to read a person's ``off`` —
#: a step inside a standalone graph (the workflow carries the authority).
SELF_AUTHORIZING: frozenset[str] = frozenset({"workflow"})
#: Doors whose own dispatcher already resolved the apply policy for this exact call (the
#: directive dispatcher asks agent → surface → user, and the person may have clicked
#: Accept); the router does not ask twice.
SELF_RESOLVED_DOORS: frozenset[str] = frozenset({"directive"})
#: Kept for readers of the old name: the doors whose caller is not a self-authorizing one.
POLICY_DOORS: frozenset[str] = frozenset({"tool", "mcp"})

#: ``async (spec, app, input, *, door, authority) -> None`` — the host's apply policy: the
#: ONE resolution of the Action's registered rule, the caller's authority and the
#: person's / organization's explicit settings. Returns to let the call run; raises
#: ``ActionFailed`` (``needs_approval`` / ``apply_off``) to stop it.
ApplyGate = Callable[..., Awaitable[None]]
_GATE: list[ApplyGate] = []


def configure_apply_gate(gate: ApplyGate | None) -> None:
    """The host plugs in its apply-policy resolver (aidream: output_directives.policy)."""
    _GATE.clear()
    if gate is not None:
        _GATE.append(gate)


#: Doors whose own caller already holds the ONE dedupe for this call. The directive
#: dispatcher claims the directive's content key in the host ledger before it reaches
#: ``run_action``; a second claim here would be a second key for the same write.
SELF_LEDGERED_DOORS: frozenset[str] = frozenset({"directive"})

#: ``async (spec, app, input, *, door, idempotency_key, run) -> output | ActionStarted``
#: — the host's idempotency ledger. ``run()`` runs the engine once; the ledger claims the
#: door's key first and, on a repeat of the same key, returns the first call's output
#: instead of calling ``run`` again.
ActionLedger = Callable[..., Awaitable[BaseModel]]
_LEDGER: list[ActionLedger] = []


def configure_action_ledger(ledger: ActionLedger | None) -> None:
    """The host plugs in its ONE idempotency ledger (aidream: platform.matrx_action_ledger).

    Every gated Action (it writes or spends) called through any door but the directive
    door — which ledgers the directive's own content key itself — runs under it, keyed by
    the door's stable idempotency key, so a retried step, tool call or mcp call never
    writes twice. With no ledger configured the call runs undeduped (a standalone graph)."""
    _LEDGER.clear()
    if ledger is not None:
        _LEDGER.append(ledger)


#: Whether the LAST ``run_action`` in this context was answered from the idempotency
#: ledger (a repeat of the same key) instead of running. Set by ``run_action`` just before
#: it returns; every door reads it with :func:`last_run_replayed` and says so in its reply —
#: a replay is never silent.
_REPLAYED: ContextVar[bool] = ContextVar("action_last_run_replayed", default=False)

REPLAY_MESSAGE = (
    "This is the first call's result, returned again because the same idempotency key was "
    "sent; nothing ran a second time. To run it again on purpose, send a new key."
)


def last_run_replayed() -> bool:
    """True when the ``run_action`` that just returned in this context replayed a prior result."""
    return _REPLAYED.get()


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
    repeat of the same door key returns the first output and writes nothing. The return is an ``output_schema`` instance or an
    :class:`ActionStarted` handle; anything else is a defect of the engine and raises.
    """
    from matrx_graph.actions.spec import ActionFailed

    _REPLAYED.set(False)
    spec = await _resolve(action, registry, app)
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
            f"{spec.name} is for platform admins only; this caller is not one.",
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
    if door not in SELF_RESOLVED_DOORS and (spec.gated or spec.declared_apply_rule != "auto"):
        if _GATE:
            await _GATE[0](spec, app, data, door=door, authority=who)
        elif who not in SELF_AUTHORIZING:
            from matrx_graph.actions.spec import ActionFailed

            raise ActionFailed(
                "apply_off",
                f"{spec.name} writes or spends, and this process has no apply policy to ask.",
                error_type="refused",
            )
    replayed = False
    if spec.gated and idempotency_key and _LEDGER and door not in SELF_LEDGERED_DOORS:
        ran = False

        async def run_once() -> BaseModel:
            nonlocal ran
            ran = True
            return await runner(spec, app, data, idempotency_key=idempotency_key)

        out = await _LEDGER[0](
            spec, app, data, door=door, idempotency_key=idempotency_key, run=run_once
        )
        replayed = not ran
    else:
        out = await runner(spec, app, data, idempotency_key=idempotency_key)
    if not isinstance(out, (spec.output_schema, ActionStarted)):
        raise TypeError(
            f"Action {spec.name!r} (engine {spec.engine!r}) returned {type(out).__name__}; "
            f"its declared output is {spec.output_schema.__name__} or ActionStarted."
        )
    _REPLAYED.set(replayed)
    return out


async def _run_code(
    spec: ActionSpec, app: Any, data: BaseModel, *, idempotency_key: str | None = None
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
    return await spec.work(app, data, **kwargs)


register_engine("code", _run_code)


def dump_result(spec: ActionSpec, out: BaseModel) -> dict[str, Any]:
    """The result as a door hands it on as JSON: the output, or the started handle."""
    if isinstance(out, ActionStarted):
        return out.model_dump(mode="json")
    return spec.dump_output(out)


__all__ = [
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
    "REPLAY_MESSAGE",
    "last_run_replayed",
    "EngineRunner",
    "dump_result",
    "register_engine",
    "registered_engines",
    "run_action",
    "validate_engine",
]
