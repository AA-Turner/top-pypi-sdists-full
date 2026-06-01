from http import HTTPStatus
from typing import Any
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response
from ... import errors

from ...models.error_response import ErrorResponse
from ...models.sso_domain_request import SSODomainRequest
from ...models.sso_domain_response import SSODomainResponse


def _get_kwargs(
    domain: str,
    *,
    body: SSODomainRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/v1/accounts/current/sso_domains/{domain}".format(
            domain=quote(str(domain), safe=""),
        ),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/vnd.api+json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ErrorResponse | SSODomainResponse | None:
    if response.status_code == 200:
        response_200 = SSODomainResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 404:
        response_404 = ErrorResponse.from_dict(response.json())

        return response_404

    if response.status_code == 429:
        response_429 = ErrorResponse.from_dict(response.json())

        return response_429

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ErrorResponse | SSODomainResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    domain: str,
    *,
    client: AuthenticatedClient,
    body: SSODomainRequest,
) -> Response[ErrorResponse | SSODomainResponse]:
    """Claim SSO Domain

     Claim a domain for SSO routing. Idempotent — re-claiming a domain already held by the account is a
    no-op success. The response includes the DNS TXT token to publish.

    Args:
        domain (str):
        body (SSODomainRequest): JSON:API request envelope for claiming a domain.

            The attributes block is intentionally optional/empty — all writeable
            data on a domain is the domain string itself (in the URL) and the
            server-generated verification token. Claim is idempotent: re-claim
            of a domain the account already holds is a no-op success.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SSODomainResponse]
    """

    kwargs = _get_kwargs(
        domain=domain,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    domain: str,
    *,
    client: AuthenticatedClient,
    body: SSODomainRequest,
) -> ErrorResponse | SSODomainResponse | None:
    """Claim SSO Domain

     Claim a domain for SSO routing. Idempotent — re-claiming a domain already held by the account is a
    no-op success. The response includes the DNS TXT token to publish.

    Args:
        domain (str):
        body (SSODomainRequest): JSON:API request envelope for claiming a domain.

            The attributes block is intentionally optional/empty — all writeable
            data on a domain is the domain string itself (in the URL) and the
            server-generated verification token. Claim is idempotent: re-claim
            of a domain the account already holds is a no-op success.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SSODomainResponse
    """

    return sync_detailed(
        domain=domain,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    domain: str,
    *,
    client: AuthenticatedClient,
    body: SSODomainRequest,
) -> Response[ErrorResponse | SSODomainResponse]:
    """Claim SSO Domain

     Claim a domain for SSO routing. Idempotent — re-claiming a domain already held by the account is a
    no-op success. The response includes the DNS TXT token to publish.

    Args:
        domain (str):
        body (SSODomainRequest): JSON:API request envelope for claiming a domain.

            The attributes block is intentionally optional/empty — all writeable
            data on a domain is the domain string itself (in the URL) and the
            server-generated verification token. Claim is idempotent: re-claim
            of a domain the account already holds is a no-op success.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ErrorResponse | SSODomainResponse]
    """

    kwargs = _get_kwargs(
        domain=domain,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    domain: str,
    *,
    client: AuthenticatedClient,
    body: SSODomainRequest,
) -> ErrorResponse | SSODomainResponse | None:
    """Claim SSO Domain

     Claim a domain for SSO routing. Idempotent — re-claiming a domain already held by the account is a
    no-op success. The response includes the DNS TXT token to publish.

    Args:
        domain (str):
        body (SSODomainRequest): JSON:API request envelope for claiming a domain.

            The attributes block is intentionally optional/empty — all writeable
            data on a domain is the domain string itself (in the URL) and the
            server-generated verification token. Claim is idempotent: re-claim
            of a domain the account already holds is a no-op success.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ErrorResponse | SSODomainResponse
    """

    return (
        await asyncio_detailed(
            domain=domain,
            client=client,
            body=body,
        )
    ).parsed
