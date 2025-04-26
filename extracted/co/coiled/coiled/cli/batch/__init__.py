import click

from ..utils import CONTEXT_SETTINGS
from .list import batch_list_cli
from .run import batch_run_cli
from .status import batch_status_cli
from .wait import batch_wait_cli


@click.group(name="batch", context_settings=CONTEXT_SETTINGS)
def batch_group():
    """
    Commands for managing Coiled Batch Jobs.

    Batch Jobs is currently an experimental feature.
    """


batch_group.add_command(batch_run_cli, "run")
batch_group.add_command(batch_status_cli, "status")
batch_group.add_command(batch_list_cli, "list")
batch_group.add_command(batch_wait_cli, "wait")
