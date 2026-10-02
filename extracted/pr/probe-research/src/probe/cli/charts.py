"""Metric curves drawn where the metrics are already read: the terminal.

`probe metrics wide` has always returned the step x metric table. What it could
not do is let you SEE it -- so the fast question ("is the loss actually moving?")
had to leave the terminal you were already in, for a browser or a plotting
script. This module answers it in place.

Two renderings, because there are two questions:

  a BOARD   one sparkline per series -- the whole run at a glance, every key
  a PANEL   one metric on a full canvas, with axes and tick labels

The panel draws with braille (U+28xx), which packs a 2x4 subpixel grid into a
single character cell: an 80x12 block of terminal holds a 160x48 curve. When a
panel carries MORE than one series that resolution is spent on identity
instead -- a marker grid, one glyph per series -- because color alone does not
survive a pipe, a monochrome terminal, a `script` capture, or a reader with a
color vision deficiency. Color rides along as a second encoding, never the only
one, and a legend is drawn whenever there is more than one series to name.

Two deliberate limits:

  ONE AXIS.  Overlaid series share a single y-scale. A second scale drawn on
  the same canvas makes any two curves cross wherever the author chose, which
  is a picture of the scaling, not of the data. Metrics on different scales get
  a panel each -- which is what the default does.

  NO INTERPOLATION ACROSS ABSENCE, but no gaps either: a series is its finite
  points and the line connects them. A key logged every tenth step sits in a
  wide table with nine holes between values; those holes are the pivot's, not
  the metric's, and drawing them as breaks would make every sparse metric look
  like a series of crashes.

Stdlib only, like tui.py -- `probe log` must not pay an import for a drawing
surface it never touches.
"""

from __future__ import annotations

import math
import os
import sys
import unicodedata
from collections import Counter
from collections.abc import Iterator, Sequence
from typing import NamedTuple

#: Braille dot bit for (subcolumn, subrow) inside one 2x4 cell. The dots are
#: numbered 1,2,3,7 down the left and 4,5,6,8 down the right -- an ordering
#: inherited from six-dot braille, which is why the bottom row is not 4 and 8's
#: neighbours but a pair bolted on at 0x40/0x80.
_DOT = ((0x01, 0x02, 0x04, 0x40), (0x08, 0x10, 0x20, 0x80))
_BRAILLE_BASE = 0x2800

#: Per-series glyphs for the marker canvas, in fixed order. ASCII on purpose:
#: this is the encoding that has to work when nothing else does.
_GLYPHS = ("o", "x", "+", "*", "#", "@")

#: Owner of a cell more than one series landed on. Not a series index: the cell
#: belongs to no single curve, and drawing one of them there would report an
#: overlap as an absence.
SHARED = -1
_SHARED_GLYPH = "%"


def glyph_for(series: int) -> str:
    return _SHARED_GLYPH if series == SHARED else _GLYPHS[series % len(_GLYPHS)]

#: ANSI foreground codes, in fixed order, assigned by series position and never
#: cycled. Six, because a seventh series on one canvas is unreadable however it
#: is colored -- the caller is told what it dropped rather than being handed a
#: repeated hue. These are the terminal's own palette slots, so the actual hues
#: come from the reader's theme: they cannot be validated for contrast here,
#: which is the other reason identity lives in the glyph.
_COLORS = ("36", "33", "32", "35", "34", "31")
_DIM = "2"

#: How many series one canvas will carry before the rest are refused.
MAX_OVERLAY = len(_GLYPHS)

#: Sparkline levels, low to high.
_BLOCKS = "▁▂▃▄▅▆▇█"

#: Axis furniture: (tick, wall, corner, rule), by whether unicode is safe.
_AXIS = {True: ("┤", "│", "└", "─"), False: ("+", "|", "+", "-")}


class Series(NamedTuple):
    """One curve: a label and its finite (x, y) points, x ascending.

    ``dropped`` counts the points that were NOT finite. They cannot be given a
    row on any scale, but a NaN in a loss curve is the single most important
    thing a training run ever logs -- dropping it without a word turns a run
    that diverged into a run that looks healthy. The count travels with the
    curve so every surface can say it.

    Today's backend renders JSON with `allow_nan=False`, so a stored NaN raises
    THERE rather than arriving here; the client's `json.loads` accepts a bare
    `NaN` literal, so this stays the boundary that any other producer meets.
    """

    label: str
    points: Sequence[tuple[float, float]]
    dropped: int = 0


# -- terminal capabilities ----------------------------------------------------


def columns(default: int = 80) -> int:
    """Terminal width, or a sane default when there is no terminal."""
    import shutil

    try:
        return shutil.get_terminal_size((default, 24)).columns
    except OSError:
        return default


def use_color(explicit: bool | None = None) -> bool:
    """Color only where it can be seen, and never against the reader's wishes.

    A pipe gets none: escape codes in a captured chart are noise every consumer
    has to strip. ``NO_COLOR`` (any value) is honored because it is the one
    cross-tool spelling of "I do not want this".
    """
    if explicit is not None:
        return explicit
    if os.environ.get("NO_COLOR") is not None:
        return False
    if os.environ.get("TERM") == "dumb":
        return False
    return sys.stdout.isatty()


def use_unicode(explicit: bool | None = None) -> bool:
    """Whether the braille and box-drawing glyphs can survive the encoding.

    Asked of the actual stream rather than assumed: a chart of mojibake is
    strictly worse than the ASCII fallback, and the encoding is knowable.
    """
    if explicit is not None:
        return explicit
    encoding = getattr(sys.stdout, "encoding", None) or ""
    try:
        "⠿…┤".encode(encoding or "ascii")
    except (LookupError, UnicodeEncodeError):
        return False
    return True


def _paint(text: str, code: str | None, color: bool) -> str:
    return f"\033[{code}m{text}\033[0m" if color and code else text


# -- numbers ------------------------------------------------------------------


def fmt(value: float) -> str:
    """Four significant digits, without exponent theatre for ordinary numbers.

    ``%g`` alone gives `1e-09` for a plain zero-ish loss and `0.0342` for a
    reasonable one, which is right -- but it also gives `1.234e+05` for a step
    count, so the ordinary band is pinned to fixed notation first.
    """
    if value == 0:
        return "0"
    if not math.isfinite(value):
        return "nan" if math.isnan(value) else ("inf" if value > 0 else "-inf")
    magnitude = abs(value)
    if magnitude >= 1e6 or magnitude < 1e-3:
        return f"{value:.3e}"
    return f"{value:.4g}"


def _fmt_x(value: float) -> str:
    """Steps are integers in every producer we have; print them as such."""
    return str(int(value)) if float(value).is_integer() else fmt(value)


# -- canvases -----------------------------------------------------------------


def _walk(x0: int, y0: int, x1: int, y1: int) -> Iterator[tuple[int, int]]:
    """Every integer pixel on the segment (Bresenham, all octants).

    Segments, not scattered points: at 2x4 subpixels a 50-step curve leaves 50
    marks in 160 columns, which reads as a dot plot rather than a line. The
    connecting walk is what makes a shape out of them.
    """
    dx, dy = abs(x1 - x0), -abs(y1 - y0)
    step_x = 1 if x0 < x1 else -1
    step_y = 1 if y0 < y1 else -1
    err = dx + dy
    while True:
        yield x0, y0
        if x0 == x1 and y0 == y1:
            return
        double = 2 * err
        if double >= dy:
            err += dy
            x0 += step_x
        if double <= dx:
            err += dx
            y0 += step_y


class _Canvas:
    """A subpixel grid that collapses to one character per cell.

    Subclasses differ only in how many subpixels a cell holds and what a marked
    cell prints; the mapping from data space is shared, so a panel's geometry
    does not change when the renderer does.
    """

    sub_x = 1
    sub_y = 1

    def __init__(self, width: int, height: int) -> None:
        self.width, self.height = width, height
        self.px = width * self.sub_x
        self.py = height * self.sub_y

    def mark(self, x: int, y: int, series: int) -> None:  # pragma: no cover - interface
        raise NotImplementedError

    def rows(self) -> list[list[tuple[str, int | None]]]:  # pragma: no cover - interface
        raise NotImplementedError

    def draw(self, points: Sequence[tuple[int, int]], series: int) -> None:
        if len(points) == 1:
            self.mark(points[0][0], points[0][1], series)
            return
        for (x0, y0), (x1, y1) in zip(points, points[1:]):
            for x, y in _walk(x0, y0, x1, y1):
                self.mark(x, y, series)


class _Braille(_Canvas):
    """Highest fidelity, one series: 8 subpixels per cell, no identity to spare."""

    sub_x, sub_y = 2, 4

    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self._cells = [[0] * width for _ in range(height)]

    def mark(self, x: int, y: int, series: int) -> None:
        if 0 <= x < self.px and 0 <= y < self.py:
            self._cells[y // 4][x // 2] |= _DOT[x % 2][y % 4]

    def rows(self) -> list[list[tuple[str, int | None]]]:
        return [
            [("".join(chr(_BRAILLE_BASE + bits) for bits in row), 0 if any(row) else None)]
            for row in self._cells
        ]


class _Markers(_Canvas):
    """One cell, one series: the glyph carries identity, color merely repeats it.

    First writer keeps the cell. Overlap has to resolve somehow and "the series
    the legend names first" would be a rule a reader could learn -- but it is not
    one they can SEE, and two curves that coincide would then draw as one while
    the legend went on naming both. A contested cell gets its own glyph instead,
    so overlap is a thing on the screen rather than a series that vanished.
    """

    def __init__(self, width: int, height: int) -> None:
        super().__init__(width, height)
        self._cells: list[list[int | None]] = [[None] * width for _ in range(height)]

    def mark(self, x: int, y: int, series: int) -> None:
        if not (0 <= x < self.px and 0 <= y < self.py):
            return
        owner = self._cells[y][x]
        if owner is None:
            self._cells[y][x] = series
        elif owner != series:
            self._cells[y][x] = SHARED

    def rows(self) -> list[list[tuple[str, int | None]]]:
        out = []
        for row in self._cells:
            spans: list[tuple[str, int | None]] = []
            for owner in row:
                glyph = " " if owner is None else glyph_for(owner)
                if spans and spans[-1][1] == owner:
                    spans[-1] = (spans[-1][0] + glyph, owner)
                else:
                    spans.append((glyph, owner))
            out.append(spans)
        return out


# -- panel --------------------------------------------------------------------


class _Scale(NamedTuple):
    lo: float
    hi: float
    flat: bool

    def at(self, value: float, pixels: int) -> int:
        """Pixel row for a value: 0 is the top, ``pixels - 1`` the bottom.

        A span that overflows to infinity (finite extremes near the float
        ceiling still subtract to `inf`) would make every ratio `inf/inf` and
        every row `nan`. There is no honest scale left at that point, so the
        series collapses to the middle row the way a constant one does.
        """
        span = self.hi - self.lo
        if self.flat or not math.isfinite(span) or span <= 0:
            return (pixels - 1) // 2
        return int(round((self.hi - value) / span * (pixels - 1)))


def _scale(values: Sequence[float]) -> _Scale:
    lo, hi = min(values), max(values)
    # A constant series is drawn down the middle rather than stretched to fill
    # the canvas: inventing a range around it would put tick labels on the axis
    # that no point ever took, which reads as movement that did not happen.
    return _Scale(lo, hi, flat=lo == hi)


def _nice_step(raw: float) -> float:
    """Round a tick interval up to something a person would have chosen.

    Ticks placed by dividing the range evenly land on 231.7 and 139 -- numbers
    that describe the canvas height rather than the data. A 1/2/2.5/5 step
    lands on 200 and 100, and then the uneven ROW spacing that produces is
    invisible, because the reader is looking at the values.
    """
    if raw <= 0 or not math.isfinite(raw):
        return 0.0
    magnitude = 10 ** math.floor(math.log10(raw))
    for multiple in (1, 2, 2.5, 5):
        if raw <= magnitude * multiple:
            return magnitude * multiple
    return magnitude * 10


def _ticks(scale: _Scale, height: int, target: int = 5) -> dict[int, str]:
    """Row -> label for the y-axis, on round values inside the data's range."""
    span = scale.hi - scale.lo
    step = _nice_step(span / max(1, min(target, height) - 1)) if span > 0 else 0.0
    if span <= 0 or not math.isfinite(span) or step <= 0:
        # step underflows to zero between adjacent subnormals: a span that
        # exists but is too small to divide. The extremes are still true.
        rows = {0: scale.hi, height - 1: scale.lo}
    else:
        rows = {}
        for index in range(math.ceil(scale.lo / step), math.floor(scale.hi / step) + 1):
            rows.setdefault(scale.at(index * step, height), index * step)
        # A range that encloses no multiple of the step at all would leave the
        # axis bare; its own extremes are a worse label but a better axis.
        rows = rows or {0: scale.hi, height - 1: scale.lo}
    return dict(zip(rows, _tick_labels(list(rows.values()))))


def _tick_labels(values: Sequence[float]) -> list[str]:
    """One notation for the whole axis, chosen by the value that needs the most.

    Per-value formatting puts `1.000e+06` above `5e+05` on the same axis, which
    reads as two different quantities rather than one scale.
    """
    if any(v and (abs(v) >= 1e6 or abs(v) < 1e-3) for v in values):
        return [f"{v:.3e}" if v else "0" for v in values]
    return [fmt(v) for v in values]


def panel(
    series: Sequence[Series],
    *,
    title: str = "",
    footer: str = "",
    width: int | None = None,
    height: int = 12,
    color: bool | None = None,
    unicode: bool | None = None,
    x_label: str = "step",
) -> str:
    """One chart: axes, tick labels, and every series on a single y-scale.

    ``width`` and ``height`` are in character cells and describe the PLOT, not
    the block -- the y-axis gutter and the label rows are added outside them, so
    a caller sizing to the terminal should subtract nothing.
    """
    color, uni = use_color(color), use_unicode(unicode)
    tick, wall, corner, rule = _AXIS[uni]

    title, footer = _for_stream(title, uni), _for_stream(footer, uni)
    drawable = [s for s in series if s.points]
    if not drawable:
        return "\n".join(part for part in (title, "  (no points)", footer) if part)

    height = max(3, min(height, 60))
    width = max(20, min(width if width else columns() - 14, 400))

    xs = [x for s in drawable for x, _ in s.points]
    ys = [y for s in drawable for _, y in s.points]
    x_scale = _Scale(min(xs), max(xs), flat=min(xs) == max(xs))
    y_scale = _scale(ys)

    canvas: _Canvas
    if len(drawable) == 1 and uni:
        canvas = _Braille(width, height)
    else:
        canvas = _Markers(width, height)

    for index, item in enumerate(drawable):
        canvas.draw(
            [
                (
                    (canvas.px - 1) // 2
                    if x_scale.flat
                    else int(
                        round((x - x_scale.lo) / (x_scale.hi - x_scale.lo) * (canvas.px - 1))
                    ),
                    y_scale.at(y, canvas.py),
                )
                for x, y in item.points
            ],
            index,
        )

    ticks = (
        {(height - 1) // 2: fmt(y_scale.lo)} if y_scale.flat else _ticks(y_scale, height)
    )
    gutter = max(len(v) for v in ticks.values())

    lines = []
    if title:
        lines.append(title)
    for row, spans in enumerate(canvas.rows()):
        label = ticks.get(row, "")
        edge = _paint(tick if label else wall, _DIM, color)
        painted = "".join(
            _paint(text, _series_color(owner, len(drawable)), color) for text, owner in spans
        )
        lines.append(f"{label:>{gutter}} {edge}{painted}")
    lines.append(_paint(f"{'':>{gutter}} {corner}{rule * width}", _DIM, color))
    lines.append(f"{'':>{gutter}}  {_x_axis(x_scale, width, x_label)}")
    if len(drawable) > 1:
        lines.append(f"{'':>{gutter}}  {_legend(drawable, color, uni)}")
    if footer:
        lines.append(f"{'':>{gutter}}  {footer}")
    return "\n".join(lines)


def _series_color(owner: int | None, total: int) -> str | None:
    """No hue for blank cells, and none at all for a lone curve.

    A single series is already named by the title; coloring it would say
    nothing the reader does not know and would make the one-series case look
    like a legend is missing.
    """
    if owner is None or total < 2:
        return None
    return _COLORS[owner % len(_COLORS)]


def _x_axis(scale: _Scale, width: int, x_label: str) -> str:
    """Endpoints under the plot, plus a midpoint when there is room for it."""
    left, right = _fmt_x(scale.lo), _fmt_x(scale.hi)
    line = left.ljust(width)
    if len(left) + len(right) + 2 <= width:
        line = line[: width - len(right)] + right
    middle = _fmt_x((scale.lo + scale.hi) / 2)
    start = (width - len(middle)) // 2
    if start > len(left) + 1 and start + len(middle) < width - len(right) - 1:
        line = line[:start] + middle + line[start + len(middle) :]
    return f"{line.rstrip()}  {x_label}" if x_label else line.rstrip()


def _legend(series: Sequence[Series], color: bool, unicode_ok: bool = True) -> str:
    """Glyph then name -- the name in plain ink, so the mark carries identity.

    `%` is named last and only when it can appear: a cell more than one curve
    reached. Without it in the legend an overlap reads as a seventh series.
    """
    entries = [
        f"{_paint(glyph_for(i), _COLORS[i % len(_COLORS)], color)} "
        f"{_for_stream(s.label, unicode_ok)}"
        for i, s in enumerate(series)
    ]
    if len(series) > 1:
        entries.append(f"{_SHARED_GLYPH} overlap")
    return "   ".join(entries)


# -- board --------------------------------------------------------------------


def sparkline(values: Sequence[float], width: int | None = None) -> str:
    """One line per series, eight levels, bucket-averaged down to ``width``.

    Averaged rather than sampled: a sampled spark of a noisy curve shows
    whichever points the stride happened to land on, and redraws differently at
    a different width.
    """
    finite = [v for v in values if v is not None and math.isfinite(v)]
    if not finite:
        return ""
    if width and len(finite) > width:
        size = len(finite) / width
        finite = [
            sum(bucket) / len(bucket)
            for i in range(width)
            if (bucket := finite[int(i * size) : max(int((i + 1) * size), int(i * size) + 1)])
        ]
    lo, hi = min(finite), max(finite)
    if hi == lo:
        return _BLOCKS[len(_BLOCKS) // 2] * len(finite)
    return "".join(
        _BLOCKS[min(len(_BLOCKS) - 1, int((v - lo) / (hi - lo) * len(_BLOCKS)))] for v in finite
    )


def board(
    series: Sequence[Series],
    *,
    width: int | None = None,
    spark_width: int | None = None,
    color: bool | None = None,
    unicode: bool | None = None,
) -> str:
    """Every series, one line each: name, curve, and where it ended up.

    The overview a run deserves before you pick something to look at properly.
    Each spark carries its OWN scale -- these are unrelated metrics stacked for
    reading, not a comparison -- so the numeric columns beside it are what make
    two rows commensurable, and they are always printed.
    """
    color, uni = use_color(color), use_unicode(unicode)
    rows = [s for s in series if s.points]
    if not rows:
        return "  (no series)"

    total = width or columns()
    labels = [_for_stream(s.label, uni) for s in rows]
    label_width = min(max(_cells(label) for label in labels), max(12, total // 3))
    # Indexed, not keyed by label: two series can carry the same name (a key
    # logged under two kinds), and a dict would then print one series' numbers
    # on both rows -- the same picture twice, with nothing to say so.
    values = [[y for _, y in s.points] for s in rows]
    cells = [(fmt(ys[-1]), fmt(min(ys)), fmt(max(ys))) for ys in values]
    number_width = max(4, max(len(text) for cell in cells for text in cell))
    spent = label_width + 3 * (number_width + 2) + 4
    spark = spark_width or max(8, min(40, total - spent))

    header = (
        f"{'metric':<{label_width}}  {'curve':<{spark}}  "
        f"{'last':>{number_width}}  {'min':>{number_width}}  {'max':>{number_width}}"
    )
    lines = [_paint(header, _DIM, color)]
    for label, ys, (last, low, high) in zip(labels, values, cells):
        draw = sparkline if uni else _ascii_spark
        curve = draw(ys, spark)
        lines.append(
            f"{_pad(label, label_width, uni)}  {curve:<{spark}}  "
            f"{last:>{number_width}}  {low:>{number_width}}  {high:>{number_width}}"
        )
    return "\n".join(lines)


def _cells(text: str) -> int:
    """How many terminal COLUMNS a string occupies, not how many code points.

    A CJK metric name is one character per two columns and a combining mark is
    one per zero, so `len()` pads the label column to the wrong place and every
    number after it lands under the wrong heading. The board's alignment is the
    only thing making two rows comparable, so it is measured in the unit the
    terminal actually uses.
    """
    return sum(
        0 if unicodedata.combining(char) else (2 if _wide_char(char) else 1) for char in text
    )


def _wide_char(char: str) -> bool:
    return unicodedata.east_asian_width(char) in ("W", "F")


def _pad(text: str, width: int, unicode_ok: bool = True) -> str:
    """Left-align to `width` terminal columns, truncating by columns."""
    if _cells(text) <= width:
        return text + " " * (width - _cells(text))
    marker = "…" if unicode_ok else "."
    kept, used = "", 0
    for char in text:
        size = 0 if unicodedata.combining(char) else (2 if _wide_char(char) else 1)
        if used + size > width - 1:
            break
        kept, used = kept + char, used + size
    return kept + marker + " " * (width - used - 1)


def _for_stream(text: str, unicode_ok: bool) -> str:
    """Server data on a stream that may not be able to carry it.

    A metric key is whatever someone passed to `probe log`, and `--ascii` (or an
    ASCII stdout, which selects the same path) means this stream cannot print
    it. Replacing the characters is a worse label; raising UnicodeEncodeError
    out of `print` is a worse command.
    """
    return text if unicode_ok else text.encode("ascii", "replace").decode("ascii")


def _ascii_spark(values: Sequence[float], width: int) -> str:
    """The same shape in `_.-~^` for terminals that cannot show blocks."""
    levels = "_.-~^"
    top = len(levels) - 1
    return "".join(
        levels[min(top, _BLOCKS.index(block) * len(levels) // len(_BLOCKS))]
        for block in sparkline(values, width)
    )


# -- adapters -----------------------------------------------------------------


def series_from_wide(table: dict) -> list[Series]:
    """Turn `GET /v1/runs/{id}/metrics/wide` into curves, one per column.

    A key logged on several coordinates arrives as several columns that share
    it, so the dimensions ride in the label -- otherwise four `loss` rows on a
    board would be indistinguishable, and overlaying them would draw four
    curves the legend calls the same thing.
    """
    columns_ = table.get("columns") or []
    rows = table.get("rows") or []
    # A column is (kind, key, dimensions), so two columns can differ by kind
    # alone -- `probe log ... --kind` is a user-set field. Naming both `loss`
    # would put two different series on the board under one name. The kind is
    # spent only where it is the thing telling them apart.
    bases = [label_for(column) for column in columns_]
    shared = {base for base, count in Counter(bases).items() if count > 1}
    out = []
    for index, column in enumerate(columns_):
        label = bases[index]
        if label in shared:
            label = f"{column.get('kind', '?')}:{label}"
        cells = [
            (float(row["step_index"]), float(value))
            for row in rows
            if (values := row.get("values")) is not None
            and index < len(values)
            and (value := values[index]) is not None
        ]
        points = [(x, y) for x, y in cells if math.isfinite(y)]
        if points or cells:
            out.append(Series(label, points, dropped=len(cells) - len(points)))
    return out


def label_for(column: dict) -> str:
    """`key` alone, or `key{rank=0,split=train}` when it needs the coordinate."""
    key = column.get("key", "?")
    dims = column.get("dimensions") or {}
    if dims:
        key += "{" + ",".join(f"{k}={_dim_value(dims[k])}" for k in sorted(dims)) + "}"
    return _printable(key)


def _dim_value(value: object) -> str:
    """Quote a coordinate value only when it carries the separators.

    Unquoted, `{"a": "b,c=d"}` and `{"a": "b", "c": "d"}` render identically --
    two different coordinates under one name, which is the exact confusion the
    dimensions are in the label to prevent.
    """
    text = str(value)
    return f'"{text}"' if ("," in text or "=" in text or '"' in text) else text


def _printable(text: str) -> str:
    """Strip what a positional layout cannot survive.

    A label is server data -- a metric key someone typed at `probe log` -- and
    it lands in a column-aligned board and, unlike every JSON-printing verb
    here, unescaped. A tab or a newline in it shifts every column after it; an
    escape sequence is read by the terminal rather than printed. Neither is a
    thing the writer could have meant by a metric name.
    """
    return "".join(char if char.isprintable() else "?" for char in text)


def _sep(unicode: bool | None) -> str:
    """The separator these footers are strung on.

    It takes the same unicode decision the chart does, and that is the whole
    point: a footer built with a middot is printed by the same call as the
    ASCII canvas, so a hardcoded one made `--ascii` raise UnicodeEncodeError on
    exactly the stream the flag exists for.
    """
    return "  ·  " if use_unicode(unicode) else "  |  "


def summarize(item: Series, *, unicode: bool | None = None) -> str:
    """The numbers a curve cannot be read off precisely, said once beneath it."""
    sep = _sep(unicode)
    ys = [y for _, y in item.points]
    if not ys:
        return f"no finite points{sep}{item.dropped} non-finite, not plottable"
    text = (
        f"{len(ys)} points{sep}first {fmt(ys[0])}  last {fmt(ys[-1])}  "
        f"min {fmt(min(ys))}  max {fmt(max(ys))}"
    )
    return text + (f"{sep}{item.dropped} non-finite, not plotted" if item.dropped else "")


def overlay_footer(series: Sequence[Series], *, unicode: bool | None = None) -> str:
    """What a shared axis is doing to these particular curves, said out loud.

    One axis is the only honest way to draw two curves together, and it has a
    real cost: a metric three orders of magnitude smaller than its neighbour is
    a flat line on the floor. Left unsaid, that reads as a metric that never
    moved -- so the panel says it, and names the range the axis actually spans
    now that the ticks sit on round numbers rather than on the extremes.
    """
    sep = _sep(unicode)
    ys = [y for s in series for _, y in s.points]
    if not ys:
        return "one shared axis"
    text = f"one shared axis{sep}y {fmt(min(ys))} to {fmt(max(ys))}"
    magnitudes = [max(abs(y) for _, y in s.points) for s in series if s.points]
    magnitudes = [m for m in magnitudes if m]
    if len(magnitudes) > 1 and max(magnitudes) / min(magnitudes) >= 100:
        orders = math.log10(max(magnitudes) / min(magnitudes))
        text += (
            f"{sep}these scales differ by ~{orders:.0f} orders of magnitude, "
            "so the smaller curves flatten against the floor"
        )
    dropped = sum(s.dropped for s in series)
    return text + (f"{sep}{dropped} non-finite, not plotted" if dropped else "")
