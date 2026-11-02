"""Text of one console record for a person at a terminal or an agent reading a pipe."""

from typing import ClassVar

import click

from labqoat.cli.console.console_entry import ConsoleEntry


class ConsoleLine:
    """People get symbols and color; agents get a leading word that says what the line is."""

    tags: ClassVar[dict[str, str]] = {
        "stdout": "out",
        "stderr": "err",
        "logging": "log",
        "metric": "metric",
        "milestone": "mark",
        "progress": "stage",
        "build": "build",
    }
    colors: ClassVar[dict[str, str]] = {"✓": "green", "✗": "red", "⚠": "yellow", "▸": "cyan", "◆": "magenta"}

    def __init__(self, style: str, *, gutter: bool = False) -> None:
        """Retain the presentation chosen for this observer's diagnostic stream."""
        self.compact = style == "compact"
        self.gutter = gutter

    def lines(self, entry: ConsoleEntry, prefix: str) -> list[str]:
        """One line per record line, attributed to its descendant and continued without repeating the lead."""
        path = entry.path()
        first, *rest = entry.content.splitlines() or [""]
        if self.compact:
            lead = " ".join(part for part in (prefix.strip(), self.tag(entry), path) if part)
            return [f"{lead} {first}".rstrip(), *(f"  | {line}" for line in rest)]
        if self.gutter:
            return self.framed(entry, path, [first, *rest])
        label = f"{path}  " if path else ""
        symbol = entry.symbol()
        mark = click.style(symbol, fg=self.colors.get(symbol), bold=symbol in self.colors)
        lead = click.style(f"{prefix}{label}", dim=True) if prefix or label else ""
        return [f"{lead}{mark} {first}", *(f"{prefix}{label}  │ {line}" for line in rest)]

    def framed(self, entry: ConsoleEntry, path: str, lines: list[str]) -> list[str]:
        """Beside a checklist, program output sits behind a dim rule and reports are dim asides."""
        symbol = entry.symbol()
        if entry.kind and not path:
            return [click.style(f"    · {line}", dim=True) for line in lines]
        mark = (
            click.style("  │ ", dim=True) if symbol == " " else click.style(f"  {symbol} ", fg=self.colors.get(symbol))
        )
        label = click.style(f"{path}  ", dim=True) if path else ""
        return [f"{mark}{label}{line}" for line in lines]

    @classmethod
    def tag(cls, entry: ConsoleEntry) -> str:
        """Outcome and severity come first, then the stream, then lifecycle stages."""
        if entry.group() and entry.document.get("run_path"):
            return "group"
        if entry.terminal:
            return "done"
        if entry.level in ("error", "critical", "warning"):
            return "warn" if entry.level == "warning" else "error"
        if entry.kind:
            return "debug" if entry.level == "debug" else "stage"
        return cls.tags.get(entry.source, "out")
