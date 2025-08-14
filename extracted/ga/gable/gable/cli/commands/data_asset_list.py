import json

import click
from click.core import Context as ClickContext
from loguru import logger
from rich.console import Console
from rich.table import Table

from gable.api.client import GableAPIClient
from gable.cli.options import global_options

console = Console()


@click.command(
    # Disable help, we re-add it in global_options()
    add_help_option=False,
    name="list",
)
@click.option(
    "-o",
    "--output",
    type=click.Choice(["table", "json"]),
    default="table",
    help="Format of the output. Options are: table (default) or json",
)
@click.option(
    "--full",
    is_flag=True,
    help="Return full data asset details including domain and path",
)
@global_options()
@click.pass_context
def list_data_assets(ctx: ClickContext, output: str, full: bool) -> None:
    """List all data assets"""
    # Get the data
    client: GableAPIClient = ctx.obj.client
    response, success, status_code = client.get_data_assets()
    if isinstance(response, dict):
        data_assets = response.get(
            "data", []
        )  # assets inside object when paginated request
    else:
        data_assets = response
    if not data_assets:
        raise click.ClickException("No data assets found.")

    # Format the output
    if output == "json":
        data_asset_list = []
        for data_asset in data_assets:
            domain: str = data_asset.get("domain")
            path: str = data_asset.get("path")
            resource_name: str = data_asset.get("dataAssetResourceName")
            type: str = data_asset.get("type")
            row = {"resourceName": f"{resource_name}"}
            if full:
                row["type"] = type
                row["dataSource"] = domain
                row["path"] = path
            data_asset_list.append(row)
        logger.info(json.dumps(data_asset_list))
    else:
        table = Table(show_header=True, title="Data Assets")
        table.add_column("resourceName")
        if full:
            table.add_column("type")
            table.add_column("dataSource")
            table.add_column("path")
        for data_asset in data_assets:
            domain: str = data_asset.get("domain")
            path: str = data_asset.get("path")
            resource_name: str = data_asset.get("dataAssetResourceName")
            type: str = data_asset.get("type")
            if not full:
                table.add_row(f"{resource_name}")
            else:
                table.add_row(
                    f"{resource_name}",
                    type,
                    domain,
                    path,
                )
        console.print(table)
