"""the Defaults step and menu: new-session tracking default, Who records row, and the daemon's consent page."""

from __future__ import annotations
from dataclasses import dataclass
from probe.foundation.compat.compat import StrEnum


#: What the Defaults row says under its state while an environment variable
#: holds it (`session_marker.state_env_override`): choosing here would write a
#: config value the variable then overrides, so the row says where to go.
DEFAULT_ENV_LOCKED_NOTE = "Locked by an environment variable."


def tracking_default_row(state: "str | None" = None) -> tuple[str, tuple[str, ...]]:
    """The main menu's Defaults row: the setting's name, a state's word, and
    what that word means.

    `state` is what the row SHOWS -- the machine's default when not given, or
    where `←`/`→` have switched (and saved) it (`run_action_menu`). The
    chevrons round the word are the sign that the arrows move it; a row an
    environment variable holds down has none, because they would not.

    The meaning is the per-state disclosure (`SETTINGS_STATE_COPY`), so the
    words for each state live in one place whether they are read on the menu or
    on the picker behind it. Their leading blank line is dropped: it spaced the
    row on the old settings screen, and on the menu a row's detail sits
    directly under its title like every other row's.
    """
    from probe.sdk import session_marker

    held = session_marker.state_env_override() is not None
    here = setting_state(session_marker.default_session_state())
    state = setting_state(state) if state is not None else here
    name = SETTINGS_COPY[Setting.TRACKING_DEFAULT][0]
    word = session_marker.state_label(state)
    title = f"{name} — {word}" if held else f"{name}  ‹ {word} ›"
    detail = tuple(line for line in SETTINGS_STATE_COPY[Setting.TRACKING_DEFAULT][state] if line)
    if held:
        detail = (*detail, DEFAULT_ENV_LOCKED_NOTE)
    set_by = session_marker.set_by_note() if state == here else None
    if set_by:
        detail = (*detail, f"{set_by[0].upper()}{set_by[1:]}.")
    return title, detail


#: The main menu's Who records row: its name, and what each position means.
RECORDER_ROW_TITLE = "Who records"
RECORDER_ROW_COPY: dict[str, tuple[str, ...]] = {
    "agent": ("Your agents record and search Probe themselves.",),
    "daemon": (
        "The Probe daemon records and searches for your agents.",
        "Deletes go to the trash or ask first, unless prompts are off.",
    ),
}


def recorder_row(
    value: "str | None" = None, caps_by_source: "dict | None" = None
) -> tuple[str, tuple[str, ...]]:
    """The main menu's Who records row, wearing `value` (the machine's when not
    given) between the chevrons that say `←`/`→` move it.

    On a machine on the daemon, a set-up agent still recording itself is named
    under it: the row read "daemon" while pi recorded itself (2026-10-02), and
    the Enter that moves it was nowhere on screen. Same set-up test as that
    Enter (`_run_recorder_action`): in `caps_by_source` and `configured`."""
    from probe.sdk import session_marker

    value = value or machine_recorder()
    copy = RECORDER_ROW_COPY[value]
    if value == session_marker.RECORDER_DAEMON and caps_by_source:
        behind = [
            source
            for source in RECORDER_SOURCES
            if source in caps_by_source
            and getattr(caps_by_source[source], "configured", False)
            and session_marker.recorder(source) != session_marker.RECORDER_DAEMON
        ]
        if behind:
            who = agent_label(tuple(behind))
            line = (
                f"{who} still records itself: Enter moves it to the daemon."
                if len(behind) == 1
                else f"{who} still record themselves: Enter moves them to the daemon."
            )
            copy = (*copy, line)
    return f"{RECORDER_ROW_TITLE}  ‹ {value} ›", copy


@dataclass(frozen=True)
class RecorderChoice:
    """The main menu's answer the moment its Who records row was switched: the
    value to apply, for every coding agent on this machine."""

    value: str


@dataclass(frozen=True)
class DefaultChoice:
    """A Defaults state to save with no picker. The menu row used to answer it
    on Enter; the row saves on each press now, and `_run_defaults_action`
    still takes one through `chosen=`."""

    state: str


class DefaultsRow(StrEnum):
    """The install's Defaults step, row by row: the main menu's Defaults group
    (who records, and what new sessions do) on a page of its own."""

    RECORDER = "recorder"
    SESSIONS = "sessions"


@dataclass(frozen=True)
class DefaultsPick:
    """What the install's Defaults step answered. HELD, never written by the
    step: the session default is saved at the Install keypress and Who records
    once the agents are installed (`main._apply_recorder_pick`), so backing
    out of the install leaves the device as it was."""

    recorder: str
    session_state: str


class ConsentView(StrEnum):
    """Which half of the daemon's consent a screen shows."""

    SUMMARY = "summary"
    DETAILS = "details"


#: The Probe daemon's consent, in the wizard. A daemon key minted from this
#: device's sign-in (`main._authorize_companion`) never opens the browser
#: approval, so these are the SAME words that page shows a daemon-only request:
#: `CONSENT_SUMMARY` and `GRANT_COPY[ApiGrant.Companion]` in
#: dashboard/src/shared/domain/permissions/scopes.ts. `agent/tests/test_consent_copy_sync.py` holds
#: the two copies equal; change them together.
DAEMON_CONSENT_LEAD = "It will be able to:"
DAEMON_CONSENT_SUMMARY: tuple[str, ...] = (
    "Run the Probe daemon, which records as you",
    "Upload this device's coding-session transcripts",
    "Send session parts to an AI model, through Probe",
    "Upload project files it judges part of your work",
    "Trash research; remove papers, views, links for good",
)
DAEMON_CONSENT_DETAILS: tuple[str, ...] = (
    "Run the Probe daemon, which uploads this device's coding sessions and records your work in Probe as you",
    "Reads this device's coding sessions and uploads their transcripts to your team's knowledgebase.",
    "Transcripts carry your prompts and the images you paste into them, the assistant's replies and your shell commands — not file contents, not tool output.",
    "Images you paste are uploaded unscanned: a screenshot that shows a credential is uploaded with it. Turn that off in the Probe wizard's Settings.",
    "Uploads project files it judges part of your work's record, such as results and configs.",
    "Each file it uploads is scanned for secrets first: its first 16 MB, or 64 MB of a file that is not text.",
    "Files named like credentials are not uploaded unless you approve them; with your coding agent's permission prompts off, that approval is automatic.",
    "Sends parts of the session — command output and the files it reads included — to the AI model it runs on, through Probe, to decide what to record.",
    "Can read and write, and move runs, groups, experiments and projects to the trash.",
    "Never deletes a run, group, experiment or project permanently: Probe can restore trashed ones for 21 days.",
    "Can permanently remove recorded papers, views, lineage edges, and links between projects or to repositories. It asks you first, unless your coding agent's permission prompts are off.",
    "Credential-shaped values are replaced before upload — a filter, not a guarantee. Keep live credentials out of captured sessions.",
    "This device only. Turn it off any time from Integrations.",
)


def daemon_consent_lines(view: ConsentView, width: int) -> list[str]:
    """The daemon's consent as display lines `width` wide: the five-line summary,
    or every line. A bullet's wrapped lines hang under its text, not its mark."""
    from probe.cli.wizard import terminal as tui

    mark, items = (
        ("✓", DAEMON_CONSENT_SUMMARY) if view is ConsentView.SUMMARY else ("•", DAEMON_CONSENT_DETAILS)
    )
    lines = [DAEMON_CONSENT_LEAD]
    for item in items:
        first, *rest = tui.wrap(item, max(10, width - 2))
        lines.extend([f"{mark} {first}", *(f"  {line}" for line in rest)])
    return lines


def run_defaults_step(pick: DefaultsPick, *, agent_screen_shown: bool) -> "tuple[object, DefaultsPick]":
    """Install step 2: the main menu's Defaults group on a page of its own.

    Returns `(answer, pick)`: the answer is True (Next), tui.BACK or None
    (Ctrl-C), and `pick` is what the rows read when the page closed, kept by
    the caller so Back and forward again shows the same picks.

    The rows switch with `←`/`→` like the menu's (Enter switches too), but
    NOTHING is written here: the menu's rows save on each press, this page only
    answers (`DefaultsPick`). While Who records reads `daemon`, its row carries
    the daemon's consent (`DAEMON_CONSENT_SUMMARY`), and `d` swaps in every
    line (Tab is the page's own key for reading the text above the rows): the
    disclosure sits where the choice is made. An environment variable
    holding the session default down keeps that row still, as on the menu.
    """
    import questionary

    from probe.cli.wizard import terminal as tui
    from probe.sdk import session_marker

    daemon = session_marker.RECORDER_DAEMON
    cycles: dict = {DefaultsRow.RECORDER: (session_marker.RECORDER_AGENT, daemon)}
    if session_marker.state_env_override() is None:
        cycles[DefaultsRow.SESSIONS] = cycling_settings()[Setting.TRACKING_DEFAULT]
    start = {
        DefaultsRow.RECORDER: pick.recorder,
        DefaultsRow.SESSIONS: setting_state(pick.session_state),
    }
    view = {"consent": ConsentView.SUMMARY}
    indent = tui.body_indent()
    room = max(20, tui.box_width() - (2 + tui.BOX_GUTTER) - 2)

    def row_text(row: DefaultsRow, value: str) -> str:
        if row is DefaultsRow.RECORDER:
            title, detail = recorder_row(value)
            body = (
                daemon_consent_lines(view["consent"], room)
                if value == daemon
                else [line for item in detail for line in tui.wrap(item, room)]
            )
        else:
            title, detail = tracking_default_row(value)
            body = [line for item in detail for line in tui.wrap(item, room)]
        return f"\n{indent}  ".join([title, *body])

    rows = {row: questionary.Choice(title=row_text(row, start[row]), value=row) for row in DefaultsRow}
    choices: list = []
    for row in rows.values():
        choices.extend([questionary.Separator(" "), row])
    choices.extend(nav_footer())
    message = tui.framed(
        "Defaults",
        tui.wrap("Who records, and what new sessions do on this device. The menu's Defaults changes either later."),
        "How should Probe run here?",
    )
    instruction = "← → switch · d daemon details · enter · esc back · nothing is saved until Install"
    question = tui.checkbox(
        message,
        choices=choices,
        instruction=instruction,
        style=tui.style(),
        qmark=tui.qmark(),
        pointer=tui.pointer(),
    )
    content = getattr(question, "_probe_content", None)
    if isinstance(content, dict):
        content["instruction"] = instruction  # the page's key line: these rows switch, they do not tick
    tui.draw_own_boxes(question)  # these rows switch; a ticked box would say otherwise

    def values(control) -> DefaultsPick:
        cycle = getattr(control, "probe_cycle", None) or {}
        return DefaultsPick(
            recorder=cycle.get(DefaultsRow.RECORDER, start[DefaultsRow.RECORDER]),
            session_state=cycle.get(DefaultsRow.SESSIONS, start[DefaultsRow.SESSIONS]),
        )

    def redraw(control) -> None:
        for row, choice in rows.items():
            choice.title = row_text(row, values(control).recorder if row is DefaultsRow.RECORDER
                                    else values(control).session_state)

    left: dict = {}
    control = _wire_picker(
        question,
        redraw=redraw,
        on_leave=lambda ctrl: True,
        on_back=lambda ctrl: left.update(pick=values(ctrl)),
        cycles=cycles,
        cycle_state=start,
    )
    if control is None:
        # questionary's internals moved and nothing here can switch: skip the
        # page with the device's values. The menu's Defaults still sets both.
        return True, pick
    tui.point_at(control, lambda value: value == NAV_BAND)
    dress_band(question, control)
    try:
        from prompt_toolkit.filters import Condition

        bindings = question.application.key_bindings
        pointed = lambda: getattr(control.get_pointed_at(), "value", None)  # noqa: E731

        def shift(delta: int):
            def _shift(event) -> None:  # pragma: no cover - requires a live terminal
                row = pointed()
                order = cycles[row]
                here = control.probe_cycle.get(row, order[0])
                control.probe_cycle[row] = order[(order.index(here) + delta) % len(order)]
                redraw(control)

            return _shift

        # Registered after `_wire_picker`'s `←`/`→` (Back/Next), so on a row
        # that switches these win; on the band those still go back and on.
        on_row = Condition(lambda: pointed() in cycles)
        bindings.add("left", eager=True, filter=on_row)(shift(-1))
        bindings.add("right", eager=True, filter=on_row)(shift(1))

        @bindings.add(
            "d",
            eager=True,
            filter=Condition(lambda: pointed() == DefaultsRow.RECORDER and values(control).recorder == daemon),
        )
        def _(event) -> None:  # pragma: no cover - requires a live terminal
            view["consent"] = (
                ConsentView.DETAILS if view["consent"] is ConsentView.SUMMARY else ConsentView.SUMMARY
            )
            redraw(control)

    except Exception:  # noqa: BLE001 - Enter still switches a row; the band still works
        pass
    answer = tui.ask(
        question,
        height=tui.content_height(message, choices, instruction=instruction),
        margin=0,
        progress=install_header(STEP_DEFAULTS, agent_screen_shown=agent_screen_shown),
    )
    if answer is True:
        return True, values(control)
    return answer, left.get("pick", pick)


def run_daemon_consent(agent_sources: "tuple[str, ...] | list[str] | str"):
    """The daemon's consent before its key is minted from this device's sign-in
    (the main menu's Who records → daemon). Returns True (turn it on), False
    (keep the agents recording), tui.BACK or None.

    That key used to come from a browser approval, and the approval page was
    where the daemon was disclosed; minting it from the sign-in skips the page,
    so the same words show here (`DAEMON_CONSENT_SUMMARY`, every line one
    choice away). Turning it on is the first choice: the person just switched
    the row to the daemon.
    """
    from probe.cli.wizard import terminal as tui

    view = ConsentView.SUMMARY
    while True:
        lines = [
            *tui.wrap(
                f"It records for {agent_label(agent_sources)} on this device. No browser needed: "
                "this device's sign-in gives it its own key."
            ),
            "",
            *daemon_consent_lines(view, tui.CONTENT_WIDTH),
            "",
            "Turn it off any time: Who records ‹ agent ›.",
        ]
        toggle = (
            ("Show every detail", ConsentView.DETAILS)
            if view is ConsentView.SUMMARY
            else ("Show the summary", ConsentView.SUMMARY)
        )
        picked = tui.review(
            "Turn on the Probe daemon?",
            lines,
            [("Turn on the daemon", True), toggle, ("Keep my agents recording", False)],
        )
        if picked in (ConsentView.SUMMARY, ConsentView.DETAILS):
            view = picked
            continue
        return picked


#: The Defaults picker's forward label: the way forward IS the save.
SET_DEFAULT_TITLE = "Set default  ›"


def run_defaults_menu(current: "bool | str"):
    """Choose this machine's default for new sessions, from the main menu's
    Defaults row. Returns None (quit), tui.BACK, or a STATE NAME.

    The settings screen's shape and keys, as a RADIO: one row per state, each
    carrying that state's disclosure, the current one ticked. Enter (or space)
    ticks the row under the cursor, and `→` -- or Enter on `Set default ›` --
    saves the ticked one. LEAVING saves it too: `←`/Escape after ticking
    another state keeps it, where it used to be dropped (2026-10-02). The
    cursor opens on the band like every step, so Enter straight away saves
    what is already saved: nothing.

    Every state is offered, `off` included -- DELIBERATELY unlike the bare
    `/probe` switch, which is pressed blind mid-thought and must never land on
    a state that stops reads. This is a screen you are reading, and nothing is
    written until the save.

    The daemon is not a state here: it is the "Who records" setting.
    """
    import questionary

    from probe.cli.wizard import terminal as tui
    from probe.sdk import session_marker

    tui.use_checkmarks()  # the fallback path, if we cannot take the box over
    current = setting_state(current)
    order = cycling_settings()[Setting.TRACKING_DEFAULT]
    lines = describe_settings({Setting.TRACKING_DEFAULT: current})
    message = tui.framed(
        "Defaults on this device:", lines, "What should new sessions do?"
    )

    indent = tui.body_indent()
    copy = {
        state: (
            session_marker.state_label(state) + ("  (current)" if state == current else ""),
            tuple(line for line in SETTINGS_STATE_COPY[Setting.TRACKING_DEFAULT][state] if line),
        )
        for state in order
    }
    rows: dict[str, object] = {}
    choices: list = []
    for state in order:
        title, detail = copy[state]
        rows[state] = questionary.Choice(
            title=_menu_row(title, detail, checked=state == current, indent=indent),
            value=state,
            checked=state == current,
        )
        choices.extend([questionary.Separator(" "), rows[state]])
    choices.extend(nav_footer(next_title=SET_DEFAULT_TITLE))

    instruction = "(enter picks this row · → saves it)"
    question = tui.checkbox(
        message,
        choices=choices,
        instruction=instruction,
        style=tui.style(),
        qmark=tui.qmark(),
        pointer=tui.pointer(),
    )
    ticked = lambda control: next(  # noqa: E731 - one expression, used twice
        (value for value in control.selected_options if value in rows), current
    )
    left_on: dict = {}
    control = _bind_menu_keys(
        question,
        rows,
        copy=copy,
        indent=indent,
        exclusive=True,
        on_leave=ticked,
        on_back=lambda control: left_on.update(state=ticked(control)),
    )
    if control is None:
        # Unwirable: no band (nothing would be listening for it) and no radio
        # (nothing would keep it one tick). A plain list, where Enter IS the
        # choice, says exactly what it does.
        body = tui.body_indent()
        choices = []
        for state in order:
            title, detail = copy[state]
            choices.append(questionary.Separator(" "))
            choices.append(
                questionary.Choice(
                    title="\n".join([title, *(f"{body}  {line}" for line in detail)]),
                    value=state,
                )
            )
        instruction = "(enter chooses · esc goes back)"
        question = tui.select(
            message,
            choices=choices,
            default=current,
            instruction=instruction,
            style=tui.style(),
            qmark=tui.qmark(),
            pointer=tui.pointer(),
        )
    else:
        dress_band(question, control)
    picked = tui.ask(
        question, height=tui.content_height(message, choices, instruction=instruction)
    )
    if picked is tui.BACK and left_on.get("state", current) != current:
        # Left with `←`/Escape after ticking another state: keep it.
        return left_on["state"]
    return picked
from probe.cli.wizard.agents import agent_label  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.apply.recorder import RECORDER_SOURCES, machine_recorder  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.screens.install_steps import STEP_DEFAULTS, install_header  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.screens.nav_band import NAV_BAND, dress_band, nav_footer  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.screens.picker_keys import _bind_menu_keys, _menu_row, _wire_picker  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.settings.menu import SETTINGS_COPY, SETTINGS_STATE_COPY  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.settings.settings import Setting, cycling_settings, describe_settings, setting_state  # noqa: E402 -- pieces need each other; the front door loads this one first
