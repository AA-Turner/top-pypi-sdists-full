"""probe sync: deliver runs recorded with PROBE_MODE=offline."""

from __future__ import annotations
from pathlib import Path
from typing import Optional

import typer

from .... import errors
from probe.cli.cli import app


@app.command("sync")
def sync_offline(
    directory: Optional[Path] = typer.Argument(
        None,
        help="an offline run's folder, or a folder of them (e.g. copied off an "
        "air-gapped node); default: this machine's offline outbox",
    ),
    list_only: bool = typer.Option(False, "--list", help="show offline runs and their state; send nothing"),
    project: Optional[str] = typer.Option(
        None,
        "--project",
        help="file the run in this project instead of the recorded one (a run whose "
        "folder is named, or whose create was refused)",
    ),
    experiment: Optional[str] = typer.Option(
        None,
        "--experiment",
        help="file the run in this experiment instead of the recorded one (same scope as --project)",
    ),
    on_conflict: Optional[str] = typer.Option(
        None,
        "--on-conflict",
        help="`supersede`: deliver a run whose external_id another run already has as "
        "<id>-rN, a retry linked to it (same scope as --project); `error` refuses",
    ),
    allow_mismatch: bool = typer.Option(
        False,
        "--allow-mismatch",
        help="deliver a run whose folder you name even though it was recorded against "
        "another server URL, or (team unknown) under another login context",
    ),
) -> None:
    """Deliver runs recorded with PROBE_MODE=offline (plan 2.12), with the current login.

    Each run is created on the server (safe to repeat: a run synced twice, or
    from two copies of its folder, is one run), then every write it recorded,
    then its close. Looks in the outbox's `offline/` and in every torchrun/SLURM
    rank's `rank-*/offline/`. Exit 0 when everything found is synced, 2 when
    something is not, 1 when no offline run was found at all. Every write is one
    request (a 1M-step run is ~1M POSTs): the outbox's coalesced drain does not
    merge an offline run's writes yet."""
    from ....sdk.delivery import offline

    root = directory if directory is not None else (Path(_conn.spool_dir) if _conn.spool_dir else None)
    dirs = offline.find_offline_dirs(root)
    if not dirs:
        # Loud, never an empty success: a run recorded under a rank's outbox,
        # another $HOME or another machine looks exactly like "nothing to do".
        if list_only:
            _print_json([])
        places = ", ".join(str(p) for p in offline.search_places(root))
        typer.echo(
            f"probe sync: no offline runs found (looked in {places}). A run recorded "
            "on another machine or under another outbox syncs from a copy of its "
            "folder: `probe sync <dir>` (or --spool-dir / PROBE_OUTBOX_DIR).",
            err=True,
        )
        raise typer.Exit(1)
    if list_only:
        described = [offline.describe(d) for d in dirs]
        _print_json(described)
        if any(d["state"] != "synced" for d in described):
            raise typer.Exit(2)
        return
    if on_conflict is not None and on_conflict not in ("error", "supersede"):
        typer.echo("probe sync: --on-conflict takes `error` or `supersede`", err=True)
        raise typer.Exit(2)
    amending = project is not None or experiment is not None or on_conflict is not None
    # The re-filing flags change a run's identity or home, so they apply to
    # EVERY run only when DIR names that one run's folder; in a scan they fix
    # only the runs whose create the server already refused.
    named = directory is not None and len(dirs) == 1 and dirs[0] == Path(directory).expanduser()
    results = []
    with _client() as c:
        try:
            offline.require_server(c)
        except errors.CapabilityUnavailable as exc:
            typer.echo(str(exc), err=True)
            raise typer.Exit(2) from None
        for d in dirs:
            try:
                results.append(
                    offline.sync_dir(
                        d,
                        c,
                        project=project,
                        experiment=experiment,
                        on_conflict=on_conflict,
                        amend_all=named,
                        # Delivering into another server or login is a choice
                        # about ONE run: never granted to a whole scan.
                        allow_mismatch=allow_mismatch and named,
                    )
                )
            except errors.RosError as exc:
                results.append({"dir": str(d), "state": "refused", "clean": False, "errors": [str(exc)]})
    _print_json(results)
    for result in results:
        for message in [*(result.get("warnings") or []), *(result.get("errors") or [])]:
            typer.echo(f"{result.get('key') or result['dir']}: {message}", err=True)
    if allow_mismatch and not named:
        typer.echo(
            "probe sync: --allow-mismatch applies only to a run whose folder you name "
            "(`probe sync <dir> --allow-mismatch`); it changed nothing here.",
            err=True,
        )
    if amending and not any(r.get("amended") for r in results):
        typer.echo(
            "probe sync: --project/--experiment/--on-conflict changed nothing: they apply to "
            "a run whose folder you name (`probe sync <dir>`), or to one whose create the "
            "server refused.",
            err=True,
        )
    if not all(r.get("clean") for r in results):
        raise typer.Exit(2)
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client, _conn  # noqa: E402 -- pieces need each other; the front door loads this one first
