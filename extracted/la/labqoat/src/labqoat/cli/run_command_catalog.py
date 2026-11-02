"""Canonical generic run command tree."""

from __future__ import annotations

import click

from labqoat.cli.delete_endpoint_command import DeleteEndpointCommand
from labqoat.cli.endpoint_command import EndpointCommand
from labqoat.cli.run_compare_command import RunCompareCommand
from labqoat.cli.run_status_command import RunStatusCommand
from labqoat.cli.run_wait_command import RunWaitCommand
from labqoat.cli.group_help import GroupHelp
from labqoat.cli.mutation_spec import MutationSpec
from labqoat.cli.parameter_factory import ParameterFactory
from labqoat.cli.payload_command import PayloadCommand
from labqoat.cli.run_logs_command import RunLogsCommand
from labqoat.cli.run_output_command import RunOutputCommand
from labqoat.cli.run_watch_command import RunWatchCommand
from labqoat.cli.commands.authored.run_group import RunGroup
from labqoat.cli.commands.run_attempts_group import RunAttemptsGroup
from labqoat.cli.commands.run_fork_command import RunForkCommand
from labqoat.cli.commands.run_tag_command import RunTagCommand
from labqoat.cli.commands.run_workflow_command import RunWorkflowCommand
from labqoat.cli.commands.run_budget_history_command import RunBudgetHistoryCommand
from labqoat.cli.commands.run_budget_adjustment_command import RunBudgetAdjustmentCommand


class RunCommandCatalog:
    """Assemble all strict generic run reads, streams, and mutations."""

    @staticmethod
    def group() -> click.Group:
        """Build the complete generic run group."""
        group = RunGroup(
            "run",
            help="Run FILE.py[::NAME] or inspect durable executions. Launch options precede FILE.py.",
            callback=GroupHelp.show,
            invoke_without_command=True,
            params=RunGroup.launch_options(),
        )
        RunCommandCatalog._add_reads(group)
        RunCommandCatalog._add_feeds(group)
        RunCommandCatalog._add_mutations(group)
        group.add_command(RunAttemptsGroup.as_click_command())
        group.add_command(RunForkCommand.as_click_command())
        group.add_command(RunTagCommand.as_click_command())
        group.add_command(RunWorkflowCommand.as_click_command())
        group.add_command(RunBudgetHistoryCommand.as_click_command())
        group.add_command(RunBudgetAdjustmentCommand.as_click_command())
        return group

    @staticmethod
    def _add_reads(group: click.Group) -> None:
        """Register generic run pages and item reads."""
        group.add_command(EndpointCommand("list", "/api/v1/runs", RunCommandCatalog.list_filters(), "List runs."))
        reference = [ParameterFactory.argument("run_ref")]
        group.add_command(
            EndpointCommand(
                "get",
                "/api/v1/runs/{ref}",
                reference,
                "Read the run record: state, arguments (references by ID), function, resources and identities.",
                "run_ref",
            )
        )
        group.add_command(RunStatusCommand(reference))
        group.add_command(RunWaitCommand())
        group.add_command(RunCompareCommand())
        for name, path in (
            ("placement", "{ref}/placement"),
            ("machine", "{ref}/machine"),
            ("lineage", "{ref}/lineage"),
            ("fit-budget", "{ref}/fit-budget"),
        ):
            group.add_command(EndpointCommand(name, f"/api/v1/runs/{path}", reference, f"Read run {name}.", "run_ref"))
        for name, path in RunCommandCatalog.page_paths().items():
            group.add_command(
                EndpointCommand(name, path, RunCommandCatalog.page_params(), f"Read run {name}.", "run_ref")
            )
        group.add_command(RunOutputCommand("output", RunCommandCatalog.output_params()))
        group.add_command(RunOutputCommand("result", RunCommandCatalog.output_params()))
        group.add_command(
            EndpointCommand(
                "fit-intervals",
                "/api/v1/runs/{ref}/fit-budget/intervals",
                [*reference, ParameterFactory.text_option("cursor")],
                "Read fifty original fit intervals.",
                "run_ref",
            )
        )

    @staticmethod
    def _add_feeds(group: click.Group) -> None:
        """Register run logs with explicit finite and followed modes."""
        group.add_command(RunLogsCommand(RunCommandCatalog.feed_params()))
        group.add_command(RunWatchCommand([ParameterFactory.argument("run_ref")]))

    @staticmethod
    def _add_mutations(group: click.Group) -> None:
        """Register run cancellation and deletion."""
        reference = ParameterFactory.argument("run_ref")
        spec = MutationSpec("/api/v1/runs/{ref}/cancel", query_names=("run_ref",), query_renames={"run_ref": "ref"})
        group.add_command(PayloadCommand("cancel", spec, [reference], "Cancel an active run."))
        group.add_command(
            DeleteEndpointCommand(
                "delete",
                "/api/v1/runs/{ref}",
                "resource_id",
                [ParameterFactory.argument("resource_id"), ParameterFactory.yes()],
                "Delete an eligible terminal run.",
            )
        )

    @staticmethod
    def list_filters() -> list[click.Parameter]:
        """Declare exact generic-run paging and filters."""
        states = [
            "pending",
            "running",
            "cancelling",
            "finalizing",
            "completed",
            "completed_with_errors",
            "cancelled",
            "failed",
        ]
        kinds = ["import", "maintenance", "training"]
        return [
            ParameterFactory.limit(),
            ParameterFactory.text_option("cursor"),
            ParameterFactory.choice_option("state", states),
            ParameterFactory.choice_option("kind", kinds),
            ParameterFactory.text_option("app"),
            ParameterFactory.text_option("created_by"),
            ParameterFactory.text_option("tags"),
            ParameterFactory.text_option("exclude_tags"),
            click.Option(["--owner"], type=str, help="List only the child runs this run started."),
            ParameterFactory.all_projects(),
            ParameterFactory.choice_option("sort", ["created_at:asc", "created_at:desc"], "created_at:desc"),
        ]

    @staticmethod
    def page_paths() -> dict[str, str]:
        """Map page command names to explicit server resources."""
        return {
            "assets": "/api/v1/runs/{ref}/produced-assets",
            "metrics": "/api/v1/runs/{ref}/metrics",
            "outputs": "/api/v1/runs/{ref}/outputs",
            "forks": "/api/v1/runs/{ref}/forks",
        }

    @staticmethod
    def page_params() -> list[click.Parameter]:
        """Declare one run selector plus bounded page controls."""
        return [
            ParameterFactory.argument("run_ref"),
            ParameterFactory.limit(maximum=200),
            ParameterFactory.text_option("cursor"),
        ]

    @staticmethod
    def feed_params() -> list[click.Parameter]:
        """Declare bounded feed controls and optional terminal following."""
        feed = [ParameterFactory.argument("run_ref"), ParameterFactory.limit(), ParameterFactory.text_option("cursor")]
        return [*feed, click.Option(["-f", "--follow"], is_flag=True)]

    @staticmethod
    def output_params() -> list[click.Parameter]:
        """Declare the exact Run whose validated authored result is requested."""
        return [ParameterFactory.argument("run_ref")]
