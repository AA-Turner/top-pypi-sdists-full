"""PINNED_TOOLS: the tools whose full result always rides the stream (lazy tool calls).

Every other tool is a "fold" tool: its `tool_completed` frame carries the result only
when it is small (<= RESULT_INLINE_MAX_BYTES), otherwise a preview + `output_chars` +
`tool_call_id` and `result_omitted: true`, and the client reads the full result from
`chat.tool_call.output` by id on click. Design: common-docs/projects/chat-package-move/
LAZY-TOOL-CALLS.md section 3.4 / 3.5.

A tool is pinned when its payload IS the interface, not process detail:
  - ask cards / forms the person must answer (ask_person, ask_user, interaction_ask, ask)
  - a review the person must act on (google_email_send)
  - hand-off to the person (request_user_takeover, credential capture)
  - plans awaiting approval (update_plan, plan_approval)
  - image / media generation (the picture is the answer; image generation rides `agent`,
    and the retiring `agent_call` whose stored cards still render)
Also pinned per call, not per name: a write HELD for approval (awaiting_approval) and a
surface-write (the diff is the result).

Keep in step with `v_pinned_tools` in get_cx_conversation_bundle
(common-docs/projects/chat-package-move/lazy-tool-calls-bundle-rpc.sql.md).
"""

from __future__ import annotations

import os
from typing import Any

RESULT_INLINE_MAX_BYTES = 4096
RESULT_PREVIEW_MAX_CHARS = 500

LAZY_TOOL_RESULTS_ENV = "MATRX_LAZY_TOOL_RESULTS"


def lazy_tool_results_enabled() -> bool:
    """Slim stream frames are OFF unless this is switched on.

    Clients published before the lazy-detail client cannot read `result: null` /
    `result_omitted`. Turn on only once the new chat client is live everywhere
    (web, extension, desktop); the later step is a per-request client capability.
    """
    return os.environ.get(LAZY_TOOL_RESULTS_ENV, "").strip().lower() in {"1", "true", "on", "yes"}


PINNED_TOOLS: frozenset[str] = frozenset(
    {
        "ask_person",
        "ask_user",
        "interaction_ask",
        "ask",
        "google_email_send",
        "request_user_takeover",
        "credential_capture",
        "capture_credential",
        "update_plan",
        "plan_approval",
        "agent",
        "send_message",
        "agent_call",
        "generate_image",
        "image_generate",
        "image_generation",
        "generate_media",
    }
)


def is_pinned(tool_name: str, result: Any = None, *, has_surface_write: bool = False) -> bool:
    """True when this call's full result must ride the stream."""
    if tool_name in PINNED_TOOLS or has_surface_write:
        return True
    return isinstance(result, dict) and result.get("awaiting_approval") is True and result.get("applied") is not True


__all__ = ["LAZY_TOOL_RESULTS_ENV", "lazy_tool_results_enabled", "PINNED_TOOLS", "RESULT_INLINE_MAX_BYTES", "RESULT_PREVIEW_MAX_CHARS", "is_pinned"]
