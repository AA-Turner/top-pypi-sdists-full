"""Agent CLI commands for Plato."""

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import typer

from plato.cli.chronos.settings import get_settings as get_chronos_settings
from plato.cli.utils import (
    console,
    maybe_bump_package_version,
    prepare_build_context_with_sdk,
    require_api_key,
    wait_for_pypi_version,
)
from plato.utils.ecr import (
    ECR_REGISTRY,
    get_image_digest,
    publish_docker_image,
    retag_agent_image_via_chronos,
    retag_image,
)
from plato.utils.pypi_index import plato_token_simple_index
from plato.v2 import Env, Plato
from plato.v2.types import SimConfigCompute


def _extract_schemas(pkg_path: Path, package_name: str) -> tuple[dict | None, dict | None, dict | None]:
    """Extract Config, BuildConfig, and SecretsConfig schemas from the agent package.

    Looks for:
    - Config class - runtime configuration (stored as config_schema)
    - BuildConfig class - build-time template variables (stored as template_variables)
    - SecretsConfig class - secrets/API keys (stored as secrets_schema)

    Returns tuple of (config_schema, build_config_schema, secrets_schema).
    """
    import inspect

    # Convert package name to module name (replace - with _)
    module_name = package_name.replace("-", "_")

    # Extract short name (e.g., "claude-code" from "plato-agent-claude-code")
    short_name = package_name
    for prefix in ("plato-agent-", "plato-"):
        if short_name.startswith(prefix):
            short_name = short_name[len(prefix) :]
            break
    short_name_under = short_name.replace("-", "_")

    # Add package src to path temporarily
    src_path = pkg_path / "src"
    paths_added = []
    if src_path.exists():
        sys.path.insert(0, str(src_path))
        paths_added.append(str(src_path))
    sys.path.insert(0, str(pkg_path))
    paths_added.append(str(pkg_path))

    try:
        from pydantic import BaseModel

        # Build list of possible module locations
        locations = [
            module_name,
            f"{module_name}.config",
            f"{module_name}.agent",
            f"plato.agent.{short_name_under}",
            f"plato.agent.{short_name_under}.config",
            f"plato.agent.{short_name_under}.agent",
            f"plato_agent_{short_name_under}",
            f"{short_name_under}_agent",
        ]

        config_schema = None
        build_config_schema = None
        secrets_schema = None

        for loc in locations:
            try:
                module = __import__(loc, fromlist=["*"])

                # Look for Config, BuildConfig, and SecretsConfig classes
                for name, obj in inspect.getmembers(module, inspect.isclass):
                    if not isinstance(obj, type) or not issubclass(obj, BaseModel):
                        continue
                    if obj is BaseModel:
                        continue

                    if name == "Config":
                        console.print(f"[green]Found Config class in {loc}[/green]")
                        config_schema = obj.model_json_schema()
                    elif name == "BuildConfig":
                        console.print(f"[green]Found BuildConfig class in {loc}[/green]")
                        build_config_schema = obj.model_json_schema()
                    elif name == "SecretsConfig":
                        console.print(f"[green]Found SecretsConfig class in {loc}[/green]")
                        secrets_schema = obj.model_json_schema()

                # If we found at least one, stop searching
                if config_schema or build_config_schema or secrets_schema:
                    break

            except (ImportError, ModuleNotFoundError):
                continue
            except Exception as e:
                console.print(f"[yellow]Warning: Error importing {loc}: {e}[/yellow]")
                continue

        return config_schema, build_config_schema, secrets_schema
    except ImportError:
        # pydantic not available
        return None, None, None
    finally:
        # Clean up sys.path
        for path in paths_added:
            if path in sys.path:
                sys.path.remove(path)


def _extract_config_schema(pkg_path: Path, package_name: str) -> dict | None:
    """Extract config schema from the agent package (legacy wrapper)."""
    config_schema, _, _ = _extract_schemas(pkg_path, package_name)
    return config_schema


def _extract_template_variables(build_config_schema: dict | None) -> dict[str, str] | None:
    """Extract template variables from BuildConfig schema.

    All fields in BuildConfig are considered build-time template variables.
    These are stored separately for easy querying.

    Returns dict of field name -> default value (or empty string), or None if no fields.
    """
    if not build_config_schema:
        return None

    properties = build_config_schema.get("properties", {})
    if not properties:
        return None

    template_vars = {}
    for field_name, prop in properties.items():
        # Store the default value if present, otherwise empty string
        default = prop.get("default")
        if default is not None:
            template_vars[field_name] = str(default)
        else:
            template_vars[field_name] = ""

    return template_vars if template_vars else None


agent_app = typer.Typer(help="Manage and deploy agents")


def _prefetch_agent_image(image_url: str, agent_name: str) -> None:
    console.print("[cyan]Starting VM to prefetch image...[/cyan]")

    try:
        plato = Plato()
        env = Env.resource(
            simulator=f"prefetch-{agent_name}",
            sim_config=SimConfigCompute(),
            docker_image_url=image_url,
            upload_rootfs=True,
            rootfs_storage_backend="snapshot-store",
        )
        session = plato.sessions.create(
            envs=[env],
            timeout=600,
            connect_network=False,
        )
        console.print("[green]Prefetch complete - rootfs cached[/green]")
        session.close()
        plato.close()
    except Exception as e:
        console.print(f"[yellow]Prefetch failed (non-fatal): {e}[/yellow]")


def _publish_agent_image(
    agent_name: str,
    version: str,
    build_path: Path,
    description: str,
    dry_run: bool,
    build_args: dict[str, str] | None = None,
    no_cache: bool = False,
) -> None:
    """Build and publish an agent Docker image to ECR."""
    # Check Docker is available
    if not shutil.which("docker"):
        console.print("[red]Error: docker not found[/red]")
        raise typer.Exit(1)

    ecr_image = f"{ECR_REGISTRY}/vm/rootfs/plato-agents/{agent_name}:{version}"
    latest_image = f"{ECR_REGISTRY}/vm/rootfs/plato-agents/{agent_name}:latest"

    console.print(f"[cyan]Agent:[/cyan] {agent_name}")
    console.print(f"[cyan]Version:[/cyan] {version}")
    console.print()

    if dry_run:
        console.print("[yellow]Dry run - would build and push:[/yellow]")
        console.print(f"  {ecr_image}")
        console.print(f"  {latest_image}")
        return

    # Get current :latest digest before pushing (to detect changes)
    repository = f"vm/rootfs/plato-agents/{agent_name}"
    old_digest = get_image_digest(repository, "latest")

    console.print("[cyan]Building and pushing Docker image...[/cyan]")
    result = publish_docker_image(
        name=agent_name,
        version=version,
        build_path=str(build_path),
        repo_prefix="vm/rootfs/plato-agents",
        build_args=build_args,
        no_cache=no_cache,
    )

    if not result.success:
        console.print(f"[red]{result.error}[/red]")
        raise typer.Exit(1)

    console.print(f"[green]Published:[/green] {result.ecr_image}")
    console.print(f"[green]Published:[/green] {result.latest_image}")
    console.print("\n[bold]Use in config:[/bold]")
    console.print(f'  "image": "{result.ecr_image}"')

    # Prefetch if the Docker image digest changed
    new_digest = get_image_digest(repository, "latest")
    if new_digest != old_digest:
        console.print()
        console.print("[bold]Step 4: Prefetching image (digest changed)...[/bold]")
        _prefetch_agent_image(latest_image, agent_name)
    else:
        console.print("\n[dim]Docker image digest unchanged - skipping prefetch[/dim]")


def _publish_package(path: str, repo: str, dry_run: bool = False):
    """
    Helper function to build and publish a package to a Plato PyPI repository.

    Args:
        path: Path to the package directory
        repo: Repository name (e.g., "agents", "worlds")
        dry_run: If True, build without uploading
    """
    try:
        import tomli
    except ImportError:
        console.print("[red]Error: tomli is not installed[/red]")
        console.print("\n[yellow]Install with:[/yellow]")
        console.print("  pip install tomli")
        raise typer.Exit(1) from None

    # Get API key (skip check for dry_run)
    api_key = None
    if not dry_run:
        api_key = require_api_key()

    # Get base URL (default to production)
    base_url = os.getenv("PLATO_BASE_URL", "https://plato.so")
    # Normalize: remove trailing slash and /api if present
    base_url = base_url.rstrip("/")
    if base_url.endswith("/api"):
        base_url = base_url[:-4]
    api_url = f"{base_url}/api"

    # Resolve package path
    pkg_path = Path(path).resolve()
    if not pkg_path.exists():
        console.print(f"[red]Error: Path does not exist: {pkg_path}[/red]")
        raise typer.Exit(1)

    # Load pyproject.toml
    pyproject_file = pkg_path / "pyproject.toml"
    if not pyproject_file.exists():
        console.print(f"[red]Error: No pyproject.toml found at {pkg_path}[/red]")
        raise typer.Exit(1)

    try:
        with open(pyproject_file, "rb") as f:
            pyproject = tomli.load(f)
    except Exception as e:
        console.print(f"[red]Error reading pyproject.toml: {e}[/red]")
        raise typer.Exit(1) from e

    # Extract package info
    project = pyproject.get("project", {})
    package_name = project.get("name")
    version = project.get("version")

    if not package_name:
        console.print("[red]Error: No package name in pyproject.toml[/red]")
        raise typer.Exit(1)
    if not version:
        console.print("[red]Error: No version in pyproject.toml[/red]")
        raise typer.Exit(1)

    console.print(f"[cyan]Package:[/cyan] {package_name}")
    console.print(f"[cyan]Version:[/cyan] {version}")
    console.print(f"[cyan]Repository:[/cyan] {repo}")
    console.print(f"[cyan]Path:[/cyan] {pkg_path}")
    console.print()

    # Build package
    console.print("[cyan]Building package...[/cyan]")
    try:
        result = subprocess.run(
            ["uv", "build"],
            cwd=pkg_path,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            console.print("[red]Build failed:[/red]")
            console.print(result.stderr)
            raise typer.Exit(1)
        console.print("[green]Build successful[/green]")
    except FileNotFoundError:
        console.print("[red]Error: uv not found. Install with: pip install uv[/red]")
        raise typer.Exit(1) from None

    # Find built wheel
    dist_dir = pkg_path / "dist"
    if not dist_dir.exists():
        console.print("[red]Error: dist/ directory not found after build[/red]")
        raise typer.Exit(1)

    normalized_name = package_name.replace("-", "_")
    wheel_files = list(dist_dir.glob(f"{normalized_name}-{version}-*.whl"))

    if not wheel_files:
        # Try without version in pattern
        wheel_files = list(dist_dir.glob("*.whl"))

    if not wheel_files:
        console.print(f"[red]Error: No wheel file found in {dist_dir}[/red]")
        raise typer.Exit(1)

    wheel_file = wheel_files[0]
    console.print(f"[cyan]Built:[/cyan] {wheel_file.name}")

    if dry_run:
        console.print("\n[yellow]Dry run - skipping upload[/yellow]")
        return

    # Upload using uv publish
    upload_url = f"{api_url}/v2/pypi/{repo}/"
    console.print(f"\n[cyan]Uploading to {upload_url}...[/cyan]")

    # api_key is guaranteed to be set (checked earlier when not dry_run)
    assert api_key is not None, "api_key must be set when not in dry_run mode"
    try:
        result = subprocess.run(
            [
                "uv",
                "publish",
                "--publish-url",
                upload_url,
                "--username",
                "__token__",
                "--password",
                api_key,
                str(wheel_file),
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode == 0:
            console.print("[green]Upload successful![/green]")
            console.print("\n[bold]Install with:[/bold]")
            console.print(f"  uv add {package_name} --index-url {api_url}/v2/pypi/{repo}/simple/")
        else:
            console.print("[red]Upload failed:[/red]")
            if result.stdout:
                console.print(result.stdout)
            if result.stderr:
                console.print(result.stderr)
            raise typer.Exit(1)

    except FileNotFoundError:
        console.print("[red]Error: uv not found[/red]")
        raise typer.Exit(1) from None
    except Exception as e:
        console.print(f"[red]Upload error: {e}[/red]")
        raise typer.Exit(1) from e


@agent_app.command(name="list")
def agent_list():
    """List available Plato agents."""
    console.print("[bold]Plato Agents:[/bold]\n")

    plato_agents = [
        (
            "computer-use",
            "Browser automation agent (pip install plato-agent-computer-use)",
        ),
    ]

    for name, description in plato_agents:
        console.print(f"  [cyan]{name:<15}[/cyan] {description}")

    console.print("\n[bold]Usage:[/bold]")
    console.print("  plato agent publish <path>")


@agent_app.command(name="schema")
def agent_schema(
    agent_name: str = typer.Argument(..., help="Agent name to get schema for"),
):
    """Get the configuration schema for an agent.

    Shows the JSON schema defining configuration options for the specified agent.
    The schema describes what fields are available when configuring the agent for runs.

    Arguments:
        agent_name: Name of the agent (e.g., 'claude-code', 'openhands')
    """
    try:
        from plato.agents import AGENT_SCHEMAS, get_agent_schema
    except ImportError:
        console.print("[red]Error: plato.agents module not available[/red]")
        console.print("\n[yellow]Install with:[/yellow]")
        console.print("  pip install 'plato-sdk-v2[agents]'")
        raise typer.Exit(1) from None

    schema = get_agent_schema(agent_name)
    if not schema:
        console.print(f"[red]Error: No schema found for agent '{agent_name}'[/red]")
        console.print("\n[yellow]Available agents:[/yellow]")
        for name in sorted(AGENT_SCHEMAS.keys()):
            console.print(f"  {name}")
        raise typer.Exit(1)

    console.print(f"[bold]Schema for {agent_name}:[/bold]\n")
    console.print(json.dumps(schema, indent=2))


@agent_app.command(name="publish")
def agent_publish(
    target: str = typer.Argument(".", help="Path to agent directory"),
    all_agents: bool = typer.Option(False, "--all", "-a", help="Publish all agents in directory"),
    minor: bool = typer.Option(False, "--minor", help="Bump the minor version before publishing"),
    dev: bool = typer.Option(
        False,
        "--dev",
        help="Publish the next dated PEP 440 dev version without prompting",
    ),
    dry_run: bool = typer.Option(False, "--dry-run", help="Build without uploading"),
    skip_docker: bool = typer.Option(
        False,
        "--skip-docker",
        help="Skip Docker build; retag the current :latest image with the new version tag instead",
    ),
    no_cache: bool = typer.Option(False, "--no-cache", help="Build Docker image without cache"),
    no_skip_docker: bool = typer.Option(
        False,
        "--no-skip-docker",
        help="Force Docker rebuild even with --dev (overrides the default skip behavior)",
    ),
):
    """Build and publish an agent package to the Plato agents repository.

    Builds with 'uv build' and uploads to the Plato PyPI repository via uv publish.

    The agent package will be installable via:
        uv pip install <package> --index-url https://plato.so/api/v2/pypi/agents/simple/

    Arguments:
        target: Path to agent directory containing pyproject.toml

    Options:
        -a, --all: Publish all agents found in the target directory
        --dry-run: Build without uploading
        --skip-docker: Retag :latest instead of rebuilding Docker image
        --no-skip-docker: Force Docker rebuild even with --dev
    """

    # --dev implies --skip-docker unless --no-skip-docker is explicitly passed
    if dev and not skip_docker and not no_skip_docker:
        skip_docker = True
        console.print(
            "[dim]--dev implies --skip-docker (retag instead of rebuild). Use --no-skip-docker to force a rebuild.[/dim]"
        )

    # Handle --all flag with directory
    if all_agents:
        target_path = Path(target).resolve()
        if not target_path.is_dir():
            console.print(f"[red]Error: '{target}' is not a directory[/red]")
            raise typer.Exit(1)

        # Find all subdirectories with pyproject.toml (custom agents)
        agent_dirs = [d for d in target_path.iterdir() if d.is_dir() and (d / "pyproject.toml").exists()]

        if not agent_dirs:
            console.print(f"[yellow]No agents found in {target_path}[/yellow]")
            console.print("[dim]Looking for subdirectories with pyproject.toml[/dim]")
            raise typer.Exit(1)

        console.print(f"[bold]Publishing {len(agent_dirs)} agents from {target_path}...[/bold]\n")

        failed = []
        succeeded = []

        for agent_dir in sorted(agent_dirs):
            console.print(f"\n[bold cyan]{'=' * 50}[/bold cyan]")
            console.print(f"[bold cyan]{agent_dir.name}[/bold cyan]")
            console.print(f"[bold cyan]{'=' * 50}[/bold cyan]\n")

            try:
                _push_single_agent(agent_dir, dry_run, minor=minor, dev=dev, skip_docker=skip_docker, no_cache=no_cache)
                succeeded.append(agent_dir.name)
            except SystemExit:
                failed.append(agent_dir.name)
            except Exception as e:
                console.print(f"[red]Error: {e}[/red]")
                failed.append(agent_dir.name)

        console.print(f"\n[bold]{'=' * 50}[/bold]")
        console.print(f"[green]Succeeded:[/green] {len(succeeded)}")
        console.print(f"[red]Failed:[/red] {len(failed)}")
        if failed:
            console.print(f"[yellow]Failed:[/yellow] {', '.join(failed)}")
        return

    # Treat target as a path to agent directory
    pkg_path = Path(target).resolve()
    if not pkg_path.exists():
        console.print(f"[red]Error: '{target}' is not a valid path[/red]")
        raise typer.Exit(1)

    _push_single_agent(pkg_path, dry_run, minor=minor, dev=dev, skip_docker=skip_docker, no_cache=no_cache)


def _push_single_agent(
    pkg_path: Path,
    dry_run: bool,
    *,
    minor: bool = False,
    dev: bool = False,
    skip_docker: bool = False,
    no_cache: bool = False,
) -> None:
    """Publish a single agent package to PyPI and optionally Docker.

    Builds the package and uploads to the Plato agents repository.
    """
    # NOTE: The dev/skip_docker default is handled by the CLI entry point.
    # Do not override skip_docker here.
    # Load pyproject.toml for version
    pyproject_file = pkg_path / "pyproject.toml"
    if not pyproject_file.exists():
        console.print(f"[red]Error: No pyproject.toml found at {pkg_path}[/red]")
        raise typer.Exit(1)

    try:
        import tomli

        with open(pyproject_file, "rb") as f:
            pyproject = tomli.load(f)
    except Exception as e:
        console.print(f"[red]Error reading pyproject.toml: {e}[/red]")
        raise typer.Exit(1) from e

    project = pyproject.get("project", {})
    package_name = project.get("name", "")
    version = project.get("version")
    description = project.get("description", "")

    if not version:
        console.print("[red]Error: No version in pyproject.toml[/red]")
        raise typer.Exit(1)

    version = maybe_bump_package_version(
        pyproject_file,
        version,
        minor=minor,
        dev=dev,
        dry_run=dry_run,
    )

    # Extract short name (remove common prefixes)
    short_name = package_name
    for prefix in ("plato-agent-", "plato-"):
        if short_name.startswith(prefix):
            short_name = short_name[len(prefix) :]
            break

    # Get API key
    api_key = None
    if not dry_run:
        api_key = require_api_key()

    # Get registry URL (always publish to production registry by default)
    registry_url = os.getenv("PLATO_REGISTRY_BASE_URL", "https://plato.so").rstrip("/")
    if registry_url.endswith("/api"):
        registry_url = registry_url[:-4]
    api_url = f"{registry_url}/api"

    console.print(f"[cyan]Package:[/cyan] {package_name}")
    console.print(f"[cyan]Version:[/cyan] {version}")
    console.print("[cyan]Repository:[/cyan] agents")
    console.print(f"[cyan]Path:[/cyan] {pkg_path}")
    console.print()

    # ========== STEP 1: Build Python package ==========
    console.print("[bold]Step 1: Building Python package...[/bold]")
    try:
        result = subprocess.run(
            ["uv", "build"],
            cwd=pkg_path,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            console.print("[red]Build failed:[/red]")
            console.print(result.stderr)
            raise typer.Exit(1)
        console.print("[green]Build successful[/green]")
    except FileNotFoundError:
        console.print("[red]Error: uv not found. Install with: pip install uv[/red]")
        raise typer.Exit(1) from None

    # Find built wheel
    dist_dir = pkg_path / "dist"
    if not dist_dir.exists():
        console.print("[red]Error: dist/ directory not found after build[/red]")
        raise typer.Exit(1)

    normalized_name = package_name.replace("-", "_")
    wheel_files = list(dist_dir.glob(f"{normalized_name}-{version}-*.whl"))
    if not wheel_files:
        wheel_files = list(dist_dir.glob("*.whl"))
    if not wheel_files:
        console.print(f"[red]Error: No wheel file found in {dist_dir}[/red]")
        raise typer.Exit(1)

    wheel_file = wheel_files[0]
    console.print(f"[cyan]Built:[/cyan] {wheel_file.name}")

    # ========== STEP 2: Publish to PyPI ==========
    console.print()
    console.print("[bold]Step 2: Publishing to PyPI...[/bold]")

    if dry_run:
        console.print("[yellow]Dry run - skipping PyPI upload[/yellow]")
    else:
        upload_url = f"{api_url}/v2/pypi/agents/"
        console.print(f"[cyan]Uploading to {upload_url}...[/cyan]")

        assert api_key is not None
        try:
            result = subprocess.run(
                [
                    "uv",
                    "publish",
                    "--publish-url",
                    upload_url,
                    "--username",
                    "__token__",
                    "--password",
                    api_key,
                    str(wheel_file),
                ],
                capture_output=True,
                text=True,
                check=False,
            )

            if result.returncode == 0:
                console.print("[green]PyPI upload successful![/green]")
            else:
                console.print("[red]PyPI upload failed:[/red]")
                if result.stdout:
                    console.print(result.stdout)
                if result.stderr:
                    console.print(result.stderr)
                raise typer.Exit(1)

        except FileNotFoundError:
            console.print("[red]Error: uv not found[/red]")
            raise typer.Exit(1) from None

    # ========== STEP 3: Build and push Docker image (if Dockerfile exists) ==========
    dockerfile = pkg_path / "Dockerfile"
    if dockerfile.exists():
        console.print()
        if skip_docker:
            console.print("[bold]Step 3: Retagging existing Docker image...[/bold]")
            repository = f"vm/rootfs/plato-agents/{short_name}"
            # Prefer the server-side retag (Chronos uses its own ECS task creds,
            # so the author needs no local AWS access), falling back to local AWS
            # credentials if the endpoint is unavailable. The Chronos call needs
            # an API key, which is absent on dry runs — those go straight to the
            # local fallback.
            retagged = False
            if api_key is not None:
                retagged, retag_err = retag_agent_image_via_chronos(
                    get_chronos_settings().chronos_url, package_name, "latest", version, api_key
                )
                if not retagged:
                    console.print(f"[yellow]Chronos retag failed:[/yellow] {retag_err}")
                    console.print("[dim]Falling back to local AWS credentials...[/dim]")
            if not retagged:
                retagged = retag_image(repository, "latest", version)
            if retagged:
                ecr_image = f"{ECR_REGISTRY}/{repository}:{version}"
                console.print(f"[green]Retagged:[/green] {ecr_image}")
            else:
                console.print("[red]Failed to retag image. Is there an existing :latest?[/red]")
                raise typer.Exit(1)
        else:
            console.print("[bold]Step 3: Building and pushing Docker image...[/bold]")
            # Wait for PyPI index to serve the newly uploaded version
            # before Docker build tries to install it.
            wait_for_pypi_version(short_name, version, repo="agents", api_key=api_key)
            # Pass agent version and PyPI index URLs so the Dockerfile can
            # pre-bake the agent package (skips ~14s install at runtime).
            docker_build_args = {
                "AGENT_VERSION": version,
                "PYPI_AGENTS_URL": plato_token_simple_index("agents", api_key=api_key),
            }
            _publish_agent_image(
                agent_name=short_name,
                version=version,
                build_path=pkg_path,
                description=description,
                dry_run=dry_run,
                build_args=docker_build_args,
                no_cache=no_cache,
            )
    else:
        console.print()
        console.print("[dim]No Dockerfile found - skipping Docker image build[/dim]")

    # ========== Summary ==========
    console.print()
    console.print("[bold green]Agent published successfully![/bold green]")
    console.print()
    console.print("[bold]Install with:[/bold]")
    console.print(f"  uv pip install {package_name} --index-url {api_url}/v2/pypi/agents/simple/")


@agent_app.command(name="images")
def agent_images():
    """List all published agent images for your organization.

    Queries the Plato API to show all agent Docker images that have been published
    to your organization's ECR registry. Requires PLATO_API_KEY.
    """
    import httpx

    api_key = os.getenv("PLATO_API_KEY")
    if not api_key:
        console.print("[red]Error: PLATO_API_KEY not set[/red]")
        raise typer.Exit(1)

    base_url = os.getenv("PLATO_BASE_URL", "https://plato.so").rstrip("/")
    if base_url.endswith("/api"):
        base_url = base_url[:-4]

    with httpx.Client(base_url=f"{base_url}/api", timeout=30.0) as client:
        response = client.get("/v2/agents/", headers={"X-API-Key": api_key})

        if response.status_code != 200:
            console.print(f"[red]Error: {response.status_code}[/red]")
            raise typer.Exit(1)

        data = response.json()

    agents = data.get("agents", [])
    if not agents:
        console.print("[yellow]No published agents found[/yellow]")
        console.print("\n[dim]Publish with: plato agent publish <path-or-name>[/dim]")
        return

    console.print("[bold]Published Agent Images:[/bold]\n")
    for agent in agents:
        console.print(f"  [cyan]{agent['name']:<20}[/cyan] v{agent['version']:<10} {agent.get('description', '')[:40]}")
    console.print(f"\n[dim]Total: {len(agents)} agent(s)[/dim]")


@agent_app.command(name="versions")
def agent_versions(
    agent_name: str = typer.Argument(..., help="Agent name"),
):
    """List all published versions of an agent.

    Shows all available versions of the specified agent in your organization's registry.

    Arguments:
        agent_name: Name of the agent to list versions for
    """
    import httpx

    api_key = os.getenv("PLATO_API_KEY")
    if not api_key:
        console.print("[red]Error: PLATO_API_KEY not set[/red]")
        raise typer.Exit(1)

    base_url = os.getenv("PLATO_BASE_URL", "https://plato.so").rstrip("/")
    if base_url.endswith("/api"):
        base_url = base_url[:-4]

    with httpx.Client(base_url=f"{base_url}/api", timeout=30.0) as client:
        response = client.get(f"/v2/agents/{agent_name}/versions", headers={"X-API-Key": api_key})

        if response.status_code == 404:
            console.print(f"[red]Agent '{agent_name}' not found[/red]")
            raise typer.Exit(1)
        elif response.status_code != 200:
            console.print(f"[red]Error: {response.status_code}[/red]")
            raise typer.Exit(1)

        data = response.json()

    versions = data.get("versions", [])
    if not versions:
        console.print(f"[yellow]No versions found for '{agent_name}'[/yellow]")
        return

    console.print(f"[bold]Versions of {agent_name}:[/bold]\n")
    for v in versions:
        console.print(f"  [cyan]v{v['version']:<12}[/cyan] {v['published_at'][:10]}  {v['artifact_id'][:12]}...")
    console.print(f"\n[dim]Total: {len(versions)} version(s)[/dim]")


@agent_app.command(name="test")
def agent_test(
    path: str = typer.Argument(".", help="Path to the agent directory (default: current directory)"),
    sdk_path: str = typer.Option(
        None, "--sdk-path", "-s", help="Path to local SDK to use instead of published version"
    ),
    image: str = typer.Option(None, "--image", "-i", help="Test an existing image instead of building"),
    expected_sdk_version: str = typer.Option(
        None, "--expected-sdk-version", "-e", help="Expected SDK version (fails if mismatch)"
    ),
):
    """Build and test an agent image to verify it works correctly.

    Builds the image locally and runs verification checks to ensure
    the agent is properly configured and can execute.
    """

    if image:
        test_image = image
        console.print(f"[cyan]Testing existing image:[/cyan] {image}")
    else:
        pkg_path = Path(path).resolve()
        if not pkg_path.exists():
            console.print(f"[red]Error: Path does not exist: {pkg_path}[/red]")
            raise typer.Exit(1)

        dockerfile = pkg_path / "Dockerfile"
        if not dockerfile.exists():
            console.print(f"[red]Error: No Dockerfile found at {pkg_path}[/red]")
            raise typer.Exit(1)

        # Get package name from pyproject.toml
        pyproject_file = pkg_path / "pyproject.toml"
        if pyproject_file.exists():
            try:
                import tomli

                with open(pyproject_file, "rb") as f:
                    pyproject = tomli.load(f)
                package_name = pyproject.get("project", {}).get("name", pkg_path.name)
            except ImportError:
                package_name = pkg_path.name
        else:
            package_name = pkg_path.name

        test_image = f"{package_name}:test"
        build_path = pkg_path
        temp_dir = None

        try:
            if sdk_path:
                sdk_path_resolved = Path(sdk_path).resolve()
                if not sdk_path_resolved.exists():
                    console.print(f"[red]Error: SDK path does not exist: {sdk_path}[/red]")
                    raise typer.Exit(1)

                temp_dir = prepare_build_context_with_sdk(pkg_path, sdk_path_resolved)
                if not temp_dir:
                    console.print("[red]Failed to prepare build context with SDK[/red]")
                    raise typer.Exit(1)
                build_path = temp_dir

            console.print(f"[cyan]Building test image:[/cyan] {test_image}")

            # Check for multi-stage build
            dockerfile_content = (build_path / "Dockerfile").read_text()
            build_cmd = ["docker", "build", "-t", test_image]
            if "AS prod" in dockerfile_content:
                build_cmd.extend(["--target", "prod"])
            build_cmd.append(str(build_path))

            result = subprocess.run(build_cmd)
            if result.returncode != 0:
                console.print("[red]Build failed[/red]")
                raise typer.Exit(1)

        finally:
            if temp_dir and temp_dir.exists():
                shutil.rmtree(temp_dir, ignore_errors=True)

    # Get expected SDK version
    expected_version = expected_sdk_version
    if sdk_path and not expected_version:
        sdk_path_resolved = Path(sdk_path).resolve()
        try:
            import tomli

            with open(sdk_path_resolved / "pyproject.toml", "rb") as f:
                sdk_pyproject = tomli.load(f)
            expected_version = sdk_pyproject.get("project", {}).get("version")
            console.print(f"[cyan]Expected SDK version (from --sdk-path):[/cyan] {expected_version}")
        except Exception as e:
            console.print(f"[yellow]Warning: Could not read local SDK version: {e}[/yellow]")
    elif expected_version:
        console.print(f"[cyan]Expected SDK version:[/cyan] {expected_version}")

    # Run verification checks
    console.print("\n[cyan]Running verification checks...[/cyan]\n")

    checks_passed = 0
    checks_failed = 0

    # Check 1: SDK version
    console.print("[bold]1. SDK Version[/bold]")
    result = subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--entrypoint",
            "python3",
            test_image,
            "-c",
            "import plato; print(plato.__version__)",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        image_sdk_version = result.stdout.strip()
        if expected_version and image_sdk_version != expected_version:
            console.print("   [red]✗[/red] VERSION MISMATCH!")
            console.print(f"      Expected:  {expected_version}")
            console.print(f"      Image SDK: {image_sdk_version}")
            checks_failed += 1
        else:
            console.print(f"   [green]✓[/green] plato-sdk-v2 version: {image_sdk_version}")
            if expected_version:
                console.print("      (matches expected)")
            checks_passed += 1
    else:
        console.print(f"   [red]✗[/red] Failed to get SDK version: {result.stderr}")
        checks_failed += 1

    # Check 2: Agent entrypoint
    console.print("[bold]2. Agent Entrypoint[/bold]")
    result = subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--entrypoint",
            "python3",
            test_image,
            "-c",
            "from plato.agents.base import BaseAgent; print('BaseAgent importable')",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        console.print("   [green]✓[/green] BaseAgent importable")
        checks_passed += 1
    else:
        console.print(f"   [red]✗[/red] Failed to import BaseAgent: {result.stderr}")
        checks_failed += 1

    # Check 3: Agent discovery via entry points
    console.print("[bold]3. Agent Entry Points[/bold]")
    result = subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--entrypoint",
            "python3",
            test_image,
            "-c",
            """
import importlib.metadata
eps = importlib.metadata.entry_points(group='plato.agents')
for ep in eps:
    print(f"  {ep.name}: {ep.value}")
if not eps:
    print("  (no agents found)")
""",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        output = result.stdout.strip()
        if "(no agents found)" in output:
            console.print("   [yellow]![/yellow] No plato.agents entry points found")
            console.print("      [dim]Add entry point in pyproject.toml:[/dim]")
            console.print('      [dim][project.entry-points."plato.agents"][/dim]')
            console.print('      [dim]agent-name = "module:AgentClass"[/dim]')
        else:
            console.print("   [green]✓[/green] Found entry points:")
            for line in output.split("\n"):
                if line.strip():
                    console.print(f"      {line.strip()}")
        checks_passed += 1
    else:
        console.print(f"   [red]✗[/red] Failed to check entry points: {result.stderr}")
        checks_failed += 1

    # Check 4: Test agent instantiation
    console.print("[bold]4. Agent Instantiation[/bold]")
    result = subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--entrypoint",
            "python3",
            test_image,
            "-c",
            """
import importlib.metadata
eps = list(importlib.metadata.entry_points(group='plato.agents'))
if eps:
    ep = eps[0]
    agent_cls = ep.load()
    print(f"Loaded: {agent_cls.__name__}")
    # Try to get schema
    if hasattr(agent_cls, 'get_schema'):
        schema = agent_cls.get_schema()
        print(f"Schema keys: {list(schema.keys()) if schema else 'None'}")
else:
    print("No agents to test")
""",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0:
        console.print("   [green]✓[/green] Agent class loadable")
        for line in result.stdout.strip().split("\n"):
            if line.strip():
                console.print(f"      [dim]{line.strip()}[/dim]")
        checks_passed += 1
    else:
        console.print(f"   [red]✗[/red] Failed to instantiate agent: {result.stderr}")
        checks_failed += 1

    # Check 5: VM runtime support (REQUIRED for VM mode)
    console.print("[bold]5. VM Runtime Support[/bold]")
    result = subprocess.run(
        [
            "docker",
            "run",
            "--rm",
            "--entrypoint",
            "python3",
            test_image,
            "-c",
            """
try:
    from plato.runtimes.vm import VMRuntime
    print('OK')
except ImportError as e:
    print(f'IMPORT_ERROR: {e}')
except Exception as e:
    print(f'ERROR: {e}')
""",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode == 0 and "OK" in result.stdout:
        console.print("   [green]✓[/green] VMRuntime importable")
        checks_passed += 1
    else:
        error_line = [line for line in result.stdout.split("\n") if "ERROR" in line]
        if error_line:
            console.print("   [red]✗[/red] VMRuntime not available - SDK too old!")
            console.print(f"      {error_line[0]}")
            console.print("      [dim]Rebuild with --sdk-path pointing to newer SDK[/dim]")
        else:
            console.print("   [red]✗[/red] VMRuntime not available")
        checks_failed += 1

    # Summary
    console.print()
    if checks_failed == 0:
        console.print(f"[green]All {checks_passed} checks passed![/green]")
    else:
        console.print(f"[red]{checks_failed} check(s) failed, {checks_passed} passed[/red]")
        raise typer.Exit(1)


@agent_app.command(name="deploy")
def agent_deploy(
    path: str = typer.Argument(".", help="Path to the agent package directory (default: current directory)"),
):
    """Deploy a Chronos agent package to AWS CodeArtifact.

    Builds the Python package, discovers @ai agents from the codebase, and uploads
    to CodeArtifact via the Plato API for use in Chronos jobs.

    Arguments:
        path: Path to the agent package directory with pyproject.toml (default: current directory)

    Requires PLATO_API_KEY environment variable.
    """
    try:
        import tomli
    except ImportError:
        console.print("[red]❌ tomli is not installed[/red]")
        console.print("\n[yellow]Install with:[/yellow]")
        console.print("  pip install tomli")
        raise typer.Exit(1) from None

    api_key = require_api_key()
    # Get base URL (default to production)
    base_url = os.getenv("PLATO_BASE_URL", "https://plato.so")
    # Normalize: remove trailing slash and /api if present
    base_url = base_url.rstrip("/")
    if base_url.endswith("/api"):
        base_url = base_url[:-4]
    api_url = f"{base_url}/api"

    # Resolve package path
    pkg_path = Path(path).resolve()
    if not pkg_path.exists():
        console.print(f"[red]❌ Path does not exist: {pkg_path}[/red]")
        raise typer.Exit(1)

    # Load pyproject.toml
    pyproject_file = pkg_path / "pyproject.toml"
    if not pyproject_file.exists():
        console.print(f"[red]❌ No pyproject.toml found at {pkg_path}[/red]")
        raise typer.Exit(1)

    try:
        with open(pyproject_file, "rb") as f:
            pyproject = tomli.load(f)
    except Exception as e:
        console.print(f"[red]❌ Error reading pyproject.toml: {e}[/red]")
        raise typer.Exit(1) from e

    # Extract package info
    project = pyproject.get("project", {})
    package_name = project.get("name")
    version = project.get("version")
    description = project.get("description", "")

    if not package_name:
        console.print("[red]❌ No package name in pyproject.toml[/red]")
        raise typer.Exit(1)
    if not version:
        console.print("[red]❌ No version in pyproject.toml[/red]")
        raise typer.Exit(1)

    # Validate semantic version format
    if not re.match(r"^\d+\.\d+\.\d+$", version):
        console.print(f"[red]❌ Invalid version format: {version}[/red]")
        console.print("[yellow]Version must be semantic (X.Y.Z)[/yellow]")
        raise typer.Exit(1)

    console.print(f"[cyan]Package:[/cyan] {package_name}")
    console.print(f"[cyan]Version:[/cyan] {version}")
    console.print(f"[cyan]Path:[/cyan] {pkg_path}")
    console.print()

    # Build package
    console.print("[cyan]Building package...[/cyan]")
    try:
        result = subprocess.run(
            ["uv", "build"],
            cwd=pkg_path,
            capture_output=True,
            text=True,
            check=True,
        )
        console.print("[green]✅ Build successful[/green]")
    except subprocess.CalledProcessError as e:
        console.print("[red]❌ Build failed:[/red]")
        console.print(e.stderr)
        raise typer.Exit(1) from e

    # Find built files
    dist_dir = pkg_path / "dist"
    if not dist_dir.exists():
        console.print("[red]❌ dist/ directory not found after build[/red]")
        raise typer.Exit(1)

    # Python normalizes package names: dashes become underscores in filenames
    normalized_name = package_name.replace("-", "_")
    wheel_files = list(dist_dir.glob(f"{normalized_name}-{version}-*.whl"))
    sdist_files = list(dist_dir.glob(f"{normalized_name}-{version}.tar.gz"))

    if not wheel_files:
        console.print(f"[red]❌ No wheel file found in {dist_dir}[/red]")
        raise typer.Exit(1)
    if not sdist_files:
        console.print(f"[red]❌ No sdist file found in {dist_dir}[/red]")
        raise typer.Exit(1)

    wheel_file = wheel_files[0]
    sdist_file = sdist_files[0]

    console.print(f"[cyan]Wheel:[/cyan] {wheel_file.name}")
    console.print(f"[cyan]Sdist:[/cyan] {sdist_file.name}")
    console.print()

    # Upload to Plato API using generated routes
    console.print("[cyan]Uploading to Plato API...[/cyan]")
    try:
        import httpx

        from plato._generated.errors import raise_for_status
        from plato._generated.models import UploadPackageResponse

        with httpx.Client(base_url=api_url, timeout=120.0) as client:
            with open(wheel_file, "rb") as whl, open(sdist_file, "rb") as sdist:
                response = client.post(
                    "/v2/chronos-packages/upload",
                    headers={"X-API-Key": api_key},
                    data={
                        "package_name": package_name,
                        "version": version,
                        "alias": package_name,
                        "description": description,
                        "agents": json.dumps([]),  # Server will discover agents from package
                    },
                    files={
                        "wheel_file": (
                            wheel_file.name,
                            whl,
                            "application/octet-stream",
                        ),
                        "sdist_file": (
                            sdist_file.name,
                            sdist,
                            "application/octet-stream",
                        ),
                    },
                )

            # Use generated error handling
            try:
                raise_for_status(response)
                result = UploadPackageResponse.model_validate(response.json())

                console.print("[green]✅ Deployment successful![/green]")
                console.print()
                console.print(f"[cyan]Package:[/cyan] {result.package_name} v{result.version}")
                console.print(f"[cyan]Artifact ID:[/cyan] {result.artifact_id}")
                console.print()
                console.print(f"[dim]{result.message}[/dim]")
                console.print()
                console.print("[bold]Install with:[/bold]")
                console.print(f"  uv add {package_name}")

            except httpx.HTTPStatusError as e:
                # Handle specific status codes
                if e.response.status_code == 401:
                    console.print("[red]❌ Authentication failed[/red]")
                    console.print("[yellow]Check your PLATO_API_KEY[/yellow]")
                elif e.response.status_code == 403:
                    try:
                        detail = e.response.json().get("detail", "Package name conflict")
                    except Exception:
                        detail = e.response.text
                    console.print(f"[red]❌ Forbidden: {detail}[/red]")
                    console.print("[yellow]This package name is owned by another organization[/yellow]")
                elif e.response.status_code == 409:
                    try:
                        detail = e.response.json().get("detail", "Version conflict")
                    except Exception:
                        detail = e.response.text
                    console.print(f"[red]❌ Version conflict: {detail}[/red]")
                    console.print("[yellow]Bump the version in pyproject.toml[/yellow]")
                else:
                    try:
                        detail = e.response.json().get("detail", e.response.text)
                    except Exception:
                        detail = e.response.text
                    console.print(f"[red]❌ Upload failed ({e.response.status_code}): {detail}[/red]")
                raise typer.Exit(1) from e

    except httpx.HTTPError as e:
        console.print(f"[red]❌ Network error: {e}[/red]")
        raise typer.Exit(1) from e
    except Exception as e:
        console.print(f"[red]❌ Upload error: {e}[/red]")
        raise typer.Exit(1) from e
