from typing import Dict
from typing import List
from typing import Optional

import click
from rich.panel import Panel
from rich.prompt import Confirm
from rich.prompt import IntPrompt
from rich.prompt import Prompt
from rich.text import Text

from tecton import tecton_context
from tecton._internals.infra_operations import create_feature_server_cache
from tecton._internals.infra_operations import create_feature_server_group
from tecton._internals.infra_operations import create_ingest_server_group
from tecton._internals.infra_operations import create_transform_server_group
from tecton._internals.infra_operations import delete_feature_server_cache
from tecton._internals.infra_operations import delete_feature_server_group
from tecton._internals.infra_operations import delete_ingest_server_group
from tecton._internals.infra_operations import delete_transform_server_group
from tecton._internals.infra_operations import get_feature_server_cache
from tecton._internals.infra_operations import get_feature_server_group
from tecton._internals.infra_operations import get_ingest_server_group
from tecton._internals.infra_operations import get_realtime_logs
from tecton._internals.infra_operations import get_transform_server_group
from tecton._internals.infra_operations import list_feature_server_caches
from tecton._internals.infra_operations import list_feature_server_groups
from tecton._internals.infra_operations import list_ingest_server_groups
from tecton._internals.infra_operations import list_transform_server_groups
from tecton._internals.infra_operations import update_feature_server_cache
from tecton._internals.infra_operations import update_feature_server_group
from tecton._internals.infra_operations import update_ingest_server_group
from tecton._internals.infra_operations import update_transform_server_group
from tecton.cli import printer
from tecton.cli.cli_utils import click_exception_wrapper
from tecton.cli.cli_utils import display_table
from tecton.cli.cli_utils import timestamp_to_string
from tecton.cli.command import TectonCommand
from tecton.cli.command import TectonCommandCategory
from tecton.cli.command import TectonGroup
from tecton_core.conf import STREAM_INGEST_V2_ENABLED
from tecton_core.conf import TRANSFORM_SERVER_GROUPS_ENABLED
from tecton_proto.servergroupservice.server_group_service__client_pb2 import AutoscalingConfig
from tecton_proto.servergroupservice.server_group_service__client_pb2 import FeatureServerCache
from tecton_proto.servergroupservice.server_group_service__client_pb2 import FeatureServerGroup
from tecton_proto.servergroupservice.server_group_service__client_pb2 import GetRealtimeLogsResponse
from tecton_proto.servergroupservice.server_group_service__client_pb2 import IngestServerGroup
from tecton_proto.servergroupservice.server_group_service__client_pb2 import ProvisionedScalingConfig
from tecton_proto.servergroupservice.server_group_service__client_pb2 import Status
from tecton_proto.servergroupservice.server_group_service__client_pb2 import TransformServerGroup


INFO_SIGN = "💡"


def _get_validated_workspace(workspace_name: Optional[str]) -> str:
    """Gets the workspace name, falling back to current context, and exits if none is found."""
    workspace = workspace_name or tecton_context.get_current_workspace()
    if not workspace:
        msg = "No workspace selected. Please specify a workspace with --workspace or run 'tecton workspace select <workspace>'"
        raise click.ClickException(msg)
    return workspace


def _get_scaling_config_str(
    autoscaling_config: Optional[AutoscalingConfig], provisioned_scaling_config: Optional[ProvisionedScalingConfig]
) -> str:
    if autoscaling_config is not None:
        return f"Autoscaling (Min:{autoscaling_config.min_nodes}, Max:{autoscaling_config.max_nodes})"
    elif provisioned_scaling_config:
        return f"Provisioned (Desired:{provisioned_scaling_config.desired_nodes})"
    return ""


def _get_pairs_str(pairs) -> str:
    """Convert pairs to string, handling both dict and protobuf map types."""
    if not pairs:
        return ""

    # Handle both dict and protobuf ScalarMapContainer types
    if hasattr(pairs, "items"):
        return ", ".join(f"{k}={v}" for k, v in pairs.items()) if pairs else ""
    else:
        # If pairs doesn't have items() method, try to convert to dict first
        try:
            pairs_dict = dict(pairs)
            return ", ".join(f"{k}={v}" for k, v in pairs_dict.items()) if pairs_dict else ""
        except (TypeError, ValueError):
            return str(pairs)


def _get_color_for_status(status):
    status_name = Status.Name(status)
    color_map = {"READY": "green", "CREATING": "cyan", "UPDATING": "yellow", "DELETING": "red"}
    return color_map.get(status_name, "white")


def _get_colored_status(status):
    """Get a colored status display using Rich Text formatting."""
    from rich.text import Text

    status_name = Status.Name(status)
    color = _get_color_for_status(status)
    return Text(status_name, style=color)


def _parse_pairs_str(pairs_str: Optional[str], var_name: str) -> Optional[Dict[str, str]]:
    if pairs_str is None:
        return None
    pairs = {}
    for pair in pairs_str.split(","):
        if not pair or pair.count("=") != 1:
            msg = f"Invalid {var_name} format. Expected format: KEY1=VALUE1,KEY2=VALUE2"
            raise click.ClickException(msg)
        k, v = pair.split("=")
        pairs[k] = v
    return pairs


def _prompt_for_pairs_with_validation(prompt_text: str, var_name: str) -> Optional[Dict[str, str]]:
    """
    Prompt for key-value pairs with validation and retry logic.

    Args:
        prompt_text: Text to show in the prompt
        var_name: Variable name for error messages

    Returns:
        Dictionary of parsed pairs or None if empty input
    """
    while True:
        pairs_str = Prompt.ask(prompt_text)
        if not pairs_str:
            return None

        try:
            return _parse_pairs_str(pairs_str, var_name)
        except click.ClickException as e:
            printer.rich_print(f"[bold red]{e.message}[/bold red]")
            printer.safe_print("[dim]Please try again or press Enter to skip.[/dim]")


def _confirm_retry_on_failure(retry_prompt: str) -> bool:
    """
    Helper function to ask user if they want to retry after a failure.

    Args:
        retry_prompt: Prompt to show for retry confirmation

    Returns:
        True if user wants to retry, False otherwise
    """
    printer.safe_print()
    should_retry = Confirm.ask(retry_prompt, default=True)
    if should_retry:
        printer.safe_print()  # Add space before retrying
    return should_retry


def _interactive_server_group_creation_flow(
    workspace_name: str,
    server_type: str,
    default_name_suffix: str,
    include_environment: bool,
    create_function,
    provide_name_defaults: bool = True,
):
    """
    Common interactive flow for server group creation.

    Args:
        workspace_name: The workspace name
        server_type: "Transform" or "Ingest" for display purposes
        default_name_suffix: Suffix for default name
        include_environment: Whether to prompt for environment name
        create_function: Function to call for actual creation
        provide_name_defaults: Whether to provide default values for name and description

    Returns:
        The created server group or None if canceled
    """
    while True:  # Retry loop for creation failures
        try:
            default_name = None
            if provide_name_defaults:
                default_name = f"{workspace_name}-default-{default_name_suffix}"

            while True:
                name = Prompt.ask("Server Group Name", default=default_name)
                if name is not None and name.strip():
                    break
                printer.rich_print("[bold red]Server group name cannot be empty.[/bold red]")

            if provide_name_defaults:
                description = Prompt.ask(
                    "Description", default=f"Default {server_type} Server Group for workspace {workspace_name}"
                )
            else:
                description = Prompt.ask("Description")

            printer.rich_print("\n[bold]Scaling Configuration[/bold]")
            printer.safe_print("Choose scaling type: [1] Provisioned (fixed nodes) [2] Autoscaling (min/max range)")

            scaling_choice = Prompt.ask("Scaling Type", choices=["1", "2"], default="1")

            min_nodes = max_nodes = desired_nodes = None

            if scaling_choice == "1":
                desired_nodes = IntPrompt.ask("Desired Nodes", default=1)
            else:
                min_nodes = IntPrompt.ask("Minimum Nodes", default=1)
                max_nodes = IntPrompt.ask("Maximum Nodes", default=1)

            node_type = Prompt.ask("Node Type", default="m6a.2xlarge")
            tags = _prompt_for_pairs_with_validation("Tags (format: KEY1=VALUE1,KEY2=VALUE2)", "tags")

            environment_name = None
            if include_environment:
                environment_name = Prompt.ask(
                    "Environment Name (check your workspace for available environments)", default="tecton-core-1.2.0"
                )
                env_vars = _prompt_for_pairs_with_validation(
                    "Environment Variables (format: KEY1=VALUE1,KEY2=VALUE2)", "env-vars"
                )

            printer.rich_print(f"\n[bold green]Creating {server_type} Server Group '{name}'...[/bold green]")

            try:
                create_args = {
                    "workspace": workspace_name,
                    "name": name,
                    "min_nodes": min_nodes,
                    "max_nodes": max_nodes,
                    "desired_nodes": desired_nodes,
                    "node_type": node_type,
                    "description": description,
                    "tags": tags,
                }

                if include_environment:
                    create_args["environment"] = environment_name
                    create_args["environment_variables"] = env_vars

                server_group = create_function(**create_args)

                printer.rich_print(f"[bold green]✓ {server_type} Server Group created successfully![/bold green]")
                return server_group

            except Exception as e:
                printer.rich_print(f"[bold red]✗ Failed to create {server_type} Server Group:[/bold red] {str(e)}")
                if not _confirm_retry_on_failure(
                    f"Would you like to try creating the {server_type} Server Group again?",
                ):
                    return None
                continue

        except (KeyboardInterrupt, EOFError):
            printer.rich_print(f"\n[yellow]{server_type} Server Group creation canceled.[/yellow]")
            return None


def _create_multi_line_display(
    current_value: str, pending_value: str, pending_color: str, prefix: str = "Pending"
) -> Dict:
    """Helper function to create multi-line display for current and pending values."""
    if current_value == "":
        current_value = "None"

    return {
        "type": "multi_line",
        "lines": [
            {"text": current_value, "style": "dim"},
            {"text": f"{prefix}: {pending_value}", "style": f"{pending_color}"},
        ],
    }


def _process_pending_scaling_config(current_scaling: str, pending_config, pending_color: str):
    """Process pending scaling configuration for any server group type."""
    if not pending_config:
        return current_scaling

    has_pending_scaling = pending_config.HasField("autoscaling_config") or pending_config.HasField("provisioned_config")

    if has_pending_scaling:
        pending_scaling = _get_scaling_config_str(
            pending_config.autoscaling_config if pending_config.HasField("autoscaling_config") else None,
            pending_config.provisioned_config if pending_config.HasField("provisioned_config") else None,
        )
        return _create_multi_line_display(current_scaling, pending_scaling, pending_color)

    return current_scaling


def _process_pending_field(current_value: str, pending_config, field_name: str, pending_color: str):
    """Process any pending field for display."""
    if not pending_config:
        return current_value

    # Handle map fields (like environment_variables) differently from optional fields
    if field_name == "environment_variables":
        pending_value = getattr(pending_config, field_name, {})
        if not pending_value:
            return current_value
    else:
        if not pending_config.HasField(field_name) or getattr(pending_config, field_name) == "":
            return current_value
        pending_value = getattr(pending_config, field_name)

    if isinstance(pending_value, dict):
        pending_value = _get_pairs_str(pending_value)

    return _create_multi_line_display(current_value, pending_value, pending_color)


def interactive_create_transform_server_group(
    workspace_name: str, show_description: bool = True, provide_name_defaults: bool = False
) -> Optional[TransformServerGroup]:
    """
    Interactive creation of a Transform Server Group with rich prompts.

    Args:
        workspace_name: The workspace name to create the TSG in
        show_description: Whether to show the description panel (default: True)
        provide_name_defaults: Whether to provide default values for name and description (default: False)

    Returns:
        The created TransformServerGroup or None if canceled
    """
    if show_description:
        description_panel = Panel(
            Text.assemble(
                ("Transform Server Groups\n", "bold blue"),
                (
                    "Used to execute user defined transformations for streaming and realtime feature computations.\n\n",
                    "",
                ),
                ("This will create the compute infrastructure needed for realtime feature transformations.", "dim"),
            ),
            title="About Transform Server Groups",
            border_style="blue",
            padding=(1, 2),
        )
        printer.rich_print(description_panel)
        printer.safe_print()

    return _interactive_server_group_creation_flow(
        workspace_name=workspace_name,
        server_type="Transform",
        default_name_suffix="transform-server-group",
        include_environment=True,
        create_function=create_transform_server_group,
        provide_name_defaults=provide_name_defaults,
    )


def interactive_create_ingest_server_group(
    workspace_name: str, show_description: bool = True, provide_name_defaults: bool = False
) -> Optional[IngestServerGroup]:
    """
    Interactive creation of an Ingest Server Group with rich prompts.

    Args:
        workspace_name: The workspace name to create the ISG in
        show_description: Whether to show the description panel (default: True)
        provide_name_defaults: Whether to provide default values for name and description (default: False)

    Returns:
        The created IngestServerGroup or None if canceled
    """
    if show_description:
        description_panel = Panel(
            Text.assemble(
                ("Ingest Server Groups\n", "bold green"),
                ("Used to ingest streaming data for Tecton's Stream Ingest API.\n\n", ""),
                ("This will create the compute infrastructure needed for streaming data ingestion.", "dim"),
            ),
            title="About Ingest Server Groups",
            border_style="green",
            padding=(1, 2),
        )
        printer.rich_print(description_panel)
        printer.safe_print()

    return _interactive_server_group_creation_flow(
        workspace_name=workspace_name,
        server_type="Ingest",
        default_name_suffix="ingest-server-group",
        include_environment=False,
        create_function=create_ingest_server_group,
        provide_name_defaults=provide_name_defaults,
    )


@click.command(
    "feature-server-cache",
    cls=TectonGroup,
    command_category=TectonCommandCategory.INFRA,
    hidden=True,
)
def feature_server_cache():
    """Provision and manage Feature Server Caches."""


def _extract_metadata(obj):
    """Extract description and tags from metadata field."""
    description = ""
    tags = {}
    if obj.HasField("metadata"):
        description = obj.metadata.description if obj.metadata.HasField("description") else ""
        tags = obj.metadata.tags
    return description, tags


def _extract_server_fields(server_or_servers, columnar=False, field_config=None):
    """
    Generic function to extract fields for any server type display.

    Args:
        server_or_servers: Single server object or list of servers
        columnar: Whether this is for columnar display (Field | Value format)
        field_config: Dictionary containing field extraction configuration
    """
    if field_config is None:
        field_config = {}

    if columnar:
        server = server_or_servers
        data = []

        data.extend(
            [
                ("ID", server.id),
                ("Workspace", server.workspace),
                ("Name", server.name),
                ("Status", _get_colored_status(server.status)),
                ("Status Details", server.status_details or ""),
            ]
        )

        if field_config.get("has_scaling", True):
            current_scaling = _get_scaling_config_str(
                getattr(server, "autoscaling_config", None) if server.HasField("autoscaling_config") else None,
                getattr(server, "provisioned_config", None) if server.HasField("provisioned_config") else None,
            )
            pending_config = getattr(server, "pending_config", None) if server.HasField("pending_config") else None
            pending_color = _get_color_for_status(server.status)
            scaling_display = _process_pending_scaling_config(current_scaling, pending_config, pending_color)
            data.append(("Scaling", scaling_display))

        if field_config.get("has_node_type", True):
            pending_config = getattr(server, "pending_config", None) if server.HasField("pending_config") else None
            pending_color = _get_color_for_status(server.status)
            node_type_display = _process_pending_field(server.node_type, pending_config, "node_type", pending_color)
            data.append(("Node Type", node_type_display))

        if field_config.get("has_cache_fields", False):
            data.extend(
                [
                    ("Num Shards", server.provisioned_config.num_shards),
                    ("Num Replicas", server.provisioned_config.num_replicas_per_shard),
                    ("Preferred Maintenance Window", server.preferred_maintenance_window or ""),
                ]
            )

        if field_config.get("has_cache_id", False):
            data.extend(
                [
                    ("Cache ID", server.cache_id or ""),
                ]
            )

        if field_config.get("has_environment", False):
            current_env_vars = _get_pairs_str(server.environment_variables)
            pending_config = getattr(server, "pending_config", None) if server.HasField("pending_config") else None
            pending_color = _get_color_for_status(server.status)
            environment_display = _process_pending_field(
                server.environment, pending_config, "environment", pending_color
            )
            env_vars_display = _process_pending_field(
                current_env_vars, pending_config, "environment_variables", pending_color
            )
            data.extend(
                [
                    ("Environment", environment_display),
                    ("Environment Variables", env_vars_display),
                ]
            )

        if field_config.get("has_metadata", True):
            description, tags = _extract_metadata(server)
            data.extend(
                [
                    ("Description", description),
                    ("Tags", _get_pairs_str(tags)),
                ]
            )

        data.extend(
            [
                ("Created At", timestamp_to_string(server.created_at)),
                ("Updated At", timestamp_to_string(server.updated_at)),
            ]
        )

        headings = ["Field", "Value"]
        return headings, data

    else:
        # Multi-item display
        headings = field_config.get("multi_headings", ["ID", "Workspace", "Name", "Status", "Updated At"])

        rows = []
        for server in server_or_servers:
            row_data = []

            for heading in headings:
                if heading == "ID":
                    row_data.append(server.id)
                elif heading == "Workspace":
                    row_data.append(server.workspace)
                elif heading == "Name":
                    row_data.append(server.name)
                elif heading == "Status":
                    row_data.append(_get_colored_status(server.status))
                elif heading == "Scaling":
                    current_scaling = _get_scaling_config_str(
                        getattr(server, "autoscaling_config", None) if server.HasField("autoscaling_config") else None,
                        getattr(server, "provisioned_config", None) if server.HasField("provisioned_config") else None,
                    )
                    pending_config = (
                        getattr(server, "pending_config", None) if server.HasField("pending_config") else None
                    )
                    pending_color = _get_color_for_status(server.status)
                    row_data.append(_process_pending_scaling_config(current_scaling, pending_config, pending_color))
                elif heading == "Node Type":
                    pending_config = (
                        getattr(server, "pending_config", None) if server.HasField("pending_config") else None
                    )
                    pending_color = _get_color_for_status(server.status)
                    row_data.append(
                        _process_pending_field(server.node_type, pending_config, "node_type", pending_color)
                    )
                elif heading == "Cache ID":
                    row_data.append(server.cache_id or "")
                elif heading == "Pending Config":
                    row_data.append(server.pending_config or "")
                elif heading == "Num Shards":
                    row_data.append(server.provisioned_config.num_shards)
                elif heading == "Num Replicas":
                    row_data.append(server.provisioned_config.num_replicas_per_shard)
                elif heading == "Preferred Maintenance Window":
                    row_data.append(server.preferred_maintenance_window or "")
                elif heading == "Environment":
                    pending_config = (
                        getattr(server, "pending_config", None) if server.HasField("pending_config") else None
                    )
                    pending_color = _get_color_for_status(server.status)
                    row_data.append(
                        _process_pending_field(server.environment, pending_config, "environment", pending_color)
                    )
                elif heading == "Environment Variables":
                    current_env_vars = _get_pairs_str(server.environment_variables)
                    pending_config = (
                        getattr(server, "pending_config", None) if server.HasField("pending_config") else None
                    )
                    pending_color = _get_color_for_status(server.status)
                    row_data.append(
                        _process_pending_field(current_env_vars, pending_config, "environment_variables", pending_color)
                    )
                elif heading == "Description":
                    description, _ = _extract_metadata(server)
                    row_data.append(description)
                elif heading == "Tags":
                    _, tags = _extract_metadata(server)
                    row_data.append(_get_pairs_str(tags))
                elif heading == "Updated At":
                    row_data.append(timestamp_to_string(server.updated_at))
                else:
                    row_data.append("")

            rows.append(tuple(row_data))

        return headings, rows


def print_feature_server_caches(caches: List[FeatureServerCache], columnar: bool = False):
    """Print Feature Server Caches in columnar or multi-item format."""
    FEATURE_SERVER_CACHE_CONFIG = {
        "has_scaling": False,
        "has_node_type": False,
        "has_cache_fields": True,
        "has_metadata": True,
        "multi_headings": [
            "ID",
            "Workspace",
            "Name",
            "Status",
            "Num Shards",
            "Num Replicas",
            "Preferred Maintenance Window",
            "Pending Config",
            "Description",
            "Tags",
            "Updated At",
        ],
    }

    if columnar and len(caches) == 1:
        headings, rows = _extract_server_fields(caches[0], columnar=True, field_config=FEATURE_SERVER_CACHE_CONFIG)
    else:
        headings, rows = _extract_server_fields(caches, columnar=False, field_config=FEATURE_SERVER_CACHE_CONFIG)

    display_table(headings, rows, title="Feature Server Caches", show_lines=True)


def print_feature_server_groups(fsgs: List[FeatureServerGroup], columnar: bool = False):
    """Print Feature Server Groups in columnar or multi-item format."""
    FEATURE_SERVER_GROUP_CONFIG = {
        "has_scaling": True,
        "has_node_type": True,
        "has_cache_id": True,
        "has_metadata": True,
        "multi_headings": [
            "ID",
            "Workspace",
            "Name",
            "Status",
            "Scaling",
            "Node Type",
            "Cache ID",
            "Pending Config",
            "Description",
            "Tags",
            "Updated At",
        ],
    }

    if columnar and len(fsgs) == 1:
        headings, rows = _extract_server_fields(fsgs[0], columnar=True, field_config=FEATURE_SERVER_GROUP_CONFIG)
    else:
        headings, rows = _extract_server_fields(fsgs, columnar=False, field_config=FEATURE_SERVER_GROUP_CONFIG)

    display_table(headings, rows, title="Feature Server Groups", show_lines=True)


def print_ingest_server_groups(isgs: List[IngestServerGroup], columnar: bool = False):
    """Print Ingest Server Groups in columnar or multi-item format."""
    if not isgs:
        printer.safe_print("No Ingest Server Groups found")
        return

    INGEST_SERVER_GROUP_CONFIG = {
        "has_scaling": True,
        "has_node_type": True,
        "has_metadata": True,
        "multi_headings": [
            "ID",
            "Workspace",
            "Name",
            "Status",
            "Scaling",
            "Node Type",
            "Description",
            "Tags",
            "Updated At",
        ],
    }

    if columnar:
        title = f"Ingest Server Group: {isgs[0].name}"
    else:
        title = "Ingest Server Groups"

    if columnar and len(isgs) == 1:
        headings, rows = _extract_server_fields(isgs[0], columnar=True, field_config=INGEST_SERVER_GROUP_CONFIG)
    else:
        headings, rows = _extract_server_fields(isgs, columnar=False, field_config=INGEST_SERVER_GROUP_CONFIG)

    display_table(headings, rows, title=title, show_lines=True)


def print_transform_server_groups(tsgs: List[TransformServerGroup], columnar: bool = False):
    """Print Transform Server Groups in columnar or multi-item format."""
    if not tsgs:
        printer.safe_print("No Transform Server Groups found")
        return

    TRANSFORM_SERVER_GROUP_CONFIG = {
        "has_scaling": True,
        "has_node_type": True,
        "has_environment": True,
        "has_metadata": True,
        "multi_headings": [
            "ID",
            "Workspace",
            "Name",
            "Status",
            "Scaling",
            "Node Type",
            "Environment",
            "Environment Variables",
            "Description",
            "Tags",
            "Updated At",
        ],
    }

    if columnar and len(tsgs) == 1:
        headings, rows = _extract_server_fields(tsgs[0], columnar=True, field_config=TRANSFORM_SERVER_GROUP_CONFIG)
    else:
        headings, rows = _extract_server_fields(tsgs, columnar=False, field_config=TRANSFORM_SERVER_GROUP_CONFIG)

    if columnar:
        title = f"Transform Server Group: {tsgs[0].name}"
    else:
        title = "Transform Server Groups"

    display_table(headings, rows, title=title, show_lines=True)


@feature_server_cache.command("create", requires_auth=True, cls=TectonCommand)
@click.option("--name", help="Name of the cache", required=True, type=str)
@click.option("--num-shards", help="Number of shards", required=True, type=int)
@click.option("--num-replicas-per-shard", help="Number of replicas per shard", required=True, type=int)
@click.option(
    "--preferred-maintenance-window",
    help="Preferred maintenance window (format: ddd:hh24:mi-ddd:hh24:mi)",
    required=False,
    type=str,
)
@click.option("--description", help="Description of the cache", required=False, type=str)
@click.option("--tags", help="Tags for the cache", required=False, type=str)
@click.option("--workspace", help="Workspace name", required=False, type=str)
@click_exception_wrapper
def create_feature_server_cache_cmd(
    name: str,
    num_shards: int,
    num_replicas_per_shard: int,
    preferred_maintenance_window: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[str] = None,
    workspace: Optional[str] = None,
):
    """Create a new Feature Server Cache."""
    workspace = _get_validated_workspace(workspace)

    tags = _parse_pairs_str(tags, "tags")

    cache = create_feature_server_cache(
        workspace=workspace,
        name=name,
        num_shards=num_shards,
        num_replicas_per_shard=num_replicas_per_shard,
        preferred_maintenance_window=preferred_maintenance_window,
        description=description,
        tags=tags,
    )

    print_feature_server_caches([cache], columnar=True)


@feature_server_cache.command("get", requires_auth=True, cls=TectonCommand)
@click.option("--id", help="ID of the cache", required=True, type=str)
@click_exception_wrapper
def get_feature_server_cache_cmd(id: str):
    """Get a Feature Server Cache by ID."""
    cache = get_feature_server_cache(id=id)

    print_feature_server_caches([cache], columnar=True)


@feature_server_cache.command("list", requires_auth=True, cls=TectonCommand)
@click.option("--workspace", help="Workspace name", required=False, type=str)
@click_exception_wrapper
def list_feature_server_caches_cmd(workspace: Optional[str] = None):
    """List all Feature Server Caches."""
    workspace = _get_validated_workspace(workspace)

    response = list_feature_server_caches(workspace=workspace)

    print_feature_server_caches(response.caches)


@feature_server_cache.command("update", requires_auth=True, cls=TectonCommand)
@click.option("--id", help="ID of the cache", required=True, type=str)
@click.option("--num-shards", help="Number of shards", required=False, type=int)
@click.option("--num-replicas-per-shard", help="Number of replicas per shard", required=False, type=int)
@click.option("--preferred-maintenance-window", help="Preferred maintenance window", required=False, type=str)
@click.option("--description", help="Description of the cache", required=False, type=str)
@click.option("--tags", help="Tags for the cache", required=False, type=str)
@click_exception_wrapper
def update_feature_server_cache_cmd(
    id: str,
    num_shards: Optional[int] = None,
    num_replicas_per_shard: Optional[int] = None,
    preferred_maintenance_window: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[str] = None,
):
    """Update a Feature Server Cache."""
    cache = update_feature_server_cache(
        id=id,
        num_shards=num_shards,
        num_replicas_per_shard=num_replicas_per_shard,
        preferred_maintenance_window=preferred_maintenance_window,
        description=description,
        tags=_parse_pairs_str(tags, "tags") or {},
    )
    print_feature_server_caches([cache], columnar=True)


@feature_server_cache.command("delete", requires_auth=True, cls=TectonCommand)
@click.option("--id", help="ID of the cache", required=True, type=str)
@click_exception_wrapper
def delete_feature_server_cache_cmd(id: str):
    """Delete a Feature Server Cache by ID."""
    delete_feature_server_cache(id=id)
    printer.safe_print(f"Deleted Feature Server Cache with ID {id}")


@click.command(
    "feature-server-group",
    cls=TectonGroup,
    command_category=TectonCommandCategory.INFRA,
    hidden=True,
)
def feature_server_group():
    """Provision and manage Feature Server Groups."""


@feature_server_group.command("create", requires_auth=True, cls=TectonCommand)
@click.option("--name", help="Name of the server group", required=True, type=str)
@click.option("--cache-id", help="ID of the Feature Server Cache to use", required=False, type=str)
@click.option("--min-nodes", help="Minimum number of nodes for autoscaling", required=False, type=int)
@click.option("--max-nodes", help="Maximum number of nodes for autoscaling", required=False, type=int)
@click.option("--desired-nodes", help="Fixed number of nodes for provisioned scaling", required=False, type=int)
@click.option("--node-type", help="EC2 instance type", required=False, type=str)
@click.option("--description", help="Description of the server group", required=False, type=str)
@click.option("--tags", help="Tags for the server group", required=False, type=str)
@click.option("--workspace", help="Workspace name", required=False, type=str)
@click_exception_wrapper
def create_feature_server_group_cmd(
    name: str,
    cache_id: Optional[str] = None,
    min_nodes: Optional[int] = None,
    max_nodes: Optional[int] = None,
    desired_nodes: Optional[int] = None,
    node_type: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[str] = None,
    workspace: Optional[str] = None,
):
    """Create a new Feature Server Group."""
    workspace = _get_validated_workspace(workspace)

    server_group = create_feature_server_group(
        workspace=workspace,
        name=name,
        cache_id=cache_id,
        min_nodes=min_nodes,
        max_nodes=max_nodes,
        desired_nodes=desired_nodes,
        node_type=node_type,
        description=description,
        tags=_parse_pairs_str(tags, "tags") or {},
    )

    print_feature_server_groups([server_group], columnar=True)


@feature_server_group.command("get", requires_auth=True, cls=TectonCommand)
@click.option("--id", help="ID of the server group", required=True, type=str)
@click_exception_wrapper
def get_feature_server_group_cmd(id: str):
    """Get a Feature Server Group by ID."""
    server_group = get_feature_server_group(id=id)

    print_feature_server_groups([server_group], columnar=True)


@feature_server_group.command("list", requires_auth=True, cls=TectonCommand)
@click.option("--workspace", help="Workspace name", required=False, type=str)
@click_exception_wrapper
def list_feature_server_groups_cmd(workspace: Optional[str] = None):
    """List all Feature Server Groups."""
    workspace = _get_validated_workspace(workspace)

    response = list_feature_server_groups(workspace=workspace)

    print_feature_server_groups(list(response.feature_server_groups))


@feature_server_group.command("update", requires_auth=True, cls=TectonCommand)
@click.option("--id", help="ID of the server group", required=True, type=str)
@click.option("--min-nodes", help="Minimum number of nodes for autoscaling", required=False, type=int)
@click.option("--max-nodes", help="Maximum number of nodes for autoscaling", required=False, type=int)
@click.option("--desired-nodes", help="Fixed number of nodes for provisioned scaling", required=False, type=int)
@click.option("--node-type", help="EC2 instance type", required=False, type=str)
@click.option("--description", help="Description of the server group", required=False, type=str)
@click.option("--tags", help="Tags to add to the server group", required=False, type=str)
@click_exception_wrapper
def update_feature_server_group_cmd(
    id: str,
    min_nodes: Optional[int] = None,
    max_nodes: Optional[int] = None,
    desired_nodes: Optional[int] = None,
    node_type: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[str] = None,
):
    """Update a Feature Server Group."""
    server_group = update_feature_server_group(
        id=id,
        min_nodes=min_nodes,
        max_nodes=max_nodes,
        desired_nodes=desired_nodes,
        node_type=node_type,
        description=description,
        tags=_parse_pairs_str(tags, "tags") or {},
    )
    print_feature_server_groups([server_group])


@feature_server_group.command("delete", requires_auth=True, cls=TectonCommand)
@click.option("--id", help="ID of the server group", required=True, type=str)
@click_exception_wrapper
def delete_feature_server_group_cmd(id: str):
    """Delete a Feature Server Group by ID."""
    delete_feature_server_group(id=id)
    printer.safe_print(f"Deleted Feature Server Group with ID {id}")


@click.command(
    "ingest-server-group",
    cls=TectonGroup,
    command_category=TectonCommandCategory.INFRA,
    feature_flag=STREAM_INGEST_V2_ENABLED,
)
def ingest_server_group():
    """Provision and manage Ingest Server Groups.

    This command can also be called using the alias 'isg'.
    """


def _validate_scaling_params(min_nodes: Optional[int], max_nodes: Optional[int], desired_nodes: Optional[int]):
    if (min_nodes is None and max_nodes is None) and desired_nodes is None:
        msg = "Please specify either `min-nodes` and `max-nodes` for autoscaling or `desired-nodes` for provisioned scaling."
        raise click.ClickException(msg)
    if (min_nodes is not None and max_nodes is None) or (min_nodes is None and max_nodes is not None):
        msg = "Both min-nodes and max-nodes must be specified together for autoscaling."
        raise click.ClickException(msg)
    if (min_nodes is not None or max_nodes is not None) and desired_nodes is not None:
        msg = (
            "Either specify min-nodes and max-nodes for autoscaling or desired-nodes for provisioned scaling, not both."
        )
        raise click.ClickException(msg)


@ingest_server_group.command("create", requires_auth=True, cls=TectonCommand)
@click.option("--name", help="Name of the server group", required=False, type=str)
@click.option("--min-nodes", help="Minimum number of nodes for autoscaling", required=False, type=int)
@click.option("--max-nodes", help="Maximum number of nodes for autoscaling", required=False, type=int)
@click.option("--desired-nodes", help="Fixed number of nodes for provisioned scaling", required=False, type=int)
@click.option("--node-type", help="EC2 instance type", required=False, type=str)
@click.option("--description", help="Description of the server group", required=False, type=str)
@click.option("--tags", help="Tags to add to the server group", required=False, type=str)
@click.option("--workspace", help="Workspace name", required=False, type=str)
@click.option("-i", "--interactive", is_flag=True, help="Go through a step-by-step server group creation process")
@click_exception_wrapper
def create_ingest_server_group_cmd(
    name: Optional[str] = None,
    min_nodes: Optional[int] = None,
    max_nodes: Optional[int] = None,
    desired_nodes: Optional[int] = None,
    node_type: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[str] = None,
    workspace: Optional[str] = None,
    interactive: bool = False,
):
    """Create a new Ingest Server Group."""
    workspace = _get_validated_workspace(workspace)

    has_flags = any(
        [
            name is not None,
            min_nodes is not None,
            max_nodes is not None,
            desired_nodes is not None,
            node_type is not None,
            description is not None,
            tags is not None,
        ]
    )

    should_use_interactive = interactive or not has_flags

    if should_use_interactive:
        server_group = interactive_create_ingest_server_group(workspace)
        if server_group is not None:
            print_ingest_server_groups([server_group], columnar=True)
        return

    if name is None:
        msg = "Missing required parameter '--name'."
        raise click.ClickException(msg)

    _validate_scaling_params(min_nodes, max_nodes, desired_nodes)

    server_group = create_ingest_server_group(
        workspace=workspace,
        name=name,
        min_nodes=min_nodes,
        max_nodes=max_nodes,
        desired_nodes=desired_nodes,
        node_type=node_type,
        description=description,
        tags=_parse_pairs_str(tags, "tags") or {},
    )

    print_ingest_server_groups([server_group], columnar=True)


@ingest_server_group.command("get", requires_auth=True, cls=TectonCommand)
@click.option("--id", help="ID of the server group", required=True, type=str)
@click_exception_wrapper
def get_ingest_server_group_cmd(id: str):
    """Get an Ingest Server Group by ID."""
    server_group = get_ingest_server_group(id=id)

    print_ingest_server_groups([server_group], columnar=True)


@ingest_server_group.command("list", requires_auth=True, cls=TectonCommand)
@click.option("--workspace", help="Workspace name", required=False, type=str)
@click_exception_wrapper
def list_ingest_server_groups_cmd(workspace: Optional[str] = None):
    """List all Ingest Server Groups."""
    workspace = _get_validated_workspace(workspace)

    response = list_ingest_server_groups(workspace=workspace)
    print_ingest_server_groups(list(response.ingest_server_groups))


@ingest_server_group.command("update", requires_auth=True, cls=TectonCommand)
@click.option("--id", help="ID of the server group", required=True, type=str)
@click.option("--min-nodes", help="Minimum number of nodes for autoscaling", required=False, type=int)
@click.option("--max-nodes", help="Maximum number of nodes for autoscaling", required=False, type=int)
@click.option("--desired-nodes", help="Fixed number of nodes for provisioned scaling", required=False, type=int)
@click.option("--node-type", help="EC2 instance type", required=False, type=str)
@click.option("--description", help="Description of the server group", required=False, type=str)
@click.option("--tags", help="Tags to add to the server group", required=False, type=str)
@click_exception_wrapper
def update_ingest_server_group_cmd(
    id: str,
    min_nodes: Optional[int] = None,
    max_nodes: Optional[int] = None,
    desired_nodes: Optional[int] = None,
    node_type: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[str] = None,
):
    """Update an Ingest Server Group."""
    server_group = update_ingest_server_group(
        id=id,
        min_nodes=min_nodes,
        max_nodes=max_nodes,
        desired_nodes=desired_nodes,
        node_type=node_type,
        description=description,
        tags=_parse_pairs_str(tags, "tags") or {},
    )

    print_ingest_server_groups([server_group], columnar=True)


@ingest_server_group.command("delete", requires_auth=True, cls=TectonCommand)
@click.option("--id", help="ID of the server group", required=True, type=str)
@click_exception_wrapper
def delete_ingest_server_group_cmd(id: str):
    """Delete an Ingest Server Group by ID."""
    delete_ingest_server_group(id=id)
    printer.safe_print(f"Deleted Ingest Server Group with ID {id}")


@click.command(
    "transform-server-group",
    cls=TectonGroup,
    command_category=TectonCommandCategory.INFRA,
    feature_flag=TRANSFORM_SERVER_GROUPS_ENABLED,
)
def transform_server_group():
    """Provision and manage Transform Server Groups."""


@transform_server_group.command("create", requires_auth=True, cls=TectonCommand)
@click.option("--name", help="Name of the server group", required=False, type=str)
@click.option("--environment-name", help="Name of the Python environment to use", required=False, type=str)
@click.option("--min-nodes", help="Minimum number of nodes for autoscaling", required=False, type=int)
@click.option("--max-nodes", help="Maximum number of nodes for autoscaling", required=False, type=int)
@click.option("--desired-nodes", help="Fixed number of nodes for provisioned scaling", required=False, type=int)
@click.option("--node-type", help="EC2 instance type", required=False, type=str)
@click.option("--description", help="Description of the server group", required=False, type=str)
@click.option(
    "--tags", help="Tags to add to the server group in the format TAG1=VALUE1,TAG2=VALUE2", required=False, type=str
)
@click.option("--env-vars", help="Environment variable in the format KEY1=VALUE1,KEY2=VALUE2", required=False, type=str)
@click.option("--workspace", help="Workspace name", required=False, type=str)
@click.option("-i", "--interactive", is_flag=True, help="Go through a step-by-step server group creation process")
@click_exception_wrapper
def create_transform_server_group_cmd(
    name: Optional[str] = None,
    environment_name: Optional[str] = None,
    min_nodes: Optional[int] = None,
    max_nodes: Optional[int] = None,
    desired_nodes: Optional[int] = None,
    node_type: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[str] = None,
    env_vars: Optional[str] = None,
    workspace: Optional[str] = None,
    interactive: bool = False,
):
    """Create a new Transform Server Group."""
    workspace = _get_validated_workspace(workspace)

    has_flags = any(
        [
            name is not None,
            environment_name is not None,
            min_nodes is not None,
            max_nodes is not None,
            desired_nodes is not None,
            node_type is not None,
            description is not None,
            tags is not None,
            env_vars is not None,
        ]
    )

    should_use_interactive = interactive or not has_flags

    if should_use_interactive:
        server_group = interactive_create_transform_server_group(workspace)
        if server_group is not None:
            print_transform_server_groups([server_group], columnar=True)
        return

    if name is None:
        msg = "Missing required parameter '--name'."
        raise click.ClickException(msg)
    if environment_name is None:
        msg = "Missing required parameter '--environment-name'."
        raise click.ClickException(msg)

    _validate_scaling_params(min_nodes, max_nodes, desired_nodes)

    server_group = create_transform_server_group(
        workspace=workspace,
        name=name,
        environment=environment_name,
        min_nodes=min_nodes,
        max_nodes=max_nodes,
        desired_nodes=desired_nodes,
        node_type=node_type,
        description=description,
        tags=_parse_pairs_str(tags, "tags") or {},
        environment_variables=_parse_pairs_str(env_vars, "env-vars") or {},
    )

    print_transform_server_groups([server_group], columnar=True)


@transform_server_group.command("get", requires_auth=True, cls=TectonCommand)
@click.option("--id", help="ID of the server group", required=True, type=str)
@click_exception_wrapper
def get_transform_server_group_cmd(id: str):
    """Get a Transform Server Group by ID."""
    server_group = get_transform_server_group(id=id)

    print_transform_server_groups([server_group], columnar=True)


@transform_server_group.command("list", requires_auth=True, cls=TectonCommand)
@click.option("--workspace", help="Workspace name", required=False, type=str)
@click_exception_wrapper
def list_transform_server_groups_cmd(workspace: Optional[str] = None):
    """List all Transform Server Groups."""
    workspace = _get_validated_workspace(workspace)

    response = list_transform_server_groups(workspace=workspace)

    print_transform_server_groups(list(response.transform_server_groups))


@transform_server_group.command("update", requires_auth=True, cls=TectonCommand)
@click.option("--id", help="ID of the server group", required=True, type=str)
@click.option("--environment-name", help="Name of the Python environment to use", required=False, type=str)
@click.option("--min-nodes", help="Minimum number of nodes for autoscaling", required=False, type=int)
@click.option("--max-nodes", help="Maximum number of nodes for autoscaling", required=False, type=int)
@click.option("--desired-nodes", help="Fixed number of nodes for provisioned scaling", required=False, type=int)
@click.option("--node-type", help="EC2 instance type", required=False, type=str)
@click.option("--description", help="Description of the server group", required=False, type=str)
@click.option(
    "--tags", help="Tags to add to the server group in the format TAG1=VALUE1,TAG2=VALUE2", required=False, type=str
)
@click.option("--env-vars", help="Environment variable in the format KEY1=VALUE1,KEY2=VALUE2", required=False, type=str)
@click_exception_wrapper
def update_transform_server_group_cmd(
    id: str,
    environment_name: Optional[str] = None,
    min_nodes: Optional[int] = None,
    max_nodes: Optional[int] = None,
    desired_nodes: Optional[int] = None,
    node_type: Optional[str] = None,
    description: Optional[str] = None,
    tags: Optional[str] = None,
    env_vars: Optional[str] = None,
):
    """Update a Transform Server Group."""
    server_group = update_transform_server_group(
        id=id,
        environment=environment_name,
        min_nodes=min_nodes,
        max_nodes=max_nodes,
        desired_nodes=desired_nodes,
        node_type=node_type,
        description=description,
        tags=_parse_pairs_str(tags, "tags") or {},
        environment_variables=_parse_pairs_str(env_vars, "env-vars") or {},
    )
    print_transform_server_groups([server_group], columnar=True)


@transform_server_group.command("delete", requires_auth=True, cls=TectonCommand)
@click.option("--id", help="ID of the server group", required=True, type=str)
@click_exception_wrapper
def delete_transform_server_group_cmd(id: str):
    """Delete a Transform Server Group by ID."""
    delete_transform_server_group(id=id)
    printer.safe_print(f"Deleted Transform Server Group with ID {id}")


def _display_realtime_logs(response: GetRealtimeLogsResponse):
    if not response.logs:
        printer.safe_print("No data to display")
        return

    display_table(
        headings=["Timestamp", "Node", "Message"],
        display_rows=[(log.timestamp.ToJsonString(), log.node, log.message) for log in response.logs],
        center_align=False,
    )

    if response.warnings:
        printer.safe_print(f"{INFO_SIGN} WARNING: {response.warnings}")


@transform_server_group.command("logs", requires_auth=True, cls=TectonCommand)
@click.option("--id", help="ID of the transform server group", required=True, type=str)
@click.option(
    "-s",
    "--start",
    help="Start timestamp filter, in ISO 8601 format with UTC zone (YYYY-MM-DDThh:mm:ss.SSSSSSZ). Microseconds optional. Defaults to the one day prior to the current time if both start and end time are not specified.",
    required=False,
    type=str,
)
@click.option(
    "-e",
    "--end",
    help="End timestamp filter, in ISO 8601 format with UTC zone (YYYY-MM-DDThh:mm:ss.SSSSSSZ). Microseconds optional. Defaults to the current time if both start and end time are not specified.",
    required=False,
    type=str,
)
@click.option("-t", "--tail", help="Tail number of logs to return (max/default 100)", required=False, type=int)
@click_exception_wrapper
def logs(id: str, start: Optional[str] = None, end: Optional[str] = None, tail: Optional[int] = None):
    server_group_logs = get_realtime_logs(id, start, end, tail)
    _display_realtime_logs(server_group_logs)


@click.command(name="isg", hidden=True, cls=TectonGroup, feature_flag=STREAM_INGEST_V2_ENABLED)
def isg():
    """Provision and manage Ingest Server Groups."""


isg.add_command(create_ingest_server_group_cmd)
isg.add_command(get_ingest_server_group_cmd)
isg.add_command(list_ingest_server_groups_cmd)
isg.add_command(update_ingest_server_group_cmd)
isg.add_command(delete_ingest_server_group_cmd)


@click.command(name="tsg", hidden=True, cls=TectonGroup, feature_flag=TRANSFORM_SERVER_GROUPS_ENABLED)
def tsg():
    """Provision and manage Transform Server Groups."""


tsg.add_command(create_transform_server_group_cmd)
tsg.add_command(get_transform_server_group_cmd)
tsg.add_command(list_transform_server_groups_cmd)
tsg.add_command(update_transform_server_group_cmd)
tsg.add_command(delete_transform_server_group_cmd)
tsg.add_command(logs)
