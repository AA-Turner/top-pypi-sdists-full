from datetime import datetime
from typing import List, Optional

import click
from rich import print as rprint
import tabulate

import anyscale
from anyscale.cli_logger import BlockLogger
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
from anyscale.service_account.models import (
    OrganizationPermissionLevel,
    ServiceAccount,
)
from anyscale.util import validate_non_negative_arg


DEFAULT_OVERFLOW = "fold"
DEFAULT_COL_WIDTH = 36


log = BlockLogger()  # CLI Logger


@click.group(
    "service-account",
    short_help="Manage service accounts for your anyscale workloads.",
)
def service_account_cli() -> None:
    pass


def _print_new_api_key(api_key: str):
    log.warning(
        "The following API token for the service account will only appear once:",
    )
    log.info(api_key)


def _print_service_account_table(service_accounts: List[ServiceAccount]):
    table_rows = []
    for service_account in service_accounts:
        table_rows.append(
            [
                service_account.name,
                service_account.created_at.strftime("%m/%d/%Y"),
                service_account.permission_level,
                service_account.email,
            ]
        )
    table = tabulate.tabulate(
        table_rows,
        headers=["NAME", "CREATED AT", "ORGANIZATION PERMISSION LEVEL", "EMAIL",],
        tablefmt="plain",
    )

    rprint(f"Service accounts:\n{table}")


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT, OutputFormat.JSON, OutputFormat.YAML],
    examples=[
        CommandExample(
            description="Create a service account.",
            command="anyscale service-account create -n my-service-account",
            output_instance={
                "name": "my-service-account",
                "api_key": "<the service account's API token>",
            },
        ),
    ],
)
@service_account_cli.command(
    name="create",
    short_help="Create a service account.",
    help=(
        "Create a service account.\n\n"
        "The service account's API token is printed once on creation and can't "
        "be retrieved later, so store it securely."
    ),
    cls=AnyscaleCommand,
)
@click.option(
    "--name", "-n", help="Name for the service account.", type=str, required=True
)
@click.option(
    OUTPUT_FLAG,
    OUTPUT_FLAG_LONG,
    "output_format",
    type=click.Choice(
        [OutputFormat.TEXT.value, OutputFormat.JSON.value, OutputFormat.YAML.value]
    ),
    default=OutputFormat.TEXT.value,
    show_default=True,
    help="Output format for the created service account and its API token.",
)
def create(name: str, output_format: str) -> None:
    try:
        api_key = anyscale.service_account.create(name)

        if output_format != OutputFormat.TEXT.value:
            print_output({"name": name, "api_key": api_key}, output_format)
            return

        log.info(f"Service account {name} created successfully.")
        _print_new_api_key(api_key)
    except ValueError as e:
        log.error(f"Error creating service account: {e}")


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT, OutputFormat.JSON, OutputFormat.YAML],
    examples=[
        CommandExample(
            description="Create a new API key for a service account by name.",
            command="anyscale service-account create-api-key --name my-service-account",
            output_instance={"api_key": "<the new API token>"},
        ),
    ],
)
@service_account_cli.command(
    name="create-api-key",
    short_help="Create a new API key for a service account.",
    help=(
        "Create a new API key for a service account.\n\n"
        "Specify the service account by --email or --name. The new API token is "
        "printed once and can't be retrieved later, so store it securely."
    ),
    cls=AnyscaleCommand,
)
@click.option(
    "--email", help="Email of the service account to create the new key for.", type=str
)
@click.option(
    "--name", help="Name of the service account to create the new key for.", type=str
)
@click.option(
    OUTPUT_FLAG,
    OUTPUT_FLAG_LONG,
    "output_format",
    type=click.Choice(
        [OutputFormat.TEXT.value, OutputFormat.JSON.value, OutputFormat.YAML.value]
    ),
    default=OutputFormat.TEXT.value,
    show_default=True,
    help="Output format for the new API token.",
)
def create_api_key(
    email: Optional[str], name: Optional[str], output_format: str
) -> None:
    try:
        api_key = anyscale.service_account.create_api_key(email, name)

        if output_format != OutputFormat.TEXT.value:
            print_output({"api_key": api_key}, output_format)
            return

        _print_new_api_key(api_key)
    except ValueError as e:
        log.error(f"Error creating API key: {e}")


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
            description="List the service accounts in your organization.",
            command="anyscale service-account list",
            output_instance=lambda: [
                ServiceAccount(
                    name="my-service-account",
                    created_at=datetime(2024, 9, 11),
                    permission_level=OrganizationPermissionLevel.COLLABORATOR,
                    email="my-service-account@service-account.anyscale.com",
                )
            ],
        ),
    ],
    output_schema=ServiceAccount,
)
@service_account_cli.command(
    name="list",
    short_help="List service accounts.",
    help="List service accounts.",
    cls=AnyscaleCommand,
)
@click.option(
    "--max-items",
    required=False,
    default=20,
    type=int,
    help="Max items to show in list.",
    callback=validate_non_negative_arg,
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
def list_service_accounts(max_items: int, output_format: str) -> None:
    service_accounts = anyscale.service_account.list(max_items)
    if output_format != OutputFormat.TEXT.value:
        print_output(service_accounts, output_format)
        return
    _print_service_account_table(service_accounts)


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Delete a service account by name.",
            command="anyscale service-account delete --name my-service-account",
        ),
    ],
)
@service_account_cli.command(
    name="delete",
    short_help="Delete a service account.",
    help=(
        "Delete a service account.\n\n"
        "Specify the service account by --email or --name."
    ),
    cls=AnyscaleCommand,
)
@click.option("--email", help="Email of the service account to delete.", type=str)
@click.option("--name", help="Name of the service account to delete.", type=str)
def delete(email: Optional[str], name: Optional[str]) -> None:
    try:
        anyscale.service_account.delete(email, name)
        log.info(f"Service account {email or name} deleted successfully.")
    except ValueError as e:
        log.error(f"Error deleting service account: {e}")
