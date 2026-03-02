"""Project Management CLI commands for Plato simulator workflow."""

import asyncio
import json
import os
import re
import shutil
import tempfile
from datetime import datetime, timedelta
from pathlib import Path

import httpx
import typer
import yaml
from rich.table import Table

from plato._generated.api.v1.env import get_simulator_by_name, get_simulators
from plato._generated.api.v1.organization import get_organization_members
from plato._generated.api.v1.simulator import (
    add_simulator_review,
    update_simulator,
    update_simulator_status,
    update_tag,
)
from plato._generated.models import (
    AddReviewRequest,
    AppApiV1SimulatorRoutesUpdateSimulatorRequest,
    Authentication,
    Outcome,
    ReviewType,
    SimReviewComment,
    UpdateStatusRequest,
    UpdateTagRequest,
)
from plato.cli.utils import (
    console,
    handle_async,
    read_plato_config,
    require_api_key,
    require_plato_config_field,
)
from plato.v1.flow_executor import FlowExecutor
from plato.v1.models.flow import Flow
from plato.v1.sdk import Plato

# =============================================================================
# CONSTANTS
# =============================================================================

# UUID pattern for detecting artifact IDs in sim:artifact notation
UUID_PATTERN = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE)

# =============================================================================
# APP STRUCTURE
# =============================================================================

pm_app = typer.Typer(help="Project management for simulator workflow")
list_app = typer.Typer(help="List simulators pending review")
review_app = typer.Typer(help="Review simulator artifacts")
submit_app = typer.Typer(help="Submit simulator artifacts for review")

pm_app.add_typer(list_app, name="list")
pm_app.add_typer(review_app, name="review")
pm_app.add_typer(submit_app, name="submit")


# =============================================================================
# SHARED HELPERS
# =============================================================================


def parse_simulator_artifact(
    simulator: str | None,
    artifact: str | None,
    require_artifact: bool = False,
    command_name: str = "command",
) -> tuple[str | None, str | None]:
    """
    Parse simulator and artifact from CLI args, supporting colon notation.

    Supports:
        -s simulator                    # Simulator only
        -s simulator -a <artifact-uuid> # Explicit artifact
        -s simulator:<artifact-uuid>    # Colon notation

    Args:
        simulator: The -s/--simulator arg value
        artifact: The -a/--artifact arg value
        require_artifact: If True, artifact is required
        command_name: Name of command for error messages

    Returns:
        (simulator_name, artifact_id) tuple
    """
    simulator_name = None
    artifact_id = artifact or ""

    if simulator:
        # Check for colon notation: sim:artifact
        if ":" in simulator:
            sim_part, colon_part = simulator.split(":", 1)
            simulator_name = sim_part
            if UUID_PATTERN.match(colon_part):
                artifact_id = colon_part
            else:
                console.print(f"[red]❌ Invalid artifact UUID after colon: '{colon_part}'[/red]")
                console.print()
                console.print("[yellow]Usage:[/yellow]")
                console.print(f"  plato pm {command_name} -s <simulator>                      # Simulator only")
                console.print(f"  plato pm {command_name} -s <simulator> -a <artifact-uuid>   # With artifact")
                console.print(f"  plato pm {command_name} -s <simulator>:<artifact-uuid>      # Colon notation")
                raise typer.Exit(1)
        else:
            simulator_name = simulator

    if not simulator_name:
        console.print("[red]❌ Simulator name is required[/red]")
        console.print()
        console.print("[yellow]Usage:[/yellow]")
        console.print(f"  plato pm {command_name} -s <simulator>                      # Simulator only")
        console.print(f"  plato pm {command_name} -s <simulator> -a <artifact-uuid>   # With artifact")
        console.print(f"  plato pm {command_name} -s <simulator>:<artifact-uuid>      # Colon notation")
        raise typer.Exit(1)

    if require_artifact and not artifact_id:
        console.print("[red]❌ Artifact ID is required[/red]")
        console.print()
        console.print("[yellow]Usage:[/yellow]")
        console.print(f"  plato pm {command_name} -s <simulator> -a <artifact-uuid>   # With artifact flag")
        console.print(f"  plato pm {command_name} -s <simulator>:<artifact-uuid>      # Colon notation")
        raise typer.Exit(1)

    return simulator_name, artifact_id or None


def _get_base_url() -> str:
    """Get base URL with /api suffix stripped."""
    base_url = os.getenv("PLATO_BASE_URL", "https://plato.so")
    if base_url.endswith("/api"):
        base_url = base_url[:-4]
    return base_url.rstrip("/")


def validate_status_transition(current_status: str, expected_status: str, command_name: str):
    """Validate that current status matches expected status for the command."""
    if current_status != expected_status:
        console.print(f"[red]❌ Invalid status for {command_name}[/red]")
        console.print(f"\n[yellow]Current status:[/yellow]  {current_status}")
        console.print(f"[yellow]Expected status:[/yellow] {expected_status}")
        console.print(f"\n[yellow]Cannot run {command_name} from status '{current_status}'[/yellow]")
        raise typer.Exit(1)


# =============================================================================
# LIST COMMANDS
# =============================================================================


def _list_pending_reviews(review_type: str):
    """Shared logic for listing pending reviews."""
    api_key = require_api_key()

    target_status = "env_review_requested" if review_type == "base" else "data_review_requested"

    async def _list_reviews():
        base_url = _get_base_url()

        async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as client:
            simulators = await get_simulators.asyncio(
                client=client,
                x_api_key=api_key,
            )

            # Fetch organization members to map user IDs to usernames
            user_id_to_name: dict[int, str] = {}
            try:
                members = await get_organization_members.asyncio(
                    client=client,
                    x_api_key=api_key,
                )
                for member in members:
                    user_id = member.get("id")
                    username = member.get("username") or member.get("email", "")
                    if user_id is not None:
                        user_id_to_name[user_id] = username
            except Exception:
                pass  # Continue without usernames if fetch fails

            # Filter by target status
            pending_review = []
            for sim in simulators:
                config = sim.get("config", {}) if isinstance(sim, dict) else getattr(sim, "config", {})
                status = config.get("status", "not_started") if isinstance(config, dict) else "not_started"
                if status == target_status:
                    pending_review.append(sim)

            if not pending_review:
                console.print(f"[yellow]No simulators pending {review_type} review (status: {target_status})[/yellow]")
                return

            # Build table
            table = Table(title=f"Simulators Pending {review_type.title()} Review")
            table.add_column("Name", style="cyan", no_wrap=True)
            table.add_column("Assignees", style="magenta", no_wrap=True)
            table.add_column("Notes", style="white", max_width=40)
            artifact_col_name = "base_artifact_id" if review_type == "base" else "data_artifact_id"
            table.add_column(artifact_col_name, style="green", no_wrap=True)

            for sim in pending_review:
                if isinstance(sim, dict):
                    name = sim.get("name", "N/A")
                    config = sim.get("config", {})
                else:
                    name = getattr(sim, "name", "N/A")
                    config = getattr(sim, "config", {})

                notes = config.get("notes", "") if isinstance(config, dict) else ""
                notes = notes or "-"
                artifact_key = "base_artifact_id" if review_type == "base" else "data_artifact_id"
                artifact_id = config.get(artifact_key, "") if isinstance(config, dict) else ""
                artifact_id = artifact_id or "-"

                # Get assignees based on review type (env_assignees for base, data_assignees for data)
                assignee_key = "env_assignees" if review_type == "base" else "data_assignees"
                assignee_ids = config.get(assignee_key, []) if isinstance(config, dict) else []
                assignee_names = []
                if assignee_ids:
                    for uid in assignee_ids:
                        assignee_names.append(user_id_to_name.get(uid, str(uid)))
                assignees_str = ", ".join(assignee_names) if assignee_names else "-"

                table.add_row(name, assignees_str, notes, artifact_id)

            console.print(table)
            console.print(f"\n[cyan]Total: {len(pending_review)} simulator(s) pending {review_type} review[/cyan]")

    handle_async(_list_reviews())


@list_app.command(name="base")
def list_base():
    """List simulators pending base/environment review.

    Shows simulators with status 'env_review_requested' in a table format.
    Displays name, assignees, notes, and base_artifact_id for each simulator.
    """
    _list_pending_reviews("base")


@list_app.command(name="data")
def list_data():
    """List simulators pending data review.

    Shows simulators with status 'data_review_requested' in a table format.
    Displays name, assignees, notes, and data_artifact_id for each simulator.
    """
    _list_pending_reviews("data")


# =============================================================================
# REVIEW COMMANDS
# =============================================================================


@review_app.command(name="base")
def review_base(
    simulator: str = typer.Option(
        None,
        "--simulator",
        "-s",
        help="Simulator name. Supports colon notation: -s sim:<artifact-uuid>",
    ),
    artifact: str = typer.Option(
        None,
        "--artifact",
        "-a",
        help="Artifact UUID to review. If not provided, uses server's base_artifact_id.",
    ),
    skip_review: bool = typer.Option(
        False,
        "--skip-review",
        help="Run login flow and check state, but skip interactive review. For automated verification.",
    ),
    local: str = typer.Option(
        None,
        "--local",
        "-l",
        help="Path to a local flow YAML file to run instead of the default login flow.",
    ),
    clock: str = typer.Option(
        None,
        "--clock",
        help="Set fake browser time (ISO format or offset like '-30d' for 30 days ago).",
    ),
):
    """Review base/environment artifact for a simulator.

    Creates an environment from the artifact, launches a browser for testing,
    runs the login flow, and checks for database mutations. After testing,
    choose pass (→ env_approved) or reject (→ env_in_progress).

    Requires simulator status: env_review_requested

    Options:
        -s, --simulator: Simulator name. Supports colon notation for artifact:
            '-s sim' (uses server's base_artifact_id) or '-s sim:<uuid>'
        -a, --artifact: Explicit artifact UUID to review. Overrides server's value.
        --skip-review: Run automated checks without interactive review session.
    """
    api_key = require_api_key()

    # Parse simulator and artifact from args (artifact not required - falls back to server config)
    simulator_name, artifact_id_input = parse_simulator_artifact(
        simulator, artifact, require_artifact=False, command_name="review base"
    )

    async def _review_base():
        import warnings

        base_url = _get_base_url()
        # v1 SDK expects base_url to include /api suffix
        v1_base_url = f"{base_url}/api"
        # Suppress the deprecation warning from v1 Plato
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            plato = Plato(api_key=api_key, base_url=v1_base_url)
        env = None
        playwright = None
        browser = None

        try:
            # simulator_name is guaranteed set by parse_simulator_artifact (or we exit)
            assert simulator_name is not None, "simulator_name must be set"

            # Get simulator by name using httpx for API calls
            async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as http_client:
                sim = await get_simulator_by_name.asyncio(
                    client=http_client,
                    name=simulator_name,
                    x_api_key=api_key,
                )
            simulator_id = sim.id
            current_config = sim.config or {}
            current_status = current_config.get("status", "not_started")

            console.print(f"[cyan]Current status:[/cyan] {current_status}")

            # Use provided artifact ID or fall back to base_artifact_id from server config
            artifact_id: str | None = artifact_id_input if artifact_id_input else current_config.get("base_artifact_id")
            if not artifact_id:
                console.print("[red]❌ No artifact ID provided.[/red]")
                console.print(
                    "[yellow]This simulator hasn't been submitted yet, so there's no base artifact on record.[/yellow]"
                )
                console.print(
                    "[yellow]Specify the artifact ID from your snapshot using: plato pm review base --artifact <artifact_id>[/yellow]"
                )
                raise typer.Exit(1)

            console.print(f"[cyan]Using artifact:[/cyan] {artifact_id}")

            # Try to create environment from artifact using v1 API
            try:
                console.print(f"[cyan]Creating {simulator_name} environment with artifact {artifact_id}...[/cyan]")
                env = await plato.make_environment(
                    env_id=simulator_name,
                    artifact_id=artifact_id,
                )
                console.print(f"[green]✅ Environment created: {env.id}[/green]")

                # Wait for environment to be ready
                console.print("[cyan]Waiting for environment to be ready...[/cyan]")
                await env.wait_for_ready(timeout=300)
                console.print("[green]✅ Environment ready![/green]")

                # Reset
                console.print("[cyan]Resetting environment...[/cyan]")
                await env.reset()
                console.print("[green]✅ Environment reset complete![/green]")

                # Get public URL (v1 returns string directly)
                public_url = await env.get_public_url()
                console.print(f"[cyan]Public URL:[/cyan] {public_url}")

                # Launch Playwright browser and login
                console.print("[cyan]Launching browser and logging in...[/cyan]")
                from playwright.async_api import async_playwright

                # Clear existing browser data for a fresh session
                user_data_dir = Path.home() / ".plato" / "chrome-data-base"
                if user_data_dir.exists():
                    shutil.rmtree(user_data_dir, ignore_errors=True)
                user_data_dir.mkdir(parents=True, exist_ok=True)

                playwright = await async_playwright().start()
                browser = await playwright.chromium.launch_persistent_context(
                    str(user_data_dir),
                    headless=False,
                )

                # Install fake clock if requested
                fake_time: datetime | None = None
                if clock:
                    # Parse clock option: ISO format or offset like '-30d'
                    if clock.startswith("-") and clock[-1] in "dhms":
                        # Offset format: -30d, -1h, -30m, -60s
                        unit = clock[-1]
                        amount = int(clock[1:-1])
                        if unit == "d":
                            fake_time = datetime.now() - timedelta(days=amount)
                        elif unit == "h":
                            fake_time = datetime.now() - timedelta(hours=amount)
                        elif unit == "m":
                            fake_time = datetime.now() - timedelta(minutes=amount)
                        elif unit == "s":
                            fake_time = datetime.now() - timedelta(seconds=amount)
                        else:
                            raise ValueError(f"Invalid clock offset unit: {unit}")
                    else:
                        # ISO format
                        fake_time = datetime.fromisoformat(clock)

                    assert fake_time is not None, f"Failed to parse clock value: {clock}"
                    console.print(f"[cyan]Setting fake browser time to:[/cyan] {fake_time.isoformat()}")

                if local:
                    # Use local flow file instead of default login
                    local_path = Path(local)
                    if not local_path.exists():
                        console.print(f"[red]❌ Local flow file not found: {local}[/red]")
                        raise typer.Exit(1)

                    console.print(f"[cyan]Loading local flow from: {local}[/cyan]")
                    with open(local_path) as f:
                        flow_dict = yaml.safe_load(f)

                    # Find login flow (or first flow if only one)
                    flows = flow_dict.get("flows", [])
                    if not flows:
                        console.print("[red]❌ No flows found in flow file[/red]")
                        raise typer.Exit(1)

                    # Try to find 'login' flow, otherwise use first flow
                    flow_data = next((f for f in flows if f.get("name") == "login"), flows[0])
                    flow = Flow.model_validate(flow_data)
                    console.print(f"[cyan]Running flow: {flow.name}[/cyan]")

                    # Create page and navigate to public URL
                    page = await browser.new_page()

                    # Install fake clock if requested
                    if fake_time:
                        await page.clock.install(time=fake_time)
                        console.print(f"[green]✅ Fake clock installed: {fake_time.isoformat()}[/green]")

                    if public_url:
                        await page.goto(public_url)

                    # Execute the flow
                    try:
                        executor = FlowExecutor(page, flow)
                        await executor.execute()
                        console.print("[green]✅ Local flow executed successfully[/green]")
                    except Exception as e:
                        console.print(f"[yellow]⚠️  Flow execution error: {e}[/yellow]")
                else:
                    # Use default login via env.login() (v1 API takes Page, not Browser)
                    if fake_time:
                        console.print("[yellow]⚠️  --clock with default login may not work correctly.[/yellow]")
                        console.print("[yellow]   Use --local with a flow file for reliable clock testing.[/yellow]")
                    try:
                        # Create page and navigate to public URL first
                        page = await browser.new_page()
                        if fake_time:
                            await page.clock.install(time=fake_time)
                            console.print(f"[green]✅ Fake clock installed: {fake_time.isoformat()}[/green]")
                        if public_url:
                            await page.goto(public_url)
                        # v1 login takes a Page and uses from_api=True to fetch flows from server
                        await env.login(page, dataset="base", from_api=True)
                        console.print("[green]✅ Logged into environment[/green]")
                    except Exception as e:
                        console.print(f"[yellow]⚠️  Login error: {e}[/yellow]")
                        # Page already created above, just navigate if not already done
                        if public_url and page:
                            try:
                                await page.goto(public_url)
                            except Exception:
                                pass

                # ALWAYS check state after login to verify no mutations
                console.print("\n[cyan]Checking environment state after login...[/cyan]")
                has_mutations = False
                has_errors = False
                try:
                    # v1 API: env.get_state() returns state dict directly
                    state_data = await env.get_state(merge_mutations=True)
                    console.print(f"\n[bold cyan]Environment {env.id}:[/bold cyan]")

                    if isinstance(state_data, dict):
                        # Check for error in state response (only if error has a truthy value)
                        if state_data.get("error"):
                            has_errors = True
                            console.print("\n[bold red]❌ State API Error:[/bold red]")
                            console.print(f"[red]{state_data['error']}[/red]")
                        else:
                            mutations = state_data.pop("mutations", [])
                            console.print("\n[bold]State:[/bold]")
                            console.print(json.dumps(state_data, indent=2, default=str))
                            if mutations:
                                has_mutations = True
                                console.print(f"\n[bold red]Mutations ({len(mutations)}):[/bold red]")
                                console.print(json.dumps(mutations, indent=2, default=str))
                            else:
                                console.print("\n[green]No mutations recorded[/green]")
                    else:
                        console.print(f"[yellow]Unexpected state format: {type(state_data)}[/yellow]")

                    if has_errors:
                        console.print("\n[bold red]❌ State check failed due to errors![/bold red]")
                        console.print("[yellow]The worker may not be properly connected.[/yellow]")
                    elif has_mutations:
                        console.print("\n[bold red]⚠️  WARNING: Login flow created mutations![/bold red]")
                        console.print("[yellow]The login flow should NOT modify database state.[/yellow]")
                    else:
                        console.print("\n[bold green]✅ Login flow verified - no mutations created[/bold green]")
                except Exception as e:
                    console.print(f"[red]❌ Error getting state: {e}[/red]")

                # If skip_review, exit without interactive loop
                if skip_review:
                    console.print("\n[cyan]Skipping interactive review (--skip-review)[/cyan]")
                    return

                console.print("\n" + "=" * 60)
                console.print("[bold green]Environment Review Session Active[/bold green]")
                console.print("=" * 60)
                console.print("[bold]Commands:[/bold]")
                console.print("  - 'state' or 's': Show environment state and mutations")
                console.print("  - 'finish' or 'f': Exit loop and submit review outcome")
                console.print("=" * 60)

                # Show recent env review if available
                reviews = current_config.get("reviews") or []
                env_reviews = [r for r in reviews if r.get("review_type") == "env"]
                if env_reviews:
                    env_reviews.sort(key=lambda r: r.get("timestamp_iso", ""), reverse=True)
                    recent_review = env_reviews[0]
                    outcome = recent_review.get("outcome", "unknown")
                    timestamp = recent_review.get("timestamp_iso", "")[:10]
                    console.print()
                    if outcome == "reject":
                        console.print(f"[bold red]📋 Most Recent Base Review: REJECTED[/bold red] ({timestamp})")
                    else:
                        console.print(f"[bold green]📋 Most Recent Base Review: PASSED[/bold green] ({timestamp})")
                    comments = recent_review.get("comments")
                    if comments:
                        console.print(f"[yellow]Reviewer Comments:[/yellow] {comments}")

                console.print()

                # Interactive loop
                while True:
                    try:
                        command = input("Enter command: ").strip().lower()

                        if command in ["finish", "f"]:
                            console.print("\n[yellow]Finishing review...[/yellow]")
                            break
                        elif command in ["state", "s"]:
                            console.print("\n[cyan]Getting environment state with mutations...[/cyan]")
                            try:
                                # v1 API: env.get_state() returns state dict directly
                                state_data = await env.get_state(merge_mutations=True)
                                console.print(f"\n[bold cyan]Environment {env.id}:[/bold cyan]")

                                if isinstance(state_data, dict):
                                    # Check for error in state response (only if error has a truthy value)
                                    if state_data.get("error"):
                                        console.print("\n[bold red]❌ State API Error:[/bold red]")
                                        console.print(f"[red]{state_data['error']}[/red]")
                                    else:
                                        mutations = state_data.pop("mutations", [])
                                        console.print("\n[bold]State:[/bold]")
                                        console.print(json.dumps(state_data, indent=2, default=str))
                                        if mutations:
                                            console.print(f"\n[bold]Mutations ({len(mutations)}):[/bold]")
                                            console.print(json.dumps(mutations, indent=2, default=str))
                                        else:
                                            console.print("\n[yellow]No mutations recorded[/yellow]")
                                else:
                                    console.print(json.dumps(state_data, indent=2, default=str))
                                console.print()
                            except Exception as e:
                                console.print(f"[red]❌ Error getting state: {e}[/red]")
                        else:
                            console.print("[yellow]Unknown command. Use 'state' or 'finish'[/yellow]")

                    except KeyboardInterrupt:
                        console.print("\n[yellow]Interrupted! Finishing review...[/yellow]")
                        break

            except Exception as env_error:
                console.print(f"[yellow]⚠️  Environment creation failed: {env_error}[/yellow]")
                console.print("[yellow]You can still submit a review without testing the environment.[/yellow]")

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
                validate_status_transition(current_status, "env_review_requested", "review base pass")
                new_status = "env_approved"
            else:
                validate_status_transition(current_status, "env_review_requested", "review base reject")
                new_status = "env_in_progress"

            # Create httpx client for API calls
            async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as api_client:
                # Update status
                await update_simulator_status.asyncio(
                    client=api_client,
                    simulator_id=simulator_id,
                    body=UpdateStatusRequest(status=new_status),
                    x_api_key=api_key,
                )

                # Add review if rejecting
                if outcome == "reject":
                    comments = ""
                    while not comments:
                        comments = typer.prompt("Comments (required for reject)").strip()
                        if not comments:
                            console.print(
                                "[yellow]Comments are required when rejecting. Please provide feedback.[/yellow]"
                            )

                    await add_simulator_review.asyncio(
                        client=api_client,
                        simulator_id=simulator_id,
                        body=AddReviewRequest(
                            review_type=ReviewType.env,
                            outcome=Outcome.reject,
                            artifact_id=artifact_id,
                            sim_comments=[SimReviewComment(comment=comments)],
                        ),
                        x_api_key=api_key,
                    )

                console.print(f"[green]✅ Review submitted: {outcome}[/green]")
                console.print(f"[cyan]Status:[/cyan] {current_status} → {new_status}")

                # If passed, automatically tag artifact as prod-latest
                if outcome == "pass" and artifact_id:
                    console.print("\n[cyan]Tagging artifact as prod-latest...[/cyan]")
                    try:
                        # simulator_name and artifact_id are guaranteed to be set at this point
                        assert simulator_name is not None
                        await update_tag.asyncio(
                            client=api_client,
                            body=UpdateTagRequest(
                                simulator_name=simulator_name,
                                artifact_id=artifact_id,
                                tag_name="prod-latest",
                                dataset="base",
                            ),
                            x_api_key=api_key,
                        )
                        console.print(f"[green]✅ Tagged {artifact_id[:8]}... as prod-latest[/green]")
                    except Exception as e:
                        console.print(f"[yellow]⚠️  Could not tag as prod-latest: {e}[/yellow]")

        except typer.Exit:
            raise
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
            except Exception as e:
                console.print(f"[yellow]⚠️  Browser cleanup error: {e}[/yellow]")

            if env:
                try:
                    console.print("[cyan]Shutting down environment...[/cyan]")
                    await env.close()
                    console.print("[green]✅ Environment shut down[/green]")
                except Exception as e:
                    console.print(f"[yellow]⚠️  Environment cleanup error: {e}[/yellow]")

            try:
                await plato.close()
            except Exception as e:
                console.print(f"[yellow]⚠️  Client cleanup error: {e}[/yellow]")

    handle_async(_review_base())


@review_app.command(name="data")
def review_data(
    simulator: str = typer.Option(
        None,
        "--simulator",
        "-s",
        help="Simulator name. Supports colon notation: -s sim:<artifact-uuid>",
    ),
    artifact: str = typer.Option(
        None,
        "--artifact",
        "-a",
        help="Artifact UUID to review. If not provided, uses server's data_artifact_id.",
    ),
):
    """
    Launch browser with Data Review extension for data review.

    Opens Chrome with the Data Review extension installed for reviewing
    data artifacts. Close the browser when done.

    SPECIFYING SIMULATOR AND ARTIFACT:

        -s <simulator>                      Use server's data_artifact_id
        -s <simulator> -a <artifact-uuid>   Explicit artifact
        -s <simulator>:<artifact-uuid>      Colon notation (same as above)

    EXAMPLES:

        plato pm review data -s fathom
        plato pm review data -s fathom -a e9c25ca5-1234-5678-9abc-def012345678
        plato pm review data -s fathom:e9c25ca5-1234-5678-9abc-def012345678

    Requires simulator status: data_review_requested
    """
    api_key = require_api_key()

    # Parse simulator and artifact from args (artifact not required - falls back to server config)
    simulator_name, artifact_id = parse_simulator_artifact(
        simulator, artifact, require_artifact=False, command_name="review data"
    )

    console.print(f"[cyan]Simulator:[/cyan] {simulator_name}")

    # Fetch simulator config and get artifact ID if not provided
    data_reviews = []

    async def _fetch_artifact_info():
        nonlocal artifact_id
        # simulator_name is guaranteed set by parse_simulator_artifact (or we exit)
        assert simulator_name is not None, "simulator_name must be set"

        base_url = _get_base_url()
        async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as client:
            try:
                sim = await get_simulator_by_name.asyncio(
                    client=client,
                    name=simulator_name,
                    x_api_key=api_key,
                )
                config = sim.config or {}

                # If no artifact provided, try to get data_artifact_id from server
                if not artifact_id:
                    artifact_id = config.get("data_artifact_id")
                    if artifact_id:
                        console.print(f"[cyan]Using data_artifact_id from server:[/cyan] {artifact_id}")
                    else:
                        console.print("[yellow]No artifact specified and no data_artifact_id on server[/yellow]")

                # Find all data reviews, sorted by most recent first
                reviews = config.get("reviews") or []
                found_reviews = [r for r in reviews if r.get("review_type") == "data"]
                if found_reviews:
                    found_reviews.sort(key=lambda r: r.get("timestamp_iso", ""), reverse=True)
                    return found_reviews
            except Exception as e:
                console.print(f"[yellow]⚠️  Could not fetch simulator info: {e}[/yellow]")
            return []

    data_reviews = handle_async(_fetch_artifact_info())

    if artifact_id:
        console.print(f"[cyan]Artifact:[/cyan] {artifact_id}")

    # Find Chrome extension source
    package_dir = Path(__file__).resolve().parent.parent  # plato/
    is_installed = "site-packages" in str(package_dir)

    if is_installed:
        extension_source_path = package_dir / "extensions" / "data-review"
    else:
        repo_root = package_dir.parent.parent  # plato-client/
        extension_source_path = repo_root / "extensions" / "data-review"

    # Fallback to env var
    if not extension_source_path.exists():
        plato_client_dir_env = os.getenv("PLATO_CLIENT_DIR")
        if plato_client_dir_env:
            env_path = Path(plato_client_dir_env) / "extensions" / "data-review"
            if env_path.exists():
                extension_source_path = env_path

    if not extension_source_path.exists():
        console.print("[red]❌ Data Review extension not found[/red]")
        console.print(f"\n[yellow]Expected location:[/yellow] {extension_source_path}")
        raise typer.Exit(1)

    # Copy extension to temp directory
    temp_ext_dir = Path(tempfile.mkdtemp(prefix="plato-extension-"))
    extension_path = temp_ext_dir / "data-review"

    console.print("[cyan]Copying extension to temp directory...[/cyan]")
    shutil.copytree(extension_source_path, extension_path, dirs_exist_ok=False)
    console.print(f"[green]✅ Extension copied to: {extension_path}[/green]")

    async def _review_data():
        import warnings

        base_url = _get_base_url()
        # v1 SDK expects base_url to include /api suffix
        v1_base_url = f"{base_url}/api"
        # Suppress the deprecation warning from v1 Plato
        with warnings.catch_warnings():
            warnings.simplefilter("ignore", DeprecationWarning)
            plato = Plato(api_key=api_key, base_url=v1_base_url)
        env = None
        playwright = None
        browser = None

        try:
            # Check if we have an artifact ID to create a session
            if not artifact_id:
                console.print("[red]❌ No artifact ID available. Cannot create session.[/red]")
                console.print("[yellow]Specify artifact with: plato pm review data -s simulator:artifact_id[/yellow]")
                raise typer.Exit(1)

            # Create environment with artifact using v1 API
            assert simulator_name is not None, "simulator_name must be set"
            console.print(f"[cyan]Creating {simulator_name} environment with artifact {artifact_id}...[/cyan]")
            env = await plato.make_environment(
                env_id=simulator_name,
                artifact_id=artifact_id,
            )
            console.print(f"[green]✅ Session created: {env.id}[/green]")

            # Wait for environment to be ready
            console.print("[cyan]Waiting for environment to be ready...[/cyan]")
            await env.wait_for_ready(timeout=300)
            console.print("[green]✅ Environment ready![/green]")

            # Reset environment
            console.print("[cyan]Resetting environment...[/cyan]")
            await env.reset()
            console.print("[green]✅ Environment reset complete![/green]")

            # Get public URL
            public_url = await env.get_public_url()
            console.print(f"[cyan]Public URL:[/cyan] {public_url}")

            user_data_dir = Path.home() / ".plato" / "chrome-data"
            # Clear existing browser data for a fresh session
            if user_data_dir.exists():
                shutil.rmtree(user_data_dir, ignore_errors=True)
            user_data_dir.mkdir(parents=True, exist_ok=True)

            console.print("[cyan]Launching Chrome with Data Review extension...[/cyan]")

            from playwright.async_api import async_playwright

            playwright = await async_playwright().start()

            browser = await playwright.chromium.launch_persistent_context(
                str(user_data_dir),
                headless=False,
                args=[
                    f"--disable-extensions-except={extension_path}",
                    f"--load-extension={extension_path}",
                ],
            )

            # Wait for extension to load
            await asyncio.sleep(2)

            # Find extension ID via CDP
            extension_id = None
            temp_page = await browser.new_page()
            try:
                cdp = await temp_page.context.new_cdp_session(temp_page)
                targets_result = await cdp.send("Target.getTargets")
                for target_info in targets_result.get("targetInfos", []):
                    ext_url = target_info.get("url", "")
                    if "chrome-extension://" in ext_url:
                        parts = ext_url.replace("chrome-extension://", "").split("/")
                        if parts:
                            extension_id = parts[0]
                            break
            except Exception as e:
                console.print(f"[yellow]⚠️  CDP query failed: {e}[/yellow]")
            finally:
                await temp_page.close()

            if extension_id:
                console.print("[green]✅ Extension loaded[/green]")
            else:
                console.print("[yellow]⚠️  Could not find extension ID. Please set API key manually.[/yellow]")

            # Navigate to public URL and auto-login
            console.print("[cyan]Opening environment...[/cyan]")
            main_page = await browser.new_page()
            if public_url:
                await main_page.goto(public_url)
                console.print(f"[green]✅ Loaded: {public_url}[/green]")

            # Auto-login using env.login() (same as review base)
            console.print("[cyan]Logging into environment...[/cyan]")
            try:
                await env.login(main_page, dataset="base", from_api=True)
                console.print("[green]✅ Logged into environment[/green]")
            except Exception as e:
                console.print(f"[yellow]⚠️  Auto-login failed: {e}[/yellow]")
                console.print("[yellow]   You may need to log in manually[/yellow]")

            # Check state after login to verify no mutations
            console.print("\n[cyan]Checking environment state after login...[/cyan]")
            try:
                state_data = await env.get_state(merge_mutations=True)
                console.print(f"\n[bold cyan]Environment {env.id}:[/bold cyan]")

                if isinstance(state_data, dict):
                    if state_data.get("error"):
                        console.print("\n[bold red]❌ State API Error:[/bold red]")
                        console.print(f"[red]{state_data['error']}[/red]")
                        console.print("[yellow]The worker may not be properly connected.[/yellow]")
                    else:
                        mutations = state_data.pop("mutations", [])
                        console.print("\n[bold]State:[/bold]")
                        console.print(json.dumps(state_data, indent=2, default=str))
                        if mutations:
                            console.print(f"\n[bold red]⚠️  Mutations ({len(mutations)}):[/bold red]")
                            console.print(json.dumps(mutations, indent=2, default=str))
                        else:
                            console.print("\n[green]No mutations recorded[/green]")
                else:
                    console.print(f"[yellow]Unexpected state format: {type(state_data)}[/yellow]")
            except Exception as e:
                console.print(f"[red]❌ Error getting state: {e}[/red]")

            # Use options page to set API key
            if extension_id:
                options_page = await browser.new_page()
                try:
                    await options_page.goto(
                        f"chrome-extension://{extension_id}/options.html",
                        wait_until="domcontentloaded",
                        timeout=5000,
                    )

                    # Set API key
                    await options_page.fill("#platoApiKey", api_key)
                    save_button = options_page.locator('button:has-text("Save")')
                    if await save_button.count() > 0:
                        await save_button.click()
                        await asyncio.sleep(0.3)
                    console.print("[green]✅ API key saved[/green]")

                except Exception as e:
                    console.print(f"[yellow]⚠️  Could not set up extension: {e}[/yellow]")
                finally:
                    await options_page.close()

            # Bring main page to front
            if main_page:
                await main_page.bring_to_front()

            console.print()
            console.print("[bold]Instructions:[/bold]")
            console.print("  1. Click the Data Review extension icon to open the sidebar")
            console.print(f"  2. Enter '{simulator_name}' as the simulator name and click Start Review")
            console.print("  3. Take screenshots and add comments for any issues")
            console.print("  4. Select Pass or Reject and submit the review")
            console.print("  5. When done, press Control-C to exit")

            # Show all data reviews if available
            if data_reviews:
                console.print()
                console.print("=" * 60)
                console.print(f"[bold]📋 Data Reviews ({len(data_reviews)}):[/bold]")
                for review in data_reviews:
                    outcome = review.get("outcome", "unknown")
                    timestamp = review.get("timestamp_iso", "")[:10]  # Just the date
                    if outcome == "reject":
                        console.print(f"\n[red]REJECTED[/red] ({timestamp})")
                    else:
                        console.print(f"\n[green]PASSED[/green] ({timestamp})")

                    # Handle both old 'comments' field and new 'sim_comments' structure
                    sim_comments = review.get("sim_comments")
                    if sim_comments:
                        for item in sim_comments:
                            comment_text = item.get("comment", "")
                            if comment_text:
                                console.print(f"  - {comment_text}")
                    else:
                        # Fallback to old comments field
                        comments = review.get("comments")
                        if comments:
                            console.print(f"  {comments}")
                console.print("=" * 60)

            console.print()
            console.print("[bold]Press Control-C when done[/bold]")

            try:
                await asyncio.Event().wait()
            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted by user[/yellow]")
            except Exception:
                pass

            console.print("\n[green]✅ Browser closed. Review session ended.[/green]")

        except Exception as e:
            console.print(f"[red]❌ Error during review session: {e}[/red]")
            raise

        finally:
            try:
                if env:
                    await env.close()
                if browser:
                    await browser.close()
                if playwright:
                    await playwright.stop()
                if temp_ext_dir.exists():
                    shutil.rmtree(temp_ext_dir, ignore_errors=True)
            except Exception as e:
                console.print(f"[yellow]⚠️  Cleanup error: {e}[/yellow]")

    handle_async(_review_data())


# =============================================================================
# SUBMIT COMMANDS
# =============================================================================


@submit_app.command(name="base")
def submit_base():
    """Submit base/environment artifact for review after snapshot.

    Reads simulator name and artifact_id from .plato/state.json, syncs metadata from
    plato-config.yml to the server, and transitions status to env_review_requested.
    Run from the simulator directory after creating a snapshot.

    Requires simulator status: env_in_progress
    No arguments needed - reads everything from .plato/state.json and plato-config.yml.
    """
    api_key = require_api_key()

    # Read sandbox state from .plato/state.json (written by plato sandbox snapshot)
    state_file = Path(".plato/state.json")
    if not state_file.exists():
        console.print("[red]No .plato/state.json found[/red]")
        console.print("[yellow]Run 'plato sandbox snapshot' first.[/yellow]")
        raise typer.Exit(1)
    sandbox_data = json.loads(state_file.read_text())

    artifact_id = sandbox_data.get("artifact_id")
    if not artifact_id:
        console.print("[red]No artifact_id in .plato/state.json[/red]")
        console.print("[yellow]Run 'plato sandbox snapshot' to create one.[/yellow]")
        raise typer.Exit(1)

    plato_config_path = sandbox_data.get("plato_config_path", "plato-config.yml")

    # Read plato-config.yml to get simulator name and metadata
    plato_config = read_plato_config(plato_config_path)
    simulator_name = require_plato_config_field(plato_config, "service")

    # Extract metadata from plato-config.yml
    datasets = plato_config.get("datasets", {})
    base_dataset = datasets.get("base", {})
    metadata = base_dataset.get("metadata", {})

    # Get metadata fields
    config_description = metadata.get("description")
    config_license = metadata.get("license")
    config_source_code_url = metadata.get("source_code_url")
    config_start_url = metadata.get("start_url")
    config_favicon_url = metadata.get("favicon_url")  # Explicit favicon URL

    # Get authentication from variables
    variables = metadata.get("variables", [])
    username = None
    password = None
    for var in variables:
        if isinstance(var, dict):
            var_name = var.get("name", "").lower()
            var_value = var.get("value")
            if var_name in ("username", "user", "email", "admin_email", "adminmail"):
                username = var_value
            elif var_name in ("password", "pass", "admin_password", "adminpass"):
                password = var_value

    # Use explicit favicon_url from config, or warn if missing
    favicon_url = config_favicon_url
    if not favicon_url:
        console.print("[yellow]⚠️  No favicon_url in plato-config.yml metadata - favicon will not be set[/yellow]")
        console.print(
            "[yellow]   Add 'favicon_url: https://www.google.com/s2/favicons?domain=APPNAME.com&sz=32' to metadata[/yellow]"
        )

    async def _submit_base():
        base_url = _get_base_url()

        async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as client:
            # Get simulator by name
            sim = await get_simulator_by_name.asyncio(
                client=client,
                name=simulator_name,
                x_api_key=api_key,
            )
            simulator_id = sim.id
            current_config = sim.config or {}
            current_status = current_config.get("status", "not_started")

            # Validate status transition
            validate_status_transition(current_status, "env_in_progress", "submit base")

            # Show info and submit
            console.print(f"[cyan]Simulator:[/cyan]      {simulator_name}")
            console.print(f"[cyan]Artifact ID:[/cyan]    {artifact_id}")
            console.print(f"[cyan]Current Status:[/cyan] {current_status}")
            console.print()

            # Sync metadata from plato-config.yml to server
            console.print("[cyan]Syncing metadata to server...[/cyan]")

            # Build update request with metadata from plato-config.yml
            update_fields: dict = {}

            if config_description:
                update_fields["description"] = config_description
                console.print(f"  [dim]description:[/dim] {config_description[:50]}...")

            if favicon_url:
                update_fields["img_url"] = favicon_url
                console.print(f"  [dim]img_url:[/dim] {favicon_url}")

            if config_license:
                update_fields["license"] = config_license
                console.print(f"  [dim]license:[/dim] {config_license}")

            if config_source_code_url:
                update_fields["source_code_url"] = config_source_code_url
                console.print(f"  [dim]source_code_url:[/dim] {config_source_code_url}")

            if config_start_url:
                update_fields["start_url"] = config_start_url
                console.print(f"  [dim]start_url:[/dim] {config_start_url}")

            if username and password:
                update_fields["authentication"] = Authentication(user=username, password=password)
                console.print(f"  [dim]authentication:[/dim] {username} / {'*' * len(password)}")

            # Always include base_artifact_id
            update_fields["base_artifact_id"] = artifact_id

            try:
                await update_simulator.asyncio(
                    client=client,
                    simulator_id=simulator_id,
                    body=AppApiV1SimulatorRoutesUpdateSimulatorRequest(**update_fields),
                    x_api_key=api_key,
                )
                console.print("[green]✅ Metadata synced to server[/green]")
            except Exception as e:
                console.print(f"[yellow]⚠️  Could not sync metadata: {e}[/yellow]")

            console.print()

            # Update simulator status
            await update_simulator_status.asyncio(
                client=client,
                simulator_id=simulator_id,
                body=UpdateStatusRequest(status="env_review_requested"),
                x_api_key=api_key,
            )

            console.print("[green]✅ Environment review requested successfully![/green]")
            console.print(f"[cyan]Status:[/cyan] {current_status} → env_review_requested")
            console.print(f"[cyan]Base Artifact:[/cyan] {artifact_id}")

    handle_async(_submit_base())


@submit_app.command(name="data")
def submit_data(
    simulator: str = typer.Option(
        None,
        "--simulator",
        "-s",
        help="Simulator name. Supports colon notation: -s sim:<artifact-uuid>",
    ),
    artifact: str = typer.Option(
        None,
        "--artifact",
        "-a",
        help="Artifact UUID to submit for data review (required).",
    ),
):
    """Submit data artifact for review after data generation.

    Transitions simulator from data_in_progress → data_review_requested and
    tags the artifact as 'data-pending-review'.

    Requires simulator status: data_in_progress

    Options:
        -s, --simulator: Simulator name. Supports colon notation:
            '-s sim:<uuid>' or use separate -a flag
        -a, --artifact: Artifact UUID to submit (required)
    """
    api_key = require_api_key()

    # Parse simulator and artifact from args (artifact IS required for data submit)
    simulator_name, artifact_id = parse_simulator_artifact(
        simulator, artifact, require_artifact=True, command_name="submit data"
    )

    async def _submit_data():
        # simulator_name and artifact_id are guaranteed set by parse_simulator_artifact with require_artifact=True
        assert simulator_name is not None, "simulator_name must be set"
        assert artifact_id is not None, "artifact_id must be set"

        base_url = _get_base_url()

        async with httpx.AsyncClient(base_url=base_url, timeout=60.0) as client:
            # Get simulator by name
            sim = await get_simulator_by_name.asyncio(
                client=client,
                name=simulator_name,
                x_api_key=api_key,
            )
            simulator_id = sim.id
            current_config = sim.config or {}
            current_status = current_config.get("status", "not_started")

            # Validate status transition
            validate_status_transition(current_status, "data_in_progress", "submit data")

            # Show info and submit
            console.print(f"[cyan]Simulator:[/cyan]      {simulator_name}")
            console.print(f"[cyan]Artifact ID:[/cyan]    {artifact_id}")
            console.print(f"[cyan]Current Status:[/cyan] {current_status}")
            console.print()

            # Update simulator status
            await update_simulator_status.asyncio(
                client=client,
                simulator_id=simulator_id,
                body=UpdateStatusRequest(status="data_review_requested"),
                x_api_key=api_key,
            )

            # Set data_artifact_id via tag update (simulator_name and artifact_id already asserted above)
            try:
                await update_tag.asyncio(
                    client=client,
                    body=UpdateTagRequest(
                        simulator_name=simulator_name,
                        artifact_id=artifact_id,
                        tag_name="data-pending-review",
                        dataset="base",
                    ),
                    x_api_key=api_key,
                )
            except Exception as e:
                console.print(f"[yellow]⚠️  Could not set artifact tag: {e}[/yellow]")

            console.print("[green]✅ Data review requested successfully![/green]")
            console.print(f"[cyan]Status:[/cyan] {current_status} → data_review_requested")
            console.print(f"[cyan]Data Artifact:[/cyan] {artifact_id}")

    handle_async(_submit_data())
