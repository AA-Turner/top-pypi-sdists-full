from __future__ import annotations

import json
import logging
import time
from typing import Any

from matrx_connect.context.app_context import set_app_context, try_get_app_context

from matrx_ai.tools.models import (
    AGENT_DEPTH_METADATA_KEY,
    ToolContext,
    ToolDefinition,
    ToolError,
    ToolResult,
    ToolType,
    build_agent_media_content,
    read_agent_depth,
)

logger = logging.getLogger(__name__)

# Keys the dispatch layer MAY consume itself — but a name the agent author
# DECLARED as a variable always wins as a variable (schema-aware resolution
# below); only undeclared occurrences feed the free-text user_input chain.
_RESERVED_ARG_KEYS = frozenset({"variables", "input", "user_input", "query", "task"})


def _declared_variable_names(tool_def: ToolDefinition) -> set[str]:
    """The parameter names the projected schema advertises as AGENT VARIABLES.

    Every projected parameter is a declared variable except the auto-added
    free-text ``input`` (recognized by its exact description constant — an
    author-declared variable named ``input`` keeps its own helpText)."""
    from matrx_ai.tools.agent_projection import AUTO_INPUT_DESCRIPTION

    declared: set[str] = set()
    for name, prop in (tool_def.parameters or {}).items():
        if (
            name == "input"
            and isinstance(prop, dict)
            and prop.get("description") == AUTO_INPUT_DESCRIPTION
        ):
            continue
        declared.add(name)
    return declared


# Dispatch-consumed keys on reference-returning agent tools (never variables).
_REFERENCE_ARG_KEYS = frozenset({"result_key", "result_description"})


def _native_agent_tool_output(output: Any) -> Any:
    """Keep prose as text while restoring complete JSON objects to native values."""
    if not isinstance(output, str):
        return output
    candidate = output.strip()
    if len(candidate) < 2 or candidate[0] not in "{[" or candidate[-1] not in "}]":
        return output
    try:
        parsed = json.loads(candidate)
    except (json.JSONDecodeError, ValueError):
        return output
    return parsed if isinstance(parsed, dict | list) else output


async def _capture_agent_tool_boundary_failure(
    exc: BaseException, *, tool_def: ToolDefinition, ctx: ToolContext
) -> None:
    from matrx_connect.streaming.error_capture import capture_error

    app_ctx = try_get_app_context()
    await capture_error(
        exc,
        kind="agent_tool_result_boundary_failed",
        request_id=getattr(app_ctx, "request_id", None),
        user_id=getattr(app_ctx, "user_id", None),
        conversation_id=getattr(app_ctx, "conversation_id", None),
        route="tool_executor.agent_tool_result",
        error_type=type(exc).__name__,
        context={"tool_name": tool_def.name, "call_id": ctx.call_id},
    )


def _incomplete_child_status(result: Any) -> str:
    status = str((result.metadata or {}).get("status") or "")
    if status.startswith("suspended") or status in {"failed", "paused", "truncated"}:
        return status
    return ""


async def _finalize_handoff_result(
    agent: Any,
    tool_def: ToolDefinition,
    result: Any,
    ctx: ToolContext,
    started_at: float,
    *,
    child_execution_id: str | None = None,
) -> ToolResult:
    """Convert a completed handoff child run into the terminal ToolResult.

    Success → ``handoff_final=True`` + a ``HandoffOutcome`` carrying B's final
    text; the tool_result the model would see is a compact stub (B's text is
    NEVER duplicated — the orchestrator appends it as the very next assistant
    message). A suspended or empty run is a FAILURE (the loop continues and the
    caller corrects) — a handoff must deliver a complete answer or nothing."""
    from matrx_ai.tools.models import HandoffOutcome

    child_status = _incomplete_child_status(result)
    if child_status:
        # Suspended = no final answer exists; failed = the child's loop died
        # with a CONTAINED error (success=True + partial text is the
        # silent-garbage shape); truncated = the child hit its output token
        # limit mid-sentence — treated like paused (same as the summary
        # mapping, truncated → paused, commit 6bc8bbf5a): a cut-off answer
        # must never persist as the conversation's final response. None may
        # be delivered as the response.
        if child_status == "failed":
            error_type = "agent_failed"
        elif child_status == "truncated":
            error_type = "child_truncated"
        else:
            error_type = "agent_suspended"
        if child_status == "failed":
            suggested = "Adjust the inputs and retry."
        elif child_status == "truncated":
            suggested = (
                "The child hit its output token limit mid-answer; the run is "
                "resumable. Retry with a narrower ask or a higher output budget."
            )
        else:
            suggested = "Remove client-delegated tools from the handoff agent's toolset."
        return ToolResult(
            success=False,
            error=ToolError(
                error_type=error_type,
                message=(
                    f"Handoff agent '{tool_def.prompt_id}' did not complete "
                    f"(status={child_status}) — a handoff must deliver a "
                    "complete answer or nothing."
                ),
                is_retryable=child_status in ("failed", "truncated"),
                suggested_action=suggested,
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name=tool_def.name,
            call_id=ctx.call_id,
        )

    final_text = result.output or ""
    if not final_text.strip():
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="agent_empty_response",
                message=(
                    f"Handoff agent '{tool_def.prompt_id}' produced no text — "
                    "nothing to deliver as the response."
                ),
                is_retryable=True,
                suggested_action="Adjust the inputs and call the handoff again.",
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name=tool_def.name,
            call_id=ctx.call_id,
        )

    # Best-effort: keep the handoff answer in the value store too (fetchable
    # later by key; also gives the spine's result_ref a target). Never fatal —
    # the answer is delivered regardless.
    value_ref_key: str | None = None
    try:
        from matrx_ai._ext import get_conversation_value_writer

        writer = get_conversation_value_writer()
        if writer is not None:
            stored = await writer(
                key=f"handoff-{getattr(agent, 'name', None) or tool_def.name}",
                description=(
                    f"Handoff response delivered by "
                    f"{getattr(agent, 'name', None) or tool_def.prompt_id}"
                ),
                value=final_text,
                json_schema=None,
                source_agent_id=None
                if getattr(agent, "source_is_version", False)
                else getattr(agent, "source_id", None),
                source_call_id=ctx.call_id or None,
            )
            if isinstance(stored, dict):
                value_ref_key = stored.get("key")
    except Exception as exc:  # noqa: BLE001 — storage is a bonus, delivery is the job
        logger.warning("handoff value-store write failed (answer still delivered): %s", exc)
        from matrx_connect.streaming.error_capture import capture_error

        await capture_error(
            exc,
            kind="handoff_value_store_failed",
            request_id=ctx.request_id,
            user_id=ctx.user_id,
            conversation_id=ctx.conversation_id,
            route="tool/agent_handoff/value_store",
            error_type=type(exc).__name__,
            payload={"tool_name": tool_def.name, "call_id": ctx.call_id},
        )

    # Version-pinned handoffs: source_id is a VERSION row id — it must ride
    # agent_version_id, never agent_id (that promoted column is an FK to
    # agent.definition; a version UUID passes the shape guard and then fails
    # the FK at the one handoff barrier, killing a delivered turn).
    _source_is_version = bool(getattr(agent, "source_is_version", False))
    outcome = HandoffOutcome(
        final_text=final_text,
        agent_id=None if _source_is_version else getattr(agent, "source_id", None),
        agent_version_id=getattr(agent, "source_id", None)
        if _source_is_version
        else None,
        child_conversation_id=(result.metadata or {}).get("conversation_id"),
        child_execution_id=child_execution_id,
        model_id=result.model_id,
        response_chars=len(final_text),
        value_ref_key=value_ref_key,
    )
    handoff_result = ToolResult(
        success=True,
        # The stub is what the model sees as the tool_result on future turns —
        # deliberately WITHOUT B's text (the very next assistant message IS
        # B's text; duplicating it would double the context cost).
        output={
            "status": "handoff_delivered",
            "response_chars": outcome.response_chars,
            "child_conversation_id": outcome.child_conversation_id,
            "value_ref_key": value_ref_key,
        },
        child_usages=list(result.usage_history),
        started_at=started_at,
        completed_at=time.time(),
        tool_name=tool_def.name,
        call_id=ctx.call_id,
    )
    handoff_result.output_self_capped = True
    handoff_result.handoff_final = True
    handoff_result.handoff = outcome
    if value_ref_key:
        handoff_result.value_ref_key = value_ref_key
    return handoff_result


async def _store_reference_result(
    agent: Any,
    tool_def: ToolDefinition,
    args: dict[str, Any],
    result: Any,
    ctx: ToolContext,
) -> dict[str, Any] | None:
    """Store the child's output via the host's injected value writer and return
    the bounded descriptor dict, or None when no writer is configured. A writer
    failure RAISES (caught by the caller's generic handler) — a dangling
    descriptor must never be returned."""
    from matrx_ai._ext import get_conversation_value_writer

    writer = get_conversation_value_writer()
    if writer is None:
        return None

    # Structured children store as json (schema kept for field-path refs).
    value: Any = result.output
    json_schema = getattr(agent, "output_schema", None)
    if json_schema and isinstance(result.output, str):
        from matrx_ai.agents.output import parse_agent_output

        extraction = parse_agent_output(result.output, agent)
        if extraction.success and isinstance(extraction.data, dict | list):
            value = extraction.data

    description = str(args.get("result_description") or "").strip()
    if not description and isinstance(value, dict):
        description = str(value.get("description") or value.get("summary") or "").strip()[:500]
    if not description:
        description = (
            f"Result of {getattr(agent, 'name', None) or tool_def.name}"
        )

    return await writer(
        key=str(args.get("result_key") or "")
        or (getattr(agent, "name", None) or tool_def.name),
        description=description,
        value=value,
        json_schema=json_schema if isinstance(json_schema, dict) else None,
        source_agent_id=getattr(agent, "source_id", None),
        source_call_id=ctx.call_id or None,
    )


def _merge_projected_variables(
    args: dict[str, Any], tool_def: ToolDefinition
) -> tuple[dict[str, Any], str]:
    """Collect the child agent's variable values + the free-text user input.

    The projected tool schema declares each agent variable as a top-level
    parameter, while older callers pass a nested ``variables`` dict. Rules:
    a DECLARED name is always a variable (even ``query``/``task``/``input`` —
    the author's intent, per the projection contract); undeclared reserved
    names feed user_input; other unknown names pass through as variables
    (harmless — they only substitute where a ``{{name}}`` placeholder exists).
    An explicit nested ``variables`` entry wins over a top-level one.
    """
    declared = _declared_variable_names(tool_def)
    if tool_def.result_mode != "inline":
        # result_key / result_description are dispatch-consumed on
        # reference-returning tools, never agent variables.
        declared -= _REFERENCE_ARG_KEYS
    variables: dict[str, Any] = {}
    for key, value in args.items():
        if value is None or key == "variables":
            continue
        if tool_def.result_mode != "inline" and key in _REFERENCE_ARG_KEYS:
            continue
        if key in _RESERVED_ARG_KEYS and key not in declared:
            continue
        if isinstance(value, str):
            variables[key] = value
        else:
            # Variables are strings everywhere in the agent system; non-string
            # values arrive when a model passes structured content — keep it
            # valid JSON rather than Python repr.
            variables[key] = json.dumps(value, ensure_ascii=False, default=str)
    nested = args.get("variables")
    if isinstance(nested, dict):
        variables.update(nested)

    user_input = next(
        (
            args[k]
            for k in ("input", "user_input", "query", "task")
            if k not in declared and isinstance(args.get(k), str) and args[k]
        ),
        "",
    )
    return variables, user_input


async def execute_agent_tool(
    tool_def: ToolDefinition,
    args: dict[str, Any],
    ctx: ToolContext,
) -> ToolResult:
    """Execute an agent prompt as a tool call.

    Forks the current ExecutionContext for the child agent so it inherits
    user identity, emitter, and project scope automatically.
    """
    started_at = time.time()

    if not tool_def.prompt_id:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="configuration",
                message=f"Agent tool '{tool_def.name}' has no prompt_id configured.",
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name=tool_def.name,
            call_id=ctx.call_id,
        )

    try:
        from matrx_ai.agents.definition import Agent
        from matrx_ai.agents.executor import run_agent
    except ImportError as exc:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="import",
                message=f"Cannot import agent modules: {exc}",
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name=tool_def.name,
            call_id=ctx.call_id,
        )

    try:
        variables, user_input = _merge_projected_variables(args, tool_def)
        agent = await Agent.from_agent(
            tool_def.prompt_id,
            is_version=tool_def.prompt_is_version,
            variables=variables,
        )
        # Carry the nesting depth to the child WITHOUT touching shared state:
        # rebind THIS task's AppContext to a copy whose metadata carries the
        # child depth (each batch tool call runs in its own asyncio task with a
        # copied contextvars scope, so the rebinding is invisible to sibling
        # calls and to the parent loop — an in-place bump on the shared dict
        # raced concurrent siblings into false nesting and leaked depth).
        # run_agent's fork then copies the bumped metadata, so the child loop's
        # ToolContexts carry the true depth for the max_recursion_depth guard.
        # ctx.recursion_depth already IS parent+1 (set by _execute_agent).
        # Reference mode: the child's tokens never reach the client (the
        # descriptor + host event are the caller's signal) and the FULL output
        # never enters the caller's context.
        reference_mode = tool_def.result_mode in ("reference", "inline_once")
        # Handoff mode: the child's tokens ARE the response (they stream on the
        # parent wire) and its lifecycle events are suppressed on success —
        # the user sees one seamless answer.
        handoff_mode = bool(tool_def.handoff_terminal)
        app_ctx = try_get_app_context()
        if app_ctx is not None and isinstance(app_ctx.metadata, dict):
            child_depth = (
                ctx.recursion_depth
                if ctx.recursion_depth > 0
                else read_agent_depth(app_ctx.metadata) + 1
            )
            overrides: dict[str, Any] = {
                "metadata": {**app_ctx.metadata, AGENT_DEPTH_METADATA_KEY: child_depth}
            }
            if reference_mode or handoff_mode:
                # A silenced (reference) child could never announce a
                # client-delegated call; a handoff child must run to completion
                # (its answer IS the response). Either way the child gets NO
                # client tools — its toolset is its own server-side definition.
                overrides["client_tools"] = []
            set_app_context(app_ctx.with_overrides(**overrides))
        # Spine lineage (best-effort, host-injected): record this child agent
        # run as a child execution on the request-management spine. Returns
        # None (untracked) unless the host wired it AND a root execution is
        # live; the settle detaches internally — nothing here blocks the run.
        child_execution_id: str | None = None
        spine_settle = None
        try:
            from matrx_ai._ext import get_child_execution_spawner

            spawner = get_child_execution_spawner()
            if spawner is not None:
                spawned = await spawner(label=tool_def.name, link_id=None)
                if spawned is not None:
                    child_execution_id, spine_settle = spawned
        except Exception:  # noqa: BLE001 — tracking must never affect the run
            child_execution_id, spine_settle = None, None
        try:
            # run_agent is THE ONE execution funnel — it forks the child agent
            # context (lifecycle events, reservation isolation, parent restore)
            # and never raises; failures arrive as result.success=False.
            result = await run_agent(
                agent,
                label=tool_def.name,
                source_feature="agent_tool",
                user_input=user_input,
                suppress_stream=tool_def.result_mode == "reference",
                allow_client_delegation=not (reference_mode or handoff_mode),
                emit_lifecycle=not handoff_mode,
                require_complete_output=handoff_mode or reference_mode,
            )
            if spine_settle is not None:
                try:
                    await spine_settle(
                        success=bool(result.success),
                        usage_history=list(result.usage_history or []),
                    )
                except Exception:  # noqa: BLE001
                    pass
        finally:
            # Restore THIS task's binding — a no-op for siblings (task-local),
            # but keeps the depth from leaking if a future refactor ever runs
            # tool calls sequentially in the loop task.
            if app_ctx is not None:
                set_app_context(app_ctx)
        if not result.success:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="agent_execution",
                    message=f"Agent '{tool_def.prompt_id}' failed: {result.error}",
                    is_retryable=False,
                    suggested_action="Check the agent prompt configuration and input parameters.",
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name=tool_def.name,
                call_id=ctx.call_id,
            )

        native_output = _native_agent_tool_output(result.output)

        if handoff_mode:
            return await _finalize_handoff_result(
                agent, tool_def, result, ctx, started_at,
                child_execution_id=child_execution_id,
            )

        if reference_mode:
            # A child that hard-suspended (client delegation slipped through,
            # or any paused state) has NO final output — success=True with
            # partial text is the silent-garbage shape. A truncated child is
            # treated like paused (matching the summary mapping truncated →
            # paused, commit 6bc8bbf5a): its cut-off output must never be
            # stored as the value. Never mint a descriptor for either; fail
            # the call so the caller can correct.
            child_status = _incomplete_child_status(result)
            empty_output = not (result.output or "").strip()
            if child_status or empty_output:
                truncated = child_status == "truncated"
                failed = child_status == "failed"
                empty = not child_status
                error_type = (
                    "child_truncated"
                    if truncated
                    else "agent_failed"
                    if failed
                    else "agent_empty_response"
                    if empty
                    else "agent_suspended"
                )
                return ToolResult(
                    success=False,
                    error=ToolError(
                        error_type=error_type,
                        message=(
                            f"Agent '{tool_def.prompt_id}' "
                            + (
                                "hit its output token limit mid-run"
                                if truncated
                                else "failed during execution"
                                if failed
                                else "produced no output"
                                if empty
                                else "suspended mid-run"
                            )
                            + f" (status={child_status or 'empty_response'}) — a reference-mode child "
                            "must run to completion; no value was stored."
                        ),
                        is_retryable=truncated or failed or empty,
                        suggested_action=(
                            "The child's run is resumable. Retry with a narrower "
                            "ask or a higher output budget."
                            if truncated
                            else "Adjust the inputs and retry."
                            if failed or empty
                            else "Remove client-delegated tools from the child agent's toolset."
                        ),
                    ),
                    started_at=started_at,
                    completed_at=time.time(),
                    tool_name=tool_def.name,
                    call_id=ctx.call_id,
                )
            stored = await _store_reference_result(agent, tool_def, args, result, ctx)
            if stored is not None:
                output: Any = (
                    stored
                    if tool_def.result_mode == "reference"
                    else {"result": native_output, "stored": stored}
                )
                ref_result = ToolResult(
                    success=True,
                    output=output,
                    child_usages=list(result.usage_history),
                    started_at=started_at,
                    completed_at=time.time(),
                    tool_name=tool_def.name,
                    call_id=ctx.call_id,
                )
                stored_key = stored.get("key") if isinstance(stored, dict) else None
                if isinstance(stored_key, str) and stored_key:
                    ref_result.value_ref_key = stored_key
                if tool_def.result_mode == "reference":
                    # The descriptor is bounded by construction.
                    ref_result.output_self_capped = True
                else:
                    # inline_once: the full inline copy is consumed THIS turn;
                    # the next rebuild stubs it (the stored value remains).
                    ref_result.auto_stub = True
                return ref_result
            # No host store configured — degrade LOUDLY to inline.
            logger.warning(
                "agent tool %s requested result_mode=%s but no conversation_value_writer "
                "is configured — returning the full output inline",
                tool_def.name,
                tool_def.result_mode,
            )

        # An agent registered as a tool is the SECOND agent-as-tool funnel (the
        # first is agent_call). It must carry media the same way: `result.output`
        # is TEXT, and for a media agent that text is now a file_id — handing the
        # calling model a bare UUID with no image block would leave it blind AND
        # unable to resolve anything. The images become real vision blocks; the
        # rest stays as text.
        tool_media = list(getattr(result, "media", None) or [])
        tool_output: Any = native_output
        if tool_media:
            tool_output = {"result": native_output, "media": tool_media}

        return ToolResult(
            success=True,
            output=tool_output,
            provider_content=(
                build_agent_media_content(tool_output, tool_media) if tool_media else None
            ),
            child_usages=list(result.usage_history),
            started_at=started_at,
            completed_at=time.time(),
            tool_name=tool_def.name,
            call_id=ctx.call_id,
        )

    except Exception as exc:
        import traceback as tb

        await _capture_agent_tool_boundary_failure(exc, tool_def=tool_def, ctx=ctx)

        return ToolResult(
            success=False,
            error=ToolError(
                error_type="agent_execution",
                message=f"Agent '{tool_def.prompt_id}' failed: {exc}",
                traceback=tb.format_exc(),
                is_retryable=False,
                suggested_action="Check the agent prompt configuration and input parameters.",
            ),
            started_at=started_at,
            completed_at=time.time(),
            tool_name=tool_def.name,
            call_id=ctx.call_id,
        )


async def register_agent_as_tool(
    prompt_id: str,
    tool_name: str,
    description: str,
    input_schema: dict[str, Any] | None = None,
    max_calls_per_conversation: int = 5,
    cost_cap_per_call: float = 1.0,
    timeout_seconds: float = 300.0,
) -> ToolDefinition:
    default_schema: dict[str, Any] = {
        "input": {
            "type": "string",
            "description": "The input/query to send to the agent",
            "required": True,
        },
    }

    return ToolDefinition(
        name=tool_name,
        description=description,
        parameters=input_schema or default_schema,
        tool_type=ToolType.AGENT,
        function_path=f"agent:{prompt_id}",
        prompt_id=prompt_id,
        max_calls_per_conversation=max_calls_per_conversation,
        cost_cap_per_call=cost_cap_per_call,
        timeout_seconds=timeout_seconds,
        must_complete=True,
        max_recursion_depth=2,
    )
