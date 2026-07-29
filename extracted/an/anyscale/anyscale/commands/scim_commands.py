"""
CLI commands for SCIM-related operations.

These commands handle SCIM-specific functionality like enforcing
user group permissions after SCIM is enabled.
"""

from typing import Dict, List

import click
from rich.console import Console
from rich.table import Table

from anyscale._private.anyscale_client import AnyscaleClient
from anyscale.cli_logger import BlockLogger
from anyscale.commands import command_examples
from anyscale.commands.doc_metadata import (
    command_metadata,
    CommandExample,
    ReleaseStatus,
)
from anyscale.commands.output_format import OutputFormat
from anyscale.commands.util import AnyscaleCommand


log = BlockLogger()


def _format_permission_diff(result: Dict) -> str:
    """Format the permission diff result for display."""
    lines = []

    users_with_changes = result.get("users_with_changes", [])
    users_to_remove = result.get("users_to_remove", [])

    if not users_with_changes and not users_to_remove:
        return "No permission changes detected."

    # Users with permission changes
    for user in users_with_changes:
        user_email = user.get("user_email", "unknown")
        lines.append(f"\n{user_email}:")

        # Cloud changes
        cloud_changes = user.get("cloud_changes", [])
        if cloud_changes:
            lines.append("  - clouds:")
            for change in cloud_changes:
                name = change.get("resource_name", change.get("resource_id"))
                old_role = change.get("old_role") or "(none)"
                new_role = change.get("new_role") or "(removed)"
                lines.append(f"      - {name}: {old_role} -> {new_role}")
                if change.get("new_role") is None:
                    lines.append("        (default project access revoked)")

        # Project changes
        project_changes = user.get("project_changes", [])
        if project_changes:
            lines.append("  - projects:")
            for change in project_changes:
                name = change.get("resource_name", change.get("resource_id"))
                old_role = change.get("old_role") or "(none)"
                new_role = change.get("new_role") or "(removed)"
                lines.append(f"      - {name}: {old_role} -> {new_role}")

        # Org role change
        org_role_change = user.get("org_role_change")
        if org_role_change:
            old_role = org_role_change.get("old_role") or "(none)"
            new_role = org_role_change.get("new_role") or "(removed)"
            lines.append(f"  - organization: {old_role} -> {new_role}")

    # Users to be removed
    if users_to_remove:
        lines.append("\n--- Users to be removed (not in any active user group) ---")
        for user in users_to_remove:
            user_email = user.get("user_email", "unknown")
            lines.append(f"  - {user_email}")

    return "\n".join(lines)


@click.group(
    "scim", help="Manage SCIM (System for Cross-domain Identity Management) settings."
)
def scim_cli() -> None:
    pass


@command_metadata(
    status=ReleaseStatus.BETA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Preview the permission changes without applying them.",
            command="anyscale scim enforce-groups --dry-run",
            output_raw=command_examples.SCIM_ENFORCE_GROUP_PERMISSIONS_EXAMPLE,
        ),
    ],
)
@scim_cli.command(
    name="enforce-groups",
    short_help="Enforce SCIM-based user group permissions.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "--dry-run",
    is_flag=True,
    default=False,
    help="Preview permission changes without applying them. "
    "Shows only actual changes from users' perspective.",
)
def enforce_group_permissions(dry_run: bool) -> None:
    """
    Enforce SCIM-based user group permissions by removing individual user permissions.

    This command removes ALL direct user permissions so that users only derive
    permissions from their user groups.

    Use --dry-run to preview what permission changes users will experience
    before actually applying them.
    """
    client = AnyscaleClient()

    try:
        if dry_run:
            log.info("Running in dry-run mode. Analyzing permission changes...")
            response = client.scim_migration_preview()
            result = response.get("result", response)

            formatted_output = _format_permission_diff(result)
            click.echo("\n=== Permission Changes Preview ===")
            click.echo(formatted_output)
            click.echo(
                "\n(No changes were applied. Remove --dry-run to apply changes.)"
            )
            return

        # Live mode - first show permission changes preview
        log.info("Analyzing permission changes...")
        diff_response = client.scim_migration_preview()
        diff_result = diff_response.get("result", diff_response)

        formatted_output = _format_permission_diff(diff_result)
        click.echo("\n=== Permission Changes Preview ===")
        click.echo(formatted_output)

        click.echo(
            "\n"
            "╭─────────────────── ⚠️  Confirmation Required ───────────────────╮\n"
            "│ WARNING: This is a destructive operation that cannot be undone. │\n"
            "│                                                                 │\n"
            "│ All role bindings on users will be removed.                     │\n"
            "│ Role bindings on user groups and service accounts are unchanged.│\n"
            "│                                                                 │\n"
            "│ Cloud membership edges also removed (default-project access).   │\n"
            "╰─────────────────────────────────────────────────────────────────╯\n"
        )
        click.confirm(
            "Do you want to proceed?", default=False, abort=True,
        )

        log.info("Starting SCIM permission migration...")
        response = client.migrate_scim_permissions(dry_run=False)

        result = response.get("result", response)
        errors = result.get("errors", [])

        if errors:
            raise click.ClickException("; ".join(errors))

        click.echo("\n=== Applied Permission Changes ===")
        click.echo(formatted_output)
        log.info("SCIM permission migration completed successfully.")

    except (click.ClickException, click.Abort):
        raise
    except Exception as e:  # noqa: BLE001
        log.error(f"Failed to migrate SCIM permissions: {e}")
        raise click.ClickException(str(e))


def _analyze_permissions(result: Dict) -> List[Dict]:
    """Analyze SCIM user permissions and return entries with incomplete setup.

    Checks each non-service-account user's cloud permissions. A cloud role that
    is not readonly but has no project-level permissions is flagged as incomplete.

    Args:
        result: The API response dict from list_scim_user_permissions,
                containing a "users" list.

    Returns:
        List of dicts with keys: email, cloud_name, role, issue.
    """
    warnings: List[Dict] = []
    for user in result.get("users", []):
        if user.get("is_service_account"):
            continue
        clouds = user.get("clouds") or []
        if not clouds:
            continue
        for cloud in clouds:
            if cloud.get("role") == "readonly":
                continue
            projects = cloud.get("projects") or []
            if not projects:
                warnings.append(
                    {
                        "email": user.get("user_email", "unknown"),
                        "cloud_name": cloud.get("cloud_name", "unknown"),
                        "role": cloud.get("role", "unknown"),
                        "issue": "No project permissions",
                    }
                )
    return warnings


@command_metadata(
    status=ReleaseStatus.BETA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Check for SCIM users with incomplete permission setup.",
            command="anyscale scim check-permissions",
            output_raw=command_examples.SCIM_CHECK_PERMISSIONS_EXAMPLE,
        ),
    ],
)
@scim_cli.command(
    name="check-permissions",
    short_help="Check for SCIM users with incomplete permission setup.",
    cls=AnyscaleCommand,
    is_beta=True,
)
def check_permissions() -> None:
    """Check for SCIM users with incomplete permission setup.

    Identifies users who have a cloud role (owner or collaborator) but are
    missing project-level permissions. These users can access the cloud but
    cannot use any projects within it.
    """
    client = AnyscaleClient()

    try:
        log.info("Checking SCIM user permissions...")
        response = client.list_scim_user_permissions()
        result = response.get("result", response)
        warnings = _analyze_permissions(result)

        if not warnings:
            click.echo("All SCIM users have complete permission setup.")
            return

        table = Table(show_header=True, header_style="bold")
        table.add_column("User Email", no_wrap=True)
        table.add_column("Cloud", no_wrap=True)
        table.add_column("Role", no_wrap=True)
        table.add_column("Issue", no_wrap=True)

        for w in warnings:
            table.add_row(w["email"], w["cloud_name"], w["role"], w["issue"])

        click.echo("Users with incomplete SCIM permission setup:")
        Console().print(table)
        n = len({w["email"] for w in warnings})
        noun = "user" if n == 1 else "users"
        verb = "has" if n == 1 else "have"
        click.echo(f"\n{n} {noun} {verb} incomplete permission setup.")
        click.echo("\nRun 'anyscale policy set' to grant project-level permissions.")
        click.echo(
            "See https://docs.anyscale.com/administration/organization/scim"
            " for details."
        )

    except click.ClickException:
        raise
    except Exception as e:  # noqa: BLE001
        log.error(f"Failed to check SCIM permissions: {e}")
        raise click.ClickException(str(e))
