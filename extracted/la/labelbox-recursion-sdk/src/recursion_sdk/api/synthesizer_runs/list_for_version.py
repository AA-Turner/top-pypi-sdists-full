from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.list_for_version_sort_direction import ListForVersionSortDirection
from ...models.synthesizer_run_page_dto import SynthesizerRunPageDto
from ...models.target_api_error_forbidden import TargetApiErrorForbidden
from ...models.target_api_error_internal_error import TargetApiErrorInternalError
from ...models.target_api_error_invalid_request import TargetApiErrorInvalidRequest
from ...models.target_api_error_invariant_violation import TargetApiErrorInvariantViolation
from ...models.target_api_error_not_found import TargetApiErrorNotFound
from ...models.target_api_error_rate_limit_exceeded import TargetApiErrorRateLimitExceeded
from ...models.target_api_error_unauthorized import TargetApiErrorUnauthorized
from ...types import UNSET, Unset
from typing import cast
from uuid import UUID



def _get_kwargs(
    problem_version_id: UUID,
    *,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    sort_direction: ListForVersionSortDirection | Unset = UNSET,
    search: str | Unset = UNSET,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["limit"] = limit

    params["cursor"] = cursor

    params["sortBy"] = sort_by

    json_sort_direction: str | Unset = UNSET
    if not isinstance(sort_direction, Unset):
        json_sort_direction = sort_direction.value

    params["sortDirection"] = json_sort_direction

    params["search"] = search


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/versions/{problem_version_id}/synthesizer-runs".format(problem_version_id=quote(str(problem_version_id), safe=""),),
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> SynthesizerRunPageDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    if response.status_code == 200:
        response_200 = SynthesizerRunPageDto.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = TargetApiErrorInvalidRequest.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = TargetApiErrorUnauthorized.from_dict(response.json())



        return response_401

    if response.status_code == 403:
        response_403 = TargetApiErrorForbidden.from_dict(response.json())



        return response_403

    if response.status_code == 404:
        response_404 = TargetApiErrorNotFound.from_dict(response.json())



        return response_404

    if response.status_code == 429:
        response_429 = TargetApiErrorRateLimitExceeded.from_dict(response.json())



        return response_429

    if response.status_code == 500:
        def _parse_response_500(data: object) -> TargetApiErrorInternalError | TargetApiErrorInvariantViolation:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_500_type_0 = TargetApiErrorInternalError.from_dict(data)



                return response_500_type_0
            except (TypeError, ValueError, AttributeError, KeyError):
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_500_type_1 = TargetApiErrorInvariantViolation.from_dict(data)



            return response_500_type_1

        response_500 = _parse_response_500(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[SynthesizerRunPageDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    problem_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    sort_direction: ListForVersionSortDirection | Unset = UNSET,
    search: str | Unset = UNSET,

) -> Response[SynthesizerRunPageDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ List synthesizer runs for a problem version

    Args:
        problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have
            many versions; this points at one specific version.
        limit (int | Unset): Maximum number of items to return in the page (1-100). Default: 10.
            Example: 20.
        cursor (str | Unset): Opaque cursor returned by a previous page response. Omit to fetch
            the first page.
        sort_by (str | Unset): Field to sort by. Allowed values depend on the entity being listed.
        sort_direction (ListForVersionSortDirection | Unset): Sort direction. Defaults to
            ascending when omitted.
        search (str | Unset): Free-text filter applied to the entity searchable fields.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SynthesizerRunPageDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        problem_version_id=problem_version_id,
limit=limit,
cursor=cursor,
sort_by=sort_by,
sort_direction=sort_direction,
search=search,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    problem_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    sort_direction: ListForVersionSortDirection | Unset = UNSET,
    search: str | Unset = UNSET,

) -> SynthesizerRunPageDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ List synthesizer runs for a problem version

    Args:
        problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have
            many versions; this points at one specific version.
        limit (int | Unset): Maximum number of items to return in the page (1-100). Default: 10.
            Example: 20.
        cursor (str | Unset): Opaque cursor returned by a previous page response. Omit to fetch
            the first page.
        sort_by (str | Unset): Field to sort by. Allowed values depend on the entity being listed.
        sort_direction (ListForVersionSortDirection | Unset): Sort direction. Defaults to
            ascending when omitted.
        search (str | Unset): Free-text filter applied to the entity searchable fields.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SynthesizerRunPageDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return sync_detailed(
        problem_version_id=problem_version_id,
client=client,
limit=limit,
cursor=cursor,
sort_by=sort_by,
sort_direction=sort_direction,
search=search,

    ).parsed

async def asyncio_detailed(
    problem_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    sort_direction: ListForVersionSortDirection | Unset = UNSET,
    search: str | Unset = UNSET,

) -> Response[SynthesizerRunPageDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ List synthesizer runs for a problem version

    Args:
        problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have
            many versions; this points at one specific version.
        limit (int | Unset): Maximum number of items to return in the page (1-100). Default: 10.
            Example: 20.
        cursor (str | Unset): Opaque cursor returned by a previous page response. Omit to fetch
            the first page.
        sort_by (str | Unset): Field to sort by. Allowed values depend on the entity being listed.
        sort_direction (ListForVersionSortDirection | Unset): Sort direction. Defaults to
            ascending when omitted.
        search (str | Unset): Free-text filter applied to the entity searchable fields.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[SynthesizerRunPageDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        problem_version_id=problem_version_id,
limit=limit,
cursor=cursor,
sort_by=sort_by,
sort_direction=sort_direction,
search=search,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    problem_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    limit: int | Unset = 10,
    cursor: str | Unset = UNSET,
    sort_by: str | Unset = UNSET,
    sort_direction: ListForVersionSortDirection | Unset = UNSET,
    search: str | Unset = UNSET,

) -> SynthesizerRunPageDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ List synthesizer runs for a problem version

    Args:
        problem_version_id (UUID): Stable problem-version identifier (UUID). Each problem can have
            many versions; this points at one specific version.
        limit (int | Unset): Maximum number of items to return in the page (1-100). Default: 10.
            Example: 20.
        cursor (str | Unset): Opaque cursor returned by a previous page response. Omit to fetch
            the first page.
        sort_by (str | Unset): Field to sort by. Allowed values depend on the entity being listed.
        sort_direction (ListForVersionSortDirection | Unset): Sort direction. Defaults to
            ascending when omitted.
        search (str | Unset): Free-text filter applied to the entity searchable fields.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        SynthesizerRunPageDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return (await asyncio_detailed(
        problem_version_id=problem_version_id,
client=client,
limit=limit,
cursor=cursor,
sort_by=sort_by,
sort_direction=sort_direction,
search=search,

    )).parsed
