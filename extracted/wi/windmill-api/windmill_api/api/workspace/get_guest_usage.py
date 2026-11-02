from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_guest_usage_response_200 import GetGuestUsageResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "get",
        "url": "/w/{workspace}/workspaces/guest_usage".format(
            workspace=workspace,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetGuestUsageResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetGuestUsageResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetGuestUsageResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[GetGuestUsageResponse200]:
    """the instance's standing against the guest allowance

     Instance-wide, since a licence is per instance and one email is one guest however many workspaces it
    opens. Read by workspace admins and app publishers to see how close the cap (Community and Pro) or
    the meter (Enterprise) is.

    Args:
        workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetGuestUsageResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[GetGuestUsageResponse200]:
    """the instance's standing against the guest allowance

     Instance-wide, since a licence is per instance and one email is one guest however many workspaces it
    opens. Read by workspace admins and app publishers to see how close the cap (Community and Pro) or
    the meter (Enterprise) is.

    Args:
        workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetGuestUsageResponse200
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[GetGuestUsageResponse200]:
    """the instance's standing against the guest allowance

     Instance-wide, since a licence is per instance and one email is one guest however many workspaces it
    opens. Read by workspace admins and app publishers to see how close the cap (Community and Pro) or
    the meter (Enterprise) is.

    Args:
        workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetGuestUsageResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[GetGuestUsageResponse200]:
    """the instance's standing against the guest allowance

     Instance-wide, since a licence is per instance and one email is one guest however many workspaces it
    opens. Read by workspace admins and app publishers to see how close the cap (Community and Pro) or
    the meter (Enterprise) is.

    Args:
        workspace (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetGuestUsageResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
        )
    ).parsed
