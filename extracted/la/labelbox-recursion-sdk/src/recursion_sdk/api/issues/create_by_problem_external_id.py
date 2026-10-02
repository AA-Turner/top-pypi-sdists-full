from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.create_issue_body_dto import CreateIssueBodyDto
from ...models.issue_dto import IssueDto
from ...models.target_api_error_forbidden import TargetApiErrorForbidden
from ...models.target_api_error_internal_error import TargetApiErrorInternalError
from ...models.target_api_error_invalid_request import TargetApiErrorInvalidRequest
from ...models.target_api_error_invariant_violation import TargetApiErrorInvariantViolation
from ...models.target_api_error_not_found import TargetApiErrorNotFound
from ...models.target_api_error_rate_limit_exceeded import TargetApiErrorRateLimitExceeded
from ...models.target_api_error_unauthorized import TargetApiErrorUnauthorized
from typing import cast



def _get_kwargs(
    environment_external_id: str,
    problem_external_id: str,
    *,
    body: CreateIssueBodyDto,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/v1/environments/by-external-id/{environment_external_id}/problems/by-external-id/{problem_external_id}/issues".format(environment_external_id=quote(str(environment_external_id), safe=""),problem_external_id=quote(str(problem_external_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> IssueDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    if response.status_code == 201:
        response_201 = IssueDto.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[IssueDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    environment_external_id: str,
    problem_external_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CreateIssueBodyDto,

) -> Response[IssueDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Create an issue for a problem by external ID

    Args:
        environment_external_id (str): External environment identifier provided by the caller's
            source-of-truth system.
        problem_external_id (str): External problem identifier provided by the caller's source-of-
            truth system.
        body (CreateIssueBodyDto): Request body for creating an issue on a problem. Example:
            {'description': 'The "detect-surface-defects" prompt is ambiguous about hairline
            scratches: it does not say whether sub-0.5mm scratches count as defects, so graders
            disagree on the expected label. Please clarify the threshold in the task description.'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[IssueDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        environment_external_id=environment_external_id,
problem_external_id=problem_external_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    environment_external_id: str,
    problem_external_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CreateIssueBodyDto,

) -> IssueDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Create an issue for a problem by external ID

    Args:
        environment_external_id (str): External environment identifier provided by the caller's
            source-of-truth system.
        problem_external_id (str): External problem identifier provided by the caller's source-of-
            truth system.
        body (CreateIssueBodyDto): Request body for creating an issue on a problem. Example:
            {'description': 'The "detect-surface-defects" prompt is ambiguous about hairline
            scratches: it does not say whether sub-0.5mm scratches count as defects, so graders
            disagree on the expected label. Please clarify the threshold in the task description.'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        IssueDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return sync_detailed(
        environment_external_id=environment_external_id,
problem_external_id=problem_external_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    environment_external_id: str,
    problem_external_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CreateIssueBodyDto,

) -> Response[IssueDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Create an issue for a problem by external ID

    Args:
        environment_external_id (str): External environment identifier provided by the caller's
            source-of-truth system.
        problem_external_id (str): External problem identifier provided by the caller's source-of-
            truth system.
        body (CreateIssueBodyDto): Request body for creating an issue on a problem. Example:
            {'description': 'The "detect-surface-defects" prompt is ambiguous about hairline
            scratches: it does not say whether sub-0.5mm scratches count as defects, so graders
            disagree on the expected label. Please clarify the threshold in the task description.'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[IssueDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        environment_external_id=environment_external_id,
problem_external_id=problem_external_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    environment_external_id: str,
    problem_external_id: str,
    *,
    client: AuthenticatedClient | Client,
    body: CreateIssueBodyDto,

) -> IssueDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Create an issue for a problem by external ID

    Args:
        environment_external_id (str): External environment identifier provided by the caller's
            source-of-truth system.
        problem_external_id (str): External problem identifier provided by the caller's source-of-
            truth system.
        body (CreateIssueBodyDto): Request body for creating an issue on a problem. Example:
            {'description': 'The "detect-surface-defects" prompt is ambiguous about hairline
            scratches: it does not say whether sub-0.5mm scratches count as defects, so graders
            disagree on the expected label. Please clarify the threshold in the task description.'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        IssueDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return (await asyncio_detailed(
        environment_external_id=environment_external_id,
problem_external_id=problem_external_id,
client=client,
body=body,

    )).parsed
