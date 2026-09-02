from http import HTTPStatus
from typing import Any, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.commit_sandbox import CommitSandbox
from ...models.template import Template
from ...models.error import Error
from ...types import UNSET, Response, Unset


def _get_kwargs(
    sandbox_id: str,
    *,
    body: Union[CommitSandbox, Unset] = UNSET,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/sandboxes/{sandbox_id}/commit",
    }

    if not isinstance(body, Unset):
        _kwargs["json"] = body.to_dict()
        headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Template, Error]]:
    if response.status_code == 201:
        response_201 = Template.from_dict(response.json())

        return response_201
    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())

        return response_401
    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())

        return response_404
    if response.status_code == 409:
        response_409 = Error.from_dict(response.json())

        return response_409
    if response.status_code == 500:
        response_500 = Error.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Template, Error]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    sandbox_id: str,
    *,
    client: AuthenticatedClient,
    body: Union[CommitSandbox, Unset] = UNSET,
) -> Response[Union[Template, Error]]:
    """Commit the sandbox to create a template snapshot

    Args:
        sandbox_id (str):
        body (Union[CommitSandbox, Unset]): Optional commit parameters

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Template, Error]]
    """

    kwargs = _get_kwargs(
        sandbox_id=sandbox_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    sandbox_id: str,
    *,
    client: AuthenticatedClient,
    body: Union[CommitSandbox, Unset] = UNSET,
) -> Optional[Union[Template, Error]]:
    """Commit the sandbox to create a template snapshot

    Args:
        sandbox_id (str):
        body (Union[CommitSandbox, Unset]): Optional commit parameters

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Template, Error]
    """

    return sync_detailed(
        sandbox_id=sandbox_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    sandbox_id: str,
    *,
    client: AuthenticatedClient,
    body: Union[CommitSandbox, Unset] = UNSET,
) -> Response[Union[Template, Error]]:
    """Commit the sandbox to create a template snapshot

    Args:
        sandbox_id (str):
        body (Union[CommitSandbox, Unset]): Optional commit parameters

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Template, Error]]
    """

    kwargs = _get_kwargs(
        sandbox_id=sandbox_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    sandbox_id: str,
    *,
    client: AuthenticatedClient,
    body: Union[CommitSandbox, Unset] = UNSET,
) -> Optional[Union[Template, Error]]:
    """Commit the sandbox to create a template snapshot

    Args:
        sandbox_id (str):
        body (Union[CommitSandbox, Unset]): Optional commit parameters

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Template, Error]
    """

    return (
        await asyncio_detailed(
            sandbox_id=sandbox_id,
            client=client,
            body=body,
        )
    ).parsed
