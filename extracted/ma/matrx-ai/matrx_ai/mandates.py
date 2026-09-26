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
from dataclasses import dataclass, field
from typing import Any, NoReturn

from pydantic import BaseModel

from matrx_ai.agents import AgentRunResult
from matrx_ai.agents.named import AgentSource, NamedAgent, offer_view, to_template_value
from matrx_ai.orchestrator.mandate_carrier import mandate_carrier_passthrough

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
    #: The host's ONE consumption pipeline for a code call site that builds its
    #: own request (aidream ``consumption.run_variables_for_mandate``): the
    #: binding's consumption map, the provision's guaranteed values and the
    #: required-input gate, applied to the site's offered values. Returns the
    #: variables the Holder runs on, or raises in words. ``None`` = the host
    #: offers no pipeline, and the site's values pass by name.
    materialize: Callable[[dict[str, Any]], Awaitable[dict[str, Any]]] | None = None
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
    #: Values the binding SPILLS into the user text (``spill_variables``): a
    #: site composing its own user turn appends this; ``run_held_call`` does.
    spilled_text: str | None = None
    #: The host's post-run honesty callback for this exact pin (required output
    #: keys, exemplar capture). Called by :meth:`finish`.
    complete: MandateCompletion | None = None
    #: Every variable the Holder DECLARES, as it resolved for this call (the
    #: site's offered value, else the Holder's own default). A Holder-authored
    #: text that is not a turn (a retry nudge, a per-turn budget line) lives here
    #: as a variable default; :meth:`authored_text` reads it.
    holder_values: dict[str, str] = field(default_factory=dict)

    # ── THE ONE PRECEDENCE RULE for every held call (2026-09-25) ───────────
    # The Holder's settings apply. A caller's value wins ONLY when it was
    # explicitly set (a workflow author's node field, an API request field) —
    # never a code default dressed up as a choice.

    def pick_model(self, explicit: str | None = None) -> str:
        return explicit or self.model

    def pick_temperature(self, explicit: float | None = None) -> float | None:
        return explicit if explicit is not None else self.temperature

    def pick_max_tokens(self, explicit: int | None = None, *, unset: int) -> int:
        """``unset`` is what the funnel needs when BOTH the caller and the
        Holder leave the ceiling unset — the funnel's own default, not a choice."""
        if explicit is not None:
            return explicit
        return self.max_output_tokens if self.max_output_tokens else unset

    def user_text(self, text: str) -> str:
        """The site's user turn plus whatever the binding spills into it."""
        return f"{text}\n\n{self.spilled_text}" if self.spilled_text else text

    def authored_user(self) -> str:
        """The user turn the HOLDER authors, the site's values applied.

        For a site whose framing text ("Below is a case…", "## Your Task…")
        lives on the Holder, not in code: the site offers only the data as
        variables (``hold_code_call(variables=...)``) and sends this. A Holder
        rebound to an agent that authors no user turn is refused in words —
        never an empty prompt sent to a model.
        """
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

        # One pass: a value's own braces are data, never re-filled.
        return substitute_authored(str(text), str(text), values, prompt_safe_value)

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
        invalidate a delivered response, but a failure is said out loud.
        """
        if self.complete is None:
            return
        result = AgentRunResult(
            success=success,
            output=output or "",
            model_id=self.model,
            parsed=parsed,
            error=error,
            error_kind="provider" if not success else None,
        )
        try:
            await self.complete(result, dict(self.variables), self.spilled_text)
        except Exception as exc:  # noqa: BLE001 — see docstring
            from matrx_utils import vcprint

            vcprint(
                f"[mandates] post-run honesty callback FAILED for {self.mandate_key!r}: "
                f"{type(exc).__name__}: {exc}",
                color="red",
            )


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
    if resolution.holder_type != "agent" or resolution.source is None:
        await _refuse_code_call(
            mandate_key,
            consumer,
            f"it resolved to a {resolution.holder_type!r} Holder, and a code call needs an "
            "AGENT Holder to take its model and instructions from — rebind it to an agent",
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
    # A binding that carries a consumption map re-routes the site's offered
    # values, so the host's ONE pipeline decides what the Holder receives (and
    # refuses a context/media route this call site cannot deliver). With no map
    # — the default pin — values pass by name, exactly as for run_mandated.
    if resolution.consumption_map and resolution.materialize is not None:
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
    agent.with_variables(**held_variables)
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
            text = "\n".join(
                str(part.get("text") or "")
                for part in content
                if isinstance(part, dict) and part.get("type") == "text"
            )
        else:
            text = str(content or "")
        turns.append({"role": role, "content": text})
    carried: dict[str, Any] = dict(metadata or {})
    carried[MANDATE_KEY_METADATA_KEY] = mandate_key
    carried[MANDATE_HOLDER_METADATA_KEY] = {
        "mandate_key": mandate_key,
        "holder_type": "agent",
        "agent_id": str(getattr(resolution.source, "agent_id", "") or ""),
        "is_version": bool(getattr(resolution.source, "is_version", False)),
        "name": getattr(agent, "name", None),
        "consumer": consumer,
    }
    return HeldCall(
        mandate_key=mandate_key,
        model=model,
        system=system,
        temperature=getattr(config, "temperature", None),
        max_output_tokens=getattr(config, "max_output_tokens", None),
        turns=turns,
        config=config,
        metadata=carried,
        variables=held_variables,
        spilled_text=bound.spilled_text or None,
        complete=resolution.complete,
        holder_values=holder_values,
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
)


def held_request_config(
    held: HeldCall,
    *,
    extra_turns: list[dict[str, Any]] | None = None,
    stream: bool = False,
    max_output_tokens: int | None = None,
) -> Any:
    """The whole request a held call sends, built ONLY from its Holder.

    ``hold_code_call`` hands back the model, prompt and sampling knobs; a site
    that needs the Holder's OTHER settings too — its reasoning effort, its
    response format (JSON mode), its authored few-shot turns — sends this
    instead of re-typing any of them. ``extra_turns`` are the run's own turns
    (the text being processed), appended after the Holder's authored ones.
    ``max_output_tokens`` is a run-scope ceiling a caller may lower, never a
    default: when omitted the Holder's own ceiling applies.
    """
    from matrx_ai.config import UnifiedConfig

    cfg: dict[str, Any] = {
        "model": held.model,
        "system_instruction": held.system,
        "messages": [
            *held.turns,
            *(extra_turns or []),
            *([{"role": "user", "content": held.spilled_text}] if held.spilled_text else []),
        ],
        "stream": stream,
    }
    ceiling = max_output_tokens if max_output_tokens is not None else held.max_output_tokens
    if ceiling is not None:
        cfg["max_output_tokens"] = ceiling
    if held.temperature is not None:
        cfg["temperature"] = held.temperature
    for knob in _HELD_KNOBS:
        value = getattr(held.config, knob, None)
        if value not in (None, [], ""):
            cfg[knob] = value
    return UnifiedConfig.from_dict(cfg)


@mandate_carrier_passthrough(
    "the HeldCall handed in IS the resolved Holder (hold_code_call); its metadata names it"
)
async def run_held_call(
    held: HeldCall,
    *,
    extra_turns: list[dict[str, Any]] | None = None,
    max_output_tokens: int | None = None,
    store: bool = False,
) -> Any:
    """Run one held call to completion and return the normalized result.

    One turn, no tools, not streamed to any listener — the shape of a code call
    (a labeler, a cleaner, an observer). Returns ``AiExecutionResult``:
    ``final_text`` plus the usage the funnel measured. The metadata names the
    Holder, so the runtime carrier gate and ``chat.request`` both record who
    held it.
    """
    import asyncio

    from matrx_ai.graph_nodes.shared import normalize_completed
    from matrx_ai.orchestrator.executor import execute_ai_request

    from matrx_connect.context.app_context import (
        clear_app_context,
        set_app_context,
        try_get_app_context,
    )
    from matrx_connect.emitters.console_emitter import ConsoleEmitter

    # A code call belongs to no listener: whatever stream the surrounding
    # request owns (a person's chat) must never receive this call's events.
    parent = try_get_app_context()
    token = None
    if parent is not None:
        token = set_app_context(
            parent.with_overrides(
                emitter=ConsoleEmitter(label=f"held:{held.mandate_key}", debug=False),
                store=store,
            )
        )
    try:
        completed = await execute_ai_request(
            held_request_config(
                held, extra_turns=extra_turns, max_output_tokens=max_output_tokens
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


@mandate_carrier_passthrough(
    "the HeldCall handed in IS the resolved Holder (hold_code_call); its metadata names it"
)
async def run_held_pydantic(
    held: HeldCall,
    *,
    output_cls: type[Any],
    user: str | None = None,
    messages: list[dict[str, Any]] | None = None,
    model: str | None = None,
    max_tokens: int | None = None,
    temperature: float | None = None,
    unset_max_tokens: int = 8092,
    system: str | None = None,
    metadata: dict[str, Any] | None = None,
    **funnel_kwargs: Any,
) -> Any:
    """A held strict-JSON call: the Holder's settings, the one precedence rule,
    the binding's spill, and the post-run check — in one place.

    ``model`` / ``max_tokens`` / ``temperature`` are EXPLICIT caller overrides
    (a workflow author's field, an API request's field) and win only when set.
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
        "system": held.system if system is None else system,
        "output_cls": output_cls,
        "max_tokens": held.pick_max_tokens(max_tokens, unset=unset_max_tokens),
        "temperature": held.pick_temperature(temperature),
        "metadata": {**(metadata or {}), **held.metadata},
        **funnel_kwargs,
    }
    try:
        if messages is None:
            value = await funnel.llm_to_pydantic(user=held.user_text(user or ""), **common)
        else:
            if held.spilled_text:
                messages = [*messages, {"role": "user", "content": held.spilled_text}]
            value = await funnel.llm_messages_to_pydantic(messages=messages, **common)
    except Exception as exc:
        await held.finish(
            getattr(exc, "raw_output", "") or "",
            success=False,
            error=f"{type(exc).__name__}: {exc}"[:500],
        )
        raise
    dumped = value.model_dump(mode="json") if hasattr(value, "model_dump") else value
    await held.finish(json.dumps(dumped, ensure_ascii=False, default=str), parsed=dumped)
    return value


@mandate_carrier_passthrough(
    "the HeldCall handed in IS the resolved Holder (hold_code_call); its metadata names it"
)
async def run_held_text(
    held: HeldCall,
    *,
    user: str,
    model: str | None = None,
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
