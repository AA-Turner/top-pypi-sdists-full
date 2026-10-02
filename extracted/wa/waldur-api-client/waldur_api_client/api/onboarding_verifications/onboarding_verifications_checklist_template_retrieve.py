from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.checklist_template import ChecklistTemplate
from ...types import UNSET, Response


def _get_kwargs(
    *,
    parent_uuid: UUID,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_parent_uuid = str(parent_uuid)
    params["parent_uuid"] = json_parent_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/onboarding-verifications/checklist-template/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Any, ChecklistTemplate]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ChecklistTemplate.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = response.json()
        return response_400
    if response.status_code == 404:
        response_404 = response.json()
        return response_404
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, ChecklistTemplate]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    parent_uuid: UUID,
) -> Response[Union[Any, ChecklistTemplate]]:
    """Get checklist template for creating new objects.

    Args:
        parent_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ChecklistTemplate]]
    """

    kwargs = _get_kwargs(
        parent_uuid=parent_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    parent_uuid: UUID,
) -> Union[Any, ChecklistTemplate]:
    """Get checklist template for creating new objects.

    Args:
        parent_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ChecklistTemplate]
    """

    return sync_detailed(
        client=client,
        parent_uuid=parent_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    parent_uuid: UUID,
) -> Response[Union[Any, ChecklistTemplate]]:
    """Get checklist template for creating new objects.

    Args:
        parent_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ChecklistTemplate]]
    """

    kwargs = _get_kwargs(
        parent_uuid=parent_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    parent_uuid: UUID,
) -> Union[Any, ChecklistTemplate]:
    """Get checklist template for creating new objects.

    Args:
        parent_uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ChecklistTemplate]
    """

    return (
        await asyncio_detailed(
            client=client,
            parent_uuid=parent_uuid,
        )
    ).parsed
