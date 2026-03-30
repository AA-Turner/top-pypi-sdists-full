"""Shared utilities for Plato CLI commands."""

import asyncio
import os
import re
import shutil
import time
from datetime import datetime
from pathlib import Path

import httpx
import typer
import yaml
from rich.console import Console
from rich.markup import MarkupError

from plato.utils.pypi_index import plato_token_simple_index

# Initialize Rich console - shared across all CLI modules
console = Console()


def safe_print(*args, **kwargs):
    """Print with Rich markup, falling back to raw output on MarkupError."""
    try:
        console.print(*args, **kwargs)
    except MarkupError:
        fallback_kwargs = dict(kwargs)
        fallback_kwargs.pop("markup", None)
        console.print(*args, markup=False, **fallback_kwargs)


def wait_for_pypi_version(
    package_name: str,
    version: str,
    *,
    repo: str = "agents",
    api_key: str | None = None,
    timeout: float = 30.0,
    poll_interval: float = 2.0,
) -> None:
    """Poll a Plato PyPI index until the given version is listed."""
    index_url = plato_token_simple_index(repo, api_key=api_key)
    package_url = f"{index_url}{package_name}/"
    deadline = time.monotonic() + timeout
    console.print(f"[dim]Waiting for {package_name}=={version} on {repo} index...[/dim]")
    while time.monotonic() < deadline:
        try:
            resp = httpx.get(package_url, timeout=10, follow_redirects=True)
            if resp.status_code == 200 and version in resp.text:
                console.print(f"[green]{package_name}=={version} available on {repo} index[/green]")
                return
        except httpx.HTTPError:
            pass
        time.sleep(poll_interval)
    console.print(
        f"[yellow]Warning: {package_name}=={version} not found on {repo} index after {timeout}s, proceeding anyway[/yellow]"
    )


def read_plato_config(config_path: str | Path) -> dict:
    """Read plato-config.yml file or exit with error."""
    try:
        with open(config_path) as f:
            return yaml.safe_load(f)
    except Exception as e:
        console.print(f"[red]❌ Error reading plato-config.yml: {e}[/red]")
        raise typer.Exit(1) from e


def require_plato_config_field(config: dict, field: str) -> str:
    """Get a required field from plato config or exit with error."""
    value = config.get(field)
    if not value:
        console.print(f"[red]❌ No {field} in plato-config.yml[/red]")
        raise typer.Exit(1)
    return value


def require_api_key() -> str:
    """Get API key or exit with error."""
    api_key = os.getenv("PLATO_API_KEY")
    if not api_key:
        console.print("[red]PLATO_API_KEY environment variable not set[/red]")
        console.print("\n[yellow]Set your API key:[/yellow]")
        console.print("  export PLATO_API_KEY='your-api-key-here'")
        raise typer.Exit(1)
    return api_key


def get_http_client() -> httpx.Client:
    """Get configured httpx client."""
    base_url = os.getenv("PLATO_BASE_URL", "https://plato.so")
    # Strip trailing /api if present (to match v2 SDK behavior)
    if base_url.endswith("/api"):
        base_url = base_url[:-4]
    base_url = base_url.rstrip("/")
    return httpx.Client(base_url=base_url, timeout=httpx.Timeout(600.0))


def handle_async(coro):
    """Helper to run async functions with proper error handling."""
    try:
        return asyncio.run(coro)
    except KeyboardInterrupt:
        console.print("\n[red]🛑 Operation cancelled by user.[/red]")
        raise typer.Exit(1) from None
    except Exception as e:
        console.print(f"[red]❌ Error: {e}[/red]")
        if "401" in str(e) or "Unauthorized" in str(e):
            console.print("💡 [yellow]Hint: Make sure PLATO_API_KEY is set in your environment[/yellow]")
        raise typer.Exit(1) from e


_PROJECT_VERSION_RE = re.compile(r"""^(\s*version\s*=\s*)(["'])([^"']+)(["'])(\s*(?:#.*)?)$""")
_SEMVER_DEV_RE = re.compile(r"^(?P<major>\d+)\.(?P<minor>\d+)\.(?P<patch>\d+)(?:\.dev(?P<dev>\d+))?$")


def compute_bumped_version(
    current_version: str,
    *,
    minor: bool = False,
    dev: bool = False,
    now: datetime | None = None,
) -> str:
    """Compute the next version for patch/minor and optional dev publishes."""
    match = _SEMVER_DEV_RE.fullmatch(current_version)
    if not match:
        raise ValueError(f"Unsupported version format '{current_version}'. Expected X.Y.Z or X.Y.Z.devYYYYMMDDHHMMSS.")

    major = int(match.group("major"))
    minor_value = int(match.group("minor"))
    patch = int(match.group("patch"))
    existing_dev = match.group("dev")

    if not (dev and existing_dev is not None):
        if minor:
            minor_value += 1
            patch = 0
        else:
            patch += 1

    next_version = f"{major}.{minor_value}.{patch}"
    if dev:
        stamp = (now or datetime.now()).strftime("%Y%m%d%H%M%S")
        next_version = f"{next_version}.dev{stamp}"
    return next_version


def update_project_version(pyproject_file: Path, new_version: str) -> None:
    """Rewrite project.version in pyproject.toml while preserving surrounding formatting."""
    lines = pyproject_file.read_text().splitlines(keepends=True)
    in_project = False

    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("[") and stripped.endswith("]"):
            in_project = stripped == "[project]"
            continue

        if not in_project:
            continue

        match = _PROJECT_VERSION_RE.match(line.rstrip("\n"))
        if not match:
            continue

        prefix, quote, _, _, suffix = match.groups()
        newline = "\n" if line.endswith("\n") else ""
        lines[index] = f"{prefix}{quote}{new_version}{quote}{suffix}{newline}"
        pyproject_file.write_text("".join(lines))
        return

    raise ValueError(f"Could not find [project].version in {pyproject_file}")


def maybe_bump_package_version(
    pyproject_file: Path,
    current_version: str,
    *,
    minor: bool = False,
    dev: bool = False,
    dry_run: bool = False,
) -> str:
    """Optionally update a package version before publish and return the effective version."""
    bump_kind = "minor" if minor else "patch"
    next_version = compute_bumped_version(current_version, minor=minor, dev=dev)

    if dry_run:
        console.print(
            f"[yellow]Dry run - would bump version ({bump_kind}) from {current_version} to {next_version}[/yellow]"
        )
        if dev:
            console.print(f"[yellow]Updated version:[/yellow] {next_version}")
            console.print("[yellow]Note:[/yellow] sdk changes will have to be published if there were any changes")
        return current_version

    if not dev:
        should_bump = typer.confirm(
            f"Bump version ({bump_kind}) from {current_version} to {next_version}?",
            default=True,
        )
        if not should_bump:
            console.print(f"[yellow]Keeping version:[/yellow] {current_version}")
            return current_version

    if next_version != current_version:
        update_project_version(pyproject_file, next_version)
        console.print(f"[green]Updated version:[/green] {next_version}")
    else:
        console.print(f"[green]Keeping existing dev version:[/green] {next_version}")
    if dev:
        console.print("[yellow]Note:[/yellow] sdk changes will have to be published if there were any changes")
    return next_version


# =============================================================================
# SDK Build Helpers (shared by agent and world publish commands)
# =============================================================================


def build_sdk_wheel(sdk_path: Path, dest_dir: Path) -> Path | None:
    """Build SDK wheel and copy to destination directory.

    Args:
        sdk_path: Path to the SDK source directory
        dest_dir: Directory to copy the built wheel to

    Returns:
        Path to the wheel file in dest_dir, or None if build failed.
    """
    import subprocess

    console.print(f"[cyan]Building SDK from {sdk_path}...[/cyan]")

    result = subprocess.run(
        ["uv", "build"],
        cwd=sdk_path,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        console.print(f"[red]SDK build failed:[/red] {result.stderr}")
        return None

    dist_dir = sdk_path / "dist"
    wheels = list(dist_dir.glob("plato_sdk_v2-*.whl"))
    if not wheels:
        console.print("[red]No SDK wheel found after build[/red]")
        return None

    wheel = max(wheels, key=lambda p: p.stat().st_mtime)
    dest_wheel = dest_dir / wheel.name
    shutil.copy(wheel, dest_wheel)
    console.print(f"[green]SDK wheel:[/green] {wheel.name}")
    return dest_wheel


def prepare_build_context_with_sdk(pkg_path: Path, sdk_path: Path) -> Path | None:
    """Create a temp build context with SDK wheel injected into Dockerfile.

    Handles multi-stage builds by injecting SDK install into the 'prod' stage.
    For simple Dockerfiles, appends SDK install at the end.

    Args:
        pkg_path: Path to the package directory with Dockerfile
        sdk_path: Path to the SDK source directory

    Returns:
        Path to temp build context directory, or None if failed.
        Caller is responsible for cleaning up the temp directory.
    """
    import re
    import tempfile

    temp_dir = Path(tempfile.mkdtemp(prefix="plato-build-sdk-"))

    try:
        # Copy all files from original build context
        shutil.copytree(pkg_path, temp_dir, dirs_exist_ok=True)

        # Build SDK wheel and copy to temp dir
        sdk_wheel = build_sdk_wheel(sdk_path, temp_dir)
        if not sdk_wheel:
            shutil.rmtree(temp_dir, ignore_errors=True)
            return None

        # Read original Dockerfile
        dockerfile_path = temp_dir / "Dockerfile"
        original_dockerfile = dockerfile_path.read_text()

        sdk_install_lines = f"""
# Install local SDK (injected by plato publish --sdk-path)
USER root
COPY {sdk_wheel.name} /tmp/{sdk_wheel.name}
RUN UV_CACHE_DIR=/tmp uv pip install --system --reinstall /tmp/{sdk_wheel.name} && rm /tmp/{sdk_wheel.name}
"""

        # Check for multi-stage build with 'prod' target
        if "AS prod" in original_dockerfile:
            # Find the prod stage and inject SDK install before the next FROM or end
            lines = original_dockerfile.split("\n")
            modified_lines = []
            in_prod_stage = False
            sdk_injected = False

            for i, line in enumerate(lines):
                # Detect start of prod stage
                if re.match(r"FROM\s+.*\s+AS\s+prod", line, re.IGNORECASE):
                    in_prod_stage = True
                    modified_lines.append(line)
                    continue

                # Detect end of prod stage (next FROM or section separator)
                if in_prod_stage and not sdk_injected:
                    if line.startswith("FROM ") or line.startswith("# ==="):
                        # Inject SDK install before this line
                        modified_lines.append(sdk_install_lines)
                        sdk_injected = True
                        in_prod_stage = False

                modified_lines.append(line)

            # If prod stage goes to end of file, append there
            if in_prod_stage and not sdk_injected:
                modified_lines.append(sdk_install_lines)

            modified_dockerfile = "\n".join(modified_lines)
            console.print("[dim]Injected SDK install into 'prod' stage[/dim]")
        else:
            # No multi-stage build, just append at end
            modified_dockerfile = original_dockerfile.rstrip() + "\n" + sdk_install_lines

        # Write modified Dockerfile
        dockerfile_path.write_text(modified_dockerfile)

        # Debug output
        console.print(f"[dim]Build context: {temp_dir}[/dim]")
        console.print(f"[dim]SDK wheel at: {sdk_wheel}[/dim]")
        console.print(f"[dim]Wheel exists: {sdk_wheel.exists()}[/dim]")

        return temp_dir
    except Exception as e:
        console.print(f"[red]Error preparing build context: {e}[/red]")
        shutil.rmtree(temp_dir, ignore_errors=True)
        return None
