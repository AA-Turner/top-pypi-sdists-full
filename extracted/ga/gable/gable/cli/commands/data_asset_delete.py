import click
from click.core import Context as ClickContext
from gable.cli.client import GableAPIClient
from gable.openapi import ErrorResponse
from loguru import logger


@click.command(
    name="delete",
    epilog="""Example:
                    
gable data-asset delete postgres://sample.host:5432:db.public.table""",
)
@click.pass_context
@click.argument(
    "data_asset_resource_name",
    nargs=1,
)
def delete_data_asset(
    ctx: ClickContext,
    data_asset_resource_name: str,
) -> None:
    """Delete a data asset by its resource name."""
    client: GableAPIClient = ctx.obj.client
    response = client.delete_data_asset(data_asset_resource_name)
    if isinstance(response, ErrorResponse):
        raise click.ClickException(
            f"Error deleting data asset {data_asset_resource_name}: {response.title}: {response.message}"
        )
    logger.info(f"Data asset {data_asset_resource_name} deleted successfully.")
