"""the Defaults action: this machine's default for new sessions and its Who records pick, at install and from the menu."""

from __future__ import annotations
from ....sdk import session_marker


def _save_session_default(state: str) -> list[str]:
    """The install's Defaults pick for new sessions, saved at the Install
    keypress. [] when the device already has it, or when an environment
    variable holds it (a write that changes nothing anyone can see)."""
    from probe.cli import wizard as wizard

    if session_marker.state_env_override() is not None:
        return []
    picked = wizard.setting_state(state)
    if picked == wizard.setting_state(session_marker.default_session_state()):
        return []
    return wizard.apply_settings({wizard.Setting.TRACKING_DEFAULT: picked})


def _apply_recorder_pick(
    recorder: str,
    *,
    sources: tuple[str, ...],
    completion,
    base_now: str,
    collect,
    telemetry=None,
) -> list[str]:
    """The install's Defaults pick for Who records, once the agents are in.

    Through the menu's own switch (`_run_recorder_action`: availability, the
    daemon's key and libraries, the plugin move, telemetry), without its
    consent page (the Defaults step carried it) or the daemon's page after.
    Compared agent by agent, never by `machine_recorder()`, which reads
    `daemon` when ANY agent is on it (Codex O3). Only after an install that
    settled: a half install keeps its agents recording themselves.
    """
    from probe.cli import wizard as wizard

    movable = [source for source in sources if source in wizard.RECORDER_SOURCES]
    if not any(session_marker.recorder(source) != recorder for source in movable):
        return []
    if completion is None or completion.remaining or not completion.settled:
        return [f"{wizard.RECORDER_ROW_TITLE} stays as it was: the install did not finish. "
                "Switch it from the menu's Defaults."]
    caps_by_source = {source: collect(source) for source in sources}
    return _run_recorder_action(
        yes=False,
        caps_by_source=caps_by_source,
        base_now=base_now,
        chosen=recorder,
        telemetry=telemetry,
        disclosed=True,
        show_daemon_page=False,
    ) or []


def _run_defaults_action(
    *, yes: bool, base_now: str | None = None, chosen: str | None = None
) -> list[str] | None:
    """The main menu's Defaults row: this machine's default for new sessions.

    `chosen` is a state already picked elsewhere (`wizard.DefaultChoice`; the
    menu row itself saves on each press now); without one, the picker opens
    (`run_defaults_menu`), where `→` saves and so does leaving after a change. The states are on / read / off; whether the daemon records is the
    "Who records" setting, which mints and revokes the daemon's key
    (`setup.apply_recorder`).
    """
    from probe.cli import wizard as wizard
    from probe.cli.wizard import terminal as tui

    report = ["Probe in new sessions:", *wizard.describe_settings()]
    if yes or not wizard.interactive():
        # A screen nobody can answer must not answer for them.
        return [*report, "", "`probe session default on|read|off` sets it."]
    # The THREE-valued override, not the boolean one: `PROBE_SESSION_STATE`
    # holds this default down just as hard, and a picker drawn under it would
    # write a value that changes nothing anyone can see (the 0.96.0 rule: a
    # control that cannot do what it says does not get drawn).
    if session_marker.state_env_override() is not None:
        return [*report, "", "Unset that variable to choose the default here."]

    current = wizard.setting_state(session_marker.default_session_state())
    if chosen is not None:
        picked = wizard.setting_state(chosen)
    else:
        tui.clear()
        picked = wizard.run_defaults_menu(current)
    if picked is None or picked is tui.BACK or picked == current:
        return None  # backed out, or chose what it already was: nothing happened
    lines = wizard.apply_settings({wizard.Setting.TRACKING_DEFAULT: picked})
    if chosen is not None and len(lines) == 1 and not wizard.reports_failure(lines[0]):
        # Saved from the menu row with nothing else to say: the menu comes
        # straight back, and the row itself is the confirmation -- it now
        # wears the saved state. A page to press through would be a second
        # confirmation of the one keystroke that already was one.
        return None
    return lines
from probe.cli.commands.machine.wizard import wizard  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.actions.recorder import _run_recorder_action  # noqa: E402 -- pieces need each other; the front door loads this one first
