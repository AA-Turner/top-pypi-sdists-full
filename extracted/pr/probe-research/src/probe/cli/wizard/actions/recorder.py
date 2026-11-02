"""the Who records action: the agent or the Probe daemon records; the daemon's key (consent, mint, refused key) and its page."""

from __future__ import annotations
import os
import time

from .... import errors
from ....sdk.settings.settings import (
    load_context,
    resolve,
    save_context)
from ....sdk import session_marker
from ....sdk.settings.device import DevicePrompt


def _recorder_page(
    chosen: str,
    sources: list[str],
    moved: list[str],
    lines: list[str],
    *,
    daemon_page: list[str],
    left_alone: list[str],
    switched: list[str] | None = None,
) -> list[str]:
    """Who records' final page: who records now, for how many agents, what to
    do next and the errors. It used to be every step for every agent ("Who
    records in X → ...", "Takes effect in new X sessions." four times, the
    reasoning-summaries paragraph, "Installed 11 skill(s) in <path>: <names>"
    as its title)."""
    from probe.cli import wizard as wizard

    # `moved` is who records as chosen now; `switched`, who this run moved
    # (an agent already there is in the first only).
    switched = moved if switched is None else switched
    counted = wizard.agents_counted(sources, moved)
    if not switched:
        headline = ["Who records did not change", *left_alone]
    elif chosen == session_marker.RECORDER_DAEMON:
        headline = [f"The Probe daemon now records for {counted}", *left_alone]
    elif len(sources) == 1:
        headline = [f"{counted} records for itself again"]
    else:
        headline = [f"{counted[0].upper()}{counted[1:]} record for themselves again"]
    # What the daemon page set (reasoning summaries) is part of the answer.
    headline += [line for line in daemon_page if line.strip()]
    next_steps = []
    if switched:
        next_steps.append("Start new sessions to use it: open ones keep recording as before.")
    next_steps += [line.strip() for line in lines if "`/hooks`" in line or line.startswith("Kept the daemon's key")]
    details = [line for line in wizard.attention_lines(lines) if line.strip() not in next_steps]
    return wizard.result_page(headline, next_steps=next_steps, details=details)


def _run_recorder_action(
    *,
    yes: bool,
    caps_by_source: dict | None = None,
    base_now: str | None = None,
    chosen: str | None = None,
    telemetry=None,
    agent_rules: bool | None = None,
    disclosed: bool = False,
    show_daemon_page: bool = True,
) -> list[str] | None:
    """The main menu's Who records row: the agent or the Probe daemon, ONE value
    for every coding agent on this device (Richard 2026-09-29).

    `chosen`: the row was switched (`←`/`→`), and the switch applies now, no
    Enter: each agent moves (`setup.apply_recorder`: plugins, the instruction
    block), and moving to the daemon asks for the daemon's own sign-in (the
    browser approval that mints its key) and then its page. A team the daemon
    is not open to (the server's answer) is told so and nothing moves.
    Without `chosen` (Enter on the row): the daemon's page, when it records.

    Every switch reports `wizard.recorder_changed` with how it ended, the
    server's refusal included (#probe-usage pings it).

    `agent_rules` is `--agent-rules/--no-agent-rules` beside `--who-records`:
    it decides each moved agent's instruction block, and None keeps whatever
    each file has (`setup.apply_recorder`).

    A switch to the daemon that will mint its key shows the daemon's consent
    first (`setup.run_daemon_consent`): the key comes from this device's
    sign-in, so the browser page that used to disclose it never opens.
    `disclosed` says a screen already showed it (the install's Defaults
    step); `show_daemon_page=False` skips the page that follows a switch.
    """
    from probe.cli import wizard as wizard
    from probe import analytics as telemetry_mod

    tel = telemetry_mod.null_context() if telemetry is None else telemetry
    caps_by_source = caps_by_source or {}
    base = base_now or resolve(base_url=_conn.base_url).base_url
    current = wizard.machine_recorder()
    headless = yes or not wizard.interactive()
    if headless and chosen is None:
        return [f"{wizard.RECORDER_ROW_TITLE}: {current}", "",
                "`probe wizard` › Defaults › Who records switches it."]
    daemon = session_marker.RECORDER_DAEMON
    if chosen is None:
        if current != daemon:
            return None
        # Enter on the row while the daemon records also brings along any
        # set-up agent still recording itself: an agent that gained a daemon
        # profile in an update (pi, 2026-10) never moves on its own, because
        # who records decides what leaves the machine.
        behind = [
            source
            for source in wizard.RECORDER_SOURCES
            if source in caps_by_source
            and caps_by_source[source].configured
            and session_marker.recorder(source) != daemon
        ]
        if not behind:
            # Otherwise Enter is the daemon's repair: a key revoked on the
            # dashboard, or libraries gone after an update, have no other way
            # back in the wizard (switching away and back would revoke the key
            # and ask for a second approval).
            # A revoked key is re-minted only after the consent is shown again:
            # revoking it on the dashboard was a person turning the daemon off.
            consent = _sign_in_mint_consent(base, [], disclosed=False)
            if consent is None:
                return None
            repaired = _ensure_daemon(base, sign_in=consent)
            page = _run_daemon_page(caps_by_source=caps_by_source)
            # A repair says what it replaced and why (a refused key): a line or
            # two, and the reason a browser approval just opened.
            return [*repaired, *(page or [])] or None
        chosen = daemon
    sources = [source for source in wizard.RECORDER_SOURCES if source in caps_by_source]
    # SAY WHICH AGENTS STAY BEHIND: an agent with no daemon profile, if one is
    # ever set up. A switch that names only the agents it moved reads as "every
    # agent here" -- a customer with pi found out from what was missing
    # (2026-10-02). Only agents Probe is set up for.
    left_alone = [
        f"{wizard.agent_label(source)} keeps recording itself: it has no daemon profile yet."
        for source, snapshot in caps_by_source.items()
        if chosen == daemon and source not in wizard.RECORDER_SOURCES and snapshot.configured
    ]
    # An agent already on the chosen profile is left alone: moving it again
    # would reinstall a plugin its owner may have declined.
    pending = [source for source in sources if session_marker.recorder(source) != chosen]
    # Agents a pre-flight already kept on their profile (and said why).
    held: set[str] = set()
    # A rules flag beside the switch applies to agents already on the profile
    # too, and FIRST: it is a local edit that needs no sign-in, no daemon key
    # and no server's yes, and on a machine already on the daemon
    # `--who-records daemon --no-agent-rules` is the way to take out a block
    # the switch should never have written.
    lines: list[str] = []
    if agent_rules is not None:
        for source in sources:
            if source not in pending:
                lines.extend(wizard.apply_recorder_rules(source, chosen, agent_rules))
    # The rules edit above happened whatever stops the switch below.
    nothing = "Who records did not change" if lines else "nothing changed"
    unchanged = f"{nothing[0].upper()}{nothing[1:]}."

    def _stopped(*why: str) -> list[str]:
        """A switch that stopped: why, then only the errors of what ran before
        (a key minted, skills copied are the routine report)."""
        if headless:
            return [*lines, *why]
        return wizard.result_page([line.removeprefix("! ") for line in why], details=wizard.attention_lines(lines))

    if chosen == daemon and not resolve(base_url=base).token:
        # A signed-out machine would move every agent onto a profile with no
        # credential to record with. Back to the agent stays open: it is the
        # way off the daemon.
        return _stopped("Sign in before switching Who records to the daemon (`probe wizard --action login`).",
                        unchanged)
    if not sources:
        return ["No coding agent set up on this device has a daemon profile yet.", *left_alone, "Nothing changed."]
    from probe.cli.wizard import terminal as tui

    started = time.monotonic()

    def _report(outcome: "telemetry_mod.RecorderOutcome", moved: list[str]) -> None:
        tel.emit(
            telemetry_mod.EVENT_WIZARD_RECORDER_CHANGED,
            recorder=chosen,
            outcome=outcome,
            agents=moved,
            agent_count=len(sources),
            duration_seconds=round(time.monotonic() - started, 3),
        )

    if chosen == daemon:
        # The spinner, never a blank screen, while the server answers.
        with tui.working("Checking the Probe daemon is open to your team"):
            offered, note = wizard.daemon_availability(base_url=base)
        if offered is False:
            _report(telemetry_mod.RecorderOutcome.REFUSED_PLAN, [])
            return _stopped(note or wizard.DAEMON_UNAVAILABLE_NOTE, unchanged)
        # A key minted from this device's sign-in opens no browser, so the
        # daemon's consent shows here first; a run nobody is watching keeps the
        # browser approval, where the consent is shown (`_sign_in_mint_consent`).
        # A desktop click is a person's explicit choice, even though its CLI
        # child has no terminal. Reuse the installation sign-in, just as the
        # interactive switch does, without a second approval surface.
        sign_in = os.environ.get(telemetry_mod.DESKTOP_HUMAN_ENV) == "1"
        if not headless and not sign_in:
            consent = _sign_in_mint_consent(base, pending, disclosed=disclosed)
            if consent is None:
                return lines or None  # declined or backed out: nothing minted or moved
            sign_in = consent
        # The daemon's key (from the sign-in, else a browser approval; only when
        # missing or refused) and its AI libraries (an install, only when
        # missing), OUTSIDE the spinner: an approval prints its link and waits
        # on the browser, and the install shows its own output (R12). Headless
        # prints the link and never opens a browser.
        from probe.cli.commands.daemon.daemon import ai_libraries

        lines.extend(_ensure_daemon(base, open_browser=not headless, sign_in=sign_in))
        if not wizard.companion_token_held():
            _report(telemetry_mod.RecorderOutcome.NO_KEY, [])
            return _stopped(f"! The daemon has no key, so {nothing}.")
        if ai_libraries() is None:
            _report(telemetry_mod.RecorderOutcome.NO_LIBRARIES, [])
            return _stopped(f"! The daemon's AI libraries are missing, so {nothing}.")
        # An agent whose daemon starts from its own capture (pi) pairs it here,
        # outside the spinner below: the approval prints a link to open. Its
        # package is checked (and updated) FIRST: pairing mints its capture
        # token, and a switch that then stopped on an old package would leave
        # it capturing on agent, which it did not do before.
        for source in pending:
            if wizard.needs_capture_pairing(source):
                with tui.working(f"Checking {wizard.agent_label(source)}'s Probe package"):
                    package = wizard.daemon_package_ready(source)
                lines.extend(package.lines)
                if not package.ok:
                    held.add(source)
                    continue
                lines.extend(
                    wizard.pair_capture(source, base_url=base, open_browser=not headless, sign_in=sign_in)
                )
    if not pending:
        _report(telemetry_mod.RecorderOutcome.MOVED, sources)
        everyone = "every coding agent here" if not left_alone else wizard.agent_label(tuple(sources))
        return _stopped(f"{wizard.RECORDER_ROW_TITLE}: already {chosen} for {everyone}.", *left_alone)
    # Plugin moves capture their own output, so the spinner owns the screen.
    with tui.working("Moving your coding agents to the daemon" if chosen == daemon
                     else "Moving your coding agents back to recording themselves"):
        for source in pending:
            if source not in held:
                lines.extend(wizard.apply_recorder(caps_by_source[source], chosen, base_url=base, rules=agent_rules))
    lines.extend(left_alone)
    # What each agent's config SAYS now, not which steps ran: `apply_recorder`
    # reports a failure as a line and keeps going.
    moved = [source for source in sources if session_marker.recorder(source) == chosen]
    _report(
        telemetry_mod.RecorderOutcome.MOVED if len(moved) == len(sources)
        else telemetry_mod.RecorderOutcome.PARTIAL if moved
        else telemetry_mod.RecorderOutcome.FAILED,
        moved,
    )
    if headless:
        return lines
    daemon_page = (
        _run_daemon_page(caps_by_source=caps_by_source) or []
        if chosen == daemon and wizard.machine_recorder() == daemon and show_daemon_page
        else []
    )
    return _recorder_page(
        chosen, sources, moved, lines, daemon_page=daemon_page, left_alone=left_alone,
        switched=[source for source in moved if source in pending],
    )


def _ensure_daemon(base: str, *, open_browser: bool = True, sign_in: bool = False) -> list[str]:
    """What the Probe daemon needs to record, fetched only where it is missing:
    its key (when none is saved or the server refuses the saved one: minted from
    this device's sign-in when `sign_in` -- the caller showed the daemon's
    consent -- else one browser approval) and its AI libraries (an install, no
    approval). Call it outside any spinner: an approval prints a link and waits
    on the browser."""
    from probe.cli import wizard as wizard
    from probe.cli.wizard import terminal as tui
    from probe.cli.commands.daemon.companion import provision_daemon
    from probe.cli.commands.daemon.daemon import ai_libraries

    is_refused = False
    if wizard.companion_token_held():
        with tui.working("Checking the Probe daemon's key"):
            is_refused = _daemon_key_refused(base)
    if not is_refused and wizard.companion_token_held() and ai_libraries() is not None:
        return []
    lines: list[str] = []
    if is_refused:
        # A refused key is dead weight: dropped first, so a declined approval
        # leaves NO key -- which every caller reads as "nothing moves" -- rather
        # than a saved key the server will not take.
        from probe.sdk.settings.settings import save_context

        save_context({"companion_token": None})
        lines.append("The server refuses the Probe daemon's key, so it needs a new one.")
    return [*lines, *provision_daemon(base, open_browser=open_browser, sign_in=sign_in)]


def _sign_in_mint_consent(base: str, capture_sources, *, disclosed: bool) -> "bool | None":
    """Whether this interactive run may mint the daemon's key (and the capture
    key a settings-profile agent such as pi needs) from this device's sign-in,
    with no browser (Richard 2026-10-26): only once a person saw the daemon's
    consent on THIS run.

    True: they agreed, here or on the install's Defaults step (`disclosed`).
    False: nothing new is needed (the saved key works, no capture to pair), so
    nothing is minted and nothing is asked. None: they declined. A run nobody
    is watching never calls this and keeps the browser approval, where the
    consent is shown."""
    from probe.cli import wizard as wizard
    from probe.cli.wizard import terminal as tui

    if disclosed:
        return True
    with tui.working("Checking the Probe daemon's key"):
        needed = (
            not wizard.companion_token_held()
            or _daemon_key_refused(base)
            or any(wizard.needs_capture_pairing(source) for source in capture_sources)
        )
    if not needed:
        return False
    tui.clear()
    sources = tuple(source for source in wizard.RECORDER_SOURCES) if not capture_sources else tuple(capture_sources)
    return True if wizard.run_daemon_consent(sources) is True else None


def _daemon_key_refused(base: str) -> bool:
    """Whether the server refuses the daemon's saved key (revoked under
    Settings › Connected clients, say). False with no key saved, or when the
    server cannot be reached: an outage is not a reason to mint another key."""
    from probe.sdk.settings.settings import load_context

    try:
        token = str((load_context() or {}).get("companion_token") or "")
    except Exception:  # noqa: BLE001 - an unreadable config holds no key
        return False
    if not token:
        return False
    try:
        return _verify(token, base)[0] == "rejected"
    except errors.RosError:  # a 429, a 404, a 5xx after retries: no answer, not a refusal
        return False


def _run_daemon_page(*, caps_by_source: dict) -> list[str] | None:
    """The daemon's page: what the Probe daemon sees (the agents' reasoning
    summaries). Enter on the main menu's Who records row while the daemon
    records, and straight after switching to it. The settings screen's
    machinery on `setup.DAEMON_GROUPS`: a change is written by `Set settings ›`,
    or by leaving the page with `←`/Escape after making it."""
    from probe.cli import wizard as wizard
    from probe.cli.wizard import terminal as tui

    if not caps_by_source:
        return None
    tui.clear()
    current = wizard.read_settings(caps_by_source)
    picked = wizard.run_settings_menu(
        current,
        groups=wizard.DAEMON_GROUPS,
        frame=(
            "The Probe daemon:",
            [f"  {wizard.RECORDER_ROW_TITLE:<28} {wizard.machine_recorder()}"],
            "What should the daemon see?",
        ),
    )
    if picked is None or picked is tui.BACK:
        return None
    changes = {s: v for s, v in picked.items() if current.get(s) != v}
    return wizard.apply_settings(changes, caps_by_source=caps_by_source) if changes else None


def _authorize_companion(base_url: str, *, open_browser: bool = True, sign_in: bool = False) -> list[str]:
    """Mint the Probe daemon's own credential: from this device's sign-in when
    it can (`setup.mint_from_sign_in`), else through one browser approval.

    Without it the daemon cannot write, and a session in the `daemon` state runs
    DEGRADED -- the agent records, exactly as under `on` -- so a declined or
    failed approval loses nothing; it says so and names the retry.

    The link and code are always printed: the flow blocks polling for an
    approval, and a browser that fails to open (headless, `--no-browser`) would
    otherwise leave the user waiting on a page they were never shown.
    """
    from probe.cli import wizard as wizard

    def _prompt(prompt: DevicePrompt) -> None:
        print("Approve the Probe daemon's key in the browser:", flush=True)
        _show_device_prompt(prompt)

    # From this device's sign-in when the caller showed the daemon's consent
    # (`sign_in`): no browser. Otherwise, or when the device cannot (no
    # installation-bound sign-in, an older server), the browser approval.
    from probe.analytics.analytics import DESKTOP_HUMAN_ENV

    desktop = os.environ.get(DESKTOP_HUMAN_ENV) == "1"
    from_sign_in = wizard.mint_from_sign_in(wizard.COMPANION_GRANT, base_url=base_url) if sign_in or desktop else None
    minted, errors = wizard.authorize(
        [wizard.COMPANION_GRANT],
        base_url=base_url,
        open_browser=open_browser,
        on_prompt=_prompt,
        minted=from_sign_in,
        allow_browser_approval=not desktop,
    )
    if errors or not wizard.companion_token_held():
        return [
            *errors,
            "! The daemon has no key yet, so your agent keeps recording.",
            "  Retry: probe wizard › Who records › daemon.",
        ]
    return ["The Probe daemon has its own key."]
from probe.cli.commands.machine.wizard import wizard  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.snapshots.snapshots import snapshot  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _conn  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.account.device_prompt import _show_device_prompt  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.state.token_verify import _verify  # noqa: E402 -- pieces need each other; the front door loads this one first
