import os
from typing import Union

from .contract import GableContract
from .data_asset import GableDataAsset


class GableClient:
    def __init__(
        self, api_endpoint: Union[str, None] = None, api_key: Union[str, None] = None
    ) -> None:
        if api_endpoint is None:
            self.api_endpoint = os.getenv("GABLE_API_ENDPOINT", "")
        else:
            self.api_endpoint = api_endpoint
        if api_key is None:
            self.api_key = os.getenv("GABLE_API_KEY", "")
        else:
            self.api_key = api_key
        self.contracts = GableContract(api_endpoint, api_key)
        self.data_assets = GableDataAsset(api_endpoint, api_key)
