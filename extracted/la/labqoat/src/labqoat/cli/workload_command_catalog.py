"""Import workload command tree."""

from __future__ import annotations

from typing import ClassVar

import click

from labqoat.cli.delete_endpoint_command import DeleteEndpointCommand
from labqoat.cli.endpoint_command import EndpointCommand
from labqoat.cli.group_help import GroupHelp
from labqoat.cli.mutation_spec import MutationSpec
from labqoat.cli.parameter_factory import ParameterFactory
from labqoat.cli.payload_command import PayloadCommand
from labqoat.cli.run_logs_command import RunLogsCommand
from labqoat.cli.run_output_command import RunOutputCommand
from labqoat.cli.run_watch_command import RunWatchCommand


class WorkloadCommandCatalog:
    """Assemble remaining workload aliases over shared run resources."""

    kinds: ClassVar[dict[str, str]] = {
        "import": "import",
    }

    @classmethod
    def add(cls, root: click.Group) -> None:
        """Register all canonical workload groups."""
        for workload in cls.kinds:
            root.add_command(cls.group(workload))

    @classmethod
    def group(cls, workload: str) -> click.Group:
        """Build one complete kind-scoped workload group."""
        group = click.Group(
            workload,
            help=f"Inspect and manage {workload} workloads.",
            callback=GroupHelp.show,
            invoke_without_command=True,
        )
        cls._add_reads(group, workload)
        cls._add_feeds(group, workload)
        cls._add_mutations(group, workload)
        return group

    @classmethod
    def _add_reads(cls, group: click.Group, workload: str) -> None:
        """Register kind-scoped run reads and child pages."""
        fixed = {"expected_kind": cls.kinds[workload]}
        group.add_command(
            EndpointCommand(
                "list",
                "/api/v1/runs",
                cls.list_filters(),
                "List workload runs.",
                fixed_query={"kind": cls.kinds[workload]},
            )
        )
        reference = [ParameterFactory.argument("run_ref")]
        for name, path in (("get", "{ref}"), ("status", "{ref}"), ("placement", "{ref}/placement")):
            group.add_command(
                EndpointCommand(name, f"/api/v1/runs/{path}", reference, f"Read {name}.", "run_ref", fixed)
            )
        for name in ("assets", "outputs"):
            path = "produced-assets" if name == "assets" else "outputs"
            group.add_command(
                EndpointCommand(
                    name, f"/api/v1/runs/{{ref}}/{path}", cls.page_params(), f"Read {name}.", "run_ref", fixed
                )
            )
        group.add_command(RunOutputCommand("result", cls.output_params(), cls.kinds[workload]))

    @classmethod
    def _add_feeds(cls, group: click.Group, workload: str) -> None:
        """Register kind-scoped finite and terminal feeds."""
        expected = cls.kinds[workload]
        cls._add_feed_commands(group, cls.feed_params(), expected)

    @classmethod
    def _add_feed_commands(
        cls,
        group: click.Group,
        params: list[click.Parameter],
        expected: str,
    ) -> None:
        """Register the snapshot/follow log feed and the durable event watcher."""
        group.add_command(RunLogsCommand(params, expected))
        group.add_command(RunWatchCommand([ParameterFactory.argument("run_ref")], expected))

    @classmethod
    def _add_mutations(cls, group: click.Group, workload: str) -> None:
        """Register kind-scoped cancellation and deletion."""
        fixed = {"expected_kind": cls.kinds[workload]}
        spec = MutationSpec(
            "/api/v1/runs/{ref}/cancel",
            query_names=("run_ref",),
            query_renames={"run_ref": "ref"},
            fixed_query=fixed,
        )
        group.add_command(
            PayloadCommand("cancel", spec, [ParameterFactory.argument("run_ref")], "Cancel an active run.")
        )
        group.add_command(
            DeleteEndpointCommand(
                "delete",
                "/api/v1/runs/{ref}",
                "resource_id",
                [ParameterFactory.argument("resource_id"), ParameterFactory.yes()],
                "Delete an eligible terminal run.",
                fixed,
            )
        )

    @staticmethod
    def list_filters() -> list[click.Parameter]:
        """Declare exact workload-run list filters."""
        states = [
            "pending",
            "preparing",
            "validating",
            "queued",
            "starting",
            "running",
            "finalizing",
            "completed",
            "completed_with_errors",
            "cancelling",
            "cancelled",
            "failed",
        ]
        return [
            ParameterFactory.limit(),
            ParameterFactory.text_option("cursor"),
            ParameterFactory.choice_option("state", states),
            ParameterFactory.text_option("app"),
            ParameterFactory.text_option("created_by"),
            ParameterFactory.all_projects(),
            ParameterFactory.choice_option("sort", ["created_at:asc", "created_at:desc"], "created_at:desc"),
        ]

    @staticmethod
    def page_params() -> list[click.Parameter]:
        """Declare one run selector plus bounded paging."""
        return [
            ParameterFactory.argument("run_ref"),
            ParameterFactory.limit(maximum=200),
            ParameterFactory.text_option("cursor"),
        ]

    @staticmethod
    def feed_params() -> list[click.Parameter]:
        """Declare one kind-scoped run feed."""
        feed = [ParameterFactory.argument("run_ref"), ParameterFactory.limit(), ParameterFactory.text_option("cursor")]
        return [*feed, click.Option(["--follow"], is_flag=True)]

    @staticmethod
    def output_params() -> list[click.Parameter]:
        """Declare the exact Run whose validated authored result is requested."""
        return [ParameterFactory.argument("run_ref")]
