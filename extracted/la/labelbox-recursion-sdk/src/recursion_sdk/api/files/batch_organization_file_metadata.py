from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.batch_organization_file_metadata_request_dto import BatchOrganizationFileMetadataRequestDto
from ...models.organization_file_metadata_list_dto_item import OrganizationFileMetadataListDtoItem
from ...models.target_api_error_forbidden import TargetApiErrorForbidden
from ...models.target_api_error_internal_error import TargetApiErrorInternalError
from ...models.target_api_error_invalid_request import TargetApiErrorInvalidRequest
from ...models.target_api_error_invariant_violation import TargetApiErrorInvariantViolation
from ...models.target_api_error_not_found import TargetApiErrorNotFound
from ...models.target_api_error_rate_limit_exceeded import TargetApiErrorRateLimitExceeded
from ...models.target_api_error_unauthorized import TargetApiErrorUnauthorized
from typing import cast
from uuid import UUID



def _get_kwargs(
    organization_id: UUID,
    *,
    body: BatchOrganizationFileMetadataRequestDto,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/organizations/{organization_id}/files/metadata".format(organization_id=quote(str(organization_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[OrganizationFileMetadataListDtoItem] | None:
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for componentsschemas_organization_file_metadata_list_dto_item_data in (_response_200):
            componentsschemas_organization_file_metadata_list_dto_item = OrganizationFileMetadataListDtoItem.from_dict(componentsschemas_organization_file_metadata_list_dto_item_data)



            response_200.append(componentsschemas_organization_file_metadata_list_dto_item)

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[OrganizationFileMetadataListDtoItem]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    organization_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: BatchOrganizationFileMetadataRequestDto,

) -> Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[OrganizationFileMetadataListDtoItem]]:
    """ Batch-resolve org-scoped file metadata

     Returns filename, sizeBytes, and createdAt for each requested file id. Every id must be reachable in
    the organization: for user callers, the file must have a same-org (or platform-skill) attachment or
    be created by the caller; conflicting other-org attachments always 404. If any id is missing or out
    of scope, the whole request fails with 404 — no partial success.

    Args:
        organization_id (UUID): Stable organization identifier (UUID). Top-level tenant boundary.
        body (BatchOrganizationFileMetadataRequestDto): Request body for a batch org-scoped file-
            metadata lookup. Rejects the whole batch if any id is missing or out of scope. Example:
            {'fileIds': ['e2a910d9-32c4-4ed6-8071-c7190a8c1951']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[OrganizationFileMetadataListDtoItem]]
     """


    kwargs = _get_kwargs(
        organization_id=organization_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    organization_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: BatchOrganizationFileMetadataRequestDto,

) -> TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[OrganizationFileMetadataListDtoItem] | None:
    """ Batch-resolve org-scoped file metadata

     Returns filename, sizeBytes, and createdAt for each requested file id. Every id must be reachable in
    the organization: for user callers, the file must have a same-org (or platform-skill) attachment or
    be created by the caller; conflicting other-org attachments always 404. If any id is missing or out
    of scope, the whole request fails with 404 — no partial success.

    Args:
        organization_id (UUID): Stable organization identifier (UUID). Top-level tenant boundary.
        body (BatchOrganizationFileMetadataRequestDto): Request body for a batch org-scoped file-
            metadata lookup. Rejects the whole batch if any id is missing or out of scope. Example:
            {'fileIds': ['e2a910d9-32c4-4ed6-8071-c7190a8c1951']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[OrganizationFileMetadataListDtoItem]
     """


    return sync_detailed(
        organization_id=organization_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    organization_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: BatchOrganizationFileMetadataRequestDto,

) -> Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[OrganizationFileMetadataListDtoItem]]:
    """ Batch-resolve org-scoped file metadata

     Returns filename, sizeBytes, and createdAt for each requested file id. Every id must be reachable in
    the organization: for user callers, the file must have a same-org (or platform-skill) attachment or
    be created by the caller; conflicting other-org attachments always 404. If any id is missing or out
    of scope, the whole request fails with 404 — no partial success.

    Args:
        organization_id (UUID): Stable organization identifier (UUID). Top-level tenant boundary.
        body (BatchOrganizationFileMetadataRequestDto): Request body for a batch org-scoped file-
            metadata lookup. Rejects the whole batch if any id is missing or out of scope. Example:
            {'fileIds': ['e2a910d9-32c4-4ed6-8071-c7190a8c1951']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[OrganizationFileMetadataListDtoItem]]
     """


    kwargs = _get_kwargs(
        organization_id=organization_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    organization_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: BatchOrganizationFileMetadataRequestDto,

) -> TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[OrganizationFileMetadataListDtoItem] | None:
    """ Batch-resolve org-scoped file metadata

     Returns filename, sizeBytes, and createdAt for each requested file id. Every id must be reachable in
    the organization: for user callers, the file must have a same-org (or platform-skill) attachment or
    be created by the caller; conflicting other-org attachments always 404. If any id is missing or out
    of scope, the whole request fails with 404 — no partial success.

    Args:
        organization_id (UUID): Stable organization identifier (UUID). Top-level tenant boundary.
        body (BatchOrganizationFileMetadataRequestDto): Request body for a batch org-scoped file-
            metadata lookup. Rejects the whole batch if any id is missing or out of scope. Example:
            {'fileIds': ['e2a910d9-32c4-4ed6-8071-c7190a8c1951']}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[OrganizationFileMetadataListDtoItem]
     """


    return (await asyncio_detailed(
        organization_id=organization_id,
client=client,
body=body,

    )).parsed
