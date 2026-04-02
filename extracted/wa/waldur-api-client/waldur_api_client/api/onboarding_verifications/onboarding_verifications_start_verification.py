from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.onboarding_company_validation_request_request import OnboardingCompanyValidationRequestRequest
from ...models.onboarding_verification import OnboardingVerification
from ...types import Response


def _get_kwargs(
    *,
    body: OnboardingCompanyValidationRequestRequest,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/onboarding-verifications/start_verification/",
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
    *,
    client: AuthenticatedClient,
    body: OnboardingCompanyValidationRequestRequest,
) -> Response[OnboardingVerification]:
    """Start company validation process by creating a verification record. User selects validation_method
    (e.g., 'ariregister', 'wirtschaftscompass'). Checklists are used for intent and customer data
    collection. Then call run_validation to perform automatic validation or create manual justification.

    Args:
        body (OnboardingCompanyValidationRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OnboardingVerification]
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
    client: AuthenticatedClient,
    body: OnboardingCompanyValidationRequestRequest,
) -> OnboardingVerification:
    """Start company validation process by creating a verification record. User selects validation_method
    (e.g., 'ariregister', 'wirtschaftscompass'). Checklists are used for intent and customer data
    collection. Then call run_validation to perform automatic validation or create manual justification.

    Args:
        body (OnboardingCompanyValidationRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OnboardingVerification
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: OnboardingCompanyValidationRequestRequest,
) -> Response[OnboardingVerification]:
    """Start company validation process by creating a verification record. User selects validation_method
    (e.g., 'ariregister', 'wirtschaftscompass'). Checklists are used for intent and customer data
    collection. Then call run_validation to perform automatic validation or create manual justification.

    Args:
        body (OnboardingCompanyValidationRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[OnboardingVerification]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: OnboardingCompanyValidationRequestRequest,
) -> OnboardingVerification:
    """Start company validation process by creating a verification record. User selects validation_method
    (e.g., 'ariregister', 'wirtschaftscompass'). Checklists are used for intent and customer data
    collection. Then call run_validation to perform automatic validation or create manual justification.

    Args:
        body (OnboardingCompanyValidationRequestRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        OnboardingVerification
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
