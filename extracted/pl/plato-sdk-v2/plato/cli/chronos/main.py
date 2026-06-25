"""Plato Chronos CLI - Launch and manage Chronos jobs."""

from __future__ import annotations

import asyncio
import json
import logging
import os
import tempfile
import time
from contextlib import contextmanager
from datetime import UTC, datetime
from enum import Enum
from pathlib import Path
from typing import Annotated, Any

import httpx
import typer
from pydantic import ValidationError
from rich.table import Table

from plato.chronos.analysis import analyze_session
from plato.chronos.api.settings import get_setting, update_setting
from plato.chronos.errors import NotFoundError
from plato.chronos.models import OTelSpanSchema, UpdateSettingRequest
from plato.chronos.sdk import Chronos
from plato.cli.chronos.settings import get_settings
from plato.cli.chronos.workspace_upload import (
    download_git_workspace_via_archive,
    download_session_workspace_archive,
    ref_has_archive_dvc,
    workspace_app,
)
from plato.cli.utils import console, safe_print

chronos_app = typer.Typer(help="Chronos job management commands.")
chronos_app.add_typer(workspace_app, name="workspace")
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

    # Auto-inject parent_session_id from env if not set (same as Chronos.launch)
    if not raw.get("parent_session_id"):
        parent_sid = os.environ.get("SESSION_ID")
        if parent_sid:
            raw["parent_session_id"] = parent_sid

    # Normalize tags (same as Chronos.launch → _build_launch_body)
    if raw.get("tags"):
        raw["tags"] = [t.replace("-", "_").replace(":", ".").replace(" ", "_") for t in raw["tags"]]

    try:
        request = LaunchJobRequest.model_validate(raw)
    except ValidationError as e:
        console.print(f"[red]Invalid config:[/red]\n{e}")
        raise typer.Exit(1)

    console.print("[blue]Launching job via Chronos API...[/blue]")
    console.print(f"   World: {request.world.package}")
    if prerelease:
        console.print("   Prerelease: enabled")
    if request.retry:
        console.print(f"   Retries: {request.retry.max_retries}")

    try:
        from plato.chronos.api.jobs import launch_job

        with Chronos(base_url=chronos_url, api_key=api_key) as client:
            resp = launch_job.sync(client._client, body=request)

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
    AgentType.codex: "CODEX_AUTH_CREDENTIALS",
}

_ANALYZER_ENV_KEY = "chronos:analyzer-env"
_CLAUDE_OAUTH_CLIENT_ID = (
    "9d1c250a-e61b-44d9-88ed-5944d1962f5e"  # gitleaks:allow — public Claude Code OAuth client_id, not a secret
)
_CLAUDE_OAUTH_TOKEN_URL = "https://platform.claude.com/v1/oauth/token"


@chronos_app.command("refresh-creds")
def refresh_creds(
    agent: Annotated[AgentType, typer.Argument(help="Agent type: claude or codex")],
    env_file: Annotated[
        Path | None,
        typer.Argument(help="Optional .env file to also update"),
    ] = None,
    chronos_url: str = typer.Option(None, "--url", "-u", envvar="CHRONOS_URL", help="Chronos API URL"),
    api_key: str = typer.Option(None, "--api-key", "-k", envvar="PLATO_API_KEY", help="Plato API key"),
):
    """Refresh OAuth creds and push them into the Chronos analyzer-env (user scope).

    For claude: reads ~/.claude/.credentials.json, calls the Anthropic OAuth refresh
    endpoint, writes the rotated creds back to that file, and PUTs the compact JSON
    as CLAUDE_OAUTH_CREDENTIALS into the user-scoped chronos:analyzer-env setting.

    For codex: reads ~/.codex/auth.json as-is and PUTs it as CODEX_AUTH_CREDENTIALS
    into the same setting (no remote refresh — re-run `codex login` first if stale).

    If `env_file` is supplied, the compact JSON is also mirrored into that .env file.
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

    # Fail fast on missing API key before any irreversible side effects
    # (claude's refresh rotates the Anthropic refresh token and rewrites the
    # local credentials file).
    chronos_url_resolved = chronos_url or settings.chronos_url
    api_key_resolved = _require_api_key(api_key)

    if agent == AgentType.claude:
        creds = _refresh_claude_creds(creds, cred_path)

    compact = json.dumps(creds, separators=(",", ":"))
    _push_to_analyzer_env(chronos_url_resolved, api_key_resolved, env_key, compact)
    if env_file is not None:
        _write_env_value(env_file, env_key, compact)
        console.print(f"[green]Updated {env_key} in {env_file}[/green]")


def _refresh_claude_creds(creds: dict[str, Any], cred_path: Path) -> dict[str, Any]:
    """Refresh the claudeAiOauth block via Anthropic and write it back to cred_path."""
    inner = creds.get("claudeAiOauth")
    if not isinstance(inner, dict):
        console.print(f"[red]Missing claudeAiOauth block in {cred_path}[/red]")
        raise typer.Exit(1)

    refresh_token = inner.get("refreshToken")
    scopes = inner.get("scopes") or []
    if not refresh_token:
        console.print(f"[red]Missing refreshToken in {cred_path}[/red]")
        raise typer.Exit(1)

    console.print("[blue]Refreshing OAuth token via Anthropic...[/blue]")
    # Claude Code itself POSTs JSON (not form-urlencoded) to this endpoint —
    # see the `feH` refresh routine in the claude binary.
    try:
        resp = httpx.post(
            _CLAUDE_OAUTH_TOKEN_URL,
            json={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": _CLAUDE_OAUTH_CLIENT_ID,
                "scope": " ".join(scopes),
            },
            timeout=30.0,
        )
    except httpx.RequestError as e:
        safe_print(f"[red]OAuth refresh request failed:[/red] {e}")
        raise typer.Exit(1)

    if not resp.is_success:
        safe_print(f"[red]OAuth refresh failed ({resp.status_code}):[/red] {resp.text}")
        raise typer.Exit(1)

    token_data = resp.json()
    access_token = token_data.get("access_token")
    new_refresh = token_data.get("refresh_token")
    if not access_token or not new_refresh:
        console.print("[red]OAuth response missing access_token/refresh_token[/red]")
        raise typer.Exit(1)

    expires_in = int(token_data.get("expires_in", 28800))
    expires_at_ms = int((time.time() + expires_in) * 1000)

    new_inner = {
        **inner,
        "accessToken": access_token,
        "refreshToken": new_refresh,
        "expiresAt": expires_at_ms,
        "scopes": scopes,
    }
    new_creds = {**creds, "claudeAiOauth": new_inner}

    cred_path.write_text(json.dumps(new_creds, indent=2))
    console.print(f"[green]Updated {cred_path}[/green] (expires in {expires_in // 60} min)")
    return new_creds


def _push_to_analyzer_env(chronos_url: str, api_key: str, env_key: str, value: str) -> None:
    """Splice ``env_key=value`` into the user-scoped chronos:analyzer-env setting."""
    with Chronos(base_url=chronos_url, api_key=api_key) as client:
        try:
            existing = get_setting.sync(client._client, key=_ANALYZER_ENV_KEY, scope="user")
            current = dict(existing.value or {})
        except NotFoundError:
            current = {}
        current[env_key] = value
        update_setting.sync(
            client._client,
            key=_ANALYZER_ENV_KEY,
            scope="user",
            body=UpdateSettingRequest(value=current),
        )
    console.print(f"[green]Updated {env_key} in Chronos analyzer-env (user scope)[/green]")


def _write_env_value(env_path: Path, key: str, value: str) -> None:
    """Update or append ``key=value`` in env_path, creating the file if missing."""
    lines = env_path.read_text().splitlines() if env_path.exists() else []
    found = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}"
            found = True
            break
    if not found:
        lines.append(f"{key}={value}")
    env_path.write_text("\n".join(lines) + "\n")


# ---------------------------------------------------------------------------
# Common options for session commands
# ---------------------------------------------------------------------------

_chronos_url_option = typer.Option(None, "--url", "-u", envvar="CHRONOS_URL", help="Chronos API URL")
_api_key_option = typer.Option(None, "--api-key", "-k", envvar="PLATO_API_KEY", help="Plato API key")
_output_option = typer.Option(None, "--output", "-o", help="Override output file path")


def _default_output_path(command: str, session_id: str) -> Path:
    """Generate a default output file path in /tmp."""
    return Path(tempfile.gettempdir()) / f"chronos-{command}-{session_id[:12]}.json"


@contextmanager
def _span_stream_progress(label: str):
    """Yield an ``on_progress(span_count, page_count)`` callback backed by a
    transient Rich spinner that reports streaming progress live."""
    from rich.progress import Progress, SpinnerColumn, TextColumn

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True,
    ) as progress:
        task = progress.add_task(f"{label}: 0 spans", total=None)

        def on_progress(span_count: int, page_count: int) -> None:
            progress.update(task, description=f"{label}: {span_count:,} spans ({page_count} pages)")

        yield on_progress


def _write_output(data: str, output: Path, command: str = "") -> None:
    """Write data to file and print the path."""
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(data)
    console.print(f"[green]{output}[/green]")


def _spans_cache_path(session_id: str) -> Path:
    """On-disk cache of a session's full (unfiltered) span set.

    Shared by ``traces`` and ``analysis`` so a session's 90k+ spans only have
    to be streamed once — the second command reuses the cache unless
    ``--refresh`` is passed."""
    return Path(tempfile.gettempdir()) / f"chronos-spans-{session_id}.json"


def _get_spans(
    client: Chronos,
    session_id: str,
    *,
    atif_only: bool = False,
    errors_only: bool = False,
    search: str | None = None,
    refresh: bool = False,
    label: str = "Streaming spans",
) -> list[OTelSpanSchema]:
    """Return all spans for a session, reusing the on-disk cache when possible.

    Only the full, unfiltered span set is cached/reused — when any filter is
    active the stream is always run live (filters are applied server-side).
    """
    filtered = atif_only or errors_only or bool(search)
    cache_path = _spans_cache_path(session_id)

    if not filtered and not refresh and cache_path.exists():
        try:
            cached = json.loads(cache_path.read_text())
            spans = [OTelSpanSchema.model_validate(s) for s in cached]
            console.print(
                f"[dim]Using {len(spans):,} cached spans ({cache_path}) — pass --refresh to re-download[/dim]"
            )
            return spans
        # OSError: unreadable file; ValueError (covers JSONDecodeError): bad JSON;
        # TypeError: non-list payload; ValidationError: stale/invalid span shape.
        # Any of these means an unusable cache — fall through to a fresh stream.
        except (OSError, ValueError, TypeError, ValidationError):
            pass

    with _span_stream_progress(label) as on_progress:
        spans = client.get_all_traces(
            session_id,
            atif_only=atif_only,
            errors_only=errors_only,
            search=search,
            on_progress=on_progress,
        )

    if not filtered:
        try:
            cache_path.write_text(json.dumps([s.model_dump() for s in spans]))
        except OSError:
            pass  # Cache is best-effort; never fail the command over it.

    return spans


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
    refresh: Annotated[bool, typer.Option("--refresh", help="Ignore the local span cache and re-download")] = False,
    chronos_url: str = _chronos_url_option,
    api_key: str = _api_key_option,
    output: Path | None = _output_option,
):
    """Fetch ALL session traces (OTel spans) via the logs-stream endpoint.

    Streams the entire session in one pass — no cursor cap — so large sessions
    (10k+ spans) come back complete. The unfiltered span set is cached locally
    and reused by ``analysis``; pass ``--refresh`` to re-download.
    """
    chronos_url = chronos_url or settings.chronos_url
    api_key = _require_api_key(api_key)

    try:
        with Chronos(base_url=chronos_url, api_key=api_key) as client:
            spans = _get_spans(
                client,
                session_id,
                atif_only=atif_only,
                errors_only=errors_only,
                search=search,
                refresh=refresh,
            )

        output_dict: dict[str, Any] = {
            "session_id": session_id,
            "total_count": len(spans),
            "spans": [s.model_dump() for s in spans],
        }
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
        console.print(f"[green]{len(spans):,}[/green] spans")
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
    refresh: Annotated[bool, typer.Option("--refresh", help="Ignore the local span cache and re-download")] = False,
    chronos_url: str = _chronos_url_option,
    api_key: str = _api_key_option,
    output: Path | None = _output_option,
):
    """Run OTel-based session analysis (token usage, phases, durations).

    Reuses the span cache populated by ``traces`` (or a prior ``analysis``) when
    present, so large sessions (10k+ spans) aren't re-streamed every run; pass
    ``--refresh`` to re-download.
    """
    chronos_url = chronos_url or settings.chronos_url
    api_key = _require_api_key(api_key)

    try:
        with Chronos(base_url=chronos_url, api_key=api_key) as client:
            spans = _get_spans(client, session_id, refresh=refresh)
        result = analyze_session(spans, session_id)
        data = result.model_dump_json(indent=2)
        out = output or _default_output_path("analysis", session_id)
        console.print(f"[green]{result.total_spans:,}[/green] spans analyzed")
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
# Mount workspace locally
# ---------------------------------------------------------------------------


@chronos_app.command("mount")
def mount(
    session_ref: Annotated[
        str,
        typer.Argument(help="Session ID, or session_id:step_name"),
    ],
    repo_name: Annotated[str | None, typer.Option("--repo", "-r", help="Workspace repo name")] = None,
    step_name: Annotated[
        str | None, typer.Option("--step", "-s", help="Step name (parsed from session_ref if present)")
    ] = None,
    mount_path: Annotated[
        str | None,
        typer.Option("--mount", "-m", help="Local mount path (default: ~/plato-workspaces/<session>-<repo>)"),
    ] = None,
    cpus: Annotated[int, typer.Option(help="VM CPUs")] = 1,
    memory: Annotated[int, typer.Option(help="VM memory in MB")] = 2048,
    disk: Annotated[int, typer.Option(help="VM disk in MB")] = 10240,
    api_key: str = _api_key_option,
):
    """Mount a workspace locally and return a short mount alias.

    This starts a detached helper that keeps the VM, tunnel, and local mount alive.
    The helper records mount metadata in `~/plato-workspaces/.plato-mounts/state.json`.
    Use `plato chronos unmount <alias>` to tear it down later.

    Examples:

        plato chronos mount abc123:step.1.stage.build --repo webclone/stripe/code

        plato chronos mount abc123 --repo code --step step.1
    """
    from plato.cli.chronos.mount import start_mount_daemon

    resolved_api_key = api_key or os.environ.get("PLATO_API_KEY")
    if not resolved_api_key:
        console.print("[red]PLATO_API_KEY required[/red]")
        raise typer.Exit(1)

    # Parse session_ref — supports "session_id:step_name" format
    if ":" in session_ref and step_name is None:
        session_id, step_name = session_ref.split(":", 1)
    else:
        session_id = session_ref

    try:
        console.print("[blue]Starting workspace mount...[/blue]")

        def _render_mount_event(event: dict[str, object]) -> None:
            kind = event.get("kind")
            message = str(event.get("message", ""))
            duration = event.get("duration_s")
            duration_s = float(duration) if isinstance(duration, (int, float)) else None
            if kind == "start":
                safe_print(f"  [dim]\u2192[/dim] {message}")
            elif kind == "done":
                suffix = f" [dim]({duration_s:.1f}s)[/dim]" if duration_s is not None else ""
                safe_print(f"  [green]\u2713[/green] {message}{suffix}")
            elif kind == "timing":
                suffix = f" [dim]({duration_s:.1f}s)[/dim]" if duration_s is not None else ""
                safe_print(f"    [dim]-[/dim] {message}{suffix}")
            else:
                safe_print(f"  [yellow]![/yellow] {message}")

        record = start_mount_daemon(
            session_id,
            repo_name=repo_name,
            step_name=step_name,
            mount_path=mount_path,
            api_key=resolved_api_key,
            cpus=cpus,
            memory=memory,
            disk=disk,
            on_event=_render_mount_event,
        )
        safe_print(f"[green]Mounted[/green] {record['mount_path']}")
        safe_print(f"[dim]Alias:[/dim] {record['alias']}")
        safe_print(f"[dim]Session:[/dim] {record['session_id']}")
        if record.get("repo_name"):
            safe_print(f"[dim]Repo:[/dim] {record['repo_name']}")
        if record.get("step_name"):
            safe_print(f"[dim]Step:[/dim] {record['step_name']}")
        safe_print(f"[dim]Unmount:[/dim] plato chronos unmount {record['alias']}")
    except Exception as e:
        safe_print(f"[red]Failed: {e}[/red]")
        raise typer.Exit(1)


@chronos_app.command("unmount")
def unmount(
    mount_id: Annotated[
        str,
        typer.Argument(help="Mount alias returned by `plato chronos mount`, or the mount path"),
    ],
):
    """Unmount a previously mounted Chronos workspace."""
    from plato.cli.chronos.mount import unmount_workspace

    try:
        safe_print(f"[blue]Unmounting[/blue] {mount_id}...")
        unmount_workspace(mount_id)
        safe_print(f"[green]Unmounted[/green] {mount_id}")
    except Exception as e:
        safe_print(f"[red]Failed: {e}[/red]")
        raise typer.Exit(1)


# ---------------------------------------------------------------------------
# Download workspace files
# ---------------------------------------------------------------------------


@chronos_app.command("download")
def download(
    session_id: Annotated[str, typer.Argument(help="Session ID")],
    repo_name: Annotated[str, typer.Option("--repo", "-r", help="Workspace repo name")] = "code",
    step_name: Annotated[str | None, typer.Option("--step", "-s", help="Step name (uses latest if omitted)")] = None,
    output: Annotated[Path | None, typer.Option("--output", "-o", help="Output path")] = None,
    session_workspace: Annotated[
        bool, typer.Option("--session-workspace", help="Download the session workspace tarball instead of repo files")
    ] = False,
    workspace_name: Annotated[
        str, typer.Option("--name", help="Session workspace object name for --session-workspace")
    ] = "workspace",
    extract: Annotated[
        bool,
        typer.Option(
            "--extract",
            help="Download and extract the git workspace via DVC archive restore "
            "(fetches workspace ref, downloads tar.gz from S3, re-clones repo/ from .git-bare)",
        ),
    ] = False,
    dir_name: Annotated[
        str | None,
        typer.Option(
            "--dir-name",
            help="For --extract: which dvc archive dir to restore when the ref has several "
            "(default: the only/first format:archive entry)",
        ),
    ] = None,
    chronos_url: str = _chronos_url_option,
    api_key: str = _api_key_option,
):
    """Download workspace files as a ZIP archive, or a session workspace tarball."""
    chronos_url = chronos_url or settings.chronos_url
    api_key = _require_api_key(api_key)

    def _extract_git_workspace() -> None:
        dest_dir = output or Path.cwd() / f"{session_id[:12]}-{repo_name.replace('/', '-')}-workspace"
        dest_dir.parent.mkdir(parents=True, exist_ok=True)
        repo_dir = download_git_workspace_via_archive(
            dest_dir,
            session_id=session_id,
            repo_name=repo_name,
            step_name=step_name,
            dir_name=dir_name,
            chronos_url=chronos_url,
            api_key=api_key,
        )
        console.print(f"[green]Extracted git workspace to {dest_dir}[/green]")
        console.print(f"[dim]Repo: {repo_dir}[/dim]")

    try:
        if extract:
            _extract_git_workspace()
            return

        if session_workspace:
            out_path = output or Path(tempfile.gettempdir()) / f"{session_id[:12]}-{workspace_name}.tar"
            size = download_session_workspace_archive(
                out_path,
                session_id=session_id,
                name=workspace_name,
                chronos_url=chronos_url,
                api_key=api_key,
            )
            console.print(f"[green]Downloaded to {out_path}[/green]")
            console.print(f"[dim]Size: {size / 1024 / 1024:.1f} MB[/dim]")
            return

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
                console.print("[dim]Hint: pass --session-workspace to download a session workspace tarball.[/dim]")
                raise typer.Exit(1)

            if step_name is None:
                step_name = refs[-1].get("step_name", "")
                console.print(f"[dim]Using latest step: {step_name}[/dim]")

            ref_id = None
            selected_ref = None
            for ref in reversed(refs):
                if ref.get("step_name") == step_name:
                    ref_id = ref.get("public_id")
                    selected_ref = ref
                    break

            # Auto-detect git/archive workspaces (format: archive dvc_files) and
            # extract + clone from .git-bare, so callers get a working git tree
            # without having to pass --extract. Plain workspaces fall through to
            # the legacy server-side ZIP below.
            if selected_ref is not None and ref_has_archive_dvc(selected_ref):
                console.print("[dim]Detected git workspace — extracting and cloning from .git-bare[/dim]")
                _extract_git_workspace()
                return

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
    keep_vm: Annotated[
        bool,
        typer.Option("--keep-vm", help="Keep VM alive after run and save state for --reuse-vm"),
    ] = False,
    reuse_vm: Annotated[
        bool,
        typer.Option(
            "--reuse-vm", help="Reuse a previously kept VM (skip provisioning and editable install, rsync only)"
        ),
    ] = False,
    clean: Annotated[
        bool,
        typer.Option("--clean", help="Clean workspace state before running tests (use with --reuse-vm)"),
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
            keep_vm=keep_vm,
            reuse_vm=reuse_vm,
            clean=clean,
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
