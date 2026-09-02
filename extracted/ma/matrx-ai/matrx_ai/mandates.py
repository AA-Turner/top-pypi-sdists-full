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
        mandate_key = "pdf.content_cleaner"   # the DB decides which agent runs

    result = await run_mandated(MyAgent, inputs=...)

This started as a private helper inside ``agent_runners/podcast_generator``.
It is package-level because a second copy of an injection seam is how two
resolvers, two fallback rules, and two silent divergences get born — the exact
failure the Mandate system exists to end.
"""

from __future__ import annotations

import inspect
import json
from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel

from matrx_ai.agents import AgentRunResult
from matrx_ai.agents.named import AgentSource, NamedAgent, offer_view, to_template_value

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
    #: D2 — one static example of what this value looks like, declared with the
    #: provision. An ILLUSTRATION for whoever is choosing where it should land,
    #: never a default and never a fallback: nothing reads it at run time.
    example: str = ""


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


def _run_variables(agent_cls: type[NamedAgent], kwargs: dict[str, Any]) -> dict[str, Any]:
    inputs_obj = _coerce_inputs(agent_cls, kwargs)
    if inputs_obj is None:
        return {}
    return {
        key: to_template_value(value)
        for key, value in agent_cls.prepare_variables(inputs_obj).items()
    }


def _offer_view(agent_cls: type[NamedAgent], kwargs: dict[str, Any]) -> dict[str, Any]:
    """The CALL SITE's vocabulary for this run — see :func:`matrx_ai.agents.named.offer_view`.

    NOT ``_run_variables``: those are the HOLDER's variables, already renamed
    through ``variable_map``/``prepare_variables``. An offer check reads the
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


async def resolve_mandate_by_key(mandate_key: str, *, consumer: str) -> MandateResolution:
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


def _assert_offer_complete(
    agent_cls: type[NamedAgent],
    mandate_key: str,
    resolution: MandateResolution,
    kwargs: dict[str, Any],
) -> None:
    """🚨 THE SAME RULE THE HOST FUNNEL ENFORCES — see aidream
    ``services/mandates/named_agents.py::_assert_offer_complete_for_named``.

    ``offered_values`` rides the resolution precisely so this check needs no
    host import. Skipped when the resolution carries no offer (nothing was
    declared) or when the class was driven without its typed ``Inputs`` (a
    raw-kwargs call makes no offer through this funnel at all).
    """
    if not resolution.offered_values or kwargs.get("inputs") is None:
        return
    supplied = _offer_view(agent_cls, kwargs)
    missing = [
        value.name
        for value in resolution.offered_values
        if value.guaranteed and supplied.get(value.name) is None
    ]
    if missing:
        raise BrokenOfferPromise(mandate_key, agent_cls.__name__, missing)


async def run_mandated(agent_cls: type[NamedAgent], **kwargs: Any) -> AgentRunResult:
    """Run a ``NamedAgent`` through its DB-managed mandate when a resolver is installed.

    Resolves ``agent_cls.mandate_key`` to the mandate's current agent and passes it as
    ``source_override``; the mandate's ``config_overrides`` merge UNDER any
    call-site overrides, so a per-run argument (a tts voice, a model for one
    call) always wins.

    A class with no ``mandate_key`` is not mandated and runs on its own source.

    🚨 A class WITH a ``mandate_key`` must resolve. No resolver installed, or a
    resolver that fails, raises :class:`MandateResolutionUnavailable` — it never
    falls back to the id in the class body. A failure emits a red alarm and
    calls the host's injected ``record_error`` seam with
    ``mandate_resolution_failed`` before raising.

    A modern resolver returns :class:`MandateResolution`; its completion callback
    receives the result plus the exact variables/user input after the run.
    Hosts use that callback for structural checking and exemplar capture
    without the package importing host code. Legacy two-tuples remain accepted
    for third-party compatibility but cannot provide host post-run behavior.
    """
    mandate_key = getattr(agent_cls, "mandate_key", None)
    if not mandate_key:
        return await agent_cls.run(**kwargs)

    resolution = await resolve_mandate_for(agent_cls)
    if resolution.holder_type != "agent" or resolution.source is None:
        # A NamedAgent funnel runs an AGENT record. A workflow-held mandate
        # executes through the host's workflow-mandate runner (run_mandate /
        # the ai.agent.start workflow-holder branch) — never a silent guess.
        raise MandateResolutionUnavailable(
            mandate_key,
            agent_cls.__name__,
            f"resolved to a {resolution.holder_type!r} Holder — this funnel can "
            "only run an agent record; call the mandate through the host's "
            "run_mandate (workflow Holders execute as durable child runs)",
        )
    source = resolution.source
    mandate_overrides = resolution.config_overrides
    complete = resolution.complete
    if resolution.variable_mapping:
        kwargs["variable_mapping"] = resolution.variable_mapping
    if resolution.spill_variables:
        kwargs["spill_variables"] = set(resolution.spill_variables)

    call_overrides = kwargs.pop("config_overrides", None) or {}
    merged = {**(mandate_overrides or {}), **(dict(call_overrides) if call_overrides else {})}
    kwargs["source_override"] = source
    if merged:
        kwargs["config_overrides"] = merged
    _assert_offer_complete(agent_cls, mandate_key, resolution, kwargs)
    result = await agent_cls.run(**kwargs)
    if complete is not None:
        try:
            await complete(
                result,
                _run_variables(agent_cls, kwargs),
                _capture_user_input(kwargs.get("user_input")),
            )
        except Exception as exc:  # completion cannot invalidate a delivered response
            from matrx_utils import vcprint

            vcprint(
                f"[mandates] post-run honesty callback FAILED for {mandate_key!r}: "
                f"{type(exc).__name__}: {exc}",
                color="red",
            )
    return result
