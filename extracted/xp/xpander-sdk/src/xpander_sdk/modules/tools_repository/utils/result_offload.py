"""Agent-directed tool-result offload for ``xp_execute_tool``.

When the model passes ``save_output_to_file=true`` the executed tool's result is
written PLAINTEXT to ``.tool_calls/{uuid}.xpres`` in the agent workspace and the
model receives a short pointer instead of the full output. Deliberately the
opposite of the context-optimizer L1 offload (encrypted ``CONTEXT_OPTIMIZATION/
*.xp``, readable only via ``xpworkspace-context-retrieve``): these files exist
so the agent can explore them with bash/grep/file-read.
"""

import uuid
from typing import Any

from xpander_sdk.consts.api_routes import APIRoute
from xpander_sdk.core.context_optimizer.helpers.tool_result import (
    unwrap_tool_result_content,
)

TOOL_CALLS_DIR = ".tool_calls"
RESULT_FILE_EXT = ".xpres"
MIN_SAVE_CHARS = 512
PREVIEW_CHARS = 500


def _escape_text(text: str) -> str:
    """Escape element-text-sensitive chars only, keeping quotes copy-paste friendly."""
    return (text or "").replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _escape_attr(text: str) -> str:
    """Attribute-context escaping: quotes too — tool ids are unconstrained
    external strings (MCP function names) and must not break the wrapper tag."""
    return _escape_text(text).replace('"', "&quot;")


def serialize_tool_result(result: Any) -> str:
    """Plaintext form of a tool result — exactly what the LLM would have seen inline."""
    if hasattr(result, "tool_id") and hasattr(result, "is_error"):
        result = getattr(result, "result", None)
    return unwrap_tool_result_content(result)


def append_inline_notice(result: Any, notice: str) -> Any:
    """Append a one-line notice to the result the model will read.

    Every shape gets the notice — the model must always learn the offload did
    not happen. String results (and ToolInvocationResult with a string
    ``result``) get it appended in place; other inner shapes are serialized to
    their inline text form first (same text the LLM would have seen anyway).
    """
    if isinstance(result, str):
        return f"{result}\n\n{notice}"
    if hasattr(result, "tool_id"):
        inner = getattr(result, "result", None)
        if isinstance(inner, str):
            result.result = f"{inner}\n\n{notice}"
        else:
            result.result = f"{unwrap_tool_result_content(inner)}\n\n{notice}"
        return result
    return f"{unwrap_tool_result_content(result)}\n\n{notice}"


async def save_result_to_workspace(
    *, configuration: Any, agent_id: str, content: str
) -> str:
    """Write *content* plaintext to a fresh ``.tool_calls/{uuid}.xpres`` path.

    Awaited (not queued): the pointer promises the file exists, so it must be
    on disk before we return. Raises on failure — caller falls back to inline.
    """
    from xpander_sdk.core.xpander_api_client import APIClient

    path = f"{TOOL_CALLS_DIR}/{uuid.uuid4().hex}{RESULT_FILE_EXT}"
    client = APIClient(configuration=configuration)
    await client.make_request(
        path=str(APIRoute.WorkspaceToolInvoke).format(
            agent_id=agent_id, tool_name="file_write"
        ),
        method="POST",
        payload={"path": path, "content": content},
    )
    return path


def build_saved_result_pointer(*, tool_id: str, path: str, content: str) -> str:
    """The message the LLM gets instead of the full result: path, size, preview,
    and read instructions (plaintext file — bash IS allowed, unlike ``.xp``)."""
    est_tokens = int(len(content) / 4 * 1.2)
    preview = _escape_text(content[:PREVIEW_CHARS])
    return (
        f'<tool_result_saved tool="{_escape_attr(tool_id)}" path="{_escape_attr(path)}" '
        f'chars="{len(content):,}" est_tokens="{est_tokens:,}">\n'
        f"Preview (first {min(PREVIEW_CHARS, len(content))} chars):\n"
        f"{preview}\n"
        f"</tool_result_saved>\n"
        f"Full result saved as PLAINTEXT to {path} in your workspace "
        f"(you set save_output_to_file=true).\n"
        f"Read it with xpworkspace-grep (search), xpworkspace-file-read (paged read), "
        f"or xpworkspace-bash (jq/head/wc/awk on the path). "
        f"Do NOT use xpworkspace-context-retrieve — this file is not encrypted context. "
        f"Note: the file may be cleaned up after a few days."
    )
