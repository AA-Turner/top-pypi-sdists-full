"""Shared conversation compaction service.

Single owner of compaction behavior for both the shared agent loop
(web UI + CLI auto-compact) and the CLI ``/compact`` command.

This module is a pure refactor: it preserves the exact current shipped
compacted-message shape (role + content format) for each caller via a
parameterized role and content template. No behavioral changes are
introduced beyond routing the CLI path through ``ai_service.complete()``
(the proper service-layer abstraction) instead of bypassing it with a
direct ``client.chat.completions.create()`` call.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass
from typing import Any

from .ai_service import AIService
from .token_estimator import count_message_tokens

logger = logging.getLogger(__name__)


COMPACTION_MIN_MESSAGES = 4
"""Below this message count, compaction is skipped and returns failure."""

PROACTIVE_COMPACTION_MSG_THRESHOLD = 80
"""Fallback trigger: compact when the message count exceeds this value."""

PROACTIVE_COMPACTION_TOKEN_THRESHOLD = 90_000
"""Primary trigger: compact when estimated tokens exceed this value."""


AGENT_LOOP_CONTENT_TEMPLATE = (
    "[Previous conversation summary (auto-compacted from {original_count} messages)]\n\n"
    "{summary}\n\nPlease continue from where we left off."
)
"""Shared agent loop template. Format keys: ``original_count``, ``summary``."""


REPL_CONTENT_TEMPLATE = (
    "Previous conversation summary "
    "(auto-compacted from {original_count} messages, "
    "~{original_tokens:,} tokens):\n\n{summary}"
)
"""CLI ``/compact`` template. Format keys: ``original_count``, ``original_tokens``, ``summary``."""


_SUMMARY_PROMPT_PREFIX = (
    "Summarize the following conversation concisely, preserving:\n"
    "- Key decisions and conclusions\n"
    "- File paths that were read, written, or edited\n"
    "- Important code changes and their purpose\n"
    "- Which steps of any multi-step plan have been COMPLETED (tool_result SUCCESS) vs remaining\n"
    "- Current state of the task — what has been done and what is next\n"
    "- Any errors encountered and how they were resolved\n\n"
)


@dataclass(frozen=True)
class CompactionResult:
    """Outcome of a compaction attempt."""

    success: bool
    original_count: int
    original_tokens: int
    summary: str


def build_compaction_history(messages: list[dict[str, Any]]) -> str:
    """Build a structured history string for the compaction summary prompt.

    Includes tool call outcomes (not just names) so the AI can distinguish
    completed steps from pending ones after compaction.
    """
    history_text: list[str] = []
    tool_id_to_name: dict[str, str] = {}
    for msg in messages:
        for tc in msg.get("tool_calls", []):
            tc_id = tc.get("id", "")
            func = tc.get("function", {})
            if tc_id and func.get("name"):
                tool_id_to_name[tc_id] = func["name"]

    for msg in messages:
        role = msg.get("role", "unknown")
        content = msg.get("content", "")

        if role == "tool":
            tc_id = msg.get("tool_call_id", "")
            tool_name = tool_id_to_name.get(tc_id, "unknown")
            try:
                result = json.loads(content) if isinstance(content, str) and content else {}
            except (json.JSONDecodeError, ValueError):
                result = {"raw": content}
            if isinstance(result, dict) and "error" in result:
                snippet = str(result["error"])[:200]
                history_text.append(f"  tool_result: {tool_name} -> ERROR: {snippet}")
            else:
                safe_content = content if isinstance(content, str) else ""
                snippet = safe_content[:200] + "..." if len(safe_content) > 200 else safe_content
                history_text.append(f"  tool_result: {tool_name} -> SUCCESS: {snippet}")
            continue

        if isinstance(content, str) and content:
            truncated = content[:500] + "..." if len(content) > 500 else content
            history_text.append(f"{role}: {truncated}")

        for tc in msg.get("tool_calls", []):
            func = tc.get("function", {})
            name = func.get("name", "?")
            args_raw = func.get("arguments", "")
            try:
                args = json.loads(args_raw) if args_raw else {}
                args_preview = ", ".join(f"{k}={str(v)[:40]!r}" for k, v in list(args.items())[:3])
            except (json.JSONDecodeError, ValueError):
                args_preview = args_raw[:80]
            history_text.append(f"  tool_call: {name}({args_preview})")

    return "\n".join(history_text)


async def compact_messages(
    ai_service: AIService,
    messages: list[dict[str, Any]],
    *,
    role: str = "user",
    content_template: str = AGENT_LOOP_CONTENT_TEMPLATE,
    min_messages: int = COMPACTION_MIN_MESSAGES,
) -> CompactionResult:
    """Summarize conversation history in place to reduce context size.

    Callers pass the ``role`` and ``content_template`` they currently use so
    each call site preserves its exact shipped behavior:

    - Shared agent loop (web UI + CLI auto-compact): ``role="user"`` with
      :data:`AGENT_LOOP_CONTENT_TEMPLATE`.
    - CLI ``/compact`` command: ``role="system"`` with
      :data:`REPL_CONTENT_TEMPLATE`.

    The ``messages`` list is mutated in place: on success it is cleared and
    replaced with the single summary message. On failure it is left
    untouched.

    Returns a :class:`CompactionResult` with metadata useful for caller UX
    rendering (token counts, original message count, summary text).
    """
    original_count = len(messages)
    original_tokens = count_message_tokens(messages)

    if original_count < min_messages:
        return CompactionResult(
            success=False,
            original_count=original_count,
            original_tokens=original_tokens,
            summary="",
        )

    history_text = build_compaction_history(messages)
    summary_prompt = _SUMMARY_PROMPT_PREFIX + history_text

    try:
        raw_summary = await ai_service.complete(
            messages=[{"role": "user", "content": summary_prompt}],
            max_completion_tokens=1000,
        )
    except Exception:
        logger.exception("Failed to generate compaction summary")
        return CompactionResult(
            success=False,
            original_count=original_count,
            original_tokens=original_tokens,
            summary="",
        )

    # ``AIService.complete()`` swallows provider errors (AuthenticationError,
    # network, rate limits, etc.) and returns ``None``.  Treating that as a
    # success path with fallback text would silently collapse the live
    # conversation into "Conversation summary unavailable." — the CLI
    # ``/compact`` flow in particular historically rendered an error and
    # left ``ai_messages`` untouched.  Preserve that contract: any falsy
    # result from ``complete()`` is a failure that leaves ``messages``
    # alone and signals the caller to surface an error.
    if not raw_summary:
        logger.warning("Compaction summary empty/None — treating as failure; messages left untouched")
        return CompactionResult(
            success=False,
            original_count=original_count,
            original_tokens=original_tokens,
            summary="",
        )

    summary = raw_summary

    compacted_content = content_template.format(
        original_count=original_count,
        original_tokens=original_tokens,
        summary=summary,
    )

    messages.clear()
    messages.append({"role": role, "content": compacted_content})

    logger.info(
        "Compacted %d messages into summary (role=%s, ~%d tokens original)",
        original_count,
        role,
        original_tokens,
    )
    return CompactionResult(
        success=True,
        original_count=original_count,
        original_tokens=original_tokens,
        summary=summary,
    )
