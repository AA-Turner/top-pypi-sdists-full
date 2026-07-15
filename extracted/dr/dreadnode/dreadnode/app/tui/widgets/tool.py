"""Widgets and helpers for displaying tool calls."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, ClassVar

from markdown_it import MarkdownIt
from rich import box
from rich.console import Group
from rich.markdown import CodeBlock, Heading, Markdown, TableElement
from rich.segment import Segment
from rich.style import Style
from rich.syntax import Syntax
from rich.table import Table
from rich.text import Text
from rich.theme import Theme as RichTheme
from textual.reactive import reactive
from textual.widget import Widget

from dreadnode.app.tui.theme import (
    ACCENT,
    BORDER,
    BORDER_LIGHT,
    CODE,
    CODE_BG,
    ERROR,
    FG,
    FG_FAINTEST,
    FG_MUTED,
    FG_SUBTLE,
    LINK,
)

if TYPE_CHECKING:
    from rich.console import (
        Console,
        ConsoleOptions,
        ConsoleRenderable,
        JustifyMethod,
        RenderableType,
        RenderResult,
    )
    from rich.markdown import MarkdownContext

# Short label rendered in place of the raw URL when a tool result carries
# a deep link — the URL itself can be 100+ chars wide and wraps past the
# tool widget's gutter, breaking the bordered visual frame and adding
# noise. The link target rides on the OSC 8 hyperlink the label carries.
URL_LABEL = "View in web"


class _ThemedHeading(Heading):
    """Rich heading subclass that mirrors the project's TCSS palette.

    Rich's defaults center H1, color H2/H3 magenta, and underline both —
    fine for ``rich.print``, jarring next to the conversation's themed
    Textual ``Markdown`` widgets. The proper fix is to refactor
    ``ToolCall`` to a ``compose()`` widget so the expanded body can use
    the same Textual ``Markdown`` (and inherit ``MarkdownH1`` / ``MarkdownH2``
    rules from ``dreadnode.tcss``). Until that lands, we override
    ``Heading`` in our Rich Markdown subclass below to apply the same
    accent-bold-no-underline styling Rich's renderer produces.
    """

    LEVEL_ALIGN: ClassVar[dict[str, str]] = {f"h{i}": "left" for i in range(1, 7)}

    _STYLES: ClassVar[dict[str, Style]] = {
        "h1": Style(color=FG, bold=True),
        "h2": Style(color=FG, bold=True),
        "h3": Style(color=FG, bold=True),
        "h4": Style(color=FG, bold=True),
        "h5": Style(color=FG_SUBTLE, bold=True),
        "h6": Style(color=FG_MUTED, bold=True),
    }

    def on_enter(self, context: MarkdownContext) -> None:
        # Push a no-op style instead of ``markdown.h{n}`` so the magenta
        # / underline from Rich's default theme don't bake into
        # per-character styles. The push is still required because
        # ``on_leave`` always pops; we apply our themed style in
        # ``__rich_console__`` afterwards.
        context.enter_style("none")
        self.text = Text()

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        text = self.text.copy()
        text.justify = "left"
        text.stylize(self._STYLES.get(self.tag, Style(bold=True)))
        yield text


class _BorderedTable(TableElement):
    """Render Markdown tables with a visible border and header rule.

    Rich's default table element uses ``box.SIMPLE_HEAVY`` (borderless); this
    restores the bordered grid the Textual ``MarkdownTable`` widget produced so
    committed messages match the previous look.
    """

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        table = Table(box=box.SQUARE, border_style=BORDER_LIGHT, header_style=f"bold {FG}")
        if self.header is not None and self.header.row is not None:
            for column in self.header.row.cells:
                table.add_column(column.content)
        if self.body is not None:
            for row in self.body.rows:
                table.add_row(*[cell.content for cell in row.cells])
        yield table


class _ThemedCodeBlock(CodeBlock):
    """Fenced code block on the conversation's own background.

    Rich's ``CodeBlock`` lets the Pygments ``code_theme`` paint the block
    background, which clashes with the surrounding chat. The Textual
    ``MarkdownFence`` widget (used while streaming) instead sits on
    ``$bg-lighter`` via ``dreadnode.tcss``; we force the same background here so
    a committed fence doesn't change colour the instant the turn commits.
    """

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        code = str(self.text).rstrip()
        yield Syntax(
            code,
            self.lexer_name,
            theme=self.theme,
            background_color=CODE_BG,
            word_wrap=True,
            padding=1,
        )


# Style names Rich resolves via ``console.get_style`` while rendering Markdown.
# Rich's defaults (magenta quotes, ``bold cyan on black`` code, bold bullets)
# don't match ``dreadnode.tcss``'s Markdown rules, and those TCSS rules only
# reach the Textual ``Markdown`` widget — never this Rich renderable. We push
# this theme while rendering so committed assistant messages match the
# streaming draft. Keep in sync with the ``/* -- Markdown -- */`` block in
# ``dreadnode.tcss``.
_MARKDOWN_THEME = RichTheme(
    {
        "markdown.em": Style(italic=True),
        "markdown.emph": Style(italic=True),
        "markdown.strong": Style(bold=True, color=FG),
        "markdown.code": Style(color=CODE, bgcolor=CODE_BG),
        "markdown.code_block": Style(color=CODE, bgcolor=CODE_BG),
        "markdown.block_quote": Style(color=FG_MUTED),
        "markdown.list": Style(color=FG_SUBTLE),
        "markdown.item.bullet": Style(color=FG_MUTED),
        "markdown.item.number": Style(color=FG_MUTED),
        "markdown.hr": Style(color=BORDER),
        # With hyperlinks enabled Rich styles the *visible link text* via
        # ``markdown.link_url`` (not ``markdown.link``) and wraps it in an OSC-8
        # hyperlink — so the color must live on ``link_url`` to actually paint.
        # Links read as near-white + underline (the underline carries the
        # affordance); warm accent is reserved for tool calls.
        "markdown.link": Style(color=LINK, underline=True),
        "markdown.link_url": Style(color=LINK, underline=True),
    },
    inherit=True,
)


class ThemedMarkdown(Markdown):
    """Rich ``Markdown`` restyled to match the TCSS conversation theme.

    Committed assistant messages render through this Rich path, but the
    ``dreadnode.tcss`` Markdown rules only style the Textual ``Markdown`` widget
    used while streaming. To keep the stream->commit swap from visibly
    restyling, this subclass mirrors those rules three ways: heading and table
    *elements* are overridden (see ``_ThemedHeading`` / ``_BorderedTable``),
    fenced code uses ``_ThemedCodeBlock`` for the conversation background, and
    every remaining inline/block style is supplied by pushing
    :data:`_MARKDOWN_THEME` for the duration of the render. It also parses with
    the same ``gfm-like`` preset Textual's ``Markdown`` widget uses so content
    renders identically through either path.
    """

    elements: ClassVar[dict[str, type]] = {
        **Markdown.elements,
        "heading_open": _ThemedHeading,
        "table_open": _BorderedTable,
        "fence": _ThemedCodeBlock,
        "code_block": _ThemedCodeBlock,
    }

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        # Push the Markdown palette so Rich's ``markdown.*`` style lookups
        # resolve to our theme instead of its magenta/cyan defaults; the theme
        # must stay on the stack for the whole render since styles are resolved
        # lazily as segments are produced.
        console.push_theme(_MARKDOWN_THEME)
        try:
            yield from super().__rich_console__(console, options)
        finally:
            console.pop_theme()

    def __init__(
        self,
        markup: str,
        code_theme: str = "monokai",
        justify: JustifyMethod | None = None,
        style: str | Style = "none",
        hyperlinks: bool = True,
        inline_code_lexer: str | None = None,
        inline_code_theme: str | None = None,
    ) -> None:
        # Set up the same attributes Rich's ``Markdown.__init__`` would, but
        # parse with the ``gfm-like`` preset Textual's Markdown widget uses
        # (tables, strikethrough, and linkified bare URLs) so content renders
        # identically through this Rich path or a Textual widget. We inline the
        # setup rather than call ``super().__init__`` so the document is parsed
        # once, not twice.
        self.markup = markup
        self.parsed = MarkdownIt("gfm-like").parse(markup)
        self.code_theme = code_theme
        self.justify = justify
        self.style = style
        self.hyperlinks = hyperlinks
        self.inline_code_lexer = inline_code_lexer
        self.inline_code_theme = inline_code_theme or code_theme


class _GutterFrame:
    """Wrap a renderable so each rendered line is prefixed with the
    tool-call gutter (``│ ``).

    The header/meta block built in :func:`render_tool_call` paints its
    own per-line gutter while assembling a single ``Text``. A multi-line
    body (Markdown for the report tool) is a Rich renderable that
    doesn't know about that gutter — without help, headings/lists/blank
    lines bleed past column 0 and look like they've escaped the tool
    frame. We let Rich do the line breaking (so headings and code blocks
    still render natively at the reduced width), then prepend the gutter
    Segment to each resulting line. Width is reserved up front so the
    inner renderable wraps correctly.
    """

    def __init__(
        self,
        renderable: ConsoleRenderable,
        *,
        gutter: str = "│ ",
        gutter_style: str = FG_FAINTEST,
    ) -> None:
        self.renderable = renderable
        self.gutter = gutter
        self.gutter_style = gutter_style

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        gutter_width = len(self.gutter)
        inner_width = max(options.max_width - gutter_width, 1)
        # ``update_width`` keeps ``options.height`` — when Textual renders
        # the parent widget it passes the widget's full height, which then
        # causes ``render_lines`` below to pad short bodies up to that
        # height with empty rows. The padding consumes the widget's row
        # budget so later siblings (e.g. the meta section) get clipped.
        # Clear height so each body renders at its natural row count.
        inner_options = options.update(width=inner_width, height=None)
        prefix = Segment(self.gutter, console.get_style(self.gutter_style))
        new_line = Segment.line()
        for line in console.render_lines(self.renderable, inner_options, pad=False):
            yield prefix
            yield from line
            yield new_line


def _link_style(url: str) -> Style:
    return Style.from_meta({"@click": f"open_url({url!r})"})


@dataclass(frozen=True)
class _Section:
    """One prefixed block in a rendered tool call.

    ``first_prefix`` paints the leading visual line (e.g. ``│ ↳ ``);
    ``continuation_prefix`` paints every visual line after it — both
    explicit ``\\n`` breaks in the body AND word-wrap continuations Rich
    introduces to fit the terminal width. Both prefixes must be the same
    visible width so the inner content stays aligned across visual lines.
    """

    first_prefix: str
    continuation_prefix: str
    body: Text
    prefix_style: str = FG_FAINTEST


class _SectionedRenderable:
    """Render :class:`_Section` blocks with wrap-aware gutter prefixes.

    Rich's text wrapper doesn't know about the visual gutter the tool
    widget paints to its left, so a long meta/details line gets soft-
    wrapped at column 0 — the continuation leaks past the ``│`` border
    and looks like text that escaped the tool frame. We give each section
    its own first/continuation prefix, reserve their width up front so
    Rich wraps to the inner column, then prepend the right prefix to
    every visual line as Segments.

    The two prefixes for a section are assumed to be the same width;
    callers pad ``continuation_prefix`` with spaces to match
    ``first_prefix`` (e.g. ``"│ ↳ "`` → ``"│   "``).
    """

    def __init__(self, sections: list[_Section]) -> None:
        self.sections = sections

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        new_line = Segment.line()
        for section in self.sections:
            prefix_width = len(section.first_prefix)
            inner_width = max(options.max_width - prefix_width, 1)
            # See ``_GutterFrame.__rich_console__`` — Textual passes the
            # widget's full height in ``options.height``. Without clearing
            # it, ``render_lines`` pads each section's body up to that
            # height with blank lines, which (a) emits the wrong prefix
            # (``continuation_prefix`` instead of ``first_prefix`` for
            # later sections) and (b) crowds subsequent sections off the
            # widget's row budget so they don't render.
            inner_options = options.update(width=inner_width, height=None)
            prefix_style = console.get_style(section.prefix_style)
            first_seg = Segment(section.first_prefix, prefix_style)
            cont_seg = Segment(section.continuation_prefix, prefix_style)
            for i, line in enumerate(console.render_lines(section.body, inner_options, pad=False)):
                yield first_seg if i == 0 else cont_seg
                yield from line
                yield new_line

    @property
    def plain(self) -> str:
        """Plain-text form for tests / debugging.

        Reflects the section structure with explicit-newline continuations
        only — does NOT simulate Rich's word-wrap (that requires a Console
        width which this property doesn't have). Use ``__rich_console__``
        via a real Console to inspect wrap behavior.
        """
        out: list[str] = []
        for section in self.sections:
            body_lines = section.body.plain.splitlines() or [""]
            out.append(section.first_prefix + body_lines[0])
            for line in body_lines[1:]:
                out.append(section.continuation_prefix + line)
        return "\n".join(out)


def render_tool_call(
    label: str,
    *,
    meta: str | None = None,
    details: str = "",
    meta_style: str = FG_FAINTEST,
    url: str | None = None,
    body: ConsoleRenderable | None = None,
) -> RenderableType:
    """Render a tool call — or a Group when a rich body is attached.

    Pure rendering function — no awareness of display modes.
    Used by ToolCall.render() as the single output path.

    ``meta_style`` colors the ``↳ <meta>`` line; defaults to the same
    dim gray used for summaries. Errored calls pass :data:`ERROR` so the
    failure pops without changing the tool-name color.

    ``url`` renders a compact Textual-clickable link on the summary line
    (currently used by the ``report`` tool). The raw URL is not shown.

    ``body`` is an optional Rich renderable (typically ``Markdown`` for
    the ``report`` tool's expanded view). When present, the function
    returns a ``Group`` with the body sitting after the header/meta
    block, wrapped in :class:`_GutterFrame` so every line of the body
    carries the same ``│ `` gutter as the header — Rich still does the
    line breaking, so multi-line markdown elements (lists, code blocks,
    headings) render natively at the reduced width.
    """
    sections: list[_Section] = []

    label_text = Text()
    match = re.match(r"^([a-zA-Z0-9_-]+)\((.*)\)$", label)
    if match:
        name, args = match.groups()
        label_text.append(name, style=ACCENT)
        label_text.append(f"({args})", style=FG_MUTED)
    else:
        label_text.append(label, style=ACCENT)
    sections.append(
        _Section(first_prefix="│ ", continuation_prefix="│   ", body=label_text),
    )

    if meta:
        # Multi-line meta (e.g. "Command failed (1):\n<stderr>...") and
        # single-line meta that's too wide for the terminal both need the
        # same continuation gutter so the tool frame stays visually
        # contiguous. The link label sits on the first visual line so it
        # stays adjacent to the meta summary; if that combined line wraps,
        # the URL_LABEL may end up on a continuation line — still inside
        # the gutter, still clickable.
        meta_lines = meta.splitlines() or [""]
        meta_text = Text(meta_lines[0], style=meta_style)
        if url:
            meta_text.append(" - ", style=meta_style)
            meta_text.append(URL_LABEL, style=_link_style(url))
        for line in meta_lines[1:]:
            meta_text.append("\n", style=meta_style)
            meta_text.append(line, style=meta_style)
        sections.append(
            _Section(
                first_prefix="│ ↳ ",
                continuation_prefix="│   ",
                body=meta_text,
                prefix_style=meta_style,
            ),
        )

    if details:
        details_text = Text(details, style=FG_FAINTEST)
        sections.append(
            _Section(
                first_prefix="│   " if meta else "│ ↳ ",
                continuation_prefix="│   ",
                body=details_text,
            ),
        )

    if url and not meta:
        url_text = Text()
        url_text.append(URL_LABEL, style=_link_style(url))
        sections.append(
            _Section(first_prefix="│ ↗ ", continuation_prefix="│   ", body=url_text),
        )

    frame = _SectionedRenderable(sections)
    if body is None:
        return frame
    return Group(frame, _GutterFrame(body))


class ToolCall(Widget):
    """A widget to display a tool call — in-progress or completed.

    Used by both the live interactive stream (tool_start → tool_end) and the
    transcript rebuild path. Stores full data; display mode is resolved
    at render time via app._output_mode.
    """

    DEFAULT_CSS = """
    ToolCall {
        height: auto;
    }
    """

    # ``layout=True`` is load-bearing: the widget mounts in-progress with
    # only ``tool_name`` populated (height resolves to 1 line), then
    # ``complete()`` fills in ``meta`` / ``details`` / ``error`` /
    # ``expanded_body`` from the ``ToolEnd`` event. With the default
    # ``layout=False`` the re-render runs but the auto height stays at
    # the original 1 line, so the new lines get clipped — visible as
    # "tool output sporadically doesn't render" (they show up only when
    # something else later invalidates layout). Force a relayout on every
    # change so the widget grows to match its rendered content.
    tool_name: reactive[str] = reactive("", layout=True)
    meta: reactive[str] = reactive("", layout=True)
    details: reactive[str] = reactive("", layout=True)
    error: reactive[str] = reactive("", layout=True)
    url: reactive[str] = reactive("", layout=True)
    expanded_body: reactive[str] = reactive("", layout=True)
    expanded_body_format: reactive[str] = reactive("", layout=True)

    def __init__(
        self,
        *,
        name: str,
        details: str = "",
        meta: str | None = None,
        error: str | None = None,
        url: str | None = None,
        expanded_body: str | None = None,
        expanded_body_format: str | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.tool_name = name
        self.details = details
        self.meta = meta or ""
        self.error = error or ""
        self.url = url or ""
        self.expanded_body = expanded_body or ""
        self.expanded_body_format = expanded_body_format or ""

    def _output_mode(self) -> str:
        try:
            return self.app.output_mode  # type: ignore[attr-defined]
        except Exception:
            return "compact"

    def _get_visible_details(self) -> str:
        """Return details respecting the app-level output mode.

        Applies 8-line truncation for display. The full details are
        always stored on the widget — truncation is render-time only.
        """
        if not self.details:
            return ""
        if self._output_mode() != "expanded":
            return ""
        lines = self.details.splitlines()
        if len(lines) > 8:
            omitted = len(lines) - 6
            return "\n".join(lines[:3] + [f"... {omitted} lines omitted ..."] + lines[-3:])
        return self.details

    def _get_visible_error(self) -> str:
        """Return the error string respecting the app-level output mode.

        Mirrors :meth:`_get_visible_details`: compact mode keeps the
        first line only (so the failure is still visible at a glance
        without a multi-screen traceback dominating the conversation),
        expanded mode shows the full error with the same 8-line
        truncation applied to long bodies.
        """
        if not self.error:
            return ""
        lines = self.error.splitlines() or [""]
        if self._output_mode() != "expanded":
            first = lines[0]
            if len(lines) > 1:
                return f"{first} (+{len(lines) - 1} more lines)"
            return first
        if len(lines) > 8:
            omitted = len(lines) - 6
            return "\n".join(lines[:3] + [f"... {omitted} lines omitted ..."] + lines[-3:])
        return self.error

    def complete(
        self,
        *,
        meta: str | None = None,
        details: str = "",
        error: str | None = None,
        url: str | None = None,
        expanded_body: str | None = None,
        expanded_body_format: str | None = None,
    ) -> None:
        """Transition from in-progress to completed state."""
        if meta is not None:
            self.meta = meta
        self.details = details
        if error:
            self.error = error
        if url:
            self.url = url
        if expanded_body:
            self.expanded_body = expanded_body
        if expanded_body_format:
            self.expanded_body_format = expanded_body_format

    def _build_expanded_body_renderable(self) -> ConsoleRenderable | None:
        if not self.expanded_body:
            return None
        if self.expanded_body_format == "markdown":
            return ThemedMarkdown(self.expanded_body)
        return Text(self.expanded_body)

    def render(self) -> RenderableType:
        """Render the tool call."""
        if self.error:
            visible_error = self._get_visible_error()
            return render_tool_call(
                self.tool_name,
                meta=f"error: {visible_error}",
                meta_style=ERROR,
            )
        visible_details = self._get_visible_details()
        body: ConsoleRenderable | None = None
        if self._output_mode() == "expanded":
            body = self._build_expanded_body_renderable()
        if body is not None:
            return render_tool_call(
                self.tool_name,
                meta=self.meta or None,
                url=self.url or None,
                body=body,
            )
        return render_tool_call(
            self.tool_name,
            meta=None if visible_details else (self.meta or None),
            details=visible_details,
            url=self.url or None,
        )

    def action_open_url(self, url: str) -> None:
        self.app.open_url(url)
