"""one wizard session inside its window: flags, account, agent targets, the main-menu loop, device actions and the finish."""

from __future__ import annotations

import contextlib
import dataclasses
import os
import sys

import typer
from ....sdk.settings.settings import resolve
from ....sdk import session_marker
from ....sdk.settings.device import OnboardingRequired

#: How old the wizard's held server answer may be when Diagnose reports it.
_DIAGNOSE_MAX_AGE_S = 30.0


def _exit_wizard() -> None:
    """Leave the terminal UI; approved imports keep their detached workers."""
    raise typer.Exit(0)


def _start_device_state(*, warm_manifest: bool = False):
    """The wizard's one server call (`POST /v1/device-state`), sent now on a
    daemon thread: its resolver, at once. Never raises: the menu must render
    without it, so a request that cannot be built answers UNREACHABLE."""
    from probe.cli.wizard import state as capabilities_mod
    from probe.cli import wizard as wizard

    try:
        # `resolve()`, exactly as `doctor.collect()` resolves the API it
        # reports on: the answer is graded against that server, and its
        # bearer is only ever sent to it.
        settings = resolve()
        request = capabilities_mod.device_state_request(
            settings.base_url, settings.token, wizard.INSTALLABLE_AGENT_SOURCES
        )
    except Exception as exc:  # noqa: BLE001 - the menu must render without it
        return capabilities_mod.answered_already(
            capabilities_mod.DeviceState(
                capabilities_mod.DeviceStateOutcome.UNREACHABLE, error=str(exc)
            )
        )
    return capabilities_mod.start_device_state(request, warm_manifest_on_fallback=warm_manifest)


def _wizard_session(
    *,
    agent,
    tracking,
    capture,
    auto_update,
    agent_rules,
    channel,
    uninstall,
    action,
    folder,
    yes,
    auth_code,
    who_records=None,
) -> None:
    """`wizard`, inside its window. See `wizard` for the contract."""
    from probe.cli.wizard.actions import onboarding as actions_mod
    from probe.cli.wizard import doctor as doctor_impl
    from probe.core import events as json_events
    from probe.cli import wizard as wizard
    from probe import analytics as telemetry_mod
    from probe.cli.wizard import terminal as tui

    # `--channel` is accepted and ignored. Plugins update on the USER's schedule,
    # so a machine whose plugin has not been refreshed still spawns
    # `probe wizard --action update --yes --channel latest`; rejecting the flag
    # would break auto-update on exactly the machines that are behind.
    del channel

    (
        install_code,
        explicit_agent_sources,
        tel,
        capabilities_mod,
        _ask_server,
        device_state,
        available_sources,
        agent_defaults,
    ) = _begin_wizard_session(
        agent=agent,
        action=action,
        auth_code=auth_code,
    )

    from contextlib import contextmanager

    @contextmanager
    def _agent_target(source: str):
        """Scope PROBE_AGENT to one operation without leaking it to callers."""
        previous = os.environ.get("PROBE_AGENT")
        os.environ["PROBE_AGENT"] = source
        try:
            yield
        finally:
            if previous is None:
                os.environ.pop("PROBE_AGENT", None)
            else:
                os.environ["PROBE_AGENT"] = previous

    def _collect_agent(source: str, *, fresh: bool = False):
        # `fresh` asks the server again for THIS read: inside an action that
        # runs agent by agent, an earlier agent's step can change what the
        # server would say about the next one.
        state = _ask_server() if fresh else device_state
        with _agent_target(source), doctor_impl.device_state_scope(state):
            return doctor_impl.collect()

    # The action is selected BEFORE an agent. Discover state read-only for the
    # main menu, then collect only the chosen agents after the user picks what
    # they want to do. This keeps the first screen about intent, not plumbing.
    state_sources = explicit_agent_sources or available_sources or agent_defaults
    from probe.cli.wizard.state.mcp_checks import refresh_mcp_token_verdict

    #
    # The Versions row is graded against the cached manifest, which the one
    # call refreshes (nothing else refreshes it when auto-update is off, so
    # without it the box nothing keeps current could never be told so). An
    # older server that lacks the route gets `warm_manifest()`, as before.
    with tui.working("Checking what's installed on this device"):
        # One /v1/me for the read token, under the spinner: a refused one reads
        # "login needed" and makes the install re-authorize `mcp`.
        refresh_mcp_token_verdict()
        state_caps_by_source = {source: _collect_agent(source) for source in state_sources}
    explicit_flags = any(f is not None for f in (tracking, capture, auto_update, agent_rules))

    tel.emit(
        telemetry_mod.EVENT_WIZARD_STARTED,
        fresh_install=not any(c.configured for c in state_caps_by_source.values()),
        agents_available=sorted(available_sources),
        install_method=state_caps_by_source[state_sources[0]].install_method,
        interactive=wizard.interactive(),
    )

    # ONE GATE IN FRONT OF EVERY EXCHANGE, and it has to be here — above both
    # the entry sign-in below (`probe wizard CODE`) and the guided apply further
    # down (`probe install CODE`), because those are the two doors a code can
    # come through and a gate on one of them is a gate on neither.
    #
    # A website install code carries its own identity: it was minted for
    # whoever was signed in on the website, and redeeming it binds THIS device
    # to that account. On a device that already holds a credential that is an
    # account switch, and it is not reversible from here — the exchange detaches
    # the credentials bound to this device (see the rotation block in the
    # backend's device exchange), so by the time we could name the new account
    # the old one is already gone. Asking afterwards would be asking about
    # something that had already happened.
    #
    # Only when we can NAME the account being replaced (see `prior_account`): an
    # unnameable one is an offline device or a revoked token, and redeeming a
    # code there is a repair rather than a switch.
    if install_code is not None:
        switching_from = wizard.prior_account(state_caps_by_source)
        if (
            switching_from is None
            and resolve().token
            and not any(
                snapshot.api_credential_valid is False
                for snapshot in state_caps_by_source.values()
            )
        ):
            # A credential nobody refused, but the one call could not NAME its
            # account (a slow server, a network urllib could not cross). The
            # switch is irreversible, so ask the old way before deciding that
            # there is nothing to switch from.
            switching_from = doctor_impl.name_account()
            if switching_from:
                state_caps_by_source = {
                    source: dataclasses.replace(snapshot, logged_in_as=switching_from)
                    if snapshot.logged_in_as is None
                    else snapshot
                    for source, snapshot in state_caps_by_source.items()
                }
        if switching_from and not yes:
            if not wizard.interactive():
                # Refuse rather than switch. The same rule the bare-headless
                # guard below applies to capture: a consequence nobody can be
                # shown is a consequence nobody consented to.
                for line in wizard.account_switch_refusal(switching_from):
                    tui.say(line)
                raise typer.Exit(1)
            tui.clear()
            if wizard.run_confirm_account_switch(switching_from) is not True:
                tui.say(f"Left as it was — this device is still signed in as {switching_from}.")
                raise typer.Exit(0)

    # A DEVICE WITH NO PROBE ON IT opens straight into the guided install
    # (Richard 2026-10-26; reverses the 2026-08-25 "a bare launch always opens
    # the menu" for this case only): no credential, no coding agent set up, and
    # at least one coding agent here for the install to act on. Its one browser
    # approval at Review is the sign-in, so the menu's sign-in below is skipped;
    # once it finishes, the menu opens as after any install.
    fresh_onboarding = (
        action is None
        and not yes
        and not explicit_flags
        and install_code is None
        and wizard.interactive()
        and _opens_onboarding(state_caps_by_source, available_sources)
    )

    # A bare launch signs in before showing the menu. `install CODE` waits for
    # the agent/capability selection so the one-time exchange grants exactly
    # what the user chose. Existing unattended maintenance stays independent.
    menu_entry = action is None and not yes and not explicit_flags and not fresh_onboarding
    # `wizard.action_chosen`'s `auto_onboarding`: the first pass only, not an
    # Install picked from the menu later in the same run.
    auto_onboarding_pending = fresh_onboarding
    authenticated_action_entry = (
        action in {"account", "defaults", "settings", "import-research", "recorder"} and not yes
    )
    authenticate_menu = (
        (menu_entry or authenticated_action_entry)
        and wizard.interactive()
        and (
            not resolve(base_url=_conn.base_url).token
            or any(
                snapshot.api_credential_valid is False for snapshot in state_caps_by_source.values()
            )
        )
    )
    if (install_code is not None and action != "configure") or authenticate_menu:
        tui.say(
            "Signing in with the website code…"
            if install_code
            else "Sign in to Probe Research in your browser."
        )
        try:
            signed_in = wizard.sign_in(
                base_url=resolve(base_url=_conn.base_url).base_url,
                sources=state_sources,
                on_prompt=_show_device_prompt,
                prepare_install=bool(available_sources),
                **({"install_code": install_code} if install_code is not None else {}),
            )
        except OnboardingRequired as exc:
            _finish_website_onboarding(exc)
        tel.emit(
            telemetry_mod.EVENT_WIZARD_SIGNED_IN,
            outcome=(
                telemetry_mod.SignInOutcome.SUCCESS
                if signed_in.ok
                else telemetry_mod.SignInOutcome.FAILED
            ),
            via_wizard_entry=True,
        )
        for line in signed_in.lines:
            tui.say(line)
        if not signed_in.ok:
            raise typer.Exit(1)
        install_code = None
        # Signing in changed the account (and may have paired capture): ask again.
        device_state = _ask_server()
        state_caps_by_source = {source: _collect_agent(source) for source in state_sources}

    def _require_account():
        # Every entry and return shares this gate. A removal or revoked token
        # must not reopen an unauthenticated menu, and an explicit sign-out
        # must never start another browser sign-in in the same invocation.
        if not resolve(base_url=_conn.base_url).token or any(
            snapshot.api_credential_valid is False for snapshot in state_caps_by_source.values()
        ):
            tui.say("Sign in to use the wizard. Run `npx probe-research` again.")
            raise typer.Exit(0)

    # A state handed back as `wizard.DefaultChoice`, for the DEFAULTS action to
    # apply without opening its picker. The menu's Defaults row saves on each
    # press itself now, so only a caller that still answers DefaultChoice sets
    # it. Reset on every menu, so it never outlives the choice that set it.
    menu_default: str | None = None
    # The same for the Who records row, which applies the moment it is switched
    # (`wizard.RecorderChoice`); None means Enter on the row. `--who-records`
    # sets it for `--action recorder`, `--yes` included (R7).
    menu_recorder: str | None = who_records

    def _show_main_menu():
        nonlocal menu_default, menu_recorder
        _require_account()
        from probe.cli.imports import jobs as import_jobs

        import_jobs.recover_jobs()
        # The menu waits on a person, for as long as they like: it holds no run
        # lock meanwhile (C1). The action picked takes it (`_hold_for_action`).
        _release_for_menu()
        default_before = session_marker.default_session_state()
        picked = wizard.run_action_menu(state_caps_by_source)
        if (
            session_marker.default_session_state() != default_before
            and picked is not actions_mod.Action.DEFAULTS
        ):
            # The Defaults row saves on each press, inside the menu, so it never
            # reaches the pass's own event: count it here as the `defaults`
            # action it is, once per menu -- unless the menu answers DEFAULTS
            # (Enter on the same row), whose pass counts it already.
            tel.emit(
                telemetry_mod.EVENT_WIZARD_ACTION_CHOSEN,
                action=actions_mod.Action.DEFAULTS.value,
                via_flag=False,
            )
        menu_default = None
        menu_recorder = None
        if isinstance(picked, wizard.DefaultChoice):
            menu_default = picked.state
            return actions_mod.Action.DEFAULTS
        if isinstance(picked, wizard.RecorderChoice):
            menu_recorder = picked.value
            return actions_mod.Action.RECORDER
        return picked

    if authenticated_action_entry and wizard.interactive():
        _require_account()

    # Everything the dashboard used to hide in collapsed sections lives here,
    # next to the state it acts on. The main menu is always the first
    # interactive decision, including on a fresh machine; agent and capability
    # selection follow only after the user chooses an action.
    chosen_action = actions_mod.Action.CONFIGURE
    if action is not None:
        try:
            chosen_action = actions_mod.Action(action)
        except ValueError:
            unknown = (
                f"unknown action {action!r}; expected one of: "
                f"{', '.join(a.value for a in actions_mod.Action)}"
            )
            tui.final(unknown, file=sys.stderr)
            json_events.error(json_events.ErrorCode.USAGE, unknown)
            raise typer.Exit(2) from None
    elif fresh_onboarding:
        chosen_action = actions_mod.Action.CONFIGURE
    elif not yes and not explicit_flags and wizard.interactive():
        tui.clear()
        picked = _show_main_menu()
        if picked is None or picked is tui.BACK:
            _exit_wizard()
        chosen_action = picked
    elif not yes and not explicit_flags and explicit_agent_sources is None:
        # BARE `probe wizard`, HEADLESS: refuse rather than install.
        #
        # `chosen_action` defaults to CONFIGURE, and every screen that would
        # have turned that default into a decision is gated on `interactive()`
        # -- the action menu just above, and `run_confirm_install` further down,
        # which is where the capture disclosure is drawn. So a bare
        # `npx probe-research` from an agent's shell tool skipped BOTH and ran a
        # complete install: tracking, capture, auto-update and agent rules all
        # enabled from FRESH_DEFAULTS, with no menu, no disclosure and no
        # keystroke. It then reported success, which is worse than crashing --
        # capture streams prompts, assistant replies and shell commands off the
        # machine, and the run that enabled it never showed anyone that it had.
        #
        # Refusing is narrow on purpose, and every deliberate caller is already
        # outside it: `probe install` passes `action="configure"`, auto-update
        # spawns `--action update --yes`, and a script that means it says `--yes`,
        # names a capability flag, or names `--agent`. What is left is exactly
        # the case that cannot have been meant -- no verb, no flags, no agent,
        # nobody watching.
        print(
            "probe wizard: refusing to configure without a decision.\n"
            "  Nothing has been changed.\n"
            "  This is the interactive menu, and there is no terminal here to "
            "draw it on.\n"
            "  To install:  probe wizard --action configure\n"
            "  Non-interactively, say what you want: --yes, or --action <name>.",
            file=sys.stderr,
        )
        json_events.error(
            json_events.ErrorCode.USAGE,
            "refusing to configure without a decision: pass --yes, or --action <name>",
        )
        raise typer.Exit(2)

    base_now = resolve(base_url=_conn.base_url).base_url

    # The menu comes BACK after each action. Dropping the user to a shell once
    # one task finishes is the same "go do it yourself" failure as printing a
    # command: after an update you want doctor, after a removal you often want
    # to turn something else on.
    looping = action is None and not yes and not explicit_flags and wizard.interactive()

    while True:
        if chosen_action is actions_mod.Action.EXIT:
            _exit_wizard()

        # The menu let go of the run lock while it waited (C1): this action
        # takes it again. Another setup that took it meanwhile turns the action
        # away, having run nothing, back to the menu.
        if not _hold_for_action(chosen_action, yes=yes, who_records=who_records):
            from probe.cli.wizard.session import lock as wizard_lock

            if not looping:  # an `--action` run has no menu to go back to
                tui.final(f"probe wizard: {wizard_lock.BUSY_MESSAGE} on this device. Nothing has been changed.",
                          file=sys.stderr)
                json_events.error(json_events.ErrorCode.BUSY, wizard_lock.BUSY_MESSAGE)
                raise typer.Exit(wizard_lock.BUSY_EXIT_CODE)
            tui.page(
                [
                    actions_mod.ACTION_COPY[chosen_action][0],
                    "",
                    f"{wizard_lock.BUSY_MESSAGE} on this device (a terminal or the desktop app). "
                    "Nothing has been changed: try again when it finishes.",
                ],
                prompt="Press enter to return to the menu…",
            )
            tui.clear()
            picked = _show_main_menu()
            if picked is None or picked is tui.BACK:
                _exit_wizard()
            chosen_action = picked
            continue

        # At the convergence point where the action is known for this pass,
        # whether it came from the menu or --action — never inside menu code,
        # which the test suite cannot execute.
        tel.emit(
            telemetry_mod.EVENT_WIZARD_ACTION_CHOSEN,
            action=chosen_action.value,
            via_flag=action is not None,
            # A fresh device's first install, opened without the menu: the
            # funnel tells it apart from an Install picked there.
            auto_onboarding=auto_onboarding_pending and chosen_action is actions_mod.Action.CONFIGURE,
        )
        auto_onboarding_pending = False

        # THE GUIDED INSTALL: choose the coding agents (only when this
        # machine offers a choice), then review everything the install turns
        # on and confirm. There is no capability picker -- the install is
        # complete by design (see setup.py's module docstring for what carries
        # the capture disclosure now), and the interactive Install action is
        # FORCE-ON: everything enables, the capture killswitch included, with
        # the disclosure on screen before the confirming keystroke. The flag
        # path is untouched -- an omitted flag on a scripted re-run still
        # PRESERVES.
        shared_selection = None
        install_needs: list[str] | None = None
        install_context: dict | None = None
        install_capture_sources: list[str] | None = None
        guided_install = False
        agent_screen_shown = False
        back_to_menu = False
        # The Defaults step's picks, HELD until the Install keypress: they start
        # on what this device has now (a fresh one: agent, on).
        onboarding_pick = wizard.DefaultsPick(
            recorder=wizard.machine_recorder(),
            session_state=session_marker.default_session_state(),
        )
        # What Who records opened on: only a CHANGED row moves agents. On a
        # machine where some agents record through the daemon the row opens on
        # `daemon`, and pressing Next must not move the others (an agent already
        # set up never moves on its own, `follow_machine_recorder`).
        opened_recorder = onboarding_pick.recorder
        saved_default_lines: list[str] = []
        wizard.INSTALL_RECORDER_PICK.set(None)
        while True:
            agent_sources = explicit_agent_sources
            if (
                agent_sources is None
                # A screen that asks a question with one possible answer is a
                # step for nothing: the agent picker only appears when BOTH
                # coding agents are actually on this machine. `--yes` promised
                # to skip the prompts, so it skips this one too.
                and not yes
                and len(available_sources) > 1
                and chosen_action not in actions_mod.IMPORT_ACTIONS
                # Account and settings are device-wide: one config file, not one
                # per agent. Asking which coding agents to configure before
                # "sign out" is a question with no bearing on the answer. The
                # selection still defaults to every agent found here, because
                # the CAPTURE half of an account change is per agent.
                and chosen_action not in actions_mod.DEVICE_ACTIONS
                and wizard.interactive()
            ):
                tui.clear()
                picked_agents = wizard.run_agent_menu(agent_defaults, action=chosen_action)
                if picked_agents is None or picked_agents is tui.BACK:
                    back_to_menu = True
                    break
                agent_sources = picked_agents
                agent_defaults = picked_agents
                agent_screen_shown = True
            elif agent_sources is None:
                # Zero or one agent found (no choice to ask), or a headless
                # call, which has no picker to show. Backfill is
                # agent-independent but _run_wizard_action still needs one
                # capability snapshot for shared account/base-url state.
                #
                # DEVICE actions cover every agent FOUND on the machine, never
                # what the previous action happened to select: `agent_defaults`
                # remembers the last picker answer (and a Codex session pins
                # it to codex), so scoping Settings to it let a device-wide
                # screen report "capture off" while the other agent kept
                # capturing.
                if chosen_action in actions_mod.IMPORT_ACTIONS:
                    agent_sources = agent_defaults[:1]
                elif chosen_action in actions_mod.DEVICE_ACTIONS:
                    agent_sources = available_sources or agent_defaults
                else:
                    agent_sources = agent_defaults

                # SAY WHICH AGENTS, when nothing else on this run will.
                #
                # Interactively the picker or the confirm screen names the
                # selection; headless there is neither, so an implicit choice
                # across a multi-agent machine would otherwise be reported
                # nowhere at all -- and "which agents did that configure?" is
                # exactly the question a caller cannot answer afterwards from a
                # log full of green ticks. Printed only when it is genuinely a
                # choice (more than one agent found, none named on the command
                # line): a one-agent machine has nothing to disambiguate.
                if (
                    not wizard.interactive()
                    and explicit_agent_sources is None
                    and len(available_sources) > 1
                ):
                    print(
                        "configuring every coding agent found on this device: "
                        f"{wizard.agent_label(agent_sources)}"
                        " (pass --agent to choose)",
                        flush=True,
                    )

            # Every action draws from the menu's snapshot rather than
            # re-collecting: the menu loop re-reads state after every action
            # that changes it, so the snapshot is current, and nothing has
            # changed between drawing the menu and this keypress. An agent the
            # snapshot lacks (picked in the agent step) is read through the
            # same server answer, with no new call.
            with tui.working("Checking what's installed on this device") if any(
                source not in state_caps_by_source for source in agent_sources
            ) else contextlib.nullcontext():
                caps_by_source = {
                    source: state_caps_by_source.get(source) or _collect_agent(source)
                    for source in agent_sources
                }
            caps = caps_by_source[agent_sources[0]]
            configured = any(snapshot.configured for snapshot in caps_by_source.values())

            # The SAME condition `_run_wizard_action` used to gate its own copy
            # of these prompts, deliberately -- including `--action configure`
            # (and `probe install`, its alias), which is interactive but does
            # not loop.
            if not (
                chosen_action is actions_mod.Action.CONFIGURE
                and not yes
                and not explicit_flags
                and wizard.interactive()
            ):
                break

            tui.clear()
            # Availability of the agents this run actually SELECTED — not of
            # the machine at large: `probe install --agent codex` on a
            # Claude-only box must get the degraded screen, not a promise of
            # Codex plugins the apply cannot keep. A PARTIAL miss (`--agent
            # both`, one binary present) keeps the full screen but names the
            # absent agent on it, so the screen promises exactly what the
            # apply will do.
            #
            # pi is excluded from this question entirely, not folded into it:
            # "degraded" here measures whether a MARKETPLACE binary the apply
            # needs is missing, and pi's install is a settings.json write
            # that needs no binary at all -- so this filters on
            # wizard.MARKETPLACE_AGENT_SOURCES, NOT the (pi-inclusive)
            # INSTALLABLE_AGENT_SOURCES. Filtering on the latter would make a
            # pi-only interactive run compute plugins_available=False and show
            # the degraded "skipped, install pi and re-run" screen for a run
            # whose install cannot be degraded by any missing binary.
            #
            # `available_sources` itself CAN contain "pi" now (see
            # `detectable_sources`) -- that is what lets a pi-only machine
            # skip this screen family entirely via the `len(available_sources)
            # > 1` gate above, before ever reaching this filter. What must
            # stay true here is narrower: pi must never enter
            # `plugin_promising_sources`, because it is never what
            # "degraded" is measuring.
            plugin_promising_sources = tuple(
                source for source in agent_sources if source in wizard.MARKETPLACE_AGENT_SOURCES
            )
            plugins_available = not plugin_promising_sources or any(
                source in available_sources for source in plugin_promising_sources
            )
            # Defaults (who records, what new sessions do), then Review: Back on
            # Review returns to Defaults, Back on Defaults to the agent screen.
            while True:
                answer, onboarding_pick = wizard.run_defaults_step(
                    onboarding_pick, agent_screen_shown=agent_screen_shown
                )
                if answer is None:
                    _exit_wizard()
                if answer is tui.BACK:
                    confirmed = tui.BACK
                    break
                tui.clear()
                confirmed = wizard.run_confirm_install(
                    agent_sources,
                    # Omit the skipped agent screen from the progress count.
                    step=wizard.STEP_CONFIRM if agent_screen_shown else None,
                    plugins_available=plugins_available,
                    unavailable=tuple(
                        source for source in plugin_promising_sources if source not in available_sources
                    ),
                    defaults=onboarding_pick,
                )
                if confirmed is not tui.BACK:
                    break
                tui.clear()
            if confirmed is None:
                _exit_wizard()
            if confirmed is tui.BACK:
                if agent_screen_shown and explicit_agent_sources is None:
                    continue  # re-open the agent screen; the selection is kept
                # `--agent` answered the only earlier step, or there was none.
                # The action menu is the previous screen.
                back_to_menu = True
                break
            guided_install = True
            # The Install keypress applies the session default NOW, before any
            # plugin is installed: an `off` picked here must hold even if the
            # person walks away mid-install (Codex O2). Who records follows the
            # installs (`_apply_recorder_pick`): it needs the plugins in place.
            default_lines = _save_session_default(onboarding_pick.session_state)
            # The installs read this: a changed Who records keeps a newly set-up
            # agent from following the device's old recorder first.
            wizard.INSTALL_RECORDER_PICK.set(
                onboarding_pick.recorder if onboarding_pick.recorder != opened_recorder else None
            )
            if default_lines:
                failed = next((line for line in default_lines if wizard.reports_failure(line)), None)
                if failed is not None:
                    tui.page(
                        ["Probe in new sessions", "", failed, "", "Nothing was installed."],
                        prompt="Press enter to return to the menu…",
                    )
                    back_to_menu = True
                    break
                tel.emit(
                    telemetry_mod.EVENT_WIZARD_ACTION_CHOSEN,
                    action=actions_mod.Action.DEFAULTS.value,
                    via_flag=False,
                )
                saved_default_lines = default_lines  # said on the summary page
            # FORCE-ON: Install means install. Everything enables -- including
            # re-pairing a killswitched capture, which the confirm screen just
            # disclosed. Scripted paths never reach here; their omitted flags
            # PRESERVE (see resolve_selection).
            #
            # UNLESS the degraded screen was the one shown: it disclosed the
            # CLI and the sign-in and said the plugins are SKIPPED -- so the
            # selection enables exactly that, and everything it did NOT
            # mention is PRESERVED as it stands. Applying the full force-on
            # there would request a capture grant no bullet ever named;
            # applying all-off would be just as undisclosed in the other
            # direction — on a configured machine whose binaries are
            # temporarily missing it would killswitch a live capture and
            # strip the rules a screen that said "skipped" never named.
            # The wizard authenticated before opening the menu. Reuse those
            # credentials, including capture paired but left disabled until
            # this confirmation. Direct installs and older logins can still
            # lack grants; only those need a browser approval here.
            if plugins_available:
                shared_selection = wizard.Selection(
                    tracking=True, capture=True, auto_update=True, agent_rules=True
                )
            else:
                current_union = {
                    capability: any(
                        snapshot.enabled()[capability] for snapshot in caps_by_source.values()
                    )
                    for capability in wizard.Capability
                }
                shared_selection = wizard.Selection(
                    tracking=True,
                    capture=current_union[wizard.Capability.CAPTURE],
                    auto_update=current_union[wizard.Capability.AUTO_UPDATE],
                    agent_rules=current_union[wizard.Capability.AGENT_RULES],
                    # Never named on this screen, so kept as it stands: the union
                    # read says off behind a sign-in's pending lock, and applying
                    # that off revoked the parked credential (`Selection.preserve`).
                    preserve=frozenset({wizard.Capability.CAPTURE}),
                )
            install_needs = (
                []
                if install_code is None
                and _install_grants_held(caps_by_source, shared_selection, base_url=base_now)
                else wizard.grants_for(shared_selection)
            )
            if (
                install_needs
                and onboarding_pick.recorder == session_marker.RECORDER_DAEMON
                and wizard.COMPANION_GRANT not in install_needs
                and not wizard.companion_token_held()
            ):
                # The install opens a browser approval anyway: the daemon's key
                # rides it, and that page carries the daemon's disclosure.
                install_needs.append(wizard.COMPANION_GRANT)
            install_context = wizard.install_client_context(caps_by_source)
            if not plugins_available:
                # The degraded path preserves capture rather than granting it,
                # so the only capture credentials this approval may touch are
                # the ones the device ALREADY holds locally — sign_in's
                # ride-along rule. Without it, an account switch here moved
                # api/mcp to the new team while capture kept uploading to the
                # old one, under a token the new team cannot see or revoke.
                install_capture_sources = (
                    wizard.locally_paired_capture(agent_sources) if shared_selection.capture else []
                )
            else:
                install_capture_sources = list(agent_sources) if shared_selection.capture else []
            break

        if back_to_menu:
            if not looping:
                raise typer.Exit(0)
            if fresh_onboarding and not resolve(base_url=_conn.base_url).token:
                # Backed out of a fresh device's onboarding: there is no account
                # yet, so there is no menu to go back to.
                tui.final("Nothing changed. Run `npx probe-research` again to set up Probe.")
                raise typer.Exit(0)
            tui.clear()
            picked = _show_main_menu()
            if picked is None or picked is tui.BACK:
                _exit_wizard()
            chosen_action = picked
            continue

        if install_code is not None and chosen_action is actions_mod.Action.CONFIGURE:
            # A code always authenticates, including on a configured machine or
            # when all optional tooling capabilities were explicitly declined.
            _aggregate, resolved = _shared_selection(
                caps_by_source,
                tracking=tracking,
                capture=capture,
                auto_update=auto_update,
                agent_rules=agent_rules,
                configured=configured,
            )
            shared_selection = shared_selection or resolved
            install_needs = list(
                dict.fromkeys(["api", "mcp", *wizard.grants_for(shared_selection)])
            )
            # The desktop already obtained browser consent for this one-use install code.
            # Include the explicitly selected daemon's own scoped key in that same
            # exchange; never substitute the account PAT or widen an Inline install.
            if who_records == session_marker.RECORDER_DAEMON:
                install_needs.append(wizard.COMPANION_GRANT)
            install_capture_sources = list(agent_sources) if shared_selection.capture else []
            install_context = wizard.install_client_context(caps_by_source)

        installation_completion = (
            _InstallationCompletion(
                len(agent_sources),
                was_configured=_probe_already_installed(
                    [*state_caps_by_source.values(), *caps_by_source.values()]
                ),
            )
            if chosen_action is actions_mod.Action.CONFIGURE
            else None
        )
        if chosen_action is actions_mod.Action.UNINSTALL and not explicit_agent_sources:
            # The menu's Uninstall is `probe uninstall` (its own confirmation,
            # phases and finisher): one implementation for every way in. With
            # `--agent`, only those agents (the per-agent removal below).
            raise typer.Exit(_run_uninstall(yes=yes, json_output=json_events.enabled()))
        if chosen_action is actions_mod.Action.DIAGNOSE:
            # Diagnose reports what is true NOW: ask again when the held answer
            # is old or was not an answer at all (one call, for every agent).
            if device_state.stale(_DIAGNOSE_MAX_AGE_S):
                device_state = _ask_server()
            # Each agent's own CLI, not its record: a `claude` that cannot start
            # is what Diagnose is there to show, and the menu read the records.
            with capabilities_mod.plugin_records(False):
                caps_by_source = {source: _collect_agent(source) for source in agent_sources}
            caps = caps_by_source[agent_sources[0]]
        # `--json`'s `result`: a row per coding agent changed, or one for the
        # device's own credentials (agent null).
        if chosen_action in {
            actions_mod.Action.CONFIGURE, actions_mod.Action.UPDATE, actions_mod.Action.UNINSTALL,
        }:
            json_events.begin_result(chosen_action.value, agent_sources)
        elif chosen_action in {actions_mod.Action.SIGN_IN, actions_mod.Action.SIGN_OUT}:
            json_events.begin_result(chosen_action.value, [None])
        elif chosen_action is actions_mod.Action.RECORDER and menu_recorder is not None:
            # Its rows are the agents the switch applies to (`_record_recorder`).
            json_events.begin_result(chosen_action.value, [])
        # Update's one question for capture a sign-in left waiting
        # (`_confirm_pending_capture`): above every Update path, one agent or
        # several, and BEFORE the hand-off, which may exec the newest release
        # and never come back to ask.
        pending_capture_lines: list[str] = []
        if (
            chosen_action is actions_mod.Action.UPDATE
            and not yes
            and wizard.interactive()
            and not os.environ.get(CAPTURE_QUESTION_ASKED_ENV)
        ):
            answered = _confirm_pending_capture(caps_by_source, base_now=base_now, telemetry=tel)
            if answered is None:
                _exit_wizard()
            if answered is tui.BACK:
                # Esc: back to the menu, the Update never started.
                if not looping:
                    raise typer.Exit(0)
                tui.clear()
                picked = _show_main_menu()
                if picked is None or picked is tui.BACK:
                    _exit_wizard()
                chosen_action = picked
                continue
            if any(line.startswith("!") for line in answered):
                # A failure is shown NOW: the hand-off below may exec the newest
                # release, and this process would never reach the result page.
                verdict, problems = _capture_answer(answered)
                tui.page(wizard.result_page(verdict, details=problems), prompt="Press enter to continue the update…")
                answered = []
            pending_capture_lines = answered
        dispatched = _run_chosen_action(
            _agent_target=_agent_target,
            _collect_agent=_collect_agent,
            agent_rules=agent_rules,
            agent_screen_shown=agent_screen_shown,
            agent_sources=agent_sources,
            auto_update=auto_update,
            base_now=base_now,
            capture=capture,
            caps=caps,
            caps_by_source=caps_by_source,
            chosen_action=chosen_action,
            configured=configured,
            folder=folder,
            install_capture_sources=install_capture_sources,
            install_code=install_code,
            install_context=install_context,
            install_needs=install_needs,
            installation_completion=installation_completion,
            menu_default=menu_default,
            menu_recorder=menu_recorder,
            shared_selection=shared_selection,
            tel=tel,
            tracking=tracking,
            uninstall=uninstall,
            yes=yes,
        )
        if dispatched is None:
            return
        lines, run_summary = dispatched

        if chosen_action is actions_mod.Action.CONFIGURE and lines is not None:
            # Every install ends with the Probe service started, as an agent
            # session's hooks start it; its start installs the OS keeper and
            # the lifeboat. A fresh machine had none of the three until its
            # first agent session (plan clean-uninstall-reinstall C5).
            from probe.cli.install import install as install_pipeline

            service_note = install_pipeline.start_service()
            if service_note:
                lines = [*lines, service_note]

        if pending_capture_lines and lines is not None:
            if run_summary:
                # Under the Update's headline, the answer and its errors; not
                # each agent's configure report (`_capture_answer`).
                verdict, problems = _capture_answer(pending_capture_lines)
                lines = [*lines[:1], *verdict, *lines[1:]]
                if problems:
                    if "Details:" in lines:
                        at = lines.index("Details:") + 1
                        lines[at:at] = [f"  {line}" for line in problems]
                    else:
                        lines += ["", "Details:", *(f"  {line}" for line in problems)]
            else:
                lines = [*pending_capture_lines, "", *lines]

        install_code = None
        if chosen_action is actions_mod.Action.IMPORT_RESEARCH:
            # The shared selector and monitor return to the menu even when
            # reached directly with --action import-research.
            looping = True
            action = None
        if chosen_action is actions_mod.Action.SIGN_OUT and lines is not None:
            # None: the confirmation page was answered "stay signed in" --
            # back to the menu, nothing changed.
            if lines:
                tui.final("\n".join(lines))
            raise typer.Exit(0)
        # The install's Defaults step chose Who records: move the agents now
        # that their plugins are in place, before the summary page, so its
        # lines are on that page (Codex O2).
        recorder_lines: list[str] = []
        if (
            guided_install
            and chosen_action is actions_mod.Action.CONFIGURE
            and onboarding_pick.recorder != opened_recorder
        ):
            recorder_lines = _apply_recorder_pick(
                onboarding_pick.recorder,
                sources=tuple(dict.fromkeys((
                    *agent_sources,
                    *(source for source, snapshot in state_caps_by_source.items() if snapshot.configured),
                ))),
                completion=installation_completion,
                base_now=base_now,
                collect=lambda source: _collect_agent(source, fresh=True),
                telemetry=tel,
            )
        wizard.INSTALL_RECORDER_PICK.set(None)
        if guided_install and (saved_default_lines or recorder_lines):
            lines = [*(lines or []), *([""] if lines else []), *saved_default_lines, *recorder_lines]

        # The action's work is done and its result page waits on a person. Only
        # an install changes more after it (this computer's workspace, its
        # imports): every other action lets go of the run lock here (C1).
        if looping and chosen_action is not actions_mod.Action.CONFIGURE:
            _release_for_menu()
        # Inside the menu loop this is a PAGE of the wizard, so it gets the
        # same centred treatment as every prompt. A one-shot `--action` run is
        # command output: printing it plainly leaves the user's scrollback
        # alone, which clearing the screen for a single result would not.
        paged = bool(lines) and looping and wizard.interactive()
        copyable: bool | str = False
        if paged and chosen_action is actions_mod.Action.DIAGNOSE:
            # The verdict and the problems on screen; the whole report on `c`.
            copyable = "\n".join(lines)
            lines = doctor_impl.summary(caps_by_source, recorder=wizard.machine_recorder())
        if paged:
            tui.page(
                lines,
                prompt=(
                    "Press enter to continue…"
                    if guided_install
                    # Signed out (an Uninstall): the wizard ends here, no menu.
                    else "Press enter to finish…"
                    if not resolve(base_url=_conn.base_url).token
                    else "Press enter to return to the menu…"
                ),
                copyable=copyable,
            )
        elif lines:
            tui.final("\n".join(lines))

        # The guided install's OWN completion. `configure_completed` fires once
        # per configure call -- a two-agent install emits two of them and
        # neither says whether the installation as a whole is usable. This
        # fires once, and carries the verdict the dashboard gates on.
        if installation_completion is not None and installation_completion.remaining == 0:
            tel.emit(
                telemetry_mod.EVENT_WIZARD_INSTALL_SETTLED,
                outcome=(
                    telemetry_mod.InstallSettledOutcome.SETTLED
                    if installation_completion.settled
                    else telemetry_mod.InstallSettledOutcome.UNSETTLED
                ),
                agent_count=len(agent_sources),
                guided=bool(guided_install),
                # One event per run names every agent, so #probe-usage can say
                # "added Codex" once instead of a message per agent.
                agents=list(agent_sources),
                was_configured=installation_completion.was_configured,
                # Omitted, not [], when nothing was added: PostHog's `is_set`
                # is the filter a destination writes, and an empty list is set.
                **(
                    {"agents_added": list(installation_completion.added)}
                    if installation_completion.added
                    else {}
                ),
            )
        # This computer's workspace: where every project made on it goes (the CLI,
        # the daemon, SDK runs). After every agent applied and the credential is
        # saved, before the import offer so imports land there too. Asks only on
        # a guided, interactive install; `--yes`, explicit flags and no TTY never
        # guess between several. Fail-open: it never blocks a finished install.
        if (
            chosen_action is actions_mod.Action.CONFIGURE
            and installation_completion is not None
            and installation_completion.remaining == 0
        ):
            from probe.cli.wizard.account import computer_workspace

            for line in computer_workspace.choose(
                asking=wizard.interactive() and not yes and not explicit_flags
            ):
                tui.say(line)

        # Offer imports only after every selected agent has finished setup.
        # Failed or canceled installs never reach this point; scripted installs
        # skip the offer. Back leaves the completed install in place.
        imports: set[wizard.BackfillChoice] = set()
        if guided_install:
            picked_imports = _select_and_run_imports(
                caps=caps,
                base_now=base_now,
                folder=folder,
                selected_agents=agent_sources,
                telemetry=tel,
                agent_screen_shown=agent_screen_shown,
                progress_header=lambda fraction: wizard.install_header(
                    wizard.STEP_IMPORTS,
                    agent_screen_shown=agent_screen_shown,
                    fraction=fraction,
                ),
            )
            if picked_imports is tui.BACK:
                looping = True
                action = None
                paged = True
            else:
                imports = picked_imports
        if imports:
            looping = True
            action = None
            paged = True  # The import flow already handled its own pages.

        if (
            guided_install
            and picked_imports is not tui.BACK
            and installation_completion is not None
            and installation_completion.settled
            and installation_completion.remaining == 0
        ):
            from probe.cli.imports.jobs import ui as import_jobs_ui
            from probe.cli.wizard.account import onboarding_complete

            with tui.onboarding(
                lambda: wizard.install_header(
                    wizard.STEP_IMPORTS,
                    agent_screen_shown=agent_screen_shown,
                    fraction=1.0,
                )
            ):
                try:
                    completion = onboarding_complete.show(base_now)
                except KeyboardInterrupt:
                    # Not "back", and not the wizard's Exit either: this is the
                    # last screen of a guided install being walked away from,
                    # which is the drop-off the funnel exists to count.
                    tel.emit(
                        telemetry_mod.EVENT_WIZARD_ONBOARDING_COMPLETED,
                        outcome=telemetry_mod.OnboardingOutcome.ABANDONED,
                        imports_chosen=sorted(str(choice) for choice in imports),
                    )
                    raise
                tel.emit(
                    telemetry_mod.EVENT_WIZARD_ONBOARDING_COMPLETED,
                    outcome=(
                        telemetry_mod.OnboardingOutcome.EXITED
                        if completion == import_jobs_ui.Navigation.EXIT
                        else telemetry_mod.OnboardingOutcome.DASHBOARD_OPENED
                        if completion
                        else telemetry_mod.OnboardingOutcome.RETURNED_TO_MENU
                    ),
                    imports_chosen=sorted(str(choice) for choice in imports),
                )
                if completion:
                    # Approved imports keep running after this UI closes.
                    raise typer.Exit(0)
            looping = True
            action = None
            paged = True

        if not looping:
            raise typer.Exit(0)

        # Re-read state: the action just changed it, and the next choice should
        # be made against what is true now, not what was true on entry.
        # `lines is None` is an action saying NOTHING happened -- a pure
        # back-out. The pause exists so streamed output (configure's progress
        # screen) is not wiped by the menu redraw; stopping a back-out on an
        # empty page to press Enter reads as landing on a broken screen.
        if not paged and lines is not None and wizard.interactive():
            tui.page(
                [actions_mod.ACTION_COPY[chosen_action][0], "", "Finished."],
                prompt="Press enter to return to the menu…",
            )
        # Re-read state ONLY when the action could have changed it. A pure
        # back-out (`lines is None`) changed nothing, and re-collecting costs
        # ~a second per agent -- which turned `‹ Back` into a visible stall
        # between the screen closing and the menu coming back.
        if lines is not None:
            state_sources = tuple(dict.fromkeys((*state_sources, *agent_sources)))
            # Diagnose only READS, so the server's answer still stands.
            if chosen_action is not actions_mod.Action.DIAGNOSE:
                device_state = _ask_server()
            with tui.working("Checking what's installed on this device"):
                state_caps_by_source = {source: _collect_agent(source) for source in state_sources}
        tui.clear()
        picked = _show_main_menu()
        if picked is None or picked is tui.BACK:
            _exit_wizard()
        chosen_action = picked


def _opens_onboarding(snapshots: dict, available_sources) -> bool:
    """A device with no Probe on it, which a bare launch takes straight into the
    guided install: no saved credential, no coding agent set up, and at least
    one coding agent here for the install to act on."""
    return (
        bool(available_sources)
        and not resolve(base_url=_conn.base_url).token
        and not any(snapshot.configured for snapshot in snapshots.values())
    )
from probe.cli.commands.machine.wizard import wizard  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.snapshots.snapshots import snapshot  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _conn  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.account.device_prompt import _show_device_prompt  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.account.website_onboarding import _finish_website_onboarding  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.actions.capabilities import CAPTURE_QUESTION_ASKED_ENV, _capture_answer, _confirm_pending_capture  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.actions.defaults import _apply_recorder_pick, _save_session_default  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.actions.uninstall import _run_uninstall  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.session.device_actions import _run_chosen_action  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.session.import_offer import _select_and_run_imports  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.session.install import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _InstallationCompletion,
    _install_grants_held,
    _probe_already_installed,
    _shared_selection,
)
from probe.cli.wizard.session.run_lock import _hold_for_action, _release_for_menu  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.session.start import _begin_wizard_session  # noqa: E402 -- pieces need each other; the front door loads this one first
