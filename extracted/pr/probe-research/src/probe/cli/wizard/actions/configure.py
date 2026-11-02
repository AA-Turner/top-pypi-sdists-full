"""agent/src/probe/cli/main.py."""

from __future__ import annotations
import time

import typer
from ....sdk.settings.settings import (
    load_context,
    resolve)
from ....sdk.settings.device import OnboardingRequired
from ....shared.harness import plugins as plugin_cli


def _run_configure_action(
    *,
    agent_rules,
    authorization_context,
    authorization_needs,
    auto_update,
    base_now,
    caps,
    capture,
    capture_sources,
    configured,
    install_code,
    installation_completion,
    progress_header,
    selection_override,
    tel,
    tracking,
    uninstall,
    yes,
):
    """`_run_wizard_action`'s configure path: what to install, then `_run_configure_steps`."""
    import time

    from probe.cli.wizard import doctor as doctor_impl
    from probe.cli import wizard as wizard
    from probe import analytics as telemetry_mod
    from probe.core import events as json_events
    from probe.cli.wizard.state.state import Capability
    from probe.cli.capture.capture import OffMode
    from probe.core.events import Step

    # CONFIGURE. NON-INTERACTIVE, always: the install steps are asked ONCE by
    # `wizard()`, before the per-agent apply loop, and arrive here as
    # `selection_override`. This used to ask them itself -- which meant a
    # two-agent run asked them once per agent, and, worse, that Back could only
    # unwind to the caller (which read it as "quit") because the screen before
    # this one belonged to a different function.
    configure_t0 = time.monotonic()

    def register_configure(current, *, complete=True):
        settings = resolve(base_url=base_now)
        if installation_completion is not None:
            return installation_completion.register(current, settings=settings, complete=complete)
        return _register_local_capabilities(current, settings=settings, complete=complete)

    selection = selection_override or wizard.resolve_selection(
        caps,
        tracking=tracking,
        capture=capture,
        auto_update=auto_update,
        agent_rules=agent_rules,
        configured=configured,
    )
    # pi used to be forced capture-only here. Its three stated reasons -- "no
    # marketplace plugin, no MCP server, no global-instructions file this run
    # could install" -- are no longer true: the packages entry installs the
    # extension, skills AND the MCP manifest together (pi_config), and
    # agent_rules.memory_path() has resolved pi's own ~/.pi/agent/AGENTS.md
    # since #1089. pi reads that file (its --no-context-files flag exists to
    # turn exactly this off), so the tracking block reaches the model.
    #
    # The force was also self-reinforcing: TRACKING is what requests the `mcp`
    # grant, that grant is what writes `mcp_token`, and `mcp_token` is what the
    # extension's own bearer fast path (src/mcpAuth.ts) reads. Refusing
    # tracking guaranteed the token was never minted, so every pi user fell
    # through to /probe-mcp-login's interactive OAuth -- the "Known limitation"
    # the README documents. The limitation WAS this branch.

    # Installed means usable (plan clean-uninstall-reinstall R-T5): the retired
    # tap or both recorders' plugins side by side, a disabled plugin or one
    # whose files are gone, pi's filtered-out extension and Kimi's missing
    # files are put right BEFORE the plan reads what is installed -- they read
    # installed, and "Nothing to change" hid them. A configure is an install
    # start too: the OS keeper may come back (R1).
    from probe.cli.install import install as install_pipeline
    from probe.cli.install.integrations import integrations as integration_repair

    install_pipeline.clear_keeper_off()
    repaired: list[str] = []
    from probe.shared.harness import plugins as plugin_cli

    codex_hooks_before = (integration_repair.codex_hooks_digest()
                          if caps.agent_source == plugin_cli.CODEX else None)
    if (selection.tracking or selection.capture) and (
            integration_repair.unusable_plugins(caps.agent_source) or integration_repair.leftovers(caps.agent_source)):
        fixed = integration_repair.repair(caps.agent_source)
        repaired = [*fixed.lines, *(f"! {problem}" for problem in fixed.problems)]
        with doctor_impl.device_state_scope(_old_way_unless_answered(_start_device_state())):
            caps = doctor_impl.collect()

    steps = wizard.plan(caps, selection)
    mcp_token_drifted = selection.tracking and wizard.mcp_token_drifted()
    # Codex skips Probe's hooks until they are approved, and says nothing: a
    # machine set up before the wizard approved them, or after an update that
    # changed an entry, reads "already set up" here while recording nothing.
    # Asked only on a Codex run, where Probe's plugins are in Codex
    # (`codex_hooks_waiting`); a Claude run never does Codex's work.
    codex_hooks_waiting = (
        caps.agent_source == plugin_cli.CODEX
        and caps.codex_available
        and (selection.tracking or selection.capture)
        and wizard.codex_hooks_waiting()
    )
    needs = (
        authorization_needs
        if authorization_needs is not None
        else _needs_for_this_run(wizard.needs_authorization(caps, selection), yes=yes)
    )
    if (
        not steps
        and not authorization_needs
        # `--json`: a grant the plan has no row for -- the MCP's read token
        # alone; `tracking_on` does not read it -- is still work, because the
        # program reading the run shows its approval link (`device_prompt`).
        and not (needs and json_events.enabled())
        and not mcp_token_drifted
        and not codex_hooks_waiting
        and not (
            selection.capture
            and not selection.keeps(Capability.CAPTURE)
            and caps.legacy_capture_plugin_installed
        )
    ):
        tel.emit(
            telemetry_mod.EVENT_WIZARD_CONFIGURE_STARTED,
            plan_steps=0,
            needs_authorization=False,
            already_configured=configured,
        )
        tel.emit(
            telemetry_mod.EVENT_WIZARD_CONFIGURE_COMPLETED,
            outcome=telemetry_mod.ConfigureOutcome.SUCCESS,
            no_changes=True,
            duration_seconds=int(time.monotonic() - configure_t0),
        )
        _record_configure(caps.agent_source, selection, caps, ok=True)
        registered = list(register_configure(caps))
        _record_install(
            caps.agent_source, ok=True, summary="already set up",
            notes=[message for message in registered if wizard.needs_attention(message)],
        )
        hooks_line = ([integration_repair.CODEX_HOOKS_LINE] if codex_hooks_before is not None
                      and integration_repair.codex_hooks_digest() != codex_hooks_before else [])
        if repaired:
            return [*repaired, "Set up the way you asked once those were put right.", *hooks_line, *registered]
        return ["Already set up the way you asked. Nothing to change.", *hooks_line, *registered]

    # From here it STREAMS, through a Progress screen that redraws on every
    # state change. Installing a plugin shells out to `claude` and a browser
    # approval prints a URL you are meant to act on while it waits, so this
    # page cannot be buffered -- it is written while it happens. It used to
    # collect every message and print them only after all four steps returned,
    # which showed a blank screen for as long as the subprocesses took.
    # The single retry BUDGET for this run. install_plugin() calls it to ask
    # whether it may try again; the first caller to fail spends it. Per-plugin
    # retries would multiply refreshes by the number of failures, which is how
    # a fix for a 3-minute wait turns into a 30-minute one.
    _retry_budget = [1]

    def _may_retry() -> bool:
        if _retry_budget[0] <= 0:
            return False
        _retry_budget[0] -= 1
        return True

    # THE WORK LIST, built before anything renders. Deliberately NOT `steps`
    # from plan(): the two stopped being 1:1 the moment plan() learned to say
    # "sign in" for a machine whose plugin is already installed. Indexing one
    # by the other's position left the bar pinned at 0/2 while the run did its
    # real work in the authorization phase, which no step covered.
    #
    # The install decision reads the PLUGIN fact, not the composite capability.
    # `caps.tracking_on` is "plugin installed AND logged in", and `capture_on`
    # does not look at the plugin at all -- so a machine with both plugins
    # present but no credential yet read as "both off" and reinstalled both.
    # Measured: `claude plugin install` on an already-installed plugin returns
    # "already installed" and does NOT upgrade it, so that work was pure waste
    # -- and it was the step that failed, on the one path a new user is on.
    tel.emit(
        telemetry_mod.EVENT_WIZARD_CONFIGURE_STARTED,
        # None for a kept capability: it was read, not asked for (`preserve`).
        tracking=None if selection.keeps(Capability.TRACKING) else selection.tracking,
        capture=None if selection.keeps(Capability.CAPTURE) else selection.capture,
        auto_update=selection.auto_update,
        agent_rules=selection.agent_rules,
        plan_steps=len(steps),
        needs_authorization=bool(needs),
        already_configured=configured,
    )
    # (label, action, gate). `gate` names the capability whose credential this step
    # cannot work without, and is None for steps that need none -- removals,
    # auto-update, the CLAUDE.md block. It is what stops a run whose browser
    # approval failed from installing a plugin that then sits there unauthenticated:
    # the tracking plugin publishes an MCP server, and an unauthenticated connect is
    # answered with a `WWW-Authenticate` challenge that pins Claude Code to OAuth.
    # Turning a capability OFF is deliberately ungated -- refusing to uninstall
    # because a credential could not be minted would trap someone on a plugin they
    # just asked to remove.
    # The fourth field is the step's stable name for `--json` (`json_events.Step`).
    work: list[tuple[str, object, object, Step]] = []

    # Whether the selected agent's own CLI is on this machine. A plugin install
    # shells out to it, so without it the step can only fail — and on the
    # degraded install path the confirm screen has already SAID the plugins
    # are skipped, so failing at them anyway would contradict the screen. The
    # honest step is a skip that names the recovery.
    if caps.agent_source == "pi":
        # pi has no marketplace CLI a plugin-install step could shell out to
        # (see wizard.INSTALLABLE_AGENT_SOURCES) -- there is no "is it on
        # this machine" question to ask here, because nothing below ever
        # attempts a plugin install for pi (apply_capture()/install_plugin()
        # refuse it themselves; see their own pi guards). True rather than
        # False specifically so a pi run never shows the "Skipped ... —
        # Claude Code is not on this machine" message, which used to fire
        # here (via the old ternary's silent claude_code default) for a run
        # that was never about Claude Code at all.
        agent_here = True
        agent_name = wizard.agent_label(caps.agent_source)
    elif caps.agent_source == plugin_cli.KIMI:
        # Kimi Code's plugins are files the wizard writes (kimi_config); it
        # still needs the agent itself on the machine to be worth installing.
        from probe.shared.harness.harnesses.kimi_code import config as kimi_config

        agent_here = kimi_config.binary_available()
        agent_name = wizard.agent_label(caps.agent_source)
    else:
        agent_here = caps.codex_available if caps.agent_source == "codex" else caps.claude_available
        agent_name = "Codex" if caps.agent_source == "codex" else "Claude Code"

    def _skip_plugin(what: str):
        return lambda: [
            f"Skipped {what} — {agent_name} is not on this machine. "
            "After installing it, run `probe wizard` and pick “Install Probe”."
        ]

    # `preserve` (Settings, Update's capture question): the booleans for a
    # capability the caller is not changing are only a read, so they install
    # and remove nothing (`Selection.preserve`).
    if selection.keeps(Capability.TRACKING):
        pass
    elif selection.tracking and not caps.tracking_plugin_installed:
        if agent_here:
            work.append(
                (
                    "install the CLI + MCP plugin",
                    lambda: wizard.apply_tracking(True, on_retry=_may_retry),
                    Capability.TRACKING,
                    Step.TRACKING_PLUGIN,
                )
            )
        else:
            work.append(
                ("skip the CLI + MCP plugin", _skip_plugin("the CLI + MCP plugin"), None, Step.TRACKING_PLUGIN)
            )
    elif not selection.tracking and not caps.tracking_plugin_installed:
        # The plugin is already gone -- removed with `/plugin uninstall` rather
        # than here -- but its skills are copies in the agent's OWN folder, and
        # with no plugin left no session-start hook runs to prune them. Without
        # this they sit there unrefreshed forever: the `POINTER_VERSION` failure,
        # reachable by one command. Silent when there is nothing to remove.
        work.append((
            "remove Probe's skills",
            lambda: wizard.remove_root_skills(caps.agent_source),
            None,
            Step.REMOVE_SKILLS,
        ))
    elif not selection.tracking and caps.tracking_plugin_installed:
        work.append((
            "remove the CLI + MCP plugin",
            # pi keeps its one package while capture stays selected.
            lambda: wizard.apply_tracking(False, keep_capture=selection.capture or selection.keeps(Capability.CAPTURE)),
            None,
            Step.TRACKING_PLUGIN,
        ))

    if (
        selection.tracking
        and not selection.keeps(Capability.TRACKING)
        and caps.agent_source == "codex"
        and agent_here
        and caps.mcp_authenticated is not True
        # The daemon profile's plugin carries no MCP to log in to.
        and not wizard.daemon_records(caps.agent_source)
    ):
        # `agent_here` gates this like the installs: `codex mcp login` shells
        # out to the absent binary, and a failed step right after a screen
        # that said the coding-agent work is skipped contradicts the screen.
        work.append(
            (
                "authenticate the Codex MCP",
                wizard.apply_codex_mcp_auth,
                Capability.TRACKING,
                Step.CODEX_MCP_LOGIN,
            )
        )
    elif mcp_token_drifted:
        # THE REPAIR NEEDS ITS OWN SIGNAL, because every other gate on this
        # screen closes in exactly the state that needs repairing:
        #
        #   * needs_authorization() reads `mcp` as held whenever a read token
        #     is saved, stale or not, so a signed-in device never re-enters
        #     authorize() and never reaches the sync inside it.
        #   * the branch above wants `mcp_authenticated is not True`, but
        #     `codex mcp list` answers `bearer_token` for a DEAD header, so
        #     this reads as authenticated precisely when it is not.
        #   * and it wants agent_source == "codex", which a machine running
        #     both agents does not report.
        #
        # `probe doctor` tells people to run this command; before this branch
        # existed the command did nothing for them, which is the doctor/wizard
        # circle this repo has paid for before (see `plan()`'s AGENT_RULES
        # comment). The drift check is two file reads and self-guarding, so it
        # is cheap to ask on every run and a no-op on a healthy machine.
        work.append(
            (
                "re-point your agents' Probe MCP at your current read token",
                wizard.sync_mcp_token,
                Capability.TRACKING,
                Step.MCP_TOKEN_SYNC,
            )
        )

    if selection.keeps(Capability.CAPTURE):
        pass
    elif selection.capture and not agent_here and not caps.capture_plugin_installed:
        work.append(
            ("skip the Session capture plugin", _skip_plugin("the Session capture plugin"), None, Step.CAPTURE)
        )
    elif selection.capture and (
        not caps.capture_plugin_installed
        or not caps.capture_on
        or caps.legacy_capture_plugin_installed
    ):
        # NOT gated on "plugin absent": the killswitch is cleared here too, and
        # a killswitched machine with the plugin already installed needs that
        # clear or capture stays off while the run reports success.
        # apply_capture skips the install itself when the plugin is present, so
        # this cannot reintroduce the reinstall.
        if caps.agent_source not in wizard.INSTALLABLE_AGENT_SOURCES:
            # pi: capture_plugin_installed is always False here (see
            # capabilities.installed_plugins()'s pi guard), which would
            # otherwise pick "install the Session capture plugin" below --
            # a label starting with "install" is exactly what the
            # marketplace-refresh trigger a few lines down keys on, and
            # apply_capture() itself now refuses any actual plugin install
            # for pi (see its own guard). The work IS real -- clear the
            # killswitch, let the token authorize() already minted take
            # effect -- it is just never a plugin install for pi.
            capture_label = "pair Session capture"
        elif not caps.capture_plugin_installed:
            capture_label = "install the Session capture plugin"
        elif caps.legacy_capture_plugin_installed:
            capture_label = "retire the legacy Session capture plugin"
        else:
            capture_label = "re-enable Session capture"
        work.append(
            (
                capture_label,
                lambda: wizard.apply_capture(caps, True, mode=OffMode.DISABLE, on_retry=_may_retry),
                Capability.CAPTURE,
                Step.CAPTURE,
            )
        )
    elif not selection.capture and (caps.capture_plugin_installed or caps.capture_on):
        work.append(
            (
                "turn Session capture off",
                lambda: wizard.apply_capture(
                    caps,
                    False,
                    mode=OffMode.UNINSTALL if uninstall else OffMode.DISABLE,
                ),
                None,
                Step.CAPTURE,
            )
        )

    # After every Codex plugin install above: Codex runs none of a plugin's hooks
    # until they are approved, so an install that stops at the plugin records
    # nothing. Probe approves its own (`approve_codex_hooks`).
    codex_installs = (
        caps.agent_source == plugin_cli.CODEX
        and agent_here
        and (selection.tracking or selection.capture)
        # An install or a re-enable carries its capability; a removal or "turn
        # capture off" carries None and must not approve what it switched off.
        and any(item[3] in (Step.TRACKING_PLUGIN, Step.CAPTURE) and item[2] is not None for item in work)
    )
    #: Whether that step left no Probe hook waiting: the closing "`/hooks` ›
    #: approve" line is only for a Codex where it did not.
    codex_hooks_done: list[bool] = []

    def _get_approve_codex_hooks() -> list[str]:
        lines, done = wizard.approve_codex_hooks(only=wizard.codex_plugins_kept_on(selection))
        codex_hooks_done.append(done)
        return lines

    if agent_here and (codex_hooks_waiting or codex_installs):
        work.append(("approve Probe's hooks in Codex", _get_approve_codex_hooks, None, Step.CODEX_HOOKS_TRUST))

    if selection.auto_update != caps.auto_update_enabled:
        work.append(
            (
                f"{'enable' if selection.auto_update else 'disable'} automatic updates",
                lambda: wizard.apply_auto_update(selection.auto_update),
                None,
                Step.AUTO_UPDATE,
            )
        )
    if (
        selection.agent_rules != caps.agent_rules_installed
        or caps.agent_rules_stale
        or (not selection.agent_rules and wizard.leftover_team_note(caps))
    ):
        work.append(
            (
                f"write the rules into your global {wizard.instruction_files(caps.agent_source)}",
                lambda: wizard.apply_agent_rules(
                    selection.agent_rules, stale=caps.agent_rules_stale
                ),
                None,
                Step.AGENT_RULES,
            )
        )
    elif selection.agent_rules and wizard.statusline_catch_up_due(caps.agent_source):
        # Rules already current, so the step above (which writes the status
        # line) does not run: Kimi Code's footer shipped after them.
        work.append((
            f"add Probe's state to {wizard.agent_label(caps.agent_source)}'s status line",
            lambda: wizard.catch_up_statusline(caps.agent_source),
            None,
            Step.STATUSLINE,
        ))

    #: Why the refresh failed, when it did (`_refresh`, `_run_step`).
    refresh_failure: list[str] = []

    # The refresh is hoisted out of install_plugin (it used to run per plugin,
    # discarding both results), so the CALLER owns it now -- and owning it means
    # actually doing it. Without this the first attempt installs from whatever
    # stale copy is on disk, which is the failure the original comment warned
    # about, and a machine that never added the marketplace fails attempt one
    # every time and is only repaired by the retry.
    #
    # Prepended, not appended: it has to happen BEFORE any install. And only
    # when something is actually being installed -- it is two `claude`
    # subprocesses, and the common re-run installs nothing.
    def _refresh() -> list[str]:
        """Adapts refresh_marketplace's Result to the message list a step returns.

        A failed refresh is REPORTED, not swallowed -- discarding it is what
        made the original bug present as Claude's downstream "not found in
        marketplace". It does not abort the run: the install can still succeed
        from the copy already on disk, and if it does not, the retry gets
        another go at the refresh.
        """
        result = wizard.refresh_marketplace()
        if result is not None and not getattr(result, "ok", True):
            from probe.cli.install import updater

            # Scrubbed like every other child output we print, and a Mac that
            # cannot run git gets its one-line fix, not Apple's paragraph.
            reason = updater.git_blocker(result.detail) or updater.clean_reason(result.detail)
            refresh_failure.append(reason)
            return [f"! could not refresh the marketplace: {reason}"]
        return []

    if any(label.startswith("install") for label, action, _, _ in work if action is not None):
        work.insert(0, (REFRESH_STEP_LABEL, _refresh, None, Step.REFRESH_MARKETPLACE))

    return _run_configure_steps(
        authorization_context=authorization_context,
        base_now=base_now,
        caps=caps,
        capture_sources=capture_sources,
        codex_hooks_before=codex_hooks_before,
        codex_hooks_done=codex_hooks_done,
        configure_t0=configure_t0,
        install_code=install_code,
        installation_completion=installation_completion,
        needs=needs,
        progress_header=progress_header,
        refresh_failure=refresh_failure,
        register_configure=register_configure,
        repaired=repaired,
        selection=selection,
        tel=tel,
        work=work,
    )


def _run_configure_steps(
    *,
    authorization_context,
    base_now,
    caps,
    capture_sources,
    codex_hooks_before,
    codex_hooks_done,
    configure_t0,
    install_code,
    installation_completion,
    needs,
    progress_header,
    refresh_failure,
    register_configure,
    repaired,
    selection,
    tel,
    work,
):
    """The configure path's steps, sign-in included, and its summary lines."""
    import time

    from probe.cli.wizard import state as capabilities
    from probe.cli.wizard import doctor as doctor_impl
    from probe.cli.install.integrations import integrations as integration_repair
    from probe.cli import wizard as wizard
    from probe import analytics as telemetry_mod
    from probe.core import events as json_events
    from probe.cli.wizard import terminal as tui
    from probe.cli.wizard.state.state import Capability
    from probe.core.events import Step

    # The browser approval is REAL WORK and the longest wait in the run -- it
    # blocks on a human in a browser. Leaving it off the list is what made a
    # sign-in-only run sit at 0/2 with nothing moving.
    #
    # It goes FIRST, ahead of the marketplace refresh and both installs. The
    # tracking plugin ships an `.mcp.json` pointing at the hosted MCP, and the
    # credential it serves is the one this step mints -- so installing before
    # signing in publishes a server that provably cannot authenticate, for as
    # long as a human takes to approve it in a browser. Claude Code answering a
    # connect in that window gets a 401 carrying a `WWW-Authenticate` challenge,
    # discovers an authorization server from it, and pins the server to OAuth:
    # the user then has to go to `/mcp` and authenticate a device this very run
    # had already authorized. Credential first, and the window does not exist.
    auth_index = 0 if needs else None
    if needs:
        work.insert(0, (f"sign in ({', '.join(needs)})", None, None, Step.SIGN_IN))

    tui.clear()
    install_run = wizard.current_install_run()
    progress = tui.Progress(
        "This run will:",
        [label for label, *_ in work],
        overall=progress_header,
        run=install_run.for_agent(caps.agent_source) if install_run is not None else None,
    )
    if install_run is not None:
        install_run.watch(progress.render)
    progress.render()

    skipped: list[str] = []

    def _run_step(index: int, label: str, fn, name: Step) -> list[str]:
        """Run one apply step, unless the phase has already run out of time.

        The budget refuses to START work; it never interrupts a step already in
        flight. A `claude plugin install` killed mid-write is how a plugin cache
        gets corrupted, so a slow step is allowed to finish on its own timeout.
        """
        agent = caps.agent_source
        if time.monotonic() > deadline:
            skipped.append(label)
            json_events.step(
                name, json_events.Status.SKIPPED,
                f"stopped after {wizard.PHASE_BUDGET_S:.0f}s without starting: {label}", agent=agent,
            )
            return []
        progress.start(index)
        json_events.step(name, json_events.Status.STARTED, label, agent=agent)
        try:
            out = list(fn())
        except Exception as exc:  # noqa: BLE001 - one bad step must not eat the rest
            progress.finish(index, ok=False)
            progress.note(f"! {label}: {exc}")
            if name is Step.REFRESH_MARKETPLACE:
                json_events.step(name, json_events.Status.DONE, _get_used_copy_on_disk(str(exc)), agent=agent)
            else:
                json_events.step(name, json_events.Status.FAILED, f"{label}: {exc}", agent=agent)
            return []
        # A step reports failure in prose, not by raising: the apply_* helpers
        # return "could not install ..." strings. The classifier lives next to
        # the producers in setup.py so a reworded message cannot leave the tick
        # mark disagreeing with the line printed underneath it.
        ok = not any(wizard.reports_failure(m) for m in out)
        progress.finish(index, ok=ok)
        if out:
            progress.note(*out)
        if name is Step.REFRESH_MARKETPLACE and not ok and refresh_failure:
            json_events.step(name, json_events.Status.DONE, _get_used_copy_on_disk(refresh_failure[-1]), agent=agent)
            return out
        json_events.step(
            name,
            # A "skip ..." step is the one that reports why it could not run.
            json_events.Status.SKIPPED if label.startswith("skip ")
            else json_events.Status.DONE if ok else json_events.Status.FAILED,
            "\n".join(out) or label,
            agent=agent,
        )
        return out

    def _get_used_copy_on_disk(reason: str) -> str:
        """A failed refresh, as its `--json` step: DONE, because the run goes on
        and installs from the marketplace copy already on disk. Marking it failed
        cleared `complete`, so the desktop app showed a failed install for one that
        works. The failure text is kept; when the copy on disk cannot serve the
        install, the install's own step fails and clears `complete` instead."""
        return f"used the copy already on this machine (refresh failed: {reason})"

    granted: dict = {}
    if needs:
        # Snapshot BEFORE the mint: the always-browser install re-mints on a
        # signed-in device, and the token being replaced has to be read while
        # it is still the stored one — after `authorize` persists, it is gone
        # locally and can only be revoked from this copy.
        from probe.sdk.settings.settings import load_context

        try:
            previous_context = load_context() or {}
        except Exception:  # noqa: BLE001 - an unreadable config just skips the revoke
            previous_context = {}
        progress.start(auth_index)
        json_events.step(Step.SIGN_IN, json_events.Status.STARTED, work[auth_index][0])
        progress.note(
            "",
            "Signing in with the website code…"
            if install_code
            else f"One browser approval covers everything listed ({', '.join(needs)}).",
        )
        try:
            granted, auth_messages = wizard.authorize(
                needs,
                base_url=base_now,
                capture_sources=capture_sources,
                client_context=authorization_context,
                on_prompt=lambda prompt: progress.note(
                    f"  visit: {prompt.verification_uri_complete}",
                    f"  code:  {prompt.user_code}",
                ),
                open_browser=True,
                **({"install_code": install_code} if install_code is not None else {}),
            )
        except OnboardingRequired as exc:
            json_events.step(Step.SIGN_IN, json_events.Status.FAILED, str(exc))
            _finish_website_onboarding(exc)
        signed_in_ok = not [g for g in needs if g not in granted]
        progress.finish(auth_index, ok=signed_in_ok)
        if auth_messages:
            progress.note(*auth_messages)
        json_events.step(
            Step.SIGN_IN,
            json_events.Status.DONE if signed_in_ok else json_events.Status.FAILED,
            "\n".join(auth_messages) or work[auth_index][0],
        )
        if install_code is not None and not signed_in_ok:
            raise typer.Exit(1)
        revoked = wizard.revoke_replaced_token(previous_context, granted, base_url=base_now)
        if revoked:
            progress.note(*revoked)
        if install_code is not None and signed_in_ok:
            # THE OTHER HALF of the account-switch gate at the top of `wizard`.
            # That gate could only name the account being replaced — a website
            # code is opaque until it is redeemed — so this is the first point
            # at which the account it selected can be stated at all, and a
            # guided install otherwise finished without ever saying whose data
            # it is now writing. A courtesy, never load-bearing: the credential
            # is already saved, so an endpoint that goes unreachable one call
            # after the exchange costs a line of output and nothing else (the
            # same rule `sign_in` applies to its own version of this line).
            switched_to = wizard.account_email(base_now)
            if switched_to:
                progress.note(f"Signed in as {switched_to}.")
        tel.emit(
            telemetry_mod.EVENT_WIZARD_SIGNED_IN,
            outcome=(
                telemetry_mod.SignInOutcome.SUCCESS
                if signed_in_ok
                else telemetry_mod.SignInOutcome.FAILED
            ),
            grants_needed=len(needs),
        )

    # Started AFTER the approval, not before it. The budget bounds the work this
    # process does; the browser approval is a human deciding, and clocking it
    # against the same 300s would let a slow reader consume the entire budget and
    # leave every install "stopped without starting" -- a run that signed in and
    # installed nothing.
    deadline = time.monotonic() + wizard.PHASE_BUDGET_S

    ungranted: list[str] = []

    for position, (label, action, gate, step_name) in enumerate(work):
        if action is None:
            continue  # the authorization step, run above
        # The gate. Installing a plugin whose credential this run tried and failed
        # to mint is how a cancelled browser approval still leaves an `.mcp.json`
        # on disk with nothing behind it -- and an unauthenticated connect is
        # answered with a `WWW-Authenticate` challenge, which pins Claude Code to
        # OAuth. The user is then sent to `/mcp` to authenticate a device that was
        # never authorized at all. Refusing the install leaves the machine in the
        # state it was already in, which is the honest outcome of a refused
        # approval, and `probe wizard` re-run is the repair.
        blocked = (
            wizard.blocked_by_missing_grants(gate, needed=needs, granted=granted)
            if gate is not None
            else []
        )
        if step_name is Step.REFRESH_MARKETPLACE and not any(
            not (
                other_gate is not None
                and wizard.blocked_by_missing_grants(other_gate, needed=needs, granted=granted)
            )
            for other_label, other_action, other_gate, _ in work
            if other_action is not None and other_label.startswith("install")
        ):
            # Every install it is for was refused a credential: adding the
            # marketplace (which writes the agent's own config, every agent's
            # in a batch) would change a machine whose approval was refused.
            progress.finish(position, ok=False)
            json_events.step(
                step_name, json_events.Status.SKIPPED,
                f"skipped {label} — nothing to install without a credential.", agent=caps.agent_source,
            )
            continue
        if blocked:
            ungranted.append(label)
            progress.finish(position, ok=False)
            progress.note(f"! skipped {label} — no credential for {', '.join(blocked)}.")
            json_events.step(
                step_name, json_events.Status.SKIPPED,
                f"skipped {label} — no credential for {', '.join(blocked)}.", agent=caps.agent_source,
            )
            continue
        if step_name is Step.REFRESH_MARKETPLACE:
            # A batch (several agents) installs their plugins with the refresh:
            # only those whose credential this run's sign-in got.
            wizard.allow_batch_installs(
                capability
                for capability in (Capability.TRACKING, Capability.CAPTURE)
                if not wizard.blocked_by_missing_grants(capability, needed=needs, granted=granted)
            )
        started = time.monotonic()
        _run_step(position, label, action, step_name)
        if step_name is Step.REFRESH_MARKETPLACE:
            # The network's time (git, bounded on its own) and, in a batch,
            # every agent's: not this agent's budget for its own steps.
            deadline += time.monotonic() - started

    if skipped:
        progress.note(
            f"! stopped after {wizard.PHASE_BUDGET_S:.0f}s without starting: "
            f"{', '.join(skipped)}. Re-run `probe wizard` to finish."
        )

    # A coding agent set up for the FIRST time (neither of its own plugins was
    # here) joins the device's Who records: where the others record through the
    # daemon, it starts there too (Richard 2026-10-06). Only with tracking AND
    # capture chosen (the daemon records from capture), only after a clean run,
    # and never a browser (`follow_machine_recorder` needs the daemon set up).
    first_setup = not caps.tracking_plugin_installed and not caps.capture_plugin_installed
    if first_setup and selection.tracking and selection.capture and not skipped and not ungranted:
        # A snapshot only when the agent moves: it rarely does, and taking one
        # costs a call to the server.
        joined = wizard.follow_machine_recorder(
            caps.agent_source, doctor_impl.collect, base_url=base_now, rules=selection.agent_rules
        )
        if joined:
            progress.note(*joined)

    # THE VERDICT. Verify the postcondition rather than trusting the install
    # command: on the run that prompted this fix both installs reported failure
    # while both plugins were in fact present, so believing the exit status
    # would have cried wolf. `plugins.missing()` answers only when it actually
    # managed to look -- an absent `claude` is normal on a GPU pod and must
    # never be reported as a failed install.
    # ONE re-collect, reused. In the wizard collect() reads the agent's plugin
    # record (`capabilities.plugin_records`), the file its `plugin list` reads.
    # Its server half from one fresh `POST /v1/device-state`; when that does
    # not answer, collect() asks the old way (`/v1/me` and the capture key's
    # status), so a refused key is still reported.
    server = _old_way_unless_answered(_start_device_state())

    def _wanted(snapshot) -> list[str]:
        names = []
        if selection.tracking and not selection.keeps(Capability.TRACKING) and not snapshot.tracking_plugin_installed:
            names.append(capabilities.tracking_plugin_name(caps.agent_source))
        if selection.capture and not selection.keeps(Capability.CAPTURE) and not snapshot.capture_plugin_installed:
            names.append(capabilities.TAP_PLUGIN_NAME)
        return names

    with doctor_impl.device_state_scope(server):
        after = doctor_impl.collect()
        if _wanted(after) and after.plugins_verified:
            # The record says a plugin is absent: ask the agent's own CLI
            # before calling the install failed (a wrapper that points the
            # agent at another config folder, a release that moves the file).
            # A CLI that cannot answer leaves the record's answer standing.
            with capabilities.plugin_records(False):
                listed = doctor_impl.collect()
            if listed.plugins_verified:
                after = listed
    wanted_plugins = _wanted(after)
    # Only names we VERIFIED absent. An unanswerable question is not a negative
    # answer: `claude` missing is normal on a GPU pod and must never read as a
    # failed install.
    absent = wanted_plugins if after.plugins_verified else []

    missing = [grant for grant in needs if grant not in granted]
    runtime_failures: list[str] = []
    # A kept capability was not this run's to fix, so it cannot fail it either.
    capture_asked = selection.capture and not selection.keeps(Capability.CAPTURE)
    tracking_asked = selection.tracking and not selection.keeps(Capability.TRACKING)
    if capture_asked and after.capture_credential_valid is False:
        runtime_failures.append("the capture credential is rejected")
    if capture_asked and after.legacy_capture_plugin_installed:
        runtime_failures.append("the legacy Codex capture plugin is still installed")
    if tracking_asked and after.agent_source == "codex" and after.mcp_authenticated is False:
        runtime_failures.append("the Codex MCP is not logged in")
    # Identity first (plan clean-uninstall-reinstall R-T4): a daemon key of
    # another account is replaced, and a credential variable that disagrees
    # with the sign-in leaves the install unfinished, the variable named.
    from probe.cli.install import identity_check

    runtime_failures.extend(identity_check.reconcile_once().problems)

    if missing or absent or runtime_failures:
        # "Restart Claude Code to finish" after a FAILED run reads as success:
        # the user restarts, finds the capability off, and has no idea why.
        reasons = []
        if absent:
            # A gated skip is not a failed install, and saying so sends the user
            # to debug `claude plugin install` when the actual fault was the
            # approval they cancelled two steps earlier. The credential is named
            # separately below; this clause only has to stop claiming an attempt
            # that never happened.
            verb = "were not installed" if ungranted else "did not install"
            reasons.append(f"these plugins {verb}: {', '.join(absent)}")
        if missing:
            reasons.append(f"no credential for: {', '.join(missing)}")
        reasons.extend(runtime_failures)
        tel.emit(
            telemetry_mod.EVENT_WIZARD_CONFIGURE_COMPLETED,
            outcome=telemetry_mod.ConfigureOutcome.FAILED,
            failure_kind=(
                telemetry_mod.ConfigureFailureKind.MISSING_GRANTS
                if missing
                else telemetry_mod.ConfigureFailureKind.PLUGINS_ABSENT
                if absent
                else telemetry_mod.ConfigureFailureKind.RUNTIME
            ),
            steps_skipped=len(skipped),
            duration_seconds=int(time.monotonic() - configure_t0),
        )
        progress.note(
            "", f"Not finished — {'; '.join(reasons)}.", "Re-run `probe wizard` to retry."
        )
        if absent:
            json_events.step(
                Step.VERIFY_PLUGINS, json_events.Status.FAILED,
                f"these plugins are not installed: {', '.join(absent)}", agent=caps.agent_source,
            )
        _record_configure(
            caps.agent_source, selection, after, ok=False, message=f"Not finished — {'; '.join(reasons)}."
        )
        progress.close()
        if _record_install(
            caps.agent_source, ok=False,
            # The screen's own lines already say "Not finished — ..." and
            # how to retry.
            notes=_problems(progress) or [f"not finished: {'; '.join(reasons)}."],
        ):
            # The run stops here: its summary is the screen it leaves.
            tui.page(wizard.current_run_summary().lines())
        # complete=False: this run did NOT finish, and the dashboard treats a
        # fresh registration as the install completing. Reporting the observed
        # state here made a failed install advance onboarding to the next step
        # and flip the approval page to Installed.
        for message in register_configure(after, complete=False):
            tui.say(message)
        raise typer.Exit(1)

    unverified = (
        f"Could not confirm the plugins are installed ({wizard.agent_label(caps.agent_source)} did not answer). "
        "Run `probe doctor` to check."
    )
    if wanted_plugins and not after.plugins_verified:
        # Could not ask. Say so rather than claiming either outcome.
        progress.note("", unverified)
        json_events.step(
            Step.VERIFY_PLUGINS, json_events.Status.SKIPPED, unverified, agent=caps.agent_source
        )
    elif selection.tracking or selection.capture:
        json_events.step(Step.VERIFY_PLUGINS, json_events.Status.DONE, agent=caps.agent_source)
    _record_configure(
        caps.agent_source, selection, after, ok=True,
        message=unverified if wanted_plugins and not after.plugins_verified else "",
    )
    tracking_newly_installed = bool(
        selection.tracking and not caps.tracking_plugin_installed and after.tracking_plugin_installed
    )
    capture_newly_installed = bool(
        selection.capture and not caps.capture_plugin_installed and after.capture_plugin_installed
    )
    if installation_completion is not None and (tracking_newly_installed or capture_newly_installed):
        installation_completion.added.append(caps.agent_source)
    tel.emit(
        telemetry_mod.EVENT_WIZARD_CONFIGURE_COMPLETED,
        outcome=(
            telemetry_mod.ConfigureOutcome.UNVERIFIABLE
            if wanted_plugins and not after.plugins_verified
            else telemetry_mod.ConfigureOutcome.SUCCESS
        ),
        tracking_newly_installed=tracking_newly_installed,
        tracking_already_present=bool(selection.tracking and caps.tracking_plugin_installed),
        capture_newly_installed=capture_newly_installed,
        capture_already_present=bool(selection.capture and caps.capture_plugin_installed),
        steps_skipped=len(skipped),
        duration_seconds=int(time.monotonic() - configure_t0),
    )
    codex_hooks_approved = bool(codex_hooks_done) and all(codex_hooks_done)
    notice = list(wizard.restart_notice(caps, selection, codex_hooks_approved=codex_hooks_approved))
    if (not codex_hooks_approved and codex_hooks_before is not None
            and integration_repair.codex_hooks_digest() != codex_hooks_before
            and not any("/hooks" in line for line in notice)):
        # Probe's hook entries changed (a plugin installed, updated or put
        # back) and this run did not approve them: Codex runs none of them
        # until a person approves them again.
        notice.append(integration_repair.CODEX_HOOKS_LINE)
    progress.note_next(*notice)
    progress.close()
    for line in repaired:
        tui.say(line)
    registered = list(register_configure(
        after,
        complete=not skipped and not (wanted_plugins and not after.plugins_verified),
    ))
    for message in registered:
        tui.say(message)
    unconfirmed = bool(wanted_plugins and not after.plugins_verified)
    # A step that failed (the rules, auto-update), one never started (the time
    # budget) or plugins nobody could confirm: not installed the way asked.
    # A refresh that failed while the install worked from the copy on disk
    # (`_get_used_copy_on_disk`) is a warning under Details, not an unfinished install.
    failed = [step for step in getattr(progress, "failed_steps", list)() if step != REFRESH_STEP_LABEL]
    finished = not skipped and not unconfirmed and not failed
    restart, must = wizard.install_next(caps, selection, codex_hooks_approved=codex_hooks_approved)
    _record_install(
        caps.agent_source,
        ok=finished,
        notes=[
            *_problems(progress),
            *([unverified] if unconfirmed else []),
            *(message for message in registered if wizard.needs_attention(message)),
        ],
        restart=restart,
        must=must,
    )

    return []
from probe.cli.commands.machine.wizard import wizard  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.snapshots.snapshots import snapshot  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.account.website_onboarding import _finish_website_onboarding  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.actions.actions import REFRESH_STEP_LABEL, _old_way_unless_answered, _problems  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.actions.result_rows import _record_configure, _record_install  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.session.install import _needs_for_this_run, _register_local_capabilities  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.session.session import _start_device_state  # noqa: E402 -- pieces need each other; the front door loads this one first
