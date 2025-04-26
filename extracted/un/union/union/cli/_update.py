import logging
from pathlib import Path
from typing import Optional

import rich.markup
import rich_click as click
from rich.console import Console

from union.app import App
from union.cli._option import MutuallyExclusiveArgument, MutuallyExclusiveOption
from union.internal.secret.definition_pb2 import SecretIdentifier, SecretSpec
from union.internal.secret.payload_pb2 import UpdateSecretRequest
from union.remote import UnionRemote
from union.workspace._vscode import WorkspaceConfig, build_workspace_image

logger = logging.getLogger("union.cli._update")


@click.group(name="update")
def update():
    """Update a resource."""


@update.command()
@click.argument(
    "name",
    required=False,
    cls=MutuallyExclusiveArgument,
    mutually_exclusive=["name_option"],
    error_msg="Please pass --name once: `union update secret --name NAME`",
)
@click.option(
    "--name",
    "name_option",
    help="Secret name",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["name"],
    error_msg="Please pass --name once: `union update secret --name NAME`",
)
@click.option(
    "--value",
    help="Secret value",
    prompt="Enter secret value",
    hide_input=True,
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["value_file"],
)
@click.option(
    "-f",
    "--value-file",
    help="Path to file containing the secret",
    type=click.Path(exists=True, file_okay=True, dir_okay=False, readable=True, allow_dash=True),
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["value"],
)
@click.option("--project", help="Project name")
@click.option("--domain", help="Domain name")
def secret(
    name: Optional[str],
    name_option: Optional[str],
    value: str,
    value_file: str,
    project: Optional[str],
    domain: Optional[str],
):
    """Update secret with NAME."""
    name = name or name_option

    if value_file:
        with open(value_file, "rb") as f:
            secret_spec = SecretSpec(binary_value=f.read())
    else:
        secret_spec = SecretSpec(string_value=value)

    remote = UnionRemote(default_domain=domain, default_project=project)
    stub = remote.secret_client

    request = UpdateSecretRequest(
        id=SecretIdentifier(name=name, domain=domain, project=project),
        secret_spec=secret_spec,
    )

    try:
        stub.UpdateSecret(request)
        click.echo(f"Updated secret with name: {name}")
    except Exception as e:
        raise click.ClickException(f"Unable to update secret with name: {name}\n{e}") from e


def update_application(app: App, project: str, domain: str):
    from union.configuration import UnionAIPlugin

    remote = UnionAIPlugin.get_remote(config=None, project=project, domain=domain)
    remote._app_remote.update(app)


@update.command()
@click.pass_context
@click.argument("config_file", type=click.Path(path_type=Path))
def workspace(ctx: click.Context, config_file: Path):
    """Update a workspace."""
    config_content = config_file.read_text()
    workspace_config = WorkspaceConfig.from_yaml(config_content)

    remote = UnionRemote(default_domain=workspace_config.domain, default_project=workspace_config.project)
    logger.debug(f"Workspace config: {workspace_config}")
    logger.debug(f"Remote: {remote.__dict__}")
    if not isinstance(workspace_config.container_image, str):
        _image_build_task = build_workspace_image(remote, workspace_config)
        # override container image with the built image
        workspace_config.container_image = _image_build_task.template.container.image
    _update_workspace(remote, workspace_config)


def _update_workspace(remote: UnionRemote, ws_config: WorkspaceConfig):
    from union._async import run_sync
    from union.internal.workspace.workspace_definition_payload_pb2 import CreateWorkspaceDefinitionResponse
    from union.workspace._vscode_remote import WorkspaceRemote

    ws_remote = WorkspaceRemote(
        default_project=ws_config.project,
        default_domain=ws_config.domain,
        union_remote=remote,
    )

    console = Console()
    try:
        ws_def: CreateWorkspaceDefinitionResponse = run_sync(ws_remote.update_workspace_definition, ws_config)
    except Exception as e:
        raise click.ClickException(f"Error updating workspace definition: {rich.markup.escape(str(e))}") from e

    console.print(f"Updated: {ws_def}")
