import click
from gable.api.client import GableAPIClient
from gable.cli.helpers.emoji import EMOJI
from gable.openapi import ErrorResponse
from loguru import logger


@click.command(
    name="show",
    epilog="""Example:
                    
gable data-asset show "postgres://sample.host:5432:db.public.table"
""",
)
@click.pass_context
@click.argument(
    "data_asset_resource_name",
    nargs=1,
)
def show_data_asset(
    ctx: click.Context,
    data_asset_resource_name: str,
) -> None:
    """Shows the details of the requested data asset."""
    client: GableAPIClient = ctx.obj.client
    asset_or_error = client.get_data_asset(data_asset_resource_name)
    if isinstance(asset_or_error, ErrorResponse):
        raise click.ClickException(
            f"{EMOJI.RED_X.value} Failed to get data asset: {asset_or_error.title}: {asset_or_error.message}"
        )
    asset = asset_or_error
    logger.info(
        asset.json(
            indent=2,
            exclude_none=True,
            sort_keys=True,
            exclude={"versionDetail": {"rawSchema"}},
        )
    )
