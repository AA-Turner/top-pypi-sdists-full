"""Explicit failed-descendant preview, recovery acceptance and captured-cycle waiting."""

from typing import TYPE_CHECKING

import click

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.observation_deadline import ObservationDeadline
from labqoat.cli.strict_command import StrictCommand

if TYPE_CHECKING:
    from labqoat.json_document import JsonDocument
    from labqoat.management_client import ManagementClient


class RunWorkflowCommand(StrictCommand):
    """Preserve workflow intent and explicit child strategy while keeping dry runs read-only and paginated."""

    @classmethod
    def as_click_command(cls) -> click.Command:
        """Declare graph scope, bounded preview navigation and exact mutation identity."""
        return cls(
            "recover",
            help="Recover failed descendants and replay retained orchestration.",
            params=[
                click.Argument(["run_id"]),
                click.Option(["--failed-descendants"], is_flag=True, help="Recover the workflow's failed children."),
                click.Option(
                    ["--dry-run"], is_flag=True, help="Read one advisory child page without accepting recovery."
                ),
                click.Option(["--parent-id"], help="Explore this nested parent in a dry run."),
                click.Option(["--operation-id"], help="Read a page of an existing frozen recovery plan."),
                click.Option(["--limit"], type=click.IntRange(1, 200), default=50),
                click.Option(["--cursor"]),
                click.Option(["--expected-state-version"], type=click.IntRange(min=0)),
                click.Option(["--include-cancelled"], is_flag=True),
                click.Option(["--operation-key"]),
                click.Option(["--reason"], default=""),
                click.Option(["--wait"], is_flag=True),
                ObservationDeadline.option(),
            ],
        )

    def invoke(self, ctx: click.Context) -> object:
        """Return stable JSON for advisory pages or acceptance and preserve asynchronous failure receipts."""
        from labqoat.cli.output.error_reporter import ErrorReporter
        from labqoat.cli.output.result_writer import ResultWriter
        from labqoat.errors.recovery_failed_error import RecoveryFailedError

        self._require_scope(ctx)
        self._validate(ctx)
        client = ContextAccessor.current().management()
        try:
            ResultWriter().write_dict(self._execute(client, ctx))
        except RecoveryFailedError as error:
            ResultWriter().write_dict(error.operation.to_dict())
            ErrorReporter.report(error)
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
        return None

    @staticmethod
    def _require_scope(ctx: click.Context) -> None:
        """Name the single-run commands when the run is not a workflow being recovered child by child."""
        if not ctx.params["failed_descendants"]:
            raise click.UsageError(
                "lab run recover recovers a workflow's failed children: add --failed-descendants. For one run, "
                "lab run attempts resume RUN continues from its newest checkpoint and "
                "lab run attempts restart RUN starts it again."
            )

    @staticmethod
    def _validate(ctx: click.Context) -> None:
        """Reject mixed read and mutation controls rather than silently accepting a different action."""
        values = ctx.params
        if values["dry_run"] and values["operation_id"]:
            raise click.UsageError("--dry-run and --operation-id cannot be combined")
        if values["wait"] and (values["dry_run"] or values["operation_id"]):
            raise click.UsageError("--wait applies to a new recovery")
        if values["parent_id"] and not values["dry_run"]:
            raise click.UsageError("--parent-id requires --dry-run")
        if values["cursor"] and not (values["dry_run"] or values["operation_id"]):
            raise click.UsageError("--cursor requires --dry-run or --operation-id")

    @staticmethod
    def _execute(client: "ManagementClient", ctx: click.Context) -> "JsonDocument":
        """Read one bounded page or freeze the discovered version before submitting immutable workflow intent."""
        values = ctx.params
        run_id = str(values["run_id"])
        if values["operation_id"]:
            return client.runs.workflow_recovery.plan(
                run_id,
                values["operation_id"],
                limit=values["limit"],
                cursor=values["cursor"],
            ).to_dict()
        if values["dry_run"]:
            return client.runs.workflow_recovery.preview(
                run_id,
                parent_id=values["parent_id"],
                include_cancelled=values["include_cancelled"],
                limit=values["limit"],
                cursor=values["cursor"],
            ).to_dict()
        version = values["expected_state_version"]
        if version is None:
            version = client.runs.recovery(run_id).expected_state_version
        handle = client.runs.recover(
            run_id,
            expected_state_version=version,
            reason=values["reason"],
            include_cancelled=values["include_cancelled"],
            operation_key=values["operation_key"],
        )
        with ObservationDeadline.current(run_id).watching():
            return (handle.wait() if values["wait"] else handle.accepted).to_dict()
