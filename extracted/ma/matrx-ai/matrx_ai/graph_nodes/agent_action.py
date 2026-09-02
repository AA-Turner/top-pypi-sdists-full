"""``ai.agent.start`` — run a saved agent inside a workflow.

This action is a thin transport-only wrapper. The actual work — agent
load, conversation gating, cache bypass, scope/IDE state, observational
memory, custom tools, context objects, and ``cx_user_request`` row
creation — runs through the **same** ``run_agent`` helper the
``/agents/{agent_id}`` HTTP endpoint uses. Anything the API supports the
workflow supports, by construction (see ``aidream/api/core/agent_run.py``).

Streaming
---------
Every event the agent / executor emits is sent through ``ctx.app.emitter``.
The scheduler's ``fork_for_workflow_step`` preserves the parent emitter by
reference, so the LLM chunks, tool-call events, and completion notifications
flow into the same connection that's streaming the workflow node events.
Nested calls (an agent tool that triggers another workflow, or a sub-agent
spawn) inherit the same emitter via ``fork_for_child_agent`` /
``fork_for_workflow_step`` — one connection, all updates.

Parity contract
---------------
Caller-context fields (``ide_state``, ``source_app``, ``source_feature``,
``cache_bypass``, ``tools``/``tools_replace``, ``writable_variables``, ``context``,
``memory``, conversation gating, etc.) are all forwarded verbatim. A
workflow that received them on its own request body is responsible for
threading them through to this action — there is no "workflow-only short
form" of an agent run.
"""

from __future__ import annotations

import logging
from collections.abc import AsyncIterator
from contextlib import AsyncExitStack, asynccontextmanager
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Literal

from matrx_connect.context.app_context import (
    clear_app_context,
    get_app_context,
    set_app_context,
)
from matrx_graph.actions import register_node
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult
from matrx_graph.types.usl import field_extras
from matrx_utils import vcprint
from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_ai._ext import get_ext, has_ext
from matrx_ai.capabilities import ClientContext, UserOverrides
from matrx_ai.graph_nodes.shared import AiExecutionResult, normalize_completed_result

if TYPE_CHECKING:
    pass

logger = logging.getLogger(__name__)


class AgentStartConfig(BaseModel):
    """Author-time config persisted on the node (not runtime input).

    ``exposed_variables`` names agent variables the workflow author chose to
    wire from upstream steps. The studio writes this list; compile validates
    it here so stale graph JSON doesn't fail with EmptyConfig's extra=forbid.
    """

    model_config = ConfigDict(extra="forbid")

    exposed_variables: list[str] = Field(
        default_factory=list,
        description=(
            "Agent variable names exposed as upstream connection points in the "
            "workflow studio. Not sent to the agent — only used for edge wiring."
        ),
    )


class AgentStartStrictInput(BaseModel):
    """Workflow-side request body for the ``ai.agent.start`` action.

    Field names are kept identical to ``aidream.api.routers.agents.AgentStartRequest``
    so the action's input form is a 1:1 mirror of the API contract. Types
    that live in the host application (``IdeState``, ``CacheBypass``) are
    accepted as ``dict`` and validated by the host-injected request class
    on the boundary.

    ONE field is workflow-only: ``runtime_config_overrides``. It is not a
    request field — it is the per-run config layer an upstream step delivers
    on an edge, folded into ``config_overrides`` before the host request is
    built (see ``agent_start``). A workflow step's authored config is static
    by definition, so without it nothing computed during the run could ever
    reach the agent's config.
    """

    model_config = ConfigDict(extra="forbid")

    # --- target agent: a mandate (preferred), an explicit id, or both ---
    #
    # 🚨 A workflow definition that names ONLY an `agent_id` FREEZES that agent
    # at authoring time — a hardcoded agent by another route, invisible to
    # every org/user Binding, and the reason `deep_research_v1` carries four
    # ids in the hardcoded-agents ratchet. `mandate_key` is the sanctioned
    # form: code (here, the definition) names the JOB, and the DATABASE
    # decides which Holder fulfils it, resolved fresh on EVERY run.
    #
    # EXACTLY ONE may be set. Naming both is REFUSED, naming both values
    # (D-46 / C-32): which authority chose the agent is precisely the question
    # a Mandate exists to answer, so there is no "one thing the caller can
    # mean". Until 2026-08-20 the code instead read a second `agent_id` as a
    # build-time "drift snapshot", warned, and continued — a silent default of
    # exactly the shape the no-seed-fallback ruling deleted (Arman,
    # 2026-08-16). Nothing ever read that snapshot.
    mandate_key: str | None = Field(
        default=None,
        description=(
            "Mandate key naming the JOB this step performs (e.g. "
            "'podcast.deep_research'). The database decides which agent runs "
            "it, resolved at run time — so an org or user Binding swaps this "
            "step's agent without touching the workflow. Preferred over "
            "agent_id, and mutually exclusive with it: a step naming both is "
            "refused."
        ),
        json_schema_extra=field_extras(widget="mandate_agent_picker"),
    )
    agent_id: str | None = Field(
        default=None,
        description=(
            "UUID of a specific agent (or agent version, when is_version=true). "
            "Pins this step to one agent forever — prefer mandate_key. "
            "Mutually exclusive with mandate_key: a step naming both is "
            "refused, because a Mandate exists to settle which authority "
            "picks the agent."
        ),
        json_schema_extra=field_extras(widget="agent_picker"),
    )
    is_version: bool = Field(
        default=False,
        description=(
            "If true, `agent_id` is treated as a pinned version_id instead of a current-agent id."
        ),
        json_schema_extra=field_extras(widget="toggle"),
    )

    # --- per-turn input ---
    user_input: str | list[dict[str, JsonValue]] | None = Field(
        default=None,
        description=(
            "User message to append before running. Accepts a string or a list of content parts."
        ),
        json_schema_extra=field_extras(widget="textarea", multiline_rows=3),
    )
    variables: dict[str, JsonValue] = Field(
        default_factory=dict,
        description="Agent variable overrides for this invocation.",
        json_schema_extra=field_extras(widget="json"),
    )
    variable_resource_context: dict[str, JsonValue] | None = Field(
        default=None,
        description=(
            "Per-request media-context presentation policy keyed by agent "
            "variable name (promote/exclude a resource's representations). "
            "Changes context presentation only, never the saved agent "
            "definition. Validated against the host's ResourceContextPolicy "
            "model per key on entry."
        ),
        json_schema_extra=field_extras(widget="json"),
    )
    config_overrides: dict[str, JsonValue] | None = Field(
        default=None,
        description=(
            "LLM parameter overrides (temperature, max_tokens, model, ...) the "
            "workflow AUTHOR set for this step. Static by nature — it is part "
            "of the saved definition. Validated against LLMParams by the "
            "host's AgentStartRequest on entry."
        ),
        json_schema_extra=field_extras(widget="json"),
    )
    runtime_config_overrides: dict[str, JsonValue] | None = Field(
        default=None,
        description=(
            "Per-RUN LLM parameter overrides, meant to arrive on an EDGE from "
            "an upstream step (e.g. a voice map computed from the run's cast). "
            "Merged on TOP of both the mandate's config and this step's "
            "authored config_overrides, key by key — this is the run-scope "
            "layer, so it never wipes the other two the way a plain "
            "edge-delivered config_overrides would (the engine's input merge "
            "is last-writer-wins per KEY of the node input, so an edge feeding "
            "config_overrides replaces the whole authored dict)."
        ),
        json_schema_extra=field_extras(widget="json"),
    )

    # --- conversation gating ---
    conversation_id: str | None = Field(
        default=None,
        description="Continue an existing conversation. Leave blank for a fresh thread.",
    )
    is_new: bool | None = Field(
        default=None,
        description=(
            "Explicit assertion about whether this is a new conversation. "
            "True = create new (409 if id already exists), False = continue "
            "(404 if id missing). Blank means: new when no conversation_id was "
            "given, continue when one was."
        ),
    )

    # --- stateless multi-turn (only valid with store=false; the host's
    # AgentStartRequest re-enforces the guard on entry) ---
    prior_messages: list[dict[str, JsonValue]] = Field(
        default_factory=list,
        description=(
            "Transcript of THIS ephemeral run, owned by the caller and ordered "
            "oldest-first — appended after the agent's own definition messages "
            "and before user_input. The server still owns the agent (model, "
            "tools, system prompt); only the history comes from here. ONLY "
            "valid with store=false — a persisted conversation's history is "
            "the DB's, and the host request refuses a second, conflicting "
            "transcript. Validated against the host's ChatMessageInput model "
            "on entry."
        ),
        json_schema_extra=field_extras(widget="json"),
    )

    # --- caller context ---
    client: ClientContext | None = Field(
        default=None,
        description=(
            "Client capability envelope: surface, active capabilities "
            "(editor-state, sandbox-fs, browser-dom, desktop-native, ...), and "
            "their typed state payloads. Gates every client-capability tool "
            "bundle and desktop-instance targeting "
            "(client.state['desktop-native'].target_instance_id)."
        ),
        json_schema_extra=field_extras(widget="json"),
    )
    user: UserOverrides | None = Field(
        default=None,
        description=(
            "Per-request user-level tool inclusion/exclusion overrides "
            "(add/remove, apply_policy). Highest inclusion precedence: "
            "user.remove beats everything, user.add beats agent.forbidden."
        ),
        json_schema_extra=field_extras(widget="json"),
    )
    ide_state: dict[str, JsonValue] | None = Field(
        default=None,
        description=(
            "IDE / editor state from the caller (vsc_* variables, active file, "
            "selection, diagnostics, workspace, git). Validated against the "
            "host's IdeState model on entry."
        ),
        json_schema_extra=field_extras(widget="json"),
    )
    sandbox: dict[str, JsonValue] | None = Field(
        default=None,
        description=(
            "Sandbox binding for this step (container/session identity for "
            "sandbox-delegated tool calls). Validated against the host's "
            "SandboxBindingRequest model on entry."
        ),
        json_schema_extra=field_extras(widget="json"),
    )
    context: dict[str, JsonValue] = Field(
        default_factory=dict,
        description="Deferred context objects keyed by name (context / context_patch payloads).",
        json_schema_extra=field_extras(widget="json"),
    )
    writable_variables: list[str] = Field(
        default_factory=list,
        description="Variables the agent is allowed to mutate at runtime via context_patch.",
    )
    allow_context_create: bool = Field(
        default=False,
        description="Permit the agent to spawn new context objects via the context tool's create action.",
    )

    # --- tool wiring (unified injection — TOOL_INJECTION_REFACTOR.md) ---
    # The legacy `client_tools` / `custom_tools` fields were BURNED at the host
    # boundary (AgentStartRequest no longer declares them; extra="ignore" drops
    # them) — so they are removed here too instead of being advertised and
    # silently dropped. `_BURNED_TOOL_FIELDS` below rejects them loudly.
    tools: list[dict[str, JsonValue]] = Field(
        default_factory=list,
        description=(
            "Additive ToolSpec list merged into the agent's resolved tool set. "
            "Each item is {kind: 'registered'|'inline'|'agent', ...}; validated "
            "against the host's ToolSpec union on entry."
        ),
        json_schema_extra=field_extras(widget="json"),
    )
    tools_replace: list[dict[str, JsonValue]] | None = Field(
        default=None,
        description=(
            "When set, this list becomes the agent's ENTIRE tool set for the "
            "turn — capability defaults and the agent's own declared tools are "
            "skipped. Same ToolSpec item shape as `tools`."
        ),
        json_schema_extra=field_extras(widget="json"),
    )

    # --- scope / source tracking ---
    organization_id: str | None = Field(
        default=None, description="Organization scope applied to every item execution."
    )
    project_id: str | None = Field(
        default=None, description="Optional project context applied to every item execution."
    )
    task_id: str | None = Field(
        default=None, description="Optional task context applied to every item execution."
    )
    source_app: str | None = Field(
        default=None, description="Stable application slug that initiated the agent run."
    )
    source_feature: str | None = Field(
        default=None, description="Stable feature slug within the source application."
    )
    store: bool = Field(
        default=True, description="Persist each item's conversation and messages when true."
    )
    scope_ids: list[str] | None = Field(
        default=None,
        description=(
            "Active context-scope ids selected by the caller's global picker, "
            "membership-validated server-side. Threads the selected scopes' "
            "context cells to the agent even when the entity carries no scope "
            "tags of its own."
        ),
    )
    context_anchor: dict[str, JsonValue] | None = Field(
        default=None,
        description=(
            "Durable resource identity ({resource_type, resource_id}) from "
            "which authoritative organization/project/task context is "
            "reloaded, overruling ambient picker values. Validated against "
            "the host's ContextAnchor model on entry."
        ),
        json_schema_extra=field_extras(widget="json"),
    )
    initiation: Literal["user", "auto"] | None = Field(
        default=None,
        description=(
            "How the caller initiated this request: 'user' for a direct "
            "human action, 'auto' for client-code automation. Omit for "
            "ordinary workflow/API-triggered steps."
        ),
    )

    # --- streaming / debug toggles ---
    stream: bool = Field(
        default=True, description="Stream the agent's tokens as they are produced."
    )
    debug: bool = Field(
        default=False, description="Enable verbose execution diagnostics for the agent run."
    )
    block_mode: bool = Field(
        default=False,
        description="Return block-oriented output events when supported by the agent.",
    )
    dry_run: bool = Field(
        default=False,
        description=(
            "Run the full pre-LLM assembly (context, system-prompt render, "
            "message + tool merge) and return it as JSON instead of streaming "
            "an LLM turn. Pair with store=false for a true read-only preview "
            "— enables preview/approval/cost-estimate steps."
        ),
    )
    snapshot: bool | None = Field(
        default=None,
        description=(
            "Request-snapshot capture override. Omit for the platform default "
            "(capture ON — the exact provider request/response of every persisted "
            "iteration is recorded for replay); false to opt this step out; true to "
            "force capture on plus wire-level outbound-capture debug events."
        ),
    )

    # --- observational memory ---
    memory: bool | None = Field(
        default=None,
        description=(
            "True = enable OM and persist on conversation; False = disable and "
            "persist; None = inherit persisted state."
        ),
    )
    memory_model: str | None = Field(
        default=None, description="Optional model override for observational-memory processing."
    )
    memory_scope: str = Field(
        default="thread", description="Observational-memory scope, normally the current thread."
    )

    # --- cache bypass ---
    cache_bypass: dict[str, JsonValue] | None = Field(
        default=None,
        description=(
            "Per-call cache invalidation flags ({conversation, agent, tools, "
            "models}). Validated against the host's CacheBypass model on entry."
        ),
        json_schema_extra=field_extras(widget="json"),
    )

    # --- agent loop bounds ---
    max_iterations: int = Field(
        default=100, ge=1, le=500, description="Maximum agent reasoning/tool-loop iterations."
    )
    max_retries_per_iteration: int = Field(
        default=2,
        ge=0,
        le=10,
        description="Maximum provider retries allowed within one agent iteration.",
    )

    # --- skill visibility override ---
    skill_config: dict[str, JsonValue] | None = Field(
        default=None,
        description=(
            "Per-request skill visibility override (Smart Input additive "
            "picks). Validated against the host's skill-config shape on entry."
        ),
        json_schema_extra=field_extras(widget="json"),
    )


class AgentStartInput(AgentStartStrictInput):
    """Agent input plus authored top-level variable connection points.

    The ordinary action intentionally allows extras because workflow authors
    expose arbitrary agent variable names as node ports. Coordinated assignment
    uses :class:`AgentStartStrictInput` instead: its variable override map is an
    explicit field, so every known part of the durable request stays strict.
    """

    model_config = ConfigDict(extra="allow")


# Former tool-wiring fields removed from BOTH this input and the host
# AgentStartRequest. Because AgentStartInput is extra="allow", a stale workflow
# that still sets one would otherwise fold it into the agent's VARIABLES —
# a silent misbehavior. Reject loudly instead, pointing at the replacement.
_BURNED_TOOL_FIELDS = ("client_tools", "custom_tools")


def _strip_inert_burned_tool_fields(extra: dict[str, Any]) -> None:
    """Drop empty legacy tool keys left over from pre-unified-injection workflows.

    Non-empty values still fail loudly in ``agent_start`` — only ``None`` /
    ``[]`` / ``{}`` are treated as inert schema cruft.
    """
    for field in _BURNED_TOOL_FIELDS:
        if field not in extra:
            continue
        val = extra[field]
        if val is None or val == [] or val == {}:
            del extra[field]


def _resolve_conversation_start_fields(
    payload: dict[str, Any], *, organization_id: str | None = None
) -> None:
    """Fill the REQUIRED conversation-start fields for the host request.

    The host's ``AgentStartRequest`` requires ``organization_id`` /
    ``conversation_id`` / ``is_new`` / ``store`` with no defaults — a caller
    always knows all four, and the ambiguity of omitting one is what that
    contract exists to kill. A workflow author, however, legitimately leaves
    the node's conversation fields blank for "just run it", so the node
    resolves them deterministically here:

    * no id     → mint one and create it (``is_new=True``)
    * id given  → continue it unless the author explicitly said ``is_new``
    * ``store`` → always present on the node input (defaults True)
    * ``organization_id`` → the author's value, else the RUN's organization
      (passed in from the step context). This is not the server manufacturing
      an organization: a workflow run carries the organization its starter
      explicitly selected, and every agent step of that run belongs to it.
      When neither is available the step fails with a plain sentence rather
      than a Pydantic ``Field required`` dump.
    """
    import uuid as _uuid

    conversation_id = payload.get("conversation_id")
    if not conversation_id:
        payload["conversation_id"] = str(_uuid.uuid4())
        payload["is_new"] = True
    elif payload.get("is_new") is None:
        payload["is_new"] = False
    payload.setdefault("store", True)
    if not payload.get("organization_id"):
        if not organization_id:
            raise ValueError(
                "this step runs an agent, and an agent run belongs to an "
                "organization — but neither the step nor the workflow run "
                "carries one. Start the run with an organization selected, or "
                "set the step's organization."
            )
        payload["organization_id"] = str(organization_id)


@dataclass(frozen=True, slots=True)
class StepAgent:
    """Everything a workflow step learned about the agent it is about to run.

    ``agent_id`` / ``is_version`` / ``config_overrides`` are what actually
    executes. ``declared_output_kind`` is what the DATABASE says this JOB
    answers in (the Mandate's ``output_kind``) — carried so a step that can
    SHAPE the call (``ai.agent.produce``) can check its own graph declaration
    against the mandate's instead of the two silently disagreeing. It is None
    on the pinned-``agent_id`` path: an id names an agent, never a job.
    """

    agent_id: str
    is_version: bool
    config_overrides: dict[str, Any] | None
    declared_output_kind: str | None


@dataclass(frozen=True, slots=True)
class StepWorkflowMandate:
    """The step's mandate resolved to a WORKFLOW Holder (SPEC §6.2/§6.3 lift).

    Returned by :func:`resolve_step_agent_full` only when the caller opted in
    (``allow_workflow_holder=True``) — the step then executes the mandate
    through the host's ``workflow_mandate_runner`` extension as a durable
    child workflow run, with the depth guard doing the real protection.
    """

    mandate_key: str
    workflow_id: str
    workflow_version_id: str | None
    declared_output_kind: str | None


async def resolve_step_agent(
    inputs: AgentStartStrictInput, *, consumer: str
) -> tuple[str, bool, dict[str, Any] | None]:
    """The three-value form of :func:`resolve_step_agent_full` (see it for the
    rules). Kept as the shape every existing agent step unpacks."""
    resolved = await resolve_step_agent_full(inputs, consumer=consumer)
    assert isinstance(resolved, StepAgent)  # allow_workflow_holder defaults False
    return resolved.agent_id, resolved.is_version, resolved.config_overrides


async def resolve_step_agent_full(
    inputs: AgentStartStrictInput,
    *,
    consumer: str,
    allow_workflow_holder: bool = False,
) -> StepAgent | StepWorkflowMandate:
    """Decide WHICH agent this step runs: the mandate's Holder, or a pinned id.

    ``mandate_key`` is the authority whenever it is present. On that path the
    step resolves on EVERY run through the ONE door
    (`matrx_ai.mandates.resolve_mandate_by_key`), so an org/user Binding
    swapping the Holder takes effect on the next run with no edit to the
    workflow — and an unresolvable mandate REFUSES rather than running
    something nobody chose (there is no seed fallback, anywhere).

    A step names EXACTLY ONE selector. Carrying both is REFUSED, naming both
    values (D-46 / C-32) — which authority chose the agent is precisely the
    question a Mandate exists to answer, so the two are not reconcilable.
    Until 2026-08-20 this function instead treated a second ``agent_id`` as a
    build-time "drift snapshot", warned, and ran the mandate's Holder anyway;
    nobody ever recorded a reversal of D-46, and nothing ever read the
    snapshot. Warn-and-continue is the silent-default shape the
    no-seed-fallback ruling deleted (Arman, 2026-08-16), so the code was
    brought back to the ruling rather than the ruling to the code.

    ``consumer`` names the step for alarms and the durable failure record —
    every node type that runs an authored agent shares this one door.
    """
    if inputs.mandate_key and inputs.agent_id:
        raise ValueError(
            f"{consumer} names BOTH a mandate and an agent id: mandate_key="
            f"{inputs.mandate_key!r} and agent_id={inputs.agent_id!r}. A step "
            f"names exactly one — the mandate (the database picks the Holder, "
            f"and org/user Bindings can swap it) or the id (pinned to that one "
            f"agent forever). Drop whichever is not the authority here; if the "
            f"mandate is, the id is vestigial and removing it changes nothing."
        )
    if inputs.mandate_key:
        from matrx_ai.mandates import resolve_mandate_by_key

        resolution = await resolve_mandate_by_key(inputs.mandate_key, consumer=consumer)
        if resolution.holder_type == "workflow":
            # SPEC §6.3 STEP-SIDE LIFT: a workflow step MAY name a
            # workflow-held mandate — it executes as a durable child workflow
            # run through the host's workflow_mandate_runner, with the
            # metadata._mandate depth/cycle guard doing the real protection.
            # Only node types that know how to run that lane opt in.
            if allow_workflow_holder and resolution.workflow_id:
                return StepWorkflowMandate(
                    mandate_key=inputs.mandate_key,
                    workflow_id=resolution.workflow_id,
                    workflow_version_id=resolution.workflow_version_id,
                    declared_output_kind=resolution.output_kind,
                )
            raise ValueError(
                f"{consumer}: mandate {inputs.mandate_key!r} resolved to a "
                f"WORKFLOW Holder, which this node type cannot execute — use "
                f"ai.agent.start (it runs workflow-held mandates as durable "
                f"child runs), or rebind the mandate to an agent."
            )
        source = resolution.source
        resolved_id = getattr(source, "agent_id", None)
        if not resolved_id:
            raise ValueError(
                f"{consumer}: mandate {inputs.mandate_key!r} resolved to a source "
                f"with no agent id ({type(source).__name__})."
            )
        return StepAgent(
            agent_id=str(resolved_id),
            is_version=bool(getattr(source, "is_version", False)),
            config_overrides=(
                dict(resolution.config_overrides) if resolution.config_overrides else None
            ),
            declared_output_kind=resolution.output_kind,
        )
    if inputs.agent_id:
        return StepAgent(
            agent_id=inputs.agent_id,
            is_version=inputs.is_version,
            config_overrides=None,
            declared_output_kind=None,
        )
    raise ValueError(
        f"{consumer} names no agent: set mandate_key (preferred — the database "
        f"picks the agent, and org/user Bindings can swap it) or agent_id."
    )


def build_agent_request(
    ctx: NodeExecutionContext,
    inputs: AgentStartInput,
    resolved: StepAgent,
    *,
    node_type: str,
    top_config_overrides: dict[str, Any] | None = None,
) -> Any:
    """Build the host ``AgentStartRequest`` for one workflow agent step.

    ONE builder for every node type that runs an authored agent
    (``ai.agent.start``, ``ai.agent.produce``, anything added later) — a second
    copy is how two variable-folding rules and two config ladders get born.

    ``top_config_overrides`` is the layer ABOVE everything the author or the
    binding set: the node type's own non-negotiable contract with the provider.
    ``ai.agent.produce`` puts the kind-bound ``response_format`` there, because
    a step whose declared output kind IS its contract cannot let an authored
    config override silently unbind it.
    """
    AgentStartRequest = get_ext("AgentStartRequest")

    # An agent VARIABLE exposed as a connection point and fed by an upstream
    # workflow step arrives here as a TOP-LEVEL extra field (AgentStartInput is
    # extra="allow"), keyed by the variable name — because the edge maps
    # `{<variable>: <source field>}`. Capture those extras from ``model_extra``
    # BEFORE ``exclude_none`` runs, so a variable explicitly fed ``null`` (or
    # ``0`` / ``false`` / "") folds in UNIFORMLY rather than being silently
    # dropped — no asymmetry vs author-set literals. Substitution then treats a
    # ``None``/absent value as empty string (``AgentVariable.get_value`` ignores
    # the agent's design-time default on this path), so folding a ``None`` is
    # safe — it can't corrupt or override anything. Excluded from the top level
    # so they only reach the agent as variables, never as stray request fields.
    extra_vars = dict(inputs.model_extra or {})
    _strip_inert_burned_tool_fields(extra_vars)
    burned = [f for f in _BURNED_TOOL_FIELDS if f in extra_vars]
    if burned:
        raise ValueError(
            f"{node_type} no longer accepts {burned} — these legacy tool "
            "fields were removed from both the node input and the host "
            "AgentStartRequest (which silently ignored them). Use the unified "
            "`tools` (additive ToolSpec list) or `tools_replace` (full-set "
            "override) fields instead."
        )
    request_payload = inputs.model_dump(
        exclude_none=True,
        exclude={"agent_id", "mandate_key", "runtime_config_overrides", *extra_vars},
    )
    if extra_vars:
        request_payload["variables"] = {
            **(request_payload.get("variables") or {}),
            **extra_vars,
        }
    # ── config precedence, lowest → highest ──────────────────────────────
    #   1. the MANDATE's config   (system default → org binding → user binding,
    #      already merged by `resolve_mandate`)
    #   2. this step's AUTHORED `config_overrides`  (the saved definition)
    #   3. `runtime_config_overrides`  (edge-delivered, per run)
    #   4. the NODE TYPE's own contract (`top_config_overrides`) — only
    #      ai.agent.produce's kind binding sits here today.
    #
    # (1) under (2) is exactly how `run_mandated` merges them for a NamedAgent
    # (`aidream/services/mandates/named_agents.py::_resolve_mandate_kwargs`),
    # and (3) on top is the RUN-SCOPE layer `resolve_mandate` already documents
    # as the top of the ladder ("run-scope keys win"). It is where the twin's
    # own computed `config_overrides` sits: `_create_audio` builds the cast's
    # `tts_voice` per run and passes it at the call site, above the binding.
    layered = {
        **(resolved.config_overrides or {}),
        **(request_payload.get("config_overrides") or {}),
        **(inputs.runtime_config_overrides or {}),
        **(top_config_overrides or {}),
    }
    if layered:
        request_payload["config_overrides"] = layered
    request_payload["is_version"] = resolved.is_version
    _resolve_conversation_start_fields(request_payload, organization_id=ctx.organization_id)
    request = AgentStartRequest.model_validate(request_payload)
    # ``mandate_key`` is consumed by resolution rather than forwarded as a
    # public request field. Preserve it on the host request's private
    # provenance channel so the resulting run remains attributable to the
    # Mandate without creating a second execution authority.
    if inputs.mandate_key:
        request._mandate_key = inputs.mandate_key
    return request


async def run_step_agent(ctx: NodeExecutionContext, agent_id: str, request: Any) -> Any:
    """Run the resolved agent inside the workflow step's forked AppContext.

    Set the AppContext ContextVar to the workflow step's forked context for the
    duration of the AI call. matrx-ai's executor and run_ai_task read
    get_app_context() to pick up conversation_id, agent tracking, memory state,
    block_mode, snapshot, etc. — without this they would see the parent
    (workflow root) context and miss everything ``prepare_agent_run`` writes
    onto ctx.app.
    """
    agent_runner = get_ext("agent_runner")
    token = set_app_context(ctx.app)
    try:
        async with _block_stream_scope():
            # The AMBIENT context, read INSIDE the scope — never the captured
            # ``ctx.app``. The block-stream scope works by installing a
            # context whose emitter wraps the node's, and a host runner that
            # streams through the context it was HANDED (aidream's does:
            # ``run_ai_task_on_spine(ctx.emitter, ...)``) would push every
            # token straight past the wrapper. That is what made the seam
            # inert in production — it opened the scope and then bypassed it.
            return await agent_runner(agent_id, request, get_app_context())
    finally:
        clear_app_context(token)


@asynccontextmanager
async def _block_stream_scope() -> AsyncIterator[None]:
    """Stream this step's agent tokens as canonical render blocks.

    ONE STREAMING LAW FOR CHAT AND WORKFLOWS (plan of record §7.6). Without
    this the agent's tokens leave the workflow run as bare ``chunk`` events —
    raw text — so the run page has nothing typed to render and a user watching
    a multi-minute workflow sees prose scroll past while the structured result
    appears only at the end. Inside it, the agent's output leaves as the SAME
    ``render_block`` events ``/chat`` emits, carrying the SAME
    ``metadata.__ir_partial`` progressive kinds and the SAME verified
    ``metadata.__ir`` envelope on completion. No second implementation, and
    nothing here knows it is a workflow.

    The scope is host-injected (``agent_block_stream_scope`` via
    ``matrx_ai.configure``) because the wrapper needs the host's concrete
    streaming emitter. Unconfigured — a standalone matrx-ai, a console run, a
    worker with no client — it is a no-op and the step behaves exactly as
    before: a degraded stream is never a broken run.
    """
    scope_factory = (
        get_ext("agent_block_stream_scope")
        if has_ext("agent_block_stream_scope")
        else None
    )
    if scope_factory is None:
        yield
        return

    # AsyncExitStack, not a bare try/except around the yield: catching an
    # exception raised by the BODY and then yielding again is a second yield
    # from one generator (RuntimeError). Only a failure to ENTER the scope is
    # recoverable here, and the stack expresses exactly that.
    async with AsyncExitStack() as stack:
        try:
            await stack.enter_async_context(scope_factory())
        except Exception as exc:  # noqa: BLE001 — wire shape never fails a run
            vcprint(
                f"[agent_action] block-stream scope failed to open "
                f"(workflow step streams as raw chunks, run unaffected): "
                f"{type(exc).__name__}: {exc}",
                color="yellow",
            )
        yield


def require_agent_host(node_type: str) -> None:
    """Fail loudly when the host never registered the agent-run extensions."""
    if not has_ext("agent_runner") or not has_ext("AgentStartRequest"):
        raise RuntimeError(
            f"{node_type} requires the host application to register an "
            "agent_runner and AgentStartRequest via matrx_ai.configure(). "
            "See aidream/package_integration.py for the reference wiring."
        )


async def _run_workflow_held_mandate(
    ctx: NodeExecutionContext,
    inputs: AgentStartInput,
    resolved: StepWorkflowMandate,
) -> NodeResult[AiExecutionResult]:
    """Execute a WORKFLOW-held mandate from a workflow step (SPEC §6.3 lift).

    Delegates to the host's ``workflow_mandate_runner`` extension, which runs
    the Holder as a durable child ``workflow.run`` whose identity derives from
    THIS invocation's correlation key (``child_run_id_for`` semantics) — a
    crash replay or retry reattaches instead of double-spending. The host
    raises ``GraphInterrupt`` when the child parks on a question, so the
    parent parks exactly as a ``subgraph.call`` child would.
    """
    runner = get_ext("workflow_mandate_runner")
    extra_vars = dict(inputs.model_extra or {})
    _strip_inert_burned_tool_fields(extra_vars)
    variables: dict[str, Any] = {
        **(getattr(inputs, "variables", None) or {}),
        **extra_vars,
    }
    outcome = await runner(
        resolved.mandate_key,
        variables,
        {
            "run_id": ctx.run_id,
            "node_id": ctx.node_id,
            "dispatch_id": ctx.dispatch_id,
            "item_index": ctx.item_index,
            "firing": ctx.firing,
            "attempt": ctx.attempt,
        },
    )
    from matrx_graph.types.result import success

    parsed = outcome.get("parsed")
    child_run_id = str(outcome.get("run_id") or "")
    return success(
        AiExecutionResult(
            conversation_id=child_run_id,
            request_id=child_run_id,
            iterations=1,
            finish_reason="stop",
            final_text=str(outcome.get("output") or ""),
            structured_output=parsed if isinstance(parsed, dict | list) else None,
            metadata={
                "mandate_key": resolved.mandate_key,
                "holder_type": "workflow",
                "child_run_id": child_run_id,
                "workflow_id": resolved.workflow_id,
            },
        )
    )


@register_node(
    name="ai.agent.start",
    display_name="Run Agent",
    description="Run one of your saved agents with your input and get its reply.",
    category=NodeCategory.AGENT,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=AgentStartInput,
    output_schema=AiExecutionResult,
    output_kind="agent_result",
    config_schema=AgentStartConfig,
    icon="bot",
    tags=("ai", "agent", "llm"),
)
async def agent_start(
    ctx: NodeExecutionContext, inputs: AgentStartInput
) -> NodeResult[AiExecutionResult]:
    require_agent_host("ai.agent.start")
    node_id = getattr(ctx, "node_id", None) or "?"
    resolved = await resolve_step_agent_full(
        inputs,
        consumer=f"ai.agent.start:{node_id}",
        allow_workflow_holder=has_ext("workflow_mandate_runner"),
    )
    if isinstance(resolved, StepWorkflowMandate):
        return await _run_workflow_held_mandate(ctx, inputs, resolved)
    request = build_agent_request(ctx, inputs, resolved, node_type="ai.agent.start")
    completed = await run_step_agent(ctx, resolved.agent_id, request)

    # A host agent_runner may return an ALREADY-normalized AiExecutionResult —
    # e.g. a compiled Orchestra (sequential/parallel/dag) whose run executed
    # as a child plan run and whose final step output IS the agent result.
    # Pass it through: same output_kind, same contract, one agent_result.
    if isinstance(completed, AiExecutionResult):
        from matrx_graph.types.result import success

        return success(completed)

    # Node Result System: a failed turn becomes a structured Failure
    # (code='ai_turn_failed', billed usage in details) instead of a raise.
    return normalize_completed_result(completed)
