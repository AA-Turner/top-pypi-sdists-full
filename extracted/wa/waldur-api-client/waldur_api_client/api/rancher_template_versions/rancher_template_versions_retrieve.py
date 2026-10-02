from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.template_version import TemplateVersion
from ...types import Response


def _get_kwargs(
    template_uuid: str,
    version: str,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": f"/api/rancher-template-versions/{template_uuid}/{version}/",
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> TemplateVersion:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = TemplateVersion.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[TemplateVersion]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    template_uuid: str,
    version: str,
    *,
    client: AuthenticatedClient,
) -> Response[TemplateVersion]:
    """
    Args:
        template_uuid (str):
        version (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TemplateVersion]
    """

    kwargs = _get_kwargs(
        template_uuid=template_uuid,
        version=version,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    template_uuid: str,
    version: str,
    *,
    client: AuthenticatedClient,
) -> TemplateVersion:
    """
    Args:
        template_uuid (str):
        version (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TemplateVersion
    """

    return sync_detailed(
        template_uuid=template_uuid,
        version=version,
        client=client,
    ).parsed


async def asyncio_detailed(
    template_uuid: str,
    version: str,
    *,
    client: AuthenticatedClient,
) -> Response[TemplateVersion]:
    """
    Args:
        template_uuid (str):
        version (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TemplateVersion]
    """

    kwargs = _get_kwargs(
        template_uuid=template_uuid,
        version=version,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    template_uuid: str,
    version: str,
    *,
    client: AuthenticatedClient,
) -> TemplateVersion:
    """
    Args:
        template_uuid (str):
        version (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TemplateVersion
    """

    return (
        await asyncio_detailed(
            template_uuid=template_uuid,
            version=version,
            client=client,
        )
    ).parsed
