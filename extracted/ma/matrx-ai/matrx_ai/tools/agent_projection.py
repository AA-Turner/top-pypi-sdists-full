"""Project saved agents as opaque ``custom_tool_N`` tools.

Phase E of TOOL_INJECTION_REFACTOR.md. Each ``AgentToolSpec`` in
``request.tools`` (or ``request.tools_replace``) is resolved by:

  1. Loading the agent record from the DB.
  2. Allocating a sequential opaque name (``custom_tool_1``,
     ``custom_tool_2``, …) so the model never sees the agent's UUID
     and doesn't realize it's calling another agent.
  3. Building a synthetic ``ToolDefinition`` (``tool_type=AGENT``) with the
     agent's description and a JSON-Schema-shaped ``parameters`` dict
     derived from ``variable_definitions``.
  4. Stashing the projection on ``AppContext.metadata['projected_agent_tools']``
     so the executor can find it at dispatch time. **Per-request scope** —
     phase D-loop will add cross-request persistence on
     ``cx_conversation.dynamic_tool_state``.

Why opaque names: research-backed observation that smaller models behave
worse when they recognize they're calling an agent. Generic names hide the
abstraction; the model picks based on description + input schema, just like
any other tool.

Why per-request now: avoids the global-registry race condition where two
concurrent requests would clobber each other's ``custom_tool_1`` mapping.
The executor consults ``ctx.metadata`` first, falls back to the global
registry, so each request sees its own projections only.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from matrx_utils import vcprint

from matrx_ai.tools.models import ToolDefinition, ToolType
from matrx_ai.tools.specs import AgentToolSpec, RegisteredToolSpec, ToolSpec

if TYPE_CHECKING:
    from matrx_connect import AppContext

# The nesting ceiling every projected agent tool carries. Named so a host that
# must reason about the remaining budget BEFORE dispatch (an Orchestra deciding
# whether its members are reachable at all) reads the real number instead of
# re-declaring a literal that can drift away from this one.
PROJECTED_AGENT_MAX_RECURSION_DEPTH = 2


# Key under which request-local synthetic definitions are stashed on
# AppContext.metadata. Agent projections and caller-supplied inline tools both
# live here because neither definition is process-global. The executor reads
# from here before falling back to ToolRegistry.
PROJECTED_AGENT_TOOLS_KEY = "projected_agent_tools"

# Map under PROJECTED_AGENT_TOOLS_KEY: { custom_tool_N: { ...ToolDefinition.model_dump()... } }


def stash_request_tool_definition(ctx: AppContext, tool_def: ToolDefinition) -> None:
    """Bind one synthetic definition to this request's execution context.

    Inline tool names can be reused by unrelated concurrent requests with
    different schemas. Keeping their active definition here prevents the
    process-global registry's first-seen fallback from becoming another
    request's validation and dispatch contract.
    """
    metadata = ctx.metadata if ctx.metadata is not None else {}
    if ctx.metadata is None:
        ctx.metadata = metadata
    projections = metadata.setdefault(PROJECTED_AGENT_TOOLS_KEY, {})
    if not isinstance(projections, dict):
        projections = {}
        metadata[PROJECTED_AGENT_TOOLS_KEY] = projections
    projections[tool_def.name] = tool_def.model_dump(mode="json")


# The description of the auto-added free-text "input" parameter. Load-bearing
# for dispatch: execute_agent_tool treats an "input" arg as the task text ONLY
# when the projected schema's input param carries exactly this description —
# an author-declared variable named "input" keeps its own helpText and is
# routed as a variable instead.
AUTO_INPUT_DESCRIPTION = (
    "The request/task for this tool — the distilled instructions "
    "and any content it needs."
)


def _variable_definitions_to_parameters(
    variable_definitions: list | None,
) -> dict[str, Any]:
    """Translate the agent's ``variable_definitions`` JSONB into the dotted
    ``parameters`` shape ``ToolDefinition`` expects.

    Delegates to the FAITHFUL converter
    (``matrx_ai.agents.variable_schema.variable_definitions_to_parameters``):
    option sets (with open-enum ``allowOther`` semantics via anyOf), defaults,
    descriptions, numeric bounds, and checkbox items enums all reach the
    calling model instead of collapsing to bare strings. The auto free-text
    ``input`` param (recognized by ``AUTO_INPUT_DESCRIPTION``) is unchanged —
    without it a variable-less agent would project an EMPTY schema.
    """
    from matrx_ai.agents.variable_schema import variable_definitions_to_parameters

    return variable_definitions_to_parameters(
        variable_definitions, auto_input_description=AUTO_INPUT_DESCRIPTION
    )


async def _load_agent_row(agent_id: str, *, is_version: bool) -> Any:
    """Fetch the agent (or version) record. Raises if not found."""
    from matrx_ai.db.agx_manager import agx_agent_manager_instance, agx_version_manager_instance

    manager = agx_version_manager_instance if is_version else agx_agent_manager_instance
    return await manager.load_by_id(agent_id)


async def resolve_agent_specs(
    specs: list[ToolSpec],
    ctx: AppContext,
    *,
    starting_index: int = 1,
) -> tuple[list[ToolSpec], dict[str, dict[str, Any]]]:
    """Resolve every ``AgentToolSpec`` in ``specs`` into a ``RegisteredToolSpec``
    with an opaque ``custom_tool_N`` name.

    Returns
    -------
    (rewritten_specs, projection_map)
        ``rewritten_specs`` — the input list with each ``AgentToolSpec``
        replaced by a ``RegisteredToolSpec(name=custom_tool_N)``. Other
        spec kinds pass through unchanged.

        ``projection_map`` — ``{custom_tool_N: ToolDefinition.model_dump()}``
        for every projection allocated this call. Caller MUST stash this
        on ``ctx.metadata[PROJECTED_AGENT_TOOLS_KEY]`` (or merge with
        existing) before invoking the executor.

    Raises
    ------
    ValueError
        On agent lookup failures (manager raises). Caller surfaces as 422.
    """
    has_any = any(isinstance(s, AgentToolSpec) for s in specs)
    if not has_any:
        return list(specs), {}

    # Pull the existing projection map (if any) so we don't overwrite prior
    # allocations within the same request.
    existing = (ctx.metadata or {}).get(PROJECTED_AGENT_TOOLS_KEY, {})
    next_index = max(starting_index, len(existing) + 1)

    rewritten: list[ToolSpec] = []
    new_projections: dict[str, dict[str, Any]] = {}

    # Cache: same agent_id appearing twice in one request reuses the same
    # projected name. Keyed on (agent_id, is_version) since versions are
    # different records.
    seen: dict[tuple[str, bool], str] = {}
    for cap_name, dumped in existing.items():
        prompt_id = dumped.get("prompt_id")
        if prompt_id:
            seen[(prompt_id, bool(dumped.get("prompt_is_version", False)))] = cap_name

    for spec in specs:
        if not isinstance(spec, AgentToolSpec):
            rewritten.append(spec)
            continue

        cache_key = (spec.agent_id, spec.is_version)
        if cache_key in seen:
            rewritten.append(RegisteredToolSpec(name=seen[cache_key]))
            continue

        try:
            row = await _load_agent_row(spec.agent_id, is_version=spec.is_version)
        except Exception as exc:
            raise ValueError(
                f"AgentToolSpec resolution failed for agent_id={spec.agent_id!r} "
                f"(is_version={spec.is_version}): {exc}"
            ) from exc

        projected_name = f"custom_tool_{next_index}"
        next_index += 1

        description = (
            spec.description_override
            or getattr(row, "description", None)
            or f"Specialised tool: {getattr(row, 'name', spec.agent_id)}"
        )

        parameters = _variable_definitions_to_parameters(
            getattr(row, "variable_definitions", None)
        )
        if spec.result_mode != "inline":
            # Reference-returning tools let the CALLER name + describe the stored
            # value — the "agent-generated id + description" contract. Dispatch
            # consumes these two keys (never routed as agent variables).
            parameters.setdefault(
                "result_key",
                {
                    "type": "string",
                    "description": "Short kebab-case name for the stored result "
                    "(e.g. 'acme-q3-transcript'). The returned descriptor carries "
                    "the FINAL key.",
                    "required": False,
                },
            )
            parameters.setdefault(
                "result_description",
                {
                    "type": "string",
                    "description": "One line describing what the result will "
                    "contain — how it will be identified without reading it.",
                    "required": False,
                },
            )

        if spec.handoff and getattr(row, "output_schema", None):
            # A handoff target's final text IS the user-facing response —
            # structured-output agents would deliver raw JSON as the answer.
            vcprint(
                f"[agent_projection] handoff target {spec.agent_id} declares an "
                "output_schema — its JSON would be delivered as the user-facing "
                "response verbatim. Prefer a prose-response agent.",
                color="red",
            )

        tool_def = ToolDefinition(
            name=projected_name,
            description=description,
            parameters=parameters,
            tool_type=ToolType.AGENT,
            function_path=f"agent:{spec.agent_id}",
            prompt_id=spec.agent_id,
            prompt_is_version=spec.is_version,
            result_mode=spec.result_mode if not spec.handoff else "inline",
            handoff_terminal=spec.handoff,
            max_calls_per_conversation=spec.max_calls_per_conversation,
            cost_cap_per_call=spec.cost_cap_per_call,
            must_complete=True,
            # D-39: a composition-declared budget on the spec wins; the module
            # constant remains the platform default for every undeclared spec.
            max_recursion_depth=(
                spec.max_recursion_depth
                if spec.max_recursion_depth is not None
                else PROJECTED_AGENT_MAX_RECURSION_DEPTH
            ),
        )

        new_projections[projected_name] = tool_def.model_dump(exclude={"_callable"})
        seen[cache_key] = projected_name
        rewritten.append(RegisteredToolSpec(name=projected_name))

        vcprint(
            f"[agent_projection] Projected agent {spec.agent_id} as {projected_name}",
            color="cyan",
        )

    return rewritten, new_projections


def lookup_projected_tool(name: str) -> ToolDefinition | None:
    """Per-request lookup hook for the executor.

    Returns the synthetic ``ToolDefinition`` for a projected agent tool when
    ``name`` is in the active request's projection map, ``None`` otherwise.
    Always called BEFORE consulting ``ToolRegistry`` so projected names
    take precedence over global registry entries with the same name.

    Reads the active ``AppContext`` directly via the ContextVar — the
    executor is always invoked inside the streaming task that has set the
    ContextVar.
    """
    from matrx_connect.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if ctx is None or not ctx.metadata:
        return None
    projections = ctx.metadata.get(PROJECTED_AGENT_TOOLS_KEY)
    if not projections:
        return None
    dumped = projections.get(name)
    if not dumped:
        return None
    try:
        return ToolDefinition.model_validate(dumped)
    except Exception as exc:
        vcprint(
            f"[agent_projection] Failed to rehydrate projected tool {name!r}: {exc}",
            color="red",
        )
        return None


def list_projected_tool_names() -> list[str]:
    """Names of every projected agent tool in the active request's projection
    map (empty outside a request or when nothing is projected). Used by the
    executor's unknown-tool did-you-mean so projected names are part of the
    suggestion vocabulary."""
    from matrx_connect.context.app_context import try_get_app_context

    ctx = try_get_app_context()
    if ctx is None or not ctx.metadata:
        return []
    projections = ctx.metadata.get(PROJECTED_AGENT_TOOLS_KEY)
    if not projections:
        return []
    return list(projections.keys())
