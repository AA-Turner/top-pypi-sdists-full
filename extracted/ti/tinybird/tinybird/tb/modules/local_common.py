import hashlib
import json
import logging
import os
import re
import subprocess
import time
from typing import Any, Dict, Optional

import boto3
import click
import requests

import docker
from docker.client import DockerClient
from docker.models.containers import Container
from tinybird.tb.client import AuthNoTokenException, TinyB
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.exceptions import CLILocalException
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.secret_common import load_secrets
from tinybird.tb.modules.telemetry import add_telemetry_event

TB_IMAGE_NAME = "tinybirdco/tinybird-local:latest"
TB_CONTAINER_NAME = "tinybird-local"
TB_LOCAL_PORT = int(os.getenv("TB_LOCAL_PORT", 7181))
TB_LOCAL_HOST = re.sub(r"^https?://", "", os.getenv("TB_LOCAL_HOST", "localhost"))
TB_LOCAL_ADDRESS = f"http://{TB_LOCAL_HOST}:{TB_LOCAL_PORT}"
TB_LOCAL_DEFAULT_WORKSPACE_NAME = "Tinybird_Local_Testing"


def get_tinybird_local_client(
    config_obj: Dict[str, Any], test: bool = False, staging: bool = False, silent: bool = False
) -> TinyB:
    """Get a Tinybird client connected to the local environment."""

    config = get_tinybird_local_config(config_obj, test=test, silent=silent)
    client = config.get_client(host=TB_LOCAL_ADDRESS, staging=staging)
    load_secrets(config_obj.get("path", ""), client)
    return client


def get_tinybird_local_config(config_obj: Dict[str, Any], test: bool = False, silent: bool = False) -> CLIConfig:
    """Craft a client config with a workspace name based on the path of the project files

    It uses the tokens from tinybird local
    """
    path = config_obj.get("path")
    config = CLIConfig.get_project_config()
    tokens = get_local_tokens()
    user_token = tokens["user_token"]
    admin_token = tokens["admin_token"]
    default_token = tokens["workspace_admin_token"]
    # Create a new workspace if path is provided. This is used to isolate the build in a different workspace.
    if path:
        user_client = config.get_client(host=TB_LOCAL_ADDRESS, token=user_token)
        if test:
            ws_name = get_test_workspace_name(path)
        else:
            ws_name = config.get("name") or config_obj.get("name") or get_build_workspace_name(path)
        if not ws_name:
            raise AuthNoTokenException()

        logging.debug(f"Workspace used for build: {ws_name}")

        user_workspaces = requests.get(
            f"{TB_LOCAL_ADDRESS}/v1/user/workspaces?with_organization=true&token={admin_token}"
        ).json()
        user_org_id = user_workspaces.get("organization_id", {})
        local_workspaces = user_workspaces.get("workspaces", [])

        ws = next((ws for ws in local_workspaces if ws["name"] == ws_name), None)

        # If we are running a test, we need to delete the workspace if it already exists
        if test and ws:
            requests.delete(
                f"{TB_LOCAL_ADDRESS}/v1/workspaces/{ws['id']}?token={user_token}&hard_delete_confirmation=yes"
            )
            ws = None

        if not ws:
            user_client.create_workspace(ws_name, assign_to_organization_id=user_org_id, version="v1")
            user_workspaces = requests.get(f"{TB_LOCAL_ADDRESS}/v1/user/workspaces?token={admin_token}").json()
            ws = next((ws for ws in user_workspaces["workspaces"] if ws["name"] == ws_name), None)
            if not ws:
                raise AuthNoTokenException()

        ws_token = ws["token"]
        config.set_token(ws_token)
        config.set_token_for_host(TB_LOCAL_ADDRESS, ws_token)
        config.set_host(TB_LOCAL_ADDRESS)
    else:
        config.set_token(default_token)
        config.set_token_for_host(TB_LOCAL_ADDRESS, default_token)

    config.set_user_token(user_token)
    return config


def get_build_workspace_name(path: str) -> str:
    folder_hash = hashlib.sha256(path.encode()).hexdigest()
    return f"Tinybird_Local_Build_{folder_hash}"


def get_test_workspace_name(path: str) -> str:
    folder_hash = hashlib.sha256(path.encode()).hexdigest()
    return f"Tinybird_Local_Test_{folder_hash}"


def get_local_tokens() -> Dict[str, str]:
    try:
        return requests.get(f"{TB_LOCAL_ADDRESS}/tokens").json()
    except Exception:
        # Check if tinybird-local is running using docker client (some clients use podman and won't have docker cmd)
        try:
            docker_client = get_docker_client()
            container = get_existing_container_with_matching_env(docker_client, TB_CONTAINER_NAME, {})

            output = {}
            if container:
                output = container.attrs
            add_telemetry_event(
                "docker_debug",
                data={
                    "container_attrs": output,
                },
            )

            if container and container.status == "running":
                if container.health == "healthy":
                    raise CLILocalException(
                        FeedbackManager.error(
                            message=(
                                "Looks like Tinybird Local is running but we are not able to connect to it.\n\n"
                                "If you've run it manually using different host or port, please set the environment variables "
                                "TB_LOCAL_HOST and TB_LOCAL_PORT to match the ones you're using.\n"
                                "If you're not sure about this, please run `tb local restart` and try again."
                            )
                        )
                    )
                raise CLILocalException(
                    FeedbackManager.error(
                        message=(
                            "Tinybird Local is running but it's unhealthy. Please check if it's running and try again.\n"
                            "If the problem persists, please run `tb local restart` and try again."
                        )
                    )
                )
        except CLILocalException as e:
            raise e
        except Exception:
            pass

        # Check if tinybird-local is running with docker
        try:
            output_str = subprocess.check_output(
                ["docker", "ps", "--filter", f"name={TB_CONTAINER_NAME}", "--format", "json"], text=True
            )
            output = {}
            if output_str:
                output = json.loads(output_str)
            add_telemetry_event(
                "docker_debug",
                data={
                    "docker_ps_output": output,
                },
            )

            if output.get("State", "") == "running":
                if "(healthy)" in output.get("Status", ""):
                    raise CLILocalException(
                        FeedbackManager.error(
                            message=(
                                "Looks like Tinybird Local is running but we are not able to connect to it.\n\n"
                                "If you've run it manually using different host or port, please set the environment variables "
                                "TB_LOCAL_HOST and TB_LOCAL_PORT to match the ones you're using.\n"
                                "If you're not sure about this, please run `tb local restart` and try again."
                            )
                        )
                    )
                raise CLILocalException(
                    FeedbackManager.error(
                        message="Tinybird Local is running but it's unhealthy. Please check if it's running and try again.\n"
                        "If the problem persists, please run `tb local restart` and try again."
                    )
                )
        except CLILocalException as e:
            raise e
        except Exception:
            pass

        is_ci = (
            os.getenv("GITHUB_ACTIONS")
            or os.getenv("TRAVIS")
            or os.getenv("CIRCLECI")
            or os.getenv("GITLAB_CI")
            or os.getenv("CI")
            or os.getenv("TB_CI")
        )
        if not is_ci:
            yes = click.confirm(
                FeedbackManager.warning(message="Tinybird local is not running. Do you want to start it? [Y/n]"),
                prompt_suffix="",
                show_default=False,
                default=True,
            )
            if yes:
                click.echo(FeedbackManager.highlight(message="» Starting Tinybird Local..."))
                docker_client = get_docker_client()
                start_tinybird_local(docker_client, False)
                click.echo(FeedbackManager.success(message="✓ Tinybird Local is ready!"))
                return get_local_tokens()

        raise CLILocalException(
            FeedbackManager.error(message="Tinybird local is not running. Please run `tb local start` first.")
        )


def start_tinybird_local(
    docker_client: DockerClient,
    use_aws_creds: bool,
    volumes_path: Optional[str] = None,
    skip_new_version: bool = False,
) -> None:
    """Start the Tinybird container."""
    pull_show_prompt = False
    pull_required = False

    if not skip_new_version:
        try:
            local_image = docker_client.images.get(TB_IMAGE_NAME)
            local_image_id = local_image.attrs["RepoDigests"][0].split("@")[1]
            remote_image = docker_client.images.get_registry_data(TB_IMAGE_NAME)
            pull_show_prompt = local_image_id != remote_image.id
        except Exception:
            pull_show_prompt = False
            pull_required = True

        if pull_show_prompt and click.confirm(
            FeedbackManager.warning(message="△ New version detected, download? [y/N]:"),
            show_default=False,
            prompt_suffix="",
        ):
            click.echo(FeedbackManager.info(message="* Downloading latest version of Tinybird Local..."))
            pull_required = True

        if pull_required:
            docker_client.images.pull(TB_IMAGE_NAME, platform="linux/amd64")

    environment = get_use_aws_creds() if use_aws_creds else {}

    container = get_existing_container_with_matching_env(docker_client, TB_CONTAINER_NAME, environment)

    if container and not pull_required:
        # Container `start` is idempotent. It's safe to call it even if the container is already running.
        container.start()
    else:
        if container:
            container.remove(force=True)

        volumes = {}
        if volumes_path:
            volumes = {
                f"{volumes_path}/data": {"bind": "/var/lib/clickhouse", "mode": "rw"},
                f"{volumes_path}/metadata": {"bind": "/redis-data", "mode": "rw"},
            }

        container = docker_client.containers.run(
            TB_IMAGE_NAME,
            name=TB_CONTAINER_NAME,
            detach=True,
            ports={"7181/tcp": TB_LOCAL_PORT},
            remove=False,
            platform="linux/amd64",
            environment=environment,
            volumes=volumes,
        )

    click.echo(FeedbackManager.info(message="* Waiting for Tinybird Local to be ready..."))
    while True:
        container.reload()  # Refresh container attributes
        health = container.attrs.get("State", {}).get("Health", {}).get("Status")
        if health == "healthy":
            break
        if health == "unhealthy":
            raise CLILocalException(
                FeedbackManager.error(
                    message="Tinybird Local is unhealthy. Try running `tb local restart` in a few seconds."
                )
            )

        time.sleep(5)

    # Remove tinybird-local dangling images to avoid running out of disk space
    images = docker_client.images.list(name=re.sub(r":.*$", "", TB_IMAGE_NAME), all=True, filters={"dangling": True})
    for image in images:
        image.remove(force=True)


def get_existing_container_with_matching_env(
    docker_client: DockerClient, container_name: str, required_env: dict[str, str]
) -> Optional[Container]:
    """
    Checks if a container with the given name exists and has matching environment variables.
    If it exists but environment doesn't match, it returns None.

    Args:
        docker_client: The Docker client instance
        container_name: The name of the container to check
        required_env: Dictionary of environment variables that must be present

    Returns:
        The container if it exists with matching environment, None otherwise
    """
    container = None
    containers = docker_client.containers.list(all=True, filters={"name": container_name})
    if containers:
        container = containers[0]

    if container and required_env:
        container_info = container.attrs
        container_env = container_info.get("Config", {}).get("Env", [])
        env_missing = False
        for key, value in required_env.items():
            env_var = f"{key}={value}"
            if env_var not in container_env:
                env_missing = True
                break

        if env_missing:
            container.remove(force=True)
            container = None

    return container


def get_docker_client() -> DockerClient:
    """Check if Docker is installed and running."""
    try:
        docker_host = os.getenv("DOCKER_HOST")
        if not docker_host:
            # Try to get docker host from docker context
            try:
                try:
                    output = subprocess.check_output(["docker", "context", "inspect"], text=True)
                except Exception as e:
                    add_telemetry_event(
                        "docker_error",
                        error=f"docker_context_inspect_error: {str(e)}",
                    )
                    raise e
                try:
                    context = json.loads(output)
                except Exception as e:
                    add_telemetry_event(
                        "docker_error",
                        error=f"docker_context_inspect_parse_output_error: {str(e)}",
                        data={
                            "docker_context_inspect_output": output,
                        },
                    )
                    raise e
                if context and len(context) > 0:
                    try:
                        docker_host = context[0].get("Endpoints", {}).get("docker", {}).get("Host")
                        if docker_host:
                            os.environ["DOCKER_HOST"] = docker_host
                    except Exception as e:
                        add_telemetry_event(
                            "docker_error",
                            error=f"docker_context_parse_host_error: {str(e)}",
                            data={
                                "context": json.dumps(context),
                            },
                        )
                        raise e
            except Exception:
                pass
        try:
            client = docker.from_env()  # type: ignore
        except Exception as e:
            add_telemetry_event(
                "docker_error",
                error=f"docker_get_client_from_env_error: {str(e)}",
            )
            raise e
        try:
            client.ping()
        except Exception as e:
            client_dict_non_sensitive = {k: v for k, v in client.api.__dict__.items() if "auth" not in k}
            add_telemetry_event(
                "docker_error",
                error=f"docker_ping_error: {str(e)}",
                data={
                    "client": repr(client_dict_non_sensitive),
                },
            )
            raise e
        return client
    except Exception:
        docker_location_message = ""
        if docker_host:
            docker_location_message = f"Trying to connect to Docker-compatible runtime at {docker_host}"

        raise CLILocalException(
            FeedbackManager.error(
                message=(
                    f"No container runtime is running. Make sure a Docker-compatible runtime is installed and running. "
                    f"{docker_location_message}\n\n"
                    "If you're using a custom location, please provide it using the DOCKER_HOST environment variable."
                )
            )
        )


def get_use_aws_creds() -> dict[str, str]:
    credentials: dict[str, str] = {}
    try:
        # Get the boto3 session and credentials
        session = boto3.Session()
        creds = session.get_credentials()

        if creds:
            # Create environment variables for the container based on boto credentials
            credentials["AWS_ACCESS_KEY_ID"] = creds.access_key
            credentials["AWS_SECRET_ACCESS_KEY"] = creds.secret_key

            # Add session token if it exists (for temporary credentials)
            if creds.token:
                credentials["AWS_SESSION_TOKEN"] = creds.token

            # Add region if available
            if session.region_name:
                credentials["AWS_DEFAULT_REGION"] = session.region_name

            click.echo(
                FeedbackManager.success(
                    message=f"✓ AWS credentials found and will be passed to Tinybird Local (region: {session.region_name or 'not set'})"
                )
            )
        else:
            click.echo(
                FeedbackManager.warning(
                    message="△ No AWS credentials found. S3 operations will not work in Tinybird Local."
                )
            )
    except Exception as e:
        click.echo(
            FeedbackManager.warning(
                message=f"△ Error retrieving AWS credentials: {str(e)}. S3 operations will not work in Tinybird Local."
            )
        )

    return credentials
