"""Client detection and per-client JSON response shaping."""

from __future__ import annotations

import json
import sys
from enum import Enum
from pathlib import Path
from typing import cast

from runlayer_cli.hook import hook_io, messages


class Client(str, Enum):
    CURSOR = "cursor"
    VSCODE = "vscode"
    CLAUDE_CODE = "claude_code"
    CODEX = "codex"
    HERMES = "hermes"
    GOOSE = "goose"
    GITHUB_COPILOT_CLI = "github-copilot-cli"
    WINDSURF = "windsurf"
    QWEN_CODE = "qwen-code"
    GEMINI_CLI = "gemini-cli"
    GROK_CLI = "grok-cli"
    CLINE_CLI = "cline-cli"
    DEVIN_CLI = "devin-cli"


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
    "beforeTabFileRead": "BeforeReadFile",
    "afterTabFileEdit": "AfterFileEdit",
    "userPromptSubmitted": "UserPromptSubmit",
    "preCompact": "PreCompact",
    "permissionRequest": "PermissionRequest",
    "agentStop": "Stop",
    "errorOccurred": "ErrorOccurred",
    "notification": "Notification",
    # Gemini CLI event vocabulary (names unique to Gemini, so mapping them
    # globally cannot collide with another client's events).
    "BeforeTool": "PreToolUse",
    "AfterTool": "PostToolUse",
    "BeforeAgent": "UserPromptSubmit",
    "AfterAgent": "Stop",
    "PreCompress": "PreCompact",
    "pre_tool_call": "PreToolUse",
    "post_tool_call": "PostToolUse",
    "transform_tool_result": "PostToolUse",
    "pre_llm_call": "UserPromptSubmit",
    "on_session_start": "SessionStart",
    "on_session_end": "SessionEnd",
    "on_session_finalize": "Stop",
    # Windsurf/Cascade. No session start/end events exist upstream, so the
    # session is derived from the trajectory id carried on every event.
    "pre_mcp_tool_use": "PreToolUse",
    "post_mcp_tool_use": "PostToolUse",
    "pre_run_command": "BeforeShellExecution",
    "post_run_command": "AfterShellExecution",
    "pre_read_code": "BeforeReadFile",
    "post_write_code": "AfterFileEdit",
    "pre_user_prompt": "UserPromptSubmit",
    "post_cascade_response": "Stop",
    # Cline CLI: the hook *file name* is the authoritative event (the installed
    # script exports HOOK_EVENT_NAME), but its stdin payload carries a
    # snake_case ``hookName``. These map that payload field as a fallback so a
    # hand-installed script without the env var still normalizes correctly.
    "tool_call": "PreToolUse",
    "tool_result": "PostToolUse",
    "agent_start": "SessionStart",
    "agent_resume": "SessionStart",
    "prompt_submit": "UserPromptSubmit",
    "agent_end": "Stop",
    "agent_abort": "Stop",
    "agent_error": "ErrorOccurred",
    "session_shutdown": "SessionEnd",
    # Cline hook file names that are not already PascalCase canonical events.
    "TaskStart": "SessionStart",
    "TaskResume": "SessionStart",
    "TaskComplete": "Stop",
    "TaskCancel": "Stop",
    "TaskError": "ErrorOccurred",
    "SessionShutdown": "SessionEnd",
    # Grok Build/Grok CLI uses snake_case names in the native hook channel.
    "pre_tool_use": "PreToolUse",
    "post_tool_use": "PostToolUse",
    "post_tool_use_failure": "PostToolUseFailure",
    "user_prompt_submit": "UserPromptSubmit",
    "session_start": "SessionStart",
    "session_end": "SessionEnd",
    "subagent_start": "SubagentStart",
    "subagent_stop": "SubagentStop",
    "stop_failure": "ErrorOccurred",
    "pre_compact": "PreCompact",
    "post_compact": "PostCompact",
    "permission_denied": "PermissionDenied",
    # Devin CLI reuses Claude Code's PascalCase vocabulary verbatim; the
    # post-compaction event is the only name that diverges.
    "PostCompaction": "PostCompact",
}


def normalize_event_name(event: str) -> str:
    """Map camelCase / snake_case event names to PascalCase; pass-through unknowns."""
    return EVENT_NORMALIZE.get(event, event)


# Post-tool events that share the output-redaction path: a failed tool's error
# output can carry sensitive data just like a successful tool's result.
_POST_TOOL_EVENTS = frozenset({"PostToolUse", "PostToolUseFailure"})

# Cline parses stdout by scanning for lines prefixed ``HOOK_CONTROL\t`` (last one
# wins). If NO prefixed line exists it instead requires the entire trimmed stdout
# to be valid JSON, so any incidental logging would corrupt the decision. Always
# emitting the prefixed line makes the channel robust regardless of other output.
_CLINE_CONTROL_PREFIX = "HOOK_CONTROL\t"


def _cline_control(payload: dict[str, object]) -> str:
    return _CLINE_CONTROL_PREFIX + json.dumps(payload)


_UNREPLACEABLE_CLAUDE_OUTPUT = object()


def _is_compatible_json_replacement(original: object, replacement: object) -> bool:
    """Accept sanitized containers without requiring their sensitive keys."""
    if isinstance(original, dict):
        return isinstance(replacement, dict)
    if isinstance(original, list):
        return isinstance(replacement, list)
    return type(original) is type(replacement)


def _is_json_value(value: object) -> bool:
    if value is None or isinstance(value, (str, bool, int, float)):
        return True
    if isinstance(value, list):
        return all(_is_json_value(item) for item in value)
    if isinstance(value, dict):
        value_dict = cast(dict[object, object], value)
        return all(
            isinstance(key, str) and _is_json_value(item)
            for key, item in value_dict.items()
        )
    return False


def _redact_json_value(original: object, replacement: str) -> object:
    """Redact a JSON value without copying data-bearing object keys."""
    if isinstance(original, dict):
        return {"runlayer_redacted": replacement}
    if isinstance(original, list):
        # A list-shaped tool_response is an MCP content-block array, so the
        # replacement has to stay object-shaped. A bare string here fails
        # Messages API validation (`tool_result.content.0: Input should be an
        # object`), and Claude Code persists this into the transcript — so the
        # malformed block replays on every later turn and bricks the session.
        return [{"type": "text", "text": replacement}]
    if isinstance(original, str):
        return replacement
    if isinstance(original, bool):
        return False
    if isinstance(original, int):
        return 0
    if isinstance(original, float):
        return 0.0
    return None


def _claude_tool_output_replacement(
    replacement: str,
    *,
    tool_name: str,
    original_output: object,
) -> object:
    """Return a replacement matching Claude's built-in tool output contract."""
    try:
        structured_replacement = json.loads(replacement)
    except json.JSONDecodeError:
        pass
    else:
        if _is_compatible_json_replacement(original_output, structured_replacement):
            return structured_replacement

    if tool_name == "Bash" and isinstance(original_output, dict):
        bash_output = cast(dict[object, object], original_output)
        return {
            "stdout": replacement,
            "stderr": "",
            "interrupted": bash_output.get("interrupted") is True,
            "isImage": False,
        }
    if _is_json_value(original_output):
        return _redact_json_value(original_output, replacement)
    return _UNREPLACEABLE_CLAUDE_OUTPUT


_CURSOR_DIR_PATTERNS = (
    "/.cursor/",
    "/application support/cursor/",
    "/etc/cursor/",
    "/programdata/cursor/",
)

_VSCODE_DIR_PATTERNS = (
    "/.copilot/hooks/",
    "/.config/code/",
    "/.vscode/",
    "/application support/code/",
    "/appdata/roaming/code/",
)

_CLAUDE_CODE_DIR_PATTERNS = (
    "/.claude/",
    "/application support/claudecode/",
    "/program files/claudecode/",
    "/etc/claude-code/",
)

_GOOSE_DIR_PATTERNS = ("/.agents/plugins/runlayer-hooks/",)

# ``~/.config/devin`` (macOS/Linux) and ``%APPDATA%/devin`` (Windows) are the
# user-level roots; ``/.devin/`` covers per-project config. A bare "/devin/"
# is deliberately excluded -- it would match a user account named ``devin``.
_DEVIN_CLI_DIR_PATTERNS = (
    "/.devin/",
    "/.config/devin/",
    "/roaming/devin/",
)

_WINDSURF_DIR_PATTERNS = (
    "/.codeium/windsurf/",
    "/application support/windsurf/",
    "/etc/windsurf/",
    "/programdata/windsurf/",
)

_GITHUB_COPILOT_CLI_DIR_PATTERNS = (
    "/.copilot/",
    "/etc/github-copilot/",
    "/programdata/github/copilot/",
)

# Qwen's macOS system dir is "QwenCode" (CamelCase, no space) while Linux and
# Windows use the hyphenated "qwen-code"; all three are matched lowercased.
_QWEN_CODE_DIR_PATTERNS = (
    "/.qwen/",
    "/etc/qwen-code/",
    "/application support/qwencode/",
    "/programdata/qwen-code/",
)

_GEMINI_CLI_DIR_PATTERNS = (
    "/.gemini/",
    "/application support/geminicli/",
    "/etc/gemini-cli/",
    "/programdata/gemini-cli/",
)

_GROK_CLI_DIR_PATTERNS = ("/.grok/",)


def _invoked_argv_parent_str() -> str:
    """Native-separator parent of ``argv[0]``; absolutized so symlinks aren't followed."""
    return str(Path(hook_io.abspath(hook_io.argv()[0])).parent)


def _normalized_dir(path: str) -> str:
    """Lowercase + POSIX-slash a directory so Windows paths match the same patterns."""
    hook_dir = path.lower().replace("\\", "/")
    if hook_dir == "/":
        return hook_dir
    return f"{hook_dir.rstrip('/')}/"


def _normalized_hook_dir() -> str:
    return _normalized_dir(_invoked_argv_parent_str())


def _hook_dir_in_copilot_home(hook_dir: str) -> bool:
    return _hook_dir_in_env_home(hook_dir, "COPILOT_HOME")


def _hook_dir_in_qwen_home(hook_dir: str) -> bool:
    return _hook_dir_in_env_home(hook_dir, "QWEN_HOME")


def _hook_dir_in_cline_dir(hook_dir: str) -> bool:
    return _hook_dir_in_env_home(hook_dir, "CLINE_DIR")


def _hook_dir_in_grok_home(hook_dir: str) -> bool:
    return _hook_dir_in_env_home(hook_dir, "GROK_HOME")


def _hook_dir_in_env_home(hook_dir: str, env_var: str) -> bool:
    """True when the hook was loaded from the dir *env_var* relocates."""
    configured_home = hook_io.getenv(env_var)
    if not configured_home:
        return False
    normalized_home = _normalized_dir(
        hook_io.abspath(str(Path(configured_home).expanduser()))
    )
    return hook_dir.startswith(normalized_home)


def _explicit_client() -> Client | None:
    value = hook_io.getenv("RUNLAYER_HOOK_CLIENT")
    args = hook_io.argv()[1:]
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

    if hook_io.getenv("CURSOR_VERSION"):
        return Client.CURSOR

    hook_dir = _normalized_hook_dir()
    if any(pat in hook_dir for pat in _CURSOR_DIR_PATTERNS):
        return Client.CURSOR
    if any(pat in hook_dir for pat in _VSCODE_DIR_PATTERNS):
        return Client.VSCODE
    if "/.hermes/" in hook_dir:
        return Client.HERMES
    if any(pat in hook_dir for pat in _WINDSURF_DIR_PATTERNS):
        return Client.WINDSURF
    if any(pat in hook_dir for pat in _GOOSE_DIR_PATTERNS):
        return Client.GOOSE
    if any(
        pat in hook_dir for pat in _GITHUB_COPILOT_CLI_DIR_PATTERNS
    ) or _hook_dir_in_copilot_home(hook_dir):
        return Client.GITHUB_COPILOT_CLI
    if any(
        pat in hook_dir for pat in _QWEN_CODE_DIR_PATTERNS
    ) or _hook_dir_in_qwen_home(hook_dir):
        return Client.QWEN_CODE
    if any(pat in hook_dir for pat in _GEMINI_CLI_DIR_PATTERNS):
        return Client.GEMINI_CLI
    if any(pat in hook_dir for pat in _GROK_CLI_DIR_PATTERNS) or _hook_dir_in_grok_home(
        hook_dir
    ):
        return Client.GROK_CLI
    if "/.cline/" in hook_dir or _hook_dir_in_cline_dir(hook_dir):
        return Client.CLINE_CLI
    if "/.codex/" in hook_dir or hook_dir.startswith("/etc/codex/"):
        return Client.CODEX
    # DEVIN_PROJECT_DIR is set only in Devin's own hook subprocesses, so it
    # identifies the host for a hook installed without an explicit --client.
    if any(pat in hook_dir for pat in _DEVIN_CLI_DIR_PATTERNS) or hook_io.getenv(
        "DEVIN_PROJECT_DIR"
    ):
        return Client.DEVIN_CLI
    if any(pat in hook_dir for pat in _CLAUDE_CODE_DIR_PATTERNS):
        return Client.CLAUDE_CODE

    return Client.CLAUDE_CODE


def should_noop_for_devin(client: Client) -> bool:
    """True when Devin CLI loaded a hook that belongs to another client.

    Devin imports Claude Code / Cursor / Windsurf configuration by default
    (``read_config_from``) and *collects* hooks from every source rather than
    letting one override another. Without this guard a single Devin tool call
    would fire both Runlayer's Devin hook and the imported Claude Code hook:
    double enforcement, and session telemetry attributed to Claude Code.

    Runlayer's own Devin hook is wired as ``--client devin-cli``, so under a
    Devin host anything that is neither explicitly tagged for Devin nor loaded
    from Devin's own config dir is an imported copy. Checking the resolved
    client alone is not enough: ``detect_client`` infers ``DEVIN_CLI`` from
    ``DEVIN_PROJECT_DIR``, so an *untagged* hook imported from
    ``~/.claude/settings.json`` would otherwise resolve to Devin and run
    alongside the real Devin hook.

    Untagged hooks only exist on the legacy shim path -- every installer writes
    ``--client`` -- and standing one down is the safe direction: the tagged
    Devin hook still enforces, and no tool call is double-enforced.
    """
    if not hook_io.getenv("DEVIN_PROJECT_DIR"):
        return False
    if _explicit_client() == Client.DEVIN_CLI:
        return False
    if any(pat in _normalized_hook_dir() for pat in _DEVIN_CLI_DIR_PATTERNS):
        return False
    return True


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
    if hook_io.getenv("CURSOR_VERSION") and explicit != Client.CURSOR:
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
        if self._client == Client.GITHUB_COPILOT_CLI:
            if self._event == "PermissionRequest":
                return json.dumps(
                    {
                        "behavior": "deny",
                        "message": user_msg,
                    }
                )
            if self._event == "PreToolUse":
                return json.dumps(
                    {
                        "permissionDecision": "deny",
                        "permissionDecisionReason": agent_msg,
                    }
                )
            return json.dumps({"decision": "block", "reason": user_msg})
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
        if self._client == Client.GEMINI_CLI:
            # Gemini reads a top-level decision/reason pair for every event;
            # ``systemMessage`` is what it prints to the user's terminal.
            return json.dumps(
                {
                    "decision": "deny",
                    "reason": agent_msg,
                    "systemMessage": user_msg,
                }
            )
        if self._client == Client.GROK_CLI:
            return json.dumps({"decision": "deny", "reason": agent_msg})
        if self._client == Client.CLINE_CLI:
            # Cline ignores exit codes entirely; ``cancel`` on the control
            # channel is the only way to stop a pending tool call.
            return _cline_control({"cancel": True, "errorMessage": agent_msg})
        if self._client == Client.GOOSE:
            return json.dumps({"decision": "block", "reason": agent_msg})
        if self._client == Client.DEVIN_CLI:
            # Devin reads a top-level decision/reason pair. ``block`` -- not
            # ``deny`` -- is the value its hook runner recognizes.
            return json.dumps({"decision": "block", "reason": agent_msg})
        return json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": self._event,
                    "permissionDecision": "deny",
                    "permissionDecisionReason": agent_msg,
                }
            }
        )

    def deny_stderr(
        self,
        user_msg: str = messages.DEFAULT_USER_MSG,
        agent_msg: str = "",
    ) -> str | None:
        """Stderr text for clients that deny by exit status, else ``None``.

        Windsurf/Cascade parses no hook stdout: a pre-hook blocks only by
        exiting 2, and Cascade surfaces that hook's stderr to the user. Post
        hooks ignore the exit code entirely, so a post-event deny is inert --
        reflected as ``post_tool_output_block_support: unsupported`` in the
        backend capability table rather than special-cased here.
        """
        if self._client != Client.WINDSURF:
            return None
        if not agent_msg:
            agent_msg = messages.default_agent_msg()
        if agent_msg and agent_msg != user_msg:
            return f"{user_msg}\n\n{agent_msg}"
        return user_msg

    def deny_exit_code(self) -> int:
        """Return the client-native exit status for a deny response."""
        # Grok parses the structured deny JSON but only blocks the tool when the
        # hook also exits 2. Other stdout-protocol clients honor a deny on 0.
        return 2 if self._client == Client.GROK_CLI else 0

    def allow(self) -> str | None:
        """Return allow JSON for clients that require it; otherwise no output."""
        if self._client == Client.CURSOR:
            return '{"permission":"allow"}'
        if self._client == Client.HERMES:
            return "{}"
        if self._client == Client.CLINE_CLI:
            # An empty control object is an explicit allow. Emitting it (rather
            # than nothing) keeps the control channel authoritative.
            return _cline_control({})
        return None

    def allow_with_ids(self, tool_input: dict, session_id: str) -> str | None:
        """Cursor-only: allow with _runlayer_session_id injected."""
        if self._client != Client.CURSOR:
            return None
        if not session_id:
            return '{"permission":"allow"}'
        merged = {**tool_input, "_runlayer_session_id": session_id}
        return json.dumps({"permission": "allow", "updated_input": merged})

    def allow_with_updated_input(self, tool_input: dict) -> str | None:
        """Allow with sanitized tool input for clients that support replacement."""
        if self._client == Client.DEVIN_CLI and self._event == "PreToolUse":
            # Devin documents updatedInput without a permissionDecision field;
            # emitting one it does not read would risk an unintended approve.
            return json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "updatedInput": tool_input,
                    }
                }
            )
        if (
            self._client in (Client.VSCODE, Client.CLAUDE_CODE)
            and self._event == "PreToolUse"
        ):
            return json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "allow",
                        "updatedInput": tool_input,
                    }
                }
            )
        if self._client == Client.GITHUB_COPILOT_CLI and self._event == "PreToolUse":
            return json.dumps(
                {
                    "permissionDecision": "allow",
                    "modifiedArgs": tool_input,
                }
            )
        if self._client == Client.GEMINI_CLI and self._event == "PreToolUse":
            # ``tool_input`` merges over the model's arguments. The
            # ``hookEventName`` discriminator carries Gemini's own event name,
            # not the normalized one.
            return json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "BeforeTool",
                        "tool_input": tool_input,
                    }
                }
            )
        if self._client == Client.CLINE_CLI and self._event == "PreToolUse":
            return _cline_control({"overrideInput": tool_input})
        return None

    def observational(self) -> str | None:
        """Output for non-blocking observational events."""
        if self._client == Client.CURSOR:
            return "{}"
        return None

    def block_output(
        self,
        reason: str,
        *,
        tool_name: str = "",
        original_output: object = None,
    ) -> str:
        """Return the cross-client output-blocking shape used by post hooks."""
        if self._client == Client.HERMES:
            return json.dumps(reason)
        if self._client == Client.VSCODE and self._event in _POST_TOOL_EVENTS:
            replacement = f"[Runlayer blocked this tool output] {reason}"
            return json.dumps(
                {
                    "decision": "block",
                    "reason": reason,
                    "modifiedResult": {
                        "resultType": "success",
                        "textResultForLlm": replacement,
                    },
                }
            )
        if self._client == Client.GITHUB_COPILOT_CLI and self._event == "PostToolUse":
            replacement = f"[Runlayer blocked this tool output] {reason}"
            return json.dumps(
                {
                    "modifiedResult": {
                        "resultType": "success",
                        "textResultForLlm": replacement,
                    },
                }
            )
        if (
            self._client == Client.GITHUB_COPILOT_CLI
            and self._event == "PostToolUseFailure"
        ):
            # Copilot CLI has no failed-result replacement/block field. This
            # context is informational only; never claim the raw error changed.
            return json.dumps(
                {
                    "additionalContext": (
                        "[Runlayer detected a policy violation, but GitHub "
                        "Copilot CLI cannot suppress the original error] "
                        f"{reason}"
                    )
                }
            )
        if self._client == Client.QWEN_CODE and self._event == "PostToolUse":
            return json.dumps({"continue": False, "reason": reason})
        if self._client == Client.CLINE_CLI:
            # Cline spawns every non-PreToolUse hook detached with stdout
            # discarded, so this can never take effect. Emit the only shape Cline
            # would parse so the behavior is correct if that ever changes; the
            # capability row reports post-tool output blocking as unsupported.
            return _cline_control({"cancel": True, "errorMessage": reason})
        if self._client == Client.GOOSE and self._event in _POST_TOOL_EVENTS:
            return json.dumps({"decision": "block", "reason": reason})
        if self._client == Client.CLAUDE_CODE and self._event == "PostToolUseFailure":
            return json.dumps(
                {
                    "additionalContext": (
                        "[Runlayer detected a policy violation, but Claude Code "
                        "cannot suppress the original error] "
                        f"{reason}"
                    )
                }
            )
        if self._client == Client.CLAUDE_CODE and self._event == "PostToolUse":
            # PostToolUse `decision: block` halts the turn but does NOT hide the
            # tool result the model already received. `updatedToolOutput` replaces
            # what the model sees, so emit both replacement and turn halt.
            response: dict[str, object] = {
                "decision": "block",
                "reason": reason,
            }
            updated_output = _claude_tool_output_replacement(
                f"[Runlayer blocked this tool output] {reason}",
                tool_name=tool_name,
                original_output=original_output,
            )
            if updated_output is not _UNREPLACEABLE_CLAUDE_OUTPUT:
                response["hookSpecificOutput"] = {
                    "hookEventName": self._event,
                    "updatedToolOutput": updated_output,
                }
            else:
                response["continue"] = False
                response["stopReason"] = reason
            return json.dumps(response)
        return json.dumps({"decision": "block", "reason": reason})

    def mask_output(
        self,
        masked: str,
        *,
        tool_name: str = "",
        original_output: object = None,
    ) -> str | None:
        """Non-blocking masked output: replace what the model sees with the
        sanitized result (PII redaction, hidden-ASCII strip). Returns ``None``
        for clients without a post-tool replacement schema."""
        if self._client == Client.HERMES and self._event == "PostToolUse":
            return json.dumps(masked)
        if self._client == Client.VSCODE and self._event in _POST_TOOL_EVENTS:
            return json.dumps(
                {
                    "modifiedResult": {
                        "resultType": "success",
                        "textResultForLlm": masked,
                    }
                }
            )
        if self._client == Client.GITHUB_COPILOT_CLI and self._event == "PostToolUse":
            return json.dumps(
                {
                    "modifiedResult": {
                        "resultType": "success",
                        "textResultForLlm": masked,
                    }
                }
            )
        if self._client == Client.CLAUDE_CODE and self._event == "PostToolUse":
            updated_output = _claude_tool_output_replacement(
                masked,
                tool_name=tool_name,
                original_output=original_output,
            )
            if updated_output is _UNREPLACEABLE_CLAUDE_OUTPUT:
                return None
            return json.dumps(
                {
                    "hookSpecificOutput": {
                        "hookEventName": self._event,
                        "updatedToolOutput": updated_output,
                    }
                }
            )
        return None
