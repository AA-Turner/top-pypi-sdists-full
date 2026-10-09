"""CLI wiring for the organisation archive command."""

import json

import click

from agilicus.command_helpers import Command
from agilicus.output import output_if_console

from . import archive

cmd = Command()


@cmd.command(name="archive-org")
@click.argument("organisation", required=False, default=None)
@click.option(
    "--directory",
    "-d",
    required=True,
    type=click.Path(file_okay=False, dir_okay=True),
    help="Directory to write the archive into. Created if it does not exist.",
)
@click.option(
    "--recursive/--no-recursive",
    default=True,
    help="Also archive every sub-organisation, recursively (default: recursive).",
)
@click.option(
    "--workers",
    type=int,
    default=8,
    show_default=True,
    help="Concurrency for per-object lookups (multi-factor, connector services, ...).",
)
@click.option(
    "--include-mfa/--no-mfa",
    default=True,
    help="Include per-user multi-factor enrolments (one API call per user).",
)
@click.option(
    "--type",
    "include_types",
    multiple=True,
    help="Only archive these object types (repeatable).",
)
@click.option(
    "--exclude-type",
    "exclude_types",
    multiple=True,
    help="Skip these object types (repeatable).",
)
@click.pass_context
def cli_command_archive_org(
    ctx,
    organisation,
    directory,
    recursive,
    workers,
    include_mfa,
    include_types,
    exclude_types,
):
    """Archive every object in an organisation (and its sub-orgs) as JSON.

    Objects are written to DIRECTORY, one JSON file per object, at
    DIRECTORY/org-<org-id>/<type>/<guid>.json. This is the SDK equivalent of
    `kubectl get all -A -o json`.
    """
    try:
        result = archive.archive_org(
            ctx,
            org_id=organisation,
            directory=directory,
            recursive=recursive,
            workers=workers,
            include_types=include_types,
            exclude_types=exclude_types,
            include_mfa=include_mfa,
        )
    except ValueError as exc:
        raise click.ClickException(str(exc))

    if (ctx.obj or {}).get("output_format") == "json":
        click.echo(json.dumps(result.to_dict(), indent=2, default=str))
        return

    output_if_console(
        ctx,
        "Archived {} objects across {} organisation(s) into {}".format(
            sum(result.counts.values()),
            len(result.visited),
            result.directory,
        ),
    )
    for name in sorted(result.counts):
        output_if_console(ctx, "  {:36s} {}".format(name, result.counts[name]))

    _print_errors(ctx, result)
    output_if_console(ctx, "Manifest: {}".format(result.directory + "/manifest.json"))


def _print_errors(ctx, result):
    """Print a compact, per-organisation summary of the non-fatal errors."""
    if not result.errors:
        return
    by_org: dict = {}
    for error in result.errors:
        by_org.setdefault(error.get("org_id") or "-", []).append(error)
    for org_id, errors in by_org.items():
        labels = []
        for error in errors:
            status = error.get("status")
            if status:
                labels.append("{} ({})".format(error["type"], status))
            else:
                labels.append(error["type"])
        shown = labels[:8]
        remainder = len(labels) - len(shown)
        summary = ", ".join(shown)
        if remainder > 0:
            summary += ", and {} more".format(remainder)
        output_if_console(
            ctx,
            "  ! {}: {} type(s) could not be read: {}".format(
                org_id, len(errors), summary
            ),
        )


def add_commands(cli):
    cmd.add_to_cli(cli)
