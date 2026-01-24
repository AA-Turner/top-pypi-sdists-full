import hashlib
import json
import logging
import os
import re
import subprocess
import threading
import time
import uuid
from typing import Any, Dict, Optional

import boto3
import click
import requests
from docker.client import DockerClient
from docker.models.containers import Container

import docker
from tinybird.tb.client import AuthNoTokenException, TinyB
from tinybird.tb.modules.config import CLIConfig
from tinybird.tb.modules.exceptions import CLILocalException
from tinybird.tb.modules.feedback_manager import FeedbackManager
from tinybird.tb.modules.local_logs import (
    check_memory_sufficient,
    clickhouse_is_ready,
    container_stats,
    events_is_ready,
    local_authentication_is_ready,
    redis_is_ready,
    server_is_ready,
)
from tinybird.tb.modules.secret_common import load_secrets
from tinybird.tb.modules.telemetry import add_telemetry_event

TB_IMAGE_NAME = "tinybirdco/tinybird-local:latest"
TB_CONTAINER_NAME = "tinybird-local"
TB_LOCAL_PORT = int(os.getenv("TB_LOCAL_PORT", 7181))
TB_LOCAL_CLICKHOUSE_INTERFACE_PORT = int(os.getenv("TB_LOCAL_CLICKHOUSE_INTERFACE_PORT", 7182))
TB_LOCAL_HOST = re.sub(r"^https?://", "", os.getenv("TB_LOCAL_HOST", "localhost"))
TB_LOCAL_ADDRESS = f"http://{TB_LOCAL_HOST}:{TB_LOCAL_PORT}"
TB_LOCAL_DEFAULT_WORKSPACE_NAME = "Tinybird_Local_Testing"


def get_tinybird_local_client(
    config_obj: Dict[str, Any], test: bool = False, staging: bool = False, silent: bool = False
) -> TinyB:
    """Get a Tinybird client connected to the local environment."""
    try:
        config = get_tinybird_local_config(config_obj, test=test, silent=silent)
        client = config.get_client(host=TB_LOCAL_ADDRESS, staging=staging)
        load_secrets(config_obj.get("path", ""), client)
        return client
    # if some of the API calls to tinybird local fail due to a JSONDecodeError, it means that container is running but it's unhealthy
    except json.JSONDecodeError:
        raise CLILocalException(
            message=FeedbackManager.error(
                message="Tinybird Local is running but it's unhealthy. Please check if it's running and try again. If the problem persists, please run `tb local restart` and try again."
            )
        )


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
            # delete any Tinybird_Local_Test_* workspace
            user_workspaces = requests.get(
                f"{TB_LOCAL_ADDRESS}/v1/user/workspaces?with_organization=true&token={admin_token}"
            ).json()
            local_workspaces = user_workspaces.get("workspaces", [])
            for ws in local_workspaces:
                is_test_workspace = ws["name"].startswith("Tinybird_Local_Test_")
                if is_test_workspace:
                    requests.delete(
                        f"{TB_LOCAL_ADDRESS}/v1/workspaces/{ws['id']}?token={user_token}&hard_delete_confirmation=yes"
                    )

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
    random_folder_suffix = str(uuid.uuid4()).replace("-", "_")
    return f"Tinybird_Local_Test_{random_folder_suffix}"


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

            # TODO: If docker errors persist, explain that you can use custom environments too once they are open for everyone
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
                click.echo(FeedbackManager.highlight(message="» Watching Tinybird Local... (Press Ctrl+C to stop)"))
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
    skip_new_version: bool = True,
    user_token: Optional[str] = None,
    workspace_token: Optional[str] = None,
    watch: bool = False,
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

    environment = {}
    if use_aws_creds:
        environment.update(get_use_aws_creds())
    if user_token:
        environment["TB_LOCAL_USER_TOKEN"] = user_token
    if workspace_token:
        environment["TB_LOCAL_WORKSPACE_TOKEN"] = workspace_token

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
            ports={"7181/tcp": TB_LOCAL_PORT, "7182/tcp": TB_LOCAL_CLICKHOUSE_INTERFACE_PORT},
            remove=False,
            platform="linux/amd64",
            environment=environment,
            volumes=volumes,
        )

    click.echo(FeedbackManager.info(message="* Waiting for Tinybird Local to be ready..."))

    if watch:
        # Stream logs in a separate thread while monitoring container health
        container_ready = threading.Event()
        stop_requested = threading.Event()
        health_check: dict[str, str] = {}

        log_thread = threading.Thread(
            target=stream_logs_with_health_check,
            args=(container, container_ready, stop_requested),
            daemon=True,
        )
        log_thread.start()

        health_check_thread = threading.Thread(
            target=check_endpoints_health,
            args=(container, docker_client, container_ready, stop_requested, health_check),
            daemon=True,
        )
        health_check_thread.start()

        # Monitor container health in main thread
        memory_warning_shown = False
        try:
            while True:
                container.reload()  # Refresh container attributes
                health = container.attrs.get("State", {}).get("Health", {}).get("Status")
                if not container_ready.is_set():
                    click.echo(FeedbackManager.info(message=f"* Tinybird Local container status: {health}"))
                    stats = container_stats(container, docker_client)
                    click.echo(f"* {stats}")

                    # Check memory sufficiency
                    if not memory_warning_shown:
                        is_sufficient, warning_msg = check_memory_sufficient(container, docker_client)
                        if not is_sufficient and warning_msg:
                            click.echo(FeedbackManager.warning(message=f"△ {warning_msg}"))
                            memory_warning_shown = True

                if health == "healthy":
                    click.echo(FeedbackManager.highlight(message="» Checking services..."))
                    stats = container_stats(container, docker_client)
                    click.echo(FeedbackManager.info(message=f"✓ Tinybird Local container ({stats})"))

                    # Check memory sufficiency before checking services
                    if not memory_warning_shown:
                        is_sufficient, warning_msg = check_memory_sufficient(container, docker_client)
                        if not is_sufficient and warning_msg:
                            click.echo(FeedbackManager.warning(message=f"△ {warning_msg}"))
                            memory_warning_shown = True

                    if not clickhouse_is_ready(container):
                        raise Exception("Clickhouse is not ready.")
                    click.echo(FeedbackManager.info(message="✓ Clickhouse"))

                    if not redis_is_ready(container):
                        raise Exception("Redis is not ready.")
                    click.echo(FeedbackManager.info(message="✓ Redis"))

                    if not server_is_ready(container):
                        raise Exception("Server is not ready.")
                    click.echo(FeedbackManager.info(message="✓ Server"))

                    if not events_is_ready(container):
                        raise Exception("Events is not ready.")
                    click.echo(FeedbackManager.info(message="✓ Events"))

                    if not local_authentication_is_ready(container):
                        raise Exception("Tinybird Local authentication is not ready.")
                    click.echo(FeedbackManager.info(message="✓ Tinybird Local authentication"))
                    container_ready.set()
                    # Keep monitoring and streaming logs until Ctrl+C or health check failure
                    while True:
                        # Check if health check detected an error
                        if stop_requested.is_set() and health_check.get("error"):
                            time.sleep(0.5)  # Give log thread time to finish printing
                            raise CLILocalException(
                                FeedbackManager.error(
                                    message=f"{health_check.get('error')}\n"
                                    "Please run `tb local restart` to restart the container."
                                )
                            )
                            return
                        time.sleep(1)
                if health == "unhealthy":
                    stop_requested.set()
                    # Check if memory might be the cause of unhealthy status
                    is_sufficient, warning_msg = check_memory_sufficient(container, docker_client)
                    error_msg = "Tinybird Local is unhealthy. Try running `tb local restart` in a few seconds."
                    if not is_sufficient and warning_msg:
                        error_msg = (
                            "Tinybird Local is unhealthy.\nnAfter adjusting memory, try running `tb local restart`."
                        )
                    raise CLILocalException(FeedbackManager.error(message=error_msg))
                time.sleep(5)
        except KeyboardInterrupt:
            stop_requested.set()
            click.echo(FeedbackManager.highlight(message="» Stopping Tinybird Local..."))
            try:
                container.stop()
                click.echo(FeedbackManager.success(message="✓ Tinybird Local stopped."))
            except KeyboardInterrupt:
                click.echo(FeedbackManager.warning(message="⚠ Forced exit. Container may still be running."))
                click.echo(FeedbackManager.info(message="  Run `tb local stop` to stop the container manually."))
            return

    # Non-watch mode: just wait for container to be healthy
    memory_warning_shown = False
    while True:
        container.reload()  # Refresh container attributes
        health = container.attrs.get("State", {}).get("Health", {}).get("Status")
        click.echo(FeedbackManager.info(message=f"* Tinybird Local container status: {health}"))
        stats = container_stats(container, docker_client)
        click.echo(f"* {stats}")

        # Check memory sufficiency
        if not memory_warning_shown:
            is_sufficient, warning_msg = check_memory_sufficient(container, docker_client)
            if not is_sufficient and warning_msg:
                click.echo(FeedbackManager.warning(message=f"△ {warning_msg}"))
                memory_warning_shown = True

        if health == "healthy":
            click.echo(FeedbackManager.highlight(message="» Checking services..."))
            stats = container_stats(container, docker_client)
            click.echo(FeedbackManager.info(message=f"✓ Tinybird Local container ({stats})"))
            if not clickhouse_is_ready(container):
                raise Exception("Clickhouse is not ready.")
            click.echo(FeedbackManager.info(message="✓ Clickhouse"))
            if not redis_is_ready(container):
                raise Exception("Redis is not ready.")
            click.echo(FeedbackManager.info(message="✓ Redis"))
            if not server_is_ready(container):
                raise Exception("Server is not ready.")
            click.echo(FeedbackManager.info(message="✓ Server"))
            if not events_is_ready(container):
                raise Exception("Events is not ready.")
            click.echo(FeedbackManager.info(message="✓ Events"))
            if not local_authentication_is_ready(container):
                raise Exception("Tinybird Local authentication is not ready.")
            click.echo(FeedbackManager.info(message="✓ Tinybird Local authentication"))
            break
        if health == "unhealthy":
            error_msg = "Tinybird Local is unhealthy. Try running `tb local restart` in a few seconds."
            raise CLILocalException(FeedbackManager.error(message=error_msg))
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
                    "If you're using a custom location, please provide it using the DOCKER_HOST environment variable.\n\n"
                    "Alternatively, you can use Tinybird branches to develop your project without Docker. Run `tb branch create my_feature_branch` to create one. Learn more at: https://www.tinybird.co/docs/forward/test-and-deploy/branches"
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


SERVICE_COLORS = {
    "[EVENTS]": "\033[95m",  # Magenta
    "[SERVER]": "\033[94m",  # Blue
    "[HEALTH]": "\033[96m",  # Cyan
    "[KAFKA]": "\033[93m",  # Yellow
    "[AUTH]": "\033[90m",  # Gray
}

RESET = "\033[0m"


def check_endpoints_health(
    container: Container,
    docker_client: DockerClient,
    container_ready: threading.Event,
    stop_requested: threading.Event,
    health_check: dict[str, str],
) -> None:
    """Continuously check /tokens and /v0/health endpoints"""
    # Wait for container to be ready before starting health checks
    container_ready.wait()

    # Give container a moment to fully start up
    time.sleep(2)

    check_interval = 10  # Check every 10 seconds

    while not stop_requested.is_set():
        try:
            # Check /tokens endpoint
            tokens_response = requests.get(f"{TB_LOCAL_ADDRESS}/tokens", timeout=5)
            if tokens_response.status_code != 200:
                health_check["error"] = (
                    f"/tokens endpoint returned status {tokens_response.status_code}. Tinybird Local may be unhealthy."
                )
                stop_requested.set()
                break

            # Check /v0/health endpoint
            health_response = requests.get(f"{TB_LOCAL_ADDRESS}/v0/health", timeout=5)
            if health_response.status_code != 200:
                health_check["error"] = (
                    f"/v0/health endpoint returned status {health_response.status_code}. "
                    "Tinybird Local may be unhealthy."
                )
                stop_requested.set()
                break

            # Verify tokens response has expected structure
            try:
                tokens_data = tokens_response.json()
                if not all(key in tokens_data for key in ["user_token", "admin_token", "workspace_admin_token"]):
                    health_check["error"] = (
                        "/tokens endpoint returned unexpected data. Tinybird Local may be unhealthy."
                    )
                    stop_requested.set()
                    break
            except json.JSONDecodeError:
                health_check["error"] = "/tokens endpoint returned invalid JSON. Tinybird Local may be unhealthy."
                stop_requested.set()
                break

        except Exception as e:
            # Check if it's a connection error
            error_str = str(e)
            if "connect" in error_str.lower() or "timeout" in error_str.lower():
                health_check["error"] = f"Failed to connect to Tinybird Local: {error_str}"
            else:
                health_check["error"] = f"Health check failed: {error_str}"
            stop_requested.set()
            break

        if container_ready.is_set():
            stats = container_stats(container, docker_client)
            click.echo(f"{SERVICE_COLORS['[HEALTH]']}[HEALTH]{RESET} {stats}")

        # Wait before next check
        for _ in range(check_interval):
            if stop_requested.is_set():
                break
            time.sleep(1)


def stream_logs_with_health_check(
    container: Container, container_ready: threading.Event, stop_requested: threading.Event
) -> None:
    """Stream logs and monitor container health in parallel"""
    # Wait for container to be ready before starting health checks
    container_ready.wait()

    # Give container a moment to fully start up
    time.sleep(2)

    retry_count = 0
    max_retries = 10
    exec_result = None

    while retry_count < max_retries and not stop_requested.is_set():
        try:
            # Try to tail the log files (only new logs, not historical)
            # Use -F to follow by name and retry if files don't exist yet
            log_files = {
                "/var/log/tinybird-local-server.log": "SERVER",
                "/var/log/tinybird-local-hfi.log": "EVENTS",
                "/var/log/tinybird-local-setup.log": "AUTH",
                "/var/log/tinybird-local-kafka.log": "KAFKA",
            }
            # Build commands to tail each file and prefix with its label (using stdbuf for unbuffered output)
            tail_commands = [
                f'tail -n 0 -f {path} | stdbuf -oL sed "s/^/[{source}] /"' for path, source in log_files.items()
            ]
            # Join with & to run in parallel, then wait for all
            cmd = f"sh -c '({' & '.join(tail_commands)}) & wait'"
            exec_result = container.exec_run(cmd, stream=True, tty=False, stdout=True, stderr=True)
            break  # Success, exit retry loop
        except Exception:
            # Log file might not exist yet, wait and retry
            retry_count += 1
            if retry_count < max_retries:
                time.sleep(2)

    # Stream logs continuously
    if exec_result:
        try:
            for line in exec_result.output:
                if stop_requested.is_set():
                    break

                raw_line = line.decode("utf-8").rstrip()
                lines = raw_line.split("\n")

                # Print "ready" message when container becomes healthy
                if container_ready.is_set() and not hasattr(stream_logs_with_health_check, "ready_printed"):
                    click.echo(FeedbackManager.success(message="✓ Tinybird Local is ready!"))
                    stream_logs_with_health_check.ready_printed = True  # type: ignore

                for line in lines:
                    # Apply color to service label
                    for service, color in SERVICE_COLORS.items():
                        if line.startswith(service):
                            message = line[len(service) :]
                            # extract content of message="...""
                            match = re.search(r'message="([^"]*)"', message)
                            if match:
                                message = match.group(1)
                            line = f"{color}{service}{RESET} {message}"
                            break

                    click.echo(line)

        except Exception:
            pass  # Silently ignore errors when stream is interrupted
