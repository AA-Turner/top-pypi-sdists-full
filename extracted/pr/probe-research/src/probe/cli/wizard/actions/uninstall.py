"""the Uninstall action: the one uninstall (cli/install/uninstall) inside a --json event session."""

from __future__ import annotations

import typer


def _run_uninstall(
    *, yes: bool, force: bool = False, offline: bool = False, discard_unsent: bool = False,
    backup_unsent: bool = False, json_output: bool = False
) -> int:
    """The one uninstall (`probe.cli.install.uninstall`), in a `--json` event session
    when asked. Returns its exit code (when the finisher did not take over)."""
    from probe.core import events as json_events
    from probe.cli import wizard as wizard
    from probe.cli.install import uninstall

    options = uninstall.Options(
        yes=yes, force=force, offline=offline, discard_unsent=discard_unsent, backup_unsent=backup_unsent,
        json=json_output,
        interactive=not yes and not json_output and wizard.interactive(),
    )
    if json_events.enabled():  # inside a run that is already writing events
        return uninstall.run(options)
    with json_events.session(json_output):
        if discard_unsent and backup_unsent:  # inside the session: a `--json` reader gets `error` + `done`
            raise typer.BadParameter("--discard-unsent and --backup-unsent cannot be used together: pick one")
        code = uninstall.run(options)
        if code:
            raise typer.Exit(code)
    return code
from probe.cli.commands.machine.wizard import wizard  # noqa: E402 -- pieces need each other; the front door loads this one first
