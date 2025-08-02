import click
from qwak.feature_store.execution.execution_query import ExecutionQuery

from qwak_sdk.inner.tools.cli_tools import QwakCommand


@click.command(
    "execution-status",
    cls=QwakCommand,
    help="Retrieve the current status of an execution (backfill/batch job ingestion)",
)
@click.option(
    "--execution-id",
    type=str,
    required=True,
    help="The id of the execution to retrieve the status for.",
)
def execution_status(execution_id: str, **kwargs):
    print(ExecutionQuery.get_execution_status_message(execution_id=execution_id))
