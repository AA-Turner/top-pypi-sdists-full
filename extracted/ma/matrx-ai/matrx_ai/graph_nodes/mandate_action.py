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
from matrx_graph.knobs import MAX_STEP_SECONDS
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, success
from pydantic import ConfigDict, Field, JsonValue

from matrx_ai._ext import get_ext, has_ext
from matrx_ai.graph_nodes.agent_action import (
    _AGENT_RESULT_BOOKKEEPING,
    _AGENT_RESULT_QUORUM,
    _AGENT_RESULT_WITNESSES,
    AgentRunCommonInput,
    AgentStartConfig,
    StepProtectionInput,
    StepWorkflowMandate,
    _run_workflow_held_mandate,
    _strip_inert_burned_tool_fields,
    build_agent_request,
    mandate_key_field,
    refuse_if_mandate_paused,
    require_agent_host,
    resolve_step_agent_full,
    run_sampled_firewall_check,
    run_walled_step_agent,
    firewall_before_replay,
    record_served_answer,
    step_firewall,
    step_firewall_key,
    step_result_version,
)
from matrx_ai.graph_nodes.iteration_limit import resolve_step_iteration_limit
from matrx_ai.graph_nodes.shared import (
    UNUSABLE_ANSWER_RETRY,
    AiExecutionResult,
    normalize_completed_result,
)

logger = logging.getLogger(__name__)

_NODE_TYPE = "ai.mandate.start"


class MandateStartStrictInput(AgentRunCommonInput, StepProtectionInput):
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
    provision_values: dict[str, JsonValue] | None = Field(
        default=None,
        description=("Every value the mandate's provision offers at this point, by offered name. The "
                     "mandate's binding picks and joins them into the doer's inputs."),
    )
    #: ON ERROR, CONTINUE WITH THE ERROR. Off (the default): a doer that is refused or fails fails the
    #: step, and the run stops there. On: the step SUCCEEDS with no answer and says what happened in
    #: ``metadata`` (``failed: true``, ``error`` = the one sentence a person reads, ``error_code``,
    #: ``error_details``), with whatever was billed in ``usage`` — so the workflow's own next step can
    #: record the failure (a "failed" row with its reason) the way the code it replaces does. Only the
    #: doer's failed turn, and a job nobody holds (refusal ``unfulfilled``), are carried; a step that is
    #: wired wrong still fails loudly.
    continue_on_failure: bool = Field(
        default=False,
        description=("When the agent is refused or fails, finish this step anyway with no answer and "
                     "the reason in metadata.error, so a later step can record the failure."),
    )
    # THE REQUEST FIREWALL (must_not_contain, must_not_contain_match, no_tools, no_auto_context):
    # declared once on ``StepProtectionInput``, shared with Run Typed Agent, enforced by
    # ``run_walled_step_agent`` on both.


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


def mandate_wiring_issues(definition: Any) -> list[Any]:
    """Run Mandate steps a SAVED definition feeds by the doer's own names — ERRORS naming step, keys and what it takes.

    The save-time twin of ``refuse_agent_variables_outside_provision``: the SAME rule (``agent_variables_outside_provision``)
    applied to the names a step is handed by its fixed inputs and its connections' field links, so a wiring that can
    only fail at run time (live 2026-11-17: Company Setup fed ['policies','request']) is named when it is saved.
    A name the step also carries in its fixed ``provision_values`` is an echo, as at run time, and passes.
    """
    from matrx_graph.types.primitives import EdgeKind
    from matrx_graph.validation import ValidationIssue

    typed = set(MandateStartInput.model_fields)
    issues: list[ValidationIssue] = []
    nodes = {n.id: n for n in definition.nodes if getattr(n, "spec_type", None) == _NODE_TYPE}
    for node_id, node in nodes.items():
        fixed = node.data.get("input") if isinstance(node.data.get("input"), dict) else node.data.get("inputs")
        fixed = dict(fixed) if isinstance(fixed, dict) else {}
        state = fixed.get("provision_values") if isinstance(fixed.get("provision_values"), dict) else {}
        fed: dict[str, str] = {}  # name -> where it came from
        for key in fixed:
            fed[str(key)] = "its fixed input"
        for edge in definition.edges:
            mappings = edge.data.get("mappings")
            if edge.target != node_id or edge.kind is EdgeKind.STREAM or not isinstance(mappings, dict):
                continue
            for key in mappings:
                fed.setdefault(str(key), f"connection '{edge.id}' from '{edge.source}'")
        probe = {
            "mandate_key": str(fixed.get("mandate_key") or "x"),
            **{k: "" for k in fed if k not in typed and not k.startswith("__") and k not in state},
        }
        if isinstance(fixed.get("variables"), dict):
            probe["variables"] = {str(k): "" for k in fixed["variables"]}
        names = agent_variables_outside_provision(MandateStartInput.model_validate(probe))
        if not names:
            continue
        where = sorted({fed.get(n.removeprefix("variables."), "its fixed input") for n in names})
        issues.append(
            ValidationIssue(
                path=f"nodes[{node_id}].data",
                node_id=node_id,
                code="mandate_fed_outside_provision_values",
                message=(
                    f"Step '{node_id}' (Run Mandate) is given {names} by {' and '.join(where)}, which it does not take: "
                    "every run would stop there. A Run Mandate step takes the job's state only as 'provision_values' "
                    f"(it takes: {', '.join(sorted(typed))}). Hand the values over inside one 'provision_values' object, "
                    "or, if they are the agent's own inputs one-to-one, make this a Run Agent step."
                ),
            )
        )
    return issues


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


async def _bind_provision_values(
    inputs: MandateStartInput, resolved: Any, bound: dict[str, Any] | None = None
) -> MandateStartInput:
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
    # THE STATE at the point is IN HAND (the run already holds every value), so it reaches the compute rule as
    # ``given`` — never as plain values the rule counts as a not-yet-migrated eager-legacy call site
    # (ops.system_error ``mandate_offer_eager_legacy``, ~60 rows, e.g. ``brand_discovery.curate @
    # matrx_ai/graph_nodes/mandate_action.py``). The compute rule unwraps each value in place.
    from matrx_ai.mandates import Offer

    variables = await materialize(Offer.given_values(supplied))
    refuse_variables_shadowing_typed_fields(variables, where)
    if bound is not None:
        bound.update(variables)  # the variables the doer runs on: the replay fingerprint (mandate_taps)
    extras = dict(inputs.model_extra or {})
    return MandateStartInput.model_validate(
        {**inputs.model_dump(exclude={"provision_values"}, exclude_none=True), **extras, **variables}
    )


def failed_turn_as_answer(result: Any, *, node_id: str, mandate_key: str) -> Any:
    """``continue_on_failure``: a doer's failed turn (``ai_turn_failed``) becomes a SUCCESSFUL step result that
    carries no answer and names the failure in ``metadata``; anything else is returned untouched. Never silent:
    one WARNING line per carried failure, and ``metadata.failed`` is true on the result every later step reads."""
    error = getattr(result, "error", None)
    if getattr(result, "status", None) != "error" or error is None or error.code != "ai_turn_failed":
        return result
    details = dict(error.details or {})
    usage = details.pop("usage", None) or {}
    logger.warning("[mandate step] %s (mandate %s): the agent's turn failed and the step continues with the "
                   "error, as its continue_on_failure says: %s", node_id, mandate_key, error.message)
    return success(AiExecutionResult(
        conversation_id=str(details.get("conversation_id") or ""), request_id=str(details.get("request_id") or ""),
        iterations=0, finish_reason="failed", usage=usage,
        metadata={"failed": True, "error": error.message, "error_code": error.code, "error_details": details,
                  **({"error_technical": error.technical} if error.technical else {})}))


async def _name_what_a_caller_would_catch(result: Any, completed: Any, mandate_key: str, agent_id: str) -> None:
    """A carried failure also says what a CODE caller of this mandate would have caught for the same failed
    turn: ``metadata.error_raised = {error_class, message}``, from the host's one author of those words
    (ext ``mandate_failed_run_error``). A later step that must word the failure exactly as the code does
    reads it; without the host ext the key is absent."""
    payload = getattr(result, "result", None)
    if not isinstance(payload, AiExecutionResult) or not payload.metadata.get("failed"):
        return
    if not has_ext("mandate_failed_run_error"):
        return
    # The run's own recorded error, read as the agent executor reads it (``AgentRunResult.error``).
    raw = (getattr(completed, "metadata", None) or {}).get("error")
    if isinstance(raw, dict):
        raw = raw.get("user_message") or raw.get("message") or raw
    error = str(raw) if raw is not None else payload.metadata.get("error")
    raised = await get_ext("mandate_failed_run_error")(mandate_key, agent_id, error, source=completed)
    payload.metadata["error_raised"] = {"error_class": type(raised).__name__, "message": str(raised)}


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
    retry=UNUSABLE_ANSWER_RETRY,
    sample_preflight=lambda ctx, inputs, config: mandate_sample_preflight(ctx, inputs, config),
    # A workflow holder is a wait, like subgraph.call: its own steps run under their own clocks, so this step
    # is not held to the platform step clock (cut off at 600 s, 2026-11-10). An AGENT holder is bounded by the
    # platform clock inside the body (``_mandate_start_body``). An author's data.step_clock still sets a shorter limit.
    timeout_ms=MAX_STEP_SECONDS * 1000,
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
            carried = unheld_job_as_answer(exc, inputs=inputs, node_id=getattr(ctx, "node_id", None) or "?")
            if carried is not None:
                return carried
        raise


def unheld_job_as_answer(exc: BaseException, *, inputs: MandateStartInput, node_id: str) -> Any:
    """``continue_on_failure`` + a job NOBODY HOLDS: the refusal ``unfulfilled`` (no Holder at any rung) is a
    state of the platform, not a wiring defect, so it is carried exactly like a failed turn — the step succeeds
    with no answer, ``metadata.failed`` true, ``error_code`` ``mandate_unfulfilled`` and the runner's own
    sentence — and the workflow's next step degrades the way the code it replaces does (research triage: one
    run-wide warning, the arithmetic order). Every other refusal and every other error still fails the step.
    Never silent: one WARNING line per carried refusal."""
    if not inputs.continue_on_failure:
        return None
    from matrx_ai.mandates import MandateRefused

    seen: BaseException | None = exc
    while seen is not None and not isinstance(seen, MandateRefused):
        seen = seen.__cause__
    if not isinstance(seen, MandateRefused) or seen.code != "unfulfilled":
        return None
    logger.warning("[mandate step] %s (mandate %s): nobody holds this job, and the step continues with the "
                   "refusal, as its continue_on_failure says: %s", node_id, inputs.mandate_key, seen.sentence)
    return success(AiExecutionResult(
        conversation_id="", request_id="", iterations=0, finish_reason="failed",
        metadata={"failed": True, "error": seen.sentence, "error_code": "mandate_unfulfilled",
                  "error_details": {"refusal_code": seen.code, "missing": list(seen.missing), "door": seen.door}}))


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
    return await run_sampled_firewall_check(
        ctx,
        step_firewall(inputs),
        node_type=_NODE_TYPE,
        job=f"mandate {inputs.mandate_key!r}",
        body=lambda capture_ctx: _mandate_start_body(
            capture_ctx, inputs.model_copy(deep=True), config, capture=True
        ),
    )


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
    # THE PAUSE SWITCH — the host's ONE pause check, the same ``run_mandate`` makes: a paused
    # mandate refuses in words here, before anything resolves or spends. (A capture-mode check
    # spends nothing, so a sampled step's firewall proof still runs.)
    if not capture:
        await refuse_if_mandate_paused(inputs.mandate_key)
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
    firewall = step_firewall(inputs)
    if isinstance(resolved, StepWorkflowMandate):
        if firewall is not None:
            raise ValueError(
                f"{_NODE_TYPE}:{node_id} (mandate {inputs.mandate_key!r}) has a request firewall, but "
                "this job is done by a whole workflow, whose many AI calls this step cannot check. "
                "Give the job to an agent, or put the firewall on the AI steps inside that workflow."
            )
        if inputs.max_call_cost_usd or inputs.max_output_tokens:
            raise ValueError(
                f"{_NODE_TYPE}:{node_id} (mandate {inputs.mandate_key!r}) has a cap per AI call or a "
                "longest-answer limit, but this job is done by a whole workflow, whose AI calls this "
                "step cannot cap. Give the job to an agent, or set the limits on the AI steps inside "
                "that workflow. Nothing was run or charged."
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
    # THE ONE MANDATE REPLAY (``mandate_taps.answer_fingerprint``): keyed on the mandate, the resolved Holder and
    # the FULLY RESOLVED request this step would send (variables after binding and every edge, the turn, the
    # settings after every layer, and every other set field) — the same key the code path builds, so either
    # side can record and the other replay. The host decides when (a replay session, or AI test mode); else None.
    from matrx_ai.mandate_taps import ReplayKey, answer_fingerprint, record_answer, replay_answer, request_fingerprint

    run_id = getattr(ctx, "run_id", None)
    # THE FORMAT THIS RUN WILL SEND is part of the question: the host binds the mandate's declared kind later
    # (``prepare_agent_run``), so the request holds none yet while the code lane keys the format it sends. The host
    # seam names it (research parity row a79c5563: every auto_tagger call keyed apart on it). Asked only when a
    # replay may answer this run; an authored ``response_format`` override wins, as it does at the bind.
    bound_format: dict[str, Any] | None = None
    if (
        not capture
        and has_ext("mandate_bound_response_format")
        and getattr(request.config_overrides, "response_format", None) is None
    ):
        from matrx_ai.mandate_taps import replay_may_answer

        if await replay_may_answer(run_id):
            bound_format = await get_ext("mandate_bound_response_format")(
                inputs.mandate_key, resolved.agent_id, is_version=bool(resolved.is_version))

    # Built only inside a replay session / test mode, never on a real call (``ReplayKey``).
    def _key() -> dict[str, Any]:
        parts = request_fingerprint(request)
        parts["request"] = {**parts["request"], "firewall": step_firewall_key(inputs)}
        if bound_format is not None:
            parts["config_overrides"] = {**parts["config_overrides"], "response_format": bound_format}
        return answer_fingerprint(agent_id=resolved.agent_id, is_version=bool(resolved.is_version), **parts)

    fingerprint = ReplayKey(_key, label=inputs.mandate_key)
    replayed = None if capture else await replay_answer(inputs.mandate_key, run_id, fingerprint)
    if replayed is not None:
        # The firewall checks the request this step would send BEFORE any recorded answer is served.
        walled = await firewall_before_replay(
            ctx, request, agent_id=resolved.agent_id, firewall=firewall, node_type=_NODE_TYPE,
            job=f"mandate {inputs.mandate_key!r}", mandate_key=inputs.mandate_key, run_stamp=resolved.run_stamp)
        answer = AiExecutionResult.model_validate(replayed)
        if walled is not None:
            answer.metadata["request_firewall"] = walled
        await record_served_answer(ctx, mandate_key=inputs.mandate_key, run_stamp=resolved.run_stamp, answer=replayed)
        # WHO would have done the job: a stand-in somebody typed names no doer, and the code path's row always
        # names the resolved one — so the step's result does too (a recorded answer already carries its own).
        answer.metadata.setdefault("agent_id", resolved.agent_id)
        return success(answer)

    progress["holder_started"] = True
    # AN AGENT HOLDER KEEPS THE PLATFORM CLOCK. The step declares the engine's longest limit so a WORKFLOW holder
    # (a wait, like subgraph.call) is not cut at 600 s; an agent holder is one provider call, which must never
    # hang for hours — so it is bounded here by the platform step clock (``workflow.step_clock``). An author's
    # ``data.step_clock`` is the scheduler's outer clock: when shorter, it still stops the step first.
    from matrx_graph.errors import NodeTimeoutError
    from matrx_graph.knobs import default_step_seconds

    agent_seconds = float(await default_step_seconds())
    agent_clock = asyncio.timeout(agent_seconds)
    try:
        async with agent_clock:
            completed, firewall_records = await run_walled_step_agent(
                ctx,
                resolved.agent_id,
                request,
                node_type=_NODE_TYPE,
                firewall=firewall,
                mandate_key=inputs.mandate_key,
                run_stamp=resolved.run_stamp,
                capture=capture,
            )
    except TimeoutError:
        if not agent_clock.expired():
            raise
        raise NodeTimeoutError(
            node_id, int(agent_seconds * 1000), int(getattr(ctx, "attempt", 1) or 1), source="platform"
        ) from None
    if capture:
        return firewall_records

    # A host agent_runner may return an ALREADY-normalized AiExecutionResult
    # (a compiled Orchestra whose final step IS the result). Pass it through.
    if isinstance(completed, AiExecutionResult):
        completed.metadata.setdefault("agent_id", resolved.agent_id)
        if firewall_records is not None:
            completed.metadata["request_firewall"] = firewall_records
        await record_answer(inputs.mandate_key, run_id, fingerprint, completed.model_dump(mode="json"))
        return success(completed)
    # ``config`` carries the author's ``allow_empty_structured_output`` into the all-zero refusal,
    # exactly as Run Agent passes it (the field is on the shared AgentStartConfig).
    result = await asyncio.to_thread(normalize_completed_result, completed, step_config=config)
    if inputs.continue_on_failure:
        result = failed_turn_as_answer(result, node_id=node_id, mandate_key=inputs.mandate_key)
        await _name_what_a_caller_would_catch(result, completed, inputs.mandate_key, resolved.agent_id)
    # WHO did the job: the doer the database resolved for this run (a research
    # row records it as agent_id, exactly as the research code path does).
    payload = getattr(result, "result", None)
    if isinstance(payload, AiExecutionResult):
        payload.metadata["agent_id"] = resolved.agent_id
        if firewall_records is not None:
            payload.metadata["request_firewall"] = firewall_records
        if not payload.metadata.get("failed"):  # a carried failure is never an answer to replay
            await record_answer(inputs.mandate_key, run_id, fingerprint, payload.model_dump(mode="json"))
    return limit.name_on(result)

