from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.configuration_response import ConfigurationResponse
from ...models.error_response_400 import ErrorResponse400
from ...models.upload_configuration_bytes_body import UploadConfigurationBytesBody
from ...types import Response


def _get_kwargs(
    configuration_id: UUID,
    *,
    body: UploadConfigurationBytesBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/configurations/{configuration_id}/upload".format(
            configuration_id=quote(str(configuration_id), safe=""),
        ),
    }

    _kwargs["files"] = body.to_multipart()

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ConfigurationResponse | ErrorResponse400 | None:
    if response.status_code == 200:
        response_200 = ConfigurationResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse400.from_dict(response.json())

        return response_400

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ConfigurationResponse | ErrorResponse400]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    configuration_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UploadConfigurationBytesBody,
) -> Response[ConfigurationResponse | ErrorResponse400]:
    """UploadConfigurationBytes

     Upload configuration tarball bytes. Auth: ``DataplaneUserJwt`` with ``configuration:upload`` grant
    on the URL ``configuration_id``. Server parses the tarball, stores it + the files manifest in vault,
    then writes the row back to the CP API. Returns the freshly-created ``ConfigurationResponse``.

    Args:
        configuration_id (UUID):
        body (UploadConfigurationBytesBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConfigurationResponse | ErrorResponse400]
    """

    kwargs = _get_kwargs(
        configuration_id=configuration_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    configuration_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UploadConfigurationBytesBody,
) -> ConfigurationResponse | ErrorResponse400 | None:
    """UploadConfigurationBytes

     Upload configuration tarball bytes. Auth: ``DataplaneUserJwt`` with ``configuration:upload`` grant
    on the URL ``configuration_id``. Server parses the tarball, stores it + the files manifest in vault,
    then writes the row back to the CP API. Returns the freshly-created ``ConfigurationResponse``.

    Args:
        configuration_id (UUID):
        body (UploadConfigurationBytesBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConfigurationResponse | ErrorResponse400
    """

    return sync_detailed(
        configuration_id=configuration_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    configuration_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UploadConfigurationBytesBody,
) -> Response[ConfigurationResponse | ErrorResponse400]:
    """UploadConfigurationBytes

     Upload configuration tarball bytes. Auth: ``DataplaneUserJwt`` with ``configuration:upload`` grant
    on the URL ``configuration_id``. Server parses the tarball, stores it + the files manifest in vault,
    then writes the row back to the CP API. Returns the freshly-created ``ConfigurationResponse``.

    Args:
        configuration_id (UUID):
        body (UploadConfigurationBytesBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConfigurationResponse | ErrorResponse400]
    """

    kwargs = _get_kwargs(
        configuration_id=configuration_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    configuration_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UploadConfigurationBytesBody,
) -> ConfigurationResponse | ErrorResponse400 | None:
    """UploadConfigurationBytes

     Upload configuration tarball bytes. Auth: ``DataplaneUserJwt`` with ``configuration:upload`` grant
    on the URL ``configuration_id``. Server parses the tarball, stores it + the files manifest in vault,
    then writes the row back to the CP API. Returns the freshly-created ``ConfigurationResponse``.

    Args:
        configuration_id (UUID):
        body (UploadConfigurationBytesBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConfigurationResponse | ErrorResponse400
    """

    return (
        await asyncio_detailed(
            configuration_id=configuration_id,
            client=client,
            body=body,
        )
    ).parsed
