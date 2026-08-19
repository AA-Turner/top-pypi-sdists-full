from typing import Optional

import click
from rich import print as rprint
import tabulate
import yaml

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
from anyscale.policy.models import (
    Policy,
    PolicyBinding,
    PolicyConfig,
    PolicySyncStatus,
    ResourcePolicy,
)


log = BlockLogger()


@click.group("policy", help="Manage resource permission policies.")
def policy_cli() -> None:
    pass


@command_metadata(
    status=ReleaseStatus.BETA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Set the policy of a cloud from a YAML config file.",
            command="anyscale policy set --resource-type cloud --resource-id cld_abc123 -f policy.yaml",
            output_raw="Policy for cloud cld_abc123 has been updated.\n",
        ),
        CommandExample(
            description="Set the policy for your organization (no --resource-id).",
            command="anyscale policy set --resource-type organization -f org_policy.yaml",
            output_raw="Policy for organization your organization has been updated.\n",
        ),
    ],
)
@policy_cli.command(
    name="set",
    short_help="Set user group permission policy for a resource.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "--resource-type",
    required=True,
    type=click.Choice(["cloud", "project", "organization"], case_sensitive=False),
    help="Resource type ('cloud', 'project', or 'organization').",
)
@click.option(
    "--resource-id",
    required=False,
    default=None,
    type=str,
    help="Resource ID (e.g., cld_abc123, prj_xyz789). Required for 'cloud' and 'project' types, not allowed for 'organization'.",
)
@click.option(
    "-f",
    "--config-file",
    required=True,
    type=click.Path(exists=True),
    help="Path to a YAML config file with policy bindings.",
)
def set_policy(
    resource_type: str, resource_id: Optional[str], config_file: str,
) -> None:
    """
    Set user group permission policy for a resource.

    The config file should be in YAML format with bindings list.

    For organization policies, --resource-id cannot be specified, the policy will
    be set for your current organization automatically.

    Example policy.yaml:

    \b
    bindings:
      - role_name: collaborator
        principals:
          - ug_abc123
      - role_name: readonly
        principals:
          - ug_def456
          - ug_ghi789

    Valid role_name values:

    \b
      Cloud:        collaborator, readonly
      Project:      owner, collaborator, readonly
      Organization: owner, collaborator
    """
    # Validate resource_id based on resource_type
    if resource_type.lower() == "organization":
        if resource_id is not None:
            raise click.ClickException(
                "--resource-id cannot be specified for 'organization' resource type. "
                "The policy will be set for your current organization automatically."
            )
        display_id = "your organization"
    elif resource_id is None:
        raise click.ClickException(
            f"--resource-id is required for resource type '{resource_type}'."
        )
    else:
        display_id = resource_id

    log.info(f"Setting policy for {resource_type} {display_id}...")

    try:
        with open(config_file) as f:
            config_dict = yaml.safe_load(f)
    except yaml.YAMLError as e:
        raise click.ClickException(f"Failed to parse YAML file '{config_file}': {e}")

    if config_dict is None:
        raise click.ClickException(
            f"Invalid config file '{config_file}': file is empty."
        )
    if not isinstance(config_dict, dict):
        raise click.ClickException(
            f"Invalid config file '{config_file}': expected a YAML mapping with top-level 'bindings'."
        )

    try:
        bindings = [
            PolicyBinding(role_name=b["role_name"], principals=b["principals"],)
            for b in config_dict.get("bindings", [])
        ]
        config = PolicyConfig(bindings=bindings)
    except (KeyError, TypeError) as e:
        raise click.ClickException(f"Invalid config file format: {e}")

    try:
        anyscale.policy.set(
            resource_type=resource_type, resource_id=resource_id, config=config,
        )
    except ValueError as e:
        raise click.ClickException(f"Failed to set policy: {e}")

    log.info(f"Policy for {resource_type} {display_id} has been updated.")


@command_metadata(
    status=ReleaseStatus.BETA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT, OutputFormat.JSON, OutputFormat.YAML],
    examples=[
        CommandExample(
            description="Get the policy of a cloud.",
            command="anyscale policy get --resource-type cloud --resource-id cld_abc123",
            output_raw=command_examples.POLICY_GET_EXAMPLE,
            output_instance=lambda: Policy(
                bindings=[
                    PolicyBinding(role_name="collaborator", principals=["ug_abc123"])
                ],
                sync_status=PolicySyncStatus.success,
            ),
        ),
    ],
    output_schema=Policy,
)
@policy_cli.command(
    name="get",
    short_help="Get user group permission policy for a resource.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "--resource-type",
    required=True,
    type=click.Choice(["cloud", "project", "organization"], case_sensitive=False),
    help="Resource type ('cloud', 'project', or 'organization').",
)
@click.option(
    "--resource-id",
    required=False,
    default=None,
    type=str,
    help="Resource ID (e.g., cld_abc123, prj_xyz789). Required for 'cloud' and 'project' types, not allowed for 'organization'.",
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
def get_policy(
    resource_type: str, resource_id: Optional[str], output_format: str,
) -> None:
    """
    Get user group permission policy for a resource.

    For organization policies, --resource-id cannot be specified, the policy for
    your current organization will be returned automatically.
    """
    # Validate resource_id based on resource_type
    if resource_type.lower() == "organization":
        if resource_id is not None:
            raise click.ClickException(
                "--resource-id cannot be specified for 'organization' resource type. "
                "The policy will be retrieved for your current organization automatically."
            )
        display_id = "your organization"
    elif resource_id is None:
        raise click.ClickException(
            f"--resource-id is required for resource type '{resource_type}'."
        )
    else:
        display_id = resource_id

    try:
        policy = anyscale.policy.get(
            resource_type=resource_type, resource_id=resource_id,
        )
    except ValueError as e:
        raise UserError(f"Failed to get policy: {e}", legacy_exit_code=0) from None

    if output_format != OutputFormat.TEXT.value:
        print_output(policy, output_format)
        return

    if not policy.bindings:
        log.info(f"No policy bindings found for {resource_type} {display_id}.")
        return

    status_str = policy.sync_status.value

    log.info(f"Policy for {resource_type} {display_id}:")

    table_data = []
    for binding in policy.bindings:
        for principal in binding.principals:
            table_data.append((binding.role_name, principal, status_str))

    table = tabulate.tabulate(
        table_data, headers=["Role", "Principal (User Group ID)", "Process Status"],
    )
    rprint(table)


@command_metadata(
    status=ReleaseStatus.BETA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT, OutputFormat.JSON, OutputFormat.YAML],
    examples=[
        CommandExample(
            description="List the policies of all clouds with bindings configured.",
            command="anyscale policy list --resource-type cloud",
            output_raw=command_examples.POLICY_LIST_EXAMPLE,
            output_instance=lambda: [
                ResourcePolicy(
                    resource_id="cld_abc123",
                    resource_type="cloud",
                    bindings=[
                        PolicyBinding(
                            role_name="collaborator", principals=["ug_abc123"]
                        )
                    ],
                    sync_status=PolicySyncStatus.success,
                )
            ],
        ),
    ],
    output_schema=ResourcePolicy,
)
@policy_cli.command(
    name="list",
    short_help="List permission policies for all resources of a specific type.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "--resource-type",
    required=True,
    type=click.Choice(["cloud", "project"], case_sensitive=False),
    help="Resource type to list policies for ('cloud' or 'project').",
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
def list_policies(resource_type: str, output_format: str) -> None:
    """
    List permission policies for all resources of a specific type.

    Only shows resources that have bindings configured.
    """
    try:
        policies = anyscale.policy.list(resource_type=resource_type)
    except ValueError as e:
        raise UserError(f"Failed to list policies: {e}", legacy_exit_code=0) from None

    if output_format != OutputFormat.TEXT.value:
        print_output([p for p in policies if p.bindings], output_format)
        return

    if not policies:
        log.info(f"No {resource_type}s found.")
        return

    # Filter to only show policies with bindings
    policies_with_bindings = [p for p in policies if p.bindings]

    if not policies_with_bindings:
        log.info(f"No bindings configured for any {resource_type}s.")
        return

    for policy in policies_with_bindings:
        log.info(f"\n{policy.resource_type}: {policy.resource_id}")

        status_str = policy.sync_status.value
        table_data = []
        for binding in policy.bindings:
            for principal in binding.principals:
                table_data.append((binding.role_name, principal, status_str))
        table = tabulate.tabulate(
            table_data, headers=["Role", "Principal (User Group ID)", "Process Status"],
        )
        rprint(table)
