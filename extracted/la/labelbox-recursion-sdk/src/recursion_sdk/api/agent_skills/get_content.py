from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

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
    skill_id: UUID,

) -> dict[str, Any]:
    

    

    

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/organizations/{organization_id}/skills/{skill_id}/content".format(organization_id=quote(str(organization_id), safe=""),skill_id=quote(str(skill_id), safe=""),),
    }


    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | str | None:
    if response.status_code == 200:
        response_200 = response.text
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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | str]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    organization_id: UUID,
    skill_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | str]:
    """ Get a skill’s SKILL.md body as plain text

     Fetches the skill bundle server-side and returns SKILL.md as text/plain (extracting from a zip when
    needed). Same org-scoping as skill detail — org members can read org + platform skills; soft-deleted
    skills remain resolvable. Prefer this over fetching the signed contentUrl from the browser (GCS
    CORS).

    Args:
        organization_id (UUID): Stable organization identifier (UUID). Top-level tenant boundary.
        skill_id (UUID): Stable skill identifier (UUID). Org-uploaded or platform-curated skill
            bundle mounted into an agent workspace.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | str]
     """


    kwargs = _get_kwargs(
        organization_id=organization_id,
skill_id=skill_id,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    organization_id: UUID,
    skill_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | str | None:
    """ Get a skill’s SKILL.md body as plain text

     Fetches the skill bundle server-side and returns SKILL.md as text/plain (extracting from a zip when
    needed). Same org-scoping as skill detail — org members can read org + platform skills; soft-deleted
    skills remain resolvable. Prefer this over fetching the signed contentUrl from the browser (GCS
    CORS).

    Args:
        organization_id (UUID): Stable organization identifier (UUID). Top-level tenant boundary.
        skill_id (UUID): Stable skill identifier (UUID). Org-uploaded or platform-curated skill
            bundle mounted into an agent workspace.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | str
     """


    return sync_detailed(
        organization_id=organization_id,
skill_id=skill_id,
client=client,

    ).parsed

async def asyncio_detailed(
    organization_id: UUID,
    skill_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | str]:
    """ Get a skill’s SKILL.md body as plain text

     Fetches the skill bundle server-side and returns SKILL.md as text/plain (extracting from a zip when
    needed). Same org-scoping as skill detail — org members can read org + platform skills; soft-deleted
    skills remain resolvable. Prefer this over fetching the signed contentUrl from the browser (GCS
    CORS).

    Args:
        organization_id (UUID): Stable organization identifier (UUID). Top-level tenant boundary.
        skill_id (UUID): Stable skill identifier (UUID). Org-uploaded or platform-curated skill
            bundle mounted into an agent workspace.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | str]
     """


    kwargs = _get_kwargs(
        organization_id=organization_id,
skill_id=skill_id,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    organization_id: UUID,
    skill_id: UUID,
    *,
    client: AuthenticatedClient | Client,

) -> TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | str | None:
    """ Get a skill’s SKILL.md body as plain text

     Fetches the skill bundle server-side and returns SKILL.md as text/plain (extracting from a zip when
    needed). Same org-scoping as skill detail — org members can read org + platform skills; soft-deleted
    skills remain resolvable. Prefer this over fetching the signed contentUrl from the browser (GCS
    CORS).

    Args:
        organization_id (UUID): Stable organization identifier (UUID). Top-level tenant boundary.
        skill_id (UUID): Stable skill identifier (UUID). Org-uploaded or platform-curated skill
            bundle mounted into an agent workspace.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        TargetApiErrorForbidden | TargetApiErrorInternalError | TargetApiErrorInvariantViolation | TargetApiErrorInvalidRequest | TargetApiErrorNotFound | TargetApiErrorRateLimitExceeded | TargetApiErrorUnauthorized | str
     """


    return (await asyncio_detailed(
        organization_id=organization_id,
skill_id=skill_id,
client=client,

    )).parsed
