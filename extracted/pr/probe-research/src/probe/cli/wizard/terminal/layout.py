"""lay a page out: styled lines as rows, wrapping, the frame's margin/header/body split, vertical centring, the shared page and style."""

from __future__ import annotations
from collections.abc import Sequence
from typing import NamedTuple
from probe.cli.wizard.terminal.terminal import (
    CONTENT_WIDTH,
    MARGIN,
    _Window,
    _enter_window,
    _new_screen,
    _onboarding,
    clear,
    columns,
    interactive,
    left_pad,
    onboarding_header,
    rows,
    safe_margin,
)


class StyledLine(str):
    """Plain text with a shared TUI style, including after wrapping.

    `clip` keeps the line on ONE row: past the width it is cut with "…" instead
    of wrapped, for a table row whose wrapped tail would read as a row of its
    own. `escapes` are `(column, sequence)` pairs written raw before that
    column, taking no room (an agent's logo, `image_escape`), and `hover` is
    what the menu shows at the row's end while the mouse is over it. Only a
    clipped line honours either: wrapping moves the columns they count.
    """

    def __new__(cls, text: str, *, style: str = "", clip: bool = False,
                escapes: tuple[tuple[int, str], ...] = (), hover: str | None = None):
        line = super().__new__(cls, text)
        line.style = style
        line.clip = clip
        line.escapes = escapes
        line.hover = hover
        return line


#: prompt_toolkit writes a fragment carrying this style raw and gives it no
#: width: the only way to hand a terminal an image inside a drawn screen.
ZERO_WIDTH_ESCAPE = "[ZeroWidthEscape]"


def line_rows(line: str, width: int, default: str = "") -> list[list[tuple[str, str]]]:
    """The `(style, text)` fragments of each row a status line draws on."""
    style = line.style if isinstance(line, StyledLine) and line.style else default
    if not getattr(line, "clip", False):
        return [[(style, part)] for part in wrap(line, width=width)]
    text = str(line) if len(line) <= width else str(line)[: max(0, width - 1)] + "…"
    fragments: list[tuple[str, str]] = []
    at = 0
    for column, sequence in sorted(line.escapes):
        if column > len(text):
            break
        if column > at:
            fragments.append((style, text[at:column]))
            at = column
        fragments.append((ZERO_WIDTH_ESCAPE, sequence))
    if at < len(text) or not fragments:
        fragments.append((style, text[at:]))
    return [fragments]


def indent(text: str, pad: int | None = None) -> str:
    """Shift every line right so a block sits centred."""
    prefix = " " * (left_pad() if pad is None else pad)
    return "\n".join(prefix + line if line.strip() else line for line in text.splitlines())


def wrap(text: str, width: int = CONTENT_WIDTH) -> list[str]:
    """Break a paragraph at CONTENT_WIDTH so centring has something to centre.

    A line wider than the block runs off the right edge once it carries the
    left pad, and then wraps at whatever column the terminal happens to end at
    -- which reads as a broken layout rather than a long sentence.

    Leading indent is preserved. A bullet hangs two further, to clear its own
    "- " marker; a plain paragraph stays flush, because indenting its second
    line makes it look like a list item that lost its bullet.
    """
    import textwrap

    lead = " " * (len(text) - len(text.lstrip()))
    hang = lead + ("  " if text.lstrip().startswith("- ") else "")
    return textwrap.wrap(text.strip(), width, initial_indent=lead, subsequent_indent=hang) or [""]


class Frame(NamedTuple):
    """How one full screen's rows are spent, top to bottom."""

    top: int
    header: int
    body: int
    bottom: int


def frame_rows(available: int, height: int | None, header: int = 0, *, margin: int = MARGIN) -> Frame:
    """Split `available` screen rows into top margin, header, body, bottom margin.

    The one place the margin arithmetic lives, so `center_vertically` and the
    tests cannot drift apart. Guarantees, in order of precedence:

    1. Every field is >= 0 and the four sum to exactly `available`. A negative
       Dimension is not a cosmetic bug -- prompt_toolkit raises on it, and the
       whole point of this module's guards is that layout never takes the
       prompt down with it.
    2. `body` never exceeds `available - header - 2*margin`. Content taller
       than that SCROLLS inside the frame rather than overflowing past the
       bottom edge, which is why the body gets a fixed height instead of its
       preferred one.
    3. `top` and `bottom` are each at least `margin` (default MARGIN) -- until
       the terminal is too short to afford it, when the margin shrinks.
       Whitespace is what gives way on a tiny screen.
    """
    available = max(1, available)
    header = max(0, min(header, available - 1))
    margin = max(0, min(margin, (available - header - 1) // 2))
    body_max = max(1, available - header - 2 * margin)
    body = body_max if height is None else max(1, min(height, body_max))
    extra = max(0, available - header - body)
    top = min(extra, max(margin, extra // 2))
    return Frame(top=top, header=header, body=body, bottom=extra - top)


def top_spacer(height: int) -> int:
    """Blank rows `page()` prints above a block of `height` rows.

    `page()` cannot reserve rows the way a prompt_toolkit layout can -- it is
    plain prints onto a screen `clear()` has already blanked, so the bottom
    margin is simply the rows it declines to fill. That makes the top spacer
    the only knob, and it carries both jobs: the MARGIN, and the centring.

    Two rules survive from before the margin existed:

    * A block taller than the SCREEN still gets no spacer at all. Centring it
      would only choose which end to amputate, and the top is the end with the
      verdict on it.
    * Between those, the margin gives way before the content does: a block that
      fits the screen but not the framed area keeps every line, with whatever
      margin is left over.
    """
    screen = max(1, rows())
    framed_height = max(1, screen - 2 * MARGIN)
    return min(MARGIN + max(0, framed_height - height) // 2, max(0, screen - height))


def page(
    lines: list[str], prompt: str | None = None, *, copyable: bool | str = False,
    progress: Sequence[str] | None = None,
) -> str:
    """Show output in the shared frame; a pause uses scrollable content.

    Piped output remains plain text. Live progress without a prompt leaves
    its latest state visible. Reports with a prompt keep Continue and keyboard
    help in the same place as other pages. Copy includes the full original
    report, including rows outside the viewport.
    """
    progress = progress if progress is not None else onboarding_header()
    raw = "\n".join(lines).splitlines()
    if not interactive():
        # Verbatim: hard-wrapping piped output only breaks a grep.
        print("\n".join([*(progress or []), *raw]))
        return ""
    if prompt is not None:
        import questionary

        title, *details = raw or ["Probe Research"]
        question = questionary.select(
            "Continue", choices=[questionary.Choice("Continue", value="")],
            style=style(), pointer=pointer(), instruction=" ",
        )
        hint = "enter continue · tab read · pgup/dn · esc back"
        if copyable:
            hint = "enter continue · c copy · tab read · pgup/dn · esc back"

            @question.application.key_bindings.add("c", eager=True)
            @question.application.key_bindings.add("C", eager=True)
            def copy_report(event):
                # A page that shows a summary copies the report it summarises.
                _copy_to_clipboard(copyable if isinstance(copyable, str) else "\n".join(lines), event.app.output)

        sectioned(question, title=title, lines=details, prompt=prompt, instruction=hint)
        ask(question, progress=progress)
        return ""
    body: list[str] = []
    width = max(1, min(CONTENT_WIDTH, columns() - left_pad() - 1))
    for line in raw:
        # Wrapped HERE, not by the terminal: a line that overflows the block
        # wraps back to column 0, which breaks the centred column the whole
        # page is built on.
        body += wrap(line, width) if len(line) > width else [line]
    screen = max(1, rows())
    margin = safe_margin(screen)
    pinned = [*header_lines(progress), ""] if progress else []
    pinned = pinned[:max(0, screen - 2 * margin - 1)]
    room = max(1, screen - 2 * margin - len(pinned))
    if len(body) > room:
        # Live progress must not scroll the heading under terminal chrome.
        # Keep the title and most recent status, marking omitted history.
        hidden = len(body) - room + 1
        body = ([body[0], f"… {hidden} earlier lines hidden"[:width], *body[-(room - 2):]]
                if room > 2 else body[:room])
    clear()
    if _Window.entered:
        _Window.shown = list(raw)
    print("\n" * margin, end="")
    for line in [*pinned, *(indent(line) if line.strip() else "" for line in body)]:
        print(line)
    return ""


def style():
    """Questionary styling.

    Two deliberate choices:

    * `highlighted` is `noreverse`. The default inverts the whole entry into a
      block of background colour, which on a multi-line choice paints three
      lines of solid white and is genuinely hard to read.
    * `selected` is green, so a ticked box reads as ticked at a glance rather
      than needing you to compare two similar glyphs.
    * `separator` and `instruction` are warm tan, not grey. At #6c6c6c the
      headings and hints read as disabled; #b56f28 is the amber the
      dashboard's status dots use (globals.css), so the two surfaces share a
      palette -- its lighter tint #f7ecdd was tried first and washed out.
      `nav_back` is the one deliberate grey survivor -- see `dim_band_back`.
    """
    import questionary

    return questionary.Style(
        [
            ("qmark", "fg:#5f87ff bold"),
            ("question", "bold"),
            ("pointer", "fg:#5f87ff bold"),
            ("highlighted", "noreverse bold"),
            ("selected", "fg:#00af5f noreverse"),
            ("separator", "fg:#b56f28"),
            ("instruction", "fg:#b56f28"),
            ("nav_back", "fg:#6c6c6c"),
            ("answer", "fg:#00af5f bold"),
            ("danger", "fg:#d75f5f"),
        ]
    )


def use_checkmarks() -> None:
    """Swap questionary's ●/○ for ✔/○.

    `common` does `from questionary.constants import INDICATOR_SELECTED`, so the
    name is bound at import time and patching `questionary.constants` has no
    effect. The module that actually reads it is the one to patch.

    Still used by prompts that let questionary draw the box. The capability
    picker draws its own -- see `TICK` / `UNTICK` and `checkbox_control`.
    """
    from questionary.prompts import common

    common.INDICATOR_SELECTED = "✔"
    common.INDICATOR_UNSELECTED = "○"


#: The box we draw OURSELVES, on rows that carry one.
TICK = "✔"
UNTICK = "○"
#: The MIDDLE of a three-state row (`setup.row_box`). A third glyph rather than
#: a tick reused: a cycling row drawn with two glyphs makes two of its three
#: states look identical, and on the tracking default the pair that would
#: collide is `read-only` and `off` -- the state where the team's history is
#: still searchable and the state where it is not.
HALF = "◐"
#: The `daemon` position of the same row: recording is on, and something other
#: than the agent does it. Filled rather than ticked so it never reads as `on`.
AUTO = "◉"


def content_height(message: str, choices=(), instruction: str = "") -> int:
    """How many rows the prompt will occupy.

    Counted, not asked. `Container.preferred_height()` needs a running event
    loop and returns a placeholder without one, which silently produced a
    22-row spacer for 44 rows of content and pushed the BOTTOM off instead --
    the same bug wearing a different hat.

    Pass the prompt's `instruction` too when the LAST rows matter: questionary
    appends it to the question line at render, and if the combined line wraps
    at the terminal edge every count below it is one row short -- the body
    window folds its final rows, which since the band moved to the bottom are
    exactly `‹ Back / Next ›`. Measured, not hypothetical: a 14-char longer
    instruction folded the band off a real 80x24 pty while blank rows sat
    unused below it.
    """
    import questionary

    rows = message.count("\n") + 1  # the message block, question included
    if instruction:
        # The question's own last line already carries its pad; questionary
        # renders `<last line> <instruction>` as one row, wrapping at the edge.
        last = message.rsplit("\n", 1)[-1]
        if len(last) + 1 + len(instruction) >= columns():
            rows += 1
    for choice in choices:
        if isinstance(choice, questionary.Separator):
            rows += 1
        else:
            rows += str(getattr(choice, "title", "")).count("\n") + 1
    # Only a list prompt draws an instruction line. A confirm renders its
    # answer inline on the last message row, so counting one for it would sit
    # the whole page half a row high.
    return rows + (1 if choices else 0)


def header_lines(header: str | Sequence[str] | None) -> list[str]:
    """Normalise a `header=` argument into the rows that get pinned.

    Public because the caller needs to know what its header will cost before it
    counts the rest: the header sits OUTSIDE `content_height()`, which counts
    only what questionary draws. Long lines are wrapped to CONTENT_WIDTH and
    every line carries the same `left_pad()` as the block below it, so a pinned
    path lines up with the question rather than floating at column 0.

    Accepts a plain string (split on newlines) or any sequence of lines.
    """
    if header is None:
        return []
    raw = header.splitlines() if isinstance(header, str) else list(header)
    out: list[str] = []
    width = max(1, min(CONTENT_WIDTH, columns() - left_pad() - 1))
    for line in raw:
        for part in wrap(line, width) if len(line) > width else [line]:
            out.append(indent(part) if part.strip() else "")
    return out


def center_vertically(
    question,
    height: int | None = None,
    header: str | Sequence[str] | None = None,
    *,
    margin: int = MARGIN,
    progress: Sequence[str] | None = None,
):
    """Render full-screen, with shared pages anchored and legacy prompts centred.

    questionary renders inline, growing downward from the cursor, so anything
    taller than the room below it scrolls -- which is what kept eating the first
    rows of the state block, and is worse in a block-based terminal like Warp
    where the block boundary is not where a classic terminal's would be.

    Full screen removes the problem outright: prompt_toolkit owns the viewport,
    so there is no "above" to scroll into. It is also the only way centring
    becomes possible at all.

    The layout is four bands -- top margin, pinned header, body, bottom margin
    -- sized by `frame_rows()`. Three consequences worth stating:

    * The top and bottom bands are EXACT, so the body is whatever is left. That
      is what makes content taller than the frame scroll inside it instead of
      running off the bottom edge: squeezed below its preferred height,
      questionary's choice window scrolls itself to keep the pointed row
      visible -- it emits a `[SetCursorPosition]` token, and that is what
      prompt_toolkit scrolls to. Step screens keep the state block above it;
      the main menu keeps status and choices together, expanding into spare
      bottom space before scrolling the whole page on a short terminal.
    * NOT a ScrollablePane, which is the obvious thing to reach for and is
      wrong here. It follows the FOCUSED window's cursor, and the focused
      window is questionary's input buffer up in the message block -- so the
      pane sits at scroll 0 and the choices below the fold become unreachable.
      Bounding the band lets each window scroll on its own cursor instead.
    * `header` rows are pinned ABOVE the body, so a folder path stays readable
      at the bottom of a long list. They are NOT part of `height`.

    Every reach into questionary/prompt_toolkit internals is guarded, same
    posture as `checkbox_control`: questionary is pinned `>=2.0,<3` and a
    library reshuffle must degrade the prompt, never fail to render it.
    """
    try:
        from prompt_toolkit.layout import HSplit, Layout, Window
        from prompt_toolkit.layout.controls import FormattedTextControl
        from prompt_toolkit.layout.dimension import Dimension

        app = question.application
        inner = app.layout.container
        focused = app.layout.current_window
        pinned = header_lines(header)
        def progress_lines():
            return header_lines(progress if progress is not None else onboarding_header())

        def progress_height():
            lines = progress_lines()
            return len(lines) + 1 if lines else 0

        def frame() -> Frame:
            from prompt_toolkit.application import get_app

            screen_rows = get_app().output.get_size().rows
            available = max(1, screen_rows - progress_height())
            if (getattr(question, "_probe_sectioned", False)
                    or getattr(question, "_probe_continuous", False)):
                frame = frame_rows(available, None, len(pinned), margin=safe_margin(screen_rows))
                fit_choices = getattr(question, "_probe_fit_choices", None)
                if fit_choices is not None:
                    # Keep the top clearance, but let a complete menu use
                    # spare whitespace below it before it has to scroll.
                    spare = max(0, frame.bottom - 2)
                    preferred = fit_choices(frame.body + spare)
                    extra = min(spare, max(0, preferred - frame.body))
                    frame = frame._replace(body=frame.body + extra, bottom=frame.bottom - extra)
                return frame
            return frame_rows(
                available, height, len(pinned), margin=max(margin, safe_margin(screen_rows)),
            )

        def band(name: str):
            return lambda: Dimension.exact(getattr(frame(), name))

        question._probe_body_height = lambda: frame().body

        # Padding surrounds the entire UI, including the progress header.
        bands = [Window(height=band("top"))]
        if progress is not None or _onboarding.get() is not None:
            bands.append(Window(
                height=lambda: Dimension.exact(progress_height()),
                content=FormattedTextControl(lambda: "\n".join(progress_lines()) + "\n"),
                wrap_lines=False, always_hide_cursor=True,
            ))
        if pinned:
            bands.append(
                Window(
                    height=band("header"),
                    content=FormattedTextControl(
                        [("class:question", "\n".join(pinned))], focusable=False
                    ),
                    # Exact height is only exact if a long line cannot silently
                    # become two rows and push the body down.
                    wrap_lines=False,
                    always_hide_cursor=True,
                )
            )
        bands += [HSplit([inner], height=band("body")), Window(height=band("bottom"))]

        app.full_screen = True
        app.layout = Layout(HSplit(bands), focused_element=focused)
    except Exception:  # noqa: BLE001 - layout is cosmetic, never break the prompt
        pass
    if _Window.armed:
        full_window(question)
    return question


def full_window(question) -> None:
    """Draw this prompt over the whole of the wizard's window.

    `app.full_screen = True` above does NOT do this, and never did: prompt_toolkit
    reads full-screen from the RENDERER, which the Application built with its
    own flag before this module saw it. So every prompt drew INLINE, from the
    cursor down, and a terminal that treats inline output as a transcript
    (Warp) scrolled it instead of handing the keys to the menu.

    The renderer is switched here, but the alternate screen stays the
    `window`'s: a prompt that entered and left it itself would drop the whole
    wizard back to the shell's screen between two prompts. Entering is
    replaced by what entering looks like -- a clean window, cursor home -- and
    leaving by nothing, so the next screen draws over this one.
    """
    try:
        _enter_window()
        _new_screen()
        app = question.application
        output = app.output
        if output not in _Window.patched:
            # Leaving wipes the window too: prompt_toolkit's last paint parks
            # the cursor below the prompt, and whatever prints next would land
            # under a prompt that is already answered.
            output.enter_alternate_screen = lambda: output.write_raw("\033[H\033[2J")
            output.quit_alternate_screen = lambda: output.write_raw("\033[H\033[2J")
            _Window.patched.append(output)
        app.renderer.full_screen = True
    except Exception:  # noqa: BLE001 - an inline prompt beats no prompt
        pass


#: A menu row that ends something (sign out): red, and bold while pointed at.
#: Set as `choice.probe_style`; `menu` draws it.
DANGER_STYLE = "class:danger"


def plain_title(title) -> str:
    """A choice title as text, whether a string or formatted `(style, text)` parts."""
    if isinstance(title, list):
        return "".join(part[1] for part in title)
    return str(title)
from probe.cli.wizard.terminal.choices import pointer  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.terminal.clipboard import _copy_to_clipboard  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.terminal.forms import ask, sectioned, text  # noqa: E402 -- pieces need each other; the front door loads this one first
