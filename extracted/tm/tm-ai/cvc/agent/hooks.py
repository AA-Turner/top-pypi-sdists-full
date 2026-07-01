"""
cvc.agent.hooks — Pre/Post tool execution automation (Claude Code-style).

Hooks let you run custom shell commands before or after tool calls:
  - PreToolUse:   Runs before a tool executes. Exit code 2 = block the tool.
  - PostToolUse:  Runs after a tool completes. Can process/validate results.
  - SessionStart: Runs when an agent session begins.
  - SessionStop:  Runs when an agent session ends.

Configuration (in .cvc/settings.json or ~/.cvc/settings.json):
  {
    "hooks": [
      {
        "event": "PreToolUse",
        "matcher": "bash",
        "command": "python .cvc/hooks/pre_bash.py"
      },
      {
        "event": "PostToolUse",
        "matcher": "Edit(*)",
        "command": "npx eslint --fix"
      }
    ]
  }

Hook commands receive context as JSON on stdin:
  PreToolUse:  {"tool_name": "bash", "arguments": {"command": "..."}}
  PostToolUse: {"tool_name": "bash", "arguments": {...}, "result": "..."}
  SessionStart: {"workspace": "...", "model": "...", "branch": "..."}
  SessionStop:  {"turns": 5, "cost": "$0.12", "duration": "5m"}

Exit codes:
  0 = proceed normally
  1 = ask user for confirmation
  2 = block the action
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
from cvc._subprocess_compat import HIDDEN_KW
from dataclasses import dataclass, field
from enum import Enum
from fnmatch import fnmatch
from pathlib import Path
from typing import Any

logger = logging.getLogger("cvc.agent.hooks")


class HookEvent(str, Enum):
    PRE_TOOL_USE = "PreToolUse"
    POST_TOOL_USE = "PostToolUse"
    SESSION_START = "SessionStart"
    SESSION_STOP = "SessionStop"


class HookOutcome(Enum):
    PROCEED = 0
    ASK_USER = 1
    BLOCK = 2


@dataclass
class HookConfig:
    """A single hook definition."""
    event: HookEvent
    matcher: str       # Tool name pattern (e.g. "bash", "Edit(*)", "*")
    command: str       # Shell command to run
    timeout: int = 30  # Max seconds for hook execution

    @staticmethod
    def from_dict(d: dict[str, Any]) -> HookConfig:
        return HookConfig(
            event=HookEvent(d["event"]),
            matcher=d.get("matcher", "*"),
            command=d["command"],
            timeout=int(d.get("timeout", 30)),
        )


@dataclass
class HookResult:
    """Result of running a hook."""
    outcome: HookOutcome
    stdout: str = ""
    stderr: str = ""
    exit_code: int = 0


class HookEngine:
    """Manages and fires hooks based on events and tool patterns."""

    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace
        self._hooks: list[HookConfig] = []

    def add_hook(self, hook: HookConfig) -> None:
        self._hooks.append(hook)

    def load_from_settings(self, hooks_list: list[dict[str, Any]]) -> None:
        """Load hooks from settings dict (e.g. from settings.json)."""
        for h in hooks_list:
            try:
                self._hooks.append(HookConfig.from_dict(h))
            except (KeyError, ValueError) as e:
                logger.warning("Invalid hook config: %s — %s", h, e)

    def _matches(self, matcher: str, tool_name: str, arguments: dict) -> bool:
        """Check if a hook matcher applies to a given tool call."""
        # Pattern formats:
        #   "bash"        → exact match on tool name
        #   "Edit(*)"     → tool name with argument glob
        #   "*"           → matches everything
        #   "Bash(npm *)" → bash tool where command matches glob

        if matcher == "*":
            return True

        # Check for Tool(pattern) syntax
        if "(" in matcher and matcher.endswith(")"):
            hook_tool = matcher[:matcher.index("(")].lower()
            pattern = matcher[matcher.index("(") + 1:-1]

            if hook_tool != tool_name.lower():
                return False

            # Match pattern against the primary argument
            primary_arg = ""
            if tool_name == "bash":
                primary_arg = arguments.get("command", "")
            elif tool_name in ("write_file", "edit_file", "patch_file", "read_file"):
                primary_arg = arguments.get("path", "")
            elif tool_name == "agent":
                primary_arg = arguments.get("name", "")

            return fnmatch(primary_arg, pattern)

        # Simple name match
        return matcher.lower() == tool_name.lower()

    def fire(
        self,
        event: HookEvent,
        context: dict[str, Any],
        tool_name: str = "",
        arguments: dict | None = None,
    ) -> HookResult:
        """
        Fire all hooks matching the event and tool pattern.

        Returns the most restrictive outcome (block > ask > proceed).
        """
        matching = []
        for hook in self._hooks:
            if hook.event != event:
                continue

            # For tool events, check matcher against tool name
            if event in (HookEvent.PRE_TOOL_USE, HookEvent.POST_TOOL_USE):
                if not self._matches(hook.matcher, tool_name, arguments or {}):
                    continue

            matching.append(hook)

        if not matching:
            return HookResult(outcome=HookOutcome.PROCEED)

        # Run all matching hooks and collect results
        worst_outcome = HookOutcome.PROCEED
        all_stdout = []
        all_stderr = []

        for hook in matching:
            result = self._run_hook(hook, context)
            all_stdout.append(result.stdout)
            all_stderr.append(result.stderr)

            if result.outcome.value > worst_outcome.value:
                worst_outcome = result.outcome

        return HookResult(
            outcome=worst_outcome,
            stdout="\n".join(filter(None, all_stdout)),
            stderr="\n".join(filter(None, all_stderr)),
        )

    def _run_hook(self, hook: HookConfig, context: dict[str, Any]) -> HookResult:
        """Execute a single hook command."""
        try:
            # Determine shell
            if os.name == "nt":
                shell_cmd = ["powershell", "-NoProfile", "-Command", hook.command]
            else:
                shell_cmd = ["/bin/sh", "-c", hook.command]

            proc = subprocess.run(
                shell_cmd,
                input=json.dumps(context),
                capture_output=True,
                text=True,
                cwd=str(self.workspace),
                timeout=hook.timeout,
                env={**os.environ},
                            **HIDDEN_KW,
            )

            # Map exit code to outcome
            if proc.returncode == 0:
                outcome = HookOutcome.PROCEED
            elif proc.returncode == 1:
                outcome = HookOutcome.ASK_USER
            else:
                outcome = HookOutcome.BLOCK

            return HookResult(
                outcome=outcome,
                stdout=proc.stdout.strip(),
                stderr=proc.stderr.strip(),
                exit_code=proc.returncode,
            )

        except subprocess.TimeoutExpired:
            logger.warning("Hook timed out: %s (timeout=%ds)", hook.command, hook.timeout)
            return HookResult(
                outcome=HookOutcome.PROCEED,
                stderr=f"Hook timed out after {hook.timeout}s",
            )
        except Exception as e:
            logger.error("Hook failed: %s — %s", hook.command, e)
            return HookResult(
                outcome=HookOutcome.PROCEED,
                stderr=f"Hook error: {e}",
            )

    @property
    def hook_count(self) -> int:
        return len(self._hooks)
