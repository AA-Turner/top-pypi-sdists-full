from datetime import datetime
from typing import Optional

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
from anyscale.errors import UserError
from anyscale.role.models import Role
from anyscale.util import validate_non_negative_arg


log = BlockLogger()

_LIST_OUTPUT = """\
ID          Name      Type    Archived    Description
----------  --------  ------  ----------  --------------------------
rol_abc123  Operator  Custom              Runs and manages workloads
"""

_GET_OUTPUT = """\
Role Operator (rol_abc123)
  Type:         Custom
  Description:  Runs and manages workloads
  Grants:       cloud_get, job_create, job_delete
  Denies:       -
  Archived:     no
"""


@click.group("role", help="Read the roles your organization can assign.")
def role_cli() -> None:
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
            description="List the roles the organization can assign.",
            command="anyscale role list",
            output_raw=_LIST_OUTPUT,
            output_instance=lambda: [
                Role(
                    id="rol_abc123",
                    name="Operator",
                    built_in=False,
                    description="Runs and manages workloads",
                    created_at=datetime(2026, 9, 18),
                )
            ],
        ),
    ],
    output_schema=Role,
)
@role_cli.command(
    name="list",
    short_help="List the roles your organization can assign.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "--name",
    "-n",
    required=False,
    default=None,
    type=str,
    help="Only roles whose name contains this text.",
)
@click.option(
    "--include-archived",
    is_flag=True,
    default=False,
    help="Include archived roles, which cannot be newly assigned.",
)
@click.option(
    "--max-items",
    default=None,
    type=int,
    callback=validate_non_negative_arg,
    help="Maximum number of roles to return. Every role by default.",
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
def list_roles(
    name: Optional[str],
    include_archived: bool,
    max_items: Optional[int],
    output_format: str,
) -> None:
    """List the roles your organization can assign."""
    roles = anyscale.role.list(
        name=name,
        include_archived=include_archived,
        max_items=max_items,
    )

    if output_format != OutputFormat.TEXT.value:
        print_output(roles, output_format)
        return

    if not roles:
        log.info("No roles found.")
        return

    rprint(
        tabulate.tabulate(
            [
                [
                    role.id,
                    role.name,
                    "System" if role.built_in else "Custom",
                    "yes" if role.archived_at else "",
                    role.description or "",
                ]
                for role in roles
            ],
            headers=["ID", "Name", "Type", "Archived", "Description"],
        )
    )


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
            description="Show one role and what it grants.",
            command="anyscale role get --id rol_abc123",
            output_raw=_GET_OUTPUT,
            output_instance=lambda: Role(
                id="rol_abc123",
                name="Operator",
                built_in=False,
                description="Runs and manages workloads",
                allowed_permissions=["cloud_get", "job_create", "job_delete"],
                denied_permissions=[],
                created_at=datetime(2026, 9, 18),
            ),
        ),
    ],
    output_schema=Role,
)
@role_cli.command(
    name="get",
    short_help="Show one role and the permissions it carries.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "--role-id",
    "--id",
    "role_id",
    required=True,
    type=str,
    help="The id of the role to show. Find one with `anyscale role list`.",
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
def get_role(role_id: str, output_format: str) -> None:
    """Show one role and the permissions it carries."""
    try:
        role = anyscale.role.get(role_id=role_id)
    except ValueError as e:
        raise UserError(str(e), legacy_exit_code=0) from None

    if output_format != OutputFormat.TEXT.value:
        print_output(role, output_format)
        return

    rprint(f"Role {role.name} ({role.id})")
    for label, value in (
        ("Type", "System" if role.built_in else "Custom"),
        ("Description", role.description or "-"),
        ("Grants", ", ".join(role.allowed_permissions or []) or "-"),
        ("Denies", ", ".join(role.denied_permissions or []) or "-"),
        ("Archived", str(role.archived_at) if role.archived_at else "no"),
    ):
        rprint(f"  {label + ':':<13} {value}")
