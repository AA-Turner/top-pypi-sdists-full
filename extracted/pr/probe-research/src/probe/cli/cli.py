"""the `probe` command's Typer app; cli/main.py mounts every command group on it."""

from __future__ import annotations

import typer

from probe.cli.commands.commands import register_group


# -- app --------------------------------------------------------------------
app = typer.Typer(
    name="probe",
    no_args_is_help=True,
    add_completion=False,
    help=(
        "Probe Research CLI. Run/event/artifact commands upload experiments; "
        "the `hook` group is reserved for deterministic coding-agent adapters."
    ),
)

#: `probe --help` order of the root commands: the groups' pieces register them.
ROOT_GROUP = register_group(
    app,
    (
        "login", "logout", "whoami", "backfill", "update", "doctor", "status", "uninstall",
        "install", "repair", "wizard", "setup", "provenance", "approvals", "deny", "ask", "docs",
        "commits", "exec", "log", "coordinates", "link", "snapshot", "snapshot-prune-refs",
        "snapshot-show", "snapshot-restore", "flush", "sync", "get", "bundle", "events",
    ),
)
