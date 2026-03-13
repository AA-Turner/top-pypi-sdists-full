"""Session CLI commands for Plato - manage multi-environment sessions."""

import json
import time
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.table import Table
from rich.text import Text

from plato.cli.utils import require_api_key
from plato.v2.sync.client import Plato
from plato.v2.types import Env

app = typer.Typer(
    name="session",
    help="Manage sessions with multiple environments.",
    no_args_is_help=True,
)

console = Console()

# State file location
STATE_DIR = Path(".plato")
STATE_FILE = STATE_DIR / "session.json"


def save_state(state: dict) -> None:
    """Save session state to .plato/session.json."""
    STATE_DIR.mkdir(exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def load_state() -> dict | None:
    """Load session state from .plato/session.json."""
    if not STATE_FILE.exists():
        return None
    try:
        return json.loads(STATE_FILE.read_text())
    except Exception:
        return None


def clear_state() -> None:
    """Clear session state."""
    if STATE_FILE.exists():
        STATE_FILE.unlink()


def make_status_table(session, title: str = "Session Status") -> Table:
    """Create a rich table showing session/environment status."""
    table = Table(title=title, show_header=True, header_style="bold cyan")
    table.add_column("Alias", style="bold")
    table.add_column("Simulator")
    table.add_column("Status")
    table.add_column("Job ID", style="dim")
    table.add_column("Public URL", style="blue underline")

    for env in session.envs:
        status_style = "green" if env.status == "running" else "yellow"
        table.add_row(
            env.alias or "-",
            env.simulator or "-",
            Text(env.status or "unknown", style=status_style),
            env.job_id[:12] + "..." if env.job_id and len(env.job_id) > 12 else (env.job_id or "-"),
            env.public_url or "-",
        )

    return table


@app.command("start")
def start(
    # Environment specification options
    sim: Annotated[
        list[str] | None,
        typer.Option(
            "--sim",
            "-s",
            help="Simulator to start (can specify multiple). Format: 'name' or 'name:tag' or 'name:tag@dataset'",
        ),
    ] = None,
    artifact: Annotated[
        list[str] | None,
        typer.Option(
            "--artifact",
            "-a",
            help="Artifact ID to start (can specify multiple)",
        ),
    ] = None,
    task: Annotated[
        str | None,
        typer.Option(
            "--task",
            "-t",
            help="Task ID to create session from",
        ),
    ] = None,
    n: Annotated[
        int,
        typer.Option(
            "--n",
            "-n",
            help="Number of instances (only with single --sim)",
        ),
    ] = 1,
    # Resource options
    timeout: Annotated[
        int,
        typer.Option(
            "--timeout",
            help="VM timeout in seconds",
        ),
    ] = 1800,
    no_network: Annotated[
        bool,
        typer.Option(
            "--no-network",
            help="Don't connect VMs to network",
        ),
    ] = False,
    # Output options
    json_output: Annotated[
        bool,
        typer.Option(
            "--json",
            "-j",
            help="Output as JSON",
        ),
    ] = False,
    wait: Annotated[
        bool,
        typer.Option(
            "--wait/--no-wait",
            "-w",
            help="Wait for all environments to be ready",
        ),
    ] = True,
) -> None:
    """Start a new session with one or more environments.

    Examples:
        # Single simulator
        plato session start --sim espocrm

        # Multiple simulators
        plato session start --sim espocrm --sim gitea

        # With specific tags
        plato session start --sim espocrm:staging --sim gitea:latest

        # With dataset
        plato session start --sim espocrm:latest@blank

        # Multiple instances of same simulator
        plato session start --sim espocrm -n 3

        # From artifact
        plato session start --artifact abc123

        # From task
        plato session start --task task-id-123
    """
    api_key = require_api_key()

    # Validate inputs
    if task and (sim or artifact):
        console.print("[red]Error:[/red] Cannot specify --task with --sim or --artifact")
        raise typer.Exit(1)

    if not task and not sim and not artifact:
        console.print("[red]Error:[/red] Must specify --sim, --artifact, or --task")
        raise typer.Exit(1)

    if n > 1 and (len(sim or []) > 1 or artifact):
        console.print("[red]Error:[/red] --n only works with a single --sim")
        raise typer.Exit(1)

    # Build environment list
    envs = []

    if sim:
        for i, s in enumerate(sim):
            # Parse format: name, name:tag, or name:tag@dataset
            dataset = None
            tag = "latest"

            if "@" in s:
                s, dataset = s.rsplit("@", 1)
            if ":" in s:
                name, tag = s.split(":", 1)
            else:
                name = s

            # Handle --n for multiple instances
            count = n if len(sim) == 1 else 1
            for j in range(count):
                alias = f"{name}-{j}" if count > 1 else (name if len(sim) == 1 else f"{name}-{i}")
                envs.append(Env.simulator(name, tag=tag, dataset=dataset, alias=alias))

    if artifact:
        for i, a in enumerate(artifact):
            alias = f"artifact-{i}" if len(artifact) > 1 else "artifact"
            envs.append(Env.artifact(a, alias=alias))

    # Create session
    plato = Plato(api_key=api_key)

    try:
        if not json_output:
            console.print(f"\n[bold]Starting session with {len(envs) if envs else 'task'} environment(s)...[/bold]\n")

            if envs:
                for env in envs:
                    if hasattr(env, "simulator"):
                        console.print(
                            f"  • {env.alias}: {env.simulator}:{env.tag}"
                            + (f" (dataset: {env.dataset})" if env.dataset else "")
                        )
                    else:
                        console.print(f"  • {env.alias}: artifact {env.artifact_id}")
                console.print()

        start_time = time.time()

        with console.status("[bold green]Creating session..."):
            if task:
                session = plato.sessions.create(testcase=task, timeout=timeout, connect_network=not no_network)
            else:
                session = plato.sessions.create(envs=envs, timeout=timeout, connect_network=not no_network)

            elapsed = time.time() - start_time

        if json_output:
            output = {
                "session_id": session.session_id,
                "environments": [
                    {
                        "alias": env.alias,
                        "job_id": env.job_id,
                        "simulator": env.simulator,
                        "status": env.status,
                        "public_url": env.public_url,
                    }
                    for env in session.envs
                ],
            }
            print(json.dumps(output, indent=2))
        else:
            console.print(f"[green]✓[/green] Session created in {elapsed:.1f}s\n")
            console.print(f"[bold]Session ID:[/bold] {session.session_id}\n")
            console.print(make_status_table(session))
            console.print()

            # Show helpful commands
            console.print("[dim]Helpful commands:[/dim]")
            console.print("  [cyan]plato session status[/cyan]     - Check environment status")
            console.print("  [cyan]plato session stop[/cyan]       - Stop the session")
            console.print()

        # Save state
        save_state(
            {
                "session_id": session.session_id,
                "environments": [
                    {
                        "alias": env.alias,
                        "job_id": env.job_id,
                        "simulator": env.simulator,
                        "public_url": env.public_url,
                    }
                    for env in session.envs
                ],
            }
        )

        # Start heartbeat in background
        session.start_heartbeat()

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    finally:
        plato.close()


@app.command("status")
def status(
    session_id: Annotated[
        str | None,
        typer.Option(
            "--session-id",
            "-s",
            help="Session ID (uses saved state if not provided)",
        ),
    ] = None,
    json_output: Annotated[
        bool,
        typer.Option(
            "--json",
            "-j",
            help="Output as JSON",
        ),
    ] = False,
) -> None:
    """Show status of the current session and all environments."""
    from plato._generated.api.v2.sessions import state as sessions_state

    api_key = require_api_key()

    # Get session ID and env info from state if not provided
    saved_state = load_state()
    if not session_id:
        if not saved_state:
            console.print("[red]Error:[/red] No session found. Run `plato session start` first or provide --session-id")
            raise typer.Exit(1)
        session_id = saved_state.get("session_id")

    if not session_id:
        console.print("[red]Error:[/red] No session ID found")
        raise typer.Exit(1)

    plato = Plato(api_key=api_key)

    try:
        # Get session state from API
        state_response = sessions_state.sync(
            client=plato._http,
            session_id=session_id,
            x_api_key=api_key,
        )

        # Build env info from saved state and API response
        saved_envs = {e.get("job_id"): e for e in (saved_state or {}).get("environments", [])}

        if json_output:
            output = {
                "session_id": session_id,
                "environments": [
                    {
                        "job_id": job_id,
                        "alias": saved_envs.get(job_id, {}).get("alias", job_id[:8]),
                        "simulator": saved_envs.get(job_id, {}).get("simulator", "-"),
                        "status": result.status if hasattr(result, "status") else "unknown",
                    }
                    for job_id, result in state_response.results.items()
                ],
            }
            print(json.dumps(output, indent=2))
        else:
            console.print(f"\n[bold]Session ID:[/bold] {session_id}\n")

            table = Table(title="Session Status", show_header=True, header_style="bold cyan")
            table.add_column("Alias", style="bold")
            table.add_column("Simulator")
            table.add_column("Job ID", style="dim")
            table.add_column("Status")

            for job_id, result in state_response.results.items():
                env_info = saved_envs.get(job_id, {})
                status_val = getattr(result, "status", "unknown") if result else "unknown"
                status_style = "green" if status_val == "running" else "yellow"
                table.add_row(
                    env_info.get("alias", job_id[:8]),
                    env_info.get("simulator", "-"),
                    job_id[:12] + "..." if len(job_id) > 12 else job_id,
                    Text(status_val, style=status_style),
                )

            console.print(table)
            console.print()

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    finally:
        plato.close()


@app.command("stop")
def stop(
    session_id: Annotated[
        str | None,
        typer.Option(
            "--session-id",
            "-s",
            help="Session ID (uses saved state if not provided)",
        ),
    ] = None,
    force: Annotated[
        bool,
        typer.Option(
            "--force",
            "-f",
            help="Force stop without confirmation",
        ),
    ] = False,
) -> None:
    """Stop the current session and all environments."""
    from plato._generated.api.v2.sessions import close as sessions_close

    api_key = require_api_key()

    # Get session ID from state if not provided
    if not session_id:
        state = load_state()
        if not state:
            console.print("[red]Error:[/red] No session found. Run `plato session start` first or provide --session-id")
            raise typer.Exit(1)
        session_id = state.get("session_id")

    if not session_id:
        console.print("[red]Error:[/red] No session ID found")
        raise typer.Exit(1)

    if not force:
        confirm = typer.confirm(f"Stop session {session_id}?")
        if not confirm:
            console.print("Cancelled")
            raise typer.Exit(0)

    plato = Plato(api_key=api_key)

    try:
        with console.status("[bold red]Stopping session..."):
            sessions_close.sync(
                client=plato._http,
                session_id=session_id,
                x_api_key=api_key,
            )

        console.print(f"[green]✓[/green] Session {session_id} stopped")
        clear_state()

    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1)
    finally:
        plato.close()


@app.command("list")
def list_sessions(
    json_output: Annotated[
        bool,
        typer.Option(
            "--json",
            "-j",
            help="Output as JSON",
        ),
    ] = False,
) -> None:
    """List all active sessions."""
    require_api_key()  # Validate API key is set

    # Just show saved state for now
    state = load_state()

    if not state:
        if json_output:
            print(json.dumps({"sessions": []}))
        else:
            console.print("[dim]No active session saved locally.[/dim]")
            console.print("[dim]Use `plato session start` to create one.[/dim]")
        return

    if json_output:
        print(json.dumps({"sessions": [state]}))
    else:
        console.print(f"\n[bold]Active Session:[/bold] {state.get('session_id')}")
        console.print(f"[dim]Environments: {len(state.get('environments', []))}[/dim]\n")

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Alias")
        table.add_column("Simulator")
        table.add_column("Job ID", style="dim")

        for env in state.get("environments", []):
            table.add_row(
                env.get("alias", "-"),
                env.get("simulator", "-"),
                env.get("job_id", "-")[:12] + "..." if env.get("job_id") else "-",
            )

        console.print(table)
        console.print()


if __name__ == "__main__":
    app()
