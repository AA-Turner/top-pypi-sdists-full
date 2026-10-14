from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.adopt_provider_accounts_request import AdoptProviderAccountsRequest
from ...models.adopt_provider_accounts_response import AdoptProviderAccountsResponse
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: AdoptProviderAccountsRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-service-providers/{uuid}/adopt_provider_accounts/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> AdoptProviderAccountsResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = AdoptProviderAccountsResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[AdoptProviderAccountsResponse]:
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
    body: AdoptProviderAccountsRequest,
) -> Response[AdoptProviderAccountsResponse]:
    """Adopt provider-level accounts

     Backs every offering account at this provider with one provider-level account per user, so a person
    resolves to a single username and POSIX identity across the provider's offerings.

    Users whose accounts already agree are adopted without input. A user whose accounts disagree must be
    given a surviving username in 'resolutions', keyed by user UUID — see the 'username_conflicts'
    action. The call is refused while any conflict is unresolved, rather than adopting part of the
    provider and leaving the rest on the old per-offering behaviour.

    Args:
        uuid (UUID):
        body (AdoptProviderAccountsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdoptProviderAccountsResponse]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: AdoptProviderAccountsRequest,
) -> AdoptProviderAccountsResponse:
    """Adopt provider-level accounts

     Backs every offering account at this provider with one provider-level account per user, so a person
    resolves to a single username and POSIX identity across the provider's offerings.

    Users whose accounts already agree are adopted without input. A user whose accounts disagree must be
    given a surviving username in 'resolutions', keyed by user UUID — see the 'username_conflicts'
    action. The call is refused while any conflict is unresolved, rather than adopting part of the
    provider and leaving the rest on the old per-offering behaviour.

    Args:
        uuid (UUID):
        body (AdoptProviderAccountsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdoptProviderAccountsResponse
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: AdoptProviderAccountsRequest,
) -> Response[AdoptProviderAccountsResponse]:
    """Adopt provider-level accounts

     Backs every offering account at this provider with one provider-level account per user, so a person
    resolves to a single username and POSIX identity across the provider's offerings.

    Users whose accounts already agree are adopted without input. A user whose accounts disagree must be
    given a surviving username in 'resolutions', keyed by user UUID — see the 'username_conflicts'
    action. The call is refused while any conflict is unresolved, rather than adopting part of the
    provider and leaving the rest on the old per-offering behaviour.

    Args:
        uuid (UUID):
        body (AdoptProviderAccountsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[AdoptProviderAccountsResponse]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: AdoptProviderAccountsRequest,
) -> AdoptProviderAccountsResponse:
    """Adopt provider-level accounts

     Backs every offering account at this provider with one provider-level account per user, so a person
    resolves to a single username and POSIX identity across the provider's offerings.

    Users whose accounts already agree are adopted without input. A user whose accounts disagree must be
    given a surviving username in 'resolutions', keyed by user UUID — see the 'username_conflicts'
    action. The call is refused while any conflict is unresolved, rather than adopting part of the
    provider and leaving the rest on the old per-offering behaviour.

    Args:
        uuid (UUID):
        body (AdoptProviderAccountsRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        AdoptProviderAccountsResponse
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
