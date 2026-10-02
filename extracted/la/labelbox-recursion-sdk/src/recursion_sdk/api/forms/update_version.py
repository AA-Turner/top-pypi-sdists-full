from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.form_version_already_published_error_dto import FormVersionAlreadyPublishedErrorDto
from ...models.form_version_dto import FormVersionDto
from ...models.target_api_error_forbidden import TargetApiErrorForbidden
from ...models.target_api_error_internal_error import TargetApiErrorInternalError
from ...models.target_api_error_invalid_request import TargetApiErrorInvalidRequest
from ...models.target_api_error_invariant_violation import TargetApiErrorInvariantViolation
from ...models.target_api_error_not_found import TargetApiErrorNotFound
from ...models.target_api_error_rate_limit_exceeded import TargetApiErrorRateLimitExceeded
from ...models.target_api_error_unauthorized import TargetApiErrorUnauthorized
from ...models.update_form_version_body_dto import UpdateFormVersionBodyDto
from typing import cast
from uuid import UUID



def _get_kwargs(
    form_id: UUID,
    form_version_id: UUID,
    *,
    body: UpdateFormVersionBodyDto,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/v1/forms/{form_id}/versions/{form_version_id}".format(form_id=quote(str(form_id), safe=""),form_version_id=quote(str(form_version_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> FormVersionAlreadyPublishedErrorDto | FormVersionDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    if response.status_code == 200:
        response_200 = FormVersionDto.from_dict(response.json())



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

    if response.status_code == 409:
        response_409 = FormVersionAlreadyPublishedErrorDto.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[FormVersionAlreadyPublishedErrorDto | FormVersionDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    form_id: UUID,
    form_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateFormVersionBodyDto,

) -> Response[FormVersionAlreadyPublishedErrorDto | FormVersionDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Edit a draft version (full schema replace)

     Full replace, not a partial patch: callers must send the complete schema. Only draft versions can be
    edited; published versions are permanently frozen so existing answers remain valid.

    Args:
        form_id (UUID): Stable form identifier (UUID). Forms are versioned structured-input
            schemas.
        form_version_id (UUID): Stable form-version identifier (UUID).
        body (UpdateFormVersionBodyDto): Request body for replacing the schema content of a draft
            form version. Example: {'schema': {'data': {'type': 'object', 'required': ['severity'],
            'properties': {'severity': {'type': 'string', 'title': 'Defect severity', 'enum': ['none',
            'minor', 'major', 'critical']}, 'notes': {'type': 'string', 'title': 'Reviewer notes'}}},
            'ui': {'severity': {'ui:widget': 'radio'}, 'notes': {'ui:widget': 'textarea'}}}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FormVersionAlreadyPublishedErrorDto | FormVersionDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        form_id=form_id,
form_version_id=form_version_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    form_id: UUID,
    form_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateFormVersionBodyDto,

) -> FormVersionAlreadyPublishedErrorDto | FormVersionDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Edit a draft version (full schema replace)

     Full replace, not a partial patch: callers must send the complete schema. Only draft versions can be
    edited; published versions are permanently frozen so existing answers remain valid.

    Args:
        form_id (UUID): Stable form identifier (UUID). Forms are versioned structured-input
            schemas.
        form_version_id (UUID): Stable form-version identifier (UUID).
        body (UpdateFormVersionBodyDto): Request body for replacing the schema content of a draft
            form version. Example: {'schema': {'data': {'type': 'object', 'required': ['severity'],
            'properties': {'severity': {'type': 'string', 'title': 'Defect severity', 'enum': ['none',
            'minor', 'major', 'critical']}, 'notes': {'type': 'string', 'title': 'Reviewer notes'}}},
            'ui': {'severity': {'ui:widget': 'radio'}, 'notes': {'ui:widget': 'textarea'}}}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FormVersionAlreadyPublishedErrorDto | FormVersionDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return sync_detailed(
        form_id=form_id,
form_version_id=form_version_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    form_id: UUID,
    form_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateFormVersionBodyDto,

) -> Response[FormVersionAlreadyPublishedErrorDto | FormVersionDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Edit a draft version (full schema replace)

     Full replace, not a partial patch: callers must send the complete schema. Only draft versions can be
    edited; published versions are permanently frozen so existing answers remain valid.

    Args:
        form_id (UUID): Stable form identifier (UUID). Forms are versioned structured-input
            schemas.
        form_version_id (UUID): Stable form-version identifier (UUID).
        body (UpdateFormVersionBodyDto): Request body for replacing the schema content of a draft
            form version. Example: {'schema': {'data': {'type': 'object', 'required': ['severity'],
            'properties': {'severity': {'type': 'string', 'title': 'Defect severity', 'enum': ['none',
            'minor', 'major', 'critical']}, 'notes': {'type': 'string', 'title': 'Reviewer notes'}}},
            'ui': {'severity': {'ui:widget': 'radio'}, 'notes': {'ui:widget': 'textarea'}}}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[FormVersionAlreadyPublishedErrorDto | FormVersionDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        form_id=form_id,
form_version_id=form_version_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    form_id: UUID,
    form_version_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateFormVersionBodyDto,

) -> FormVersionAlreadyPublishedErrorDto | FormVersionDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Edit a draft version (full schema replace)

     Full replace, not a partial patch: callers must send the complete schema. Only draft versions can be
    edited; published versions are permanently frozen so existing answers remain valid.

    Args:
        form_id (UUID): Stable form identifier (UUID). Forms are versioned structured-input
            schemas.
        form_version_id (UUID): Stable form-version identifier (UUID).
        body (UpdateFormVersionBodyDto): Request body for replacing the schema content of a draft
            form version. Example: {'schema': {'data': {'type': 'object', 'required': ['severity'],
            'properties': {'severity': {'type': 'string', 'title': 'Defect severity', 'enum': ['none',
            'minor', 'major', 'critical']}, 'notes': {'type': 'string', 'title': 'Reviewer notes'}}},
            'ui': {'severity': {'ui:widget': 'radio'}, 'notes': {'ui:widget': 'textarea'}}}}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        FormVersionAlreadyPublishedErrorDto | FormVersionDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return (await asyncio_detailed(
        form_id=form_id,
form_version_id=form_version_id,
client=client,
body=body,

    )).parsed
