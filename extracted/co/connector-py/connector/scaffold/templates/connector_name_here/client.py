import typing as t

from connector.oai.base_clients import BaseIntegrationClient
from connector.oai.capability import Request, get_oauth
from connector.utils.httpx_auth import BearerAuth
from connector.utils.client_utils import create_client_response

from {name}.constants import BASE_URL


class {pascal}Client(BaseIntegrationClient):
    @classmethod
    def prepare_client_args(cls, args: Request) -> dict[str, t.Any]:
        return {{
            "auth": BearerAuth(token=get_oauth(args).access_token),
            "base_url": BASE_URL,
        }}

    # example of a method that fetches users
    # async def get_users(self, limit: int | None = None, offset: int | None = None) -> UsersResponse:
    #     params = {{}}
    #     if limit:
    #         params["limit"] = limit
    #     if offset:
    #         params["offset"] = offset
    #     response = await self._http_client.get({pascal}Endpoint.REST_USERS, params=params)
    #     return create_client_response(response, UsersResponse)
