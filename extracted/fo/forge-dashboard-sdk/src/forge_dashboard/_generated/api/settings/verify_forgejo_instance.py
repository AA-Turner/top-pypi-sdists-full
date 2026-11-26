from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx2

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.forgejo_instance_check import ForgejoInstanceCheck
from ...models.verify_forgejo_instance_request import VerifyForgejoInstanceRequest
from typing import cast



def _get_kwargs(
    *,
    body: VerifyForgejoInstanceRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/setup/forgejo-instance",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Error | ForgejoInstanceCheck | None:
    if response.status_code == 200:
        response_200 = ForgejoInstanceCheck.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx2.Response) -> Response[Error | ForgejoInstanceCheck]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: VerifyForgejoInstanceRequest,

) -> Response[Error | ForgejoInstanceCheck]:
    """ Check that an address is a reachable Forgejo

     Asks `<instanceUrl>/api/v1/version`, which a Forgejo answers without a
    sign-in, with a short timeout. The same address rules as
    `POST /api/v1/connections/forgejo` apply. Stores nothing. Private and
    loopback addresses are allowed on purpose: a Forgejo on a home or office
    network is the normal case, so the address is not filtered.

    Args:
        body (VerifyForgejoInstanceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ForgejoInstanceCheck]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    body: VerifyForgejoInstanceRequest,

) -> Error | ForgejoInstanceCheck | None:
    """ Check that an address is a reachable Forgejo

     Asks `<instanceUrl>/api/v1/version`, which a Forgejo answers without a
    sign-in, with a short timeout. The same address rules as
    `POST /api/v1/connections/forgejo` apply. Stores nothing. Private and
    loopback addresses are allowed on purpose: a Forgejo on a home or office
    network is the normal case, so the address is not filtered.

    Args:
        body (VerifyForgejoInstanceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ForgejoInstanceCheck
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: VerifyForgejoInstanceRequest,

) -> Response[Error | ForgejoInstanceCheck]:
    """ Check that an address is a reachable Forgejo

     Asks `<instanceUrl>/api/v1/version`, which a Forgejo answers without a
    sign-in, with a short timeout. The same address rules as
    `POST /api/v1/connections/forgejo` apply. Stores nothing. Private and
    loopback addresses are allowed on purpose: a Forgejo on a home or office
    network is the normal case, so the address is not filtered.

    Args:
        body (VerifyForgejoInstanceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | ForgejoInstanceCheck]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    body: VerifyForgejoInstanceRequest,

) -> Error | ForgejoInstanceCheck | None:
    """ Check that an address is a reachable Forgejo

     Asks `<instanceUrl>/api/v1/version`, which a Forgejo answers without a
    sign-in, with a short timeout. The same address rules as
    `POST /api/v1/connections/forgejo` apply. Stores nothing. Private and
    loopback addresses are allowed on purpose: a Forgejo on a home or office
    network is the normal case, so the address is not filtered.

    Args:
        body (VerifyForgejoInstanceRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx2.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | ForgejoInstanceCheck
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
