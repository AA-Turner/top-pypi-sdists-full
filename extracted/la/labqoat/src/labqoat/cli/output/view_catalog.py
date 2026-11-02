"""Curated columns for the resource lists people look at most."""

from typing import ClassVar

from labqoat.cli.output.view_column import ViewColumn


class ViewCatalog:
    """Name the few fields that identify and explain each kind of resource."""

    views: ClassVar[dict[str, tuple[ViewColumn, ...]]] = {
        "project list": (
            ViewColumn("NAME", "name"),
            ViewColumn("SELECTED", "selected"),
            ViewColumn("RUNS", "runs"),
            ViewColumn("ACTIVE", "active_runs"),
            ViewColumn("DATASETS", "datasets"),
            ViewColumn("DASHBOARDS", "dashboards"),
            ViewColumn("LAST RUN", "last_run_at", "time"),
            ViewColumn("DESCRIPTION", "description"),
        ),
        "volume list": (
            ViewColumn("NAME", "name"),
            ViewColumn("FILES", "files"),
            ViewColumn("SIZE", "bytes", "bytes"),
            ViewColumn("LIMIT", "limit_bytes", "bytes"),
            ViewColumn("VERSION", "version"),
            ViewColumn("UPDATED", "updated_at", "time"),
            ViewColumn("WARNING", "warning", optional=True),
        ),
        "volume ls": (
            ViewColumn("PATH", "path"),
            ViewColumn("KIND", "kind"),
            ViewColumn("SIZE", "size", "bytes"),
            ViewColumn("MODIFIED", "modified", "time"),
        ),
        "run list": (
            ViewColumn("ID", "id", "id"),
            ViewColumn("NAME", "name"),
            ViewColumn("KEY", "child_operation_key", optional=True),
            ViewColumn("STATUS", "status", "status"),
            ViewColumn("REASON", "failure_detail.reason"),
        ),
        "build list": (
            ViewColumn("ID", "id", "id"),
            ViewColumn("STATUS", "status", "status"),
            ViewColumn("SOURCE", "recipe.source_kind"),
            ViewColumn("CREATED", "inserted_at", "time"),
            ViewColumn("UPDATED", "updated_at", "time"),
        ),
        "node list": (
            ViewColumn("ID", "id", "id"),
            ViewColumn("LOCATION", "location_id"),
            ViewColumn("TYPE", "instance_family"),
            ViewColumn("STATE", "state", "status"),
            ViewColumn("RUNS", "allocations"),
            ViewColumn("FREE CPU", "allocatable.cpu_millicores", "cpu"),
            ViewColumn("FREE MEM", "allocatable.memory_mb", "memory"),
            ViewColumn("GPUS", "capacity.gpu_count"),
        ),
        "pool list": (
            ViewColumn("ID", "id"),
            ViewColumn("PROVIDER", "provider"),
            ViewColumn("STATE", "state", "status"),
            ViewColumn("MACHINES", "configuration.machine_count"),
            ViewColumn("FREE CPU", "allocatable.cpu_millicores", "cpu"),
            ViewColumn("FREE MEM", "allocatable.memory_mb", "memory"),
            ViewColumn("PAUSED", "configuration.paused"),
        ),
        "worker list": (
            ViewColumn("ID", "id", "id"),
            ViewColumn("STATE", "state", "status"),
            ViewColumn("KIND", "workload_kind"),
            ViewColumn("TYPE", "placement.family"),
            ViewColumn("LOCATION", "placement.location_id"),
            ViewColumn("RUN", "run_id", "id"),
            ViewColumn("STARTED", "started_at", "time"),
            ViewColumn("ENDED", "ended_at", "time"),
        ),
        "asset list": (
            ViewColumn("ID", "id", "id"),
            ViewColumn("STATE", "availability", "status"),
            ViewColumn("SIZE", "byte_size", "bytes"),
            ViewColumn("TYPE", "media_type"),
        ),
        "dict list": (
            ViewColumn("NAME", "name"),
            ViewColumn("ENTRIES", "entries"),
            ViewColumn("CREATED", "created_at", "time"),
        ),
        "queue list": (
            ViewColumn("NAME", "name"),
            ViewColumn("VALUES", "items"),
            ViewColumn("CREATED", "created_at", "time"),
        ),
        "compute offerings": (
            ViewColumn("GPU", "gpu"),
            ViewColumn("GPU GB", "gpu_memory_gb"),
            ViewColumn("PER MACHINE", "gpus_per_machine"),
            ViewColumn("CHEAPEST", "cheapest.shape"),
            ViewColumn("USD/H", "cheapest.hourly_rate"),
            ViewColumn("AT", "cheapest.location"),
            ViewColumn("LOCATIONS", "locations"),
        ),
        "compute quotas": (
            ViewColumn("LOCATION", "location"),
            ViewColumn("GROUP", "group"),
            ViewColumn("KIND", "kind"),
            ViewColumn("LIMIT", "limit"),
            ViewColumn("USED", "used"),
            ViewColumn("FREE", "free"),
            ViewColumn("UNIT", "unit"),
            ViewColumn("CURRENT", "current"),
            ViewColumn("ERROR", "error", optional=True),
        ),
        "compute usage": (
            ViewColumn("GPU", "family"),
            ViewColumn("RUNNING", "lifecycle.active"),
            ViewColumn("STARTING", "lifecycle.starting"),
            ViewColumn("WARM", "lifecycle.warm"),
            ViewColumn("RELEASING", "lifecycle.releasing"),
        ),
        "doctor": (
            ViewColumn("CHECK", "name"),
            ViewColumn("STATUS", "status", "status"),
            ViewColumn("DETAIL", "message"),
        ),
    }

    @classmethod
    def columns(cls, command: str) -> tuple[ViewColumn, ...] | None:
        """Curated columns for a command such as ``run list``; None lets columns be inferred."""
        return cls.views.get(command)
