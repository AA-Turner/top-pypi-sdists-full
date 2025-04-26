from typing import Optional

import rich_click as click

from union._config import _DEFAULT_DOMAIN, _DEFAULT_PROJECT_BYOC, _UNION_DEFAULT_CONFIG_PATH
from union.cli._option import MutuallyExclusiveArgument, MutuallyExclusiveOption
from union.internal.identity.app_payload_pb2 import DeleteAppRequest, GetAppRequest
from union.internal.secret.definition_pb2 import SecretIdentifier
from union.internal.secret.payload_pb2 import DeleteSecretRequest
from union.remote import UnionRemote
from union.workspace._vscode_remote import _get_workspace_executions


@click.group()
def delete():
    """Delete a resource."""


@delete.command()
@click.argument(
    "name",
    required=False,
    cls=MutuallyExclusiveArgument,
    mutually_exclusive=["name_option"],
    error_msg="Please pass --name once: `union delete secret --name NAME`",
)
@click.option(
    "--name",
    "name_option",
    help="Secret name",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["name"],
    error_msg="Please pass --name once: `union create secret --name NAME`",
)
@click.option("--project", help="Project name")
@click.option("--domain", help="Domain name")
def secret(
    name: Optional[str],
    name_option: Optional[str],
    project: Optional[str],
    domain: Optional[str],
):
    """Delete secret with NAME."""
    name = name or name_option

    remote = UnionRemote(default_domain=domain, default_project=project)
    stub = remote.secret_client

    request = DeleteSecretRequest(
        id=SecretIdentifier(name=name, domain=domain, project=project),
    )
    try:
        stub.DeleteSecret(request)
        click.echo(f"Deleted secret with name: {name}")
    except Exception as e:
        raise click.ClickException(f"Unable to delete secret with name: {name}\n{e}") from e


@delete.group("api-key")
def api_key():
    """Manage API keys."""


@api_key.command("admin")
@click.option("--name", type=str, help="Name for API key", required=True)
def admin(name: str):
    """Delete api key."""
    remote = UnionRemote()
    stub = remote.apps_service_client

    # Get app first to make sure it exist
    get_request = GetAppRequest(client_id=name)
    try:
        stub.Get(get_request)
    except Exception as e:
        raise click.ClickException(f"Unable to delete api-key with name: {name} because it does not exist.\n{e}") from e

    delete_request = DeleteAppRequest(client_id=name)
    try:
        stub.Delete(delete_request)
        click.echo(f"Deleted api-key with name: {name}")
    except Exception as e:
        raise click.ClickException(f"Unable to delete api-key with name: {name}\n{e}") from e


@delete.command()
def login():
    """Delete login information."""
    if not _UNION_DEFAULT_CONFIG_PATH.exists():
        click.echo(f"Login at {_UNION_DEFAULT_CONFIG_PATH} does not exist. No need to delete.")
        return

    try:
        _UNION_DEFAULT_CONFIG_PATH.unlink()
        click.echo("Deleted login.")
    except Exception as e:
        msg = f"Unable to delete login.\n{e}"
        raise click.ClickException(msg) from e


@delete.command()
@click.pass_context
@click.argument("name")
@click.option("--project", default=_DEFAULT_PROJECT_BYOC, help="Project name")
@click.option("--domain", default=_DEFAULT_DOMAIN, help="Domain name")
def workspace(ctx: click.Context, name: str, project: str, domain: str):
    """Delete workspace with NAME."""
    remote = UnionRemote(default_domain=domain, default_project=project)

    executions = _get_workspace_executions(remote, project, domain)

    for execution, workspace_name in executions:
        if workspace_name == name:
            remote.terminate(execution, cause="Stopped from CLI")
            click.echo(f"Workspace {name} deleted!")
            break
    else:  # no break
        click.echo(f"Workspace with name: {name} does not exist or no longer running")
