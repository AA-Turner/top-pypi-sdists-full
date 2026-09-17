"""World CLI commands for Plato."""

import json
import subprocess
import zipfile
from pathlib import Path

import typer

from plato.cli.publish_flow import WORLD, find_wheel, publish_image_then_wheel, registry_api_url
from plato.cli.utils import console, maybe_bump_package_version, require_api_key

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


def _update_config_package_version(
    config_path: Path,
    package_name: str,
    new_version: str,
) -> None:
    """Rewrite world.package in a config JSON to <package_name>:<new_version>.

    Warns and skips if the config is missing, malformed, lacks world.package,
    or its package name doesn't match.
    """
    try:
        with open(config_path) as f:
            config = json.load(f)
    except FileNotFoundError:
        console.print(f"[yellow]Warning: Config not found, skipping: {config_path}[/yellow]")
        return
    except json.JSONDecodeError as e:
        console.print(f"[yellow]Warning: Invalid JSON in {config_path}, skipping: {e}[/yellow]")
        return

    world = config.get("world")
    if not isinstance(world, dict) or "package" not in world:
        console.print(f"[yellow]Warning: No world.package in {config_path}, skipping[/yellow]")
        return

    current = world["package"]
    current_name = current.split(":", 1)[0] if isinstance(current, str) else ""
    if current_name != package_name:
        console.print(
            f"[yellow]Warning: {config_path} has world.package='{current}' "
            f"(name '{current_name}' != '{package_name}'), skipping[/yellow]"
        )
        return

    new_package = f"{package_name}:{new_version}"
    world["package"] = new_package

    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
        f.write("\n")

    console.print(f"[green]Updated config:[/green] {config_path} -> world.package = {new_package}")


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
    skip_docker: bool = typer.Option(
        False,
        "--skip-docker",
        help="Skip Docker build; retag the image of the version being bumped from (falling back to :latest) "
        "as the new version tag instead",
    ),
    no_skip_docker: bool = typer.Option(
        False,
        "--no-skip-docker",
        help="Force Docker rebuild even with --dev (overrides the default skip behavior). "
        "A dev rebuild pushes and prefetches :<version> only; :latest moves only on a release publish",
    ),
    wheel_only: bool = typer.Option(
        False,
        "--wheel-only",
        help="Upload only the wheel; the image :<version> must already be in ECR. For re-running a publish whose image step succeeded but whose upload failed",
    ),
    update_config: list[str] = typer.Option(
        None,
        "--update-config",
        help="Path to a config JSON whose 'world.package' version should be updated to "
        "match the published version. For --dev/--minor uses the bumped version; for a "
        "release publish pins to ':latest'. Pass multiple times to update multiple configs.",
    ),
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
    if wheel_only and (skip_docker or no_skip_docker):
        console.print("[red]--wheel-only cannot be combined with --skip-docker / --no-skip-docker[/red]")
        raise typer.Exit(1)

    # --dev implies --skip-docker unless --no-skip-docker is explicitly passed
    if dev and not skip_docker and not no_skip_docker and not wheel_only:
        skip_docker = True
        console.print(
            "[dim]--dev implies --skip-docker (retag instead of rebuild). Use --no-skip-docker to force a rebuild.[/dim]"
        )

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

    api_url = registry_api_url()

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

    previous_version = version
    if wheel_only:
        # The re-run after a failed upload: the image step already ran for the
        # version in pyproject.toml, so publish exactly that version. Bumping
        # (a fresh dated dev version, or the release prompt defaulting to yes)
        # would point the wheel at an image tag that was never pushed.
        console.print(f"[dim]--wheel-only: keeping version {version} (no bump)[/dim]")
    else:
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

    # Build package. We use --no-build-isolation against the world's own
    # .venv so the hatch schema hook can import world.py with all runtime
    # deps available (fastmcp, opentelemetry, etc. for worlds that need
    # them). Otherwise hatchling's isolated build env installs only
    # [build-system.requires], the world module import fails, and we ship
    # a wheel with stale or missing schema.json.
    console.print("[cyan]Syncing world venv...[/cyan]")
    try:
        for cmd in (
            ["uv", "sync", "--no-dev", "--quiet"],
            # Hatchling isn't a runtime dep so uv sync doesn't pull it;
            # install it explicitly into the world's venv for the build.
            ["uv", "pip", "install", "--quiet", "hatchling"],
        ):
            result = subprocess.run(cmd, cwd=pkg_path, capture_output=True, text=True)
            if result.returncode != 0:
                console.print(f"[red]Command failed ({' '.join(cmd)}):[/red]")
                console.print(result.stderr)
                raise typer.Exit(1)

        console.print("[cyan]Building package...[/cyan]")
        result = subprocess.run(
            ["uv", "build", "--no-build-isolation"],
            cwd=pkg_path,
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            console.print("[red]Build failed:[/red]")
            console.print(result.stderr)
            raise typer.Exit(1)
        if result.stdout:
            # Surface the hook's "Generated schema.json..." line.
            console.print(result.stdout.strip())
        console.print("[green]Build successful[/green]")
    except FileNotFoundError:
        console.print("[red]Error: uv not found. Install with: pip install uv[/red]")
        raise typer.Exit(1) from None

    wheel_file = find_wheel(pkg_path, package_name, version)
    console.print(f"[cyan]Built:[/cyan] {wheel_file.name}")

    # Extract schema from wheel
    module_name = _get_module_name(pkg_path, package_name)
    schema_data = _extract_schema_from_wheel(wheel_file, module_name)
    if schema_data:
        # Handle catalog format: {"worlds": {"name": {...}}}
        if "worlds" in schema_data and isinstance(schema_data["worlds"], dict):
            for wname, wschema in schema_data["worlds"].items():
                props = wschema.get("config_schema", {}).get("properties", {})
                w_agents = wschema.get("agents", [])
                w_secrets = (
                    wschema.get("secrets_schema", {}).get("properties", {}) if wschema.get("secrets_schema") else {}
                )
                w_image = wschema.get("image")
                w_type = wschema.get("type", "world")
                console.print(
                    f"[green]Schema found:[/green] {wname} ({w_type}) — {len(props)} properties, {len(w_agents)} agents, {len(w_secrets)} secrets"
                )
                if w_image:
                    console.print(f"  [green]Image:[/green] {w_image}")
        else:
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

    if dry_run and schema_data:
        console.print("\n[bold]Schema:[/bold]")
        console.print(json.dumps(schema_data, indent=2))

    # Image first (retag, or push -> prefetch -> promote), wheel last: the
    # wheel is what makes the version launchable. See plato.cli.publish_flow.
    publish_image_then_wheel(
        WORLD,
        package_name=package_name,
        previous_version=previous_version,
        version=version,
        pkg_path=pkg_path,
        wheel_file=wheel_file,
        api_key=api_key,
        dry_run=dry_run,
        skip_docker=skip_docker,
        # A dev rebuild never moves :latest — it is prod's tag and a laptop
        # iteration has no business moving it. The dev image is launchable
        # by its pinned version (schema.json bakes :<version>).
        promote_latest=not dev,
        wheel_only=wheel_only,
    )

    if update_config:
        console.print()
        if dry_run:
            console.print("[yellow]Dry run - skipping --update-config rewrites (version was not bumped):[/yellow]")
            for cfg_path in update_config:
                console.print(f"  {Path(cfg_path).resolve()}")
        else:
            target_version = version if (dev or minor) else "latest"
            for cfg_path in update_config:
                _update_config_package_version(Path(cfg_path).resolve(), package_name, target_version)

    console.print("\n[bold]Install with:[/bold]")
    console.print(f"  uv pip install {package_name} --index-url {api_url}/v2/pypi/worlds/simple/")
