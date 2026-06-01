from __future__ import annotations

import click

from ovide.assemble import assemble_changelog, bump_version, compute_bump, get_latest_version
from ovide.config import VALID_BUMPS, VALID_KINDS
from ovide.fragment import Fragment, FragmentError, create_fragment, list_fragments


@click.group()
def main() -> None:
    """ovide - Changelog fragment management tool."""


@main.command()
@click.option("--bump", type=click.Choice(VALID_BUMPS), prompt="Bump level")
@click.option("--kind", type=click.Choice(VALID_KINDS, case_sensitive=False), prompt="Change kind")
@click.option("--slug", type=str, default=None, help="Optional slug for the filename")
@click.option("-m", "--message", type=str, default=None, help="Change description (omit to open editor)")
def new(bump: str, kind: str, slug: str | None, message: str | None) -> None:
    """Create a new changelog fragment."""
    if message is None:
        message = click.edit("# Describe the change (lines starting with # are removed)\n")
        if message is None:
            raise click.Abort()
        message = "\n".join(line for line in message.splitlines() if not line.startswith("#")).strip()
        if not message:
            raise click.ClickException("Empty message, aborting.")

    path = create_fragment(bump, kind, message, slug)
    click.echo(f"Created {path}")


@main.command()
def check() -> None:
    """Validate all changelog fragments."""
    paths = list_fragments()
    if not paths:
        click.echo("No fragments found in changelog.d/")
        return

    errors: list[str] = []
    for path in paths:
        try:
            Fragment.parse(path)
        except FragmentError as e:
            errors.append(str(e))

    if errors:
        for err in errors:
            click.echo(f"ERROR: {err}", err=True)
        raise SystemExit(1)

    click.echo(f"All {len(paths)} fragment(s) are valid.")


@main.command()
@click.option("--version", type=str, default=None, help="Release version (e.g. 2.2.0)")
@click.option("--yes", "-y", is_flag=True, help="Skip confirmation prompt")
def assemble(version: str | None, yes: bool) -> None:
    """Assemble fragments into CHANGELOG.md and remove them."""
    paths = list_fragments()
    if not paths:
        raise click.ClickException("No fragments found in changelog.d/")

    fragments: list[Fragment] = []
    errors: list[str] = []
    for path in paths:
        try:
            fragments.append(Fragment.parse(path))
        except FragmentError as e:
            errors.append(str(e))

    if errors:
        for err in errors:
            click.echo(f"ERROR: {err}", err=True)
        raise click.ClickException("Fix invalid fragments before assembling.")

    required_bump = compute_bump(fragments)

    if version is None:
        latest = get_latest_version()
        if latest is None:
            raise click.ClickException("No previous version found in CHANGELOG.md. Use --version to specify.")
        version = bump_version(latest, required_bump)

    click.echo(f"Required bump: {required_bump}")
    click.echo(f"Version: {version}")
    click.echo(f"Fragments: {len(fragments)}")

    if not yes:
        click.confirm("Proceed?", abort=True)

    assemble_changelog(version, fragments)
    click.echo(f"Assembled {len(fragments)} fragment(s) into CHANGELOG.md")
