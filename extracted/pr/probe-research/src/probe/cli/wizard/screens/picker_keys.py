"""wire a step's keys: Enter activates the row under the cursor, Back/Next stops, and capability checkbox rows with their glyph and words."""

from __future__ import annotations
from probe.cli.wizard.state.state import Capability


def _wire_picker(
    question,
    *,
    redraw=None,
    can_submit=None,
    on_leave=None,
    on_back=None,
    single=False,
    cycles=None,
    cycle_state=None,
):
    """One rule for every step: ENTER ACTIVATES THE ROW UNDER THE CURSOR.

    On a capability that means toggle; on the nav band it means whichever end
    the rectangle is around -- `Next ›` (where every step opens) or `‹ Back`.
    questionary's own rule is space-toggles / enter-submits, which is the
    checkbox convention -- but the wizard's two checkbox screens ran BACK TO
    BACK with opposite meanings for Enter, because one of them had its own
    binding and the other did not. Whichever you learned first was wrong on the
    next screen.

    THE BAND TAKES THE CURSOR, and it is where the cursor starts. Continuing
    costs one Enter, and the options are reached by going deliberately up --
    which is the point: a step you are happy with should not ask you to travel
    to leave it, and one you want to change should ask you to say so. `↑`/`↓`
    walk `NAV_STOPS` while the cursor is on the band, so its two ends behave
    like two rows despite sharing one line; `←`/`→` and Escape keep working
    from anywhere as shortcuts.

    `single=True` is for a `select` prompt, where a row is an ANSWER rather than
    a checkbox: Enter on a non-band row submits it instead of ticking it.

    `cycles` is `{value: (state, ...)}` for rows that CYCLE instead of ticking:
    the same key does the same thing -- act on this row -- but it advances one
    step round that tuple instead of flipping a box, and wraps. The states live
    on `control.probe_cycle`, which the caller reads back after the prompt
    exits. `cycle_state` seeds them; a row with no seed starts at `[0]`.

    `can_submit` is the step's own guard (the agent picker needs at least one
    agent). It is checked HERE rather than through questionary's `validate=`,
    which only ever runs on questionary's submit -- the path this binding
    replaces. A step whose guard says no simply does not leave, and says so on
    the Next row; see `run_agent_menu`.

    Every reach into questionary is guarded. If any of it stops working the
    prompt still runs with the library's own behaviour rather than failing to
    render -- a picker that looks slightly wrong beats a wizard that cannot ask
    the question at all.
    """
    import questionary

    from probe.cli.wizard import terminal as tui

    control = tui.checkbox_control(question)
    if control is None:
        return None  # library defaults; enter still submits, space still toggles

    cycles = dict(cycles or {})
    # The cycling rows' state, and the ONLY copy of it: `selected_options` has
    # two positions and these rows have three, so a screen that read the box
    # back would lose whichever state the box cannot spell. Kept on the control
    # because the control is what outlives the prompt -- see `run_settings_menu`.
    control.probe_cycle = {
        value: (cycle_state or {}).get(value) or order[0] for value, order in cycles.items()
    }
    band = next((c for c in control.choices if getattr(c, "value", None) == NAV_BAND), None)
    stops = band_stops(band)
    # Read back by `nav_focus`, which is how a caller styles the end the cursor
    # is on without reaching into this closure.
    state = {"focus": stops[0] if stops else None}
    control.probe_nav = state
    slots = [
        choice
        for choice in control.choices
        if isinstance(choice, questionary.Separator) and not str(choice.title).strip()
    ]
    cache: dict[int, tuple[str, str]] = {}

    def refresh() -> None:
        if redraw is not None:
            redraw(control)

    def leave(event, result) -> None:
        control.is_answered = True
        event.app.exit(result=result)

    def submit(event) -> None:
        if can_submit is not None and not can_submit(control):
            refresh()
            return
        if on_leave is not None:
            leave(event, on_leave(control))
            return
        # No `on_leave`: answer with the pointed row. `getattr`, not
        # `.value` -- `activate` routes here when NOTHING is pointed at, and an
        # AttributeError raised inside a key binding takes the prompt down
        # rather than surfacing anywhere a user could act on.
        leave(event, getattr(control.get_pointed_at(), "value", None))

    def retreat(event) -> None:
        # The toggles the user made before backing out are reported, not
        # discarded: leaving a screen is not the same as un-deciding on it.
        if on_back is not None:
            on_back(control)
        leave(event, tui.BACK)

    def activate(event) -> None:
        """Enter, and it means ONE thing: act on the row you are on.

        On the band that reads off the rectangle rather than the row -- the two
        ends share a line, so "the row you are on" is only half an answer there
        and the box is what supplies the other half.
        """
        pointed = control.get_pointed_at()
        if pointed is None:
            submit(event)
            return
        if pointed.value == NAV_BAND:
            if state["focus"] == NAV_SKIP:
                leave(event, tui.SKIP)
                return
            (retreat if state["focus"] == NAV_BACK else submit)(event)
            return
        if single:
            submit(event)
            return
        toggle(control, pointed.value)
        refresh()

    def step(delta: int) -> None:
        """questionary's own move, skipping separators, in one direction."""
        move = control.select_next if delta > 0 else control.select_previous
        move()
        for _ in range(control.choice_count):
            if control.is_selection_valid():
                return
            move()

    def travel(delta: int) -> None:
        """`↑`/`↓`, with the band counting as one stop per END.

        The band is a single questionary Choice -- the library draws one choice
        per line -- so the second stop cannot come from `pointed_at`. It comes
        from walking `NAV_STOPS` while the cursor sits on the band and only
        stepping off once the walk runs out of ends.

        Entering the band from ABOVE lands on the first stop (`Next ›`, so the
        common path is Enter and nothing else) and from BELOW on the last, which
        is what `↑` out of the top of the list has to do to be reversible.
        """
        if band is not None and stops and control.get_pointed_at() is band:
            index = (stops.index(state["focus"]) if state["focus"] in stops else 0) + delta
            if 0 <= index < len(stops):
                state["focus"] = stops[index]
                return
        step(delta)
        if band is not None and stops and control.get_pointed_at() is band:
            state["focus"] = stops[0] if delta > 0 else stops[-1]

    def toggle(ctrl, value) -> None:
        if value in cycles:
            advance(ctrl, value)
            return
        if value in ctrl.selected_options:
            ctrl.selected_options.remove(value)
        else:
            ctrl.selected_options.append(value)

    def advance(ctrl, value, *, to=None) -> None:
        """One press of a CYCLING row: the next state round, wrapping.

        Membership is kept in step with the FIRST state rather than left to
        drift, because it is what the row falls back to on the degraded path
        where our bindings never got installed -- and a `selected_options` that
        disagreed with `probe_cycle` would make which path you were on decide
        what the screen committed.
        """
        order = cycles[value]
        if to is None:
            here = ctrl.probe_cycle.get(value)
            to = order[(order.index(here) + 1) % len(order)] if here in order else order[0]
        ctrl.probe_cycle[value] = to
        if to == order[0] and value not in ctrl.selected_options:
            ctrl.selected_options.append(value)
        elif to != order[0] and value in ctrl.selected_options:
            ctrl.selected_options.remove(value)

    def bulk(event, select_all: bool) -> None:
        """questionary's own `a` / `i`, routed through OUR repaint.

        The library binds bare `a` (select all) and `i` (invert) eagerly and
        mutates `selected_options` directly. That was fine while questionary
        drew the boxes -- it repaints from the same list. We turned its
        indicator OFF (`draw_own_boxes`) and paint the box into the title
        ourselves, so its handlers changed the ANSWER without changing the
        SCREEN: untick capture, press `a`, and the row still rendered `○
        Session capture` while the submitted Selection carried capture=True.
        The consent gate cannot be a screen the answer disagrees with.
        """
        for choice in control.choices:
            value = getattr(choice, "value", None)
            # The band is a ROW, not an option: `a` ticking it would put the
            # sentinel in the answer and leave a rail drawn round a checkbox
            # nobody offered.
            if value is None or value == NAV_BAND or getattr(choice, "disabled", None):
                continue
            if value in cycles:
                # `a` means "everything on", which on a cycling row is its first
                # state; `i` inverts, and the nearest thing a three-state row has
                # to an inversion is the step the space bar would have taken.
                advance(control, value, to=cycles[value][0] if select_all else None)
                continue
            wanted = select_all if select_all else value not in control.selected_options
            if wanted and value not in control.selected_options:
                control.selected_options.append(value)
            elif not wanted and value in control.selected_options:
                control.selected_options.remove(value)
        refresh()

    refresh()

    try:
        from prompt_toolkit.keys import Keys

        bindings = question.application.key_bindings

        @bindings.add("c-m", eager=True)  # Enter
        def _(event) -> None:  # pragma: no cover - requires a live terminal
            activate(event)

        @bindings.add(" ", eager=True)
        def _(event) -> None:  # pragma: no cover - requires a live terminal
            activate(event)

        # Registered AFTER questionary's, so prompt_toolkit's `matches[-1]`
        # resolution picks ours. Same keys, same meaning, but they repaint.
        @bindings.add("a", eager=True)
        def _(event) -> None:  # pragma: no cover - requires a live terminal
            bulk(event, select_all=True)

        @bindings.add("i", eager=True)
        def _(event) -> None:  # pragma: no cover - requires a live terminal
            bulk(event, select_all=False)

        # EVERY key questionary moves the cursor with, not just the arrows: the
        # band's second stop lives outside `pointed_at`, so a movement key left
        # on the library's handler would step straight over `‹ Back` and make
        # which key you pressed decide whether that row exists.
        def mover(delta: int):
            def _move(event) -> None:  # pragma: no cover - requires a live terminal
                travel(delta)

            return _move

        for key in (Keys.Down, "j", Keys.ControlN):
            bindings.add(key, eager=True)(mover(1))
        for key in (Keys.Up, "k", Keys.ControlP):
            bindings.add(key, eager=True)(mover(-1))

    except Exception:  # noqa: BLE001 - never let a binding break the prompt
        pass

    # `→` only where the band actually draws a forward half, so the shortcut
    # always agrees with the visible forward action.
    tui.bind_step_keys(
        question, on_back=retreat, on_next=submit if (band is None or NAV_NEXT in stops) else None
    )
    try:
        # Registered after `tui.bind_escape`, so this one wins. Escape is the
        # other half of the `‹ Back` label and has to route through `retreat`
        # too, or it exits without reporting the toggles `←` keeps.
        @question.application.key_bindings.add("escape", eager=True)
        def _(event) -> None:  # pragma: no cover - requires a live terminal
            retreat(event)

    except Exception:  # noqa: BLE001 - never let a binding break the prompt
        pass

    try:
        # The rectangle is painted from the RENDER, not from the key handlers.
        # `control.text` is the token source prompt_toolkit calls every frame
        # (the same door `tui.dim_band_back` goes through), so the box follows
        # the cursor however it moved -- including paths this module never
        # bound, and including the very first frame, before any key is pressed.
        original = control.text

        def repaint():
            try:
                refresh()
                _paint_boxes(control, band=band, focus=state["focus"], slots=slots, cache=cache)
            except Exception:  # noqa: BLE001 - an unboxed row beats no prompt
                pass
            return original()

        control.text = repaint
    except Exception:  # noqa: BLE001 - an unboxed row beats no prompt
        pass
    return control


def row_box(value: "bool | str") -> str:
    """The glyph one row wears for the value it currently carries.

    A BOOL is a checkbox: ticked or empty. A STRING is a CYCLING row's state
    name, and each state gets its own glyph -- two glyphs over three states
    would draw two of them identically, and the pair that would collide on the
    tracking default is `read-only` and `off`: the state where the team's
    history is still searchable and the state where it is not.

    The names come from `session_marker`, never a copy of them here: the wizard
    and the `/probe` switch have to agree about how many states there are, and a
    second spelling of the vocabulary is where that agreement would rot. An
    unrecognised state draws the empty box, matching `default_session_state`'s
    posture of never *quietly* claiming more is on than is.
    """
    from probe.cli.wizard import terminal as tui
    from probe.sdk import session_marker

    if isinstance(value, str):
        return {
            session_marker.STATE_FULL: tui.TICK,
            session_marker.STATE_DAEMON: tui.AUTO,
            session_marker.STATE_READ_ONLY: tui.HALF,
            session_marker.STATE_OFF: tui.UNTICK,
            # "Who records": `agent` is today's, ticked; `daemon` wears the
            # glyph above (a stored `daemon` session state is `on (daemon)`).
            session_marker.RECORDER_AGENT: tui.TICK,
        }.get(value, tui.UNTICK)
    return tui.TICK if value else tui.UNTICK


def _menu_row(title: str, detail: tuple[str, ...], *, checked: "bool | str", indent: str) -> str:
    """One capability row, box included.

    WE draw the box (see tui.draw_own_boxes). questionary's own is
    all-rows-or-nothing, and the "Next" row must not have one -- `○ Next` reads
    as an option someone forgot to tick rather than the way forward.

    `checked` is a bool on a checkbox row and a STATE NAME on a cycling one;
    `row_box` is the one place that difference is read.
    """
    from probe.cli.wizard import terminal as tui

    box = row_box(checked)
    # WRAPPED to the room actually available, not to a constant. prompt_toolkit
    # runs with autowrap off, so a detail longer than the terminal is CLIPPED,
    # not wrapped -- and on the capture row the half that disappears is the
    # clause naming where the data goes. At 60 columns this read "Sends this
    # device's Claude Code and Codex sessions to yo". A disclosure you cannot
    # finish reading is not a disclosure.
    #
    # `content_height` counts a choice's rows from the newlines in its title, so
    # wrapping here also keeps the frame arithmetic honest about how tall these
    # rows are.
    #
    # Measured against the RECTANGLE, not the terminal: the row is drawn inside
    # `tui.box_width()` columns, of which the rails and their padding take four
    # and a detail line's own two-space indent takes two. Wrapping to anything
    # wider puts text under the right rail -- or past the terminal edge on the
    # row that is not currently boxed, which is where it first showed up.
    room = max(20, tui.box_width() - (2 + tui.BOX_GUTTER) - 2)
    lines: list[str] = [f"{box} {title}"]
    for line in detail:
        lines.extend(tui.wrap(line, room))
    # The box sits on the title line only; wrapped detail lines clear it, so
    # they do not read as further options.
    return f"\n{indent}  ".join(lines)


def _row_copy(
    key,
    copy: dict,
    state_copy: dict | None,
    *,
    value: "bool | str",
) -> tuple[str, tuple[str, ...]]:
    """The words one row wears for the value it is currently carrying.

    Rows whose copy does not depend on their value have no `state_copy` entry
    and read out of `copy` whatever they hold -- which is every row except the
    "Who records" rows, whose states are different disclosures rather than one
    sentence with a glyph swapped. Kept as one
    function because the row is painted from THREE places (the first paint, the
    repaint on every press, and the strip when questionary keeps its own boxes),
    and a state-dependent lookup that only two of them do is a row that changes
    its mind when you touch it.
    """
    if isinstance(value, str) and state_copy and key in state_copy:
        per_state = state_copy[key]
        if value in per_state:
            return per_state[value]
    return copy[key]


def _bind_menu_keys(
    question,
    rows: dict[Capability, object],
    *,
    copy: dict[Capability, tuple[str, tuple[str, ...]]],
    indent: str,
    state_copy: dict | None = None,
    cycles: dict | None = None,
    cycle_state: dict | None = None,
    on_back=None,
    on_leave=None,
    exclusive: bool = False,
):
    """Wire step 2's picker: the shared key rule, plus our own checkboxes.

    Returns the control, or None when questionary's internals were unreachable
    -- which the caller has to act on rather than shrug at, because the nav band
    is only safe while WE own the keys.

    WE draw the boxes (`tui.draw_own_boxes`), because questionary's are
    all-rows-or-nothing and the nav rows must not have one -- `○ Next` reads as
    an option someone forgot to tick rather than the way forward. That is also
    why the boxes have to be repainted by hand on every toggle: the library is
    no longer doing it.

    `cycles` names the rows that CYCLE rather than tick -- `{value: (state,
    ...)}` -- and `cycle_state` says where each of them starts. Their state
    lives on the control (`probe_cycle`), which is what the caller reads back
    after the prompt exits; `state_copy` gives such a row DIFFERENT detail lines
    per state, for the rows where the states are not one sentence with a glyph
    swapped. Since we already repaint every row on every press, this costs a
    lookup; the caller that has no such row passes nothing and nothing changes.

    `exclusive` makes the boxes a RADIO: ticking a row unticks the one that was
    ticked, and the last tick cannot be taken away -- a default has to be
    something. `on_leave` replaces the answer (the ticked rows) with the
    caller's own reading of the control.
    """
    from probe.cli.wizard import terminal as tui

    own_boxes = tui.draw_own_boxes(question)
    radio: dict = {}

    def keep_one(control) -> None:
        ticked = [value for value in control.selected_options if value in rows]
        if "on" not in radio:
            radio["on"] = ticked[0] if ticked else None
        fresh = [value for value in ticked if value != radio["on"]]
        if len(fresh) == 1:
            radio["on"] = fresh[0]
        control.selected_options[:] = [] if radio["on"] is None else [radio["on"]]

    def redraw(control) -> None:
        if exclusive:
            keep_one(control)
        # `own_boxes` is False only when `checkbox_control()` returned None, and
        # `_wire_picker` bails on that same condition before it calls this -- so
        # this only ever runs with the boxes ours to draw. Kept as an assertion
        # of that coupling rather than a branch anyone should expect to take.
        if not own_boxes:
            return
        states = getattr(control, "probe_cycle", None) or {}
        for capability, row in rows.items():
            # A cycling row is drawn from ITS state, never from membership: the
            # membership list has two positions and the row has three, so the
            # box would stop moving after the first press.
            value = (
                states[capability]
                if capability in states
                else capability in control.selected_options
            )
            title, detail = _row_copy(capability, copy, state_copy, value=value)
            row.title = _menu_row(title, detail, checked=value, indent=indent)

    control = _wire_picker(
        question,
        redraw=redraw,
        on_leave=on_leave or (lambda control: [c for c in control.selected_options if c in rows]),
        on_back=on_back,
        cycles=cycles,
        cycle_state=cycle_state,
    )
    if control is None:
        return None
    if not own_boxes:
        # questionary is drawing its own indicator in front of a title that
        # already carries one; strip ours rather than ship `✔ ✔ CLI + MCP`.
        states = getattr(control, "probe_cycle", None) or {}
        for capability, row in rows.items():
            value = states.get(capability, False)
            title, detail = _row_copy(capability, copy, state_copy, value=value)
            row.title = _menu_row(title, detail, checked=value, indent=indent).split(" ", 1)[1]
    tui.point_at(control, lambda value: value == NAV_BAND)
    return control
from probe.cli.wizard.screens.nav_band import NAV_BACK, NAV_BAND, NAV_NEXT, NAV_SKIP, _paint_boxes, band_stops  # noqa: E402 -- pieces need each other; the front door loads this one first
