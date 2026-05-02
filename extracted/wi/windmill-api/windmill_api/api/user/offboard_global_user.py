from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.offboard_global_user_json_body import OffboardGlobalUserJsonBody
from ...models.offboard_global_user_response_200 import OffboardGlobalUserResponse200
from ...types import Response


def _get_kwargs(
    email: str,
    *,
    json_body: OffboardGlobalUserJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/users/offboard/{email}".format(
            email=email,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[OffboardGlobalUserResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = OffboardGlobalUserResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[OffboardGlobalUserResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    email: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: OffboardGlobalUserJsonBody,
) -> Response[OffboardGlobalUserResponse200]:
    """offboard a user globally (reassign objects across workspaces, optionally delete)

    Args:
        email (str):
        json_body (OffboardGlobalUserJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OffboardGlobalUserResponse200]
    """

    kwargs = _get_kwargs(
        email=email,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    email: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: OffboardGlobalUserJsonBody,
) -> Optional[OffboardGlobalUserResponse200]:
    """offboard a user globally (reassign objects across workspaces, optionally delete)

    Args:
        email (str):
        json_body (OffboardGlobalUserJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OffboardGlobalUserResponse200
    """

    return sync_detailed(
        email=email,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    email: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: OffboardGlobalUserJsonBody,
) -> Response[OffboardGlobalUserResponse200]:
    """offboard a user globally (reassign objects across workspaces, optionally delete)

    Args:
        email (str):
        json_body (OffboardGlobalUserJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OffboardGlobalUserResponse200]
    """

    kwargs = _get_kwargs(
        email=email,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    email: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: OffboardGlobalUserJsonBody,
) -> Optional[OffboardGlobalUserResponse200]:
    """offboard a user globally (reassign objects across workspaces, optionally delete)

    Args:
        email (str):
        json_body (OffboardGlobalUserJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OffboardGlobalUserResponse200
    """

    return (
        await asyncio_detailed(
            email=email,
            client=client,
            json_body=json_body,
        )
    ).parsed
