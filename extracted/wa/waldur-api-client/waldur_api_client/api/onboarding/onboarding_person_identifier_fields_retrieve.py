from http import HTTPStatus
from typing import Any, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.person_identifier_fields_response import PersonIdentifierFieldsResponse
from ...models.validation_method_enum import ValidationMethodEnum
from ...types import UNSET, Response


def _get_kwargs(
    *,
    validation_method: ValidationMethodEnum,
) -> dict[str, Any]:
    params: dict[str, Any] = {}

    json_validation_method = validation_method.value
    params["validation_method"] = json_validation_method

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "get",
        "url": "/api/onboarding/person-identifier-fields/",
        "params": params,
    }

    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> PersonIdentifierFieldsResponse:
    if response.status_code == 404:
        raise errors.UnexpectedStatus(response.status_code, response.content, response.url)
    if response.status_code == 200:
        response_200 = PersonIdentifierFieldsResponse.from_dict(response.json())

        return response_200
    raise errors.UnexpectedStatus(response.status_code, response.content, response.url)


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[PersonIdentifierFieldsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    validation_method: ValidationMethodEnum,
) -> Response[PersonIdentifierFieldsResponse]:
    """Return person identifier field specification for a specific validation method. The validation_method
    parameter should match one of the available methods (e.g., 'ariregister', 'wirtschaftscompass',
    'bolagsverket', 'breg').

    Args:
        validation_method (ValidationMethodEnum):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PersonIdentifierFieldsResponse]
    """

    kwargs = _get_kwargs(
        validation_method=validation_method,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    validation_method: ValidationMethodEnum,
) -> PersonIdentifierFieldsResponse:
    """Return person identifier field specification for a specific validation method. The validation_method
    parameter should match one of the available methods (e.g., 'ariregister', 'wirtschaftscompass',
    'bolagsverket', 'breg').

    Args:
        validation_method (ValidationMethodEnum):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PersonIdentifierFieldsResponse
    """

    return sync_detailed(
        client=client,
        validation_method=validation_method,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    validation_method: ValidationMethodEnum,
) -> Response[PersonIdentifierFieldsResponse]:
    """Return person identifier field specification for a specific validation method. The validation_method
    parameter should match one of the available methods (e.g., 'ariregister', 'wirtschaftscompass',
    'bolagsverket', 'breg').

    Args:
        validation_method (ValidationMethodEnum):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[PersonIdentifierFieldsResponse]
    """

    kwargs = _get_kwargs(
        validation_method=validation_method,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    validation_method: ValidationMethodEnum,
) -> PersonIdentifierFieldsResponse:
    """Return person identifier field specification for a specific validation method. The validation_method
    parameter should match one of the available methods (e.g., 'ariregister', 'wirtschaftscompass',
    'bolagsverket', 'breg').

    Args:
        validation_method (ValidationMethodEnum):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        PersonIdentifierFieldsResponse
    """

    return (
        await asyncio_detailed(
            client=client,
            validation_method=validation_method,
        )
    ).parsed
