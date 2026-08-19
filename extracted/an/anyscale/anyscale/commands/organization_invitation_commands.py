from datetime import datetime

import click
from dateutil import tz
from rich import print as rprint
import tabulate

import anyscale
from anyscale.cli_logger import BlockLogger
from anyscale.commands import command_examples
from anyscale.commands.doc_metadata import (
    command_metadata,
    CommandExample,
    ReleaseStatus,
)
from anyscale.commands.output_format import (
    OUTPUT_FLAG,
    OUTPUT_FLAG_LONG,
    OutputFormat,
    print_output,
)
from anyscale.commands.util import AnyscaleCommand
from anyscale.errors import UserError
from anyscale.organization_invitation.models import OrganizationInvitation


log = BlockLogger()  # CLI Logger


@click.group("organization-invitation", help="Manage organization invitations.")
def organization_invitation_cli() -> None:
    pass


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Invite users to your organization by email.",
            command="anyscale organization-invitation create --emails someone@myorg.com,other@myorg.com",
            output_raw=command_examples.ORGANIZATION_INVITATION_CREATE_EXAMPLE,
        ),
    ],
)
@organization_invitation_cli.command(
    name="create",
    short_help="Create organization invitations for the provided emails.",
    cls=AnyscaleCommand,
)
@click.option(
    "--emails",
    required=True,
    type=str,
    help="The emails to send the organization invitations to. Delimited by commas.",
)
def create(emails: str,) -> None:
    """
    Creates organization invitations for the provided emails.
    """
    log.info("Creating organization invitations...")

    success_emails, error_messages = anyscale.organization_invitation.create(
        emails.split(",")
    )

    if success_emails:
        log.info(f"Organization invitations sent to: {', '.join(success_emails)}")

    if error_messages:
        for error_message in error_messages:
            log.error(
                f"Failed to send organization invitations with the following errors: {error_message}"
            )


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[
        OutputFormat.TEXT,
        OutputFormat.JSON,
        OutputFormat.YAML,
        OutputFormat.TABLE,
    ],
    examples=[
        CommandExample(
            description="List pending organization invitations.",
            command="anyscale organization-invitation list",
            output_raw=command_examples.ORGANIZATION_INVITATION_LIST_EXAMPLE,
            output_instance=lambda: [
                OrganizationInvitation(
                    id="orginv_abc123",
                    email="someone@myorg.com",
                    created_at=datetime(2024, 9, 11),
                    expires_at=datetime(2024, 9, 25),
                )
            ],
        ),
    ],
    output_schema=OrganizationInvitation,
)
@organization_invitation_cli.command(
    name="list", short_help="List organization invitations.", cls=AnyscaleCommand,
)
@click.option(
    OUTPUT_FLAG,
    OUTPUT_FLAG_LONG,
    "output_format",
    type=click.Choice([f.value for f in OutputFormat]),
    default=OutputFormat.TEXT.value,
    show_default=True,
    help="Output format for the result.",
)
def list(output_format: str) -> None:  # noqa: A001
    """
    Lists organization invitations.
    """
    organization_invitations = anyscale.organization_invitation.list()

    if output_format != OutputFormat.TEXT.value:
        print_output(organization_invitations, output_format)
        return

    table = tabulate.tabulate(
        [
            (
                i.id,
                i.email,
                i.created_at.astimezone(tz=tz.tzlocal()).strftime("%m/%d/%Y %I:%M %p"),
                i.expires_at.astimezone(tz=tz.tzlocal()).strftime("%m/%d/%Y %I:%M %p"),
            )
            for i in organization_invitations
        ],
        headers=["ID", "Email", "Created At", "Expires At"],
    )
    rprint(table)


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Delete an organization invitation by email.",
            command="anyscale organization-invitation delete --email someone@myorg.com",
            output_raw=command_examples.ORGANIZATION_INVITATION_DELETE_EXAMPLE,
        ),
    ],
)
@organization_invitation_cli.command(
    name="delete", short_help="Delete an organization invitation.", cls=AnyscaleCommand,
)
@click.option(
    "--email",
    required=True,
    type=str,
    help="The email of the organization invitation to delete.",
)
def delete(email: str,) -> None:
    """
    Deletes an organization invitation.
    """
    try:
        organization_invitation_email = anyscale.organization_invitation.delete(email)
    except ValueError as e:
        raise UserError(
            f"Failed to delete organization invitation: {e}", legacy_exit_code=0
        ) from None

    log.info(f"Organization invitation for {organization_invitation_email} deleted.")
