"""probe views ...: saved expression views over a run's series."""

from __future__ import annotations
import json
import sys
from pathlib import Path

import typer

from .... import errors
from probe.cli.commands.refs import run_ref


views_app = typer.Typer(
    no_args_is_help=True, help="expression views: formulas over a run's logged series"
)


def _read_spec(spec: str | None, spec_file: str | None) -> dict:
    """Resolve --spec / --spec-file into a validated view spec.

    ``--spec-file -`` reads stdin, so a generator script can pipe straight in
    without a temp file. Validation happens here rather than at the server, so a
    typo names its own field instead of coming back as a 422.
    """
    if (spec is None) == (spec_file is None):
        raise typer.BadParameter("pass exactly one of --spec or --spec-file")
    if spec_file is not None:
        raw = sys.stdin.read() if spec_file == "-" else Path(spec_file).read_text()
    else:
        raw = spec
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise typer.BadParameter(f"spec is not valid JSON: {exc}") from exc

    from probe import expr as expr_module

    try:
        return expr_module.spec(parsed)
    except Exception as exc:  # noqa: BLE001 -- pydantic error text is the message
        raise typer.BadParameter(f"invalid expression spec: {exc}") from exc


@views_app.command("list")
def views_list(run: str = run_ref()) -> None:
    """Every expression view on a run, with its spec and provenance."""
    with _client() as c:
        _print_json(c.list_views(run))


@views_app.command("show")
def views_show(
    run: str = run_ref(),
    view: str = typer.Argument(..., metavar="VIEW", help="view id or name"),
) -> None:
    """One view, by id or by name."""
    with _client() as c:
        views = c.list_views(run)
    for row in views:
        if view in (str(row.get("id")), row.get("name")):
            _print_json(row)
            return
    names = ", ".join(sorted(str(r.get("name")) for r in views)) or "none"
    raise typer.BadParameter(f"no view {view!r} on run {run}; run has: {names}")


@views_app.command("create")
def views_create(
    run: str = run_ref(),
    name: str = typer.Argument(..., help="panel title; unique per run"),
    spec: str = typer.Option(None, "--spec", metavar="JSON", help="inline spec"),
    spec_file: str = typer.Option(
        None, "--spec-file", metavar="PATH", help="spec JSON from a file, or - for stdin"
    ),
) -> None:
    """Save a view. Works on a completed run — a view reads, it never appends."""
    body = _read_spec(spec, spec_file)
    with _client() as c:
        _print_json(c.create_view(run, name, body))


@views_app.command("preview")
def views_preview(
    run: str = run_ref(),
    spec: str = typer.Option(None, "--spec", metavar="JSON"),
    spec_file: str = typer.Option(None, "--spec-file", metavar="PATH", help="or - for stdin"),
    step_from: int = typer.Option(None, "--step-from"),
    step_to: int = typer.Option(None, "--step-to"),
    max_points: int = typer.Option(None, "--max-points"),
) -> None:
    """Evaluate a spec WITHOUT saving it.

    Run this before `create`: a spec naming a series the run never logged comes
    back here with `missing_inputs`, instead of being saved as a panel that
    renders empty for everyone who opens the run.
    """
    body = _read_spec(spec, spec_file)
    with _client() as c:
        _print_json(
            c.preview_view(run, body, step_from=step_from, step_to=step_to, max_points=max_points)
        )


@views_app.command("data")
def views_data(
    run: str = run_ref(),
    view_id: str = typer.Argument(...),
    step_from: int = typer.Option(None, "--step-from"),
    step_to: int = typer.Option(None, "--step-to"),
    max_points: int = typer.Option(None, "--max-points"),
) -> None:
    """Evaluate a saved view and print its curve.

    Read the whole envelope, not just `points`: `missing_inputs` names series the
    expression referenced that the run has none of, `dropped_nonfinite` counts
    NaN/inf results, and `truncated` says the input scan hit its bound.
    """
    with _client() as c:
        _print_json(
            c.view_data(run, view_id, step_from=step_from, step_to=step_to, max_points=max_points)
        )


@views_app.command("rename")
def views_rename(
    view_id: str = typer.Argument(...),
    name: str = typer.Argument(...),
) -> None:
    """Rename a view. The expression is untouched."""
    with _client() as c:
        _print_json(c.update_view(view_id, name=name))


@views_app.command("update")
def views_update(
    view_id: str = typer.Argument(..., help="view id (`probe views list RUN` shows it)"),
    name: str = typer.Option(None, "--name", help="new name; omit to keep it"),
    spec: str = typer.Option(
        None, "--spec", metavar="JSON", help="new expression; REPLACES the stored one whole"
    ),
    spec_file: str = typer.Option(
        None, "--spec-file", metavar="PATH", help="spec JSON from a file, or - for stdin"
    ),
    expected_updated_at: str = typer.Option(
        None,
        "--expected-updated-at",
        metavar="TIMESTAMP",
        help="the view's updated_at as you read it; refused if it changed since",
    ),
) -> None:
    """Change a view's expression and/or name.

    The spec replaces the stored one whole, so read the view first (`probe views
    list RUN`) and build on what is there. Pass its `updated_at` as
    `--expected-updated-at` and an edit made since you read it is refused rather
    than overwritten; the refusal prints the view as it is now.
    """
    body = _read_spec(spec, spec_file) if (spec is not None or spec_file is not None) else None
    if name is None and body is None:
        raise typer.BadParameter("pass --name, --spec or --spec-file")
    with _client() as c:
        try:
            updated = c.update_view(
                view_id, name=name, spec=body, expected_updated_at=expected_updated_at
            )
        except errors.ConflictError as exc:
            if not (isinstance(exc.detail, dict) and "current" in exc.detail):
                raise  # a name clash, not a moved view: the plain error says it
            print(f"error: {exc}", file=sys.stderr)
            # The view as it stands, so the caller can rebuild its change on it
            # without a second read. null: it was deleted meanwhile.
            current = json.dumps(exc.detail["current"], ensure_ascii=False)
            print(f"current: {current}", file=sys.stderr)
            raise typer.Exit(1) from exc
    _print_json(updated)


@views_app.command("delete")
def views_delete(view_id: str = typer.Argument(...)) -> None:
    """Delete a view. The series it read are untouched."""
    with _client() as c:
        c.delete_view(view_id)
    print(f"deleted view {view_id}")
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
