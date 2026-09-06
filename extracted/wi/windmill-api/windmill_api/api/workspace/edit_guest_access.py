from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.edit_guest_access_json_body import EditGuestAccessJsonBody
from ...types import Response


def _get_kwargs(
    workspace: str,
    *,
    json_body: EditGuestAccessJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/workspaces/edit_guest_access".format(
            workspace=workspace,
        ),
        "json": json_json_body,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
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
    json_body: EditGuestAccessJsonBody,
) -> Response[Any]:
    """enable or disable guest sessions for this workspace

     Guests are people the identity provider authenticates who have no Windmill account; the `guest` app
    execution mode admits them. Off by default. Re-read where a guest session is minted and at the auth
    door on every guest request, so turning it off takes effect immediately, for sessions already issued
    and for apps whose policy already says `guest`.

    Args:
        workspace (str):
        json_body (EditGuestAccessJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    workspace: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: EditGuestAccessJsonBody,
) -> Response[Any]:
    """enable or disable guest sessions for this workspace

     Guests are people the identity provider authenticates who have no Windmill account; the `guest` app
    execution mode admits them. Off by default. Re-read where a guest session is minted and at the auth
    door on every guest request, so turning it off takes effect immediately, for sessions already issued
    and for apps whose policy already says `guest`.

    Args:
        workspace (str):
        json_body (EditGuestAccessJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
