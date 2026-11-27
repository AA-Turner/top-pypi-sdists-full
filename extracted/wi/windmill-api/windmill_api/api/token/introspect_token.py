from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.introspect_token_response_200 import IntrospectTokenResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    workspace: Union[Unset, None, str] = UNSET,
    path: Union[Unset, None, str] = UNSET,
    method: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["workspace"] = workspace

    params["path"] = path

    params["method"] = method

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/tokens/introspect",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[IntrospectTokenResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = IntrospectTokenResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[IntrospectTokenResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    workspace: Union[Unset, None, str] = UNSET,
    path: Union[Unset, None, str] = UNSET,
    method: Union[Unset, None, str] = UNSET,
) -> Response[IntrospectTokenResponse200]:
    """describe the token presenting the request

     Reports what the bearer credential of this request is: its row (label, expiry, bound
    workspace, scopes, carried admin rights), the identity it acts as in `workspace`, and
    whether the route layer would admit it on `method` `path`. Only the presented token is
    ever described. Every token may call it, whatever its scopes.

    Args:
        workspace (Union[Unset, None, str]):
        path (Union[Unset, None, str]):
        method (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[IntrospectTokenResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
        method=method,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Union[AuthenticatedClient, Client],
    workspace: Union[Unset, None, str] = UNSET,
    path: Union[Unset, None, str] = UNSET,
    method: Union[Unset, None, str] = UNSET,
) -> Optional[IntrospectTokenResponse200]:
    """describe the token presenting the request

     Reports what the bearer credential of this request is: its row (label, expiry, bound
    workspace, scopes, carried admin rights), the identity it acts as in `workspace`, and
    whether the route layer would admit it on `method` `path`. Only the presented token is
    ever described. Every token may call it, whatever its scopes.

    Args:
        workspace (Union[Unset, None, str]):
        path (Union[Unset, None, str]):
        method (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        IntrospectTokenResponse200
    """

    return sync_detailed(
        client=client,
        workspace=workspace,
        path=path,
        method=method,
    ).parsed


async def asyncio_detailed(
    *,
    client: Union[AuthenticatedClient, Client],
    workspace: Union[Unset, None, str] = UNSET,
    path: Union[Unset, None, str] = UNSET,
    method: Union[Unset, None, str] = UNSET,
) -> Response[IntrospectTokenResponse200]:
    """describe the token presenting the request

     Reports what the bearer credential of this request is: its row (label, expiry, bound
    workspace, scopes, carried admin rights), the identity it acts as in `workspace`, and
    whether the route layer would admit it on `method` `path`. Only the presented token is
    ever described. Every token may call it, whatever its scopes.

    Args:
        workspace (Union[Unset, None, str]):
        path (Union[Unset, None, str]):
        method (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[IntrospectTokenResponse200]
    """

    kwargs = _get_kwargs(
        workspace=workspace,
        path=path,
        method=method,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Union[AuthenticatedClient, Client],
    workspace: Union[Unset, None, str] = UNSET,
    path: Union[Unset, None, str] = UNSET,
    method: Union[Unset, None, str] = UNSET,
) -> Optional[IntrospectTokenResponse200]:
    """describe the token presenting the request

     Reports what the bearer credential of this request is: its row (label, expiry, bound
    workspace, scopes, carried admin rights), the identity it acts as in `workspace`, and
    whether the route layer would admit it on `method` `path`. Only the presented token is
    ever described. Every token may call it, whatever its scopes.

    Args:
        workspace (Union[Unset, None, str]):
        path (Union[Unset, None, str]):
        method (Union[Unset, None, str]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        IntrospectTokenResponse200
    """

    return (
        await asyncio_detailed(
            client=client,
            workspace=workspace,
            path=path,
            method=method,
        )
    ).parsed
