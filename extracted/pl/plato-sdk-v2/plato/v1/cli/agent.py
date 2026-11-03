"""Agent CLI commands for Plato."""

import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import typer

from plato.v1.cli.utils import console, require_api_key

if TYPE_CHECKING:
    from plato.agents.build import BuildConfig


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

    All fields in BuildConfig are considered template variables for Harbor's
    installation templates. These are stored separately for easy querying.

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


agent_app = typer.Typer(help="Manage, deploy, and run agents (uses Harbor)")

# Harbor agent name to install script path (relative to harbor/agents/installed/)
HARBOR_AGENTS = {
    "claude-code": "install-claude-code.sh.j2",
    "openhands": "install-openhands.sh.j2",
    "codex": "install-codex.sh.j2",
    "aider": "install-aider.sh.j2",
    "gemini-cli": "install-gemini-cli.sh.j2",
    "goose": "install-goose.sh.j2",
    "swe-agent": "install-swe-agent.sh.j2",
    "mini-swe-agent": "install-mini-swe-agent.sh.j2",
    "cline-cli": "cline/install-cline.sh.j2",
    "cursor-cli": "install-cursor-cli.sh.j2",
    "opencode": "install-opencode.sh.j2",
    "qwen-coder": "install-qwen-code.sh.j2",
}

# Base Dockerfile template for Harbor agents
HARBOR_AGENT_DOCKERFILE_BASE = """FROM python:3.12-slim

# Install common dependencies
RUN apt-get update && apt-get install -y \\
    curl \\
    git \\
    bash \\
    build-essential \\
    && rm -rf /var/lib/apt/lists/*
"""

HARBOR_AGENT_DOCKERFILE_INSTALL = """
# Copy and run the install script
COPY install.sh /tmp/install.sh
RUN chmod +x /tmp/install.sh && /tmp/install.sh

WORKDIR /app
"""


def _build_harbor_dockerfile(aux_files: list[str]) -> str:
    """Build Dockerfile content, optionally including COPY for aux files."""
    dockerfile = HARBOR_AGENT_DOCKERFILE_BASE

    # Add COPY for each auxiliary file
    for filename in aux_files:
        dockerfile += f"\n# Copy auxiliary file\nCOPY {filename} /{filename}\n"

    dockerfile += HARBOR_AGENT_DOCKERFILE_INSTALL
    return dockerfile


# Auxiliary files needed by certain agents (relative to harbor/agents/installed/)
HARBOR_AGENT_AUX_FILES = {
    "openhands": ["patch_litellm.py"],
}


def _get_harbor_version() -> str:
    """Get Harbor package version."""
    try:
        import harbor

        return getattr(harbor, "__version__", "0.0.0")
    except ImportError:
        return "0.0.0"


def _get_harbor_install_script(agent_name: str, template_vars: dict[str, str] | None = None) -> str | None:
    """Get the install script content from Harbor package.

    Args:
        agent_name: Name of the Harbor agent (e.g., 'claude-code', 'openhands')
        template_vars: Template variables to render (e.g., {'version': '1.0.0'})
                      If None, uses latest version.

    Returns:
        Rendered install script content, or None if agent not found.
    """
    try:
        import harbor

        harbor_path = Path(harbor.__file__).parent
        script_file = HARBOR_AGENTS.get(agent_name)
        if not script_file:
            return None

        script_path = harbor_path / "agents" / "installed" / script_file
        if not script_path.exists():
            return None

        # Read and render the Jinja2 template
        from jinja2 import Environment

        env = Environment()
        template = env.from_string(script_path.read_text())

        # Use provided template vars or empty dict (which means latest)
        render_vars = template_vars or {}
        rendered = template.render(**render_vars)

        # Strip trailing whitespace from each line to fix heredoc issues
        # (some Harbor templates have trailing spaces after EOF delimiters)
        lines = [line.rstrip() for line in rendered.splitlines()]
        return "\n".join(lines) + "\n"
    except ImportError:
        return None
    except Exception:
        return None


def _copy_harbor_aux_files(agent_name: str, dest_path: Path) -> None:
    """Copy auxiliary files needed by an agent to the build directory."""
    aux_files = HARBOR_AGENT_AUX_FILES.get(agent_name, [])
    if not aux_files:
        return

    try:
        import harbor

        harbor_path = Path(harbor.__file__).parent
        installed_path = harbor_path / "agents" / "installed"

        for filename in aux_files:
            src = installed_path / filename
            if src.exists():
                shutil.copy(src, dest_path / filename)
    except ImportError:
        pass
    except Exception:
        pass


def _pull_ecr_cache(agent_name: str) -> str | None:
    """Pull the latest ECR image for use as Docker build cache.

    Returns the image tag if successful, None otherwise.
    """
    import httpx

    api_key = os.getenv("PLATO_API_KEY")
    if not api_key:
        return None

    base_url = os.getenv("PLATO_BASE_URL", "https://plato.so").rstrip("/")
    if base_url.endswith("/api"):
        base_url = base_url[:-4]
    api_url = f"{base_url}/api"

    try:
        with httpx.Client(base_url=api_url, timeout=30.0) as client:
            response = client.post(
                "/v2/agents/ecr-token",
                params={"agent_name": agent_name},
                headers={"X-API-Key": api_key},
            )
            if response.status_code != 200:
                return None
            ecr_info = response.json()

        registry = ecr_info["registry"]
        ecr_token = ecr_info["token"]
        image_uri = ecr_info["image_uri"]

        # Login to ECR
        subprocess.run(
            ["docker", "login", "--username", "AWS", "--password-stdin", registry],
            input=ecr_token,
            text=True,
            capture_output=True,
        )

        # Pull latest tag as cache
        cache_tag = f"{image_uri}:latest"
        result = subprocess.run(
            ["docker", "pull", cache_tag],
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return cache_tag
    except Exception:
        pass
    return None


def _publish_agent_image(
    agent_name: str,
    version: str,
    build_path: Path,
    description: str,
    dry_run: bool,
    schema_data: dict | None = None,
    build_config: "BuildConfig | None" = None,
) -> None:
    """Common logic for publishing an agent Docker image to ECR."""
    import httpx

    # Check Docker is available
    if not shutil.which("docker"):
        console.print("[red]Error: docker not found[/red]")
        raise typer.Exit(1)

    console.print(f"[cyan]Agent:[/cyan] {agent_name}")
    console.print(f"[cyan]Version:[/cyan] {version}")
    console.print()

    # Build Docker image with streaming output
    console.print("[cyan]Building Docker image...[/cyan]")
    local_tag = f"{agent_name}:{version}"

    # Build docker command with build args from config
    docker_cmd = ["docker", "build", "--progress=plain", "-t", local_tag]

    # Add --target prod if Dockerfile has multi-stage builds
    dockerfile_path = build_path / "Dockerfile"
    if dockerfile_path.exists():
        dockerfile_content = dockerfile_path.read_text()
        if "FROM" in dockerfile_content and "AS prod" in dockerfile_content:
            docker_cmd.extend(["--target", "prod"])
            console.print("[cyan]Using target: prod[/cyan]")

    # Pull latest ECR image as build cache to avoid rebuilding unchanged layers
    cache_image = _pull_ecr_cache(agent_name)
    if cache_image:
        docker_cmd.extend(["--cache-from", cache_image])
        console.print(f"[cyan]Using cache from:[/cyan] {cache_image}")

    # Add build args from build config's env dict
    if build_config and build_config.env:
        for key, value in build_config.env.items():
            docker_cmd.extend(["--build-arg", f"{key}={value}"])

    docker_cmd.append(str(build_path))

    # Use Popen to stream output in real-time
    process = subprocess.Popen(
        docker_cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )

    # Stream build output
    build_output = []
    if process.stdout is None:
        console.print("[red]Error: Failed to capture Docker build output[/red]")
        raise typer.Exit(1)
    for line in iter(process.stdout.readline, ""):
        line = line.rstrip()
        if line:
            build_output.append(line)
            # Show key build steps
            if line.startswith("#") or "Step" in line or "ERROR" in line or "error" in line.lower():
                if "ERROR" in line or "error" in line.lower():
                    console.print(f"[red]{line}[/red]")
                else:
                    console.print(f"[dim]{line}[/dim]")

    process.wait()

    if process.returncode != 0:
        console.print("\n[red]Docker build failed![/red]")
        # Show last 30 lines of output for context
        console.print("[yellow]Last build output:[/yellow]")
        for line in build_output[-30:]:
            console.print(f"  {line}")
        raise typer.Exit(1)

    console.print(f"\n[green]Built image:[/green] {local_tag}")

    if dry_run:
        console.print("\n[yellow]Dry run - skipping ECR push and registration[/yellow]")
        return

    # Get API key
    api_key = os.getenv("PLATO_API_KEY")
    if not api_key:
        console.print("[red]Error: PLATO_API_KEY environment variable not set[/red]")
        raise typer.Exit(1)

    # Get base URL
    base_url = os.getenv("PLATO_BASE_URL", "https://plato.so").rstrip("/")
    if base_url.endswith("/api"):
        base_url = base_url[:-4]
    api_url = f"{base_url}/api"

    # Get ECR token
    console.print("[cyan]Getting ECR credentials...[/cyan]")
    with httpx.Client(base_url=api_url, timeout=30.0) as client:
        response = client.post(
            "/v2/agents/ecr-token",
            params={"agent_name": agent_name},
            headers={"X-API-Key": api_key},
        )

        if response.status_code == 401:
            console.print("[red]Error: Authentication failed - check PLATO_API_KEY[/red]")
            raise typer.Exit(1)
        elif response.status_code != 200:
            console.print(f"[red]Error getting ECR token: {response.status_code}[/red]")
            console.print(response.text)
            raise typer.Exit(1)

        ecr_info = response.json()

    registry = ecr_info["registry"]
    ecr_token = ecr_info["token"]
    image_uri = ecr_info["image_uri"]

    # Docker login to ECR
    console.print("[cyan]Logging in to ECR...[/cyan]")
    login_result = subprocess.run(
        ["docker", "login", "--username", "AWS", "--password-stdin", registry],
        input=ecr_token,
        text=True,
        capture_output=True,
    )
    if login_result.returncode != 0:
        console.print(f"[red]ECR login failed:[/red] {login_result.stderr}")
        raise typer.Exit(1)

    # Tag and push
    ecr_image = f"{image_uri}:{version}"
    console.print(f"[cyan]Pushing to:[/cyan] {ecr_image}")

    subprocess.run(["docker", "tag", local_tag, ecr_image], check=True)

    push_result = subprocess.run(["docker", "push", ecr_image], capture_output=True, text=True)
    if push_result.returncode != 0:
        console.print(f"[red]Push failed:[/red] {push_result.stderr}")
        raise typer.Exit(1)
    console.print(f"[green]Pushed:[/green] {ecr_image}")

    # Also push as latest for future build cache
    latest_image = f"{image_uri}:latest"
    subprocess.run(["docker", "tag", local_tag, latest_image], check=True)
    subprocess.run(["docker", "push", latest_image], capture_output=True, text=True)

    # Register agent artifact
    console.print("[cyan]Registering agent...[/cyan]")
    with httpx.Client(base_url=api_url, timeout=30.0) as client:
        registration_data = {
            "name": agent_name,
            "version": version,
            "image_uri": ecr_image,
            "description": description,
            "config_schema": schema_data,
        }
        response = client.post(
            "/v2/agents/register",
            json=registration_data,
            headers={"X-API-Key": api_key},
        )

        if response.status_code == 409:
            detail = response.json().get("detail", "Version conflict")
            console.print(f"[red]Error: {detail}[/red]")
            raise typer.Exit(1)
        elif response.status_code != 200:
            console.print(f"[red]Registration failed: {response.status_code}[/red]")
            console.print(response.text)
            raise typer.Exit(1)

        reg_result = response.json()

    console.print()
    console.print("[bold green]Agent published successfully![/bold green]")
    console.print(f"[cyan]Artifact ID:[/cyan] {reg_result['artifact_id']}")
    console.print(f"[cyan]Image:[/cyan] {ecr_image}")

    # Clean up local images after successful push
    console.print("[dim]Cleaning up local images...[/dim]")
    subprocess.run(["docker", "rmi", local_tag], capture_output=True)
    subprocess.run(["docker", "rmi", ecr_image], capture_output=True)


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


@agent_app.command(name="run")
def agent_run(
    ctx: typer.Context,
    agent: str = typer.Option(None, "--agent", "-a", help="Agent name (e.g., 'claude-code', 'openhands')"),
    model: str = typer.Option(None, "--model", "-m", help="Model name (e.g., 'anthropic/claude-sonnet-4')"),
    dataset: str = typer.Option(None, "--dataset", "-d", help="Dataset to run on"),
):
    """Run an agent using Harbor's runner infrastructure.

    Wraps `harbor run` to execute agents on a dataset. Supports Harbor built-in agents
    (claude-code, openhands, codex, aider, etc.) and Plato custom agents (computer-use).

    Options:
        -a, --agent: Agent name to run. See 'plato agent list' for available agents.
        -m, --model: Model name for the agent (e.g., 'anthropic/claude-sonnet-4')
        -d, --dataset: Dataset to run on (e.g., 'swe-bench-lite', 'terminal-bench')

    Additional arguments can be passed to Harbor after '--' separator.
    """
    # Check if harbor is installed
    if not shutil.which("harbor"):
        console.print("[red]Error: harbor CLI not found[/red]")
        console.print("\n[yellow]Install Harbor with:[/yellow]")
        console.print("  pip install harbor")
        console.print("  # or")
        console.print("  uv tool install harbor")
        raise typer.Exit(1)

    # Build command
    cmd = ["harbor", "run"]

    if agent:
        cmd.extend(["-a", agent])
    if model:
        cmd.extend(["-m", model])
    if dataset:
        cmd.extend(["-d", dataset])

    # Add any extra arguments passed after --
    if ctx.args:
        cmd.extend(ctx.args)

    # If no arguments provided, show help
    if len(cmd) == 2:
        console.print("[yellow]Usage: plato agent run -a <agent> -m <model> -d <dataset>[/yellow]")
        console.print("\n[bold]Harbor agents:[/bold]")
        console.print("  claude-code, openhands, codex, aider, gemini-cli,")
        console.print("  goose, swe-agent, mini-swe-agent, cline-cli,")
        console.print("  cursor-cli, opencode, qwen-coder")
        console.print("\n[bold]Plato agents:[/bold]")
        console.print("  computer-use (pip install plato-agent-computer-use)")
        console.print("\n[bold]Example:[/bold]")
        console.print("  plato agent run -a claude-code -m anthropic/claude-sonnet-4 -d swe-bench-lite")
        raise typer.Exit(0)

    console.print(f"[cyan]Running:[/cyan] {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd)
        raise typer.Exit(result.returncode)
    except KeyboardInterrupt:
        console.print("\n[yellow]Interrupted by user[/yellow]")
        raise typer.Exit(130) from None
    except Exception as e:
        console.print(f"[red]Error running harbor: {e}[/red]")
        raise typer.Exit(1) from e


@agent_app.command(name="list")
def agent_list():
    """List all available agents.

    Shows Harbor built-in agents (claude-code, openhands, etc.) and Plato custom agents
    (computer-use) that can be used with 'plato agent run' and 'plato agent publish'.
    """
    console.print("[bold]Harbor Agents:[/bold]\n")

    harbor_agents = [
        ("claude-code", "Claude Code - Anthropic's CLI coding agent"),
        ("openhands", "OpenHands - All Hands AI coding agent"),
        ("codex", "Codex - OpenAI CLI coding agent"),
        ("aider", "Aider - AI pair programming tool"),
        ("gemini-cli", "Gemini CLI - Google's CLI coding agent"),
        ("goose", "Goose - Block's coding agent"),
        ("swe-agent", "SWE-agent - Princeton's software engineering agent"),
        ("mini-swe-agent", "Mini SWE-agent - Lightweight SWE-agent"),
        ("cline-cli", "Cline CLI - VS Code extension CLI"),
        ("cursor-cli", "Cursor CLI - Cursor editor CLI"),
        ("opencode", "OpenCode - Open source coding agent"),
        ("qwen-coder", "Qwen Coder - Alibaba's coding agent"),
    ]

    for name, description in harbor_agents:
        console.print(f"  [cyan]{name:<15}[/cyan] {description}")

    console.print("\n[bold]Plato Agents:[/bold]\n")

    plato_agents = [
        (
            "computer-use",
            "Browser automation agent (pip install plato-agent-computer-use)",
        ),
    ]

    for name, description in plato_agents:
        console.print(f"  [cyan]{name:<15}[/cyan] {description}")

    console.print("\n[bold]Usage:[/bold]")
    console.print("  plato agent run -a <agent> -m <model> -d <dataset>")
    console.print("\n[bold]Example:[/bold]")
    console.print("  plato agent run -a claude-code -m anthropic/claude-sonnet-4 -d swe-bench-lite")


@agent_app.command(name="schema")
def agent_schema(
    agent_name: str = typer.Argument(..., help="Agent name to get schema for"),
):
    """Get the configuration schema for a Harbor agent.

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
    target: str = typer.Argument(".", help="Path to agent directory OR Harbor agent name"),
    all_agents: bool = typer.Option(False, "--all", "-a", help="Publish all agents in directory"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Build without pushing to ECR"),
):
    """Build and publish an agent Docker image to ECR.

    Builds a Docker image for the agent and pushes it to the Plato ECR registry.
    Version is determined automatically from pyproject.toml (custom agents) or the
    installed Harbor package version (Harbor agents).

    Arguments:
        target: Path to custom agent directory with Dockerfile + pyproject.toml,
            OR name of a Harbor built-in agent (e.g., 'claude-code')

    Options:
        -a, --all: Publish all agents found in the target directory
        --dry-run: Build the Docker image without pushing to ECR
    """

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
                # Recursively call agent_push for each agent
                _push_single_agent(agent_dir, dry_run)
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

    _push_single_agent(pkg_path, dry_run)


def _push_single_agent(pkg_path: Path, dry_run: bool) -> None:
    """Push a single custom agent from a directory."""
    from plato.agents.build import BuildConfig

    # Check for Dockerfile
    if not (pkg_path / "Dockerfile").exists():
        console.print(f"[red]Error: No Dockerfile found at {pkg_path}[/red]")
        raise typer.Exit(1)

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

    # Extract short name (remove common prefixes)
    short_name = package_name
    for suffix in ("-agent",):
        if short_name.endswith(suffix):
            short_name = short_name[: -len(suffix)]
            break

    # Load build config from pyproject.toml (optional, for build args)
    build_config = None
    try:
        build_config = BuildConfig.from_pyproject(pkg_path)
        if build_config.env:
            console.print(f"[cyan]Build args:[/cyan] {list(build_config.env.keys())}")
    except Exception:
        pass  # Build config is optional

    # Load schema from entry point defined in pyproject.toml
    schema_data = None
    entry_points_config = pyproject.get("project", {}).get("entry-points", {}).get("plato.agents", {})

    if not entry_points_config:
        console.print("[yellow]No plato.agents entry point in pyproject.toml - agent will have no schema[/yellow]")
    else:
        # Get the first (and typically only) entry point
        # Format is: agent_name = "module_name:ClassName"
        for ep_name, ep_value in entry_points_config.items():
            try:
                if ":" not in ep_value:
                    console.print(f"[yellow]Invalid entry point format '{ep_value}' - expected 'module:Class'[/yellow]")
                    continue

                module_name, class_name = ep_value.split(":", 1)

                # Add src/ to path and import
                import sys

                src_path = pkg_path / "src"
                if src_path.exists():
                    sys.path.insert(0, str(src_path))

                try:
                    module = __import__(module_name, fromlist=[class_name])
                    agent_cls = getattr(module, class_name)
                    schema_data = agent_cls.get_schema()
                    console.print(f"[green]Loaded schema from {class_name}[/green]")
                    break
                finally:
                    if src_path.exists() and str(src_path) in sys.path:
                        sys.path.remove(str(src_path))

            except Exception as e:
                console.print(f"[yellow]Failed to load schema from entry point: {e}[/yellow]")

    if not schema_data:
        console.print("[yellow]No schema found (agent will have no config validation)[/yellow]")

    _publish_agent_image(
        agent_name=short_name,
        version=version,
        build_path=pkg_path,
        description=description or f"Custom agent: {short_name}",
        dry_run=dry_run,
        schema_data=schema_data,
        build_config=build_config,
    )


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
