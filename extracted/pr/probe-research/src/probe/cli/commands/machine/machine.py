"""probe install / repair / uninstall: each a --json event session that always ends with a `done` line."""

from __future__ import annotations
from typing import Optional

import typer
from probe.cli.cli import app
from probe.cli.commands.machine.json_command import _JSON_HELP, _JsonCommand
from probe.cli.wizard.agent_flags import _AGENT_HELP


@app.command(name="uninstall", cls=_JsonCommand)
def uninstall_cmd(
    yes: bool = typer.Option(
        False, "--yes", "-y", help="ask nothing: what would need an answer stops the run (exit 2) instead"
    ),
    force: bool = typer.Option(
        False, "--force", help="go on although Probe is still in use here: stop every live user of it first"
    ),
    offline: bool = typer.Option(
        False, "--offline", help="this computer only: revoke its keys in the dashboard yourself afterwards"
    ),
    discard_unsent: bool = typer.Option(
        False, "--discard-unsent", help="delete research that could not be sent, instead of stopping"
    ),
    backup_unsent: bool = typer.Option(
        False, "--backup-unsent",
        help="save research that could not be sent to ~/probe-unsent-<date>.tar.gz, then go on, instead of stopping",
    ),
    json_output: bool = typer.Option(False, "--json", help=_JSON_HELP),
) -> None:
    """Remove Probe from this computer and leave nothing of it behind (= `probe wizard --action uninstall`).

    Stops every Probe process, sends what is still queued, retires this
    computer and revokes its keys on the server, takes Probe out of every
    coding agent, deletes Probe's files and finally the CLI itself. Killed
    anywhere, running it again finishes the job. Exit 0 done, 2 refused
    (nothing changed), 1 partly done (run it again). With `--json`, the
    `result` event's `reason` says why a run stopped, as data.
    """
    from probe.cli.wizard.actions.uninstall import _run_uninstall
    raise typer.Exit(
        _run_uninstall(yes=yes, force=force, offline=offline, discard_unsent=discard_unsent is True,
                       backup_unsent=backup_unsent is True, json_output=json_output is True)
    )


@app.command(name="install", cls=_JsonCommand)
def install(
    agent: Optional[list[str]] = typer.Option(  # noqa: UP007
        None,
        "--agent",
        help=_AGENT_HELP,
    ),
    tracking: Optional[bool] = typer.Option(  # noqa: UP007
        None, "--tracking/--no-tracking", help="research tracking skills + read-only MCP search"
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
    yes: bool = typer.Option(False, "--yes", "-y", help="skip the prompts"),
    json_output: bool = typer.Option(False, "--json", help=_JSON_HELP),
    auth_code: str = typer.Argument(
        None, help="one-time 10-character sign-in code from the website"
    ),
) -> None:
    """Set Probe Research up on this device — straight into the guided install.

    `probe wizard` opens on the action menu, which is right when you do not know
    what you want yet and wrong when you do. `npx probe-research install` is the
    sentence someone types when they have already decided, and the launcher
    forwards its arguments verbatim -- so the verb has to exist HERE or it
    reaches typer as an unknown command and exits 2.

    Deliberately a thin alias over `wizard --action configure` rather than its
    own copy of the flow. The install steps, the shared authorization and the
    per-agent apply loop are subtle enough that a second entry point into a
    second implementation is how the two drift.
    """
    wizard(
        agent=agent,
        tracking=tracking,
        capture=capture,
        auto_update=auto_update,
        agent_rules=agent_rules,
        channel=None,
        uninstall=False,
        action="configure",
        folder=None,
        yes=yes,
        experimental=False,
        # Called as a function, so every option is named: an omitted one is a
        # truthy `typer.Option` default, not None.
        token=None,
        base_url=None,
        context=None,
        ingest_token=None,
        hmac_secret=None,
        endpoint_only=False,
        no_browser=False,
        who_records=None,
        auth_code=auth_code,
        json_output=json_output is True,
    )


@app.command(name="repair", cls=_JsonCommand)
def repair(
    json_output: bool = typer.Option(False, "--json", help=_JSON_HELP),
) -> None:
    """Check this machine's Probe and fix what is broken: the CLI, the keeper, the service, the credentials, the agents' plugins.

    The install pipeline in repair mode: a broken CLI env is rebuilt beside
    the running one and switched to, the `probe` command and the OS keeper
    are put back, the daemon key is held to the signed-in account, and each
    coding agent's plugins are made usable. Ends COMPLETE (exit 0) or
    INCOMPLETE with the reasons (exit 1); refused while an uninstall runs
    (exit 2). When `probe` itself will not run: `npx probe-research repair`.
    """
    from probe.cli.install import repair as repair_impl

    repair_impl.run(json_output=json_output is True)
from probe.cli.commands.machine.wizard import wizard  # noqa: E402 -- pieces need each other; the front door loads this one first
