"""take ONE coding agent back to nothing and verify the capture half is gone."""

from __future__ import annotations
from probe.shared.harness.harnesses.codex import config as codex_config
from probe.shared.harness import reasoning_summaries
from probe.cli.wizard.state.state import (
    CODEX_MCP_NAME,
    DAEMON_PLUGIN_NAME,
    Capabilities)
from probe.cli.wizard.state.agent_identity import tracking_plugin_name
from probe.cli.capture.capture import OffMode, clear_killswitch, turn_off


def _forget_recorder(source: str) -> list[str]:
    from probe.sdk import session_marker
    from probe.sdk.settings.settings import ConfigUnreadable

    try:
        session_marker.write_recorder(source, session_marker.RECORDER_AGENT)
    except (OSError, ValueError, ConfigUnreadable) as exc:
        return [f"! could not reset who records in {agent_label(source)}: {exc}"]
    return []


def remove_everything(caps: Capabilities) -> list[str]:
    """Take ONE coding agent back to nothing, and VERIFY the capture half.

    Replaces the page's "Remove the plugin" section, which only told you to
    uninstall -- and warned that uninstalling does not revoke credentials.
    Doing it here means we can actually clear them and prove capture stopped,
    rather than leaving the user to notice.

    Per agent, so a device with both Claude Code and Codex runs this twice. The
    ACCOUNT is not part of it -- there is one config file, not one per agent --
    and `finish_removal` releases that once, after the last pass through here.

    NOTHING DEVICE-WIDE either (`probe wizard --action uninstall --agent A`,
    the only caller): the import jobs (one job imports several agents' sessions,
    and a folder import is no agent's; there is no per-agent clear) and the
    automatic-updates choice (one device-wide file, `autoupdate`) stay. The
    whole-device `probe uninstall` removes both with the rest of Probe's state.
    """
    messages: list[str] = []
    result = turn_off(OffMode.UNINSTALL)
    messages.append(result.summary())
    messages.extend(f"! {warning}" for warning in result.warnings)

    # `uninstall_plugin` returns a Result, not a 2-tuple. Unpacking it raised
    # TypeError on the FIRST line of removal that touches a plugin, so
    # `probe wizard --action uninstall` crashed for everyone -- after the
    # plugins were gone, before the instruction block, the auto-update flag and
    # (below) the Codex MCP entry were dealt with. A half-removed machine that
    # ends in a traceback, and no test caught it because none called this.
    tracking_name = tracking_plugin_name(caps.agent_source)
    removal = uninstall_plugin(tracking_name)
    if not removal.ok and "not found" not in removal.detail.lower():
        messages.append(f"! could not remove {tracking_name}: {removal.detail}")
    elif tracking_name == DAEMON_PLUGIN_NAME:
        # Removed means back to nothing: a later install starts on today's profile.
        messages.extend(_forget_recorder(caps.agent_source))
    if caps.agent_source in reasoning_summaries.SOURCES:
        messages.extend(reasoning_summaries.undo_for_agent(caps.agent_source))

    from probe.foundation.harness_registry import get_registry

    if get_registry().get(caps.agent_source).statusline:
        messages.extend(remove_statusline())

    # The MCP entry we may have written into the user's own config.toml is not
    # ours to leave behind: after this call its token is orphaned, so Codex
    # would keep a server that lists as configured and answers 401.
    if caps.agent_source == "codex":
        try:
            removed = codex_config.remove_mcp_server(CODEX_MCP_NAME)
        except codex_config.ConfigError as exc:
            messages.append(
                f"! left the Codex MCP entry in place: {exc}. "
                f"Delete [mcp_servers.{CODEX_MCP_NAME}] by hand."
            )
        else:
            if removed.changed:
                messages.append(f"Removed the {CODEX_MCP_NAME} MCP entry from {removed.path}.")

    # The block lives OUTSIDE the repo, in the researcher's global CLAUDE.md,
    # and removal used to skip it entirely -- so "Removed." left every agent in
    # every repository still being told to use skills this very call had just
    # uninstalled. It also keeps `Capabilities.configured` True forever, so a
    # fully removed device can never look fresh again.
    messages.extend(apply_agent_rules(False))

    # `.disabled` is written by the teardown above to stop a session that starts
    # mid-uninstall from respawning the uploader. Once the plugin is gone and
    # `verified` says no credential resolves ANYWHERE (an exported ingest token
    # included), it guards nothing and only makes the device look half-off
    # forever. Both halves of that condition matter: a marker cleared while a
    # surviving plugin can still read an environment credential would turn
    # capture back on, which is the one thing this file may never do quietly.
    if result.plugin_removed and result.verified:
        clear_killswitch()

    # NOT the account: that is `finish_removal`, once for the device, after the
    # last coding agent has run through here. Releasing it from inside this
    # function would revoke the credential that the NEXT agent's pass -- and
    # this one's own capability registration -- still has to authenticate with.
    messages.append("Removed.")
    return messages
from probe.cli.wizard.agents import agent_label  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.apply.agent_files import apply_agent_rules, remove_statusline  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.apply.plugins import uninstall_plugin  # noqa: E402 -- pieces need each other; the front door loads this one first
