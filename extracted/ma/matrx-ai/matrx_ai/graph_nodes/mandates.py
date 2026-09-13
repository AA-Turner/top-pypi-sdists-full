"""THE HOLDER OF A WORKFLOW'S AI STEPS — one mandate, named here, RESOLVED here.

WHY THIS EXISTS
---------------
A workflow's AI step nodes (extract, llm, chat, image, video, tts, the agent
loop) reached the provider through ``execute_ai_request`` carrying nothing but
a model id read out of the node's config. No mandate key, no agent, no Holder —
so no scanner could find them, no admin could rebind them, and one of them
shipped ``"gpt-4o-mini"`` hard-coded in code as its default. `D20
</systems/mandates/DECISIONS.md>`_: intelligence outside a Mandate is a defect
row, never an approved class.

WHAT THIS IS, AND WHAT IT IS NOT
--------------------------------
``workflow.step_intelligence`` is the Mandate that HOLDS those calls. It is
declared, with its goal and its provision, in aidream — see
``aidream/workflows/mandates.py``, which imports the constant below so the key
is spelled exactly once in the platform and the mandate scanner resolves every
call site to it.

**A key is a name; a Holder is what runs.** For one day (2026-09-11) the nodes
carried the key as ``execute_ai_request(mandate_key=...)`` and resolved nothing,
so a Holder an admin bound would have changed nothing about any run — the
coverage board could read green over a label. :func:`hold_step` closes that:
every step RESOLVES the mandate on every run through the one door every Run
Mandate step already uses (``matrx_ai.mandates.resolve_mandate_by_key``), loads
the Holder, and stamps it onto the request metadata so the persisted request
names who held it. The runtime gate ``matrx_ai.orchestrator.mandate_carrier``
records ``mandate_carried_unresolved`` for any call that names the key without
that stamp, so the label-only shape cannot come back silently.

**No Holder at any rung → the step SCREAMS and RUNS, never refuses.** This
mandate is SEEDLESS ON PURPOSE and red until an admin binds one (D21, declared
that way in ``aidream/workflows/mandates.py``), and an authored step already
carries the model and instructions its author chose — so unbound is the
mandate's DECLARED state and there is a correct thing to run. The unbound case
files one ``mandate_holder_unbound`` row and stamps ``mandate_unheld`` on the
request; it never becomes a 500. That is D20 ("we'll live with the ones we've
got") and D23 ("scream loud and red and REPORT… but without blocking"). For one
afternoon (2026-09-12) it refused instead, and every authored ``ai.*`` step on
production died at its first AI node. A mandate whose Holder IS the work — a
Run Mandate step, ``aidream.services.mandates.named_agents`` — still resolves
or refuses, because there nothing else could run.

**The Holder is what an authored step is when its author says nothing.** The
workflow AUTHOR chose the model and the instructions on the node, and that
choice stays exactly where it is: the run-scope layer, the top rung of the
precedence walk (agent definition → binding overrides → mandate pins, with
run-scope config winning — ``/systems/mandates/RUNTIME.md`` § THE PINS LAW,
which also forbids a mandate from ever naming a model in code). The Holder's
definition and the winning binding's ``config_overrides`` fill only the fields
the step LEFT UNSET, and only fields the step type has (an image step has no
system instruction to fill). The Mandate names WHO is accountable for the
call and supplies the floor; the node still names WHAT runs it.

The key lives in matrx-ai (never a declaration — matrx-ai never imports aidream)
so the nodes that carry it and the host that declares it read the same string.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from matrx_utils import vcprint

from matrx_ai.config.output_ceiling import enforce_document_ceiling

#: The Mandate that holds every runtime AI step of an authored workflow.
#: Declared in ``aidream/workflows/mandates.py``; spelled here once.
WORKFLOW_STEP_INTELLIGENCE_MANDATE = "workflow.step_intelligence"


def step_metadata(
    metadata: dict[str, Any] | None = None,
    *,
    spec_type: str,
) -> dict[str, Any]:
    """The node's metadata, saying WHICH KIND of step produced the call.

    The Holder travels as the ``mandate_key=`` argument to
    ``execute_ai_request`` — one carrier, named at the call, where a static
    resolver can read it. This only adds the step type, so any report (a bypass
    row, a usage row, the references board) can say "ai.extract" instead of
    naming a file. A ``spec_type`` already on the caller's metadata wins.

    It also stamps ``continuable: False``, because THAT IS WHAT A WORKFLOW STEP
    IS: there is no conversation here and no next turn, so a reply cut off at
    the output ceiling must never be answered with "ask me to continue".
    (Live 2026-09-12, run 2cf711eb…, step "Montessori asks": a parent was told
    exactly that, inside a run with nobody to ask, and saw four of her seven
    questions.) Every AI graph node reaches a provider through ``hold_step``,
    so stamping it here covers all of them and every node added later.
    """
    from matrx_ai.config.finish_reason import CONTINUABLE_METADATA_KEY

    carried: dict[str, Any] = dict(metadata or {})
    if not str(carried.get("spec_type") or "").strip():
        carried["spec_type"] = spec_type
    carried[CONTINUABLE_METADATA_KEY] = False
    return carried


def _declared_output_schema(step: dict[str, Any]) -> Any:
    """The JSON Schema this step forces its answer into, or ``None`` for prose.

    Reads the ``response_format`` the node already built — ``{"type":
    "json_schema", "json_schema": {"name": …, "schema": {...}}}`` — plus the
    bare ``output_schema`` some nodes carry. ``None`` means free prose, which
    ``document_output_reason`` treats as a document here because a workflow
    step has nowhere to continue.
    """
    fmt = step.get("response_format")
    if isinstance(fmt, dict):
        inner = fmt.get("json_schema")
        if isinstance(inner, dict):
            return inner
        if fmt.get("type") not in (None, "text"):
            return fmt
    schema = step.get("output_schema")
    return schema if isinstance(schema, dict) and schema else None


async def model_output_maximum(model_id_or_name: Any) -> int | None:
    """The model's REAL output maximum (``ai.model_definition.max_tokens``), or
    ``None`` when the catalog cannot say.

    ``None`` is a deliberate no-op for the document-ceiling floor: inventing a
    maximum it could not read would be worse than staying quiet, and the
    release-health audit still catches the row.
    """
    if not model_id_or_name:
        return None
    try:
        from matrx_ai.db.ai_models.ai_model_manager import ai_model_manager_instance

        row = await ai_model_manager_instance.load_model(str(model_id_or_name))
        value = getattr(row, "max_tokens", None)
        return int(value) if isinstance(value, int | float) and value > 0 else None
    except Exception as exc:  # noqa: BLE001 — never fail a step over a guard's lookup
        vcprint(
            f"document-ceiling floor could not read max_tokens for {model_id_or_name}: {exc}",
            color="yellow",
        )
        return None


@dataclass(frozen=True, slots=True)
class HeldStep:
    """An authored step with its Holder resolved: the config to run and the
    metadata that names who held it."""

    config: dict[str, Any]
    metadata: dict[str, Any]
    #: The step fields the Holder (or its binding) filled because the author
    #: left them unset. Empty is the normal case: the author said everything.
    filled_by_holder: tuple[str, ...] = field(default=())


def _holder_identity(resolution: Any, agent: Any) -> dict[str, Any]:
    source = resolution.source
    return {
        "mandate_key": WORKFLOW_STEP_INTELLIGENCE_MANDATE,
        "holder_type": "agent",
        "agent_id": str(getattr(source, "agent_id", "") or ""),
        "is_version": bool(getattr(source, "is_version", False)),
        "name": getattr(agent, "name", None),
    }


async def hold_step(
    step: dict[str, Any],
    *,
    spec_type: str,
    consumer: str,
    metadata: dict[str, Any] | None = None,
) -> HeldStep:
    """Resolve the Holder of ``workflow.step_intelligence`` for one authored step.

    ``step`` is the node's own config dict — exactly what it would have handed
    ``UnifiedConfig.from_dict``. Every key present with a ``None`` value is a
    field the author left unset; the winning binding's ``config_overrides``
    fill those first, then the Holder agent's own definition. A key the step
    does not carry is never added (the step type's schema is the ceiling), and
    a value the author set is never touched (run scope wins).

    **It NEVER refuses.** When no Holder is bound at any rung, when the Holder
    is a workflow (an authored step needs an agent to stand on), or when the
    Holder cannot be loaded, the step runs on the configuration ITS OWN AUTHOR
    chose — which is a real, complete, deliberate answer, not a seed fallback
    and not an invented default — and the missing Holder is SCREAMED: a red
    terminal block, a logger line, one ``ops.system_error`` row of kind
    ``mandate_holder_unbound`` per code path, and a ``mandate_unheld`` stamp on
    the request metadata the persistence layer already writes, so no screen can
    ever say "Held by X" over a run nobody held.

    Why refusing is the wrong floor, in the platform's own words:
    ``workflow.step_intelligence`` is **SEEDLESS ON PURPOSE and red until bound**
    (``aidream/workflows/mandates.py``, D21 — "unreachable or broken is tracked
    exactly like real, plus a red flag"), so the unbound state is the DECLARED,
    INTENDED state of this mandate, not an error. D20 keeps today's inventory a
    fix list rather than a licence to 500, and D23 rules the whole class:
    scream loud and red and REPORT, never block. Live on 2026-09-12 the
    refusing shape took down every authored ``ai.*`` step on production (run
    fbe577d6…, definition 129a4ec1… "Montessori Parenting Adviser", node
    ``ask_questions``) — a parent asking for help got an outage so the platform
    could enforce a list it had already agreed to work off.

    This is NOT the rule for a Run Mandate step or any other mandate whose
    Holder IS the work (``aidream.services.mandates.named_agents``): those
    resolve or they refuse, because without a Holder there is nothing to run.
    Here there is: the author already said what to run.
    """
    from matrx_ai.mandates import MandateResolutionUnavailable, resolve_mandate_by_key
    from matrx_ai.orchestrator.mandate_carrier import (
        MANDATE_HOLDER_METADATA_KEY,
        MANDATE_UNHELD_METADATA_KEY,
        record_unheld_step,
    )

    unheld: dict[str, Any] | None = None
    resolution = None
    agent = None
    try:
        resolution = await resolve_mandate_by_key(
            WORKFLOW_STEP_INTELLIGENCE_MANDATE, consumer=consumer
        )
        if resolution.holder_type != "agent" or resolution.source is None:
            raise MandateResolutionUnavailable(
                WORKFLOW_STEP_INTELLIGENCE_MANDATE,
                consumer,
                f"it resolved to a {resolution.holder_type!r} Holder, and an authored step "
                "needs an AGENT Holder to stand on — rebind the mandate to an agent",
            )
        try:
            agent = await resolution.source.load()
        except Exception as exc:  # noqa: BLE001 — every load failure is one shape
            raise MandateResolutionUnavailable(
                WORKFLOW_STEP_INTELLIGENCE_MANDATE,
                consumer,
                f"its Holder could not be loaded: {type(exc).__name__}: {exc}",
            ) from exc
    except Exception as exc:  # noqa: BLE001 — an unbound mandate never fails a run
        resolution = None
        agent = None
        unheld = record_unheld_step(
            mandate_key=WORKFLOW_STEP_INTELLIGENCE_MANDATE,
            consumer=consumer,
            spec_type=spec_type,
            model=str(step.get("model") or ""),
            detail=f"{type(exc).__name__}: {exc}",
        )

    merged = dict(step)
    filled: list[str] = []
    if resolution is not None:
        holder_config = getattr(agent, "config", None)
        binding_overrides = dict(resolution.config_overrides or {})
        for key, value in step.items():
            if value is not None:
                continue
            candidate = binding_overrides.get(key)
            if candidate is None and holder_config is not None:
                candidate = getattr(holder_config, key, None)
                if callable(candidate):
                    candidate = None
            if candidate is None:
                continue
            merged[key] = candidate
            filled.append(key)

    # THE DOCUMENT-CEILING FLOOR FOR AUTHORED STEPS. A step whose output is a
    # DOCUMENT — free prose, or a declared schema carrying an array or a
    # free-form string — has a length decided by its INPUT, so no ceiling an
    # author types can be right; and unlike a chat, a cut here is final. Live
    # 2026-09-12, run 2cf711eb…: the Masterwork Conductor authored one step at
    # 1,200 tokens (a parent lost three of seven questions) and another at
    # 2,500 (its JSON never closed and the whole run errored). A BOUNDED schema
    # keeps its cost knob. Reconciled + screamed, never raised — the ruling is
    # in `matrx_ai.config.output_ceiling`.
    model_max = await model_output_maximum(merged.get("model"))
    declared_schema = _declared_output_schema(merged)
    # Node config spells the ceiling both ways ("max_tokens" on ai.llm.chat,
    # "max_output_tokens" on the config-shaped nodes); both are the same knob.
    for ceiling_key in ("max_tokens", "max_output_tokens"):
        for repair in enforce_document_ceiling(
            merged,
            model_max=model_max,
            output_schema=declared_schema,
            continuable=False,
            key=ceiling_key,
            label=f"{spec_type} step ({consumer})",
        ):
            vcprint(
                repair,
                title="⚠️ WORKFLOW STEP: output ceiling raised to the model maximum",
                color="yellow",
                log_level="WARNING",
            )

    carried = step_metadata(metadata, spec_type=spec_type)
    if unheld is not None:
        # NEVER a Holder identity — nothing held this call. The unheld record is
        # its own key so the persisted request, the admin screen and the runtime
        # gate all read the same true sentence.
        carried[MANDATE_UNHELD_METADATA_KEY] = unheld
        return HeldStep(config=merged, metadata=carried, filled_by_holder=())
    identity = _holder_identity(resolution, agent)
    if filled:
        identity["filled"] = list(filled)
    carried[MANDATE_HOLDER_METADATA_KEY] = identity
    return HeldStep(config=merged, metadata=carried, filled_by_holder=tuple(filled))
