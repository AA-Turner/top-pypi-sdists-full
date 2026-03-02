"""World CLI commands for Plato."""

import json
import os
import subprocess
import zipfile
from pathlib import Path

import typer

from plato.v1.cli.utils import console, require_api_key

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
                # Extract module name from path like "src/code_world"
                module_path = packages[0]
                return module_path.split("/")[-1]

            # Check setuptools config
            packages = pyproject.get("tool", {}).get("setuptools", {}).get("packages", [])
            if packages:
                return packages[0]
    except Exception:
        pass

    # Fall back to normalized package name
    return package_name.replace("-", "_")


def _extract_schema_from_wheel(wheel_path: Path, module_name: str) -> dict | None:
    """Extract schema.json from a built wheel file."""
    try:
        with zipfile.ZipFile(wheel_path, "r") as zf:
            # Look for schema.json in the module directory
            schema_path = f"{module_name}/schema.json"
            if schema_path in zf.namelist():
                with zf.open(schema_path) as f:
                    return json.load(f)
    except Exception as e:
        console.print(f"[yellow]Warning: Could not read schema from wheel: {e}[/yellow]")
    return None


@world_app.command(name="publish")
def world_publish(
    path: str = typer.Argument(".", help="Path to the world package directory (default: current directory)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Build without uploading"),
):
    """Build and publish a world package to the Plato worlds repository.

    Reads pyproject.toml for package info, builds with 'uv build', extracts the
    config schema from schema.json in the wheel, and uploads to the Plato worlds
    repository via uv publish.

    The schema.json is automatically generated during build by a hatch build hook
    that calls the world's get_schema() method.

    Arguments:
        path: Path to the world package directory containing pyproject.toml
            (default: current directory)

    Options:
        --dry-run: Build the package and show schema without uploading

    Requires PLATO_API_KEY environment variable for upload.
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
    console.print("[cyan]Repository:[/cyan] worlds")
    console.print(f"[cyan]Path:[/cyan] {pkg_path}")
    console.print()

    # Build package (this will trigger the schema generation hook)
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

    # Extract schema from the wheel
    module_name = _get_module_name(pkg_path, package_name)
    schema_data = _extract_schema_from_wheel(wheel_file, module_name)
    if schema_data:
        props = schema_data.get("properties", {})
        agents = schema_data.get("agents", [])
        secrets = schema_data.get("secrets", [])
        console.print(
            f"[green]Schema found:[/green] {len(props)} properties, {len(agents)} agents, {len(secrets)} secrets"
        )
        console.print(f"[dim]  Properties: {', '.join(props.keys()) if props else 'none'}[/dim]")
        if agents:
            console.print(f"[dim]  Agents: {', '.join(a.get('name', '?') for a in agents)}[/dim]")
    else:
        console.print("[red]Error: No schema.json found in wheel[/red]")
        console.print("[dim]  Add a hatch build hook to generate schema.json from get_schema()[/dim]")
        console.print("[dim]  See: https://docs.plato.so/worlds/publishing#schema-generation[/dim]")
        raise SystemExit(1)

    if dry_run:
        console.print("\n[yellow]Dry run - skipping upload[/yellow]")
        if schema_data:
            console.print("\n[bold]Schema:[/bold]")
            console.print(json.dumps(schema_data, indent=2))
        return

    # Upload wheel using uv publish
    upload_url = f"{api_url}/v2/pypi/worlds/"
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

    console.print("\n[bold]Install with:[/bold]")
    console.print(f"  uv add {package_name} --index-url {api_url}/v2/pypi/worlds/simple/")
