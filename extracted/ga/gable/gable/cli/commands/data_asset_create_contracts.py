import base64
import json
import os
import re
from typing import List, Optional

import click
import yaml
from click.core import Context as ClickContext
from gable.api.client import GableAPIClient
from gable.cli.helpers.emoji import EMOJI
from loguru import logger


@click.command(
    name="create-contract",
    epilog="""Example:
                    
gable data-asset create-contract postgres://sample.host:5432:db.public.table --output-dir contracts

gable data-asset create-contract --data-asset-id-pattern "postgres://*" --output-dir contracts""",
)
@click.pass_context
@click.argument(
    "data_asset_ids",
    nargs=-1,
    type=str,
)
@click.option(
    "--data-asset-id-pattern",
    type=str,
    help="Regex pattern to match data asset IDs. Contracts will be created for all data asset IDs that match this pattern.",
)
@click.option(
    "--output-dir",
    type=click.Path(
        exists=False,
        file_okay=False,
        dir_okay=True,
    ),
    help="Directory to output contracts. This directory must exist",
)
def create_data_asset_contracts(
    ctx: ClickContext,
    data_asset_ids: List[str],
    output_dir: Optional[str],
    data_asset_id_pattern: Optional[str],
) -> None:
    """Creates the YAML contract specification for a list of data assets. If a regex
    pattern (`--data-asset-id-pattern`) is provided, the command will create contracts
    for all data assets that match the pattern as well as the data assets provided in.

    The specification that is produced is based off the registered data asset but the
    user will need to fill in places marked with 'PLACEHOLDER:' such as field
    descriptions and ownership information.
    """
    LOG_OUTPUT_ASSET_LIMIT = 1  # Only print the contracts if the assets are <= number

    data_asset_ids_list = list(data_asset_ids)
    client: GableAPIClient = ctx.obj.client

    if data_asset_id_pattern:
        # Get all data assets that match the pattern
        response, success, status_code = client.get_data_assets()
        if not success:
            raise click.ClickException(
                f"{EMOJI.RED_X.value} Failed to get data assets by pattern: {data_asset_id_pattern} ({status_code})"
            )
        if isinstance(response, dict):
            data_assets = response.get(
                "data", []
            )  # assets inside object when paginated request
        else:
            data_assets = response
        for data_asset in data_assets:
            data_asset_id = data_asset.get("dataAssetResourceName")
            if re.match(data_asset_id_pattern, data_asset_id):
                data_asset_ids_list.append(data_asset_id)

        if not data_asset_ids_list:
            raise click.ClickException(
                f"{EMOJI.RED_X.value} No data assets found matching pattern: {data_asset_id_pattern}"
            )

    num_assets = len(data_asset_ids_list)
    for data_asset_id in data_asset_ids_list:

        # Base64 encode the data asset ID
        encoded_resource_name = base64.b64encode(data_asset_id.encode("utf-8")).decode(
            "utf-8"
        )

        # Get the inferred contract for the data asset
        (
            response,
            success,
            status_code,
        ) = client.get_data_asset_infer_contract(encoded_resource_name)
        if not success:
            raise click.ClickException(
                f"{EMOJI.RED_X.value} Failed to generate contract for data asset: {data_asset_id} ({status_code}))"
            )

        # Get the raw contract spec and convert to yaml
        contract_spec_dict = json.loads(response["contractSpecRaw"])
        contract_spec_yaml = yaml.dump(
            contract_spec_dict, default_flow_style=False, sort_keys=False
        )

        if num_assets <= LOG_OUTPUT_ASSET_LIMIT:
            # Print out the data asset
            logger.info(contract_spec_yaml)

        if output_dir:
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            # Get the contract name for the filename
            name = response["contractSpec"]["name"].lower().replace(".", "_")
            filepath = os.path.join(output_dir, f"{name}.yaml")

            # Write the contract spec to a file
            with open(filepath, "w") as f:
                f.write(contract_spec_yaml)
            if num_assets > LOG_OUTPUT_ASSET_LIMIT:
                logger.info(
                    f"Created contract file for data asset: {data_asset_id} at {filepath}"
                )

    if num_assets > LOG_OUTPUT_ASSET_LIMIT and not output_dir:
        logger.info(
            f"Too many assets for logging output. Please run again with an output directory."
        )
