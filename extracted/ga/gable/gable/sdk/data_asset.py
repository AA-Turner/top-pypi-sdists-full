from typing import List, Union

from gable.api.client import GableAPIClient
from gable.openapi import ErrorResponse


class GableDataAsset:
    def __init__(self, api_endpoint, api_key) -> None:
        self.api_client = GableAPIClient(api_endpoint, api_key)
        self._dataframe = None

    def get_full_darns(self, partial_darn: str) -> Union[List[str], ErrorResponse]:
        return self.api_client.get_full_darns(partial_darn)

    @property
    def dataframe(self):
        if self._dataframe is None:
            from gable.sdk.data_asset_dataframe import GableDataFrameDataAsset

            self._dataframe = GableDataFrameDataAsset(self.api_client)
        return self._dataframe
