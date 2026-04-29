from http import HTTPStatus
from typing import Any, Optional, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.error_response_400 import ErrorResponse400
from ...models.error_response_401 import ErrorResponse401
from ...models.error_response_403 import ErrorResponse403
from ...models.error_response_404 import ErrorResponse404
from ...models.organization_plan_response import OrganizationPlanResponse
from ...types import Response


def _get_kwargs(
    organization_id: UUID,
) -> dict[str, Any]:
    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/v1/organizations/{organization_id}/plan".format(
            organization_id=organization_id,
        ),
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        ErrorResponse400,
        ErrorResponse401,
        ErrorResponse403,
        ErrorResponse404,
        OrganizationPlanResponse,
    ]
]:
    if response.status_code == 200:
        response_200 = OrganizationPlanResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse400.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse401.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse403.from_dict(response.json())

        return response_403

    if response.status_code == 404:
        response_404 = ErrorResponse404.from_dict(response.json())

        return response_404

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        ErrorResponse400,
        ErrorResponse401,
        ErrorResponse403,
        ErrorResponse404,
        OrganizationPlanResponse,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    organization_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[
        ErrorResponse400,
        ErrorResponse401,
        ErrorResponse403,
        ErrorResponse404,
        OrganizationPlanResponse,
    ]
]:
    """GetOrganizationPlan


    Gets the plan for an organization.

    Returns the plan type and trial status.

    Requires READ permission on the organization level.

    Args:
        organization_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse400, ErrorResponse401, ErrorResponse403, ErrorResponse404, OrganizationPlanResponse]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    organization_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[
        ErrorResponse400,
        ErrorResponse401,
        ErrorResponse403,
        ErrorResponse404,
        OrganizationPlanResponse,
    ]
]:
    """GetOrganizationPlan


    Gets the plan for an organization.

    Returns the plan type and trial status.

    Requires READ permission on the organization level.

    Args:
        organization_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse400, ErrorResponse401, ErrorResponse403, ErrorResponse404, OrganizationPlanResponse]
    """

    return sync_detailed(
        organization_id=organization_id,
        client=client,
    ).parsed


async def asyncio_detailed(
    organization_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Response[
    Union[
        ErrorResponse400,
        ErrorResponse401,
        ErrorResponse403,
        ErrorResponse404,
        OrganizationPlanResponse,
    ]
]:
    """GetOrganizationPlan


    Gets the plan for an organization.

    Returns the plan type and trial status.

    Requires READ permission on the organization level.

    Args:
        organization_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[ErrorResponse400, ErrorResponse401, ErrorResponse403, ErrorResponse404, OrganizationPlanResponse]]
    """

    kwargs = _get_kwargs(
        organization_id=organization_id,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    organization_id: UUID,
    *,
    client: Union[AuthenticatedClient, Client],
) -> Optional[
    Union[
        ErrorResponse400,
        ErrorResponse401,
        ErrorResponse403,
        ErrorResponse404,
        OrganizationPlanResponse,
    ]
]:
    """GetOrganizationPlan


    Gets the plan for an organization.

    Returns the plan type and trial status.

    Requires READ permission on the organization level.

    Args:
        organization_id (UUID):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[ErrorResponse400, ErrorResponse401, ErrorResponse403, ErrorResponse404, OrganizationPlanResponse]
    """

    return (
        await asyncio_detailed(
            organization_id=organization_id,
            client=client,
        )
    ).parsed
