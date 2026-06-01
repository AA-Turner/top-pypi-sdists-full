import json
from typing import Optional, Union

import httpx

from . import types
from ._client import AsyncClient, Client
from ._version import __version__
from .tasks.api import AsyncTasksAPI, TasksAPI

AGENT = json.dumps(dict(name="api-gateway-python-client", version=__version__))


class APIGatewayClient:
    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        auth_type: types.AuthType = types.AuthType.USER,
        endpoint: Union[str, types.GatewayEndpoint] = types.GatewayEndpoint.PRODUCTION,
        http_client: Optional[httpx.Client] = None,
    ):
        """Construct a new synchronous JetBrains AI api gateway client instance. It's a facade that combines all the APIs clients.

        It automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` and `auth_type` from `GRAZIE_JWT_TOKEN`, `GRAZIE_USER_JWT_TOKEN`, `GRAZIE_SERVICE_JWT_TOKEN` or `GRAZIE_APPLICATION_JWT_TOKEN`
        """
        self.client = Client(
            api_key=api_key,
            auth_type=auth_type,
            endpoint=endpoint,
            http_client=http_client,
            headers={
                "Grazie-Agent": AGENT,
            },
        )
        self.tasks = TasksAPI(self.client)


class AsyncAPIGatewayClient:
    def __init__(
        self,
        *,
        api_key: Optional[str] = None,
        auth_type: types.AuthType = types.AuthType.USER,
        endpoint: Union[str, types.GatewayEndpoint] = types.GatewayEndpoint.PRODUCTION,
        http_client: Optional[httpx.AsyncClient] = None,
    ):
        """Construct a new asynchronous JetBrains AI api gateway client instance. It's a facade that combines all the APIs clients.

        It automatically infers the following arguments from their corresponding environment variables if they are not provided:
        - `api_key` and `auth_type` from `GRAZIE_JWT_TOKEN`, `GRAZIE_USER_JWT_TOKEN`, `GRAZIE_SERVICE_JWT_TOKEN` or `GRAZIE_APPLICATION_JWT_TOKEN`
        """
        self.client = AsyncClient(
            api_key=api_key,
            auth_type=auth_type,
            endpoint=endpoint,
            http_client=http_client,
            headers={
                types.GrazieHeaders.AGENT: AGENT,
            },
        )
        self.tasks = AsyncTasksAPI(self.client)
