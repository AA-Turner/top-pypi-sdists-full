from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.list_session_resource_samples_resolution import ListSessionResourceSamplesResolution
from ...models.managed_agents_api_error import ManagedAgentsApiError
from ...models.managed_agents_api_error_bad_gateway import ManagedAgentsApiErrorBadGateway
from ...models.managed_agents_api_error_forbidden import ManagedAgentsApiErrorForbidden
from ...models.managed_agents_api_error_gateway_timeout import ManagedAgentsApiErrorGatewayTimeout
from ...models.managed_agents_session_resource_samples_response import ManagedAgentsSessionResourceSamplesResponse
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID
import datetime



def _get_kwargs(
    session_id: UUID,
    *,
    from_: datetime.datetime | Unset = UNSET,
    to: datetime.datetime | Unset = UNSET,
    resolution: ListSessionResourceSamplesResolution | Unset = ListSessionResourceSamplesResolution.MINUTE,
    limit: int | Unset = 120,
    page_token: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    json_from_: str | Unset = UNSET
    if not isinstance(from_, Unset):
        json_from_ = from_.isoformat()
    params["from"] = json_from_

    json_to: str | Unset = UNSET
    if not isinstance(to, Unset):
        json_to = to.isoformat()
    params["to"] = json_to

    json_resolution: str | Unset = UNSET
    if not isinstance(resolution, Unset):
        json_resolution = resolution.value

    params["resolution"] = json_resolution

    params["limit"] = limit

    params["page_token"] = page_token


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/managed-agents/v1/sessions/{session_id}/resource-samples".format(session_id=quote(str(session_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionResourceSamplesResponse | None:
    if response.status_code == 200:
        response_200 = ManagedAgentsSessionResourceSamplesResponse.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = ManagedAgentsApiError.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = ManagedAgentsApiError.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = ManagedAgentsApiErrorForbidden.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = ManagedAgentsApiError.from_dict(response.json())



        return response_404

    if response.status_code == 429:
        response_429 = ManagedAgentsApiError.from_dict(response.json())



        return response_429

    if response.status_code == 500:
        response_500 = ManagedAgentsApiError.from_dict(response.json())



        return response_500

    if response.status_code == 502:
        response_502 = ManagedAgentsApiErrorBadGateway.from_dict(response.json())



        return response_502

    if response.status_code == 503:
        response_503 = ManagedAgentsApiError.from_dict(response.json())



        return response_503

    if response.status_code == 504:
        response_504 = ManagedAgentsApiErrorGatewayTimeout.from_dict(response.json())



        return response_504

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionResourceSamplesResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    session_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    from_: datetime.datetime | Unset = UNSET,
    to: datetime.datetime | Unset = UNSET,
    resolution: ListSessionResourceSamplesResolution | Unset = ListSessionResourceSamplesResolution.MINUTE,
    limit: int | Unset = 120,
    page_token: str | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionResourceSamplesResponse]:
    """ Read sandbox CPU, memory, and GPU usage for a session tree

     Returns the tree's sandbox attachments and one page of per-minute resource usage buckets for them,
    ordered by attachment then time. Each bucket carries the minute's average and peak; resolution=raw
    adds the individual samples as parallel arrays indexed by offsets_ms. A tree whose compute was
    released and revived has several attachments; follow revived_from_sandbox_id to connect them. live
    reports whether a sandbox is still attached, which is the cue to keep polling. An empty sandboxes
    list means the tree never ran in a sandbox or sampling is disabled; an attachment with
    sampling_source=unsupported means the sandbox could not measure itself.

    Args:
        session_id (UUID): Any session id (UUID) in the tree. The sandbox is shared by the whole
            tree, so every id in it returns the same usage.
        from_ (datetime.datetime | Unset): Inclusive lower bound on bucket_start, RFC 3339. Omit
            for the start of the tree.
        to (datetime.datetime | Unset): Exclusive upper bound on bucket_start, RFC 3339. Omit for
            now.
        resolution (ListSessionResourceSamplesResolution | Unset): minute returns per-minute
            summaries only; raw also includes each bucket's per-sample arrays at the producer's
            cadence (five seconds by default). Use raw for the window on screen and minute for the
            overview. Default: ListSessionResourceSamplesResolution.MINUTE.
        limit (int | Unset): Maximum buckets per page, across all of the tree's sandbox
            attachments. Default: 120.
        page_token (str | Unset): Signed continuation token from a previous page's
            next_page_token. Bound to the organization, session, and filters it was issued for.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionResourceSamplesResponse]
     """


    kwargs = _get_kwargs(
        session_id=session_id,
from_=from_,
to=to,
resolution=resolution,
limit=limit,
page_token=page_token,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    session_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    from_: datetime.datetime | Unset = UNSET,
    to: datetime.datetime | Unset = UNSET,
    resolution: ListSessionResourceSamplesResolution | Unset = ListSessionResourceSamplesResolution.MINUTE,
    limit: int | Unset = 120,
    page_token: str | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionResourceSamplesResponse | None:
    """ Read sandbox CPU, memory, and GPU usage for a session tree

     Returns the tree's sandbox attachments and one page of per-minute resource usage buckets for them,
    ordered by attachment then time. Each bucket carries the minute's average and peak; resolution=raw
    adds the individual samples as parallel arrays indexed by offsets_ms. A tree whose compute was
    released and revived has several attachments; follow revived_from_sandbox_id to connect them. live
    reports whether a sandbox is still attached, which is the cue to keep polling. An empty sandboxes
    list means the tree never ran in a sandbox or sampling is disabled; an attachment with
    sampling_source=unsupported means the sandbox could not measure itself.

    Args:
        session_id (UUID): Any session id (UUID) in the tree. The sandbox is shared by the whole
            tree, so every id in it returns the same usage.
        from_ (datetime.datetime | Unset): Inclusive lower bound on bucket_start, RFC 3339. Omit
            for the start of the tree.
        to (datetime.datetime | Unset): Exclusive upper bound on bucket_start, RFC 3339. Omit for
            now.
        resolution (ListSessionResourceSamplesResolution | Unset): minute returns per-minute
            summaries only; raw also includes each bucket's per-sample arrays at the producer's
            cadence (five seconds by default). Use raw for the window on screen and minute for the
            overview. Default: ListSessionResourceSamplesResolution.MINUTE.
        limit (int | Unset): Maximum buckets per page, across all of the tree's sandbox
            attachments. Default: 120.
        page_token (str | Unset): Signed continuation token from a previous page's
            next_page_token. Bound to the organization, session, and filters it was issued for.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionResourceSamplesResponse
     """


    return sync_detailed(
        session_id=session_id,
client=client,
from_=from_,
to=to,
resolution=resolution,
limit=limit,
page_token=page_token,

    ).parsed

async def asyncio_detailed(
    session_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    from_: datetime.datetime | Unset = UNSET,
    to: datetime.datetime | Unset = UNSET,
    resolution: ListSessionResourceSamplesResolution | Unset = ListSessionResourceSamplesResolution.MINUTE,
    limit: int | Unset = 120,
    page_token: str | Unset = UNSET,

) -> Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionResourceSamplesResponse]:
    """ Read sandbox CPU, memory, and GPU usage for a session tree

     Returns the tree's sandbox attachments and one page of per-minute resource usage buckets for them,
    ordered by attachment then time. Each bucket carries the minute's average and peak; resolution=raw
    adds the individual samples as parallel arrays indexed by offsets_ms. A tree whose compute was
    released and revived has several attachments; follow revived_from_sandbox_id to connect them. live
    reports whether a sandbox is still attached, which is the cue to keep polling. An empty sandboxes
    list means the tree never ran in a sandbox or sampling is disabled; an attachment with
    sampling_source=unsupported means the sandbox could not measure itself.

    Args:
        session_id (UUID): Any session id (UUID) in the tree. The sandbox is shared by the whole
            tree, so every id in it returns the same usage.
        from_ (datetime.datetime | Unset): Inclusive lower bound on bucket_start, RFC 3339. Omit
            for the start of the tree.
        to (datetime.datetime | Unset): Exclusive upper bound on bucket_start, RFC 3339. Omit for
            now.
        resolution (ListSessionResourceSamplesResolution | Unset): minute returns per-minute
            summaries only; raw also includes each bucket's per-sample arrays at the producer's
            cadence (five seconds by default). Use raw for the window on screen and minute for the
            overview. Default: ListSessionResourceSamplesResolution.MINUTE.
        limit (int | Unset): Maximum buckets per page, across all of the tree's sandbox
            attachments. Default: 120.
        page_token (str | Unset): Signed continuation token from a previous page's
            next_page_token. Bound to the organization, session, and filters it was issued for.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionResourceSamplesResponse]
     """


    kwargs = _get_kwargs(
        session_id=session_id,
from_=from_,
to=to,
resolution=resolution,
limit=limit,
page_token=page_token,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    session_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    from_: datetime.datetime | Unset = UNSET,
    to: datetime.datetime | Unset = UNSET,
    resolution: ListSessionResourceSamplesResolution | Unset = ListSessionResourceSamplesResolution.MINUTE,
    limit: int | Unset = 120,
    page_token: str | Unset = UNSET,

) -> ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionResourceSamplesResponse | None:
    """ Read sandbox CPU, memory, and GPU usage for a session tree

     Returns the tree's sandbox attachments and one page of per-minute resource usage buckets for them,
    ordered by attachment then time. Each bucket carries the minute's average and peak; resolution=raw
    adds the individual samples as parallel arrays indexed by offsets_ms. A tree whose compute was
    released and revived has several attachments; follow revived_from_sandbox_id to connect them. live
    reports whether a sandbox is still attached, which is the cue to keep polling. An empty sandboxes
    list means the tree never ran in a sandbox or sampling is disabled; an attachment with
    sampling_source=unsupported means the sandbox could not measure itself.

    Args:
        session_id (UUID): Any session id (UUID) in the tree. The sandbox is shared by the whole
            tree, so every id in it returns the same usage.
        from_ (datetime.datetime | Unset): Inclusive lower bound on bucket_start, RFC 3339. Omit
            for the start of the tree.
        to (datetime.datetime | Unset): Exclusive upper bound on bucket_start, RFC 3339. Omit for
            now.
        resolution (ListSessionResourceSamplesResolution | Unset): minute returns per-minute
            summaries only; raw also includes each bucket's per-sample arrays at the producer's
            cadence (five seconds by default). Use raw for the window on screen and minute for the
            overview. Default: ListSessionResourceSamplesResolution.MINUTE.
        limit (int | Unset): Maximum buckets per page, across all of the tree's sandbox
            attachments. Default: 120.
        page_token (str | Unset): Signed continuation token from a previous page's
            next_page_token. Bound to the organization, session, and filters it was issued for.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ManagedAgentsApiError | ManagedAgentsApiErrorBadGateway | ManagedAgentsApiErrorForbidden | ManagedAgentsApiErrorGatewayTimeout | ManagedAgentsSessionResourceSamplesResponse
     """


    return (await asyncio_detailed(
        session_id=session_id,
client=client,
from_=from_,
to=to,
resolution=resolution,
limit=limit,
page_token=page_token,

    )).parsed
