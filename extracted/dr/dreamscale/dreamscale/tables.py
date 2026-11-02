"""The one table every `dreamscale … list` prints.

A bold title with a dim count, a dim header over a single rule, one fact per column, and a
dim hint naming the next command. States read the same everywhere (`status`): green for
ready, yellow for under way, grey for resting, red for broken.

On a terminal narrower than the table, the columns with the highest `drop` rank leave whole,
never cut mid-word; only a `shrink` column (free text such as a run's name) shortens, with an
ellipsis. Piped output keeps every column, uncoloured, so it greps the same.
"""

from __future__ import annotations

import io
import re
import shutil
import sys
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

from rich import box
from rich.console import Console
from rich.measure import Measurement
from rich.table import Table
from rich.text import Text

DIM = "bright_black"
BRAND = "#00ffd1"
# What a state means to the reader, whatever the list: (mark, colour).
KINDS = {
    "ok": ("●", "green"),       # ready, running
    "active": ("●", "yellow"),  # starting, building, training, busy, queued
    "idle": ("○", DIM),         # cold start, canceled, stopped, closed
    "bad": ("●", "red"),        # failed, unavailable
}
# Wide enough that nothing drops or shortens when output isn't a terminal.
UNLIMITED = 10_000
_TRAILING = re.compile(r"[ \t]+((?:\x1b\[[0-9;]*m)*)$")


@dataclass(frozen=True)
class Column:
    header: str
    drop: int = 0  # 0 never drops; on a narrow terminal the highest rank goes first
    justify: str = "left"
    style: str = ""
    shrink: bool = False


def status(word: str, kind: str, detail: str = "") -> Text:
    """`● Ready`, `● Training · ~2 h 10 m left`: the mark and word in the kind's colour."""
    mark, colour = KINDS[kind]
    text = Text(f"{mark} {word}", style=colour)
    if detail:
        text.append(f" · {detail}", style=DIM)
    return text


def dim(value: str) -> Text:
    return Text(value, style=DIM)


def none() -> Text:
    """An empty cell."""
    return dim("—")


def command(value: str) -> Text:
    return Text(value, style="cyan")


def hint(*parts: str | Text) -> Text:
    """A footer line: plain strings dim, `command(...)` cyan."""
    line = Text()
    for part in parts:
        line.append_text(part if isinstance(part, Text) else dim(part))
    return line


class _Table:
    def __init__(self, columns: Sequence[Column], rows: Sequence[Sequence], sections: set[int]):
        self.columns = columns
        self.rows = [[_text(cell) for cell in row] for row in rows]
        self.sections = sections

    def build(self, keep: list[int], shrink_to: int | None = None) -> Table:
        table = Table(box=box.SIMPLE_HEAD, header_style=f"bold {DIM}", show_edge=False,
                      pad_edge=False, padding=(0, 2, 0, 0), collapse_padding=True)
        for i in keep:
            column = self.columns[i]
            table.add_column(
                column.header, justify=column.justify, style=column.style or None,
                no_wrap=True, overflow="ellipsis" if column.shrink else "fold",
                max_width=shrink_to if column.shrink else None,
            )
        for index, row in enumerate(self.rows):
            table.add_row(*(row[i] for i in keep), end_section=index in self.sections)
        return table

    def fit(self, console: Console, width: int) -> Table:
        def measured(table: Table) -> int:
            return Measurement.get(console, console.options.update(width=UNLIMITED),
                                   table).maximum

        keep = list(range(len(self.columns)))
        for i in sorted((i for i in keep if self.columns[i].drop),
                        key=lambda i: -self.columns[i].drop):
            if measured(self.build(keep)) <= width:
                break
            keep.remove(i)
        table = self.build(keep)
        over = measured(table) - width
        shrinkable = [i for i in keep if self.columns[i].shrink]
        if over > 0 and shrinkable and self.rows:
            longest = max(row[shrinkable[0]].cell_len for row in self.rows)
            table = self.build(keep, shrink_to=max(12, longest - over))
        return table


def _text(cell) -> Text:
    if isinstance(cell, Text):
        return cell
    return none() if cell is None or cell == "" else Text(str(cell))


def render(
    title: str,
    detail: str,
    columns: Sequence[Column],
    rows: Sequence[Sequence],
    *,
    footer: Iterable[Text] = (),
    sections: Iterable[int] = (),
    color: bool | None = None,
    width: int | None = None,
) -> list[str]:
    """The list as lines for `print_fn`: title, table, then each footer line.

    `sections` are the row indexes a rule follows (the end of a group). Colour and width
    follow stdout: a terminal gets both, a pipe neither.
    """
    terminal = sys.stdout.isatty()
    color = terminal if color is None else color
    if width is None:
        width = shutil.get_terminal_size().columns if terminal else UNLIMITED
    out = io.StringIO()
    console = Console(file=out, width=UNLIMITED, force_terminal=color,
                      color_system="auto" if color else None, highlight=False,
                      legacy_windows=False)
    heading = Text(title, style="bold")
    if detail:
        heading.append(f"  {detail}", style=DIM)
    console.print(heading)
    console.print()
    console.print(_Table(columns, rows, set(sections)).fit(console, width))
    footer = list(footer)
    if footer:
        console.print()
        for line in footer:
            console.print(line, width=width, soft_wrap=False)
    return [_TRAILING.sub(r"\1", line) for line in out.getvalue().rstrip("\n").split("\n")]
