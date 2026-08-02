"""
Tool call activity reporting utility.

Shared helper used by both the agno framework hook and direct SDK tool
invocations (e.g. OpenClaw) to emit ToolCallRequest / ToolCallResult
events to the task activity queue.

All pushes are fire-and-forget: failures are logged as warnings and
never raise. There is NO skip/filter logic here — every caller decides
whether to report and this module simply does the reporting.
"""

from __future__ import annotations

import ast
import asyncio
import json
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Optional, TYPE_CHECKING

from loguru import logger

from xpander_sdk.consts.api_routes import APIRoute
from xpander_sdk.core.xpander_api_client import APIClient
from xpander_sdk.models.events import (
    TaskUpdateEventType,
    ToolCallRequest,
    ToolCallRequestReasoning,
    ToolCallResult,
)

if TYPE_CHECKING:
    from xpander_sdk.modules.tasks.sub_modules.task import Task


# Sizing mirrors Layer 1 microcompaction, but this clamp is DISPLAY-ONLY: the
# model may well have received the full result (L1 skips most xp* tools).
DEFAULT_MAX_CONTENT_LENGTH = 8_000
DEFAULT_PREVIEW_LENGTH = 2_000

# "display truncation only" is load-bearing: without it this marker reads like the L1 marker and log readers conclude the MODEL was blinded.
TRUNCATION_MARKER_TEMPLATE = (
    "\n\n[TRUNCATED OUTPUT - {total:,} chars (~{tokens:,} tokens) total, "
    "showing first {preview:,} chars - display truncation only, the model "
    "received the full content]"
)

TOOL_CALL_REASONING_TITLE = "toolcallreasoningtitle"
TOOL_CALL_REASONING_DESCRIPTION = "toolcallreasoningdescription"
TOOL_CALL_PLAN_TASK_ID = "toolcallplantaskid"

# Deep-planning tool ids. These manage plan lifecycle (create/get/update/
# complete/ask/start) and are considered internal orchestration — they
# should NOT produce tool-call activity entries.
PLANNING_TOOLS = frozenset(
    [
        "xpcreate_agent_plan",
        "xpget_agent_plan",
        "xpadd_new_agent_plan_item",
        "xpupdate_agent_plan_item",
        "xpdelete_agent_plan_item",
        "xpcomplete_agent_plan_items",
        "xpask_for_information",
        "xpstart_execution_plan",
    ]
)

# Agno reasoning tool names. These are handled as a separate reasoning
# activity entry (via Think / Analyze event types), NOT as regular tool
# calls. The activity consumer renders them as AgentActivityThreadReasoning.
THINK_TOOL = "think"
ANALYZE_TOOL = "analyze"
REASONING_TOOLS = frozenset([THINK_TOOL, ANALYZE_TOOL])

# Agno team-orchestration tool names. When an xpander agent runs as an agno
# team, agno emits these internal tool calls to route work to members. They
# are framework plumbing, not real agent actions, so they are fully hidden
# from the activity log (no ToolCallRequest / ToolCallResult). See PRO-1383.
AGNO_INTERNAL_TEAM_TOOLS = frozenset(
    [
        "delegate_task_to_member",
        "delegate_task_to_members",
        "execute_task",
        "execute_tasks_parallel",
        "get_member_information",
    ]
)

# Dynamic-tools meta-tools. These are SDK plumbing for progressive tool
# disclosure (discover/inspect/run hidden tools). Their own calls are hidden
# from the activity log — only the REAL tool dispatched through xp_execute_tool
# is reported (xp_execute_tool calls ainvoke with report_activity=True). See
# modules/tools_repository/sub_modules/dynamic_tools.py.
DYNAMIC_META_TOOLS = frozenset(
    [
        "xp_list_tools",
        "xp_search_tools",
        "xp_get_tool",
        "xp_execute_tool",
    ]
)


# Tool-call summary pre-warm. When a task is dispatched by the agent gateway
# (carries the ``x-is-from-agent-gateway`` header in payload_extension), the SDK
# fires the TOOL_CALL_ANALYSIS summarizer in the background right after a tool
# result is produced. This pre-warms the Redis cache the chat web-app reads when
# a user expands a tool call, turning that lazy fetch into an instant cache hit.
# Module constant (not an env var) per repo convention.
TOOL_CALL_SUMMARY_PREWARM_ENABLED = True
# Mirrors SummarizerPreset.TOOL_CALL_ANALYSIS in the agent-controller summarizer.
TOOL_CALL_SUMMARY_PRESET = "tool_call_analysis"


def is_agent_gateway_task(task: Optional["Task"]) -> bool:
    """Return True when the task was dispatched by the agent gateway.

    The gateway tags child executions with
    ``payload_extension={"headers": {"x-is-from-agent-gateway": "true"}}``.
    """
    pe = getattr(task, "payload_extension", None)
    if not isinstance(pe, dict):
        return False
    headers = pe.get("headers")
    if not isinstance(headers, dict):
        return False
    return str(headers.get("x-is-from-agent-gateway", "")).strip().lower() == "true"


def _unwrap_payload_envelope(request: Any) -> Any:
    """Strip the ``payload`` envelope the SDK wraps tool args in.

    Tool args are dispatched as ``{"payload": {body_params, headers, ...}}``.
    The chat web-app renders/summarizes the inner data (``unwrapToolPayload``),
    so the pre-warm must do the same for the cache key to line up. Falls back to
    the value unchanged when there is no envelope.
    """
    if isinstance(request, dict) and "payload" in request:
        return request["payload"]
    return request


def _normalize_for_cache_parity(value: Any) -> Any:
    """Mirror the lossy JSON round-trip the UI value goes through.

    The web-app reads the activity-log request/result, which has passed through
    a JavaScript ``JSON.parse``/``stringify`` cycle. JS has no int/float split,
    so integral floats collapse to ints (``0.0`` -> ``0``). Python keeps
    ``0.0``, which serializes to ``"0.0"`` and breaks the org+preset+payload
    cache key. Recursively coerce integral floats to ints so the SDK pre-warm
    hashes identically to the UI's later request.
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, float):
        return int(value) if value.is_integer() else value
    if isinstance(value, dict):
        return {k: _normalize_for_cache_parity(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [_normalize_for_cache_parity(v) for v in value]
    return value


async def _prewarm_tool_call_summary(
    task: "Task", tool_name: str, request: Any, response: Any
) -> None:
    """Fire the TOOL_CALL_ANALYSIS summarizer to pre-warm the cache the chat
    web-app reads on tool-call expand.

    Calls the summarizer endpoint directly (``/summarizer/run``) with the same
    preset + payload shape the chat-backend wrapper uses, so the org+preset+
    payload-keyed Redis entry matches the UI's later request. The request is
    unwrapped from its ``payload`` envelope and both request/result are number-
    normalized to match the UI's JS-round-tripped values. Fire-and-forget:
    failures are logged at debug and never raised.
    """
    try:
        client = APIClient(configuration=task.configuration)
        await client.make_request(
            path=APIRoute.RunSummarizer,
            method="POST",
            payload={
                "preset": TOOL_CALL_SUMMARY_PRESET,
                "payload": {
                    "tool_name": tool_name,
                    "request": _normalize_for_cache_parity(
                        _unwrap_payload_envelope(request)
                    ),
                    "response": _normalize_for_cache_parity(response),
                },
                "use_cache": True,
            },
        )
    except Exception as exc:
        logger.debug(
            f"[tool-call-events] tool-call summary pre-warm skipped for task "
            f"{getattr(task, 'id', '?')}: {exc}"
        )


async def get_tool_call_summary(
    task: "Task", tool_name: str, request: Any, response: Any
) -> Optional[str]:
    """Run the TOOL_CALL_ANALYSIS summarizer and return its one-line summary text.

    Same payload shape as ``_prewarm_tool_call_summary`` (so it shares the same
    org+preset+payload cache entry), but returns the formatted summary instead of
    discarding it — used to append a ready summary to an offloaded result's
    preview. Returns ``None`` on any failure or an unexpected response shape.
    """
    try:
        client = APIClient(configuration=task.configuration)
        resp = await client.make_request(
            path=APIRoute.RunSummarizer,
            method="POST",
            payload={
                "preset": TOOL_CALL_SUMMARY_PRESET,
                "payload": {
                    "tool_name": tool_name,
                    "request": _normalize_for_cache_parity(
                        _unwrap_payload_envelope(request)
                    ),
                    "response": _normalize_for_cache_parity(response),
                },
                "use_cache": True,
            },
        )
        result = resp.get("result") if isinstance(resp, dict) else None
        if not isinstance(result, dict):
            return None
        req_s = str(result.get("request_summary") or "").strip()
        resp_s = str(result.get("response_summary") or "").strip()
        if not resp_s:
            return None
        return f"{req_s} {resp_s}".strip() if req_s else resp_s
    except Exception as exc:
        logger.debug(
            f"[tool-call-events] tool-call summary fetch failed for task "
            f"{getattr(task, 'id', '?')}: {exc}"
        )
        return None


def should_skip_tool_report(tool_name: Optional[str]) -> bool:
    """Return True when the tool's activity should NOT be reported as a
    regular tool call.

    This covers the deep-planning tools (fully hidden from activity), the
    reasoning tools (reported via the separate Think / Analyze helper below),
    and agno's internal team-orchestration tools (framework plumbing, fully
    hidden). Callers should short-circuit tool-call emission when this
    returns True.
    """
    if not tool_name:
        return False
    return (
        tool_name in PLANNING_TOOLS
        or tool_name in REASONING_TOOLS
        or tool_name in AGNO_INTERNAL_TEAM_TOOLS
        or tool_name in DYNAMIC_META_TOOLS
    )


def is_reasoning_tool(tool_name: Optional[str]) -> bool:
    """Return True when the tool is agno's think/analyze reasoning tool."""
    if not tool_name:
        return False
    return tool_name in REASONING_TOOLS


async def report_reasoning_event(
    task: "Task",
    tool_name: str,
    arguments: Optional[Dict[str, Any]],
    request_id: Optional[str] = None,
    plan_task_id: Optional[str] = None,
) -> None:
    """Push a Think / Analyze activity event for the given reasoning tool.

    The mono activity consumer builds an ``AgentActivityThreadReasoning``
    entry from this event by spreading ``tool_call.payload["input"]`` into
    the reasoning model (which expects ``title``, ``confidence``, and
    optionally ``thought`` / ``action`` / ``result`` / ``analysis``).
    This helper therefore wraps the caller's ``arguments`` dict in
    ``{"input": arguments}`` to match that contract.

    Fire-and-forget: failures are logged but never raised.
    """
    try:
        tool_name = (tool_name or "").lower()
        if tool_name not in REASONING_TOOLS:
            return
        event_type = (
            TaskUpdateEventType.Think
            if tool_name == THINK_TOOL
            else TaskUpdateEventType.Analyze
        )
        # Normalize the reasoning payload to the shape mono's activity
        # consumer expects: payload["input"] carries title/confidence/etc.
        input_dict: Dict[str, Any] = {}
        coerced_arguments = (
            coerce_json_like(arguments) if arguments is not None else None
        )
        if isinstance(coerced_arguments, dict):
            # Agno passes reasoning fields as top-level keyword arguments.
            # Tolerate both shapes: direct fields, or an already-wrapped
            # {"input": {...}} form.
            if isinstance(coerced_arguments.get("input"), dict):
                input_dict = dict(coerced_arguments["input"])
            else:
                input_dict = {
                    k: v
                    for k, v in coerced_arguments.items()
                    if k not in ("headers", TOOL_CALL_PLAN_TASK_ID)
                }
        data = ToolCallRequest(
            request_id=request_id or str(uuid.uuid4()),
            operation_id=tool_name,
            tool_name=tool_name,
            payload={"input": input_dict},
            plan_task_id=plan_task_id,
        )
        await _push_event(task=task, event_type=event_type, data=data)
    except Exception as exc:
        logger.warning(f"[tool-call-events] failed to build reasoning event: {exc}")


def _to_string(value: Any) -> str:
    """Best-effort conversion of an arbitrary result to a string for truncation sizing."""
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    try:
        return json.dumps(value, default=str, ensure_ascii=False)
    except Exception:
        try:
            return str(value)
        except Exception:
            return ""


def coerce_json_like(value: Any) -> Any:
    """If *value* is a string that looks like JSON or a Python literal
    describing a dict/list, parse it into the structured form so the
    activity log carries proper JSON instead of an embedded string blob.

    Recurses into dicts and lists so nested fields (e.g. ``result``,
    ``content``, ``output``) are also normalized. Non-string primitives
    are returned as-is. Parse failures fall back to the original value.
    """
    # Primitives / None pass through.
    if value is None or isinstance(value, (int, float, bool)):
        return value

    if isinstance(value, str):
        stripped = value.strip()
        # Only attempt parsing for strings that plausibly represent a
        # structured value. Skip obvious plain text to avoid false
        # positives (json.loads accepts lone numbers/booleans too).
        if stripped.startswith(("{", "[")) and stripped.endswith(("}", "]")):
            # Try JSON first (strict, fast).
            try:
                parsed = json.loads(stripped)
                if isinstance(parsed, (dict, list)):
                    return coerce_json_like(parsed)
            except Exception:
                pass
            # Lenient retry: payloads with literal newlines/tabs in string
            # values (e.g. a file-write ``content`` field) break strict
            # json.loads with an "Invalid control character" error. strict=False
            # accepts them, recovering the dict instead of leaking the raw str
            # to pydantic / the wcache fast-path.
            try:
                parsed = json.loads(stripped, strict=False)
                if isinstance(parsed, (dict, list)):
                    return coerce_json_like(parsed)
            except Exception:
                pass
            # Fallback: Python literal (single quotes, tuples, etc.).
            try:
                parsed = ast.literal_eval(stripped)
                if isinstance(parsed, (dict, list, tuple)):
                    if isinstance(parsed, tuple):
                        parsed = list(parsed)
                    return coerce_json_like(parsed)
            except Exception:
                pass
        return value

    if isinstance(value, dict):
        return {k: coerce_json_like(v) for k, v in value.items()}

    if isinstance(value, (list, tuple)):
        return [coerce_json_like(v) for v in value]

    # Unknown types (pydantic models, custom objects, etc.) — leave
    # them alone; the downstream Pydantic model_dump_safe handles them.
    return value


def shape_result_for_activity(
    result: Any,
    max_content_length: int = DEFAULT_MAX_CONTENT_LENGTH,
    preview_length: int = DEFAULT_PREVIEW_LENGTH,
    skip_truncation: bool = False,
) -> Any:
    """Return *result* as-is unless it is too large, in which case return a
    preview + truncation marker mirroring Layer 1 microcompaction.

    When ``skip_truncation`` is True the result is returned verbatim
    regardless of size. Use this for cases where the agent explicitly
    asked for the full content (e.g. reading back an offloaded
    CONTEXT_OPTIMIZATION file from the workspace).

    Non-string results that exceed the threshold are serialized to JSON for
    the preview. Small results are returned verbatim so typed values
    (dicts/lists) continue to render correctly downstream.
    """
    if skip_truncation:
        return result
    try:
        as_str = _to_string(result)
        if len(as_str) <= max_content_length:
            return result
        preview = as_str[:preview_length]
        marker = TRUNCATION_MARKER_TEMPLATE.format(
            total=len(as_str),
            tokens=int(len(as_str) / 4 * 1.2),
            preview=preview_length,
        )
        return preview + marker
    except Exception:
        # Never fail the caller because of shaping logic.
        return result


def extract_reasoning(
    arguments: Optional[Dict[str, Any]],
) -> Optional[ToolCallRequestReasoning]:
    """Extract reasoning metadata from a tool-call payload.

    Looks for ``toolcallreasoningtitle`` / ``toolcallreasoningdescription``
    in the common shapes:
      * ``arguments["headers"]``
      * ``arguments["payload"]["headers"]``
      * ``arguments["payload"]["body_params"]["headers"]``
      * top-level ``arguments``
    Returns ``None`` when no reasoning keys are present.
    """
    if not arguments or not isinstance(arguments, dict):
        return None

    candidates = []
    candidates.append(arguments)
    headers = arguments.get("headers")
    if isinstance(headers, dict):
        candidates.append(headers)
    payload = arguments.get("payload")
    if isinstance(payload, dict):
        candidates.append(payload)
        if isinstance(payload.get("headers"), dict):
            candidates.append(payload["headers"])
        body_params = payload.get("body_params")
        if isinstance(body_params, dict):
            candidates.append(body_params)
            if isinstance(body_params.get("headers"), dict):
                candidates.append(body_params["headers"])

    for source in candidates:
        title = source.get(TOOL_CALL_REASONING_TITLE)
        description = source.get(TOOL_CALL_REASONING_DESCRIPTION)
        if title or description:
            return ToolCallRequestReasoning(
                title=title,
                description=description,
            )

    return None


# Sentinel distinguishing an absent ``toolcallplantaskid`` header from one that
# is explicitly present but empty ("" = the LLM opting out of a plan step).
_PLAN_TASK_ID_MISSING = object()


def _plan_task_id_candidate_sources(arguments: Dict[str, Any]) -> list:
    """The payload shapes that may carry the plan-step header (same shapes as
    :func:`extract_reasoning`)."""
    candidates: list = [arguments]
    headers = arguments.get("headers")
    if isinstance(headers, dict):
        candidates.append(headers)
    payload = arguments.get("payload")
    if isinstance(payload, dict):
        candidates.append(payload)
        if isinstance(payload.get("headers"), dict):
            candidates.append(payload["headers"])
        body_params = payload.get("body_params")
        if isinstance(body_params, dict):
            candidates.append(body_params)
            if isinstance(body_params.get("headers"), dict):
                candidates.append(body_params["headers"])
    return candidates


def _raw_plan_task_id(arguments: Optional[Dict[str, Any]]) -> Any:
    """Return the raw header value if the key is present in any candidate shape,
    else :data:`_PLAN_TASK_ID_MISSING`.

    This preserves the distinction between an explicit empty string (the LLM
    saying "no step") and a header that was never supplied.
    """
    if not arguments or not isinstance(arguments, dict):
        return _PLAN_TASK_ID_MISSING
    for source in _plan_task_id_candidate_sources(arguments):
        if isinstance(source, dict) and TOOL_CALL_PLAN_TASK_ID in source:
            return source[TOOL_CALL_PLAN_TASK_ID]
    return _PLAN_TASK_ID_MISSING


def extract_plan_task_id(
    arguments: Optional[Dict[str, Any]],
) -> Optional[str]:
    """Extract the LLM-assigned ``toolcallplantaskid`` from a tool-call payload.

    Returns the trimmed value, or ``None`` when the header is absent or empty
    (an empty string means "no step").
    """
    raw = _raw_plan_task_id(arguments)
    if raw is _PLAN_TASK_ID_MISSING:
        return None
    return raw if (isinstance(raw, str) and raw.strip()) else None


def _active_plan_task_id(task: Optional["Task"]) -> Optional[str]:
    """Return the id of the first not-yet-completed plan step, if any.

    Only meaningful once the plan has been started (``xpstart_execution_plan``);
    before that there is no step to attribute work to.
    """
    try:
        deep_planning = getattr(task, "deep_planning", None)
        if (
            not deep_planning
            or not getattr(deep_planning, "enabled", False)
            or not getattr(deep_planning, "started", False)
        ):
            return None
        for item in deep_planning.tasks or []:
            if not getattr(item, "completed", False):
                return item.id
    except Exception:
        pass
    return None


# Last trusted plan-step header per task. Under batched completions steps stay
# completed=False until a boundary, so first-incomplete is a poor guess for a
# header-less call mid-phase — the last real header is the better attribution.
_LAST_TRUSTED_PLAN_TASK_ID: Dict[str, str] = {}
_LAST_TRUSTED_PLAN_TASK_ID_CAP = 512


def _remember_trusted_plan_task_id(task: Optional["Task"], step_id: str) -> None:
    """Record the last plan-step header that named a real step for this task."""
    task_id = getattr(task, "id", None)
    if not task_id:
        return
    if (
        task_id not in _LAST_TRUSTED_PLAN_TASK_ID
        and len(_LAST_TRUSTED_PLAN_TASK_ID) >= _LAST_TRUSTED_PLAN_TASK_ID_CAP
    ):
        _LAST_TRUSTED_PLAN_TASK_ID.pop(next(iter(_LAST_TRUSTED_PLAN_TASK_ID)))
    _LAST_TRUSTED_PLAN_TASK_ID[task_id] = step_id


def resolve_plan_task_id(
    arguments: Optional[Dict[str, Any]],
    task: Optional["Task"],
) -> Optional[str]:
    """Resolve the plan step id for a tool call from header, last trusted, or active step.

    A header that references a real plan step is trusted even if that step is
    already completed (a call can legitimately belong to a step just finished).
    A missing/empty header or an id absent from the plan falls back to the last
    trusted header seen in this task, then to the first-incomplete step. With no
    started plan we keep the raw header.
    """
    deep_planning = getattr(task, "deep_planning", None)
    if (
        not deep_planning
        or not getattr(deep_planning, "enabled", False)
        or not getattr(deep_planning, "started", False)
        or not (deep_planning.tasks or [])
    ):
        return extract_plan_task_id(arguments)
    plan_ids = {item.id for item in deep_planning.tasks}
    candidate = extract_plan_task_id(arguments)
    if candidate and candidate in plan_ids:
        _remember_trusted_plan_task_id(task, candidate)
        return candidate
    last_trusted = _LAST_TRUSTED_PLAN_TASK_ID.get(getattr(task, "id", None) or "")
    if last_trusted and last_trusted in plan_ids:
        return last_trusted
    return _active_plan_task_id(task)


async def _push_event(task: "Task", event_type: TaskUpdateEventType, data: Any) -> None:
    """POST a task-update event to the activity queue. Fire-and-forget."""
    if not task or not getattr(task, "id", None):
        return
    try:
        from xpander_sdk.modules.tasks.sub_modules.task import TaskUpdateEvent

        evt = TaskUpdateEvent(
            task_id=task.id,
            organization_id=task.organization_id,
            time=datetime.now(timezone.utc).isoformat(),
            type=event_type,
            data=data,
        )
        client = APIClient(configuration=task.configuration)
        await client.make_request(
            path=APIRoute.PushExecutionEventToQueue.format(task_id=task.id),
            method="POST",
            payload=[evt.model_dump_safe()],
        )
    except Exception as exc:
        logger.warning(
            f"[tool-call-events] failed to push {event_type} for task "
            f"{getattr(task, 'id', '?')}: {exc}"
        )


async def report_tool_call_request(
    task: "Task",
    request_id: str,
    operation_id: str,
    tool_name: Optional[str] = None,
    payload: Any = None,
    reasoning: Optional[ToolCallRequestReasoning] = None,
    graph_node_id: Optional[str] = None,
    tool_call_id: Optional[str] = None,
    plan_task_id: Optional[str] = None,
) -> None:
    """Push a ``ToolCallRequest`` event for the given task. Fire-and-forget.

    String payloads that look like JSON/Python-literal dicts or lists are
    coerced into structured form so the activity log carries proper JSON
    rather than an embedded blob.
    """
    try:
        data = ToolCallRequest(
            request_id=request_id,
            operation_id=operation_id,
            tool_call_id=tool_call_id,
            graph_node_id=graph_node_id,
            tool_name=tool_name or operation_id,
            payload=coerce_json_like(payload),
            reasoning=reasoning,
            plan_task_id=plan_task_id,
        )
        await _push_event(
            task=task, event_type=TaskUpdateEventType.ToolCallRequest, data=data
        )
    except Exception as exc:
        logger.warning(f"[tool-call-events] failed to build ToolCallRequest: {exc}")


async def report_tool_call_result(
    task: "Task",
    request_id: str,
    operation_id: str,
    result: Any,
    is_error: bool = False,
    tool_name: Optional[str] = None,
    payload: Any = None,
    graph_node_id: Optional[str] = None,
    tool_call_id: Optional[str] = None,
    max_content_length: int = DEFAULT_MAX_CONTENT_LENGTH,
    preview_length: int = DEFAULT_PREVIEW_LENGTH,
    skip_truncation: bool = False,
    plan_task_id: Optional[str] = None,
) -> None:
    """Push a ``ToolCallResult`` event for the given task. Fire-and-forget.

    The result payload is shaped via ``shape_result_for_activity`` - a
    display-only clamp; the model may have received the full content.

    Pass ``skip_truncation=True`` when the activity log must carry the
    full content verbatim (e.g. reading back an offloaded
    CONTEXT_OPTIMIZATION file from the workspace).
    """
    try:
        # Coerce first so truncation operates on the already-structured value
        # (improves the JSON-stringified length check + preview quality).
        normalized_result = coerce_json_like(result)
        shaped = shape_result_for_activity(
            result=normalized_result,
            max_content_length=max_content_length,
            preview_length=preview_length,
            skip_truncation=skip_truncation,
        )
        data = ToolCallResult(
            request_id=request_id,
            operation_id=operation_id,
            tool_call_id=tool_call_id,
            graph_node_id=graph_node_id,
            tool_name=tool_name or operation_id,
            payload=coerce_json_like(payload),
            result=shaped,
            is_error=is_error,
            plan_task_id=plan_task_id,
        )
        await _push_event(
            task=task, event_type=TaskUpdateEventType.ToolCallResult, data=data
        )
        # Pre-warm the tool-call summary for gateway-originated tasks. Uses the
        # same coerced request payload + shaped result just logged, so the
        # summarizer cache key matches the chat web-app's later expand request.
        if (
            TOOL_CALL_SUMMARY_PREWARM_ENABLED
            and not should_skip_tool_report(tool_name or operation_id)
            and is_agent_gateway_task(task)
        ):
            asyncio.create_task(
                _prewarm_tool_call_summary(
                    task=task,
                    tool_name=tool_name or operation_id,
                    request=data.payload,
                    response=shaped,
                )
            )
    except Exception as exc:
        logger.warning(f"[tool-call-events] failed to build ToolCallResult: {exc}")
