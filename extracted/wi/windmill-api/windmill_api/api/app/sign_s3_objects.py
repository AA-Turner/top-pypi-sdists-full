from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.sign_s3_objects_json_body import SignS3ObjectsJsonBody
from ...models.sign_s3_objects_response_200_item import SignS3ObjectsResponse200Item
from ...types import Response


def _get_kwargs(
    workspace: str,
    *,
    json_body: SignS3ObjectsJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/apps/sign_s3_objects".format(
            workspace=workspace,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[List["SignS3ObjectsResponse200Item"]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = SignS3ObjectsResponse200Item.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[List["SignS3ObjectsResponse200Item"]]:
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
    json_body: SignS3ObjectsJsonBody,
) -> Response[List["SignS3ObjectsResponse200Item"]]:
    """sign s3 objects, to be used by anonymous users in public apps

    Args:
        workspace (str):
        json_body (SignS3ObjectsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['SignS3ObjectsResponse200Item']]
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
    json_body: SignS3ObjectsJsonBody,
) -> Optional[List["SignS3ObjectsResponse200Item"]]:
    """sign s3 objects, to be used by anonymous users in public apps

    Args:
        workspace (str):
        json_body (SignS3ObjectsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['SignS3ObjectsResponse200Item']
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
    json_body: SignS3ObjectsJsonBody,
) -> Response[List["SignS3ObjectsResponse200Item"]]:
    """sign s3 objects, to be used by anonymous users in public apps

    Args:
        workspace (str):
        json_body (SignS3ObjectsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[List['SignS3ObjectsResponse200Item']]
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
    json_body: SignS3ObjectsJsonBody,
) -> Optional[List["SignS3ObjectsResponse200Item"]]:
    """sign s3 objects, to be used by anonymous users in public apps

    Args:
        workspace (str):
        json_body (SignS3ObjectsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        List['SignS3ObjectsResponse200Item']
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            json_body=json_body,
        )
    ).parsed
