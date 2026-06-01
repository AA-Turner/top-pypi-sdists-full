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
    """Map Cursor-style camelCase event names to Claude Code PascalCase.

    Pass-through for already-PascalCase names and unknown variants. Used both
    for internal dispatch and for response shaping (deny `hookEventName`),
    so any future client-specific spelling only needs one map entry.
    """
    return EVENT_NORMALIZE.get(event, event)


_CURSOR_DIR_PATTERNS = (
    "/.cursor/",
    "/application support/cursor/",
    "/etc/cursor/",
    "/programdata/cursor/",
)


def _invoked_argv_parent_str() -> str:
    """Native-separator string of the invoked hook directory.

    Uses Path.absolute() (not resolve()) so symlinks are NOT followed: the
    MDM-installed binary lives at /usr/local/lib/runlayer/aiwatch-enforce/
    and clients invoke it through symlinks in their own hooks dirs (e.g.
    ~/.cursor/hooks/, ~/.codex/hooks/). Following the symlink would erase
    the per-client path component and silently break client detection plus
    the cursor-noop guard. Matches bash `dirname "$0"` semantics.
    """
    return str(Path(sys.argv[0]).absolute().parent)


def _normalized_hook_dir() -> str:
    """Hook dir lowercased with backslashes flipped to slashes.

    Path.absolute() yields native separators, so on Windows a Codex install at
    C:\\Users\\user\\.codex\\hooks would never match patterns like '/.codex/'.
    Normalizing here keeps a single set of POSIX-shaped patterns valid on both.
    """
    return _invoked_argv_parent_str().lower().replace("\\", "/")


def detect_client() -> Client:
    """Detect which AI coding client invoked this hook."""
    if os.environ.get("CURSOR_VERSION"):
        return Client.CURSOR

    hook_dir = _normalized_hook_dir()
    if "/.hermes/" in hook_dir:
        return Client.HERMES
    if "/.codex/" in hook_dir or hook_dir.startswith("/etc/codex/"):
        return Client.CODEX

    return Client.CLAUDE_CODE


def should_noop_for_cursor(client: Client) -> bool:
    """Return True if Cursor loaded this hook from a non-Cursor config dir.

    Avoids double-enforcement when both Cursor and Claude Code hooks are installed.
    """
    if client != Client.CURSOR:
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
