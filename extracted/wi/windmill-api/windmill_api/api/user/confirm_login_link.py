from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.confirm_login_link_response_200 import ConfirmLoginLinkResponse200
from ...types import Response


def _get_kwargs(
    token: str,
) -> Dict[str, Any]:
    pass

    return {
        "method": "post",
        "url": "/auth/login_link/{token}".format(
            token=token,
        ),
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[ConfirmLoginLinkResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = ConfirmLoginLinkResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ConfirmLoginLinkResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    token: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ConfirmLoginLinkResponse200]:
    """consume a single-use login link from its confirmation page, set the session cookie and answer where
    to go

    Args:
        token (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConfirmLoginLinkResponse200]
    """

    kwargs = _get_kwargs(
        token=token,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    token: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ConfirmLoginLinkResponse200]:
    """consume a single-use login link from its confirmation page, set the session cookie and answer where
    to go

    Args:
        token (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConfirmLoginLinkResponse200
    """

    return sync_detailed(
        token=token,
        client=client,
    ).parsed


async def asyncio_detailed(
    token: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[ConfirmLoginLinkResponse200]:
    """consume a single-use login link from its confirmation page, set the session cookie and answer where
    to go

    Args:
        token (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConfirmLoginLinkResponse200]
    """

    kwargs = _get_kwargs(
        token=token,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    token: str,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[ConfirmLoginLinkResponse200]:
    """consume a single-use login link from its confirmation page, set the session cookie and answer where
    to go

    Args:
        token (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConfirmLoginLinkResponse200
    """

    return (
        await asyncio_detailed(
            token=token,
            client=client,
        )
    ).parsed
