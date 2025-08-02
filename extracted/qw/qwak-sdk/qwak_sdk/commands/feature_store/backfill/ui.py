from datetime import datetime
from typing import Optional

import click
from qwak.feature_store.execution.backfill import Backfill

from qwak_sdk.commands.feature_store.backfill._logic import _BackfillLogic
from qwak_sdk.inner.tools.cli_tools import QwakCommand, ask_yesno
from qwak_sdk.tools.colors import Color


@click.command(
    "backfill", cls=QwakCommand, help="Trigger a backfill process for a Feature Set"
)
@click.option(
    "--feature-set",
    "--name",
    help="Feature Set name to perform the backfill process for",
    required=True,
    type=click.STRING,
)
@click.option(
    "--reset-backfill",
    "--reset",
    is_flag=True,
    metavar="FLAG",
    default=False,
    help="Perform a complete reset of the featuresets data. "
    "This will result in the deletion of the current existing data.",
)
@click.option(
    "--start-time",
    type=click.DateTime(),
    default=None,
    required=False,
    help="The time from which the featuresets data should be backfilled in UTC. "
    "Defaults to the featuresets configured backfill start time.",
)
@click.option(
    "--stop-time",
    type=click.DateTime(),
    default=None,
    required=False,
    help="The time up until the featuresets data should be backfilled in UTC. Defaults to the current timestamp. "
    "If the time provided is in the future, stop time will be rounded down to the current time. ",
)
@click.option(
    "--cluster-template",
    type=str,
    default=None,
    required=False,
    help="Backfill resource configuration, expects a ClusterType size. "
    "Defaults to the featureset resource configuration",
)
@click.option(
    "--comment",
    type=str,
    default=None,
    required=False,
    help="Backfill job optional comment tag line",
)
def backfill(
    feature_set: str,
    reset_backfill: bool,
    start_time: Optional[datetime],
    stop_time: Optional[datetime],
    cluster_template: Optional[str],
    comment: Optional[str],
    **kwargs,
):
    backill_logic = _BackfillLogic()
    if not backill_logic.is_valid_input(
        reset_backfill=reset_backfill,
        start_time=start_time,
        stop_time=stop_time,
        featureset_name=feature_set,
    ):
        return

    if reset_backfill:
        backfill_execution = _configure_backfill_triggered(
            featureset_name=feature_set,
            comment=comment,
            cluster_template=cluster_template,
        )
    else:
        start, stop = backill_logic.get_start_stop_times(
            requested_start_time=start_time, requested_stop_time=stop_time
        )
        if start >= stop:
            print(
                f"{Color.RED} Stop time {stop.isoformat()} must be after start time {start.isoformat()}"
            )
            return

        backfill_execution = backill_logic.configure_window_backfill(
            featureset_name=feature_set,
            start_time=start,
            stop_time=stop,
            comment=comment,
            cluster_template=cluster_template,
        )

    if backfill_execution:
        execution_id: str = backfill_execution.trigger_batch_backfill()
        print(
            f"{Color.BLUE}✅  Triggered backfill execution for featureset {feature_set}, "
            f"execution id for follow up on is {execution_id}."
        )
        print(
            f"To inquire the status of the execution run "
            f"'qwak features execution-status --execution-id {execution_id}'"
        )


def _configure_backfill_triggered(
    featureset_name: str, comment: str, cluster_template: str
) -> Optional[Backfill]:
    if ask_yesno(
        f"You are about to remove and re-populate all data in {featureset_name}",
        force=False,
    ):
        print(f"{Color.RED} - A backfill reset was triggered")
        return Backfill(
            featureset_name=featureset_name,
            comment=comment,
            cluster_template=cluster_template,
        )
    return None
