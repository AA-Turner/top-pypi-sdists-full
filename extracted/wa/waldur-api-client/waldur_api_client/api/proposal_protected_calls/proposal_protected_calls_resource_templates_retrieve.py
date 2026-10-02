from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.call_resource_template import CallResourceTemplate
from ...types import Response


def _get_kwargs(
    uuid: str,
    obj_uuid: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/proposal-protected-calls/{uuid}/resource_templates/{obj_uuid}/",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> CallResourceTemplate:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = CallResourceTemplate.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[CallResourceTemplate]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: str,
    obj_uuid: str,
    *,
    client: AuthenticatedClient,
) -> Response[CallResourceTemplate]:
    """
    Args:
        uuid (str):
        obj_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CallResourceTemplate]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        obj_uuid=obj_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: str,
    obj_uuid: str,
    *,
    client: AuthenticatedClient,
) -> CallResourceTemplate:
    """
    Args:
        uuid (str):
        obj_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CallResourceTemplate
    """

    return sync_detailed(
        uuid=uuid,
        obj_uuid=obj_uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    uuid: str,
    obj_uuid: str,
    *,
    client: AuthenticatedClient,
) -> Response[CallResourceTemplate]:
    """
    Args:
        uuid (str):
        obj_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[CallResourceTemplate]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        obj_uuid=obj_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: str,
    obj_uuid: str,
    *,
    client: AuthenticatedClient,
) -> CallResourceTemplate:
    """
    Args:
        uuid (str):
        obj_uuid (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        CallResourceTemplate
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            obj_uuid=obj_uuid,
            client=client,
        )
    ).parsed
