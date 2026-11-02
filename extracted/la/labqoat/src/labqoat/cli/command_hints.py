"""Point a mistyped or guessed command at the one that does what was meant."""

import re
from typing import ClassVar

import click


class CommandHints:
    """Names agents reach for that the CLI spells differently, by the group they were typed under."""

    HINTS: ClassVar[dict[tuple[str, str], str]] = {
        ("", "query"): "lab dataset query DATASET QUERY_JSON",
        ("", "analytics"): "lab dataset query DATASET QUERY_JSON",
        ("", "costs"): "lab project budget show, or lab run attempts list RUN for one run's cost",
        ("", "budget"): "lab project budget show",
        ("", "logs"): "lab run logs RUN",
        ("", "gpus"): "lab compute offerings",
        ("", "hardware"): "lab compute offerings",
        ("", "offerings"): "lab compute offerings",
        ("memory", "hypothesis"): "lab memory node create --type hypothesis",
        ("run", "children"): "lab run list --owner RUN",
        ("run", "files"): "lab run assets RUN",
        ("run", "artifacts"): "lab run assets RUN",
        ("run", "costs"): "lab run attempts list RUN (cost per attempt)",
        ("run", "budget"): "lab run attempts list RUN (cost per attempt), or lab project budget show",
        ("memory", "note"): "lab memory node create --type note, or lab memory publish step.json",
        ("memory", "add"): "lab memory node create, or lab memory publish step.json",
        ("memory", "step"): "lab memory publish step.json",
        ("memory", "get"): "lab memory node show NODE",
        ("memory", "show"): "lab memory node show NODE",
        ("memory", "status"): "lab memory set-status",
        (
            "experiment",
            "status",
        ): "lab memory attention (finished, untested and undecided work), or lab memory node show NODE",
        ("experiment", "list"): "lab memory attention, or lab memory search QUERY",
    }

    @staticmethod
    def explain(error: click.ClickException) -> str:
        """The error's message, followed by the command meant when the typed name is a known guess."""
        message = error.format_message()
        typed = re.match(r"No such command '([^']+)'", message)
        context = getattr(error, "ctx", None)
        if typed is None or context is None:
            return message
        group = context.info_name if context.parent is not None else ""
        hint = CommandHints.HINTS.get((group or "", typed.group(1)))
        if hint:
            return f"{message} Use: {hint}."
        siblings = CommandHints.siblings(context)
        if siblings:
            return f"{message} Commands in {context.command_path}: {', '.join(siblings)}."
        related = CommandHints.related(context.find_root().command, typed.group(1))
        return f"{message} Related: {', '.join(related)}." if related else message

    @staticmethod
    def siblings(context: click.Context) -> list[str]:
        """A small subgroup's own commands, which are what a mistyped name under it was looking for."""
        command = context.command
        if context.parent is None or not isinstance(command, click.Group) or len(command.commands) > 12:
            return []
        return [name for name, child in command.commands.items() if not child.hidden]

    @staticmethod
    def related(root: click.Command, word: str) -> list[str]:
        """Up to three commands whose name or help mentions the typed word (four letters or more)."""
        stem = word.lower()[:6]
        if len(stem) < 4:
            return []
        matches = [
            path for path, words in CommandHints.leaves(root, "lab", "") if any(w.startswith(stem) for w in words)
        ]
        return sorted(matches, key=len)[:3]

    @staticmethod
    def leaves(command: click.Command, path: str, context: str) -> list[tuple[str, list[str]]]:
        """Every runnable command with the words of its path, its help and its group's help."""
        text = f"{context} {command.help or ''}"
        if not isinstance(command, click.Group):
            return [(path, re.findall(r"[a-z]+", f"{path} {text}".lower()))]
        found: list[tuple[str, list[str]]] = []
        for name, child in command.commands.items():
            if not child.hidden:
                found.extend(CommandHints.leaves(child, f"{path} {name}", text))
        return found
