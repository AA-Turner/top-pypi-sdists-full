"""World CLI commands for Plato."""

import json
import os
import shutil
import subprocess
import zipfile
from pathlib import Path

import typer

from plato.cli.chronos.settings import get_settings as get_chronos_settings
from plato.cli.utils import console, maybe_bump_package_version, require_api_key, wait_for_pypi_version
from plato.utils.ecr import (
    ECR_REGISTRY,
    get_image_digest,
    publish_docker_image,
    retag_image,
    retag_image_via_chronos,
)

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


# Cold-image boot = docker pull + rootfs conversion + snapshot-store ingest,
# which is the 10+ minute path this prefetch exists to absorb, so the client
# polls wait_for_ready for up to 30 minutes (a timeout here blocks promotion
# to :latest). The VM lifetime sent in the /make body must cover that same
# window: the backend stamps job_start_time when the job is matched to a VM
# slot — before the rootfs build — and the VM agent force-shuts the VM once
# job_max_timeout elapses (plato: node_provider match callback +
# vm_lifecycle.check_job_timeout), so a short lifetime would kill a slow
# ingest mid-flight. The VM is closed the moment it is ready and the worker
# heartbeat timeout (300s) reaps it if this CLI dies, so the long lifetime
# never actually keeps a VM alive.
_PREFETCH_TIMEOUT_S = 1800


def _prefetch_world_image(image_url: str, world_name: str) -> bool:
    """Boot one throwaway VM from ``image_url`` so its rootfs lands in the snapshot store.

    Returns True only if the VM actually came up. This is the gate for promoting
    the image to ``:latest``: a digest that has never booted must not become the
    tag every launch resolves.
    """
    console.print(f"[cyan]Starting VM to prefetch {image_url}...[/cyan]")

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
            timeout=_PREFETCH_TIMEOUT_S,
            ready_timeout=_PREFETCH_TIMEOUT_S,
            connect_network=False,
        )
        console.print("[green]Prefetch complete - rootfs cached[/green]")
        session.close()
        plato.close()
        return True
    except Exception as e:
        console.print(f"[red]Prefetch failed: {e}[/red]")
        return False


def _retag_world_image(
    package_name: str, repository: str, source_tag: str, target_tag: str, api_key: str | None
) -> bool:
    """Copy ``source_tag`` -> ``target_tag`` in the world's ECR repo (manifest copy, same digest).

    Prefers the Chronos retag endpoint (server-side creds); falls back to local
    AWS credentials so an author without the endpoint deployed isn't stranded.
    """
    retagged = False
    if api_key is not None:
        retagged, retag_err = retag_image_via_chronos(
            get_chronos_settings().chronos_url, package_name, source_tag, target_tag, api_key
        )
        if not retagged:
            # TODO: remove this local-AWS fallback once the Chronos retag
            # endpoint (POST /api/worlds/{package_name}/retag-image) is
            # deployed everywhere.
            console.print(
                f"[dim]Chronos retag :{source_tag} -> :{target_tag} failed ({retag_err}); trying local AWS[/dim]"
            )
    if not retagged:
        retagged = retag_image(repository, source_tag, target_tag)
    return retagged


def _retag_source_tags(previous_version: str, version: str) -> list[str]:
    """Image tags a --skip-docker publish tries, in order, as the source for :<version>.

    The version being bumped from comes first: it is the last thing this
    checkout published, so a ``--dev --no-skip-docker`` rebuild (which never
    moves :latest) chains forward into the python-only dev publishes that
    follow it, and a fresh checkout starts from its release tag. :latest is the
    fallback — it is also the only candidate when the version was bumped
    externally (CI's version-bump.sh) so previous == new.
    """
    tags = []
    if previous_version and previous_version != version:
        tags.append(previous_version)
    tags.append("latest")
    return tags


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
    # --dev implies --skip-docker unless --no-skip-docker is explicitly passed
    if dev and not skip_docker and not no_skip_docker:
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

    previous_version = version
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

        # Extract short name (remove common prefixes)
        short_name = package_name
        for prefix in ("plato-world-", "plato-"):
            if short_name.startswith(prefix):
                short_name = short_name[len(prefix) :]
                break

        repository = f"vm/rootfs/plato-worlds/{short_name}"
        latest_image = f"{ECR_REGISTRY}/{repository}:latest"

        version_image = f"{ECR_REGISTRY}/{repository}:{version}"

        # A dev rebuild never moves :latest — it is prod's tag and a laptop
        # iteration has no business moving it. The dev image is launchable
        # by its pinned version (schema.json bakes :<version>), and the next
        # --dev --skip-docker publish chains from it via _retag_source_tags.
        promote_latest = not dev

        if dry_run:
            console.print("[yellow]Dry run - would build and push Docker image:[/yellow]")
            console.print(f"  {version_image}")
            if promote_latest:
                console.print(f"  then prefetch it and promote it to {latest_image}")
            else:
                console.print("  then prefetch it (dev publish: :latest is not moved)")
        elif skip_docker:
            assert api_key is not None
            source_tags = _retag_source_tags(previous_version, version)
            for source_tag in source_tags:
                console.print(f"[cyan]Retagging :{source_tag} as :{version}...[/cyan]")
                if _retag_world_image(package_name, repository, source_tag, version, api_key):
                    console.print(f"[green]Retagged:[/green] {version_image} (from :{source_tag})")
                    break
            else:
                console.print(
                    f"[red]Failed to retag image from any of {source_tags}. Is there an existing :latest?[/red]"
                )
                raise typer.Exit(1)
        else:
            # Check Docker is available
            if not shutil.which("docker"):
                console.print("[red]Error: docker not found[/red]")
                raise typer.Exit(1)

            # Current :latest digest, to detect a no-op rebuild below.
            old_latest_digest = get_image_digest(repository, "latest")

            wait_for_pypi_version(package_name, version, repo="worlds", api_key=api_key)
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

            # Promotion is ordered push :<version> -> prefetch :<version> ->
            # retag :<version> as :latest. :latest only ever moves to a digest
            # that has already booted on a node and seeded the snapshot store;
            # a retag is a manifest copy, so the promoted tag is warm the
            # instant it flips. Anything that resolves :latest (launches, the
            # next --skip-docker retag) never pays the 10+ minute cold-ingest path.
            new_digest = get_image_digest(repository, version)
            if new_digest is not None and new_digest == old_latest_digest:
                console.print(
                    "\n[dim]Docker image digest unchanged - :latest already points at it, skipping prefetch[/dim]"
                )
            else:
                console.print()
                console.print("[bold]Prefetching image...[/bold]")
                if not _prefetch_world_image(version_image, short_name):
                    console.print(
                        f"[red]Prefetch failed: {version_image} is pushed but has not booted"
                        + (" and :latest was NOT moved" if promote_latest else "")
                        + ". Fix the boot failure and re-run the publish.[/red]"
                    )
                    raise typer.Exit(1)
                if promote_latest:
                    console.print("[cyan]Promoting to :latest...[/cyan]")
                    if not _retag_world_image(package_name, repository, version, "latest", api_key):
                        console.print(
                            f"[red]Failed to promote {version_image} to :latest (prefetch succeeded; "
                            ":latest was NOT moved). Re-run the publish.[/red]"
                        )
                        raise typer.Exit(1)
                    console.print(f"[green]Promoted:[/green] {latest_image}")
                else:
                    console.print(
                        f"[dim]Dev publish - :latest not moved. Launch by pinned version {package_name}:{version}; "
                        "later --dev publishes retag from it.[/dim]"
                    )
    else:
        console.print("\n[dim]No Dockerfile found - skipping Docker image build[/dim]")

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
