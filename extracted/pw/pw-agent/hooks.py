"""Hooks — shell commands triggered by pw-agent lifecycle events.

Users put executable scripts in ~/.pw-agent/hooks/ and they fire on
specific events. Inspired by Claude Code's hook system.

Hook events:
  pre_tool_use   — fires before a tool runs. Receives JSON on stdin
                   {tool: name, args: {...}}. Exit code 2 → block the
                   call. Other non-zero → log warning, continue.
  post_tool_use  — fires after a tool runs. Receives
                   {tool: name, args: {...}, result: "..."}. Exit code
                   ignored — informational only.
  session_start  — fires when pw-agent boots. No stdin. Stdout is
                   shown to the user as a banner.
  user_prompt_submit — fires when the user submits a prompt. Stdin is
                   {prompt: "..."}. Stdout is appended to the prompt
                   as additional context. Exit 2 blocks the prompt.

Hooks can also be configured via ~/.pw-agent/hooks.json:
{
  "pre_tool_use": ["~/.pw-agent/hooks/log-tools.sh"],
  "session_start": ["~/.pw-agent/hooks/banner.sh"]
}

If hooks.json doesn't exist, every executable file in ~/.pw-agent/hooks/
named like the event (e.g. pre_tool_use, pre_tool_use.sh) is fired.
"""

import json
import os
import subprocess
from typing import Optional

DEFAULT_HOOKS_DIR = os.path.expanduser("~/.pw-agent/hooks")
HOOKS_CONFIG_FILE = os.path.expanduser("~/.pw-agent/hooks.json")

EVENTS = [
    "pre_tool_use",
    "post_tool_use",
    "session_start",
    "user_prompt_submit",
]


def _load_hooks_config() -> dict[str, list[str]]:
    """Load hook config from JSON or fall back to scanning the hooks dir."""
    if os.path.exists(HOOKS_CONFIG_FILE):
        try:
            with open(HOOKS_CONFIG_FILE, "r") as f:
                cfg = json.load(f)
            return {ev: list(cfg.get(ev, [])) for ev in EVENTS}
        except Exception:
            pass

    # Fall back: scan ~/.pw-agent/hooks/ for files matching event names
    config: dict[str, list[str]] = {ev: [] for ev in EVENTS}
    if not os.path.isdir(DEFAULT_HOOKS_DIR):
        return config

    try:
        for fname in sorted(os.listdir(DEFAULT_HOOKS_DIR)):
            full = os.path.join(DEFAULT_HOOKS_DIR, fname)
            if not os.path.isfile(full) or not os.access(full, os.X_OK):
                continue
            base = os.path.splitext(fname)[0]
            if base in EVENTS:
                config[base].append(full)
    except OSError:
        pass

    return config


def _expand(path: str) -> str:
    return os.path.expanduser(path)


def run_hook(event: str, payload: dict, timeout: int = 10) -> tuple[bool, str]:
    """Fire all hooks for an event. Returns (allowed, combined_stdout).

    allowed=False means at least one pre_tool_use or user_prompt_submit
    hook returned exit code 2 — caller should block the action.
    """
    if event not in EVENTS:
        return True, ""

    config = _load_hooks_config()
    hooks = [_expand(h) for h in config.get(event, [])]
    if not hooks:
        return True, ""

    payload_json = json.dumps(payload) if payload else ""
    combined_out = []
    allowed = True

    for hook in hooks:
        if not os.path.exists(hook):
            continue
        try:
            result = subprocess.run(
                [hook],
                input=payload_json,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            if result.stdout:
                combined_out.append(result.stdout.strip())
            if result.returncode == 2 and event in ("pre_tool_use", "user_prompt_submit"):
                allowed = False
                if result.stderr:
                    combined_out.append(f"[hook block]: {result.stderr.strip()}")
        except subprocess.TimeoutExpired:
            combined_out.append(f"[hook timeout]: {os.path.basename(hook)}")
        except Exception as e:
            combined_out.append(f"[hook error]: {os.path.basename(hook)} — {e}")

    return allowed, "\n".join(combined_out)


def list_hooks() -> dict[str, list[str]]:
    """Return the active hook config for inspection."""
    return _load_hooks_config()
