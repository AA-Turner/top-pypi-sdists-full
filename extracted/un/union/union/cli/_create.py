import logging
import re
import typing
from pathlib import Path
from typing import List, Optional

import rich.markup
import rich_click as click
from flytekit.configuration import AuthType, Config, PlatformConfig
from flytekit.remote import remote_fs
from rich.console import Console

from union import Artifact
from union._config import (
    AppClientCredentials,
    _encode_app_client_credentials,
    _get_endpoint_for_login,
    _get_user_handle,
    _is_serverless_endpoint,
    _write_config_to_path,
)
from union.cli._artifact_create_common import ArtifactCreateCommand
from union.cli._common import _get_organization, _validate_key_value_pairs
from union.cli._option import MutuallyExclusiveArgument, MutuallyExclusiveOption
from union.internal.identity.app_payload_pb2 import CreateAppRequest
from union.internal.identity.enums_pb2 import ConsentMethod, GrantTypes, ResponseTypes, TokenEndpointAuthMethod
from union.internal.secret.definition_pb2 import (
    SECRET_TYPE_GENERIC,
    SECRET_TYPE_IMAGE_PULL_SECRET,
    SecretIdentifier,
    SecretSpec,
    SecretType,
)
from union.internal.secret.payload_pb2 import CreateSecretRequest
from union.remote import UnionRemote
from union.ucimage._docker_credentials_helper import derive_docker_credentials
from union.workspace._config import _DEFAULT_CONFIG_YAML_FOR_BASE_IMAGE, _DEFAULT_CONFIG_YAML_FOR_IMAGE_SPEC
from union.workspace._vscode import WorkspaceConfig, build_workspace_image

logger = logging.getLogger("union.cli._create")

# Simplified --type option for users they don't have to fill entire enum string "SECRET_TYPE_IMAGE_PULL_SECRET"
_SIMPLE_IMAGEPULL_TYPE = (
    SecretType.Name(SECRET_TYPE_IMAGE_PULL_SECRET).replace("SECRET_TYPE_", "").replace("_", "-").lower()
)


@click.group()
def create():
    """Create a resource."""


@create.command()
@click.argument(
    "name",
    required=False,
    cls=MutuallyExclusiveArgument,
    mutually_exclusive=["name_option"],
    error_msg="Please pass --name once: `union create secret --name NAME`",
)
@click.option(
    "--name",
    "name_option",
    help="Secret name",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["name"],
    error_msg="Please pass --name once: `union create secret --name NAME`",
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
@click.option(
    "-t",
    "--type",
    type=click.Choice([_SIMPLE_IMAGEPULL_TYPE]),
    help=f"The type of secret. Currently only '{_SIMPLE_IMAGEPULL_TYPE}' is supported.",
)
def secret(
    name: Optional[str],
    name_option: Optional[str],
    value: str,
    value_file: str,
    project: Optional[str],
    domain: Optional[str],
    type: Optional[str],
):
    """Create a secret with NAME."""
    name = name or name_option

    if type == _SIMPLE_IMAGEPULL_TYPE:
        if not value_file:
            click.ClickException("The type of secret is only supported with a file")
        type = SECRET_TYPE_IMAGE_PULL_SECRET
    else:
        type = SECRET_TYPE_GENERIC

    if value_file:
        with open(value_file, "rb") as f:
            secret_spec = SecretSpec(
                binary_value=f.read(),
                type=type,
            )
    else:
        secret_spec = SecretSpec(string_value=value, type=type)

    remote = UnionRemote(default_domain=domain, default_project=project)
    stub = remote.secret_client

    request = CreateSecretRequest(
        id=SecretIdentifier(name=name, domain=domain, project=project),
        secret_spec=secret_spec,
    )
    try:
        stub.CreateSecret(request)
        click.echo(f"Created secret with name: {name}")
    except Exception as e:
        raise click.ClickException(f"Unable to create secret with name: {name}\n{e}") from e


@create.group("api-key")
def api_key():
    """Manage API keys."""


@api_key.command("admin")
@click.option("--name", type=str, help="Name for API key", required=True)
def admin(name: str):
    """Create an api key."""
    remote = UnionRemote()
    platform_obj = remote.config.platform

    normalized_client_name = re.sub("[^0-9a-zA-Z]+", "-", name.lower())
    if _is_serverless_endpoint(platform_obj.endpoint):
        userhandle = _get_user_handle(platform_obj, channel=remote.sync_channel)
        tenant = platform_obj.endpoint.split(".")[0]
        client_id = f"{tenant}-{userhandle}-{normalized_client_name}"
    else:
        client_id = normalized_client_name
    org = _get_organization(platform_obj, channel=remote.sync_channel)

    stub = remote.apps_service_client
    request = CreateAppRequest(
        organization=org,
        client_id=client_id,
        client_name=client_id,
        grant_types=[GrantTypes.CLIENT_CREDENTIALS, GrantTypes.AUTHORIZATION_CODE],
        redirect_uris=["http://localhost:8080/authorization-code/callback"],
        response_types=[ResponseTypes.CODE],
        token_endpoint_auth_method=TokenEndpointAuthMethod.CLIENT_SECRET_BASIC,
        consent_method=ConsentMethod.CONSENT_METHOD_REQUIRED,
    )

    try:
        response = stub.Create(request)
    except Exception as e:
        raise click.ClickException(f"Unable to create api-key with name: {name}\n{e}") from e

    click.echo(f"Client ID: {response.app.client_id}")
    click.echo("The following API key will only be shown once. Be sure to keep it safe!")
    click.echo("Configure your headless CLI by setting the following environment variable:")
    click.echo()

    union_api_key = _encode_app_client_credentials(
        AppClientCredentials(
            endpoint=platform_obj.endpoint,
            client_id=response.app.client_id,
            client_secret=response.app.client_secret,
            org=org,
        )
    )
    click.echo(f'export UNION_API_KEY="{union_api_key}"')


@create.command()
@click.option(
    "--auth",
    type=click.Choice(["device-flow", "pkce"]),
    default="pkce",
    help="Authorization method to ues",
)
@click.option(
    "--host", default=None, help="Host to connect to.", cls=MutuallyExclusiveOption, mutually_exclusive=["serverless"]
)
@click.option(
    "--serverless",
    default=False,
    is_flag=True,
    help="Connect to serverless.",
    cls=MutuallyExclusiveOption,
    mutually_exclusive=["host"],
)
def login(auth: str, host: Optional[str], serverless: bool):
    """Log into Union

    - On Union Serverless run: `union create login --serverless`

    - On Union BYOC run: `union create login --host UNION_TENANT`
    """
    endpoint = _get_endpoint_for_login(host=host, serverless=serverless)

    if auth == "pkce":
        auth_mode = AuthType.PKCE
    else:
        auth_mode = AuthType.DEVICEFLOW

    config = Config.auto().with_params(
        platform=PlatformConfig(
            endpoint=endpoint,
            insecure=False,
            auth_mode=auth_mode,
        )
    )

    console = Console()
    try:
        path = _write_config_to_path(endpoint, auth_mode.value)
        console.print(f"🔐 [yellow]Configuration saved to {path}[/yellow]")

        # Accessing the client will trigger authentication
        remote = UnionRemote(config=config)
        remote._user_info()
        ep = "serverless" if serverless else endpoint
        console.print(f"Login successful into [green][bold]{ep}[/bold][/green]")

    except Exception as e:
        raise click.ClickException(f"Unable to login.\n{e}") from e


@create.command()
@click.pass_context
@click.argument("config_file", type=click.Path(path_type=Path))
def workspace(ctx: click.Context, config_file: Path):
    """Create workspace."""
    config_content = config_file.read_text()
    workspace_config = WorkspaceConfig.from_yaml(config_content)

    remote = UnionRemote(default_domain=workspace_config.domain, default_project=workspace_config.project)
    logger.debug(f"Workspace config: {workspace_config}")
    logger.debug(f"Remote: {remote.__dict__}")
    if not isinstance(workspace_config.container_image, str):
        _image_build_task = build_workspace_image(remote, workspace_config)
        # override container image with the built image
        workspace_config.container_image = _image_build_task.template.container.image
    _create_workspace(remote, workspace_config)


@create.command("workspace-config")
@click.argument("config_file", type=click.Path(path_type=Path))
@click.option("--init", type=click.Choice(["base_image", "custom_image"]), required=True, default="base_image")
def workspace_config(config_file: Path, init: str):
    """Create workspace config at CONFIG_FILE."""
    from union._config import _is_serverless_endpoint

    if config_file.exists():
        raise click.ClickException(f"{config_file} already exists")

    remote = UnionRemote()
    if _is_serverless_endpoint(remote.config.platform.endpoint):
        default_project = "default"
    else:
        default_project = "flytesnacks"

    click.echo(f"Writing workspace configuration to {config_file}")
    if init == "base_image":
        config_file.write_text(_DEFAULT_CONFIG_YAML_FOR_BASE_IMAGE.format(default_project=default_project))
    else:
        config_file.write_text(_DEFAULT_CONFIG_YAML_FOR_IMAGE_SPEC.format(default_project=default_project))


def _create_workspace(remote: UnionRemote, ws_config: WorkspaceConfig):
    from union._async import run_sync
    from union.internal.workspace.workspace_definition_payload_pb2 import CreateWorkspaceDefinitionResponse
    from union.workspace._vscode_remote import WorkspaceRemote

    name = ws_config.name
    ws_remote = WorkspaceRemote(
        default_project=ws_config.project,
        default_domain=ws_config.domain,
        union_remote=remote,
    )

    console = Console()
    try:
        ws_def: CreateWorkspaceDefinitionResponse = run_sync(ws_remote.create_workspace_definition, ws_config)
    except Exception as e:
        raise click.ClickException(f"Error creating workspace definition: {rich.markup.escape(str(e))}") from e

    console.print(f"Created: {ws_def}")
    console.print(f"Starting workspace '{name}'")
    with console.status("Provisioning workspace", spinner="dots"):
        try:
            response = run_sync(ws_remote.start_workspace_instance, ws_def.workspace_definition.id.name)
        except Exception as e:
            raise click.ClickException(f"Error provisioning workspace: {rich.markup.escape(e.details())}") from e

    url = f"https://{remote.config.platform.endpoint}/{response.workspace_instance.spec.uri}"
    loading_url = f"https://{remote.config.platform.endpoint}/loading?type=workspace&url={url}"
    console.print(f"\n🚀 Workspace started: [link={loading_url}]Open VSCode in Browser[/link]")


@create.command("artifact", cls=ArtifactCreateCommand)
@click.argument("name")
@click.option("--version", type=str, required=True, help="Version of the artifact")
@click.option(
    "--partitions", "-p", callback=_validate_key_value_pairs, help="Partitions for the artifact", multiple=True
)
@click.option("--short-description", help="Short description of the artifact")
def artifact(
    name: str,
    project: str,
    domain: str,
    version: Optional[str],
    partitions: Optional[typing.List[str]],
    short_description: Optional[str],
    **kwargs,
):
    """Create an artifact with NAME."""
    remote = UnionRemote(
        default_domain=domain, default_project=project, data_upload_location=remote_fs.REMOTE_PLACEHOLDER
    )
    lit, lt = ArtifactCreateCommand.get_literal_from_args(remote.context, kwargs)
    a = Artifact(
        project=project,
        domain=domain,
        name=name,
        version=version,
        partitions=partitions,
        short_description=short_description,
        literal=lit,
        literal_type=lt,
    )
    remote.create_artifact(artifact=a)
    url = remote.generate_console_url(a)
    Console().print(f"[green]Created artifact with name: [bold][link={url}]{name}:{version}[/link][/bold][/green]")


@create.command("imagepullsecret")
@click.option(
    "-r",
    "--registries",
    help="Docker registries to create image pull secret for",
    multiple=True,
)
@click.option(
    "-i",
    "--input-file",
    type=click.Path(path_type=Path),
    help="Path to the input file, defaults to DOCKER_CONFIG and ~/.docker/config.json",
)
@click.option(
    "-o",
    "--output-file",
    type=click.Path(path_type=Path),
    help="Path to the output file, defaults to randome temporary file",
)
@click.option(
    "-q",
    "--quiet",
    is_flag=True,
    help="Only output the file path without any formatting",
)
def image_pull_secret(
    registries: Optional[List[str]], input_file: Optional[Path], output_file: Optional[Path], quiet: bool = False
):
    """Attempts to create dockerconfigjson by generating tokens that don't require credHelpers."""
    output_file_path = derive_docker_credentials(
        registries=registries,
        docker_config_path=input_file,
        output_path=output_file,
    )

    if quiet:
        print(output_file_path)
    else:
        console = Console()
        console.print(f"🔐 [yellow]Configuration saved to {output_file_path}[/yellow]")
