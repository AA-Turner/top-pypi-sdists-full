"""the top-level menu: its grouped rows and the left/right switches on its Who records and Defaults rows."""

from __future__ import annotations
import sys
from probe.cli.wizard.state.state import Capabilities


def action_choices(caps_by_source: "dict | None" = None) -> list:
    """The top-level menu: headings lead groups, blank rows separate options.

    Each title stays next to its description. A single blank row separates
    options within a group; the existing blank before each heading keeps the
    heading attached to the group it names.
    """
    import questionary

    from probe.cli.wizard import terminal as tui
    from probe.cli.wizard.actions.onboarding import ACTION_COPY, DANGER_ACTIONS, Action, grouped_actions

    body = tui.body_indent()
    # The Defaults row wears the machine's CURRENT state, read fresh each time
    # the menu is drawn -- the menu comes back after every action, so a change
    # made through the row shows on the row.
    copy: dict = {
        **ACTION_COPY,
        Action.RECORDER: recorder_row(caps_by_source=caps_by_source),
        Action.DEFAULTS: tracking_default_row(),
    }
    # A blank before EVERY group, the first one included. It was skipped at the
    # top on the theory that a leading gap reads as "after the question" rather
    # than "between groups" -- which is exactly what it should read as. Without
    # it the first heading sits flush under the question and the menu starts
    # before the question has finished being a question.
    choices: list = []
    for group, actions in grouped_actions():
        choices.append(questionary.Separator(" "))
        if group:
            choices.append(questionary.Separator(tui.heading(group)))
            # Air between a heading and its rows (Richard 2026-09-29). A folded
            # group hides it with its rows (`tui.collapsed`), so only the open
            # group spends the line.
            choices.append(questionary.Separator(" "))
        for index, action in enumerate(actions):
            if index:
                choices.append(questionary.Separator(" "))
            title, detail = copy[action]
            lines = (detail,) if isinstance(detail, str) else detail
            choice = questionary.Choice(
                title="\n".join([title, *(f"{body}  {line}" for line in lines)]),
                value=action,
            )
            if action in DANGER_ACTIONS:
                choice.probe_style = tui.DANGER_STYLE  # drawn red by `tui.menu`
            choices.append(choice)
    return choices


def run_action_menu(caps: Capabilities | dict[str, Capabilities]):
    """The top-level menu. Returns None (quit), tui.BACK, an Action, or a
    `RecorderChoice` the moment the Who records row is switched. The Defaults
    row saves itself on each `←`/`→` press (`_DefaultSwitch`) and answers
    nothing."""

    from probe.cli.imports.jobs import ui as import_jobs_ui
    from probe.cli.wizard import terminal as tui

    choices = action_choices(caps if isinstance(caps, dict) else None)

    from probe.cli.wizard import doctor as doctor_impl  # noqa: F401

    # Read once per menu, not per frame: the menu is rebuilt after every action,
    # so an agent installed meanwhile shows on the next one.
    installed = detectable_sources()
    images = tui.image_protocol()
    agent_images = len(caps) if isinstance(caps, dict) else 1

    def live_lines():
        progress = import_jobs_ui.active_progress_lines()
        lines = describe_state(caps, installed=installed, images=images)
        if progress:
            lines += ["", tui.StyledLine("Import progress", style="class:question"), "", *progress]
        return lines

    switch = _DefaultSwitch(choices)
    recorder = _RecorderSwitch(choices)
    message = tui.framed("On this device:", live_lines(), "What do you want to do?")
    question = tui.menu(
        message,
        live_lines=live_lines,
        collapse=True,
        hint=lambda value: recorder.hint(value) or switch.hint(value),
        choices=choices,
        instruction="(arrow keys, enter to choose)",
        style=tui.style(),
        qmark=tui.qmark(),
        pointer=tui.pointer(),
    )
    switch.wire(question)
    recorder.wire(question)
    try:
        return tui.ask(question, height=tui.content_height(message, choices))
    finally:
        if images:
            sys.stdout.write(tui.forget_images(images, agent_images))
            sys.stdout.flush()


class _RecorderSwitch:
    """`←`/`→` on the main menu's Who records row: the agent or the Probe daemon,
    for every coding agent on this machine at once (Richard 2026-09-29: "no
    codex/claude split", and "no need to click enter to confirm").

    A press answers the menu straight away with `RecorderChoice(the other one)`;
    the caller moves the agents (plugins, the daemon's key through a browser
    approval, the instruction block) and draws the menu again. Enter on the row
    is the ordinary answer, `Action.RECORDER`: on the daemon it opens the
    daemon's page.
    """

    def __init__(self, choices: list) -> None:
        from probe.cli.wizard.actions.onboarding import Action

        self.row = next((c for c in choices if getattr(c, "value", None) is Action.RECORDER), None)
        self.saved = machine_recorder()
        self.control = None

    def on_row(self) -> bool:
        try:
            return self.control is not None and self.control.get_pointed_at() is self.row
        except Exception:  # noqa: BLE001 - a key filter is never worth a crash
            return False

    def hint(self, value) -> str | None:
        from probe.cli.wizard.actions.onboarding import Action
        from probe.sdk import session_marker

        if value is not Action.RECORDER or self.row is None:
            return None
        if self.saved == session_marker.RECORDER_DAEMON:
            return "← → switch · enter: what the daemon sees"
        return "← → switch"

    def other(self) -> str:
        from probe.sdk import session_marker

        return (session_marker.RECORDER_AGENT if self.saved == session_marker.RECORDER_DAEMON
                else session_marker.RECORDER_DAEMON)

    def wire(self, question) -> None:
        from probe.cli.wizard import terminal as tui

        if self.row is None:
            return
        self.control = tui.checkbox_control(question)
        if self.control is None:
            return
        try:
            from prompt_toolkit.filters import Condition

            on_row = Condition(self.on_row)
            bindings = question.application.key_bindings

            def switch(event) -> None:  # pragma: no cover - requires a live terminal
                self.control.is_answered = True
                event.app.exit(result=RecorderChoice(self.other()))

            bindings.add("right", eager=True, filter=on_row)(switch)
            bindings.add("left", eager=True, filter=on_row)(switch)
        except Exception:  # noqa: BLE001 - the menu without the switch still works
            pass


class _DefaultSwitch:
    """`←`/`→` on the main menu's Defaults row: switch the default for new
    sessions right there. Each press SAVES it -- a local config write, like the
    Who records row beside it, which applies on press too. It used to wait for
    Enter, and a researcher who switched it and moved on lost the change
    without a word (2026-10-02). Enter on the row is the ordinary menu answer,
    `Action.DEFAULTS`, which opens the picker.

    A write that fails puts the row back on what is saved and says why under it.

    The walk is the switch, `session_marker.SWITCH_STATES`: on / read / off.
    Whether the daemon records is the "Who records" setting, never a position
    here (Richard 2026-09-29).
    """

    def __init__(self, choices: list) -> None:
        from probe.cli.wizard.actions.onboarding import Action
        from probe.sdk import session_marker

        self.row = next((c for c in choices if getattr(c, "value", None) is Action.DEFAULTS), None)
        self.held = session_marker.state_env_override() is not None
        self.saved = setting_state(session_marker.default_session_state())
        self.shown = self.saved
        self.order = cycling_settings()[Setting.TRACKING_DEFAULT]
        self.question = None
        self.control = None
        #: The failure line of the last save, shown under the row until the next.
        self.error: str | None = None

    def on_row(self) -> bool:
        try:
            return self.control is not None and self.control.get_pointed_at() is self.row
        except Exception:  # noqa: BLE001 - a key filter is never worth a crash
            return False

    def hint(self, value) -> str | None:
        from probe.cli.wizard.actions.onboarding import Action

        if value is not Action.DEFAULTS or self.held or self.row is None:
            return None
        return "← → switch"

    def repaint(self) -> None:
        from probe.cli.wizard import terminal as tui

        title, detail = tracking_default_row(self.shown)
        if self.error:
            detail = (*detail, self.error)
        body = tui.body_indent()
        self.question._probe_retitle(
            self.row, "\n".join([title, *(f"{body}  {line}" for line in detail)])
        )

    def step(self, delta: int) -> None:
        from probe.cli.wizard.session import lock as wizard_lock

        wanted = self.order[(self.order.index(self.shown) + delta) % len(self.order)]
        # The menu holds no run lock while it waits on a person (plan C1), so
        # this write takes it, as every write of the wizard's does.
        try:
            with wizard_lock.held():
                lines = apply_settings({Setting.TRACKING_DEFAULT: wanted})
        except wizard_lock.Busy:
            lines = [f"! {wizard_lock.BUSY_MESSAGE}: not switched"]
        failed = next((line for line in lines if reports_failure(line)), None)
        if failed is None:
            self.saved = self.shown = wanted
            self.error = None
        else:
            self.shown = self.saved
            self.error = failed
        if self.question is not None:
            self.repaint()

    def wire(self, question) -> None:
        from probe.cli.wizard import terminal as tui

        if self.row is None or self.held or not hasattr(question, "_probe_retitle"):
            return
        self.question = question
        self.control = tui.checkbox_control(question)
        if self.control is None:
            return
        try:
            from prompt_toolkit.filters import Condition

            on_row = Condition(self.on_row)
            bindings = question.application.key_bindings

            @bindings.add("right", eager=True, filter=on_row)
            def _(event) -> None:  # pragma: no cover - requires a live terminal
                self.step(1)

            @bindings.add("left", eager=True, filter=on_row)
            def _(event) -> None:  # pragma: no cover - requires a live terminal
                self.step(-1)
        except Exception:  # noqa: BLE001 - the menu without the switch still works
            pass
from probe.cli.wizard.agents import detectable_sources  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.apply.recorder import machine_recorder  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.screens.device_summary import describe_state  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.screens.run_summary import reports_failure  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.settings.defaults import RecorderChoice, recorder_row, tracking_default_row  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.settings.settings import Setting, apply_settings, cycling_settings, setting_state  # noqa: E402 -- pieces need each other; the front door loads this one first
