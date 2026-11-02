"""the Settings action: automatic updates and pasted-image uploads, applied per agent through CONFIGURE."""

from __future__ import annotations
from ....sdk.settings.settings import resolve
from ....sdk import session_marker


def _run_settings_action(
    *,
    yes: bool,
    caps_by_source: dict | None = None,
    base_now: str | None = None,
    telemetry=None,
) -> list[str] | None:
    """The settings screen: automatic updates and pasted-image uploads. Who
    records and what the daemon sees are on the main menu's Defaults
    (`_run_recorder_action`).

    Tracking, capture and the instruction rules had rows here and do not any
    more: Probe is installed whole and removed whole (see setup.py's module
    docstring). The default for new sessions moved to the main menu
    (`_run_defaults_action`). Nothing is written while you toggle; `Set
    settings ›` commits the DIFF.

    Automatic updates applies through the CONFIGURE machinery
    (`_apply_capability_settings`) rather than a bare write, so the toggle and
    an Install are the same code asking for a different end state.
    """
    from probe.cli import wizard as wizard
    from probe.cli.wizard import terminal as tui

    caps_by_source = caps_by_source or {}
    if yes or not wizard.interactive():
        # A screen nobody can answer must not answer for them: report state
        # and name the commands that set things headlessly. The capability
        # rows ride along when the caller had snapshots — read with the SAME
        # predicates the interactive boxes use, so headless and interactive
        # can never describe the same machine differently.
        capability_lines: list[str] = []
        if caps_by_source:
            state = wizard.read_settings(caps_by_source)
            cycles = wizard.cycling_settings()
            recorder = wizard.machine_recorder()
            # Who records is ONE value for the machine; what the daemon sees
            # matters only where it records.
            hidden = {*wizard.RECORDER_SETTINGS}
            if recorder != session_marker.RECORDER_DAEMON:
                hidden.add(wizard.Setting.REASONING_SUMMARIES)
            capability_lines.append(f"  {wizard.RECORDER_ROW_TITLE:<28} {recorder}")
            for setting in wizard.Setting:
                if setting in hidden:
                    continue
                title, _detail = wizard.SETTINGS_COPY[setting]
                if setting in cycles:
                    # Three-valued rows say their WORD, not on/off: "off" here
                    # would be indistinguishable from `read`, which is the one
                    # pair a person reading this block must be able to tell
                    # apart -- one of them still searches the team's history.
                    value = wizard.value_label(setting, wizard.cycle_value(setting, state[setting]))
                else:
                    value = "on" if state[setting] else "off"
                capability_lines.append(f"  {title:<28} {value}")
        return [
            "Settings on this device:",
            *capability_lines,
            *([] if caps_by_source else wizard.describe_settings()),
            "",
            "`probe session default on|read|off` sets the default for new sessions.",
            "`probe wizard --auto-update/--no-auto-update` sets automatic updates.",
            *(
                ["`showThinkingSummaries` (Claude Code's settings.json) and `model_reasoning_summary`",
                 "(Codex's config.toml) are whether the daemon sees the agent's reasoning."]
                if caps_by_source and wizard.Setting.REASONING_SUMMARIES not in hidden
                else []
            ),
        ]

    # The interactive screen without the device's snapshots would draw the
    # Automatic updates box OFF regardless of reality, and a commit would
    # iterate zero agents — a lying screen over a silent no-op. The one
    # production call site always passes them; hold the next one to that.
    if not caps_by_source:
        raise AssertionError("interactive settings needs the device's capability snapshots")

    tui.clear()
    # ONE read feeds both the boxes the screen draws and the diff computed
    # against what comes back. Reading again at apply time would reopen the
    # gap: a config change landing while the prompt sat open would make the
    # screen and the write disagree.
    current = wizard.read_settings(caps_by_source)
    picked = wizard.run_settings_menu(current)
    if picked is None or picked is tui.BACK:
        return None  # backed out: nothing happened, nothing to pause on
    # `Set settings` commits the DIFF, not the picker state: unchanged boxes
    # are not rewritten. An empty diff is a no-op, straight back to the menu.
    # `!=`, not `is not`: a cycling row answers with a STATE NAME, and two equal
    # strings are not required to be the same object -- an identity diff would
    # report every unchanged state as a change and rewrite the config on exit.
    changes = {s: v for s, v in picked.items() if current.get(s) != v}
    if not changes:
        return None
    lines: list[str] = []
    problems: list[str] = []
    capability_changes = {s: v for s, v in changes.items() if s in wizard.CAPABILITY_SETTINGS}
    if capability_changes:
        # Each changed setting once, as the other rows say theirs ("Research
        # plan review → on"); of the install machinery's per-agent report
        # (`_apply_capability_settings`) only the errors: it said "Codex:",
        # "Already set up the way you asked. Nothing to change." per agent.
        applied = _apply_capability_settings(
            capability_changes,
            caps_by_source=caps_by_source,
            base_now=base_now or resolve(base_url=_conn.base_url).base_url,
            telemetry=telemetry,
        )
        found = _labelled_problems(applied)
        # What the device says now, not what was asked: Automatic updates is
        # one device-wide file, and an agent's apply can fail after (or
        # without) writing it.
        for setting, value in capability_changes.items():
            title = wizard.SETTINGS_COPY[setting][0]
            now = _capability_setting_now(setting)
            if now is None or now == value:
                lines.append(f"{title} → {'on' if value else 'off'}")
            else:
                lines.append(f"{title} did not change")
        problems += found
    plain = {s: v for s, v in changes.items() if s not in wizard.CAPABILITY_SETTINGS}
    if plain:
        settled = wizard.apply_settings(plain, caps_by_source=caps_by_source)
        lines += [line for line in settled if not wizard.needs_attention(line)]
        problems += wizard.attention_lines(settled)
    return wizard.result_page(
        lines or ["Settings did not change" if problems else "Settings saved."], details=problems
    )


def _capability_setting_now(setting) -> bool | None:
    """A capability setting as the device has it now (None: not one this
    can read): what Settings' page reports after its apply."""
    from probe.shared.updates import autoupdate
    from probe.cli import wizard as wizard

    if setting is wizard.Setting.AUTO_UPDATE:
        try:
            return bool(autoupdate.load().enabled)
        except Exception:  # noqa: BLE001 - unreadable: report what was asked, errors below
            return None
    return None


def _labelled_problems(lines: list[str]) -> list[str]:
    """`setup.attention_lines` of a report made of `Agent:` sections, each
    error named for its agent."""
    from probe.cli import wizard as wizard

    labels = {f"{wizard.agent_label(source)}:" for source in wizard.INSTALLABLE_AGENT_SOURCES}
    out: list[str] = []
    sections: list[tuple[str, list[str]]] = [("", [])]
    for line in lines:
        if line.strip() in labels:
            sections.append((line.strip()[:-1], []))
        elif not line.strip():
            # A section ends on its blank line: what follows is no agent's.
            sections.append(("", []))
        else:
            sections[-1][1].append(line)
    for label, section in sections:
        out += [
            f"{label}: {problem}" if label and not problem.startswith("  ") else problem
            for problem in wizard.attention_lines(section)
        ]
    return out


def _apply_capability_settings(
    changes: dict,
    *,
    caps_by_source: dict,
    base_now: str,
    telemetry=None,
) -> list[str]:
    """Apply capability toggles through the CONFIGURE machinery, PER AGENT.

    NEVER a bare `apply_*` call: the CONFIGURE path owns retries, the progress
    screen and the verified postcondition. Reusing it here means a Settings
    toggle and an Install apply are the same code asking for a different end
    state.

    Each agent gets its OWN target: that agent's current state — read with
    `capability_state_for`, the exact predicates the screen's boxes used —
    with only the toggled rows overridden. Committing one box never touches a
    capability that has no box, on ANY agent. The first ship of this screen
    built one union-derived target and applied it to every agent, which meant
    toggling auto-update on a mixed device re-enabled Session capture on the
    agent that had it off, and — because the preserve baseline used
    `enabled()` while the boxes read the plugin facts — uninstalled a
    signed-out machine's tracking plugin.

    No agent is ever asked for a browser approval: grants follow the CHANGES,
    and no row left on this screen needs one -- deriving the needs from the
    reconciled target is what once turned an unrelated toggle into a login
    prompt. An untouched tracking or capture is left exactly as found
    (`Selection.preserve`): no repair, no install, no removal.

    A failing agent is CONTAINED: the CONFIGURE path reports failure by
    raising `typer.Exit`, and letting that escape here would kill the whole
    wizard mid-Settings and silently skip the remaining agent. Each agent's
    Exit is caught, reported in its own labelled lines, and the loop continues.
    """
    from probe.cli import wizard as wizard

    return _apply_capability_targets(
        {wizard.SETTING_CAPABILITY[setting]: value for setting, value in changes.items()},
        caps_by_source=caps_by_source,
        base_now=base_now,
        telemetry=telemetry,
        retry_hint="re-run `probe wizard` › Settings to retry",
    )
from probe.cli.commands.machine.wizard import wizard  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _conn  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.actions.capabilities import _apply_capability_targets  # noqa: E402 -- pieces need each other; the front door loads this one first
