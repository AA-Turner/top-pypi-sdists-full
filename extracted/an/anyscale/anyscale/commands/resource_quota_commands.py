from datetime import datetime
from typing import List, Optional, Tuple

import click
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
from anyscale.resource_quota.models import CreateResourceQuota, Quota, ResourceQuota
from anyscale.util import validate_non_negative_arg


log = BlockLogger()  # CLI Logger


@click.group("resource-quota", help="Anyscale resource quota commands.")
def resource_quota_cli() -> None:
    pass


def _format_resource_quotas(resource_quotas: List[ResourceQuota]) -> str:
    table_rows = []
    for resource_quota in resource_quotas:
        table_rows.append(
            [
                resource_quota.id,
                resource_quota.name,
                resource_quota.cloud_id,
                resource_quota.project_id,
                resource_quota.user_id,
                resource_quota.is_enabled,
                resource_quota.created_at.strftime("%m/%d/%Y"),
                resource_quota.deleted_at.strftime("%m/%d/%Y")
                if resource_quota.deleted_at
                else None,
                resource_quota.quota,
                resource_quota.is_soft_quota,
            ]
        )
    table = tabulate.tabulate(
        table_rows,
        headers=[
            "ID",
            "NAME",
            "CLOUD ID",
            "PROJECT ID",
            "USER ID",
            "IS ENABLED",
            "CREATED AT",
            "DELETED AT",
            "QUOTA",
            "IS SOFT QUOTA",
        ],
        tablefmt="plain",
    )

    return f"Resource quotas:\n{table}"


@command_metadata(
    status=ReleaseStatus.BETA,
    since="0.0.0",
    # TODO(MLDX-1486): flip to all OutputFormat values when -o is unhidden.
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Create a resource quota for a user in a project.",
            command=(
                "anyscale resource-quota create -n my-resource-quota --cloud my-cloud "
                "--project my-project --user-email someone@myorg.com --num-instances 100 "
                "--num-cpus 1000 --num-gpus 50 --num-accelerators A10G 10"
            ),
            output_raw=command_examples.RESOURCE_QUOTAS_CREATE_EXAMPLE,
            output_instance=lambda: ResourceQuota(
                id="rsq_abcdef",
                name="my-resource-quota",
                quota=Quota(
                    num_cpus=1000,
                    num_instances=100,
                    num_gpus=50,
                    num_accelerators={"A10G": 10},
                ),
                created_at=datetime(2024, 9, 11),
                cloud_id="cld_abcdef",
                project_id="prj_abcdef",
                user_id="usr_abcdef",
                is_enabled=True,
                is_soft_quota=False,
                deleted_at=None,
            ),
        ),
    ],
    output_schema=ResourceQuota,
)
@resource_quota_cli.command(
    name="create",
    short_help="Create a resource quota.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "-n", "--name", required=True, help="Name of the resource quota to create.",
)
@click.option(
    "--cloud",
    required=True,
    help="Name of the cloud that this resource quota applies to.",
)
@click.option(
    "--project",
    default=None,
    help="Name of the project that this resource quota applies to.",
)
@click.option(
    "--user-email",
    default=None,
    help="Email of the user that this resource quota applies to.",
)
@click.option(
    "--num-cpus",
    required=False,
    help="The quota limit for the number of CPUs.",
    type=int,
)
@click.option(
    "--num-instances",
    required=False,
    help="The quota limit for the number of instances.",
    type=int,
)
@click.option(
    "--num-gpus",
    required=False,
    help="The quota limit for the total number of GPUs.",
    type=int,
)
@click.option(
    "--num-accelerators",
    required=False,
    help="The quota limit for the number of accelerators. Example: --num-accelerators A100-80G 10",
    nargs=2,
    type=(str, int),
    multiple=True,
)
@click.option(
    "--is-soft-quota/--no-is-soft-quota",
    default=False,
    help="Whether this is a soft quota. When True, workloads can exceed the quota limit without being blocked.",
)
@click.option(
    OUTPUT_FLAG,
    OUTPUT_FLAG_LONG,
    "output_format",
    type=click.Choice([f.value for f in OutputFormat]),
    default=OutputFormat.TEXT.value,
    show_default=True,
    hidden=True,
    help="Output format for the created resource quota.",
)
def create(  # noqa: PLR0913
    name: str,
    cloud: str,
    project: Optional[str],
    user_email: Optional[str],
    num_cpus: Optional[int],
    num_instances: Optional[int],
    num_gpus: Optional[int],
    num_accelerators: List[Tuple[str, int]],
    is_soft_quota: bool,
    output_format: str,
) -> None:
    """Create a resource quota.

    A name and cloud name must be provided. Scope the quota with --project or
    --user-email, and set limits with --num-cpus, --num-instances, --num-gpus,
    or --num-accelerators (repeatable).
    """
    create_resource_quota = CreateResourceQuota(
        name=name,
        cloud=cloud,
        project=project,
        user_email=user_email,
        num_cpus=num_cpus,
        num_instances=num_instances,
        num_gpus=num_gpus,
        num_accelerators=dict(num_accelerators),
        is_soft_quota=is_soft_quota,
    )

    try:
        with log.spinner("Creating resource quota..."):
            resource_quota = anyscale.resource_quota.create(create_resource_quota)

        if output_format != OutputFormat.TEXT.value:
            print_output(resource_quota, output_format)
            return

        create_resource_quota_message = [f"Name: {name}\nCloud name: {cloud}"]
        if project:
            create_resource_quota_message.append(f"Project name: {project}")
        if user_email:
            create_resource_quota_message.append(f"User email: {user_email}")
        if num_cpus:
            create_resource_quota_message.append(f"Number of CPUs: {num_cpus}")
        if num_instances:
            create_resource_quota_message.append(
                f"Number of instances: {num_instances}"
            )
        if num_gpus:
            create_resource_quota_message.append(f"Number of GPUs: {num_gpus}")
        if num_accelerators:
            create_resource_quota_message.append(
                f"Number of accelerators: {dict(num_accelerators)}"
            )
        if is_soft_quota:
            create_resource_quota_message.append("Is soft quota: True")

        log.info("\n".join(create_resource_quota_message))
        log.info(f"Resource quota created successfully ID: {resource_quota.id}")

    except ValueError as e:
        log.error(f"Error creating resource quota: {e}")
        return


@command_metadata(
    status=ReleaseStatus.BETA,
    since="0.0.0",
    # TODO(MLDX-1486): flip to all OutputFormat values when -o is unhidden.
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="List the resource quotas of a cloud.",
            command="anyscale resource-quota list --cloud my-cloud",
            output_raw=command_examples.RESOURCE_QUOTAS_LIST_EXAMPLE,
            output_instance=lambda: [
                ResourceQuota(
                    id="rsq_123",
                    name="resource-quota-1",
                    quota=Quota(
                        num_cpus=1000,
                        num_instances=100,
                        num_gpus=50,
                        num_accelerators={"A10G": 10},
                    ),
                    created_at=datetime(2024, 9, 11),
                    cloud_id="cld_abcdef",
                    project_id="prj_abcdef",
                    user_id="usr_abcdef",
                    is_enabled=True,
                    is_soft_quota=False,
                    deleted_at=None,
                )
            ],
        ),
    ],
    output_schema=ResourceQuota,
)
@resource_quota_cli.command(
    name="list", short_help="List resource quotas.", cls=AnyscaleCommand, is_beta=True,
)
@click.option(
    "-n", "--name", required=False, help="The name filter for the resource quotas.",
)
@click.option(
    "--cloud", required=False, help="The cloud filter for the resource quotas.",
)
@click.option(
    "--creator-id",
    required=False,
    help="The creator ID filter for the resource quotas.",
)
@click.option(
    "--is-enabled",
    required=False,
    default=None,
    help="The is_enabled filter for the resource quotas.",
    type=bool,
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
    hidden=True,
    help="Output format for the result.",
)
def list_resource_quotas(
    name: Optional[str],
    cloud: Optional[str],
    creator_id: Optional[str],
    is_enabled: Optional[bool],
    max_items: int,
    output_format: str,
) -> None:
    """List resource quotas.

    Optionally filter by name, cloud, creator, or enabled state.
    """
    resource_quotas = anyscale.resource_quota.list(
        name=name,
        cloud=cloud,
        creator_id=creator_id,
        is_enabled=is_enabled,
        max_items=max_items,
    )

    if output_format != OutputFormat.TEXT.value:
        print_output(resource_quotas, output_format)
        return

    rprint(_format_resource_quotas(resource_quotas))


@command_metadata(
    status=ReleaseStatus.BETA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Delete a resource quota by ID.",
            command="anyscale resource-quota delete --id rsq_abcdef",
            output_raw=command_examples.RESOURCE_QUOTAS_DELETE_EXAMPLE,
        ),
    ],
)
@resource_quota_cli.command(
    name="delete",
    short_help="Delete a resource quota.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "--id", required=True, help="ID of the resource quota to delete.",
)
def delete(id: str) -> None:  # noqa: A002
    """Delete a resource quota.

    The ID of the resource quota must be provided.
    """
    try:
        with log.spinner("Deleting resource quota..."):
            anyscale.resource_quota.delete(resource_quota_id=id)
    except ValueError as e:
        log.error(f"Error deleting resource quota: {e}")
        return

    log.info(f"Resource quota with ID {id} deleted successfully.")


@command_metadata(
    status=ReleaseStatus.BETA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Enable a resource quota by ID.",
            command="anyscale resource-quota enable --id rsq_abcdef",
            output_raw=command_examples.RESOURCE_QUOTAS_ENABLE_EXAMPLE,
        ),
    ],
)
@resource_quota_cli.command(
    name="enable",
    short_help="Enable a resource quota.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "--id", required=True, help="ID of the resource quota to enable.",
)
def enable(id: str) -> None:  # noqa: A002
    """Enable a resource quota.

    The ID of the resource quota must be provided.
    """
    try:
        with log.spinner("Setting resource quota status..."):
            anyscale.resource_quota.enable(resource_quota_id=id)
    except ValueError as e:
        log.error(f"Error enabling resource quota: {e}")
        return

    log.info(f"Enabled resource quota with ID {id} successfully.")


@command_metadata(
    status=ReleaseStatus.BETA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Disable a resource quota by ID.",
            command="anyscale resource-quota disable --id rsq_abcdef",
            output_raw=command_examples.RESOURCE_QUOTAS_DISABLE_EXAMPLE,
        ),
    ],
)
@resource_quota_cli.command(
    name="disable",
    short_help="Disable a resource quota.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "--id", required=True, help="ID of the resource quota to disable.",
)
def disable(id: str) -> None:  # noqa: A002
    """Disable a resource quota.

    The ID of the resource quota must be provided.
    """
    try:
        with log.spinner("Setting resource quota status..."):
            anyscale.resource_quota.disable(resource_quota_id=id)
    except ValueError as e:
        log.error(f"Error disabling resource quota: {e}")
        return

    log.info(f"Disabled resource quota with ID {id} successfully.")
