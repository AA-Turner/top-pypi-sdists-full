from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.list_images_sort import ListImagesSort
from ...models.marketplace_list_response_dto import MarketplaceListResponseDto
from ...models.target_api_error_forbidden import TargetApiErrorForbidden
from ...models.target_api_error_internal_error import TargetApiErrorInternalError
from ...models.target_api_error_invalid_request import TargetApiErrorInvalidRequest
from ...models.target_api_error_invariant_violation import TargetApiErrorInvariantViolation
from ...models.target_api_error_rate_limit_exceeded import TargetApiErrorRateLimitExceeded
from ...models.target_api_error_unauthorized import TargetApiErrorUnauthorized
from ...types import UNSET, Unset
from typing import cast



def _get_kwargs(
    *,
    search: str | Unset = UNSET,
    limit: int | Unset = 24,
    offset: int | Unset = 0,
    sort: ListImagesSort | Unset = ListImagesSort.RECENT,

) -> dict[str, Any]:
    

    

    params: dict[str, Any] = {}

    params["search"] = search

    params["limit"] = limit

    params["offset"] = offset

    json_sort: str | Unset = UNSET
    if not isinstance(sort, Unset):
        json_sort = sort.value

    params["sort"] = json_sort


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/marketplace/images",
        "params": params,
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> MarketplaceListResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    if response.status_code == 200:
        response_200 = MarketplaceListResponseDto.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[MarketplaceListResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    search: str | Unset = UNSET,
    limit: int | Unset = 24,
    offset: int | Unset = 0,
    sort: ListImagesSort | Unset = ListImagesSort.RECENT,

) -> Response[MarketplaceListResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ List marketplace images

     Marketplace images are shared across all organizations.

    Args:
        search (str | Unset): Optional case-insensitive substring to filter images by repository
            name or description.
        limit (int | Unset): Maximum number of items to return per page (1-100). Default: 24.
            Example: 24.
        offset (int | Unset): Zero-based offset into the result set. Default: 0. Example: 0.
        sort (ListImagesSort | Unset): Sort order: by most recent push time, by repository name,
            or by tag count. Default: ListImagesSort.RECENT.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MarketplaceListResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        search=search,
limit=limit,
offset=offset,
sort=sort,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient | Client,
    search: str | Unset = UNSET,
    limit: int | Unset = 24,
    offset: int | Unset = 0,
    sort: ListImagesSort | Unset = ListImagesSort.RECENT,

) -> MarketplaceListResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ List marketplace images

     Marketplace images are shared across all organizations.

    Args:
        search (str | Unset): Optional case-insensitive substring to filter images by repository
            name or description.
        limit (int | Unset): Maximum number of items to return per page (1-100). Default: 24.
            Example: 24.
        offset (int | Unset): Zero-based offset into the result set. Default: 0. Example: 0.
        sort (ListImagesSort | Unset): Sort order: by most recent push time, by repository name,
            or by tag count. Default: ListImagesSort.RECENT.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MarketplaceListResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return sync_detailed(
        client=client,
search=search,
limit=limit,
offset=offset,
sort=sort,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    search: str | Unset = UNSET,
    limit: int | Unset = 24,
    offset: int | Unset = 0,
    sort: ListImagesSort | Unset = ListImagesSort.RECENT,

) -> Response[MarketplaceListResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ List marketplace images

     Marketplace images are shared across all organizations.

    Args:
        search (str | Unset): Optional case-insensitive substring to filter images by repository
            name or description.
        limit (int | Unset): Maximum number of items to return per page (1-100). Default: 24.
            Example: 24.
        offset (int | Unset): Zero-based offset into the result set. Default: 0. Example: 0.
        sort (ListImagesSort | Unset): Sort order: by most recent push time, by repository name,
            or by tag count. Default: ListImagesSort.RECENT.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[MarketplaceListResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        search=search,
limit=limit,
offset=offset,
sort=sort,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    search: str | Unset = UNSET,
    limit: int | Unset = 24,
    offset: int | Unset = 0,
    sort: ListImagesSort | Unset = ListImagesSort.RECENT,

) -> MarketplaceListResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ List marketplace images

     Marketplace images are shared across all organizations.

    Args:
        search (str | Unset): Optional case-insensitive substring to filter images by repository
            name or description.
        limit (int | Unset): Maximum number of items to return per page (1-100). Default: 24.
            Example: 24.
        offset (int | Unset): Zero-based offset into the result set. Default: 0. Example: 0.
        sort (ListImagesSort | Unset): Sort order: by most recent push time, by repository name,
            or by tag count. Default: ListImagesSort.RECENT.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        MarketplaceListResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return (await asyncio_detailed(
        client=client,
search=search,
limit=limit,
offset=offset,
sort=sort,

    )).parsed
