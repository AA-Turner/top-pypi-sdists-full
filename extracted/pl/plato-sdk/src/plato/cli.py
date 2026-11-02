import asyncio
import json
import logging
import os
import platform
import shutil
import subprocess
import tempfile
from pathlib import Path

import typer
import yaml
from dotenv import load_dotenv
from rich.console import Console
from rich.logging import RichHandler

from plato.sdk import Plato

# Initialize Rich console
console = Console()
app = typer.Typer(
    help="[bold blue]Plato CLI[/bold blue] - Manage Plato environments and simulators."
)

# Set up Rich logging handler for FlowExecutor
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    handlers=[RichHandler(console=console, show_time=False, show_path=False)],
)
flow_logger = logging.getLogger("plato.flow")


def _find_bundled_cli() -> str | None:
    """
    Find the bundled Plato CLI binary.

    Returns:
        Path to the bundled CLI binary if found, None otherwise.
    """
    # Determine the expected binary name
    binary_name = "plato-cli.exe" if platform.system().lower() == "windows" else "plato-cli"

    # Look for the binary in the package's bin directory
    # This file (__file__) is at src/plato/cli.py, so bin is at src/plato/bin/
    package_dir = Path(__file__).resolve().parent
    bin_dir = package_dir / "bin"
    binary_path = bin_dir / binary_name

    if binary_path.exists() and os.access(binary_path, os.X_OK):
        return str(binary_path)

    return None


# Load environment variables
load_dotenv()
load_dotenv(dotenv_path=os.path.join(os.path.expanduser("~"), ".env"))
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), ".env"))


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
            console.print(
                "💡 [yellow]Hint: Make sure PLATO_API_KEY is set in your environment[/yellow]"
            )
        raise typer.Exit(1) from e


# =============================================================================
# REVIEW WORKFLOW HELPERS
# =============================================================================


async def get_simulator_by_name(base_url: str, api_key: str, simulator_name: str):
    """Get simulator by name from API."""
    import aiohttp

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f"{base_url}/simulator/{simulator_name}", headers={"X-API-Key": api_key}
        ) as resp:
            if resp.status == 404:
                raise Exception(f"Simulator '{simulator_name}' not found")
            elif resp.status != 200:
                try:
                    data = await resp.json()
                    detail = data.get("detail", data) if isinstance(data, dict) else data
                except Exception:
                    detail = await resp.text()
                raise Exception(f"Failed to get simulator: {resp.status} - {detail}")

            return await resp.json()


async def _raise_api_error(resp):
    """Raise a rich error with detail if available."""
    try:
        data = await resp.json()
        detail = data.get("detail", data) if isinstance(data, dict) else data
    except Exception:
        detail = await resp.text()
    raise Exception(f"API error {resp.status}: {detail}")


async def put_simulator_fields(base_url: str, api_key: str, simulator_id: int, payload: dict):
    """Partial simulator update (artifact IDs, notes, etc.)."""
    import aiohttp

    async with aiohttp.ClientSession() as session:
        async with session.put(
            f"{base_url}/simulator/{simulator_id}",
            headers={"X-API-Key": api_key, "Content-Type": "application/json"},
            json=payload,
        ) as resp:
            if resp.status >= 400:
                await _raise_api_error(resp)
            return await resp.json()


async def post_simulator_status(base_url: str, api_key: str, simulator_id: int, new_status: str):
    """Change simulator status via the new status endpoint."""
    import aiohttp

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{base_url}/simulator/{simulator_id}/status",
            headers={"X-API-Key": api_key, "Content-Type": "application/json"},
            json={"status": new_status},
        ) as resp:
            if resp.status >= 400:
                await _raise_api_error(resp)
            return await resp.json()


async def post_simulator_review(base_url: str, api_key: str, simulator_id: int, review: dict):
    """Submit an environment or data review."""
    import aiohttp

    # Drop None fields to keep payload tidy
    cleaned_review = {k: v for k, v in review.items() if v is not None}

    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{base_url}/simulator/{simulator_id}/reviews",
            headers={"X-API-Key": api_key, "Content-Type": "application/json"},
            json=cleaned_review,
        ) as resp:
            if resp.status >= 400:
                await _raise_api_error(resp)
            return await resp.json()


def validate_status_transition(current_status: str, expected_status: str, command_name: str):
    """Validate that current status matches expected status for the command."""
    if current_status != expected_status:
        console.print(f"[red]❌ Invalid status for {command_name}[/red]")
        console.print(f"\n[yellow]Current status:[/yellow]  {current_status}")
        console.print(f"[yellow]Expected status:[/yellow] {expected_status}")
        console.print(
            f"\n[yellow]Cannot run {command_name} from status '{current_status}'[/yellow]"
        )
        raise typer.Exit(1)


# =============================================================================
# ENVIRONMENT COMMANDS
# =============================================================================


@app.command(context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def hub(
    ctx: typer.Context,
):
    """
    Launch the Plato Hub CLI (interactive TUI for managing simulators).

    The hub command opens the Go-based Plato CLI which provides an interactive
    terminal UI for browsing simulators, launching environments, and managing VMs.

    Available subcommands:
    - clone <service>: Clone a service from Plato Hub
    - credentials: Display your Plato Hub credentials
    - (no args): Start interactive TUI mode

    Examples:
        plato hub clone espocrm
        plato hub credentials
        plato hub
    """
    # Find the bundled CLI binary
    plato_bin = _find_bundled_cli()

    if not plato_bin:
        console.print("[red]❌ Plato CLI binary not found in package[/red]")
        console.print(
            "\n[yellow]The bundled CLI binary was not found in this installation.[/yellow]"
        )
        console.print("This indicates an installation issue with the plato-sdk package.")
        console.print("\n[yellow]💡 Try reinstalling the package:[/yellow]")
        console.print("   pip install --upgrade --force-reinstall plato-sdk")
        console.print("\n[dim]If the issue persists, please report it at:[/dim]")
        console.print("[dim]https://github.com/plato-app/plato-client/issues[/dim]")
        raise typer.Exit(1)

    # Get any additional arguments passed after 'hub'
    args = ctx.args if hasattr(ctx, "args") else []

    try:
        # Launch the Go CLI, passing through all arguments
        # Use execvp to replace the current process so the TUI works properly
        os.execvp(plato_bin, [plato_bin] + args)
    except Exception as e:
        console.print(f"[red]❌ Failed to launch Plato Hub: {e}[/red]")
        raise typer.Exit(1) from e


# =============================================================================
# SYNC COMMAND
# =============================================================================


@app.command()
def sync():
    """
    Sync local code to a remote Plato VM using rsync.

    Reads .sandbox.yaml to get ssh_host and service name.
    Syncs to /home/plato/worktree/<service-name>.

    Example:
        plato sync
    """
    # Check if rsync is available
    if not shutil.which("rsync"):
        console.print("[red]❌ rsync is not installed[/red]")
        console.print("\n[yellow]Please install rsync:[/yellow]")
        console.print("  macOS:   brew install rsync")
        console.print("  Linux:   apt-get install rsync or yum install rsync")
        raise typer.Exit(1)

    # Read .sandbox.yaml
    sandbox_file = Path.cwd() / ".sandbox.yaml"

    if not sandbox_file.exists():
        console.print("[red]❌ .sandbox.yaml not found[/red]")
        console.print("\n[yellow]Create a sandbox with: [bold]plato hub[/bold][/yellow]")
        raise typer.Exit(1)

    try:
        with open(sandbox_file) as f:
            sandbox_data = yaml.safe_load(f)
    except Exception as e:
        console.print(f"[red]❌ Error reading .sandbox.yaml: {e}[/red]")
        raise typer.Exit(1) from e

    # Get required fields
    ssh_host = sandbox_data.get("ssh_host")
    plato_config_path = sandbox_data.get("plato_config_path")
    ssh_config_path = sandbox_data.get("ssh_config_path")

    if not ssh_host:
        console.print("[red]❌ .sandbox.yaml missing 'ssh_host'[/red]")
        raise typer.Exit(1)

    if not plato_config_path:
        console.print("[red]❌ .sandbox.yaml missing 'plato_config_path'[/red]")
        raise typer.Exit(1)

    # Load plato-config.yml to get service name
    try:
        with open(plato_config_path) as f:
            plato_config = yaml.safe_load(f)
    except Exception as e:
        console.print(f"[red]❌ Could not read plato-config.yml: {e}[/red]")
        raise typer.Exit(1) from e

    service = plato_config.get("service")
    if not service:
        console.print("[red]❌ plato-config.yml missing 'service'[/red]")
        raise typer.Exit(1)

    # Build remote path
    remote_path = f"/home/plato/worktree/{service}"

    console.print(f"[cyan]SSH host: {ssh_host}[/cyan]")
    console.print(f"[cyan]Service: {service}[/cyan]")
    console.print(f"[cyan]Remote path: {remote_path}[/cyan]")

    # Build rsync command
    local_path = Path.cwd()

    # Hardcoded excludes
    excludes = [
        "__pycache__",
        "*.pyc",
        ".git",
        ".venv",
        ".sandbox.yaml",
    ]

    # Use --progress instead of --info=progress2 for broader rsync compatibility
    cmd = ["rsync", "-avz", "--delete", "--progress"]

    # Add excludes
    for pattern in excludes:
        cmd.extend(["--exclude", pattern])

    # Use SSH with config file. Prefer sandbox-specific config if provided.
    if ssh_config_path:
        ssh_config_file = Path(ssh_config_path)
        if not ssh_config_file.exists():
            console.print(f"[red]❌ SSH config file not found: {ssh_config_file}[/red]")
            raise typer.Exit(1)
    else:
        ssh_config_file = Path.home() / ".ssh" / "config"
        if not ssh_config_file.exists():
            console.print("[red]❌ SSH config file not found[/red]")
            console.print(f"[yellow]Expected: {ssh_config_file}[/yellow]")
            raise typer.Exit(1)
    cmd.extend(["-e", f"ssh -F {ssh_config_file}"])

    # Add source and destination
    source = str(local_path) + "/"
    destination = f"{ssh_host}:{remote_path}/"
    cmd.extend([source, destination])

    # Display info
    console.print(f"\n[bold]Syncing {local_path} to {ssh_host}:{remote_path}[/bold]\n")

    # Execute rsync
    try:
        result = subprocess.run(cmd)
        if result.returncode == 0:
            console.print(f"\n[green]✓ Successfully synced to {ssh_host}[/green]")
        else:
            console.print(f"\n[red]✗ Sync failed with exit code {result.returncode}[/red]")
            raise typer.Exit(result.returncode)
    except KeyboardInterrupt:
        console.print("\n[yellow]Sync interrupted by user[/yellow]")
        raise typer.Exit(130) from None
    except Exception as e:
        console.print(f"[red]❌ Error running rsync: {e}[/red]")
        raise typer.Exit(1) from e


# =============================================================================
# SUBMIT AND REVIEW COMMANDS
# =============================================================================

# Create Typer apps for submit and review actions
submit_app = typer.Typer(help="Submit artifacts for review")
review_app = typer.Typer(help="Review artifacts")

# Add action apps to main app
app.add_typer(submit_app, name="submit")
app.add_typer(review_app, name="review")
# force bump to v36
# TEST/MO CK: This comment marks test-related code. Used for verification in release workflow.


@submit_app.command(name="base")
def submit_base():
    """
    Submit base/environment artifact for review after snapshot.

    Worker submits base artifact for review after creating a snapshot.
    Requires status: env_in_progress
    Transitions to: env_review_requested

    Example:
        plato submit base
    """
    # Get API key (hard fail if missing)
    api_key = os.getenv("PLATO_API_KEY")
    if not api_key:
        console.print("[red]❌ PLATO_API_KEY environment variable not set[/red]")
        console.print("\n[yellow]Set your API key:[/yellow]")
        console.print("  export PLATO_API_KEY='your-api-key-here'")
        raise typer.Exit(1)

    # Read .sandbox.yaml (hard fail if missing)
    sandbox_file = Path.cwd() / ".sandbox.yaml"
    if not sandbox_file.exists():
        console.print("[red]❌ .sandbox.yaml not found in current directory[/red]")
        console.print("\n[yellow]Run 'plato hub' first to create a sandbox[/yellow]")
        raise typer.Exit(1)

    try:
        with open(sandbox_file) as f:
            sandbox_data = yaml.safe_load(f)
    except Exception as e:
        console.print(f"[red]❌ Error reading .sandbox.yaml: {e}[/red]")
        raise typer.Exit(1) from e

    # Get artifact_id (hard fail if missing)
    artifact_id = sandbox_data.get("artifact_id")
    if not artifact_id:
        console.print("[red]❌ No artifact_id found in .sandbox.yaml[/red]")
        console.print("\n[yellow]The sandbox must have an artifact_id to request review[/yellow]")
        raise typer.Exit(1)

    # Get plato_config_path
    plato_config_path = sandbox_data.get("plato_config_path")
    if not plato_config_path:
        console.print("[red]❌ No plato_config_path in .sandbox.yaml[/red]")
        raise typer.Exit(1)

    # Read plato-config.yml to get simulator name
    try:
        with open(plato_config_path) as f:
            plato_config = yaml.safe_load(f)
    except Exception as e:
        console.print(f"[red]❌ Error reading plato-config.yml: {e}[/red]")
        raise typer.Exit(1) from e

    simulator_name = plato_config.get("service")
    if not simulator_name:
        console.print("[red]❌ No service name in plato-config.yml[/red]")
        raise typer.Exit(1)

    async def _submit_base():
        base_url = "https://plato.so/api"

        # Get simulator by name
        simulator = await get_simulator_by_name(base_url, api_key, simulator_name)
        simulator_id = simulator["id"]
        current_config = simulator.get("config", {})
        current_status = current_config.get("status", "not_started")

        # Validate status transition (hard fail if wrong status)
        validate_status_transition(current_status, "env_in_progress", "submit base")

        # Show info and submit
        console.print(f"[cyan]Simulator:[/cyan]      {simulator_name}")
        console.print(f"[cyan]Artifact ID:[/cyan]    {artifact_id}")
        console.print(f"[cyan]Current Status:[/cyan] {current_status}")
        console.print()

        # Set base artifact, then request review
        await put_simulator_fields(
            base_url=base_url,
            api_key=api_key,
            simulator_id=simulator_id,
            payload={"base_artifact_id": artifact_id},
        )
        await post_simulator_status(
            base_url=base_url,
            api_key=api_key,
            simulator_id=simulator_id,
            new_status="env_review_requested",
        )

        console.print("[green]✅ Environment review requested successfully![/green]")
        console.print(f"[cyan]Status:[/cyan] {current_status} → env_review_requested")
        console.print(f"[cyan]Base Artifact:[/cyan] {artifact_id}")

    handle_async(_submit_base())


@review_app.command(name="base")
def review_base():
    """
    Review base/environment artifact session (reviewer testing the environment).

    Opens simulator with artifact in browser for manual testing.
    At the end, prompts to pass (→ env_approved) or reject (→ env_in_progress).

    Requires simulator status: env_review_requested

    Example:
        plato review base
    """
    # Get API key (hard fail if missing)
    api_key = os.getenv("PLATO_API_KEY")
    if not api_key:
        console.print("[red]❌ PLATO_API_KEY environment variable not set[/red]")
        console.print("\n[yellow]Set your API key:[/yellow]")
        console.print("  export PLATO_API_KEY='your-api-key-here'")
        raise typer.Exit(1)

    # Check Playwright (hard fail if missing)
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        console.print("[red]❌ Playwright is not installed[/red]")
        console.print("\n[yellow]Install with:[/yellow]")
        console.print("  pip install playwright")
        console.print("  playwright install chromium")
        raise typer.Exit(1) from None

    # Prompt for simulator name
    simulator_name = typer.prompt("Enter simulator name").strip()
    if not simulator_name:
        console.print("[red]❌ Simulator name is required[/red]")
        raise typer.Exit(1)

    # Prompt for artifact ID (optional - will use base_artifact_id from config if empty)
    artifact_id_input = typer.prompt(
        "Enter artifact ID (or press Enter to use base_artifact_id)", default=""
    ).strip()

    async def _review_base():
        base_url = "https://plato.so/api"
        client = Plato(base_url=base_url, api_key=api_key)
        environment = None
        playwright = None
        browser = None
        page = None

        try:
            # Get simulator by name
            simulator = await get_simulator_by_name(base_url, api_key, simulator_name)
            simulator_id = simulator["id"]
            current_config = simulator.get("config", {})
            current_status = current_config.get("status", "not_started")

            console.print(f"[cyan]Current status:[/cyan] {current_status}")

            # Use provided artifact ID or fall back to base_artifact_id from config
            artifact_id = (
                artifact_id_input if artifact_id_input else current_config.get("base_artifact_id")
            )
            if not artifact_id:
                console.print(
                    "[red]❌ No artifact ID provided and simulator has no base_artifact_id set[/red]"
                )
                raise typer.Exit(1)

            console.print(f"[cyan]Using artifact:[/cyan] {artifact_id}")

            # Create environment
            console.print(
                f"[cyan]Creating {simulator_name} environment with artifact {artifact_id}...[/cyan]"
            )
            environment = await client.make_environment(
                simulator_name, artifact_id=artifact_id, timeout=int(3600.0)
            )
            console.print(f"[green]✅ Environment created: {environment.id}[/green]")

            # Wait for ready
            console.print("[cyan]Waiting for environment to be ready...[/cyan]")
            await environment.wait_for_ready(timeout=120.0)
            console.print("[green]✅ Environment is ready![/green]")

            # Reset
            console.print("[cyan]Resetting environment...[/cyan]")
            await environment.reset()
            console.print("[green]✅ Environment reset complete![/green]")

            # Get public URL
            public_url = await environment.get_public_url()
            console.print(f"[cyan]Public URL:[/cyan] {public_url}")

            # Launch Playwright browser (headless=False)
            console.print("[cyan]Launching browser...[/cyan]")
            playwright = await async_playwright().start()
            browser = await playwright.chromium.launch(headless=False)
            page = await browser.new_page()
            await page.goto(public_url)

            # Login
            try:
                await environment.login(page, from_api=True, throw_on_login_error=True)
                console.print("[green]✅ Logged into environment[/green]")
            except Exception as e:
                console.print(f"[yellow]⚠️  Login error: {e}[/yellow]")

            console.print("\n" + "=" * 60)
            console.print("[bold green]Environment Review Session Active[/bold green]")
            console.print("=" * 60)
            console.print("[bold]Commands:[/bold]")
            console.print("  - 'state' or 's': Show environment state")
            console.print("  - 'finish' or 'f': Exit loop and submit review outcome")
            console.print("=" * 60)
            console.print()

            # Interactive loop
            while True:
                try:
                    command = input("Enter command: ").strip().lower()

                    if command in ["finish", "f"]:
                        console.print("\n[yellow]Finishing review...[/yellow]")
                        break
                    elif command in ["state", "s"]:
                        console.print("\n[cyan]Getting environment state...[/cyan]")
                        try:
                            state = await environment.get_state()
                            console.print("\n[bold]Current Environment State:[/bold]")
                            console.print(json.dumps(state, indent=2))
                            console.print()
                        except Exception as e:
                            console.print(f"[red]❌ Error getting state: {e}[/red]")
                    else:
                        console.print("[yellow]Unknown command. Use 'state' or 'finish'[/yellow]")

                except KeyboardInterrupt:
                    console.print("\n[yellow]Interrupted! Finishing review...[/yellow]")
                    break

            # Prompt for outcome
            console.print("\n[bold]Choose outcome:[/bold]")
            console.print("  1. pass")
            console.print("  2. reject")
            console.print("  3. skip (no status update)")
            outcome_choice = typer.prompt("Choice [1/2/3]").strip()

            if outcome_choice == "1":
                outcome = "pass"
            elif outcome_choice == "2":
                outcome = "reject"
            elif outcome_choice == "3":
                console.print("[yellow]Review session ended without status update[/yellow]")
                return
            else:
                console.print("[red]❌ Invalid choice. Aborting.[/red]")
                raise typer.Exit(1)

            # Validate status BEFORE submitting outcome
            if outcome == "pass":
                validate_status_transition(
                    current_status, "env_review_requested", "review base pass"
                )
                new_status = "env_approved"
            else:
                validate_status_transition(
                    current_status, "env_review_requested", "review base reject"
                )
                new_status = "env_in_progress"

            # Build review payload (always include outcome; comments required on reject)
            comments = None
            if outcome == "reject":
                comments = ""
                while not comments:
                    comments = typer.prompt("Comments (required for reject)").strip()
                    if not comments:
                        console.print(
                            "[yellow]Comments are required when rejecting. Please provide feedback.[/yellow]"
                        )

            reviewer_user_id = None
            env_review_assignees = current_config.get("env_review_assignees", [])
            if env_review_assignees:
                reviewer_user_id = env_review_assignees[0]

            review_payload = {
                "review_type": "env",
                "outcome": outcome,
                "artifact_id": artifact_id,
                "comments": comments,
                "reviewer_user_id": reviewer_user_id,
            }

            # Submit review then transition status
            await post_simulator_review(
                base_url=base_url,
                api_key=api_key,
                simulator_id=simulator_id,
                review=review_payload,
            )
            await post_simulator_status(
                base_url=base_url,
                api_key=api_key,
                simulator_id=simulator_id,
                new_status=new_status,
            )

            console.print(f"[green]✅ Review submitted: {outcome}[/green]")
            console.print(f"[cyan]Status:[/cyan] {current_status} → {new_status}")

            # If passed, automatically tag data artifact as prod-latest
            if outcome == "pass":
                console.print("\n[cyan]Tagging artifact as prod-latest...[/cyan]")
                try:
                    import aiohttp

                    async with aiohttp.ClientSession() as session:
                        tag_response = await session.post(
                            f"{base_url}/simulator/update-tag",
                            headers={"X-API-Key": api_key, "Content-Type": "application/json"},
                            json={
                                "simulator_name": simulator_name,
                                "artifact_id": artifact_id,
                                "tag_name": "prod-latest",
                                "dataset": "base",
                            },
                        )
                        if tag_response.status == 200:
                            console.print(
                                f"[green]✅ Tagged {artifact_id[:8]}... as prod-latest[/green]"
                            )
                        else:
                            error_text = await tag_response.text()
                            console.print(
                                f"[yellow]⚠️  Could not tag as prod-latest: {error_text}[/yellow]"
                            )
                except Exception as e:
                    console.print(f"[yellow]⚠️  Could not tag as prod-latest: {e}[/yellow]")

        except Exception as e:
            console.print(f"[red]❌ Error during review session: {e}[/red]")
            raise

        finally:
            # Cleanup
            try:
                if page:
                    await page.close()
                if browser:
                    await browser.close()
                if playwright:
                    await playwright.stop()
            except Exception as e:
                console.print(f"[yellow]⚠️  Browser cleanup error: {e}[/yellow]")

            if environment:
                try:
                    console.print("[cyan]Shutting down environment...[/cyan]")
                    await environment.close()
                    console.print("[green]✅ Environment shut down[/green]")
                except Exception as e:
                    console.print(f"[yellow]⚠️  Environment cleanup error: {e}[/yellow]")

            try:
                await client.close()
            except Exception as e:
                console.print(f"[yellow]⚠️  Client cleanup error: {e}[/yellow]")

    handle_async(_review_base())


@submit_app.command(name="data")
def submit_data():
    """
    Submit data artifact for review after data generation.

    Worker manually specifies artifact ID for data review.
    Requires status: data_in_progress
    Transitions to: data_review_requested

    Example:
        plato submit data
    """
    # Get API key (hard fail if missing)
    api_key = os.getenv("PLATO_API_KEY")
    if not api_key:
        console.print("[red]❌ PLATO_API_KEY environment variable not set[/red]")
        console.print("\n[yellow]Set your API key:[/yellow]")
        console.print("  export PLATO_API_KEY='your-api-key-here'")
        raise typer.Exit(1)

    # Prompt for simulator name
    simulator_name = typer.prompt("Enter simulator name").strip()
    if not simulator_name:
        console.print("[red]❌ Simulator name is required[/red]")
        raise typer.Exit(1)

    # Prompt for artifact ID
    artifact_id = typer.prompt("Enter artifact ID").strip()
    if not artifact_id:
        console.print("[red]❌ Artifact ID is required[/red]")
        raise typer.Exit(1)

    async def _submit_data():
        base_url = "https://plato.so/api"

        # Get simulator by name
        simulator = await get_simulator_by_name(base_url, api_key, simulator_name)
        simulator_id = simulator["id"]
        current_config = simulator.get("config", {})
        current_status = current_config.get("status", "not_started")

        # Validate status transition (hard fail if wrong status)
        validate_status_transition(current_status, "data_in_progress", "submit data")

        # Show info and submit
        console.print(f"[cyan]Simulator:[/cyan]      {simulator_name}")
        console.print(f"[cyan]Artifact ID:[/cyan]    {artifact_id}")
        console.print(f"[cyan]Current Status:[/cyan] {current_status}")
        console.print()

        # Set data artifact, then request review
        await put_simulator_fields(
            base_url=base_url,
            api_key=api_key,
            simulator_id=simulator_id,
            payload={"data_artifact_id": artifact_id},
        )
        await post_simulator_status(
            base_url=base_url,
            api_key=api_key,
            simulator_id=simulator_id,
            new_status="data_review_requested",
        )

        console.print("[green]✅ Data review requested successfully![/green]")
        console.print(f"[cyan]Status:[/cyan] {current_status} → data_review_requested")
        console.print(f"[cyan]Data Artifact:[/cyan] {artifact_id}")

    handle_async(_submit_data())


# TEST/MOCK: This comment marks test-related code. Used for verification in release workflow.


@review_app.command(name="data")
def review_data():
    """
    Launch browser with EnvGen Recorder extension for data review.

    Opens Chrome with the extension installed and navigates to sims.plato.so.
    Use the extension to create sessions, record, and submit reviews.
    When done, simply close the browser to exit.

    Example:
        plato review data
    """
    # Get API key (hard fail if missing)
    api_key = os.getenv("PLATO_API_KEY")
    if not api_key:
        console.print("[red]❌ PLATO_API_KEY environment variable not set[/red]")
        console.print("\n[yellow]Set your API key:[/yellow]")
        console.print("  export PLATO_API_KEY='your-api-key-here'")
        raise typer.Exit(1)

    # Find Chrome extension source (hard fail if missing)
    # Always copy to temp directory to avoid cache issues
    package_dir = Path(__file__).resolve().parent  # src/plato/ or site-packages/plato/

    # Detect if we're in installed vs development mode
    is_installed = "site-packages" in str(package_dir)

    if is_installed:
        # Installed: Extension is bundled inside the package at plato/extensions/envgen-recorder
        extension_source_path = package_dir / "extensions" / "envgen-recorder"
    else:
        # Development: Extension is at repo root extensions/envgen-recorder
        # From src/plato/cli.py: plato -> src -> python -> plato-client
        repo_root = package_dir.parent.parent.parent  # plato-client/
        extension_source_path = repo_root / "extensions" / "envgen-recorder"

    # Optional fallback: PLATO_CLIENT_DIR environment variable (for edge cases)
    if not extension_source_path.exists():
        plato_client_dir_env = os.getenv("PLATO_CLIENT_DIR")
        if plato_client_dir_env:
            env_path = Path(plato_client_dir_env) / "extensions" / "envgen-recorder"
            if env_path.exists():
                extension_source_path = env_path

    if not extension_source_path.exists():
        console.print("[red]❌ EnvGen Recorder extension not found[/red]")
        console.print(f"\n[yellow]Expected location:[/yellow] {extension_source_path}")
        if is_installed:
            console.print("\n[yellow]The extension should be bundled inside the package.[/yellow]")
            console.print("This indicates a build/packaging issue.")
        else:
            console.print(
                "\n[yellow]Make sure you're running from the plato-client repository root.[/yellow]"
            )
        raise typer.Exit(1)

    # Always copy extension to temp directory to avoid cache issues
    # This ensures we always get fresh extension files, not cached versions
    temp_ext_dir = Path(tempfile.mkdtemp(prefix="plato-extension-"))
    extension_path = temp_ext_dir / "envgen-recorder"

    console.print("[cyan]Copying extension to temp directory (no cache)...[/cyan]")
    shutil.copytree(extension_source_path, extension_path, dirs_exist_ok=False)
    console.print(f"[green]✅ Extension copied to: {extension_path}[/green]")

    # Check Playwright (hard fail if missing)
    try:
        from playwright.async_api import async_playwright
    except ImportError:
        console.print("[red]❌ Playwright is not installed[/red]")
        console.print("\n[yellow]Install with:[/yellow]")
        console.print("  pip install playwright")
        console.print("  playwright install chromium")
        raise typer.Exit(1) from None

    async def _review_data():
        playwright = None
        browser = None

        try:
            # Use persistent profile so extension settings are saved
            user_data_dir = Path.home() / ".plato" / "chrome-data"
            user_data_dir.mkdir(parents=True, exist_ok=True)

            console.print("[cyan]Launching Chrome with EnvGen Recorder extension...[/cyan]")

            playwright = await async_playwright().start()

            # Use persistent context so extension settings persist
            browser = await playwright.chromium.launch_persistent_context(
                str(user_data_dir),
                headless=False,
                args=[
                    f"--disable-extensions-except={extension_path}",
                    f"--load-extension={extension_path}",
                ],
            )

            # Set API key in extension storage
            console.print("[cyan]Setting API key in extension storage...[/cyan]")
            await asyncio.sleep(1)  # Wait for extension to initialize

            try:
                # Find extension ID by checking existing pages
                extension_id = None
                for existing_page in browser.pages:
                    url = existing_page.url
                    if "chrome-extension://" in url:
                        parts = url.replace("chrome-extension://", "").split("/")
                        if parts:
                            extension_id = parts[0]
                            break

                # If not found, try to get extension ID via CDP Target.getTargets
                if not extension_id:
                    temp_page = await browser.new_page()
                    try:
                        cdp = await temp_page.context.new_cdp_session(temp_page)
                        # Get all targets including extension targets
                        targets_result = await cdp.send("Target.getTargets")
                        for target_info in targets_result.get("targetInfos", []):
                            target_url = target_info.get("url", "")
                            if "chrome-extension://" in target_url:
                                parts = target_url.replace("chrome-extension://", "").split("/")
                                if parts:
                                    extension_id = parts[0]
                                    break
                    except Exception as e:
                        console.print(f"[yellow]⚠️  CDP query failed: {e}[/yellow]")
                    finally:
                        await temp_page.close()

                # Set API key via extension's options page
                if extension_id:
                    temp_page = await browser.new_page()
                    try:
                        options_url = f"chrome-extension://{extension_id}/options.html"
                        await temp_page.goto(
                            options_url, wait_until="domcontentloaded", timeout=5000
                        )

                        # Fill in the API key field
                        await temp_page.fill("#platoApiKey", api_key)
                        await asyncio.sleep(0.2)

                        # Click save button to trigger the extension's save handler
                        # This ensures storage is set properly and all listeners are triggered
                        save_button = temp_page.locator('button:has-text("Save")')
                        if await save_button.count() > 0:
                            await save_button.click()
                            await asyncio.sleep(0.5)
                            console.print("[green]✅ API key set in extension storage[/green]")
                        else:
                            # Fallback: set directly if no save button found
                            await temp_page.evaluate(f"""
                                (async () => {{
                                    await chrome.storage.local.set({{ platoApiKey: {json.dumps(api_key)} }});
                                }})();
                            """)
                            await asyncio.sleep(0.5)
                            console.print(
                                "[green]✅ API key set in extension storage (direct)[/green]"
                            )
                    except Exception as e:
                        console.print(f"[yellow]⚠️  Could not set API key: {e}[/yellow]")
                    finally:
                        await temp_page.close()
                else:
                    console.print(
                        f"[yellow]⚠️  Could not find extension ID. Please set API key manually: {api_key}[/yellow]"
                    )
            except Exception as e:
                console.print(f"[yellow]⚠️  Could not auto-set API key: {e}[/yellow]")
                console.print(
                    f"[yellow]   Please configure manually in extension settings: {api_key}[/yellow]"
                )

            # Navigate to sims.plato.so
            page = await browser.new_page()
            await page.goto("https://sims.plato.so", wait_until="domcontentloaded")

            console.print("[green]✅ Browser launched with extension[/green]")
            console.print("[cyan]URL:[/cyan] https://sims.plato.so")
            console.print()
            console.print("[bold]Instructions:[/bold]")
            console.print("  1. Click the EnvGen Recorder extension icon")
            console.print("  2. Use the extension to create sessions, record, and submit reviews")
            console.print("  3. When done, close the browser window to exit")
            console.print()
            console.print(
                "[yellow]💡 The extension handles all recording and review submission[/yellow]"
            )
            console.print(
                "[yellow]💡 It's okay if sims.plato.so shows an error message - that's expected[/yellow]"
            )
            console.print()
            console.print("[bold]Press Control-C when done[/bold]")

            # Wait for user to close the browser
            # Simple approach: wait indefinitely until KeyboardInterrupt
            # The browser will stay open until user closes it manually
            try:
                # Wait indefinitely - user will close browser manually
                # Or press Ctrl+C to exit
                await asyncio.Event().wait()  # This waits forever
            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted by user[/yellow]")
            except Exception:
                # Any other exception - browser probably closed
                pass

            console.print("\n[green]✅ Browser closed. Review session ended.[/green]")

        except Exception as e:
            console.print(f"[red]❌ Error during review session: {e}[/red]")
            raise

        finally:
            # Cleanup
            try:
                if browser:
                    await browser.close()
                if playwright:
                    await playwright.stop()
                # Clean up temp extension directory
                if "temp_ext_dir" in locals() and temp_ext_dir.exists():
                    shutil.rmtree(temp_ext_dir, ignore_errors=True)
            except Exception as e:
                console.print(f"[yellow]⚠️  Browser cleanup error: {e}[/yellow]")

    handle_async(_review_data())


@app.command()
def flow(
    flow_name: str = typer.Option("login", "--flow-name", "-f", help="Name of the flow to execute"),
):
    """
    Execute a test flow against a simulator environment.

    Reads .sandbox.yaml to get the URL. Auto-detects flow file
    (flows.yaml, flows.yml, flow.yaml, flow.yml). Uses "login" as default flow name.

    Example:
        plato run-flow
    """
    from playwright.async_api import async_playwright

    from plato.flow_executor import FlowExecutor
    from plato.models.flow import Flow

    sandbox_file = Path.cwd() / ".sandbox.yaml"
    if not sandbox_file.exists():
        console.print("[red]❌ .sandbox.yaml not found[/red]")
        console.print("\n[yellow]Create a sandbox with: [bold]plato hub[/bold][/yellow]")
        raise typer.Exit(1)
    try:
        with open(sandbox_file) as f:
            sandbox_data = yaml.safe_load(f)
    except Exception as e:
        console.print(f"[red]❌ Error reading .sandbox.yaml: {e}[/red]")
        raise typer.Exit(1) from e

    url = sandbox_data.get("url")
    dataset = sandbox_data.get("dataset")
    if not url:
        console.print("[red]❌ .sandbox.yaml missing 'url'[/red]")
        raise typer.Exit(1)
    if not dataset:
        console.print("[red]❌ .sandbox.yaml missing 'dataset'[/red]")
        raise typer.Exit(1)

    plato_config_path = sandbox_data.get("plato_config_path")
    if not plato_config_path:
        console.print("[red]❌ .sandbox.yaml missing 'plato_config_path'[/red]")
        raise typer.Exit(1)
    try:
        with open(plato_config_path) as f:
            plato_config = yaml.safe_load(f)
    except Exception as e:
        console.print(f"[red]❌ Could not read plato-config.yml: {e}[/red]")
        raise typer.Exit(1) from e

    flow_file = None
    if dataset and "datasets" in plato_config:
        dataset_config = plato_config["datasets"].get(dataset, {})
        metadata = dataset_config.get("metadata", {})
        flows_path = metadata.get("flows_path")

        if flows_path:
            if not Path(flows_path).is_absolute():
                config_dir = Path(plato_config_path).parent
                flow_file = str(config_dir / flows_path)
            else:
                flow_file = flows_path
    if not flow_file or not Path(flow_file).exists():
        console.print("[red]❌ Flow file not found in plato-config[/red]")
        console.print(
            f"[yellow]Dataset '{dataset}' missing metadata.flows_path in plato-config.yml[/yellow]"
        )
        raise typer.Exit(1)
    with open(flow_file) as f:
        flow_dict = yaml.safe_load(f)

    console.print(f"[cyan]Flow file: {flow_file}[/cyan]")
    console.print(f"[cyan]URL: {url}[/cyan]")
    console.print(f"[cyan]Flow name: {flow_name}[/cyan]")

    flow = next(
        (
            Flow.model_validate(flow)
            for flow in flow_dict.get("flows", [])
            if flow.get("name") == flow_name
        ),
        None,
    )
    if not flow:
        console.print(f"[red]❌ Flow named '{flow_name}' not found in {flow_file}[/red]")
        raise typer.Exit(1)

    screenshots_dir = Path(flow_file).parent / "screenshots"

    async def _run():
        browser = None
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=False)
                page = await browser.new_page()
                await page.goto(url)
                executor = FlowExecutor(page, flow, screenshots_dir, logger=flow_logger)
                result = await executor.execute_flow()
                console.print("[green]✅ Flow executed successfully[/green]")
                return result
        except Exception as e:
            console.print(f"[red]❌ Flow execution failed: {e}[/red]")
            raise typer.Exit(1) from e
        finally:
            if browser:
                await browser.close()

    handle_async(_run())


@app.command()
def state():
    """Get the current state of the simulator environment (reads .sandbox.yaml)."""
    # Read .sandbox.yaml
    sandbox_file = Path.cwd() / ".sandbox.yaml"
    if not sandbox_file.exists():
        console.print("[red]❌ No .sandbox.yaml - run: plato hub[/red]")
        raise typer.Exit(1)

    with open(sandbox_file) as f:
        data = yaml.safe_load(f)

    job_group_id = data.get("job_group_id")
    if not job_group_id:
        console.print("[red]❌ .sandbox.yaml missing job_group_id[/red]")
        raise typer.Exit(1)

    # Get API key
    api_key = os.getenv("PLATO_API_KEY")
    if not api_key:
        console.print("[red]❌ PLATO_API_KEY not set[/red]")
        raise typer.Exit(1)

    async def _get_state():
        client = Plato(api_key=api_key)
        try:
            console.print(f"[cyan]Getting state for job_group_id: {job_group_id}[/cyan]")
            state = await client.get_environment_state(job_group_id, merge_mutations=False)

            console.print("\n[bold]Environment State:[/bold]")
            console.print(json.dumps(state, indent=2))
        finally:
            await client.close()

    handle_async(_get_state())


@app.command()
def audit_ui():
    """
    Launch Streamlit UI for auditing database ignore rules.

    Note: Requires streamlit to be installed:
        pip install streamlit psycopg2-binary pymysql

    Examples:
        plato audit-ui
    """
    # Check if streamlit is installed
    if not shutil.which("streamlit"):
        console.print("[red]❌ streamlit is not installed[/red]")
        console.print("\n[yellow]Install with:[/yellow]")
        console.print("  pip install streamlit psycopg2-binary pymysql")
        raise typer.Exit(1)

    # Find the audit_ui.py file d
    package_dir = Path(__file__).resolve().parent
    ui_file = package_dir / "audit_ui.py"

    if not ui_file.exists():
        console.print(f"[red]❌ UI file not found: {ui_file}[/red]")
        raise typer.Exit(1)

    console.print("[cyan]Launching Streamlit UI...[/cyan]")

    try:
        # Launch streamlit
        os.execvp("streamlit", ["streamlit", "run", str(ui_file)])
    except Exception as e:
        console.print(f"[red]❌ Failed to launch Streamlit: {e}[/red]")
        raise typer.Exit(1) from e


def main():
    """Main entry point for the Plato CLI."""
    app()


# ab


# Backward compatibility
cli = main

if __name__ == "__main__":
    main()
