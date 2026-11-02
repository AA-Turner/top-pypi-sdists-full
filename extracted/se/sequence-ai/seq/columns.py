"""
A table's columns as wide as what they hold: each its widest cell - its heading's among them - and two spaces more, so no
two columns ever run together however long a value is (a card's name, a weights URI), and none is cut short to fit. The
last column is left as it is.


"""
from __future__ import annotations

from typing import Sequence

GAP = 2


def widths(rows: Sequence[Sequence[str]], gap: int = GAP) -> list[int]:
    """Each column's width over `rows` - the heading's row among them: its widest cell and `gap` more."""
    count = max((len(row) for row in rows), default=0)
    return [max((len(str(row[i])) for row in rows if i < len(row)), default=0) + gap for i in range(count)]


def line(cells: Sequence[str], widths: Sequence[int]) -> str:
    """One row: each cell but the last padded to its column's width, the last as it is."""
    if not cells:
        return ""
    return "".join(f"{str(c):{w}}" for c, w in zip(cells[:-1], widths)) + str(cells[-1])
