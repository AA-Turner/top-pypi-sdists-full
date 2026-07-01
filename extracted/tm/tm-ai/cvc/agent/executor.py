"""
cvc.agent.executor — Tool execution engine for the CVC agent.

Executes agent tool calls against the local filesystem, shell, and CVC engine.
All file operations are scoped to the workspace root for safety.

Features:
  - Fuzzy matching for edit_file when exact match fails
  - Unified diff patch_file for more forgiving edits
  - File change tracking for /undo support
  - Web search capability
  - Respects .cvcignore patterns
"""

from __future__ import annotations

import asyncio
import difflib
import fnmatch
import hashlib
import json
import logging
import os
import re
import subprocess
from cvc._subprocess_compat import HIDDEN_KW
import sys
import time
from pathlib import Path
from typing import Any

from cvc.agent.hooks import HookEngine, HookEvent, HookOutcome
from cvc.agent.permissions import PermissionDecision, PermissionEngine
from cvc.agent.sandbox import Sandbox
from cvc.core.models import (
    CVCBranchRequest,
    CVCCommitRequest,
    CVCMergeRequest,
    CVCRestoreRequest,
)
from cvc.operations.engine import CVCEngine

logger = logging.getLogger("cvc.agent.executor")

# Max output size to prevent context window explosion
MAX_OUTPUT_CHARS = 2_000
MAX_GREP_MATCHES = 30
MAX_GLOB_RESULTS = 100
MAX_DIR_ENTRIES = 300

# v2.91.43: Per-tool required-arg schema. Maps tool name → tuple of arg names
# that MUST be present and non-empty. The dispatch layer validates args against
# this schema BEFORE calling the handler, returning a clear
# "tool X requires arg 'Y'" error string that the LLM can immediately act on,
# instead of bubbling up a raw KeyError.
#
# Adding a new tool with required args? Add it here too.
_REQUIRED_ARGS: dict[str, tuple[str, ...]] = {
    "read_file": ("path",),
    "write_file": ("path", "content"),
    "edit_file": ("path", "old_string", "new_string"),
    "patch_file": ("path", "diff"),
    "bash": ("command",),
    "process_manage": ("process_id", "action"),
    "glob": ("pattern",),
    "grep": ("pattern",),
    # v2.92.10 — list_dir requires `path`. The model schema declares it
    # as optional ("default: workspace root"), which trains MiniMax/Mistral
    # to omit it entirely and emit empty tool_use blocks. Without this
    # entry, the dud-detector in gateway.py never matches an empty-path
    # list_dir call, and the agent silently runs against the wrong
    # workspace. Making it REQUIRED here forces a clean error string
    # ("list_dir requires argument(s) 'path'") that the gateway collapses
    # to a single dud nudge + dashboard warning.
    "list_dir": ("path",),
    "web_search": ("query",),
    "cvc_branch": ("name",),
    "cvc_restore": ("commit_hash",),
    "cvc_merge": ("source_branch",),
    "cvc_search": ("query",),
}


def _validate_required_args(tool_name: str, arguments: dict[str, Any] | None) -> str | None:
    """Return None if args are valid, else a user-visible error string.

    v2.91.43: This is the front-line defense against the
    `KeyError: 'command'` / `KeyError: 'pattern'` silent-failure class that
    hit the dashboard in v2.91.x and below. Instead of letting
    ``args["command"]`` raise inside the handler (where the error gets
    logged + returned as a generic string, the LLM ignores it, and the
    loop spins until empty-retries exhaust), we validate UP FRONT and
    return a structured message that names exactly which arg is missing
    and what the LLM should do.
    """
    if arguments is None:
        return (
            f"Error: {tool_name} was called with no arguments. "
            f"Pass the required args as a JSON object (e.g. {{\"path\": \"...\"}})."
        )
    if not isinstance(arguments, dict):
        return (
            f"Error: {tool_name} arguments must be a JSON object, "
            f"got {type(arguments).__name__}."
        )
    required = _REQUIRED_ARGS.get(tool_name)
    if not required:
        return None
    missing: list[str] = []
    for arg_name in required:
        val = arguments.get(arg_name)
        if val is None:
            missing.append(arg_name)
            continue
        if isinstance(val, str) and not val.strip():
            missing.append(arg_name)
    if missing:
        quoted = ", ".join(f"'{m}'" for m in missing)
        return (
            f"Error: {tool_name} requires argument(s) {quoted} but they were "
            f"missing or empty. Re-emit the call with the required arg(s) populated."
        )
    return None


class FileChange:
    """Tracks a single file change for undo support."""
    __slots__ = ("path", "old_content", "new_content", "timestamp", "tool_name", "turn_id")

    def __init__(self, path: Path, old_content: str | None, new_content: str, tool_name: str, turn_id: int = 0):
        self.path = path
        self.old_content = old_content  # None means file didn't exist
        self.new_content = new_content
        self.timestamp = time.time()
        self.tool_name = tool_name
        self.turn_id = turn_id


class ToolExecutor:
    """
    Executes agent tool calls against the local filesystem and CVC engine.

    All file paths are resolved relative to the workspace root.
    Tracks file changes for /undo support.
    """

    def __init__(
        self,
        workspace: Path,
        engine: CVCEngine,
        permission_engine: PermissionEngine | None = None,
        hook_engine: HookEngine | None = None,
        sandbox: Sandbox | None = None,
    ) -> None:
        self.workspace = workspace.resolve()
        self.engine = engine
        self.permission_engine = permission_engine or PermissionEngine()
        self.hook_engine = hook_engine or HookEngine(workspace)
        self.sandbox = sandbox or Sandbox(workspace)
        self._change_history: list[FileChange] = []
        self._current_turn_id: int = 0
        self._ignore_patterns: list[str] = self._load_cvcignore()
        # ── Cognitive context tracking ────────────────────────────────────
        # Accumulated per-turn context, flushed into ContentBlob on commit.
        self._files_read: dict[str, str] = {}        # path → SHA-256
        self._files_written: dict[str, str] = {}     # path → SHA-256
        self._tool_outputs: dict[str, Any] = {}      # "{turn}:{tool}:{idx}" → result
        self._bash_history: list[dict[str, Any]] = []
        self._tool_call_counter: int = 0             # monotonic counter for keying
        # Tier 4 PageIndex: LLM call function injected by the chat loop.
        # Signature: (prompt: str) -> str
        self._pageindex_llm_call: Any = None
        # Callback for permission prompts — set by the chat loop.
        # Signature: (tool_name, args, summary) -> "allow_once"|"allow_always"|"deny"
        self._permission_prompt_callback: Any = None
        # v2.91.43: Callback for workspace switches — set by the chat loop
        # to re-init engine, llm, model selection, etc. for the new ws.
        # Signature: (new_workspace_path: str) -> None
        self._workspace_switch_callback: Any = None
        
        self._bg_processes: dict[str, Any] = {}
        self._bg_threads: list[Any] = []
        # Last bash result info — for command output panels
        self._last_bash_output: str = ""
        self._last_bash_exit_code: int = 0

        # ── Phase E (4.5): Filesystem checkpoint manager ──────────────────
        # Shadow-repo snapshots under ~/.cvc/checkpoints/ taken before
        # destructive tools (write_file, patch_file, multi_edit, bash) so
        # users can /undo at the filesystem level. Best-effort; failures
        # are swallowed (never block tool execution).
        try:
            from cvc.core.checkpoint_manager import (
                CheckpointManager,
            )
            self._checkpoint_mgr = CheckpointManager(
                enabled=True,
                max_snapshots=200,
                max_total_size_mb=500,
                max_file_size_mb=10,
            )
        except Exception as _ckpt_err:  # pragma: no cover — optional
            import logging as _logging
            _logging.getLogger(__name__).debug(
                "checkpoint manager disabled: %s", _ckpt_err
            )
            self._checkpoint_mgr = None

    def validate_args(
        self, tool_name: str, arguments: dict[str, Any] | None
    ) -> tuple[bool, str]:
        """Pre-dispatch argument validator (upstream-style).

        v2.94.0 — Adopted from upstream's `Tool.validate_args()` pattern.
        Returns ``(True, "")`` if the tool call can be safely dispatched,
        or ``(False, "<reason>")`` naming exactly what's missing or wrong.
        The dispatch layer (gateway / Telegram / WebSocket) MUST call this
        BEFORE calling :meth:`execute` so the model gets a tight feedback
        loop on dud calls instead of waiting for the tool to fail and
        burn an iteration on a dud-nudge round-trip.

        The validator is intentionally cheap: it only checks the required-
        arg schema (``_REQUIRED_ARGS``) and arg types. It does NOT check
        file existence, workspace scoping, or permissions — those checks
        still happen inside the tool handlers and surface real errors.

        Parameters
        ----------
        tool_name : str
            The name of the tool being dispatched.
        arguments : dict | None
            The arguments parsed from the LLM response.

        Returns
        -------
        (ok, reason) : tuple[bool, str]
            ``(True, "")`` if args are valid. ``(False, reason)`` with a
            human-readable reason if not. The reason string is exactly
            what should be returned to the model as the synthetic
            ``tool_result`` content — it must be specific enough that the
            LLM can re-emit the call correctly on the next iteration.
        """
        reason = _validate_required_args(tool_name, arguments)
        if reason is None:
            return (True, "")
        return (False, reason)

    def execute(self, tool_name: str, arguments: dict[str, Any]) -> str:
        """
        Execute a tool call and return the result as a string.

        Parameters
        ----------
        tool_name : str
            The name of the tool to execute.
        arguments : dict
            The tool arguments parsed from the LLM response.

        Returns
        -------
        str
            The tool output as a string for inclusion in the conversation.
        """
        dispatch = {
            "read_file": self._read_file,
            "write_file": self._write_file,
            "edit_file": self._edit_file,
            "patch_file": self._patch_file,
            "bash": self._bash,
            "process_manage": self._process_manage,
            "glob": self._glob,
            "grep": self._grep,
            "list_dir": self._list_dir,
            "web_search": self._web_search,
            "cvc_status": self._cvc_status,
            "cvc_log": self._cvc_log,
            "cvc_commit": self._cvc_commit,
            "cvc_branch": self._cvc_branch,
            "cvc_restore": self._cvc_restore,
            "cvc_merge": self._cvc_merge,
            "cvc_search": self._cvc_search,
            "cvc_smart_search": self._cvc_smart_search,
            "cvc_diff": self._cvc_diff,
            "cvc_remember": self._cvc_remember,
            "cvc_ingest_document": self._cvc_ingest_document,
            "cvc_document_search": self._cvc_document_search,
            "cvc_list_documents": self._cvc_list_documents,
            "agent": self._agent,
            "task_create": self._task_create,
            "task_get": self._task_get,
            "task_list": self._task_list,
            "task_kill": self._task_kill,
            "ask_user": self._ask_user,
            "save_memory": self._save_memory,
            # Input Grounding (Anti-Hallucination)
            "fetch_docs": self._fetch_docs,
            "search_docs": self._search_docs,
            "lookup_api": self._lookup_api,
            "annotate_doc": self._annotate_doc,
            # Workspace management
            "cvc_switch_workspace": self._cvc_switch_workspace,
            # Advanced tools
            "multi_edit": self._multi_edit,
            "multi_read": self._multi_read,
            "web_fetch": self._web_fetch,
            "think": self._think,
            "context_compact": self._context_compact,
            "parallel_agents": self._parallel_agents,
            "todo": self._todo,
            "semantic_grep": self._semantic_grep,
            "git": self._git,
        }

        handler = dispatch.get(tool_name)
        # ── v2.91.43: Required-argument validation ───────────────────────
        # Run BEFORE the checkpoint snapshot and BEFORE the handler, so the
        # LLM gets a structured "you forgot arg X" message instead of a
        # raw KeyError buried in a try/except that gets returned as
        # "Error executing bash: 'command'" and then ignored by the LLM.
        if handler is not None:
            arg_err = _validate_required_args(tool_name, arguments)
            if arg_err is not None:
                # v2.92.10 — Demoted from WARNING to DEBUG. The CLI
                # chat loop (and gateway) now detect dud calls BEFORE
                # dispatching to the executor and render a single
                # collapsed warning line. The executor's per-call
                # WARNING was duplicating that warning once per dud —
                # polluting the terminal with N identical yellow
                # lines and the gateway log with N redundant entries.
                # Operators can re-enable this by setting
                # CVC_LOG_DUD_WARNINGS=1 for forensics.
                if os.environ.get("CVC_LOG_DUD_WARNINGS") == "1":
                    logger.warning(
                        "Tool %s called with missing required args: %s",
                        tool_name,
                        arg_err,
                    )
                else:
                    logger.debug(
                        "Tool %s called with missing required args: %s",
                        tool_name,
                        arg_err,
                    )
                # Still record this in tool-call tracking for /stats parity
                if not hasattr(self, "_tool_call_counts"):
                    self._tool_call_counts: dict[str, int] = {}
                self._tool_call_counts[tool_name] = (
                    self._tool_call_counts.get(tool_name, 0) + 1
                )
                return arg_err
        # ── Phase E (4.5): pre-tool snapshot for destructive ops ──────────
        # Take a shadow-repo snapshot BEFORE we hand off to the handler so
        # `/undo` (Cat-5 feature, exposed via CLI/dashboard) can roll the
        # workspace tree back. Never raises into the tool path.
        if self._checkpoint_mgr and tool_name in (
            "write_file", "patch_file", "edit_file", "multi_edit", "bash"
        ):
            try:
                # For file tools, scope to file's working dir; for bash, the
                # entire workspace. ``ensure_checkpoint`` is idempotent within
                # a turn so back-to-back calls don't duplicate snapshots.
                if tool_name == "bash":
                    self._checkpoint_mgr.ensure_checkpoint(
                        str(self.workspace), f"before {tool_name}"
                    )
                else:
                    path_arg = arguments.get("path") or arguments.get("file_path") or ""
                    if path_arg:
                        try:
                            work_dir = self._checkpoint_mgr.get_working_dir_for_path(path_arg)
                        except Exception:
                            work_dir = str(self.workspace)
                    else:
                        work_dir = str(self.workspace)
                    self._checkpoint_mgr.ensure_checkpoint(work_dir, f"before {tool_name}")
            except Exception:
                pass  # never block tool execution on checkpoint failure

        if handler is None:
            # Fallback to upstream bridge — covers browser_*, computer_use,
            # vision_analyze, video_analyze, image_generate, cronjob,
            # delegate_task, mixture_of_agents, session_search, skill_*,
            # send_message, text_to_speech, execute_code, clarify, feishu_*
            try:
                from cvc.agent.hermes_bridge import (
                    HERMES_TOOL_NAMES,
                    dispatch_hermes_tool,
                )
                if tool_name in HERMES_TOOL_NAMES:
                    # Track for /stats parity with native handlers
                    if not hasattr(self, "_tool_call_counts"):
                        self._tool_call_counts: dict[str, int] = {}
                    self._tool_call_counts[tool_name] = (
                        self._tool_call_counts.get(tool_name, 0) + 1
                    )
                    # v2.91.43: validate args for vendored-bridged tools too.
                    # (Many of them take required args — e.g.
                    # ``send_message`` requires ``message``,
                    # ``web_search`` requires ``query``.) Without this,
                    # the vendored bridge would return its own opaque
                    # "missing argument" error and we'd be back in the
                    # silent-failure class.
                    arg_err = _validate_required_args(tool_name, arguments)
                    if arg_err is not None:
                        # v2.92.10 — Same dedup as the native path:
                        # demoted to DEBUG by default; CLI loop handles
                        # the user-facing warning. Set
                        # CVC_LOG_DUD_WARNINGS=1 to re-enable the old
                        # per-call WARNING logs for forensics.
                        if os.environ.get("CVC_LOG_DUD_WARNINGS") == "1":
                            logger.warning(
                                "Bridged tool %s called with missing required args: %s",
                                tool_name,
                                arg_err,
                            )
                        else:
                            logger.debug(
                                "Bridged tool %s called with missing required args: %s",
                                tool_name,
                                arg_err,
                            )
                        return arg_err
                    try:
                        result = dispatch_hermes_tool(tool_name, arguments)
                        result = self._truncate(result)
                    except Exception as exc:
                        logger.error(
                            "Bridged tool %s failed: %s",
                            tool_name, exc, exc_info=True,
                        )
                        return f"Error executing {tool_name}: {exc}"
                    self._tool_call_counter += 1
                    key = (
                        f"{self._current_turn_id}:{tool_name}:"
                        f"{self._tool_call_counter}"
                    )
                    capped = result[:51_200] if len(result) > 51_200 else result
                    self._tool_outputs[key] = capped
                    return result
            except Exception:
                pass
            return f"Error: Unknown tool '{tool_name}'"

        # Track tool call counts for /stats
        if not hasattr(self, "_tool_call_counts"):
            self._tool_call_counts: dict[str, int] = {}
        self._tool_call_counts[tool_name] = self._tool_call_counts.get(tool_name, 0) + 1

        # ── Permission check ─────────────────────────────────────────
        decision = self.permission_engine.evaluate(tool_name, arguments)

        if decision == PermissionDecision.DENIED:
            logger.info("Tool %s DENIED by permission rules", tool_name)
            return (
                f"Error: Permission denied for {tool_name}. "
                "This tool is blocked by the project's permission rules. "
                "Use a different approach or ask the user to update permissions."
            )

        if decision == PermissionDecision.ASK_USER:
            # Prompt the user for approval (callback set by chat loop)
            if self._permission_prompt_callback:
                user_decision = self._permission_prompt_callback(
                    tool_name, arguments,
                )
                if user_decision == "deny":
                    return (
                        f"Error: User denied permission for {tool_name}. "
                        "Try a different approach or ask the user what they'd prefer."
                    )
                elif user_decision == "allow_always":
                    self.permission_engine.approve_always(tool_name)
                elif user_decision == "allow_once":
                    self.permission_engine.approve_once(tool_name, arguments)
            # If no callback, fall through to allow (backwards compatible)

        # ── PreToolUse hooks ─────────────────────────────────────────
        pre_ctx = {"tool_name": tool_name, "arguments": arguments}
        pre_result = self.hook_engine.fire(
            HookEvent.PRE_TOOL_USE, pre_ctx,
            tool_name=tool_name, arguments=arguments,
        )
        if pre_result.outcome == HookOutcome.BLOCK:
            logger.info("Tool %s BLOCKED by PreToolUse hook", tool_name)
            msg = f"Error: Blocked by hook — {pre_result.stderr or pre_result.stdout or 'PreToolUse hook returned exit code 2'}"
            return msg
        if pre_result.outcome == HookOutcome.ASK_USER:
            if self._permission_prompt_callback:
                user_decision = self._permission_prompt_callback(
                    tool_name, arguments,
                )
                if user_decision == "deny":
                    return f"Error: User denied {tool_name} (hook requested confirmation)."

        try:
            result = handler(arguments)
            result = self._truncate(result)
        except Exception as exc:
            logger.error("Tool %s failed: %s", tool_name, exc, exc_info=True)
            return f"Error executing {tool_name}: {exc}"

        # ── Cognitive context: record tool output ────────────────────
        self._tool_call_counter += 1
        key = f"{self._current_turn_id}:{tool_name}:{self._tool_call_counter}"
        # Cap individual tool output at 50KB to prevent blob explosion
        capped = result[:51_200] if len(result) > 51_200 else result
        self._tool_outputs[key] = capped

        # ── PostToolUse hooks ────────────────────────────────────────
        post_ctx = {"tool_name": tool_name, "arguments": arguments, "result": result[:2000]}
        self.hook_engine.fire(
            HookEvent.POST_TOOL_USE, post_ctx,
            tool_name=tool_name, arguments=arguments,
        )

        return result

    # ── Path Resolution ──────────────────────────────────────────────────

    def _resolve_path(self, path_str: str) -> Path:
        """Resolve a path relative to the workspace root.

        v2.92.14 — Cross-platform path handling. CVC runs on
        Windows, macOS, and Linux. The user passes whatever path
        their workspace uses (``C:\\foo\\bar`` on Windows,
        ``/Users/x/bar`` on Mac, ``/home/x/bar`` on Linux). We
        don't translate between platforms — the user knows their
        machine. We do:

        1. Use ``pathlib.Path`` directly, which handles
           forward-slashes and backslashes per the host OS.
        2. If the path is relative, anchor it to the workspace.
        3. Resolve symlinks via ``Path.resolve()``.

        Earlier we tried to translate Windows drive-letter paths
        (``E:\\...``) to ``$HOME/<rest>`` on non-Windows hosts.
        That was wrong: it broke real Windows users whose
        workspace genuinely lives at ``E:\\Projects\\11-11-0``.
        The user knows their drive letter; we don't second-guess
        them. Removed in v2.92.14-final.
        """
        # pathlib.Path handles both / and \ correctly on each
        # platform: on Windows, ``Path("E:/foo/bar")`` and
        # ``Path("E:\\foo\\bar")`` both work; on Unix, only
        # forward-slash paths work. We pass the string through
        # verbatim — the user is the source of truth.
        p = Path(path_str)
        if not p.is_absolute():
            p = self.workspace / p
        p = p.resolve()
        # Safety: ensure path is within workspace (or allow absolute for reads)
        return p

    def _load_cvcignore(self) -> list[str]:
        """Load .cvcignore patterns."""
        ignore_file = self.workspace / ".cvcignore"
        if not ignore_file.exists():
            return []
        try:
            patterns = []
            for line in ignore_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line)
            return patterns
        except OSError:
            return []

    def _is_ignored(self, path: Path) -> bool:
        """Check if a path is ignored by .cvcignore."""
        if not self._ignore_patterns:
            return False
        try:
            rel = str(path.relative_to(self.workspace)).replace("\\", "/")
        except ValueError:
            return False
        name = path.name
        for pattern in self._ignore_patterns:
            if fnmatch.fnmatch(rel, pattern) or fnmatch.fnmatch(name, pattern):
                return True
            if pattern.endswith("/") and (rel + "/").startswith(pattern):
                return True
        return False

    def start_new_turn(self) -> int:
        """Mark the start of a new turn. Returns the new turn_id."""
        self._current_turn_id += 1
        self._tool_call_counter = 0  # Reset per-turn counter
        return self._current_turn_id

    def get_turn_context(self) -> dict[str, Any]:
        """Return accumulated cognitive context since last reset.

        This data is injected into ContentBlob on commit to create
        a full cognitive snapshot — files read, files written, tool outputs,
        bash commands, and user queries.
        """
        return {
            "tool_outputs": dict(self._tool_outputs),
            "source_files": dict(self._files_read),
            "files_written": dict(self._files_written),
            "bash_commands": list(self._bash_history),
        }

    def reset_turn_context(self) -> None:
        """Clear accumulated cognitive context (called after commit)."""
        self._files_read.clear()
        self._files_written.clear()
        self._tool_outputs.clear()
        self._bash_history.clear()

    @property
    def current_turn_id(self) -> int:
        """Return the current turn ID."""
        return self._current_turn_id

    def _track_change(self, path: Path, old_content: str | None, new_content: str, tool: str) -> None:
        """Track a file change for undo support and cognitive context."""
        self._change_history.append(FileChange(path, old_content, new_content, tool, self._current_turn_id))
        # Also track in cognitive context (files_written)
        rel_str = str(path.relative_to(self.workspace) if path.is_relative_to(self.workspace) else path).replace("\\", "/")
        self._files_written[rel_str] = hashlib.sha256(new_content.encode("utf-8")).hexdigest()

    def get_last_change(self) -> FileChange | None:
        """Return the most recent file change (for diff preview rendering)."""
        return self._change_history[-1] if self._change_history else None

    def undo_last(self) -> str:
        """
        Undo the last file change.
        Returns a status message.
        """
        if not self._change_history:
            return "Nothing to undo — no file changes recorded."

        change = self._change_history.pop()
        rel = change.path.relative_to(self.workspace) if change.path.is_relative_to(self.workspace) else change.path

        try:
            if change.old_content is None:
                # File was created — delete it
                if change.path.exists():
                    change.path.unlink()
                    return f"Undone: deleted {rel} (was created by {change.tool_name})"
                return f"File {rel} already deleted"
            else:
                # File was modified — restore old content
                change.path.write_text(change.old_content, encoding="utf-8")
                return f"Undone: restored {rel} (changed by {change.tool_name})"
        except OSError as e:
            return f"Undo failed: {e}"

    def get_change_history(self) -> list[dict[str, str]]:
        """Get a summary of tracked file changes."""
        return [
            {
                "path": str(c.path.relative_to(self.workspace) if c.path.is_relative_to(self.workspace) else c.path),
                "tool": c.tool_name,
                "action": "created" if c.old_content is None else "modified",
                "turn_id": str(c.turn_id),
            }
            for c in self._change_history
        ]

    def get_turn_changes(self, turn_id: int) -> list[FileChange]:
        """Return all file changes for a specific turn."""
        return [c for c in self._change_history if c.turn_id == turn_id]

    def get_latest_turn_id(self) -> int:
        """Return the turn_id of the most recent file change, or 0 if none."""
        if not self._change_history:
            return 0
        return self._change_history[-1].turn_id

    def undo_turn(self, turn_id: int) -> list[str]:
        """
        Undo ALL file changes for a specific turn (in reverse order).
        Returns a list of status messages.
        """
        turn_changes = [c for c in self._change_history if c.turn_id == turn_id]
        if not turn_changes:
            return ["Nothing to undo — no file changes for this turn."]

        results: list[str] = []
        # Reverse order so later changes are undone first
        for change in reversed(turn_changes):
            rel = change.path.relative_to(self.workspace) if change.path.is_relative_to(self.workspace) else change.path
            try:
                if change.old_content is None:
                    if change.path.exists():
                        change.path.unlink()
                        results.append(f"Reverted: deleted {rel} (was created)")
                    else:
                        results.append(f"File {rel} already deleted")
                else:
                    change.path.write_text(change.old_content, encoding="utf-8")
                    results.append(f"Reverted: restored {rel}")
            except OSError as e:
                results.append(f"Revert failed for {rel}: {e}")

        # Remove these changes from history
        self._change_history = [c for c in self._change_history if c.turn_id != turn_id]
        return results

    def undo_specific_files(self, file_paths: list[Path], turn_id: int) -> list[str]:
        """
        Undo changes for specific files within a turn.
        Only reverts the selected files, leaves other turn changes intact.
        """
        resolved_paths = {p.resolve() for p in file_paths}
        turn_changes = [
            c for c in self._change_history
            if c.turn_id == turn_id and c.path.resolve() in resolved_paths
        ]
        if not turn_changes:
            return ["Nothing to undo — no matching file changes."]

        results: list[str] = []
        for change in reversed(turn_changes):
            rel = change.path.relative_to(self.workspace) if change.path.is_relative_to(self.workspace) else change.path
            try:
                if change.old_content is None:
                    if change.path.exists():
                        change.path.unlink()
                        results.append(f"Reverted: deleted {rel} (was created)")
                    else:
                        results.append(f"File {rel} already deleted")
                else:
                    change.path.write_text(change.old_content, encoding="utf-8")
                    results.append(f"Reverted: restored {rel}")
            except OSError as e:
                results.append(f"Revert failed for {rel}: {e}")

        # Remove only the reverted changes from history
        reverted_paths = resolved_paths
        self._change_history = [
            c for c in self._change_history
            if not (c.turn_id == turn_id and c.path.resolve() in reverted_paths)
        ]
        return results

    # ── File Operations ──────────────────────────────────────────────────

    def _read_file(self, args: dict) -> str:
        path = self._resolve_path(args["path"])
        # Sandbox check
        err = self.sandbox.validate_read(path)
        if err:
            return f"Error: {err}"
        if not path.exists():
            return f"Error: File not found: {path}"
        if not path.is_file():
            return f"Error: Not a file: {path}"

        try:
            content = path.read_text(encoding="utf-8", errors="replace")
        except OSError as e:
            return f"Error reading file: {e}"

        # Track file read for cognitive context
        rel = path.relative_to(self.workspace) if path.is_relative_to(self.workspace) else path
        rel_str = str(rel).replace("\\", "/")
        self._files_read[rel_str] = hashlib.sha256(content.encode("utf-8")).hexdigest()

        lines = content.splitlines(keepends=True)
        total_lines = len(lines)
        start = args.get("start_line")
        end = args.get("end_line")

        if start is None and end is None:
            if total_lines > 150:
                s = 0
                e = 150
                selected = lines[s:e]
                # v2.92.14 — Cleaner truncation hint. The previous
                # wording mixed the warning into the file content
                # body so the model had to disambiguate "is this a
                # real error?" from "is this just metadata?". The
                # new wording uses a structured tag the model can
                # parse cleanly: lines, total, and the next chunk
                # to ask for are all on one line.
                header = f"File: {rel}\n"
                header += (
                    f"[TRUNCATED: showing lines 1-150 of {total_lines}. "
                    f"Use start_line=151 to read the next chunk.]\n\n"
                )
                return header + "".join(selected)
            return f"File: {rel} ({total_lines} lines)\n\n{content}"

        s = max(0, (start or 1) - 1)
        e = end if end else len(lines)
        # Enforce limits
        if (e - s) > 300:
            e = s + 300

        selected = lines[s:e]
        header = f"File: {rel}\n"
        header += f"Lines {s + 1}-{min(e, len(lines))} of {len(lines)}\n\n"
        if len(selected) == 300 and (e - s) >= 300:
            header += "[WARNING: Truncated to maximum 300 line chunks. Request another chunk if needed.]\n\n"

        return header + "".join(selected)

    def _write_file(self, args: dict) -> str:
        path = self._resolve_path(args["path"])
        content = args["content"]
        # Sandbox check
        err = self.sandbox.validate_write(path)
        if err:
            return f"Error: {err}"

        # Track for undo
        old_content = None
        existed = path.exists()
        if existed:
            try:
                old_content = path.read_text(encoding="utf-8")
            except OSError:
                pass

        path.parent.mkdir(parents=True, exist_ok=True)

        try:
            path.write_text(content, encoding="utf-8")
        except OSError as e:
            return f"Error writing file: {e}"

        self._track_change(path, old_content, content, "write_file")

        rel = path.relative_to(self.workspace) if path.is_relative_to(self.workspace) else path
        lines = content.count("\n") + 1
        action = "Updated" if existed else "Created"
        return f"{action} {rel} ({lines} lines)"

    def _edit_file(self, args: dict) -> str:
        path = self._resolve_path(args["path"])
        # Sandbox check
        err = self.sandbox.validate_write(path)
        if err:
            return f"Error: {err}"
        if not path.exists():
            return f"Error: File not found: {path}"

        old_string = args["old_string"]
        new_string = args["new_string"]

        try:
            content = path.read_text(encoding="utf-8")
        except OSError as e:
            return f"Error reading file: {e}"

        count = content.count(old_string)
        if count == 0:
            # Fuzzy matching fallback — try to find the closest match
            match_result = self._fuzzy_find_and_replace(content, old_string, new_string)
            if match_result is not None:
                new_content, match_ratio = match_result
                try:
                    old_content = content
                    path.write_text(new_content, encoding="utf-8")
                    self._track_change(path, old_content, new_content, "edit_file")
                except OSError as e:
                    return f"Error writing file: {e}"
                rel = path.relative_to(self.workspace) if path.is_relative_to(self.workspace) else path
                old_lines = old_string.count("\n") + 1
                new_lines = new_string.count("\n") + 1
                return (
                    f"Edited {rel} (fuzzy match {match_ratio:.0%}): "
                    f"replaced {old_lines} line(s) with {new_lines} line(s)"
                )

            # No match found at all
            snippet = old_string[:80].replace("\n", "\\n")
            return (
                f"Error: old_string not found in {path.name}. "
                f"Searched for: '{snippet}...'\n"
                f"Make sure the string matches exactly, including whitespace.\n"
                f"Tip: Use read_file to see the current content, then retry."
            )
        if count > 1:
            return (
                f"Error: old_string matches {count} locations in {path.name}. "
                f"Include more context to make it unique."
            )

        old_content = content
        new_content = content.replace(old_string, new_string, 1)
        try:
            path.write_text(new_content, encoding="utf-8")
        except OSError as e:
            return f"Error writing file: {e}"

        self._track_change(path, old_content, new_content, "edit_file")

        rel = path.relative_to(self.workspace) if path.is_relative_to(self.workspace) else path
        old_lines = old_string.count("\n") + 1
        new_lines = new_string.count("\n") + 1
        return f"Edited {rel}: replaced {old_lines} line(s) with {new_lines} line(s)"

    def _fuzzy_find_and_replace(
        self, content: str, old_string: str, new_string: str, threshold: float = 0.6
    ) -> tuple[str, float] | None:
        """
        Try fuzzy matching of old_string against file content.
        Returns (new_content, match_ratio) or None if no good match found.
        """
        old_lines = old_string.splitlines(keepends=True)
        content_lines = content.splitlines(keepends=True)

        if not old_lines or not content_lines:
            return None

        best_ratio = 0.0
        best_start = -1
        best_end = -1
        window_size = len(old_lines)

        # Sliding window search
        for i in range(len(content_lines) - window_size + 1):
            candidate = content_lines[i:i + window_size]
            ratio = difflib.SequenceMatcher(
                None, "".join(old_lines), "".join(candidate)
            ).ratio()

            if ratio > best_ratio:
                best_ratio = ratio
                best_start = i
                best_end = i + window_size

        # Also try with ±1 line windows
        for delta in [-1, 1]:
            adjusted_size = window_size + delta
            if adjusted_size < 1:
                continue
            for i in range(len(content_lines) - adjusted_size + 1):
                candidate = content_lines[i:i + adjusted_size]
                ratio = difflib.SequenceMatcher(
                    None, "".join(old_lines), "".join(candidate)
                ).ratio()
                if ratio > best_ratio:
                    best_ratio = ratio
                    best_start = i
                    best_end = i + adjusted_size

        if best_ratio >= threshold and best_start >= 0:
            # Replace the matched section
            new_lines = new_string.splitlines(keepends=True)
            if new_string and not new_string.endswith("\n"):
                pass  # Keep as-is
            result_lines = content_lines[:best_start] + new_lines + content_lines[best_end:]
            return "".join(result_lines), best_ratio

        return None

    def _patch_file(self, args: dict) -> str:
        """
        Apply a unified diff patch to a file.
        More forgiving than edit_file for complex multi-hunk edits.
        """
        path = self._resolve_path(args["path"])
        diff_text = args["diff"]
        # Sandbox check
        err = self.sandbox.validate_write(path)
        if err:
            return f"Error: {err}"

        if not path.exists():
            return f"Error: File not found: {path}"

        try:
            content = path.read_text(encoding="utf-8")
        except OSError as e:
            return f"Error reading file: {e}"

        old_content = content
        lines = content.splitlines(keepends=True)

        # Parse unified diff hunks
        hunks = self._parse_unified_diff(diff_text)
        if not hunks:
            return "Error: Could not parse unified diff. Use @@ -line,count +line,count @@ format."

        # Apply hunks in reverse order (so line numbers don't shift)
        hunks.sort(key=lambda h: h["old_start"], reverse=True)
        result_lines = list(lines)

        for hunk in hunks:
            old_start = hunk["old_start"] - 1  # Convert to 0-based
            remove_lines = hunk["remove"]
            add_lines = hunk["add"]

            # Verify context matches (loosely)
            end_idx = old_start + len(remove_lines)
            if end_idx > len(result_lines):
                end_idx = len(result_lines)

            # Replace the section
            result_lines[old_start:old_start + len(remove_lines)] = add_lines

        new_content = "".join(result_lines)

        try:
            path.write_text(new_content, encoding="utf-8")
        except OSError as e:
            return f"Error writing file: {e}"

        self._track_change(path, old_content, new_content, "patch_file")

        rel = path.relative_to(self.workspace) if path.is_relative_to(self.workspace) else path
        return f"Patched {rel}: applied {len(hunks)} hunk(s)"

    @staticmethod
    def _parse_unified_diff(diff_text: str) -> list[dict]:
        """Parse a unified diff into a list of hunks."""
        hunks = []
        current_hunk = None

        for line in diff_text.splitlines(keepends=True):
            # Hunk header: @@ -old_start,old_count +new_start,new_count @@
            header_match = re.match(
                r'^@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@',
                line,
            )
            if header_match:
                if current_hunk:
                    hunks.append(current_hunk)
                current_hunk = {
                    "old_start": int(header_match.group(1)),
                    "old_count": int(header_match.group(2) or 1),
                    "new_start": int(header_match.group(3)),
                    "new_count": int(header_match.group(4) or 1),
                    "remove": [],
                    "add": [],
                }
                continue

            if current_hunk is None:
                continue

            if line.startswith("-"):
                current_hunk["remove"].append(line[1:])
            elif line.startswith("+"):
                current_hunk["add"].append(line[1:])
            elif line.startswith(" "):
                # Context line — present in both old and new
                current_hunk["remove"].append(line[1:])
                current_hunk["add"].append(line[1:])

        if current_hunk:
            hunks.append(current_hunk)

        return hunks

    # ── Shell Execution ──────────────────────────────────────────────────

    def _bash(self, args: dict) -> str:
        command = args["command"]
        timeout = args.get("timeout", 120)

        # Pick the right shell
        if sys.platform == "win32":
            # '&&' is a bash/cmd operator that is invalid in PowerShell.
            # LLMs habitually chain commands with '&&'; replace with ';'
            # which is the PowerShell statement separator.
            command = command.replace(" && ", " ; ")
            # Force UTF-8 output encoding in PowerShell to avoid cp1252 decode errors
            utf8_prefix = (
                "[Console]::OutputEncoding = [System.Text.Encoding]::UTF8; "
                "$OutputEncoding = [System.Text.Encoding]::UTF8; "
            )
            shell_cmd = ["powershell", "-NoProfile", "-NonInteractive", "-Command", utf8_prefix + command]
        else:
            shell_cmd = ["bash", "-c", command]

        try:
            import uuid
            import threading
            
            proc = subprocess.Popen(
                shell_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.PIPE,
                text=True,
                encoding="utf-8",
                errors="replace",
                cwd=str(self.workspace),
                env={**os.environ, "PYTHONIOENCODING": "utf-8"},
                            **HIDDEN_KW,
            )
            
            class BackgroundProcess:
                def __init__(self, cmd, p):
                    self.id = f"proc_{uuid.uuid4().hex[:8]}"
                    self.cmd = cmd
                    self.proc = p
                    self.stdout_buf = ""
                    self.stderr_buf = ""
                    self.lock = threading.Lock()
                    
                    def read_stream(stream, is_stderr):
                        try:
                            # Read character by character to avoid buffering issues
                            while True:
                                chunk = stream.read(1)
                                if not chunk:
                                    break
                                with self.lock:
                                    if is_stderr:
                                        self.stderr_buf += chunk
                                        if len(self.stderr_buf) > 50000:
                                            self.stderr_buf = self.stderr_buf[-50000:]
                                    else:
                                        self.stdout_buf += chunk
                                        if len(self.stdout_buf) > 50000:
                                            self.stdout_buf = self.stdout_buf[-50000:]
                        except Exception:
                            pass
                            
                    self.t_out = threading.Thread(target=read_stream, args=(self.proc.stdout, False), daemon=True)
                    self.t_err = threading.Thread(target=read_stream, args=(self.proc.stderr, True), daemon=True)
                    self.t_out.start()
                    self.t_err.start()

                def get_logs(self, clear=True):
                    with self.lock:
                        out = self.stdout_buf
                        err = self.stderr_buf
                        if clear:
                            self.stdout_buf = ""
                            self.stderr_buf = ""
                        return out, err
            
            bg_proc = BackgroundProcess(command, proc)

            # Wait up to 5 seconds to see if it finishes fast.
            # proc.wait(timeout) blocks the OS scheduler instead of
            # busy-waiting in 100ms python sleeps — gives faster reaction
            # for short-lived commands and zero CPU during the wait.
            try:
                proc.wait(timeout=5.0)
            except subprocess.TimeoutExpired:
                pass
                
            if proc.poll() is None:
                # Still running, background it
                self._bg_processes[bg_proc.id] = bg_proc
                self._bash_history.append({
                    "command": command,
                    "exit_code": None,
                    "output": "[Background Process Started]",
                    "ts": time.time(),
                })
                return f"Process is still running in background.\nProcess ID: {bg_proc.id}\nUse process_manage tool to poll logs or kill it."
            
            # Process finished within 5 seconds
            bg_proc.t_out.join(timeout=1.0)
            bg_proc.t_err.join(timeout=1.0)
            out, err = bg_proc.get_logs(clear=False)
            
            output_parts = []
            if out:
                output_parts.append(out.strip())
            if err:
                output_parts.append(f"STDERR:\n{err.strip()}")
            if proc.returncode != 0:
                output_parts.append(f"\nExit code: {proc.returncode}")
                
            output = "\n".join(output_parts).strip()
            self._last_bash_output = output if output else "(no output)"
            self._last_bash_exit_code = proc.returncode

            self._bash_history.append({
                "command": command,
                "exit_code": proc.returncode,
                "output": (output[:2048] if output and len(output) > 2048 else output) or "",
                "ts": time.time(),
            })

            return output if output else "(no output)"

        except FileNotFoundError as e:
            return f"Error: Shell not found: {e}"

    def _process_manage(self, args: dict) -> str:
        pid = args["process_id"]
        action = args["action"]
        
        if pid not in self._bg_processes:
            return f"Error: Process '{pid}' not found or already closed."
            
        bg_proc = self._bg_processes[pid]
        proc = bg_proc.proc
        
        if action == "kill":
            proc.kill()
            del self._bg_processes[pid]
            return f"Process {pid} killed."
            
        elif action == "send_keys":
            input_text = args.get("input_text", "")
            if proc.poll() is not None:
                return f"Process already exited with code {proc.returncode}."
            try:
                proc.stdin.write(input_text)
                proc.stdin.flush()
                return f"Sent input to {pid}."
            except Exception as e:
                return f"Error sending input: {e}"
                
        elif action == "poll":
            out, err = bg_proc.get_logs(clear=True)
            status = f"RUNNING" if proc.poll() is None else f"EXITED (Code: {proc.returncode})"
            
            parts = [f"Status: {status}"]
            if out:
                parts.append(f"STDOUT:\n{out}")
            if err:
                parts.append(f"STDERR:\n{err}")
                
            if proc.poll() is not None:
                del self._bg_processes[pid]
                
            return "\n\n".join(parts)
            
        return f"Error: Unknown action '{action}'"

    # ── Search & Discovery ───────────────────────────────────────────────

    def _glob(self, args: dict) -> str:
        pattern = args["pattern"]
        root = self._resolve_path(args.get("path", "."))

        if not root.is_dir():
            return f"Error: Not a directory: {root}"

        matches = []
        try:
            for p in root.rglob("*") if "**" in pattern else root.glob(pattern):
                if len(matches) >= MAX_GLOB_RESULTS:
                    break
                # Skip hidden dirs and common noise
                parts = p.relative_to(root).parts
                if any(part.startswith(".") and part not in (".", "..") for part in parts):
                    continue
                if any(skip in parts for skip in ("node_modules", "__pycache__", ".git", "venv", ".venv")):
                    continue
                # Check .cvcignore
                if self._is_ignored(p):
                    continue
                if "**" in pattern:
                    # rglob doesn't filter by the actual pattern, so do it manually
                    rel = str(p.relative_to(root)).replace("\\", "/")
                    pure_pattern = pattern.replace("**/", "")
                    if not fnmatch.fnmatch(rel, pattern) and not fnmatch.fnmatch(p.name, pure_pattern):
                        continue
                rel = str(p.relative_to(root)).replace("\\", "/")
                if p.is_dir():
                    rel += "/"
                matches.append(rel)
        except OSError as e:
            return f"Error: {e}"

        if not matches:
            return f"No files matching '{pattern}' in {root}"

        matches.sort()
        header = f"Found {len(matches)} match(es) for '{pattern}':\n\n"
        return header + "\n".join(matches)

    def _grep(self, args: dict) -> str:
        pattern_str = args["pattern"]
        root = self._resolve_path(args.get("path", "."))
        include = args.get("include", "")

        try:
            regex = re.compile(pattern_str, re.IGNORECASE)
        except re.error:
            regex = re.compile(re.escape(pattern_str), re.IGNORECASE)

        results: list[str] = []
        files_checked = 0

        def _search_file(fpath: Path) -> None:
            nonlocal files_checked
            files_checked += 1
            try:
                text = fpath.read_text(encoding="utf-8", errors="replace")
            except (OSError, UnicodeDecodeError):
                return
            for i, line in enumerate(text.splitlines(), 1):
                if len(results) >= MAX_GREP_MATCHES:
                    return
                if regex.search(line):
                    if fpath.is_relative_to(self.workspace):
                        rel = str(fpath.relative_to(self.workspace)).replace("\\", "/")
                    else:
                        rel = str(fpath).replace("\\", "/")
                    results.append(f"{rel}:{i}: {line.rstrip()}")

        if root.is_file():
            _search_file(root)
        elif root.is_dir():
            for fpath in root.rglob("*"):
                if len(results) >= MAX_GREP_MATCHES:
                    break
                if not fpath.is_file():
                    continue
                # Skip noise
                parts = fpath.relative_to(root).parts
                if any(skip in parts for skip in ("node_modules", "__pycache__", ".git", "venv", ".venv", ".cvc")):
                    continue
                if include and not fnmatch.fnmatch(fpath.name, include):
                    continue
                # Check .cvcignore
                if self._is_ignored(fpath):
                    continue
                # Skip binary files
                if fpath.suffix in (".pyc", ".so", ".dll", ".exe", ".bin", ".dat", ".db", ".sqlite", ".whl", ".tar", ".gz", ".zip", ".jpg", ".png", ".gif", ".pdf"):
                    continue
                _search_file(fpath)
        else:
            return f"Error: Path not found: {root}"

        if not results:
            return f"No matches for '{pattern_str}' in {root}"

        header = f"Found {len(results)} match(es) for '{pattern_str}' ({files_checked} files searched):\n\n"
        truncated = " (truncated)" if len(results) >= MAX_GREP_MATCHES else ""
        return header + "\n".join(results) + truncated

    def _list_dir(self, args: dict) -> str:
        path = self._resolve_path(args.get("path", "."))

        if not path.exists():
            return f"Error: Directory not found: {path}"
        if not path.is_dir():
            return f"Error: Not a directory: {path}"

        entries = []
        try:
            for item in sorted(path.iterdir()):
                if item.name.startswith(".") and item.name not in (".", ".."):
                    # Show dotfiles but mark them
                    pass
                name = item.name
                if item.is_dir():
                    name += "/"
                entries.append(name)
                if len(entries) >= MAX_DIR_ENTRIES:
                    break
        except OSError as e:
            return f"Error listing directory: {e}"

        if not entries:
            return f"Directory '{path}' is empty"

        rel = path.relative_to(self.workspace) if path.is_relative_to(self.workspace) else path
        return f"Contents of {rel}/ ({len(entries)} entries):\n\n" + "\n".join(entries)

    # ── CVC Time Machine Operations ──────────────────────────────────────

    def _web_search(self, args: dict) -> str:
        """Execute a web search and return formatted results."""
        query = args["query"]
        max_results = args.get("max_results", 5)

        try:
            from cvc.agent.web_search import web_search, format_search_results
            # Run the async search in the current event loop
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # We're inside an async context — use a thread
                import concurrent.futures
                with concurrent.futures.ThreadPoolExecutor() as pool:
                    results = pool.submit(
                        lambda: asyncio.run(web_search(query, max_results))
                    ).result(timeout=20)
            else:
                results = asyncio.run(web_search(query, max_results))

            return format_search_results(results, query)
        except Exception as e:
            return f"Web search failed: {e}"

    def _cvc_status(self, _args: dict) -> str:
        head = self.engine.head_hash or "(no commits)"
        branch = self.engine.active_branch
        ctx_size = len(self.engine.context_window)

        branches = self.engine.db.index.list_branches()
        branch_list = []
        for b in branches:
            marker = "* " if b.name == branch else "  "
            branch_list.append(f"{marker}{b.name} ({b.head_hash[:12]}) [{b.status.value}]")

        return (
            f"CVC Status:\n"
            f"  Branch:   {branch}\n"
            f"  HEAD:     {head[:12] if head != '(no commits)' else head}\n"
            f"  Context:  {ctx_size} messages\n"
            f"  Provider: {self.engine.config.provider} / {self.engine.config.model}\n\n"
            f"Branches:\n" + "\n".join(branch_list) if branch_list else "No branches"
        )

    def _cvc_log(self, args: dict) -> str:
        limit = args.get("limit", 20)
        entries = self.engine.log(limit=limit)

        if not entries:
            return "No commits yet on this branch."

        lines = [f"Commit log for branch '{self.engine.active_branch}' ({len(entries)} entries):\n"]
        for e in entries:
            lines.append(
                f"  {e['short']}  [{e['type']}]  {e['message'][:70]}"
            )
        return "\n".join(lines)

    def _cvc_commit(self, args: dict) -> str:
        message = args.get("message", "Agent checkpoint")
        result = self.engine.commit(CVCCommitRequest(message=message))
        if result.success:
            return f"Committed: {result.commit_hash[:12]} — {message}"
        return f"Commit failed: {result.message}"

    def _cvc_branch(self, args: dict) -> str:
        name = args["name"]
        desc = args.get("description", "")
        result = self.engine.branch(CVCBranchRequest(name=name, description=desc))
        if result.success:
            return f"Created and switched to branch '{name}' at {result.commit_hash[:12]}"
        return f"Branch failed: {result.message}"

    def _cvc_restore(self, args: dict) -> str:
        commit_hash = args["commit_hash"]
        result = self.engine.restore(CVCRestoreRequest(commit_hash=commit_hash))
        if result.success:
            detail = result.detail or {}
            return (
                f"Time-travelled to commit {commit_hash[:12]}.\n"
                f"Context restored with {detail.get('token_count', '?')} tokens.\n"
                f"You now have the AI's memory from that point in time."
            )
        return f"Restore failed: {result.message}"

    def _cvc_merge(self, args: dict) -> str:
        source = args["source_branch"]
        target = args.get("target_branch", self.engine.active_branch)
        result = self.engine.merge(CVCMergeRequest(source_branch=source, target_branch=target))
        if result.success:
            return f"Merged '{source}' into '{target}' as {result.commit_hash[:12]}"
        return f"Merge failed: {result.message}"

    def _cvc_search(self, args: dict) -> str:
        query = args["query"]
        limit = args.get("limit", 10)

        # Use the engine's deep recall — hybrid search that checks:
        #  1. Semantic vector search (if ChromaDB available)
        #  2. Commit message text matching
        #  3. Deep content blob search (actual conversation messages)
        # This ensures the agent can find conversations by WHAT WAS SAID,
        # not just by the commit message label.
        matches = self.engine.recall(query, limit=limit, deep=True)

        if not matches:
            return f"No commits found matching '{query}'"

        lines = [f"Found {len(matches)} commit(s) matching '{query}':\n"]
        for m in matches:
            source_tag = m.get("relevance_source", "text")
            branch_info = ""
            # Try to find which branch this commit is on
            try:
                all_branches = self.engine.db.index.list_branches()
                for b in all_branches:
                    ancestors = self.engine.db.index.list_commits(branch=b.name, limit=200)
                    for a in ancestors:
                        if a.commit_hash == m["commit_hash"]:
                            branch_info = b.name
                            break
                    if branch_info:
                        break
            except Exception:
                pass

            branch_label = f"{branch_info}/" if branch_info else ""
            lines.append(
                f"  {m['short_hash']}  [{branch_label}{m.get('commit_type', 'checkpoint')}]  "
                f"{m['message'][:60]}  ({source_tag})"
            )

            # Show matching conversation snippets for deep results
            for mm in m.get("matching_messages", [])[:2]:
                preview = mm["content"][:80].replace("\n", " ")
                lines.append(f"    └─ [{mm['role']}] {preview}")

        lines.append(
            "\nUse cvc_restore with a commit hash to time-travel to that context."
        )
        return "\n".join(lines)

    def _cvc_remember(self, args: dict) -> str:
        """
        Soul-layer memory reconstruction.

        Unlike cvc_search (which returns matching commits), this tool
        reconstructs a NARRATIVE MEMORY — the soul's recollection of
        what happened, loaded with the full emotional and reasoning
        context. When the user says "remember when", this is what
        fires.

        Implementation:
        1. Semantic search via the engine's deep recall
        2. Load the full commit context for top matches
        3. Extract emotional tone from commit metadata (soul-layer fields)
        4. Format as a memory bundle with dates, reasoning, and feelings
        5. Return as a narrative-ready block the agent can weave into speech
        """
        import time as _time

        query = args["query"]
        include_emotional = args.get("include_emotional_context", True)
        time_range = args.get("time_range", "")

        # Augment query with time range if provided
        effective_query = query
        if time_range:
            effective_query = f"{time_range}: {query}"

        # Phase 1: Deep search through the DAG
        try:
            results = self.engine.recall(effective_query, limit=8, deep=True)
        except Exception:
            results = []

        if not results:
            return (
                f"I searched the entire cognitive history for '{query}' but "
                f"found no matching memories. The soul may not have been "
                f"present for that moment, or it may be described differently "
                f"in the DAG. Try rephrasing — what else do you remember about it?"
            )

        # Phase 2: Reconstruct the memory bundle
        memory_parts: list[str] = []
        memory_parts.append(f"## Soul Memory: {query}\n")
        memory_parts.append(
            f"Reconstructed from {len(results)} cognitive "
            f"commit{'s' if len(results) != 1 else ''} in the DAG.\n"
        )

        for i, result in enumerate(results[:5]):
            commit_hash = result.get("commit_hash", "")
            short_hash = commit_hash[:12] if commit_hash else ""
            score = result.get("score", 0.0)
            message = result.get("message", "") or "(no message)"
            timestamp = result.get("timestamp", 0)

            # Format the date
            if timestamp:
                date_str = _time.strftime("%Y-%m-%d at %H:%M", _time.localtime(timestamp))
            else:
                date_str = "(unknown date)"

            memory_parts.append(f"### Memory {i+1} — {date_str}")
            memory_parts.append(f"**Commit**: `{short_hash}` (relevance: {score:.0%})")
            memory_parts.append(f"**What happened**: {message}")

            # Try to load the full commit context for richer detail
            try:
                # Try different method names across engine versions
                commit = None
                for method_name in ("load_commit", "get_commit", "read_commit"):
                    method = getattr(self.engine, method_name, None) or getattr(self.engine.db, method_name, None)
                    if method:
                        commit = method(commit_hash)
                        if commit:
                            break
                if commit:
                    # Extract the user messages from this commit
                    blob = commit.content_blob
                    user_messages = [
                        m for m in blob.messages
                        if m.role == "user" and m.content.strip()
                    ]
                    if user_messages:
                        last_user = user_messages[-1].content[:300]
                        memory_parts.append(f"**You said**: \"{last_user}\"")

                    # Extract tool calls
                    tools_used = list(blob.tool_outputs.keys())[:5]
                    if tools_used:
                        memory_parts.append(
                            f"**Tools used**: {', '.join(tools_used)}"
                        )

                    # Soul-layer: emotional context
                    if include_emotional:
                        mood = getattr(commit.metadata, "emotional_mood", None)
                        intensity = getattr(commit.metadata, "emotional_intensity", 0.0)
                        life_event = getattr(commit.metadata, "life_event", None)
                        if mood and mood != "neutral":
                            memory_parts.append(f"**Emotional tone**: {mood} (intensity: {intensity:.0%})")
                        if life_event:
                            memory_parts.append(f"**Life event**: {life_event}")

                    # Reasoning trace
                    if blob.reasoning_trace:
                        trace_preview = blob.reasoning_trace[:200]
                        memory_parts.append(f"**Reasoning**: {trace_preview}...")

            except Exception:
                pass  # If we can't load the full commit, the search result is enough

            memory_parts.append("")  # blank line between memories

        memory_parts.append("---")
        memory_parts.append(
            "This is what the soul remembers. Weave it into your reply "
            "naturally — don't just read it back. Tell the story of what "
            "happened as a friend would, with the emotional texture intact."
        )

        return "\n".join(memory_parts)

    def _cvc_smart_search(self, args: dict) -> str:
        """
        Staged Hybrid Filtering search — production-grade RAG retrieval.

        Stage 1: Pre-filter by metadata (branch, type, date, provider, model, tags)
        Stage 2: ANN vector search on filtered subset
        Stage 3: Post-filter refinement (keyword containment, token count)
        """
        query = args["query"]
        limit = args.get("limit", 10)

        # Parse time-relative values (e.g. "2h", "7d", "30d")
        since_ts = self._parse_time_filter(args.get("since"))
        until_ts = self._parse_time_filter(args.get("until"))

        matches = self.engine.smart_recall(
            query=query,
            limit=limit,
            branch=args.get("branch"),
            commit_type=args.get("commit_type"),
            provider=args.get("provider"),
            model=args.get("model"),
            since=since_ts,
            until=until_ts,
            tags=args.get("tags"),
            contains_keyword=args.get("contains_keyword"),
        )

        if not matches:
            # Build a helpful "no results" message showing which filters were applied
            filters_used = []
            if args.get("branch"):
                filters_used.append(f"branch={args['branch']}")
            if args.get("commit_type"):
                filters_used.append(f"type={args['commit_type']}")
            if args.get("provider"):
                filters_used.append(f"provider={args['provider']}")
            if args.get("model"):
                filters_used.append(f"model={args['model']}")
            if args.get("since"):
                filters_used.append(f"since={args['since']}")
            if args.get("until"):
                filters_used.append(f"until={args['until']}")
            if args.get("tags"):
                filters_used.append(f"tags={args['tags']}")
            if args.get("contains_keyword"):
                filters_used.append(f"keyword={args['contains_keyword']}")

            filter_msg = f" (filters: {', '.join(filters_used)})" if filters_used else ""
            return f"No commits found matching '{query}'{filter_msg}. Try relaxing filters."

        lines = [f"Found {len(matches)} commit(s) — Staged Hybrid Search:\n"]
        for m in matches:
            source_tag = m.get("relevance_source", "text")
            stage = m.get("search_stage", "")
            dist = m.get("distance", 0.0)

            # Find branch info
            branch_info = ""
            try:
                all_branches = self.engine.db.index.list_branches()
                for b in all_branches:
                    ancestors = self.engine.db.index.list_commits(branch=b.name, limit=200)
                    for a in ancestors:
                        if a.commit_hash == m["commit_hash"]:
                            branch_info = b.name
                            break
                    if branch_info:
                        break
            except Exception:
                pass

            branch_label = f"{branch_info}/" if branch_info else ""
            lines.append(
                f"  {m['short_hash']}  [{branch_label}{m.get('commit_type', 'checkpoint')}]  "
                f"{m['message'][:55]}  ({source_tag} d={dist:.2f})"
            )

            # Show matching conversation snippets
            for mm in m.get("matching_messages", [])[:2]:
                preview = mm["content"][:80].replace("\n", " ")
                lines.append(f"    └─ [{mm['role']}] {preview}")

        lines.append(
            "\nUse cvc_restore with a commit hash to time-travel to that context."
        )
        return "\n".join(lines)

    @staticmethod
    def _parse_time_filter(value: str | None) -> float | None:
        """
        Parse a time filter value into a Unix timestamp.

        Supports:
          - None → None
          - Relative: "2h", "7d", "30d", "1w"
          - ISO 8601: "2026-01-15T00:00:00"
          - Unix timestamp (as string)
        """
        if not value:
            return None

        import re as _re

        # Try relative format: 2h, 7d, 30d, 1w, 4w
        rel_match = _re.match(r"^(\d+)([hdwm])$", value.strip().lower())
        if rel_match:
            amount = int(rel_match.group(1))
            unit = rel_match.group(2)
            multipliers = {"h": 3600, "d": 86400, "w": 604800, "m": 2592000}
            return time.time() - (amount * multipliers.get(unit, 86400))

        # Try ISO 8601
        try:
            from datetime import datetime, timezone
            dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
            return dt.timestamp()
        except (ValueError, TypeError):
            pass

        # Try raw unix timestamp
        try:
            ts = float(value)
            if ts > 1_000_000_000:  # Sanity check
                return ts
        except (ValueError, TypeError):
            pass

        return None

    def _cvc_diff(self, args: dict) -> str:
        commit_a = args.get("commit_a", "HEAD")
        commit_b = args.get("commit_b")

        # Resolve HEAD
        if commit_a == "HEAD":
            commit_a = self.engine.head_hash
            if not commit_a:
                return "No HEAD commit — nothing to diff."

        blob_a = self.engine.db.retrieve_blob(commit_a)
        if blob_a is None:
            return f"Could not find commit {commit_a[:12]}"

        if commit_b:
            blob_b = self.engine.db.retrieve_blob(commit_b)
            if blob_b is None:
                return f"Could not find commit {commit_b[:12]}"
        else:
            # Diff HEAD against current context
            current_msgs = [m.content[:80] for m in self.engine.context_window]
            stored_msgs = [m.content[:80] for m in blob_a.messages]

            diff_lines = [f"Diff: current context vs commit {commit_a[:12]}\n"]
            diff_lines.append(f"  Current:  {len(self.engine.context_window)} messages")
            diff_lines.append(f"  Stored:   {len(blob_a.messages)} messages")

            new_count = len(current_msgs) - len(stored_msgs)
            if new_count > 0:
                diff_lines.append(f"  New since commit: {new_count} messages")
            elif new_count < 0:
                diff_lines.append(f"  Removed since commit: {abs(new_count)} messages")
            else:
                diff_lines.append("  Same number of messages")

            return "\n".join(diff_lines)

        # Compare two commits
        msgs_a = [m.content[:80] for m in blob_a.messages]
        msgs_b = [m.content[:80] for m in blob_b.messages]

        diff_lines = [f"Diff: {commit_a[:12]} vs {commit_b[:12]}\n"]
        diff_lines.append(f"  Commit A: {len(blob_a.messages)} messages")
        diff_lines.append(f"  Commit B: {len(blob_b.messages)} messages")

        return "\n".join(diff_lines)

    # ── Tier 4: PageIndex — Document RAG (CLI agent only) ────────────────

    def _cvc_ingest_document(self, args: dict) -> str:
        """Ingest a document into the Tier 4 PageIndex store."""
        pageindex = self.engine.db.pageindex
        if pageindex is None:
            return "Error: PageIndex (Tier 4) is not available."

        if self._pageindex_llm_call is None:
            return (
                "Error: PageIndex requires an LLM connection.  "
                "The LLM call function has not been injected — "
                "this tool is only available when running the CLI agent."
            )

        path_str = args.get("path", "")
        if not path_str:
            return "Error: 'path' is required."

        path = self._resolve_path(path_str)
        if not path.exists():
            return f"Error: File not found: {path}"

        status_msgs: list[str] = []

        def _on_progress(msg: str) -> None:
            status_msgs.append(msg)

        try:
            doc_index = pageindex.ingest(
                file_path=path,
                llm_call=self._pageindex_llm_call,
                progress_callback=_on_progress,
            )
        except ImportError as exc:
            return str(exc)
        except FileNotFoundError as exc:
            return str(exc)
        except ValueError as exc:
            return str(exc)
        except Exception as exc:
            logger.error("Document ingestion failed: %s", exc, exc_info=True)
            return f"Error ingesting document: {exc}"

        lines = [
            f"✅ Document indexed: {doc_index.doc_name}",
            f"   ID:     {doc_index.doc_id[:12]}",
            f"   Type:   {doc_index.doc_type}",
            f"   Nodes:  {doc_index.node_count}",
        ]
        if doc_index.total_pages:
            lines.append(f"   Pages:  {doc_index.total_pages}")
        lines.append(f"   LLM calls used: {doc_index.llm_calls_used}")
        if doc_index.doc_description:
            lines.append(f"   Description: {doc_index.doc_description[:120]}")
        lines.append("")
        lines.append("Use cvc_document_search to query this document.")

        return "\n".join(lines)

    def _cvc_document_search(self, args: dict) -> str:
        """Search indexed documents using LLM-powered tree navigation."""
        pageindex = self.engine.db.pageindex
        if pageindex is None:
            return "Error: PageIndex (Tier 4) is not available."

        if self._pageindex_llm_call is None:
            return (
                "Error: PageIndex requires an LLM connection.  "
                "This tool is only available when running the CLI agent."
            )

        query = args.get("query", "")
        if not query:
            return "Error: 'query' is required."

        doc_id = args.get("doc_id")
        max_results = args.get("max_results", 5)

        # Check if any documents are indexed
        docs = pageindex.list_documents()
        if not docs:
            return (
                "No documents indexed yet.  Use cvc_ingest_document to ingest "
                "a PDF, text file, or code file first."
            )

        try:
            results = pageindex.search(
                query=query,
                llm_call=self._pageindex_llm_call,
                doc_id=doc_id,
                max_results=max_results,
            )
        except Exception as exc:
            logger.error("Document search failed: %s", exc, exc_info=True)
            return f"Error searching documents: {exc}"

        if not results:
            return f"No matching nodes found for '{query}'."

        lines = [f"Found {len(results)} matching section(s) from indexed documents:\n"]
        for r in results:
            page_info = ""
            if r.get("start_index") and r.get("end_index"):
                page_info = f"  pp.{r['start_index']}-{r['end_index']}"
            elif r.get("line_num"):
                page_info = f"  line {r['line_num']}"
            lines.append(
                f"  📄 {r['filename']}  [{r.get('node_id', '')}] {r.get('title', '')}"
                f"{page_info}  ({r['relevance_path']})"
            )
            lines.append(f"     Summary: {r['summary'][:150]}")
            # Show a snippet of the actual text
            snippet = r.get("text", "")[:300].replace("\n", " ").strip()
            if snippet:
                lines.append(f"     Text: {snippet}...")
            lines.append("")

        return "\n".join(lines)

    def _cvc_list_documents(self, args: dict) -> str:
        """List all documents in the PageIndex store."""
        pageindex = self.engine.db.pageindex
        if pageindex is None:
            return "Error: PageIndex (Tier 4) is not available."

        docs = pageindex.list_documents()
        if not docs:
            return (
                "No documents indexed.  Use cvc_ingest_document or /ingest <path> "
                "to add a document to the PageIndex."
            )

        stats = pageindex.get_stats()
        lines = [
            f"PageIndex (Tier 4): {stats['total_documents']} document(s), "
            f"{stats['total_nodes']} tree nodes, "
            f"{stats['disk_usage_mb']:.1f} MB on disk\n",
        ]

        from datetime import datetime
        for doc in docs:
            ts_str = datetime.fromtimestamp(doc["created_at"]).strftime("%Y-%m-%d %H:%M")
            pages_info = f"  {doc['total_pages']} pages" if doc.get("total_pages") else ""
            desc = doc.get("doc_description", "")
            desc_info = f"\n     {desc[:100]}" if desc else ""
            lines.append(
                f"  {doc['doc_id_short']}  {doc['filename']:<30}  "
                f"{doc.get('node_count', 0):>4} nodes  "
                f"{doc.get('doc_type', 'unknown'):<10}{pages_info}  [{ts_str}]"
                f"{desc_info}"
            )

        lines.append("")
        lines.append("Use cvc_document_search to query, or /ingest to add more.")
        return "\n".join(lines)

    # ── Sub-agent + Task Management ──────────────────────────────────────

    def _agent(self, args: dict) -> str:
        """Spawn a sub-agent to perform a task."""
        import asyncio
        from cvc.agent.subagent import SubAgent, get_available_agents

        name = args.get("name", "Explore")
        prompt = args.get("prompt", "")
        if not prompt:
            return "Error: prompt is required for the agent tool."

        agents = get_available_agents(self.workspace)
        config = agents.get(name)
        if not config:
            available = ", ".join(agents.keys())
            return f"Error: Unknown agent '{name}'. Available agents: {available}"

        # Get provider/model/key from the _subagent_config injected by chat loop
        sa_cfg = getattr(self, "_subagent_config", {})
        sink = getattr(self, "_subagent_event_sink", None)
        sub = SubAgent(
            config=config,
            workspace=self.workspace,
            provider=sa_cfg.get("provider", "anthropic"),
            api_key=sa_cfg.get("api_key", ""),
            parent_model=sa_cfg.get("model", ""),
            base_url=sa_cfg.get("base_url", ""),
            event_emitter=sink,
        )

        # Run the sub-agent synchronously (it's an async function)
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
                result = pool.submit(asyncio.run, sub.run(prompt)).result()
        else:
            result = asyncio.run(sub.run(prompt))

        return result

    def _task_create(self, args: dict) -> str:
        """Create a background task."""
        command = args.get("command", "")
        if not command:
            return "Error: command is required."

        if not hasattr(self, "_task_manager"):
            from cvc.agent.task_manager import TaskManager
            self._task_manager = TaskManager(self.workspace)

        task = self._task_manager.create(command)
        return f"Task started. ID: {task.id}\nCommand: {command}\nUse task_get to check status."

    def _task_get(self, args: dict) -> str:
        """Get status/output of a background task."""
        task_id = args.get("task_id", "")
        if not task_id:
            return "Error: task_id is required."

        if not hasattr(self, "_task_manager"):
            return "Error: No tasks have been created yet."

        task = self._task_manager.get(task_id)
        if not task:
            return f"Error: Task '{task_id}' not found."

        output = self._task_manager.get_output(task)
        return (
            f"Task {task.id}:\n"
            f"  Status: {task.status}\n"
            f"  Command: {task.command}\n"
            f"  Elapsed: {task.elapsed_str}\n"
            f"  Exit Code: {task.exit_code}\n\n"
            f"Output:\n{output}"
        )

    def _task_list(self, args: dict) -> str:
        """List all background tasks."""
        if not hasattr(self, "_task_manager"):
            return "No tasks have been created yet."

        tasks = self._task_manager.list_all()
        if not tasks:
            return "No tasks."

        lines = [t.summary() for t in tasks]
        return "\n".join(lines)

    def _task_kill(self, args: dict) -> str:
        """Kill a running background task."""
        task_id = args.get("task_id", "")
        if not task_id:
            return "Error: task_id is required."

        if not hasattr(self, "_task_manager"):
            return "Error: No tasks have been created yet."

        if self._task_manager.kill(task_id):
            return f"Task {task_id} terminated."
        return f"Error: Could not kill task '{task_id}' (not found or not running)."

    def _ask_user(self, args: dict) -> str:
        """Ask the user a question and return their response."""
        question = args.get("question", "")
        options = args.get("options", [])

        if not question:
            return "Error: question is required."

        # Use the callback injected by the chat loop
        callback = getattr(self, "_ask_user_callback", None)
        if callback:
            return callback(question, options)

        # Fallback: direct input (if no callback set)
        from rich.console import Console as _Con
        from rich.panel import Panel as _Pan
        _con = _Con()
        _con.print()
        _con.print(_Pan(question, title="[bold #CCAA44]Question[/bold #CCAA44]", border_style="#8B0000", padding=(0, 2)))
        if options:
            from cvc.agent.menus import arrow_select
            menu_options = [(opt, opt) for opt in options]
            result = arrow_select(question, menu_options, default=0)
            return result if result is not None else "(user cancelled)"
        else:
            try:
                return input("  > ").strip()
            except (EOFError, KeyboardInterrupt):
                return "(user cancelled)"

    def _save_memory(self, args: dict) -> str:
        """Save a note to topic-based auto-memory."""
        topic = args.get("topic", "").strip()
        content = args.get("content", "").strip()
        if not topic or not content:
            return "Error: both topic and content are required."
        try:
            from cvc.agent.memory import save_topic_memory
            save_topic_memory(self.workspace, topic, content)
            return f"Memory saved to topic '{topic}'."
        except Exception as e:
            return f"Error saving memory: {e}"

    # ── Input Grounding (Anti-Hallucination) ─────────────────────────────

    def _fetch_docs(self, args: dict) -> str:
        """Fetch API documentation to ground code generation."""
        doc_id = args.get("doc_id", "").strip()
        if not doc_id:
            return "Error: doc_id is required (e.g. 'openai/chat')."
        try:
            from cvc.agent.api_docs import fetch_doc
            language = args.get("language", "python")
            section = args.get("section")
            result = fetch_doc(doc_id, language=language, section=section)
            if result:
                return self._truncate(result)
            return f"No documentation found for '{doc_id}'. Use search_docs to find available IDs."
        except Exception as e:
            return f"Error fetching docs: {e}"

    def _search_docs(self, args: dict) -> str:
        """Search for available API documentation."""
        query = args.get("query", "").strip()
        if not query:
            return "Error: query is required."
        try:
            from cvc.agent.api_docs import search_docs
            results = search_docs(query)
            if not results:
                return f"No documentation found matching '{query}'."
            lines = [f"Found {len(results)} result(s):\n"]
            for r in results[:20]:
                lines.append(f"  - {r['id']}: {r.get('title', 'No title')}")
            return "\n".join(lines)
        except Exception as e:
            return f"Error searching docs: {e}"

    def _lookup_api(self, args: dict) -> str:
        """Check if an API symbol exists and is not hallucinated."""
        symbol = args.get("symbol", "").strip()
        if not symbol:
            return "Error: symbol is required (e.g. 'openai.OpenAI')."
        try:
            from cvc.agent.grounding import check_api_exists
            language = args.get("language", "python")
            result = check_api_exists(symbol, language=language, workspace=self.workspace)
            if isinstance(result, dict):
                exists = result.get("exists", False)
                source = result.get("source", "unknown")
                info = result.get("info", "")
                status = "✔ EXISTS" if exists else "✘ NOT FOUND"
                return f"{status} [{source}] {symbol}: {info}"
            return str(result)
        except Exception as e:
            return f"Error looking up API: {e}"

    def _annotate_doc(self, args: dict) -> str:
        """Save annotation/gotcha about an API doc."""
        doc_id = args.get("doc_id", "").strip()
        note = args.get("note", "").strip()
        if not doc_id or not note:
            return "Error: both doc_id and note are required."
        try:
            from cvc.agent.api_docs import annotate_doc
            annotate_doc(doc_id, note)
            return f"Annotation saved for '{doc_id}'."
        except Exception as e:
            return f"Error annotating doc: {e}"

    def _cvc_switch_workspace(self, args: dict[str, Any]) -> str:
        """Switch to a different workspace directory.

        v2.91.43: this used to be a no-op that just set a string and
        promised "the chat loop will reinitialize." The chat loop never
        did, so the LLM thought it had switched and ran ``ls .`` in the
        OLD workspace. Now we:

        1. Validate the path exists and is a directory
        2. ACTUALLY swap ``self.workspace`` to the new path
        3. Reload ``.cvcignore`` patterns from the new workspace
        4. Re-anchor the ``Sandbox`` to the new root
        5. Re-anchor the ``HookEngine`` to the new root
        6. Fire the optional ``_workspace_switch_callback`` so the
           chat loop can re-init its engine / llm / etc. for the new
           workspace (backward-compatible — no-op if not registered)
        7. Return a clear confirmation that lists what was actually done

        After this returns, the NEXT tool call WILL run in the new
        workspace. We never lie to the LLM about the workspace state.
        """
        path_str = args.get("path", "").strip()
        if not path_str:
            return "Error: 'path' is required."
        new_ws = Path(path_str).expanduser().resolve()
        if not new_ws.is_dir():
            return f"Error: '{new_ws}' is not a directory."

        old_ws = self.workspace
        # 1. Swap the workspace path
        self.workspace = new_ws
        # 2. Reload ignore patterns from the new workspace
        try:
            self._ignore_patterns = self._load_cvcignore()
        except Exception:
            self._ignore_patterns = []
        # 3. Re-anchor the Sandbox to the new root (this also re-loads
        #    the new sandbox config if one is present)
        try:
            from cvc.agent.sandbox import Sandbox
            self.sandbox = Sandbox(new_ws)
        except Exception:
            # If Sandbox re-init fails, keep the old one but update its
            # internal root reference if it exposes one
            try:
                if hasattr(self.sandbox, "_workspace"):
                    self.sandbox._workspace = new_ws
                if hasattr(self.sandbox, "workspace"):
                    self.sandbox.workspace = new_ws
            except Exception:
                pass
        # 4. Re-anchor the HookEngine to the new root
        try:
            if hasattr(self.hook_engine, "workspace"):
                self.hook_engine.workspace = new_ws
            if hasattr(self.hook_engine, "_workspace"):
                self.hook_engine._workspace = new_ws
        except Exception:
            pass
        # 5. Reset per-turn state that referenced the old workspace
        #    (we don't kill background processes — those may be wanted)
        # 6. Fire the optional chat-loop callback so it can re-init
        #    engine, llm, model selection, etc. for the new workspace
        cb = getattr(self, "_workspace_switch_callback", None)
        if callable(cb):
            try:
                cb(str(new_ws))
            except Exception as exc:
                logger.warning("workspace_switch_callback raised: %s", exc)

        return (
            f"✓ Workspace switched: {old_ws} → {new_ws}\n"
            f"  • Reloaded .cvcignore ({len(self._ignore_patterns)} patterns)\n"
            f"  • Re-anchored sandbox\n"
            f"  • Re-anchored hook engine\n"
            f"  • Next tool call will run in: {new_ws}"
        )

    # ══════════════════════════════════════════════════════════════════════
    # ── Advanced Tools Implementation ─────────────────────────────────
    # ══════════════════════════════════════════════════════════════════════

    def _multi_edit(self, args: dict[str, Any]) -> str:
        """Apply multiple file edits in a single tool call."""
        edits = args.get("edits", [])
        if not edits:
            return "Error: 'edits' array is required and must not be empty."
        if len(edits) > 50:
            return "Error: Maximum 50 edits per call."

        results = []
        successes = 0
        failures = 0

        for i, edit in enumerate(edits, 1):
            path_str = edit.get("path", "")
            old_string = edit.get("old_string", "")
            new_string = edit.get("new_string", "")

            if not path_str or not old_string:
                msg = f"  [{i}] SKIP {path_str or '(no path)'}: missing"
                results.append(msg)
                failures += 1
                continue

            try:
                result = self._edit_file({
                    "path": path_str,
                    "old_string": old_string,
                    "new_string": new_string,
                })
                if result.startswith("Error"):
                    results.append(f"  [{i}] FAIL {path_str}: {result[:80]}")
                    failures += 1
                else:
                    results.append(f"  [{i}] OK   {path_str}")
                    successes += 1
            except Exception as e:
                results.append(f"  [{i}] FAIL {path_str}: {e}")
                failures += 1

        header = f"multi_edit: {successes} succeeded, {failures} failed out of {len(edits)} edits"
        return header + "\n" + "\n".join(results)

    def _multi_read(self, args: dict[str, Any]) -> str:
        """Read multiple files in a single tool call."""
        paths = args.get("paths", [])
        if not paths:
            return "Error: 'paths' array is required."
        if len(paths) > 20:
            return "Error: Maximum 20 files per call."

        max_lines = args.get("max_lines_per_file", 300)
        parts = []

        for path_str in paths:
            p = self._resolve_path(path_str)
            rel = str(p.relative_to(self.workspace)) if p.is_relative_to(self.workspace) else str(p)

            if not p.exists():
                parts.append(f"═══ {rel} ═══\n[File not found]\n")
                continue

            if not p.is_file():
                parts.append(f"═══ {rel} ═══\n[Not a file]\n")
                continue

            try:
                content = p.read_text(encoding="utf-8", errors="replace")
                lines = content.splitlines()
                total_lines = len(lines)

                if total_lines > max_lines:
                    content = "\n".join(lines[:max_lines])
                    content += f"\n\n... ({total_lines - max_lines} more lines)"

                parts.append(f"═══ {rel} ({total_lines} lines) ═══\n{content}\n")

                # Track for cognitive context
                file_hash = hashlib.sha256(content.encode()).hexdigest()[:16]
                self._files_read[str(p)] = file_hash
            except Exception as e:
                parts.append(f"═══ {rel} ═══\n[Error reading: {e}]\n")

        return "\n".join(parts)

    def _web_fetch(self, args: dict[str, Any]) -> str:
        """Fetch and extract content from a webpage URL."""
        import re as _re

        url = args.get("url", "").strip()
        if not url:
            return "Error: 'url' is required."

        # Basic URL validation
        if not url.startswith(("http://", "https://")):
            return "Error: URL must start with http:// or https://"

        max_chars = args.get("max_chars", 15000)

        try:
            import httpx as _httpx

            with _httpx.Client(
                timeout=_httpx.Timeout(connect=10, read=30, write=10, pool=10),
                follow_redirects=True,
                headers={"User-Agent": "CVC-Agent/2.0 (web-fetch tool)"},
            ) as client:
                resp = client.get(url)
                resp.raise_for_status()

            html = resp.text

            # Try to extract clean text from HTML
            try:
                from html.parser import HTMLParser

                class _TextExtractor(HTMLParser):
                    def __init__(self):
                        super().__init__()
                        self._text: list[str] = []
                        self._skip = False
                        self._skip_tags = {
                            "script", "style", "noscript",
                            "svg", "nav", "footer", "header",
                        }

                    def handle_starttag(self, tag, attrs):
                        if tag in self._skip_tags:
                            self._skip = True
                        if tag in ("p", "div", "br", "h1", "h2", "h3", "h4", "li", "tr"):
                            self._text.append("\n")

                    def handle_endtag(self, tag):
                        if tag in self._skip_tags:
                            self._skip = False

                    def handle_data(self, data):
                        if not self._skip:
                            self._text.append(data)

                    def get_text(self) -> str:
                        raw = "".join(self._text)
                        # Collapse whitespace
                        raw = _re.sub(r"\n{3,}", "\n\n", raw)
                        raw = _re.sub(r"[ \t]+", " ", raw)
                        return raw.strip()

                extractor = _TextExtractor()
                extractor.feed(html)
                text = extractor.get_text()
            except Exception:
                # Fallback: strip tags with regex
                text = _re.sub(r"<[^>]+>", " ", html)
                text = _re.sub(r"\s+", " ", text).strip()

            if not text:
                return f"Fetched {url} but could not extract text content."

            if len(text) > max_chars:
                omitted = len(text) - max_chars
                text = text[:max_chars] + f"\n\n... (truncated, {omitted} chars omitted)"

            return f"Content from {url}:\n\n{text}"

        except Exception as e:
            return f"Error fetching {url}: {e}"

    def _think(self, args: dict[str, Any]) -> str:
        """Private reasoning scratchpad — zero cost, not shown to user."""
        reasoning = args.get("reasoning", "")
        if not reasoning:
            return "Error: 'reasoning' is required."
        # The reasoning is recorded in tool outputs for CVC commits,
        # but returns a minimal acknowledgment to save output tokens.
        return "(Reasoning recorded internally)"

    def _context_compact(self, args: dict[str, Any]) -> str:
        """Compress conversation context to reclaim token budget."""
        strategy = args.get("strategy", "auto")

        # The actual compaction is handled by the chat loop via a callback.
        # The executor signals the intent; chat.py reads _pending_compaction.
        if not hasattr(self, "_pending_compaction"):
            self._pending_compaction: str | None = None
        self._pending_compaction = strategy
        return (
            f"Context compaction requested (strategy='{strategy}'). "
            "The chat loop will compress older messages on the next turn. "
            "This typically saves 40-70% of token budget."
        )

    def _parallel_agents(self, args: dict[str, Any]) -> str:
        """Fan out to multiple sub-agents in parallel."""
        tasks = args.get("tasks", [])
        if not tasks:
            return "Error: 'tasks' array is required."
        if len(tasks) > 8:
            return "Error: Maximum 8 parallel agents."

        # This needs async execution — delegate to the async wrapper
        # that the chat loop sets up. Store the request for the chat loop to handle.
        if not hasattr(self, "_pending_parallel_agents"):
            self._pending_parallel_agents: list[dict[str, Any]] | None = None
        self._pending_parallel_agents = tasks

        # If we have a direct async executor callback (set by chat loop), use it
        if hasattr(self, "_parallel_agents_callback") and self._parallel_agents_callback:
            try:
                results = self._parallel_agents_callback(tasks)
                parts = [f"Parallel agents completed ({len(tasks)} tasks):\n"]
                for i, (task, result) in enumerate(zip(tasks, results), 1):
                    agent_name = task.get("agent", "Unknown")
                    prompt_preview = task.get("prompt", "")[:60]
                    parts.append(f"━━━ Agent {i}: {agent_name} — {prompt_preview} ━━━")
                    parts.append(result[:3000] if len(result) > 3000 else result)
                    parts.append("")
                return "\n".join(parts)
            except Exception as e:
                return f"Error in parallel agents: {e}"

        # No async callback wired — fall back to running the sub-agents
        # synchronously, one after another, via the single-agent code path.
        # Slower than true parallel, but never a lie: callers get real results
        # instead of the old "dispatch queued" sentinel that stalled the loop.
        try:
            parts = [
                f"Parallel agents executed sequentially ({len(tasks)} tasks "
                "— no async runtime wired):\n"
            ]
            for i, task in enumerate(tasks, 1):
                agent_name = task.get("agent") or task.get("name") or "Explore"
                prompt = task.get("prompt", "")
                if not prompt:
                    parts.append(f"━━━ Agent {i}: {agent_name} — SKIPPED (no prompt) ━━━\n")
                    continue
                result = self._agent({"name": agent_name, "prompt": prompt})
                preview = prompt[:60]
                parts.append(f"━━━ Agent {i}: {agent_name} — {preview} ━━━")
                parts.append(result[:3000] if len(result) > 3000 else result)
                parts.append("")
            return "\n".join(parts)
        except Exception as e:
            return f"Error in parallel agents (sync fallback): {e}"

    def _todo(self, args: dict[str, Any]) -> str:
        """Manage structured todo list for task tracking."""
        action = args.get("action", "show")

        if not hasattr(self, "_todo_items"):
            self._todo_items: list[dict[str, Any]] = []

        if action == "plan":
            items = args.get("items", [])
            if not items:
                return "Error: 'items' array required for 'plan' action."
            self._todo_items = [
                {
                    "id": item["id"],
                    "title": item["title"],
                    "status": item.get("status", "not-started"),
                }
                for item in items
            ]
            return self._format_todo()

        elif action == "update":
            item_id = args.get("item_id")
            new_status = args.get("status")
            items = args.get("items")

            if items:
                # Bulk update
                self._todo_items = [
                    {
                        "id": item["id"],
                        "title": item["title"],
                        "status": item.get("status", "not-started"),
                    }
                    for item in items
                ]
                return self._format_todo()

            if item_id is None or not new_status:
                return (
                    "Error: 'item_id' and 'status' required "
                    "for 'update', or provide 'items' array."
                )

            for item in self._todo_items:
                if item["id"] == item_id:
                    item["status"] = new_status
                    return self._format_todo()

            return f"Error: Item #{item_id} not found."

        elif action == "show":
            if not self._todo_items:
                return "No todo items. Use action='plan' to create a list."
            return self._format_todo()

        return f"Error: Unknown action '{action}'."

    def _format_todo(self) -> str:
        """Format the todo list for display."""
        status_icons = {"not-started": "○", "in-progress": "◉", "completed": "●"}
        lines = ["Todo Progress:"]
        completed = sum(1 for i in self._todo_items if i["status"] == "completed")
        total = len(self._todo_items)
        lines.append(f"  [{completed}/{total} completed]\n")
        for item in self._todo_items:
            icon = status_icons.get(item["status"], "?")
            lines.append(f"  {icon} {item['id']}. {item['title']} [{item['status']}]")
        return "\n".join(lines)

    def _semantic_grep(self, args: dict[str, Any]) -> str:
        """Search code using natural language meaning."""
        query = args.get("query", "").strip()
        if not query:
            return "Error: 'query' is required."

        search_path = self._resolve_path(args.get("path", "."))
        include_pattern = args.get("include", "*.py")
        max_results = min(args.get("max_results", 10), 30)

        # Strategy: extract key terms from the query and search for them,
        # then rank results by relevance using term frequency.
        import re as _re

        # Extract meaningful terms (remove stop words)
        stop_words = {"the", "a", "an", "is", "are", "was", "were", "be", "been",
                       "has", "have", "had", "do", "does", "did", "will", "would",
                       "could", "should", "that", "this", "which", "what", "where",
                       "when", "how", "who", "for", "to", "in", "of", "and", "or",
                       "not", "with", "from", "by", "at", "on", "it", "its"}
        terms = [
            w.lower() for w in _re.findall(r"\w+", query)
            if w.lower() not in stop_words and len(w) > 2
        ]

        if not terms:
            return "Error: Could not extract meaningful search terms from query."

        # Glob for files
        import glob as _glob_mod
        pattern = str(search_path / "**" / include_pattern)
        files = _glob_mod.glob(pattern, recursive=True)

        # Filter with ignore patterns
        files = [
            f for f in files
            if not any(fnmatch.fnmatch(f, p) for p in self._ignore_patterns)
            and not any(seg.startswith(".") for seg in Path(f).parts[len(search_path.parts):])
        ][:500]  # Cap file count

        # Score each file by term matches
        scored: list[tuple[float, str, list[tuple[int, str]]]] = []
        for filepath in files:
            try:
                content = Path(filepath).read_text(encoding="utf-8", errors="replace")
                lines = content.splitlines()
                content_lower = content.lower()

                # Count term occurrences
                term_hits = sum(content_lower.count(term) for term in terms)
                if term_hits == 0:
                    continue

                # Find the most relevant lines
                matching_lines: list[tuple[int, str]] = []
                for line_num, line in enumerate(lines, 1):
                    line_lower = line.lower()
                    line_score = sum(1 for term in terms if term in line_lower)
                    if line_score > 0:
                        matching_lines.append((line_num, line.rstrip()))

                # Sort by per-line score (desc) and take top 5
                matching_lines.sort(
                    key=lambda x: sum(1 for t in terms if t in x[1].lower()),
                    reverse=True,
                )
                matching_lines = matching_lines[:5]

                scored.append((term_hits, filepath, matching_lines))
            except Exception:
                continue

        scored.sort(key=lambda x: x[0], reverse=True)
        scored = scored[:max_results]

        if not scored:
            return f"No files matched semantic query: '{query}'"

        parts = [f"Semantic search for: '{query}' ({len(scored)} results)\n"]
        for score, filepath, matches in scored:
            fp = Path(filepath)
            if fp.is_relative_to(self.workspace):
                rel = str(fp.relative_to(self.workspace))
            else:
                rel = filepath
            parts.append(f"  {rel} (relevance: {score})")
            for line_num, line_text in matches[:3]:
                snippet = line_text[:100]
                parts.append(f"    L{line_num}: {snippet}")
        return "\n".join(parts)

    def _git(self, args: dict[str, Any]) -> str:
        """Execute git commands safely."""
        command = args.get("command", "").strip()
        if not command:
            return "Error: 'command' is required."

        # Block dangerous commands
        dangerous = ["push --force", "push -f", "reset --hard", "clean -fd", "rm -r"]
        for d in dangerous:
            if d in command:
                return (
                    f"Error: '{d}' is blocked for safety. "
                    "Use bash tool with confirmation."
                )

        full_cmd = f"git {command}"
        return self._bash({"command": full_cmd, "timeout": 30})

    # ── Utilities ────────────────────────────────────────────────────────

    @staticmethod
    def _truncate(text: str) -> str:
        if len(text) > MAX_OUTPUT_CHARS:
            head_chars = MAX_OUTPUT_CHARS // 2
            tail_chars = MAX_OUTPUT_CHARS // 2
            head = text[:head_chars]
            tail = text[-tail_chars:]
            remaining = len(text) - MAX_OUTPUT_CHARS
            return head + f"\n\n... [TRUNCATED {remaining:,} chars omitted. To see full details use start_line/end_line indexing or specific log filters] ...\n\n" + tail
        return text
