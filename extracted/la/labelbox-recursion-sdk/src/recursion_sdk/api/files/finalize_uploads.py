from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.file_list_dto_item import FileListDtoItem
from ...models.finalize_upload_request_dto import FinalizeUploadRequestDto
from ...models.target_api_error_forbidden import TargetApiErrorForbidden
from ...models.target_api_error_internal_error import TargetApiErrorInternalError
from ...models.target_api_error_invalid_request import TargetApiErrorInvalidRequest
from ...models.target_api_error_invariant_violation import TargetApiErrorInvariantViolation
from ...models.target_api_error_rate_limit_exceeded import TargetApiErrorRateLimitExceeded
from ...models.target_api_error_unauthorized import TargetApiErrorUnauthorized
from typing import cast



def _get_kwargs(
    *,
    body: FinalizeUploadRequestDto,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/files/finalize-uploads",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[FileListDtoItem] | None:
    if response.status_code == 201:
        response_201 = []
        _response_201 = response.json()
        for componentsschemas_file_list_dto_item_data in (_response_201):
            componentsschemas_file_list_dto_item = FileListDtoItem.from_dict(componentsschemas_file_list_dto_item_data)



            response_201.append(componentsschemas_file_list_dto_item)

        return response_201

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[FileListDtoItem]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: FinalizeUploadRequestDto,

) -> Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[FileListDtoItem]]:
    """ Finalize files uploaded directly to GCS via signed URLs

     Materialises file DB rows for each successfully-uploaded GCS object. Files are environment-level and
    become attachable to any problem version in the environment after finalize.

    Args:
        body (FinalizeUploadRequestDto): Request body that finalizes a batch of direct-to-object-
            storage uploads into file records on the environment. Example: {'files': [{'objectPath': '
            environments/784e2386-e297-4f9d-a886-838422383b65/uploads/e2a910d9-32c4-4ed6-8071-
            c7190a8c1951/dataset.jsonl'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[FileListDtoItem]]
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
    client: AuthenticatedClient | Client,
    body: FinalizeUploadRequestDto,

) -> TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[FileListDtoItem] | None:
    """ Finalize files uploaded directly to GCS via signed URLs

     Materialises file DB rows for each successfully-uploaded GCS object. Files are environment-level and
    become attachable to any problem version in the environment after finalize.

    Args:
        body (FinalizeUploadRequestDto): Request body that finalizes a batch of direct-to-object-
            storage uploads into file records on the environment. Example: {'files': [{'objectPath': '
            environments/784e2386-e297-4f9d-a886-838422383b65/uploads/e2a910d9-32c4-4ed6-8071-
            c7190a8c1951/dataset.jsonl'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[FileListDtoItem]
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: FinalizeUploadRequestDto,

) -> Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[FileListDtoItem]]:
    """ Finalize files uploaded directly to GCS via signed URLs

     Materialises file DB rows for each successfully-uploaded GCS object. Files are environment-level and
    become attachable to any problem version in the environment after finalize.

    Args:
        body (FinalizeUploadRequestDto): Request body that finalizes a batch of direct-to-object-
            storage uploads into file records on the environment. Example: {'files': [{'objectPath': '
            environments/784e2386-e297-4f9d-a886-838422383b65/uploads/e2a910d9-32c4-4ed6-8071-
            c7190a8c1951/dataset.jsonl'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[FileListDtoItem]]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: FinalizeUploadRequestDto,

) -> TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[FileListDtoItem] | None:
    """ Finalize files uploaded directly to GCS via signed URLs

     Materialises file DB rows for each successfully-uploaded GCS object. Files are environment-level and
    become attachable to any problem version in the environment after finalize.

    Args:
        body (FinalizeUploadRequestDto): Request body that finalizes a batch of direct-to-object-
            storage uploads into file records on the environment. Example: {'files': [{'objectPath': '
            environments/784e2386-e297-4f9d-a886-838422383b65/uploads/e2a910d9-32c4-4ed6-8071-
            c7190a8c1951/dataset.jsonl'}]}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | list[FileListDtoItem]
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
