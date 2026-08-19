from datetime import datetime
import json
from typing import Optional

import click
from rich import print as rprint
import tabulate

import anyscale
from anyscale._private.anyscale_client import AnyscaleClient
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
    warn_deprecated_flag,
)
from anyscale.commands.util import AnyscaleCommand
from anyscale.errors import UserError
from anyscale.user_group.models import UserGroup


log = BlockLogger()


@click.group("user-group", help="Manage user groups.")
def user_group_cli() -> None:
    pass


@command_metadata(
    status=ReleaseStatus.BETA,
    since="0.0.0",
    output_formats=[
        OutputFormat.TEXT,
        OutputFormat.JSON,
        OutputFormat.YAML,
        OutputFormat.TABLE,
    ],
    examples=[
        CommandExample(
            description="List user groups in the organization.",
            command="anyscale user-group list",
            output_raw=command_examples.USER_GROUP_LIST_EXAMPLE,
            output_instance=lambda: [
                UserGroup(
                    id="ug_abc123",
                    name="data-team",
                    org_id="org_abc123",
                    created_at=datetime(2024, 9, 11),
                    updated_at=datetime(2024, 9, 11),
                )
            ],
        ),
    ],
    output_schema=UserGroup,
)
@user_group_cli.command(
    name="list",
    short_help="List user groups in the organization.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "--max-items",
    default=50,
    type=int,
    help="Maximum number of user groups to return.",
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
def list_user_groups(max_items: int, output_format: str) -> None:
    """
    List user groups in the organization.
    """
    try:
        user_groups = anyscale.user_group.list(max_items=max_items)
    except ValueError as e:
        raise UserError(str(e), legacy_exit_code=0) from None

    if output_format != OutputFormat.TEXT.value:
        print_output(user_groups, output_format)
        return

    if not user_groups:
        log.info("No user groups found.")
        return

    table = tabulate.tabulate(
        [(ug.id, ug.name) for ug in user_groups], headers=["ID", "Name"],
    )
    rprint(table)


@command_metadata(
    status=ReleaseStatus.BETA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT, OutputFormat.JSON, OutputFormat.YAML],
    examples=[
        CommandExample(
            description="Get a user group by ID.",
            command="anyscale user-group get --id ug_abc123",
            output_raw=command_examples.USER_GROUP_GET_EXAMPLE,
            output_instance=lambda: UserGroup(
                id="ug_abc123",
                name="data-team",
                org_id="org_abc123",
                created_at=datetime(2024, 9, 11),
                updated_at=datetime(2024, 9, 11),
            ),
        ),
    ],
    output_schema=UserGroup,
)
@user_group_cli.command(
    name="get",
    short_help="Get a specific user group by ID.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "--user-group-id",
    "--id",
    "id",
    type=str,
    required=True,
    help="The ID of the user group to retrieve.",
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
    help="Output format for the result.",
)
def get_user_group(id: str, output_format: str) -> None:  # noqa: A002
    """
    Get a specific user group by ID.
    """
    try:
        user_group = anyscale.user_group.get(id=id)
    except ValueError as e:
        raise UserError(f"Failed to get user group: {e}", legacy_exit_code=0) from None

    if output_format != OutputFormat.TEXT.value:
        print_output(user_group, output_format)
        return

    details = [
        ("ID", user_group.id),
        ("Name", user_group.name),
        ("Organization ID", user_group.org_id),
        ("Created At", user_group.created_at.strftime("%Y-%m-%d %H:%M:%S UTC")),
        ("Updated At", user_group.updated_at.strftime("%Y-%m-%d %H:%M:%S UTC")),
    ]
    table = tabulate.tabulate(details, tablefmt="plain")
    rprint(table)


@user_group_cli.group("membership", help="Manage user group memberships.")
def membership_cli() -> None:
    pass


@command_metadata(
    status=ReleaseStatus.BETA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT, OutputFormat.JSON, OutputFormat.YAML],
    option_docs={
        "--output": {
            "status": ReleaseStatus.DEPRECATED,
            "deprecation_info": {"message": "Use --output-file instead."},
        }
    },
    examples=[
        CommandExample(
            description="List all user groups with their members.",
            command="anyscale user-group membership list",
            output_raw=command_examples.USER_GROUP_MEMBERSHIP_LIST_EXAMPLE,
            output_instance={
                "Engineering": ["alice@example.com", "charlie@example.com"],
                "Data Science": ["bob@example.com"],
            },
        ),
        CommandExample(
            description="Write the membership list to a JSON file.",
            command="anyscale user-group membership list --output-file memberships.json",
            output_raw="Results written to memberships.json\n",
        ),
    ],
)
@membership_cli.command(
    name="list",
    short_help="List all user groups with their members.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "--output-file",
    "output_file",
    type=click.Path(),
    default=None,
    help="Write JSON output to a file instead of stdout.",
)
@click.option(
    "--output",
    "-o",
    type=click.Path(),
    default=None,
    help="Write JSON output to a file instead of stdout.",
)
@click.option(
    "--output-format",
    "output_format",
    type=click.Choice(
        [OutputFormat.TEXT.value, OutputFormat.JSON.value, OutputFormat.YAML.value]
    ),
    default=OutputFormat.TEXT.value,
    show_default=True,
    help="Output format for the result. Ignored when writing to a file.",
)
def list_memberships(
    output_file: Optional[str], output: Optional[str], output_format: str
) -> None:
    """
    List all user groups with their members.

    Shows each user group and which users are members of that group.

    Output is JSON. Use --output to save to a file.
    """
    client = AnyscaleClient()
    try:
        log.info("Listing user group memberships...")
        response = client.list_user_group_memberships()
        result = response.get("result", response)

        groups = result.get("groups", [])
        simple_output = {}
        for group in groups:
            group_name = group.get("group_name", group.get("group_id", "unknown"))
            members = group.get("members", [])
            simple_output[group_name] = sorted(
                m.get("user_email", "") for m in members if m.get("user_email")
            )

        json_output = json.dumps(simple_output, indent=2)

        if output:
            warn_deprecated_flag("-o/--output", "--output-file")
        file_target = output_file or output
        if file_target:
            with open(file_target, "w") as f:
                f.write(json_output)
            log.info(f"Results written to {file_target}")
        elif output_format != OutputFormat.TEXT.value:
            print_output(simple_output, output_format)
        else:
            print(json_output)
    except click.ClickException:
        raise
    except Exception as e:  # noqa: BLE001
        log.error(f"Failed to list user group memberships: {e}")
        raise click.ClickException(str(e))
