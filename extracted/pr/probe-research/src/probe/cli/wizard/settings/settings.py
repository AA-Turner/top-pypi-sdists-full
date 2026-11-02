"""the settings the wizard manages: the Setting vocabulary, read every value once, apply only what changed, describe them."""

from __future__ import annotations
import os
from probe.foundation.compat.compat import StrEnum
from probe.shared.harness import reasoning_summaries
from probe.cli.wizard.state.state import Capability


# -- settings ---------------------------------------------------------------
#
# What is left of a screen that used to hold every capability:
#
# * "Updates" — automatic updates, the one capability that is not a PART of
#   Probe. Tracking, capture and the instruction rules had rows here too, and
#   they are gone on purpose: Probe is installed whole and removed whole
#   (Uninstall), and a row per part is how devices ended up with half of it.
#   Per-agent control stays on the flag path (`--agent codex --no-capture`).
# * "Who records" — per agent, offered to every team the daemon is open to.
#
# `TRACKING_DEFAULT` — the default for new sessions, a preference, NOT the
# tracking plugin — is still a `Setting`, but it is drawn on the MAIN MENU
# (`tracking_default_row`, `run_defaults_menu`) rather than on this screen: it
# is the one setting worth seeing every time the wizard opens.


class Setting(StrEnum):
    """One option the settings screen manages. The vocabulary only --
    `SETTINGS_GROUPS` is the screen order, `SETTINGS_COPY` the words, and
    the caller's snapshot (`read_settings` plus the capability state it is
    handed) the state. Adding a setting means one entry in each; the screen
    itself never changes."""

    AUTO_UPDATE = "auto_update"
    TRACKING_DEFAULT = "tracking_default"
    RECORDER_CLAUDE_CODE = "recorder_claude_code"
    RECORDER_CODEX = "recorder_codex"
    RECORDER_PI = "recorder_pi"
    RECORDER_KIMI_CODE = "recorder_kimi_code"
    REASONING_SUMMARIES = "reasoning_summaries"
    PASTED_IMAGES = "pasted_images"


#: The "Who records" rows (daemon reads), one per coding agent with a daemon
#: profile, and the agent each drives. Like the capability rows they apply
#: through their own machinery (`apply_recorder`: plugins, the daemon's key,
#: the instruction block), never `apply_settings`. Shown wherever the server
#: does not say the daemon is closed to this team, and always where the daemon
#: already records.
RECORDER_SETTINGS: dict["Setting", str] = {
    Setting.RECORDER_CLAUDE_CODE: "claude_code",
    Setting.RECORDER_CODEX: "codex",
    Setting.RECORDER_PI: "pi",
    Setting.RECORDER_KIMI_CODE: "kimi_code",
}


#: The capability rows — the ones whose apply path is the CONFIGURE machinery
#: (verification, the progress screen), never a bare config write.
#: `apply_settings` refuses them by design; see `_run_settings_action`.
CAPABILITY_SETTINGS: frozenset[Setting] = frozenset({Setting.AUTO_UPDATE})

#: Which `Capability` each capability row drives. One table, so the screen,
#: the union read, and the target Selection cannot disagree about the mapping.
SETTING_CAPABILITY: dict[Setting, Capability] = {
    Setting.AUTO_UPDATE: Capability.AUTO_UPDATE,
}


def capability_state_for(snapshot) -> dict[Capability, bool]:
    """ONE agent's capability state, read with the SCREEN's own predicates.

    Every capability, not only the ones with a row: the Automatic updates box
    is drawn from this read, and `_apply_capability_settings` builds each
    agent's target from it with only the toggled row overridden. The rows it
    does not change ride along marked `Selection.preserve`, because a read
    cannot say "leave it" (a pending capture lock reads as off); this read
    still decides the booleans the screen and the apply compare. The first ship of the settings screen preserved from
    `Capabilities.enabled()` instead, whose TRACKING member also requires a
    login, so on a signed-out machine an unrelated commit uninstalled the
    tracking plugin.

    TRACKING deliberately reads the PLUGIN fact, not `tracking_on`: "is it
    installed here" is what a commit would change, and `probe doctor` owns
    diagnosing a plugin that is installed but signed out.
    """
    return {
        Capability.TRACKING: bool(snapshot.tracking_plugin_installed),
        Capability.CAPTURE: bool(snapshot.capture_on),
        Capability.AGENT_RULES: bool(snapshot.agent_rules_installed),
        Capability.AUTO_UPDATE: bool(snapshot.auto_update_enabled),
    }


def capability_settings_state(caps_by_source: dict) -> dict[Setting, bool]:
    """The capability rows' boxes, read as the UNION across this device's agents.

    Union, not intersection: the box answers "does this device do X at all",
    which is the same reading `describe_state` gives the menu header. There is
    no per-agent split to note: the one remaining row, automatic updates, is a
    single device-wide file (`autoupdate`), so the agents cannot disagree.
    """
    states = [capability_state_for(snapshot) for snapshot in caps_by_source.values()]
    return {
        setting: any(state[capability] for state in states)
        for setting, capability in SETTING_CAPABILITY.items()
    }


def cycling_settings() -> dict[Setting, tuple[str, ...]]:
    """The rows that CYCLE rather than tick, and the order one press walks.

    The order is `session_marker.STATES` itself, never a copy of it: the wizard's
    space bar and the researcher's bare `/probe` are the same switch seen from
    two places, and a screen that walked its own order would make one of them
    wrong the first time a state moved.
    """
    from probe.sdk import session_marker

    return {
        Setting.TRACKING_DEFAULT: session_marker.SWITCH_STATES,
        **{setting: session_marker.RECORDERS for setting in RECORDER_SETTINGS},
    }


def setting_state(value: "bool | str") -> str:
    """One cycling row's value as a STATE NAME.

    A bool is the two-valued answer this row used to give, read as what that
    boolean has always meant -- ticked is `full`, empty is `read-only`, never the
    hard `off` (`session_marker.write_default_tracking` maps it the same way).
    Callers still handing a bool get the old meaning rather than a TypeError
    drawing the box.

    A stored `daemon` (from when the switch had that position) reads as `on`:
    a session started from it is `on_state`, the daemon only where "Who
    records" says so.
    """
    from probe.sdk import session_marker

    if isinstance(value, str):
        state = session_marker.normalize_state(value) or session_marker.DEFAULT_STATE
        return session_marker.STATE_FULL if state == session_marker.STATE_DAEMON else state
    return session_marker.STATE_FULL if value else session_marker.STATE_READ_ONLY


def cycle_value(setting: Setting, value: "bool | str") -> str:
    """One cycling row's value in ITS vocabulary: a session state for the
    tracking default (`setting_state`), `agent`/`daemon` for a "Who records"
    row -- where a bool is the box (ticked = the first position, `agent`) and
    anything unrecognised reads as `agent`, today's profile."""
    from probe.sdk import session_marker

    if setting in RECORDER_SETTINGS:
        if isinstance(value, str):
            return value if value in session_marker.RECORDERS else session_marker.RECORDER_AGENT
        return session_marker.RECORDER_AGENT if value else session_marker.RECORDER_DAEMON
    return setting_state(value)


def value_label(setting: Setting, value: str) -> str:
    """The word a cycling row wears for `value`."""
    from probe.sdk import session_marker

    if setting in RECORDER_SETTINGS:
        return RECORDER_WORDS.get(value, value)
    return session_marker.state_label(value)


def read_settings(caps_by_source: dict | None = None) -> dict[Setting, bool]:
    """Every setting's current value, read once.

    ONE read feeds both the boxes the screen draws and the diff
    `_run_settings_action` computes against what comes back -- reading again
    at apply time would reopen the gap 0.96.0 closed, where a config change
    landing while the prompt sat open made the screen and the write disagree.

    `caps_by_source` supplies the capability rows' state (see
    `capability_settings_state`); without it only the config-file settings are
    returned -- enough for `describe_settings`, not for the screen, whose
    registry check demands every row have a value.
    """
    from probe.sdk import session_marker

    values: dict[Setting, "bool | str"] = {
        # The THREE-valued read, because the row is three-valued: reading the
        # boolean here would draw `off` as `read` and commit it back as `read`
        # the moment anything else on the screen changed.
        # A stored `daemon` from before reads as `on` (`setting_state`).
        Setting.TRACKING_DEFAULT: setting_state(session_marker.default_session_state()),
        # Who records, per agent: read from the same config, whether or not
        # the row is drawn, so the registry check always has a value.
        **{setting: session_marker.recorder(source) for setting, source in RECORDER_SETTINGS.items()},
        Setting.REASONING_SUMMARIES: reasoning_summaries.row_on(reasoning_sources(caps_by_source)),
        Setting.PASTED_IMAGES: session_marker.pasted_images_on(),
    }
    if caps_by_source is not None:
        values.update(capability_settings_state(caps_by_source))
    return values


def reasoning_sources(caps_by_source: dict | None = None) -> tuple[str, ...]:
    """The agents the reasoning row covers: those set up on this device (every
    one when unknown). ONE answer for the read and the write, or the box would
    draw one set of agents and commit another."""
    return tuple(
        source for source in reasoning_summaries.SOURCES
        if caps_by_source is None or source in caps_by_source
    )


def apply_settings(
    changes: dict[Setting, bool], *, caps_by_source: dict | None = None,
) -> list[str]:
    """Write ONLY the settings whose box changed, and say what each became.

    Callers pass the diff, not the whole picker state: rewriting an unchanged
    setting is a pointless config write, and on the tracking default it would
    also stamp a `defaults` block into a config that never had one.

    Failures are PER SETTING, reported in place rather than raised: with two
    settings in one commit, a raise after the first write would leave it
    silently applied while the screen reported only the failure. And a
    `Setting` this function has no writer for is a BUG, not a no-op --
    accepting it as a change and writing nothing is exactly the silent
    registry drift `grouped_settings` exists to catch.

    CAPABILITY settings are refused here BY DESIGN, not by drift: turning a
    capability on needs authorization, grant gating, retries and verification
    -- the CONFIGURE machinery -- and a bare `apply_*` call would report "on"
    while the capability stayed off. `_run_settings_action` owns that route.
    """
    from probe.sdk import session_marker
    from probe.sdk.settings.settings import ConfigUnreadable

    lines: list[str] = []
    for setting, value in changes.items():
        if setting in CAPABILITY_SETTINGS:
            raise AssertionError(
                f"{setting!r} is a capability: it applies through the CONFIGURE "
                "machinery in _run_settings_action, never a bare config write"
            )
        if setting in RECORDER_SETTINGS:
            raise AssertionError(
                f"{setting!r} moves plugins and mints a key: it applies through "
                "apply_recorder in _run_settings_action, never a bare config write"
            )
        if setting is Setting.TRACKING_DEFAULT:
            state = setting_state(value)
            try:
                session_marker.write_default_state(state)
            except (OSError, ValueError, ConfigUnreadable) as exc:
                lines.append(f"! could not set the Probe default for new sessions: {exc}")
                continue
            lines.append(f"Probe in new sessions → {session_marker.state_label(state)}")
        elif setting is Setting.REASONING_SUMMARIES:
            lines.extend(reasoning_summaries.set_explicit(bool(value), reasoning_sources(caps_by_source)))
        elif setting is Setting.PASTED_IMAGES:
            try:
                session_marker.write_pasted_images(bool(value))
            except (OSError, ValueError, ConfigUnreadable) as exc:
                lines.append(f"! could not set image upload: {exc}")
                continue
            lines.append(f"Upload images you paste → {'on' if value else 'off'}")
        else:
            raise AssertionError(f"apply_settings has no writer for {setting!r}")
    return lines


def describe_settings(current: "dict[Setting, bool | str] | None" = None) -> list[str]:
    """The state block above the settings menu.

    `current` is the SAME snapshot the boxes are drawn from, when the caller
    has one -- the block and the picker must not read the config twice, or a
    write landing between the reads shows a state line disagreeing with the
    box beside it. Headless callers pass nothing and get a fresh read.

    Says what the default currently IS before offering to change it, and
    discloses the env override honestly: a RECOGNIZED value beats the config
    file, so moving the setting under it changes nothing visible -- but an
    unrecognized value (a typo like `of`) is IGNORED by `default_session_state`,
    and calling that an override would misdiagnose the typo as the row not
    working. BOTH variables are named, because either one can be the thing
    holding the row down and a block that disclosed only the older one would
    send someone hunting for a setting that is not the one winning. The value is
    printed through a printable-only filter and bounded, because the environment
    is not this program's to trust with raw escape sequences.
    """
    from probe.sdk import session_marker

    state = setting_state(
        current[Setting.TRACKING_DEFAULT]
        if current is not None
        else session_marker.default_session_state()
    )
    lines = [f"  {'Probe in new sessions':<28} {session_marker.state_label(state)}"]
    for name in ("PROBE_SESSION_STATE", "PROBE_SESSION_TRACKING"):
        raw = os.environ.get(name) or ""
        if not raw.strip():
            continue
        recognized = session_marker.normalize_state(raw) is not None
        note = "env wins over this setting" if recognized else "unrecognized, ignored"
        shown = "".join(ch for ch in raw if ch.isprintable())[:32] or "<unprintable>"
        lines.append(f"  {name:<28} {shown}  ({note})")
    return lines
from probe.cli.wizard.apply.recorder import RECORDER_WORDS  # noqa: E402 -- pieces need each other; the front door loads this one first
