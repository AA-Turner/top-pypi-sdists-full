"""``ai.mandate.start`` — Run Mandate: run the JOB, whoever your org gave it to.

WHY THIS IS A DIFFERENT STEP FROM RUN AGENT (Arman's ruling, 2026-09-10)
-----------------------------------------------------------------------
Run Agent and Run Mandate "have nothing in common and it would be silly and
stupid to attempt to make them the same… a mandate is not a representation of
an agent. It's a representation of some sort of intelligence… Agents work with
an ID, a version number, and then mapping of inputs and outputs. And a mandate
doesn't have that sort of thing."

So:

* **Run Agent** (``ai.agent.start``) names an agent: id + version + the input
  and output mapping. It has NO mandate field, and refuses one loudly.
* **Run Mandate** (this node) names a Mandate KEY. It has no agent id and no
  version, because neither is its to choose — the database is. Its Holder may
  be an agent OR a whole workflow, and the workflow case runs as a durable
  child run (the step-side lift).

Mandates exist inside workflows for exactly one reason: so a person can tweak
ONE part of a system-wide workflow — by rebinding the job to a different doer —
without copying the workflow. Building a workflow out of mandates for its own
sake is not the point.

Everything after "which thing runs" is the SAME code Run Agent uses:
``resolve_step_agent_full`` → ``build_agent_request`` → ``run_step_agent``.
This is not a second way to run intelligence; it is the same way, entered by a
different door.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from matrx_graph.actions import register_node
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from pydantic import ConfigDict, Field

from matrx_ai._ext import get_ext, has_ext
from matrx_ai.config.request_firewall import (
    FirewallMatch,
    FirewallScope,
    FirewallTerm,
    firewall_from_step_fields,
    request_firewall_scope,
)
from matrx_ai.graph_nodes.agent_action import (
    _AGENT_RESULT_BOOKKEEPING,
    _AGENT_RESULT_QUORUM,
    _AGENT_RESULT_WITNESSES,
    AgentRunCommonInput,
    AgentStartConfig,
    StepWorkflowMandate,
    _run_workflow_held_mandate,
    _strip_inert_burned_tool_fields,
    build_agent_request,
    mandate_key_field,
    require_agent_host,
    resolve_step_agent_full,
    run_step_agent,
    step_result_version,
)
from matrx_ai.graph_nodes.iteration_limit import resolve_step_iteration_limit
from matrx_ai.graph_nodes.shared import AiExecutionResult, normalize_completed_result

logger = logging.getLogger(__name__)

_NODE_TYPE = "ai.mandate.start"


class MandateStartStrictInput(AgentRunCommonInput):
    """Run Mandate's request body: the job, plus the shared run lift.

    ``mandate_key`` is REQUIRED — a Run Mandate step with no job named is not a
    step at all. There is deliberately no ``agent_id`` and no ``is_version``:
    who does the job is the database's answer, re-asked on every run, and a
    frozen id beside it would be exactly the hardcoded agent the Mandate system
    exists to abolish.
    """

    model_config = ConfigDict(extra="forbid")

    mandate_key: str = mandate_key_field(required=True)
    #: THE STATE AT THE CALL POINT: every value the mandate's provision offers, by its offered name
    #: (Arman, 2026-10-14). The mandate's BINDING decides what the doer receives: which values, joined
    #: how, under which of its own variable names. Nothing upstream shapes values for one agent.
    provision_values: dict[str, Any] | None = Field(
        default=None,
        description=("Every value the mandate's provision offers at this point, by offered name. The "
                     "mandate's binding picks and joins them into the doer's inputs."),
    )
    #: THE REQUEST FIREWALL (2026-10-27, ``matrx_ai.config.request_firewall``): checked at the send
    #: boundary on the exact outgoing request of EVERY provider call (prompt, every message, every
    #: context block, tool results of earlier turns) and by the host's doors; a hit refuses before
    #: anything is spent and names the class, never the term. An unmatchable term refuses at start.
    must_not_contain: list[str | FirewallTerm] | None = Field(
        default=None,
        title="Must not contain",
        description=("Words the request sent to the AI must never contain — often fed from another step. "
                     "A word, or {term, class}. Any hit stops the step before it is paid for."),
    )
    must_not_contain_match: FirewallMatch = Field(
        default="folded",
        title="Match",
        description="folded: ignore case, accents and punctuation. exact: the same characters.",
    )
    no_tools: bool = Field(
        default=False,
        title="No tools",
        description="Stop the step if the agent doing the job carries any tool.",
    )
    no_auto_context: bool = Field(
        default=False,
        title="No automatic context",
        description="Stop the step if automatic context is on for the agent doing the job.",
    )


class MandateStartInput(MandateStartStrictInput):
    """Run Mandate input plus authored top-level variable connection points.

    Extras are allowed for the same reason Run Agent allows them: a workflow
    author exposes the doer's variable names as node ports, and an edge feeding
    one arrives as a top-level extra keyed by the variable name.
    """

    model_config = ConfigDict(extra="allow")


def agent_variables_outside_provision(inputs: MandateStartInput) -> list[str]:
    """The doer's variable names this step was fed OUTSIDE ``provision_values``.

    A Run Mandate step hands the mandate its STATE by the provision's offered names, and the
    mandate's BINDING decides what the doer receives (Arman, 2026-10-19). A value fed under
    the doer's own variable names (a top-level port, or the ``variables`` dict) skips the
    binding — the step is either a faked mandate (really Run Agent) or a real one bypassing
    its binding. An upstream agent result broadcast down an unmapped edge is bookkeeping,
    not variables, and is ignored here exactly as the request builder drops it.
    """
    extras = dict(inputs.model_extra or {})
    _strip_inert_burned_tool_fields(extras)
    present = [k for k in extras if k in _AGENT_RESULT_BOOKKEEPING]
    if len(present) >= _AGENT_RESULT_QUORUM and (_AGENT_RESULT_WITNESSES & set(present)):
        extras = {k: v for k, v in extras.items() if k not in _AGENT_RESULT_BOOKKEEPING}
    names = sorted(extras)
    names += sorted(f"variables.{k}" for k in (inputs.variables or {}))
    return names


def drop_state_echoes(inputs: MandateStartInput) -> MandateStartInput:
    """The step without top-level copies of the state it already hands over (defect 75, 2026-10-20).

    The graph engine hands an ENTRY node the run's input as its own top-level fields, so a Run
    Mandate step that starts a workflow and hands that same input over as ``provision_values``
    (``{"$input": name}``) also received every value a second time, by name. Those copies are not
    values fed outside the state — they ARE the state: counting them refused a correct step
    (``mandate_unresolved``, PB-02 R3), and before the refusal they rode to the doer beside the
    binding (``insurance_policy`` included). A top-level field is an echo only when the state
    carries the SAME name with the SAME value; anything else is still refused below."""
    state = inputs.provision_values
    extras = dict(inputs.model_extra or {})
    if not state or not extras:
        return inputs
    echoes = {k for k, v in extras.items() if k in state and state[k] == v}
    if not echoes:
        return inputs
    kept = {k: v for k, v in extras.items() if k not in echoes}
    return MandateStartInput.model_validate(
        {**inputs.model_dump(exclude=set(extras), exclude_none=True), **kept}
    )


def refuse_agent_variables_outside_provision(inputs: MandateStartInput, node_id: str) -> None:
    """Refuse, before anything resolves or spends, a step that feeds the doer by name."""
    names = agent_variables_outside_provision(inputs)
    if not names:
        return
    raise ValueError(
        f"{_NODE_TYPE}:{node_id} (mandate {inputs.mandate_key!r}) was fed {names} outside "
        "provision_values. A Run Mandate step hands the mandate its state — every value it has, "
        "under the provision's offered names — as provision_values, and the mandate's binding "
        "picks what the doer gets. Fix: wire those values into provision_values (in code, "
        "aidream/workflows/step_state.hand_state_to_mandate). If they are simply the agent's own "
        "inputs, one-to-one, this is not a mandate step: make it a Run Agent step "
        "(ai.agent.start) naming that agent."
    )


def _state_as_extras(inputs: MandateStartInput) -> MandateStartInput:
    """A workflow Holder takes the state on its own input surface: the provision values ride as the supplied
    offer (by offered name) and the workflow runner applies the mandate's binding to them."""
    if inputs.provision_values is None:
        return inputs
    extras = dict(inputs.model_extra or {})
    return MandateStartInput.model_validate(
        {**inputs.model_dump(exclude={"provision_values"}, exclude_none=True), **inputs.provision_values, **extras}
    )


def refuse_variables_shadowing_typed_fields(variables: dict[str, Any], where: str) -> None:
    """Refuse, at bind time, doer variables named like a typed field of the step (``store``, ``context``, ``tools``…).

    Bound variables ride as top-level extras; one named like a typed field is not a variable at all — it is parsed
    as that run setting (a type error that kills the run, or worse a value that validates and silently changes how
    the run behaves) and the doer never receives it (live 2026-10-24: ``store`` on the self-description binding)."""
    shadowing = sorted(set(variables) & set(MandateStartInput.model_fields))
    if shadowing:
        raise ValueError(
            f"{where}: the binding names doer variable(s) {shadowing} that shadow this step's typed input "
            "field(s) of the same name, so the doer would never receive them. Rename the variable on the doer and "
            "in the mandate's binding (e.g. 'store' -> 'store_collections').")


async def _bind_provision_values(inputs: MandateStartInput, resolved: Any) -> MandateStartInput:
    """Run the step's provision values (THE STATE at the point) through the mandate's BINDING (the host's
    one consumption pipeline): the variables the doer runs on replace the raw state. Edge-fed variables
    (top-level extras) still ride beside them; a binding variable of the same name wins.

    Without ``provision_values`` the step behaves exactly as before. It REFUSES, never runs unbound, when:
    the point handed an empty state (nothing was captured), the host offers no pipeline, or the mandate has
    no binding map — the default pin would hand the doer every value of the state by name.
    """
    supplied = inputs.provision_values
    if supplied is None:
        return inputs
    where = f"{_NODE_TYPE}: mandate {inputs.mandate_key!r}"
    if not supplied:
        raise ValueError(f"{where} was handed an empty state — the point before it captured nothing, so "
                         "there is nothing to bind. See that step's error.")
    materialize = getattr(resolved, "materialize", None)
    if materialize is None:
        raise ValueError(f"{where} was handed its provision values, but this host offers no consumption "
                         "pipeline to apply the mandate's binding — the doer cannot receive the state unbound.")
    if not getattr(resolved, "consumption_map", None):
        raise ValueError(f"{where} has no binding map: the whole state would reach the doer by name. Bind the "
                         "doer's inputs on the mandate's Binding tab (its default consumption map).")
    variables = await materialize(dict(supplied))
    refuse_variables_shadowing_typed_fields(variables, where)
    extras = dict(inputs.model_extra or {})
    return MandateStartInput.model_validate(
        {**inputs.model_dump(exclude={"provision_values"}, exclude_none=True), **extras, **variables}
    )


@register_node(
    name=_NODE_TYPE,
    display_name="Run Mandate",
    description=(
        "Run a named job — your organization decides which agent or workflow "
        "actually does it, looked up fresh every time this step runs."
    ),
    category=NodeCategory.AGENT,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=MandateStartInput,
    output_schema=AiExecutionResult,
    output_kind="agent_result",
    config_schema=AgentStartConfig,
    icon="target",
    tags=("ai", "mandate", "agent"),
    result_version=step_result_version,
    sample_preflight=lambda ctx, inputs, config: mandate_sample_preflight(ctx, inputs, config),
)
async def mandate_start(
    ctx: NodeExecutionContext,
    inputs: MandateStartInput,
    config: AgentStartConfig | None = None,
) -> NodeResult[AiExecutionResult]:
    require_agent_host(_NODE_TYPE)
    # MANDATE CANDIDATES — the host observes this real run: the step's inputs
    # and config are copied HERE, before the body mutates them
    # (``inputs.max_iterations``), and a candidate Holder may re-run them in the
    # background. The tap never alters the step.
    from matrx_ai.mandate_taps import tapped_door

    return await tapped_door(
        "workflow_step",
        inputs.mandate_key,
        lambda: {
            "node_type": _NODE_TYPE,
            "node_id": getattr(ctx, "node_id", None),
            "run_id": getattr(ctx, "run_id", None),
            "inputs": inputs.model_copy(),
            "config": config.model_copy() if config is not None else None,
        },
        lambda: _mandate_start_recorded(ctx, inputs, config),
    )


async def _mandate_start_recorded(
    ctx: NodeExecutionContext,
    inputs: MandateStartInput,
    config: AgentStartConfig | None,
) -> NodeResult[AiExecutionResult]:
    """EVERY FAILURE LEAVES A RECORD (defect 76, 2026-10-20). A step that fails before its Holder
    starts (a refused input, an unresolved mandate, a binding that cannot apply) kept no
    conversation and no request — the person had only a red step. The host's
    ``mandate_step_failure_recorder`` keeps the run's mandate record with the failure; a failure
    after the Holder started is the Holder run's own record. Never changes the step's outcome."""
    progress = {"holder_started": False}
    try:
        return await _mandate_start_body(ctx, inputs, config, progress)
    except Exception as exc:
        from matrx_graph.errors import GraphInterrupt

        if not progress["holder_started"] and not isinstance(exc, GraphInterrupt):
            await _record_step_failure(ctx, inputs.mandate_key, exc)
        raise


async def _record_step_failure(ctx: NodeExecutionContext, mandate_key: str, exc: BaseException) -> None:
    if not has_ext("mandate_step_failure_recorder"):
        logger.warning("[mandate step] %s failed and the host keeps no failure record: %s", mandate_key, exc)
        return
    try:
        await get_ext("mandate_step_failure_recorder")(
            mandate_key=mandate_key,
            error=exc,
            workflow_run_id=str(getattr(ctx, "run_id", "") or "") or None,
            node_id=getattr(ctx, "node_id", None),
        )
    except Exception:  # noqa: BLE001 — a record never changes the step's outcome
        logger.exception("[mandate step] %s: the failure record could not be written", mandate_key)


async def mandate_sample_preflight(
    ctx: NodeExecutionContext,
    inputs: MandateStartInput,
    config: AgentStartConfig | None = None,
) -> dict[str, Any] | None:
    """THE FIREWALL ON A SAMPLED STEP. A TEST run answers this step from its declared sample, but
    its request firewall must still be provable without spending: the step's normal body runs in
    capture mode (``capturing_provider_request``, ``store=False``, a muted emitter) — every door
    check, the send boundary's ``check_at_send`` and the dispatch check run on the request it
    WOULD send, and the transport stops it, so nothing is sent, spent or stored. A refusal raises
    exactly as the live call would; a clean scan returns ``{"request_firewall": [...]}`` for the
    sampled outcome. A step with no firewall checks nothing here (None)."""
    firewall = firewall_from_step_fields(
        inputs.must_not_contain,
        match=inputs.must_not_contain_match,
        no_tools=inputs.no_tools,
        no_auto_context=inputs.no_auto_context,
    )
    if firewall is None:
        return None
    import copy

    from matrx_connect.emitters.silent_emitter import SilentEmitter

    from matrx_ai.providers.request_capture import (
        PaidSendBlockedInCapture,
        capturing_provider_request,
    )

    capture_ctx = copy.copy(ctx)
    override = getattr(ctx.app, "with_overrides", None)
    if callable(override):
        capture_ctx.app = override(emitter=SilentEmitter(), store=False)
    node_id = getattr(ctx, "node_id", None) or "?"
    with capturing_provider_request():
        try:
            records = await _mandate_start_body(capture_ctx, inputs.model_copy(deep=True), config, capture=True)
        except PaidSendBlockedInCapture as blocked:
            raise ValueError(
                f"{_NODE_TYPE}:{node_id} (mandate {inputs.mandate_key!r}) is answered from its sample, "
                f"but its request firewall could not be checked: the run makes a paid call "
                f"({blocked.method} {blocked.url}) before its request, which a check never makes."
            ) from None
    return {"request_firewall": records}


async def _mandate_start_body(
    ctx: NodeExecutionContext,
    inputs: MandateStartInput,
    config: AgentStartConfig | None,
    progress: dict[str, bool] | None = None,
    *,
    capture: bool = False,
) -> Any:
    """The step's body. ``capture`` (``mandate_sample_preflight`` only): the request is built and
    run to the transport inside the firewall scope, never answered from a replay and never sent;
    returns the scan records instead of a result."""
    progress = progress if progress is not None else {}
    node_id = getattr(ctx, "node_id", None) or "?"
    inputs = drop_state_echoes(inputs)
    refuse_agent_variables_outside_provision(inputs, node_id)
    resolved = await resolve_step_agent_full(
        inputs,
        consumer=f"{_NODE_TYPE}:{node_id}",
        # A Mandate's Holder is legitimately a whole workflow. This is the node
        # type that knows how to run that lane, so it is the one that opts in.
        allow_workflow_holder=has_ext("workflow_mandate_runner"),
    )
    declared_variables = list(getattr(config, "exposed_variables", None) or [])
    firewall = firewall_from_step_fields(
        inputs.must_not_contain,
        match=inputs.must_not_contain_match,
        no_tools=inputs.no_tools,
        no_auto_context=inputs.no_auto_context,
    )
    if isinstance(resolved, StepWorkflowMandate):
        if firewall is not None:
            raise ValueError(
                f"{_NODE_TYPE}:{node_id} (mandate {inputs.mandate_key!r}) has a request firewall, but "
                "this job is done by a whole workflow, whose many AI calls this step cannot check. "
                "Give the job to an agent, or put the firewall on the AI steps inside that workflow."
            )
        if capture:
            return None
        progress["holder_started"] = True
        return await _run_workflow_held_mandate(
            ctx, _state_as_extras(inputs), resolved, declared_variables=declared_variables
        )
    limit = await resolve_step_iteration_limit(ctx, inputs.max_iterations)
    inputs.max_iterations = limit.value
    inputs = await _bind_provision_values(inputs, resolved)
    request = build_agent_request(
        ctx,
        inputs,
        resolved,
        node_type=_NODE_TYPE,
        declared_variables=declared_variables,
        variable_sources=dict(getattr(config, "variable_sources", None) or {}),
        # The step's declared opt-out of the ~5k-token ``<org_catalog>`` intro (and the
        # ``scope_system`` reader it brings). Dropped here until 2026-10-27, so every Run Mandate
        # step carried the catalog even with ``include_org_catalog: false``.
        include_org_catalog=getattr(config, "include_org_catalog", True),
    )
    # AI TEST MODE — the host may answer this exact step from a recorded test baseline (opt-in per
    # test session only; ``mandate_taps.MandateReplay``). Not installed / real mode → None → real run.
    from matrx_ai.mandate_taps import replay_lookup, replay_store

    run_id = getattr(ctx, "run_id", None)
    fingerprint = {
        "inputs": inputs.model_dump(mode="json", exclude_none=True),
        "agent_id": resolved.agent_id,
        "is_version": resolved.is_version,
        "config_overrides": resolved.config_overrides or {},
        "declared_variables": declared_variables,
        "variable_sources": dict(getattr(config, "variable_sources", None) or {}),
    }
    replayed = None if capture else await replay_lookup("workflow_step", inputs.mandate_key, run_id, fingerprint)
    if replayed is not None:
        return success(AiExecutionResult.model_validate(replayed))

    progress["holder_started"] = True
    if capture and hasattr(request, "store"):
        request.store = False
    from matrx_ai.providers.request_capture import ProviderRequestCaptured

    with request_firewall_scope(firewall, mandate_key=inputs.mandate_key) as scope:
        try:
            completed = await run_step_agent(
                ctx,
                resolved.agent_id,
                request,
                mandate_key=inputs.mandate_key,
                run_stamp=resolved.run_stamp,
            )
        except ProviderRequestCaptured:
            if not capture:
                raise
            completed = None
        except Exception as exc:
            if scope is not None and scope.refusals:
                raise scope.refusals[-1] from exc
            raise
    firewall_records = _firewall_outcome(scope, inputs.mandate_key, node_id)
    if capture:
        return firewall_records

    # A host agent_runner may return an ALREADY-normalized AiExecutionResult
    # (a compiled Orchestra whose final step IS the result). Pass it through.
    if isinstance(completed, AiExecutionResult):
        completed.metadata.setdefault("agent_id", resolved.agent_id)
        if firewall_records is not None:
            completed.metadata["request_firewall"] = firewall_records
        await replay_store("workflow_step", inputs.mandate_key, run_id, fingerprint,
                           completed.model_dump(mode="json"))
        return success(completed)
    # ``config`` carries the author's ``allow_empty_structured_output`` into the all-zero refusal,
    # exactly as Run Agent passes it (the field is on the shared AgentStartConfig).
    result = await asyncio.to_thread(normalize_completed_result, completed, step_config=config)
    # WHO did the job: the doer the database resolved for this run (a research
    # row records it as agent_id, exactly as the research code path does).
    payload = getattr(result, "result", None)
    if isinstance(payload, AiExecutionResult):
        payload.metadata["agent_id"] = resolved.agent_id
        if firewall_records is not None:
            payload.metadata["request_firewall"] = firewall_records
        await replay_store("workflow_step", inputs.mandate_key, run_id, fingerprint,
                           payload.model_dump(mode="json"))
    return limit.name_on(result)


def _firewall_outcome(scope: FirewallScope | None, mandate_key: str, node_id: str) -> list[dict[str, Any]] | None:
    """What the request firewall scanned (door records first, then one per provider call the send
    boundary cleared), for the step outcome — or a refusal the host turned into a failed result,
    raised as itself. BACKSTOP: the send boundary refuses before any unscanned call, so a run with
    neither a door record nor a cleared send reached no provider through it — never trusted."""
    if scope is None:
        return None
    if scope.refusals:
        raise scope.refusals[-1]
    if not scope.records and not scope.sends:
        raise ValueError(
            f"{_NODE_TYPE}:{node_id} (mandate {mandate_key!r}) ran, but no dispatch door checked its "
            "request firewall, so nothing proves the request was clean. Its answer is not used. This "
            "host's agent runner does not run the firewall; report it."
        )
    return [record.to_dict() for record in (*scope.records, *scope.sends)]
