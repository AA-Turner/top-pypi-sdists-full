"""``ai.conversation.continue`` — add a user turn to an existing conversation.

Routes through a host-injected ``conversation_continuer`` seam that takes a
real ``ConversationContinueRequest`` and runs it through
``prepare_continue_conversation`` + ``run_ai_task_on_spine`` — the SAME
pipeline ``POST /conversations/{id}`` runs under (aidream's
``aidream/services/conversation_context/continue_conversation.py``). This
mirrors exactly how ``ai.agent.start`` calls the injected ``agent_runner``
(see ``agent_action.py::run_step_agent``): the node is a thin transport, not
a second implementation.

Before 2026-08, this node called ``ConversationResolver`` +
``execute_ai_request`` directly, bypassing ``prepare_continue_conversation``
entirely — no ownership check, no tools, no context objects, no sandbox
arming, no skills, no memory, no dictionary, no ``cx_user_request`` row, and
no cost ledger / durability / cancel-resume. It also read
``resolution.config`` on a ``UnifiedConfig`` (no such attribute), so it had
never executed. See ``common-docs/systems/workflows/NODE_API_PARITY.md``.

This is the right entry point when a workflow needs to thread multiple turns
onto the same conversation. Use ``agent.start`` to begin a thread, and
``conversation.continue`` to push further turns onto it.
"""

from __future__ import annotations

from collections.abc import AsyncIterator
from contextlib import AsyncExitStack, asynccontextmanager
from typing import Literal

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
from matrx_ai.graph_nodes.shared import AiExecutionResult, normalize_completed_result


class ConversationContinueInput(BaseModel):
    """Workflow-side request body for ``ai.conversation.continue``.

    Field names mirror ``aidream.services.conversation_context.continue_conversation
    .ConversationContinueRequest`` 1:1 (the same contract ``POST
    /conversations/{id}`` accepts) so this node's input form is a true mirror
    of the API, not a hand-picked subset. Types owned by the host application
    (``ClientContext``, ``SandboxBindingRequest``, ``IdeState``,
    ``ContextAnchor``, ``UserOverrides``, ``CacheBypass``, ``ToolSpec``) are
    accepted here as plain ``dict`` and validated by the host-injected
    ``ConversationContinueRequest`` on the boundary — the same pattern
    ``AgentStartStrictInput.ide_state`` already uses
    (``agent_action.py:199``).
    """

    model_config = ConfigDict(extra="forbid")

    conversation_id: str = Field(
        min_length=1,
        description="Existing conversation_id to continue.",
        json_schema_extra=field_extras(widget="text"),
    )

    # --- per-turn input ---
    user_input: str | list[dict[str, JsonValue]] | None = Field(
        default=None,
        description=(
            "Message to append. Accepts plain text or a list of content "
            "parts. Omit AND set retry=true to re-run the conversation's "
            "current persisted state as-is (recovery after a failed turn)."
        ),
        json_schema_extra=field_extras(widget="textarea", multiline_rows=3),
    )
    retry: bool = Field(
        default=False,
        description=(
            "Re-run the last (failed) turn using the conversation's existing "
            "state — no new input is taken. Mutually meaningful with "
            "user_input left unset."
        ),
    )
    config_overrides: dict[str, JsonValue] = Field(
        default_factory=dict,
        description="LLM parameter overrides for this turn (temperature, model, ...).",
        json_schema_extra=field_extras(widget="json"),
    )

    # --- caller context ---
    ide_state: dict[str, JsonValue] | None = Field(
        default=None,
        description=(
            "IDE / editor state from the caller, appended to user_input for "
            "this turn. Validated against the host's IdeState model on entry."
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
    tools: list[dict[str, JsonValue]] = Field(
        default_factory=list,
        description=(
            "Additive ToolSpec list merged into the conversation's resolved "
            "tool set. Each item is {kind: 'registered'|'inline'|'agent', ...}; "
            "validated against the host's ToolSpec union on entry."
        ),
        json_schema_extra=field_extras(widget="json"),
    )
    tools_replace: list[dict[str, JsonValue]] | None = Field(
        default=None,
        description=(
            "When set, this list becomes the ENTIRE tool set for the turn — "
            "capability defaults and the agent's own declared tools are "
            "skipped. Same ToolSpec item shape as `tools`."
        ),
        json_schema_extra=field_extras(widget="json"),
    )
    client: dict[str, JsonValue] | None = Field(
        default=None,
        description="Client/surface context. Validated against the host's ClientContext model on entry.",
        json_schema_extra=field_extras(widget="json"),
    )
    user: dict[str, JsonValue] | None = Field(
        default=None,
        description="Per-turn user overrides. Validated against the host's UserOverrides model on entry.",
        json_schema_extra=field_extras(widget="json"),
    )
    sandbox: dict[str, JsonValue] | None = Field(
        default=None,
        description=(
            "Explicit per-turn sandbox binding — arms the fs/shell/git tools "
            "for this turn. Validated against the host's SandboxBindingRequest "
            "model on entry. When absent, the conversation's persisted binding "
            "is auto-resolved."
        ),
        json_schema_extra=field_extras(widget="json"),
    )
    skill_config: dict[str, JsonValue] | None = Field(
        default=None,
        description="Per-request skill visibility override (Smart Input additive picks).",
        json_schema_extra=field_extras(widget="json"),
    )
    cache_bypass: dict[str, JsonValue] | None = Field(
        default=None,
        description=(
            "Per-call cache invalidation flags ({conversation, agent, tools, "
            "models}). Validated against the host's CacheBypass model on entry."
        ),
        json_schema_extra=field_extras(widget="json"),
    )

    # --- scope / source tracking ---
    store: bool = Field(
        default=True, description="Persist this turn's conversation and messages when true."
    )
    scope_ids: list[str] | None = Field(
        default=None,
        description="Active context-scope ids selected by the caller, membership-validated server-side.",
    )
    context_anchor: dict[str, JsonValue] | None = Field(
        default=None,
        description=(
            "Durable resource identity from which authoritative organization "
            "and task context is reloaded. Validated against the host's "
            "ContextAnchor model on entry."
        ),
        json_schema_extra=field_extras(widget="json"),
    )
    project_id: str | None = Field(
        default=None, description="Optional project context applied to this turn."
    )
    task_id: str | None = Field(
        default=None, description="Optional task context applied to this turn."
    )
    source_app: str | None = Field(
        default=None, description="Stable application slug that initiated this turn."
    )
    source_feature: str | None = Field(
        default=None, description="Stable feature slug within the source application."
    )
    initiation: Literal["user", "auto"] | None = Field(
        default=None,
        description="How the caller initiated this turn: 'user' for a direct human action, 'auto' for automation.",
    )
    target_instance_id: str | None = Field(
        default=None,
        description="Specific connected desktop instance allowed to claim delegated local tools.",
    )

    # --- streaming / debug toggles ---
    debug: bool = Field(
        default=False, description="Enable verbose execution diagnostics for this turn."
    )
    block_mode: bool = Field(
        default=False,
        description="Return block-oriented output events when supported by the agent.",
    )
    snapshot: bool | None = Field(
        default=None,
        description=(
            "Request-snapshot capture override. Omit for the platform default "
            "(capture ON); false to opt this turn out; true to force capture "
            "on plus wire-level outbound-capture debug events."
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


def require_conversation_host(node_type: str) -> None:
    """Fail loudly when the host never registered the conversation-continue extensions."""
    if not has_ext("conversation_continuer") or not has_ext("ConversationContinueRequest"):
        raise RuntimeError(
            f"{node_type} requires the host application to register a "
            "conversation_continuer and ConversationContinueRequest via "
            "matrx_ai.configure(). See aidream/package_integration.py for "
            "the reference wiring."
        )


def build_continue_request(inputs: ConversationContinueInput):
    """Build the host ``ConversationContinueRequest`` for one continue step.

    ``conversation_id`` is excluded — it is a path parameter on the HTTP
    route and a separate argument to ``conversation_continuer`` here, never a
    request-body field.
    """
    ConversationContinueRequest = get_ext("ConversationContinueRequest")
    payload = inputs.model_dump(
        exclude_none=True,
        exclude={"conversation_id"},
    )
    return ConversationContinueRequest.model_validate(payload)


async def run_step_conversation_continue(
    ctx: NodeExecutionContext, conversation_id: str, request
):
    """Run the resolved continue-request inside the workflow step's forked AppContext.

    Mirrors ``agent_action.py::run_step_agent`` exactly: sets the AppContext
    ContextVar to the workflow step's forked context for the duration of the
    call (matrx-ai's executor and run_ai_task read ``get_app_context()``),
    and wraps the call in the same block-stream scope so a continue step's
    tokens render as typed blocks instead of raw chunks.
    """
    conversation_continuer = get_ext("conversation_continuer")
    token = set_app_context(ctx.app)
    try:
        async with _block_stream_scope():
            return await conversation_continuer(
                conversation_id, request, get_app_context()
            )
    finally:
        clear_app_context(token)


@asynccontextmanager
async def _block_stream_scope() -> AsyncIterator[None]:
    """Stream this step's continuation tokens as canonical render blocks.

    Identical in shape and intent to ``agent_action.py::_block_stream_scope``
    — duplicated rather than imported because the two node modules are
    independent registrations and neither should import the other's private
    helper. See that docstring for the full rationale (ONE STREAMING LAW FOR
    CHAT AND WORKFLOWS, plan of record §7.6).
    """
    scope_factory = (
        get_ext("agent_block_stream_scope") if has_ext("agent_block_stream_scope") else None
    )
    if scope_factory is None:
        yield
        return

    async with AsyncExitStack() as stack:
        try:
            await stack.enter_async_context(scope_factory())
        except Exception as exc:  # noqa: BLE001 — wire shape never fails a run
            vcprint(
                f"[conversation_action] block-stream scope failed to open "
                f"(workflow step streams as raw chunks, run unaffected): "
                f"{type(exc).__name__}: {exc}",
                color="yellow",
            )
        yield


@register_node(
    name="ai.conversation.continue",
    display_name="Continue Conversation",
    description="Add a new message to an existing conversation and get the reply.",
    category=NodeCategory.AGENT,
    determinism=ActionTier.NON_DETERMINISTIC,
    input_schema=ConversationContinueInput,
    output_schema=AiExecutionResult,
    output_kind="agent_result",
    icon="messages-square",
    tags=("ai", "conversation", "llm"),
)
async def conversation_continue(
    ctx: NodeExecutionContext, inputs: ConversationContinueInput
) -> NodeResult[AiExecutionResult]:
    require_conversation_host("ai.conversation.continue")
    request = build_continue_request(inputs)
    completed = await run_step_conversation_continue(ctx, inputs.conversation_id, request)

    # Node Result System: a failed turn becomes a structured Failure
    # (code='ai_turn_failed', billed usage in details) instead of a raise.
    return normalize_completed_result(completed)
