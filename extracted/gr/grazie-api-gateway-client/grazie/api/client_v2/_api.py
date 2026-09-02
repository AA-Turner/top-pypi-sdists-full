from ._client import AsyncClient, Client


class BaseAPI:
    def __init__(self, client: Client):
        self.client = client


class BaseAsyncAPI:
    def __init__(self, client: AsyncClient):
        self.client = client
