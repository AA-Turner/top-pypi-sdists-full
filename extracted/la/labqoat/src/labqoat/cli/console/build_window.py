"""A bounded live build window that collapses when the build phase ends."""

import sys
from datetime import datetime
from typing import TYPE_CHECKING
from labqoat.cli.console.child_overview import ChildOverview
from labqoat.cli.console.console_entry import ConsoleEntry
from labqoat.cli.console.stage_status import StageStatus

if TYPE_CHECKING:
    from rich.console import RenderableType
    from rich.live import Live


class BuildWindow:
    """Redraw on incoming evidence, keep an open stage's clock moving, and leave redirected output append-only."""

    def __init__(self, *, records: bool = False) -> None:
        """Delay Rich imports and terminal allocation until output actually arrives.

        ``records``: the lines are what the command was asked to print (reading logs), so they go to stdout;
        otherwise they narrate other work and go to stderr.
        """
        self.records = records
        self.live: Live | None = None
        self.finished = False
        self.owner: str | None = None
        self.lines: list[str] = []
        self.children = ChildOverview()
        self.status: StageStatus | None = None
        self.samples: list[str] = []

    def measure(self, samples: list[str]) -> None:
        """Show the newest metric samples under the current stage."""
        self.samples = samples[-4:]
        if sys.stderr.isatty() and self.live is not None:
            self.draw()

    def stage(self, label: str | None, since: datetime | None = None) -> None:
        """Show the run's current stage above builder output, or stop showing one."""
        self.status = None if label is None else StageStatus(label, since)
        if not sys.stderr.isatty():
            return
        if self.status is not None:
            self.draw()
        elif self.live is not None and not self.lines and not self.children.rows:
            self.close()
        elif self.live is not None:
            self.draw()

    def update(self, lines: list[str], *, owner: str = "") -> None:
        """Show the most recent five build lines in a real terminal."""
        if not sys.stderr.isatty():
            return
        if owner != self.owner:
            self.close()
            self.finished = False
        self.owner = owner
        if self.finished:
            return
        self.lines = lines[-5:]
        self.draw()

    def child(self, entry: ConsoleEntry) -> None:
        """Refresh descendant rows on incoming evidence without creating a polling timer."""
        if sys.stderr.isatty() and self.children.accept(entry):
            self.draw()

    def draw(self) -> None:
        """Share one live region between builder output and child-run status rows."""
        from rich.console import Console
        from rich.console import Group
        from rich.live import Live
        from rich.text import Text

        title = [] if self.status is not None else ["Building image"]
        build = Text("\n".join(title + ["  │ " + line for line in self.lines])) if self.lines else Text("")
        parts: list[RenderableType] = [] if self.status is None else [self.status]
        if self.samples:
            parts.append(Text("\n".join(f"    · {sample}" for sample in self.samples), style="bright_black"))
        if self.lines:
            parts.append(build)
        if self.children.rows:
            parts.append(self.children.table())
        text = Group(*parts)
        moving = self.status is not None
        if self.live is not None and self.live.auto_refresh != moving:
            self.live.stop()
            self.live = None
        if self.live is None:
            self.live = Live(text, console=Console(stderr=True), transient=True, auto_refresh=moving)
            self.live.start()
        self.live.update(text, refresh=True)

    def collapse(self) -> None:
        """Hide completed builder output while keeping the descendant overview live."""
        self.lines = []
        self.finished = True
        if self.children.rows or self.status is not None:
            self.draw()
        else:
            self.close()

    def write(self, text: str) -> None:
        """Print above the active region so an arriving diagnostic never corrupts the table."""
        import click

        if self.live is None:
            click.echo(text, err=not self.records)
        else:
            from rich.text import Text

            self.live.console.print(Text.from_ansi(text), highlight=False)

    def close(self) -> None:
        """Restore the terminal after completion, disconnect, or interruption."""
        self.finished = True
        if self.live is not None:
            self.live.stop()
            self.live = None
