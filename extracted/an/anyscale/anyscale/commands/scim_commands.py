"""
CLI commands for SCIM-related operations.

These commands handle SCIM-specific functionality like enforcing
user group permissions after SCIM is enabled.
"""

import click

from anyscale._private.anyscale_client import AnyscaleClient
from anyscale.cli_logger import BlockLogger
from anyscale.commands import command_examples
from anyscale.commands.util import AnyscaleCommand


log = BlockLogger()


@click.group(
    "scim", help="Manage SCIM (System for Cross-domain Identity Management) settings."
)
def scim_cli() -> None:
    pass


@scim_cli.command(
    name="enforce-groups",
    cls=AnyscaleCommand,
    example=command_examples.SCIM_ENFORCE_GROUP_PERMISSIONS_EXAMPLE,
    is_beta=True,
)
def enforce_group_permissions() -> None:
    """
    Enforce SCIM-based user group permissions by removing individual user permissions.

    This command removes ALL direct user permissions so that users only derive
    permissions from their user groups.
    """
    client = AnyscaleClient()

    try:
        click.echo(
            "\n"
            "╭─────────────────── ⚠️  Confirmation Required ───────────────────╮\n"
            "│ WARNING: This is a destructive operation that cannot be undone. │\n"
            "│                                                                 │\n"
            "│ All role bindings on users will be removed.                     │\n"
            "│ Role bindings on user groups and service accounts are unchanged.│\n"
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

        log.info("SCIM permission migration completed successfully.")

    except (click.ClickException, click.Abort):
        raise
    except Exception as e:  # noqa: BLE001
        log.error(f"Failed to migrate SCIM permissions: {e}")
        raise click.ClickException(str(e))
