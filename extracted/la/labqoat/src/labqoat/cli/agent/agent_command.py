"""``lab agent``: what Claude Code, Codex and opencode hooks run to keep agents on Labqoat's tools."""

import json
import sys
from pathlib import Path

import click

from labqoat.cli.agent.agent_rules import AgentRules
from labqoat.cli.agent.command_check import CommandCheck
from labqoat.cli.group_help import GroupHelp
from labqoat.cli.strict_command import StrictCommand


class AgentCommand:
    """Hook entry points that read the hook's JSON on stdin and answer in the shape every agent accepts."""

    @staticmethod
    def brief(event: str | None) -> None:
        """Print the rules card, as hook context for ``event`` or as plain text."""
        text = AgentRules.brief(Path.cwd())
        if event is None:
            click.echo(text)
            return
        click.echo(json.dumps({"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}))

    @staticmethod
    def check() -> None:
        """Answer a PreToolUse hook: refuse a command that breaks the rules, or add a note to one that bends them."""
        try:
            hook = json.loads(sys.stdin.read() or "{}")
        except json.JSONDecodeError:
            return
        tool = hook.get("tool_input") if isinstance(hook, dict) else None
        command = tool.get("command") if isinstance(tool, dict) else None
        verdict = CommandCheck.verdict(command) if isinstance(command, str) else None
        if verdict is None:
            return
        answer: dict[str, str] = {"hookEventName": "PreToolUse"}
        if verdict.refused:
            answer |= {"permissionDecision": "deny", "permissionDecisionReason": verdict.reason}
        else:
            answer["additionalContext"] = verdict.reason
        click.echo(json.dumps({"hookSpecificOutput": answer}))

    @staticmethod
    def as_click_command() -> click.Group:
        """The ``agent`` group with ``brief`` and ``check``."""
        group = click.Group(
            "agent",
            help="Rules and command checks for coding-agent hooks (installed by `lab init`).",
            callback=GroupHelp.show,
            invoke_without_command=True,
        )
        event = click.Option(["--event"], help="Answer as hook context for this event, such as SessionStart.")
        group.add_command(
            StrictCommand(
                "brief", callback=AgentCommand.brief, params=[event], help="Print this project's rules for agents."
            )
        )
        group.add_command(
            StrictCommand("check", callback=AgentCommand.check, help="Check a PreToolUse hook's command on stdin.")
        )
        return group
