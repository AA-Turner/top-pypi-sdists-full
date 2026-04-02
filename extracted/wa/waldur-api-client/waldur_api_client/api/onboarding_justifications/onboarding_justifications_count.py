from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.onboarding_justification_o_enum import OnboardingJustificationOEnum
from ...models.onboarding_justification_validation_decision_enum import OnboardingJustificationValidationDecisionEnum
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    o: Union[Unset, list[OnboardingJustificationOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    validation_decision: Union[Unset, list[OnboardingJustificationValidationDecisionEnum]] = UNSET,
    verification_uuid: Union[Unset, UUID] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_o: Union[Unset, list[str]] = UNSET
    if not isinstance(o, Unset):
        json_o = []
        for o_item_data in o:
            o_item = o_item_data.value
            json_o.append(o_item)

    params["o"] = json_o

    params["page"] = page

    params["page_size"] = page_size

    params["query"] = query

    json_user_uuid: Union[Unset, str] = UNSET
    if not isinstance(user_uuid, Unset):
        json_user_uuid = str(user_uuid)
    params["user_uuid"] = json_user_uuid

    json_validation_decision: Union[Unset, list[str]] = UNSET
    if not isinstance(validation_decision, Unset):
        json_validation_decision = []
        for validation_decision_item_data in validation_decision:
            validation_decision_item = validation_decision_item_data.value
            json_validation_decision.append(validation_decision_item)

    params["validation_decision"] = json_validation_decision

    json_verification_uuid: Union[Unset, str] = UNSET
    if not isinstance(verification_uuid, Unset):
        json_verification_uuid = str(verification_uuid)
    params["verification_uuid"] = json_verification_uuid

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "head",
        "url": "/api/onboarding-justifications/",
        "params": params,
    }

    return _kwargs


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> int:
    if response.status_code == HTTPStatus.OK:
        try:
            return int(response.headers["x-result-count"])
        except KeyError:
            raise errors.UnexpectedStatus(
                response.status_code,
                b"Expected 'X-Result-Count' header for HEAD request, but it was not found.",
                response.url,
            )
        except ValueError:
            count_val = response.headers.get("x-result-count")
            msg = f"Expected 'X-Result-Count' header to be an integer, but got '{count_val}'."
            raise errors.UnexpectedStatus(response.status_code, msg.encode(), response.url)
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[int]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    o: Union[Unset, list[OnboardingJustificationOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    validation_decision: Union[Unset, list[OnboardingJustificationValidationDecisionEnum]] = UNSET,
    verification_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        o (Union[Unset, list[OnboardingJustificationOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):
        validation_decision (Union[Unset, list[OnboardingJustificationValidationDecisionEnum]]):
        verification_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        o=o,
        page=page,
        page_size=page_size,
        query=query,
        user_uuid=user_uuid,
        validation_decision=validation_decision,
        verification_uuid=verification_uuid,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    o: Union[Unset, list[OnboardingJustificationOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    validation_decision: Union[Unset, list[OnboardingJustificationValidationDecisionEnum]] = UNSET,
    verification_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        o (Union[Unset, list[OnboardingJustificationOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):
        validation_decision (Union[Unset, list[OnboardingJustificationValidationDecisionEnum]]):
        verification_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return sync_detailed(
        client=client,
        o=o,
        page=page,
        page_size=page_size,
        query=query,
        user_uuid=user_uuid,
        validation_decision=validation_decision,
        verification_uuid=verification_uuid,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    o: Union[Unset, list[OnboardingJustificationOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    validation_decision: Union[Unset, list[OnboardingJustificationValidationDecisionEnum]] = UNSET,
    verification_uuid: Union[Unset, UUID] = UNSET,
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

    Args:
        o (Union[Unset, list[OnboardingJustificationOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):
        validation_decision (Union[Unset, list[OnboardingJustificationValidationDecisionEnum]]):
        verification_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[int]
    """

    kwargs = _get_kwargs(
        o=o,
        page=page,
        page_size=page_size,
        query=query,
        user_uuid=user_uuid,
        validation_decision=validation_decision,
        verification_uuid=verification_uuid,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    o: Union[Unset, list[OnboardingJustificationOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    validation_decision: Union[Unset, list[OnboardingJustificationValidationDecisionEnum]] = UNSET,
    verification_uuid: Union[Unset, UUID] = UNSET,
) -> int:
    """Get number of items in the collection matching the request parameters.

    Args:
        o (Union[Unset, list[OnboardingJustificationOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):
        validation_decision (Union[Unset, list[OnboardingJustificationValidationDecisionEnum]]):
        verification_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        int
    """

    return (
        await asyncio_detailed(
            client=client,
            o=o,
            page=page,
            page_size=page_size,
            query=query,
            user_uuid=user_uuid,
            validation_decision=validation_decision,
            verification_uuid=verification_uuid,
        )
    ).parsed
