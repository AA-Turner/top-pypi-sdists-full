from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.scim_pull_attributes_response import ScimPullAttributesResponse
from ...types import Response


def _get_kwargs(
    uuid: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/users/{uuid}/pull_scim_attributes/",
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> ScimPullAttributesResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = ScimPullAttributesResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[ScimPullAttributesResponse]:
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
) -> Response[ScimPullAttributesResponse]:
    """Pull SCIM attributes from external IdP for this user

     Staff-only action that pulls the user's attributes from the configured external SCIM 2.0 directory
    (SCIM_PULL_API_URL). Pulled attributes are merged via the same source-aware policy as inbound SCIM
    and the Identity Bridge.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ScimPullAttributesResponse]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> ScimPullAttributesResponse:
    """Pull SCIM attributes from external IdP for this user

     Staff-only action that pulls the user's attributes from the configured external SCIM 2.0 directory
    (SCIM_PULL_API_URL). Pulled attributes are merged via the same source-aware policy as inbound SCIM
    and the Identity Bridge.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ScimPullAttributesResponse
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> Response[ScimPullAttributesResponse]:
    """Pull SCIM attributes from external IdP for this user

     Staff-only action that pulls the user's attributes from the configured external SCIM 2.0 directory
    (SCIM_PULL_API_URL). Pulled attributes are merged via the same source-aware policy as inbound SCIM
    and the Identity Bridge.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ScimPullAttributesResponse]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
) -> ScimPullAttributesResponse:
    """Pull SCIM attributes from external IdP for this user

     Staff-only action that pulls the user's attributes from the configured external SCIM 2.0 directory
    (SCIM_PULL_API_URL). Pulled attributes are merged via the same source-aware policy as inbound SCIM
    and the Identity Bridge.

    Args:
        uuid (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ScimPullAttributesResponse
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
        )
    ).parsed
