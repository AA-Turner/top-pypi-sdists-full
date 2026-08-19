from datetime import datetime, timezone
from io import StringIO
import pathlib
import re
import secrets
from typing import Any, Dict, List, Optional

import click
from rich.console import Console
from rich.table import Table
import yaml

import anyscale
from anyscale.cli_logger import BlockLogger
from anyscale.client.openapi_client.models import (
    AWSConfig,
    AzureConfig,
    CloudDeployment,
    CloudProviders,
    ClusterManagementStackVersions,
    ConnectorConfig,
    FileStorage,
    GCPConfig,
    KubernetesConfig,
    NetworkingMode,
    NFSMountTarget,
    ObjectStorage,
)
from anyscale.client.openapi_client.models.compute_stack import ComputeStack
from anyscale.cloud.models import (
    Cloud,
    CloudInfo,
    CloudProvider,
    ComputeStack as CloudModelComputeStack,
    CreateCloudCollaborator,
    CreateCloudCollaborators,
)
from anyscale.cloud_utils import get_cloud_id_and_name, get_organization_id
from anyscale.commands import command_examples
from anyscale.commands.doc_metadata import (
    command_metadata,
    CommandExample,
    ReleaseStatus,
)
from anyscale.commands.list_util import (
    display_list,
    MAX_PAGE_SIZE,
    NON_INTERACTIVE_DEFAULT_MAX_ITEMS,
    resolve_interactive,
    validate_page_size,
)
from anyscale.commands.output_format import (
    OUTPUT_FLAG,
    OUTPUT_FLAG_LONG,
    OutputFormat,
    print_output,
    warn_deprecated_flag,
)
from anyscale.commands.setup_k8s import (
    setup_kubernetes_cloud,
    setup_kubernetes_cloud_resource,
)
from anyscale.commands.util import AnyscaleCommand, OptionPromptNull
from anyscale.controllers.cloud_controller import CloudController
from anyscale.errors import InvalidConfigError, ResourceNotFoundError, UserError
from anyscale.util import (
    _apn_boto3_session,
    allow_optional_file_storage,
    get_endpoint,
    SharedStorageType,
    validate_non_negative_arg,
)
from anyscale.utils.azure_util import disabled_on_azure
from anyscale.utils.cloud_utils import (
    placeholder_credential_problems,
    validate_aws_credentials,
)
from anyscale.utils.imports.gcp import (
    try_import_gcp_managed_setup_utils,
    try_import_gcp_utils,
)


log = BlockLogger()  # CLI Logger

# The providers `cloud register` can route. Narrower than CloudProviders, which
# also carries CLOUDGATEWAY and PCP.
_REGISTER_PROVIDERS = ("aws", "gcp", "azure", "generic")


def setup_vm_cloud_resource(  # noqa: PLR0912, PLR0913
    provider: str,
    region: str,
    cloud_name: Optional[str],
    cloud_id: Optional[str],
    project_id: Optional[str],
    enable_head_node_fault_tolerance: bool,
    shared_storage: SharedStorageType,
    controller: Optional[CloudController] = None,
    boto3_session: Optional[Any] = None,
    anyscale_iam_role_name: Optional[str] = None,
    cluster_node_iam_role_name: Optional[str] = None,
    anyscale_access_service_account: Optional[str] = None,
    pool_name: Optional[str] = None,
) -> None:
    """Set up VM cloud resources for an existing Anyscale cloud."""
    if not cloud_name and not cloud_id:
        raise click.ClickException("Either --cloud or --cloud-id is required.")

    if controller is None:
        controller = CloudController()

    resolved_cloud_id, resolved_cloud_name = get_cloud_id_and_name(
        api_client=controller.api_client, cloud_id=cloud_id, cloud_name=cloud_name,
    )

    controller.log.info(
        f"Adding VM resources to cloud '{resolved_cloud_name}' ({resolved_cloud_id})"
    )

    if provider == "aws":
        if boto3_session is None:
            boto3_session = _apn_boto3_session(region_name=region)
        if not validate_aws_credentials(controller.log, boto3_session):
            raise click.ClickException(
                "Cloud setup requires valid AWS credentials to be set locally. "
                "Learn more: https://boto3.amazonaws.com/v1/documentation/api/latest/guide/credentials.html"
            )

        resource_id = f"vm-{region}-{secrets.token_hex(4)}"
        if anyscale_iam_role_name is None:
            anyscale_iam_role_name = f"anyscale-iam-role-{secrets.token_hex(4)}"
        if cluster_node_iam_role_name is None:
            cluster_node_iam_role_name = f"{resource_id}-cluster_node_role"

        try:
            anyscale_aws_account = (
                controller.api_client.get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get().result.anyscale_aws_account
            )
            cfn_stack = controller.run_cloudformation(
                region=region,
                cloud_id=resolved_cloud_id,
                anyscale_iam_role_name=anyscale_iam_role_name,
                cluster_node_iam_role_name=cluster_node_iam_role_name,
                enable_head_node_fault_tolerance=enable_head_node_fault_tolerance,
                anyscale_aws_account=anyscale_aws_account,
                boto3_session=boto3_session,
                shared_storage=shared_storage,
                resource_id=resource_id,
            )
            controller.update_cloud_with_resources(
                cfn_stack, resolved_cloud_id, region, enable_head_node_fault_tolerance
            )
            controller.wait_for_cloud_to_be_active(resolved_cloud_id)

            controller.log.info(
                f"Successfully added VM resources to cloud '{resolved_cloud_name}'."
            )

        except Exception as e:  # noqa: BLE001
            controller.log.error(str(e))
            raise click.ClickException(f"Failed to add VM resources: {e}")

    elif provider == "gcp":
        if not project_id:
            raise click.ClickException("--project-id is required for GCP clouds.")

        gcp_utils = try_import_gcp_utils()
        setup_utils = try_import_gcp_managed_setup_utils()
        factory = gcp_utils.get_google_cloud_client_factory(controller.log, project_id)

        try:
            organization_id = get_organization_id(controller.api_client)
            anyscale_aws_account = (
                controller.api_client.get_anyscale_aws_account_api_v2_clouds_anyscale_aws_account_get().result.anyscale_aws_account
            )

            setup_utils.enable_project_apis(
                factory, project_id, controller.log, enable_head_node_fault_tolerance
            )

            token = secrets.token_hex(4)
            if anyscale_access_service_account is None:
                anyscale_access_service_account = (
                    f"anyscale-access-{token}@{project_id}.iam.gserviceaccount.com"
                )
            pool_id = f"anyscale-provider-pool-{token}"
            deployment_name = f"{resolved_cloud_id}-{token}".replace("_", "-").lower()

            actual_pool_name = controller.create_workload_identity_federation_provider(
                factory, project_id, pool_id, anyscale_access_service_account
            )
            pool_name = pool_name or actual_pool_name

            controller.setup_gcp_cloud_resources(
                factory,
                deployment_name,
                resolved_cloud_id,
                project_id,
                region,
                anyscale_access_service_account,
                pool_name,
                anyscale_aws_account,
                organization_id,
                enable_head_node_fault_tolerance,
                shared_storage=shared_storage,
            )
            controller.wait_for_cloud_to_be_active(resolved_cloud_id)

            controller.log.info(
                f"Successfully added VM resources to cloud '{resolved_cloud_name}'."
            )

        except Exception as e:  # noqa: BLE001
            controller.log.error(str(e))
            raise click.ClickException(f"Failed to add VM resources: {e}")

    else:
        raise click.ClickException(f"Unsupported provider: {provider}")


@click.group(
    "cloud",
    short_help="Configure cloud provider authentication for Anyscale.",
    help="""Configure cloud provider authentication and setup
to allow Anyscale to launch instances in your account.""",
)
def cloud_cli() -> None:
    pass


def _create_cloud_list_table(show_header: bool) -> Table:
    table = Table(show_header=show_header, expand=True)
    table.add_column("NAME", no_wrap=False, overflow="fold", ratio=3, min_width=15)
    table.add_column("ID", no_wrap=False, overflow="fold", ratio=2, min_width=12)
    for heading in ("PROVIDER", "REGION", "DEFAULT", "CREATED AT"):
        table.add_column(heading, no_wrap=False, overflow="fold", ratio=1, min_width=8)
    return table


def _format_cloud_output_data(cloud: Any) -> Dict[str, str]:
    created_at = ""
    if getattr(cloud, "created_at", None):
        created_at = cloud.created_at.strftime("%Y-%m-%d %H:%M:%S")
    return {
        "name": getattr(cloud, "name", ""),
        "id": getattr(cloud, "id", ""),
        "provider": str(getattr(cloud, "provider", "") or ""),
        "region": str(getattr(cloud, "region", "") or ""),
        "default": str(getattr(cloud, "is_default", False)),
        "created_at": created_at,
    }


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Delete a cloud by name.",
            command="anyscale cloud delete -n my-cloud",
        ),
    ],
)
@cloud_cli.command(
    name="delete",
    short_help="Delete a cloud.",
    help=(
        "Delete a cloud.\n\n"
        "Specify the cloud by name (-n/--name) or by ID (--cloud-id)."
    ),
    cls=AnyscaleCommand,
)
@click.argument("cloud-name", required=False)
@click.option("--name", "-n", help="Delete cloud by name.", type=str)
@click.option(
    "--cloud-id",
    "--id",
    "cloud_id",
    help="Cloud id to delete. Alternative to cloud name.",
    required=False,
)
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Don't ask for confirmation."
)
@click.option(
    "--force",
    is_flag=True,
    default=False,
    help=(
        "Force-delete the cloud even if it has active clusters (bypasses the "
        "active-cluster check). You are responsible for cleaning up any "
        "cloud-provider resources, and for any costs incurred by clusters that "
        "are left in an active state, yourself."
    ),
)
@disabled_on_azure("cloud delete")
def cloud_delete(
    cloud_name: Optional[str],
    name: Optional[str],
    cloud_id: Optional[str],
    yes: bool,
    force: bool,
) -> None:
    if cloud_name and name and cloud_name != name:
        raise click.ClickException(
            "The positional argument CLOUD_NAME and the keyword argument --name "
            "were both provided. Please only provide one of these two arguments."
        )
    CloudController().delete_cloud(
        cloud_name=cloud_name or name,
        cloud_id=cloud_id,
        skip_confirmation=yes,
        force=force,
    )


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Set the default cloud for your organization.",
            command="anyscale cloud set-default -n my-cloud",
        ),
    ],
)
@cloud_cli.command(
    name="set-default",
    short_help="Set the default cloud for your organization.",
    help=(
        "Set the default cloud for your organization. This operation can only be performed "
        "by organization admins, and the default cloud must have organization level "
        "permissions. Specify the cloud by name (-n/--name) or by ID (--cloud-id)."
    ),
    cls=AnyscaleCommand,
)
@click.argument("cloud-name", required=False)
@click.option("--name", "-n", help="Set cloud as default by name.", type=str)
@click.option(
    "--cloud-id",
    "--id",
    "cloud_id",
    help="Cloud id to set as default. Alternative to cloud name.",
    required=False,
)
def cloud_set_default(
    cloud_name: Optional[str], name: Optional[str], cloud_id: Optional[str]
) -> None:
    if cloud_name and name and cloud_name != name:
        raise click.ClickException(
            "The positional argument CLOUD_NAME and the keyword argument --name "
            "were both provided. Please only provide one of these two arguments."
        )
    CloudController().set_default_cloud(
        cloud_name=cloud_name or name, cloud_id=cloud_id
    )


def default_region(provider: str) -> str:
    default_regions = {
        "aws": "us-west-2",
        "gcp": "us-west1",
        "azure": "westus2",
    }
    return default_regions.get(provider, "default")


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Set up an AWS cloud with a Kubernetes compute stack.",
            command=(
                "anyscale cloud setup --provider aws --region us-west-2 --name my-cloud "
                "--stack k8s --cluster-name my-eks-cluster"
            ),
            output_raw=command_examples.CLOUD_SETUP_K8S_AWS_EXAMPLE,
        ),
        CommandExample(
            description="Set up a GCP cloud with a Kubernetes compute stack.",
            command=(
                "anyscale cloud setup --provider gcp --region us-central1 --name my-cloud "
                "--stack k8s --cluster-name my-gke-cluster --project-id my-project-123"
            ),
            output_raw=command_examples.CLOUD_SETUP_K8S_GCP_EXAMPLE,
        ),
        CommandExample(
            description="Set up a Kubernetes cloud, writing the generated Helm values to a specific path.",
            command=(
                "anyscale cloud setup --provider aws --region us-west-2 --name my-cloud "
                "--stack k8s --cluster-name my-eks-cluster --values-file /path/to/custom-values.yaml"
            ),
            output_raw=command_examples.CLOUD_SETUP_K8S_CUSTOM_VALUES_EXAMPLE,
        ),
    ],
)
@cloud_cli.command(
    name="setup",
    short_help="Set up a cloud provider.",
    help="Set up a cloud provider.",
    cls=AnyscaleCommand,
)
@click.option(
    "--provider",
    help="The cloud provider type.",
    required=False,
    type=click.Choice(["aws", "gcp", "azure"], case_sensitive=False),
)
@click.option(
    "--region",
    cls=OptionPromptNull,
    help="Region to set up the credentials in.",
    required=False,
    default_option="provider",
    default=default_region,
    show_default=True,
)
@click.option("--name", "-n", help="Name of the cloud.", required=True, prompt="Name")
@click.option(
    "--stack",
    help="The compute stack to use (vm or k8s).",
    required=False,
    type=click.Choice(["vm", "k8s"], case_sensitive=False),
    default="vm",
    show_default=True,
)
@click.option(
    "--cluster-name", help="Kubernetes cluster name. (K8s)", required=False, type=str,
)
@click.option(
    "--namespace",
    help="Kubernetes namespace for Anyscale operator. (K8s)",
    required=False,
    type=str,
    default="anyscale-operator",
)
@click.option(
    "--gcp-project-id",
    "--project-id",
    "project_id",
    help="Globally Unique project ID for GCP clouds (e.g., my-project-abc123)",
    required=False,
    type=str,
)
@click.option(
    "--resource-group",
    help="Resource group for Azure clouds.",
    required=False,
    type=str,
)
@click.option(
    "--functional-verify",
    help="Verify the cloud is functional. This will check that the cloud can launch workspace/service.",
    required=False,
    is_flag=False,
    flag_value="workspace",
)
@click.option(
    "--anyscale-managed",
    is_flag=True,
    default=False,
    help="Let anyscale create all the resources. (VM)",
)
@click.option(
    "--enable-head-node-fault-tolerance",
    is_flag=True,
    default=False,
    help="Whether to enable head node fault tolerance for services. (VM)",
)
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Skip asking for confirmation."
)
@click.option(
    "--disable-auto-add-user",
    is_flag=True,
    default=False,
    help=(
        "All users in the organization will be added to clouds created "
        "with `anyscale cloud setup` by default. Specify --disable-auto-add-user to "
        "disable this and instead manually grant users permissions to the cloud."
    ),
)
@click.option(
    "--shared-storage",
    required=False,
    type=click.Choice([e.value for e in SharedStorageType], case_sensitive=False),
    default=SharedStorageType.OBJECT_STORAGE.value,
    show_default=True,
    help="The type of shared storage to use for the cloud. Use 'object-storage' for cloud bucket-based storage (e.g., S3, GCS), or 'nfs' for network file systems. (VM)",
)
@click.option(
    "--values-file",
    help="Path to save the generated Helm values file (for k8s stack, default: auto-generated with timestamp). (K8s)",
    required=False,
    type=str,
)
@click.option(
    "--debug", is_flag=True, default=False, help="Enable debug logging.",
)
@click.option(
    "--operator-chart",
    help="Path to operator chart (skips helm repo add/update). (K8s)",
    required=False,
    type=str,
    hidden=True,
)
@click.option(
    "--skip-resources",
    is_flag=True,
    default=False,
    help=(
        "Create an empty cloud without provisioning resources. "
        "Use this to create a cloud record first and add resources later."
    ),
)
@disabled_on_azure("cloud setup")
def setup_cloud(  # noqa: PLR0913
    provider: str,
    region: str,
    name: str,
    stack: str,
    cluster_name: Optional[str],
    namespace: str,
    project_id: str,
    resource_group: Optional[str],
    functional_verify: Optional[str],
    anyscale_managed: bool,  # noqa: ARG001
    enable_head_node_fault_tolerance: bool,
    yes: bool,
    disable_auto_add_user: bool,
    shared_storage: str,
    values_file: Optional[str],
    debug: bool,
    operator_chart: Optional[str],
    skip_resources: bool,
) -> None:
    # TODO (congding): remove `anyscale_managed` in the future, now keeping it for compatibility

    # Handle --skip-resources flag: create an empty cloud without provisioning resources
    if skip_resources:
        CloudController().create_empty_cloud(name=name)
        return

    # For normal setup, provider and region are required - prompt if not provided
    if not provider:
        provider = click.prompt(
            "Provider", type=click.Choice(["aws", "gcp", "azure"], case_sensitive=False)
        )
    # Treat an unset or "default" sentinel region as "needs prompting": Click can
    # surface default_region()'s "default" fallback as a literal region when --provider
    # is unset (notably on Click >= 8.2), which would otherwise reach the cloud SDK.
    if not region or region == "default":
        region = click.prompt("Region", default=default_region(provider))

    # Handle Kubernetes stack
    if stack == "k8s":
        if not cluster_name:
            raise click.ClickException(
                "--cluster-name is required when using --stack=k8s"
            )

        setup_kubernetes_cloud(
            provider=provider,
            region=region,
            name=name,
            cluster_name=cluster_name,
            namespace=namespace,
            project_id=project_id,
            resource_group=resource_group,
            functional_verify=bool(functional_verify),
            yes=yes,
            values_file=values_file,
            debug=debug,
            operator_chart=operator_chart,
        )
        return

    # Handle VM stack
    # VM clouds need a real region; an unresolved/sentinel region would reach the
    # cloud SDK and fail with a cryptic endpoint error (e.g. ec2.default.amazonaws.com).
    if not region or region == "default":
        raise click.ClickException(
            "Could not determine a region for the cloud. Re-run with an explicit region, "
            "e.g. `anyscale cloud setup --provider aws --region us-west-2 --name <name>`."
        )

    # Convert string to enum for type safety
    shared_storage_type = SharedStorageType(shared_storage)
    if provider == "aws":
        CloudController().setup_managed_cloud(
            provider=provider,
            region=region,
            name=name,
            functional_verify=functional_verify,
            cluster_management_stack_version=ClusterManagementStackVersions.V2,
            enable_head_node_fault_tolerance=enable_head_node_fault_tolerance,
            yes=yes,
            auto_add_user=(not disable_auto_add_user),
            shared_storage=shared_storage_type,
        )
    elif provider == "gcp":
        if not project_id:
            project_id = click.prompt("GCP Project ID", type=str)
        if project_id[0].isdigit():
            # project ID should start with a letter
            raise click.ClickException(
                "Please provide a valid project ID. Note that project ID is not project number, see https://cloud.google.com/resource-manager/docs/creating-managing-projects#before_you_begin for details."
            )
        CloudController().setup_managed_cloud(
            provider=provider,
            region=region,
            name=name,
            project_id=project_id,
            functional_verify=functional_verify,
            cluster_management_stack_version=ClusterManagementStackVersions.V2,
            enable_head_node_fault_tolerance=enable_head_node_fault_tolerance,
            yes=yes,
            auto_add_user=(not disable_auto_add_user),
            shared_storage=shared_storage_type,
        )


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT, OutputFormat.JSON],
    option_docs={
        "--json": {
            "status": ReleaseStatus.DEPRECATED,
            "deprecation_info": {"message": "Use -o json instead."},
        }
    },
    examples=[
        CommandExample(
            description="List the clouds in your Anyscale organization.",
            command="anyscale cloud list",
            output_instance=[
                {
                    "id": "cld_abc123",
                    "name": "my-cloud",
                    "provider": "AWS",
                    "region": "us-west-2",
                    "compute_stack": "VM",
                    "is_default": True,
                    "created_at": "2023-04-10T20:34:15.211510+00:00",
                }
            ],
        ),
    ],
)
@cloud_cli.command(
    name="list",
    short_help="List information about clouds in your Anyscale organization.",
    help="List information about clouds in your Anyscale organization.",
    cls=AnyscaleCommand,
)
@click.option(
    "--name",
    "-n",
    required=False,
    default=None,
    help="Name of cloud to get information about.",
)
@click.option(
    "--cloud-id",
    "--id",
    "cloud_id",
    required=False,
    default=None,
    help=("Id of cloud to get information about."),
)
@click.option(
    "--max-items",
    required=False,
    default=None,
    type=int,
    help="Maximum number of clouds to return. If not specified, all results are returned.",
    callback=validate_non_negative_arg,
)
@click.option(
    "--page-size",
    type=int,
    default=10,
    show_default=True,
    callback=validate_page_size,
    help=f"Items per page (max {MAX_PAGE_SIZE}).",
)
@click.option(
    "--interactive/--no-interactive",
    default=True,
    show_default=True,
    help="Use interactive paging.",
)
@click.option(
    OUTPUT_FLAG,
    OUTPUT_FLAG_LONG,
    "output_format",
    type=click.Choice([OutputFormat.TEXT.value, OutputFormat.JSON.value]),
    default=OutputFormat.TEXT.value,
    show_default=True,
    help="Output format for the result.",
)
@click.option(
    "-j",
    "--json",
    "json_output",
    is_flag=True,
    default=False,
    help="Emit structured JSON to stdout.",
)
def list_cloud(  # noqa: A001
    name: Optional[str],
    cloud_id: Optional[str],
    max_items: Optional[int],
    page_size: int,
    interactive: bool,
    output_format: str,
    json_output: bool,
) -> None:
    if json_output:
        warn_deprecated_flag("--json", "-o json")
    json_output = json_output or output_format == OutputFormat.JSON.value

    interactive = resolve_interactive(interactive, json_output)

    if max_items is not None and interactive:
        raise click.UsageError("--max-items only allowed with --no-interactive")

    effective_max = max_items
    stderr = Console(stderr=True)
    if not interactive and effective_max is None:
        stderr.print(
            f"Defaulting to {NON_INTERACTIVE_DEFAULT_MAX_ITEMS} items in batch mode; "
            "use --max-items to override."
        )
        effective_max = NON_INTERACTIVE_DEFAULT_MAX_ITEMS

    console = Console()

    # diagnostics
    stderr.print("[bold]Listing clouds with:[/]")
    stderr.print(f"• name            = {name or '<any>'}")
    stderr.print(f"• id              = {cloud_id or '<any>'}")
    stderr.print(f"• mode            = {'interactive' if interactive else 'batch'}")
    stderr.print(f"• per-page limit  = {page_size}")
    stderr.print(f"• max-items total = {effective_max or 'all'}")
    stderr.print(f"\nView your Clouds in the UI at {get_endpoint('/clouds')}\n")

    # choose formatter
    if json_output:

        def json_formatter(cloud: Any) -> Dict[str, Any]:
            to_dict = getattr(cloud, "to_dict", None)
            return to_dict() if callable(to_dict) else dict(cloud.__dict__)

        formatter = json_formatter
    else:
        formatter = _format_cloud_output_data

    total = 0
    try:
        iterator = anyscale.cloud.list(
            cloud_id=cloud_id,
            name=name,
            max_items=None if interactive else effective_max,
            page_size=page_size,
        )
        total = display_list(
            iterator=iter(iterator),
            item_formatter=formatter,
            table_creator=_create_cloud_list_table,
            json_output=json_output,
            page_size=page_size,
            interactive=interactive,
            max_items=effective_max,
            console=console,
        )

        # Always print diagnostics to stderr, even in JSON mode.
        if total > 0:
            stderr.print(f"\nFetched {total} clouds.")
        else:
            stderr.print("\nNo clouds found.")
    except Exception as e:  # noqa: BLE001
        log.error(f"Failed to list clouds: {e}")
        raise SystemExit(1)


@cloud_cli.group("resource", help="Manage the configuration for a cloud resource.")
def cloud_resource_group() -> None:
    pass


@cloud_cli.group("config", help="Manage the configuration for a cloud.")
def cloud_config_group() -> None:
    pass


@command_metadata(
    status=ReleaseStatus.BETA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Create a new cloud resource in an existing cloud.",
            command="anyscale cloud resource create --cloud my-cloud -f resource.yaml",
            output_raw=command_examples.CLOUD_RESOURCE_CREATE_EXAMPLE,
        ),
    ],
)
@cloud_resource_group.command(
    name="create",
    short_help="Create a new cloud resource in an existing cloud.",
    help="Create a new cloud resource in an existing cloud.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "--cloud",
    help="The name of the cloud to add the new resource to.",
    type=str,
    required=False,
)
@click.option(
    "--cloud-id",
    help="The ID of the cloud to add the new resource to.",
    type=str,
    required=False,
)
@click.option(
    "--file",
    "-f",
    help="Path to a YAML file defining the cloud resource. Schema: https://docs.anyscale.com/reference/cloud#cloudresource.",
    required=True,
)
@click.option(
    "--skip-verification",
    is_flag=True,
    default=False,
    help=(
        "Skip cloud resource verification. This also skips local AWS/GCP "
        "credential checks and resource preprocessing, sending the provided "
        "resource to Anyscale as-is."
    ),
)
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Skip asking for confirmation."
)
@disabled_on_azure("cloud resource create")
def cloud_resource_create(
    cloud: Optional[str],
    cloud_id: Optional[str],
    file: str,
    skip_verification: bool,
    yes: bool,
) -> None:
    try:
        CloudController().create_cloud_resource(
            cloud, cloud_id, file, skip_verification, yes
        )
    except click.ClickException as e:
        print(e)


@command_metadata(
    status=ReleaseStatus.ALPHA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Set up K8s resources in an existing cloud on AWS.",
            command=(
                "anyscale cloud resource setup --provider aws --region us-west-2 "
                "--cloud my-cloud --stack k8s --cluster-name my-eks-cluster"
            ),
            output_raw="Kubernetes cloud resource setup for 'my-cloud' completed successfully!\n",
        ),
        CommandExample(
            description="Set up VM resources in an existing cloud on GCP.",
            command=(
                "anyscale cloud resource setup --provider gcp --region us-central1 "
                "--cloud my-cloud --stack vm --project-id my-project-abc123"
            ),
            output_raw="Successfully added VM resources to cloud 'my-cloud'.\n",
        ),
    ],
)
@cloud_resource_group.command(
    name="setup",
    short_help="Set up cloud resources for an existing cloud.",
    help="Set up cloud resources for an existing cloud.",
    cls=AnyscaleCommand,
    is_alpha=True,
)
@click.option(
    "--provider",
    help="The cloud provider type.",
    required=True,
    type=click.Choice(["aws", "gcp"], case_sensitive=False),
)
@click.option(
    "--region", help="Region to set up the resources in.", required=True,
)
@click.option(
    "--stack",
    help="The compute stack to use",
    required=False,
    type=click.Choice(["vm", "k8s"], case_sensitive=False),
    default="k8s",
    show_default=True,
)
@click.option(
    "--cloud",
    help="The name of the existing cloud to add resources to. Either this or --cloud-id is required.",
    type=str,
    required=False,
)
@click.option(
    "--cloud-id",
    help="The ID of the existing cloud to add resources to. Either this or --cloud is required.",
    type=str,
    required=False,
)
@click.option(
    "--cluster-name", help="Kubernetes cluster name. (K8s)", required=False, type=str,
)
@click.option(
    "--namespace",
    help="Kubernetes namespace for Anyscale operator. (K8s)",
    required=False,
    type=str,
    default="anyscale-operator",
)
@click.option(
    "--gcp-project-id",
    "--project-id",
    "project_id",
    help="Globally Unique project ID for GCP clouds (e.g., my-project-abc123)",
    required=False,
    type=str,
)
@click.option(
    "--functional-verify",
    help="Verify the cloud is functional. This will check that the cloud can launch workspace/service.",
    required=False,
    is_flag=False,
    flag_value="workspace",
)
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Skip asking for confirmation."
)
@click.option(
    "--values-file",
    help="Path to save the generated Helm values file (K8s: default - auto-generated with timestamp). (K8s)",
    required=False,
    type=str,
)
@click.option(
    "--debug", is_flag=True, default=False, help="Enable debug logging.",
)
@click.option(
    "--operator-chart",
    help="Path to operator chart (skips helm repo add/update). (K8s)",
    required=False,
    type=str,
    hidden=True,
)
@click.option(
    "--resource-name",
    help="Name for the cloud resource (optional, will be auto-generated if not provided)",
    required=False,
    type=str,
    default=None,
)
@click.option(
    "--enable-head-node-fault-tolerance",
    is_flag=True,
    default=False,
    help="Whether to enable head node fault tolerance for services. (VM)",
)
@click.option(
    "--shared-storage",
    required=False,
    type=click.Choice([e.value for e in SharedStorageType], case_sensitive=False),
    default=SharedStorageType.OBJECT_STORAGE.value,
    show_default=True,
    help="The type of shared storage to use. Use 'object-storage' for cloud bucket-based storage (e.g., S3, GCS), or 'nfs' for network file systems. (VM)",
)
@disabled_on_azure("cloud resource setup")
def cloud_resource_setup(  # noqa: PLR0913
    provider: str,
    region: str,
    stack: str,
    cloud: Optional[str],
    cloud_id: Optional[str],
    cluster_name: Optional[str],
    namespace: str,
    project_id: Optional[str],
    functional_verify: Optional[str],
    yes: bool,
    values_file: Optional[str],
    debug: bool,
    operator_chart: Optional[str],
    resource_name: Optional[str],
    enable_head_node_fault_tolerance: bool,
    shared_storage: str,
) -> None:
    """
    Set up cloud resources for an existing Anyscale cloud.

    This command sets up infrastructure (S3/GCS buckets, IAM roles, etc.) and creates
    a cloud resource in an existing cloud instead of registering a new cloud.

    For K8s stack: Also installs the Anyscale operator on your Kubernetes cluster.
    For VM stack: Creates CloudFormation (AWS) or Deployment Manager (GCP) resources.
    """
    if stack == "k8s":
        if not cluster_name:
            raise click.ClickException(
                "--cluster-name is required when using --stack=k8s"
            )
        setup_kubernetes_cloud_resource(
            provider=provider,
            region=region,
            cloud_name=cloud,
            cloud_id=cloud_id,
            cluster_name=cluster_name,
            namespace=namespace,
            project_id=project_id,
            functional_verify=bool(functional_verify),
            yes=yes,
            values_file=values_file,
            debug=debug,
            operator_chart=operator_chart,
            resource_name=resource_name,
        )
    elif stack == "vm":
        setup_vm_cloud_resource(
            provider=provider,
            region=region,
            cloud_name=cloud,
            cloud_id=cloud_id,
            project_id=project_id,
            enable_head_node_fault_tolerance=enable_head_node_fault_tolerance,
            shared_storage=SharedStorageType(shared_storage),
        )
    else:
        raise click.ClickException(f"Unsupported stack: {stack}")


@command_metadata(
    status=ReleaseStatus.BETA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Remove a cloud resource from an existing cloud.",
            command="anyscale cloud resource delete --cloud my-cloud --resource my-resource",
            output_raw=command_examples.CLOUD_RESOURCE_DELETE_EXAMPLE,
        ),
    ],
)
@cloud_resource_group.command(
    name="delete",
    short_help="Remove a cloud resource from an existing cloud.",
    help="Remove a cloud resource from an existing cloud.",
    cls=AnyscaleCommand,
    is_beta=True,
)
@click.option(
    "--cloud",
    help="The name of the cloud to remove the resource from.",
    type=str,
    required=True,
)
@click.option(
    "--resource",
    help="The name of the cloud resource to remove.",
    type=str,
    required=True,
)
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Skip asking for confirmation."
)
@disabled_on_azure("cloud resource delete")
def cloud_resource_delete(cloud: str, resource: str, yes: bool,) -> None:
    try:
        CloudController().remove_cloud_resource(cloud, resource, yes)
    except click.ClickException as e:
        print(e)


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Update a cloud by name.",
            command="anyscale cloud update -n my-cloud",
        ),
    ],
)
@cloud_cli.command(
    name="update",
    short_help="Update a cloud.",
    help=(
        "Update a cloud.\n\n"
        "Specify the cloud by name (-n/--name) or by ID (--cloud-id)."
    ),
    cls=AnyscaleCommand,
)
@click.argument("cloud-name", required=False)
@click.option(
    "--cloud-id",
    "--id",
    "cloud_id",
    help="Cloud id to update. Alternative to cloud name.",
    required=False,
)
@click.option("--name", "-n", help="Update configuration of cloud by name.", type=str)
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Skip asking for confirmation."
)
@click.option(
    "--functional-verify",
    help="Verify the cloud is functional. This will check that the cloud can launch workspace/service.",
    required=False,
    is_flag=False,
    flag_value="workspace",
)
@click.option(
    "--enable-auto-add-user/--disable-auto-add-user",
    default=None,
    help=(
        "If --enable-auto-add-user is specified for a cloud, all users in the organization "
        "will be added to the cloud by default. Note: There may be up to 30 sec delay for all users to be granted "
        "permissions after this feature is enabled. Specifying --disable-auto-add-user will require that users "
        "are manually granted permissions to access the cloud. No existing cloud permissions are altered by specifying this flag."
    ),
)
@click.option(
    "--resources-file",
    "-f",
    help="Path to a YAML file defining a single cloud resource or a list of cloud resources. Only applicable for customer-managed resources. Schema: https://docs.anyscale.com/reference/cloud#cloudresource.",
    required=False,
)
@click.option(
    "--enable-head-node-fault-tolerance",
    is_flag=True,
    default=False,
    help="Whether to enable head node fault tolerance for services. Only applicable for clouds with Anyscale-managed resources (clouds created via `anyscale cloud setup`).",
)
@click.option(
    "--skip-verification",
    is_flag=True,
    default=False,
    help=(
        "Skip cloud resource verification. This also skips local AWS/GCP "
        "credential checks and resource preprocessing, sending the provided "
        "resources to Anyscale as-is."
    ),
)
@click.option(
    "--migrate-dm-to-im",
    is_flag=True,
    default=False,
    help="Migrate GCP cloud resources from Deployment Manager to Infrastructure Manager. Only applicable for GCP clouds with Anyscale-managed resources.",
)
def cloud_update(  # noqa: PLR0913
    cloud_name: Optional[str],
    name: Optional[str],
    cloud_id: Optional[str],
    functional_verify: Optional[str],
    yes: bool,
    enable_auto_add_user: Optional[bool],
    resources_file: Optional[str],
    enable_head_node_fault_tolerance: bool,
    skip_verification: bool,
    migrate_dm_to_im: bool,
) -> None:
    if cloud_name and name and cloud_name != name:
        raise click.ClickException(
            "The positional argument CLOUD_NAME and the keyword argument --name "
            "were both provided. Please only provide one of these two arguments."
        )
    CloudController().update_cloud(
        cloud_name=cloud_name or name,
        cloud_id=cloud_id,
        enable_auto_add_user=enable_auto_add_user,
        enable_head_node_fault_tolerance=enable_head_node_fault_tolerance,
        resources_file=resources_file,
        functional_verify=functional_verify,
        yes=yes,
        skip_verification=skip_verification,
        migrate_dm_to_im=migrate_dm_to_im,
    )


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Update storage CORS configuration for a cloud.",
            command="anyscale cloud update-storage-cors -n my-cloud",
        ),
    ],
)
@cloud_cli.command(
    name="update-storage-cors",
    short_help="Update CORS configuration on cloud storage to support Anyscale UI features.",
    help="Update CORS configuration on cloud storage to support Anyscale UI features. Works with both managed and customer-managed clouds. When a cloud resource is not specified, updates CORS for all cloud resources under the cloud.",
    cls=AnyscaleCommand,
)
@click.argument("cloud-name", required=False)
@click.option(
    "--cloud-id",
    "--id",
    "cloud_id",
    help="Cloud id to update. Alternative to cloud name.",
    required=False,
)
@click.option("--name", "-n", help="Update storage CORS for cloud by name.", type=str)
@click.option(
    "--resource",
    help="Name of the cloud resource to update. If not provided, updates all cloud resources under the cloud.",
    type=str,
    required=False,
)
@click.option(
    "--resource-id",
    "cloud_resource_id",
    help="Cloud resource ID to update. Alternative to cloud resource name.",
    type=str,
    required=False,
)
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Skip asking for confirmation."
)
def cloud_update_storage_cors(
    cloud_name: Optional[str],
    name: Optional[str],
    cloud_id: Optional[str],
    resource: Optional[str],
    cloud_resource_id: Optional[str],
    yes: bool,
) -> None:
    """
    Update CORS configuration on cloud storage to support Anyscale UI features.

    This command configures CORS rules on cloud storage buckets (S3, GCS, Azure Blob)
    to enable features like the file viewer in the Anyscale UI. Works with both managed
    and customer-managed clouds.

    `$ anyscale cloud update-storage-cors my-cloud`
    `$ anyscale cloud update-storage-cors my-cloud --resource my-resource`
    """
    if cloud_name and name and cloud_name != name:
        raise click.ClickException(
            "The positional argument CLOUD_NAME and the keyword argument --name "
            "were both provided. Please only provide one of these two arguments."
        )
    if resource and cloud_resource_id:
        raise click.ClickException(
            "Cannot specify both --resource and --resource-id. Please provide only one."
        )
    CloudController().update_cors(
        cloud_name=cloud_name or name,
        cloud_id=cloud_id,
        resource=resource,
        cloud_resource_id=cloud_resource_id,
        yes=yes,
    )


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT, OutputFormat.JSON, OutputFormat.YAML],
    examples=[
        CommandExample(
            description="Get the current configuration for a cloud.",
            command="anyscale cloud config get -n my-cloud",
            output_instance={
                "cloud_deployment_id": "cldrsrc_abc123",
                "cloud_provider": "AWS",
                "compute_stack": "VM",
                "dataplane_iam_mapping": {},
            },
        ),
    ],
)
@cloud_config_group.command(
    "get",
    short_help="Get the current configuration for a cloud.",
    help="Get the current configuration for a cloud.",
    cls=AnyscaleCommand,
)
@click.argument("cloud-name", required=False)
@click.option("--name", "-n", help="Get configuration of cloud by name.", type=str)
@click.option(
    "--cloud-id",
    "--id",
    "cloud_id",
    help="Cloud id to get details about. Alternative to cloud name.",
    required=False,
)
@click.option(
    "--resource",
    help="Name of the cloud resource to get details for. If not provided, defaults to the primary resource for the cloud.",
    type=str,
    required=False,
)
@click.option(
    "--resource-id",
    "cloud_resource_id",
    help="Cloud resource ID to get details for. Alternative to cloud resource name.",
    type=str,
    required=False,
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
def cloud_config_get(
    cloud_name: Optional[str],
    name: Optional[str],
    cloud_id: Optional[str],
    resource: Optional[str],
    cloud_resource_id: Optional[str],
    output_format: str,
) -> None:
    if cloud_name and name and cloud_name != name:
        raise click.ClickException(
            "The positional argument CLOUD_NAME and the keyword argument --name "
            "were both provided. Please only provide one of these two arguments."
        )

    # Validate resource selection options
    if resource and cloud_resource_id:
        raise click.ClickException(
            "Cannot specify both --resource and --resource-id. Please provide only one."
        )

    config = CloudController().get_cloud_config(
        cloud_name=cloud_name or name,
        cloud_id=cloud_id,
        resource=resource,
        cloud_resource_id=cloud_resource_id,
    )
    if output_format != OutputFormat.TEXT.value:
        print_output(config.spec, output_format)
        return
    stream = StringIO()
    yaml.dump(config.spec, stream)
    print(stream.getvalue())


def _validate_cloud_config_update_args(
    cloud_name: Optional[str],
    name: Optional[str],
    resource: Optional[str],
    cloud_resource_id: Optional[str],
    passed_enable_disable_flags: bool,
    spec_file: Optional[str],
) -> None:
    """Validate arguments for cloud config update command."""
    if cloud_name and name and cloud_name != name:
        raise click.ClickException(
            "The positional argument CLOUD_NAME and the keyword argument --name "
            "were both provided. Please only provide one of these two arguments."
        )

    if resource and cloud_resource_id:
        raise click.ClickException(
            "Cannot specify both --resource and --resource-id. Please provide only one."
        )

    if passed_enable_disable_flags and spec_file:
        raise click.ClickException(
            "Invalid combination of arguments: --spec-file should not be provided with any other enable/disable flags."
        )

    if (resource or cloud_resource_id) and not spec_file:
        raise click.ClickException(
            "--resource and --resource-id can only be used with --spec-file."
        )


def _handle_log_ingestion_config(enable_log_ingestion: Optional[bool]) -> None:
    """Handle log ingestion configuration with user prompts."""
    if enable_log_ingestion is True:
        consent_message = click.prompt(
            "--enable-log-ingestion is specified. Please note the logs produced by "
            "your cluster will be ingested into Anyscale's service in region "
            "us-west-2. Your clusters may incur extra data transfer cost from the "
            "cloud provider. If you are sure you want to enable this feature, "
            'please type "consent"',
            type=str,
        )
        if consent_message != "consent":
            raise click.ClickException(
                'You must type "consent" to enable log ingestion.'
            )
    elif enable_log_ingestion is False:
        confirm_response = click.confirm(
            "--disable-log-ingestion is specified. Please note the logs that's "
            "already ingested will not be deleted. Existing clusters will not stop"
            "the log ingestion until you restart them. Logs are automatically "
            "deleted after 30 days from the time of ingestion. Are you sure you "
            "want to disable log ingestion?"
        )
        if not confirm_response:
            raise click.ClickException("You must confirm to disable log ingestion.")


def _handle_system_cluster_config(enable_system_cluster: Optional[bool]) -> None:
    """Handle system cluster configuration with user prompts."""
    confirm_response = True
    if enable_system_cluster is True:
        confirm_response = click.confirm(
            "--enable-system-cluster is specified. Please note that this will enable "
            "system cluster functionality for the cloud and will incur extra cost. "
            "Are you sure you want to enable system cluster?"
        )
    elif enable_system_cluster is False:
        confirm_response = click.confirm(
            "--disable-system-cluster is specified. This will disable system cluster "
            "functionality for the cloud. Please note that this will not terminate "
            "the system cluster if it is currently running. "
            "Are you sure you want to disable system cluster?"
        )

    if enable_system_cluster is not None and not confirm_response:
        raise click.ClickException(
            f"You must confirm to {'enable' if enable_system_cluster else 'disable'} system cluster."
        )


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Enable log ingestion and the system cluster for a cloud (prompts for confirmation).",
            command=(
                "anyscale cloud config update -n my-cloud "
                "--enable-log-ingestion --enable-system-cluster"
            ),
            output_raw=(
                "Successfully updated log ingestion configuration for cloud, cld_abc123 to True\n"
                "Successfully enabled system cluster for cloud cld_abc123\n"
            ),
        ),
        CommandExample(
            description="Update a cloud's configuration from a spec file.",
            command="anyscale cloud config update -n my-cloud --spec-file iam.yaml",
            output_raw="Successfully updated cloud configuration for cloud my-cloud (resource: cldrsrc_abc123)\n",
        ),
        CommandExample(
            description="Update the configuration of a specific cloud resource.",
            command="anyscale cloud config update -n my-cloud --resource shared-usw2 --spec-file iam.yaml",
            output_raw="Successfully updated cloud configuration for cloud my-cloud (resource: cldrsrc_abc456)\n",
        ),
    ],
)
@cloud_config_group.command(
    "update",
    short_help="Update the current configuration for a cloud.",
    help="Update the current configuration for a cloud.",
    cls=AnyscaleCommand,
)
@click.argument("cloud-name", required=False)
@click.option("--name", "-n", help="Update configuration of cloud by name.", type=str)
@click.option(
    "--cloud-id",
    "--id",
    "cloud_id",
    help="Cloud id to update. Alternative to cloud name.",
    required=False,
)
@click.option(
    "--enable-log-ingestion/--disable-log-ingestion",
    default=None,
    help=(
        "If --enable-log-ingestion is specified for a cloud, it will enable the log "
        "viewing and querying UI features for the clusters on this cloud. This will "
        "enable easier debugging. The logs produced by the clusters will "
        "be sent from the data plane to the control plane. Anyscale does not share "
        "this data with any third party or use it for any purpose other than serving "
        "the log UI for the customer. The log will be stored at most 30 days."
        "Please note by disable this feature again, Anyscale doesn't "
        "delete the logs that have already been ingested. Your clusters may incur "
        "extra data transfer cost from the cloud provider by enabling this feature."
    ),
)
@click.option(
    "--enable-system-cluster/--disable-system-cluster",
    default=None,
    help="Enable or disable system cluster functionality.",
    required=False,
)
@click.option(
    "--spec-file",
    type=str,
    required=False,
    help="Provide a path to a specification file.",
)
@click.option(
    "--resource",
    help="Name of the cloud resource to update. If not provided, defaults to the primary resource for the cloud.",
    type=str,
    required=False,
)
@click.option(
    "--resource-id",
    "cloud_resource_id",
    help="Cloud resource ID to update. Alternative to cloud resource name.",
    type=str,
    required=False,
)
def cloud_config_update(  # noqa: PLR0913
    cloud_name: Optional[str],
    name: Optional[str],
    cloud_id: Optional[str],
    enable_log_ingestion: Optional[bool],
    enable_system_cluster: Optional[bool],
    spec_file: Optional[str],
    resource: Optional[str],
    cloud_resource_id: Optional[str],
) -> None:
    passed_enable_disable_flags = any(
        [enable_log_ingestion is not None, enable_system_cluster is not None]
    )

    _validate_cloud_config_update_args(
        cloud_name,
        name,
        resource,
        cloud_resource_id,
        passed_enable_disable_flags,
        spec_file,
    )

    cloud_name_resolved = cloud_name or name

    if passed_enable_disable_flags:
        _handle_log_ingestion_config(enable_log_ingestion)
        CloudController().update_cloud_config(
            cloud_name=cloud_name_resolved,
            cloud_id=cloud_id,
            enable_log_ingestion=enable_log_ingestion,
        )

        _handle_system_cluster_config(enable_system_cluster)
        CloudController().update_system_cluster_config(
            cloud_name=cloud_name_resolved,
            cloud_id=cloud_id,
            system_cluster_enabled=enable_system_cluster,
        )
    elif spec_file:
        CloudController().update_cloud_config(
            cloud_name=cloud_name_resolved,
            cloud_id=cloud_id,
            spec_file=spec_file,
            resource=resource,
            cloud_resource_id=cloud_resource_id,
        )
    else:
        raise click.ClickException(
            "Please provide at least one of the following arguments: --enable-log-ingestion, --disable-log-ingestion, --enable-system-cluster, --disable-system-cluster, --spec-file."
        )


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Register an AWS cloud with your own resources.",
            command="anyscale cloud register --provider aws --region us-west-2 --name my-cloud",
        ),
        CommandExample(
            description="Register a cloud from a cloud resource file, which supplies the provider and region.",
            command="anyscale cloud register --name my-cloud --resource-file cloud.yaml",
        ),
    ],
)
@cloud_cli.command(
    name="register",
    short_help="Register an Anyscale cloud with your own resources.",
    help="Register an Anyscale cloud with your own resources.",
    cls=AnyscaleCommand,
)
@click.option(
    "--provider",
    help="The cloud provider type. Required unless a cloud resource file is provided with --resource-file.",
    required=False,
    type=click.Choice(_REGISTER_PROVIDERS, case_sensitive=False),
)
@click.option(
    "--region",
    cls=OptionPromptNull,
    help="Region to set up the credentials in. Defaults to a per-provider region. Required unless a cloud resource file is provided with --resource-file, in which case this option is ignored.",
    required=False,
    default_option="provider",
    default=default_region,
    show_default=True,
)
@click.option(
    "--compute-stack",
    help="The compute stack type (VM or K8S).",
    required=False,
    type=click.Choice([ComputeStack.VM, ComputeStack.K8S], case_sensitive=False),
    default=ComputeStack.VM,
    # TODO (shomilj): Unhide this option when full support for Kubernetes has been rolled out.
    hidden=True,
)
@click.option(
    "--per-cloud-domain",
    is_flag=True,
    default=False,
    help=(
        "Use a cloud-scoped DNS namespace for Session and Service hostnames. "
        "Requires --compute-stack k8s."
    ),
    hidden=True,
)
@click.option(
    "--per-cloud-domain-label",
    type=str,
    default=None,
    help=(
        "Override the derived cloud DNS ID with a fixed label, so the "
        "cloud-scoped namespace becomes '*.<label>.n.<domain>'. Requires "
        "--per-cloud-domain."
    ),
    hidden=True,
)
@click.option(
    "--name", "-n", help="Name of the cloud.", required=True,
)
@click.option(
    "--vpc-id", help="The ID of the VPC.", required=False, type=str,
)
@click.option(
    "--subnet-ids",
    help="Comma separated list of subnet ids.",
    required=False,
    type=str,
)
@click.option(
    "--file-storage-id",
    help="File storage ID (e.g. EFS ID for AWS, Filestore instance ID for GCP)",
    required=False,
    type=str,
)
@click.option(
    "--efs-id", help="The EFS ID.", required=False, type=str, hidden=True,
)
@click.option(
    "--anyscale-iam-role-id",
    help="The Anyscale IAM Role ARN.",
    required=False,
    type=str,
)
@click.option(
    "--instance-iam-role-id",
    help="The instance IAM role ARN.",
    required=False,
    type=str,
)
@click.option(
    "--security-group-ids",
    help="IDs of the security groups.",
    required=False,
    type=str,
)
@click.option(
    "--s3-bucket-id", help="S3 bucket ID.", required=False, type=str, hidden=True,
)
@click.option(
    "--external-id",
    help="The trust policy external ID for the cross account IAM role. It must begin with the organization ID, followed by a hyphen and a random string of any length. For example: org_1234567890abcdef-1234567890abcdef.",
    required=False,
    type=str,
)
@click.option(
    "--memorydb-cluster-id", help="Memorydb cluster ID", required=False, type=str,
)
@click.option(
    "--gcp-project-id",
    "--project-id",
    "project_id",
    help="Globally Unique project ID for GCP clouds (e.g., my-project-abc123)",
    required=False,
    type=str,
)
@click.option(
    "--vpc-name", help="VPC name for GCP clouds", required=False, type=str,
)
@click.option(
    "--subnet-names",
    help="Comma separated list of subnet names for GCP clouds",
    required=False,
    type=str,
)
@click.option(
    "--filestore-instance-id",
    help="Filestore instance ID for GCP clouds.",
    required=False,
    type=str,
    hidden=True,
)
@click.option(
    "--filestore-location",
    help="Filestore location for GCP clouds.",
    required=False,
    type=str,
)
@click.option(
    "--anyscale-service-account-email",
    help="Anyscale service account email for GCP clouds.",
    required=False,
    type=str,
)
@click.option(
    "--instance-service-account-email",
    help="Instance service account email for GCP clouds.",
    required=False,
    type=str,
)
@click.option(
    "--provider-name",
    help="Workload Identity Federation provider name for Anyscale access.",
    required=False,
    type=str,
)
@click.option(
    "--firewall-policy-names",
    help="Firewall policy names for GCP clouds",
    required=False,
    type=str,
)
@click.option(
    "--cloud-storage-bucket-name",
    help="A fully qualified storage bucket name for cloud storage, e.g. s3://bucket-name, gs://bucket-name, or abfss://bucket-name@account.dfs.core.windows.net.",
    required=False,
    type=str,
)
@click.option(
    "--cloud-storage-bucket-endpoint",
    help="An endpoint for cloud storage, e.g. used to override the default cloud storage scheme's endpoint (e.g. for S3, this would be passed to the AWS_ENDPOINT_URL environment variable).",
    required=False,
    type=str,
)
@click.option(
    "--cloud-storage-bucket-region",
    help="The region of the cloud storage bucket. If not provided, the region of the cloud will be used to access the cloud storage bucket.",
    required=False,
    type=str,
)
@click.option(
    "--nfs-mount-target",
    help="A comma-separated value representing a (zone, mount target) tuple, e.g. us-west-2a,1.2.3.4 (may be provided multiple times, one for each zone). If only one value is provided (e.g. 1.2.3.4), then that value will be used for all zones.",
    required=False,
    type=str,
    multiple=True,
)
@click.option(
    "--nfs-mount-path",
    help="The path of the NFS server to mount from (e.g. nfs-target-address/nfs-path will be mounted).",
    required=False,
    type=str,
)
@click.option(
    "--persistent-volume-claim",
    help="For Kubernetes deployments only, the name of the persistent volume claim used to mount shared storage into pods. Mutually exclusive with NFS configurations.",
    required=False,
    type=str,
)
@click.option(
    "--csi-ephemeral-volume-driver",
    help="For Kubernetes deployments only, the CSI ephemeral volume driver used to mount shared storage into pods. Mutually exclusive with NFS configurations.",
    required=False,
    type=str,
)
@click.option(
    "--memorystore-instance-name",
    help="Memorystore instance name for GCP clouds",
    required=False,
    type=str,
)
@click.option(
    "--host-project-id",
    help="Host project ID for shared VPC",
    required=False,
    type=str,
)
@click.option(
    "--kubernetes-zones",
    help="On the Kubernetes compute stack, a comma-separated list of zones to launch pods in.",
    required=False,
    type=str,
)
@click.option(
    "--kubernetes-redis-endpoint",
    help="On the Kubernetes compute stack, the Redis endpoint reachable from the data plane (e.g. 'redis.ray-system.svc.cluster.local:6379'). Used for Ray GCS fault tolerance.",
    required=False,
    type=str,
)
@click.option(
    "--anyscale-operator-iam-identity",
    help="On the Kubernetes compute stack, the cloud provider IAM identity federated with the Anyscale Operator's kubernetes service account, which will be used by Anyscale control plane for validation during Anyscale Operator bootstrap in the dataplane. IN AWS EKS, this is the ARN of the IAM role. For GCP GKE, this is the service account email.",
    required=False,
    type=str,
)
@click.option(
    "--private-network", help="Use private network.", is_flag=True, default=False,
)
@click.option(
    "--functional-verify",
    help="Verify the cloud is functional. This will check that the cloud can launch workspace/service.",
    required=False,
    is_flag=False,
    flag_value="workspace",
)
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Skip asking for confirmation."
)
@click.option(
    "--skip-verifications",
    help="Skip verifications. This will skip all verifications.",
    required=False,
    is_flag=True,
    type=bool,
    default=False,
)
@click.option(
    "--enable-auto-add-user",
    is_flag=True,
    default=False,
    help=(
        "If --enable-auto-add-user is specified for a cloud, all users in the organization "
        "will be added to the cloud by default. Otherwise users will need to be manually granted "
        "permissions to the cloud. Note: There may be up to 30 sec delay for all users to be granted "
        "permissions after the cloud is created."
    ),
)
@click.option(
    "--resource-file",
    "-f",
    help="Path to a YAML file defining a cloud resource. Schema: https://docs.anyscale.com/reference/cloud#cloudresource.",
    required=False,
)
@click.option(
    "--azure-tenant-id",
    help="The Azure Tenant ID to use for the cloud.",
    required=False,
    type=str,
)
@disabled_on_azure("cloud register")
def register_cloud(  # noqa: PLR0913, PLR0912, C901
    provider: Optional[str],
    region: Optional[str],
    compute_stack: ComputeStack,
    per_cloud_domain: bool,
    per_cloud_domain_label: Optional[str],
    name: str,
    vpc_id: str,
    subnet_ids: str,
    file_storage_id: str,
    efs_id: str,
    anyscale_iam_role_id: str,
    instance_iam_role_id: str,
    security_group_ids: str,
    s3_bucket_id: str,
    external_id: Optional[str],
    memorydb_cluster_id: str,
    project_id: str,
    vpc_name: str,
    subnet_names: str,
    filestore_instance_id: str,
    filestore_location: str,
    anyscale_service_account_email: str,
    instance_service_account_email: str,
    provider_name: str,
    firewall_policy_names: str,
    cloud_storage_bucket_name: str,
    cloud_storage_bucket_endpoint: Optional[str],
    cloud_storage_bucket_region: Optional[str],
    nfs_mount_target: List[str],
    nfs_mount_path: str,
    persistent_volume_claim: Optional[str],
    csi_ephemeral_volume_driver: Optional[str],
    memorystore_instance_name: str,
    host_project_id: Optional[str],
    kubernetes_zones: Optional[str],
    kubernetes_redis_endpoint: Optional[str],
    anyscale_operator_iam_identity: Optional[str],
    azure_tenant_id: Optional[str],
    functional_verify: Optional[str],
    private_network: bool,
    yes: bool,
    skip_verifications: bool,
    enable_auto_add_user: bool,
    resource_file: Optional[str],
) -> None:
    if per_cloud_domain_label and not per_cloud_domain:
        raise click.UsageError("--per-cloud-domain-label requires --per-cloud-domain.")
    if per_cloud_domain and compute_stack != ComputeStack.K8S:
        raise click.UsageError("--per-cloud-domain requires --compute-stack k8s.")
    # Load CloudDeployment from the resource file if provided, otherwise build from CLI flags
    if resource_file:
        # Read the spec file.
        path = pathlib.Path(resource_file)
        if not path.exists():
            raise click.ClickException(f"{resource_file} does not exist.")
        if not path.is_file():
            raise click.ClickException(f"{resource_file} is not a file.")

        try:
            # Reading and parsing stay inside the guard: this path is reachable
            # with no flags at all, so a YAML syntax error must not surface as a
            # traceback.
            spec = yaml.safe_load(path.read_text())
            if not isinstance(spec, dict):
                raise ValueError(
                    f"expected a mapping of cloud resource fields, got {type(spec).__name__}"
                )
            cloud_resource = CloudDeployment(**spec)

            # Convert nested dict objects to model objects
            if cloud_resource.file_storage:
                cloud_resource.file_storage = FileStorage(**cloud_resource.file_storage)
            if cloud_resource.object_storage:
                cloud_resource.object_storage = ObjectStorage(
                    **cloud_resource.object_storage
                )
            if cloud_resource.aws_config:
                cloud_resource.aws_config = AWSConfig(**cloud_resource.aws_config)
            if cloud_resource.gcp_config:
                cloud_resource.gcp_config = GCPConfig(**cloud_resource.gcp_config)
            if cloud_resource.azure_config:
                cloud_resource.azure_config = AzureConfig(**cloud_resource.azure_config)
            if cloud_resource.kubernetes_config:
                cloud_resource.kubernetes_config = KubernetesConfig(
                    **cloud_resource.kubernetes_config
                )
            if cloud_resource.connector_config:
                cloud_resource.connector_config = ConnectorConfig(
                    **cloud_resource.connector_config
                )

        except Exception as e:  # noqa: BLE001
            raise click.ClickException(f"Failed to parse cloud resource: {e}")

        # The file is the input source, so routing derives from it. The model's
        # setter only rejects None -- it checks neither casing nor membership --
        # so both have to be enforced here.
        file_provider = str(cloud_resource.provider).strip().lower()
        if file_provider not in _REGISTER_PROVIDERS:
            raise click.ClickException(
                f"Invalid Cloud provider: {cloud_resource.provider} in {resource_file}. "
                f"Available providers are [{', '.join(_REGISTER_PROVIDERS)}]."
            )
        if provider is not None and provider.lower() != file_provider:
            raise click.ClickException(
                f"--provider {provider} conflicts with provider {cloud_resource.provider} "
                f"in {resource_file}. Omit --provider to use the value from the file."
            )
        # The parsed model is sent to the backend verbatim, so store the canonical
        # uppercase enum value rather than whatever casing the file used.
        cloud_resource.provider = file_provider.upper()
        provider = file_provider

    else:
        if not provider:
            raise click.ClickException(
                "--provider is required unless a cloud resource file is provided with --resource-file/-f."
            )

        missing_args: List[str] = []

        # Validate K8S-only storage flags
        if (
            persistent_volume_claim or csi_ephemeral_volume_driver
        ) and compute_stack != ComputeStack.K8S:
            raise click.ClickException(
                "--persistent-volume-claim and --csi-ephemeral-volume-driver are only supported with --compute-stack=k8s"
            )

        # Validate mutual exclusivity of storage configurations
        storage_configs = []
        if nfs_mount_target or nfs_mount_path:
            storage_configs.append("NFS")
        if persistent_volume_claim:
            storage_configs.append("persistent volume claim")
        if csi_ephemeral_volume_driver:
            storage_configs.append("CSI ephemeral volume driver")

        if len(storage_configs) > 1:
            raise click.ClickException(
                f"Storage configurations are mutually exclusive. Found: {', '.join(storage_configs)}. "
                "Please specify only one of: --nfs-mount-target/--nfs-mount-path, --persistent-volume-claim, or --csi-ephemeral-volume-driver"
            )

        if provider == "aws":
            if s3_bucket_id and not cloud_storage_bucket_name:
                cloud_storage_bucket_name = s3_bucket_id
            if efs_id and not file_storage_id:
                file_storage_id = efs_id
            # Check for missing required arguments for AWS clouds,
            # based on the compute stack (not all args are required
            # on all compute stacks).
            required_resources = [
                (vpc_id, "--vpc-id", (ComputeStack.VM)),
                (subnet_ids, "--subnet-ids", (ComputeStack.VM)),
                (anyscale_iam_role_id, "--anyscale-iam_role-id", (ComputeStack.VM),),
                (instance_iam_role_id, "--instance-iam-role-id", (ComputeStack.VM)),
                (security_group_ids, "--security-group-ids", (ComputeStack.VM)),
                (
                    cloud_storage_bucket_name,
                    "--cloud-storage-bucket-name",
                    (ComputeStack.VM, ComputeStack.K8S),
                ),
                (kubernetes_zones, "--kubernetes-zones", (ComputeStack.K8S)),
                (
                    anyscale_operator_iam_identity,
                    "--anyscale-operator-iam-identity",
                    (ComputeStack.K8S),
                ),
            ]

            if not allow_optional_file_storage():
                required_resources.append(
                    (file_storage_id, "--file-storage-id", (ComputeStack.VM)),
                )

            for resource in required_resources:
                if compute_stack in resource[2] and resource[0] is None:
                    missing_args.append(resource[1])

            if len(missing_args) > 0:
                raise click.ClickException(f"Please provide a value for {missing_args}")

            cloud_resource = CloudDeployment(
                compute_stack=compute_stack,
                provider=CloudProviders.AWS,
                region=region,
                networking_mode=NetworkingMode.PRIVATE
                if private_network
                else NetworkingMode.PUBLIC,
                object_storage=ObjectStorage(bucket_name=cloud_storage_bucket_name),
                file_storage=FileStorage(
                    file_storage_id=file_storage_id,
                    persistent_volume_claim=persistent_volume_claim,
                    csi_ephemeral_volume_driver=csi_ephemeral_volume_driver,
                )
                if file_storage_id
                or persistent_volume_claim
                or csi_ephemeral_volume_driver
                else None,
                aws_config=AWSConfig(
                    vpc_id=vpc_id,
                    subnet_ids=subnet_ids.split(",") if subnet_ids else [],
                    security_group_ids=security_group_ids.split(",")
                    if security_group_ids
                    else [],
                    anyscale_iam_role_id=anyscale_iam_role_id,
                    external_id=external_id,
                    cluster_iam_role_id=instance_iam_role_id,
                    memorydb_cluster_name=memorydb_cluster_id,
                ),
                kubernetes_config=KubernetesConfig(
                    anyscale_operator_iam_identity=anyscale_operator_iam_identity,
                    zones=kubernetes_zones.split(",") if kubernetes_zones else [],
                    redis_endpoint=kubernetes_redis_endpoint,
                )
                if compute_stack == ComputeStack.K8S
                else None,
            )

        elif provider == "gcp":
            if filestore_instance_id and not file_storage_id:
                file_storage_id = filestore_instance_id
            # Keep the parameter naming ({resource}_name or {resource}_id) consistent with GCP to reduce confusion for customers
            # Check if all required parameters are provided
            # memorystore_instance_name and host_project_id are optional for GCP clouds
            required_resources = [
                (project_id, "--project-id", (ComputeStack.VM)),
                (vpc_name, "--vpc-name", (ComputeStack.VM)),
                (subnet_names, "--subnet-names", (ComputeStack.VM)),
                (
                    anyscale_service_account_email,
                    "--anyscale-service-account-email",
                    (ComputeStack.VM),
                ),
                (
                    instance_service_account_email,
                    "--instance-service-account-email",
                    (ComputeStack.VM),
                ),
                (provider_name, "--provider-name", (ComputeStack.VM)),
                (firewall_policy_names, "--firewall-policy-names", (ComputeStack.VM)),
                (
                    cloud_storage_bucket_name,
                    "--cloud-storage-bucket-name",
                    (ComputeStack.VM, ComputeStack.K8S),
                ),
                (kubernetes_zones, "--kubernetes-zones", (ComputeStack.K8S)),
                (
                    anyscale_operator_iam_identity,
                    "--anyscale-operator-iam-identity",
                    (ComputeStack.K8S),
                ),
            ]

            if not allow_optional_file_storage():
                required_resources.extend(
                    [
                        (file_storage_id, "--file-storage-id", (ComputeStack.VM)),
                        (filestore_location, "--filestore-location", (ComputeStack.VM)),
                    ]
                )

            for resource in required_resources:
                if compute_stack in resource[2] and resource[0] is None:
                    missing_args.append(resource[1])

            if len(missing_args) > 0:
                raise click.ClickException(f"Please provide a value for {missing_args}")

            cloud_resource = CloudDeployment(
                compute_stack=compute_stack,
                provider=CloudProviders.GCP,
                region=region,
                networking_mode=NetworkingMode.PRIVATE
                if private_network
                else NetworkingMode.PUBLIC,
                object_storage=ObjectStorage(bucket_name=cloud_storage_bucket_name),
                file_storage=FileStorage(
                    file_storage_id="projects/{}/locations/{}/instances/{}".format(
                        project_id, filestore_location, file_storage_id
                    )
                    if file_storage_id
                    else None,
                    persistent_volume_claim=persistent_volume_claim,
                    csi_ephemeral_volume_driver=csi_ephemeral_volume_driver,
                )
                if file_storage_id
                or persistent_volume_claim
                or csi_ephemeral_volume_driver
                else None,
                gcp_config=GCPConfig(
                    project_id=project_id,
                    host_project_id=host_project_id,
                    provider_name=provider_name,
                    vpc_name=vpc_name,
                    subnet_names=subnet_names.split(",") if subnet_names else [],
                    firewall_policy_names=firewall_policy_names.split(",")
                    if firewall_policy_names
                    else [],
                    anyscale_service_account_email=anyscale_service_account_email,
                    cluster_service_account_email=instance_service_account_email,
                    memorystore_instance_name=memorystore_instance_name,
                ),
                kubernetes_config=KubernetesConfig(
                    anyscale_operator_iam_identity=anyscale_operator_iam_identity,
                    zones=kubernetes_zones.split(",") if kubernetes_zones else [],
                    redis_endpoint=kubernetes_redis_endpoint,
                )
                if compute_stack == ComputeStack.K8S
                else None,
            )

        elif provider in ("azure", "generic"):
            # For the 'generic' provider type, for the time being, most fields are optional; only 'name', 'provider', and 'compute-stack' are required.
            if not name:
                raise click.ClickException("Please provide a value for --name.")

            if compute_stack != ComputeStack.K8S:
                raise click.ClickException(
                    "--compute-stack=k8s must be passed to register this Anyscale cloud."
                )

            # Handle parsing / conversion of nfs_mount_targets.
            mount_targets: List[NFSMountTarget] = []
            for target in nfs_mount_target or []:
                parts = [part.strip() for part in target.split(",")]
                if len(parts) == 1:
                    mount_targets.append(NFSMountTarget(address=parts[0]))
                elif len(parts) == 2:
                    mount_targets.append(
                        NFSMountTarget(address=parts[1], zone=parts[0])
                    )
                else:
                    raise click.ClickException(
                        f"Invalid mount target {target}; expected (zone,address) tuple or a singular address."
                    )

            cloud_provider = (
                CloudProviders.AZURE if provider == "azure" else CloudProviders.GENERIC
            )

            cloud_resource = CloudDeployment(
                compute_stack=ComputeStack.K8S,
                provider=cloud_provider,
                region=region or "default",
                object_storage=ObjectStorage(
                    bucket_name=cloud_storage_bucket_name,
                    region=cloud_storage_bucket_region or region,
                    endpoint=cloud_storage_bucket_endpoint,
                )
                if cloud_storage_bucket_name
                else None,
                file_storage=FileStorage(
                    mount_targets=mount_targets,
                    mount_path=nfs_mount_path,
                    persistent_volume_claim=persistent_volume_claim,
                    csi_ephemeral_volume_driver=csi_ephemeral_volume_driver,
                )
                if mount_targets
                or persistent_volume_claim
                or csi_ephemeral_volume_driver
                else None,
                azure_config=AzureConfig(tenant_id=azure_tenant_id)
                if provider == "azure" and azure_tenant_id
                else None,
                kubernetes_config=KubernetesConfig(
                    anyscale_operator_iam_identity=anyscale_operator_iam_identity
                    if provider == "azure"
                    else None,
                    zones=kubernetes_zones.split(",") if kubernetes_zones else [],
                    redis_endpoint=kubernetes_redis_endpoint,
                ),
            )

        else:
            raise click.ClickException(
                f"Invalid Cloud provider: {provider}. Available providers are [{', '.join(_REGISTER_PROVIDERS)}]."
            )

    if cloud_resource.compute_stack != ComputeStack.VM:
        placeholder_problems = placeholder_credential_problems(cloud_resource)
        if placeholder_problems:
            raise click.ClickException(" ".join(placeholder_problems))

    if provider == "aws":
        CloudController().register_aws_cloud(
            name=name,
            cloud_resource=cloud_resource,
            functional_verify=functional_verify,
            cluster_management_stack_version=ClusterManagementStackVersions.V2,
            yes=yes,
            skip_verifications=skip_verifications,
            auto_add_user=enable_auto_add_user,
            per_cloud_domain=per_cloud_domain,
            per_cloud_domain_label=per_cloud_domain_label,
        )
    elif provider == "gcp":
        CloudController().register_gcp_cloud(
            name=name,
            cloud_resource=cloud_resource,
            functional_verify=functional_verify,
            cluster_management_stack_version=ClusterManagementStackVersions.V2,
            yes=yes,
            skip_verifications=skip_verifications,
            auto_add_user=enable_auto_add_user,
            per_cloud_domain=per_cloud_domain,
            per_cloud_domain_label=per_cloud_domain_label,
        )
    elif provider in ("azure", "generic"):
        CloudController().register_azure_or_generic_cloud(
            name=name,
            provider=provider,
            cloud_resource=cloud_resource,
            auto_add_user=enable_auto_add_user,
            per_cloud_domain=per_cloud_domain,
            per_cloud_domain_label=per_cloud_domain_label,
        )
    else:
        raise click.ClickException(
            f"Invalid Cloud provider: {provider}. Available providers are [{', '.join(_REGISTER_PROVIDERS)}]."
        )


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Verify the health of a cloud.",
            command="anyscale cloud verify -n my-cloud",
        ),
    ],
)
@cloud_cli.command(
    name="verify",
    short_help="Check the health of a cloud.",
    help=(
        "Check the health of a cloud.\n\n"
        "Specify the cloud by name (-n/--name) or by ID (--cloud-id)."
    ),
    cls=AnyscaleCommand,
)
@click.argument("cloud-name", required=False)
@click.option("--name", "-n", help="Verify cloud by name.", type=str)
@click.option(
    "--cloud-id",
    "--id",
    "cloud_id",
    help="Verify cloud by cloud id, alternative to cloud name.",
    required=False,
)
@click.option(
    "--functional-verify",
    help="Verify the cloud is functional. This will check that the cloud can launch workspace/service.",
    required=False,
    is_flag=False,
    flag_value="workspace",
)
@click.option(
    "--cloud-resource-name",
    help=(
        "Verify only the cloud resource with this name. If omitted, all cloud "
        "resources for the cloud are verified."
    ),
    required=False,
)
@click.option(
    "--strict",
    is_flag=True,
    default=False,
    help="Strict Verify. Treat warnings as failures.",
)
@click.option(
    "--yes", "-y", is_flag=True, default=False, help="Skip asking for confirmation."
)
def cloud_verify(
    cloud_name: Optional[str],
    name: Optional[str],
    cloud_id: Optional[str],
    functional_verify: Optional[str],
    cloud_resource_name: Optional[str],
    strict: bool = False,
    yes: bool = False,
) -> bool:
    if cloud_name and name and cloud_name != name:
        raise click.ClickException(
            "The positional argument CLOUD_NAME and the keyword argument --name "
            "were both provided. Please only provide one of these two arguments."
        )

    return CloudController().verify_cloud(
        cloud_name=cloud_name or name,
        cloud_id=cloud_id,
        functional_verify=functional_verify,
        cloud_resource_name=cloud_resource_name,
        strict=strict,
        yes=yes,
    )


@command_metadata(
    status=ReleaseStatus.DEPRECATED,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Edit the S3 bucket of a registered cloud.",
            command="anyscale cloud edit -n my-cloud --aws-s3-id my-new-bucket",
        ),
    ],
    deprecation_info={"message": "Use anyscale cloud update instead."},
)
@cloud_cli.command(
    name="edit",
    short_help="Edit a registered cloud.",
    help="Use `anyscale cloud update` instead.\n\nEdit registered cloud resource on Anyscale. Only applicable for Anyscale registered clouds.",
    cls=AnyscaleCommand,
)
@click.argument("cloud-name", required=False)
@click.option("--name", "-n", help="Edit cloud by name.", type=str)
@click.option(
    "--cloud-id",
    "--id",
    "cloud_id",
    help="Edit cloud by id, alternative to cloud name.",
    required=False,
)
@click.option(
    "--aws-s3-id", help="New S3 bucket ID.", required=False, type=str,
)
@click.option("--aws-efs-id", help="New EFS ID.", required=False, type=str)
@click.option(
    "--aws-efs-mount-target-ip",
    help="New EFS mount target IP.",
    required=False,
    type=str,
)
@click.option(
    "--memorydb-cluster-id",
    help="New AWS Memorydb cluster ID.",
    required=False,
    type=str,
)
@click.option(
    "--gcp-filestore-instance-id",
    help="New GCP filestore instance id.",
    required=False,
    type=str,
)
@click.option(
    "--gcp-filestore-location",
    help="New GCP filestore location.",
    required=False,
    type=str,
)
@click.option(
    "--gcp-cloud-storage-bucket-name",
    help="New GCP Cloud storage bucket name.",
    required=False,
    type=str,
)
@click.option(
    "--memorystore-instance-name",
    help="New Memorystore instance name for GCP clouds",
    required=False,
    type=str,
)
@click.option(
    "--functional-verify",
    help="Verify the cloud is functional. This will check that the cloud can launch workspace/service.",
    required=False,
    is_flag=False,
    flag_value="workspace",
)
@click.option(
    "--enable-auto-add-user/--disable-auto-add-user",
    default=None,
    help=(
        "If --enable-auto-add-user is specified for a cloud, all users in the organization "
        "will be added to the cloud by default. Note: There may be up to 30 sec delay for all users to be granted "
        "permissions after this feature is enabled.\n\n"
        "Specifying --disable-auto-add-user will require that users "
        "are manually granted permissions to access the cloud. No existing cloud permissions are altered by specifying this flag."
    ),
)
def cloud_edit(  # noqa: PLR0913
    cloud_name: Optional[str],
    name: Optional[str],
    cloud_id: Optional[str],
    aws_s3_id: Optional[str],
    aws_efs_id: Optional[str],
    aws_efs_mount_target_ip: Optional[str],
    memorydb_cluster_id: Optional[str],
    gcp_filestore_instance_id: Optional[str],
    gcp_filestore_location: Optional[str],
    gcp_cloud_storage_bucket_name: Optional[str],
    memorystore_instance_name: Optional[str],
    functional_verify: Optional[str],
    enable_auto_add_user: Optional[bool],
) -> None:
    if cloud_name and name and cloud_name != name:
        raise click.ClickException(
            "The positional argument CLOUD_NAME and the keyword argument --name "
            "were both provided. Please only provide one of these two arguments."
        )
    if any(
        [
            aws_s3_id,
            aws_efs_id,
            aws_efs_mount_target_ip,
            memorydb_cluster_id,
            gcp_filestore_instance_id,
            gcp_filestore_location,
            gcp_cloud_storage_bucket_name,
            memorystore_instance_name,
            enable_auto_add_user is not None,
        ]
    ):
        if any([gcp_filestore_instance_id, gcp_filestore_location]) and not all(
            [gcp_filestore_instance_id, gcp_filestore_location]
        ):
            # Make sure both gcp_filestore_instance_id and gcp_filestore_location are provided if you want to edit filestore.
            raise click.ClickException(
                "Please provide both --gcp-filestore-instance-id and --gcp-filestore-location if you want to edit filestore."
            )
        if (
            memorystore_instance_name is not None
            and re.search(
                "projects/.+/locations/.+/instances/.+", memorystore_instance_name
            )
            is None
        ):
            raise click.ClickException(
                "Please provide a valid memorystore instance name. Example: projects/<project number>/locations/<location>/instances/<instance id>"
            )
        CloudController().edit_cloud(
            cloud_name=cloud_name or name,
            cloud_id=cloud_id,
            aws_s3_id=aws_s3_id,
            aws_efs_id=aws_efs_id,
            aws_efs_mount_target_ip=aws_efs_mount_target_ip,
            memorydb_cluster_id=memorydb_cluster_id,
            gcp_filestore_instance_id=gcp_filestore_instance_id,
            gcp_filestore_location=gcp_filestore_location,
            gcp_cloud_storage_bucket_name=gcp_cloud_storage_bucket_name,
            memorystore_instance_name=memorystore_instance_name,
            functional_verify=functional_verify,
            auto_add_user=enable_auto_add_user,
        )
    else:
        raise click.ClickException(
            "Please provide at least one of the following arguments: --aws-s3-id, --aws-efs-id, --aws-efs-mount-target-ip, --memorydb-cluster-id, --gcp-filestore-instance-id, --gcp-filestore-location, --gcp-cloud-storage-bucket-name, --memorystore-instance-name, --enable-auto-add-user, --disable-auto-add-user."
        )


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Add collaborators to a cloud from a YAML file.",
            command="anyscale cloud add-collaborators -c my-cloud --users-file collaborators.yaml",
            output_raw=command_examples.CLOUD_ADD_COLLABORATORS_EXAMPLE,
        ),
    ],
)
@cloud_cli.command(
    name="add-collaborators",
    short_help="Add collaborators to the cloud.",
    help="Add collaborators to the cloud.",
    cls=AnyscaleCommand,
)
@click.option(
    "--cloud", "-c", help="Name of the cloud to add collaborators to.", required=True
)
@click.option(
    "--users-file",
    help="Path to a YAML file containing a list of users to add to the cloud.",
    required=True,
)
def add_collaborators(cloud: str, users_file: str,) -> None:
    collaborators = CreateCloudCollaborators.from_yaml(users_file)

    try:
        anyscale.cloud.add_collaborators(
            cloud=cloud,
            collaborators=[
                CreateCloudCollaborator(**collaborator)
                for collaborator in collaborators.collaborators
            ],
        )
    except ValueError as e:
        raise UserError(
            f"Error adding collaborators to cloud: {e}", legacy_exit_code=0
        ) from None

    log.info(
        f"Successfully added {len(collaborators.collaborators)} collaborators to cloud {cloud}."
    )


def _get_cloud_info(
    cloud_id: Optional[str],
    name: Optional[str],
    output: Optional[str],
    include_status: bool,
    output_format: str = OutputFormat.TEXT.value,
) -> None:
    """
    Internal helper to retrieve cloud information.

    :param cloud_id: The ID of the cloud to retrieve.
    :param name: The name of the cloud to retrieve.
    :param output: Optional file path to write output to.
    :param include_status: If True, include status fields (created_at, is_default,
        operator_status, operator_status_details). If False, these fields are hidden.
    :param output_format: Structured output format for stdout; ignored when
        writing to a file.
    """
    # Validate that exactly one of --name or --cloud-id is provided
    if (cloud_id and name) or (not cloud_id and not name):
        raise InvalidConfigError(
            "Please provide exactly one of --name or --cloud-id.", legacy_exit_code=0
        )

    try:
        cloud = anyscale.cloud.get(id=cloud_id, name=name)

        if not cloud:
            raise ResourceNotFoundError("Cloud not found.", legacy_exit_code=0)

        # Include all cloud resources for the cloud.
        cloud_resources = CloudController().get_formatted_cloud_resources(
            cloud_id=cloud.id
        )

        if not include_status:
            # Remove status fields from cloud resources for cleaner output.
            # Use `anyscale cloud status` to see full status information.
            status_fields_to_hide = {
                "created_at",
                "is_default",
                "operator_status",
                "operator_status_details",
            }
            for resource in cloud_resources:
                for field in status_fields_to_hide:
                    resource.pop(field, None)

        info = CloudInfo(
            name=cloud.name,
            id=cloud.id,
            created_at=cloud.created_at if include_status else None,
            is_default=cloud.is_default if include_status else None,
            resources=cloud_resources,
        )

        # On status, keep None-valued keys (e.g. created_at) as explicit nulls.
        # on get, omit them entirely,
        # This matches the legacy hand-built dicts behaviour.
        info_dict = info.to_dict(exclude_none=not include_status)

        if output:
            with open(output, "w") as f:
                yaml.dump(info_dict, f, sort_keys=False)
        elif output_format != OutputFormat.TEXT.value:
            print_output(info_dict, output_format)
        else:
            print(yaml.dump(info_dict, sort_keys=False))

    except ValueError as e:
        raise UserError(f"Error retrieving cloud: {e}", legacy_exit_code=0) from None


@command_metadata(
    status=ReleaseStatus.GA,
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
            description="Get information about a cloud by name.",
            command="anyscale cloud get -n my-cloud",
            output_raw=command_examples.CLOUD_GET_CLOUD_EXAMPLE,
            output_instance=lambda: CloudInfo(
                name="my-cloud",
                id="cld_abc123",
                created_at=None,
                is_default=None,
                resources=[
                    {
                        "cloud_resource_id": "cldrsrc_abc123",
                        "name": "vm-aws-us-west-2",
                        "provider": "AWS",
                        "compute_stack": "VM",
                        "region": "us-west-2",
                        "networking_mode": "PUBLIC",
                    }
                ],
            ),
        ),
    ],
    output_schema=CloudInfo,
)
@cloud_cli.command(
    name="get",
    short_help="Get information about a specific cloud.",
    help="Get information about a specific cloud.",
    cls=AnyscaleCommand,
)
@click.option(
    "--name",
    "-n",
    help="Name of the cloud to get information about.",
    type=str,
    required=False,
)
@click.option(
    "--cloud-id",
    "--id",
    "cloud_id",
    help="ID of the cloud to get information about.",
    type=str,
    required=False,
)
@click.option(
    "--output-file",
    "output_file",
    help="File to write the output YAML to.",
    type=click.Path(),
    required=False,
)
@click.option(
    "--output",
    "-o",
    help="File to write the output YAML to.",
    type=str,
    required=False,
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
def get_cloud(
    cloud_id: Optional[str],
    name: Optional[str],
    output_file: Optional[str],
    output: Optional[str],
    output_format: str,
) -> None:
    """
    Retrieve a cloud by its name or ID and display its details.

    This command outputs a simplified format suitable for use with `anyscale cloud update`.
    For full cloud status information including operator status, use `anyscale cloud status`.

    :param cloud_id: The ID of the cloud to retrieve.
    :param name: The name of the cloud to retrieve.
    """
    if output:
        warn_deprecated_flag("-o/--output", "--output-file")
    _get_cloud_info(
        cloud_id,
        name,
        output_file or output,
        include_status=False,
        output_format=output_format,
    )


@command_metadata(
    status=ReleaseStatus.GA,
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
            description="Get the full status of a cloud by name.",
            command="anyscale cloud status -n my-cloud",
            output_raw=command_examples.CLOUD_STATUS_EXAMPLE,
            output_instance=lambda: CloudInfo(
                name="my-cloud",
                id="cld_abc123",
                created_at=datetime(2026, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
                is_default=True,
                resources=[
                    {
                        "cloud_resource_id": "cldrsrc_abc123",
                        "name": "k8s-aws-us-west-2",
                        "provider": "AWS",
                        "compute_stack": "K8S",
                        "region": "us-west-2",
                        "operator_status": "HEALTHY",
                        "operator_status_details": {
                            "operator_version": "1.2.1",
                            "check_results": [
                                {"name": "kubernetes_permissions", "status": "HEALTHY"},
                                {"name": "iam_identity", "status": "HEALTHY"},
                            ],
                            "reported_at": "2026-01-01T00:00:00+00:00",
                        },
                    }
                ],
            ),
        ),
    ],
    output_schema=CloudInfo,
)
@cloud_cli.command(
    name="status",
    short_help="Get full status information about a specific cloud including operator status.",
    help="Get full status information about a specific cloud including operator status.",
    cls=AnyscaleCommand,
)
@click.option(
    "--name",
    "-n",
    help="Name of the cloud to get status for.",
    type=str,
    required=False,
)
@click.option(
    "--cloud-id",
    "--id",
    "cloud_id",
    help="ID of the cloud to get status for.",
    type=str,
    required=False,
)
@click.option(
    "--output-file",
    "output_file",
    help="File to write the output YAML to.",
    type=click.Path(),
    required=False,
)
@click.option(
    "--output",
    "-o",
    help="File to write the output YAML to.",
    type=str,
    required=False,
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
def cloud_status(
    cloud_id: Optional[str],
    name: Optional[str],
    output_file: Optional[str],
    output: Optional[str],
    output_format: str,
) -> None:
    """
    Retrieve full status information for a cloud including operator status details.

    This command outputs all fields including created_at, is_default, operator_status,
    and operator_status_details. For a simplified format suitable for `anyscale cloud update`,
    use `anyscale cloud get`.

    :param cloud_id: The ID of the cloud to retrieve.
    :param name: The name of the cloud to retrieve.
    """
    if output:
        warn_deprecated_flag("-o/--output", "--output-file")
    _get_cloud_info(
        cloud_id,
        name,
        output_file or output,
        include_status=True,
        output_format=output_format,
    )


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT, OutputFormat.JSON, OutputFormat.YAML],
    examples=[
        CommandExample(
            description="Get the default cloud for your organization.",
            command="anyscale cloud get-default",
            output_raw=command_examples.CLOUD_GET_DEFAULT_CLOUD_EXAMPLE,
            output_instance=lambda: Cloud(
                name="my-cloud",
                id="cld_abc123",
                provider=CloudProvider.AWS,
                compute_stack=CloudModelComputeStack.VM,
                region="us-west-2",
                is_default=True,
            ),
        ),
    ],
    output_schema=Cloud,
)
@cloud_cli.command(
    name="get-default",
    short_help="Get the default cloud for your organization.",
    help="Get the default cloud for your organization.",
    cls=AnyscaleCommand,
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
def get_default_cloud(output_format: str) -> None:
    """
    Retrieve and display the default cloud configured for your organization.
    """
    try:
        default_cloud = anyscale.cloud.get_default()

        if not default_cloud:
            raise ResourceNotFoundError("No default cloud found.", legacy_exit_code=0)

        if output_format != OutputFormat.TEXT.value:
            print_output(default_cloud, output_format)
            return

        cloud_dict = (
            default_cloud.to_dict()
            if hasattr(default_cloud, "to_dict")
            else default_cloud.__dict__
        )

        print(yaml.dump(cloud_dict, sort_keys=False))

    except ValueError as e:
        raise UserError(
            f"Error retrieving default cloud: {e}", legacy_exit_code=0
        ) from None


@cloud_cli.command(
    name="jobs-report",
    help=(
        "Generate a report of the jobs created in the last 7 days in HTML format. "
        "Shows unused CPU-hours, unused GPU-hours, and other data."
    ),
    cls=AnyscaleCommand,
    hidden=True,
)
@click.option(
    "--cloud-id",
    help="ID of the cloud to generate a report on.",
    type=str,
    required=True,
)
@click.option(
    "--csv",
    help="Outputs the report in CSV format.",
    type=bool,
    required=False,
    default=False,
    is_flag=True,
)
@click.option(
    "--out",
    help="Output file name for the report. (Default jobs_report.html)",
    type=str,
    required=False,
    default=None,
)
@click.option(
    "--sort-by",
    help=(
        "Column to sort by. (Default created_at). "
        "created_at: Job creation time. "
        "gpu: Unused GPU hours. "
        "cpu: Unused CPU hours. "
        "instances: Number of instances."
    ),
    type=click.Choice(["created_at", "gpu", "cpu", "instances"], case_sensitive=False),
    required=False,
    default="created_at",
)
@click.option(
    "--sort-order",
    help="Sort order. (Default desc)",
    type=click.Choice(["asc", "desc"], case_sensitive=False),
    required=False,
    default="desc",
)
def generate_jobs_report(
    cloud_id: str, csv: bool, out: Optional[str], sort_by: str, sort_order: str
) -> None:
    """
    Generate a report of the jobs created in the last 7 days in HTML format.
    Shows unused CPU-hours, unused GPU-hours, and other data.
    :param cloud_id: The ID of the cloud to generate a report on.
    :param csv: Outputs the report in CSV format.
    :param out: Output file name for the report.
    """
    if out is None:
        out = "jobs_report.html" if not csv else "jobs_report.csv"

    try:
        CloudController().generate_jobs_report(
            cloud_id, csv, out, sort_by, sort_order == "asc"
        )
    except ValueError as e:
        raise UserError(
            f"Error generating jobs report: {e}", legacy_exit_code=0
        ) from None


@command_metadata(
    status=ReleaseStatus.GA,
    since="0.0.0",
    output_formats=[OutputFormat.TEXT],
    examples=[
        CommandExample(
            description="Terminate the system cluster of a cloud by ID.",
            command="anyscale cloud terminate-system-cluster --cloud-id cld_abcdef",
            output_raw=command_examples.CLOUD_TERMINATE_SYSTEM_CLUSTER_EXAMPLE,
        ),
    ],
)
@cloud_cli.command(
    name="terminate-system-cluster",
    short_help="Terminate the system cluster for a specific cloud.",
    help="Terminate the system cluster for a specific cloud.",
    cls=AnyscaleCommand,
)
@click.option(
    "--cloud-id",
    "--id",
    "cloud_id",
    help="ID of the cloud to terminate the system cluster for.",
    type=str,
    required=True,
)
@click.option(
    "-w",
    "--wait",
    required=False,
    default=False,
    type=bool,
    is_flag=True,
    help="Block this CLI command until the system cluster is terminated.",
)
def terminate_system_cluster(cloud_id: str, wait: Optional[bool]) -> None:
    """
    Terminate the system cluster for a specific cloud.

    :param cloud_id: The ID of the cloud to terminate the system cluster for.
    :param wait: If True, wait for the system cluster to be terminated before returning. Defaults to False.
    """
    try:
        anyscale.cloud.terminate_system_cluster(cloud_id, wait)
    except ValueError as e:
        raise UserError(
            f"Error terminating system cluster: {e}", legacy_exit_code=0
        ) from None


# --- Gateway Migration Commands ---


@cloud_cli.command(
    name="start-gateway-migration",
    help="Start gateway migration. Creates dual-stack (Ingress + HTTPRoute) with canary_weight=0.",
    cls=AnyscaleCommand,
    hidden=True,
)
@click.option(
    "--cloud-id", help="ID of the cloud.", type=str, required=True,
)
def start_gateway_migration(cloud_id: str) -> None:
    controller = CloudController()
    controller.start_gateway_migration(cloud_id)


@cloud_cli.command(
    name="set-gateway-canary-weight",
    help="Set the gateway migration canary weight (0-100). 100 = migration done, HTTPRoute only.",
    cls=AnyscaleCommand,
    hidden=True,
)
@click.option(
    "--cloud-id", help="ID of the cloud.", type=str, required=True,
)
@click.option(
    "--weight",
    help="Canary weight (0-100). Percentage of traffic routed through the gateway.",
    type=int,
    required=True,
)
def set_gateway_canary_weight(cloud_id: str, weight: int) -> None:
    controller = CloudController()
    controller.set_gateway_canary_weight(cloud_id, weight)


@cloud_cli.command(
    name="gateway-migration-status",
    help="Get the gateway migration status for a cloud.",
    cls=AnyscaleCommand,
    hidden=True,
)
@click.option(
    "--cloud-id", help="ID of the cloud.", type=str, required=True,
)
def gateway_migration_status(cloud_id: str) -> None:
    controller = CloudController()
    controller.gateway_migration_status(cloud_id)
