"""Plato Chronos CLI - Launch and manage Chronos jobs."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import tempfile
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Annotated

import typer
from rich.table import Table

from plato.chronos.sdk import Chronos
from plato.cli.chronos.settings import get_settings
from plato.cli.utils import console

chronos_app = typer.Typer(help="Chronos job management commands.")
logger = logging.getLogger(__name__)
settings = get_settings()


def _require_api_key(api_key: str | None) -> str:
    """Validate API key is provided, exit if not."""
    if not api_key:
        console.print("[red]No API key provided[/red]")
        console.print("Set PLATO_API_KEY environment variable or use --api-key")
        raise typer.Exit(1)
    return api_key


@chronos_app.command()
def launch(
    config: Path = typer.Argument(
        ...,
        help="Path to job config JSON file",
        exists=True,
        readable=True,
    ),
    prerelease: bool = typer.Option(
        False,
        "--prerelease",
        help="Allow prerelease versions (dev, alpha, beta, rc) for packages",
    ),
    chronos_url: str = typer.Option(
        None,
        "--url",
        "-u",
        envvar="CHRONOS_URL",
        help="Chronos API URL",
    ),
    api_key: str = typer.Option(
        None,
        "--api-key",
        "-k",
        envvar="PLATO_API_KEY",
        help="Plato API key for authentication",
    ),
):
    """Launch a Chronos job from a config file.

    Submits the job to Chronos API which:
    - Gets the base image from the world's schema.json
    - Installs the world package via uv at runtime
    - World code is NOT baked into the image

    Package format: "plato-world-name:version" (e.g., plato-world-structured-execution:0.1.0)

    """
    import json

    from pydantic import ValidationError

    from plato.chronos.models import LaunchJobRequest

    chronos_url = chronos_url or settings.chronos_url
    api_key = _require_api_key(api_key)

    config_path = Path(config).expanduser().resolve()

    # Load config file WITHOUT expanding ${VAR} references — the Chronos
    # backend stores the raw template and substitutes env vars at runtime so
    # re-runs always pick up the latest values.
    try:
        with open(config_path) as f:
            raw = json.load(f)
    except Exception as e:
        console.print(f"[red]Invalid config file: {e}[/red]")
        raise typer.Exit(1)

    # Strip non-launch fields
    raw.pop("dev", None)
    raw.pop("session", None)

    # Auto-inject plato_api_key into world.config if not present
    world_cfg = raw.get("world", {})
    if "config" not in world_cfg:
        world_cfg["config"] = {}
    if "plato_api_key" not in world_cfg.get("config", {}):
        world_cfg["config"]["plato_api_key"] = api_key

    if prerelease:
        raw["allow_prerelease"] = True

    # Validate with Pydantic model
    try:
        request = LaunchJobRequest.model_validate(raw)
    except ValidationError as e:
        console.print(f"[red]Invalid config:[/red]\n{e}")
        raise typer.Exit(1)

    console.print("[blue]Launching job via Chronos API...[/blue]")
    console.print(f"   World: {request.world.package}")
    if prerelease:
        console.print("   Prerelease: enabled")

    try:
        with Chronos(base_url=chronos_url, api_key=api_key) as client:
            resp = client.launch(
                package=request.world.package,
                config=request.world.config,
                tags=request.tags,
                runtime=request.world.runtime.model_dump() if request.world.runtime else None,
                allow_prerelease=request.allow_prerelease or False,
                world_name=request.world.world_name,
            )

        console.print("\n[green]Job launched successfully![/green]")
        console.print(f"   Session ID: {resp.session_id}")
        console.print(f"   Status: {resp.status}")
        console.print(f"\n[dim]View at: {chronos_url}/sessions/{resp.session_id}[/dim]")

    except Exception as e:
        console.print(f"[red]Failed to launch job: {e}[/red]")
        raise typer.Exit(1)


@chronos_app.command()
def stop(
    session_id: Annotated[str, typer.Argument(help="Session ID to stop")],
    chronos_url: str = typer.Option(
        None,
        "--url",
        "-u",
        envvar="CHRONOS_URL",
        help="Chronos API URL",
    ),
    api_key: str = typer.Option(
        None,
        "--api-key",
        "-k",
        envvar="PLATO_API_KEY",
        help="Plato API key for authentication",
    ),
):
    """Stop a running Chronos session."""
    chronos_url = chronos_url or settings.chronos_url
    api_key = _require_api_key(api_key)

    console.print(f"[yellow]Stopping session {session_id}...[/yellow]")

    try:
        with Chronos(base_url=chronos_url, api_key=api_key) as client:
            client.stop(session_id)
        console.print(f"[green]Session {session_id} stopped[/green]")
    except Exception as e:
        console.print(f"[red]Failed to stop session: {e}[/red]")
        raise typer.Exit(1)


@chronos_app.command()
def dev(
    config: Annotated[
        Path,
        typer.Argument(help="Path to dev config JSON file", exists=True, readable=True),
    ],
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Show detailed logs"),
    ] = False,
    memray: Annotated[
        bool,
        typer.Option("--memray", help="Run world under memray memory profiler"),
    ] = False,
    startup_profile_out: Annotated[
        Path | None,
        typer.Option("--startup-profile-out", help="Write startup timing profile JSON to this path"),
    ] = None,
):
    """Run world + agents on VMs with rsync hot reload."""
    from rich.logging import RichHandler

    from plato.cli.chronos.config import Config
    from plato.cli.chronos.dev.runner import DevRunner

    # Set up log file in /tmp
    timestamp = datetime.now(UTC).strftime("%Y%m%d_%H%M%S")
    log_file = Path(tempfile.gettempdir()) / f"chronos-dev-{timestamp}.log"
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(name)s %(levelname)s %(message)s"))

    # Configure logging with Rich handler for colored output + file handler
    rich_handler = RichHandler(
        rich_tracebacks=True,
        show_path=False,
        show_time=verbose,
    )
    if not verbose:
        # In non-verbose mode, default to WARNING but allow specific loggers through
        _always_show = {"plato.cli.chronos.dev.runner", "plato.cli.chronos.dev.sync"}
        rich_handler.addFilter(lambda record: record.levelno >= logging.WARNING or record.name in _always_show)
    logging.basicConfig(
        level=logging.DEBUG if verbose else logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[rich_handler, file_handler],
    )
    console.print(f"[dim]Logs: {log_file}[/dim]")
    # Suppress noisy libraries
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    if not os.environ.get("PLATO_API_KEY"):
        console.print("[red]PLATO_API_KEY environment variable required[/red]")
        raise typer.Exit(1)

    try:
        dev_config = Config.from_file(config)
    except json.JSONDecodeError as e:
        console.print(f"[red]Invalid JSON in {config}: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Failed to load config: {e}[/red]")
        if verbose:
            logger.exception("Failed to load dev config")
        raise typer.Exit(1)

    try:
        runner = DevRunner(
            config=dev_config,
            config_path=config,
            verbose=verbose,
            memray=memray,
            startup_profile_out=startup_profile_out,
        )
        asyncio.run(runner.run())
    except KeyboardInterrupt:
        raise typer.Exit(0)
    except Exception as e:
        if verbose:
            console.print(f"[red]Failed: {e}[/red]")
            logger.exception("Dev mode failed")
        raise typer.Exit(1)


# ---------------------------------------------------------------------------
# Credential refresh
# ---------------------------------------------------------------------------


class AgentType(str, Enum):
    claude = "claude"
    codex = "codex"


_CRED_PATHS = {
    AgentType.claude: Path.home() / ".claude" / ".credentials.json",
    AgentType.codex: Path.home() / ".codex" / "auth.json",
}

_ENV_KEYS = {
    AgentType.claude: "CLAUDE_OAUTH_CREDENTIALS",
    AgentType.codex: "CODEX_OAUTH_CREDENTIALS",
}


@chronos_app.command("refresh-creds")
def refresh_creds(
    agent: Annotated[AgentType, typer.Argument(help="Agent type: claude or codex")],
    env_file: Annotated[Path, typer.Argument(help="Path to .env file to update", exists=True)],
):
    """Read OAuth credentials and update the corresponding key in a .env file.

    Reads from ~/.claude/.credentials.json or ~/.codex/auth.json,
    compacts the JSON, and writes it as the value of CLAUDE_OAUTH_CREDENTIALS
    or CODEX_OAUTH_CREDENTIALS in the target .env file.
    """
    cred_path = _CRED_PATHS[agent]
    env_key = _ENV_KEYS[agent]

    if not cred_path.exists():
        console.print(f"[red]Credentials file not found: {cred_path}[/red]")
        raise typer.Exit(1)

    try:
        creds = json.loads(cred_path.read_text())
    except json.JSONDecodeError as e:
        console.print(f"[red]Invalid JSON in {cred_path}: {e}[/red]")
        raise typer.Exit(1)

    # Show expiry info if available
    expires_at = creds.get("expiresAt") or creds.get("expires_at")
    if expires_at:
        try:
            exp_dt = datetime.fromisoformat(expires_at.replace("Z", "+00:00"))
            remaining = exp_dt - datetime.now(UTC)
            mins = int(remaining.total_seconds() / 60)
            if mins < 0:
                console.print(f"[yellow]Warning: token expired {-mins} minutes ago[/yellow]")
            else:
                console.print(f"[dim]Token expires in {mins} minutes[/dim]")
        except (ValueError, TypeError):
            pass

    compact = json.dumps(creds, separators=(",", ":"))

    # Read existing .env and update or append the key
    env_path = Path(env_file)
    lines = env_path.read_text().splitlines()
    found = False
    for i, line in enumerate(lines):
        if line.startswith(f"{env_key}="):
            lines[i] = f"{env_key}={compact}"
            found = True
            break
    if not found:
        lines.append(f"{env_key}={compact}")

    env_path.write_text("\n".join(lines) + "\n")
    console.print(f"[green]Updated {env_key} in {env_file}[/green]")


# ---------------------------------------------------------------------------
# Common options for session commands
# ---------------------------------------------------------------------------

_chronos_url_option = typer.Option(None, "--url", "-u", envvar="CHRONOS_URL", help="Chronos API URL")
_api_key_option = typer.Option(None, "--api-key", "-k", envvar="PLATO_API_KEY", help="Plato API key")
_output_option = typer.Option(None, "--output", "-o", help="Override output file path")


def _default_output_path(command: str, session_id: str) -> Path:
    """Generate a default output file path in /tmp."""
    return Path(tempfile.gettempdir()) / f"chronos-{command}-{session_id[:12]}.json"


def _write_output(data: str, output: Path, command: str = "") -> None:
    """Write data to file and print the path."""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(data)
    console.print(f"[green]{output}[/green]")


# ---------------------------------------------------------------------------
# Session info
# ---------------------------------------------------------------------------


@chronos_app.command("session")
def session_info(
    session_id: Annotated[str, typer.Argument(help="Session ID")],
    reveal_secrets: Annotated[bool, typer.Option("--reveal-secrets", help="Include secrets in output")] = False,
    chronos_url: str = _chronos_url_option,
    api_key: str = _api_key_option,
    output: Path | None = _output_option,
):
    """Get session info."""
    chronos_url = chronos_url or settings.chronos_url
    api_key = _require_api_key(api_key)

    try:
        with Chronos(base_url=chronos_url, api_key=api_key) as client:
            resp = client.get_session(session_id)
        data = resp.model_dump_json(indent=2)
        out = output or _default_output_path("session", session_id)
        _write_output(data, out)
    except Exception as e:
        console.print(f"[red]Failed: {e}[/red]")
        raise typer.Exit(1)


# ---------------------------------------------------------------------------
# Trajectory
# ---------------------------------------------------------------------------


@chronos_app.command("traces")
def traces(
    session_id: Annotated[str, typer.Argument(help="Session ID")],
    atif_only: Annotated[bool, typer.Option("--atif-only", help="Agent traces only")] = False,
    errors_only: Annotated[bool, typer.Option("--errors-only", help="Error traces only")] = False,
    search: Annotated[str | None, typer.Option(help="Search filter")] = None,
    chronos_url: str = _chronos_url_option,
    api_key: str = _api_key_option,
    output: Path | None = _output_option,
):
    """Fetch session traces (OTel spans with filtering)."""
    chronos_url = chronos_url or settings.chronos_url
    api_key = _require_api_key(api_key)

    try:
        with Chronos(base_url=chronos_url, api_key=api_key) as client:
            result = client.get_traces(
                session_id,
                atif_only=atif_only,
                errors_only=errors_only,
                search=search,
            )
        output_dict = result.model_dump()
        filters: dict[str, str | bool] = {}
        if atif_only:
            filters["atif_only"] = True
        if errors_only:
            filters["errors_only"] = True
        if search:
            filters["search"] = search
        if filters:
            output_dict = {"filters": filters, **output_dict}
        data = json.dumps(output_dict, indent=2)
        out = output or _default_output_path("traces", session_id)
        _write_output(data, out)
    except Exception as e:
        console.print(f"[red]Failed: {e}[/red]")
        raise typer.Exit(1)


# ---------------------------------------------------------------------------
# Session analysis (OTel-based)
# ---------------------------------------------------------------------------


@chronos_app.command("analysis")
def analysis(
    session_id: Annotated[str, typer.Argument(help="Session ID")],
    chronos_url: str = _chronos_url_option,
    api_key: str = _api_key_option,
    output: Path | None = _output_option,
):
    """Run OTel-based session analysis (token usage, phases, durations)."""
    chronos_url = chronos_url or settings.chronos_url
    api_key = _require_api_key(api_key)

    try:
        with Chronos(base_url=chronos_url, api_key=api_key) as client:
            result = client.get_session_analysis(session_id)
        data = result.model_dump_json(indent=2)
        out = output or _default_output_path("analysis", session_id)
        _write_output(data, out)
    except Exception as e:
        console.print(f"[red]Failed: {e}[/red]")
        raise typer.Exit(1)


# ---------------------------------------------------------------------------
# VM metrics
# ---------------------------------------------------------------------------


@chronos_app.command("metrics")
def metrics(
    session_id: Annotated[str, typer.Argument(help="Session ID")],
    env_alias: Annotated[
        str | None, typer.Option("--env-alias", help="Filter by env alias (e.g. agent, world)")
    ] = None,
    chronos_url: str = _chronos_url_option,
    api_key: str = _api_key_option,
    output: Path | None = _output_option,
):
    """Fetch and display VM metrics (CPU, memory, etc.) for a session."""
    chronos_url = chronos_url or settings.chronos_url
    api_key = _require_api_key(api_key)

    try:
        with Chronos(base_url=chronos_url, api_key=api_key) as client:
            result = client.get_session_metrics(session_id, env_alias=env_alias)

        data_points = result.data_points
        data = result.model_dump_json(indent=2)
        out = output or _default_output_path("metrics", session_id)
        _write_output(data, out)

        # Print summary table of metric names and counts
        if data_points:
            counts: dict[str, int] = {}
            for dp in data_points:
                name = dp.name or "unknown"
                counts[name] = counts.get(name, 0) + 1

            table = Table(title=f"Metrics Summary for {session_id[:12]}...")
            table.add_column("Metric Name", style="cyan")
            table.add_column("Data Points", style="green", justify="right")

            for name, count in sorted(counts.items()):
                table.add_row(name, str(count))

            table.add_section()
            table.add_row("[bold]Total[/bold]", f"[bold]{len(data_points)}[/bold]")
            console.print(table)
        else:
            console.print("[yellow]No metrics data points found[/yellow]")

    except Exception as e:
        console.print(f"[red]Failed: {e}[/red]")
        raise typer.Exit(1)


# ---------------------------------------------------------------------------
# Workspace refs
# ---------------------------------------------------------------------------


@chronos_app.command("workspace-refs")
def workspace_refs(
    session_id: Annotated[str, typer.Argument(help="Session ID")],
    repo_name: Annotated[str | None, typer.Option("--repo", "-r", help="Filter by repo name")] = None,
    chronos_url: str = _chronos_url_option,
    api_key: str = _api_key_option,
    output: Path | None = _output_option,
):
    """List workspace refs for a session.

    Shows all checkpoint refs with their step names, repo names, and ref IDs.
    Prints instructions for how to use refs to resume from a checkpoint in a config file.
    """
    chronos_url = chronos_url or settings.chronos_url
    api_key = _require_api_key(api_key)

    try:
        with Chronos(base_url=chronos_url, api_key=api_key) as client:
            refs = client.get_workspace_refs(session_id, repo_name=repo_name)

        if not refs:
            console.print("[yellow]No workspace refs found[/yellow]")
            raise typer.Exit(0)

        if output:
            _write_output(json.dumps(refs, indent=2), output)
        else:
            # Pretty-print refs table
            from rich.table import Table

            table = Table(title=f"Workspace Refs for {session_id[:12]}...")
            table.add_column("Repo", style="cyan")
            table.add_column("Step", style="green")
            table.add_column("Ref ID", style="dim")
            table.add_column("DVC Files", style="yellow")

            for ref in refs:
                dvc_count = len(ref.get("dvc_files") or {})
                table.add_row(
                    ref.get("repo_name", ""),
                    ref.get("step_name", ""),
                    ref.get("public_id", "")[:12] + "...",
                    str(dvc_count),
                )
            console.print(table)

            # Print resume instructions using full repo names
            if refs:
                # Group by repo, show latest ref per repo
                latest_by_repo: dict[str, dict[str, str]] = {}
                for ref in refs:
                    repo = ref.get("repo_name", "")
                    latest_by_repo[repo] = ref

                console.print("\n[bold]To resume from latest refs, update your config:[/bold]")
                console.print('  "state": {')
                console.print('    "workspaces": {')
                entries = []
                for repo, ref in latest_by_repo.items():
                    entries.append(f'      "{repo}": "{session_id}:{ref.get("step_name", "")}"')
                console.print(",\n".join(entries))
                console.print("    }")
                console.print("  }")

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[red]Failed: {e}[/red]")
        raise typer.Exit(1)


# ---------------------------------------------------------------------------
# Filesystem audit
# ---------------------------------------------------------------------------


@chronos_app.command("audit")
def audit_command(
    session_id: Annotated[str, typer.Argument(help="Session public ID")],
    step: Annotated[str | None, typer.Option("--step", help="Filter by step name")] = None,
    repo: Annotated[str | None, typer.Option("--repo", help="Filter by repo name")] = None,
    path: Annotated[str | None, typer.Option("--path", help="Filter by path prefix")] = None,
    trace: Annotated[str | None, typer.Option("--trace", help="Filter by trace ID")] = None,
    agent: Annotated[str | None, typer.Option("--agent", help="Filter by agent name")] = None,
    operation: Annotated[str | None, typer.Option("--operation", help="Filter by operation name")] = None,
    format: Annotated[str, typer.Option("--format", help="Output format: table or json")] = "table",
    limit: Annotated[int, typer.Option("--limit", help="Max events to return")] = 500,
    output: Path | None = _output_option,
    chronos_url: str = _chronos_url_option,
    api_key: str = _api_key_option,
):
    """Query filesystem audit events for a session."""
    chronos_url = chronos_url or settings.chronos_url
    api_key = _require_api_key(api_key)

    try:
        with Chronos(base_url=chronos_url, api_key=api_key) as client:
            audit_response = client.get_audit_events(
                session_id,
                step_name=step,
                repo_name=repo,
                path=path,
                trace_id=trace,
                agent_name=agent,
                operation=operation,
                limit=limit,
            )
            data = audit_response.model_dump(mode="json")

        events: list[dict[str, str]] = data.get("events", [])

        if format == "json":
            json_str = json.dumps(data, indent=2)
            if output:
                _write_output(json_str, output)
            else:
                console.print(json_str)
        else:
            if not events:
                console.print("[yellow]No audit events found[/yellow]")
                raise typer.Exit(0)

            table = Table(title=f"Audit Events for {session_id[:12]}...")
            table.add_column("Timestamp", style="dim")
            table.add_column("Op", style="cyan")
            table.add_column("Path", style="green")
            table.add_column("Agent", style="yellow")
            table.add_column("Exe", style="magenta")
            table.add_column("Trace", style="dim")

            for event in events:
                table.add_row(
                    event.get("timestamp", ""),
                    event.get("operation", ""),
                    event.get("path", ""),
                    event.get("agent_name", ""),
                    event.get("exe", ""),
                    event.get("trace_id", "")[:12] + "..." if event.get("trace_id") else "",
                )
            console.print(table)

            if output:
                _write_output(json.dumps(data, indent=2), output)

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[red]Failed: {e}[/red]")
        raise typer.Exit(1)


# ---------------------------------------------------------------------------
# Download workspace files
# ---------------------------------------------------------------------------


@chronos_app.command("download")
def download(
    session_id: Annotated[str, typer.Argument(help="Session ID")],
    repo_name: Annotated[str, typer.Option("--repo", "-r", help="Workspace repo name")] = "code",
    step_name: Annotated[str | None, typer.Option("--step", "-s", help="Step name (uses latest if omitted)")] = None,
    output: Annotated[
        Path | None, typer.Option("--output", "-o", help="Output zip path (default: /tmp/<session>-<repo>.zip)")
    ] = None,
    chronos_url: str = _chronos_url_option,
    api_key: str = _api_key_option,
):
    """Download workspace files as a ZIP archive."""
    chronos_url = chronos_url or settings.chronos_url
    api_key = _require_api_key(api_key)

    try:
        with Chronos(base_url=chronos_url, api_key=api_key) as client:
            # First get refs to find the step name if not provided
            refs = client.get_workspace_refs(session_id, repo_name=repo_name)
            if not refs:
                # Show available repos to help the user
                all_refs = client.get_workspace_refs(session_id)
                available = sorted({r.get("repo_name", "") for r in all_refs}) if all_refs else []
                if available:
                    console.print(f"[red]No workspace refs for repo '{repo_name}'[/red]")
                    console.print(f"[yellow]Available repos: {', '.join(available)}[/yellow]")
                else:
                    console.print(f"[red]No workspace refs found for session {session_id}[/red]")
                raise typer.Exit(1)

            if step_name is None:
                step_name = refs[-1].get("step_name", "")
                console.print(f"[dim]Using latest step: {step_name}[/dim]")

            ref_id = None
            for ref in reversed(refs):
                if ref.get("step_name") == step_name:
                    ref_id = ref.get("public_id")
                    break

            # Download the zip
            from plato.chronos.api.workspace_repos import download_workspace_files

            zip_bytes = download_workspace_files.sync(
                client._client,
                session_public_id=session_id,
                step_name=step_name,
                repo_name=repo_name,
                ref_public_id=ref_id,
            )

            out_path = output or Path(tempfile.gettempdir()) / f"{session_id[:12]}-{repo_name.replace('/', '-')}.zip"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            out_path.write_bytes(zip_bytes)
            console.print(f"[green]Downloaded to {out_path}[/green]")
            console.print(f"[dim]Size: {len(zip_bytes) / 1024 / 1024:.1f} MB[/dim]")

    except typer.Exit:
        raise
    except Exception as e:
        console.print(f"[red]Failed: {e}[/red]")
        raise typer.Exit(1)


@chronos_app.command()
def test(
    config: Annotated[
        Path,
        typer.Argument(help="Path to test config JSON file", exists=True, readable=True),
    ],
    phase: Annotated[
        str,
        typer.Option("--phase", help="Phase filter: unit|integration|all"),
    ] = "all",
    pytest_args: Annotated[
        str,
        typer.Option("--pytest-args", help="Extra args appended to pytest commands"),
    ] = "",
    artifacts_dir: Annotated[
        Path | None,
        typer.Option("--artifacts-dir", help="Local output directory for logs and junit"),
    ] = None,
    keep_vm_on_fail: Annotated[
        bool,
        typer.Option("--keep-vm-on-fail", help="Keep VM alive when tests fail"),
    ] = False,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Show detailed logs"),
    ] = False,
):
    """Run synced tests on a one-shot Chronos VM."""
    from rich.logging import RichHandler

    from plato.cli.chronos.test import TestConfig, TestRunner

    # Configure logging with Rich handler for colored output
    logging.basicConfig(
        level=logging.INFO if verbose else logging.WARNING,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, show_path=False, show_time=verbose)],
    )
    logging.getLogger("plato.cli.chronos.test.runner").setLevel(logging.INFO)
    logging.getLogger("plato.cli.chronos.dev.sync").setLevel(logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)

    phase_key = phase.strip().lower()
    if not phase_key:
        console.print("[red]--phase must be non-empty[/red]")
        raise typer.Exit(2)

    api_key = os.environ.get("PLATO_API_KEY")
    if not api_key:
        console.print("[red]PLATO_API_KEY environment variable required[/red]")
        raise typer.Exit(1)

    try:
        test_config = TestConfig.from_file(config)
    except json.JSONDecodeError as e:
        console.print(f"[red]Invalid JSON in {config}: {e}[/red]")
        raise typer.Exit(1)
    except Exception as e:
        console.print(f"[red]Failed to load test config: {e}[/red]")
        if verbose:
            logger.exception("Failed to load test config")
        raise typer.Exit(1)

    try:
        runner = TestRunner(
            config=test_config,
            config_path=config,
            api_key=api_key,
            phase_filter=phase_key,
            pytest_args=pytest_args,
            artifacts_dir=artifacts_dir,
            keep_vm_on_fail=keep_vm_on_fail,
            verbose=verbose,
        )
        exit_code = asyncio.run(runner.run())
    except KeyboardInterrupt:
        # Runner.run() catches KeyboardInterrupt internally and cleans up
        # the session in its finally block. This only fires if the interrupt
        # happens outside the runner (e.g. during config loading).
        raise typer.Exit(130)
    except Exception as e:
        console.print(f"[red]Failed: {e}[/red]")
        if verbose:
            logger.exception("Chronos test failed")
        raise typer.Exit(1)

    if exit_code != 0:
        raise typer.Exit(exit_code)
