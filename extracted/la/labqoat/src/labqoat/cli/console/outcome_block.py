"""How a run ended, why, and what to do next."""

import textwrap
from typing import ClassVar

import click

from labqoat.cli.console.failure_advice import FailureAdvice
from labqoat.cli.console.stage_board import StageBoard
from labqoat.json_document import JsonDocument


class OutcomeBlock:
    """Close a terminal run with one bold verdict; an unsuccessful one adds its cause and next steps."""

    marks: ClassVar[dict[str, tuple[str, str]]] = {
        "completed": ("✓", "green"),
        "completed_with_errors": ("⚠", "yellow"),
        "cancelled": ("■", "yellow"),
        "failed": ("✗", "red"),
    }

    @classmethod
    def lines(cls, run: JsonDocument, child: str, link: str) -> list[str]:
        """The verdict with time executing and time since submission, then cause and hints when it went wrong."""
        status = str(run["status"])
        mark, color = cls.marks[status]
        verdict = click.style(f"{mark} {status.replace('_', ' ').capitalize()}", fg=color, bold=True)
        lines = ["", f"{verdict}{cls.timing(run)}"]
        if status == "completed":
            return lines + cls.reminder(run, link)
        lines.extend(f"  {line}" for line in cls.cause(run))
        hints = cls.hints(run, child, link)
        for index, (label, value) in enumerate(hints):
            branch = "└─" if index == len(hints) - 1 else "├─"
            lines.append(f"  {click.style(branch, dim=True)} {click.style(label.ljust(6), dim=True)} {value}")
        return lines

    @staticmethod
    def reminder(run: JsonDocument, link: str) -> list[str]:
        """After a long run its header has scrolled away, so the page link is shown again."""
        start, end = run.get("inserted_at") or run.get("started_at"), run.get("ended_at")
        if not link or not isinstance(start, str) or not isinstance(end, str):
            return []
        seconds = (StageBoard.instant_of(end) - StageBoard.instant_of(start)).total_seconds()
        return [click.style(f"  {link}", dim=True)] if seconds >= 60 else []

    @staticmethod
    def timing(run: JsonDocument) -> str:
        """Execution time, and the whole wait since submission when that is longer."""
        end = run.get("ended_at")
        ran = OutcomeBlock.between(run.get("started_at"), end)
        total = OutcomeBlock.between(run.get("inserted_at"), end)
        text = f" in {ran}" if ran else ""
        return text + (click.style(f"  ·  {total} total", dim=True) if total and total != ran else "")

    @staticmethod
    def between(start: object, end: object) -> str:
        """A short duration between two retained instants, or nothing when either is missing."""
        if not isinstance(start, str) or not isinstance(end, str):
            return ""
        opened = StageBoard.instant_of(start)
        closed = StageBoard.instant_of(end)
        return StageBoard.span((closed - opened).total_seconds())

    @staticmethod
    def cause(run: JsonDocument) -> list[str]:
        """The retained explanation, with a source location on its own line."""
        detail = run.get("failure_detail")
        detail = detail if isinstance(detail, dict) else {}
        text = str(detail.get("detail") or detail.get("reason") or "")
        message, _, location = text.partition(" at ")
        lines = textwrap.wrap(message, width=96, subsequent_indent="  ")
        return lines + ([f"  at {location}"] if location else [])

    @staticmethod
    def hints(run: JsonDocument, child: str, link: str) -> list[tuple[str, str]]:
        """Point at the failed descendant, the diagnostic command and the page for this run."""
        rows = [("child", child)] if child else []
        if run.get("kind") == "group" and run["status"] == "cancelled":
            rows.append(("stop", f"lab run cancel {run.get('id')}  (what it started is still running)"))
        for line in FailureAdvice.lines(run):
            label, _, command = line.partition(": ")
            rows.append(("next", command or label))
        return rows + ([("open", link)] if link else [])
