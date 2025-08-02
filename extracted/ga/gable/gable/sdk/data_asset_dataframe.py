import pandas as pd
from gable.api.client import GableAPIClient
from gable.cli.helpers.data_asset import (
    darn_to_string,
    format_check_data_assets_text_output,
)
from gable.cli.helpers.data_asset_dataframe import resolve_dataframe_data_asset
from gable.cli.helpers.data_asset_s3.logger import log_error
from gable.openapi import (
    DataAssetsCheckComplianceRequest,
    ErrorResponse,
    RegisterDataAssetsRequest,
    ResponseType,
)
from loguru import logger


class GableDataFrameDataAsset:
    def __init__(self, api_client: GableAPIClient) -> None:
        self.api_client = api_client

    def register(
        self,
        data_source: str,
        path: str,
        dataframe: pd.DataFrame,
        skip_profiling: bool = False,
    ):
        resolved_data_asset = resolve_dataframe_data_asset(
            data_source, path, dataframe, skip_profiling
        )
        response = self.api_client.post_register_data_assets(
            RegisterDataAssetsRequest(assets=[resolved_data_asset])
        )

        if isinstance(response, ErrorResponse):
            raise Exception(f"Error registering data asset: {response.message}")
        for outcome in response.asset_registration_outcomes:
            if outcome.error:
                log_error(
                    f"Error registering data asset {darn_to_string(outcome.data_asset_resource_name)}: {outcome.error}"
                )
            else:
                logger.info(
                    f"Data asset {darn_to_string(outcome.data_asset_resource_name)} registered successfully"
                )

    def check(self, data_source: str, path: str, dataframe: pd.DataFrame):
        resolved_data_asset = resolve_dataframe_data_asset(data_source, path, dataframe)

        response = self.api_client.post_data_assets_check_compliance(
            DataAssetsCheckComplianceRequest(
                assets=[resolved_data_asset], responseType=ResponseType.DETAILED
            )
        )
        if isinstance(response, ErrorResponse):
            raise Exception(f"Error checking data assets: {response.message}")
        if not isinstance(response, list):
            raise Exception(f"Unexpected response type: {type(response)}")
        output_string = format_check_data_assets_text_output(response)
        logger.info(output_string)
