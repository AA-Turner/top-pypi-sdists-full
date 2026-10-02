from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.api_error_status_409 import ApiErrorStatus409
from ...models.attach_qa_config_file_body_dto import AttachQaConfigFileBodyDto
from ...models.qa_config_file_response_dto import QaConfigFileResponseDto
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
    qa_config_id: UUID,
    *,
    body: AttachQaConfigFileBodyDto,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/qa-configs/{qa_config_id}/files".format(qa_config_id=quote(str(qa_config_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> ApiErrorStatus409 | QaConfigFileResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    if response.status_code == 201:
        response_201 = QaConfigFileResponseDto.from_dict(response.json())



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

    if response.status_code == 404:
        response_404 = TargetApiErrorNotFound.from_dict(response.json())



        return response_404

    if response.status_code == 409:
        response_409 = ApiErrorStatus409.from_dict(response.json())



        return response_409

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[ApiErrorStatus409 | QaConfigFileResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    qa_config_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: AttachQaConfigFileBodyDto,

) -> Response[ApiErrorStatus409 | QaConfigFileResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Attach a file to a QA config

     Attaches an organization-scoped file so it is mounted into the runner container on future jobs. In-
    flight jobs continue to use the snapshot they were dispatched with.

    Args:
        qa_config_id (UUID): Stable QA-config identifier (UUID).
        body (AttachQaConfigFileBodyDto): Payload for attaching an existing uploaded file to a QA
            config at a given mount path. Example: {'fileId': 'e2a910d9-32c4-4ed6-8071-c7190a8c1951',
            'mountPath': '/workspace/config/rubric-guidelines.md'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiErrorStatus409 | QaConfigFileResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        qa_config_id=qa_config_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    qa_config_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: AttachQaConfigFileBodyDto,

) -> ApiErrorStatus409 | QaConfigFileResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Attach a file to a QA config

     Attaches an organization-scoped file so it is mounted into the runner container on future jobs. In-
    flight jobs continue to use the snapshot they were dispatched with.

    Args:
        qa_config_id (UUID): Stable QA-config identifier (UUID).
        body (AttachQaConfigFileBodyDto): Payload for attaching an existing uploaded file to a QA
            config at a given mount path. Example: {'fileId': 'e2a910d9-32c4-4ed6-8071-c7190a8c1951',
            'mountPath': '/workspace/config/rubric-guidelines.md'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiErrorStatus409 | QaConfigFileResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return sync_detailed(
        qa_config_id=qa_config_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    qa_config_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: AttachQaConfigFileBodyDto,

) -> Response[ApiErrorStatus409 | QaConfigFileResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Attach a file to a QA config

     Attaches an organization-scoped file so it is mounted into the runner container on future jobs. In-
    flight jobs continue to use the snapshot they were dispatched with.

    Args:
        qa_config_id (UUID): Stable QA-config identifier (UUID).
        body (AttachQaConfigFileBodyDto): Payload for attaching an existing uploaded file to a QA
            config at a given mount path. Example: {'fileId': 'e2a910d9-32c4-4ed6-8071-c7190a8c1951',
            'mountPath': '/workspace/config/rubric-guidelines.md'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ApiErrorStatus409 | QaConfigFileResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        qa_config_id=qa_config_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    qa_config_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: AttachQaConfigFileBodyDto,

) -> ApiErrorStatus409 | QaConfigFileResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Attach a file to a QA config

     Attaches an organization-scoped file so it is mounted into the runner container on future jobs. In-
    flight jobs continue to use the snapshot they were dispatched with.

    Args:
        qa_config_id (UUID): Stable QA-config identifier (UUID).
        body (AttachQaConfigFileBodyDto): Payload for attaching an existing uploaded file to a QA
            config at a given mount path. Example: {'fileId': 'e2a910d9-32c4-4ed6-8071-c7190a8c1951',
            'mountPath': '/workspace/config/rubric-guidelines.md'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ApiErrorStatus409 | QaConfigFileResponseDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return (await asyncio_detailed(
        qa_config_id=qa_config_id,
client=client,
body=body,

    )).parsed
