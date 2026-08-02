"""Workspace-path payload resolver.

When an LLM sets `workspace_path` on a tool call, this module reads the file
from the agent's workspace pod (via the existing `xpworkspace-file-read` tool),
parses it (JSON by default), and returns the resolved dict so it can be used
as the actual tool payload. Activity logging records the resolved payload, not
the path.

Resolution happens **before** the agno activity-log hook in
`modules/backend/frameworks/agno.py::on_tool_call_hook`, so both the recorded
event and the dispatched tool call see the resolved arguments.
"""

import json
from typing import Any, Dict, Literal, Optional

from loguru import logger

from xpander_sdk.exceptions.module_exception import ModuleException
from xpander_sdk.models.configuration import Configuration
from xpander_sdk.modules.backend.utils.tool_call_events import coerce_json_like

WORKSPACE_PATH_KEY = "workspace_path"
WORKSPACE_FILE_READ_TOOL_ID = "xpworkspace-file-read"
DEFAULT_MAX_BYTES = 1_048_576  # 1 MB


class WorkspacePayloadError(ModuleException):
    """Base error for workspace_path resolution failures."""


class WorkspacePayloadTooLarge(WorkspacePayloadError):
    def __init__(self, path: str, size: int, limit: int):
        super().__init__(
            status_code=413,
            description=(
                f"workspace_path file '{path}' is {size} bytes; exceeds the "
                f"{limit} byte limit. Reduce the payload or split the call."
            ),
        )


class WorkspacePayloadInvalidJson(WorkspacePayloadError):
    def __init__(self, path: str, parse_error: str):
        super().__init__(
            status_code=400,
            description=(
                f"workspace_path file '{path}' is not valid JSON: {parse_error}. "
                f"Write the payload as a single JSON object using xpworkspace-file-write."
            ),
        )


class WorkspacePayloadInvalidShape(WorkspacePayloadError):
    def __init__(self, path: str):
        super().__init__(
            status_code=400,
            description=(
                f"workspace_path file '{path}' parsed to a non-object value; "
                f"the payload must be a JSON object."
            ),
        )


class WorkspacePayloadReadFailed(WorkspacePayloadError):
    def __init__(self, path: str, cause: str):
        super().__init__(
            status_code=502,
            description=(
                f"Failed to read workspace_path file '{path}' from agent workspace: {cause}"
            ),
        )


def _payload_view(arguments: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    """Return the inner payload dict if `arguments` has the agno envelope.

    agno wraps tool args as `{"payload": <dict>}` because the generated tool
    function signature is `tool_function(payload: <Schema>)`. The LLM's keys
    (workspace_path, body_params, …) live one level deeper. Earlier code only
    checked the top level and missed every offload attempt.

    Some model bindings additionally stringify the envelope, so `payload` may
    arrive as a JSON string (e.g. ``'{"workspace_path": "..."}'``). Best-effort
    parse it back into a dict via :func:`coerce_json_like`; on parse failure we
    fall through to today's behaviour (return ``arguments`` as-is and let
    downstream validation handle it).

    Returns the inner dict if the envelope is present; otherwise returns
    `arguments` itself so callers handle both shapes uniformly.
    """
    if isinstance(arguments, dict):
        inner = arguments.get("payload")
        if isinstance(inner, str):
            coerced = coerce_json_like(inner)
            if isinstance(coerced, dict):
                arguments["payload"] = coerced
                inner = coerced
        if isinstance(inner, dict):
            return inner
    return arguments if isinstance(arguments, dict) else None


def has_workspace_path(arguments: Optional[Dict[str, Any]]) -> bool:
    payload = _payload_view(arguments)
    return (
        isinstance(payload, dict)
        and isinstance(payload.get(WORKSPACE_PATH_KEY), str)
        and payload[WORKSPACE_PATH_KEY].strip() != ""
    )


def strip_workspace_path(arguments: Optional[Dict[str, Any]]) -> None:
    """Remove `workspace_path` in place, looking inside the agno envelope first.

    If the envelope arrived stringified (``payload='{"workspace_path": ...}'``),
    :func:`_payload_view` already coerced it back to a dict in-place, so the
    pop below sees the structured form.
    """
    if not isinstance(arguments, dict):
        return
    # Force coercion of any stringified envelope so the strip below operates
    # on the parsed dict rather than silently no-op'ing on the raw string.
    _payload_view(arguments)
    inner = arguments.get("payload")
    if isinstance(inner, dict) and WORKSPACE_PATH_KEY in inner:
        inner.pop(WORKSPACE_PATH_KEY, None)
        return
    arguments.pop(WORKSPACE_PATH_KEY, None)


def _build_file_read_tool(configuration: Optional[Configuration]):
    from xpander_sdk.modules.tools_repository.sub_modules.tool import Tool

    return Tool(
        configuration=configuration,
        id=WORKSPACE_FILE_READ_TOOL_ID,
        name=WORKSPACE_FILE_READ_TOOL_ID,
        method="POST",
        path=f"/operation/workspace/file_read",
        is_local=False,
    )


async def _read_workspace_file(
    *,
    agent_id: str,
    configuration: Optional[Configuration],
    task_id: Optional[str],
    path: str,
) -> str:
    file_read_tool = _build_file_read_tool(configuration=configuration)
    try:
        response = await file_read_tool.acall_remote_tool(
            agent_id=agent_id,
            payload={
                "body_params": {"path": path},
                "query_params": {},
                "path_params": {},
            },
            configuration=configuration,
            task_id=task_id,
        )
    except Exception as exc:
        raise WorkspacePayloadReadFailed(path=path, cause=str(exc)) from exc

    if not isinstance(response, dict):
        raise WorkspacePayloadReadFailed(
            path=path,
            cause=f"unexpected file_read response shape: {type(response).__name__}",
        )

    content = response.get("content")
    if content is None:
        raise WorkspacePayloadReadFailed(
            path=path,
            cause="file_read returned no 'content' field",
        )
    if not isinstance(content, str):
        raise WorkspacePayloadReadFailed(
            path=path,
            cause=f"file_read 'content' is not a string ({type(content).__name__})",
        )
    return content


async def resolve_workspace_payload(
    *,
    agent_id: str,
    configuration: Optional[Configuration],
    task_id: Optional[str],
    arguments: Dict[str, Any],
    max_bytes: int = DEFAULT_MAX_BYTES,
    payload_format: Literal["json", "raw"] = "json",
    raw_target_arg: Optional[str] = None,
) -> Dict[str, Any]:
    """Resolve `workspace_path` to the actual payload dict.

    No-op when `workspace_path` is absent or empty. When set, reads the file
    from the agent's workspace, enforces the byte cap, parses it (JSON by
    default) and returns arguments with the resolved dict swapped in — to be
    used as the *whole* tool payload. Inline args at the same level are
    discarded ("path wins").

    Envelope handling: agno passes tool kwargs as `{"payload": <dict>}`. When
    the envelope is present, the inner payload dict is replaced with the
    resolved data; the outer `payload` key is preserved so agno's argument
    binding stays correct. When the envelope is absent (callers passing
    arguments directly), the resolved dict is returned as-is.
    """
    if not has_workspace_path(arguments):
        return arguments

    has_envelope = (
        isinstance(arguments, dict)
        and isinstance(arguments.get("payload"), dict)
        and WORKSPACE_PATH_KEY in arguments["payload"]
    )
    inner = arguments["payload"] if has_envelope else arguments

    path = inner[WORKSPACE_PATH_KEY]
    content = await _read_workspace_file(
        agent_id=agent_id,
        configuration=configuration,
        task_id=task_id,
        path=path,
    )

    size = len(content.encode("utf-8"))
    if size > max_bytes:
        raise WorkspacePayloadTooLarge(path=path, size=size, limit=max_bytes)

    if payload_format == "raw":
        if not raw_target_arg:
            raise WorkspacePayloadReadFailed(
                path=path,
                cause="raw payload_format requires raw_target_arg to be configured",
            )
        resolved: Dict[str, Any] = {raw_target_arg: content}
    else:
        try:
            parsed = json.loads(content)
        except json.JSONDecodeError as exc:
            raise WorkspacePayloadInvalidJson(path=path, parse_error=str(exc)) from exc
        if not isinstance(parsed, dict):
            raise WorkspacePayloadInvalidShape(path=path)
        resolved = parsed

    logger.info(
        f"[workspace_payload] resolved workspace_path='{path}' ({size}B) for agent_id={agent_id}"
    )

    if has_envelope:
        # Preserve agno's {"payload": ...} kwargs envelope so function_call(**arguments)
        # still binds correctly; only swap the inner dict.
        return {**arguments, "payload": resolved}
    return resolved
