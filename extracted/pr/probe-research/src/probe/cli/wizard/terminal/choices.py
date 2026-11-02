"""the continuous main menu and its choice prompts (select, checkbox, collapsed groups), with the pointer and qmark markers."""

from __future__ import annotations
from collections.abc import Callable, Sequence


# NOTE: no vertical centring. questionary emits the qmark BEFORE the message,
# so leading newlines inside the message strand a lone `?` at the top of the
# screen with the content pushed below it. Padding outside the prompt does not
# work either -- prompt_toolkit renders relative to the cursor, so the padding
# is what scrolls the top away. Vertically centred would be nice; wrong-looking
# is worse than top-aligned.


class Framed(str):
    """Plain-text fallback plus the sections used by interactive prompts."""

    def __new__(cls, value: str, *, title: str, lines: Sequence[str], prompt: str):
        result = super().__new__(cls, value)
        result.sections = {"title": title, "lines": list(lines), "prompt": prompt}
        return result


def select(message: str, **kwargs):
    """Questionary select with the installer's shared page sections."""
    import questionary

    question = questionary.select(message, **kwargs)
    if isinstance(message, Framed):
        question._probe_content = message.sections
    return question


def collapsed(choices: Sequence, pointed) -> list:
    """`choices` with every group but the one holding `pointed` cut to its heading.

    A group is a heading Separator and the rows after it, up to the next
    heading. The blank rows directly ABOVE a heading belong to that heading --
    they are its air -- and are kept only where there is something to separate:
    above the first group, and either side of the open one. Collapsed headings
    otherwise stack, one line each, which is the space this saves.

    A group with no heading is never collapsed: there would be nothing left of
    it on screen, and the cursor would still walk through its rows unseen.
    """
    from questionary import Separator

    def blank(choice) -> bool:
        return isinstance(choice, Separator) and not str(choice.title).strip()

    groups: list[tuple[list, list]] = []  # (heading air + heading, rows)
    air: list = []
    for choice in choices:
        if blank(choice):
            air.append(choice)
        elif isinstance(choice, Separator):
            groups.append(([*air, choice], []))
            air = []
        else:
            if not groups:
                groups.append(([], []))
            groups[-1][1].extend([*air, choice])
            air = []
    if groups:
        groups[-1][1].extend(air)

    open_index = next((i for i, (_, rows) in enumerate(groups) if pointed in rows), None)
    shown: list = []
    for index, (lead, rows) in enumerate(groups):
        headed = any(not blank(choice) for choice in lead)
        expanded = index == open_index or not headed
        if expanded or index == 0 or (open_index is not None and index - 1 == open_index):
            shown.extend(lead)
        else:
            shown.extend(choice for choice in lead if not blank(choice))
        if expanded:
            shown.extend(rows)
    return shown


def menu(
    message: Framed,
    *,
    live_lines: Callable[[], Sequence[str]] | None = None,
    collapse: bool = False,
    hint: Callable[[object], str | None] | None = None,
    **kwargs,
):
    """A continuous main menu; separate content/action panes belong to steps.

    The status and choices share one window. Expand into spare bottom space
    before tightening empty gaps. Only a terminal too short for the complete
    menu scrolls, and then the whole page moves together.

    `collapse` draws only the cursor's group open and every other group as its
    heading alone (`collapsed`). It changes the DRAWING, never the list the
    keys walk: questionary's own up/down still step through every row in
    order, so moving past a group's last row opens the next group on its
    first row -- the cursor goes exactly where it went before, and the menu
    folds itself around it.

    `hint` names extra keys for the pointed row: handed the row's value, it
    returns a phrase for the help line (`←→ switch`) or None. And a caller
    that repaints a row after a key press does it through
    `question._probe_retitle(choice, title)`: every frame redraws the rows from
    their stored titles, so a title assigned straight onto the choice is gone
    by the next frame.
    """
    from prompt_toolkit.filters import to_filter
    from prompt_toolkit.layout import HSplit, Layout, ScrollOffsets, VSplit, Window
    from prompt_toolkit.layout.controls import FormattedTextControl
    from prompt_toolkit.layout.dimension import Dimension
    from questionary import Separator

    question = select(message, **kwargs)
    control = checkbox_control(question)
    if control is None:
        return question
    app = question.application
    content = message.sections
    if live_lines is not None:
        def refresh_lines(_app):
            # Read once per frame, so sizing and painting use one consistent
            # snapshot even when several jobs advance while this menu is open.
            content["lines"] = list(live_lines())

        app.before_render += refresh_lines
        app.refresh_interval = 1.0
    original = control.text
    full_choices = list(control.choices)
    initial_indent = body_indent()
    titles = {choice: choice.title for choice in full_choices if not isinstance(choice, Separator)}

    def retitle(choice, title: str) -> None:
        # Stored at the indent the menu was BUILT with, which is what `tokens`
        # rewrites to the current one on every frame.
        titles[choice] = title.replace("\n" + body_indent(), "\n" + initial_indent)

    question._probe_retitle = retitle
    compact_choices = [
        choice for choice in full_choices
        if not (isinstance(choice, Separator) and not str(choice.title).strip())
    ]

    def width():
        return max(1, min(app.output.get_size().columns, left_pad() + CONTENT_WIDTH + 1))

    def tokens():
        # Choices carry continuation indentation from construction. Reflow it
        # alongside the status when the terminal width changes.
        control.pointer = pointer()
        pointed = control.get_pointed_at()
        for choice, title in titles.items():
            text = title.replace("\n" + initial_indent, "\n" + body_indent())
            style = getattr(choice, "probe_style", None)
            # A styled row is drawn as formatted text (questionary shows a list
            # title as given), bold while the cursor is on it like any row.
            choice.title = [(f"{style} bold" if choice is pointed else style, text)] if style else text
        text_width = max(1, min(CONTENT_WIDTH, width() - left_pad() - 1))
        pad = " " * left_pad()
        title = indent(content["title"]) + "\n\n"
        line_no = title.count("\n")
        hover_rows.clear()
        body = []
        for line in content["lines"]:
            for row in line_rows(line, text_width, default="class:text"):
                text = "".join(cell for style, cell in row if style != ZERO_WIDTH_ESCAPE)
                if text.strip():
                    body.append((row[0][0], pad))
                body.extend(row)
                name = getattr(line, "hover", None)
                if name:
                    hover_rows[line_no] = name
                    room = text_width - len(text) - 3
                    if hovered["line"] == line_no and room > 0:
                        # A tooltip: the name the logo stands for, at the row's end.
                        body.append(("class:text", "  "))
                        body.append(("class:text reverse", f" {name} "[:room]))
                body.append((row[-1][0], "\n"))
                line_no += 1
        return [
            ("class:question", title),
            *body,
            *([("class:text", "\n")] if body else []),
            ("class:question", indent(content["prompt"]) + "\n"),
            *original(),
        ]

    if collapse:
        walk = tokens

        def tokens():
            # Draw from the folded list, then put the walked list straight
            # back: `pointed_at` indexes whichever list is current, and the
            # key handlers between two paints must see the full one.
            every, at = control.choices, control.pointed_at
            pointed = every[at]
            shown = collapsed(every, pointed)
            control.choices, control.pointed_at = shown, shown.index(pointed)
            try:
                return walk()
            finally:
                control.choices, control.pointed_at = every, at

    control.text = tokens
    control.focusable = to_filter(True)

    # Hover (Richard 2026-10-06: "make it so that you can somehow see the
    # name if you maybe hover over it"). Only a menu whose rows carry a name to
    # reveal takes the mouse: while it does, selecting text needs Option/Shift.
    # `hover_rows` maps a content line to its name and is rebuilt every paint.
    hover_rows: dict[int, str] = {}
    hovered: dict[str, int | None] = {"line": None}
    if any(getattr(line, "hover", None) for line in content["lines"]):
        from prompt_toolkit.mouse_events import MouseEventType

        click = control.mouse_handler

        def mouse_handler(event):
            if event.event_type == MouseEventType.MOUSE_MOVE:
                line = event.position.y if event.position.y in hover_rows else None
                if line != hovered["line"]:
                    hovered["line"] = line
                    app.invalidate()
                return None
            if event.event_type in (MouseEventType.SCROLL_UP, MouseEventType.SCROLL_DOWN):
                return None  # the keys move the menu; a wheel scrolling it fights them
            return click(event)

        control.mouse_handler = mouse_handler
        # Both: the renderer copies the flag when the application is built.
        app.mouse_support = app.renderer.mouse_support = to_filter(True)

    def text_height(text):
        # Each density candidate needs fresh fragments: the live control caches
        # them for a whole render pass, including earlier sizing calls.
        measured = FormattedTextControl(text).create_content(width(), app.output.get_size().rows)
        return sum(
            measured.get_height_for_line(index, width(), None)
            for index in range(measured.line_count)
        )

    def footer_height():
        # The blank above the key hints, then the hints however many rows
        # they wrap to.
        return 1 + help_rows()[0][1].count("\n") + 1

    def preferred_height():
        return footer_height() + text_height(tokens)

    def fit_choices(maximum: int) -> int:
        pointed = control.get_pointed_at()
        for choices in (full_choices, compact_choices):
            control.choices = choices
            control.pointed_at = choices.index(pointed)
            preferred = preferred_height()
            if preferred <= maximum:
                break
        return preferred

    def body_height():
        available = question._probe_body_height()
        return max(1, min(preferred_height(), available) - footer_height())

    def help_parts() -> list[str]:
        # Words, not glyphs alone: this line is how someone who has never seen
        # the wizard learns that the arrows move through it. A hint that says
        # what Enter does replaces the plain `enter choose`.
        extra = hint(getattr(control.get_pointed_at(), "value", None)) if hint else None
        enter = None if extra and "enter" in extra else "enter choose"
        return ["↑ ↓ move", *(extra.split(" · ") if extra else []),
                *([enter] if enter else []), "esc back"]

    def help_rows():
        # Broken BETWEEN phrases, never inside one: "esc / to go back" across
        # two rows reads as two instructions.
        room = max(1, min(CONTENT_WIDTH, width() - left_pad() - 1))
        lines: list[str] = []
        for part in help_parts():
            if lines and len(lines[-1]) + 3 + len(part) <= room:
                lines[-1] += " · " + part
            else:
                lines.append(part)
        return [("class:instruction", "\n".join(indent(line) for line in lines))]

    window = Window(
        control, wrap_lines=True, always_hide_cursor=True,
        width=lambda: Dimension.exact(width()),
        height=lambda: Dimension.exact(body_height()),
        scroll_offsets=ScrollOffsets(
            bottom=lambda: max(0, text_height(body_indent() + plain_title(control.get_pointed_at().title)) - 1),
        ),
    )
    # The key hints sit on the window's LAST rows, under any spare space, so
    # they are in the same place however long the menu is at the moment.
    app.layout = Layout(HSplit([
        VSplit([window, Window()]),
        Window(height=Dimension(min=0, preferred=0, weight=1)),
        Window(height=1),
        Window(
            FormattedTextControl(help_rows),
            height=lambda: Dimension.exact(help_rows()[0][1].count("\n") + 1),
            wrap_lines=False,
        ),
    ]), focused_element=window)
    question._probe_continuous = True
    question._probe_fit_choices = fit_choices
    return question


def checkbox(message: str, **kwargs):
    """The same page layout with multi-selection and existing picker bindings."""
    import questionary

    question = questionary.checkbox(message, **kwargs)
    if isinstance(message, Framed):
        question._probe_content = {
            **message.sections,
            "instruction": "↑↓ choose · space toggle · enter · tab read · pgup/dn · esc back",
        }
    return question


def framed(title: str, lines: list[str], question: str, *, progress: str | None = None) -> str:
    """State block + question as ONE prompt message.

    Printing the state separately and letting questionary render underneath is
    what cut the top off: prompt_toolkit takes the screen after the print, and
    anything already emitted scrolls away. Handing it the whole block means it
    owns the layout and nothing can drift out of view.
    """
    header = [title, "", progress, ""] if progress is not None else [title, ""]
    block = [*header, *lines, "", question]
    padded = [(" " * left_pad() + ln if ln.strip() else "") for ln in block]
    # The first line rides behind the qmark, which already carries the indent.
    padded[0] = padded[0].lstrip()
    return Framed("\n".join(padded), title=title, lines=lines, prompt=question)


def qmark() -> str:
    """The `?` marker, carrying the indent itself.

    Padding the MESSAGE instead leaves the marker stranded at column 0 with its
    text 78 columns away, which is what shipped in 0.13.0 and looks like a
    rendering fault. questionary emits `(qmark)(space)(message)`, so putting the
    pad inside the marker moves the whole line together.
    """
    return " " * left_pad() + "?"


def pointer() -> str:
    """The `»` marker, likewise carrying the indent.

    questionary draws `" {pointer} "` on the highlighted row and
    `" " * (2 + len(pointer))` on the others, so a padded pointer keeps every
    row aligned -- selected and unselected end at the same column.
    """
    return " " * max(0, left_pad() - 1) + "»"


def body_indent() -> str:
    """Where a choice's continuation lines start -- and where its box starts.

    The pointer prefix only exists on the FIRST line of a choice; wrapped
    description lines get nothing, so they carry their own pad.

    Derived from `pointer()` rather than from `left_pad()` directly, because
    what a continuation line has to line up with is the column questionary
    actually starts a title on: `" {pointer} "` / `" " * (2 + len(pointer))`.
    Those agree with `left_pad() + 2` on every terminal wide enough to have a
    left pad -- and disagree by one on a terminal too narrow for one, since the
    pointer cannot be shorter than the `»` in it. That was a cosmetic
    one-column drift while nothing was drawn in the gap; it is a rectangle with
    a rail out of true now, so the two are the same number.
    """
    return " " * (2 + len(pointer()))


def point_at(control, predicate) -> None:
    """Park the cursor on the first row `predicate` accepts.

    Load-bearing again. questionary seats the cursor on whichever selectable
    row comes first, which was harmless while the nav band was a Separator it
    would skip; the band takes the cursor now, and where a step OPENS is a
    product decision -- on `Next ›`, so continuing costs one keystroke and the
    options are reached by going deliberately up -- not something to inherit
    from the library's iteration order.
    """
    try:
        for index, choice in enumerate(control.choices):
            if getattr(choice, "disabled", None):
                continue
            if predicate(getattr(choice, "value", None)):
                control.pointed_at = index
                return
    except Exception:  # noqa: BLE001 - a cursor in the wrong place is not a crash
        pass
from probe.cli.wizard.terminal.boxes import checkbox_control  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.terminal.forms import text  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.terminal.layout import ZERO_WIDTH_ESCAPE, indent, line_rows, plain_title, style  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.terminal.terminal import CONTENT_WIDTH, left_pad, rows, window  # noqa: E402 -- pieces need each other; the front door loads this one first
