"""Tables and fact sheets for a person at a terminal."""

from datetime import UTC, datetime
from typing import IO, TYPE_CHECKING, ClassVar

from labqoat.cli.output.field_text import FieldText
from labqoat.cli.output.resource_view import ResourceView
from labqoat.cli.output.view_column import ViewColumn
from labqoat.json_document import JsonValue

if TYPE_CHECKING:
    from rich.console import RenderableType
    from rich.text import Text


class PrettyWriter:
    """Draw quiet tables with colored states, short identifiers and relative times."""

    styles: ClassVar[dict[str, str]] = {
        "completed": "green",
        "succeeded": "green",
        "ready": "green",
        "available": "green",
        "pass": "green",
        "ok": "green",
        "running": "cyan",
        "starting": "cyan",
        "building": "cyan",
        "preparing": "cyan",
        "queued": "yellow",
        "pending": "yellow",
        "draining": "yellow",
        "warn": "yellow",
        "failed": "red",
        "fail": "red",
        "cancelled": "red",
        "terminated": "bright_black",
    }

    def __init__(self, stream: IO[str], *, color: bool = True) -> None:
        """Retain the destination and whether color was declined."""
        self._stream = stream
        self._color = color
        self._now = datetime.now(UTC)

    def write(self, view: ResourceView) -> None:
        """A table for rows, a fact sheet for a record, and a count so an empty page is not silent."""
        from rich.console import Console

        console = Console(file=self._stream, highlight=False, no_color=not self._color)
        if view.rows is not None:
            console.print(self.table(view))
            console.print(f"[bright_black]{len(view.rows)} shown · --json for every field[/]")
        if view.facts:
            console.print(self.sheet(view))

    def table_only(self, view: ResourceView) -> None:
        """Rows without a footer, for values that are complete as shown."""
        from rich.console import Console

        Console(file=self._stream, highlight=False, no_color=not self._color).print(self.table(view))

    def table(self, view: ResourceView) -> "RenderableType":
        """One row per resource under dim headers, without borders."""
        from rich import box
        from rich.table import Table

        table = Table(box=box.SIMPLE_HEAD, header_style="bold bright_black", pad_edge=False, show_edge=False)
        for column in view.columns:
            table.add_column(column.header, no_wrap=column.kind in ("id", "status", "time"))
        for row in view.rows or []:
            table.add_row(*(self.cell(column, row) for column in view.columns))
        return table

    def sheet(self, view: ResourceView) -> "RenderableType":
        """Dim labels beside their values, with the members of each nested object under its name."""
        from rich.table import Table

        grid = Table.grid(padding=(0, 2))
        grid.add_column(style="bright_black")
        grid.add_column()
        section = ""
        for fact in view.facts:
            group, _, label = fact.header.rpartition(".")
            if group != section:
                grid.add_row("", "")
                grid.add_row(f"[bold]{group.replace('_', ' ')}[/]", "")
                section = group
            grid.add_row(("  " if group else "") + label.replace("_", " "), self.cell(fact, view.record, short=False))
        return grid

    def cell(self, column: ViewColumn, document: JsonValue, *, short: bool = True) -> "Text":
        """Style a value by its role; a fact sheet keeps identifiers whole so they can be copied."""
        from rich.text import Text

        value = column.value(document)
        kind = "text" if column.kind == "id" and not short else column.kind
        text = FieldText.pretty(value, kind, self._now)
        if column.kind == "status":
            return Text("● " + text, style=self.styles.get(text, ""))
        return Text(text, style="bright_black" if text == "-" or column.kind in ("id", "time") else "")
