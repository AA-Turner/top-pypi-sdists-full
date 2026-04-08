"""Sandbox CLI commands for Plato."""

import json
import logging
import os
import re
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console

from plato.cli.utils import require_api_key
from plato.v2.sync.sandbox import SandboxClient

# =============================================================================
# COMMON ARG TYPES
# =============================================================================

WORKING_DIR = Path.cwd()


# Panel names for rich help
STATE_PANEL = "State (Loaded from .plato/state.json if not provided)"
OUTPUT_PANEL = "General"


class SandboxStateError(Exception):
    """Raised when required state is missing from the client.

    This typically means either:
    - No state file exists (run `plato sandbox start` first)
    - The required field wasn't saved in state
    - The explicit CLI argument wasn't provided
    """

    def __init__(self, field: str, hint: str | None = None):
        self.field = field
        self.hint = hint or f"Provide --{field.replace('_', '-')} or run `plato sandbox start` first"
        super().__init__(f"Missing required field: {field}. {self.hint}")


# State file helpers
def required_state_field(field: str):
    """Default factory to pull a field from .plato/state.json in WORKING_DIR."""

    def _factory():
        path = WORKING_DIR / ".plato" / "state.json"
        if not path.exists():
            return None
        loaded = {}
        try:
            loaded = json.loads(path.read_text())
        except Exception:
            raise Exception("failed to load state.json")
        try:
            return loaded.get(field)
        except Exception:
            raise Exception(f"failed to get field '{field}' from state.json, and no default value provided")

    return _factory


# Working directory setter for CLI option callback
def _set_working_dir(value: Path):
    """Option callback to update global WORKING_DIR based on -w/--working-dir."""
    global WORKING_DIR
    WORKING_DIR = value
    return value


# State args - auto-resolved from .plato/state.json if not provided
SessionIdArg = Annotated[
    str | None,
    typer.Option(
        "--session-id",
        help="Session ID",
        rich_help_panel=STATE_PANEL,
        default_factory=required_state_field("session_id"),
    ),
]
SimulatorNameArg = Annotated[
    str | None,
    typer.Option(
        "--simulator-name",
        help="Simulator name",
        rich_help_panel=STATE_PANEL,
        default_factory=required_state_field("simulator_name"),
    ),
]
JobIdArg = Annotated[
    str | None,
    typer.Option(
        "--job-id",
        help="Job ID",
        rich_help_panel=STATE_PANEL,
        default_factory=required_state_field("job_id"),
    ),
]
SshConfigArg = Annotated[
    str | None,
    typer.Option(
        "--ssh-config",
        "-c",
        help="SSH config path",
        rich_help_panel=STATE_PANEL,
        default_factory=required_state_field("ssh_config_path"),
    ),
]
SshHostArg = Annotated[
    str | None,
    typer.Option(
        "--ssh-host",
        "-h",
        help="SSH host alias",
        rich_help_panel=STATE_PANEL,
        default_factory=required_state_field("ssh_host"),
    ),
]
ModeArg = Annotated[
    str | None,
    typer.Option(
        "--mode",
        "-m",
        help="Mode",
        rich_help_panel=STATE_PANEL,
        default_factory=required_state_field("mode"),
    ),
]
DatasetArg = Annotated[
    str | None,
    typer.Option(
        "--dataset",
        "-d",
        help="Dataset",
        rich_help_panel=STATE_PANEL,
        default_factory=required_state_field("dataset"),
    ),
]
PublicUrlArg = Annotated[
    str | None,
    typer.Option(
        "--public-url",
        help="Public URL",
        rich_help_panel=STATE_PANEL,
        default_factory=required_state_field("public_url"),
    ),
]

# Output args
JsonArg = Annotated[
    bool,
    typer.Option(
        "--json",
        "-j",
        help="Output as JSON",
        rich_help_panel=OUTPUT_PANEL,
    ),
]
VerboseArg = Annotated[
    bool,
    typer.Option(
        "--verbose",
        "-v",
        help="Verbose output",
        rich_help_panel=OUTPUT_PANEL,
    ),
]
WorkingDirArg = Annotated[
    Path,
    typer.Option(
        "--working-dir",
        "-w",
        help="Working directory for .plato/",
        rich_help_panel=OUTPUT_PANEL,
        callback=_set_working_dir,
        default_factory=lambda: Path.cwd(),
    ),
]

# UUID pattern for detecting artifact IDs in colon notation
UUID_PATTERN = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE)

sandbox_app = typer.Typer(
    help="""Manage sandbox VMs for simulator development.

State: 'start' writes .plato/state.json, other commands read from it.
Use --working-dir to change where state is stored/loaded."""
)


# =============================================================================
# OUTPUT HELPERS
# =============================================================================


def _to_dict(obj) -> dict:
    """Convert a result object to a dict."""
    if obj is None:
        return {}
    if isinstance(obj, dict):
        return obj
    if hasattr(obj, "model_dump"):
        return obj.model_dump(exclude_none=True)
    if hasattr(obj, "__dataclass_fields__"):
        from dataclasses import asdict

        return {k: v for k, v in asdict(obj).items() if v is not None}
    return {"result": str(obj)}


class Output:
    """Output handler that switches between JSON and pretty-print."""

    def __init__(self, json_mode: bool = False, verbose: bool = False):
        self.json_mode = json_mode
        self.verbose = verbose
        if json_mode and verbose:
            raise ValueError("Cannot use both --json and --verbose")

        self.super_console = Console()
        if verbose:
            self.console = Console()
        else:
            self.console = Console(quiet=True)

    def _format_value(self, value, indent: int = 0) -> str:
        """Format a value with YAML-like indentation."""
        prefix = "  " * indent
        if isinstance(value, dict):
            if not value:
                return "{}"
            lines = []
            for k, v in value.items():
                if v is None:
                    continue
                formatted = self._format_value(v, indent + 1)
                if isinstance(v, (dict, list)) and v:
                    lines.append(f"{prefix}  [dim]{k}:[/dim]\n{formatted}")
                else:
                    lines.append(f"{prefix}  [dim]{k}:[/dim] {formatted}")
            return "\n".join(lines)
        elif isinstance(value, list):
            if not value:
                return "[]"
            lines = []
            for item in value:
                formatted = self._format_value(item, indent + 1)
                if isinstance(item, dict):
                    lines.append(f"{prefix}  -\n{formatted}")
                else:
                    lines.append(f"{prefix}  - {formatted}")
            return "\n".join(lines)
        else:
            return str(value)

    def success(self, result, title: str | None = None) -> None:
        """Output a successful result."""
        data = _to_dict(result)
        if self.json_mode:
            # Use print() directly to avoid Rich adding ANSI codes
            print(json.dumps(data, indent=2, default=str))
        else:
            if title:
                self.super_console.print(f"[green]{title}[/green]")
            for key, value in data.items():
                if value is None:
                    continue
                formatted = self._format_value(value, 0)
                if isinstance(value, (dict, list)) and value:
                    self.super_console.print(f"[cyan]{key}:[/cyan]\n{formatted}")
                else:
                    self.super_console.print(f"[cyan]{key}:[/cyan] {formatted}")

    def error(self, msg: str) -> None:
        """Output an error."""
        if self.json_mode:
            # Use print() directly to avoid Rich adding ANSI codes
            print(json.dumps({"error": msg}))
        else:
            self.super_console.print(f"[red]{msg}[/red]")


@contextmanager
def sandbox_context(
    working_dir: Path,
    json_output: bool = False,
    verbose: bool = False,
    console: Console = Console(),
) -> Generator[tuple[SandboxClient, Output], None, None]:
    """Context manager for CLI commands with error handling.

    Yields:
        Tuple of (client, output) for use in the command.

    Raises:
        typer.Exit: On any error, after outputting error message.
    """
    # Enable HTTP request logging when verbose
    if verbose:
        logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s: %(message)s")
        logging.getLogger("httpx").setLevel(logging.INFO)
        logging.getLogger("httpcore").setLevel(logging.INFO)

    out = Output(json_output, verbose)
    # Use super_console for status updates (always visible), not the quiet console
    client = SandboxClient(
        working_dir=working_dir,
        api_key=require_api_key(),
        console=out.super_console if not json_output else out.console,
    )
    try:
        yield client, out
    except (SandboxStateError, Exception) as e:
        out.error(str(e))
        raise typer.Exit(1)
    finally:
        client.close()


@sandbox_app.command(name="start")
def sandbox_start(
    working_dir: WorkingDirArg,
    # modes
    simulator: str = typer.Option(None, "--simulator", "-s", help="Simulator (sim)", rich_help_panel="Simulator Mode"),
    from_config: bool = typer.Option(
        False, "--from-config", "-c", help="Use plato-config.yml", rich_help_panel="Config Mode"
    ),
    artifact_id: str = typer.Option(None, "--artifact-id", "-a", help="Artifact UUID", rich_help_panel="Artifact Mode"),
    blank: bool = typer.Option(False, "--blank", "-b", help="Create blank VM", rich_help_panel="Blank Mode"),
    # blank args
    cpus: int = typer.Option(2, "--cpus", help="CPUs (blank VM)", rich_help_panel="Blank Mode"),
    memory: int = typer.Option(1024, "--memory", help="Memory MB (blank VM)", rich_help_panel="Blank Mode"),
    disk: int = typer.Option(10240, "--disk", help="Disk MB (blank VM)", rich_help_panel="Blank Mode"),
    # general args
    dataset: str = typer.Option("base", "--dataset", "-d", help="Dataset we are using"),
    connect_network: bool = typer.Option(True, "--network/--no-network", help="Connect WireGuard to the sandbox"),
    timeout: int = typer.Option(1800, "--timeout", "-t", help="VM lifetime in seconds"),
    json_output: JsonArg = False,
    verbose: VerboseArg = False,
):
    """Start a new sandbox VM.

    Creates a sandbox from a simulator, artifact, config file, or blank VM.
    Saves session info to .plato/state.json for use by other commands.

    Examples:
        plato sandbox start -s espocrm           # From simulator
        plato sandbox start -c                   # From plato-config.yml
        plato sandbox start -a <uuid>            # From artifact
        plato sandbox start -b --cpus 4          # Blank VM
    """
    with sandbox_context(working_dir, json_output, verbose) as (client, out):
        out.console.print("Starting sandbox...")

        if simulator:
            state = client.start(
                mode="simulator",
                simulator_name=simulator,
                dataset=dataset,
                connect_network=connect_network,
                timeout=timeout,
            )
        elif blank:
            state = client.start(
                mode="blank",
                simulator_name=simulator,
                dataset=dataset,
                cpus=cpus,
                memory=memory,
                disk=disk,
                connect_network=connect_network,
                timeout=timeout,
            )
        elif artifact_id:
            state = client.start(
                mode="artifact",
                artifact_id=artifact_id,
                dataset=dataset,
                connect_network=connect_network,
                timeout=timeout,
            )
        elif from_config:
            state = client.start(
                mode="config",
                dataset=dataset,
                connect_network=connect_network,
                timeout=timeout,
            )
        else:
            out.error("Must specify a mode: --blank, --artifact-id, --simulator, or --from-config.")
            raise typer.Exit(1)

        out.success(state, "Sandbox started")


# CHECKED
@sandbox_app.command(name="snapshot")
def sandbox_snapshot(
    working_dir: WorkingDirArg,
    session_id: SessionIdArg,
    mode: ModeArg,
    dataset: DatasetArg,
    json_output: JsonArg = False,
    verbose: VerboseArg = False,
):
    """Create a snapshot of the current sandbox state.

    Captures VM state and database for later restoration.

    Examples:
        plato sandbox snapshot                    # Uses mode from state.json
        plato sandbox snapshot --mode config      # Override to pass local plato-config.yml and flows to artifact
    """
    with sandbox_context(working_dir, json_output, verbose) as (client, out):
        out.console.print("Creating snapshot...")

        response = client.snapshot(
            session_id=str(session_id),
            mode=str(mode),
            dataset=str(dataset),
        )
        out.success(response, "Snapshot created")


@sandbox_app.command(name="reset")
def sandbox_reset(
    working_dir: WorkingDirArg,
    session_id: SessionIdArg,
    json_output: JsonArg = False,
    verbose: VerboseArg = False,
):
    """Reset the sandbox environment.

    Sends a reset command to re-run the sim's setup callback.
    The sandbox remains running after reset.

    Examples:
        plato sandbox reset                                # Uses session_id from .plato/state.json
        plato sandbox reset --session-id abc123           # Explicitly provide the session to reset
    """
    with sandbox_context(working_dir, json_output, verbose) as (client, out):
        out.console.print("Resetting sandbox...")
        result = client.reset(session_id=str(session_id))
        out.success(result, "Sandbox reset")


# CHECKED
@sandbox_app.command(name="stop")
def sandbox_stop(
    working_dir: WorkingDirArg,
    session_id: SessionIdArg,
    json_output: JsonArg = False,
    verbose: VerboseArg = False,
):
    """Stop and destroy the current sandbox.

    Terminates the VM and cleans up resources. State file remains for reference.

    Example:
        plato sandbox stop
    """
    with sandbox_context(working_dir, json_output, verbose) as (client, out):
        out.console.print("Stopping sandbox...")
        client.stop(session_id=str(session_id))
        out.success({"status": "stopped"}, "Sandbox stopped")


# CHECKED
@sandbox_app.command(name="connect-network")
def sandbox_connect_network(
    working_dir: WorkingDirArg,
    session_id: SessionIdArg,
    json_output: JsonArg = False,
    verbose: VerboseArg = False,
):
    """Connect to the sandbox via WireGuard VPN.

    Sets up network access to the sandbox VM. Usually done automatically by start.

    Example:
        plato sandbox connect-network
    """
    with sandbox_context(working_dir, json_output, verbose) as (client, out):
        out.console.print("Connecting to network...")
        result = client.connect_network(session_id=str(session_id))
        out.success(result, "Network connected")


# CHECKED
@sandbox_app.command(name="status")
def sandbox_status(
    working_dir: WorkingDirArg,
    session_id: SessionIdArg,
    json_output: JsonArg = False,
    verbose: VerboseArg = False,
):
    """Show current sandbox status.

    Displays local state file and remote session details.

    Example:
        plato sandbox status
        plato sandbox status --json
    """
    with sandbox_context(working_dir, json_output, verbose) as (client, out):
        out.console.print("Fetching status...")
        local_state = None
        if os.path.exists(working_dir / ".plato" / "state.json"):
            local_state = json.load(open(working_dir / ".plato" / "state.json"))

        details = client.status(session_id=str(session_id))
        all_details = {"local": local_state, "remote": details}
        out.success(all_details, "Sandbox Status")


# CHECKED
@sandbox_app.command(name="state")
def sandbox_state(
    working_dir: WorkingDirArg,
    session_id: SessionIdArg,
    json_output: JsonArg = False,
    verbose: VerboseArg = False,
):
    """Get database mutations from the sandbox.

    Returns changes tracked by the Plato worker (inserts, updates, deletes).

    Example:
        plato sandbox state
        plato sandbox state --json
    """
    with sandbox_context(working_dir, json_output, verbose) as (client, out):
        out.console.print("Fetching mutations...")
        result = client.state(session_id=str(session_id))

        out.success(result, f"State: {result.session_id}")


# CHECKED
@sandbox_app.command(name="start-worker")
def sandbox_start_worker(
    working_dir: WorkingDirArg,
    job_id: JobIdArg,
    simulator: SimulatorNameArg,
    dataset: DatasetArg,
    api: bool = typer.Option(False, "--api", "-a", help="Fetch plato-config from API instead of local file"),
    wait_timeout: int = typer.Option(240, "--wait-timeout", help="Wait timeout in seconds"),
    json_output: JsonArg = False,
    verbose: VerboseArg = False,
):
    """Start the Plato worker in the sandbox.

    The worker tracks database mutations and enables state capture.
    Waits for worker to be ready (up to --wait-timeout seconds).

    Example:
        plato sandbox start-worker
        plato sandbox start-worker --api
        plato sandbox start-worker --wait-timeout 300
    """
    with sandbox_context(working_dir, json_output, verbose) as (client, out):
        out.console.print(f"Starting worker: {simulator}, dataset: {dataset}")

        client.start_worker(
            job_id=str(job_id),
            simulator=str(simulator),
            dataset=str(dataset),
            wait_timeout=wait_timeout,
            use_api=api,
        )

        out.success({"status": "started"}, "Worker started")


# CHECKED
@sandbox_app.command(name="sync")
def sandbox_sync(
    working_dir: WorkingDirArg,
    session_id: SessionIdArg,
    simulator: SimulatorNameArg,
    timeout: int = typer.Option(120, "--timeout", "-t", help="Timeout in seconds"),
    json_output: JsonArg = False,
    verbose: VerboseArg = False,
):
    """Sync local files to the sandbox VM via rsync.

    Copies working directory to /home/plato/worktree/<simulator> on the VM.

    Example:
        plato sandbox sync
        plato sandbox sync --timeout 300
    """
    with sandbox_context(working_dir, json_output, verbose) as (client, out):
        out.console.print(f"Syncing {working_dir} -> {f'/home/plato/worktree/{simulator}'}")

        result = client.sync(
            session_id=str(session_id),
            simulator=str(simulator),
            timeout=timeout,
        )

        out.success(result, "Sync complete")


# CHECKED
@sandbox_app.command(name="start-services")
def sandbox_start_services(
    working_dir: WorkingDirArg,
    simulator: SimulatorNameArg,
    ssh_config: SshConfigArg,
    ssh_host: SshHostArg,
    dataset: DatasetArg,
    json_output: JsonArg = False,
    verbose: VerboseArg = False,
):
    """Start docker compose services on the sandbox.

    Deploys containers defined in docker-compose.yml to the VM.

    Example:
        plato sandbox start-services
    """
    with sandbox_context(working_dir, json_output, verbose) as (client, out):
        # Validate required fields
        if not ssh_config:
            out.error("SSH config path not found. Run 'plato sandbox start' first or provide --ssh-config.")
            raise typer.Exit(1)
        if not ssh_host:
            out.error("SSH host not found. Run 'plato sandbox start' first or provide --ssh-host.")
            raise typer.Exit(1)
        if not simulator:
            out.error("Simulator name not found. Run 'plato sandbox start' first or provide --simulator-name.")
            raise typer.Exit(1)
        if not dataset:
            out.error("Dataset not found. Run 'plato sandbox start' first or provide --dataset.")
            raise typer.Exit(1)

        out.console.print("Starting services...")
        result = client.start_services(
            ssh_config_path=str(ssh_config),
            ssh_host=str(ssh_host),
            simulator_name=str(simulator),
            dataset=str(dataset),
        )

        out.success(result, "Services started")


@sandbox_app.command(name="flow")
def sandbox_flow(
    working_dir: WorkingDirArg,
    public_url: PublicUrlArg,
    dataset: DatasetArg,
    job_id: JobIdArg,
    flow_name: str = typer.Option("login", "--flow-name", "-f", help="Flow to execute"),
    api: bool = typer.Option(False, "--api", "-a", help="Fetch flows from API (requires job_id)"),
    headless: bool = typer.Option(False, "--headless", help="Run browser in headless mode"),
    keep_browser_open: bool = typer.Option(
        False, "--keep-browser-open", "-k", help="Keep browser open after flow completes"
    ),
    json_output: JsonArg = False,
    verbose: VerboseArg = False,
):
    """Run a Playwright flow against the sandbox.

    Executes UI automation flows defined in flows.yml or fetched from API.

    Examples:
        plato sandbox flow                       # Run 'login' flow from local config
        plato sandbox flow -f signup             # Run 'signup' flow
        plato sandbox flow --api                 # Fetch flow from API
        plato sandbox flow -k                    # Keep browser open after flow
    """
    with sandbox_context(working_dir, json_output, verbose) as (client, out):
        out.console.print(f"Running flow '{flow_name}' on {str(public_url)}")

        client.run_flow(
            url=str(public_url),
            flow_name=flow_name,
            dataset=str(dataset),
            use_api=api,
            job_id=str(job_id) if api else None,
            headless=headless,
            keep_browser_open=keep_browser_open,
        )

        out.success({"flow_name": flow_name, "url": str(public_url)}, "Flow complete")


@sandbox_app.command(name="pull-config")
def sandbox_pull_config(
    working_dir: WorkingDirArg,
    dataset: DatasetArg,
    artifact_id: str = typer.Option(
        None,
        "--artifact-id",
        "-a",
        help="Artifact UUID (reads from .plato/state.json if not provided)",
    ),
    json_output: JsonArg = False,
    verbose: VerboseArg = False,
):
    """Download plato-config.yml and flows.yml from an artifact.

    Fetches config files from the artifact API so they can be edited
    locally and applied via start-worker / sandbox flow.

    Example:
        plato sandbox pull-config
        plato sandbox pull-config -a <artifact-uuid>
    """
    with sandbox_context(working_dir, json_output, verbose) as (client, out):
        # Resolve artifact_id from state if not provided
        if not artifact_id:
            state_path = working_dir / ".plato" / "state.json"
            if state_path.exists():
                with open(state_path) as f:
                    state = json.load(f)
                artifact_id = state.get("artifact_id")
            if not artifact_id:
                out.error("No artifact_id found. Provide --artifact-id or run 'plato sandbox start -a' first.")
                raise typer.Exit(1)

        resolved_dataset = str(dataset) if dataset else "base"
        out.console.print(f"Pulling config from artifact {artifact_id}...")
        result = client.pull_config(artifact_id=artifact_id, dataset=resolved_dataset)

        if not result["plato_config_written"] and not result["flows_written"]:
            out.error(
                f"Failed to pull config for artifact {artifact_id}: neither plato-config.yml nor flows were written."
            )
            raise typer.Exit(1)

        out.success(
            {"artifact_id": artifact_id, **result},
            "Config pulled",
        )


@sandbox_app.command(name="clear-audit")
def sandbox_clear_audit(
    working_dir: WorkingDirArg,
    session_id: SessionIdArg,
    json_output: JsonArg = False,
    verbose: VerboseArg = False,
):
    """Clear the audit_log table(s) in the sandbox database.

    This clears audit logs that track database mutations, which is useful
    for resetting state between test runs.
    """
    with sandbox_context(working_dir, json_output, verbose) as (client, out):
        out.console.print("Clearing audit logs...")
        result = client.clear_audit(job_group_id=str(session_id))

        if not result.success:
            raise Exception(result.error or "Failed to clear audit logs")

        out.success({"success": result.success}, "Audit logs cleared")


@sandbox_app.command(name="audit-ui")
def sandbox_audit_ui(
    working_dir: WorkingDirArg,
    job_id: JobIdArg,
    dataset: DatasetArg,
    no_tunnel: bool = typer.Option(False, "--no-tunnel", help="Don't auto-start tunnel"),
    json_output: JsonArg = False,
    verbose: VerboseArg = False,
):
    """Launch Streamlit UI for configuring audit ignore rules.

    Opens a web UI to select tables/columns to ignore during mutation tracking.
    Auto-starts a tunnel to the database if configured in plato-config.yml.

    Example:
        plato sandbox audit-ui
        plato sandbox audit-ui --no-tunnel
    """
    with sandbox_context(working_dir, json_output, verbose) as (client, out):
        try:
            client.run_audit_ui(
                job_id=job_id,
                dataset=dataset or "base",
                no_tunnel=no_tunnel,
            )
        except ValueError as e:
            out.error(str(e))
            raise typer.Exit(1) from None


# =============================================================================
# SSH & TUNNEL COMMANDS
# =============================================================================


@sandbox_app.command(name="ssh", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def sandbox_ssh(
    working_dir: WorkingDirArg,
    ctx: typer.Context,
    ssh_config: SshConfigArg,
    ssh_host: SshHostArg,
    job_id: Annotated[
        str | None,
        typer.Option(
            "--job-id",
            "-J",
            help="Connect to a specific job ID (bypasses .plato/state.json)",
        ),
    ] = None,
    json_output: JsonArg = False,
    verbose: VerboseArg = False,
):
    """SSH to the sandbox VM.

    Uses .plato/ssh_config from 'start', or connect directly to a job with -J.

    NOTE FOR AGENTS: Do not use this command. Instead, use the raw SSH command
    from 'plato sandbox status' which shows: ssh -F .plato/ssh_config sandbox

    Examples:
        plato sandbox ssh                         # Use saved state
        plato sandbox ssh -J <job-id>             # Connect to specific job
        plato sandbox ssh -- -L 8080:localhost:8080
    """
    import subprocess
    import tempfile

    with sandbox_context(working_dir, json_output, verbose) as (client, out):
        # If job_id provided, generate SSH config dynamically
        if job_id:
            out.console.print(f"Connecting to job: {job_id}")

            # Fetch SSH config for the job (uses cached key and adds to VM)
            try:
                ssh_info = client.get_ssh_config_for_job(job_id)
                out.console.print(f"Using SSH key: {ssh_info.private_key_path}")
            except Exception as e:
                out.error(f"Failed to get SSH config for job {job_id}: {e}")
                raise typer.Exit(1)

            # Write temporary SSH config
            with tempfile.NamedTemporaryFile(mode="w", suffix=".ssh_config", delete=False) as f:
                f.write(ssh_info.config_content)
                temp_config_path = f.name

            cmd = ["ssh", "-F", temp_config_path, "sandbox"] + (ctx.args or [])

            try:
                raise typer.Exit(subprocess.run(cmd).returncode)
            except KeyboardInterrupt:
                raise typer.Exit(130) from None
            finally:
                # Clean up temp config file
                try:
                    os.unlink(temp_config_path)
                except Exception:
                    pass
        else:
            # Use saved SSH config
            if not ssh_config:
                out.error("No SSH config found. Run 'plato sandbox start' first or use -J <job-id>.")
                raise typer.Exit(1)

            config_path = client.working_dir / ssh_config if not Path(ssh_config).is_absolute() else Path(ssh_config)
            cmd = ["ssh", "-F", str(config_path), ssh_host or "sandbox"] + (ctx.args or [])

            try:
                raise typer.Exit(subprocess.run(cmd).returncode)
            except KeyboardInterrupt:
                raise typer.Exit(130) from None


@sandbox_app.command(name="tunnel")
def sandbox_tunnel(
    working_dir: WorkingDirArg,
    job_id: JobIdArg,
    remote_port: int = typer.Argument(..., help="Remote port on the VM to forward"),
    local_port: int | None = typer.Argument(None, help="Local port to listen on"),
    bind_address: str = typer.Option("127.0.0.1", "--bind", "-b"),
    json_output: JsonArg = False,
    verbose: VerboseArg = False,
):
    """Forward a local port to the sandbox VM.

    Creates a TCP tunnel through the TLS gateway. Useful for database access.

    NOTE FOR AGENTS: Do not use this command. Use raw SSH port forwarding instead:
    ssh -F .plato/ssh_config sandbox -L <local_port>:127.0.0.1:<remote_port>

    Examples:
        plato sandbox tunnel 5432              # Forward PostgreSQL
        plato sandbox tunnel 3306              # Forward MySQL
        plato sandbox tunnel 5432 15432        # VM:5432 -> localhost:15432
    """
    import time

    with sandbox_context(working_dir, json_output, verbose) as (client, out):
        if not job_id:
            out.error("No job_id found. Run 'plato sandbox start' first.")
            raise typer.Exit(1)

        local = local_port or remote_port
        tunnel = client.tunnel(job_id, remote_port, local, bind_address)

        try:
            tunnel.start()
            out.console.print(f"[green]Tunnel:[/green] {bind_address}:{local} -> VM:{remote_port}")
            out.console.print("[dim]Ctrl+C to stop[/dim]")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            out.console.print("\n[yellow]Closed[/yellow]")
        finally:
            tunnel.stop()
