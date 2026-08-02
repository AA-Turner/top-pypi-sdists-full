# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""muffuletta CLI - Geneva command-line interface."""

import logging
import re
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime, timedelta, timezone
from typing import Annotated, Optional

import typer
from . import __version__
from .client import GenevaClient, GenevaClientError
from .config import (
    CONFIG_FILE,
    Config,
    get_db_uri,
)
from .formatters import (
    OutputFormat,
    format_cluster_detail,
    format_clusters,
    format_job_detail,
    format_jobs,
    format_manifest_detail,
    format_manifests,
    format_ray_cluster_detail,
    format_ray_clusters,
)
from .k8s import (
    KubernetesError,
    get_console_api_service_target,
    get_job_pods,
    get_namespace,
    get_ray_cluster,
    list_ray_clusters,
    port_forward,
    stream_pod_logs,
)
from .models import JobStatus
from rich.console import Console
from rich.live import Live
from rich.logging import RichHandler
from rich.panel import Panel
from rich.spinner import Spinner

from geneva.constants import DEFAULT_K8S_NS

app = typer.Typer(
    name="muffuletta",
    help="Geneva CLI - Manage Geneva clusters, manifests, and jobs",
    no_args_is_help=True,
    rich_markup_mode="rich",
)

console = Console()
err_console = Console(stderr=True)

# Global options
OutputFormatOption = Annotated[
    OutputFormat,
    typer.Option(
        "--output",
        "-o",
        help="Output format",
        case_sensitive=False,
    ),
]

NamespaceOption = Annotated[
    Optional[str],
    typer.Option(
        "--namespace",
        "-n",
        help="Kubernetes namespace",
    ),
]

ContextOption = Annotated[
    Optional[str],
    typer.Option(
        "--context",
        help="Kubernetes context (uses current context if not specified)",
    ),
]


def require_db_uri() -> str:
    """Get db_uri from config or exit with error."""
    db_uri = get_db_uri()
    if not db_uri:
        err_console.print(
            "[red]Error:[/red] No database URI configured.\n"
            "Run [bold]mf configure[/bold] to set up your Geneva connection."
        )
        raise typer.Exit(1)
    return db_uri


@contextmanager
def geneva_client(
    db_uri: str,
    namespace: str | None = None,
    context: str | None = None,
    show_context: bool = True,
) -> Iterator[GenevaClient]:
    """
    Context manager for Geneva API client.

    Port-forwards to the geneva-console-api Kubernetes service.
    """
    with Live(
        Spinner("dots", text="Connecting to Geneva..."),
        console=err_console,
        transient=True,
    ):
        try:
            svc_target, ns, ctx = get_console_api_service_target(namespace, context)
        except KubernetesError as e:
            err_console.print(f"[red]Error:[/red] {e}")
            raise typer.Exit(1) from e

    if show_context:
        err_console.print(
            f"[dim]Using service:[/dim] [bold]{svc_target}[/bold]"
            f" [dim]in namespace[/dim] [bold]{ns}[/bold]"
        )

    with (
        port_forward(svc_target, ns, ctx) as local_port,
        GenevaClient(f"http://localhost:{local_port}", db_uri) as client,
    ):
        yield client


def parse_relative_time(time_str: str) -> datetime:
    """
    Parse relative time string like -3h, -2d, -30m.

    Args:
        time_str: Relative time string (e.g., "-3h", "-2d", "-30m")

    Returns:
        Datetime object
    """
    pattern = r"^-?(\d+)([hdmw])$"
    match = re.match(pattern, time_str.lower())

    if not match:
        raise typer.BadParameter(
            f"Invalid time format: {time_str}. Use format like -3h, -2d, -30m, -1w"
        )

    value = int(match.group(1))
    unit = match.group(2)

    now = datetime.now(timezone.utc)

    if unit == "m":
        return now - timedelta(minutes=value)
    elif unit == "h":
        return now - timedelta(hours=value)
    elif unit == "d":
        return now - timedelta(days=value)
    elif unit == "w":
        return now - timedelta(weeks=value)

    raise typer.BadParameter(f"Unknown time unit: {unit}")


def version_callback(value: bool) -> None:
    """Print version and exit."""
    if value:
        console.print(f"[bold]muffuletta[/bold] version {__version__}")
        raise typer.Exit()


def setup_logging(debug: bool) -> None:
    """Configure logging based on debug flag."""
    level = logging.DEBUG if debug else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(name)s: %(message)s",
        handlers=[RichHandler(console=err_console, show_time=False, show_path=False)],
    )
    # Also set httpx logging
    logging.getLogger("httpx").setLevel(level)
    logging.getLogger("httpcore").setLevel(level)


@app.callback()
def main(
    version: Annotated[
        bool,
        typer.Option(
            "--version",
            "-v",
            callback=version_callback,
            is_eager=True,
            help="Show version and exit",
        ),
    ] = False,
    debug: Annotated[
        bool,
        typer.Option(
            "--debug",
            help="Enable debug logging",
        ),
    ] = False,
) -> None:
    """muffuletta - Geneva CLI."""
    if debug:
        setup_logging(debug=True)


# ============================================================================
# Configure command
# ============================================================================


@app.command("configure")
def configure_cmd(
    db_uri: Annotated[
        Optional[str],
        typer.Option(
            "--db-uri",
            help="Geneva database URI (e.g., s3://bucket/path)",
        ),
    ] = None,
    namespace: Annotated[
        Optional[str],
        typer.Option(
            "--namespace",
            "-n",
            help="Default Kubernetes namespace",
        ),
    ] = None,
    show: Annotated[
        bool,
        typer.Option(
            "--show",
            help="Show current configuration",
        ),
    ] = False,
) -> None:
    """Configure muffuletta CLI settings."""
    config = Config.load()

    if show:
        console.print(
            Panel(
                f"[bold]db_uri:[/bold] "
                f"{config.db_uri or '[dim]not set[/dim]'}\n"
                f"[bold]namespace:[/bold] "
                f"{config.namespace or '[dim]not set[/dim]'}\n\n"
                f"[dim]Config file: {CONFIG_FILE}[/dim]",
                title="Current Configuration",
                border_style="cyan",
            )
        )
        return

    # If no options provided, prompt interactively
    if db_uri is None and namespace is None:
        console.print("[bold]Configure muffuletta[/bold]\n")

        # Prompt for db_uri
        current_uri = config.db_uri or ""
        prompt_text = "Database URI (i.e. 'db://my-data' or 's3://my-bucket/my-data')"
        if current_uri:
            prompt_text += f" [{current_uri}]"
        prompt_text += ": "

        new_uri = console.input(prompt_text).strip()
        if new_uri:
            config.db_uri = new_uri
        elif not current_uri:
            err_console.print("[red]Error:[/red] Database URI is required")
            raise typer.Exit(1)

        # Prompt for namespace
        current_ns = config.namespace or DEFAULT_K8S_NS
        new_ns = console.input(f"Namespace [{current_ns}]: ").strip()
        if new_ns:
            config.namespace = new_ns
        elif not config.namespace:
            config.namespace = DEFAULT_K8S_NS

    else:
        # Use provided options
        if db_uri is not None:
            config.db_uri = db_uri
        if namespace is not None:
            config.namespace = namespace

    config.save()
    console.print(f"\n[green]Configuration saved to {CONFIG_FILE}[/green]")


# ============================================================================
# Clusters commands
# ============================================================================

clusters_app = typer.Typer(help="Manage Geneva clusters")
app.add_typer(clusters_app, name="clusters")


@clusters_app.command("list")
def list_clusters_cmd(
    output: OutputFormatOption = OutputFormat.TABLE,
    namespace: NamespaceOption = None,
    context: ContextOption = None,
) -> None:
    """List all Geneva clusters."""
    db_uri = require_db_uri()

    try:
        with geneva_client(db_uri, namespace, context) as client:
            clusters = client.list_clusters()
    except GenevaClientError as e:
        err_console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from e

    format_clusters(clusters, output)


@clusters_app.command("get")
def get_cluster_cmd(
    name: Annotated[str, typer.Argument(help="Cluster name")],
    output: OutputFormatOption = OutputFormat.TEXT,
    namespace: NamespaceOption = None,
    context: ContextOption = None,
) -> None:
    """Get detailed information about a cluster."""
    db_uri = require_db_uri()

    try:
        with geneva_client(db_uri, namespace, context) as client:
            cluster = client.get_cluster(name)
    except GenevaClientError as e:
        err_console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from e

    format_cluster_detail(cluster, output)


# ============================================================================
# Manifests commands
# ============================================================================

manifests_app = typer.Typer(help="Manage Geneva manifests")
app.add_typer(manifests_app, name="manifests")


@manifests_app.command("list")
def list_manifests_cmd(
    output: OutputFormatOption = OutputFormat.TABLE,
    namespace: NamespaceOption = None,
    context: ContextOption = None,
) -> None:
    """List all Geneva manifests."""
    db_uri = require_db_uri()

    try:
        with geneva_client(db_uri, namespace, context) as client:
            manifests = client.list_manifests()
    except GenevaClientError as e:
        err_console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from e

    format_manifests(manifests, output)


@manifests_app.command("get")
def get_manifest_cmd(
    name: Annotated[str, typer.Argument(help="Manifest name")],
    output: OutputFormatOption = OutputFormat.TEXT,
    namespace: NamespaceOption = None,
    context: ContextOption = None,
) -> None:
    """Get detailed information about a manifest."""
    db_uri = require_db_uri()

    try:
        with geneva_client(db_uri, namespace, context) as client:
            manifest = client.get_manifest(name)
    except GenevaClientError as e:
        err_console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from e

    format_manifest_detail(manifest, output)


# ============================================================================
# Jobs commands
# ============================================================================

jobs_app = typer.Typer(help="Manage Geneva jobs")
app.add_typer(jobs_app, name="jobs")


@jobs_app.command("list")
def list_jobs_cmd(
    output: OutputFormatOption = OutputFormat.TABLE,
    namespace: NamespaceOption = None,
    context: ContextOption = None,
    status: Annotated[
        Optional[str],
        typer.Option(
            "--status",
            "-s",
            help="Filter by status (pending, running, completed, failed, cancelled)",
        ),
    ] = None,
    since: Annotated[
        Optional[str],
        typer.Option(
            "--since",
            help="Show jobs launched after this time "
            "(e.g., -3h, -2d, -1w). Default: -7d",
        ),
    ] = None,
    until: Annotated[
        Optional[str],
        typer.Option(
            "--until",
            help="Show jobs launched before this time (e.g., -1h, -30m)",
        ),
    ] = None,
    limit: Annotated[
        Optional[int],
        typer.Option(
            "--limit",
            "-l",
            help="Maximum number of jobs to show",
        ),
    ] = None,
    all_time: Annotated[
        bool,
        typer.Option(
            "--all",
            "-a",
            help="Show all jobs (disable default 7-day filter)",
        ),
    ] = False,
    watch: Annotated[
        bool,
        typer.Option(
            "--watch",
            "-w",
            help="Auto-refresh every 10 seconds (Ctrl+C to stop)",
        ),
    ] = False,
) -> None:
    """List Geneva jobs with optional filters."""
    db_uri = require_db_uri()

    # Parse status filter
    job_status = None
    if status:
        try:
            job_status = JobStatus(status.upper())
        except ValueError:
            try:
                job_status = JobStatus(status.lower())
            except ValueError:
                valid = ", ".join(s.value for s in JobStatus)
                err_console.print(
                    f"[red]Error:[/red] Invalid status '{status}'. Valid: {valid}"
                )
                raise typer.Exit(1) from None

    # Parse time filters
    launched_after = None
    launched_before = None

    if since:
        try:
            launched_after = parse_relative_time(since)
        except typer.BadParameter as e:
            err_console.print(f"[red]Error:[/red] {e}")
            raise typer.Exit(1) from e
    elif not all_time:
        # Default to last 7 days if no --since specified and not --all
        launched_after = datetime.now(timezone.utc) - timedelta(days=7)

    if until:
        try:
            launched_before = parse_relative_time(until)
        except typer.BadParameter as e:
            err_console.print(f"[red]Error:[/red] {e}")
            raise typer.Exit(1) from e

    if watch:
        import time

        try:
            while True:
                console.clear()
                console.print(
                    "[dim]Auto-refreshing every 10s. Press Ctrl+C to stop.[/dim]"
                )
                console.print(
                    f"[dim]Last updated:[/dim] {datetime.now().strftime('%H:%M:%S')}\n"
                )
                try:
                    with geneva_client(
                        db_uri, namespace, context, show_context=False
                    ) as client:
                        jobs = client.list_jobs(
                            status=job_status,
                            launched_after=launched_after,
                            launched_before=launched_before,
                            limit=limit,
                        )
                    format_jobs(jobs, output)
                except GenevaClientError as e:
                    err_console.print(f"[red]Error:[/red] {e}")
                time.sleep(10)
        except KeyboardInterrupt:
            err_console.print("\n[dim]Watch stopped[/dim]")
    else:
        try:
            with geneva_client(db_uri, namespace, context) as client:
                jobs = client.list_jobs(
                    status=job_status,
                    launched_after=launched_after,
                    launched_before=launched_before,
                    limit=limit,
                )
        except GenevaClientError as e:
            err_console.print(f"[red]Error:[/red] {e}")
            raise typer.Exit(1) from e

        format_jobs(jobs, output)


@jobs_app.command("get")
def get_job_cmd(
    job_id: Annotated[str, typer.Argument(help="Job ID")],
    output: OutputFormatOption = OutputFormat.TEXT,
    namespace: NamespaceOption = None,
    context: ContextOption = None,
    watch: Annotated[
        bool,
        typer.Option(
            "--watch",
            "-w",
            help="Auto-refresh every 10 seconds (Ctrl+C to stop)",
        ),
    ] = False,
) -> None:
    """Get detailed information about a job."""
    db_uri = require_db_uri()

    if watch:
        import time

        try:
            while True:
                console.clear()
                console.print(
                    "[dim]Auto-refreshing every 10s. Press Ctrl+C to stop.[/dim]"
                )
                console.print(
                    f"[dim]Last updated:[/dim] {datetime.now().strftime('%H:%M:%S')}\n"
                )
                try:
                    with geneva_client(
                        db_uri, namespace, context, show_context=False
                    ) as client:
                        job = client.get_job(job_id)
                    format_job_detail(job, output)
                except GenevaClientError as e:
                    err_console.print(f"[red]Error:[/red] {e}")
                time.sleep(10)
        except KeyboardInterrupt:
            err_console.print("\n[dim]Watch stopped[/dim]")
    else:
        try:
            with geneva_client(db_uri, namespace, context) as client:
                job = client.get_job(job_id)
        except GenevaClientError as e:
            err_console.print(f"[red]Error:[/red] {e}")
            raise typer.Exit(1) from e

        format_job_detail(job, output)


# ============================================================================
# RayClusters commands
# ============================================================================

rayclusters_app = typer.Typer(help="Manage Kuberay clusters")
app.add_typer(rayclusters_app, name="rayclusters")


@rayclusters_app.command("list")
def list_rayclusters_cmd(
    output: OutputFormatOption = OutputFormat.TABLE,
    namespace: NamespaceOption = None,
    context: ContextOption = None,
) -> None:
    """List RayClusters in the cluster."""
    with Live(
        Spinner("dots", text="Fetching RayClusters..."),
        console=err_console,
        transient=True,
    ):
        try:
            clusters, ctx = list_ray_clusters(namespace, context)
        except KubernetesError as e:
            err_console.print(f"[red]Error:[/red] {e}")
            raise typer.Exit(1) from e

    err_console.print(f"[dim]Using context:[/dim] [bold]{ctx}[/bold]")
    format_ray_clusters(clusters, output)


@rayclusters_app.command("get")
def get_raycluster_cmd(
    name: Annotated[str, typer.Argument(help="RayCluster name")],
    output: OutputFormatOption = OutputFormat.TEXT,
    namespace: NamespaceOption = None,
    context: ContextOption = None,
) -> None:
    """Get detailed information about a RayCluster."""
    with Live(
        Spinner("dots", text="Fetching RayCluster..."),
        console=err_console,
        transient=True,
    ):
        try:
            cluster, ctx = get_ray_cluster(name, namespace, context)
        except KubernetesError as e:
            err_console.print(f"[red]Error:[/red] {e}")
            raise typer.Exit(1) from e

    err_console.print(f"[dim]Using context:[/dim] [bold]{ctx}[/bold]")
    format_ray_cluster_detail(cluster, output)


# ============================================================================
# Logs command
# ============================================================================


@app.command("logs")
def logs_cmd(
    job_id: Annotated[
        str,
        typer.Argument(help="Job ID or pod name to stream logs from"),
    ],
    namespace: NamespaceOption = None,
    context: ContextOption = None,
    container: Annotated[
        Optional[str],
        typer.Option(
            "--container",
            "-c",
            help="Container name (for multi-container pods)",
        ),
    ] = None,
    follow: Annotated[
        bool,
        typer.Option(
            "--follow",
            "-f",
            help="Follow log output (stream continuously)",
        ),
    ] = True,
    tail: Annotated[
        Optional[int],
        typer.Option(
            "--tail",
            help="Number of lines to show from end of logs",
        ),
    ] = None,
) -> None:
    """Stream logs from a Geneva job or pod."""
    ns = namespace or get_namespace()

    # First, try to find pods for this job
    with Live(
        Spinner("dots", text="Finding pods..."), console=err_console, transient=True
    ):
        try:
            pods = get_job_pods(job_id, ns, context)
        except KubernetesError as e:
            err_console.print(f"[red]Error:[/red] {e}")
            raise typer.Exit(1) from e

    if not pods:
        # Assume job_id is actually a pod name
        pods = [job_id]

    if len(pods) > 1:
        err_console.print(
            f"[yellow]Found {len(pods)} pods, streaming from first:[/yellow] {pods[0]}"
        )

    pod_name = pods[0]
    err_console.print(f"[dim]Streaming logs from pod:[/dim] [bold]{pod_name}[/bold]")

    try:
        for line in stream_pod_logs(
            pod_name,
            namespace=ns,
            context=context,
            container=container,
            follow=follow,
            tail_lines=tail,
        ):
            console.print(line)
    except KubernetesError as e:
        err_console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from e
    except KeyboardInterrupt:
        err_console.print("\n[dim]Log streaming stopped[/dim]")


# ============================================================================
# Plan commands
# ============================================================================

plan_app = typer.Typer(
    name="plan",
    help="Plan jobs without executing them (dry-run mode)",
    no_args_is_help=True,
)
app.add_typer(plan_app)


@plan_app.command("backfill")
def plan_backfill_cmd(
    table_name: Annotated[str, typer.Argument(help="Table name")],
    column: Annotated[str, typer.Argument(help="Column name to backfill")],
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Output as JSON"),
    ] = False,
) -> None:
    """Plan a backfill job and show what work would be done."""
    db_uri = require_db_uri()

    try:
        import geneva

        conn = geneva.connect(db_uri)
        table = conn.open_table(table_name)
        plan = table.plan_backfill(column)
    except Exception as e:
        err_console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from e

    if json_output:
        import json

        import attrs

        console.print(json.dumps(attrs.asdict(plan), indent=2))
    else:
        console.print(
            Panel(
                f"[bold]Job type:[/bold] {plan.job_type}\n"
                f"[bold]Has work:[/bold] {plan.has_work}\n"
                f"[bold]Total tasks:[/bold] {plan.total_tasks}\n"
                f"[bold]Rows pending:[/bold] {plan.total_rows_pending}\n"
                f"[bold]Skipped fragments:[/bold] {plan.skipped_fragments}\n"
                f"[bold]Skipped rows:[/bold] {plan.skipped_rows}\n"
                f"[bold]Total fragments:[/bold] {plan.total_fragments}\n"
                f"[bold]Total rows:[/bold] {plan.total_rows}\n"
                f"[bold]WHERE filter:[/bold] {plan.where or '(none)'}\n"
                f"[bold]UDF mismatch:[/bold] {plan.udf_mismatch}\n"
                f"[bold]Srcfiles mismatch:[/bold] {plan.srcfiles_mismatch}",
                title=f"Backfill Plan: {table_name}.{column}",
                border_style="cyan",
            )
        )

    raise typer.Exit(0 if not plan.has_work else 2)


@plan_app.command("refresh")
def plan_refresh_cmd(
    table_name: Annotated[str, typer.Argument(help="Materialized view name")],
    src_version: Annotated[
        Optional[int],
        typer.Option("--src-version", help="Source table version to refresh from"),
    ] = None,
    json_output: Annotated[
        bool,
        typer.Option("--json", help="Output as JSON"),
    ] = False,
) -> None:
    """Plan a refresh job and show what work would be done."""
    db_uri = require_db_uri()

    try:
        import geneva

        conn = geneva.connect(db_uri)
        table = conn.open_table(table_name)
        plan = table.plan_refresh(src_version=src_version)
    except Exception as e:
        err_console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(1) from e

    if json_output:
        import json

        import attrs

        console.print(json.dumps(attrs.asdict(plan), indent=2))
    else:
        console.print(
            Panel(
                f"[bold]Job type:[/bold] {plan.job_type}\n"
                f"[bold]Has work:[/bold] {plan.has_work}\n"
                f"[bold]New source fragments:[/bold] {plan.new_source_fragments}\n"
                f"[bold]Rows pending:[/bold] {plan.total_rows_pending}\n"
                f"[bold]Total source fragments:[/bold] {plan.total_fragments}\n"
                f"[bold]Total source rows:[/bold] {plan.total_rows}",
                title=f"Refresh Plan: {table_name}",
                border_style="cyan",
            )
        )

    raise typer.Exit(0 if not plan.has_work else 2)


if __name__ == "__main__":
    app()
