"""probe group create/list/get/set: an experiment's run groups (sweeps, ensembles)."""

from __future__ import annotations

import typer
from ....sdk.reads.notes_cap import GROUP_NOTES_REMOVED


# -- run groups (sweeps / ensembles) ----------------------------------------
group_app = typer.Typer(
    no_args_is_help=True, help="run groups: sweeps, ensembles, distributed runs"
)


@group_app.command("create")
def group_create(
    experiment_id: str = typer.Argument(...),
    name: str = typer.Option(..., "--name"),
    kind: str = typer.Option("group", "--kind", help="e.g. sweep, ensemble"),
    spec: str = typer.Option(
        None, "--spec", metavar="JSON|@file", help="e.g. a sweep search space"
    ),
    # HIDDEN AND IGNORED: sweep groups no longer carry notes. Kept so an agent on
    # an older skill still creates its group; it is told once, on stderr.
    notes: str = typer.Option(None, "--notes", hidden=True),
) -> None:
    """Create a run group. Pass the printed id to `probe run start --group`.

    What the sweep tests goes in the experiment's notes, never in `--name`: the
    name is part of the group's uniqueness key within the experiment, so a
    description appended to it mints a SECOND group rather than annotating the
    one it describes.
    """
    if notes is not None:
        _warn_notes_ignored("--notes", GROUP_NOTES_REMOVED)
    with _client() as c:
        result = c.create_group(experiment_id, name, kind=kind, spec=_json_value(spec))
    _print_json(result)


@group_app.command("list")
def group_list(experiment_id: str = typer.Argument(...)) -> None:
    """List an experiment's run groups."""
    with _client() as c:
        _print_json(c.list_groups(experiment_id))


@group_app.command("get")
def group_get(group_id: str = typer.Argument(...)) -> None:
    """Print one run group."""
    with _client() as c:
        _print_json(c.get_group(group_id))


@group_app.command("set")
def group_set(
    group_id: str = typer.Argument(...),
    name: str = typer.Option(None, "--name"),
    spec: str = typer.Option(None, "--spec", metavar="JSON|@file"),
    # HIDDEN AND REFUSED: sweep groups no longer carry notes. Refused rather than
    # ignored, because a `set` whose only job was the note would otherwise exit 0
    # having written nothing.
    notes: str = typer.Option(None, "--notes", hidden=True),
) -> None:
    """Update a run group's name and/or spec.

    The spec says what was varied; what it tested and what came of it goes in
    the experiment's notes.
    """
    if notes is not None:
        typer.echo(f"error: --notes was removed: {GROUP_NOTES_REMOVED}", err=True)
        raise typer.Exit(1)
    if name is None and spec is None:
        raise typer.BadParameter("pass at least one of --name/--spec")
    with _client() as c:
        result = c.update_group(group_id, name=name, spec=_json_value(spec))
    _print_json(result)
from probe.cli.commands.flag_values import _json_value, _warn_notes_ignored  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
