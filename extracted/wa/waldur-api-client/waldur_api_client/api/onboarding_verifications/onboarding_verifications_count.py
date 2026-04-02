from http import HTTPStatus
from typing import Any, Union
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.onboarding_verification_o_enum import OnboardingVerificationOEnum
from ...models.onboarding_verification_status_enum_1 import OnboardingVerificationStatusEnum1
from ...models.onboarding_verification_validation_method_enum import OnboardingVerificationValidationMethodEnum
from ...types import UNSET, Response, Unset


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
        "method": "head",
        "url": "/api/onboarding-verifications/",
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
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

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
        Response[int]
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
) -> int:
    """Get number of items in the collection matching the request parameters.

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
        int
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
) -> Response[int]:
    """Get number of items in the collection matching the request parameters.

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
        Response[int]
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
) -> int:
    """Get number of items in the collection matching the request parameters.

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
        int
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
