"""Shared conversation compaction service.

Single owner of compaction behaviour for both the shared agent loop
(web UI + CLI auto-compact) and the CLI ``/compact`` command.

History:

* **#1412** — initial refactor that unified both caller paths behind
  ``compact_messages()``.  Preserves each caller's shipped role +
  content template.  No in-memory shape changes.
* **#1413** — boundary-based compaction.  Adds a ``preserve_tail``
  kwarg that summarises only older messages and keeps the trailing N
  messages intact.  Emits a boundary marker between summary and tail.
  Persists the compacted form to SQLite via
  :func:`persist_compacted_messages` with UPDATE + DELETE semantics so
  attachments, tool_calls, and embeddings on tail messages survive.
"""

from __future__ import annotations

import asyncio
import json
import logging
import re
import shlex
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, cast

from .ai_service import AIService, CompletionResult
from .token_estimator import count_message_tokens
from .tool_result_compact import compact_tool_output

logger = logging.getLogger(__name__)


_SESSION_STATE_RE = re.compile(r"\s*<session_state>.*?</session_state>\s*", re.DOTALL)
"""Matches a `<session_state>...</session_state>` block (with surrounding whitespace).

Used by :func:`_strip_session_state` to scrub prior rehydration state from
messages before re-compaction or before appending a freshly computed block.
"""


def _strip_session_state(content: Any) -> Any:
    """Remove existing ``<session_state>`` blocks from ``content``.

    Non-string inputs are returned unchanged (provider message content can be
    ``None`` or a list of content parts in some providers).  The regex is
    applied greedily with ``DOTALL`` and a trailing ``rstrip()`` trims any
    leftover whitespace at the tail.
    """
    if not isinstance(content, str):
        return content
    return _SESSION_STATE_RE.sub("", content).rstrip()


BOUNDARY_MARKER_CONTENT = "[Context compacted — older history summarized above, recent messages preserved below]"
"""Content string used for the boundary marker system message.

Kept as a module-level constant so renderers and tests can cross-reference it.
"""


def build_boundary_marker(
    *,
    original_count: int,
    preserved_count: int,
    summary_tokens: int,
) -> dict[str, Any]:
    """Construct the boundary marker system message (#1413).

    Emitted between the compact summary and the preserved tail.  Carries
    structured metadata that downstream rehydration (#1414) uses to identify
    compaction boundaries in a persisted conversation.  Always ``role: "system"``.
    """
    return {
        "role": "system",
        "content": BOUNDARY_MARKER_CONTENT,
        "metadata": {
            "compact_boundary": True,
            "original_count": original_count,
            "preserved_count": preserved_count,
            "summary_tokens": summary_tokens,
            "compacted_at": datetime.now(timezone.utc).isoformat(),
        },
    }


COMPACTION_MIN_MESSAGES = 4
"""Below this message count, compaction is skipped and returns failure.

Safety floor — not a tunable threshold. Stays hardcoded."""

# Deprecated in #1266 — read from ``config.compaction.summary_trigger_*``
# instead. These module constants are preserved as literal fallbacks
# frozen at the v1.165 default values so external readers continue to
# work. They are NOT live-bound to ``CompactionConfig`` — if defaults
# change in the future, update the literals here to match or remove the
# module-level re-export entirely.
PROACTIVE_COMPACTION_MSG_THRESHOLD = 80
"""Deprecated literal — use ``CompactionConfig.summary_trigger_msg_count``."""

PROACTIVE_COMPACTION_TOKEN_THRESHOLD = 90_000
"""Deprecated literal — use ``CompactionConfig.summary_trigger_token_count``."""


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
    attempts: int = 0
    retries: int = 0
    reduced_message_count: int = 0
    failure_code: str | None = None
    failure_message: str | None = None


RUNTIME_STORAGE_MESSAGE_ID_KEY = "_storage_message_id"
"""Local-only runtime message key carrying the backing SQLite message row ID."""

RUNTIME_STORAGE_PARENT_MESSAGE_ID_KEY = "_storage_parent_message_id"
"""Local-only runtime tool-result key carrying its parent assistant row ID."""


@dataclass(frozen=True)
class _LogicalTurnGroup:
    """Structural representation of one runtime or persisted turn group."""

    role: str
    start: int
    end: int
    tool_call_ids: tuple[str, ...] = ()
    message_ids: tuple[str, ...] = ()


@dataclass(frozen=True)
class LogicalTailBoundary:
    """Shared runtime/storage boundary decision for tail-preserving compaction."""

    runtime_split: int
    summarized_runtime_count: int
    preserved_runtime_count: int
    tail_message_ids: list[str]
    aligned: bool
    reason: str | None = None


@dataclass(frozen=True)
class ToolResultCollapseResult:
    """Outcome of deterministic historical tool-result collapse."""

    success: bool
    modified_count: int = 0
    bytes_saved: int = 0
    keep_recent_groups: int = 2
    compact_chars: int = 200


# ---------------------------------------------------------------------------
# Rehydration (#1414)
# ---------------------------------------------------------------------------


@dataclass(frozen=True)
class RehydrationState:
    """Bounded, deterministic session state that survives compaction (#1414).

    Extracted directly from the message list's tool call arguments/results —
    never LLM-generated — so the post-compact turn retains structured context
    (recent files, working directory, unresolved errors) without relying on
    the summary prose.  All fields are tuples to keep this immutable.
    """

    files_read: tuple[str, ...] = ()
    files_written: tuple[str, ...] = ()
    files_edited: tuple[str, ...] = ()
    last_working_dir: str | None = None
    errors_unresolved: tuple[str, ...] = ()

    def is_empty(self) -> bool:
        return (
            not self.files_read
            and not self.files_written
            and not self.files_edited
            and self.last_working_dir is None
            and not self.errors_unresolved
        )


_FILE_TOOLS_READ = {"read_file"}
_FILE_TOOLS_WRITE = {"write_file"}
_FILE_TOOLS_EDIT = {"edit_file"}

# Matches an explicit `cd <path>` token in a bash command line.  We purposely
# accept both quoted and bare paths; the captured group is used verbatim as a
# `last_working_dir` hint without shell-expanding it.
_CD_RE = re.compile(r"(?:^|[;&|]\s*)cd\s+(?:\"([^\"]+)\"|'([^']+)'|(\S+))")


def _extract_file_path(args: dict[str, Any]) -> str | None:
    """Return the file path from a tool-call argument dict, or None."""
    for key in ("path", "file_path"):
        val = args.get(key)
        if isinstance(val, str) and val:
            return val
    return None


def _bash_retry_key(args: dict[str, Any]) -> str | None:
    """Derive a narrow retry-resolution key for a ``bash`` tool call.

    Two bash calls should only resolve each other's errors when they are
    attempts at the same underlying operation.  Using ``None`` as the key (as
    the initial #1414 impl did) over-resolves: any successful bash call would
    clear an earlier unrelated failed bash command from ``errors_unresolved``.

    We derive a key from the leading command token (e.g. ``pytest`` for
    ``pytest tests/foo``, ``python`` for ``python -m pytest``), which is the
    invocation identity — retry variations like flag differences still share
    the same key, but wholly different commands (``ls`` vs ``pytest``) do not.

    For ``python -m <module>`` invocations we return ``python:<module>`` so a
    successful ``python -m pytest`` resolves an earlier failed
    ``python -m pytest …`` but not a failed ``python -m mypy …``.

    Returns ``None`` when the command cannot be parsed.  Callers should treat
    ``None`` as a non-resolving key (every error with a ``None`` key stays
    unresolved regardless of later success) so malformed bash invocations
    don't accidentally hide real errors.
    """
    cmd = args.get("command") or args.get("cmd") or ""
    if not isinstance(cmd, str) or not cmd.strip():
        return None
    # Strip any leading ``cd foo && `` / ``cd foo;`` prefix so the retry key
    # reflects the actual operation, not the directory change.
    stripped = cmd.strip()
    for sep in ("&&", ";", "|"):
        if stripped.lower().startswith("cd "):
            idx = stripped.find(sep)
            if idx > 0:
                stripped = stripped[idx + len(sep) :].strip()
                break
            # ``cd foo`` with no following command — the bash call IS the
            # directory change, which is its own operation identity.
            break
    try:
        tokens = shlex.split(stripped)
    except ValueError:
        tokens = stripped.split()
    if not tokens:
        return None
    leading = tokens[0]
    # ``python -m <module>`` → identify by the module.
    if leading in ("python", "python3") and len(tokens) >= 3 and tokens[1] == "-m":
        return f"{leading}:{tokens[2]}"
    return leading


def _parse_tool_args(raw: Any) -> dict[str, Any]:
    """Safely parse an OpenAI-style tool call arguments payload.

    OpenAI streams tool arguments as a JSON-encoded string; other providers
    may pass dicts directly.  Non-JSON strings are treated as empty args.
    """
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str) and raw:
        try:
            parsed = json.loads(raw)
        except (json.JSONDecodeError, ValueError):
            return {}
        if isinstance(parsed, dict):
            return parsed
    return {}


def _dedup_preserve_order(items: list[str]) -> list[str]:
    """Deduplicate ``items`` while preserving insertion order."""
    seen: set[str] = set()
    out: list[str] = []
    for item in items:
        if item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def extract_rehydration_state(
    messages: list[dict[str, Any]],
    *,
    max_files: int = 20,
    max_errors: int = 5,
) -> RehydrationState:
    """Extract a :class:`RehydrationState` from a message list (#1414).

    Walks ``messages`` once and collects:

    * file paths touched by ``read_file``/``write_file``/``edit_file`` tool
      calls (deduplicated per category, capped at ``max_files`` per category,
      most recent kept)
    * the last working directory hinted by ``bash`` tool calls — either via an
      explicit ``cwd`` kwarg or by parsing a leading ``cd <path>`` segment of
      the command
    * unresolved tool errors — any tool result with an ``error`` key whose
      parent tool+target is not later successfully retried.  Capped at
      ``max_errors``, most recent kept.

    The extraction is deterministic.  Any JSON parse failure silently skips
    that argument; we never raise out of this helper.
    """
    read: list[str] = []
    written: list[str] = []
    edited: list[str] = []
    last_cwd: str | None = None

    # Track tool_call_id -> (tool_name, target) for error attribution and
    # success retry detection.
    tool_id_index: dict[str, tuple[str, str | None]] = {}

    # Order-aware unresolved-error tracking.  Each pending entry is an error
    # that has NOT yet been resolved by a LATER success for the same
    # (tool_name, target) pair.  A success only clears errors that came
    # BEFORE it — a later error after that success remains unresolved.
    # This matters especially for ``bash`` where ``target`` is usually
    # ``None``; any successful bash call would otherwise hide later
    # unresolved bash errors.
    pending_errors: list[tuple[str, str | None, str]] = []

    for msg in messages:
        role = msg.get("role")
        if role == "tool":
            tc_id = msg.get("tool_call_id") or ""
            tool_name, target = tool_id_index.get(tc_id, ("unknown", None))
            raw_content = msg.get("content", "")
            parsed: Any = None
            if isinstance(raw_content, str) and raw_content:
                try:
                    parsed = json.loads(raw_content)
                except (json.JSONDecodeError, ValueError):
                    parsed = None
            if isinstance(parsed, dict) and "error" in parsed:
                snippet = str(parsed.get("error", ""))[:200]
                pending_errors.append((tool_name, target, snippet))
            else:
                # Success: clear only the errors recorded BEFORE this success
                # for the same (tool_name, target) pair.  Errors recorded
                # later remain unresolved.
                key = (tool_name, target)
                pending_errors = [e for e in pending_errors if (e[0], e[1]) != key]
            continue

        for tc in msg.get("tool_calls", []) or []:
            func = tc.get("function") or {}
            name = str(func.get("name") or "")
            if not name:
                continue
            args = _parse_tool_args(func.get("arguments"))
            # Retry-resolution key: ``target`` pairs a tool call with later
            # results for the same operation.  For file tools this is the
            # file path; for bash we derive a narrow key from the leading
            # command token so a later unrelated bash success (``ls``) does
            # not silently resolve an earlier failed bash command
            # (``pytest``).  See ``_bash_retry_key`` for the full rationale.
            if name == "bash":
                target = _bash_retry_key(args)
            else:
                target = _extract_file_path(args)

            tc_id = tc.get("id") or ""
            if tc_id:
                tool_id_index[tc_id] = (name, target)

            if name in _FILE_TOOLS_READ and target:
                read.append(target)
            elif name in _FILE_TOOLS_WRITE and target:
                written.append(target)
            elif name in _FILE_TOOLS_EDIT and target:
                edited.append(target)
            elif name == "bash":
                # Prefer an explicit cwd kwarg; fall back to parsing `cd`.
                cwd = args.get("cwd")
                if isinstance(cwd, str) and cwd:
                    last_cwd = cwd
                    continue
                cmd = args.get("command") or args.get("cmd") or ""
                if isinstance(cmd, str) and cmd:
                    match = _CD_RE.search(cmd)
                    if match:
                        last_cwd = match.group(1) or match.group(2) or match.group(3)

    # Anything left in pending_errors is unresolved — no later success for the
    # same (tool_name, target) pair was seen.
    unresolved_errors: list[str] = [f"{tool_name}: {snippet}" for tool_name, _, snippet in pending_errors]

    # Cap each category to the most recent N entries, preserving order.
    def _tail(items: list[str], cap: int) -> tuple[str, ...]:
        deduped = _dedup_preserve_order(items)
        if cap > 0 and len(deduped) > cap:
            deduped = deduped[-cap:]
        return tuple(deduped)

    return RehydrationState(
        files_read=_tail(read, max_files),
        files_written=_tail(written, max_files),
        files_edited=_tail(edited, max_files),
        last_working_dir=last_cwd,
        errors_unresolved=_tail(unresolved_errors, max_errors),
    )


def format_rehydration_block(state: RehydrationState) -> str:
    """Render ``state`` as an XML-tagged ``<session_state>`` block.

    Returns an empty string when the state is empty so callers can skip the
    append entirely.  Only non-empty subsections are included.
    """
    if state.is_empty():
        return ""

    lines: list[str] = ["<session_state>"]
    if state.files_read:
        lines.append("Files read: " + ", ".join(state.files_read))
    if state.files_written:
        lines.append("Files written: " + ", ".join(state.files_written))
    if state.files_edited:
        lines.append("Files edited: " + ", ".join(state.files_edited))
    if state.last_working_dir:
        lines.append(f"Working dir: {state.last_working_dir}")
    if state.errors_unresolved:
        lines.append("Last errors: " + "; ".join(state.errors_unresolved))
    lines.append("</session_state>")
    return "\n".join(lines)


def _find_tail_boundary(messages: list[dict[str, Any]], preserve_count: int) -> int:
    """Find the split index for boundary-based compaction.

    Returns the index where ``messages[:index]`` will be summarised and
    ``messages[index:]`` will be preserved intact.  Returns ``0`` when no
    valid split exists; callers should treat that as "full-summary fallback"
    and summarise the entire history.

    Three walk-back rules applied in order:
    1. Start at ``len(messages) - preserve_count``.
    2. Walk backward if the candidate would orphan ``role: "tool"`` messages
       (find the parent ``assistant`` with ``tool_calls`` so tool results
       are never split from their parent call).
    3. Walk backward further so the first preserved message has
       ``role: "user"``.  Required by Anthropic/Bedrock provider ordering
       (a continuation must start with a user turn after a system or summary).

    Returns ``0`` if the walk-back consumed the whole list without finding a
    safe split — the caller falls back to summarising everything.
    """
    if preserve_count <= 0:
        return 0
    if len(messages) < preserve_count + 2:
        return 0

    candidate = len(messages) - preserve_count

    # Rule 1: don't orphan tool results.  Walk back past any tool messages at
    # the candidate boundary so the parent assistant (with its tool_calls)
    # stays attached to its results.
    while candidate > 0 and messages[candidate].get("role") == "tool":
        candidate -= 1

    # Rule 2: provider-safe ordering — the first preserved message must be
    # role="user" so the continuation shape is [summary (user), user, ...].
    while candidate > 0 and messages[candidate].get("role") != "user":
        candidate -= 1

    # Degenerate: walk-back consumed the whole list without a valid user
    # boundary.  Fall back to summarising everything.
    if candidate == 0:
        return 0

    return candidate


def _tool_call_ids_from_message(msg: dict[str, Any]) -> tuple[str, ...]:
    ids: list[str] = []
    for tc in msg.get("tool_calls") or []:
        tc_id = tc.get("id")
        if tc_id:
            ids.append(str(tc_id))
    return tuple(ids)


def _runtime_logical_groups(messages: list[dict[str, Any]]) -> list[_LogicalTurnGroup]:
    groups: list[_LogicalTurnGroup] = []
    for start, end in _identify_turn_groups(messages):
        msg = messages[start]
        role = str(msg.get("role") or "")
        message_id = msg.get(RUNTIME_STORAGE_MESSAGE_ID_KEY)
        groups.append(
            _LogicalTurnGroup(
                role=role,
                start=start,
                end=end,
                tool_call_ids=_tool_call_ids_from_message(msg) if role == "assistant" else (),
                message_ids=(str(message_id),) if message_id else (),
            )
        )
    return groups


def _stored_logical_groups(stored_messages: list[dict[str, Any]]) -> list[_LogicalTurnGroup]:
    groups: list[_LogicalTurnGroup] = []
    for idx, msg in enumerate(stored_messages):
        role = str(msg.get("role") or "")
        msg_id = msg.get("id")
        groups.append(
            _LogicalTurnGroup(
                role=role,
                start=idx,
                end=idx + 1,
                tool_call_ids=_tool_call_ids_from_message(msg) if role == "assistant" else (),
                message_ids=(str(msg_id),) if msg_id else (),
            )
        )
    return groups


def _groups_compatible(runtime_group: _LogicalTurnGroup, stored_group: _LogicalTurnGroup) -> bool:
    if runtime_group.role != stored_group.role:
        return False
    if runtime_group.role == "assistant" and set(runtime_group.tool_call_ids) != set(stored_group.tool_call_ids):
        return False
    if (
        runtime_group.message_ids
        and stored_group.message_ids
        and runtime_group.message_ids[0] != stored_group.message_ids[0]
    ):
        return False
    return True


def logical_tail_boundary(
    runtime_messages: list[dict[str, Any]],
    stored_messages: list[dict[str, Any]] | None,
    preserve_count: int,
) -> LogicalTailBoundary:
    """Select one logical tail boundary and map it to persisted message IDs.

    Runtime history stores assistant tool-call turns as an assistant message
    followed by one or more ``role="tool"`` messages. SQLite stores the same
    turn as one assistant row with child ``tool_calls`` rows. This helper runs
    the existing provider-safe runtime boundary selection once, maps that
    boundary by logical turn-group index to stored rows, and returns the tail
    row IDs that persistence should preserve.
    """
    runtime_split = _find_tail_boundary(runtime_messages, preserve_count)
    if runtime_split <= 0:
        return LogicalTailBoundary(
            runtime_split=0,
            summarized_runtime_count=len(runtime_messages),
            preserved_runtime_count=0,
            tail_message_ids=[],
            aligned=True,
        )

    if stored_messages is None:
        return LogicalTailBoundary(
            runtime_split=runtime_split,
            summarized_runtime_count=runtime_split,
            preserved_runtime_count=len(runtime_messages) - runtime_split,
            tail_message_ids=[],
            aligned=False,
            reason="stored_messages_missing",
        )

    runtime_groups = _runtime_logical_groups(runtime_messages)
    stored_groups = _stored_logical_groups(stored_messages)
    if len(runtime_groups) != len(stored_groups):
        return LogicalTailBoundary(
            runtime_split=runtime_split,
            summarized_runtime_count=runtime_split,
            preserved_runtime_count=len(runtime_messages) - runtime_split,
            tail_message_ids=[],
            aligned=False,
            reason="logical_group_count_mismatch",
        )

    tail_group_index: int | None = None
    for idx, group in enumerate(runtime_groups):
        if group.start == runtime_split:
            tail_group_index = idx
            break
    if tail_group_index is None:
        return LogicalTailBoundary(
            runtime_split=runtime_split,
            summarized_runtime_count=runtime_split,
            preserved_runtime_count=len(runtime_messages) - runtime_split,
            tail_message_ids=[],
            aligned=False,
            reason="runtime_split_not_on_group_boundary",
        )

    for runtime_group, stored_group in zip(runtime_groups, stored_groups, strict=True):
        if not _groups_compatible(runtime_group, stored_group):
            return LogicalTailBoundary(
                runtime_split=runtime_split,
                summarized_runtime_count=runtime_split,
                preserved_runtime_count=len(runtime_messages) - runtime_split,
                tail_message_ids=[],
                aligned=False,
                reason="logical_group_structure_mismatch",
            )

    tail_message_ids: list[str] = []
    for group in stored_groups[tail_group_index:]:
        tail_message_ids.extend(group.message_ids)

    return LogicalTailBoundary(
        runtime_split=runtime_split,
        summarized_runtime_count=runtime_split,
        preserved_runtime_count=len(runtime_messages) - runtime_split,
        tail_message_ids=tail_message_ids,
        aligned=True,
    )


def runtime_messages_from_stored_rows(
    stored_messages: list[dict[str, Any]],
    *,
    tool_replay_max_chars: int = 10_000,
    content_by_message_id: dict[str, Any] | None = None,
) -> list[dict[str, Any]]:
    """Expand stored rows into provider/runtime chat messages.

    Assistant rows with child tool calls replay as an assistant message plus
    synthetic tool-result messages. Local storage IDs are kept on runtime
    messages for later compaction mapping and stripped at the provider
    boundary by ``provider_messages.strip_local_message_fields``.
    """
    messages: list[dict[str, Any]] = []
    content_by_message_id = content_by_message_id or {}
    for msg in stored_messages:
        role = msg.get("role")
        if role not in ("user", "assistant", "system"):
            continue

        msg_id = str(msg.get("id") or "")
        content = content_by_message_id.get(msg_id, msg.get("content"))
        entry: dict[str, Any] = {
            "role": role,
            "content": content,
        }
        if msg_id:
            entry[RUNTIME_STORAGE_MESSAGE_ID_KEY] = msg_id
        if msg.get("metadata"):
            entry["metadata"] = msg["metadata"]

        tool_calls = msg.get("tool_calls") or []
        if tool_calls and role == "assistant":
            entry["tool_calls"] = [
                {
                    "id": tc["id"],
                    "type": "function",
                    "function": {
                        "name": tc["tool_name"],
                        "arguments": json.dumps(tc.get("input") or {}),
                    },
                }
                for tc in tool_calls
            ]
            messages.append(entry)
            for tc in tool_calls:
                tool_entry: dict[str, Any] = {
                    "role": "tool",
                    "tool_call_id": tc["id"],
                    "content": compact_tool_output(tc.get("output"), max_chars=tool_replay_max_chars),
                }
                if msg_id:
                    tool_entry[RUNTIME_STORAGE_PARENT_MESSAGE_ID_KEY] = msg_id
                metadata = entry.get("metadata") or {}
                if metadata.get("compact_preserved_tail"):
                    tool_entry["metadata"] = {"compact_preserved_tail": True}
                messages.append(tool_entry)
            continue

        messages.append(entry)
    return messages


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
        content = _content_for_compaction_summary(msg.get("content", ""))
        # Strip any `<session_state>` block (#1414) from prior summaries so
        # re-compaction does not incorporate stale rehydration state into the
        # new summary prose.
        content = _strip_session_state(content)

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
                snippet = content[:200] + "..." if len(content) > 200 else content
                history_text.append(f"  tool_result: {tool_name} -> SUCCESS: {snippet}")
            continue

        if content:
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


_MEDIA_OMIT_MARKERS = {
    "image": "[image omitted from compaction summary]",
    "image_url": "[image omitted from compaction summary]",
    "input_image": "[image omitted from compaction summary]",
    "document": "[document omitted from compaction summary]",
    "input_document": "[document omitted from compaction summary]",
    "file": "[document omitted from compaction summary]",
    "pdf": "[document omitted from compaction summary]",
}


def _content_for_compaction_summary(content: Any) -> str:
    """Return compact text for the summary prompt, omitting bulky media payloads."""
    if isinstance(content, str):
        return content
    if content is None:
        return ""
    if not isinstance(content, list):
        return str(content)

    parts: list[str] = []
    for part in content:
        if isinstance(part, str):
            parts.append(part)
            continue
        if not isinstance(part, dict):
            parts.append(str(part))
            continue
        part_type = str(part.get("type") or "").lower()
        marker = _MEDIA_OMIT_MARKERS.get(part_type)
        if marker:
            parts.append(marker)
            continue
        if part_type == "text":
            text = part.get("text")
            if isinstance(text, str):
                parts.append(text)
            continue
        # Provider-specific content blocks sometimes omit type but carry a
        # bulky key directly.
        bulky_key = next((key for key in _MEDIA_OMIT_MARKERS if key in part), None)
        if bulky_key:
            parts.append(_MEDIA_OMIT_MARKERS[bulky_key])
            continue
        text = part.get("text") or part.get("content")
        if isinstance(text, str):
            parts.append(text)
    return "\n".join(parts)


def _summary_completion_budget(original_tokens: int, summary_max_completion_tokens: int) -> int:
    """Scale summary budget with input size, capped by config."""
    configured = max(256, summary_max_completion_tokens)
    scaled = max(1000, original_tokens // 50)
    return min(configured, scaled)


def _reduce_head_for_compaction_retry(
    head: list[dict[str, Any]],
    *,
    drop_groups: int = 2,
) -> tuple[list[dict[str, Any]], int]:
    """Drop oldest safe turn groups from a summary head for prompt-too-long retry."""
    groups = _identify_turn_groups(head)
    if len(groups) <= 1:
        return head, 0
    groups_to_drop = min(max(1, drop_groups), len(groups) - 1)
    cut = groups[groups_to_drop][0]
    if cut <= 0 or cut >= len(head):
        return head, 0
    return head[cut:], cut


async def _complete_for_compaction(
    ai_service: AIService,
    *,
    messages: list[dict[str, Any]],
    max_completion_tokens: int,
    cancel_event: asyncio.Event | None,
) -> CompletionResult:
    """Call the structured completion path when available, preserving old mocks."""
    complete_result = getattr(ai_service, "complete_result", None)
    instance_complete_override = "complete" in getattr(ai_service, "__dict__", {})
    if callable(complete_result) and "complete_result" in dir(type(ai_service)) and not instance_complete_override:
        return cast(
            CompletionResult,
            await complete_result(
                messages=messages,
                max_completion_tokens=max_completion_tokens,
                cancel_event=cancel_event,
            ),
        )

    try:
        text = await ai_service.complete(
            messages=messages,
            max_completion_tokens=max_completion_tokens,
            cancel_event=cancel_event,
        )
    except Exception as exc:
        raise exc
    if not text:
        return CompletionResult(text=None, error_code="empty_completion", error_message="empty completion")
    return CompletionResult(text=text)


async def compact_messages(
    ai_service: AIService,
    messages: list[dict[str, Any]],
    *,
    role: str = "user",
    content_template: str = AGENT_LOOP_CONTENT_TEMPLATE,
    min_messages: int = COMPACTION_MIN_MESSAGES,
    preserve_tail: int = 0,
    rehydrate: bool = True,
    rehydrate_max_files: int = 20,
    rehydrate_max_errors: int = 5,
    summary_max_completion_tokens: int = 1000,
    summary_retry_max_attempts: int = 3,
    summary_retry_drop_groups: int = 2,
    cancel_event: asyncio.Event | None = None,
) -> CompactionResult:
    """Summarize conversation history in place to reduce context size.

    Callers pass the ``role`` and ``content_template`` they currently use so
    each call site preserves its exact shipped behavior:

    - Shared agent loop (web UI + CLI auto-compact): ``role="user"`` with
      :data:`AGENT_LOOP_CONTENT_TEMPLATE`.
    - CLI ``/compact`` command: ``role="system"`` with
      :data:`REPL_CONTENT_TEMPLATE`.

    **Boundary-based compaction** (``preserve_tail > 0``): only the older
    portion of the conversation is summarised; the trailing *preserve_tail*
    messages are kept intact so the model retains recent context verbatim.
    The boundary is chosen by :func:`_find_tail_boundary`, which applies
    three walk-back rules (no orphaned tool results, user-first ordering,
    full-summary fallback).  When the boundary cannot be placed safely, the
    function falls back to summarising the entire history — matching the
    ``preserve_tail=0`` shape exactly.

    The ``messages`` list is mutated in place: on success it is cleared and
    replaced with ``[summary] + preserved_tail``.  On failure it is left
    untouched.

    **Rehydration** (``rehydrate=True``, #1414): a bounded
    ``<session_state>`` block describing recently touched files, the last
    working directory, and unresolved tool errors is appended to the summary
    message content.  Extraction is deterministic — it parses tool call
    arguments and results, not LLM prose.  The block is capped by
    ``rehydrate_max_files`` (per category) and ``rehydrate_max_errors``.
    Set ``rehydrate=False`` to disable.

    Returns a :class:`CompactionResult` with metadata useful for caller UX
    rendering (token counts, original message count, summary text).
    ``original_count`` and ``original_tokens`` always describe the *full*
    input, not just the summarised prefix, so UX reporting is consistent
    across boundary-based and full-summary paths.
    """
    original_count = len(messages)
    original_tokens = count_message_tokens(messages)

    if original_count < min_messages:
        return CompactionResult(
            success=False,
            original_count=original_count,
            original_tokens=original_tokens,
            summary="",
            failure_code="too_few_messages",
            failure_message="not enough messages to compact",
        )

    split = _find_tail_boundary(messages, preserve_tail)
    head = messages[:split] if split > 0 else list(messages)
    tail = messages[split:] if split > 0 else []

    attempt_head = list(head)
    max_attempts = max(1, summary_retry_max_attempts)
    output_budget = _summary_completion_budget(original_tokens, summary_max_completion_tokens)
    attempts = 0
    reduced_message_count = 0
    last_failure_code: str | None = None
    last_failure_message: str | None = None
    summary = ""

    for attempt in range(1, max_attempts + 1):
        attempts = attempt
        history_text = build_compaction_history(attempt_head)
        summary_prompt = _SUMMARY_PROMPT_PREFIX + history_text

        try:
            completion = await _complete_for_compaction(
                ai_service,
                messages=[{"role": "user", "content": summary_prompt}],
                max_completion_tokens=output_budget,
                cancel_event=cancel_event,
            )
        except Exception as exc:
            logger.exception("Failed to generate compaction summary")
            return CompactionResult(
                success=False,
                original_count=original_count,
                original_tokens=original_tokens,
                summary="",
                attempts=attempts,
                retries=max(0, attempts - 1),
                reduced_message_count=reduced_message_count,
                failure_code="provider_error",
                failure_message=str(exc),
            )

        if completion.text:
            summary = completion.text
            break

        last_failure_code = completion.error_code or "empty_completion"
        last_failure_message = completion.error_message

        if last_failure_code != "context_length_exceeded" or attempt >= max_attempts:
            logger.warning(
                "Compaction summary failed (%s) — messages left untouched",
                last_failure_code,
            )
            return CompactionResult(
                success=False,
                original_count=original_count,
                original_tokens=original_tokens,
                summary="",
                attempts=attempts,
                retries=max(0, attempts - 1),
                reduced_message_count=reduced_message_count,
                failure_code=last_failure_code,
                failure_message=last_failure_message,
            )

        reduced_head, dropped = _reduce_head_for_compaction_retry(
            attempt_head,
            drop_groups=summary_retry_drop_groups,
        )
        if dropped <= 0:
            logger.warning("Compaction summary prompt too long and no safe retry reduction is available")
            return CompactionResult(
                success=False,
                original_count=original_count,
                original_tokens=original_tokens,
                summary="",
                attempts=attempts,
                retries=max(0, attempts - 1),
                reduced_message_count=reduced_message_count,
                failure_code=last_failure_code,
                failure_message=last_failure_message,
            )

        reduced_message_count += dropped
        attempt_head = reduced_head
        logger.info(
            "Retrying compaction summary after prompt-too-long; attempt=%d/%d dropped_messages=%d",
            attempt + 1,
            max_attempts,
            reduced_message_count,
        )

    # Boundary-based output shape: the template describes how many messages
    # the summary *replaced*, not the full conversation size.  When no tail
    # is preserved, summarised_count equals original_count and the shape is
    # identical to the legacy full-summary path.
    head = attempt_head
    summarised_count = len(head)

    compacted_content = content_template.format(
        original_count=summarised_count,
        original_tokens=original_tokens,
        summary=summary,
    )

    # Rehydration (#1414): append a bounded, deterministic <session_state>
    # block to the summary content so the model retains recent file/error
    # context after compaction.  The block is extracted from *head* (the
    # messages that are actually being summarised away) — not from the
    # preserved tail, whose structured context survives verbatim.
    #
    # Two strip points guard against re-compaction nesting:
    # 1. `build_compaction_history` already strips prior <session_state>
    #    from each head message before summarisation.
    # 2. We strip from ``compacted_content`` here in case the LLM echoed one
    #    back into its prose summary.
    if rehydrate:
        compacted_content = _strip_session_state(compacted_content)
        rehydration_state = extract_rehydration_state(
            head,
            max_files=rehydrate_max_files,
            max_errors=rehydrate_max_errors,
        )
        block = format_rehydration_block(rehydration_state)
        if block:
            compacted_content = f"{compacted_content}\n\n{block}"

    # Rough token estimate for the summary — 4 chars / token — used by the
    # boundary marker metadata so downstream rehydration (#1414) knows how
    # much context the summary cost.
    summary_tokens = max(1, len(summary) // 4)

    # Summary message carries metadata.compact_summary=True for programmatic
    # detection by #1414 rehydration, independent of the in-memory role.
    summary_msg: dict[str, Any] = {
        "role": role,
        "content": compacted_content,
        "metadata": {
            "compact_summary": True,
            "original_count": summarised_count,
            "original_tokens": original_tokens,
            "summary_tokens": summary_tokens,
        },
    }

    messages.clear()
    messages.append(summary_msg)
    # Boundary marker: only emitted when a tail is actually preserved.  The
    # marker is always role=system so transcript renderers naturally hide it
    # (CSS `system-hidden` in web, skipped by `render_conversation_recap` in CLI).
    if tail:
        messages.append(
            build_boundary_marker(
                original_count=summarised_count,
                preserved_count=len(tail),
                summary_tokens=summary_tokens,
            )
        )
        messages.extend(tail)

    logger.info(
        "Compacted %d/%d messages into summary + boundary + %d preserved tail (role=%s, ~%d tokens original)",
        summarised_count,
        original_count,
        len(tail),
        role,
        original_tokens,
    )
    return CompactionResult(
        success=True,
        original_count=original_count,
        original_tokens=original_tokens,
        summary=summary,
        attempts=attempts,
        retries=max(0, attempts - 1),
        reduced_message_count=reduced_message_count,
    )


# ---------------------------------------------------------------------------
# Persistence (#1413)
# ---------------------------------------------------------------------------


_PERSISTED_SUMMARY_ROLE = "system"
"""Role used when writing the compact summary to SQLite.

In-memory, the summary can be ``user`` (shared loop) or ``system`` (CLI
``/compact``).  On persistence we always translate to ``system`` so both
the web UI transcript (which applies ``system-hidden`` CSS to system roles)
and the CLI recap (which only searches user/assistant) naturally hide the
summary.  See #1413 "Persisted Summary Role" for the full rationale.
"""


def persist_compacted_messages(
    db: Any,
    conversation_id: str,
    *,
    summary_msg: dict[str, Any],
    boundary_msg: dict[str, Any] | None,
    tail_message_ids: list[str],
) -> None:
    """Persist the compacted form of a conversation (#1413).

    Contract:

    1. **DELETE** messages whose IDs are NOT in ``tail_message_ids``.  Cascade
       removes their attachments, tool_calls, and message_embeddings — which
       is correct because those messages are being summarised away.
    2. **INSERT** the summary message with ``role: "system"`` at the head.
    3. **INSERT** the boundary marker (also ``role: "system"``) when present.
    4. **UPDATE** positions of the preserved tail messages so they come right
       after the summary + boundary.  Uses ``UPDATE messages SET position``
       (not DELETE + re-INSERT) so the tail message rows keep their IDs —
       attachments, tool_calls, and embeddings stay attached.

    The summary's in-memory role (``user`` or ``system``) is ignored at the
    storage boundary: the persisted summary is always ``role: "system"``.
    The summary's ``metadata.compact_summary`` flag is preserved.

    Raises on DB errors.  The caller is responsible for holding the
    conversation's lock if concurrent writes are possible.
    """
    # Local import to keep this module callable from tests that don't want
    # the full storage module side-effects loaded.  Cheap at runtime.
    from . import storage as _storage

    now = _storage._now()  # noqa: SLF001 — intentional single source of truth for ISO time

    # --- Step 1: DELETE non-tail messages ------------------------------------
    # We build the parameterised IN clause ourselves because sqlite3 has no
    # native list binding.  Tail IDs are UUIDs generated by storage (never
    # user input), so there is no injection surface, but we bind them as
    # parameters anyway to stay consistent with the rest of the DAL.
    if tail_message_ids:
        placeholders = ",".join("?" * len(tail_message_ids))
        delete_sql = f"DELETE FROM messages WHERE conversation_id = ? AND id NOT IN ({placeholders})"
        db.execute(delete_sql, (conversation_id, *tail_message_ids))
    else:
        db.execute("DELETE FROM messages WHERE conversation_id = ?", (conversation_id,))

    # --- Step 2: INSERT summary at position 0 -------------------------------
    summary_metadata = dict(summary_msg.get("metadata") or {})
    # Always flag for #1414 rehydration.  If the caller already set
    # compact_summary=True, this is a no-op; if they didn't, we set it.
    summary_metadata["compact_summary"] = True
    summary_id = _storage._uuid()  # noqa: SLF001
    db.execute(
        "INSERT INTO messages (id, conversation_id, role, content, user_id, user_display_name,"
        " created_at, position, metadata)"
        " VALUES (?, ?, ?, ?, NULL, NULL, ?, 0, ?)",
        (
            summary_id,
            conversation_id,
            _PERSISTED_SUMMARY_ROLE,
            summary_msg.get("content", ""),
            now,
            json.dumps(summary_metadata),
        ),
    )

    # --- Step 3: INSERT boundary marker at position 1 -----------------------
    next_position = 1
    if boundary_msg is not None:
        boundary_metadata = dict(boundary_msg.get("metadata") or {})
        boundary_metadata.setdefault("compact_boundary", True)
        boundary_id = _storage._uuid()  # noqa: SLF001
        db.execute(
            "INSERT INTO messages (id, conversation_id, role, content, user_id, user_display_name,"
            " created_at, position, metadata)"
            " VALUES (?, ?, ?, ?, NULL, NULL, ?, ?, ?)",
            (
                boundary_id,
                conversation_id,
                "system",  # boundary is always system
                boundary_msg.get("content", BOUNDARY_MARKER_CONTENT),
                now,
                next_position,
                json.dumps(boundary_metadata),
            ),
        )
        next_position += 1

    # --- Step 4: UPDATE tail positions --------------------------------------
    # Reorder preserved tail messages so they come right after summary+boundary.
    # The tail_message_ids list carries the intended order; we renumber
    # sequentially starting from ``next_position``.
    for idx, msg_id in enumerate(tail_message_ids):
        db.execute(
            "UPDATE messages SET position = ? WHERE conversation_id = ? AND id = ?",
            (next_position + idx, conversation_id, msg_id),
        )

    # --- Commit and touch conversation timestamp ----------------------------
    db.execute("UPDATE conversations SET updated_at = ? WHERE id = ?", (now, conversation_id))
    db.commit()

    logger.info(
        "Persisted compacted conversation %s: 1 summary + %d boundary + %d tail messages",
        conversation_id,
        1 if boundary_msg is not None else 0,
        len(tail_message_ids),
    )


# ---------------------------------------------------------------------------
# Staged overflow recovery helpers (#1415)
# ---------------------------------------------------------------------------


def _identify_turn_groups(messages: list[dict[str, Any]]) -> list[tuple[int, int]]:
    """Partition a message list into indivisible turn groups.

    A turn group is the atomic unit of conversation structure that must
    never be split mid-way (OpenAI-compatible APIs reject a ``role: tool``
    message whose matching ``tool_call_id`` is not present on a preceding
    assistant message's ``tool_calls``).

    Turn group rules:

    * A standalone ``user`` message → 1 group.
    * A standalone ``system`` message → 1 group.
    * A standalone ``assistant`` message (no ``tool_calls``) → 1 group.
    * An ``assistant`` message with ``tool_calls`` + all subsequent
      ``role: "tool"`` messages whose ``tool_call_id`` matches one of those
      tool_calls → 1 indivisible group.

    A trailing ``role: "tool"`` message with no preceding matching
    assistant is degenerate but handled defensively — it becomes its own
    group rather than crashing.

    Returns a list of ``(start, end_exclusive)`` index pairs such that
    ``messages[start:end_exclusive]`` is exactly one turn group.
    """
    groups: list[tuple[int, int]] = []
    i = 0
    n = len(messages)
    while i < n:
        msg = messages[i]
        role = msg.get("role")
        tool_calls = msg.get("tool_calls") or []
        if role == "assistant" and tool_calls:
            expected_ids = {tc.get("id") for tc in tool_calls if tc.get("id")}
            j = i + 1
            while j < n:
                nxt = messages[j]
                if nxt.get("role") == "tool" and nxt.get("tool_call_id") in expected_ids:
                    j += 1
                    continue
                break
            groups.append((i, j))
            i = j
        else:
            groups.append((i, i + 1))
            i += 1
    return groups


def collapse_old_tool_results(
    messages: list[dict[str, Any]],
    *,
    keep_recent_groups: int = 2,
    compact_chars: int = 200,
) -> bool:
    """Boolean-compatible wrapper for historical tool-result collapse."""
    return collapse_old_tool_results_details(
        messages,
        keep_recent_groups=keep_recent_groups,
        compact_chars=compact_chars,
    ).success


def _tool_content_for_compaction(content: Any) -> Any:
    if isinstance(content, str):
        try:
            parsed = json.loads(content)
        except (json.JSONDecodeError, ValueError, TypeError):
            return content
        if isinstance(parsed, dict):
            return parsed
    return content


def _tool_content_size(content: Any) -> int:
    if isinstance(content, str):
        return len(content)
    try:
        return len(json.dumps(content, default=str))
    except Exception:
        return len(repr(content))


def collapse_old_tool_results_details(
    messages: list[dict[str, Any]],
    *,
    keep_recent_groups: int = 2,
    compact_chars: int = 200,
) -> ToolResultCollapseResult:
    """Compact historical tool results (all older turn groups) to ``compact_chars``.

    This is a cheaper pre-compaction recovery step than full LLM compaction:
    it aggressively shrinks *all* older tool results regardless of current
    size, using :func:`services.tool_result_compact.compact_tool_output` to
    preserve structured fields (exit_code, error, path) while truncating
    bulk content (stdout, stderr).

    Different from :func:`_truncate_large_tool_outputs` in
    ``agent_loop.py``, which only acts on messages currently exceeding
    ``max_chars``.  This function acts on every older tool message.

    Operates on turn-group boundaries — the most recent
    ``keep_recent_groups`` turn groups are left untouched, including any
    tool-result messages inside them.  Returns structured details for
    proactive callers; :func:`collapse_old_tool_results` preserves the
    historical boolean contract for reactive callers.
    """
    keep_recent_groups = max(0, keep_recent_groups)
    compact_chars = max(2, compact_chars)
    groups = _identify_turn_groups(messages)
    if len(groups) <= keep_recent_groups:
        return ToolResultCollapseResult(
            success=False,
            keep_recent_groups=keep_recent_groups,
            compact_chars=compact_chars,
        )

    # Cutoff: the end-exclusive index of the last group we compact.
    cutoff = groups[-keep_recent_groups][0] if keep_recent_groups > 0 else len(messages)

    modified_count = 0
    bytes_saved = 0
    for idx in range(cutoff):
        msg = messages[idx]
        if msg.get("role") != "tool":
            continue
        original_content = msg.get("content", "")
        original_len = _tool_content_size(original_content)
        new_content = compact_tool_output(_tool_content_for_compaction(original_content), max_chars=compact_chars)
        new_len = len(new_content)
        if new_content != original_content and new_len < original_len:
            msg["content"] = new_content
            modified_count += 1
            bytes_saved += original_len - new_len
    return ToolResultCollapseResult(
        success=modified_count > 0,
        modified_count=modified_count,
        bytes_saved=bytes_saved,
        keep_recent_groups=keep_recent_groups,
        compact_chars=compact_chars,
    )


def drop_old_turn_groups(
    messages: list[dict[str, Any]],
    *,
    keep_recent_groups: int = 4,
) -> bool:
    """Drop older turn groups and replace them with a deterministic summary.

    The cheapest recovery strategy short of aborting — no LLM call, purely
    structural.  Delegates boundary selection to :func:`_find_tail_boundary`
    so the walk-back rules (no orphaned tool results, provider-safe
    user-first ordering) are applied identically to the LLM-based
    compaction path.

    The inserted summary message matches :func:`compact_messages` output
    shape exactly so downstream consumers (#1414 rehydration stripper,
    transcript renderers, introspect) do not need a special case:

    * ``role: "user"`` (shared-loop contract from #1412).
    * Content via :data:`AGENT_LOOP_CONTENT_TEMPLATE`.
    * ``metadata["compact_summary"] = True`` plus ``original_count``,
      ``original_tokens``, ``summary_tokens``.
    * When a tail is preserved, :func:`build_boundary_marker` is inserted
      between the summary and the preserved tail.

    Returns ``True`` if turn groups were dropped and the message list was
    mutated in place; ``False`` if no safe split exists.
    """
    groups = _identify_turn_groups(messages)
    if len(groups) <= keep_recent_groups:
        return False

    preserve_start_group = groups[-keep_recent_groups]
    preserve_count = len(messages) - preserve_start_group[0]

    split = _find_tail_boundary(messages, preserve_count)
    if split <= 0:
        return False

    head = messages[:split]
    tail = messages[split:]
    if not head:
        return False

    original_count = len(messages)
    # Token count describes the FULL input, not just the summarised prefix.
    # This matches compact_messages()'s metadata contract so downstream
    # consumers can treat staged-recovery summaries and full-LLM-compaction
    # summaries uniformly.  See the compact_messages() docstring and the
    # shape defined around services/compaction.py:303-327.
    original_tokens = count_message_tokens(messages)

    # Deterministic prose body from the dropped portion, capped so the
    # summary itself does not reintroduce context pressure.
    history_text = build_compaction_history(head)
    if len(history_text) > 2000:
        history_text = history_text[:2000] + "..."

    summary_content = AGENT_LOOP_CONTENT_TEMPLATE.format(
        original_count=len(head),
        original_tokens=original_tokens,
        summary=history_text,
    )

    summary_tokens = max(1, len(history_text) // 4)

    summary_msg: dict[str, Any] = {
        "role": "user",
        "content": summary_content,
        "metadata": {
            "compact_summary": True,
            "original_count": len(head),
            "original_tokens": original_tokens,
            "summary_tokens": summary_tokens,
        },
    }

    messages.clear()
    messages.append(summary_msg)
    if tail:
        messages.append(
            build_boundary_marker(
                original_count=len(head),
                preserved_count=len(tail),
                summary_tokens=summary_tokens,
            )
        )
        messages.extend(tail)

    logger.info(
        "Dropped %d/%d older turn groups into deterministic summary + %d preserved tail",
        len(head),
        original_count,
        len(tail),
    )
    return True
