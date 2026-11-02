"""the Settings screen: grouped rows (ticks and cycling rows) and the menu that applies them."""

from __future__ import annotations
from probe.cli.wizard.settings.settings import Setting, cycle_value, cycling_settings, value_label

#: The screen, as GROUPS -- the same shape as the action menu's ACTION_GROUPS
#: and for the same reason: the next setting lands in a named group instead of
#: lengthening one flat column.
SETTINGS_GROUPS: tuple[tuple[str, tuple[Setting, ...]], ...] = (
    ("Updates", (Setting.AUTO_UPDATE,)),
    ("Images", (Setting.PASTED_IMAGES,)),
)

#: The daemon's page: Enter on the main menu's Who records row while the daemon
#: records, and straight after switching to it (Richard 2026-09-29).
DAEMON_GROUPS: tuple[tuple[str, tuple[Setting, ...]], ...] = (
    ("What the daemon sees", (Setting.REASONING_SUMMARIES,)),
)

#: Settings drawn on the MAIN MENU instead of the settings screen. Still part
#: of the registry -- read by `read_settings`, written by `apply_settings` --
#: so `grouped_settings` counts them as placed rather than as missing.
MENU_SETTINGS: frozenset[Setting] = frozenset(
    {Setting.TRACKING_DEFAULT, Setting.RECORDER_CLAUDE_CODE, Setting.RECORDER_CODEX, Setting.RECORDER_PI,
     Setting.RECORDER_KIMI_CODE}
)

#: Row copy, `MENU_COPY`-shaped (title, detail lines) so `_bind_menu_keys` can
#: repaint these rows exactly the way it repaints the agent picker's. The
#: capability rows deliberately echo the confirm screen's bullets — same
#: feature, same words, on and off.
SETTINGS_COPY: dict[Setting, tuple[str, tuple[str, ...]]] = {
    Setting.AUTO_UPDATE: (
        "Automatic updates",
        ("Updates the CLI and plugins at session start.",),
    ),
    # On by default for every device, offered only here (Richard 2026-10-12:
    # "default on even for currently installed people ... dont add a step in
    # the install path"). The capture tap reads it before each upload.
    Setting.PASTED_IMAGES: (
        "Upload images you paste",
        ("Images you paste into a prompt upload with the session, unscanned.",),
    ),
    Setting.TRACKING_DEFAULT: (
        "Probe in new sessions",
        # The leading "" is a BLANK LINE, not a stray element: this row's
        # detail is a disclosure rather than a caption, and it reads as one
        # once it is not crowded against the title. `_menu_row` wraps every
        # detail line, and `tui.wrap("")` is one empty line -- so the spacing
        # lives in the copy, where a reader can see it, instead of in a render
        # rule that would silently apply to rows nobody wanted it on.
        ("", "New sessions read and write Probe."),
    ),
    Setting.RECORDER_CLAUDE_CODE: ("Who records in Claude Code", ("",)),
    Setting.RECORDER_CODEX: ("Who records in Codex", ("",)),
    Setting.RECORDER_PI: ("Who records in pi", ("",)),
    Setting.RECORDER_KIMI_CODE: ("Who records in Kimi Code", ("",)),
    # One setting per coding agent, written for the daemon into each agent's
    # own config (`reasoning_summaries`): it changes what the user sees too,
    # so the row says so.
    Setting.REASONING_SUMMARIES: (
        "Daemon sees the agent's reasoning",
        # Leading "" like the Who-records rows beside it: a disclosure, spaced as one.
        ("",
         "Claude Code and Codex write reasoning summaries for the daemon.",
         "They show in your terminal and upload with the session.",
         "New sessions only."),
    ),
}

#: The "Who records" rows' detail per position. `daemon` mints the daemon's key
#: when committed, so it says whose key it is and where its deletes stop (the
#: trash, or the researcher's yes). The ONLY place the daemon is chosen (Richard
#: 2026-09-29): the tracking default below is on / read / off.
_RECORDER_STATE_COPY: dict[str, tuple[str, ...]] = {
    "agent": (
        "",
        "Your agent records and searches Probe itself.",
    ),
    "daemon": (
        "",
        "The daemon records and searches; your agent instruments runs.",
        "Deletes go to the trash or ask first, unless prompts are off.",
        # The daemon position also edits the agent's own config
        # (`reasoning_summaries`), and the copy says so before the commit.
        "Turns on reasoning summaries unless you set them (below).",
    ),
}

#: The detail lines a CYCLING row paints in EACH of its states, for the rows
#: whose states are not one sentence with a glyph swapped. Only the tracking
#: default is here, and it is here because its three states are three different
#: disclosures: `read` stops the `probe` CLI's write commands and leaves the MCP
#: read surface running, while `off` stops the reads too -- and someone looking
#: at a row that only said "off" would have no way to tell which of those they
#: were getting. The row used to be a tick box whose empty state carried a
#: footnote pointing AWAY from this screen ("disable MCP in your coding agent to
#: stop it reading"); the third state is that footnote, made pressable.
#:
#: Keyed by `Setting` then by STORED state name (`session_marker.STATES`), values
#: are the detail lines alone -- the title is composed from `SETTINGS_COPY` plus
#: the state's word, so there is one place each half lives. A setting absent from
#: this table reads out of `SETTINGS_COPY` whatever it holds, which is every
#: other row. `grouped_settings` pins the keys against the real vocabulary.
SETTINGS_STATE_COPY: dict[Setting, dict[str, tuple[str, ...]]] = {
    Setting.TRACKING_DEFAULT: {
        # Blank first line in every state, exactly as in `SETTINGS_COPY` -- all
        # three have to space the same way, or a press jogs the text up a row.
        "full": ("", "New sessions read and write Probe."),
        "read-only": ("", "Write commands are blocked; search still works."),
        "off": ("", "No Probe calls at all, so no search either; the service captures none."),
    },
    Setting.RECORDER_CLAUDE_CODE: _RECORDER_STATE_COPY,
    Setting.RECORDER_CODEX: _RECORDER_STATE_COPY,
    Setting.RECORDER_PI: _RECORDER_STATE_COPY,
    Setting.RECORDER_KIMI_CODE: _RECORDER_STATE_COPY,
}

#: The band's forward label on the settings screen. `Next ›` would promise
#: another step; this screen has none -- the way forward IS the commit.
APPLY_TITLE = "Set settings  ›"


def grouped_settings() -> tuple[tuple[str, tuple[Setting, ...]], ...]:
    """`SETTINGS_GROUPS`, checked against the rest of the registry first.

    Same contract as `grouped_actions`: the tables are separate and a setting
    needs ALL of them. A group entry with no copy renders a titleless row;
    copy in no group is a setting that silently stopped being reachable; and
    an enum member in neither is a writer with no screen. None of these show
    up as an error on their own -- the screen just quietly has the wrong
    number of things on it -- so the agreement is asserted where it is used.
    """
    listed = tuple(s for _, settings in (*SETTINGS_GROUPS, *DAEMON_GROUPS) for s in settings)
    placed = set(listed) | MENU_SETTINGS
    if (
        len(set(listed)) != len(listed)
        or set(listed) & MENU_SETTINGS
        or placed != set(SETTINGS_COPY)
        or placed != set(Setting)
    ):
        raise AssertionError(
            f"settings registry disagrees: groups list {listed}, the menu draws "
            f"{sorted(MENU_SETTINGS)}, copy has {tuple(SETTINGS_COPY)}, "
            f"enum has {tuple(Setting)}"
        )
    # Per-state copy is OPTIONAL per row, so it is checked for strays rather
    # than for totality: a key here that is not a setting paints nothing and
    # would otherwise sit in the file looking like it works. Its STATE keys are
    # checked for totality, though, against the vocabulary itself -- a state
    # added to `session_marker.STATES` with no words here would render as the
    # previous state's sentence under a moved glyph, which is the one failure
    # this row cannot afford: copy saying reads still work over a state where
    # they do not.
    cycles = cycling_settings()
    stray = set(SETTINGS_STATE_COPY) - set(Setting)
    if stray:
        raise AssertionError(f"per-state copy names settings that do not exist: {stray}")
    for setting, per_state in SETTINGS_STATE_COPY.items():
        order = cycles.get(setting)
        if order is None:
            raise AssertionError(f"{setting!r} has per-state copy but does not cycle")
        if tuple(per_state) != tuple(order):
            raise AssertionError(
                f"{setting!r} copy covers {tuple(per_state)}, the switch has {tuple(order)}"
            )
    return SETTINGS_GROUPS


def settings_choices(
    current: "dict[Setting, bool | str]",
    indent: str,
    *,
    hidden: "frozenset[Setting]" = frozenset(),
    groups: "tuple[tuple[str, tuple[Setting, ...]], ...] | None" = None,
) -> tuple[
    list,
    dict[Setting, object],
    dict[Setting, tuple[str, tuple[str, ...]]],
    dict[Setting, dict[str, tuple[str, tuple[str, ...]]]],
]:
    """The settings screen's rows, and a handle on each one.

    Built here rather than inline so a test can render the REAL layout -- the
    one that decides where the cursor starts and which rows carry a box -- and
    not a rehearsal of it that drifts the first time this changes. (The same
    contract the capability picker's `capability_choices` carried before the
    install stopped having a picker.)

    BOTH copies come back, and the caller must hand them to `_bind_menu_keys`:
    it repaints rows from the copy it was handed, per state for a cycling row.
    """
    import questionary

    from probe.cli.wizard import terminal as tui

    cycles = cycling_settings()
    copy = dict(SETTINGS_COPY)
    # A cycling row wears its state as a WORD beside the title, not only as a
    # glyph: three shapes are learnable, but only after you have pressed the key
    # three times, and the state this row is in is the one thing a person must
    # be able to read without pressing anything.
    state_copy = {
        setting: {
            state: (f"{SETTINGS_COPY[setting][0]} — {value_label(setting, state)}", detail)
            for state, detail in per_state.items()
        }
        for setting, per_state in SETTINGS_STATE_COPY.items()
        if setting not in MENU_SETTINGS
    }
    rows: dict[Setting, questionary.Choice] = {}
    choices: list = []
    for group, settings in (grouped_settings() if groups is None else groups):
        visible = [s for s in settings if s not in hidden]
        if not visible:
            continue
        # A blank leads each group -- the first doubles as the air between the
        # question and the list (the 0.95.1 rule), the rest separate groups.
        # A blank FOLLOWS the heading for the same reason `step_heading` has
        # one: it is where the first row of the group paints the top of its
        # selection rectangle.
        choices.append(questionary.Separator(" "))
        choices.append(questionary.Separator(tui.heading(group)))
        choices.append(questionary.Separator(" "))
        for index, setting in enumerate(visible):
            if index:
                choices.append(questionary.Separator(" "))
            value = cycle_value(setting, current[setting]) if setting in cycles else bool(current[setting])
            title, detail = _row_copy(setting, copy, state_copy, value=value)
            row = questionary.Choice(
                title=_menu_row(title, detail, checked=value, indent=indent),
                value=setting,
                # A cycling row seeds its BOX from the first state, the only
                # thing a checkbox can say about three. `probe_cycle` carries
                # the rest and `_wire_picker.advance` keeps the two in step --
                # which is what the unwired fallback path falls back TO.
                checked=(value == cycles[setting][0]) if setting in cycles else value,
            )
            rows[setting] = row
            choices.append(row)
    return choices, rows, copy, state_copy


def run_settings_menu(
    current: "dict[Setting, bool | str]",
    *,
    hidden: "frozenset[Setting]" = frozenset(),
    groups: "tuple[tuple[str, tuple[Setting, ...]], ...] | None" = None,
    frame: "tuple[str, list[str], str] | None" = None,
):
    """The settings screen: the install panels' shape, pointed at what is left.

    Checkbox rows, ticked = on, grouped under headings like every other panel:
    Automatic updates and pasted-image uploads; a page handed `groups` draws its
    own rows, and a cycling row CYCLES rather than ticks (one state per press). Nothing
    is written while you press -- `→` on the `Set settings ›` band is the
    commit, and so is LEAVING: `←`/Escape after a change applies it too. They
    used to drop it without a word, and a researcher who switched a row and
    backed out found it reverted (2026-10-02). Returns None (quit), tui.BACK
    (left with nothing changed), or {Setting: bool | state}: the DRAWN rows as
    the user left them, a bool per checkbox and a STATE NAME per cycling row.

    `current` comes from the CALLER's read, never one of our own, so the boxes
    and the diff computed against what comes back are the same fact -- see
    `read_settings`.

    `hidden` names rows not to draw. `groups` and `frame` put another page on
    this machinery (the daemon's page, `DAEMON_GROUPS`).
    """
    import questionary

    from probe.cli.wizard import terminal as tui

    tui.use_checkmarks()  # the fallback path, if we cannot take the box over

    # The registry's fifth leg: a Setting added everywhere except
    # `read_settings` would otherwise surface as a raw KeyError drawing the
    # box, tracebacking the wizard instead of naming the drift.
    missing = [s for s in Setting if s not in current]
    if missing:
        raise AssertionError(f"read_settings reports no value for {missing}")

    indent = tui.body_indent()
    choices, rows, copy, state_copy = settings_choices(current, indent, hidden=hidden, groups=groups)
    cycles = {setting: order for setting, order in cycling_settings().items() if setting in rows}
    cycle_state = {setting: cycle_value(setting, current[setting]) for setting in cycles}

    # `frame`: another page on this screen's machinery (the daemon's page).
    message = tui.framed(*frame) if frame is not None else tui.framed(
        "Settings on this device:",
        [
            f"  {SETTINGS_COPY[setting][0]:<28} {'on' if current[setting] else 'off'}"
            for setting in (Setting.AUTO_UPDATE, Setting.PASTED_IMAGES)
        ],
        "How should this device behave?",
    )

    if not rows:
        # Unreachable today -- the Automatic updates row renders
        # unconditionally -- but kept as the guard for whatever hides rows
        # next: a picker with zero rows is a trap, so the degraded shape is
        # Back alone under the state block.
        choices = [
            questionary.Separator(" "),
            questionary.Choice(
                title=f"Back\n{indent}  Return to the main menu. Nothing changes.",
                value=tui.BACK,
            ),
        ]
        return tui.ask(
            tui.select(
                message,
                choices=choices,
                instruction="(enter goes back)",
                style=tui.style(),
                qmark=tui.qmark(),
                pointer=tui.pointer(),
            ),
            height=tui.content_height(message, choices),
        )

    choices.extend(nav_footer(next_title=APPLY_TITLE))
    instruction = "(enter picks this row · ↑ to change)"
    question = tui.checkbox(
        message,
        choices=choices,
        instruction=instruction,
        style=tui.style(),
        qmark=tui.qmark(),
        pointer=tui.pointer(),
    )
    # What the rows held when `←`/Escape left the screen, so leaving can keep it.
    left_with: dict = {}

    def keep_on_back(ctrl) -> None:
        left_with["selected"] = list(getattr(ctrl, "selected_options", None) or [])
        left_with["cycle"] = dict(getattr(ctrl, "probe_cycle", None) or {})

    control = _bind_menu_keys(
        question,
        rows,
        copy=copy,
        indent=indent,
        state_copy=state_copy,
        cycles=cycles,
        cycle_state=cycle_state,
        on_back=keep_on_back,
    )
    if control is None:
        # Unwirable -- same posture as the capability picker: strip the band
        # rather than ship a label nothing is listening for, and let the
        # library's own enter-submits apply the boxes.
        choices = without_nav(choices)
        instruction = "(space to toggle, enter to apply · esc goes back)"
        question = tui.checkbox(
            message,
            choices=choices,
            instruction=instruction,
            style=tui.style(),
            qmark=tui.qmark(),
            pointer=tui.pointer(),
        )
    else:
        dress_band(question, control)

    def answer(chosen: set, landed: dict) -> dict:
        # The cycling rows answer from `probe_cycle`, which is the only place
        # their third state can be written down. `control` is None only on the
        # unwired fallback, where questionary drew its own two-state box --
        # there the row answers from the box, meaning exactly what that boolean
        # has always meant (`setting_state`), rather than inventing a state
        # nobody could see.
        return {
            setting: (
                landed.get(setting, cycle_value(setting, setting in chosen))
                if setting in cycles
                else setting in chosen
            )
            for setting in rows
        }

    picked = tui.ask(question, height=tui.content_height(message, choices, instruction=instruction))
    if picked is tui.BACK and left_with:
        # Left with `←`/Escape: what was switched is kept, like `→` would.
        # Unchanged rows are still "nothing changed".
        kept = answer(set(left_with["selected"]), left_with["cycle"])
        drawn = {
            setting: cycle_value(setting, current[setting]) if setting in cycles else bool(current[setting])
            for setting in rows
        }
        return kept if kept != drawn else tui.BACK
    if picked is None or picked is tui.BACK:
        return picked
    landed = dict(getattr(control, "probe_cycle", None) or {}) if control is not None else {}
    return answer(set(picked), landed)
from probe.cli.wizard.screens.nav_band import dress_band, nav_footer, without_nav  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.screens.picker_keys import _bind_menu_keys, _menu_row, _row_copy  # noqa: E402 -- pieces need each other; the front door loads this one first
