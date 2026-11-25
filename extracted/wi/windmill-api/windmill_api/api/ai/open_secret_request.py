from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.open_secret_request_json_body import OpenSecretRequestJsonBody
from ...models.open_secret_request_response_200 import OpenSecretRequestResponse200
from ...types import Response


def _get_kwargs(
    workspace: str,
    *,
    json_body: OpenSecretRequestJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/w/{workspace}/ai_session_tools/secret_request/open".format(
            workspace=workspace,
        ),
        "json": json_json_body,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[OpenSecretRequestResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = OpenSecretRequestResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[OpenSecretRequestResponse200]:
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
    json_body: OpenSecretRequestJsonBody,
) -> Response[OpenSecretRequestResponse200]:
    """read the secret request a request_secret link carries

     The page an MCP client's request_secret link opens reads the card to draw from the link's signed
    token. Refused when the token is invalid, expired, or made for another user or workspace.

    Args:
        workspace (str):
        json_body (OpenSecretRequestJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OpenSecretRequestResponse200]
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
    json_body: OpenSecretRequestJsonBody,
) -> Optional[OpenSecretRequestResponse200]:
    """read the secret request a request_secret link carries

     The page an MCP client's request_secret link opens reads the card to draw from the link's signed
    token. Refused when the token is invalid, expired, or made for another user or workspace.

    Args:
        workspace (str):
        json_body (OpenSecretRequestJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OpenSecretRequestResponse200
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
    json_body: OpenSecretRequestJsonBody,
) -> Response[OpenSecretRequestResponse200]:
    """read the secret request a request_secret link carries

     The page an MCP client's request_secret link opens reads the card to draw from the link's signed
    token. Refused when the token is invalid, expired, or made for another user or workspace.

    Args:
        workspace (str):
        json_body (OpenSecretRequestJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OpenSecretRequestResponse200]
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
    json_body: OpenSecretRequestJsonBody,
) -> Optional[OpenSecretRequestResponse200]:
    """read the secret request a request_secret link carries

     The page an MCP client's request_secret link opens reads the card to draw from the link's signed
    token. Refused when the token is invalid, expired, or made for another user or workspace.

    Args:
        workspace (str):
        json_body (OpenSecretRequestJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OpenSecretRequestResponse200
    """

    return (
        await asyncio_detailed(
            workspace=workspace,
            client=client,
            json_body=json_body,
        )
    ).parsed
