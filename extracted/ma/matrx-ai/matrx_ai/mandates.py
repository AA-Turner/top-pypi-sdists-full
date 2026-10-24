"""Agent mandates — the package-side seam.

An "Mandate" is a DB-managed, user-swappable pointer to the agent that runs
one pipeline step. The mandate TABLES, resolution precedence (system → org → user),
and admin UI all live in the host (aidream `services/mandates/`). matrx-ai
holds ONE injected resolver.

🚨 **THERE IS NO SEED FALLBACK. A mandated agent resolves, or the run REFUSES.**
(Arman's ruling, 2026-08-16.) Until then, a missing or failing resolver silently
ran the agent id frozen in the class body — hoping a constant written months ago
still names a valid, current agent, while the platform moved to fully dynamic
DB-driven selection. That is not a safety net: it is a paid run against an agent
nobody chose, invisible in the console, immune to every org/user binding. The
run now raises :class:`MandateResolutionUnavailable` instead.

Every deployment shape HAS an authority, so refusing costs nothing legitimate:
as a server matrx-ai reads the mandate through the ORM (the host's, or its own when
standalone); as a CLIENT it must be given a resolver that fetches the mandate from
the server over HTTP, exactly like ``ServerToolSource`` does for tools. "No
authority is reachable" is a deployment defect to fix, never a reason to run a
hardcoded agent.

Host side (aidream, once at startup)::

    from matrx_ai.mandates import MandateResolution, set_mandate_resolver
    set_mandate_resolver(my_resolver)   # async (mandate_key) -> MandateResolution

Package side (any agent_runner in this package)::

    class MyAgent(NamedAgent[...]):
        mandate_key = "podcast.script_educational"   # the DB decides which agent runs

    result = await run_mandated(MyAgent, inputs=...)

This started as a private helper inside ``agent_runners/podcast_generator``.
It is package-level because a second copy of an injection seam is how two
resolvers, two fallback rules, and two silent divergences get born — the exact
failure the Mandate system exists to end.
"""

from __future__ import annotations

import inspect
import json
from collections.abc import Awaitable, Callable, Mapping
from dataclasses import dataclass, field
from typing import Any, NoReturn, Protocol, runtime_checkable

from pydantic import BaseModel

from matrx_ai.agents import AgentRunResult
from matrx_ai.agents.named import AgentSource, NamedAgent, offer_view, to_template_value
from matrx_ai.orchestrator.mandate_carrier import HolderCarrier

MandateCompletion = Callable[
    [AgentRunResult, dict[str, Any], str | None],
    Awaitable[None],
]


@dataclass(frozen=True, slots=True)
class OfferedValueSpec:
    """One value a call site's Provision OFFERS to whatever holds the mandate.

    Mirrors the host's provision declaration so a consumer that can shape the
    call sees the DECLARED input side without a second query — the exact
    rationale ``output_kind`` rides this resolution (see below). ``kind`` is a
    registered content_ir kind slug or a generic scalar slug; ``lazy`` means
    the value ships as a reference until it is actually consumed.
    """

    name: str
    kind: str
    guaranteed: bool = True
    lazy: bool = False
    #: True = the value is a LIST whose every item is an instance of ``kind``
    #: (aidream ``mandates.provisions.OfferedValue.many``).
    many: bool = False
    #: D2 — one static example of what this value looks like, declared with the
    #: provision. An ILLUSTRATION for whoever is choosing where it should land,
    #: never a default and never a fallback: nothing reads it at run time.
    example: str = ""
    #: False = offered FOR MAPPING ONLY: with no bound consumption map (the
    #: default pin) an agent Holder never receives it by name — silently. A
    #: binding whose map names it receives it. Mirrors the host declaration's
    #: ``pass_by_name`` (aidream ``mandates.provisions.OfferedValue``).
    pass_by_name: bool = True


def default_pin_offer(
    offered: dict[str, Any], specs: tuple[OfferedValueSpec, ...]
) -> dict[str, Any]:
    """The site's offered values an agent Holder receives BY NAME on the default pin.

    Everything except the values the provision offers for mapping only
    (``pass_by_name=False``): those were added beside a message the site
    already composes, and the current Holder's payload must stay byte-identical.
    Not receiving them is a normal state — nothing is logged.
    """
    mapping_only = {spec.name for spec in specs if not spec.pass_by_name}
    if not mapping_only:
        return dict(offered)
    return {name: value for name, value in offered.items() if name not in mapping_only}


@dataclass(frozen=True, slots=True)
class MandateResolution:
    """Host resolution plus the post-run honesty callback for this exact pin.

    HOLDER NEUTRALITY (SPEC-workflow-ui-contract §6.2): ``holder_type``
    discriminates. ``"agent"`` — the historical shape: ``source`` names the
    agent record to run. ``"workflow"`` — the Holder is a workflow definition
    (``workflow_id``, always the DEFINITION id; optional version pin);
    ``source`` is None because there is no agent, and consumers that can only
    run an agent must refuse with that reason. A workflow-held mandate
    EXECUTES through the host's workflow-mandate runner (a durable child
    workflow run), reached from a workflow step via the
    ``workflow_mandate_runner`` host extension.
    """

    source: AgentSource | None = None
    holder_type: str = "agent"
    workflow_id: str | None = None
    workflow_version_id: str | None = None
    version_number: int | None = None
    config_overrides: dict[str, Any] | None = None
    variable_mapping: dict[str, Any] | None = None
    spill_variables: frozenset[str] = frozenset()
    complete: MandateCompletion | None = None
    #: The host's ONE consumption pipeline for a code call site that builds its
    #: own request (aidream ``consumption.run_variables_for_mandate``): the
    #: binding's consumption map, the provision's guaranteed values and the
    #: required-input gate, applied to the site's offered values. Returns the
    #: variables the Holder runs on, or raises in words. ``None`` = the host
    #: offers no pipeline, and the site's values pass by name.
    materialize: Callable[[dict[str, Any]], Awaitable[dict[str, Any]]] | None = None
    #: The same pipeline for a mandate whose provision declares MEDIA inputs (AT-FOLLOW, 2026-10-19): returns
    #: ``(variables, media_blocks)``. A held code call carries the blocks on :attr:`HeldCall.media_blocks` and the
    #: site attaches them to its turn, instead of the pipeline refusing media this call site "has no turn" for.
    #: ``None`` = the mandate declares no media (``materialize`` keeps refusing a media route, never dropping it).
    materialize_media: Callable[[dict[str, Any]], Awaitable[tuple[dict[str, Any], list[dict[str, Any]]]]] | None = None
    #: WORKFLOW PARITY for code calls: the host's runner for THIS workflow
    #: resolution — ``(supplied, *, correlation_key, stream) -> answer dict``
    #: (``matrx_ai.mandate_workflow_holder``). Set only on a workflow Holder;
    #: ``None`` there means the host cannot run it, and the code call refuses.
    run_workflow: Callable[..., Awaitable[dict[str, Any]]] | None = None
    # THE INPUT SIDE, mirroring output_kind: the provision this mandate's call
    # site declares (all values available at the call site) travels WITH the
    # resolution, so a consumer never re-queries — or disagrees about — what
    # the DATABASE says this job is offered. Empty when the mandate declares
    # no provision (the pre-provision contract path).
    provision_key: str | None = None
    offered_values: tuple[OfferedValueSpec, ...] = ()
    # The binding's consumption map (which offered values the bound Holder
    # consumes, and on which channel). None = no map: legacy variable flow.
    consumption_map: dict[str, Any] | None = None
    # The kind slug this JOB is declared to answer in (``agent.mandate
    # .output_kind``). It travels WITH the resolution because a consumer that
    # can shape the call — a workflow's ``ai.agent.produce`` step — must be
    # able to see what the DATABASE says this job produces without a second
    # query and a second chance to disagree. Generic slugs (``text`` / ``json``
    # / …) mean "free-form": see ``matrx_ai.kinds.is_bindable_kind``.
    output_kind: str | None = None
    #: The host's run-history stamp for THIS resolution (aidream
    #: ``mandates.service.mandate_run_stamp``: the level whose choice ran, the
    #: Holder, any output warning). A held code call carries it on the request
    #: under ``metadata["mandate_resolution"]`` so the run's history can say
    #: whose choice ran. ``None`` = the host offers none.
    run_stamp: dict[str, Any] | None = None


LegacyMandateResolution = tuple[AgentSource, dict[str, Any] | None]
MandateResolver = Callable[[str], Awaitable[MandateResolution | LegacyMandateResolution]]

_MANDATE_RESOLVER: MandateResolver | None = None


class MandateResolutionUnavailable(RuntimeError):
    """A mandated consumer could not learn WHICH agent to run, so it refused.

    Raised instead of running a hardcoded seed. Two causes, both deployment
    defects with the same fix — give this process an authority: no resolver
    was installed, or the installed resolver failed.

    ``consumer`` is whatever named the mandate: a ``NamedAgent`` subclass, or a
    workflow step (``ai.agent.start:<node id>``).
    """

    def __init__(self, mandate_key: str, consumer: str, reason: str) -> None:
        super().__init__(
            f"Mandate {mandate_key!r} ({consumer}) could not be resolved: {reason}. "
            f"REFUSING to run — a mandated agent never falls back to an id frozen in code. "
            f"Install a mandate resolver for this process (ORM-backed when it owns a "
            f"database, HTTP-backed when it runs as a client)."
        )
        self.mandate_key = mandate_key
        self.consumer = consumer
        self.reason = reason


def set_mandate_resolver(resolver: MandateResolver) -> None:
    """Install the host's Mandate resolver. Called once at host startup."""
    global _MANDATE_RESOLVER
    _MANDATE_RESOLVER = resolver


def get_mandate_resolver() -> MandateResolver | None:
    return _MANDATE_RESOLVER


# ---------------------------------------------------------------------------
# THE MANDATE RUNNER PORT (runner plan 25, step 2)
# ---------------------------------------------------------------------------
#
# One module in the host runs every mandate (aidream ``services/mandate_runner``).
# matrx-ai cannot import it, so it declares the ONE structural port the host
# installs (``set_mandate_runner``), plus the value types every caller hands it.
# Graph nodes, NamedAgent, evaluators, ``memory/llm_adapter`` and
# ``agent_runners/*`` move onto this port step by step; the resolver seam above
# and its closure bag are deleted once they have.


@dataclass(frozen=True, slots=True)
class Principal:
    """Who a mandate runs for: explicit at every verb, never read from ambient state.

    ``watching`` is set only by the request boundary for that one run (AI Watch)
    and is never inherited: :meth:`child` gives fan-out, batch and child runs the
    same identity with ``watching=False``.
    """

    user_id: str | None
    org_id: str
    watching: bool = False

    def child(self) -> Principal:
        return Principal(user_id=self.user_id, org_id=self.org_id, watching=False)


@dataclass(frozen=True, slots=True)
class HolderRef:
    """A run-scope Holder override (the try door's picked candidate, a test holder)."""

    type: str  # "agent" | "workflow"
    id: str
    version_id: str | None = None
    #: The picked Holder's run-scope config (the try door's candidate config); ``None`` = the Holder's own.
    config_overrides: Mapping[str, Any] | None = None
    #: The rung whose choice this pick is, for the run record (the try door's candidate provenance:
    #: ``current`` / ``mandate-pinned`` / ``latest`` / ``agent`` / ``version``). ``None`` = ``run``.
    rung: str | None = None


@dataclass(frozen=True, slots=True)
class RunOptions:
    """Per-run options. ``door`` is a label for the record, never a code path."""

    door: str
    user_input: str | None = None
    holder: HolderRef | None = None
    correlation_key: str | None = None
    emit: Any = None
    dry_run: bool = False
    #: A raw-request site's own name for itself (the Holder stamp's ``consumer``, refusal sentences).
    consumer: str | None = None
    #: A raw-request site's request metadata (``source_app`` / ``source_feature`` / its own ids),
    #: merged UNDER the Holder stamp exactly as ``hold_code_call(metadata=)`` always did.
    metadata: Mapping[str, Any] | None = None
    #: Output keys THIS call needs beside the mandate contract's own (the honesty core refuses an answer
    #: missing one). ``None`` = the contract's keys only.
    required_keys: tuple[str, ...] | None = None
    #: A cap on an agent Holder's tool rounds for THIS run (``None`` = the agent's own ceiling).
    max_iterations: int | None = None
    #: A CHAT START (runner plan 25 step 10): the host's chat-start request (aidream ``AgentStartRequest``) this run
    #: opens a conversation with. ``prepare()`` resolves the Holder, computes the offer under the compute rule and
    #: places the bound values ON this request (mutated in place); ``run()`` also runs the chat on the ambient stream
    #: and records it. ``holder`` (an agent) is the run-scope pick — a person's own choice of agent.
    start: Any = None
    #: An AGENT Holder prepared for a door that owns its transport (runner plan 25 step 12):
    #: ``"door"`` — ``prepare()`` resolves the Holder (or takes ``resolution``), computes the offer and builds the
    #: agent, its turn and the provider schema (``Prepared.agent``); the door sends it (``agent_call``, a provider
    #: batch body) and ``finish()`` records the run. ``"landed"`` — the answer already exists (a batch item that
    #: finished in another process): ``prepare()`` resolves the Holder only and ``finish()`` runs the honesty core
    #: (artifact, required keys, exemplar) and records it. ``None`` = a raw-request held call.
    door_transport: str | None = None
    #: A Holder resolution this door already holds (``resolve()`` answered it, e.g. ``mandate_call``'s gated
    #: resolution): ``prepare(door_transport=...)`` places on it instead of resolving again.
    resolution: Any = None


# ── THE OFFER (runner plan 25 §3) ────────────────────────────────────────────
#
# Defined here, beside the port, because package code builds offers too (a graph node,
# an evaluator, a NamedAgent call); the host runner re-exports these unchanged — one
# definition of each.

#: A builder takes the run's scope (who / mandate / the values in hand) and returns the value,
#: sync or async. ``None`` means absent.
Builder = Callable[[Any], Any]


@dataclass(frozen=True, slots=True)
class Offered:
    """One offered value: a builder that runs only when the compute rule names it."""

    build: Builder
    #: ``given()``: the value is already held — zero cost, nothing to compute.
    in_hand: bool = False
    #: A plain value a not-yet-migrated caller passed (``eager_legacy``).
    legacy: bool = False


def given(value: Any, *, legacy: bool = False) -> Offered:
    """A value the call site already holds (computing it cost nothing extra)."""
    return Offered(build=lambda _scope: value, in_hand=True, legacy=legacy)


def build(fn: Builder) -> Offered:
    """A value computed only when the binding reads it (or the run is watched)."""
    return Offered(build=fn)


async def run_offered(offered: Offered, scope: Any = None) -> Any:
    built = offered.build(scope)
    return await built if inspect.isawaitable(built) else built


@dataclass(frozen=True, slots=True)
class NamedCall:
    """The typed ``NamedAgent`` call an :meth:`Offer.from_inputs` carries to the runner."""

    agent_cls: type[NamedAgent]
    #: The run's keyword arguments exactly as the call site wrote them (``inputs``, ``label``,
    #: ``user_input``, ``config_overrides``, ``request_metadata``, ``suppress_stream``, …).
    kwargs: dict[str, Any]
    #: Values held BESIDE the typed ``Inputs``, declared for mapping only (``mapped_offer``).
    offered: dict[str, Any] | None = None
    #: Media-kind offered values (durable references), the funnel's media channel.
    offered_media: dict[str, Any] | None = None
    #: A class that overrides ``run`` passes its bound base implementation here.
    runner: Callable[..., Awaitable[AgentRunResult]] | None = None


class Offer(dict):
    """What a caller offers a mandate: offered value name -> :class:`Offered`.

    A plain mapping is accepted by every verb too (each plain value then counts as eager
    legacy). :meth:`from_inputs` builds the offer of a typed ``NamedAgent`` call: its
    ``Inputs`` in the call site's vocabulary (``offer_view``), each value ``given`` — the
    call site holds it — plus the call itself, which the runner's NamedAgent engine runs.
    """

    named: NamedCall | None

    def __init__(self, values: Mapping[str, Any] | None = None, *, named: NamedCall | None = None) -> None:
        super().__init__(values or {})
        self.named = named

    @classmethod
    def given_values(cls, values: Mapping[str, Any] | None) -> Offer:
        """Every value in hand: ``{name: given(value)}`` (an ``Offered`` passes through)."""
        return cls({n: v if isinstance(v, Offered) else given(v) for n, v in dict(values or {}).items()})

    @classmethod
    def from_inputs(
        cls,
        agent_cls: type[NamedAgent],
        inputs: Any = None,
        *,
        offered: Mapping[str, Any] | None = None,
        offered_media: Mapping[str, Any] | None = None,
        runner: Callable[..., Awaitable[AgentRunResult]] | None = None,
        **run_kwargs: Any,
    ) -> Offer:
        kwargs = dict(run_kwargs)
        if inputs is not None:
            kwargs["inputs"] = inputs
        named = NamedCall(
            agent_cls=agent_cls,
            kwargs=kwargs,
            offered=dict(offered) if offered else None,
            offered_media=dict(offered_media) if offered_media else None,
            runner=runner,
        )
        view = _offer_view(agent_cls, kwargs)
        values = {**view, **dict(offered or {}), **dict(offered_media or {})}
        return cls({name: given(value) for name, value in values.items()}, named=named)


def carried_principal(user_id: str | None = None, org_id: str | None = None) -> Principal:
    """The principal the CARRIED request context names — read, never rebuilt (explicit ids win).

    The ambient context fills only what belongs to the SAME party: an explicit person takes the
    ambient organization only when the ambient context is that person's (another party's ambient
    organization is never paired with them — review 46 F7); an explicit organization takes the
    ambient person only when the ambient context is in that organization.

    No person and no organization anywhere is REFUSED (``MandateRefused`` code ``no_identity``,
    recorded): a run with no identity never silently becomes a system run. A system job declares
    itself with :func:`system_principal` (plan §0 law 8). A person with no organization is refused
    the same way (``no_organization``) — never answered with the system organization."""
    if not (user_id and org_id):
        try:
            from matrx_connect.context.app_context import try_get_app_context

            app = try_get_app_context()
        except Exception:  # noqa: BLE001 — no context machinery = no carried context
            app = None
        if app is not None:
            ambient_user = str(getattr(app, "user_id", None) or "") or None
            ambient_org = str(getattr(app, "organization_id", None) or "") or None
            if user_id and org_id is None:
                if ambient_user == str(user_id):
                    org_id = ambient_org
            elif org_id and user_id is None:
                if ambient_org == str(org_id):
                    user_id = ambient_user
            elif not user_id and not org_id:
                user_id, org_id = ambient_user, ambient_org
    if org_id:
        return Principal(user_id=str(user_id) if user_id else None, org_id=str(org_id))
    if user_id:
        raise _recorded_identity_refusal(MandateRefused(
            "<principal>",
            code="no_organization",
            sentence=(
                f"the carried request names person {user_id} and no organization of theirs — a mandate run "
                "is never org-less, never borrows another party's organization and never borrows the "
                "system organization for a person"
            ),
        ))
    raise _recorded_identity_refusal(MandateRefused(
        "<principal>",
        code="no_identity",
        sentence=(
            "this run carries no person and no organization — a run with no identity is never "
            "filed as a system run; carry the request context, or declare a system job with "
            "system_principal()"
        ),
    ))


def _recorded_identity_refusal(exc: MandateRefused) -> MandateRefused:
    """Law 6 for a refusal raised before any verb: captured (``mandate_refused``) once, then raised.
    ``carried_principal`` is synchronous, so the capture is scheduled on the running loop; with no
    loop the refusal is logged at ERROR. Never masks the refusal."""
    import logging

    log = logging.getLogger("matrx_ai.mandates")
    log.error("[mandates] refused before the run: %s (%s)", exc.sentence, exc.code)
    try:
        import asyncio

        from matrx_utils import capture_error, detached_task

        asyncio.get_running_loop()
        detached_task(
            capture_error(exc, kind="mandate_refused", context={"mandate_key": exc.mandate_key, "code": exc.code}),
            name="mandate-identity-refusal-capture",
        )
        exc.recorded = True  # type: ignore[attr-defined]
    except Exception as capture_exc:  # noqa: BLE001 — no loop / no capture: the ERROR log above stands
        log.error("[mandates] could not schedule the refusal capture: %s", capture_exc)
    return exc


def system_principal() -> Principal:
    """The runner's ``SYSTEM`` principal (Matrx System organization + account): system jobs only — no user,
    no user organization, no user billing (plan §0 law 8)."""
    system = getattr(get_mandate_runner(), "system", None)
    if not isinstance(system, Principal):
        raise MandateRunnerUnavailable("the installed mandate runner names no SYSTEM principal")
    return system


class MandateRefused(MandateResolutionUnavailable):
    """A mandate run that was refused: typed, recorded, then raised (never an empty result).

    Subclasses :class:`MandateResolutionUnavailable` so every existing catch site
    keeps catching it while callers move onto the runner.
    """

    def __init__(
        self,
        mandate_key: str,
        *,
        code: str,
        sentence: str,
        missing: tuple[str, ...] = (),
        door: str = "",
    ) -> None:
        super().__init__(mandate_key, door or "mandate_runner", sentence)
        self.code = code
        self.sentence = sentence
        self.missing = tuple(missing)
        self.door = door


class MandateRunnerUnavailable(RuntimeError):
    """No mandate runner is installed in this process — a deployment defect, never a fallback."""


@runtime_checkable
class MandateRunnerPort(Protocol):
    """The four verbs the host's runner serves to package code."""

    async def run(self, key: str, offer: Mapping[str, Any] | None, *, who: Principal, opts: RunOptions) -> Any: ...

    async def prepare(self, key: str, offer: Mapping[str, Any] | None, *, who: Principal, opts: RunOptions) -> Any: ...

    async def finish(self, prepared: Any, result: Any) -> Any: ...

    async def resolve(self, key: str, *, who: Principal, holder: HolderRef | None = None) -> Any: ...


_MANDATE_RUNNER: MandateRunnerPort | None = None


def set_mandate_runner(runner: MandateRunnerPort | None) -> None:
    """Install the host's mandate runner. Called once at host startup."""
    global _MANDATE_RUNNER
    if runner is not None and not isinstance(runner, MandateRunnerPort):
        raise TypeError(f"{runner!r} does not serve run / prepare / finish / resolve")
    _MANDATE_RUNNER = runner


def get_mandate_runner() -> MandateRunnerPort:
    """The installed runner, or a loud refusal naming the missing install."""
    if _MANDATE_RUNNER is None:
        raise MandateRunnerUnavailable(
            "No mandate runner is installed in this process. The host installs one at startup "
            "(aidream: services/mandates/runner_host.install_mandate_runner)."
        )
    return _MANDATE_RUNNER


async def _report_resolution_failure(
    *,
    mandate_key: str,
    consumer: str,
    exc: BaseException,
) -> None:
    from matrx_utils import vcprint

    message = (
        f"[mandates] resolver failed for {mandate_key!r} ({consumer}): "
        f"{type(exc).__name__}: {exc} — REFUSING the run (no seed fallback)"
    )
    vcprint(message, color="red")
    try:
        from matrx_ai._ext import get_ext

        record_error = get_ext("record_error")
    except Exception as capture_exc:
        vcprint(
            f"[mandates] structured resolution-failure capture unavailable for "
            f"{mandate_key!r}: {capture_exc!r}",
            color="red",
        )
        return

    try:
        pending = record_error(
            exc,
            kind="mandate_resolution_failed",
            error_type="mandate_resolution_failed",
            error_text=message,
            payload={
                "mandate_key": mandate_key,
                "consumer": consumer,
                "effect": "run REFUSED; no agent ran and nothing was charged",
            },
            route="matrx_ai.mandates.run_mandated",
        )
        if inspect.isawaitable(pending):
            await pending
    except Exception as capture_exc:  # capture must never fail the paid run
        vcprint(
            f"[mandates] structured resolution-failure capture FAILED for "
            f"{mandate_key!r}: {capture_exc!r}",
            color="red",
        )


def _coerce_inputs(agent_cls: type[NamedAgent], kwargs: dict[str, Any]) -> BaseModel | None:
    """The run's ``inputs`` as the class's own typed model, or None."""
    inputs = kwargs.get("inputs")
    if inputs is None:
        return None
    if isinstance(inputs, agent_cls.Inputs):
        return inputs
    if isinstance(inputs, BaseModel):
        return agent_cls.Inputs.model_validate(inputs.model_dump())
    if isinstance(inputs, dict):
        return agent_cls.Inputs.model_validate(inputs)
    return None


def _offer_view(agent_cls: type[NamedAgent], kwargs: dict[str, Any]) -> dict[str, Any]:
    """The CALL SITE's vocabulary for this run — see :func:`matrx_ai.agents.named.offer_view`.

    NOT the Holder's variables (already renamed through ``variable_map``/``prepare_variables``). An offer check reads the
    names the Provision was declared in.
    """
    inputs_obj = _coerce_inputs(agent_cls, kwargs)
    if inputs_obj is None:
        return {}
    return offer_view(agent_cls, inputs_obj)


def _capture_user_input(value: Any) -> str | None:
    if value is None or isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, default=str)


async def resolve_mandate_by_key(
    mandate_key: str,
    *,
    consumer: str,
    report_failure: bool = True,
) -> MandateResolution:
    """Ask the host WHICH agent a mandate KEY points at, or refuse.

    THE one resolution door. Two kinds of consumer arrive here and both must
    obey the same refusal rule:

    * a ``NamedAgent`` subclass declaring ``mandate_key`` (``run_mandated``,
      and anything that needs the bound agent without running it — the podcast
      image-provider diversity gate), via :func:`resolve_mandate_for`;
    * a WORKFLOW STEP naming a mandate instead of an agent id
      (``ai.agent.start`` with ``mandate_key`` set) — the seam that lets a
      graph obey the no-hardcoded-agents law, since a workflow definition
      otherwise freezes an agent id at authoring time.

    ``consumer`` is the caller's own name, used only in the alarm and the
    durable failure record, so an operator can see WHAT refused.

    A second copy of the unwrap-and-refuse logic is how two fallback rules get
    born, which is the failure this module exists to end. Legacy two-tuple
    resolvers are normalized here.

    Raises :class:`MandateResolutionUnavailable` when no resolver is installed or
    the resolver fails. It NEVER answers from an id frozen in code.

    ``report_failure`` is false only for a consumer that deliberately absorbs an
    unfulfilled mandate and emits its own truthful durable finding.  That avoids
    filing a second ``mandate_resolution_failed`` row which falsely says the run
    was refused after the consumer completed it on its authored configuration.
    """
    if not mandate_key:
        raise MandateResolutionUnavailable("<none>", consumer, "no mandate_key was given")

    if _MANDATE_RESOLVER is None:
        raise MandateResolutionUnavailable(
            mandate_key,
            consumer,
            "no mandate resolver is installed in this process",
        )

    try:
        resolution = await _MANDATE_RESOLVER(mandate_key)
    except Exception as exc:
        if report_failure:
            await _report_resolution_failure(mandate_key=mandate_key, consumer=consumer, exc=exc)
        raise MandateResolutionUnavailable(
            mandate_key,
            consumer,
            f"the installed resolver raised {type(exc).__name__}: {exc}",
        ) from exc

    if isinstance(resolution, MandateResolution):
        return resolution
    source, mandate_overrides = resolution
    return MandateResolution(source=source, config_overrides=mandate_overrides)


async def resolve_mandate_for(agent_cls: type[NamedAgent]) -> MandateResolution:
    """Resolve the mandate a ``NamedAgent`` subclass declares. See
    :func:`resolve_mandate_by_key` — this is the class-shaped door onto it."""
    mandate_key = getattr(agent_cls, "mandate_key", None)
    if not mandate_key:
        raise MandateResolutionUnavailable(
            "<none>", agent_cls.__name__, "this class declares no mandate_key"
        )
    return await resolve_mandate_by_key(mandate_key, consumer=agent_cls.__name__)


async def resolved_agent_id(agent_cls: type[NamedAgent]) -> str | None:
    """The agent (or version) id the DB currently binds to this class's mandate."""
    resolution = await resolve_mandate_for(agent_cls)
    return getattr(resolution.source, "agent_id", None)


class BrokenOfferPromise(ValueError):
    """A ``guaranteed`` offered value the call site did not actually supply.

    The declaration is a promise made by CODE. When it is broken the agent
    would answer about something it was never given, so the run REFUSES here —
    before the source loads, before a token is spent.
    """

    def __init__(self, mandate_key: str, consumer: str, missing: list[str]) -> None:
        super().__init__(
            f"Mandate {mandate_key!r} ({consumer}): guaranteed offered value(s) "
            f"{missing} were not supplied by the call site. A guaranteed value is a "
            f"promise; the run refuses rather than let the agent answer about "
            f"something it was never given. Either supply them under those exact "
            f"names, or change the Provision to declare what the call site really "
            f"offers."
        )
        self.mandate_key = mandate_key
        self.missing = missing


async def run_mandated(
    agent_cls: type[NamedAgent],
    *,
    offered: dict[str, Any] | None = None,
    **kwargs: Any,
) -> AgentRunResult:
    """SUGAR over the one runner: ``get_mandate_runner().run(key, Offer.from_inputs(...))``.

    Runner plan 25 step 5 merged the two NamedAgent funnels into ONE path — the host runner's
    NamedAgent engine (aidream ``mandates.named_agents.run_named``): resolve for the carried
    principal, mandate ``config_overrides`` UNDER the call's, the guaranteed-offer check, the
    consumption map (``offered`` = mapping-only extras), the attribution stamp, the run, the post-run
    honesty core. New call sites call the runner directly; this name goes with the last caller.

    A class with no ``mandate_key`` is not mandated and runs on its own source. There is no seed
    fallback: no runner installed raises :class:`MandateRunnerUnavailable`.
    """
    mandate_key = getattr(agent_cls, "mandate_key", None)
    if not mandate_key:
        return await agent_cls.run(**kwargs)
    # ONE PATH (runner plan 25 step 5): the host runner's NamedAgent engine — the same funnel the
    # host's own call sites reach. There is no second copy here any more.
    done = await get_mandate_runner().run(
        mandate_key,
        Offer.from_inputs(agent_cls, offered=offered, **kwargs),
        who=carried_principal(),
        opts=RunOptions(door="named_agent"),
    )
    return done.raw


#: The request-metadata key every mandate run carries — THE structured attribution
#: (``chat.user_request.metadata.mandate_key``). ``run_mandate``, the client chat-start
#: door, held code calls and both NamedAgent funnels write it at the funnel; every
#: reader (the runs list, the usage ledger's feature, the admin cost and run columns)
#: reads it before any free-text label.
MANDATE_KEY_METADATA = "mandate_key"
#: The caller's own label for the surface that ran the job, kept beside the key.
RUN_LABEL_METADATA = "run_label"


def mandate_run_feature(mandate_key: str) -> str:
    """``mandate:<key>`` — or ``mandate_candidate:<key>`` inside a candidate leg, which is
    its own labeled root and never one of the mandate's own runs."""
    from matrx_graph.candidate import candidate_marker

    prefix = "mandate_candidate" if candidate_marker() is not None else "mandate"
    return f"{prefix}:{mandate_key}"


def stamp_mandate_attribution(
    kwargs: dict[str, Any],
    mandate_key: str,
    agent_cls: type[NamedAgent],
    runner: Any = None,
) -> None:
    """THE ONE ATTRIBUTION STAMP for a NamedAgent run made for a mandate (both funnels).

    Until 2026-10-09 a NamedAgent run was filed under the class's own name
    (``agent_structure_builder``) or whatever ``source_feature`` its call site passed,
    so 236 Agent Structure Builder runs in 30 days had no ``mandate:<key>`` and the
    mandate's cost, points and runs read nothing. Now the run carries:

    * ``source_feature = mandate:<key>`` (``mandate_candidate:<key>`` in a candidate leg)
      — what the usage ledger groups by;
    * ``request_metadata.mandate_key`` — the structured key on the run's request;
    * the caller's own label (its ``source_feature``, else the class's
      ``child_source_feature`` / ``name``) as ``request_metadata.run_label`` and the
      run's ``label`` — never lost, never the attribution.

    A runner that cannot take these (a class's own ``run`` without them) is said
    LOUDLY, once per call — the run proceeds, unattributed, and the reference
    patrol's attribution leg files it.

    NEVER fails a run: any error here is said in red and the run goes on as the
    call site wrote it (Arman, 2026-10-09 — attribution never blocks a run).
    """
    snapshot = dict(kwargs)
    try:
        _stamp_mandate_attribution(kwargs, mandate_key, agent_cls, runner)
    except Exception as exc:  # noqa: BLE001 — attribution never breaks the run it labels
        kwargs.clear()
        kwargs.update(snapshot)
        from matrx_utils import vcprint

        vcprint(
            f"[mandates] attribution stamp FAILED for {mandate_key!r} "
            f"({type(exc).__name__}: {exc}) — the run proceeds unattributed",
            color="red",
        )


def _stamp_mandate_attribution(
    kwargs: dict[str, Any],
    mandate_key: str,
    agent_cls: type[NamedAgent],
    runner: Any,
) -> None:
    if runner is not None:
        try:
            params = inspect.signature(runner).parameters
        except (TypeError, ValueError):
            params = None
        if params is not None and not any(
            p.kind is inspect.Parameter.VAR_KEYWORD for p in params.values()
        ):
            missing = [n for n in ("source_feature", "request_metadata") if n not in params]
            if missing:
                from matrx_utils import vcprint

                vcprint(
                    f"[mandates] {agent_cls.__name__} runs mandate {mandate_key!r} through a "
                    f"runner that takes no {missing} — this run is NOT attributed to its mandate",
                    color="red",
                )
                return
    prior = (
        str(kwargs.get("source_feature") or "").strip()
        or str(getattr(agent_cls, "child_source_feature", None) or "").strip()
        or str(getattr(agent_cls, "name", "") or agent_cls.__name__)
    )
    feature = mandate_run_feature(mandate_key)
    kwargs["source_feature"] = feature
    if not kwargs.get("label"):
        kwargs["label"] = prior
    metadata = dict(kwargs.get("request_metadata") or {})
    metadata[MANDATE_KEY_METADATA] = mandate_key
    if prior != feature:
        metadata.setdefault(RUN_LABEL_METADATA, prior)
    kwargs["request_metadata"] = metadata


def _accepts(fn: Any, name: str) -> bool:
    try:
        params = inspect.signature(fn).parameters
    except (TypeError, ValueError):
        return False
    return name in params or any(p.kind is inspect.Parameter.VAR_KEYWORD for p in params.values())


def named_door_snapshot(
    agent_cls: type[NamedAgent], offered: dict[str, Any] | None, kwargs: dict[str, Any]
) -> dict[str, Any]:
    """The ``run_mandated`` door's input exactly as the call site handed it — SHALLOW.

    Cheap on purpose: it runs on the live path. ``agent_cls`` is recorded by
    import path so the host can re-enter the SAME door with the SAME class; the
    host serializes the rest off the path (a typed ``Inputs`` travels as its
    JSON dump — the door coerces a dict back through ``cls.Inputs``) and counts
    a value it cannot carry as an uncovered door, never silently.
    """
    return {
        "agent_cls": f"{agent_cls.__module__}:{agent_cls.__qualname__}",
        "offered": dict(offered) if offered else None,
        "kwargs": dict(kwargs),
    }


# ── THE CODE-CALL HOLDER ────────────────────────────────────────────────────
#
# A code position that calls the funnel directly (``llm_to_text`` /
# ``llm_to_pydantic`` / ``execute_ai_request`` / a host ``llm_provider`` seam)
# used to name its own model and write its own system prompt. Under the
# Universal Law that is a bypass (BYPASS-CENSUS, aidream): a change to the
# mandate changes nothing. ``hold_code_call`` is the one door that turns such a
# site into a mandated one WITHOUT changing its call mechanics: it resolves the
# mandate, loads the Holder agent with the site's variables and the winning
# binding's settings, and hands back exactly what the site used to hard-code —
# the model, the system prompt, the sampling knobs — plus the metadata that
# names who held the call. The Holder ALWAYS wins; the code chooses nothing.
#
# Resolve or refuse, like ``run_mandated``: the Holder IS the work here, so an
# unresolvable mandate raises :class:`MandateResolutionUnavailable` (loud, with
# a durable ``mandate_resolution_failed`` row) and never runs a frozen default.


@dataclass(frozen=True, slots=True)
class HeldCall:
    """What a mandated code call runs: all of it comes from the Holder."""

    mandate_key: str
    model: str
    system: str
    #: The Holder's sampling knobs after the binding's overrides. ``None`` means
    #: the Holder left it unset — pass it through as unset, never a code default.
    temperature: float | None
    max_output_tokens: int | None
    #: The Holder's own authored non-system turns, variables applied, as plain
    #: ``{"role", "content": str}`` dicts. A site whose Holder authors the user
    #: turn too sends THESE instead of composing its own.
    turns: list[dict[str, str]]
    #: The Holder's full config (variables applied) for callers that send more
    #: than model + system (image / speech settings, web search).
    config: Any
    #: ``mandate_key`` + the Holder identity, for the funnel's ``metadata=`` so
    #: the runtime carrier gate and the persisted request both name the Holder.
    metadata: dict[str, Any]
    #: The variables the Holder actually ran on (after the binding's map).
    variables: dict[str, Any] = field(default_factory=dict)
    #: The host's post-run honesty callback for this exact pin (required output
    #: keys, exemplar capture). Called by :meth:`finish`.
    complete: MandateCompletion | None = None
    #: Every variable the Holder DECLARES, as it resolved for this call (the
    #: site's offered value, else the Holder's own default). A Holder-authored
    #: text that is not a turn (a retry nudge, a per-turn budget line) lives here
    #: as a variable default; :meth:`authored_text` reads it.
    holder_values: dict[str, str] = field(default_factory=dict)
    #: ``"agent"`` or ``"workflow"``. A WORKFLOW-held call carries no model or
    #: prompt (``model`` is ``workflow:<id>``, ``system`` is empty): the funnel
    #: it reaches runs the workflow instead of a provider
    #: (``matrx_ai.mandate_workflow_holder``), so the site needs no change.
    holder_type: str = "agent"
    #: The live workflow holding (strong ref: it lives as long as this call).
    workflow: Any = None
    #: The Holder agent's chosen CLASS of its model — an ai.offering of
    #: ``model`` (one endpoint: "Matrx Fast", "Matrx Lightning"…). ``None`` = the
    #: model's preferred class. It belongs to ``model`` ONLY: a call that runs
    #: another model (an explicit request model) never carries it — use
    #: :meth:`pin_for` / :meth:`pick_offering`, never read it raw.
    offering_id: str | None = None
    #: THE RUN RECORD (AF-R): the ids of the conversation + request this call
    #: ran as, filled by ``execute_ai_request`` (:func:`note_held_run`) and
    #: handed to the host's completion by :meth:`finish`. Empty until it runs.
    run_ids: dict[str, Any] = field(default_factory=dict)
    #: Media the mandate's provision delivered (image/audio blocks built by the host's one media builder), for
    #: the site to attach to its turn. Empty for a mandate that declares no media.
    media_blocks: list[dict[str, Any]] = field(default_factory=list)
    #: The Holder AGENT itself, the binding's values already on it (config overrides, variables applied) — for a
    #: site that renders or runs the Holder on its own transport (a batch body, runner plan 25 step 7). ``None``
    #: for a workflow Holder. Read it through :meth:`holder_agent`, which refuses a workflow in words.
    agent: Any = None

    # ── THE ONE PRECEDENCE RULE for every held call (2026-09-25) ───────────
    # The Holder's settings apply. A caller's value wins ONLY when it was
    # explicitly set (a workflow author's node field, an API request field) —
    # never a code default dressed up as a choice.

    def pick_model(self, explicit: str | None = None) -> str:
        return explicit or self.model

    def pick_offering(
        self,
        explicit_model: str | None = None,
        explicit_offering: str | None = None,
        *,
        where: str = "held call",
    ) -> str | None:
        """The class pin for a call whose model is ``pick_model(explicit_model)``.

        An EXPLICIT class (a workflow author's ``offering_id`` beside their own
        ``model``) wins and runs; one with no explicit model, or one belonging
        to another model, is dropped loudly
        (:func:`matrx_ai.graph_nodes.class_pin.node_class_pin`). Otherwise the
        Holder's pin rides only when the call runs the Holder's OWN model; an
        explicit request model that differs runs its preferred class."""
        if explicit_offering:
            from matrx_ai.graph_nodes.class_pin import node_class_pin

            pinned = node_class_pin(explicit_model, explicit_offering, where=where)
            if pinned:
                return pinned
        if not self.offering_id:
            return None
        if explicit_model and str(explicit_model) != str(self.model):
            return None
        return self.offering_id

    def pin_for(
        self,
        explicit_model: str | None = None,
        explicit_offering: str | None = None,
        *,
        where: str = "held call",
    ) -> dict[str, Any]:
        """``{"offering_id": …}`` for a funnel call's kwargs, or ``{}`` — so a
        call that runs no pin passes exactly the kwargs it always passed."""
        offering = self.pick_offering(explicit_model, explicit_offering, where=where)
        return {"offering_id": offering} if offering else {}

    def pick_temperature(self, explicit: float | None = None) -> float | None:
        return explicit if explicit is not None else self.temperature

    def pick_max_tokens(self, explicit: int | None = None, *, unset: int) -> int:
        """``unset`` is what the funnel needs when BOTH the caller and the
        Holder leave the ceiling unset — the funnel's own default, not a choice."""
        if explicit is not None:
            return explicit
        return self.max_output_tokens if self.max_output_tokens else unset

    def turn_metadata(self, **values: Any) -> dict[str, Any]:
        """The metadata for ONE turn of a multi-turn call, with that turn's
        offered values (a research loop's log so far, its remaining budget).

        A WORKFLOW Holder receives them as inputs on top of the call's offered
        values, so each turn is a distinct run with distinct inputs — without
        them every turn of a loop would reattach to the first turn's answer.
        An agent Holder reads the turn from the messages, so for an agent this
        is ``self.metadata`` unchanged (nothing large lands on the request).
        """
        if self.holder_type != "workflow" or not values:
            return dict(self.metadata)
        from matrx_ai.orchestrator.mandate_carrier import MANDATE_HOLDER_METADATA_KEY

        carried = dict(self.metadata)
        stamp = dict(carried.get(MANDATE_HOLDER_METADATA_KEY) or {})
        stamp["turn_values"] = {k: to_template_value(v) for k, v in values.items()}
        carried[MANDATE_HOLDER_METADATA_KEY] = stamp
        return carried

    def user_text(self, text: str) -> str:
        """The site's user turn, exactly as the site wrote it — a binding never adds
        text to it (injection census #28: a spill is refused on a held call)."""
        return text

    def authored_user(self) -> str:
        """The user turn the HOLDER authors, the site's values applied.

        For a site whose framing text ("Below is a case…", "## Your Task…")
        lives on the Holder, not in code: the site offers only the data as
        variables (``hold_code_call(variables=...)``) and sends this. A Holder
        rebound to an agent that authors no user turn is refused in words —
        never an empty prompt sent to a model.
        """
        if self.holder_type == "workflow":
            # A workflow authors no turn: its inputs ARE the site's offered
            # values, which the funnel delivers onto its input surface. The
            # text sent is those values, so nothing reading it is lied to.
            return json.dumps(self.variables, ensure_ascii=False, default=str)
        texts = [turn["content"] for turn in self.turns if turn.get("role") == "user"]
        if not texts:
            consumer = str((self.metadata.get("mandate_holder") or {}).get("consumer") or "")
            raise MandateResolutionUnavailable(
                self.mandate_key,
                consumer,
                "this call sends the user turn its Holder authors, and the Holder authors "
                "none — rebind it to an agent whose messages include the user turn",
            )
        return "\n\n".join(texts)

    def authored_text(self, variable: str, **values: Any) -> str:
        """A text the HOLDER authors outside its turns, the site's values applied.

        For instruction text a site sends mid-run — a retry nudge after a
        malformed answer, a budget line before each research turn — which
        cannot be one of the Holder's authored turns because it is sent only
        sometimes, or once per loop. The Holder carries it as the default of
        ``variable``; ``values`` fill its ``{{placeholders}}`` through the same
        prompt door every template uses. A Holder that declares no such text
        is refused in words — never a code fallback, never an empty turn.
        """
        from matrx_ai.config.prompt_values import prompt_safe_value

        if self.holder_type == "workflow":
            # No Holder-authored text exists; the workflow reads the offered
            # values, never this turn. Say what it is instead of inventing one.
            return f"({variable})"
        text = self.holder_values.get(variable, "")
        if not str(text).strip():
            consumer = str((self.metadata.get("mandate_holder") or {}).get("consumer") or "")
            raise MandateResolutionUnavailable(
                self.mandate_key,
                consumer,
                f"this call sends the {variable!r} text its Holder authors, and the Holder "
                f"declares none — rebind it to an agent whose variable {variable!r} carries it",
            )
        from matrx_ai.config.template_substitution import substitute_authored

        # The Holder's own text: the escape and the sections run too (config/template_substitution.py).
        # One pass: a value's own braces are data, never re-filled.
        return substitute_authored(str(text), str(text), values, prompt_safe_value, unescape=True)

    def holder_agent(self) -> Any:
        """The Holder agent with the binding's values on it, for a site that renders or runs it itself (a batch
        body). A WORKFLOW Holder is refused in words: it is a durable run, never one provider request."""
        if self.holder_type != "agent" or self.agent is None:
            raise MandateRefused(
                self.mandate_key,
                code="holder_not_an_agent",
                sentence=(
                    f"this call renders its Holder agent itself, and the Holder is a {self.holder_type!r} — "
                    "rebind it to an agent"
                ),
            )
        return self.agent

    async def send(self, **kwargs: Any) -> Any:
        """One turn, no tools, through the funnel; closes the run. See :func:`_send_call`."""
        return await _send_call(self, **kwargs)

    async def send_pydantic(self, **kwargs: Any) -> Any:
        """A strict-JSON call with the Holder's settings; closes the run. See :func:`_send_pydantic`."""
        return await _send_pydantic(self, **kwargs)

    async def send_text(self, **kwargs: Any) -> Any:
        """A free-text call with the Holder's settings; closes the run. See :func:`_send_text`."""
        return await _send_text(self, **kwargs)

    async def finish(
        self,
        output: str,
        *,
        parsed: Any = None,
        success: bool = True,
        error: str | None = None,
    ) -> None:
        """Hand the call's result to the mandate's post-run check.

        Every held site calls this once its call returns — the same completion
        ``run_mandated`` runs, so a Holder that stops answering in its declared
        shape is caught for code calls too. Never raises: completion cannot
        invalidate a delivered response, but a failure is said out loud — the
        ONE exception is an error marked ``fails_the_run`` (the host's
        MandateOutputError for an answer missing required keys from a Holder
        chosen although it does not declare them), which stops the job.
        """
        if self.complete is None:
            return
        usage: dict[str, Any] = {}
        facts: dict[str, Any] = {}
        answer = getattr(self.workflow, "last_answer", None)
        if self.holder_type == "workflow" and isinstance(answer, dict):
            # The workflow's measured spend and its run, recorded with the call.
            usage = dict(answer.get("cost") or {})
            facts = {
                "workflow_run_id": answer.get("run_id"),
                "workflow_id": answer.get("workflow_id"),
                "warnings": list(answer.get("warnings") or []),
            }
        # ``AgentRunResult.parsed`` is typed as a pydantic model, so a dict handed to the constructor is coerced into
        # a BARE ``BaseModel()`` that cannot be read, dumped or printed — every held site that parses its own JSON
        # (records enrichment, the bake-off judges, docproc, masterworks) then failed its post-run check with "BaseModel
        # cannot be instantiated directly" (lane AGENT-RECORDS-MCP-2, 2026-10-19). A dict or list is the parsed
        # artifact as it is: set it after construction, untouched.
        keep_raw = isinstance(parsed, dict | list)
        result = AgentRunResult(
            success=success,
            output=output or "",
            model_id=self.model,
            parsed=None if keep_raw else parsed,
            error=error,
            error_kind="execution" if not success else None,
            usage=usage,
            metadata={**_finished_run_ids(self), **facts},
        )
        if keep_raw:
            result.parsed = parsed
        try:
            await self.complete(result, dict(self.variables), None)
        except Exception as exc:  # noqa: BLE001 — see docstring
            if getattr(exc, "fails_the_run", False):
                # The one exception (see run_mandated above): an answer missing
                # the keys the job reads stops the job, never reaches the site.
                raise
            from matrx_utils import vcprint

            vcprint(
                f"[mandates] post-run honesty callback FAILED for {self.mandate_key!r}: "
                f"{type(exc).__name__}: {exc}",
                color="red",
            )


# ---------------------------------------------------------------------------
# THE RUN RECORD for held code calls (AF-R)
# ---------------------------------------------------------------------------
#
# A held call reaches a provider through the ONE funnel (``execute_ai_request``)
# by whatever site-specific path it takes (``run_held_*`` or a site's own
# funnel call). The funnel finds the call by the ``held_call_id`` on its Holder
# stamp, runs it as its OWN conversation (linked to the one it ran inside) and
# notes the ids here; :meth:`HeldCall.finish` hands them to the host, which
# writes the run record on that conversation.

#: Live held calls' id sinks, by ``held_call_id`` (bounded: a call that never
#: finishes is forgotten after ``_HELD_RUNS_MAX`` newer ones).
_HELD_RUNS: dict[str, dict[str, Any]] = {}
_HELD_RUNS_MAX = 4096


def _register_held_run(held_call_id: str, sink: dict[str, Any]) -> None:
    _HELD_RUNS[held_call_id] = sink
    while len(_HELD_RUNS) > _HELD_RUNS_MAX:
        _HELD_RUNS.pop(next(iter(_HELD_RUNS)))


def held_call_id_of(metadata: dict[str, Any] | None) -> str | None:
    """The ``held_call_id`` an AGENT-held call's request metadata carries."""
    if not isinstance(metadata, dict):
        return None
    from matrx_ai.mandate_workflow_holder import HELD_CALL_ID_KEY
    from matrx_ai.orchestrator.mandate_carrier import MANDATE_HOLDER_METADATA_KEY

    stamp = metadata.get(MANDATE_HOLDER_METADATA_KEY)
    if not isinstance(stamp, dict) or stamp.get("holder_type") != "agent":
        return None
    held_id = stamp.get(HELD_CALL_ID_KEY)
    return str(held_id) if held_id else None


def note_held_run(
    metadata: dict[str, Any] | None,
    *,
    conversation_id: str | None,
    request_id: str | None,
    stored: bool,
) -> None:
    """Called by the funnel: the held call ran as ``conversation_id``."""
    held_id = held_call_id_of(metadata)
    sink = _HELD_RUNS.get(held_id) if held_id else None
    if sink is None:
        return
    sink.clear()
    sink.update(
        {
            "conversation_id": str(conversation_id) if conversation_id else None,
            "request_id": str(request_id) if request_id else None,
            "stored": bool(stored),
        }
    )


_UNRECORDED_ANNOUNCED: set[str] = set()


def _finished_run_ids(held: HeldCall) -> dict[str, Any]:
    """The ids :meth:`HeldCall.finish` reports — only for a stored own run.

    A call that never reached the funnel, or ran under a person's own
    do-not-save request, has no conversation to record on: said once per
    mandate key, never per call."""
    held_id = str((held.metadata.get("mandate_holder") or {}).get("held_call_id") or "")
    _HELD_RUNS.pop(held_id, None)
    ids = held.run_ids
    if ids.get("stored") and ids.get("conversation_id"):
        return {k: ids[k] for k in ("conversation_id", "request_id") if ids.get(k)}
    if held.holder_type == "agent" and held.mandate_key not in _UNRECORDED_ANNOUNCED:
        _UNRECORDED_ANNOUNCED.add(held.mandate_key)
        import logging

        logging.getLogger(__name__).warning(
            "[mandates] held code call %s keeps NO run record: %s (said once per key)",
            held.mandate_key,
            "it ran under a non-persisting request (a person's store=False, or the labeler's "
            "unsaved-run exemption)"
            if ids
            else "its funnel call never reached execute_ai_request (or carried a copy of "
            "the metadata without the Holder stamp)",
        )
    return {}


def engine_output(result: Any) -> tuple[str, Any]:
    """A finished call's ``(output text, parsed artifact)`` — what ``finish()`` records, whichever runner.

    A string is the text; a dict/list is the site's own parsed JSON (its text the JSON); a validated
    pydantic value (``llm_to_pydantic``) is dumped; anything else reads ``final_text`` / ``output`` and
    ``parsed``."""
    if isinstance(result, str):
        return result, None
    if isinstance(result, dict | list):
        return json.dumps(result, ensure_ascii=False, default=str), result
    if hasattr(result, "model_dump") and not hasattr(result, "final_text") and not hasattr(result, "output"):
        dumped = result.model_dump(mode="json")
        return json.dumps(dumped, ensure_ascii=False, default=str), dumped
    text = getattr(result, "final_text", None)
    if text is None:
        text = getattr(result, "output", None)
    return str(text or ""), getattr(result, "parsed", None)


class UncarriableHeldPart(ValueError):
    """An authored Holder part a text-only held call cannot carry honestly."""


def _speech_script_text(part: dict[str, Any]) -> str:
    lines: list[str] = []
    for turn in part.get("turns") or []:
        if not isinstance(turn, dict):
            continue
        speaker = str(turn.get("speaker") or "").strip() or "Speaker"
        direction = str(turn.get("direction") or "").strip()
        label = f"{speaker} ({direction})" if direction else speaker
        lines.append(f"{label}: {str(turn.get('text') or '').strip()}")
    return "\n".join(lines)


def held_turn_text(content: list[Any]) -> str:
    """One authored turn's parts, as the text a held (text-only) call sends.

    A held call hands plain ``{"role", "content": str}`` turns to a text funnel,
    so every part must become text HONESTLY or be refused — never emptied. Text
    stays text; decision questions become the same verbalized prose a text model
    is given by the decision translator; decision answers become their JSON; a
    speech script becomes its ``Speaker: line`` transcript. Anything else (media,
    tool calls, …) cannot ride a text turn and raises :class:`UncarriableHeldPart`
    naming the part — the caller refuses the call loudly.
    """
    pieces: list[str] = []
    for part in content:
        if isinstance(part, str):
            pieces.append(part)
            continue
        if not isinstance(part, dict):
            raise UncarriableHeldPart(
                f"an authored message part of type {type(part).__name__} cannot be carried "
                "as text by a held code call"
            )
        part_type = str(part.get("type") or "")
        if part_type == "text":
            pieces.append(str(part.get("text") or ""))
        elif part_type == "decision_questions":
            from matrx_ai.decisions.kinds import DecisionQuestions
            from matrx_ai.decisions.translate import verbalized_instructions

            batch = DecisionQuestions(questions=list(part.get("questions") or []))
            pieces.append(verbalized_instructions({}, batch, subject_above=bool(pieces)))
        elif part_type == "decision_answers":
            carried = {
                k: part.get(k)
                for k in ("model", "method", "answers", "unanswerable")
                if part.get(k) is not None
            }
            pieces.append(
                "Decision answers:\n```json\n"
                + json.dumps(carried, ensure_ascii=False, indent=2, default=str)
                + "\n```"
            )
        elif part_type == "speech_script":
            pieces.append(_speech_script_text(part))
        else:
            label = part_type or "untyped"
            if part_type == "media" and part.get("kind"):
                label = f"media ({part.get('kind')})"
            raise UncarriableHeldPart(
                f"its Holder authors a {label} part in a message, and a held code call "
                "sends text turns only — the part cannot be carried and will not be "
                "silently dropped. Run this mandate through run_mandated (the agent "
                "funnel), or describe the part in text on the Holder"
            )
    return "\n".join(p for p in pieces if p)


async def _refuse_code_call(mandate_key: str, consumer: str, reason: str) -> NoReturn:
    """Every refusal of a code call is recorded durably, then raised."""
    exc = MandateResolutionUnavailable(mandate_key, consumer, reason)
    await _report_resolution_failure(mandate_key=mandate_key, consumer=consumer, exc=exc)
    raise exc


async def hold_code_call(
    mandate_key: str,
    *,
    consumer: str,
    variables: dict[str, Any] | None = None,
    metadata: dict[str, Any] | None = None,
) -> HeldCall:
    """Resolve ``mandate_key`` and return the Holder's model, prompt and knobs.

    ``variables`` are the site's OFFERED values (the dynamic parts it used to
    f-string into its prompt). They go through the binding's whole contract —
    the host's consumption pipeline (consumption map, guaranteed values, the
    required-input gate), then the binding's ``variable_mapping`` and
    ``spill_variables`` onto the Holder's own declared variables — exactly as
    ``run_mandated`` does, so rebinding to an agent with different variable
    names works. Every refusal writes a durable ``mandate_resolution_failed``
    record before raising. ``metadata`` is merged under the Holder stamp.
    """
    from matrx_ai.agents.named import resolve_variable_mapping
    from matrx_ai.orchestrator.mandate_carrier import (
        MANDATE_HOLDER_METADATA_KEY,
        MANDATE_KEY_METADATA_KEY,
    )

    resolution = await resolve_mandate_by_key(mandate_key, consumer=consumer)
    if variables and any(isinstance(v, Offered) for v in variables.values()):
        if resolution.consumption_map and resolution.materialize is not None and resolution.holder_type == "agent":
            # The host pipeline applies the compute rule to the offers (only bound names build).
            variables = dict(variables)
        else:
            # No map (the by-name lane) or a workflow Holder: every value rides by name, so every builder runs.
            variables = {k: (await run_offered(v)) if isinstance(v, Offered) else v for k, v in variables.items()}
            variables = {k: v for k, v in variables.items() if v is not None}
    if resolution.holder_type == "workflow":
        return await _hold_by_workflow(
            mandate_key, consumer=consumer, resolution=resolution,
            variables=variables, metadata=metadata,
        )
    if resolution.holder_type != "agent" or resolution.source is None:
        await _refuse_code_call(
            mandate_key,
            consumer,
            f"it resolved to a {resolution.holder_type!r} Holder, which a code call cannot "
            "run — rebind it to an agent or a workflow",
        )
    try:
        agent = await resolution.source.load()
    except Exception as exc:  # noqa: BLE001 — every load failure is one shape
        await _refuse_code_call(
            mandate_key, consumer, f"its Holder could not be loaded: {type(exc).__name__}: {exc}"
        )
    if resolution.config_overrides:
        agent.apply_config_overrides(**dict(resolution.config_overrides))

    offered = dict(variables or {})
    if not resolution.consumption_map:
        # The default pin: values offered for mapping only never reach the
        # agent by name (and never trip the "does not consume" line below).
        offered = default_pin_offer(offered, resolution.offered_values)
    # A binding that carries a consumption map re-routes the site's offered
    # values, so the host's ONE pipeline decides what the Holder receives (and
    # refuses a context/media route this call site cannot deliver). With no map
    # — the default pin — values pass by name, exactly as for run_mandated.
    held_media: list[dict[str, Any]] = []
    if resolution.materialize_media is not None:
        try:
            offered, held_media = await resolution.materialize_media(offered)
        except Exception as exc:  # noqa: BLE001 — the pipeline refuses in words
            await _refuse_code_call(mandate_key, consumer, f"{type(exc).__name__}: {exc}")
    elif resolution.consumption_map and resolution.materialize is not None:
        try:
            offered = await resolution.materialize(offered)
        except Exception as exc:  # noqa: BLE001 — the pipeline refuses in words
            await _refuse_code_call(mandate_key, consumer, f"{type(exc).__name__}: {exc}")
    elif resolution.consumption_map:
        await _refuse_code_call(
            mandate_key,
            consumer,
            "the binding carries a consumption map and this host offers no pipeline to apply "
            "it — the map would be silently ignored, so the call refuses",
        )
    try:
        bound = resolve_variable_mapping(
            offered,
            getattr(agent, "variable_defaults", {}) or {},
            dict(resolution.variable_mapping) if resolution.variable_mapping else None,
            spill=set(resolution.spill_variables or ()),
            user_input=None,
        )
    except ValueError as exc:
        await _refuse_code_call(
            mandate_key, consumer, f"the binding's variable mapping cannot be read: {exc}"
        )
    if bound.blocking:
        detail = "; ".join(v.message for v in bound.verdicts if v.blocking)
        await _refuse_code_call(
            mandate_key, consumer, f"the binding's variable mapping is invalid: {detail}"
        )
    if bound.spilled:
        # A held call is a raw model request with no context channel, and a
        # spilled value is never written into a turn (injection census #28).
        await _refuse_code_call(
            mandate_key,
            consumer,
            f"the binding spills {sorted(bound.spilled)}, which a held code call cannot "
            "deliver except as text added to the turn — declare them as variables on the "
            "Holder instead",
        )
    dropped = [
        v.code_name for v in bound.verdicts if getattr(v, "caution", False) and v.code_name
    ]
    if dropped:
        from matrx_utils import vcprint

        vcprint(
            f"[mandates] {mandate_key} ({consumer}): the Holder does not consume {dropped}",
            color="yellow",
        )
    held_variables = {k: to_template_value(v) for k, v in bound.variables.items()}
    agent.set_variables(**held_variables)
    # The pre-substitution step before substituting (a ``sources`` value becomes text).
    await agent.prepare_variables()
    agent.apply_variables()
    holder_values: dict[str, str] = {}
    for name, declared in (getattr(agent, "variable_defaults", None) or {}).items():
        if name in held_variables:
            holder_values[name] = str(held_variables[name] or "")
            continue
        get_value = getattr(declared, "get_value", None)
        holder_values[name] = str(get_value() if callable(get_value) else "") or ""
    config = agent.config
    model = str(getattr(config, "model", "") or "").strip()
    if not model:
        await _refuse_code_call(mandate_key, consumer, "its Holder agent names no model")
    # The Holder's AUTHORED instructions, without the per-send decorations (the
    # "Current date" line, the tools list): the funnel this text is handed to
    # decorates it again, so leaving them in would send them twice.
    instruction = getattr(config, "system_instruction", None)
    if hasattr(instruction, "strip_chat_decorations"):
        import copy

        instruction = copy.deepcopy(instruction)
        instruction.strip_chat_decorations()
        system = str(instruction)
    else:
        system = config.resolved_system_instruction or ""
    turns: list[dict[str, str]] = []
    messages = getattr(config, "messages", None)
    raw_turns = messages.to_dict_list() if hasattr(messages, "to_dict_list") else list(messages or [])
    for message in raw_turns:
        role = str(message.get("role") or "")
        if role in ("system", "developer") or not role:
            continue
        content = message.get("content")
        if isinstance(content, list):
            try:
                text = held_turn_text(content)
            except UncarriableHeldPart as exc:
                await _refuse_code_call(mandate_key, consumer, str(exc))
        else:
            text = str(content or "")
        turns.append({"role": role, "content": text})
    from uuid import uuid4

    from matrx_ai.mandate_workflow_holder import HELD_CALL_ID_KEY

    held_call_id = uuid4().hex
    carried: dict[str, Any] = dict(metadata or {})
    carried[MANDATE_KEY_METADATA_KEY] = mandate_key
    if resolution.run_stamp:
        carried["mandate_resolution"] = dict(resolution.run_stamp)
    carried[MANDATE_HOLDER_METADATA_KEY] = {
        "mandate_key": mandate_key,
        "holder_type": "agent",
        "agent_id": str(getattr(resolution.source, "agent_id", "") or ""),
        "is_version": bool(getattr(resolution.source, "is_version", False)),
        "name": getattr(agent, "name", None),
        "consumer": consumer,
        HELD_CALL_ID_KEY: held_call_id,
    }
    held = HeldCall(
        mandate_key=mandate_key,
        model=model,
        system=system,
        temperature=getattr(config, "temperature", None),
        max_output_tokens=getattr(config, "max_output_tokens", None),
        turns=turns,
        config=config,
        metadata=carried,
        variables=held_variables,
        complete=resolution.complete,
        holder_values=holder_values,
        offering_id=str(getattr(config, "offering_id", None) or "") or None,
        media_blocks=list(held_media),
        agent=agent,
    )
    _register_held_run(held_call_id, held.run_ids)
    return held


async def _hold_by_workflow(
    mandate_key: str,
    *,
    consumer: str,
    resolution: MandateResolution,
    variables: dict[str, Any] | None,
    metadata: dict[str, Any] | None,
) -> HeldCall:
    """WORKFLOW PARITY: the HeldCall of a code call whose Holder is a workflow.

    It carries no model and no prompt — there are none — and a live holding
    the funnel finds through the Holder stamp, so ``execute_ai_request`` runs
    the workflow in place of a provider and hands the site its answer in the
    shape the site already reads. See ``matrx_ai.mandate_workflow_holder``.
    """
    from matrx_ai.mandate_workflow_holder import HELD_CALL_ID_KEY, register_holding
    from matrx_ai.orchestrator.mandate_carrier import (
        MANDATE_HOLDER_METADATA_KEY,
        MANDATE_KEY_METADATA_KEY,
    )

    workflow_id = str(resolution.workflow_id or "")
    if not workflow_id:
        await _refuse_code_call(
            mandate_key, consumer, "it resolved to a workflow Holder that names no workflow"
        )
    if resolution.run_workflow is None:
        await _refuse_code_call(
            mandate_key,
            consumer,
            "it resolved to a workflow Holder and this process's mandate resolver offers no "
            "workflow runner (MandateResolution.run_workflow) — install one in the host "
            "resolver; the workflow cannot be run from here",
        )
    offered = {k: to_template_value(v) for k, v in dict(variables or {}).items()}
    holding = register_holding(
        mandate_key=mandate_key,
        consumer=consumer,
        workflow_id=workflow_id,
        workflow_version_id=resolution.workflow_version_id,
        output_kind=resolution.output_kind,
        offered_values=resolution.offered_values,
        supplied=dict(variables or {}),
        runner=resolution.run_workflow,
    )
    carried: dict[str, Any] = dict(metadata or {})
    carried[MANDATE_KEY_METADATA_KEY] = mandate_key
    if resolution.run_stamp:
        carried["mandate_resolution"] = dict(resolution.run_stamp)
    carried[MANDATE_HOLDER_METADATA_KEY] = {
        "mandate_key": mandate_key,
        "holder_type": "workflow",
        "workflow_id": workflow_id,
        "workflow_version_id": resolution.workflow_version_id,
        "version_number": resolution.version_number,
        "consumer": consumer,
        HELD_CALL_ID_KEY: holding.held_call_id,
    }
    return HeldCall(
        mandate_key=mandate_key,
        model=f"workflow:{workflow_id}",
        system="",
        temperature=None,
        max_output_tokens=None,
        turns=[],
        config=None,
        metadata=carried,
        variables=offered,
        complete=resolution.complete,
        holder_values={},
        holder_type="workflow",
        workflow=holding,
    )


#: The Holder's own generation knobs a held call carries verbatim. Anything the
#: Holder leaves unset stays unset — the code never supplies a default.
_HELD_KNOBS: tuple[str, ...] = (
    "top_p",
    "top_k",
    "reasoning_effort",
    "reasoning_summary",
    "thinking_level",
    "thinking_budget",
    "include_thoughts",
    "verbosity",
    "response_format",
    "stop_sequences",
    "extended_prompt_cache",  # the agent's long-cache setting (config/cache_marks.py)
)


def held_request_config(
    held: HeldCall,
    *,
    extra_turns: list[dict[str, Any]] | None = None,
    stream: bool = False,
    max_output_tokens: int | None = None,
    hosted_tool_options: Mapping[str, Any] | None = None,
) -> Any:
    """The whole request a held call sends, built ONLY from its Holder.

    ``hold_code_call`` hands back the model, prompt and sampling knobs; a site
    that needs the Holder's OTHER settings too — its reasoning effort, its
    response format (JSON mode), its authored few-shot turns — sends this
    instead of re-typing any of them. ``extra_turns`` are the run's own turns
    (the text being processed), appended after the Holder's authored ones.
    ``max_output_tokens`` is a run-scope ceiling a caller may lower, never a
    default: when omitted the Holder's own ceiling applies.

    ``hosted_tool_options`` narrows a provider-run tool the HOLDER turned on (its ``internal_x_search`` /
    ``internal_web_search`` setting) for this one call: ``{"internal_x_search": {"allowed_x_handles": [h]},
    "max_turns": 2}``. The Holder decides whether the tool runs; the site only says what it is reading. A
    call that narrows a tool its Holder does not run is refused in words, never sent without it.
    """
    from matrx_ai.config import UnifiedConfig

    cfg: dict[str, Any] = {
        "model": held.model,
        "system_instruction": held.system,
        "messages": [
            *held.turns,
            *(extra_turns or []),
        ],
        "stream": stream,
    }
    if held.offering_id:
        # The Holder's chosen class of ITS model (this config runs held.model).
        cfg["offering_id"] = held.offering_id
    ceiling = max_output_tokens if max_output_tokens is not None else held.max_output_tokens
    if ceiling is not None:
        cfg["max_output_tokens"] = ceiling
    if held.temperature is not None:
        cfg["temperature"] = held.temperature
    for knob in _HELD_KNOBS:
        value = getattr(held.config, knob, None)
        if value not in (None, [], ""):
            cfg[knob] = value
    if hosted_tool_options:
        for setting in hosted_tool_options:
            if setting == "max_turns":
                continue
            if getattr(held.config, setting, None) is not True:
                raise MandateRefused(
                    held.mandate_key,
                    code="holder_lacks_hosted_tool",
                    sentence=(
                        f"this call narrows the provider tool {setting!r}, and its Holder does not run it — "
                        f"rebind it to an agent with {setting} on"
                    ),
                )
            cfg[setting] = True
        cfg["hosted_tool_options"] = dict(hosted_tool_options)
    return UnifiedConfig.from_dict(cfg)


async def _send_call(
    held: HolderCarrier[HeldCall],
    *,
    extra_turns: list[dict[str, Any]] | None = None,
    max_output_tokens: int | None = None,
    store: bool = True,
    hosted_tool_options: Mapping[str, Any] | None = None,
) -> Any:
    """Run one held call to completion and return the normalized result.

    One turn, no tools of ours (a provider-run tool the Holder turns on runs inside the provider's
    call; ``hosted_tool_options`` narrows it, see :func:`held_request_config`), not streamed to any listener — the shape of a code call
    (a labeler, a cleaner, an observer). Returns ``AiExecutionResult``:
    ``final_text`` plus the usage the funnel measured. The metadata names the
    Holder, so the runtime carrier gate and ``chat.request`` both record who
    held it.
    """
    import asyncio

    from matrx_connect.context.app_context import (
        clear_app_context,
        set_app_context,
        try_get_app_context,
    )
    from matrx_connect.emitters.console_emitter import ConsoleEmitter

    from matrx_ai.graph_nodes.shared import normalize_completed
    from matrx_ai.orchestrator.executor import execute_ai_request

    # A code call belongs to no listener: whatever stream the surrounding
    # request owns (a person's chat) must never receive this call's events.
    parent = try_get_app_context()
    token = None
    if parent is not None:
        token = set_app_context(
            parent.with_overrides(
                emitter=ConsoleEmitter(label=f"held:{held.mandate_key}", debug=False),
                store=store,
                # A code call is not a turn in the person's chat: keep the cost
                # spine (it IS recorded) but write no transcript into the
                # surrounding conversation.
                system_run=True,
                # Nor is it a run of the person's agent: inheriting these
                # stamped the labeler's side conversation with the parent's
                # agent id and variables, so it surfaced as a "recent run" of
                # that agent (a test case whose input was the labeler prompt).
                agent_id=None,
                agent_version_id=None,
                initial_variables={},
                initial_overrides={},
                # Nor is it a run of the PARENT'S mandate: inheriting `mandate:<parent key>`
                # filed every labeler call under the mandate that triggered it (the
                # Agent Studio chat brief listed "Agent Conversation Labeler" runs,
                # 2026-10-07). The call names its own mandate, like run_mandate does.
                source_feature=f"mandate:{held.mandate_key}",
            )
        )
    try:
        completed = await execute_ai_request(
            held_request_config(
                held,
                extra_turns=extra_turns,
                max_output_tokens=max_output_tokens,
                hosted_tool_options=hosted_tool_options,
            ),
            max_iterations=1,
            max_retries_per_iteration=2,
            # The Holder stamp (mandate_key + mandate_holder) rides the metadata;
            # that is the carrier the executor reads.
            metadata=dict(held.metadata),
            store=store,
        )
    except Exception as exc:
        await held.finish("", success=False, error=f"{type(exc).__name__}: {exc}")
        raise
    finally:
        if token is not None:
            clear_app_context(token)
    result = await asyncio.to_thread(normalize_completed, completed)
    await held.finish(result.final_text or "")
    return result


async def _send_pydantic(
    held: HolderCarrier[HeldCall],
    *,
    output_cls: type[Any],
    user: str | None = None,
    messages: list[dict[str, Any]] | None = None,
    model: str | None = None,
    offering_id: str | None = None,
    max_tokens: int | None = None,
    temperature: float | None = None,
    unset_max_tokens: int = 8092,
    system: str | None = None,
    metadata: dict[str, Any] | None = None,
    measured: bool = False,
    **funnel_kwargs: Any,
) -> Any:
    """A held strict-JSON call: the Holder's settings, the one precedence rule,
    the binding's spill, and the post-run check — in one place.

    ``measured=True`` returns the funnel's ``MeasuredStrictJson`` (``value`` + summed
    ``usage.cost_usd`` / tokens over every attempt) instead of the bare value, for a caller
    that must publish what the call cost (the Agent Evaluation judge).

    ``model`` / ``max_tokens`` / ``temperature`` are EXPLICIT caller overrides
    (a workflow author's field, an API request's field) and win only when set.
    ``offering_id`` is the explicit model's chosen class: it runs only beside
    an explicit ``model`` it belongs to, and is dropped loudly otherwise.
    ``system`` replaces the Holder's system text only when a site composes it
    FROM the Holder's (``held.system`` + an author's addendum). Everything
    else in ``funnel_kwargs`` passes to ``llm_messages_to_pydantic`` untouched.
    """
    import importlib

    # Looked up at call time on the module (not bound at import) so a test that
    # swaps the funnel module sees its double — the same seam every caller uses.
    funnel = importlib.import_module("matrx_ai.graph_nodes._strict_json")
    common: dict[str, Any] = {
        "model": held.pick_model(model),
        **held.pin_for(model, offering_id, where=held.mandate_key),
        "system": held.system if system is None else system,
        "output_cls": output_cls,
        "max_tokens": held.pick_max_tokens(max_tokens, unset=unset_max_tokens),
        "temperature": held.pick_temperature(temperature),
        "metadata": {**(metadata or {}), **held.metadata},
        **funnel_kwargs,
    }
    try:
        if messages is None:
            fn = funnel.llm_to_pydantic_measured if measured else funnel.llm_to_pydantic
            value = await fn(user=held.user_text(user or ""), **common)
        else:
            fn = funnel.llm_messages_to_pydantic_measured if measured else funnel.llm_messages_to_pydantic
            value = await fn(messages=messages, **common)
    except Exception as exc:
        await held.finish(
            getattr(exc, "raw_output", "") or "",
            success=False,
            error=f"{type(exc).__name__}: {exc}"[:500],
        )
        raise
    parsed_value = value.value if measured else value
    dumped = parsed_value.model_dump(mode="json") if hasattr(parsed_value, "model_dump") else parsed_value
    await held.finish(json.dumps(dumped, ensure_ascii=False, default=str), parsed=dumped)
    return value


async def _send_text(
    held: HolderCarrier[HeldCall],
    *,
    user: str,
    model: str | None = None,
    offering_id: str | None = None,
    max_tokens: int | None = None,
    temperature: float | None = None,
    unset_max_tokens: int = 8092,
    system: str | None = None,
    metadata: dict[str, Any] | None = None,
    measured: bool = False,
    **funnel_kwargs: Any,
) -> Any:
    """The free-text twin of :func:`run_held_pydantic` (``llm_to_text``, or
    ``llm_to_text_measured`` with ``measured=True`` — then the whole
    ``AiExecutionResult`` is returned, usage included)."""
    import importlib

    funnel = importlib.import_module("matrx_ai.graph_nodes._strict_json")
    call = funnel.llm_to_text_measured if measured else funnel.llm_to_text
    try:
        result = await call(
            model=held.pick_model(model),
            **held.pin_for(model, offering_id, where=held.mandate_key),
            system=held.system if system is None else system,
            user=held.user_text(user),
            max_tokens=held.pick_max_tokens(max_tokens, unset=unset_max_tokens),
            temperature=held.pick_temperature(temperature),
            metadata={**(metadata or {}), **held.metadata},
            **funnel_kwargs,
        )
    except Exception as exc:
        await held.finish("", success=False, error=f"{type(exc).__name__}: {exc}"[:500])
        raise
    text = (getattr(result, "final_text", None) or "") if measured else (result or "")
    await held.finish(text)
    return result


# ── PORT SUGAR (runner plan 25 step 6) ─────────────────────────────────────
#
# A site prepared through the runner sends its held call ITSELF:
#
#     prepared = await get_mandate_runner().prepare(KEY, Offer.given_values({...}), who=..., opts=...)
#     held = prepared.held_call()
#     value = await held.send_pydantic(output_cls=Model, user=held.authored_user())
#
# ``send_*`` send the request through the one funnel and close the run (``HeldCall.finish`` — the same
# completion the runner's ``finish`` runs for a prepared raw request). The ``run_held_*`` names below are the
# same sugar for sites still holding through ``hold_code_call``; they go with their last caller.


async def run_held_call(held: HolderCarrier[HeldCall], **kwargs: Any) -> Any:
    return await _send_call(held, **kwargs)


async def run_held_pydantic(held: HolderCarrier[HeldCall], **kwargs: Any) -> Any:
    return await _send_pydantic(held, **kwargs)


async def run_held_text(held: HolderCarrier[HeldCall], **kwargs: Any) -> Any:
    return await _send_text(held, **kwargs)
