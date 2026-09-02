"""Unified tool specification — request-side, capability-side, dynamic injection.

A ``ToolSpec`` is the single shape used to declare "make this tool available to
the agent" regardless of where the declaration comes from:

  - The agent's own ``tool_config.tools`` (DB-persisted).
  - A request body (``AgentStartRequest.tools`` / ``tools_replace``).
  - A capability bundle (``Capability.enabled_tools``).
  - Mid-loop dynamic injection (a registered tool's mutation API).

Three variants, discriminated by ``kind``:

  - ``RegisteredToolSpec`` — the server has an implementation. Reference the
    registry entry by name (preferred) or tool_id (UUID).
  - ``InlineToolSpec``     — caller supplies the schema; server has no impl.
    Always delegated to the client.
  - ``AgentToolSpec``      — project a saved agent as a callable tool. Phase
    A1 carries the type only; resolution is implemented in phase E.

The ``delegate`` flag exists only on ``RegisteredToolSpec`` because it is the
only variant where execution-side is a real choice. Inline tools always go to
the client (no server impl exists). Agent tools always run server-side (the
sub-agent IS the server-side implementation).
"""
from __future__ import annotations

from typing import Annotated, Literal

from pydantic import BaseModel, Field

from matrx_ai.tools.models import CustomToolInputSchema


class RegisteredToolSpec(BaseModel):
    kind: Literal["registered"] = "registered"
    name: str = Field(
        description="Registry name. Required. tool_id may also be provided for UUID lookup."
    )
    tool_id: str | None = Field(
        default=None,
        description="Optional registry UUID. When set, takes precedence over name for lookup.",
    )
    delegate: bool = Field(
        default=False,
        description="When True, the executor short-circuits dispatch and emits "
        "tool_delegated for the client to execute. When False (default), the "
        "server runs the tool via its registry implementation.",
    )

    def resolved_tool_id(self) -> str | None:
        """Return the registry UUID for this spec when knowable, else None.

        Why this exists: agents store tool refs as UUIDs (``agx_agent.tools``
        is a UUIDArrayField), but capabilities / discovery / structured-input
        helpers add ``RegisteredToolSpec(name="...")`` by canonical name. The
        merge primitive's dedup needs a single identifier space — UUIDs
        when the tool is in the registry — so the agent's UUID and a
        capability's name collapse to the same dedup key instead of
        producing two API entries that resolve to the same tool.

        Returns ``self.tool_id`` when explicitly set; otherwise consults
        ``ToolRegistry`` to map ``self.name`` → registry UUID. Returns
        ``None`` when:
          - the registry doesn't recognize the name (registry not yet
            loaded, deleted tool, foreign-namespace name);
          - the spec is a synthetic agent projection
            (``custom_tool_N`` — never in the registry by design;
            see ``matrx_ai.tools.agent_projection``).

        Callers fall back to ``self.name`` as the dedup key on ``None``.
        """
        if self.tool_id is not None:
            return self.tool_id
        # Agent projections live on ctx.metadata, never in the registry.
        if self.name.startswith("custom_tool_"):
            return None
        try:
            from matrx_ai.tools.registry import ToolRegistry

            tool = ToolRegistry.get_instance().get(self.name)
            return tool.tool_id if tool is not None else None
        except Exception:
            return None


class InlineToolSpec(BaseModel):
    kind: Literal["inline"] = "inline"
    name: str = Field(
        description="Unique tool name. Must match [a-zA-Z0-9_:-]{1,64}; a ':' "
        "namespace separator is serialized to '__' at the provider boundary."
    )
    description: str = ""
    input_schema: CustomToolInputSchema = Field(default_factory=CustomToolInputSchema)


class AgentToolSpec(BaseModel):
    kind: Literal["agent"] = "agent"
    agent_id: str = Field(description="UUID of the saved agent to project as a tool.")
    is_version: bool = Field(
        default=False,
        description="When True, agent_id refers to an agx_version row instead of agx_agent.",
    )
    description_override: str | None = Field(
        default=None,
        description="Optional override of the projected tool's description. "
        "When omitted, the agent's own description is used.",
    )
    max_calls_per_conversation: int | None = None
    cost_cap_per_call: float | None = None
    max_recursion_depth: int | None = Field(
        default=None,
        description=(
            "Per-spec agent-nesting ceiling for the projected tool. None (the "
            "default) keeps the platform constant "
            "(agent_projection.PROJECTED_AGENT_MAX_RECURSION_DEPTH). A "
            "composition that declares its own depth budget (an Orchestra's "
            "metadata.depth_budget, D-39) passes it here so projection stamps "
            "the effective ceiling instead of the constant."
        ),
    )
    result_mode: Literal["inline", "reference", "inline_once"] = Field(
        default="inline",
        description=(
            "How the child agent's result returns to the caller. 'inline' — the "
            "full output in the tool_result (default). 'reference' — the output "
            "is stored in the conversation value store and the caller receives "
            "only a bounded descriptor (key + description + size + a paste-able "
            "reference fence); the child's tokens are NOT streamed to the "
            "client. 'inline_once' — full output this turn AND stored, so it "
            "can be stubbed from history once consumed."
        ),
    )
    handoff: bool = Field(
        default=False,
        description=(
            "Agent-as-Router (Pattern 1): a successful call ENDS the caller's "
            "loop — the child's answer streams to the client and persists as "
            "the conversation's own assistant response; control returns to the "
            "caller only on error. Mutually exclusive with result_mode != "
            "'inline' (a handoff answer IS the response, never a descriptor)."
        ),
    )


ToolSpec = Annotated[
    RegisteredToolSpec | InlineToolSpec | AgentToolSpec,
    Field(discriminator="kind"),
]
"""Discriminated union of all spec variants. Pydantic uses the ``kind`` field
to dispatch validation. Always type request fields and capability lists as
``list[ToolSpec]``."""


def spec_identity(spec: ToolSpec) -> tuple[str, str]:
    """Return a stable (kind, identifier) tuple identifying the spec.

    Two specs that produce the same identity refer to the same tool. For
    ``RegisteredToolSpec`` the identifier is the registry UUID when
    knowable (so the agent's UUID and a capability's name for the same
    tool collapse to the same identity); otherwise the bare name (synthetic
    projections, unknown tools).
    """
    if isinstance(spec, RegisteredToolSpec):
        return ("registered", spec.resolved_tool_id() or spec.name)
    if isinstance(spec, InlineToolSpec):
        return ("inline", spec.name)
    return ("agent", spec.agent_id)


def spec_display_name(spec: ToolSpec) -> str:
    """Best-effort human-readable name for error messages."""
    if isinstance(spec, AgentToolSpec):
        return f"agent:{spec.agent_id}"
    return spec.name
