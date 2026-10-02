from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.issue_comment_dto import IssueCommentDto
from ...models.target_api_error_forbidden import TargetApiErrorForbidden
from ...models.target_api_error_internal_error import TargetApiErrorInternalError
from ...models.target_api_error_invalid_request import TargetApiErrorInvalidRequest
from ...models.target_api_error_invariant_violation import TargetApiErrorInvariantViolation
from ...models.target_api_error_not_found import TargetApiErrorNotFound
from ...models.target_api_error_rate_limit_exceeded import TargetApiErrorRateLimitExceeded
from ...models.target_api_error_unauthorized import TargetApiErrorUnauthorized
from ...models.update_issue_comment_body_dto import UpdateIssueCommentBodyDto
from typing import cast
from uuid import UUID



def _get_kwargs(
    issue_id: UUID,
    issue_comment_id: UUID,
    *,
    body: UpdateIssueCommentBodyDto,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/v1/issues/{issue_id}/comments/{issue_comment_id}".format(issue_id=quote(str(issue_id), safe=""),issue_comment_id=quote(str(issue_comment_id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> IssueCommentDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    if response.status_code == 200:
        response_200 = IssueCommentDto.from_dict(response.json())



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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[IssueCommentDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    issue_id: UUID,
    issue_comment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateIssueCommentBodyDto,

) -> Response[IssueCommentDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Update a comment

    Args:
        issue_id (UUID): Stable issue identifier (UUID). Issues are author-flagged notes attached
            to a problem.
        issue_comment_id (UUID): Stable issue-comment identifier (UUID).
        body (UpdateIssueCommentBodyDto): Request body for editing an existing issue comment.
            Example: {'content': 'The detect-surface-defects grader is flagging clean parts as
            defective — looks like the brightness threshold is too aggressive. Can we lower it before
            the next eval run? (Edit: confirmed with the dataset owner — proceeding with the threshold
            change.)'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[IssueCommentDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        issue_id=issue_id,
issue_comment_id=issue_comment_id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    issue_id: UUID,
    issue_comment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateIssueCommentBodyDto,

) -> IssueCommentDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Update a comment

    Args:
        issue_id (UUID): Stable issue identifier (UUID). Issues are author-flagged notes attached
            to a problem.
        issue_comment_id (UUID): Stable issue-comment identifier (UUID).
        body (UpdateIssueCommentBodyDto): Request body for editing an existing issue comment.
            Example: {'content': 'The detect-surface-defects grader is flagging clean parts as
            defective — looks like the brightness threshold is too aggressive. Can we lower it before
            the next eval run? (Edit: confirmed with the dataset owner — proceeding with the threshold
            change.)'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        IssueCommentDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return sync_detailed(
        issue_id=issue_id,
issue_comment_id=issue_comment_id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    issue_id: UUID,
    issue_comment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateIssueCommentBodyDto,

) -> Response[IssueCommentDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]:
    """ Update a comment

    Args:
        issue_id (UUID): Stable issue identifier (UUID). Issues are author-flagged notes attached
            to a problem.
        issue_comment_id (UUID): Stable issue-comment identifier (UUID).
        body (UpdateIssueCommentBodyDto): Request body for editing an existing issue comment.
            Example: {'content': 'The detect-surface-defects grader is flagging clean parts as
            defective — looks like the brightness threshold is too aggressive. Can we lower it before
            the next eval run? (Edit: confirmed with the dataset owner — proceeding with the threshold
            change.)'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[IssueCommentDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized]
     """


    kwargs = _get_kwargs(
        issue_id=issue_id,
issue_comment_id=issue_comment_id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    issue_id: UUID,
    issue_comment_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UpdateIssueCommentBodyDto,

) -> IssueCommentDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | None:
    """ Update a comment

    Args:
        issue_id (UUID): Stable issue identifier (UUID). Issues are author-flagged notes attached
            to a problem.
        issue_comment_id (UUID): Stable issue-comment identifier (UUID).
        body (UpdateIssueCommentBodyDto): Request body for editing an existing issue comment.
            Example: {'content': 'The detect-surface-defects grader is flagging clean parts as
            defective — looks like the brightness threshold is too aggressive. Can we lower it before
            the next eval run? (Edit: confirmed with the dataset owner — proceeding with the threshold
            change.)'}.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        IssueCommentDto | TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized
     """


    return (await asyncio_detailed(
        issue_id=issue_id,
issue_comment_id=issue_comment_id,
client=client,
body=body,

    )).parsed
