"""probe wizard (and the hidden `probe update`/`probe setup` aliases): run the guided wizard here or on the Probe service."""

from __future__ import annotations
import sys
from typing import Optional

import typer
from ....sdk.settings.settings import resolve
from ....sdk import session_marker
from probe.cli.cli import app
from probe.cli.commands.machine.json_command import _JSON_HELP, _JsonCommand
from probe.cli.wizard.agent_flags import _AGENT_HELP, _agent_values, _explicit_agent_sources


# `probe update` is HIDDEN, not deleted. The plugin's SessionStart hook spawns
# it, and plugins update on the USER's schedule -- deleting it would silently
# break auto-update on every machine whose plugin has not been refreshed yet.
# New plugin versions call `probe wizard --action update` instead.
@app.command(name="update", hidden=True)
def update_compat(
    check: bool = typer.Option(False, "--check"),
    yes: bool = typer.Option(False, "--yes", "-y"),
    plugin: bool = typer.Option(True, "--plugin/--no-plugin"),
    channel: str = typer.Option(None, "--channel", hidden=True),  # noqa: ARG001 - ignored
) -> None:
    """Deprecated: use `probe wizard` and pick Update."""
    from probe.cli.wizard.session.run_lock import _wizard_run_lock
    from probe.cli.wizard.session.update import _hand_off_update, _update_action_trigger
    from probe.cli.install import updater
    from probe.cli.install.upgrade.upgrade import perform_update

    base = resolve(base_url=_conn.base_url).base_url
    if check:
        from probe.shared.updates import updates as versions_mod

        try:
            manifest = updater.fetch_latest(base)
        except Exception as exc:  # noqa: BLE001
            print(f"update check failed: {exc}", file=sys.stderr)
            raise typer.Exit(updater.CHECK_ERROR) from exc
        # EVERY component, not just the CLI. This check reported on the CLI alone
        # while the manifest had published `plugin` and `tap` floors for months,
        # so a researcher could run it, read "up to date", and be two months
        # behind on the plugin that does the actual capturing. The exit codes are
        # unchanged -- BEHIND if anything is behind -- because scripts read them.
        rows = versions_mod.compare(manifest)
        for line in versions_mod.render(rows):
            print(line.strip())
        if any(row.behind for row in rows):
            raise typer.Exit(updater.CHECK_BEHIND)
        raise typer.Exit(updater.CHECK_CURRENT)

    from probe.cli.wizard import terminal as tui

    trigger = _update_action_trigger(yes)
    _hand_off_update(trigger, ["update", *(["--yes"] if yes else []), *([] if plugin else ["--no-plugin"])])
    with (
        _wizard_run_lock(command="probe update", update_trigger=trigger),
        tui.working("Updating the CLI and plugins"),
    ):
        outcome = perform_update(base_url=base, include_plugin=plugin, trigger=trigger)
    for line in outcome.lines:
        print(line)
    from probe.cli import wizard as wizard
    from probe.cli.wizard.state.agent_identity import agent_source
    from probe.cli.install.upgrade.upgrade import after_update_line

    source = agent_source()
    closing = after_update_line(outcome, wizard.agent_label(source), source)
    if closing:
        print(f"\n{closing}")
    raise typer.Exit(0 if outcome.ok else 1)


@app.command(name="wizard", cls=_JsonCommand)
def wizard(
    agent: Optional[list[str]] = typer.Option(  # noqa: UP007
        None,
        "--agent",
        help=_AGENT_HELP,
    ),
    tracking: Optional[bool] = typer.Option(  # noqa: UP007 - typer needs Optional
        None,
        "--tracking/--no-tracking",
        help="research tracking skills + read-only MCP search",
    ),
    capture: Optional[bool] = typer.Option(  # noqa: UP007
        None,
        "--capture/--no-capture",
        help="stream the selected coding agents' sessions to the knowledgebase",
    ),
    auto_update: Optional[bool] = typer.Option(  # noqa: UP007
        None, "--auto-update/--no-auto-update", help="keep the CLI and plugins current"
    ),
    agent_rules: Optional[bool] = typer.Option(  # noqa: UP007
        None,
        "--agent-rules/--no-agent-rules",
        help="managed Probe block in each selected agent's global instructions",
    ),
    channel: str = typer.Option(  # noqa: ARG001 - compat, see below
        None,
        "--channel",
        hidden=True,
        help="accepted and ignored; there is only one channel",
    ),
    uninstall: bool = typer.Option(
        False,
        "--uninstall",
        help="when turning capture off, also remove the plugin (default: keep it)",
    ),
    action: Optional[str] = typer.Option(  # noqa: UP007
        None,
        "--action",
        # Every value here is an `Action`, spelled the way the enum spells it.
        # It used to advertise `remove`, which is not one -- so the flag the
        # help text recommended for an unattended uninstall exited 2.
        help=(
            "skip the menu: recorder | defaults | configure | account | login | logout | settings | "
            "uninstall | import-research | backfill | transcripts | imports | update | diagnose | manual"
        ),
    ),
    folder: str = typer.Option(
        None,
        "--folder",
        help="backfill only: the folder to import, skipping the picker (needed headless)",
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="skip the menu and prompts"),
    experimental: bool = typer.Option(
        False,
        "--experimental",
        hidden=True,
        help="no longer needed: Defaults › Who records is on the main menu for every team",
    ),
    token: str = typer.Option(
        None, "--token", help="login: sign in with this token, no browser (a remote or air-gapped machine)"
    ),
    base_url: str = typer.Option(None, "--base-url", help="login: the Probe server to sign in to (self-host)"),
    context: str = typer.Option(
        None, "--context", help="login: the saved account to create or overwrite (default: the active one)"
    ),
    ingest_token: str = typer.Option(None, "--ingest-token", help="login: the capture token to save with it"),
    hmac_secret: str = typer.Option(None, "--hmac-secret", help="login: the self-host HMAC secret to save with it"),
    endpoint_only: bool = typer.Option(
        False, "--endpoint-only", help="login: save --base-url without signing in"
    ),
    no_browser: bool = typer.Option(
        False, "--no-browser", help="login: print the approval link instead of opening a browser"
    ),
    who_records: str = typer.Option(
        None, "--who-records", help="recorder: agent | daemon, for every coding agent on this device"
    ),
    reinstall: bool = typer.Option(False, "--reinstall", help="configure: repair selected integrations, preserving settings"),
    json_output: bool = typer.Option(False, "--json", help=_JSON_HELP),
    auth_code: str = typer.Argument(
        None, help="one-time 10-character sign-in code from the website"
    ),
) -> None:
    """Setup wizard: install and configure Probe Research on this device.

    Interactive by default. Every capability is also a flag, and THE FLAGS ARE
    THE CONTRACT -- the menu is a front end over them. An omitted flag preserves
    whatever is already configured, so `--yes` in CI can never silently revoke
    someone's capture pairing.
    """
    from probe.cli.wizard.actions.uninstall import _run_uninstall
    from probe.cli.wizard.session.run_lock import _wizard_changes_device, _wizard_run_lock
    from probe.cli.wizard.session.session import _wizard_session
    from probe.cli.wizard.session.update import _hand_off_update, _update_action_trigger, _update_argv
    from probe.cli.wizard.actions import onboarding as actions_mod
    from probe.cli.wizard import state as capabilities_mod
    from probe.cli.capture import capture as capture_mod
    from probe.core import events as json_events
    from probe.cli.wizard import terminal as tui

    if action == actions_mod.Action.UNINSTALL and not _agent_values(agent):
        # ONE implementation (`probe uninstall`): never routed to the Probe
        # service, whose own process it stops. With `--agent` it is the wizard's
        # per-agent removal below instead (only those agents' plugins, hooks and
        # rules; no key revoked, the CLI kept), as the setup command documents.
        raise typer.Exit(_run_uninstall(yes=yes is True, json_output=json_output is True))

    adopted = False
    if action == actions_mod.Action.UPDATE:
        # The hand-off first, before the Update reads anything (or is sent to
        # the service): the newest release runs it (`_hand_off_update`).
        from probe.core import adopt

        _hand_off_update(
            _update_action_trigger(yes),
            _update_argv(yes=yes, json_output=json_output is True, agent=agent),
            json_output=json_output is True,
        )
        # This release took the update over and switched the CLI to itself:
        # the rest runs HERE, in its code (the service still runs the old one).
        adopted = adopt.adopted_from() is not None

    # An action the Probe service can run for this terminal runs there, as the
    # desktop app's do (`wizard_service`: which, and when not); its text
    # streams here and its exit status is this command's.
    hosted = None if adopted else _wizard_on_service(
        action=action, yes=yes, json_output=json_output, agent=agent, tracking=tracking, capture=capture,
        auto_update=auto_update, agent_rules=agent_rules, reinstall=reinstall, who_records=who_records,
        folder=folder, uninstall=uninstall, auth_code=auth_code,
        sign_in_flags=any((token, base_url, context, ingest_token, hmac_secret, endpoint_only, no_browser)),
    )
    if hosted is not None:
        raise typer.Exit(hosted)

    # `--json`: stdout carries only events, and the last is `done` however the
    # run ends (`json_events`). A no-op without the flag.
    with json_events.session(json_output is True):
        # `--experimental` gated the Who records rows until 0.204.1; still
        # accepted so a script or a habit that passes it keeps working.
        del experimental

        if reinstall is True:
            sources = _explicit_agent_sources(agent)
            if (action != "configure" or not sources or auth_code is not None
                    or any(value is not None for value in (tracking, capture, auto_update, agent_rules,
                                                          token, base_url, context, ingest_token, hmac_secret,
                                                          who_records, folder))
                    or uninstall or endpoint_only or no_browser):
                raise typer.BadParameter("--reinstall needs --action configure and explicit --agent; leave sign-in and settings flags out")
            from probe.cli.install.integrations.reinstall import run as reinstall_integrations

            with _wizard_run_lock():
                if not reinstall_integrations(sources):
                    raise typer.Exit(1)
            return

        # First, so `--who-records` with a sign-in flag is refused below like any
        # other action rather than signing in and never switching.
        if who_records is not None:
            if who_records not in session_marker.RECORDERS:
                raise typer.BadParameter("--who-records takes agent or daemon")
            if action == "configure" and isinstance(auth_code, str):
                # A dashboard handoff may request the selected mode's credential
                # during Configure; the separate Recorder action still applies it.
                pass
            elif action in (None, "recorder"):
                action = "recorder"
            else:
                raise typer.BadParameter("--who-records goes with --action recorder, or configure with a website sign-in code")

        # SIGN IN ONLY (`--action login` with its flags): nothing is installed or
        # configured, so a GPU box or a self-hosted server gets a login and no
        # plugin, capture or rule it did not ask for (R10). Before the wizard's
        # window, so what it prints stays on the terminal.
        if any((token, base_url, context, ingest_token, hmac_secret, endpoint_only, no_browser)):
            if action not in (None, "login"):
                raise typer.BadParameter(
                    "--token, --base-url, --context, --ingest-token, --hmac-secret, --endpoint-only and "
                    "--no-browser sign in only: use them with --action login"
                )
            # Anything else asked for would be dropped in silence: say so instead.
            dropped = [
                name
                for name, value in (
                    ("--agent", _agent_values(agent) or None),
                    ("--tracking/--no-tracking", tracking),
                    ("--capture/--no-capture", capture),
                    ("--auto-update/--no-auto-update", auto_update),
                    ("--agent-rules/--no-agent-rules", agent_rules),
                    ("--uninstall", uninstall or None),
                    ("--folder", folder),
                    ("a sign-in code", auth_code),
                )
                if value is not None
            ]
            if dropped:
                raise typer.BadParameter(
                    f"these flags only sign in, so {', '.join(dropped)} would be ignored: "
                    "run it separately, without them"
                )
            json_events.begin_result(actions_mod.Action.SIGN_IN.value, [None])
            with _wizard_run_lock():
                # D4: a sign-in from before D3 may have left pi's capture off for good.
                capture_mod.clear_stray_pi_killswitch()
                _login(
                    base_url=base_url,
                    token=token,
                    ingest_token=ingest_token,
                    hmac_secret=hmac_secret,
                    device=not endpoint_only,
                    context=context,
                    open_browser=not no_browser,
                )
            return

        # After the sign-in-only refusals, which name `--agent` as a flag they
        # would drop, and before the run lock: a mistyped agent is a usage
        # error whether or not another run holds the lock.
        _explicit_agent_sources(agent)

        # The wizard's screens draw in a window of their own (`tui.window`): the
        # whole terminal, scrolled by the wizard's keys, and the shell's screen
        # put back untouched on the way out. `--yes` draws no screens.
        with (
            _wizard_run_lock(
                _wizard_changes_device(action, yes=yes, who_records=who_records),
                update_trigger=_update_action_trigger(yes) if action == actions_mod.Action.UPDATE else None,
            ),
            tui.window(enabled=not yes),
            # Every state read in the run reads the agents' plugin records, not
            # their `plugin list`: the wizard checks on entry and after every
            # change, and each listing is a Node start.
            capabilities_mod.plugin_records(),
        ):
            # D4: a sign-in from before D3 may have left pi's capture off for
            # good. Under the lock, so a run turned away changes nothing.
            capture_mod.clear_stray_pi_killswitch()
            _wizard_session(
                agent=agent,
                tracking=tracking,
                capture=capture,
                auto_update=auto_update,
                agent_rules=agent_rules,
                channel=channel,
                uninstall=uninstall,
                action=action,
                folder=folder,
                yes=yes,
                auth_code=auth_code,
                who_records=who_records,
            )


def _wizard_on_service(*, action, yes, json_output, agent, reinstall, **flags) -> int | None:
    """`wizard`'s run on the Probe service (`wizard_service`): its exit status,
    or None to run it here. A flag this cannot read (an agent typo) is the
    in-process path's to report, as it always has."""
    from probe.cli.wizard.session.update import _update_action_trigger
    from probe.cli.wizard.session import on_service as wizard_service

    if json_output is True or yes is not True:
        return None  # the common interactive case: nothing to look up
    try:
        agents = _explicit_agent_sources(agent)
    except typer.BadParameter:
        return None
    trigger = None
    if action == "update":
        try:
            trigger = _update_action_trigger(yes).value
        except Exception:  # noqa: BLE001 -- the service's default (manual) then
            trigger = None
    routed = wizard_service.plan(
        action=action, yes=yes, json_output=json_output, agents=agents, reinstall=reinstall is True,
        update_trigger=trigger, **flags,
    )
    if not isinstance(routed, wizard_service.Routed):
        return None
    return wizard_service.run(routed)
from probe.cli.commands.account.account import _login  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _conn  # noqa: E402 -- pieces need each other; the front door loads this one first
