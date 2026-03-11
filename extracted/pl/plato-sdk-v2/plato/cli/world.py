"""World CLI commands for Plato."""

import json
import os
import shutil
import subprocess
import zipfile
from pathlib import Path

import typer

from plato.cli.utils import console, maybe_bump_package_version, require_api_key
from plato.utils.ecr import ECR_REGISTRY, get_image_digest, publish_docker_image

world_app = typer.Typer(help="Manage and deploy worlds")


def _get_module_name(pkg_path: Path, package_name: str) -> str:
    """Get the actual importable module name from pyproject.toml or package name."""
    try:
        import tomli

        pyproject_file = pkg_path / "pyproject.toml"
        if pyproject_file.exists():
            with open(pyproject_file, "rb") as f:
                pyproject = tomli.load(f)

            # Check hatch config for packages
            packages = (
                pyproject.get("tool", {})
                .get("hatch", {})
                .get("build", {})
                .get("targets", {})
                .get("wheel", {})
                .get("packages", [])
            )
            if packages:
                module_path = packages[0]
                return module_path.split("/")[-1]

            # Check setuptools config
            packages = pyproject.get("tool", {}).get("setuptools", {}).get("packages", [])
            if packages:
                return packages[0]
    except Exception:
        pass

    return package_name.replace("-", "_")


def _prefetch_world_image(image_url: str, world_name: str) -> None:
    """Start a VM to prefetch and cache the world rootfs image."""
    console.print("[cyan]Starting VM to prefetch image...[/cyan]")

    try:
        from plato.v2 import Env, Plato
        from plato.v2.types import SimConfigCompute

        plato = Plato()
        env = Env.resource(
            simulator=f"prefetch-{world_name}",
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


def _extract_schema_from_wheel(wheel_path: Path, module_name: str) -> dict | None:
    """Extract schema.json from a built wheel file."""
    try:
        with zipfile.ZipFile(wheel_path, "r") as zf:
            schema_path = f"{module_name}/schema.json"
            if schema_path in zf.namelist():
                with zf.open(schema_path) as f:
                    return json.load(f)
    except Exception as e:
        console.print(f"[yellow]Warning: Could not read schema from wheel: {e}[/yellow]")
    return None


@world_app.command(name="publish")
def world_publish(
    path: str = typer.Argument(".", help="Path to the world package directory"),
    minor: bool = typer.Option(False, "--minor", help="Bump the minor version before publishing"),
    dev: bool = typer.Option(
        False,
        "--dev",
        help="Publish the next dated PEP 440 dev version without prompting",
    ),
    dry_run: bool = typer.Option(False, "--dry-run", help="Build without uploading"),
):
    """Build and publish a world package to the Plato worlds repository.

    Builds with 'uv build', extracts schema.json from the wheel, and uploads
    to the Plato PyPI repository via uv publish.

    The world package will be installable via:
        uv pip install <package> --index-url https://plato.so/api/v2/pypi/worlds/simple/

    Arguments:
        path: Path to the world package directory containing pyproject.toml

    Requires PLATO_API_KEY environment variable for upload.
    """
    try:
        import tomli
    except ImportError:
        console.print("[red]Error: tomli is not installed[/red]")
        console.print("\n[yellow]Install with:[/yellow]")
        console.print("  pip install tomli")
        raise typer.Exit(1) from None

    # Get API key
    api_key = None
    if not dry_run:
        api_key = require_api_key()

    # Get base URL
    # Get registry URL (always publish to production registry by default)
    registry_url = os.getenv("PLATO_REGISTRY_BASE_URL", "https://plato.so").rstrip("/")
    if registry_url.endswith("/api"):
        registry_url = registry_url[:-4]
    api_url = f"{registry_url}/api"

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

    version = maybe_bump_package_version(
        pyproject_file,
        version,
        minor=minor,
        dev=dev,
        dry_run=dry_run,
    )

    console.print(f"[cyan]Package:[/cyan] {package_name}")
    console.print(f"[cyan]Version:[/cyan] {version}")
    console.print("[cyan]Repository:[/cyan] worlds")
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
        wheel_files = list(dist_dir.glob("*.whl"))
    if not wheel_files:
        console.print(f"[red]Error: No wheel file found in {dist_dir}[/red]")
        raise typer.Exit(1)

    wheel_file = wheel_files[0]
    console.print(f"[cyan]Built:[/cyan] {wheel_file.name}")

    # Extract schema from wheel
    module_name = _get_module_name(pkg_path, package_name)
    schema_data = _extract_schema_from_wheel(wheel_file, module_name)
    if schema_data:
        props = schema_data.get("properties", {})
        agents = schema_data.get("agents", [])
        secrets = schema_data.get("secrets", [])
        image = schema_data.get("image")
        console.print(
            f"[green]Schema found:[/green] {len(props)} properties, {len(agents)} agents, {len(secrets)} secrets"
        )
        if image:
            console.print(f"[green]Base image:[/green] {image}")
    else:
        console.print("[red]Error: No schema.json found in wheel.[/red]")
        console.print("[red]Add a hatch build hook to generate it:[/red]")
        console.print("  1. Create hatch_build.py with: from plato.worlds.build_hook import WorldSchemaHook")
        console.print('  2. Add [tool.hatch.build.hooks.custom] path = "hatch_build.py" to pyproject.toml')
        raise typer.Exit(1)

    # ========== PyPI Upload ==========
    if dry_run:
        console.print("\n[yellow]Dry run - skipping PyPI upload[/yellow]")
        if schema_data:
            console.print("\n[bold]Schema:[/bold]")
            console.print(json.dumps(schema_data, indent=2))
    else:
        upload_url = f"{api_url}/v2/pypi/worlds/"
        console.print(f"\n[cyan]Uploading to {upload_url}...[/cyan]")

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
                console.print("[green]Upload successful![/green]")
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

    # ========== Docker Image Publishing (if Dockerfile exists) ==========
    dockerfile = pkg_path / "Dockerfile"
    if dockerfile.exists():
        console.print()

        # Check Docker is available
        if not shutil.which("docker"):
            console.print("[red]Error: docker not found[/red]")
            raise typer.Exit(1)

        # Extract short name (remove common prefixes)
        short_name = package_name
        for prefix in ("plato-world-", "plato-"):
            if short_name.startswith(prefix):
                short_name = short_name[len(prefix) :]
                break

        repository = f"vm/rootfs/plato-worlds/{short_name}"
        latest_image = f"{ECR_REGISTRY}/{repository}:latest"

        if dry_run:
            ecr_image = f"{ECR_REGISTRY}/{repository}:{version}"
            console.print("[yellow]Dry run - would build and push Docker image:[/yellow]")
            console.print(f"  {ecr_image}")
            console.print(f"  {latest_image}")
        else:
            # Get current :latest digest before pushing (to detect changes)
            old_digest = get_image_digest(repository, "latest")

            console.print("[cyan]Building and pushing Docker image...[/cyan]")
            result = publish_docker_image(
                name=short_name,
                version=version,
                build_path=str(pkg_path),
                repo_prefix="vm/rootfs/plato-worlds",
            )

            if not result.success:
                console.print(f"[red]{result.error}[/red]")
                raise typer.Exit(1)

            console.print(f"[green]Published:[/green] {result.ecr_image}")
            console.print(f"[green]Published:[/green] {result.latest_image}")

            # Prefetch if the Docker image digest changed
            new_digest = get_image_digest(repository, "latest")
            if new_digest != old_digest:
                console.print()
                console.print("[bold]Prefetching image (digest changed)...[/bold]")
                _prefetch_world_image(latest_image, short_name)
            else:
                console.print("\n[dim]Docker image digest unchanged - skipping prefetch[/dim]")
    else:
        console.print("\n[dim]No Dockerfile found - skipping Docker image build[/dim]")

    console.print("\n[bold]Install with:[/bold]")
    console.print(f"  uv pip install {package_name} --index-url {api_url}/v2/pypi/worlds/simple/")
