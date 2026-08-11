from typing import Optional

import click
import yaml

from anyscale.cli_logger import BlockLogger
from anyscale.cloud_utils import (
    get_cloud_id_and_name,
    get_organization_default_cloud,
)
from anyscale.commands.util import AnyscaleCommand
from anyscale.controllers.kuberay_workload_controller import KuberayWorkloadController


log = BlockLogger()


@click.command(
    name="apply",
    cls=AnyscaleCommand,
    # Hidden until the platform-submit flow is end-to-end (the scheduler stack must
    # land). Fully usable; kept out of public --help/docs meanwhile. To document it,
    # drop `hidden` and add an @command_metadata(examples=[...]) block.
    hidden=True,
    short_help="Submit a KubeRay workload (RayJob) to run on Anyscale.",
    example="anyscale apply -f rayjob.yaml --cloud my-cloud",
)
@click.option(
    "-f",
    "--file",
    "file",
    required=True,
    type=str,
    help="Path to a YAML file containing the KubeRay CR (a RayJob) to run.",
)
@click.option(
    "--cloud",
    required=False,
    default=None,
    type=str,
    help="Name of the Anyscale cloud to run the workload on.",
)
@click.option(
    "--cloud-id",
    required=False,
    default=None,
    type=str,
    help="ID of the Anyscale cloud to run the workload on (alternative to --cloud).",
)
@click.option(
    "--project-id",
    required=False,
    default=None,
    type=str,
    help="ID of the project to run the workload under. Defaults to the cloud's default project.",
)
@click.option(
    "-n",
    "--name",
    required=False,
    default=None,
    type=str,
    help="Name for the workload. Defaults to the CR's metadata.name.",
)
def apply(
    file: str,
    cloud: Optional[str],
    cloud_id: Optional[str],
    project_id: Optional[str],
    name: Optional[str],
) -> None:
    """Submit a KubeRay workload defined in a YAML file to run on Anyscale.

    Reads the KubeRay custom resource (a RayJob) from the file and submits it to the
    target cloud. The workload is recorded and the platform schedules and dispatches
    it onto the cloud's KubeRay cluster.
    """
    try:
        with open(file) as f:
            spec = yaml.safe_load(f)
    except OSError as e:
        raise click.ClickException(f"Could not read file '{file}': {e}")
    except yaml.YAMLError as e:
        raise click.ClickException(f"'{file}' is not valid YAML: {e}")
    if not isinstance(spec, dict):
        raise click.ClickException(
            f"'{file}' must contain a single KubeRay CR (a YAML mapping)."
        )

    controller = KuberayWorkloadController()
    if cloud or cloud_id:
        resolved_cloud_id, _ = get_cloud_id_and_name(
            controller.api_client, cloud_id=cloud_id, cloud_name=cloud,
        )
    else:
        # No cloud flag: fall back to the organization's default cloud
        # (set via `anyscale cloud set-default`).
        default_cloud_name = get_organization_default_cloud(controller.api_client)
        if not default_cloud_name:
            raise click.ClickException(
                "No cloud specified and no organization default cloud is set. "
                "Pass --cloud/--cloud-id, or set a default with "
                "`anyscale cloud set-default <cloud>`."
            )
        resolved_cloud_id, _ = get_cloud_id_and_name(
            controller.api_client, cloud_name=default_cloud_name,
        )
        log.info(f"Using organization default cloud '{default_cloud_name}'.")

    response = controller.apply(
        spec=spec, cloud_id=resolved_cloud_id, project_id=project_id, name=name,
    )
    log.info(
        f"Submitted {response.workload_type} '{response.name}' "
        f"(id: {response.workload_id}, state: {response.state})."
    )
