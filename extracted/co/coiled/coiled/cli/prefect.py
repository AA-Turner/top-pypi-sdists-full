import click

from .cluster.crud import stop
from .prefect_serve import serve
from .utils import CONTEXT_SETTINGS


@click.group(context_settings=CONTEXT_SETTINGS)
@click.pass_context
def prefect(ctx):
    """Prefect interface"""


prefect.add_command(serve, "serve")
prefect.add_command(stop, "stop")
