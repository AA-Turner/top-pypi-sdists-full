from typing import List, Optional, Tuple

import click

import anyscale.skills
from anyscale.skills.errors import (
    AlreadyInstalledError,
    PlatformVersionMismatchError,
    SKILLS_TERMS_DOC_URL,
    TermsNotAcceptedError,
)
from anyscale.skills.models import (
    CatalogEntry,
    InstalledMetadata,
    Platform,
    PLATFORMS,
    SkillsListResult,
    TermsStatus,
)


_PLATFORM_CHOICES = click.Choice(
    [platform.value for platform in Platform], case_sensitive=False,
)

_KNOWN_PLATFORM_VALUES = frozenset(platform.value for platform in Platform)


def _is_unsupported(entry: CatalogEntry) -> bool:
    """True if the entry advertises platforms but none are known to this CLI."""
    return bool(entry.platforms) and not set(entry.platforms) & _KNOWN_PLATFORM_VALUES


def _print_catalog(catalog: List[CatalogEntry]) -> None:
    for entry in catalog:
        suffix = "  (requires newer CLI)" if _is_unsupported(entry) else ""
        click.echo(f"  /{entry.name}{suffix}")


def _print_diff(added: List[CatalogEntry], removed: List[CatalogEntry]) -> None:
    for entry in added:
        tags = ["new"]
        if _is_unsupported(entry):
            tags.append("requires newer CLI")
        click.echo(f"  + /{entry.name}  {', '.join(tags)}")
    for entry in removed:
        click.echo(f"  - /{entry.name}  removed")


def _fmt_skill_count(n: int) -> str:
    return f"{n} skill{'s' if n != 1 else ''}"


def _print_version_catalog(version: str, catalog: List[CatalogEntry]) -> None:
    click.echo(f"v{version} ({_fmt_skill_count(len(catalog))})")
    if catalog:
        _print_catalog(catalog)


def _print_installed_section(metadata: Optional[InstalledMetadata]) -> None:
    if metadata is None:
        click.echo("Not installed.")
        return
    platforms_str = ", ".join(metadata.platforms)
    file_count = sum(
        len(platform_info.installed_files)
        for platform_info in metadata.platforms.values()
    )
    click.echo(f"Installed: v{metadata.version} ({platforms_str}, {file_count} files)")
    if metadata.catalog:
        _print_catalog(metadata.catalog)


def _print_update_section(info: SkillsListResult) -> None:
    metadata = info.installed
    if metadata is None:
        click.echo(
            f"Available: v{info.available_version} "
            f"({_fmt_skill_count(len(info.available_catalog))})"
        )
        if info.available_catalog:
            _print_catalog(info.available_catalog)
        click.echo("")
        click.echo("Run 'anyscale skills install' to get started.")
    elif info.up_to_date:
        click.echo("Skills are up to date.")
    else:
        click.echo(
            f"Update available: v{metadata.version} -> v{info.available_version}"
        )
        if info.added or info.removed:
            _print_diff(info.added, info.removed)
        else:
            click.echo("  (no skill changes, version bump only)")
        click.echo("")
        click.echo("Run 'anyscale skills update' to update.")


def _install_cmd(platforms: List[Platform], version: str) -> str:
    flags = "".join(f" -p {platform}" for platform in platforms)
    return f"anyscale skills install{flags} -v {version}"


def _prompt_terms_acceptance(terms: TermsStatus) -> bool:
    """Display terms and prompt for interactive acceptance. Returns True if accepted."""
    if not terms.license_text:
        raise click.ClickException(
            "Failed to retrieve license text from server. Please try again or update your CLI."
        )
    click.echo(terms.license_text)
    click.echo("")
    return click.confirm("Do you accept the terms above?", default=False)


def _prompt_platform_selection() -> List[Platform]:
    """Interactively ask the user which platform(s) to install for."""
    platform_list = list(Platform)
    click.echo("Select a platform to install skills for:")
    click.echo("  1) All platforms")
    for i, p in enumerate(platform_list, 2):
        meta = PLATFORMS[p]
        click.echo(f"  {i}) {meta.display} ({meta.dir})")
    click.echo("")

    choice = click.prompt("Platform", type=click.IntRange(1, len(platform_list) + 1),)

    if choice == 1:
        return platform_list
    return [platform_list[choice - 2]]


@click.group(
    "skills",
    short_help="Manage Anyscale agent skills for AI coding assistants",
    help="Install, update, and list Anyscale agent skills for AI coding assistants (Claude Code, Cursor etc).",
)
def skills_cli() -> None:
    pass


@skills_cli.command(name="list", help="List available Anyscale agent skills.")
@click.option("--version", "-v", help="List skills for a specific version.")
def skills_list(version: Optional[str]) -> None:
    try:
        info = anyscale.skills.list(version=version)
    except ValueError as e:
        raise click.ClickException(str(e)) from None

    if version is not None:
        _print_version_catalog(info.available_version, info.available_catalog)
        return

    _print_installed_section(info.installed)
    click.echo("")
    _print_update_section(info)


@skills_cli.command(name="install", help="Install Anyscale agent skills.")
@click.option("--version", "-v", help="Specific version to install.")
@click.option(
    "--platform",
    "-p",
    multiple=True,
    type=_PLATFORM_CHOICES,
    help="Target platform. Can be repeated (e.g. -p claude-code -p cursor).",
)
@click.option(
    "--accept-terms",
    "-y",
    "accept_terms",
    is_flag=True,
    default=False,
    help="Accept the terms of use non-interactively.",
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    default=False,
    help="Force reinstall even if already installed.",
)
@click.option(
    "--from-file",
    "from_file",
    type=click.Path(exists=True, dir_okay=False, readable=True),
    default=None,
    help=(
        "Install from a local bundle tarball instead of downloading. "
        "Requires --accept-terms."
    ),
)
def skills_install(
    version: Optional[str],
    platform: Tuple[str, ...],
    accept_terms: bool,
    force: bool,
    from_file: Optional[str],
) -> None:
    if platform:
        platforms: List[Platform] = [Platform(p) for p in platform]
    else:
        platforms = _prompt_platform_selection()

    try:
        try:
            installed_version = anyscale.skills.install(
                platforms=platforms,
                version=version,
                accept_terms=accept_terms,
                force=force,
                from_file=from_file,
            )
        except TermsNotAcceptedError as e:
            if not _prompt_terms_acceptance(e.terms):
                raise click.ClickException(
                    "You must accept the terms to install Anyscale skills.\n"
                    "  Use --accept-terms to accept non-interactively."
                ) from None
            anyscale.skills.accept_terms(e.terms)
            # accept_terms=True on retry guards against replica lag or a new
            # terms version published between the prompt and the re-fetch:
            # without it, a second TermsNotAcceptedError would escape this
            # handler and surface as an unformatted traceback.
            installed_version = anyscale.skills.install(
                platforms=platforms,
                version=version,
                accept_terms=True,
                force=force,
                from_file=from_file,
            )
    except PlatformVersionMismatchError as e:
        raise click.ClickException(
            f"Skills v{e.existing_version} currently installed on "
            f"{', '.join(e.already_installed)}.\n"
            f"All platforms must be on the same version.\n"
            f"  To install {', '.join(e.new_platforms)} at v{e.existing_version}:\n"
            f"    {_install_cmd(e.new_platforms, e.existing_version)}\n"
            f"  To reinstall all platforms at v{e.resolved_version}:\n"
            f"    {_install_cmd(e.all_platforms, e.resolved_version)}"
        ) from None
    except AlreadyInstalledError as e:
        raise click.ClickException(
            f"Skills v{e.existing_version} currently installed on "
            f"{', '.join(e.already_installed)}.\n"
            f"  Re-run with --force to reinstall at v{e.resolved_version}."
        ) from None
    except ValueError as e:
        raise click.ClickException(str(e)) from None

    click.echo(f"Successfully installed Anyscale skills v{installed_version}.")


@skills_cli.command(
    name="update", help="Update Anyscale agent skills to the latest version."
)
@click.option(
    "--force",
    "-f",
    is_flag=True,
    default=False,
    help="Re-download and reinstall even if already on the latest version.",
)
@click.option(
    "--accept-terms",
    "-y",
    "accept_terms",
    is_flag=True,
    default=False,
    help="Accept updated terms of use non-interactively.",
)
def skills_update(force: bool, accept_terms: bool) -> None:
    try:
        try:
            updated_version = anyscale.skills.update(
                force=force, accept_terms=accept_terms,
            )
        except TermsNotAcceptedError as e:
            if not _prompt_terms_acceptance(e.terms):
                raise click.ClickException(
                    "You must accept the updated terms to continue.\n"
                    "  Use --accept-terms to accept non-interactively."
                ) from None
            anyscale.skills.accept_terms(e.terms)
            # accept_terms=True on retry guards against replica lag or a new
            # terms version published between the prompt and the re-fetch:
            # without it, a second TermsNotAcceptedError would escape this
            # handler and surface as an unformatted traceback.
            updated_version = anyscale.skills.update(force=force, accept_terms=True)
    except ValueError as e:
        raise click.ClickException(str(e)) from None

    click.echo(f"Successfully updated Anyscale skills to v{updated_version}.")


@skills_cli.command(name="terms", help="View Anyscale agent skills terms of use.")
@click.option(
    "--version",
    "-v",
    help="Show terms for a specific version. Defaults to the latest available.",
)
def skills_terms(version: Optional[str]) -> None:
    try:
        terms = anyscale.skills.get_terms(version=version)
    except ValueError as e:
        raise click.ClickException(str(e)) from None

    if terms.accepted:
        accepted_at = terms.accepted_at or "unknown"
        click.echo(f"Skills terms accepted for v{terms.version} on {accepted_at}.")
        click.echo(f"  View terms: {SKILLS_TERMS_DOC_URL}")
        return

    if terms.license_text:
        click.echo(terms.license_text)
        click.echo("")
    click.echo(f"Skills terms for v{terms.version} have not been accepted.")
    click.echo(f"  View terms: {SKILLS_TERMS_DOC_URL}")
    click.echo("  Accept and install: anyscale skills install --accept-terms")
