from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.get_app_embed_token_by_custom_path_response_200 import GetAppEmbedTokenByCustomPathResponse200
from ...types import UNSET, Response, Unset


def _get_kwargs(
    custom_path: str,
    *,
    sdk_consent: Union[Unset, None, bool] = UNSET,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["sdk_consent"] = sdk_consent

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/apps_u/embed_token_by_custom_path/{custom_path}".format(
            custom_path=custom_path,
        ),
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[GetAppEmbedTokenByCustomPathResponse200]:
    if response.status_code == HTTPStatus.OK:
        response_200 = GetAppEmbedTokenByCustomPathResponse200.from_dict(response.json())

        return response_200
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[GetAppEmbedTokenByCustomPathResponse200]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    custom_path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    sdk_consent: Union[Unset, None, bool] = UNSET,
) -> Response[GetAppEmbedTokenByCustomPathResponse200]:
    """get app embed token by custom path

    Args:
        custom_path (str):
        sdk_consent (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetAppEmbedTokenByCustomPathResponse200]
    """

    kwargs = _get_kwargs(
        custom_path=custom_path,
        sdk_consent=sdk_consent,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    custom_path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    sdk_consent: Union[Unset, None, bool] = UNSET,
) -> Optional[GetAppEmbedTokenByCustomPathResponse200]:
    """get app embed token by custom path

    Args:
        custom_path (str):
        sdk_consent (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetAppEmbedTokenByCustomPathResponse200
    """

    return sync_detailed(
        custom_path=custom_path,
        client=client,
        sdk_consent=sdk_consent,
    ).parsed


async def asyncio_detailed(
    custom_path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    sdk_consent: Union[Unset, None, bool] = UNSET,
) -> Response[GetAppEmbedTokenByCustomPathResponse200]:
    """get app embed token by custom path

    Args:
        custom_path (str):
        sdk_consent (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[GetAppEmbedTokenByCustomPathResponse200]
    """

    kwargs = _get_kwargs(
        custom_path=custom_path,
        sdk_consent=sdk_consent,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    custom_path: str,
    *,
    client: Union[AuthenticatedClient, Client],
    sdk_consent: Union[Unset, None, bool] = UNSET,
) -> Optional[GetAppEmbedTokenByCustomPathResponse200]:
    """get app embed token by custom path

    Args:
        custom_path (str):
        sdk_consent (Union[Unset, None, bool]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        GetAppEmbedTokenByCustomPathResponse200
    """

    return (
        await asyncio_detailed(
            custom_path=custom_path,
            client=client,
            sdk_consent=sdk_consent,
        )
    ).parsed
