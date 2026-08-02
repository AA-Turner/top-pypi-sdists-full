"""PreToolUse hook: deny a Bash command that would print a secret in clear text.

Codex hooks are global (``~/.codex/config.toml``), not per-skill, so this is the
Codex-side equivalent of the per-skill PreToolUse hook Claude carries in the
``aws-secrets`` SKILL.md frontmatter — a guardrail against ``echo``/``cat``/``printf``
of a resolved secret. It reads the PreToolUse event JSON on stdin (see the Codex
hooks contract) and, on a match, prints the ``permissionDecision: deny`` shape.

Deliberately narrow: the same proven patterns the Claude hook uses, so a global
always-on guard almost never blocks legitimate work. Any input it cannot parse
is allowed (fail-open) — a broken guard must not wedge every Bash call.
"""

import json
import re
import sys

import typer

# Same intent as the aws-secrets SKILL.md hook: block obvious prints of a resolved secret.
_LEAK_PATTERNS = re.compile(
    r"echo.*SECRET|echo.*MGMT|cat.*/tmp/aws_secret|print.*secret_value|printf.*SECRET",
    re.IGNORECASE,
)

_DENY_REASON = "Potential secret leak blocked: never echo, cat, or print a resolved secret value."


def _bash_command(event: object) -> str | None:
    """The Bash command string of a PreToolUse event, or ``None`` when the event is not a
    Bash tool call or carries no command (both mean "nothing to scan → allow")."""
    if not isinstance(event, dict) or event.get("tool_name") != "Bash":
        return None
    tool_input = event.get("tool_input")
    if not isinstance(tool_input, dict):
        return None
    command = tool_input.get("command")
    return command if isinstance(command, str) else None


def main() -> None:
    """Read a PreToolUse event on stdin; emit the deny decision when the Bash command
    would leak a secret, otherwise stay silent (allow)."""
    try:
        event = json.loads(sys.stdin.read())
    except (json.JSONDecodeError, ValueError):
        return  # fail-open: unparseable input must not block the agent loop
    command = _bash_command(event)
    if command is None or not _LEAK_PATTERNS.search(command):
        return
    decision = {
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": _DENY_REASON,
        }
    }
    typer.echo(json.dumps(decision))


if __name__ == "__main__":
    typer.run(main)
