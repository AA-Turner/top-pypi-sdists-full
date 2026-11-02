"""bring one agent's capture and tracking to what the selection wants, on the agent's instruction profile (agent or daemon)."""

from __future__ import annotations

from probe.cli.wizard.apply import (
    agent_rules,
    root_skills)
from probe.shared.harness.harnesses import pi as pi_config
from probe.shared.harness import plugins as plugin_cli
from probe.cli.wizard.state.state import (
    CODEX_TAP_PLUGIN_NAME,
    LEGACY_CODEX_TAP_PLUGIN_ID,
    TAP_PLUGIN_NAME,
    Capabilities)
from probe.cli.wizard.state.agent_identity import (
    agent_source,
    tracking_plugin_name)
from probe.cli.capture.capture import OffMode, clear_killswitch, turn_off


#: Per-source label for the thing `apply_capture` installs, used only in its
#: own failure message. NOT the same name in every case: claude_code and
#: codex both install through the marketplace under a "tap" plugin name
#: (`TAP_PLUGIN_NAME`/`CODEX_TAP_PLUGIN_NAME` -- currently the same string,
#: see capabilities.py), while pi installs ONE package
#: (`pi_config.PACKAGE_NAME`) that bundles capture with the tracking skills
#: and MCP bridge -- there is no separate "tap" plugin for pi to name. A
#: table, never a ternary: see `apply_capture`'s own comment on the shape
#: this replaces.
CAPTURE_PLUGIN_LABEL: dict[str, str] = {
    "claude_code": TAP_PLUGIN_NAME,
    "codex": CODEX_TAP_PLUGIN_NAME,
    "pi": pi_config.PACKAGE_NAME,
    "kimi_code": TAP_PLUGIN_NAME,
}


def apply_capture(caps: Capabilities, want: bool, *, mode: OffMode, on_retry=None) -> list[str]:
    """Bring capture to `want` and report honestly.

    Turning it OFF goes through the verified postcondition in capture.py rather
    than deleting a file and hoping.
    """
    messages: list[str] = []
    if want:
        # Two INDEPENDENT jobs, and conflating them is a bug in both directions.
        # Clearing the killswitch is what actually turns capture back on for a
        # machine that already has the plugin; installing is only needed when
        # the plugin is absent. Gating the whole step on "plugin absent" (which
        # this function's caller briefly did) left `.disabled` in place while
        # the wizard reported success -- capture silently off after we said on.
        # Gating it on "capture off" instead reinstalls a plugin that is already
        # there. So: always clear, install only when missing.
        clear_killswitch()
        if caps.agent_source == "codex" and caps.legacy_capture_plugin_installed:
            retired = plugin_cli.uninstall("codex", LEGACY_CODEX_TAP_PLUGIN_ID)
            if not retired.ok:
                messages.append(
                    "could not remove the legacy Codex capture plugin "
                    f"{LEGACY_CODEX_TAP_PLUGIN_ID}: {retired.detail}"
                )
                return messages
            messages.append(
                f"Removed legacy {LEGACY_CODEX_TAP_PLUGIN_ID}; the unified tap owns capture now."
            )
        if caps.capture_plugin_installed:
            return messages
        # Table, not a ternary: `CODEX_TAP_PLUGIN_NAME if agent_source ==
        # "codex" else TAP_PLUGIN_NAME` was the exact banned two-way shape --
        # correct only while there were exactly two sources, silently wrong
        # (claude_code's name) for pi the moment it became a third. pi is
        # installable now (see INSTALLABLE_AGENT_SOURCES), so this label is
        # no longer cosmetic: it is the name `install_plugin` reports on
        # failure, and pi has its own package, not claude_code's tap name.
        tap_name = CAPTURE_PLUGIN_LABEL[caps.agent_source]
        result = install_plugin(tap_name, source=caps.agent_source, on_retry=on_retry)
        if not result.ok:
            messages.append(f"could not install {tap_name}: {result.detail}")
        return messages
    if not caps.capture_on and not caps.capture_token_sources:
        return messages
    result = turn_off(mode)
    messages.append(result.summary())
    messages.extend(f"! {warning}" for warning in result.warnings)
    return messages


def apply_tracking(want: bool, *, on_retry=None, keep_capture: bool | None = None) -> list[str]:
    """Bring tracking to `want`.

    Turning it off removes the plugin but deliberately does NOT revoke the PAT
    or log the CLI out: the wizard is not a logout command, and silently
    destroying a credential the user may be scripting against would be a nasty
    surprise. `probe logout` remains the explicit way to do that.

    pi carries both halves in one package: off keeps the package while capture
    stays (`keep_capture`, the run's selection; unknown reads the device), and
    the extension switches tracking off itself (0.4.0+, updated first).
    """
    messages: list[str] = []
    # The profile's plugin (`probe-research-daemon` where the daemon records),
    # so a re-run of the install never puts the other profile's plugin back.
    name = tracking_plugin_name()
    selected = agent_source()
    pi = _current_harness().lean_profile == LEAN_SETTINGS_FILTER  # one package, both halves
    capture_stays = (_settings_capture_on(selected) if keep_capture is None else keep_capture) if pi else False
    if pi and not want and capture_stays:
        ready = _settings_tracking_ready()
        if not ready.ok:
            return [f"! pi keeps Probe's tracking on: {ready.detail}"]
    if want:
        result = install_plugin(name, on_retry=on_retry)
        if result.ok and pi:
            # An existing entry may carry tracking-off: switch it back on.
            result = pi_config.set_tracking(True, daemon=daemon_records(selected))
        if not result.ok:
            messages.append(f"could not install {name}: {result.detail}")
        else:
            messages.extend(_apply_root_skills(selected, name))
        return [*messages, *(_pi_project_override(want=True) if pi else [])]
    result = uninstall_plugin(name, keep_capture=capture_stays) if pi else uninstall_plugin(name)
    if result.ok:
        # The plugin is the skills' source; with it gone they must go too, or the
        # agent keeps naming a skill whose plugin no longer exists.
        messages.extend(remove_root_skills(selected))
    if not result.ok:
        messages.append(f"could not uninstall {name}: {result.detail}")
    elif pi and capture_stays:
        messages.append("Probe's tracking is off in pi; session capture keeps running. You are still signed in.")
    else:
        messages.append(
            "Removed the tracking plugin. You are still signed in."
        )
    return [*messages, *(_pi_project_override(want=False) if pi else [])]


def agent_profile(source: str | None = None) -> "agent_rules.Profile":
    """The instruction-block profile of this coding agent: DAEMON where its
    "Who records" is the daemon (`session_marker.recorder`), else AGENT."""
    from probe.sdk import session_marker

    try:
        daemon = session_marker.recorder(source or agent_source()) == session_marker.RECORDER_DAEMON
    except Exception:  # noqa: BLE001 - an unreadable config is today's profile
        daemon = False
    return agent_rules.Profile.DAEMON if daemon else agent_rules.Profile.AGENT


def daemon_records(source: str | None = None) -> bool:
    """Is this coding agent on the daemon profile (the daemon records and reads)?"""
    return agent_profile(source) is agent_rules.Profile.DAEMON


def remove_root_skills(source: str) -> list[str]:
    """Prune Probe's skills when no plugin is left to do it.

    A researcher who removes the plugin with `/plugin uninstall` leaves no hook
    behind, so the copies in their own skills folder would never be refreshed or
    removed again. Marker-bearing folders only, as everywhere else.
    """
    try:
        return root_skills.remove(source)
    except OSError as exc:
        return [f"! could not remove Probe's skills: {exc}"]


def _apply_root_skills(source: str, plugin: str) -> list[str]:
    """Put the installed plugin's skills in the agent's own skills folder.

    Claude Code only (the capability gates it); every other harness reads the
    plugin's `agent-skills/` by manifest key and gets an empty list here. The
    plugin stays the source: `root_skills_sync.py` on SessionStart keeps the
    copies current, and this is the same work done at the moment of install so
    the researcher does not have to start a second session to get their skills.
    """
    try:
        return root_skills.apply(source, root_skills.installed_plugin_root(plugin), prefer=plugin)
    except OSError as exc:
        # Fail-open, the contract every other step in this wizard follows and
        # the one the hook already had: an unwritable skills folder reported a
        # PermissionError out of `apply_recorder` AFTER the new plugin was
        # installed and BEFORE `write_recorder`, leaving both plugins present
        # and the setting unwritten, with no message saying so.
        return [f"! could not install Probe's skills: {exc}"]


def _current_harness():
    """The registry row of the agent this wizard run configures."""
    from probe.foundation.harness_registry import get_registry

    return get_registry().get(agent_source())
from probe.cli.wizard.apply.plugins import install_plugin, uninstall_plugin  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.apply.recorder import LEAN_SETTINGS_FILTER  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.harness.harnesses.pi.package_install import _pi_project_override, _settings_capture_on  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.harness.harnesses.pi.readiness import _settings_tracking_ready  # noqa: E402 -- pieces need each other; the front door loads this one first
