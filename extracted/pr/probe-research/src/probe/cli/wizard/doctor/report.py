"""the report: the full render, what it says is wrong, and the wizard's Diagnose summary."""

from __future__ import annotations

from probe.cli.wizard.apply import agent_rules
from probe.shared.harness import plugins as plugin_cli
from probe.cli.wizard.state.state import (
    TAP_PLUGIN_NAME,
    Capabilities,
    TokenSource)
from probe.cli.wizard.state.capture_credentials import tap_token_env
from probe.cli.wizard.state.agent_identity import tracking_plugin_name

# TokenSource.ENVIRONMENT has no entry here on purpose: which env var it
# names varies by source (tap_token_env()), so it is computed at each call
# site instead of being a third static string that can only ever be right
# for one agent.
_SOURCE_LABEL = {
    TokenSource.PAIRED_FILE: "paired device token",
    TokenSource.PROBE_CONFIG: "probe CLI config (ingest_token)",
}


def render(caps: Capabilities, codex_hooks: list[str] | None = None, service: dict | None = None) -> str:
    """The full report. Pure, so it can be asserted in tests without a machine.

    `codex_hooks` is `codex_hook_rows(caps)`, gathered by the caller because it
    asks Codex; omitted, the section is left out. `service` is
    `service_calls.view()`, likewise (it asks the Probe service).
    """
    lines: list[str] = ["Probe Research doctor", ""]

    lines.append("Versions")
    lines.extend(_version_rows(caps))
    lines.append("")

    lines.append("Install")
    lines.append(_row("CLI version", caps.cli_version or "unknown"))
    lines.append(_row("Install method", caps.install_method or "unknown"))
    if caps.agent_source == "pi":
        # Capabilities has no `pi_available` field (only claude_available /
        # codex_available -- both source-independent booleans this dataclass
        # has carried since before pi existed), and inventing one is a real
        # field-shape change this pass did not want to make silently. The old
        # ternary's `else` defaulted straight to `caps.claude_available` here
        # too, so a pi report showed "Claude Code CLI: ok" -- true about the
        # wrong agent. Honest and unresolved beats confidently wrong: say
        # what this does not check instead.
        # "pi CLI", not "pi extension": this row occupies the slot that holds
        # "Claude Code CLI" / "Codex CLI" below, so it was always about the
        # BINARY. The label only became wrong once the rows underneath started
        # reporting the extension for real -- two adjacent "pi extension" rows,
        # the first saying doctor does not track it and the second tracking it.
        lines.append(_row("pi CLI", "see `pi --version`; not tracked by doctor"))
        # What doctor CAN see about pi: whether our own extension entry point
        # is filtered out of the package, and whether a daemon is live for this
        # session. Both are silent failures everywhere else.
        lines.extend(_pi_capture_rows())
    elif caps.agent_source == plugin_cli.KIMI:
        lines.extend(_kimi_rows())
    else:
        agent_label = "Codex CLI" if caps.agent_source == "codex" else "Claude Code CLI"
        agent_available = (
            caps.codex_available if caps.agent_source == "codex" else caps.claude_available
        )
        # The VERSION beside the tick. "installed" was all this said while an
        # entire customer's imports failed on a flag their build predated, and the
        # first place anyone would look for that is `probe doctor`.
        agent_state = _OK if agent_available else _MISSING
        if agent_available and caps.agent_version:
            agent_state = f"{agent_state} ({caps.agent_version})"
        lines.append(_row(agent_label, agent_state))
    lines.append("")

    lines.append("Account")
    lines.append(_row("Logged in as", caps.logged_in_as or "not logged in"))
    lines.append(_row("Endpoint", caps.base_url or "unknown"))
    # WHICH of this device's saved accounts answered. Without it, "not logged
    # in" on a machine holding three contexts sends someone hunting for a lost
    # credential when the real answer is that a different one is active.
    if caps.config_context:
        lines.append(_row("Saved account", caps.config_context))
    lines.extend(_interrupted_import_rows())
    lines.append("")

    lines.append("CLI + MCP")
    lines.append(
        _row(
            "Plugin",
            tracking_plugin_name(caps.agent_source) if caps.tracking_plugin_installed else _MISSING,
        )
    )
    if caps.agent_source == "codex":
        mcp_status = (
            "logged in"
            if caps.mcp_authenticated is True
            else "not logged in"
            if caps.mcp_authenticated is False
            else "unknown"
        )
        lines.append(_row("MCP OAuth", mcp_status))
    # The MCP answer every surface prints (Capabilities.mcp_state): "on" only
    # when the credential this agent's MCP sends is there; a login it needs
    # names the command, and the daemon profile says the daemon reads.
    lines.append(_row("MCP", caps.mcp_status()))
    lines.append("")

    if codex_hooks:
        lines.extend(codex_hooks)
        lines.append("")

    lines.append("Session capture")
    tap_name = TAP_PLUGIN_NAME
    lines.append(_row("Plugin", tap_name if caps.capture_plugin_installed else _MISSING))
    capture_status = "capturing" if caps.capture_on else _OFF
    if caps.capture_on and caps.capture_python_missing:
        # Installed, paired and switched on, and still nothing records: the tap
        # found no interpreter to run on (`capture_python_missing`).
        capture_status = f"not running: needs Python 3.11 or newer ({caps.capture_python_missing})"
    lines.append(_row("Status", capture_status))
    if caps.capture_device_id:
        lines.append(_row("Paired device", caps.capture_device_id))
    if caps.capture_awaiting_confirmation:
        lines.append(_row("Killswitch", "ON — waiting for Install to confirm capture (run `probe wizard`)"))
    elif caps.capture_killswitched:
        lines.append(_row("Killswitch", "ON — capture is disabled locally"))
    # The last time this machine's probe CLI deliberately stopped the uploader.
    # A daemon found dead WITHOUT a matching stop here was killed by something
    # else — surfacing the event makes a "transcripts missing" report carry its
    # own cause either way.
    if caps.capture_last_stop:
        lines.append(_row("Last daemon stop", caps.capture_last_stop))
    # Every source is listed, not just the winning one. A user who thinks capture
    # is off deserves to see the credential that is keeping it alive.
    for source in caps.capture_token_sources:
        if source is TokenSource.ENVIRONMENT:
            label = f"{tap_token_env(caps.agent_source)} environment variable"
        else:
            label = _SOURCE_LABEL[source]
        lines.append(_row("Credential from", label))
    if caps.capture_credential_valid is False:
        lines.append(_row("Credential check", "rejected — re-run `probe wizard`"))
    elif caps.capture_token_sources and caps.capture_credential_valid is None:
        lines.append(_row("Credential check", "unknown (offline or endpoint unavailable)"))
    if not caps.capture_token_sources:
        lines.append(_row("Credential", "none — this device is not paired"))
    lines.append("")

    lines.extend(_daemon_rows(caps))
    lines.append("")

    lines.append("Agent rules")
    # pi is no longer capture-only, so this asks the same real question every
    # other source gets. `agent_rules.memory_path("pi")` resolves pi's own
    # ~/.pi/agent/AGENTS.md (it used to fall through to Claude Code's
    # CLAUDE.md, which meant a machine with both agents configured could have
    # `apply_agent_rules` silently install into the wrong file); with that
    # fixed and the wizard offering the capability, the old
    # "not applicable -- pi is capture-only here" row was reporting a limit
    # that no longer exists.
    lines.append(
        _row(
            f"Global {agent_rules.memory_path(caps.agent_source).name}",
            "installed" if caps.agent_rules_installed else "not added",
        )
    )
    # Reported separately from installed/absent. A block from an older release
    # still LOADS, so it reads as working while teaching superseded wording --
    # and this file is the one copy no release can reach, so nothing else would
    # ever surface it. `probe wizard` rewrites it in place.
    if caps.agent_rules_stale:
        lines.append(
            _row("", "outdated wording -- `probe agent-rules refresh` (session start also does this)")
        )
    lines.append("")

    lines.extend(_team_note_rows())
    lines.append("")

    snapshot_rows = _snapshot_ref_rows()
    if snapshot_rows:
        lines.extend(snapshot_rows)
        lines.append("")

    lines.append("Auto-update")
    lines.append(_row(
        "Enabled",
        "yes (on by default for this install)" if caps.auto_update_by_default
        else "yes" if caps.auto_update_enabled else "no",
    ))
    lines.append(_row("Last attempt", caps.last_update_attempt or "never run on this device"))
    # A SEPARATE line, never folded into the one above. Once the run lock exists,
    # a box that has been training all week is deliberately not updating -- and
    # with only a last-attempt timestamp that is byte-identical to an auto-updater
    # that died. This is the line that tells them apart.
    if caps.last_update_skip:
        lines.append(_row("Deferred", caps.last_update_skip))
    lines.extend(_dropped_with_rows())
    if caps.live_runs:
        shown = ", ".join(caps.live_runs[:3])
        if len(caps.live_runs) > 3:
            shown += f", +{len(caps.live_runs) - 3} more"
        lines.append(_row("Runs in flight", shown))

    if service is not None:
        lines.append("")
        lines.extend(service_rows(service))

    lines.append("")
    lines.append("Outbox")
    if caps.outbox_status is None:
        lines.append(_row("Queue", "never used"))
    else:
        status = caps.outbox_status
        lines.append(_row("Pending", str(status.get("pending") or 0)))
        lines.append(_row("Dead-lettered", str(status.get("failed") or 0)))
        from ....sdk.delivery.journal.status_file import auth_blocked_since

        blocked = auth_blocked_since(status)
        if blocked:
            lines.append(_row("Auth-blocked since", str(blocked)))
        if status.get("paused"):
            until = status.get("paused_until")
            lines.append(_row("Paused", f"until {until} (`probe outbox resume`)" if until else "yes (`probe outbox resume`)"))
        if status.get("last_error"):
            lines.append(_row("Last error", str(status["last_error"])))
        rescue = status.get("rescue") or {}
        for fp, writes in (rescue.get("rescued") or {}).items():
            lines.append(
                _row("Rescued", f"credential {fp}: {writes} write(s) of a revoked token, sending "
                     "with your login (same team and user)")
            )
        if rescue.get("adopted_waiting") and not rescue.get("rescued"):
            waiting = rescue["adopted_waiting"]
            lines.append(
                _row("Rescued earlier", f"{waiting} write(s) queued to go out with your login; "
                     "`probe outbox drain` says why any stay")
            )
        for fp, why in (rescue.get("cannot_rescue") or {}).items():
            lines.append(
                _row("Stranded", f"credential {fp}: cannot be sent with your login ({why}); "
                     "`probe outbox status` says what to do")
            )

    if caps.warnings:
        lines.append("")
        lines.append("Warnings")
        for warning in caps.warnings:
            lines.append(f"  ! {warning}")

    return "\n".join(lines)


def _device_problems(caps: Capabilities, recorder: str | None) -> list[str]:
    """What the full report's device sections say is wrong (the daemon, the
    outbox), for `summary`: the sections themselves stay in the report. Only
    states that are a problem whenever they hold: the daemon's error log also
    takes routine notes (a reinstall), and an outbox's last error can belong
    to a queue already emptied, so both stay in the full report alone."""
    from probe.sdk import session_marker

    from probe.cli import wizard as wizard

    found: list[str] = []
    if recorder == session_marker.RECORDER_DAEMON and not wizard.companion_token_held():
        found.append("The Probe daemon has no key: press Enter on Who records to approve one.")
    if recorder == session_marker.RECORDER_DAEMON and caps.daemon_ai_libraries == "missing":
        found.append("The Probe daemon's AI libraries are missing: press Enter on Who records to install them.")
    status = caps.outbox_status or {}
    if status:
        from ....sdk.delivery.journal.status_file import auth_blocked_since

        if status.get("failed"):
            found.append(f"Outbox: {status['failed']} write(s) dead-lettered (`probe outbox status`).")

        if auth_blocked_since(status):
            found.append(f"Outbox: blocked on its credential since {auth_blocked_since(status)} (`probe outbox status`).")
        if status.get("paused"):
            found.append("Outbox: paused (`probe outbox resume`).")
        if (status.get("rescue") or {}).get("cannot_rescue"):
            found.append("Outbox: writes stranded under a revoked credential (`probe outbox status`).")
    return found


def summary(caps_by_source: "dict[str, Capabilities]", *, recorder: str | None = None) -> list[str]:
    """Diagnose's page in the wizard: the verdict, a line for the device and
    one per coding agent, then the problems and what to do about each. The
    full report (`render`, every section for every agent: ~300 lines for four
    agents, most of it the device's own sections said four times) is what `c`
    copies and `probe doctor` prints."""
    from probe.cli.wizard.actions import onboarding as actions
    from probe.shared.harness.harnesses.codex import hooks as codex_hooks
    from probe.cli import wizard as wizard

    from probe.cli.wizard.state.state import McpState

    per_agent: dict[str, list[str]] = {}
    for source, caps in caps_by_source.items():
        found = [*caps.warnings, *actions.problems(caps)]
        # Codex's own warning already says its MCP is not logged in.
        if caps.mcp_state == McpState.LOGIN_NEEDED and not any("not logged in" in w for w in found):
            found.append(f"MCP {caps.mcp_status()}")
        per_agent[source] = list(dict.fromkeys(found))
    # Each problem once, naming the agents that have it; one every agent has
    # is the device's, and goes unnamed.
    holders: dict[str, list[str]] = {}
    for source, found in per_agent.items():
        for w in found:
            holders.setdefault(w, []).append(source)
    problems = []
    for w, sources in holders.items():
        label = wizard.agent_label(sources)
        if len(per_agent) > 1 and len(sources) == len(per_agent):
            problems.append(w)
        else:
            problems.append(w if w.startswith(f"{label}:") else f"{label}: {w}")
    if any(caps.codex_available for caps in caps_by_source.values()):
        hooks = codex_hooks.status()
        if hooks is not None and hooks.untrusted:
            problems.append(
                f"Codex: {len(hooks.untrusted)} of {hooks.total} Probe hooks are off until approved; "
                f"{codex_hooks.FIX_HINT}."
            )
        problems += [f"Codex warns: {warning[:200]}" for warning in (hooks.warnings if hooks else ())]
    first = next(iter(caps_by_source.values()), None)
    if first is not None:
        problems += _device_problems(first, recorder)
    count = len(problems)
    verdict = "no problems found" if not count else f"{count} problem{'' if count == 1 else 's'}"
    lines = [f"Probe Research doctor: {verdict}"]
    if first is not None:
        device = [first.logged_in_as or "not signed in", f"CLI {first.cli_version or 'not found'}"]
        if recorder:
            device.append(f"Who records: {recorder}")
        lines.append(" · ".join(device))
    if caps_by_source:
        width = max(len(wizard.agent_label(source)) for source in caps_by_source)
        lines.append("")
        lines += [
            f"  {wizard.agent_label(source):<{width}}   tracking {'on' if caps.tracking_on else 'off'}"
            f" · capture {wizard._capture_word(caps)}"  # the menu's words: a sign-in's lock says what lifts it
            for source, caps in caps_by_source.items()
        ]
    if problems:
        lines += ["", "Problems:", *(f"  {problem}" for problem in problems)]
    lines += ["", "c copies the full report; `probe doctor` prints it."]
    return lines
from probe.cli.wizard.doctor.daemon_rows import _daemon_rows  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.doctor.local_rows import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _dropped_with_rows,
    _interrupted_import_rows,
    _snapshot_ref_rows,
    _team_note_rows,
)
from probe.cli.wizard.doctor.service_status import service_rows  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.doctor.version_rows import _version_rows  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.harness.diagnosis import _MISSING, _OFF, _OK, _row  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.harness.harnesses.kimi_code.doctor import _kimi_rows  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.shared.harness.harnesses.pi.doctor import _pi_capture_rows  # noqa: E402 -- pieces need each other; the front door loads this one first
