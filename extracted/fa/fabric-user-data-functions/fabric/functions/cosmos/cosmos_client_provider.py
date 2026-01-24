# flake8: noqa: I003

from datetime import datetime, timezone, timedelta
import logging
from typing import Generator
from azure.cosmos import CosmosClient
from azure.core.credentials import TokenCredential
from fabric.functions.fabric_item import FabricItem
from fabric.functions.providers.base_fabricitem_provider import BaseFabricItemProvider


class CosmosClientProvider(BaseFabricItemProvider):

    def __init__(self):
        self._client_iters = {}

    def _cosmosclient_getter(self, cosmos_db_uri: str) -> Generator[CosmosClient, FabricItem, None]:
        cosmos_client: CosmosClient = None
        client_cred: TokenCredential = None
        refresh_after: datetime = None
        try:
            # pump
            item: FabricItem = yield

            while True:
                if refresh_after is not None and refresh_after >= datetime.now(timezone.utc) and cosmos_client is not None:
                    logging.info('Reusing existing CosmosClient')
                    pass
                else:
                    credential = item.get_access_token()
                    client_cred = credential
                    refresh_after = datetime.fromtimestamp(credential.get_token().expires_on, tz=timezone.utc) - timedelta(minutes=1)
                    logging.info('Creating new CosmosClient')
                    cosmos_client = CosmosClient(cosmos_db_uri, client_cred)
                item = yield cosmos_client
        except GeneratorExit as e:
            logging.debug(f'CosmosClient generator closed: {e}')
            pass

    def create_cosmosclient_getter(self, cosmos_db_uri: str) -> Generator[CosmosClient, FabricItem, None]:
        getter = self._cosmosclient_getter(cosmos_db_uri)
        next(getter)
        return getter

    def create(self, item: FabricItem, **kwargs):
        url = kwargs.get("cosmos_endpoint")

        if url not in self._client_iters:
            self._client_iters[url] = self.create_cosmosclient_getter(url)

        client_iter = self._client_iters[url]

        return client_iter.send(item)
