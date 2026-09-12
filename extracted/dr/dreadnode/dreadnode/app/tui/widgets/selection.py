"""Selection for lightweight Rich transcript widgets.

Textual's RichVisual supplies neither selection offsets nor highlighting or
extraction. Keep the existing renderers and select their rendered rows, using
style metadata to distinguish UI prefixes from actual content (including table
borders). Offsets are character indices, as required by Textual's hit testing.
Command renderers attach source positions at their wrap call sites so copying
can rejoin soft wraps without consuming real newlines or indentation.
"""

import typing as t
from contextvars import ContextVar
from itertools import count

from rich.console import Console, ConsoleOptions, RenderableType, RenderResult
from rich.segment import Segment
from rich.style import Style
from rich.text import Text
from textual.selection import Selection
from textual.strip import Strip
from textual.style import Style as VisualStyle
from textual.visual import RenderOptions, RichVisual, Visual
from textual.widget import Widget
from textual.widgets import Static

from dreadnode.app.tui.theme import BG, FG

_SELECTION_STYLE = Style(color=BG, bgcolor=FG, dim=False, reverse=False, conceal=False)
_COPY_LINES = count()
_COPY_SOURCES: ContextVar[dict[int, str] | None] = ContextVar("copy_sources", default=None)

COPY_CHROME = Style.from_meta({"transcript_chrome": True})


def _is_chrome(segment: Segment) -> bool:
    return bool(segment.style and segment.style.meta.get("transcript_chrome"))


class _SelectableVisual(RichVisual):
    def __init__(self, widget: Widget, renderable: RenderableType) -> None:
        super().__init__(widget, renderable)
        self.copy_sources: dict[int, str] = {}

    def render_strips(
        self, width: int, height: int | None, style: VisualStyle, options: RenderOptions
    ) -> list[Strip]:
        # Keep source text once per logical line, rather than serializing a
        # potentially huge command into every styled segment's metadata.
        self.copy_sources = {}
        token = _COPY_SOURCES.set(self.copy_sources)
        try:
            rows = super().render_strips(width, height, style, options)
        finally:
            _COPY_SOURCES.reset(token)
        result: list[Strip] = []
        for y, original_row in enumerate(rows):
            row = original_row
            selection = options.selection
            span = selection.get_span(y) if selection else None
            if span is not None and options.selection_style is not None:
                start, end = span
                end = len(row.text) if end == -1 else end
                segments: list[Segment] = []
                x = 0
                for segment in row:
                    text, segment_style, control = segment
                    left = max(0, min(len(text), start - x))
                    right = max(left, min(len(text), end - x))
                    if left < right and not _is_chrome(segment):
                        selected_style = (segment_style or Style()) + _SELECTION_STYLE
                        segments.extend(
                            [
                                Segment(text[:left], segment_style, control),
                                Segment(text[left:right], selected_style, control),
                                Segment(text[right:], segment_style, control),
                            ]
                        )
                    else:
                        segments.append(segment)
                    x += len(text)
                row = Strip(segments)
            result.append(row.apply_offsets(0, y))
        return result


class SelectableWidget(Widget):
    """Rich widget that copies the selected visible rows without UI prefixes."""

    def get_selection(self, selection: Selection) -> tuple[str, str] | None:
        visual = self._render()
        if not isinstance(visual, _SelectableVisual):
            return super().get_selection(selection)
        rows = Visual.to_strips(
            self,
            visual,
            self.size.width,
            self.size.height,
            self.visual_style,
            apply_selection=False,
        )
        result = ""
        previous: tuple[int, str, int] | None = None
        first_row = True
        for y, row in enumerate(rows):
            span = selection.get_span(y)
            if span is None:
                continue
            start, end = span
            end = len(row.text) if end == -1 else end
            row_text = ""
            row_previous: tuple[int, str, int] | None = None
            first_piece = True
            x = 0
            for segment in row:
                text = segment.text
                left = max(0, min(len(text), start - x))
                right = max(left, min(len(text), end - x))
                x += len(text)
                if left == right or _is_chrome(segment):
                    continue
                meta = segment.style.meta if segment.style else {}
                source_span = meta.get("copy_source")
                if source_span is not None:
                    key, offset = source_span
                    source = visual.copy_sources[key]
                    source_start, source_end = offset + left, offset + right
                    prior = previous if first_piece else row_previous
                    if prior is not None and prior[0] == key:
                        row_text += source[prior[2] : source_start]
                    elif first_piece and not first_row:
                        row_text += "\n"
                    row_text += source[source_start:source_end]
                    row_previous = (key, source, source_end)
                else:
                    if first_piece and not first_row:
                        row_text += "\n"
                    row_text += text[left:right]
                    row_previous = None
                first_piece = False
            if first_piece and not first_row:
                row_text = "\n"
            result += row_text if row_previous is not None else row_text.rstrip(" ")
            previous = row_previous
            first_row = False
        return result, "\n"

    def selectable_visual(self, renderable: RenderableType) -> Visual:
        """Wrap Rich output with selection support without expanding the DOM."""
        return _SelectableVisual(self, renderable)


class SelectableStatic(Static, SelectableWidget):
    """Static transcript entry with rendered-row selection coordinates."""

    def render(self) -> Visual:
        content = self.content
        if isinstance(content, Visual):
            return content
        if isinstance(content, str):
            content = Text.from_markup(content) if self._render_markup else Text(content)
        return self.selectable_visual(t.cast("RenderableType", content))


class CopyableText:
    """Wrap command text while preserving its logical line and source offsets.

    Render each logical line separately through Rich's public Text.wrap API.
    Match the returned rows within that exact line before padding or gutters
    are added. This accounts for whitespace Rich removes at wrap boundaries;
    it does not infer wraps from the width of painted rows.
    """

    def __init__(self, text: Text) -> None:
        self.text = text

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        for logical in self.text.split(allow_blank=True):
            logical.expand_tabs(self.text.tab_size or console.tab_size or 8)
            source = logical.plain
            key = next(_COPY_LINES)
            sources = _COPY_SOURCES.get()
            if sources is not None:
                sources[key] = source
            position = 0
            rows = logical.wrap(console, options.max_width, justify="default", overflow="fold")
            offsets: list[int] = []
            try:
                for row in rows:
                    # Text.wrap may remove trailing whitespace that extends past
                    # the right edge. The next source offset retains that gap.
                    position = source.index(row.plain, position)
                    offsets.append(position)
                    position += len(row.plain)
            except ValueError:
                # Rich can replace a wide character with a space at width 1.
                # Copy rendered rows for this entire logical line: after a
                # mismatch, later substring matches may have ambiguous offsets.
                offsets = []
            for index, row in enumerate(rows):
                position = offsets[index] if offsets else 0
                for segment in row.render(console):
                    style = console.get_style(self.text.style) + (segment.style or Style())
                    if offsets:
                        style += Style.from_meta({"copy_source": (key, position)})
                    yield Segment(segment.text, style, segment.control)
                    position += len(segment.text)
                yield Segment.line()
