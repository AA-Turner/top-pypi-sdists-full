"""Plato Chronos CLI - Launch and manage Chronos jobs."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Annotated

import typer

from plato.v1.cli.utils import console

chronos_app = typer.Typer(help="Chronos job management commands.")
logger = logging.getLogger(__name__)


@chronos_app.command()
def launch(
    config: Path = typer.Argument(
        ...,
        help="Path to job config JSON file",
        exists=True,
        readable=True,
    ),
    chronos_url: str = typer.Option(
        None,
        "--url",
        "-u",
        envvar="CHRONOS_URL",
        help="Chronos API URL (default: https://chronos.plato.so)",
    ),
    api_key: str = typer.Option(
        None,
        "--api-key",
        "-k",
        envvar="PLATO_API_KEY",
        help="Plato API key for authentication",
    ),
    wait: bool = typer.Option(
        False,
        "--wait",
        "-w",
        help="Wait for job completion and stream logs",
    ),
):
    """Launch a Chronos job from a config file.

    Submits a job configuration to the Chronos service to run a world with its
    configured agents and secrets.

    Arguments:
        config: Path to the job configuration JSON file

    Options:
        -u, --url: Chronos API URL (default: https://chronos.plato.so, or CHRONOS_URL env var)
        -k, --api-key: Plato API key for authentication (or PLATO_API_KEY env var)
        -w, --wait: Wait for job completion and stream logs (not yet implemented)

    The config file should contain world.package (required) and optionally world.config,
    runtime.artifact_id, and tags.
    """
    from plato.chronos.sdk import Chronos

    # Set defaults
    if not chronos_url:
        chronos_url = "https://chronos.plato.so"

    if not api_key:
        console.print("[red]❌ No API key provided[/red]")
        console.print("Set PLATO_API_KEY environment variable or use --api-key")
        raise typer.Exit(1)

    # Load config
    try:
        with open(config) as f:
            job_config = json.load(f)
    except json.JSONDecodeError as e:
        console.print(f"[red]❌ Invalid JSON in config file: {e}[/red]")
        raise typer.Exit(1)

    # Validate required fields
    if "world" not in job_config or "package" not in job_config.get("world", {}):
        console.print("[red]❌ Missing required field: world.package[/red]")
        raise typer.Exit(1)

    # Normalize tags for ltree: replace '-' with '_', ':' with '.'
    raw_tags = job_config.get("tags", [])
    normalized_tags = [tag.replace("-", "_").replace(":", ".").replace(" ", "_") for tag in raw_tags]

    world_package = job_config["world"]["package"]
    world_config = job_config["world"].get("config")
    runtime = job_config.get("runtime")

    console.print("[blue]🚀 Launching job...[/blue]")
    console.print(f"   World: {world_package}")

    try:
        with Chronos(base_url=chronos_url, api_key=api_key) as client:
            resp = client.launch(
                package=world_package,
                config=world_config,
                tags=normalized_tags,
                runtime=runtime,
            )

        console.print("\n[green]✅ Job launched successfully![/green]")
        console.print(f"   Session ID: {resp.session_id}")
        console.print(f"   Plato Session: {resp.plato_session_id or 'N/A'}")
        console.print(f"   Status: {resp.status}")
        console.print(f"\n[dim]View at: {chronos_url}/sessions/{resp.session_id}[/dim]")

        if wait:
            console.print("\n[yellow]--wait not yet implemented[/yellow]")

    except Exception as e:
        console.print(f"[red]❌ Failed to launch job: {e}[/red]")
        raise typer.Exit(1)


@chronos_app.command()
def example(
    world: str = typer.Argument(
        "structured-execution",
        help="World to generate example config for",
    ),
    output: Path = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path (prints to stdout if not specified)",
    ),
):
    """Generate an example job config file.

    Creates a sample JSON configuration for launching Chronos jobs, which can be
    customized for your use case.

    Arguments:
        world: World type to generate example for (default: "structured-execution")

    Options:
        -o, --output: Output file path. If not specified, prints to stdout.

    Available worlds: structured-execution, code-world
    """
    examples = {
        "structured-execution": {
            "world_package": "plato-world-structured-execution",
            "world_version": "latest",
            "world_config": {
                "sim_name": "my-sim",
                "github_url": "https://github.com/example/repo",
                "max_attempts": 3,
                "use_backtrack": True,
                "skill_runner": {
                    "image": "claude-code:2.1.5",
                    "config": {"model_name": "anthropic/claude-sonnet-4-20250514", "max_turns": 100},
                },
                "plato_api_key": "pk_xxx",
                "anthropic_api_key": "sk-ant-xxx",
            },
            "_comment": "Agents and secrets are embedded directly in world_config",
        },
        "code-world": {
            "world_package": "plato-world-code",
            "world_config": {
                "task": "Fix the bug in src/main.py",
                "repo_url": "https://github.com/example/repo",
                "coder": {
                    "image": "claude-code:latest",
                    "config": {"model_name": "anthropic/claude-sonnet-4-20250514"},
                },
            },
            "_comment": "world_version is optional - uses latest if not specified",
        },
    }

    if world not in examples:
        console.print(f"[red]❌ Unknown world: {world}[/red]")
        console.print(f"Available examples: {list(examples.keys())}")
        raise typer.Exit(1)

    example_config = examples[world]
    json_output = json.dumps(example_config, indent=2)

    if output:
        with open(output, "w") as f:
            f.write(json_output)
        console.print(f"[green]✅ Example config written to {output}[/green]")
    else:
        console.print(json_output)


def _get_world_runner_dockerfile() -> Path:
    """Get the path to the world runner Dockerfile template."""
    return Path(__file__).parent / "templates" / "world-runner.Dockerfile"


def _build_world_runner_image(platform_override: str | None = None) -> str:
    """Build the world runner Docker image if needed."""
    image_tag = "plato-world-runner:latest"
    dockerfile_path = _get_world_runner_dockerfile()

    if not dockerfile_path.exists():
        raise FileNotFoundError(f"World runner Dockerfile not found: {dockerfile_path}")

    docker_platform = _get_docker_platform(platform_override)

    # Check if image exists
    result = subprocess.run(
        ["docker", "images", "-q", image_tag],
        capture_output=True,
        text=True,
    )

    if result.stdout.strip():
        # Image exists
        return image_tag

    console.print("[blue]Building world runner image...[/blue]")

    cmd = [
        "docker",
        "build",
        "--platform",
        docker_platform,
        "-t",
        image_tag,
        "-f",
        str(dockerfile_path),
        str(dockerfile_path.parent),
    ]

    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise RuntimeError("Failed to build world runner image")

    console.print(f"[green]✅ Built {image_tag}[/green]")
    return image_tag


def _get_docker_platform(override: str | None = None) -> str:
    """Get the appropriate Docker platform for the current system."""
    if override:
        return override

    import platform as plat

    system = plat.system()
    machine = plat.machine().lower()

    if system == "Darwin" and machine in ("arm64", "aarch64"):
        return "linux/arm64"
    elif system == "Linux" and machine in ("arm64", "aarch64"):
        return "linux/arm64"
    else:
        return "linux/amd64"


def _get_docker_host_ip() -> str:
    """Get the Docker host IP address accessible from containers."""
    try:
        result = subprocess.run(
            ["docker", "network", "inspect", "bridge", "--format", "{{range .IPAM.Config}}{{.Gateway}}{{end}}"],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0 and result.stdout.strip():
            return result.stdout.strip()
    except Exception:
        pass
    # Fallback to common Docker gateway IP
    return "172.17.0.1"


def _build_agent_image(
    agent_name: str,
    agents_dir: Path,
    platform_override: str | None = None,
) -> bool:
    """Build a local agent Docker image."""
    agents_dir = agents_dir.expanduser().resolve()
    agent_path = agents_dir / agent_name
    dockerfile_path = agent_path / "Dockerfile"

    if not dockerfile_path.exists():
        logger.warning(f"No Dockerfile found for agent '{agent_name}' at {dockerfile_path}")
        return False

    image_tag = f"{agent_name}:latest"
    docker_platform = _get_docker_platform(platform_override)

    # Determine build context - check if we're in plato-client structure
    plato_client_root = agents_dir.parent if agents_dir.name == "agents" else None

    if plato_client_root and (plato_client_root / "python-sdk").exists():
        build_context = str(plato_client_root)
        target = "dev"
        console.print(f"[blue]Building {image_tag} (dev mode from {build_context})...[/blue]")
    else:
        build_context = str(agent_path)
        target = "prod"
        console.print(f"[blue]Building {image_tag} (prod mode from {build_context})...[/blue]")

    console.print(f"[dim]Platform: {docker_platform}[/dim]")

    cmd = [
        "docker",
        "build",
        "--platform",
        docker_platform,
        "--build-arg",
        f"PLATFORM={docker_platform}",
        "--target",
        target,
        "-t",
        image_tag,
        "-f",
        str(dockerfile_path),
        build_context,
    ]

    result = subprocess.run(cmd)
    if result.returncode != 0:
        console.print(f"[red]❌ Failed to build {image_tag}[/red]")
        return False

    console.print(f"[green]✅ Built {image_tag}[/green]")
    return True


def _extract_agent_images_from_config(config_data: dict) -> list[str]:
    """Extract local agent image names from config data."""
    images = []

    # Check agents section
    agents = config_data.get("agents", {})
    for agent_config in agents.values():
        if isinstance(agent_config, dict):
            image = agent_config.get("image", "")
            # Only include local images (no registry prefix)
            if image and "/" not in image.split(":")[0]:
                name = image.split(":")[0]
                if name not in images:
                    images.append(name)

    # Also check direct coder/verifier fields
    for field in ["coder", "verifier", "skill_runner"]:
        agent_config = config_data.get(field, {})
        if isinstance(agent_config, dict):
            image = agent_config.get("image", "")
            if image and "/" not in image.split(":")[0]:
                name = image.split(":")[0]
                if name not in images:
                    images.append(name)

    return images


async def _create_chronos_session(
    chronos_url: str,
    api_key: str,
    world_name: str,
    world_config: dict,
    plato_session_id: str | None = None,
    tags: list[str] | None = None,
) -> dict:
    """Create a session in Chronos."""
    import httpx

    from plato.chronos.api.sessions import create_session
    from plato.chronos.models import CreateSessionRequest

    body = CreateSessionRequest(
        world_name=world_name,
        world_config=world_config,
        plato_session_id=plato_session_id,
        tags=tags or [],
    )

    async with httpx.AsyncClient(base_url=chronos_url.rstrip("/"), timeout=30.0) as client:
        resp = await create_session.asyncio(client, body=body, x_api_key=api_key)
        return resp.model_dump(mode="json")


async def _close_chronos_session(
    chronos_url: str,
    api_key: str,
    session_id: str,
) -> None:
    """Close a Chronos session."""
    import httpx

    from plato.chronos.api.sessions import close_session

    try:
        async with httpx.AsyncClient(base_url=chronos_url.rstrip("/"), timeout=30.0) as client:
            await close_session.asyncio(client, public_id=session_id, x_api_key=api_key)
            logger.info(f"Closed Chronos session: {session_id}")
    except Exception as e:
        logger.warning(f"Failed to close Chronos session: {e}")


async def _complete_chronos_session(
    chronos_url: str,
    api_key: str,
    session_id: str,
    status: str,
    exit_code: int | None = None,
    error_message: str | None = None,
) -> None:
    """Complete a Chronos session with final status."""
    import httpx

    from plato.chronos.api.sessions import complete_session
    from plato.chronos.models import CompleteSessionRequest

    body = CompleteSessionRequest(
        status=status,
        exit_code=exit_code,
        error_message=error_message,
    )

    try:
        async with httpx.AsyncClient(base_url=chronos_url.rstrip("/"), timeout=30.0) as client:
            await complete_session.asyncio(client, public_id=session_id, body=body, x_api_key=api_key)
            logger.info(f"Completed Chronos session: {session_id} with status: {status}")
    except Exception as e:
        logger.warning(f"Failed to complete Chronos session: {e}")


async def _run_dev_impl(
    world_dir: Path,
    config_path: Path,
    agents_dir: Path | None = None,
    platform_override: str | None = None,
    env_timeout: int = 7200,
) -> None:
    """Run a world locally in a Docker container.

    This:
    1. Builds local agent images if --agents-dir is provided
    2. Creates Plato environments
    3. Creates Chronos session for OTel traces
    4. Runs the world in a Docker container with docker.sock mounted
    """
    from plato._generated.models import Envs
    from plato.v2 import AsyncPlato
    from plato.worlds.config import EnvConfig

    # Get required env vars
    chronos_url = os.environ.get("CHRONOS_URL", "https://chronos.plato.so")
    api_key = os.environ.get("PLATO_API_KEY")

    if not api_key:
        raise ValueError("PLATO_API_KEY environment variable is required")

    # Resolve paths
    world_dir = world_dir.expanduser().resolve()
    config_path = config_path.expanduser().resolve()

    # Load config with environment variable expansion
    with open(config_path) as f:
        config_text = f.read()
    # Expand ${VAR} and $VAR patterns using os.path.expandvars
    config_text = os.path.expandvars(config_text)
    raw_config = json.loads(config_text)

    # Validate config format: { world: { package, config }, runtime: { artifact_id } }
    if "world" not in raw_config or "package" not in raw_config.get("world", {}):
        raise ValueError("Invalid config: missing world.package")

    world_package = raw_config["world"]["package"]
    config_data = raw_config["world"].get("config", {}).copy()
    runtime_artifact_id = raw_config.get("runtime", {}).get("artifact_id")
    if runtime_artifact_id:
        config_data["runtime_artifact_id"] = runtime_artifact_id

    # Parse world name from package (e.g., "plato-world-structured-execution:0.1.17")
    world_package_name = world_package.split(":")[0] if ":" in world_package else world_package
    if world_package_name.startswith("plato-world-"):
        world_name = world_package_name[len("plato-world-") :]
    else:
        world_name = world_package_name or "unknown"

    # Build local agent images if agents_dir is provided
    if agents_dir:
        agents_dir = agents_dir.expanduser().resolve()
        agent_images = _extract_agent_images_from_config(config_data)
        if agent_images:
            console.print(f"[blue]Building agent images: {agent_images}[/blue]")
            for agent_name in agent_images:
                success = _build_agent_image(agent_name, agents_dir, platform_override)
                if not success:
                    raise RuntimeError(f"Failed to build agent image: {agent_name}")

    # Import world module to get config class for environment detection
    # We need to dynamically load the world from world_dir
    import sys

    sys.path.insert(0, str(world_dir / "src"))

    try:
        # Try to import the world module

        world_module_path = list((world_dir / "src").glob("*_world/*.py"))
        if not world_module_path:
            world_module_path = list((world_dir / "src").glob("*/__init__.py"))

        env_configs: list[EnvConfig] = []

        # Try to extract env configs from world config
        if "envs" in config_data:
            for env_cfg in config_data["envs"]:
                env_configs.append(Envs.model_validate(env_cfg).root)
    finally:
        if str(world_dir / "src") in sys.path:
            sys.path.remove(str(world_dir / "src"))

    # Create Plato client and session
    plato = AsyncPlato()
    session = None
    plato_session_id: str | None = None
    chronos_session_id: str | None = None

    try:
        if env_configs:
            console.print(f"[blue]Creating {len(env_configs)} Plato environments...[/blue]")
            session = await plato.sessions.create(envs=env_configs, timeout=env_timeout)
            plato_session_id = session.session_id
            console.print(f"[green]✅ Created Plato session: {plato_session_id}[/green]")

            # Add session to config (convert Pydantic model to dict for JSON serialization)
            config_data["plato_session"] = session.dump().model_dump()

        # Create Chronos session
        console.print("[blue]Creating Chronos session...[/blue]")
        tags = raw_config.get("tags", [])
        chronos_session = await _create_chronos_session(
            chronos_url=chronos_url,
            api_key=api_key,
            world_name=world_name,
            world_config=config_data,
            plato_session_id=plato_session_id,
            tags=tags,
        )
        chronos_session_id = chronos_session["public_id"]
        console.print(f"[green]✅ Created Chronos session: {chronos_session_id}[/green]")
        console.print(f"[dim]View at: {chronos_url}/sessions/{chronos_session_id}[/dim]")

        # Add session info to config
        config_data["session_id"] = chronos_session_id
        # Use otel_url from backend response (uses tunnel if available), or construct it
        otel_url = chronos_session.get("otel_url") or f"{chronos_url.rstrip('/')}/api/otel"
        # For Docker containers, replace localhost with Docker gateway IP
        if "localhost" in otel_url or "127.0.0.1" in otel_url:
            docker_host_ip = _get_docker_host_ip()
            otel_url = otel_url.replace("localhost", docker_host_ip).replace("127.0.0.1", docker_host_ip)
        config_data["otel_url"] = otel_url
        config_data["upload_url"] = chronos_session.get("upload_url", "")

        # Write updated config to temp file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
            # Write in direct format (not Chronos format) for the world runner
            json.dump(config_data, f)
            container_config_path = f.name

        # Create shared workspace volume for DIND compatibility
        import uuid as uuid_mod

        workspace_volume = f"plato-workspace-{uuid_mod.uuid4().hex[:8]}"
        subprocess.run(
            ["docker", "volume", "create", workspace_volume],
            capture_output=True,
        )
        console.print(f"[blue]Created workspace volume: {workspace_volume}[/blue]")

        try:
            # Run world in Docker container
            console.print("[blue]Starting world in Docker container...[/blue]")

            docker_platform = _get_docker_platform(platform_override)

            # Build world runner image if needed
            world_runner_image = _build_world_runner_image(platform_override)

            # Find python-sdk relative to world_dir (assumes plato-client structure)
            # world_dir: plato-client/worlds/structured-execution
            # python_sdk: plato-client/python-sdk
            python_sdk_dir = world_dir.parent.parent / "python-sdk"

            # For Docker containers, replace localhost with Docker gateway IP
            docker_chronos_url = chronos_url
            if "localhost" in docker_chronos_url or "127.0.0.1" in docker_chronos_url:
                docker_host_ip = _get_docker_host_ip()
                docker_chronos_url = docker_chronos_url.replace("localhost", docker_host_ip).replace(
                    "127.0.0.1", docker_host_ip
                )

            docker_cmd = [
                "docker",
                "run",
                "--rm",
                "--platform",
                docker_platform,
                "--privileged",
                "-v",
                "/var/run/docker.sock:/var/run/docker.sock",
                "-v",
                f"{world_dir}:/world:ro",
                "-v",
                f"{python_sdk_dir}:/python-sdk:ro",  # Mount local SDK for dev
                "-v",
                f"{container_config_path}:/config.json:ro",
                "-v",
                f"{workspace_volume}:/tmp/workspace",  # Shared workspace volume
                "-e",
                f"WORLD_NAME={world_name}",
                "-e",
                f"WORKSPACE_VOLUME={workspace_volume}",  # Pass volume name for run_agent
                "-e",
                f"CHRONOS_URL={docker_chronos_url}",
                "-e",
                f"PLATO_API_KEY={api_key}",
                "-e",
                f"SESSION_ID={chronos_session_id}",
                "-e",
                f"OTEL_EXPORTER_OTLP_ENDPOINT={otel_url}",
                "-e",
                f"UPLOAD_URL={chronos_session.get('upload_url', '')}",
            ]

            # Use world runner image
            docker_cmd.append(world_runner_image)

            console.print(f"[dim]Running: docker run ... {world_runner_image}[/dim]")

            # Run and stream output
            process = subprocess.Popen(
                docker_cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
            )

            if process.stdout:
                for line in process.stdout:
                    print(line, end="")

            process.wait()
            world_exit_code = process.returncode

            if world_exit_code != 0:
                raise RuntimeError(f"World execution failed with exit code {world_exit_code}")

        finally:
            os.unlink(container_config_path)
            # Clean up workspace volume
            subprocess.run(
                ["docker", "volume", "rm", "-f", workspace_volume],
                capture_output=True,
            )
            console.print(f"[dim]Cleaned up workspace volume: {workspace_volume}[/dim]")

    except Exception as e:
        # Complete session as failed
        if chronos_session_id:
            await _complete_chronos_session(
                chronos_url,
                api_key,
                chronos_session_id,
                status="failed",
                exit_code=getattr(e, "exit_code", 1),
                error_message=str(e)[:500],
            )
        raise
    else:
        # Complete session as successful
        if chronos_session_id:
            await _complete_chronos_session(
                chronos_url,
                api_key,
                chronos_session_id,
                status="completed",
                exit_code=0,
            )
    finally:
        if session:
            console.print("[blue]Closing Plato session...[/blue]")
            await session.close()
        await plato.close()


@chronos_app.command()
def stop(
    session_id: Annotated[
        str,
        typer.Argument(help="Session ID to stop"),
    ],
    chronos_url: str = typer.Option(
        None,
        "--url",
        "-u",
        envvar="CHRONOS_URL",
        help="Chronos API URL (default: https://chronos.plato.so)",
    ),
    api_key: str = typer.Option(
        None,
        "--api-key",
        "-k",
        envvar="PLATO_API_KEY",
        help="Plato API key for authentication",
    ),
):
    """Stop a running Chronos session.

    Marks the session as cancelled with status reason "User cancelled" and terminates
    any running containers.

    Arguments:
        session_id: The session ID to stop (from 'plato chronos launch' output)

    Options:
        -u, --url: Chronos API URL (default: https://chronos.plato.so, or CHRONOS_URL env var)
        -k, --api-key: Plato API key for authentication (or PLATO_API_KEY env var)
    """
    # Set defaults
    if not chronos_url:
        chronos_url = "https://chronos.plato.so"

    if not api_key:
        console.print("[red]❌ No API key provided[/red]")
        console.print("Set PLATO_API_KEY environment variable or use --api-key")
        raise typer.Exit(1)

    console.print(f"[yellow]⏹ Stopping session {session_id}...[/yellow]")

    async def _stop():
        await _complete_chronos_session(
            chronos_url=chronos_url,
            api_key=api_key,
            session_id=session_id,
            status="cancelled",
            error_message="User cancelled",
        )

    try:
        asyncio.run(_stop())
        console.print(f"[green]✅ Session {session_id} stopped[/green]")
    except Exception as e:
        console.print(f"[red]❌ Failed to stop session: {e}[/red]")
        raise typer.Exit(1)


@chronos_app.command()
def dev(
    config: Annotated[
        Path,
        typer.Argument(help="Path to config JSON file", exists=True, readable=True),
    ],
    world_dir: Annotated[
        Path,
        typer.Option("--world-dir", "-w", help="Directory containing world source code"),
    ],
    agents_dir: Annotated[
        Path | None,
        typer.Option("--agents-dir", "-a", help="Directory containing agent source code"),
    ] = None,
    platform: Annotated[
        str | None,
        typer.Option("--platform", "-p", help="Docker platform (e.g., linux/amd64)"),
    ] = None,
    env_timeout: Annotated[
        int,
        typer.Option("--env-timeout", help="Timeout for environment creation (seconds)"),
    ] = 7200,
):
    """Run a world locally for development/debugging.

    Builds and runs the world in a Docker container with docker.sock mounted,
    allowing the world to spawn agent containers. Mounts local source code for
    live development without rebuilding.

    Arguments:
        config: Path to job config JSON file (same format as 'plato chronos launch')

    Options:
        -w, --world-dir: Directory containing world source code to mount into the container
        -a, --agents-dir: Directory containing agent source code to mount (optional)
        -p, --platform: Docker platform for building (e.g., 'linux/amd64' for M1 Macs)
        --env-timeout: Timeout in seconds for environment creation (default: 7200 = 2 hours)
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    if not os.environ.get("PLATO_API_KEY"):
        console.print("[red]❌ PLATO_API_KEY environment variable required[/red]")
        raise typer.Exit(1)

    try:
        asyncio.run(_run_dev_impl(world_dir, config, agents_dir, platform, env_timeout))
    except Exception as e:
        console.print(f"[red]❌ Failed: {e}[/red]")
        logger.exception("World execution failed")
        raise typer.Exit(1)
