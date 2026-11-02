"""perform ONE wizard action and return its output: dispatch, then CONFIGURE (selection, repair, plan, work list, progress, approval, steps, verify)."""

from __future__ import annotations
from collections.abc import Callable, Sequence
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from probe import analytics as probe_telemetry
    from ....sdk.client.client import Client
else:
    #: The SDK client class: a module global so the CLI package can monkeypatch
    #: it in tests, and None until then. The SDK client imports every wire model,
    #: so a command imports it when it builds one (`_client_class`), not at start.
    Client = None

import typer
from ....sdk.settings.settings import resolve


#: The install screen's marketplace refresh step.
REFRESH_STEP_LABEL = "refresh the plugin marketplace"


def _problems(progress) -> list[str]:
    """`tui.Progress.problems`; a stand-in screen (tests) has none."""
    problems = getattr(progress, "problems", None)
    return list(problems()) if problems is not None else []


def _old_way_unless_answered(resolver):
    """`resolver` (a device-state answer), with an answer that did not come
    (`UNREACHABLE`) read as a server without the call: `doctor.collect()` then
    asks the old way, as it did before the one call existed."""
    from probe.cli.wizard import state as capabilities_mod

    def resolve_state():
        state = resolver()
        if state.outcome is capabilities_mod.DeviceStateOutcome.UNREACHABLE:
            return capabilities_mod.DeviceState(capabilities_mod.DeviceStateOutcome.UNSUPPORTED)
        return state

    return resolve_state


def _run_wizard_action(
    chosen_action,
    *,
    caps,
    base_now: str,
    yes: bool,
    tracking,
    capture,
    auto_update,
    agent_rules,
    uninstall: bool,
    configured: bool,
    folder: str | None = None,
    transcripts: bool | None = None,
    selection_override=None,
    authorization_needs: list[str] | None = None,
    capture_sources: list[str] | None = None,
    authorization_context: dict | None = None,
    progress_header: Callable[[float], Sequence[str]] | None = None,
    selected_agents: tuple[str, ...] | list[str] | None = None,
    caps_by_source: dict | None = None,
    telemetry: "probe_telemetry.TelemetryContext | None" = None,
    install_code: str | None = None,
    installation_completion: _InstallationCompletion | None = None,
    back_to_selection: bool = False,
    default_state: str | None = None,
    recorder: str | None = None,
    update_outcome=None,
) -> list[str] | None:
    """Perform ONE action and RETURN its output.

    Returned, not printed, so the caller can decide whether this is a centred
    page of the wizard or plain command output. An empty list means the action
    already streamed (the configure path has to, because a browser approval
    prints a URL you are meant to read while it waits). None means nothing
    happened at all -- a pure back-out -- so the caller skips even the
    "press enter" pause and goes straight back to the menu.
    """

    from probe.cli.wizard.actions import onboarding as actions_mod
    from probe.cli.wizard import doctor as doctor_impl
    from probe.cli import wizard as wizard
    from probe import analytics as telemetry_mod

    tel = telemetry_mod.null_context() if telemetry is None else telemetry
    from probe.cli.wizard import terminal as tui

    if chosen_action in actions_mod.ACCOUNT_ACTIONS:
        return _run_account_action(
            chosen_action,
            caps=caps,
            base_now=base_now,
            yes=yes,
            sources=tuple(selected_agents or (caps.agent_source,)),
            telemetry=tel,
        )

    if chosen_action is actions_mod.Action.RECORDER:
        lines = _run_recorder_action(
            yes=yes,
            caps_by_source=caps_by_source,
            base_now=base_now,
            chosen=recorder,
            telemetry=tel,
            agent_rules=agent_rules,
        )
        _record_recorder(recorder, caps_by_source or {}, lines)
        return lines

    if chosen_action is actions_mod.Action.DEFAULTS:
        return _run_defaults_action(yes=yes, base_now=base_now, chosen=default_state)

    if chosen_action is actions_mod.Action.SETTINGS:
        return _run_settings_action(
            yes=yes,
            caps_by_source=caps_by_source,
            base_now=base_now,
            telemetry=tel,
        )

    if chosen_action is actions_mod.Action.IMPORT_JOBS:
        from probe.cli.imports import jobs as import_jobs
        from probe.cli.imports.jobs import ui as import_jobs_ui

        if not wizard.interactive():
            return [
                f"{job['label']}: {job['state']} ({job['id']})" for job in import_jobs.list_jobs()
            ]
        if import_jobs_ui.show_imports() is import_jobs_ui.Navigation.EXIT:
            _exit_wizard()
        return None

    if chosen_action is actions_mod.Action.DIAGNOSE:
        lines = doctor_impl.render(caps, codex_hooks=doctor_impl.codex_hook_rows(caps)).splitlines()
        notes = actions_mod.troubleshooting(caps)
        if notes:
            lines += ["", "If something is not working:"]
            lines += [f"  - {note}" for note in notes]
        return lines

    if chosen_action is actions_mod.Action.UPDATE:
        from probe.cli.install.upgrade.upgrade import perform_update, reporting_progress

        # No "Upgrade the CLI now?" gate: picking "Update to the latest
        # version" from the menu IS the answer to that question, and asking it
        # again dropped a bare uncentred prompt into the middle of the wizard.
        # perform_update returns its lines rather than streaming, so without
        # the spinner this sits silent for the whole `uv tool upgrade` +
        # plugin update -- the longest unexplained wait the wizard had. It
        # stays up, a bar and its percentage under it (`_UpdateProgress`),
        # through the recording below too (a server call); in a several-agent
        # Update it is the run's own.
        with tui.working("Updating Probe") as status:
            if update_outcome is not None:
                # Already done with the run's other agents (`_update_agents`).
                outcome = update_outcome
                progress = None
            else:
                progress = _UpdateProgress([caps.agent_source], status)
                with reporting_progress(progress):
                    outcome = perform_update(
                        base_url=base_now, include_plugin=True, trigger=_update_action_trigger(yes)
                    )
            _record_update(caps.agent_source, outcome)
            lines = list(outcome.lines)
            from probe.cli.install.upgrade.upgrade import after_update_line

            closing = after_update_line(outcome, wizard.agent_label(caps.agent_source), caps.agent_source)
            if closing:
                lines += ["", closing]
            # The pointer block lives in the researcher's home directory, so no
            # release can reach it: updating the CLI ships new POINTER_BODY wording
            # that the installed block never picks up, and this action -- the one an
            # upgrading machine actually takes -- used to leave it on whatever
            # version it was first written at. Gated on already-installed-and-stale,
            # so a machine that declined the block stays declined; `want=True` here
            # would install one behind the researcher's back.
            #
            # A process cannot write wording it does not have, so the refresh lands
            # on the first invocation AFTER the upgrade, not this one. It converges;
            # it is not instant.
            if caps.agent_rules_stale:
                lines += wizard.apply_agent_rules(True, stale=True)
            elif caps.agent_rules_installed:
                # Kimi Code's footer shipped after its rules: one catch-up.
                lines += wizard.catch_up_statusline(caps.agent_source)
            # An update cannot have removed anything: what it does not see stays
            # as the server last heard (`client_installation.snapshot`). Its server
            # half from one `POST /v1/device-state` (the old way when that does
            # not answer), not `/v1/me` and the capture key's status in a row.
            with doctor_impl.device_state_scope(_old_way_unless_answered(_start_device_state())):
                snapshot = doctor_impl.collect()
            lines += _register_local_capabilities(
                snapshot,
                settings=resolve(base_url=base_now),
                reports_removals=False,
            )
            if progress is not None:
                progress.recorded(caps.agent_source)
                progress.sent()  # registered above, directly
        run_summary = wizard.current_run_summary()
        if run_summary is not None:
            run_summary.subtitle = outcome.cli
            run_summary.note(*outcome.run_notes)
            if outcome.deferred:
                # Nothing ran: every agent "not updated", the reason once.
                run_summary.note(*outcome.lines)
            run_summary.must_do(*outcome.run_actions)
            run_summary.record(
                caps.agent_source,
                # Its own plugins: a CLI or pi package failure is the run's,
                # named once under Details, not this agent's.
                ok=not outcome.deferred and not outcome.problems and (outcome.ok or bool(outcome.run_notes)),
                summary=outcome.summary,
                notes=[
                    *outcome.problems,
                    # What the rules refresh and the registration said went wrong.
                    *(line for line in lines[len(outcome.lines):] if wizard.needs_attention(line)),
                ],
                restart=outcome.restart_needed,
                must=outcome.actions,
            )
        return lines

    if chosen_action is actions_mod.Action.MANUAL:
        return [
            *actions_mod.manual_steps(
                base_url=base_now,
                agent_source=selected_agents or caps.agent_source,
            ).splitlines(),
            "",
            *actions_mod.self_host_notes(
                base_url=base_now, mcp_endpoint="https://mcp.research.prbe.ai/mcp"
            ).splitlines(),
        ]

    if chosen_action is actions_mod.Action.UNINSTALL:
        # `probe wizard --action uninstall --agent A`: Probe out of that agent
        # only (its plugins, hooks and rules). No key is revoked and the CLI
        # stays; without `--agent` the wizard runs `probe uninstall` instead.
        if not yes and wizard.interactive():
            tui.clear()
            if wizard.confirm_agent_removal(caps.agent_source) is not True:
                # None, not []: nothing happened. The caller reads that as a
                # pure back-out -- no "press enter" on an empty page, no state
                # re-read -- and, since this action now ends by signing the
                # device out, it is also what keeps a declined removal from
                # clearing the credentials anyway.
                return None
        # The credential this registration authenticates with stays: a
        # per-agent removal signs nobody out.
        settings_before_removal = resolve(base_url=base_now)
        lines = list(wizard.remove_everything(caps))
        removed = doctor_impl.collect()
        lines += _register_local_capabilities(
            removed,
            settings=settings_before_removal,
        )
        _record_removal(caps.agent_source, removed, lines)
        run_summary = wizard.current_run_summary()
        if run_summary is not None:
            problems = wizard.attention_lines(lines)
            run_summary.record(caps.agent_source, ok=not problems, notes=problems)
        return lines

    if chosen_action is actions_mod.Action.IMPORT_RESEARCH:
        if yes or not wizard.interactive():
            raise typer.BadParameter(
                "import-research needs an interactive selection. "
                "Use --action backfill or --action transcripts for a direct import."
            )
        sources = tuple(selected_agents or (caps.agent_source,))
        _select_and_run_imports(
            caps=caps,
            base_now=base_now,
            folder=folder,
            selected_agents=sources,
            telemetry=tel,
        )
        return None  # The monitor already handled returning to the main menu.

    if chosen_action is actions_mod.Action.TRANSCRIPTS:
        # Retained for --action transcripts; the menu uses the shared selector.
        return _import_past_sessions(
            interactive=wizard.interactive(),
            background=wizard.interactive(),
        )

    if chosen_action is actions_mod.Action.BACKFILL:
        from pathlib import Path

        from probe.cli.imports import folder as backfill_impl

        return backfill_impl.run(
            client_factory=_backfill_client,
            start=Path.cwd(),
            folder=Path(folder) if folder else None,
            interactive=wizard.interactive(),
            background=wizard.interactive(),
            back_to_selection=back_to_selection,
            telemetry=tel,
            # The direct --action backfill path IS `probe backfill`, and the
            # two doors must offer the same thing: without this the command
            # offered the conversations at their gate and the menu silently did
            # not. Interactive-only for the same reason the command is -- the
            # lane's own gate is where consent happens.
            # Onboarding already asked about sessions independently of the
            # folder. Standalone folder imports still offer their own gate.
            transcripts=wizard.interactive() if transcripts is None else transcripts,
        )

    return _run_configure_action(
        agent_rules=agent_rules,
        authorization_context=authorization_context,
        authorization_needs=authorization_needs,
        auto_update=auto_update,
        base_now=base_now,
        caps=caps,
        capture=capture,
        capture_sources=capture_sources,
        configured=configured,
        install_code=install_code,
        installation_completion=installation_completion,
        progress_header=progress_header,
        selection_override=selection_override,
        tel=tel,
        tracking=tracking,
        uninstall=uninstall,
        yes=yes,
    )
from probe.cli.commands.machine.wizard import wizard  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.snapshots.snapshots import snapshot  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _backfill_client  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.actions.account import _run_account_action  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.actions.configure import _run_configure_action  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.actions.defaults import _run_defaults_action  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.actions.recorder import _run_recorder_action  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.actions.result_rows import _record_recorder, _record_removal, _record_update  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.actions.settings import _run_settings_action  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.session.import_offer import _import_past_sessions, _select_and_run_imports  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.session.install import _InstallationCompletion, _register_local_capabilities  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.session.session import _exit_wizard, _start_device_state  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.wizard.session.update import _UpdateProgress, _update_action_trigger  # noqa: E402 -- pieces need each other; the front door loads this one first
