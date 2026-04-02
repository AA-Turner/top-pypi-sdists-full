from http import HTTPStatus
from typing import Any, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.feature_values_body import FeatureValuesBody
from ...types import Response


def _get_kwargs(
    *,
    body: FeatureValuesBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/feature-values/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> str:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = cast(str, response.json())
        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: FeatureValuesBody,
) -> Response[str]:
    """Update feature flags

     Allows administrators to enable or disable specific feature flags in the system. The request should
    be a dictionary where keys are feature sections and values are dictionaries of feature keys and
    their boolean state.

    Args:
        body (FeatureValuesBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[str]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: FeatureValuesBody,
) -> str:
    """Update feature flags

     Allows administrators to enable or disable specific feature flags in the system. The request should
    be a dictionary where keys are feature sections and values are dictionaries of feature keys and
    their boolean state.

    Args:
        body (FeatureValuesBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        str
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: FeatureValuesBody,
) -> Response[str]:
    """Update feature flags

     Allows administrators to enable or disable specific feature flags in the system. The request should
    be a dictionary where keys are feature sections and values are dictionaries of feature keys and
    their boolean state.

    Args:
        body (FeatureValuesBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[str]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: FeatureValuesBody,
) -> str:
    """Update feature flags

     Allows administrators to enable or disable specific feature flags in the system. The request should
    be a dictionary where keys are feature sections and values are dictionaries of feature keys and
    their boolean state.

    Args:
        body (FeatureValuesBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        str
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
