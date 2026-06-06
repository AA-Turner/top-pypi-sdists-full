"""Client detection and per-client JSON response shaping."""

from __future__ import annotations

import json
import os
import sys
from enum import Enum
from pathlib import Path

from runlayer_cli.hook import messages


class Client(str, Enum):
    CURSOR = "cursor"
    CLAUDE_CODE = "claude_code"
    CODEX = "codex"
    HERMES = "hermes"


EVENT_NORMALIZE: dict[str, str] = {
    "preToolUse": "PreToolUse",
    "postToolUse": "PostToolUse",
    "postToolUseFailure": "PostToolUseFailure",
    "stop": "Stop",
    "sessionStart": "SessionStart",
    "sessionEnd": "SessionEnd",
    "subagentStart": "SubagentStart",
    "subagentStop": "SubagentStop",
    "beforeSubmitPrompt": "UserPromptSubmit",
    "preCompact": "PreCompact",
    "pre_tool_call": "PreToolUse",
    "post_tool_call": "PostToolUse",
    "transform_tool_result": "PostToolUse",
    "pre_llm_call": "UserPromptSubmit",
    "on_session_start": "SessionStart",
    "on_session_end": "SessionEnd",
    "on_session_finalize": "Stop",
}


def normalize_event_name(event: str) -> str:
    """Map camelCase / snake_case event names to PascalCase; pass-through unknowns."""
    return EVENT_NORMALIZE.get(event, event)


_CURSOR_DIR_PATTERNS = (
    "/.cursor/",
    "/application support/cursor/",
    "/etc/cursor/",
    "/programdata/cursor/",
)

_CLAUDE_CODE_DIR_PATTERNS = (
    "/.claude/",
    "/application support/claudecode/",
    "/program files/claudecode/",
    "/etc/claude-code/",
)


def _invoked_argv_parent_str() -> str:
    """Native-separator parent of ``sys.argv[0]``; ``absolute()`` so symlinks aren't followed."""
    return str(Path(sys.argv[0]).absolute().parent)


def _normalized_hook_dir() -> str:
    """Hook dir lowercased + POSIX-slashed so Windows paths match the same patterns."""
    return _invoked_argv_parent_str().lower().replace("\\", "/")


def _explicit_client() -> Client | None:
    value = os.environ.get("RUNLAYER_HOOK_CLIENT")
    args = sys.argv[1:]
    for index, arg in enumerate(args):
        if arg == "--client" and index + 1 < len(args):
            value = args[index + 1]
            break
        if arg.startswith("--client="):
            value = arg.split("=", 1)[1]
            break
    if not value:
        return None
    try:
        return Client(value)
    except ValueError:
        return None


def detect_client() -> Client:
    """Detect which AI coding client invoked this hook."""
    explicit = _explicit_client()
    if explicit is not None:
        return explicit

    if os.environ.get("CURSOR_VERSION"):
        return Client.CURSOR

    hook_dir = _normalized_hook_dir()
    if any(pat in hook_dir for pat in _CURSOR_DIR_PATTERNS):
        return Client.CURSOR
    if "/.hermes/" in hook_dir:
        return Client.HERMES
    if "/.codex/" in hook_dir or hook_dir.startswith("/etc/codex/"):
        return Client.CODEX
    if any(pat in hook_dir for pat in _CLAUDE_CODE_DIR_PATTERNS):
        return Client.CLAUDE_CODE

    return Client.CLAUDE_CODE


def should_noop_for_cursor(client: Client) -> bool:
    """Return True if Cursor loaded this hook from a non-Cursor config dir.

    Avoids double-enforcement when both Cursor and Claude Code hooks are installed.

    Only applies to the unfrozen / legacy bash-shim path, where each client gets
    its own shim copy under its config dir. The frozen ``aiwatch-hook`` binary
    is a single shared exe (e.g. ``/usr/local/lib/runlayer/aiwatch/aiwatch-hook``)
    wired into every client's config — ``sys.argv[0]`` is identical regardless
    of which client invoked it, so the path-based guard can't distinguish them.
    Trust the MDM operator's wiring on the frozen path.
    """
    explicit = _explicit_client()
    if os.environ.get("CURSOR_VERSION") and explicit != Client.CURSOR:
        hook_dir = _normalized_hook_dir()
        return not any(pat in hook_dir for pat in _CURSOR_DIR_PATTERNS)

    if client != Client.CURSOR:
        return False
    if getattr(sys, "frozen", False):
        return False

    if explicit == Client.CURSOR:
        return False

    hook_dir = _normalized_hook_dir()
    return not any(pat in hook_dir for pat in _CURSOR_DIR_PATTERNS)


class HookResponse:
    """Encapsulates a deny or allow and writes the correct JSON for the client."""

    def __init__(self, client: Client, hook_event_name: str) -> None:
        self._client = client
        self._event = normalize_event_name(hook_event_name)

    def deny(
        self,
        user_msg: str = messages.DEFAULT_USER_MSG,
        agent_msg: str = "",
    ) -> str:
        if not agent_msg:
            agent_msg = messages.default_agent_msg()
        if self._client == Client.CURSOR:
            return json.dumps(
                {
                    "permission": "deny",
                    "continue": True,
                    "user_message": user_msg,
                    "agentMessage": agent_msg,
                }
            )
        if self._client == Client.CODEX:
            if self._event == "PermissionRequest":
                return json.dumps(
                    {
                        "hookSpecificOutput": {
                            "hookEventName": "PermissionRequest",
                            "decision": {
                                "behavior": "deny",
                                "message": user_msg,
                            },
                        }
                    }
                )
            if self._event == "PreToolUse":
                return json.dumps(
                    {
                        "hookSpecificOutput": {
                            "hookEventName": "PreToolUse",
                            "permissionDecision": "deny",
                            "permissionDecisionReason": user_msg,
                        }
                    }
                )
            return json.dumps({"decision": "block", "reason": user_msg})
        if self._client == Client.HERMES:
            return json.dumps(
                {
                    "action": "block",
                    "message": user_msg,
                }
            )
        return json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": self._event,
                    "permissionDecision": "deny",
                    "permissionDecisionReason": agent_msg,
                }
            }
        )

    def allow(self) -> str | None:
        """Return allow JSON for blocking events, or None for Claude Code."""
        if self._client == Client.CURSOR:
            return '{"permission":"allow"}'
        if self._client == Client.HERMES:
            return "{}"
        return None

    def allow_with_ids(self, tool_input: dict, session_id: str) -> str | None:
        """Cursor-only: allow with _runlayer_session_id injected."""
        if self._client != Client.CURSOR:
            return None
        if not session_id:
            return '{"permission":"allow"}'
        merged = {**tool_input, "_runlayer_session_id": session_id}
        return json.dumps({"permission": "allow", "updated_input": merged})

    def observational(self) -> str | None:
        """Output for non-blocking observational events."""
        if self._client == Client.CURSOR:
            return "{}"
        return None

    def block_output(self, reason: str) -> str:
        """Return the cross-client output-blocking shape used by post hooks."""
        if self._client == Client.HERMES:
            return json.dumps(reason)
        return json.dumps({"decision": "block", "reason": reason})
