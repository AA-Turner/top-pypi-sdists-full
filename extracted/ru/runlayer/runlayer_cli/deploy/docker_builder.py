"""
Docker image building and pushing utilities.
"""

from pathlib import Path
from typing import Any, Optional

import docker
from docker.errors import BuildError, APIError, DockerException
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.console import Console

from rich.markup import escape

from runlayer_cli.api import ECRCredentials
from runlayer_cli.symbols import OK

console = Console()


class DockerBuildError(Exception):
    """Exception raised when Docker build fails."""

    pass


class DockerPushError(Exception):
    """Exception raised when Docker push fails."""

    pass


def check_docker_available() -> bool:
    """
    Check if Docker is available and running.

    Returns:
        True if Docker is available, False otherwise
    """
    try:
        client = docker.from_env()
        client.ping()
        return True
    except DockerException:
        return False


def get_registry_hostname(registry_url: str) -> str:
    """Normalize registry URLs to the hostname Docker expects."""
    return registry_url.replace("https://", "").replace("http://", "")


def get_registry_auth_config(credentials: ECRCredentials) -> dict[str, str]:
    """Build request-scoped registry auth for Docker SDK calls."""
    registry = get_registry_hostname(credentials.registry_url)
    return {
        "username": credentials.username,
        "password": credentials.password,
        "serveraddress": registry,
    }


def authenticate_ecr(credentials: ECRCredentials) -> dict[str, str]:
    """
    Authenticate Docker with ECR using provided credentials.

    Args:
        credentials: ECR credentials from backend

    Returns:
        Auth config that can be reused by later Docker SDK calls

    Raises:
        DockerException: If authentication fails
    """
    import datetime
    import subprocess

    try:
        now = datetime.datetime.now(datetime.timezone.utc)
        expires_at = credentials.expires_at

        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=datetime.timezone.utc)

        time_until_expiry = (expires_at - now).total_seconds()

        if time_until_expiry < 300:
            raise DockerException(
                f"ECR token expires in {int(time_until_expiry)} seconds. "
                "Please get fresh credentials and try again."
            )

        registry = get_registry_hostname(credentials.registry_url)
        auth_config = get_registry_auth_config(credentials)

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=True,
        ) as progress:
            task = progress.add_task(
                description="Authenticating with ECR...", total=None
            )

            try:
                login_cmd = [
                    "docker",
                    "login",
                    "--username",
                    credentials.username,
                    "--password-stdin",
                    registry,
                ]

                result = subprocess.run(
                    login_cmd,
                    input=credentials.password.encode(),
                    capture_output=True,
                    timeout=30,
                )

                if result.returncode == 0:
                    progress.update(
                        task, description=f"{escape(OK)} ECR authentication successful"
                    )
                else:
                    stderr_msg = result.stderr.decode(errors="replace").strip()
                    stdout_msg = result.stdout.decode(errors="replace").strip()
                    error_msg = stderr_msg or stdout_msg or "Unknown error"
                    raise DockerException(error_msg)

            except (subprocess.TimeoutExpired, FileNotFoundError, DockerException) as e:
                console.print(f"[red][bold]Docker CLI login failed:[/bold]\n{e}[/red]")
                console.print("[dim]Retrying with Docker SDK instead...[/dim]")

                try:
                    client = docker.from_env()
                    client.login(
                        username=credentials.username,
                        password=credentials.password,
                        registry=registry,
                        reauth=True,
                    )
                    progress.update(
                        task, description=f"{escape(OK)} ECR authentication successful"
                    )
                except Exception as sdk_error:
                    raise DockerException(f"Failed to authenticate: {sdk_error}")

        return auth_config

    except APIError as e:
        raise DockerException(f"Failed to authenticate with ECR: {e}")


def build_image(
    context: str,
    dockerfile: str,
    tag: str,
    build_args: Optional[dict[str, str]] = None,
    platform: Optional[str] = None,
    target: Optional[str] = None,
) -> str:
    """
    Build a Docker image.

    Args:
        context: Build context directory
        dockerfile: Path to Dockerfile (relative to context)
        tag: Image tag
        build_args: Build arguments
        platform: Platform to build for (e.g., "linux/amd64", "linux/arm64")
        target: Target build stage for multi-stage builds

    Returns:
        Image ID

    Raises:
        DockerBuildError: If build fails
    """
    try:
        context_path = Path(context).resolve()
        if not context_path.exists():
            raise DockerBuildError(f"Build context not found: {context}")

        dockerfile_path = context_path / dockerfile
        if not dockerfile_path.exists():
            raise DockerBuildError(f"Dockerfile not found: {dockerfile_path}")

        client = docker.from_env()

        build_kwargs: dict[str, Any] = {
            "path": str(context_path),
            "dockerfile": dockerfile,
            "tag": tag,
            "rm": True,
            "pull": True,
        }

        if build_args:
            build_kwargs["buildargs"] = build_args

        if platform:
            build_kwargs["platform"] = platform

        if target:
            build_kwargs["target"] = target

        console.print(f"\nBuilding Docker image: {tag}")

        response = client.api.build(**build_kwargs, decode=True)

        image_id = None
        current_step = ""

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=False,
        ) as progress:
            task = progress.add_task(description="Starting build...", total=None)

            for chunk in response:
                if "stream" in chunk:
                    stream_text = chunk["stream"].strip()
                    if stream_text:
                        if stream_text.startswith("Step"):
                            current_step = stream_text.split("\n")[0]
                            progress.update(task, description=current_step)
                        console.print(f"[dim]{stream_text}[/dim]")
                elif "status" in chunk:
                    status = chunk["status"]
                    if "id" in chunk:
                        progress.update(task, description=f"{chunk['id']}: {status}")
                    else:
                        progress.update(task, description=status)
                elif "error" in chunk:
                    error_msg = chunk["error"]
                    console.print(f"\n[red]ERROR: {error_msg}[/red]\n")
                    raise DockerBuildError(error_msg)
                elif "aux" in chunk:
                    if "ID" in chunk["aux"]:
                        image_id = chunk["aux"]["ID"]

        console.print(f"[bold green]\n{escape(OK)} Build completed\n[/bold green]")

        if not image_id:
            image = client.images.get(tag)
            image_id = image.id

        if not image_id:
            raise DockerBuildError("Failed to get image ID from build")

        return image_id

    except BuildError as e:
        raise DockerBuildError(f"Docker build failed: {e}")
    except APIError as e:
        raise DockerBuildError(f"Docker API error: {e}")
    except DockerBuildError:
        raise
    except Exception as e:
        raise DockerBuildError(f"Unexpected error during build: {e}")


def tag_image(image_id: str, repository: str, tag: str) -> str:
    """
    Tag a Docker image.

    Args:
        image_id: Image ID to tag
        repository: Repository URL (e.g., "123456789.dkr.ecr.us-east-1.amazonaws.com/my-app")
        tag: Tag name (e.g., "latest", "v1.0.0")

    Returns:
        Full image name with tag

    Raises:
        DockerException: If tagging fails
    """
    try:
        client = docker.from_env()
        image = client.images.get(image_id)

        full_tag = f"{repository}:{tag}"
        image.tag(repository, tag=tag)

        return full_tag

    except Exception as e:
        raise DockerException(f"Failed to tag image: {e}")


def push_image(image_tag: str, auth_config: Optional[dict[str, str]] = None) -> str:
    """
    Push a Docker image to a registry and return the digest the registry serves.

    The returned digest is resolved from the registry (not from the local push
    response), so it is always safe to pin for ECS. See
    ``_resolve_registry_digest`` for why the locally-reported digest can't be
    trusted.

    Args:
        image_tag: Full image tag (e.g., "registry/repo:tag")
        auth_config: Optional request-scoped auth for the registry

    Returns:
        Manifest digest (sha256:...) as served by the registry

    Raises:
        DockerPushError: If push fails
    """
    try:
        client = docker.from_env()

        console.print("\nPushing image to registry")

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console,
            transient=False,
        ) as progress:
            task = progress.add_task(description="Starting push...", total=None)

            push_kwargs: dict[str, Any] = {"stream": True, "decode": True}
            if auth_config:
                push_kwargs["auth_config"] = auth_config

            for line in client.images.push(image_tag, **push_kwargs):
                if "error" in line:
                    error_msg = line.get("error", "Unknown error")
                    console.print(f"\n[red]ERROR: {error_msg}[/red]\n")
                    raise DockerPushError(f"Push failed: {error_msg}")

                if "status" not in line:
                    continue

                status = line["status"]
                layer_id = line.get("id")
                progress_detail = line.get("progressDetail")

                if layer_id and progress_detail:
                    current = progress_detail.get("current")
                    total = progress_detail.get("total")
                    if current is not None and total is not None:
                        description = f"{layer_id}: {status} ({current}/{total})"
                    else:
                        description = f"{layer_id}: {status}"
                elif layer_id:
                    description = f"{layer_id}: {status}"
                else:
                    description = status

                progress.update(task, description=description)

        console.print(f"[bold green]\n{escape(OK)} Push completed\n[/bold green]")

        return _resolve_registry_digest(image_tag, auth_config=auth_config)

    except DockerPushError:
        raise
    except APIError as e:
        raise DockerPushError(f"Docker API error during push: {e}")
    except Exception as e:
        raise DockerPushError(f"Unexpected error during push: {e}")


def _resolve_registry_digest(
    image_tag: str, auth_config: Optional[dict[str, str]] = None
) -> str:
    """
    Resolve the authoritative manifest digest the registry serves for a tag.

    The digest reported locally after `docker push` (``aux.Digest`` / the image's
    ``RepoDigests``) can differ from the digest the registry actually stores and
    serves — e.g. with Docker's containerd image store, OCI/manifest-list shapes,
    or buildx attestation manifests. Pinning the local digest then makes ECS pull
    a digest ECR never had (CannotPullContainerError). Query the registry directly
    so we pin the digest ECS will actually be able to pull.

    Args:
        image_tag: Full image tag pushed to the registry (e.g. "repo:tag")
        auth_config: Optional request-scoped auth for the registry

    Returns:
        Manifest digest (sha256:...) as served by the registry

    Raises:
        DockerPushError: If the digest cannot be resolved from the registry
    """
    try:
        client = docker.from_env()
        registry_data = client.images.get_registry_data(
            image_tag, auth_config=auth_config
        )
        digest = registry_data.id
    except APIError as e:
        raise DockerPushError(f"Failed to resolve registry digest for {image_tag}: {e}")
    except Exception as e:
        raise DockerPushError(
            f"Unexpected error resolving registry digest for {image_tag}: {e}"
        )

    if not digest:
        raise DockerPushError(f"Registry returned no digest for {image_tag}")

    return digest


def build_and_push(
    context: str,
    dockerfile: str,
    repository: str,
    tag: str,
    credentials: ECRCredentials,
    build_args: Optional[dict[str, str]] = None,
    platform: Optional[str] = None,
    target: Optional[str] = None,
) -> tuple[str, str]:
    """
    Build, tag, and push a Docker image in one operation.

    Args:
        context: Build context directory
        dockerfile: Path to Dockerfile
        repository: ECR repository URL
        tag: Image tag
        credentials: ECR credentials
        build_args: Optional build arguments
        platform: Optional platform specification
        target: Optional target build stage for multi-stage builds

    Returns:
        Tuple of (full_image_uri_with_tag, image_digest)

    Raises:
        DockerBuildError: If build fails
        DockerPushError: If push fails
    """
    # Authenticate with ECR
    auth_config = authenticate_ecr(credentials)

    # Build the image with a local tag first
    local_tag = f"runlayer-build:{tag}"
    image_id = build_image(
        context=context,
        dockerfile=dockerfile,
        tag=local_tag,
        build_args=build_args,
        platform=platform,
        target=target,
    )

    # Tag with ECR repository
    full_image_uri = tag_image(image_id, repository, tag)

    # Push to ECR and get digest
    image_digest = push_image(full_image_uri, auth_config=auth_config)

    return full_image_uri, image_digest
