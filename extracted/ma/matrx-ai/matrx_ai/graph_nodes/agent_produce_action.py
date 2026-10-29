"""``ai.agent.produce`` — run an agent BOUND to the kind it must answer in.

The one-line difference from ``ai.agent.start``: this node's output IS the
platform kind the step declares, already validated, instead of the run
ENVELOPE with the answer buried inside ``final_text`` as a JSON string.

Why it exists (Arman's ruling, 2026-08-20)
------------------------------------------
Measured on live Study Pack run ``fedd6591-bec8-4813-98a3-91ec884698dc``: the
notes step's ``output_kind`` was ``agent_result`` (usage, messages, metadata),
``structured_output`` was **null**, and the kind-shaped data sat in
``final_text`` as a string. Getting from there to something renderable took
FOUR hops — agent → ``ai.util.parse_llm_json`` → ``data.map_template`` →
``data.transform`` — and the kind was LOST at the agent boundary and hand-
reconstructed downstream by seven projection nodes. Every one of those nodes
was a workaround for an agent that never saw its own declaration.

So the declaration is handed to the agent. The node reads the kind slug the
graph declared for it (``data.output_kind``, surfaced as
:attr:`NodeExecutionContext.output_kind`), turns it into a strict, provider-
portable ``response_format`` through the ONE binder
(``matrx_ai.kinds.response_format_for_kind``), and returns the model's parsed,
schema-validated answer as the node payload. The scheduler then validates that
payload against the SAME kind and stamps it on the outcome row — so
``output_kind`` / ``output_kind_ok`` describe the actual answer, and any
surface that renders the kind can render the step with no projection lane.

What this node refuses to do
----------------------------
* Run without a declared kind. A step whose whole contract is "produce X" and
  that never says which X is not a step, it is a guess.
* Run against an unbindable kind. An unenforceable ``response_format``
  degrades silently to prose, which is worse than no binding at all.
* Run when the graph's declaration and the MANDATE's declared ``output_kind``
  disagree. Two declarations about what a paid run produces cannot both be
  true, and picking one on the executor's own authority is how drift becomes
  invisible.
* Let an authored ``config_overrides`` unbind the kind — the binding is
  layered ABOVE every author/binding/run-scope layer (see
  ``build_agent_request``'s ``top_config_overrides``).

Everything else — mandate resolution, conversation gating, tools, context,
variables, streaming, cost — is the SAME code ``ai.agent.start`` runs. This is
not a second way to run an agent; it is the same way, with the declaration
carried through instead of dropped.

Run Typed Agent — what a mandate gave, on the step (Arman, 2026-10-27)
---------------------------------------------------------------------
*"Instead of running a mandate that in turn runs an agent, you just run the
agent directly"* (generic-only VISION § Mandates inside workflows). This step
IS that step, extended in place rather than built beside it: it already bound
an agent to its kind, which is the half of a mandate a workflow needs. The
other half rides on the step's config (:class:`TypedAgentConfig`):

* ``goal`` — what the step must achieve, written on the step and shown in the
  Studio; ``goal_approved`` — a person approved that sentence (a goal carried
  over from a mandate whose goal is human-grounded arrives approved).
* After a successful answer the host's ``typed_step_judge`` grades it against
  THAT goal with the SAME judge every mandate run reaches
  (``mandate_outcome.judge.judge_finalized_run``: sampled by the same knob,
  forced by "judge every output", an unapproved goal is never judged), filed
  under the workflow and step. A judge never changes the step's outcome.
* Cost attribution is the step's ``source_feature`` input; run once per key and
  fan-out are the engine's (``data.once`` + :func:`step_result_version`,
  ``control.map``) exactly as for Run Mandate.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any, Literal

from matrx_graph.actions import register_node
from matrx_graph.errors import ExecutionError
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory, RetryPolicy
from matrx_graph.types.result import RESERVED_PAYLOAD_FIELDS, NodeResult, failure, success
from matrx_graph.types.usl import field_extras
from pydantic import BaseModel, ConfigDict, Field

from matrx_ai._ext import get_ext, has_ext
from matrx_ai.graph_nodes.agent_action import (
    AgentStartConfig,
    AgentStartInput,
    MandateSelectorInput,
    StepProtectionInput,
    build_agent_request,
    job_variable_binder,
    refuse_if_mandate_paused,
    require_agent_host,
    resolve_step_agent_full,
    run_sampled_firewall_check,
    run_walled_step_agent,
    step_firewall,
    step_result_version,
)
from matrx_ai.graph_nodes.iteration_limit import resolve_step_iteration_limit
from matrx_ai.graph_nodes.shared import (
    RUN_ENVELOPE_FIELDS,
    AiExecutionResult,
    ai_output_failure,
    normalize_completed_result,
)
from matrx_ai.kinds import TEXT_SHAPED_KINDS, is_bindable_kind, response_format_for_kind

logger = logging.getLogger(__name__)

_NODE_TYPE = "ai.agent.produce"


class AgentProduceInput(AgentStartInput, MandateSelectorInput, StepProtectionInput):
    """``ai.agent.start``'s input, plus the optional Mandate selector.

    Deliberately a subclass and not a trimmed copy: everything the API supports
    the workflow supports, by construction. The kind is NOT an input field — it
    is the node instance's ``data.output_kind`` declaration, the same value the
    scheduler validates the result against. A second place to say it would be a
    second thing that can disagree.

    Unlike Run Agent, this step keeps ``mandate_key``: its whole purpose is a
    step whose OUTPUT KIND is the contract, and a Mandate declares an
    ``output_kind`` this node checks its own declaration against
    (``_assert_declarations_agree``). Exactly one selector may be set — the
    shared resolver refuses both.
    """

    # The request firewall fields come from ``StepProtectionInput`` — the SAME declaration Run
    # Mandate has, enforced the same way (``run_walled_step_agent``), so converting a step keeps it.
    # Pydantic merges multiple-inheritance config from left to right, so the
    # strict MandateSelectorInput base would otherwise overwrite
    # AgentStartInput's dynamic variable-port contract. Produce nodes accept
    # the same author-exposed top-level variables as Run Agent.
    model_config = ConfigDict(extra="allow")


class AgentProducedOutput(BaseModel):
    """The kind's own payload, verbatim — this node's output IS the answer.

    Permissive by construction (``extra="allow"``, no declared fields): the
    real shape is the declared kind's ``emitted_json_schema``, which the
    provider was bound to and the scheduler checks against. Same pattern
    ``io.user_input`` uses for author-defined fields — the pydantic class is
    the transport, the kind is the contract.
    """

    model_config = ConfigDict(
        extra="allow",
        json_schema_extra={
            "x-contract-dynamic": (
                "the node instance's declared output_kind is the real schema; "
                "the model is bound to it via response_format"
            )
        },
    )


class TypedAgentConfig(AgentStartConfig):
    """Run Agent's author-time config, plus the step's GOAL (what a mandate used to carry).

    A subclass, not a copy: every Run Agent setting stays available here by construction.
    """

    goal: str | None = Field(
        default=None,
        title="Goal",
        description=(
            "What this step must achieve. Every answer can be graded against it by the same "
            "judge mandates use."
        ),
    )
    goal_approved: bool = Field(
        default=False,
        title="Goal approved",
        description="A person approved this goal. Only an approved goal is graded.",
    )
    #: Who grounded the goal, kept distinct on the verdict ledger (H human, V verified, A agent).
    #: Set by the converter from the mandate's ``goal_grounding``; unset = H when approved, else A.
    goal_grounding: Literal["H", "V", "A"] | None = Field(
        default=None, json_schema_extra=field_extras(hidden=True),
    )
    #: Keys the answer must carry (a mandate's ``required_output_keys``), checked by the same
    #: answer check mandates use before the goal is graded.
    required_output_keys: list[str] = Field(default_factory=list, json_schema_extra=field_extras(hidden=True))
    #: Which job this run is, when one step runs several jobs that share agent, kind AND goal (a
    #: quiz and a practice test): appended to the verdict key so their grades stay apart.
    label: str | None = Field(
        default=None,
        title="Label",
        description=(
            "Names this job when one step runs several with the same agent, kind and goal "
            "(e.g. {'$input': 'output_name'}), so each is graded apart."
        ),
    )
    run_envelope: list[str] = Field(
        default_factory=list,
        title="Also hand over",
        description=(
            "Run facts handed downstream beside the answer, under their own names "
            "(final_text, content, messages, usage, conversation_id, metadata, ...) - "
            "the same fields Run Agent and Run Mandate hand over."
        ),
    )
    mandate_key_origin: str | None = Field(
        default=None,
        title="Runs as job",
        description=(
            "The mandate this step was converted from. The step still runs that job's protections: "
            "its dispatch guards, closed context, spend approval and pause switch."
        ),
    )
    output_kind: str | None = Field(
        default=None,
        title="Output kind",
        description=(
            "The kind the agent answers in, when the step itself declares none. Lets a reusable "
            "workflow take the kind as an argument ({'$input': 'output_kind'}) together with the "
            "agent and the goal, so its caller names all three once."
        ),
    )


def _with_run_envelope(
    payload: dict[str, Any], normalized: AiExecutionResult, fields: list[str], kind: str
) -> tuple[dict[str, Any], list[str]] | NodeResult[Any]:
    """The answer plus the asked-for run facts under their own names, or a named refusal."""
    wanted = [f for f in dict.fromkeys(fields or []) if f]
    if not wanted:
        return payload, []
    unknown = sorted(set(wanted) - RUN_ENVELOPE_FIELDS)
    if unknown:
        return failure(
            "run_envelope_unknown_field",
            f"'Also hand over' names {unknown}, which a run does not have. Choose from {sorted(RUN_ENVELOPE_FIELDS)}.",
            details={"fields": unknown},
        )
    clash = sorted(set(wanted) & payload.keys())
    if clash:
        return failure(
            "run_envelope_field_clash",
            (
                f"Kind '{kind}' has its own field(s) {clash}, so the run's {clash} cannot be handed over "
                "beside it under the same name. Read the kind's field, or remove it from 'Also hand over'."
            ),
            details={"declared_kind": kind, "fields": clash},
        )
    envelope = normalized.model_dump(mode="json", include=set(wanted))
    return {**payload, **envelope}, wanted


#: The one plain-text kind this step accepts besides structural kinds (coordinator decision,
#: 2026-10-27: goal + grading are the point, so text-output agents convert too). Its payload is
#: the registered ``text`` kind's shape: ``{"__kind": "text", "text": <the answer>}``.
TEXT_KIND = "text"
# ``markdown`` (and any kind in ``matrx_ai.kinds.TEXT_SHAPED_KINDS``) is handled the same way,
# wrapping the answer as ``{"__kind": <that kind>, "text": ...}``.

#: The one media kind (image / video / audio agents answer with media, not JSON). Such a step is
#: never bound to a response_format; its answer is the LAST media block the agent produced, as the
#: registered ``media_asset`` kind (aidream/kinds/media_asset.py): a durable handle, never bytes.
MEDIA_KIND = "media_asset"

#: The ``media_asset`` fields a stored media block carries under the same name
#: (``ImageContent.to_storage_dict`` & siblings: ``{"type": "media", "kind": "image", ...}``).
#: ``base64_data`` / ``file_uri`` / ``role`` are deliberately absent: never bytes, never a
#: provider-internal handle.
_MEDIA_BLOCK_FIELDS: tuple[str, ...] = (
    "origin", "file_id", "url", "cdn_url", "download_url", "external_url", "source_label",
    "mime_type", "file_name", "size_bytes", "width", "height", "duration_ms", "poster_url",
    "transcript", "page_count",
)
_MEDIA_TYPES = frozenset({"image", "video", "audio", "document", "youtube"})


def _produced_media(normalized: AiExecutionResult) -> dict[str, Any] | None:
    """The last media block of the last assistant turn that has one, as a ``media_asset``."""
    for message in reversed(normalized.messages or []):
        if message.role != "assistant" or not isinstance(message.content, list):
            continue
        for block in reversed(message.content):
            if not isinstance(block, dict) or not (block.get("url") or block.get("file_id")):
                continue
            media_type = block.get("kind") if block.get("type") == "media" else block.get("type")
            if media_type not in _MEDIA_TYPES and block.get("type") != "media":
                continue
            asset: dict[str, Any] = {
                "__kind": MEDIA_KIND,
                "media_type": media_type if media_type in _MEDIA_TYPES else "unknown",
            }
            asset.update({f: block[f] for f in _MEDIA_BLOCK_FIELDS if block.get(f) is not None})
            if asset.get("origin") not in ("matrx", "external"):
                asset["origin"] = "matrx" if asset.get("file_id") else "external"
            return asset
    return None


def _declared_kind(ctx: NodeExecutionContext, config: TypedAgentConfig | None = None) -> str:
    # The step's own declaration wins; a step that declares none may take the kind from its
    # config (a run input in a reusable workflow). The payload then carries ``__kind`` and the
    # scheduler validates it against that kind (it reads the payload's marker when no kind is
    # declared on the node).
    kind = (getattr(ctx, "output_kind", None) or "").strip() or (
        (getattr(config, "output_kind", None) or "").strip()
    )
    if not kind:
        raise ExecutionError(
            f"{_NODE_TYPE} step '{getattr(ctx, 'node_id', '?')}' declares no output "
            "kind. This node exists to make an agent answer IN a registered "
            "platform kind, so the kind is not optional: set the node's "
            "`output_kind` (data.output_kind, or the step setting output_kind) to the kind slug this step "
            "produces — e.g. 'flashcard_set'. For a free-text or free-JSON "
            "agent step, use ai.agent.start instead."
        )
    if kind in TEXT_SHAPED_KINDS or kind == MEDIA_KIND:
        return kind
    if not is_bindable_kind(kind):
        raise ExecutionError(
            f"{_NODE_TYPE} step '{getattr(ctx, 'node_id', '?')}' declares "
            f"output kind '{kind}', which names a FORMAT, not a structure — "
            "there is nothing to bind the model to. Declare a registered "
            "structural kind, or use ai.agent.start for free-form output."
        )
    return kind


def _assert_declarations_agree(
    ctx: NodeExecutionContext, kind: str, mandate_kind: str | None
) -> None:
    """The graph's declaration and the Mandate's must be the same kind.

    A mandate that declares nothing structural (``text`` / ``json`` / unset, or
    a step pinned to a bare ``agent_id``) is not a contradiction — it is a job
    that never stated what it answers in, and the graph's declaration stands.
    Say so once, at warning level, because a mandate SHOULD carry that truth:
    every other consumer of the job (a client run, a bench run) reads the
    mandate, not this graph.
    """
    if mandate_kind is None or not is_bindable_kind(mandate_kind):
        logger.warning(
            "%s step '%s' declares output kind '%s', but its mandate declares "
            "%r — the mandate is the platform-wide statement of what this JOB "
            "answers in, so set its output_kind to '%s' too (declare_mandate("
            "output_kind=...)).",
            _NODE_TYPE,
            getattr(ctx, "node_id", "?"),
            kind,
            mandate_kind,
            kind,
        )
        return
    if mandate_kind != kind:
        raise ExecutionError(
            f"{_NODE_TYPE} step '{getattr(ctx, 'node_id', '?')}' declares output "
            f"kind '{kind}', but the mandate it runs declares '{mandate_kind}'. "
            "Both claim to describe what this paid run produces and they cannot "
            "both be right. Fix whichever one is wrong — the mandate's "
            "declare_mandate(output_kind=...) or the node's data.output_kind — "
            "before this step runs again."
        )


async def _response_format_for(ctx: NodeExecutionContext, kind: str) -> dict[str, Any]:
    bound = await response_format_for_kind(kind)
    if bound is None:
        # response_format_for_kind already logged WHY (unregistered slug, no
        # schema, or a schema the portability gate cannot make strict).
        raise ExecutionError(
            f"{_NODE_TYPE} step '{getattr(ctx, 'node_id', '?')}' could not bind "
            f"kind '{kind}' to a strict response_format, so the agent would "
            "answer in whatever shape it felt like and this step's declaration "
            "would be a lie. Fix the kind's emitted_json_schema (the binder "
            "logged the findings) — this step does not run unbound."
        )
    return bound.model_dump(mode="json", by_alias=True, exclude_none=True)


async def _apply_mandate_binding(
    request: Any, resolved: Any, mandate_key: str, node_id: str
) -> Any:
    """Put the step's variables through the mandate's BINDING (the host's one
    consumption pipeline) before the doer runs — runner plan step 1, 2026-10-20.

    Until this date a produce step that named a mandate sent its variables to
    the doer BY NAME: no binding map, no guaranteed-value gate, no placement.
    The values the step built (``request.variables``, after every port and
    authored-variable rule has folded) are the offer; what the pipeline returns
    is what the doer runs on. A host with no pipeline refuses — the step never
    runs unbound.
    """
    materialize = getattr(resolved, "materialize", None)
    if materialize is None:
        raise ExecutionError(
            f"{_NODE_TYPE} step '{node_id}' runs mandate {mandate_key!r}, but this host "
            "offers no consumption pipeline to apply the mandate's binding — the step "
            "does not run unbound."
        )
    supplied = dict(getattr(request, "variables", None) or {})
    variables = await materialize(supplied)
    request.variables = dict(variables) or None
    return request


def _protected_mandate_key(inputs: AgentProduceInput, config: TypedAgentConfig | None, node_id: str) -> str | None:
    """The mandate whose protections this step runs under: ``mandate_key`` when it names one, else the
    ``mandate_key_origin`` a converted step carries. Two different jobs on one step is refused."""
    named = (getattr(inputs, "mandate_key", None) or "").strip() or None
    origin = (getattr(config, "mandate_key_origin", None) or "").strip() or None
    if named and origin and named != origin:
        raise ExecutionError(
            f"{_NODE_TYPE} step '{node_id}' runs mandate {named!r} but says it was converted from "
            f"{origin!r}. A step runs as one job: clear 'Runs as job' or make it {named!r}."
        )
    return named or origin


def _record_spend(ctx: NodeExecutionContext, normalized: AiExecutionResult) -> None:
    """Declare this invocation's billed usage on the engine plane.

    This node's payload is a platform kind — strict, additionalProperties:
    false — so there is nowhere in it to carry a usage block, and the
    scheduler's payload sniffing would silently lose the cost tick. Declaring
    it is the correct channel, not a workaround: what a run SPENT was never a
    property of what it RETURNED.
    """
    ctx.record_billed_usage(
        normalized.usage.model_dump(mode="json"),
        conversation_id=normalized.conversation_id or None,
        request_id=normalized.request_id or None,
    )


#: The host seam that grades a typed step's answer against the step's own goal.
TYPED_STEP_JUDGE_EXT = "typed_step_judge"


def _judge_against_goal(
    ctx: NodeExecutionContext,
    config: TypedAgentConfig | None,
    *,
    kind: str,
    payload: dict[str, Any],
    normalized: AiExecutionResult,
    agent_id: str,
    variables: dict[str, Any] | None,
    user_input: Any,
) -> None:
    """Hand the finished answer to the host's goal judge, DETACHED: the step never waits for the
    judge (up to two paid calls). Never raises, never changes the outcome.

    A goal-less step is still handed over — the host says why it was not graded, and surfaces it
    when the run asked to judge every output. A host with no judge seam is said loudly.
    """
    goal = (getattr(config, "goal", None) or "").strip()
    node_id = getattr(ctx, "node_id", None) or "?"
    if not has_ext(TYPED_STEP_JUDGE_EXT):
        logger.warning(
            "%s step '%s': this host installs no %r — the answer is not graded.",
            _NODE_TYPE, node_id, TYPED_STEP_JUDGE_EXT,
        )
        return
    grounding = getattr(config, "goal_grounding", None) or (
        "H" if getattr(config, "goal_approved", False) else "A"
    )
    kwargs = dict(
            workflow_id=str(getattr(ctx, "workflow_id", "") or "") or None,
            run_id=str(getattr(ctx, "run_id", "") or "") or None,
            node_id=node_id,
            organization_id=getattr(ctx, "organization_id", None),
            user_id=str(getattr(ctx, "user_id", "") or "") or None,
            goal=goal,
            goal_grounding=grounding,
            required_output_keys=list(getattr(config, "required_output_keys", None) or []),
            output_kind=kind,
            artifact=payload,
            variables=dict(variables or {}),
            user_input=user_input if isinstance(user_input, str) else None,
            agent_id=agent_id,
            model_id=next(iter(normalized.usage.models), None),
            conversation_id=normalized.conversation_id or None,
            label=(getattr(config, "label", None) or "").strip() or None,
    )
    from matrx_connect.context.app_context import set_app_context, try_get_app_context
    from matrx_utils.utils.detached_task import detached_task

    app = try_get_app_context()

    async def _judged() -> None:
        # A detached task starts in a fresh context (never the step's DB connection); the request
        # identity is CARRIED in explicitly, never rebuilt.
        if app is not None:
            set_app_context(app)
        try:
            await get_ext(TYPED_STEP_JUDGE_EXT)(**kwargs)
        except Exception:  # noqa: BLE001 — the answer was produced and paid for; a judge never sinks it
            logger.exception("%s step '%s': the goal judge failed; the answer stands.", _NODE_TYPE, node_id)

    detached_task(_judged(), name=f"typed-step-judge:{node_id}")


#: AN ANSWER WE CANNOT USE IS ASKED FOR ONCE MORE (2026-10-28). The model answered, but the one parse
#: funnel (``parse_agent_output``) refused it: malformed JSON, a schema miss, or a DEGENERATE answer
#: (placeholder filler — "the model abandoned the generation; the run must be retried"). Live: Group
#: offerings runs 48191b96 and ed375042 each lost the whole run to one Claude Haiku 5.5 call that answered
#: ``{"groups":[{"keys":[],"label":"Placeholder"}]}``; the other 15 of 16 / 8 of 9 calls were fine. A
#: second sample of a non-deterministic model is the right repair, so the step retries those codes once
#: (``structured_output_empty`` is the same "answered, unusable" class). Never ``output_truncated``: the
#: same ceiling cuts the same answer again. A ``retry_policy`` an author sets on the step still wins.
#: Guard: tests/test_typed_agent_asks_again_for_an_unusable_answer.py.
UNUSABLE_ANSWER_RETRY = RetryPolicy(
    max_attempts=2,
    retry_on=("structured_output_invalid", "structured_output_empty"),
)


@register_node(
    name=_NODE_TYPE,
    display_name="Run Typed Agent",
    description=(
        "Run one of your saved agents and get back a real, checked result of "
        "the kind this step declares, graded against the step's goal."
    ),
    category=NodeCategory.AGENT,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=AgentProduceInput,
    output_schema=AgentProducedOutput,
    # No spec-level kind: the kind is per node INSTANCE (data.output_kind), and
    # dynamic_output keeps the registry from minting a fingerprint contract
    # kind that would read as "this node declares a kind" while describing
    # nothing anyone can render.
    output_kind=None,
    dynamic_output=True,
    config_schema=TypedAgentConfig,
    icon="bot",
    tags=("ai", "agent", "llm", "kinds", "goal"),
    result_version=step_result_version,
    sample_preflight=lambda ctx, inputs, config: agent_produce_sample_preflight(ctx, inputs, config),
    retry=UNUSABLE_ANSWER_RETRY,
)
async def agent_produce(
    ctx: NodeExecutionContext,
    inputs: AgentProduceInput,
    config: TypedAgentConfig | None = None,
) -> NodeResult[AgentProducedOutput]:
    return await _agent_produce_body(ctx, inputs, config)


async def agent_produce_sample_preflight(
    ctx: NodeExecutionContext,
    inputs: AgentProduceInput,
    config: TypedAgentConfig | None = None,
) -> dict[str, Any] | None:
    """THE FIREWALL ON A SAMPLED STEP — the same shared check Run Mandate runs
    (``agent_action.run_sampled_firewall_check``): this step's own body in capture mode, so the
    request it WOULD send is checked and never sent. No firewall -> None."""
    return await run_sampled_firewall_check(
        ctx,
        step_firewall(inputs),
        node_type=_NODE_TYPE,
        job=f"job {_protected_mandate_key(inputs, config, getattr(ctx, 'node_id', None) or '?') or 'direct agent'!r}",
        body=lambda capture_ctx: _agent_produce_body(
            capture_ctx, inputs.model_copy(deep=True), config, capture=True
        ),
    )


async def _agent_produce_body(
    ctx: NodeExecutionContext,
    inputs: AgentProduceInput,
    config: TypedAgentConfig | None,
    *,
    capture: bool = False,
) -> Any:
    """The step's body. ``capture`` (``agent_produce_sample_preflight`` only): the request is built and
    run to the transport inside the firewall scope, never sent; returns the scan records."""
    require_agent_host(_NODE_TYPE)
    node_id = getattr(ctx, "node_id", None) or "?"
    kind = _declared_kind(ctx, config)
    # THE JOB THIS STEP RUNS AS (2026-10-28): the mandate it names, or the one it was converted from.
    # Every protection keyed by the mandate (pause switch, dispatch guards, contract, spend holds)
    # follows it — a converted step runs the agent directly, never around the job's walls.
    protected_as = _protected_mandate_key(inputs, config, node_id)
    if not capture:  # a capture-mode check spends nothing, so a sampled step's proof still runs
        await refuse_if_mandate_paused(protected_as)

    resolved = await resolve_step_agent_full(inputs, consumer=f"{_NODE_TYPE}:{node_id}")
    _assert_declarations_agree(ctx, kind, resolved.declared_output_kind)
    # THE HOLDER'S JOB (2026-10-28): the origin field is editable and a unit that runs whatever agent its
    # caller hands it carries none, so an agent that is the Holder of a guarded / closed-context /
    # spend-held mandate — or the SOLE holder of any one mandate — runs as that job even when the step
    # names none: the job's walls below AND its binding (``job_variable_binder``). Only when the step names
    # none; a named job wins. Several protected jobs refuse (``SeveralProtectedJobs``).
    held_by = None
    if protected_as is None and has_ext("holder_protected_mandate"):
        held_by = await get_ext("holder_protected_mandate")(resolved.agent_id, bool(resolved.is_version))
        if held_by:
            protected_as = held_by["mandate_key"]
            if not capture:
                await refuse_if_mandate_paused(protected_as)

    limit = await resolve_step_iteration_limit(ctx, inputs.max_iterations)
    inputs.max_iterations = limit.value
    request = build_agent_request(
        ctx,
        inputs,
        resolved,
        node_type=_NODE_TYPE,
        # ABOVE every other layer: the declaration is this node's contract, and
        # an authored config_overrides must never be able to unbind it.
        top_config_overrides=(
            {}
            if kind in TEXT_SHAPED_KINDS or kind == MEDIA_KIND
            else {"response_format": await _response_format_for(ctx, kind)}
        ),
        declared_variables=list(getattr(config, "exposed_variables", None) or []),
        variable_sources=dict(getattr(config, "variable_sources", None) or {}),
        include_org_catalog=getattr(config, "include_org_catalog", True),
    )
    mandate_key = getattr(inputs, "mandate_key", None)
    if mandate_key:
        request = await _apply_mandate_binding(request, resolved, mandate_key, node_id)
    elif protected_as:
        # THE JOB'S BINDING (2026-10-28): a step that runs AS a job without naming it (a converted step's
        # ``mandate_key_origin``, or its agent's protected or sole job) gets every variable it left blank filled by
        # the job's binding, exactly as Run Mandate fills it; the step's own values win. No filler -> refused.
        bind = await job_variable_binder(protected_as, consumer=f"{_NODE_TYPE}:{node_id}")
        request.variables = (await bind(getattr(request, "variables", None))) or None
    if capture and hasattr(request, "store"):
        request.store = False
    completed, firewall_records = await run_walled_step_agent(
        ctx,
        resolved.agent_id,
        request,
        node_type=_NODE_TYPE,
        firewall=step_firewall(inputs),
        capture=capture,
        mandate_key=protected_as,
        # THE RUN RECORD (runner plan step 1, 2026-10-20): the same stamp the Run Mandate node
        # passes, so the host records this step's mandate run (only when it resolved a mandate).
        run_stamp=getattr(resolved, "run_stamp", None) if mandate_key else None,
    )
    if capture:
        return firewall_records

    # A host agent_runner may hand back an already-normalized result (a
    # compiled Orchestra whose final step IS the agent result).
    if isinstance(completed, AiExecutionResult):
        outcome: NodeResult[AiExecutionResult] = success(completed)
    else:
        outcome = limit.name_on(
            await asyncio.to_thread(normalize_completed_result, completed, step_config=config)
        )
    if outcome.status == "error":
        # A failed paid turn already carries its billed usage in
        # error.details['usage'] — the scheduler settles cost from there.
        return outcome  # type: ignore[return-value]

    normalized = outcome.result
    # WHO did the job: the doer the database resolved, beside the model - the same fact a Run
    # Mandate step hands over (a research row records it as agent_id).
    normalized.metadata["agent_id"] = resolved.agent_id
    if held_by:
        # Said, never silent: this step ran as a job its agent holds (``basis``: protected / sole_holder).
        normalized.metadata["protected_by_holder"] = held_by
    if firewall_records is not None:
        normalized.metadata["request_firewall"] = firewall_records
    _record_spend(ctx, normalized)

    payload = normalized.structured_output
    if kind in TEXT_SHAPED_KINDS:
        text = (normalized.final_text or "").strip()
        payload = {"__kind": kind, "text": text} if text else None
    elif kind == MEDIA_KIND:
        payload = _produced_media(normalized)
    if not isinstance(payload, dict):
        # The richer source wins: a CompletedRequest still knows the request's
        # configured ceiling even when no truncation marker was stamped.
        return ai_output_failure(
            normalized if isinstance(completed, AiExecutionResult) else completed,
            code="kind_output_missing",
            what="the structured answer",
            message=(
                f"The agent was bound to answer in '{kind}' but returned "
                f"{'a list' if isinstance(payload, list) else ('no media' if kind == MEDIA_KIND else 'no structured result')}. "
                "A kind-bound step has nothing to hand downstream without one."
            ),
            details={
                "declared_kind": kind,
                "usage": normalized.usage.model_dump(mode="json"),
                "conversation_id": normalized.conversation_id,
                "request_id": normalized.request_id,
                "final_text_preview": normalized.final_text[:400],
            },
        )
    # ``__kind`` is part of the data: the answer names the kind it was bound to (a runtime kind
    # has no node declaration for the scheduler to stamp from).
    if payload.get("__kind") in (None, ""):
        payload = {"__kind": kind, **payload}
    collisions = sorted(RESERVED_PAYLOAD_FIELDS & payload.keys())
    if collisions:
        return failure(
            "kind_output_reserved_field",
            (
                f"Kind '{kind}' carries top-level field(s) {collisions}, which the "
                "node-result envelope reserves — a payload cannot own a key that "
                "means 'this node failed'. Rename the field in the kind."
            ),
            details={"declared_kind": kind, "fields": collisions},
        )
    judged = payload
    beside = _with_run_envelope(payload, normalized, list(getattr(config, "run_envelope", None) or []), kind)
    if not isinstance(beside, tuple):
        return beside  # type: ignore[return-value]
    payload, envelope_fields = beside
    if envelope_fields:
        ctx.declare_beside_kind(envelope_fields)
    _judge_against_goal(
        ctx,
        config,
        kind=kind,
        payload=judged,
        normalized=normalized,
        agent_id=resolved.agent_id,
        variables=getattr(request, "variables", None),
        user_input=getattr(request, "user_input", None),
    )
    return success(AgentProducedOutput.model_validate(payload))
