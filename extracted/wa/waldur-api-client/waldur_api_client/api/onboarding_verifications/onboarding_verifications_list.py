from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.onboarding_verification import OnboardingVerification
from ...models.onboarding_verification_o_enum import OnboardingVerificationOEnum
from ...models.onboarding_verification_status_enum_1 import OnboardingVerificationStatusEnum1
from ...models.onboarding_verification_validation_method_enum import OnboardingVerificationValidationMethodEnum
from ...types import UNSET, Response, Unset
from ...utils import parse_link_header


def _get_kwargs(
    *,
    country: Union[Unset, str] = UNSET,
    legal_name: Union[Unset, str] = UNSET,
    legal_person_identifier: Union[Unset, str] = UNSET,
    o: Union[Unset, list[OnboardingVerificationOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    status: Union[Unset, list[OnboardingVerificationStatusEnum1]] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    validation_method: Union[Unset, list[OnboardingVerificationValidationMethodEnum]] = UNSET,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    params["country"] = country

    params["legal_name"] = legal_name

    params["legal_person_identifier"] = legal_person_identifier

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

    json_status: Union[Unset, list[str]] = UNSET
    if not isinstance(status, Unset):
        json_status = []
        for status_item_data in status:
            status_item = status_item_data.value
            json_status.append(status_item)

    params["status"] = json_status

    json_user_uuid: Union[Unset, str] = UNSET
    if not isinstance(user_uuid, Unset):
        json_user_uuid = str(user_uuid)
    params["user_uuid"] = json_user_uuid

    json_validation_method: Union[Unset, list[str]] = UNSET
    if not isinstance(validation_method, Unset):
        json_validation_method = []
        for validation_method_item_data in validation_method:
            validation_method_item = validation_method_item_data.value
            json_validation_method.append(validation_method_item)

    params["validation_method"] = json_validation_method

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/onboarding-verifications/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> list["OnboardingVerification"]:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = []
        _response_200 = response.json()
        for response_200_item_data in _response_200:
            response_200_item = OnboardingVerification.from_dict(response_200_item_data)

            response_200.append(response_200_item)

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[list["OnboardingVerification"]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    country: Union[Unset, str] = UNSET,
    legal_name: Union[Unset, str] = UNSET,
    legal_person_identifier: Union[Unset, str] = UNSET,
    o: Union[Unset, list[OnboardingVerificationOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    status: Union[Unset, list[OnboardingVerificationStatusEnum1]] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    validation_method: Union[Unset, list[OnboardingVerificationValidationMethodEnum]] = UNSET,
) -> Response[list["OnboardingVerification"]]:
    """
    Args:
        country (Union[Unset, str]):
        legal_name (Union[Unset, str]):
        legal_person_identifier (Union[Unset, str]):
        o (Union[Unset, list[OnboardingVerificationOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        status (Union[Unset, list[OnboardingVerificationStatusEnum1]]):
        user_uuid (Union[Unset, UUID]):
        validation_method (Union[Unset, list[OnboardingVerificationValidationMethodEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['OnboardingVerification']]
    """

    kwargs = _get_kwargs(
        country=country,
        legal_name=legal_name,
        legal_person_identifier=legal_person_identifier,
        o=o,
        page=page,
        page_size=page_size,
        query=query,
        status=status,
        user_uuid=user_uuid,
        validation_method=validation_method,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    country: Union[Unset, str] = UNSET,
    legal_name: Union[Unset, str] = UNSET,
    legal_person_identifier: Union[Unset, str] = UNSET,
    o: Union[Unset, list[OnboardingVerificationOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    status: Union[Unset, list[OnboardingVerificationStatusEnum1]] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    validation_method: Union[Unset, list[OnboardingVerificationValidationMethodEnum]] = UNSET,
) -> list["OnboardingVerification"]:
    """
    Args:
        country (Union[Unset, str]):
        legal_name (Union[Unset, str]):
        legal_person_identifier (Union[Unset, str]):
        o (Union[Unset, list[OnboardingVerificationOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        status (Union[Unset, list[OnboardingVerificationStatusEnum1]]):
        user_uuid (Union[Unset, UUID]):
        validation_method (Union[Unset, list[OnboardingVerificationValidationMethodEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OnboardingVerification']
    """

    return sync_detailed(
        client=client,
        country=country,
        legal_name=legal_name,
        legal_person_identifier=legal_person_identifier,
        o=o,
        page=page,
        page_size=page_size,
        query=query,
        status=status,
        user_uuid=user_uuid,
        validation_method=validation_method,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    country: Union[Unset, str] = UNSET,
    legal_name: Union[Unset, str] = UNSET,
    legal_person_identifier: Union[Unset, str] = UNSET,
    o: Union[Unset, list[OnboardingVerificationOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    status: Union[Unset, list[OnboardingVerificationStatusEnum1]] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    validation_method: Union[Unset, list[OnboardingVerificationValidationMethodEnum]] = UNSET,
) -> Response[list["OnboardingVerification"]]:
    """
    Args:
        country (Union[Unset, str]):
        legal_name (Union[Unset, str]):
        legal_person_identifier (Union[Unset, str]):
        o (Union[Unset, list[OnboardingVerificationOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        status (Union[Unset, list[OnboardingVerificationStatusEnum1]]):
        user_uuid (Union[Unset, UUID]):
        validation_method (Union[Unset, list[OnboardingVerificationValidationMethodEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[list['OnboardingVerification']]
    """

    kwargs = _get_kwargs(
        country=country,
        legal_name=legal_name,
        legal_person_identifier=legal_person_identifier,
        o=o,
        page=page,
        page_size=page_size,
        query=query,
        status=status,
        user_uuid=user_uuid,
        validation_method=validation_method,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    country: Union[Unset, str] = UNSET,
    legal_name: Union[Unset, str] = UNSET,
    legal_person_identifier: Union[Unset, str] = UNSET,
    o: Union[Unset, list[OnboardingVerificationOEnum]] = UNSET,
    page: Union[Unset, int] = UNSET,
    page_size: Union[Unset, int] = UNSET,
    query: Union[Unset, str] = UNSET,
    status: Union[Unset, list[OnboardingVerificationStatusEnum1]] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    validation_method: Union[Unset, list[OnboardingVerificationValidationMethodEnum]] = UNSET,
) -> list["OnboardingVerification"]:
    """
    Args:
        country (Union[Unset, str]):
        legal_name (Union[Unset, str]):
        legal_person_identifier (Union[Unset, str]):
        o (Union[Unset, list[OnboardingVerificationOEnum]]):
        page (Union[Unset, int]):
        page_size (Union[Unset, int]):
        query (Union[Unset, str]):
        status (Union[Unset, list[OnboardingVerificationStatusEnum1]]):
        user_uuid (Union[Unset, UUID]):
        validation_method (Union[Unset, list[OnboardingVerificationValidationMethodEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OnboardingVerification']
    """

    return (
        await asyncio_detailed(
            client=client,
            country=country,
            legal_name=legal_name,
            legal_person_identifier=legal_person_identifier,
            o=o,
            page=page,
            page_size=page_size,
            query=query,
            status=status,
            user_uuid=user_uuid,
            validation_method=validation_method,
        )
    ).parsed


def sync_all(
    *,
    client: AuthenticatedClient,
    country: Union[Unset, str] = UNSET,
    legal_name: Union[Unset, str] = UNSET,
    legal_person_identifier: Union[Unset, str] = UNSET,
    o: Union[Unset, list[OnboardingVerificationOEnum]] = UNSET,
    query: Union[Unset, str] = UNSET,
    status: Union[Unset, list[OnboardingVerificationStatusEnum1]] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    validation_method: Union[Unset, list[OnboardingVerificationValidationMethodEnum]] = UNSET,
) -> list["OnboardingVerification"]:
    """Get All Pages

     Fetch all pages of paginated results. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        country (Union[Unset, str]):
        legal_name (Union[Unset, str]):
        legal_person_identifier (Union[Unset, str]):
        o (Union[Unset, list[OnboardingVerificationOEnum]]):
        query (Union[Unset, str]):
        status (Union[Unset, list[OnboardingVerificationStatusEnum1]]):
        user_uuid (Union[Unset, UUID]):
        validation_method (Union[Unset, list[OnboardingVerificationValidationMethodEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OnboardingVerification']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[OnboardingVerification] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        country=country,
        legal_name=legal_name,
        legal_person_identifier=legal_person_identifier,
        o=o,
        query=query,
        status=status,
        user_uuid=user_uuid,
        validation_method=validation_method,
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
    country: Union[Unset, str] = UNSET,
    legal_name: Union[Unset, str] = UNSET,
    legal_person_identifier: Union[Unset, str] = UNSET,
    o: Union[Unset, list[OnboardingVerificationOEnum]] = UNSET,
    query: Union[Unset, str] = UNSET,
    status: Union[Unset, list[OnboardingVerificationStatusEnum1]] = UNSET,
    user_uuid: Union[Unset, UUID] = UNSET,
    validation_method: Union[Unset, list[OnboardingVerificationValidationMethodEnum]] = UNSET,
) -> list["OnboardingVerification"]:
    """Get All Pages (Async)

     Fetch all pages of paginated results asynchronously. This function automatically handles pagination
     by following the 'next' link in the Link header until all results are retrieved.

     Note: page_size will be set to 100 (the maximum allowed) automatically.

    Args:
        country (Union[Unset, str]):
        legal_name (Union[Unset, str]):
        legal_person_identifier (Union[Unset, str]):
        o (Union[Unset, list[OnboardingVerificationOEnum]]):
        query (Union[Unset, str]):
        status (Union[Unset, list[OnboardingVerificationStatusEnum1]]):
        user_uuid (Union[Unset, UUID]):
        validation_method (Union[Unset, list[OnboardingVerificationValidationMethodEnum]]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        list['OnboardingVerification']: Combined results from all pages
    """
    from urllib.parse import parse_qs, urlparse

    all_results: list[OnboardingVerification] = []

    # Get initial request kwargs
    kwargs = _get_kwargs(
        country=country,
        legal_name=legal_name,
        legal_person_identifier=legal_person_identifier,
        o=o,
        query=query,
        status=status,
        user_uuid=user_uuid,
        validation_method=validation_method,
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
