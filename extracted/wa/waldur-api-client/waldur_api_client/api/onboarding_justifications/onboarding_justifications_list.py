from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.onboarding_justification import OnboardingJustification
from ...models.onboarding_justification_o_enum import OnboardingJustificationOEnum
from ...models.onboarding_justification_validation_decision_enum import OnboardingJustificationValidationDecisionEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


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
        "method": "get",
        "url": "/api/onboarding-justifications/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["OnboardingJustification"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = OnboardingJustification.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["OnboardingJustification"]]:
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
) -> Response[list["OnboardingJustification"]]:
    """
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
        Response[list['OnboardingJustification']]
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
) -> list["OnboardingJustification"]:
    """
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
        list['OnboardingJustification']
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
) -> Response[list["OnboardingJustification"]]:
    """
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
        Response[list['OnboardingJustification']]
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
) -> list["OnboardingJustification"]:
    """
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
        list['OnboardingJustification']
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


def sync_all(
    *,
    client: AuthenticatedClient,
    o: Union[Unset, list[OnboardingJustificationOEnum]] = UNSET,
    query: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    validation_decision: Union[Unset, list[OnboardingJustificationValidationDecisionEnum]] = UNSET,
    verification_uuid: Union[Unset, UUID] = UNSET,
) -> list["OnboardingJustification"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        o (Union[Unset, list[OnboardingJustificationOEnum]]):
        query (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):
        validation_decision (Union[Unset, list[OnboardingJustificationValidationDecisionEnum]]):
        verification_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OnboardingJustification']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[OnboardingJustification] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        o=o,
        query=query,
        user_uuid=user_uuid,
        validation_decision=validation_decision,
        verification_uuid=verification_uuid,
    )

    # Set page_size to maximum
    if "params" not in kwargs:
        kwargs["params"] = {}
    kwargs["params"]["page_size"] = 100

    # Make initial request
    response = client.get_httpx_client().request(**kwargs)
    parsed_response = _parse_response(client=client, response=response)

    if parsed_response:
        all_results.extend(parsed_response)

    # Follow pagination links
    while True:
        link_header = response.headers.get("Link", "")
        links = parse_link_header(link_header)

        if "next" not in links:
            break

        # Extract page number from next URL
        next_url = links["next"]
        parsed_url = urlparse(next_url)
        next_params = parse_qs(parsed_url.query)

        if "page" not in next_params:
            break

        # Update only the page parameter, keep all other params
        page_number = next_params["page"][0]
        kwargs["params"]["page"] = page_number

        # Fetch next page
        response = client.get_httpx_client().request(**kwargs)
        parsed_response = _parse_response(client=client, response=response)

        if parsed_response:
            all_results.extend(parsed_response)

    return all_results


async def asyncio_all(
    *,
    client: AuthenticatedClient,
    o: Union[Unset, list[OnboardingJustificationOEnum]] = UNSET,
    query: Union[Unset, str] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    validation_decision: Union[Unset, list[OnboardingJustificationValidationDecisionEnum]] = UNSET,
    verification_uuid: Union[Unset, UUID] = UNSET,
) -> list["OnboardingJustification"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        o (Union[Unset, list[OnboardingJustificationOEnum]]):
        query (Union[Unset, str]):
        user_uuid (Union[Unset, UUID]):
        validation_decision (Union[Unset, list[OnboardingJustificationValidationDecisionEnum]]):
        verification_uuid (Union[Unset, UUID]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OnboardingJustification']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[OnboardingJustification] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        o=o,
        query=query,
        user_uuid=user_uuid,
        validation_decision=validation_decision,
        verification_uuid=verification_uuid,
    )

    # Set page_size to maximum
    if "params" not in kwargs:
        kwargs["params"] = {}
    kwargs["params"]["page_size"] = 100

    # Make initial request
    response = await client.get_async_httpx_client().request(**kwargs)
    parsed_response = _parse_response(client=client, response=response)

    if parsed_response:
        all_results.extend(parsed_response)

    # Follow pagination links
    while True:
        link_header = response.headers.get("Link", "")
        links = parse_link_header(link_header)

        if "next" not in links:
            break

        # Extract page number from next URL
        next_url = links["next"]
        parsed_url = urlparse(next_url)
        next_params = parse_qs(parsed_url.query)

        if "page" not in next_params:
            break

        # Update only the page parameter, keep all other params
        page_number = next_params["page"][0]
        kwargs["params"]["page"] = page_number

        # Fetch next page
        response = await client.get_async_httpx_client().request(**kwargs)
        parsed_response = _parse_response(client=client, response=response)

        if parsed_response:
            all_results.extend(parsed_response)

    return all_results
