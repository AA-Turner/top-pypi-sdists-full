from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.exists_route_json_body import ExistsRouteJsonBody
from ...types import Response


def _get_kwargs(
    workspace: str,
    *,
    json_body: ExistsRouteJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/http_triggers/route_exists".format(
            workspace=workspace,
        ),
        "json": json_json_body,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[bool]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(bool, response.json())
        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[bool]:
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
    json_body: ExistsRouteJsonBody,
) -> Response[bool]:
    """does route exists

    Args:
        workspace (str):
        json_body (ExistsRouteJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[bool]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ExistsRouteJsonBody,
) -> Optional[bool]:
    """does route exists

    Args:
        workspace (str):
        json_body (ExistsRouteJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        bool
    """

    return sync_detailed(
        workspace=workspace,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ExistsRouteJsonBody,
) -> Response[bool]:
    """does route exists

    Args:
        workspace (str):
        json_body (ExistsRouteJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[bool]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: ExistsRouteJsonBody,
) -> Optional[bool]:
    """does route exists

    Args:
        workspace (str):
        json_body (ExistsRouteJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        bool
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            json_body=json_body,
        )
    ).parsed
