from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.checklist_response import ChecklistResponse
from ...types import UNSET, Response, Unset


def _get_kwargs(
    uuid: UUID,
    *,
    include_all: Union[Unset, str] = UNSET,
    step: str,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["include_all"] = include_all

    params["step"] = step

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/proposal-proposals/{uuid}/step-checklist/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[Any, ChecklistResponse]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ChecklistResponse.from_dict(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = response.json()
        return response_400
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, ChecklistResponse]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    include_all: Union[Unset, str] = UNSET,
    step: str,
) -> Response[Union[Any, ChecklistResponse]]:
    """Get a workflow step's checklist with questions and answers.

    Args:
        uuid (UUID):
        include_all (Union[Unset, str]):
        step (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ChecklistResponse]]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        include_all=include_all,
        step=step,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    include_all: Union[Unset, str] = UNSET,
    step: str,
) -> Union[Any, ChecklistResponse]:
    """Get a workflow step's checklist with questions and answers.

    Args:
        uuid (UUID):
        include_all (Union[Unset, str]):
        step (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ChecklistResponse]
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        include_all=include_all,
        step=step,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    include_all: Union[Unset, str] = UNSET,
    step: str,
) -> Response[Union[Any, ChecklistResponse]]:
    """Get a workflow step's checklist with questions and answers.

    Args:
        uuid (UUID):
        include_all (Union[Unset, str]):
        step (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, ChecklistResponse]]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        include_all=include_all,
        step=step,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    include_all: Union[Unset, str] = UNSET,
    step: str,
) -> Union[Any, ChecklistResponse]:
    """Get a workflow step's checklist with questions and answers.

    Args:
        uuid (UUID):
        include_all (Union[Unset, str]):
        step (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, ChecklistResponse]
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            include_all=include_all,
            step=step,
        )
    ).parsed
