"""Sandbox CLI commands for Plato."""

import json
import logging
import os
import re
import threading
import time
from collections.abc import Generator
from contextlib import contextmanager, suppress
from datetime import datetime
from pathlib import Path
from typing import Annotated, Any, NoReturn

import typer
from pydantic import BaseModel
from rich.console import Console
from rich.table import Table

from plato._generated.errors import APIError, NotFoundError
from plato._generated.models import (
    AppApiV2SchemasSessionCreateSnapshotResponse,
    ArtifactInfoResponse,
    ArtifactMcpConfig,
    CreateCheckpointResult,
    CreateSnapshotResult,
    SessionDetailsResponse,
    SessionStateResponse,
)
from plato.cli.utils import require_api_key
from plato.v2._wait_for_ready import (
    ARTIFACT_STATUS_FAILED,
    ARTIFACT_STATUS_READY,
    ARTIFACT_WAIT_TIMEOUT_SECONDS,
)
from plato.v2.sandbox_store import (
    NAME_ENV_VAR,
    SandboxStore,
    forget_dir,
    heartbeat_alive,
    heartbeat_log_path,
    registered_dirs,
    running_heartbeats,
    slugify,
    stop_heartbeat,
)
from plato.v2.sync.sandbox import SandboxClient, describe_mcp_config

# =============================================================================
# COMMON ARG TYPES
# =============================================================================

WORKING_DIR = Path.cwd()
#: Slot selected by -n/--name (or $PLATO_SANDBOX); None = whatever
#: .plato/current points at.
SANDBOX_NAME: str | None = None


# Panel names for rich help
STATE_PANEL = "State (Loaded from the sandbox slot if not provided)"
OUTPUT_PANEL = "General"


class SandboxStateError(Exception):
    """Raised when required state is missing from the client.

    This typically means either:
    - No sandbox exists in this working directory (run `plato sandbox start`)
    - The named slot doesn't exist (`plato sandbox list` shows the ones that do)
    - The required field wasn't saved in state
    """

    def __init__(self, field: str, hint: str | None = None):
        self.field = field
        self.hint = hint or (
            f"Provide --{field.replace('_', '-')}, pick a sandbox with -n/--name "
            "(`plato sandbox list`), or run `plato sandbox start` first"
        )
        super().__init__(f"Missing required field: {field}. {self.hint}")


def _store() -> SandboxStore:
    return SandboxStore(WORKING_DIR)


def current_state() -> dict | None:
    """The selected slot's state, or None when there is no sandbox here."""
    store = _store()
    return store.load(store.resolve(SANDBOX_NAME))


# State file helpers
def required_state_field(field: str):
    """Default factory pulling a field off the selected sandbox slot."""

    def _factory():
        state = current_state()
        return state.get(field) if state else None

    return _factory


def state_field(field: str):
    """Read a field off the selected sandbox slot (None if absent)."""
    return required_state_field(field)()


def require(value, field: str) -> str:
    """Return ``value`` as a string, or explain what's missing.

    Without this, an unresolved option reaches the API as the literal string
    ``"None"`` (``str(None)``) and comes back as an opaque 404 instead of
    "there is no sandbox here".
    """
    if value is None or value == "":
        raise SandboxStateError(field)
    return str(value)


DEFAULT_LEASE_SECONDS = 1800.0


def _renew_lease() -> None:
    """Using a sandbox extends its idle lease.

    ``expires_at`` is the deadline the heartbeat enforces: it exits (and the
    backend then reaps the VM) once it passes. Every command that *uses* the
    selected sandbox pushes the deadline out by the sandbox's ``--timeout``,
    so an actively-used sandbox stays alive and an abandoned one dies on its
    own — nobody has to remember ``plato sandbox stop``. Best-effort: a
    failure to renew must never break the command doing the using.
    """
    with suppress(Exception):
        store = _store()
        slot = store.resolve(SANDBOX_NAME)
        if not slot:
            return
        state = store.load(slot)
        if not state or state.get("stopped_at") or state.get("attached"):
            return
        lease = float(state.get("timeout") or DEFAULT_LEASE_SECONDS)
        store.update(slot, expires_at=time.time() + lease)


_RENEW_INTERVAL_SECONDS = 60.0


@contextmanager
def _renewing_lease() -> Generator[None, None, None]:
    """Keep the lease alive for as long as a blocking command runs.

    ``ssh`` and ``tunnel`` hold the sandbox open for the life of one process,
    not one command invocation — an interactive session longer than
    ``--timeout`` must not have its VM reaped mid-connection. Renews on a
    background thread until the block exits.
    """
    stop = threading.Event()

    def loop() -> None:
        while not stop.wait(_RENEW_INTERVAL_SECONDS):
            _renew_lease()

    thread = threading.Thread(target=loop, daemon=True, name="plato-lease-renewer")
    thread.start()
    try:
        yield
    finally:
        stop.set()


# Working directory setter for CLI option callback
def _set_working_dir(value: Path):
    """Option callback to update global WORKING_DIR based on -w/--working-dir."""
    global WORKING_DIR
    WORKING_DIR = value
    return value


def _set_sandbox_name(value: str | None):
    """Option callback to update the selected slot based on -n/--name."""
    global SANDBOX_NAME
    SANDBOX_NAME = slugify(value) if value else None
    return SANDBOX_NAME


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
        # Eager so WORKING_DIR is set before the state-backed options run their
        # default factories against it, whatever order they were typed in.
        is_eager=True,
        default_factory=lambda: Path.cwd(),
    ),
]
NameArg = Annotated[
    str | None,
    typer.Option(
        "--name",
        "-n",
        help="Sandbox slot to act on (default: the current one; see `plato sandbox list`)",
        rich_help_panel=OUTPUT_PANEL,
        envvar=NAME_ENV_VAR,
        callback=_set_sandbox_name,
        is_eager=True,
        # A factory (rather than `= None`) so the option can be declared before
        # the state-backed options without breaking Python's argument order.
        default_factory=lambda: None,
    ),
]
#: `start` takes the same option but *without* the env var. $PLATO_SANDBOX pins
#: which existing sandbox a shell talks to; reading it here would turn every
#: start in that shell into a start into the pinned slot — refusing, or with
#: --force replacing, the very sandbox the pin was protecting.
StartNameArg = Annotated[
    str | None,
    typer.Option(
        "--name",
        "-n",
        help="Slot to start into (default: the next free one, e.g. espocrm-2)",
        rich_help_panel=OUTPUT_PANEL,
        callback=_set_sandbox_name,
        is_eager=True,
        default_factory=lambda: None,
    ),
]

# UUID pattern for detecting artifact IDs in colon notation
UUID_PATTERN = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE)

# Job statuses that mean the VM is gone for good, so its slot is free to reuse
# and `gc` may reap it. Anything else (including an unrecognized value) counts
# as alive: refusing to clobber a sandbox that might still be running is the
# cheap mistake, tearing down a live one is not.
TERMINAL_JOB_STATUSES = {"completed", "failed", "cancelled", "timeout"}


# =============================================================================
# LIVENESS
# =============================================================================


def is_session_gone(exc: Exception) -> bool:
    """True when an API error means the session no longer exists.

    A missing session is a *success* for teardown (there is nothing left to
    close) but must be told apart from a transient failure, where the VM may
    still be running and local state must be left alone.

    Status codes only, never the message text: a DNS failure, or a session id
    that merely contains "404", would otherwise read as "already gone" and get
    the sandbox torn down under a VM that is still up. Every HTTP error from
    the generated client arrives as an :class:`APIError` carrying
    ``status_code``, so anything else is transient by construction.
    """
    return isinstance(exc, APIError) and exc.status_code in (404, 410)


def remote_job_status(client: SandboxClient, session_id: str, job_id: str | None) -> str | None:
    """Backend status of a sandbox's job.

    Returns the status string, ``"gone"`` when the session no longer exists,
    or None when it can't be determined (network error, unexpected shape) —
    which callers must treat as "possibly alive".
    """
    try:
        details = client.status(session_id=session_id)
    except Exception as exc:
        return "gone" if is_session_gone(exc) else None

    jobs = details.get("jobs") if isinstance(details, dict) else getattr(details, "jobs", None)
    statuses = []
    for job in jobs or []:
        if isinstance(job, dict):
            jid = job.get("job_id") or job.get("public_id")
            status = job.get("status")
        else:
            jid = getattr(job, "job_id", None) or getattr(job, "public_id", None)
            status = getattr(job, "status", None)
        if job_id and jid == job_id:
            return status
        statuses.append(status)
    if job_id:
        # The session exists but no longer lists our job (removed env).
        return "gone" if jobs is not None else None
    # Without a job id (an orphaned heartbeat, where all we have is the session)
    # any live job means the session must stay up — reaping on the first job's
    # status would take down its still-running siblings.
    live = next((s for s in statuses if is_live_status(s)), None)
    return live or (statuses[0] if statuses else None)


def is_live_status(status: str | None) -> bool:
    """True unless the status proves the sandbox is finished."""
    if status is None:
        return True
    return status not in TERMINAL_JOB_STATUSES and status != "gone"


def local_live_slots(store: SandboxStore) -> list[dict]:
    """Slots that look alive without asking the backend.

    Cheap enough to run on every `start`: it only reads the slot files, so it
    stays fast with dozens of sandboxes in one directory.
    """
    live = []
    for slot in store.names():
        state = store.load(slot) or {}
        # No session_id means an unfilled claim — a start still provisioning,
        # or one that died before saving. Nothing to stop or report either way.
        if state.get("stopped_at") or not state.get("session_id"):
            continue
        live.append(state)
    return live


sandbox_app = typer.Typer(
    help="""Manage sandbox VMs for simulator development.

State: 'start' writes a named slot under .plato/sandboxes/, other commands read
from it. A working directory can hold several sandboxes at once — select one
with -n/--name, $PLATO_SANDBOX or `plato sandbox use`, and see them all with
`plato sandbox list`. Use --working-dir to change where state is stored/loaded."""
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
        sandbox_name=SANDBOX_NAME,
    )
    try:
        # Converge derived state (links, current pointer, stale claims, orphan
        # SSH material, the machine-wide index) before every command, so debris
        # from a crashed command self-heals instead of needing bespoke cleanup.
        with suppress(Exception):
            client.store.reconcile()
        yield client, out
    except typer.Exit:
        # A command that already reported its outcome; wrapping it would print
        # the exit code as a second error (a second JSON document under --json).
        raise
    except (SandboxStateError, Exception) as e:
        out.error(str(e))
        raise typer.Exit(1)
    finally:
        client.close()


def _guard_existing_sandbox(
    client: SandboxClient,
    out: "Output",
    name: str | None,
    force: bool,
    json_output: bool,
) -> None:
    """Never let a start silently orphan a sandbox that is already running.

    Overwriting a live sandbox's state used to lose its session id, job id and
    heartbeat pid, leaving a VM alive that no CLI command could reach. Now:
    an explicitly named slot that is still running is a hard error (or is
    stopped first with --force), and an unnamed start reports the siblings it
    is about to run alongside so an accidental double-start is visible rather
    than silent.
    """
    store = client.store
    siblings = local_live_slots(store)

    if name:
        # The whole slot, not just the live ones: a slot kept for reference by
        # a previous `stop` still occupies the name, so leaving it in place
        # would silently push this start to `<name>-2` for good.
        existing = store.load(name)
        if existing is not None:
            already_stopped = bool(existing.get("stopped_at"))
            status = (
                None
                if already_stopped
                else remote_job_status(client, str(existing.get("session_id")), existing.get("job_id"))
            )
            if already_stopped or not is_live_status(status):
                # The sandbox is over, so the name is free — but tear the local
                # half down properly first: dropping just the slot JSON would
                # strand a heartbeat that is still looping (it exits only once
                # it sees the session gone) and leave the SSH key behind.
                if not json_output:
                    fate = "was stopped" if already_stopped else f"is {status or 'finished'}"
                    out.super_console.print(f"[dim]Reusing slot '{name}' — its previous sandbox {fate}[/dim]")
                client.cleanup_slot(name, remove=True)
            elif not force:
                out.error(
                    f"Sandbox '{name}' is already running here "
                    f"(session {existing.get('session_id')}, status {status or 'unknown'}).\n"
                    f"  Stop it:      plato sandbox stop -n {name}\n"
                    f"  Replace it:   plato sandbox start --force -n {name} ...\n"
                    f"  Run both:     plato sandbox start -n {name}-2 ..."
                )
                raise typer.Exit(1)
            else:
                # Tearing down someone's running sandbox is not a detail to
                # hide behind --verbose.
                if not json_output:
                    out.super_console.print(
                        f"[yellow]--force: stopping the existing '{name}' sandbox "
                        f"(session {existing.get('session_id')}) first[/yellow]"
                    )
                _stop_sandbox(client, out, name, existing, remove_slot=True)
        return

    if siblings and not json_output:
        listed = ", ".join(str(s.get("name")) for s in siblings)
        out.super_console.print(
            f"[yellow]Note:[/yellow] {len(siblings)} sandbox(es) already started in this directory "
            f"([cyan]{listed}[/cyan]); this one gets its own slot and its own VM.\n"
            "[dim]  plato sandbox list   — see them all\n"
            "  plato sandbox stop -n <name>   — stop one[/dim]"
        )


@sandbox_app.command(name="start")
def sandbox_start(
    working_dir: WorkingDirArg,
    name: StartNameArg,
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
    connect_network: bool = typer.Option(
        True,
        "--network/--no-network",
        help="Make the VM discoverable and reachable over the network (WireGuard) after boot, "
        "so SSH, port-forwarding, --manual-control and the other VM-access commands work "
        "(default: on). This controls whether you can REACH the VM, not the VM's own "
        "connectivity: --no-network does NOT disable networking or internet inside the VM. "
        "It leaves the VM unreachable from outside except through its public sim URL "
        "(port 80 through the router), so SSH and friends will not work. Usually leave it on; "
        "a VM started with --no-network can be made reachable later with "
        "`plato sandbox connect-network`.",
    ),
    timeout: int = typer.Option(1800, "--timeout", "-t", help="VM lifetime in seconds"),
    provider: str | None = typer.Option(
        None,
        "--provider",
        help="VM provider for blank/config modes: firecracker or qemu. Use qemu for Windows VMs.",
    ),
    manual_control: bool = typer.Option(
        False,
        "--manual-control",
        help="Windows (qemu) VMs: human RDP override. Once the VM boots and is SSH-reachable, "
        "disable the console auto-logon reclaim (Winlogon ForceAutoLogon=0) that otherwise "
        "bounces an RDP session seconds after it connects, then print the browser RDP URL.",
    ),
    attach_session: bool = typer.Option(
        False,
        "--attach-session/--no-attach-session",
        envvar="PLATO_SANDBOX_ATTACH_SESSION",
        help="Attach the sandbox to the Chronos session in $SESSION_ID (set on Chronos VMs) "
        "so it is tracked and lifecycle-managed as part of that session.",
    ),
    chronos_session: str | None = typer.Option(
        None,
        "--chronos-session",
        help="Explicit Chronos session id to attach to (implies --attach-session).",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        "-f",
        help="If -n/--name is already taken by a running sandbox, stop it first instead of refusing.",
    ),
    json_output: JsonArg = False,
    verbose: VerboseArg = False,
):
    """Start a new sandbox VM.

    Creates a sandbox from a simulator, artifact, config file, or blank VM, and
    saves it to a named slot under .plato/sandboxes/ for use by other commands.
    Several sandboxes can coexist in one working directory: an unnamed start
    takes the next free slot (espocrm, espocrm-2, …) rather than overwriting a
    running sibling.

    Examples:
        plato sandbox start -s espocrm           # From simulator
        plato sandbox start -c                   # From plato-config.yml
        plato sandbox start -a <uuid>            # From artifact
        plato sandbox start -b --cpus 4          # Blank VM
        plato sandbox start -b --provider qemu   # Blank Windows VM
        plato sandbox start -b --provider qemu --manual-control   # Windows VM a human can RDP into
        plato sandbox start -a <uuid> --manual-control            # Same, resuming a Windows artifact
        plato sandbox start -s espocrm -n crm-a  # Into a named slot
        plato sandbox start -s espocrm --attach-session   # Track under the current Chronos session
    """
    if manual_control:
        # SSH (which applies the guest-side registry change) rides the sandbox
        # network, and for blank/config modes the provider is known up front —
        # fail fast instead of after a full VM boot.
        err_console = Console(stderr=True)
        if not connect_network:
            err_console.print(
                "[red]--manual-control needs SSH, which needs the VM reachable over the sandbox "
                "network; drop --no-network[/red]"
            )
            raise typer.Exit(1)
        if (blank or from_config) and provider != "qemu":
            err_console.print("[red]--manual-control needs a Windows VM: pass --provider qemu[/red]")
            raise typer.Exit(1)
    # Explicit --chronos-session must attach or fail; the ambient env-var
    # default (on every Chronos VM) degrades to a standalone sandbox with a
    # warning so legacy flows keep working on sessions that can't attach.
    attach_strict = chronos_session is not None
    chronos_session_id = chronos_session
    if attach_session and not chronos_session_id:
        chronos_session_id = os.environ.get("SESSION_ID")
        if not chronos_session_id or chronos_session_id == "local":
            Console(stderr=True).print(
                "[red]--attach-session needs the SESSION_ID env var (set on Chronos VMs) "
                "or an explicit --chronos-session <id>[/red]"
            )
            raise typer.Exit(1)

    with sandbox_context(working_dir, json_output, verbose) as (client, out):
        _guard_existing_sandbox(client, out, name, force, json_output)
        out.console.print("Starting sandbox...")

        if simulator:
            state = client.start(
                mode="simulator",
                simulator_name=simulator,
                dataset=dataset,
                connect_network=connect_network,
                timeout=timeout,
                provider=provider,
                chronos_session_id=chronos_session_id,
                attach_strict=attach_strict,
                name=name,
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
                provider=provider,
                chronos_session_id=chronos_session_id,
                attach_strict=attach_strict,
                name=name,
            )
        elif artifact_id:
            state = client.start(
                mode="artifact",
                artifact_id=artifact_id,
                dataset=dataset,
                connect_network=connect_network,
                timeout=timeout,
                provider=provider,
                chronos_session_id=chronos_session_id,
                attach_strict=attach_strict,
                name=name,
            )
        elif from_config:
            state = client.start(
                mode="config",
                dataset=dataset,
                connect_network=connect_network,
                timeout=timeout,
                provider=provider,
                chronos_session_id=chronos_session_id,
                attach_strict=attach_strict,
                name=name,
            )
        else:
            out.error("Must specify a mode: --blank, --artifact-id, --simulator, or --from-config.")
            raise typer.Exit(1)

        if manual_control:
            try:
                client.enable_manual_control(state)
            except Exception as e:
                # The sandbox itself is up — surface that alongside the failure
                # so the user doesn't assume the whole start needs redoing.
                out.error(f"Sandbox started, but manual-control setup failed: {e}")
                raise typer.Exit(1) from e

        out.success(state, "Sandbox started")


def mcp_config_from_flags(enabled: bool | None, port: int | None, path: str | None) -> ArtifactMcpConfig | None:
    """Assemble the artifact MCP config from the --mcp-* flags.

    Returns ``None`` when none of them was passed, so the backend inherits the
    parent artifact's config instead of being handed an all-empty override.
    ``--mcp-port``/``--mcp-path`` on their own mean "serve MCP here", so they
    imply ``enabled=True``.
    """
    if enabled is None and port is None and path is None:
        return None
    if port is not None and not 1 <= port <= 65535:
        raise typer.BadParameter("must be between 1 and 65535", param_hint="--mcp-port")
    if path is not None and (path.split() != [path] or not path.startswith("/")):
        raise typer.BadParameter(
            "must start with '/' and contain no whitespace, e.g. /api/mcp", param_hint="--mcp-path"
        )
    # model_validate, not the constructor: port/path are root models on the generated type
    return ArtifactMcpConfig.model_validate(
        {"enabled": True if enabled is None else enabled, "port": port, "path": path}
    )


SnapshotResponse = AppApiV2SchemasSessionCreateSnapshotResponse | CreateSnapshotResult | CreateCheckpointResult


class SnapshotStatus(BaseModel):
    """What a snapshot consumer needs to know: which artifact, and whether it can be used yet."""

    artifact_id: str
    status: str
    archive_type: str
    simulator_name: str
    dataset: str
    parent_artifact_id: str | None = None
    snapshotted_at: datetime | None = None

    @classmethod
    def of(cls, artifact: ArtifactInfoResponse) -> "SnapshotStatus":
        return cls.model_validate(artifact.model_dump())


class SnapshotReport(BaseModel):
    """One entry per job the snapshot request covered: the artifact it created, or why it refused."""

    artifacts: list[SnapshotStatus]
    errors: list[str] | None = None

    @property
    def failed(self) -> bool:
        return bool(self.errors) or any(a.status == ARTIFACT_STATUS_FAILED for a in self.artifacts)


class SnapshotFailed(Exception):
    """The snapshot response is unusable (a job succeeded without an artifact id)."""


class SandboxStatusReport(BaseModel):
    """``plato sandbox status``: the local slot, its heartbeat, its last snapshot, the remote session."""

    slot: str | None
    local: dict[str, Any] | None
    heartbeat: dict[str, str | int] | None
    snapshot: SnapshotStatus | None
    remote: SessionDetailsResponse | dict[str, Any]


def _snapshot_results(response: SnapshotResponse) -> list[CreateSnapshotResult | CreateCheckpointResult]:
    """The session snapshot answers one result per job; the job endpoints answer a single result."""
    if isinstance(response, AppApiV2SchemasSessionCreateSnapshotResponse):
        return list(response.results.values())
    return [response]


def _created_artifact_ids(results: list[CreateSnapshotResult | CreateCheckpointResult]) -> list[str]:
    artifact_ids: list[str] = []
    for result in results:
        if not result.success:
            continue
        if result.artifact_id is None:
            raise SnapshotFailed("Snapshot succeeded but the backend returned no artifact id")
        artifact_ids.append(result.artifact_id)
    return artifact_ids


def _exit_failed(out: "Output", message: str) -> NoReturn:
    """Exit 1 after the report has been printed.

    Under ``--json`` the report already carries the failure (``errors`` or a
    ``failed`` status); a second error document would corrupt stdout.
    """
    if not out.json_mode:
        out.error(message)
    raise typer.Exit(1)


def _snapshot_status(
    client: SandboxClient, out: "Output", artifact_id: str, *, wait: bool, timeout: float
) -> SnapshotStatus:
    """The artifact's current status — or, with ``wait``, its final one.

    A wait timeout is not a failed snapshot — it is still uploading — so the
    error points at ``snapshot-status`` rather than at retrying.
    """
    if not wait:
        return SnapshotStatus.of(client.artifacts.get(artifact_id))
    out.console.print(f"[dim]Waiting up to {timeout:g}s for artifact {artifact_id} to be ready...[/dim]")
    # A wait can outlast the sandbox's idle lease; renew it like ssh/tunnel do.
    with _renewing_lease():
        try:
            return SnapshotStatus.of(client.artifacts.wait_for_ready(artifact_id, timeout=timeout))
        except TimeoutError as e:
            raise TimeoutError(f"{e}; check again with `plato sandbox snapshot-status`") from e


def _report_snapshot(
    client: SandboxClient, out: "Output", response: SnapshotResponse, *, wait: bool, timeout: float
) -> None:
    """Report the artifact(s) a snapshot request created, with their real status.

    The snapshot endpoints return once the artifact row exists — the upload
    runs on the VM afterwards — so "created" only ever means ``creating``.
    The status is read back from the artifact endpoint.
    """
    results = _snapshot_results(response)
    errors = [result.error or "unknown error" for result in results if not result.success]
    report = SnapshotReport(
        artifacts=[
            _snapshot_status(client, out, artifact_id, wait=wait, timeout=timeout)
            for artifact_id in _created_artifact_ids(results)
        ],
        errors=errors or None,
    )

    out.success(report, "Snapshot requested")
    if not out.json_mode and any(status.status != ARTIFACT_STATUS_READY for status in report.artifacts):
        out.super_console.print(
            "[dim]The artifact cannot be started from until its status is 'ready'. "
            "Check with `plato sandbox snapshot-status`, or pass --wait.[/dim]"
        )
    if report.failed:
        _exit_failed(out, "Snapshot failed: " + "; ".join(errors or ["the artifact is in status 'failed'"]))


# CHECKED
@sandbox_app.command(name="snapshot")
def sandbox_snapshot(
    working_dir: WorkingDirArg,
    name: NameArg,
    session_id: SessionIdArg,
    mode: ModeArg,
    dataset: DatasetArg,
    job_id: JobIdArg,
    job: Annotated[
        bool,
        typer.Option(
            "--job",
            help="Snapshot only this env's job (POST /api/v2/jobs/{job_id}/checkpoint) instead of the whole session.",
        ),
    ] = False,
    target: Annotated[
        str | None,
        typer.Option(
            "--target",
            help="Routing target domain stored on the artifact, e.g. <sim>.web.plato.so; inherited from the parent artifact when omitted.",
        ),
    ] = None,
    mcp_enabled: Annotated[
        bool | None,
        typer.Option(
            "--mcp-enabled/--no-mcp-enabled",
            help="Turn the artifact's MCP endpoint on/off. Pass none of the --mcp-* flags to inherit the parent artifact's config.",
        ),
    ] = None,
    mcp_port: Annotated[
        int | None,
        typer.Option("--mcp-port", help="Port the MCP endpoint is served on (1-65535). Implies --mcp-enabled."),
    ] = None,
    mcp_path: Annotated[
        str | None,
        typer.Option(
            "--mcp-path", help="HTTP path the MCP endpoint is served at, e.g. /api/mcp. Implies --mcp-enabled."
        ),
    ] = None,
    wait: Annotated[
        bool,
        typer.Option(
            "--wait/--no-wait",
            help="Block until the artifact is ready (or failed) instead of returning while it is still creating.",
        ),
    ] = False,
    timeout: Annotated[
        float,
        typer.Option("--timeout", help="Seconds to wait for the artifact with --wait.", min=1),
    ] = ARTIFACT_WAIT_TIMEOUT_SECONDS,
    json_output: JsonArg = False,
    verbose: VerboseArg = False,
):
    """Create a snapshot of the current sandbox state.

    Captures VM state and database for later restoration. Snapshotting is
    asynchronous: the command returns as soon as the artifact exists, in
    status ``creating``, while the VM uploads the snapshot in the background.
    The artifact can be started from only once it is ``ready`` — pass
    ``--wait`` to block until then, or check later with
    ``plato sandbox snapshot-status``.

    Examples:
        plato sandbox snapshot                    # Uses mode from state.json
        plato sandbox snapshot --wait             # Return only once the artifact is ready
        plato sandbox snapshot --mode config      # Override to pass local plato-config.yml, flows and login credentials to artifact
        plato sandbox snapshot --job              # Snapshot one env in a multi-env (unified) session
        plato sandbox snapshot --target grist.web.plato.so   # Record the routing domain on the artifact
        plato sandbox snapshot --mcp-port 3000 --mcp-path /api/mcp   # Serve MCP from the artifact (implies --mcp-enabled)
        plato sandbox snapshot --no-mcp-enabled   # Turn the artifact's MCP endpoint off
    """
    # Raised outside sandbox_context so a bad flag is a usage error, not a run failure.
    mcp = mcp_config_from_flags(mcp_enabled, mcp_port, mcp_path)

    with sandbox_context(working_dir, json_output, verbose) as (client, out):
        _renew_lease()
        if not job and state_field("attached"):
            # Session-level snapshot would snapshot every env in the shared
            # session; an attached sandbox only owns its job. Use the per-job
            # FULL snapshot (same op the session endpoint runs per job) — the
            # job checkpoint would reject from-scratch config/blank VMs.
            if not job_id:
                raise SandboxStateError("job_id")
            out.console.print("[dim]Attached sandbox — full snapshot of only this env's job[/dim]")
            full_response = client.snapshot_job_full(
                job_id=require(job_id, "job_id"), mode=mode, dataset=dataset, target=target, mcp=mcp
            )
            _report_snapshot(client, out, full_response, wait=wait, timeout=timeout)
            return
        if job:
            if not job_id:
                raise SandboxStateError("job_id")
            out.console.print("Creating job checkpoint...")
            response = client.snapshot_job(
                job_id=require(job_id, "job_id"), mode=mode, dataset=dataset, target=target, mcp=mcp
            )
            _report_snapshot(client, out, response, wait=wait, timeout=timeout)
            return

        out.console.print("Creating snapshot...")
        response = client.snapshot(
            session_id=require(session_id, "session_id"),
            mode=require(mode, "mode"),
            dataset=require(dataset, "dataset"),
            target=target,
            mcp=mcp,
        )
        _report_snapshot(client, out, response, wait=wait, timeout=timeout)


@sandbox_app.command(name="reset")
def sandbox_reset(
    working_dir: WorkingDirArg,
    name: NameArg,
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
        _renew_lease()
        if state_field("attached"):
            # Session-level reset would reset every env in the shared session.
            job_id = state_field("job_id")
            if not job_id:
                raise SandboxStateError("job_id")
            out.console.print("Resetting sandbox (job-scoped — attached to shared session)...")
            result = client.reset_job(job_id=require(job_id, "job_id"))
            out.success(result, "Sandbox reset")
            return
        out.console.print("Resetting sandbox...")
        result = client.reset(session_id=require(session_id, "session_id"))
        out.success(result, "Sandbox reset")


def _stop_sandbox(
    client: SandboxClient,
    out: "Output",
    name: str | None,
    state: dict,
    remove_slot: bool = False,
) -> dict:
    """Tear a sandbox down remotely, then locally.

    The local half is one shared path (``SandboxStore.stop_local``): mark the
    slot stopped — which is also the heartbeat's own exit signal — kill the
    heartbeat a beat early as a courtesy, drop the slot's SSH material, and
    reconcile the links and index.
    """
    session_id = require(state.get("session_id"), "session_id")
    result: dict = {"status": "stopped", "session_id": session_id}

    try:
        if state.get("attached"):
            # Attached sandboxes share their session with the owning Chronos
            # session — closing it would kill every env in that session.
            job_id = require(state.get("job_id"), "job_id")
            out.console.print("Stopping sandbox (removing env from shared session)...")
            client.remove_env(session_id=session_id, job_id=job_id)
            result["job_id"] = job_id
        else:
            out.console.print("Stopping sandbox...")
            client.stop(session_id=session_id, heartbeat_pid=state.get("heartbeat_pid"))
    except Exception as exc:
        # A session that is already finished still needs its local half torn
        # down — otherwise the slot keeps looking live and its heartbeat keeps
        # running. Any other failure means the VM may well still be up, so
        # leave the slot, the SSH key and the heartbeat exactly as they are.
        if not is_session_gone(exc):
            raise
        out.console.print("[dim]Session was already finished — cleaning up locally[/dim]")
        result["status"] = "already-stopped"

    if name:
        result.update(client.cleanup_slot(name, remove=remove_slot))
        result["name"] = name
    return result


# CHECKED
@sandbox_app.command(name="stop")
def sandbox_stop(
    working_dir: WorkingDirArg,
    name: NameArg,
    session_id: SessionIdArg,
    all_sandboxes: bool = typer.Option(False, "--all", help="Stop every sandbox in this working directory."),
    remove: bool = typer.Option(
        False, "--remove", help="Delete the slot as well, instead of keeping it for reference."
    ),
    json_output: JsonArg = False,
    verbose: VerboseArg = False,
):
    """Stop and destroy a sandbox.

    Terminates the VM, kills its heartbeat process and removes its SSH key.
    The slot is kept (marked stopped) for reference unless --remove is passed.

    Examples:
        plato sandbox stop                 # The current sandbox
        plato sandbox stop -n crm-a        # A specific one
        plato sandbox stop --all           # Everything in this directory
    """
    with sandbox_context(working_dir, json_output, verbose) as (client, out):
        store = client.store

        if all_sandboxes:
            targets = [(str(s.get("name")), s) for s in local_live_slots(store)]
            if not targets:
                out.success({"stopped": []}, "No running sandboxes here")
                return
            stopped = []
            failures = []
            for slot, state in targets:
                try:
                    stopped.append(_stop_sandbox(client, out, slot, state, remove_slot=remove))
                except Exception as exc:  # keep going: one bad slot shouldn't strand the rest
                    failures.append({"name": slot, "error": str(exc)})
                    out.error(f"Failed to stop '{slot}': {exc}")
            out.success(
                {"stopped": stopped, "failed": failures},
                f"Stopped {len(stopped)} sandbox(es)" + (f", {len(failures)} failed" if failures else ""),
            )
            # Those sandboxes are still running; a script that batches this must
            # not read "stopped 0 of 5" as success.
            if failures:
                raise typer.Exit(1)
            return

        slot = store.resolve(name)
        state = store.load(slot) if slot else None
        if state is not None and session_id and session_id != state.get("session_id"):
            # An explicit --session-id that isn't this slot's names a foreign
            # session. Close only that, and touch nothing local: reusing the
            # slot's heartbeat pid, job id or SSH key here would tear down the
            # selected sandbox — which is still running — on its behalf.
            out.console.print(f"[dim]--session-id {session_id} is not slot '{slot}' — stopping that session only[/dim]")
            state, slot = None, None
        if state is None:
            # No slot to work from: all we can act on is the session itself.
            state = {"session_id": require(session_id, "session_id")}
            slot = None

        result = _stop_sandbox(client, out, slot, state, remove_slot=remove)
        out.success(result, "Sandbox stopped")


# CHECKED
@sandbox_app.command(name="connect-network")
def sandbox_connect_network(
    working_dir: WorkingDirArg,
    name: NameArg,
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
        _renew_lease()
        if state_field("attached"):
            out.console.print(
                "[yellow]Attached sandbox: this connects WireGuard for the ENTIRE shared "
                "session (every env in it), not just this sandbox.[/yellow]"
            )
        out.console.print("Connecting to network...")
        result = client.connect_network(session_id=require(session_id, "session_id"))
        out.success(result, "Network connected")


@sandbox_app.command(name="artifact")
def sandbox_artifact(
    working_dir: WorkingDirArg,
    name: NameArg,
    artifact_id: Annotated[
        str | None,
        typer.Argument(help="Artifact id. Defaults to the artifact this slot last snapshotted."),
    ] = None,
    json_output: JsonArg = False,
    verbose: VerboseArg = False,
):
    """Show an artifact record: status, parent, dataset, login credentials and MCP config.

    Config-mode snapshots derive the credentials from plato-config.yml
    (``metadata.credentials`` or the login ``variables``); the MCP config comes
    from the ``--mcp-*`` snapshot flags. This is how to check what an artifact
    actually carries — ``mcp_config`` is what is stored on it, ``mcp`` what the
    backend resolves after the simulator/parent fallbacks.

    Examples:
        plato sandbox artifact                       # The slot's last snapshot
        plato sandbox artifact <uuid> --json
    """
    with sandbox_context(working_dir, json_output, verbose) as (client, out):
        target = artifact_id or state_field("artifact_id")
        if not target:
            raise SandboxStateError("artifact_id")
        info = client.artifacts.get(str(target))
        out.success(info, "Artifact")
        if not json_output:
            out.super_console.print(f"[dim]MCP stored: {describe_mcp_config(info.mcp_config)}[/dim]")
            out.super_console.print(f"[dim]MCP resolved: {describe_mcp_config(info.mcp)}[/dim]")


@sandbox_app.command(name="snapshot-status")
def sandbox_snapshot_status(
    working_dir: WorkingDirArg,
    name: NameArg,
    artifact_id: Annotated[
        str | None,
        typer.Argument(help="Artifact id. Defaults to the artifact this slot last snapshotted."),
    ] = None,
    wait: Annotated[
        bool,
        typer.Option("--wait/--no-wait", help="Poll until the artifact is ready or failed."),
    ] = False,
    timeout: Annotated[
        float,
        typer.Option("--timeout", help="Seconds to wait for the artifact with --wait.", min=1),
    ] = ARTIFACT_WAIT_TIMEOUT_SECONDS,
    json_output: JsonArg = False,
    verbose: VerboseArg = False,
):
    """Show whether a snapshot has finished: creating, ready or failed.

    ``plato sandbox snapshot`` returns while the VM is still uploading the
    snapshot; this is the command to check on it. ``creating`` means the
    upload is in flight, ``ready`` means the artifact can be started from
    (``plato sandbox start -a <id>``), ``failed`` means the upload failed.
    Exits non-zero when the artifact has failed, or when ``--wait`` runs out
    of time. ``plato sandbox artifact`` shows the full record.

    Examples:
        plato sandbox snapshot-status                # The slot's last snapshot
        plato sandbox snapshot-status --wait         # Block until ready/failed
        plato sandbox snapshot-status <uuid> --json
    """
    with sandbox_context(working_dir, json_output, verbose) as (client, out):
        _renew_lease()
        target = artifact_id or state_field("artifact_id")
        if not target:
            raise SandboxStateError("artifact_id", hint="Run `plato sandbox snapshot` first, or pass an artifact id")
        status = _snapshot_status(client, out, str(target), wait=wait, timeout=timeout)
        out.success(status, "Snapshot status")
        if not out.json_mode and status.status == ARTIFACT_STATUS_READY:
            out.super_console.print(f"[dim]Start from it with `plato sandbox start -a {status.artifact_id}`[/dim]")
        if status.status == ARTIFACT_STATUS_FAILED:
            _exit_failed(out, f"Artifact {status.artifact_id} failed to snapshot")


def _last_snapshot_status(client: SandboxClient, out: "Output", local_state: dict | None) -> SnapshotStatus | None:
    """Status of the slot's last snapshot, if it still exists.

    The slot only remembers the artifact id; the backend may since have
    deleted the artifact (expiry, cleanup). That is worth a warning, not a
    failed status command.
    """
    artifact_id = local_state.get("artifact_id") if local_state else None
    if not artifact_id:
        return None
    try:
        return SnapshotStatus.of(client.artifacts.get(str(artifact_id)))
    except NotFoundError:
        if not out.json_mode:
            out.super_console.print(f"[yellow]Last snapshot {artifact_id} no longer exists on the backend[/yellow]")
        return None


# CHECKED
@sandbox_app.command(name="status")
def sandbox_status(
    working_dir: WorkingDirArg,
    name: NameArg,
    session_id: SessionIdArg,
    json_output: JsonArg = False,
    verbose: VerboseArg = False,
):
    """Show current sandbox status.

    Displays the local slot, heartbeat health and remote session details.

    Example:
        plato sandbox status
        plato sandbox status --json
    """
    with sandbox_context(working_dir, json_output, verbose) as (client, out):
        _renew_lease()
        out.console.print("Fetching status...")
        store = client.store
        slot = store.resolve(name)
        local_state = store.load(slot) if slot else None

        # Heartbeat health is the single most useful local signal: "VM shutdown
        # due to heartbeat miss" means this process died, and nothing else
        # surfaces that.
        heartbeat = None
        if local_state is not None:
            pid = local_state.get("heartbeat_pid")
            if local_state.get("attached"):
                heartbeat = {"state": "n/a (attached — the Chronos session heartbeats)"}
            elif not pid:
                heartbeat = {"state": "none recorded"}
            else:
                alive = heartbeat_alive(pid)
                heartbeat = {
                    "state": "running" if alive else "stopped",
                    "pid": pid,
                    "log": str(heartbeat_log_path(str(local_state.get("session_id")))),
                }

        details = client.status(session_id=require(session_id, "session_id"))

        # The slot remembers the last snapshot's artifact id, but not whether
        # the (asynchronous) snapshot has finished — ask the artifact endpoint.
        snapshot = _last_snapshot_status(client, out, local_state)

        out.success(
            SandboxStatusReport(slot=slot, local=local_state, heartbeat=heartbeat, snapshot=snapshot, remote=details),
            "Sandbox Status",
        )


# CHECKED
@sandbox_app.command(name="state")
def sandbox_state(
    working_dir: WorkingDirArg,
    name: NameArg,
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
        _renew_lease()
        out.console.print("Fetching mutations...")
        if state_field("attached"):
            # Session-level state merges mutations from every env in the
            # shared session; an attached sandbox only owns its job.
            job_id = state_field("job_id")
            if not job_id:
                raise SandboxStateError("job_id")
            job_result = client.state_job(job_id=require(job_id, "job_id"))
            # Same shape as the session-level response, scoped to our job, so
            # `.results[]`-style consumers (env-create/env-fix templates, pm
            # data-ref checks) keep working unchanged.
            wrapped = SessionStateResponse(
                session_id=require(session_id, "session_id"), results={str(job_id): job_result}
            )
            out.success(wrapped, f"State: {job_id}")
            return
        result = client.state(session_id=require(session_id, "session_id"))

        out.success(result, f"State: {result.session_id}")


# CHECKED
@sandbox_app.command(name="start-worker")
def sandbox_start_worker(
    working_dir: WorkingDirArg,
    name: NameArg,
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
        _renew_lease()
        out.console.print(f"Starting worker: {simulator}, dataset: {dataset}")

        client.start_worker(
            job_id=require(job_id, "job_id"),
            simulator=require(simulator, "simulator_name"),
            dataset=require(dataset, "dataset"),
            wait_timeout=wait_timeout,
            use_api=api,
        )

        out.success({"status": "started"}, "Worker started")


# CHECKED
@sandbox_app.command(name="sync")
def sandbox_sync(
    working_dir: WorkingDirArg,
    name: NameArg,
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
        _renew_lease()
        out.console.print(f"Syncing {working_dir} -> {f'/home/plato/worktree/{simulator}'}")

        result = client.sync(
            session_id=require(session_id, "session_id"),
            simulator=require(simulator, "simulator_name"),
            timeout=timeout,
        )

        out.success(result, "Sync complete")


# CHECKED
@sandbox_app.command(name="start-services")
def sandbox_start_services(
    working_dir: WorkingDirArg,
    name: NameArg,
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
        _renew_lease()
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
    name: NameArg,
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
        _renew_lease()
        url = require(public_url, "public_url")
        out.console.print(f"Running flow '{flow_name}' on {url}")

        client.run_flow(
            url=url,
            flow_name=flow_name,
            dataset=require(dataset, "dataset"),
            use_api=api,
            job_id=require(job_id, "job_id") if api else None,
            headless=headless,
            keep_browser_open=keep_browser_open,
        )

        out.success({"flow_name": flow_name, "url": url}, "Flow complete")


@sandbox_app.command(name="pull-config")
def sandbox_pull_config(
    working_dir: WorkingDirArg,
    name: NameArg,
    dataset: DatasetArg,
    artifact_id: str = typer.Option(
        None,
        "--artifact-id",
        "-a",
        help="Artifact UUID (reads from the sandbox slot if not provided)",
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
            artifact_id = state_field("artifact_id")
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
    name: NameArg,
    session_id: SessionIdArg,
    job_id: JobIdArg,
    simulator_name: SimulatorNameArg,
    json_output: JsonArg = False,
    verbose: VerboseArg = False,
):
    """Clear the audit_log table(s) in the sandbox database.

    This clears audit logs that track database mutations, which is useful
    for resetting state between test runs.
    """
    with sandbox_context(working_dir, json_output, verbose) as (client, out):
        _renew_lease()
        attached = bool(state_field("attached"))
        if attached:
            # The job group IS the shared session; group-level cleanup would
            # truncate audit_log on every sibling env.
            out.console.print("[dim]Attached sandbox — clearing audit logs for this env's job only[/dim]")
        out.console.print("Clearing audit logs...")
        result = client.clear_audit(
            job_group_id=require(session_id, "session_id"),
            job_id=job_id,
            simulator_name=simulator_name,
            job_scoped=attached,
            mesh_ip=state_field("mesh_ip") if attached else None,
        )

        if not result.success:
            raise Exception(result.error or "Failed to clear audit logs")

        out.success({"success": result.success}, "Audit logs cleared")


@sandbox_app.command(name="audit-ui")
def sandbox_audit_ui(
    working_dir: WorkingDirArg,
    name: NameArg,
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
        _renew_lease()
        try:
            client.run_audit_ui(
                job_id=job_id,
                dataset=dataset or "base",
                no_tunnel=no_tunnel,
                mesh_ip=state_field("mesh_ip") if state_field("attached") else None,
            )
        except ValueError as e:
            out.error(str(e))
            raise typer.Exit(1) from None


# =============================================================================
# SLOT MANAGEMENT
# =============================================================================


def _age(seconds: float | None) -> str:
    if not seconds:
        return "-"
    delta = max(0, int(time.time() - seconds))
    if delta < 90:
        return f"{delta}s"
    if delta < 5400:
        return f"{delta // 60}m"
    return f"{delta // 3600}h"


def _expiry(expires_at: float | None) -> str:
    if not expires_at:
        return "-"
    remaining = int(expires_at - time.time())
    if remaining <= 0:
        return "[red]expired[/red]"
    return f"{remaining // 60}m left"


@sandbox_app.command(name="list")
def sandbox_list(
    working_dir: WorkingDirArg,
    all_dirs: bool = typer.Option(
        False, "--all", "-a", help="Every sandbox this machine has started, not just this directory."
    ),
    check: bool = typer.Option(False, "--check", help="Ask the backend for each sandbox's real status (slower)."),
    json_output: JsonArg = False,
    verbose: VerboseArg = False,
):
    """List sandboxes.

    Without --all, the slots in this working directory (the current one is
    marked *). With --all, the slots in every directory this machine has
    started sandboxes in (recorded in ~/.plato/sandboxes.json). The slot files
    are the source of truth either way — the machine-wide file is only an
    index of directories to read.

    Examples:
        plato sandbox list
        plato sandbox list --all --check
    """
    with sandbox_context(working_dir, json_output, verbose) as (client, out):
        store = client.store
        current = store.current()

        rows = []
        if all_dirs:
            this_dir = str(Path(working_dir).resolve())
            for directory in dict.fromkeys([*registered_dirs(), this_dir]):
                dir_store = SandboxStore(Path(directory))
                slots = dir_store.names()
                if not slots:
                    # Nothing there any more (or the directory itself is gone);
                    # its sandboxes' heartbeats exit on their own once the slot
                    # files disappear, so there is nothing left to show.
                    forget_dir(directory)
                    continue
                for slot in slots:
                    state = dir_store.load(slot) or {}
                    state.setdefault("name", slot)
                    state["working_dir"] = directory
                    rows.append(state)
            rows.sort(key=lambda r: r.get("created_at") or 0, reverse=True)
        else:
            for slot in store.names():
                state = store.load(slot) or {}
                state.setdefault("name", slot)
                state["working_dir"] = str(Path(working_dir).resolve())
                rows.append(state)

        if check:
            for row in rows:
                if row.get("stopped_at") or not row.get("session_id"):
                    continue
                row["remote_status"] = remote_job_status(client, str(row["session_id"]), row.get("job_id"))

        if json_output:
            out.success({"current": current, "sandboxes": rows})
            return

        if not rows:
            where = "on this machine" if all_dirs else f"in {working_dir}"
            out.super_console.print(f"[dim]No sandboxes {where}. Start one with `plato sandbox start`.[/dim]")
            return

        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("", style="bold", width=1)
        table.add_column("Name")
        table.add_column("Simulator")
        table.add_column("Session", style="dim")
        table.add_column("Heartbeat")
        table.add_column("Age")
        table.add_column("Timeout")
        if all_dirs:
            table.add_column("Working dir", style="dim")
        if check:
            table.add_column("Remote")

        for row in rows:
            if row.get("stopped_at"):
                beat = "[dim]stopped[/dim]"
            elif row.get("attached"):
                beat = "[dim]n/a (attached)[/dim]"
            elif heartbeat_alive(row.get("heartbeat_pid")):
                beat = f"[green]alive[/green] ({row.get('heartbeat_pid')})"
            else:
                beat = "[red]dead[/red]"
            cells = [
                "*" if row.get("name") == current and not all_dirs else "",
                str(row.get("name") or "-"),
                str(row.get("simulator_name") or row.get("mode") or "-"),
                str(row.get("session_id") or "-")[:12],
                beat,
                _age(row.get("created_at")),
                "[dim]stopped[/dim]" if row.get("stopped_at") else _expiry(row.get("expires_at")),
            ]
            if all_dirs:
                cells.append(str(row.get("working_dir") or "-"))
            if check:
                cells.append(str(row.get("remote_status") or "-"))
            table.add_row(*cells)

        out.super_console.print(table)


@sandbox_app.command(name="use")
def sandbox_use(
    working_dir: WorkingDirArg,
    slot: str = typer.Argument(..., help="Slot name to make current"),
    json_output: JsonArg = False,
    verbose: VerboseArg = False,
):
    """Make a sandbox the default for subsequent commands.

    Repoints .plato/current (and the .plato/state.json symlink every other tool
    reads) at this slot. For a single shell, `export PLATO_SANDBOX=<name>` does
    the same without touching any file.

    Example:
        plato sandbox use crm-a
    """
    with sandbox_context(working_dir, json_output, verbose) as (client, out):
        store = client.store
        target = slugify(slot)
        if target not in store.names():
            available = ", ".join(store.names()) or "none"
            out.error(f"No sandbox named '{target}' in {working_dir} (available: {available})")
            raise typer.Exit(1)
        store.set_current(target)
        out.success({"current": target}, f"Now using sandbox '{target}'")


@sandbox_app.command(name="gc")
def sandbox_gc(
    working_dir: WorkingDirArg,
    dry_run: bool = typer.Option(False, "--dry-run", help="Report what would be reaped, change nothing."),
    all_dirs: bool = typer.Option(
        True, "--all/--this-dir", help="Sweep every sandbox on this machine, not just this directory."
    ),
    json_output: JsonArg = False,
    verbose: VerboseArg = False,
):
    """Reap sandboxes whose VM is already finished on the backend.

    Little needs this any more: a heartbeat exits on its own when its slot is
    stopped or removed or its lease expires, and every command reconciles
    local debris. What remains is the case nothing local can observe — the
    backend finished a session while nobody was looking, leaving a slot that
    still looks live. This closes those out with the same teardown `stop`
    uses, and reaps heartbeats that predate slot ownership entirely (found by
    scanning the process table).

    Sandboxes the backend still reports as running — or that it cannot be
    reached about — are never touched.

    Examples:
        plato sandbox gc --dry-run
        plato sandbox gc
    """
    with sandbox_context(working_dir, json_output, verbose) as (client, out):
        this_dir = str(Path(working_dir).resolve())
        dirs = list(dict.fromkeys([*(registered_dirs() if all_dirs else []), this_dir]))

        reaped: list[dict] = []
        kept: list[dict] = []
        known_sessions = set()

        for directory in dirs:
            dir_store = SandboxStore(Path(directory))
            if not dry_run:
                with suppress(Exception):
                    dir_store.reconcile()
            slots = dir_store.names()
            if not slots:
                if not dry_run:
                    forget_dir(directory)
                continue
            for slot in slots:
                state = dir_store.load(slot) or {}
                session_id = state.get("session_id")
                if session_id:
                    known_sessions.add(str(session_id))
                if state.get("stopped_at") or not session_id:
                    # Already dead locally; reconcile above cleared anything
                    # it left behind. Stopped slots are kept for reference.
                    continue
                status = remote_job_status(client, str(session_id), state.get("job_id"))
                if is_live_status(status):
                    kept.append(
                        {
                            "name": slot,
                            "session_id": session_id,
                            "working_dir": directory,
                            "remote_status": status,
                        }
                    )
                    continue
                pid = state.get("heartbeat_pid")
                reaped.append(
                    {
                        "name": slot,
                        "session_id": session_id,
                        "working_dir": directory,
                        "remote_status": status,
                        "heartbeat_pid": pid if heartbeat_alive(pid) else None,
                    }
                )
                if not dry_run:
                    dir_store.stop_local(slot)

        # Heartbeats with no slot anywhere: the pre-slots clobber leaked these,
        # and nothing but the process table knows they exist.
        orphans = []
        for pid, session_id in running_heartbeats().items():
            if session_id in known_sessions:
                continue
            status = remote_job_status(client, session_id, None)
            if is_live_status(status):
                kept.append({"session_id": session_id, "heartbeat_pid": pid, "remote_status": status})
                continue
            orphans.append({"session_id": session_id, "heartbeat_pid": pid, "remote_status": status})
            if not dry_run:
                stop_heartbeat(pid)

        summary = {
            "reaped": reaped,
            "orphan_heartbeats": orphans,
            "still_running": kept,
            "dry_run": dry_run,
        }
        if json_output:
            out.success(summary)
            return

        verb = "Would reap" if dry_run else "Reaped"
        out.super_console.print(
            f"[green]{verb}[/green] {len(reaped)} dead sandbox(es) and "
            f"{len(orphans)} orphaned heartbeat(s); {len(kept)} still running."
        )
        for item in reaped + orphans:
            out.super_console.print(
                f"  [dim]-[/dim] {item.get('name') or '(no slot)'} "
                f"session={str(item.get('session_id'))[:12]} "
                f"status={item.get('remote_status')} "
                f"heartbeat={item.get('heartbeat_pid') or '-'}"
            )
        for item in kept:
            out.super_console.print(
                f"  [green]kept[/green] {item.get('name') or '(no slot)'} "
                f"session={str(item.get('session_id'))[:12]} status={item.get('remote_status')}"
            )


# =============================================================================
# SSH & TUNNEL COMMANDS
# =============================================================================


@sandbox_app.command(name="ssh", context_settings={"allow_extra_args": True, "ignore_unknown_options": True})
def sandbox_ssh(
    working_dir: WorkingDirArg,
    ctx: typer.Context,
    name: NameArg,
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
        _renew_lease()
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
                # From the working directory: the config's IdentityFile is
                # relative to it, so running from anywhere else (which is the
                # normal case with -w) fails with "Permission denied (publickey)".
                with _renewing_lease():
                    result = subprocess.run(cmd, cwd=client.working_dir)
                raise typer.Exit(result.returncode)
            except KeyboardInterrupt:
                raise typer.Exit(130) from None


@sandbox_app.command(name="tunnel")
def sandbox_tunnel(
    working_dir: WorkingDirArg,
    name: NameArg,
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
        _renew_lease()
        if not job_id:
            out.error("No job_id found. Run 'plato sandbox start' first.")
            raise typer.Exit(1)

        local = local_port or remote_port
        # Attached sandboxes forward straight to the mesh IP (in-VPC) instead
        # of hairpinning through the TLS gateway.
        mesh_ip = state_field("mesh_ip") if state_field("attached") else None
        if mesh_ip:
            out.console.print(f"[dim]Using session mesh IP {mesh_ip} (direct, no gateway)[/dim]")
        tunnel = client.tunnel(job_id, remote_port, local, bind_address, mesh_ip=mesh_ip)

        try:
            tunnel.start()
            out.console.print(f"[green]Tunnel:[/green] {bind_address}:{local} -> VM:{remote_port}")
            out.console.print("[dim]Ctrl+C to stop[/dim]")
            with _renewing_lease():
                while True:
                    time.sleep(1)
        except KeyboardInterrupt:
            out.console.print("\n[yellow]Closed[/yellow]")
        finally:
            tunnel.stop()
