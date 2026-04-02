from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.onboarding_run_validation_request_request import OnboardingRunValidationRequestRequest
from ...models.onboarding_verification import OnboardingVerification
from ...types import Response


def _get_kwargs(
    uuid: UUID,
    *,
    body: OnboardingRunValidationRequestRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": f"/api/onboarding-verifications/{uuid}/run_validation/",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> OnboardingVerification:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = OnboardingVerification.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[OnboardingVerification]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: OnboardingRunValidationRequestRequest,
) -> Response[OnboardingVerification]:
    """Run automatic validation using the required fields provided during verification creation. Checklist
    answers (if any) are only used for supplemental customer/intent data.

    Args:
        uuid (UUID):
        body (OnboardingRunValidationRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OnboardingVerification]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: OnboardingRunValidationRequestRequest,
) -> OnboardingVerification:
    """Run automatic validation using the required fields provided during verification creation. Checklist
    answers (if any) are only used for supplemental customer/intent data.

    Args:
        uuid (UUID):
        body (OnboardingRunValidationRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OnboardingVerification
    """

    return sync_detailed(
        uuid=uuid,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: OnboardingRunValidationRequestRequest,
) -> Response[OnboardingVerification]:
    """Run automatic validation using the required fields provided during verification creation. Checklist
    answers (if any) are only used for supplemental customer/intent data.

    Args:
        uuid (UUID):
        body (OnboardingRunValidationRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OnboardingVerification]
    """

    kwargs = _get_kwargs(
        uuid=uuid,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    uuid: UUID,
    *,
    client: AuthenticatedClient,
    body: OnboardingRunValidationRequestRequest,
) -> OnboardingVerification:
    """Run automatic validation using the required fields provided during verification creation. Checklist
    answers (if any) are only used for supplemental customer/intent data.

    Args:
        uuid (UUID):
        body (OnboardingRunValidationRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OnboardingVerification
    """

    return (
        await asyncio_detailed(
            uuid=uuid,
            client=client,
            body=body,
        )
    ).parsed
