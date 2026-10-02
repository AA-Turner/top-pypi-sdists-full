from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.add_managed_project_note_request import AddManagedProjectNoteRequest
from ...models.managed_project import ManagedProject
from ...types import Response


def _get_kwargs(
    identifier: str,
    destination: str,
    *,
    body: AddManagedProjectNoteRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/openportal-managed-projects/{identifier}/{destination}/add-note/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> ManagedProject:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ManagedProject.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ManagedProject]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    identifier: str,
    destination: str,
    *,
    client: AuthenticatedClient,
    body: AddManagedProjectNoteRequest,
) -> Response[ManagedProject]:
    """Append a note to the managed project. Author and timestamp are set automatically.

    Args:
        identifier (str):
        destination (str):
        body (AddManagedProjectNoteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedProject]
    """

    kwargs = _get_kwargs(
        identifier=identifier,
        destination=destination,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    identifier: str,
    destination: str,
    *,
    client: AuthenticatedClient,
    body: AddManagedProjectNoteRequest,
) -> ManagedProject:
    """Append a note to the managed project. Author and timestamp are set automatically.

    Args:
        identifier (str):
        destination (str):
        body (AddManagedProjectNoteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedProject
    """

    return sync_detailed(
        identifier=identifier,
        destination=destination,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    identifier: str,
    destination: str,
    *,
    client: AuthenticatedClient,
    body: AddManagedProjectNoteRequest,
) -> Response[ManagedProject]:
    """Append a note to the managed project. Author and timestamp are set automatically.

    Args:
        identifier (str):
        destination (str):
        body (AddManagedProjectNoteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedProject]
    """

    kwargs = _get_kwargs(
        identifier=identifier,
        destination=destination,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    identifier: str,
    destination: str,
    *,
    client: AuthenticatedClient,
    body: AddManagedProjectNoteRequest,
) -> ManagedProject:
    """Append a note to the managed project. Author and timestamp are set automatically.

    Args:
        identifier (str):
        destination (str):
        body (AddManagedProjectNoteRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedProject
    """

    return (
        await asyncio_detailed(
            identifier=identifier,
            destination=destination,
            client=client,
            body=body,
        )
    ).parsed
