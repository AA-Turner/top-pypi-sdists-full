"""Canonical capacity, worker, and platform reads."""

from __future__ import annotations

import click

from labqoat.cli.endpoint_command import EndpointCommand
from labqoat.cli.group_help import GroupHelp
from labqoat.cli.log_feed_command import LogFeedCommand
from labqoat.cli.parameter_factory import ParameterFactory


class OperationalCommandCatalog:
    """Assemble the read-only environment platform operations tree."""

    @classmethod
    def add(cls, root: click.Group) -> None:
        """Register all operational resource and platform groups."""
        root.add_command(cls._nodes())
        root.add_command(cls._pools())
        root.add_command(cls._workers())
        root.add_command(cls._platform())
        root.add_command(cls._locations())

    @classmethod
    def _locations(cls) -> click.Group:
        """Expose the permitted physical destinations separately from logical environments."""
        group = cls._group("locations", "Inspect allowed execution locations.")
        group.add_command(EndpointCommand("list", "/api/v1/locations", [], "List configured locations."))
        return group

    @classmethod
    def _nodes(cls) -> click.Group:
        """Build environment capacity node inspection commands."""
        group = cls._group("node", "Inspect schedulable capacity nodes.")
        reference = [ParameterFactory.argument("node_ref")]
        group.add_command(EndpointCommand("get", "/api/v1/nodes/item", reference, "Get a node.", "node_ref"))
        group.add_command(EndpointCommand("list", "/api/v1/nodes", cls._node_filters(), "List nodes."))
        group.add_command(
            LogFeedCommand(
                "/api/v1/nodes/item/logs",
                reference,
                "Read or follow active and retained workload logs on a node.",
                "node_ref",
            )
        )
        return group

    @classmethod
    def _pools(cls) -> click.Group:
        """Build per-location machine supply inspection commands."""
        group = cls._group("pool", "Inspect per-location machine supply (pool id = location id).")
        reference = [ParameterFactory.argument("pool_ref")]
        group.add_command(
            EndpointCommand("get", "/api/v1/pools/item", reference, "Get one location's machine supply.", "pool_ref")
        )
        group.add_command(
            EndpointCommand("list", "/api/v1/pools", cls._pool_filters(), "List per-location machine supply.")
        )
        group.add_command(
            LogFeedCommand(
                "/api/v1/pools/item/logs",
                reference,
                "Read or follow active and retained workload logs at a location.",
                "pool_ref",
            )
        )
        return group

    @classmethod
    def _workers(cls) -> click.Group:
        """Build worker lifecycle inspection commands."""
        group = cls._group("worker", "Inspect workload worker lifecycles.")
        reference = [ParameterFactory.argument("worker_ref")]
        group.add_command(EndpointCommand("get", "/api/v1/workers/item", reference, "Get a worker.", "worker_ref"))
        group.add_command(EndpointCommand("list", "/api/v1/workers", cls._worker_filters(), "List workers."))
        logs = [ParameterFactory.argument("worker_ref"), *cls._log_filters()]
        group.add_command(
            LogFeedCommand("/api/v1/workers/item/logs", logs, "Read or follow worker logs.", "worker_ref")
        )
        return group

    @classmethod
    def _platform(cls) -> click.Group:
        """Build the authenticated platform capability command."""
        group = cls._group("platform", "Inspect platform status and capabilities.")
        group.add_command(EndpointCommand("get", "/api/v1/capabilities", [], "Get platform capabilities."))
        return group

    @staticmethod
    def _node_filters() -> list[click.Parameter]:
        """Declare exact capacity node filters."""
        return [
            ParameterFactory.limit(),
            ParameterFactory.text_option("cursor"),
            ParameterFactory.text_option("pool"),
            ParameterFactory.choice_option("state", ["provisioning", "ready", "draining", "terminated"]),
            ParameterFactory.text_option("provider"),
            ParameterFactory.text_option("gpu_model"),
            ParameterFactory.text_option("instance_family"),
            ParameterFactory.choice_option("sort", ["node_id:asc"], "node_id:asc"),
        ]

    @staticmethod
    def _pool_filters() -> list[click.Parameter]:
        """Declare exact location supply filters."""
        return [
            ParameterFactory.limit(),
            ParameterFactory.text_option("cursor"),
            ParameterFactory.text_option("prefix"),
            ParameterFactory.text_option("provider"),
            ParameterFactory.choice_option("sort", ["name:asc"], "name:asc"),
        ]

    @staticmethod
    def _worker_filters() -> list[click.Parameter]:
        """Declare exact worker lifecycle filters."""
        states = ["provisioning", "starting", "running", "terminating", "failed", "succeeded", "terminated", "unknown"]
        kinds = ["import", "job", "maintenance", "training"]
        return [
            ParameterFactory.limit(),
            ParameterFactory.text_option("cursor"),
            ParameterFactory.choice_option("active", ["true", "false"]),
            ParameterFactory.time_option("created_after"),
            ParameterFactory.time_option("created_before"),
            ParameterFactory.text_option("node_id"),
            ParameterFactory.choice_option("sort", ["created_at:asc", "created_at:desc"], "created_at:desc"),
            ParameterFactory.text_option("run_id"),
            ParameterFactory.choice_option("state", states),
            ParameterFactory.choice_option("workload_kind", kinds),
        ]

    @staticmethod
    def _log_filters() -> list[click.Parameter]:
        """Declare exact worker log filters."""
        return [
            ParameterFactory.limit(),
            ParameterFactory.text_option("cursor"),
            ParameterFactory.time_option("timestamp_after"),
            ParameterFactory.time_option("timestamp_before"),
            ParameterFactory.choice_option("sort", ["timestamp:asc", "timestamp:desc"], "timestamp:desc"),
        ]

    @staticmethod
    def _group(name: str, help_text: str) -> click.Group:
        """Create one help-first operational group."""
        return click.Group(name, help=help_text, callback=GroupHelp.show, invoke_without_command=True)
