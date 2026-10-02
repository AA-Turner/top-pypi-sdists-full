from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.detail_response import DetailResponse
from ...models.member_sync_status_report_request import MemberSyncStatusReportRequest
from ...models.member_sync_status_report_result import MemberSyncStatusReportResult
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: MemberSyncStatusReportRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/marketplace-provider-resources/{uuid}/set_membership_sync_statuses/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Union[DetailResponse, MemberSyncStatusReportResult]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = MemberSyncStatusReportResult.from_dict(response.json())

        return response_200
    if response.status_code == 409:
        response_409 = DetailResponse.from_dict(response.json())

        return response_409
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[DetailResponse, MemberSyncStatusReportResult]]:
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
    body: MemberSyncStatusReportRequest,
) -> Response[Union[DetailResponse, MemberSyncStatusReportResult]]:
    """Report per-member sync statuses for a resource

     Full-replace report from the site agent: replaces every previously stored member sync status of this
    resource with the submitted set. Requires the offering to opt in via the
    enable_membership_sync_status plugin option. Entries whose user cannot be resolved are skipped and
    echoed back in the response instead of failing the whole report.

    Args:
        uuid (UUID):
        body (MemberSyncStatusReportRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DetailResponse, MemberSyncStatusReportResult]]
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
    body: MemberSyncStatusReportRequest,
) -> Union[DetailResponse, MemberSyncStatusReportResult]:
    """Report per-member sync statuses for a resource

     Full-replace report from the site agent: replaces every previously stored member sync status of this
    resource with the submitted set. Requires the offering to opt in via the
    enable_membership_sync_status plugin option. Entries whose user cannot be resolved are skipped and
    echoed back in the response instead of failing the whole report.

    Args:
        uuid (UUID):
        body (MemberSyncStatusReportRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DetailResponse, MemberSyncStatusReportResult]
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
    body: MemberSyncStatusReportRequest,
) -> Response[Union[DetailResponse, MemberSyncStatusReportResult]]:
    """Report per-member sync statuses for a resource

     Full-replace report from the site agent: replaces every previously stored member sync status of this
    resource with the submitted set. Requires the offering to opt in via the
    enable_membership_sync_status plugin option. Entries whose user cannot be resolved are skipped and
    echoed back in the response instead of failing the whole report.

    Args:
        uuid (UUID):
        body (MemberSyncStatusReportRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[DetailResponse, MemberSyncStatusReportResult]]
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
    body: MemberSyncStatusReportRequest,
) -> Union[DetailResponse, MemberSyncStatusReportResult]:
    """Report per-member sync statuses for a resource

     Full-replace report from the site agent: replaces every previously stored member sync status of this
    resource with the submitted set. Requires the offering to opt in via the
    enable_membership_sync_status plugin option. Entries whose user cannot be resolved are skipped and
    echoed back in the response instead of failing the whole report.

    Args:
        uuid (UUID):
        body (MemberSyncStatusReportRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[DetailResponse, MemberSyncStatusReportResult]
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
