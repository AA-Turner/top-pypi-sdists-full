from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.duplicate_offering_remediate_request import DuplicateOfferingRemediateRequest
from ...models.duplicate_offering_remediation import DuplicateOfferingRemediation
from ...types import Response


def _get_kwargs(
    *,
    body: DuplicateOfferingRemediateRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/marketplace-openstack-duplicate-offerings/remediate/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> DuplicateOfferingRemediation:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = DuplicateOfferingRemediation.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[DuplicateOfferingRemediation]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: DuplicateOfferingRemediateRequest,
) -> Response[DuplicateOfferingRemediation]:
    """Collapse one duplicate per-tenant offering group onto its keeper. Previews by default; pass
    dry_run=false to apply. Refuses to run when history (billing periods, usage records) cannot be re-
    pointed.

    Args:
        body (DuplicateOfferingRemediateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DuplicateOfferingRemediation]
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
    body: DuplicateOfferingRemediateRequest,
) -> DuplicateOfferingRemediation:
    """Collapse one duplicate per-tenant offering group onto its keeper. Previews by default; pass
    dry_run=false to apply. Refuses to run when history (billing periods, usage records) cannot be re-
    pointed.

    Args:
        body (DuplicateOfferingRemediateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DuplicateOfferingRemediation
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: DuplicateOfferingRemediateRequest,
) -> Response[DuplicateOfferingRemediation]:
    """Collapse one duplicate per-tenant offering group onto its keeper. Previews by default; pass
    dry_run=false to apply. Refuses to run when history (billing periods, usage records) cannot be re-
    pointed.

    Args:
        body (DuplicateOfferingRemediateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[DuplicateOfferingRemediation]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: DuplicateOfferingRemediateRequest,
) -> DuplicateOfferingRemediation:
    """Collapse one duplicate per-tenant offering group onto its keeper. Previews by default; pass
    dry_run=false to apply. Refuses to run when history (billing periods, usage records) cannot be re-
    pointed.

    Args:
        body (DuplicateOfferingRemediateRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        DuplicateOfferingRemediation
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
