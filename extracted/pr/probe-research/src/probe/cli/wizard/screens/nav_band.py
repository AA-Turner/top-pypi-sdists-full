"""the Back/Next band every step wears: where it sits, what it says, and the cursor box painted on the row under the cursor."""

from __future__ import annotations


#: The value of the row that ENDS a step, and of the row that goes BACK one.
#: Neither is a capability and neither is ever returned in a Selection.
#: What those rows say. A verb, not a noun: every other row is a thing you turn
#: on, and these two are the only things you DO.
NEXT_TITLE = "Next  ›"
BACK_TITLE = "‹  Back"

#: The band's left half, verbatim. Shared with `tui.dim_band_back`, which
#: repaints exactly this span grey while the `Next ›` half keeps the bright
#: separator colour -- the two must agree on the text or the repaint misses.
NAV_BACK_LEFT = f"{BACK_TITLE}   ←"

#: The value of the nav band ROW. One row, and one questionary Choice: the
#: library draws exactly one choice per line, so two cursor stops on one line
#: cannot be two choices. Which END the cursor is on is `NAV_STOPS` below,
#: tracked by the picker rather than by `pointed_at`.
NAV_BAND = "__nav_band__"

#: The band's two ends, IN CURSOR ORDER -- which is not their order on screen.
#:
#: `Next ›` comes first because it is where every step opens: continuing costs
#: one keystroke, and `↑` off the band goes straight to the options, which is
#: the whole point of parking there. `‹ Back` sits one `↓` further on. Reading
#: order (Back on the left, Next on the right) is what the row SHOWS; this is
#: the order the cursor walks, and the rectangle is what reconciles the two.
NAV_NEXT = "next"
NAV_BACK = "back"
NAV_SKIP = "skip"
NAV_STOPS: tuple[str, ...] = (NAV_NEXT, NAV_BACK)


def nav_row(choices: list):
    """The nav band row in a built row list, or None.

    Found by VALUE first and by content second. The agent step repaints this row
    to carry its refusal, and reaching for it positionally survives exactly
    until something else is added to the band.

    The content fallback is not dead weight: `run_confirm_install` builds its
    band through the same helper but on a `select` prompt, and any future screen
    that hand-rolls a band still resolves here rather than silently returning
    None and losing its Back key.
    """
    by_value = next((c for c in choices if getattr(c, "value", None) == NAV_BAND), None)
    if by_value is not None:
        return by_value
    return next((c for c in choices if BACK_TITLE in str(getattr(c, "title", ""))), None)


def without_nav(choices: list) -> list:
    """The same rows with the nav band stripped out.

    For the ONE case where the band is worse than nothing: `checkbox_control()`
    came back None, so `_wire_picker` installed no bindings and questionary's
    own rules are in force -- Enter submits, and its cursor parks on the first
    selectable row, which is `‹ Back`. A row that says "Back" and, when you
    press Enter on it, submits every ticked capability instead is not a
    degraded affordance, it is a mislabelled one, and on this screen the thing
    it silently agrees to is shipping your sessions off the machine.

    Escape still goes back (`tui.bind_escape` is wired outside the picker), so
    stripping the band costs discoverability on a path nobody should be on and
    removes a row that actively lies.
    """
    import questionary

    kept = [
        choice
        for choice in choices
        if getattr(choice, "value", None) != NAV_BAND
        and not (
            # Every worded separator: the band's pieces and the group headings,
            # which are the only other separators that carry text.
            isinstance(choice, questionary.Separator)
            and str(choice.title).strip()
        )
    ]
    # Drop the blanks left stranded at either edge -- the footer's spacer above
    # the band, or a leading one if the band ever moves back to the top.
    while kept and isinstance(kept[0], questionary.Separator) and not str(kept[0].title).strip():
        kept.pop(0)
    while kept and isinstance(kept[-1], questionary.Separator) and not str(kept[-1].title).strip():
        kept.pop()
    return kept


def nav_layout(*, forward: str | None = "→", next_title: str = NEXT_TITLE,
               back_title: str = BACK_TITLE, focus=None, skip_title=None):
    """The band row AS DRAWN, plus where the rectangle on it sits.

    Returns `(text, lead, width)`: the finished line, and the offset and width
    of the `┌───┐` that belongs above and below it. One function rather than a
    text half and a geometry half, because they are one fact -- a box measured
    somewhere other than where the label was placed is a cursor pointing at
    nothing, and that is a bug you can only see on a terminal.

    Both labels sit on FIXED columns, and the rails are drawn around them
    rather than pushing them along: `‹ Back` starts where every option's text
    starts (`tui.BOX_GUTTER` in) and `Next ›` ends where every option row's
    rectangle ends, focused or not. So moving the cursor between the two ends
    moves the box and nothing else -- a band whose labels slid two columns
    every time you pressed `↓` would read as the screen redrawing itself.

    `forward=None` drops the right half, and with it that end's cursor stop,
    for a screen that only offers Back.
    """
    from probe.cli.wizard import terminal as tui

    left = f"{back_title}   ←"
    rails = 2 + tui.BOX_GUTTER  # `│ ` … ` │`: what a rectangle costs a row
    right = None if forward is None else f"{forward}   {next_title}"
    total = len(left) + rails if right is None else max(tui.box_width(), len(left) + rails)
    if skip_title and right and total < len(left) + len(right) + len(skip_title) + 3 * rails:
        skip_title = "Skip"
        if total < len(left) + len(right) + len(skip_title) + 3 * rails:
            left, right = back_title.replace("‹  ", ""), next_title.replace("  ›", "")
    cells = [" "] * total

    def place(text: str, at: int) -> None:
        for offset, char in enumerate(text):
            if 0 <= at + offset < len(cells):
                cells[at + offset] = char

    back_at = tui.BOX_GUTTER
    place(left, back_at)
    next_at = total - len(right) - tui.BOX_GUTTER if right is not None else total
    if right is not None:
        place(right, next_at)
    skip_at = (total - len(skip_title)) // 2 if skip_title else 0
    if skip_title:
        place(skip_title, skip_at)

    if focus == NAV_BACK:
        place("│", back_at - tui.BOX_GUTTER)
        place("│", back_at + len(left) + 1)
        return "".join(cells).rstrip(), back_at - tui.BOX_GUTTER, len(left) + rails
    if focus == NAV_NEXT and right is not None:
        place("│", next_at - tui.BOX_GUTTER)
        place("│", next_at + len(right) + 1)
        return "".join(cells).rstrip(), next_at - tui.BOX_GUTTER, len(right) + rails
    if focus == NAV_SKIP and skip_title:
        place("│", skip_at - tui.BOX_GUTTER)
        place("│", skip_at + len(skip_title) + 1)
        return "".join(cells).rstrip(), skip_at - tui.BOX_GUTTER, len(skip_title) + rails
    return "".join(cells).rstrip(), back_at - tui.BOX_GUTTER, len(left) + rails


def nav_stops_for(forward, skip_title=None) -> tuple[str, ...]:
    """Which ends this band draws, in `NAV_STOPS` order."""
    if skip_title:
        return (NAV_NEXT, NAV_SKIP, NAV_BACK) if forward is not None else (NAV_SKIP, NAV_BACK)
    return NAV_STOPS if forward is not None else (NAV_BACK,)


def nav_band(*, forward: str | None = "→", next_title: str = NEXT_TITLE,
             back_title: str = BACK_TITLE, focus=None, skip_title=None) -> str:
    """`‹ Back  ←` on the left, `→  Next ›` on the right, in ONE row.

    They were two stacked rows, both left-aligned, which spent two lines saying
    what one line says better. Back and Next are a PAIR -- opposite ends of the
    same axis -- so stacking them hid the one relationship the band exists to
    show, and cost a row of the step's own content to do it. Left and right
    edges say "these two go opposite ways" before a word is read.

    ONE row, TWO cursor stops. questionary draws one choice per line, so the
    band cannot be two Choices; `NAV_STOPS` and the picker's own `↑`/`↓` supply
    the second stop, and the rectangle `nav_layout` places is what says which
    end Enter will fire. `←`/`→` and Escape still work from anywhere, so the
    keys printed on the band remain true -- they are shortcuts now rather than
    the only way through.
    """
    return nav_layout(forward=forward, next_title=next_title, back_title=back_title,
                      focus=focus, skip_title=skip_title)[0]


def step_heading(step: int) -> list:
    """The heading that leads a step's rows. Three separators, no cursor stops.

    A BLANK FIRST -- the 0.95.1 fix, carried into this layout. questionary
    renders the choice list flush against the question, so without it the
    first row of the list sits one line under the last thing you read: the
    boundary between "what you are being asked" and "what follows" had
    disappeared. The band no longer opens the step, so the heading is what
    gets the air now.

    A BLANK LAST, which is not decoration: it is the row the first option's
    rectangle draws its `┌───┐` into. Every other row inherits one from the
    blank that separates it from the row above; the first row of a group has a
    heading there instead, so without this it is the one row on screen that
    could be pointed at and not boxed.
    """
    import questionary

    from probe.cli.wizard import terminal as tui

    return [
        questionary.Separator(" "),
        questionary.Separator(tui.heading(step_name(step))),
        questionary.Separator(" "),
    ]


def dress_band(question, control) -> None:
    """The band's two token repaints, wired the one way every screen wants them.

    Both reach into questionary's token stream and both are guarded there, so
    this is a convenience rather than a safety net -- but the pairing is a rule:
    the pointer is suppressed on the band (the rectangle marks the cursor there)
    and `‹ Back` is dimmed EXCEPT while it is the end the cursor is on.
    """
    from probe.cli.wizard import terminal as tui

    tui.blank_pointer_when(question, lambda value: value == NAV_BAND)
    band = nav_row(getattr(control, "choices", []))
    back_title = getattr(band, "nav", {}).get("back_title", BACK_TITLE)
    tui.dim_band_back(question, f"{back_title}   ←", active=lambda: nav_focus(control) == NAV_BACK)


def nav_footer(*, forward: bool = True, next_title: str = NEXT_TITLE,
               back_title: str = BACK_TITLE, skip_title=None) -> list:
    """The nav band, drawn UNDER the step's rows, as a row the cursor can hold.

    Under the rows, not above them. The band used to open each step, which put
    the way FORWARD on screen before any of the choices it would confirm. At
    the bottom the band sits where the reading ends, after the rows it acts on
    -- and it is where every step now OPENS, so `↑` is what reaches the options
    and pressing Enter straight away accepts them as shown.

    THREE rows, not two, and only one of them carries text. The blanks above
    and below are where the selection rectangle's `┌───┐` and `└───┘` are
    painted when the cursor is on the band (see `tui.box_edge`): the box lives
    in rows the layout already spends, so nothing below it moves when the
    cursor arrives and `content_height` stays a count of fixed rows. The upper
    blank does its old job too -- the band reads as chrome rather than as the
    last option's continuation line.

    `forward=False` drops the right half and its cursor stop for a screen that
    only offers Back.
    """
    import questionary

    band = questionary.Choice(
        title=nav_band(forward="→" if forward else None, next_title=next_title,
                       back_title=back_title, skip_title=skip_title),
        value=NAV_BAND,
    )
    # Carried ON the row because the picker REBUILDS its text on every render:
    # the box has to follow the cursor between the band's two ends, and the
    # agent step swaps `forward` for a refusal. Storing the ingredients beats
    # re-deriving them from a string that has already been boxed once.
    band.nav = {"forward": "→" if forward else None, "next_title": next_title}
    if back_title != BACK_TITLE:
        band.nav["back_title"] = back_title
    if skip_title:
        band.nav["skip_title"] = skip_title
    return [
        questionary.Separator(" "),
        band,
        questionary.Separator(" "),
    ]


def nav_focus(control) -> str | None:
    """Which end of the nav band the cursor is on, or None if it is elsewhere.

    Read off the control because that is the object every caller already holds;
    the state itself belongs to `_wire_picker`, which is the only thing allowed
    to move it.

    The `or None if it is elsewhere` half is load-bearing, not tidiness: a band
    with only ONE end has `focus` permanently pinned
    to it, so a caller that read the state alone would think the cursor was
    parked on `‹ Back` for the whole screen and quietly stop dimming it.
    """
    state = getattr(control, "probe_nav", None) or {}
    try:
        if getattr(control.get_pointed_at(), "value", None) != NAV_BAND:
            return None
    except Exception:  # noqa: BLE001 - a colour question is never worth a crash
        return None
    return state.get("focus")


def band_stops(band) -> tuple[str, ...]:
    """The band's cursor stops for this screen, in cursor order.

    A step with no forward half has one stop, not two: `nav_stops_for` is the
    single place that decides, so a screen cannot grow a cursor stop for a
    label it does not draw.
    """
    if band is None:
        return ()
    return nav_stops_for(
        getattr(band, "nav", {}).get("forward"), getattr(band, "nav", {}).get("skip_title"),
    )


def _logical_lines(title: str, pad: str) -> list[str]:
    """A row's lines with the absolute left pad taken back off.

    questionary prefixes only a choice's FIRST line, so `_menu_row` gives every
    continuation line the pad itself. The rectangle is drawn in row-relative
    columns, so the pad has to come off before the rails go on and back on
    after -- otherwise the second line's rail lands `left_pad()` columns right
    of the first line's.
    """
    lines = str(title).split("\n")
    return [lines[0]] + [
        line[len(pad) :] if line.startswith(pad) else line.lstrip() for line in lines[1:]
    ]


def _paint_boxes(control, *, band, focus, slots, cache) -> None:
    """Put the rectangle on the row under the cursor, and the gutter on the rest.

    Runs on EVERY render (see `_wire_picker`), not on every keystroke, because
    the cursor moves by six different keys -- arrows, `j`/`k`, `Ctrl-N`/`Ctrl-P`
    -- and a repaint hung off any subset of them is a box that lags the cursor
    on whichever one was forgotten.

    `slots` are the blank separator rows collected before the first paint: the
    rectangle's `┌───┐` and `└───┘` go in the blanks the layout already spends
    above and below each row, so the box costs no lines and nothing on screen
    moves when the cursor arrives. Every slot is reset each pass; a border left
    behind by the previous cursor position is a rectangle around nothing.

    `cache` maps a row to the (plain, boxed) pair last painted, so a title the
    caller's redraw did NOT rewrite is un-boxed from the cache instead of being
    boxed a second time. Without it the static rows -- the confirm screen's
    `Install ›`, which no redraw owns -- gain a rail per render.
    """
    import questionary

    from probe.cli.wizard import terminal as tui

    choices = list(control.choices)
    for slot in slots:
        slot.title = " "
    pad = tui.body_indent()
    width = tui.box_width()
    pointed = control.get_pointed_at()
    for index, choice in enumerate(choices):
        if isinstance(choice, questionary.Separator):
            continue
        if choice is band:
            # The band draws ITSELF: its two labels sit on fixed columns and the
            # rails go around one of them, which is not what `box_rails` does to
            # a row with one field. `nav_layout` owns that geometry.
            text, lead, span = nav_layout(
                **getattr(band, "nav", {}), focus=focus if choice is pointed else None
            )
            choice.title = text
            if choice is pointed:
                _paint_edges(choices, index, span, lead=lead, slots=slots)
            continue
        remembered = cache.get(id(choice))
        title = str(choice.title)
        plain = remembered[0] if remembered and title == remembered[1] else title
        lines = _logical_lines(plain, pad)
        if choice is pointed:
            drawn = tui.box_rails(lines, width)
            _paint_edges(choices, index, width, lead=0, slots=slots)
        else:
            drawn = tui.box_gutter(lines)
        boxed = ("\n" + pad).join(drawn)
        cache[id(choice)] = (plain, boxed)
        choice.title = boxed


def _paint_edges(choices: list, index: int, width: int, *, lead: int, slots: list) -> None:
    """Draw the rectangle's top and bottom into the blank rows either side."""
    from probe.cli.wizard import terminal as tui

    for offset, top in ((-1, True), (1, False)):
        neighbour = index + offset
        if not 0 <= neighbour < len(choices):
            continue
        row = choices[neighbour]
        if any(row is slot for slot in slots):
            row.title = tui.box_edge(width, lead=lead, top=top)
from probe.cli.wizard.screens.install_steps import step_name  # noqa: E402 -- pieces need each other; the front door loads this one first
