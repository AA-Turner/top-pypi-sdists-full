"""Explicit same-run recovery with optimistic version protection and optional cycle waiting."""

import click
from typing import TYPE_CHECKING

from labqoat.cli.context_accessor import ContextAccessor
from labqoat.cli.observation_deadline import ObservationDeadline
from labqoat.cli.strict_command import StrictCommand

if TYPE_CHECKING:
    from labqoat.management_client import ManagementClient
    from labqoat.runs.recovery_handle import RecoveryHandle


class RunRecoveryCommand(StrictCommand):
    """Return durable acceptance promptly or wait for its admitted execution cycle."""

    @classmethod
    def as_click_command(cls, mode: str) -> click.Command:
        """Declare explicit cancelled-work inclusion and a reusable mutation key."""
        return cls(
            mode,
            help=f"{mode.capitalize()} retained work under its existing Run ID and cumulative budget.",
            params=[
                click.Argument(["run_id"]),
                click.Option(["--expected-state-version"], type=click.IntRange(min=0)),
                click.Option(["--reason"], default=""),
                click.Option(["--include-cancelled"], is_flag=True),
                click.Option(["--operation-key"], type=str),
                click.Option(["--wait"], is_flag=True),
                ObservationDeadline.option(),
                *cls._shard_options(mode),
                *(
                    [
                        click.Option(
                            ["--checkpoint"], default="latest-durable", help="latest-durable or an exact checkpoint ID."
                        )
                    ]
                    if mode in ("resume", "finalize")
                    else []
                ),
            ],
        )

    def invoke(self, ctx: click.Context) -> object:
        """Freeze the observed version before acceptance and preserve failed operation identity in JSON output."""
        from labqoat.cli.output.error_reporter import ErrorReporter
        from labqoat.cli.output.result_writer import ResultWriter
        from labqoat.errors.recovery_failed_error import RecoveryFailedError

        client = ContextAccessor.current().management()
        values = ctx.params
        run_id = str(values["run_id"])
        try:
            version = values["expected_state_version"]
            if version is None:
                version = client.runs.recovery(run_id).expected_state_version
            handle = self._accept(client, ctx, version)
            with ObservationDeadline.current(run_id).watching():
                result = handle.wait() if values["wait"] else handle.accepted
            ResultWriter().write_dict(result.to_dict())
        except RecoveryFailedError as error:
            ResultWriter().write_dict(error.operation.to_dict())
            ErrorReporter.report(error)
        except Exception as error:
            ErrorReporter.report(error)
        finally:
            client.close()
        return None

    def _accept(self, client: "ManagementClient", ctx: click.Context, version: int) -> "RecoveryHandle":
        """Dispatch the explicit action without hidden mode selection or checkpoint fallback."""
        values = ctx.params
        if self.name in ("resume", "finalize"):
            action = client.runs.resume if self.name == "resume" else client.runs.finalize
            return action(
                str(values["run_id"]),
                expected_state_version=version,
                checkpoint=values["checkpoint"],
                reason=values["reason"],
                include_cancelled=values["include_cancelled"],
                operation_key=values["operation_key"],
            )
        restart = client.runs.restart_shards if values.get("failed_shards", False) else client.runs.restart
        return restart(
            str(values["run_id"]),
            expected_state_version=version,
            reason=values["reason"],
            include_cancelled=values["include_cancelled"],
            operation_key=values["operation_key"],
        )

    @staticmethod
    def _shard_options(mode: str) -> list[click.Parameter]:
        """Offer failed-only selection solely for explicit restart, never checkpoint resume."""
        if mode != "restart":
            return []
        return [click.Option(["--failed-shards"], is_flag=True, help="Restart only unsuccessful independent shards.")]
