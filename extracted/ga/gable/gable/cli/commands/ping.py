import click
from click.core import Context as ClickContext
from gable.api.client import GableAPIClient
from gable.cli.options import global_options
from loguru import logger


@click.command()
@global_options()
@click.pass_context
def ping(ctx: ClickContext):
    """Pings the Gable API to check for connectivity"""
    client: GableAPIClient = ctx.obj.client
    try:
        response, success, status_code = client.get_ping()
    except Exception as e:
        raise click.ClickException(
            f"Unable to ping Gable API at {client.endpoint}: {str(e)}"
        )
    if not success:
        raise click.ClickException(f"Unable to ping Gable API at {client.endpoint}")
    logger.info(f"Successfully pinged Gable API at {client.endpoint}")
