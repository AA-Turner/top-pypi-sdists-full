"""agent/src/probe/cli/main.py."""

from __future__ import annotations

import contextlib
import dataclasses


def _run_chosen_action(
    *,
    _agent_target,
    _collect_agent,
    agent_rules,
    agent_screen_shown,
    agent_sources,
    auto_update,
    base_now,
    capture,
    caps,
    caps_by_source,
    chosen_action,
    configured,
    folder,
    install_capture_sources,
    install_code,
    install_context,
    install_needs,
    installation_completion,
    menu_default,
    menu_recorder,
    shared_selection,
    tel,
    tracking,
    uninstall,
    yes,
):
    """Run the chosen action once for the device, for one agent, or agent by agent;
    returns (lines, run_summary), or None when a removal was called off."""
    from probe.cli.wizard.actions import onboarding as actions_mod
    from probe.cli import wizard as wizard
    from probe.cli.wizard import terminal as tui

    # The final screen's summary, where the branch below keeps one.
    run_summary = None
    if chosen_action in actions_mod.DEVICE_ACTIONS:
        # ONCE for the device, and unlabelled: the per-agent loop below
        # would run a browser approval per coding agent and file the result
        # under "Claude Code:", which is the wrong shape for a credential
        # -- or a device-wide default -- that belongs to neither.
        lines = _run_wizard_action(
            chosen_action,
            caps=caps,
            base_now=base_now,
            yes=yes,
            tracking=tracking,
            capture=capture,
            auto_update=auto_update,
            agent_rules=agent_rules,
            uninstall=uninstall,
            configured=configured,
            folder=folder,
            selected_agents=agent_sources,
            caps_by_source=caps_by_source,
            telemetry=tel,
            default_state=menu_default,
            recorder=menu_recorder,
        )
    elif len(agent_sources) == 1:
        with (
            _agent_target(agent_sources[0]),
            wizard.install_run(agent_sources)
            if chosen_action is actions_mod.Action.CONFIGURE
            else contextlib.nullcontext(),
            _run_summary(chosen_action, agent_sources) as run_summary,
        ):
            lines = _run_wizard_action(
                chosen_action,
                caps=caps,
                base_now=base_now,
                yes=yes,
                tracking=tracking,
                capture=capture,
                auto_update=auto_update,
                agent_rules=agent_rules,
                uninstall=uninstall,
                configured=configured,
                folder=folder,
                # None unless the install steps above already answered --
                # they own the interactive path now, because they are the
                # only place that can walk BACK through it.
                selection_override=shared_selection,
                authorization_needs=install_needs,
                capture_sources=install_capture_sources,
                authorization_context=install_context,
                progress_header=(
                    wizard.install_apply_header(
                        agent_screen_shown=agent_screen_shown,
                        agent_index=0,
                        agent_count=1,
                        agent_source=agent_sources[0],
                    )
                    if install_context is not None
                    else None
                ),
                install_code=install_code,
                installation_completion=installation_completion,
                telemetry=tel,
            )
            if run_summary and lines is not None and chosen_action is not actions_mod.Action.UNINSTALL:
                lines = run_summary.lines()
    elif chosen_action is actions_mod.Action.CONFIGURE:
        aggregate, resolved = _shared_selection(
            caps_by_source,
            tracking=tracking,
            capture=capture,
            auto_update=auto_update,
            agent_rules=agent_rules,
            configured=configured,
        )
        # The interactive steps ran ABOVE, where Back can still walk them.
        # What is left here is the headless answer.
        # Headless (no install steps answered): an omitted capture flag means
        # "leave it", and for an agent whose capture is a sign-in's pending
        # lock that is "leave it pending" -- per agent, which the shared
        # union read cannot say (`resolve_selection` does it for one agent).
        leave_pending = shared_selection is None and capture is None and configured
        if shared_selection is None:
            shared_selection = resolved
        # Guided installs already checked the saved credentials above.
        shared_needs = (
            install_needs
            if install_needs is not None
            else _needs_for_this_run(
                wizard.needs_authorization(aggregate, shared_selection), yes=yes
            )
        )
        missing_capture_sources = (
            install_capture_sources
            if install_capture_sources is not None
            else [
                source
                for source, snapshot in caps_by_source.items()
                if shared_selection.capture and not snapshot.capture_token_sources
            ]
        )
        lines = []
        install_plan = _install_plan(caps_by_source, shared_selection)
        with (
            _run_summary(chosen_action, agent_sources) as run_summary,
            wizard.marketplace_refreshes(_installing(caps_by_source, shared_selection), install_plan),
            wizard.install_run(
                agent_sources,
                install_plan,
                # What each agent's screen will list, roughly: its plan
                # (none when already set up) and its refresh.
                expected={
                    source: len(wizard.plan(caps_by_source[source], shared_selection))
                    for source in agent_sources
                },
            ) as install_run,
        ):
            for index, source in enumerate(agent_sources):
                # Between two agents' screens: the run's bar stays up.
                with tui.working("Checking what's installed on this device") if index else (
                    contextlib.nullcontext()
                ) as status:
                    if status is not None:
                        status.set(fraction=install_run.fraction())
                    current = _collect_agent(source, fresh=index > 0)
                if install_plan.get(source):
                    # The batch may have installed this agent's plugins with
                    # the first refresh: its own install steps still run,
                    # take those answers and do what they do beside the
                    # install (Claude Code's skills, the killswitch).
                    before = caps_by_source[source]
                    current = dataclasses.replace(
                        current,
                        tracking_plugin_installed=before.tracking_plugin_installed,
                        capture_plugin_installed=before.capture_plugin_installed,
                    )
                # A guided run resolved every selected source together. The
                # first apply raises if approval failed; later agents reuse
                # its result even if their identity lookup is unavailable.
                authorization_needs = shared_needs if index == 0 else None
                if index > 0 and install_needs is not None:
                    authorization_needs = []
                with _agent_target(source):
                    result = _run_wizard_action(
                        chosen_action,
                        caps=current,
                        base_now=base_now,
                        yes=True,
                        tracking=tracking,
                        capture=capture,
                        auto_update=auto_update,
                        agent_rules=agent_rules,
                        uninstall=uninstall,
                        configured=configured,
                        folder=folder,
                        selection_override=(
                            dataclasses.replace(
                                shared_selection,
                                preserve=shared_selection.preserve | {wizard.Capability.CAPTURE},
                            )
                            if leave_pending and current.capture_awaiting_confirmation
                            else shared_selection
                        ),
                        authorization_needs=authorization_needs,
                        capture_sources=missing_capture_sources,
                        authorization_context=install_context,
                        progress_header=(
                            wizard.install_apply_header(
                                agent_screen_shown=agent_screen_shown,
                                agent_index=index,
                                agent_count=len(agent_sources),
                                agent_source=source,
                            )
                            if install_context is not None
                            else None
                        ),
                        install_code=install_code if index == 0 else None,
                        installation_completion=installation_completion,
                        telemetry=tel,
                    )
                # Done, screen or not (already set up opens none).
                install_run.finished(source)
                if result:
                    label = wizard.agent_label(source)
                    lines.extend([f"{label}:", *result, ""])
            if run_summary:
                lines = run_summary.lines()
        # Configure streams its own progress; successful calls return no lines.
    else:
        # Diagnostics/removal are source-local. Manual instructions and
        # backfill are agent-independent, so do not duplicate them.
        targets = (
            agent_sources
            if chosen_action
            in {
                actions_mod.Action.DIAGNOSE,
                actions_mod.Action.UPDATE,
                actions_mod.Action.UNINSTALL,
            }
            else agent_sources[:1]
        )
        action_yes = yes
        if chosen_action is actions_mod.Action.UNINSTALL and not yes and wizard.interactive():
            # `--agent A --agent B`: one question for the agents named.
            tui.clear()
            if wizard.confirm_agent_removal(agent_sources) is not True:
                return
            action_yes = True
        lines = []
        all_backed_out = True
        # ONE update report and ONE capabilities registration for the whole
        # run: each agent's pass would otherwise overwrite the machine's one
        # server row. The last agent (often one with nothing installed) hid
        # the rest, and capabilities flipped absent -> installed between
        # passes, posting a false "Probe removed" on every auto-update.
        from probe.cli.wizard.apply import client_installation
        from probe.shared.updates import update_report

        updating = chosen_action is actions_mod.Action.UPDATE
        if updating:
            # The menu's Update: the hand-off first, as `--action update`
            # does (`_hand_off_update`); the newest release then runs it.
            with tui.working("Looking for the newest Probe"):
                _hand_off_update(
                    _update_action_trigger(action_yes),
                    # The agents this Update was going to update, named.
                    _update_argv(yes=action_yes, agent=list(targets)),
                    before_exec=tui.leave_window,
                )
        together = updating and len(targets) > 1
        # ONE spinner and bar for the whole Update, outside the merged
        # registration and report: they are sent to the server as their
        # block closes, and the bar reaches 100% once they have been.
        with (
            _run_summary(chosen_action, targets) as run_summary,
            tui.working("Updating Probe") if together else contextlib.nullcontext() as status,
        ):
            update_progress = _UpdateProgress(targets, status) if together else None
            with (
                update_report.merged_run() if updating else contextlib.nullcontext(),
                client_installation.merged_registration()
                if updating
                else contextlib.nullcontext([]) as registration_warnings,
            ):
                # Several agents' updates at once: the CLI and pi's package once,
                # each agent's own plugins on a thread of its own.
                updated = (
                    _update_agents(targets, base_now=base_now, yes=action_yes, progress=update_progress)
                    if together
                    else {}
                )
                for index, source in enumerate(targets):
                    # Uninstall revokes each agent's capture key as it goes, and
                    # the next agent's answer can change under it (the server
                    # state it reads moves). Diagnose and update change nothing
                    # the server reports.
                    # Diagnose's snapshot is the one just taken from the agents'
                    # own CLIs (above); it changes nothing to read again.
                    current = (
                        caps_by_source[source]
                        if chosen_action is actions_mod.Action.DIAGNOSE
                        else _collect_agent(source)
                    )
                    with _agent_target(source):
                        result = _run_wizard_action(
                            chosen_action,
                            caps=current,
                            base_now=base_now,
                            yes=action_yes,
                            tracking=tracking,
                            capture=capture,
                            auto_update=auto_update,
                            agent_rules=agent_rules,
                            uninstall=uninstall,
                            configured=configured,
                            folder=folder,
                            selected_agents=agent_sources,
                            telemetry=tel,
                            update_outcome=updated.get(source),
                        )
                    if update_progress is not None:
                        update_progress.recorded(source)
                    if result is not None:
                        all_backed_out = False
                    if result:
                        label = wizard.agent_label(source)
                        lines.extend([f"{label}:", *result, ""])
            if update_progress is not None:
                update_progress.sent()
        lines.extend(registration_warnings)
        if run_summary:
            run_summary.note(*registration_warnings)
            if chosen_action is not actions_mod.Action.UNINSTALL:
                # Uninstall's is drawn after the device's own removal below.
                lines = run_summary.lines()
        # Every target said "nothing happened" (today: only backfill's
        # folder/agent back-outs) -- carry the signal through so the menu
        # comes back without the pause or the state re-read.
        if all_backed_out:
            lines = None
    return lines, run_summary
from probe.cli.commands.machine.wizard import wizard  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.snapshots.snapshots import snapshot  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.actions.actions import _run_wizard_action  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.actions.result_rows import _run_summary  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.session.install import _install_plan, _installing, _needs_for_this_run, _shared_selection  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.session.update import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _UpdateProgress,
    _hand_off_update,
    _update_action_trigger,
    _update_agents,
    _update_argv,
)
