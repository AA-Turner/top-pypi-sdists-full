# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Output formatters for CLI responses."""

import json
from datetime import datetime, timezone
from enum import Enum

from .models import Cluster, Job, Manifest, RayCluster
from rich.console import Console
from rich.table import Table
from rich.text import Text


class OutputFormat(str, Enum):
    """Output format enum."""

    TEXT = "text"
    JSON = "json"
    TABLE = "table"


console = Console()


def _format_datetime(dt: datetime | None) -> str:
    """Format datetime for display."""
    if dt is None:
        return "-"

    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    delta = now - dt
    seconds = delta.total_seconds()

    if seconds < 60:
        return f"{int(seconds)}s ago"
    elif seconds < 3600:
        return f"{int(seconds / 60)}m ago"
    elif seconds < 86400:
        return f"{int(seconds / 3600)}h ago"
    elif seconds < 604800:
        return f"{int(seconds / 86400)}d ago"
    else:
        return dt.strftime("%Y-%m-%d %H:%M")


def _status_style(status: str) -> str:
    """Get rich style for job status."""
    status_lower = status.lower()
    if status_lower in ("completed", "done", "ready"):
        return "green"
    elif status_lower == "running":
        return "green bold"
    elif status_lower in ("failed", "error"):
        return "red bold"
    elif status_lower in ("pending", "initializing"):
        return "yellow"
    elif status_lower == "cancelled":
        return "dim"
    return "white"


def _format_duration(
    launched_at: datetime | None, completed_at: datetime | None
) -> str:
    """Calculate and format job duration."""
    if not launched_at:
        return "-"

    end_time = completed_at or datetime.now(timezone.utc)
    if launched_at.tzinfo is None:
        launched_at = launched_at.replace(tzinfo=timezone.utc)
    if end_time.tzinfo is None:
        end_time = end_time.replace(tzinfo=timezone.utc)
    delta = end_time - launched_at
    total_seconds = int(delta.total_seconds())

    if total_seconds < 60:
        return f"{total_seconds}s"
    elif total_seconds < 3600:
        return f"{total_seconds // 60}m {total_seconds % 60}s"
    else:
        hours = total_seconds // 3600
        mins = (total_seconds % 3600) // 60
        return f"{hours}h {mins}m"


def format_clusters(clusters: list[Cluster], fmt: OutputFormat) -> None:
    """Format and print cluster list."""
    if fmt == OutputFormat.JSON:
        data = [c.model_dump(by_alias=True) for c in clusters]
        console.print_json(json.dumps(data, default=str))
        return

    if not clusters:
        console.print("[dim]No clusters found[/dim]")
        return

    if fmt == OutputFormat.TABLE:
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Name", style="bold")
        table.add_column("Type")
        table.add_column("Created By")
        table.add_column("Created")

        for cluster in clusters:
            table.add_row(
                cluster.name,
                cluster.cluster_type or "-",
                cluster.created_by or "-",
                _format_datetime(cluster.created_at),
            )
        console.print(table)
    else:
        # Text format
        for cluster in clusters:
            console.print(f"[bold]{cluster.name}[/bold]")
            if cluster.cluster_type:
                console.print(f"  [dim]Type:[/dim] {cluster.cluster_type}")
            if cluster.created_by:
                console.print(f"  [dim]Created By:[/dim] {cluster.created_by}")
            if cluster.created_at:
                console.print(
                    f"  [dim]Created:[/dim] {_format_datetime(cluster.created_at)}"
                )


def format_manifests(manifests: list[Manifest], fmt: OutputFormat) -> None:
    """Format and print manifest list."""
    if fmt == OutputFormat.JSON:
        data = [m.model_dump(by_alias=True) for m in manifests]
        console.print_json(json.dumps(data, default=str))
        return

    if not manifests:
        console.print("[dim]No manifests found[/dim]")
        return

    if fmt == OutputFormat.TABLE:
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Name", style="bold")
        table.add_column("Version")
        table.add_column("Checksum", max_width=12)
        table.add_column("Created By")
        table.add_column("Created")

        for manifest in manifests:
            checksum = manifest.checksum[:8] + "..." if manifest.checksum else "-"
            table.add_row(
                manifest.name,
                manifest.version or "-",
                checksum,
                manifest.created_by or "-",
                _format_datetime(manifest.created_at),
            )
        console.print(table)
    else:
        # Text format
        for manifest in manifests:
            version = f" v{manifest.version}" if manifest.version else ""
            console.print(f"[bold]{manifest.name}[/bold][dim]{version}[/dim]")
            if manifest.created_by:
                console.print(f"  [dim]Created By:[/dim] {manifest.created_by}")
            if manifest.created_at:
                console.print(
                    f"  [dim]Created:[/dim] {_format_datetime(manifest.created_at)}"
                )


def format_jobs(jobs: list[Job], fmt: OutputFormat) -> None:
    """Format and print job list."""
    if fmt == OutputFormat.JSON:
        data = [j.model_dump(by_alias=True) for j in jobs]
        console.print_json(json.dumps(data, default=str))
        return

    if not jobs:
        console.print("[dim]No jobs found[/dim]")
        return

    if fmt == OutputFormat.TABLE:
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Job ID", style="bold", max_width=36)
        table.add_column("Type")
        table.add_column("Table")
        table.add_column("Status")
        table.add_column("Launched By")
        table.add_column("Launched")
        table.add_column("Duration")

        for job in jobs:
            # Calculate duration
            duration = _format_duration(job.launched_at, job.completed_at)

            # Truncate table name for display
            table_name = job.table_name or "-"
            if len(table_name) > 16:
                table_name = table_name[:13] + "..."

            table.add_row(
                job.job_id,
                job.job_type or "-",
                table_name,
                Text(job.status.value, style=_status_style(job.status.value)),
                job.launched_by or "-",
                _format_datetime(job.launched_at),
                duration,
            )
        console.print(table)
    else:
        # Text format
        for job in jobs:
            status_style = _status_style(job.status.value)
            console.print(
                f"[bold]{job.job_id}[/bold] [{status_style}]{job.status.value}[/]"
            )
            if job.job_type:
                console.print(f"  [dim]Type:[/dim] {job.job_type}")
            if job.table_name:
                console.print(f"  [dim]Table:[/dim] {job.table_name}")
            if job.column_name:
                console.print(f"  [dim]Column:[/dim] {job.column_name}")
            if job.launched_by:
                console.print(f"  [dim]Launched By:[/dim] {job.launched_by}")
            if job.launched_at:
                console.print(
                    f"  [dim]Launched:[/dim] {_format_datetime(job.launched_at)}"
                )


def format_ray_clusters(clusters: list[RayCluster], fmt: OutputFormat) -> None:
    """Format and print RayCluster list."""
    if fmt == OutputFormat.JSON:
        data = [c.model_dump() for c in clusters]
        console.print_json(json.dumps(data, default=str))
        return

    if not clusters:
        console.print("[dim]No RayClusters found[/dim]")
        return

    if fmt == OutputFormat.TABLE:
        table = Table(show_header=True, header_style="bold cyan")
        table.add_column("Name", style="bold")
        table.add_column("Namespace")
        table.add_column("Status")
        table.add_column("Head Pod")
        table.add_column("Workers")
        table.add_column("Created")

        for cluster in clusters:
            status = cluster.status or "-"
            table.add_row(
                cluster.name,
                cluster.namespace,
                Text(status, style=_status_style(status)),
                cluster.head_pod or "-",
                str(cluster.worker_replicas)
                if cluster.worker_replicas is not None
                else "-",
                _format_datetime(cluster.created_at),
            )
        console.print(table)
    else:
        # Text format
        for cluster in clusters:
            status = cluster.status or ""
            status_text = f" [{_status_style(status)}]{status}[/]" if status else ""
            console.print(f"[bold]{cluster.name}[/bold]{status_text}")
            console.print(f"  [dim]Namespace:[/dim] {cluster.namespace}")
            if cluster.head_pod:
                console.print(f"  [dim]Head:[/dim] {cluster.head_pod}")
            if cluster.worker_replicas is not None:
                console.print(f"  [dim]Workers:[/dim] {cluster.worker_replicas}")
            if cluster.created_at:
                console.print(
                    f"  [dim]Created:[/dim] {_format_datetime(cluster.created_at)}"
                )


def format_ray_cluster_detail(cluster: RayCluster, fmt: OutputFormat) -> None:
    """Format and print detailed RayCluster info."""
    if fmt == OutputFormat.JSON:
        console.print_json(json.dumps(cluster.model_dump(), default=str))
        return

    status = cluster.status or ""
    status_text = f" [{_status_style(status)}]{status}[/]" if status else ""
    console.print(
        f"[bold cyan]RayCluster:[/bold cyan] [bold]{cluster.name}[/bold]{status_text}"
    )
    console.print(f"  [dim]Namespace:[/dim]   {cluster.namespace}")
    if cluster.head_pod:
        console.print(f"  [dim]Head Pod:[/dim]    {cluster.head_pod}")
    if cluster.worker_replicas is not None:
        console.print(f"  [dim]Workers:[/dim]     {cluster.worker_replicas}")
    console.print(f"  [dim]Created:[/dim]     {_format_datetime(cluster.created_at)}")


# ============================================================================
# Detailed formatters for single resources (get commands)
# ============================================================================


def format_cluster_detail(cluster: Cluster, fmt: OutputFormat) -> None:
    """Format and print detailed cluster info."""
    if fmt == OutputFormat.JSON:
        data = cluster.model_dump(by_alias=True)
        console.print_json(json.dumps(data, default=str))
        return

    console.print(f"[bold cyan]Cluster:[/bold cyan] [bold]{cluster.name}[/bold]")
    if cluster.cluster_type:
        console.print(f"  [dim]Type:[/dim]        {cluster.cluster_type}")
    if cluster.ray_address:
        console.print(f"  [dim]Ray Address:[/dim] {cluster.ray_address}")
    if cluster.created_by:
        console.print(f"  [dim]Created By:[/dim]  {cluster.created_by}")
    console.print(f"  [dim]Created:[/dim]     {_format_datetime(cluster.created_at)}")

    # Show kuberay config if present
    if cluster.kuberay:
        console.print("\n[bold cyan]KubeRay Config:[/bold cyan]")
        kuberay = cluster.kuberay
        if kuberay.get("namespace"):
            console.print(f"  [dim]Namespace:[/dim]      {kuberay['namespace']}")
        if kuberay.get("config_method"):
            console.print(f"  [dim]Config Method:[/dim]  {kuberay['config_method']}")
        if kuberay.get("aws_region"):
            console.print(f"  [dim]AWS Region:[/dim]     {kuberay['aws_region']}")

        # Head group
        if kuberay.get("head_group"):
            hg = kuberay["head_group"]
            console.print("\n  [bold]Head Group:[/bold]")
            if hg.get("image"):
                console.print(f"    [dim]Image:[/dim]    {hg['image']}")
            if hg.get("num_cpus"):
                console.print(f"    [dim]CPUs:[/dim]     {hg['num_cpus']}")
            if hg.get("memory"):
                console.print(f"    [dim]Memory:[/dim]   {hg['memory']}")

        # Worker groups
        if kuberay.get("worker_groups"):
            for i, wg in enumerate(kuberay["worker_groups"]):
                console.print(f"\n  [bold]Worker Group {i + 1}:[/bold]")
                if wg.get("image"):
                    console.print(f"    [dim]Image:[/dim]       {wg['image']}")
                if wg.get("num_cpus"):
                    console.print(f"    [dim]CPUs:[/dim]        {wg['num_cpus']}")
                if wg.get("memory"):
                    console.print(f"    [dim]Memory:[/dim]      {wg['memory']}")
                if wg.get("replicas") is not None:
                    console.print(f"    [dim]Replicas:[/dim]    {wg['replicas']}")
                if wg.get("min_replicas") is not None:
                    console.print(f"    [dim]Min Replicas:[/dim] {wg['min_replicas']}")
                if wg.get("max_replicas") is not None:
                    console.print(f"    [dim]Max Replicas:[/dim] {wg['max_replicas']}")


def format_manifest_detail(manifest: Manifest, fmt: OutputFormat) -> None:
    """Format and print detailed manifest info."""
    if fmt == OutputFormat.JSON:
        data = manifest.model_dump(by_alias=True)
        console.print_json(json.dumps(data, default=str))
        return

    console.print(f"[bold cyan]Manifest:[/bold cyan] [bold]{manifest.name}[/bold]")
    console.print(f"  [dim]Version:[/dim]            {manifest.version or '-'}")
    if manifest.checksum:
        console.print(f"  [dim]Checksum:[/dim]           {manifest.checksum}")
    if manifest.created_by:
        console.print(f"  [dim]Created By:[/dim]         {manifest.created_by}")
    console.print(
        f"  [dim]Created:[/dim]            {_format_datetime(manifest.created_at)}"
    )
    console.print(f"  [dim]Skip Site Packages:[/dim] {manifest.skip_site_packages}")

    # Images
    if manifest.head_image:
        console.print(f"  [dim]Head Image:[/dim]         {manifest.head_image}")
    if manifest.worker_image:
        console.print(f"  [dim]Worker Image:[/dim]       {manifest.worker_image}")

    if manifest.pip:
        console.print("\n[bold cyan]Pip Dependencies:[/bold cyan]")
        for dep in manifest.pip:
            console.print(f"  - {dep}")

    if manifest.py_modules:
        console.print("\n[bold cyan]Python Modules:[/bold cyan]")
        for mod in manifest.py_modules:
            console.print(f"  - {mod}")

    if manifest.zips:
        # Filter out empty zip entries
        non_empty_zips = [z for z in manifest.zips if z]
        if non_empty_zips:
            console.print("\n[bold cyan]Zips:[/bold cyan]")
            for zip_entry in non_empty_zips:
                for z in zip_entry:
                    console.print(f"  - {z}")


def format_job_detail(job: Job, fmt: OutputFormat) -> None:
    """Format and print detailed job info."""
    if fmt == OutputFormat.JSON:
        console.print_json(json.dumps(job.model_dump(by_alias=True), default=str))
        return

    status_style = _status_style(job.status.value)
    console.print(
        f"[bold cyan]Job:[/bold cyan] [bold]{job.job_id}[/bold]"
        f" [{status_style}]{job.status.value}[/]"
    )

    # Basic info
    if job.job_type:
        console.print(f"  [dim]Type:[/dim]             {job.job_type}")
    if job.table_name:
        console.print(f"  [dim]Table:[/dim]            {job.table_name}")
    if job.column_name:
        console.print(f"  [dim]Column:[/dim]           {job.column_name}")

    # Execution info
    if job.manifest_id:
        console.print(f"  [dim]Manifest ID:[/dim]      {job.manifest_id}")
    if job.manifest_checksum:
        console.print(f"  [dim]Manifest Checksum:[/dim] {job.manifest_checksum}")
    if job.launched_by:
        console.print(f"  [dim]Launched By:[/dim]      {job.launched_by}")

    # Timing info
    console.print(f"  [dim]Launched:[/dim]         {_format_datetime(job.launched_at)}")
    if job.completed_at:
        console.print(
            f"  [dim]Completed:[/dim]        {_format_datetime(job.completed_at)}"
        )
    duration = _format_duration(job.launched_at, job.completed_at)
    console.print(f"  [dim]Duration:[/dim]         {duration}")
    if job.updated_at:
        console.print(
            f"  [dim]Updated:[/dim]          {_format_datetime(job.updated_at)}"
        )

    # Config (parse from JSON string if needed)
    config_dict = job.get_config_dict()
    if config_dict:
        console.print("\n[bold cyan]Config:[/bold cyan]")
        for key, value in config_dict.items():
            if value is not None:
                console.print(f"  [dim]{key}:[/dim] {value}")

    # Events (formatted with timeline)
    if job.events:
        console.print("\n[bold cyan]Events:[/bold cyan]")
        for i, event in enumerate(job.events):
            prefix = "[green]✔[/green]" if i == len(job.events) - 1 else "[dim]│[/dim]"
            console.print(f"  {prefix} {event}")

    # Metrics (formatted as table if present)
    parsed_metrics = job.get_metrics_parsed()
    if parsed_metrics:
        console.print("\n[bold cyan]Metrics:[/bold cyan]")
        table = Table(show_header=True, header_style="bold", box=None, padding=(0, 2))
        table.add_column("Name")
        table.add_column("Progress", justify="right")
        table.add_column("Done")
        table.add_column("Description")
        for metric in parsed_metrics:
            progress = (
                f"{metric.n}/{metric.total}" if metric.total > 0 else str(metric.n)
            )
            done_text = Text(
                "✔" if metric.done else "-", style="green" if metric.done else "dim"
            )
            table.add_row(metric.name, progress, done_text, metric.desc)
        console.print(table)
    elif job.metrics:
        # Fallback for unparsed metrics
        console.print("\n[bold cyan]Metrics:[/bold cyan]")
        for metric in job.metrics:
            if metric:
                console.print(f"  - {metric}")
