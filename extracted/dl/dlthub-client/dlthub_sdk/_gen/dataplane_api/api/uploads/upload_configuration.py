from http import HTTPStatus
from typing import Any
from urllib.parse import quote
from uuid import UUID

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.configuration_response import ConfigurationResponse
from ...models.error_response import ErrorResponse
from ...models.upload_configuration_body import UploadConfigurationBody
from ...types import Response


def _get_kwargs(
    workspace_id: UUID,
    configuration_id: UUID,
    *,
    body: UploadConfigurationBody,
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/workspaces/{workspace_id}/configurations/{configuration_id}/-upload".format(
            workspace_id=quote(str(workspace_id), safe=""),
            configuration_id=quote(str(configuration_id), safe=""),
        ),
    }

    _kwargs["files"] = body.to_multipart()

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> ConfigurationResponse | ErrorResponse | None:
    if response.status_code == 200:
        response_200 = ConfigurationResponse.from_dict(response.json())

        return response_200

    if response.status_code == 400:
        response_400 = ErrorResponse.from_dict(response.json())

        return response_400

    if response.status_code == 401:
        response_401 = ErrorResponse.from_dict(response.json())

        return response_401

    if response.status_code == 403:
        response_403 = ErrorResponse.from_dict(response.json())

        return response_403

    if response.status_code == 413:
        response_413 = ErrorResponse.from_dict(response.json())

        return response_413

    if response.status_code == 500:
        response_500 = ErrorResponse.from_dict(response.json())

        return response_500

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ConfigurationResponse | ErrorResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    workspace_id: UUID,
    configuration_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UploadConfigurationBody,
) -> Response[ConfigurationResponse | ErrorResponse]:
    """UploadConfigurationBytes

     Uploads the configuration package for the id you got from `configurations/-issue-upload`, using that
    call's `upload_token`. Profiles are read from `<profile>.config.toml` and `<profile>.secrets.toml`
    file names. On success the configuration is created and returned. A package that cannot be read
    answers 400; a request body over 10 MB answers 413.

    Args:
        workspace_id (UUID):
        configuration_id (UUID):
        body (UploadConfigurationBody): Multipart body with one part, `file`: the configuration
            package, a tar.gz built by dlt that contains `manifest.yaml`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConfigurationResponse | ErrorResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        configuration_id=configuration_id,
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    workspace_id: UUID,
    configuration_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UploadConfigurationBody,
) -> ConfigurationResponse | ErrorResponse | None:
    """UploadConfigurationBytes

     Uploads the configuration package for the id you got from `configurations/-issue-upload`, using that
    call's `upload_token`. Profiles are read from `<profile>.config.toml` and `<profile>.secrets.toml`
    file names. On success the configuration is created and returned. A package that cannot be read
    answers 400; a request body over 10 MB answers 413.

    Args:
        workspace_id (UUID):
        configuration_id (UUID):
        body (UploadConfigurationBody): Multipart body with one part, `file`: the configuration
            package, a tar.gz built by dlt that contains `manifest.yaml`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConfigurationResponse | ErrorResponse
    """
    return sync_detailed(
        workspace_id=workspace_id,
        configuration_id=configuration_id,
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    workspace_id: UUID,
    configuration_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UploadConfigurationBody,
) -> Response[ConfigurationResponse | ErrorResponse]:
    """UploadConfigurationBytes

     Uploads the configuration package for the id you got from `configurations/-issue-upload`, using that
    call's `upload_token`. Profiles are read from `<profile>.config.toml` and `<profile>.secrets.toml`
    file names. On success the configuration is created and returned. A package that cannot be read
    answers 400; a request body over 10 MB answers 413.

    Args:
        workspace_id (UUID):
        configuration_id (UUID):
        body (UploadConfigurationBody): Multipart body with one part, `file`: the configuration
            package, a tar.gz built by dlt that contains `manifest.yaml`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[ConfigurationResponse | ErrorResponse]
    """
    kwargs = _get_kwargs(
        workspace_id=workspace_id,
        configuration_id=configuration_id,
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace_id: UUID,
    configuration_id: UUID,
    *,
    client: AuthenticatedClient | Client,
    body: UploadConfigurationBody,
) -> ConfigurationResponse | ErrorResponse | None:
    """UploadConfigurationBytes

     Uploads the configuration package for the id you got from `configurations/-issue-upload`, using that
    call's `upload_token`. Profiles are read from `<profile>.config.toml` and `<profile>.secrets.toml`
    file names. On success the configuration is created and returned. A package that cannot be read
    answers 400; a request body over 10 MB answers 413.

    Args:
        workspace_id (UUID):
        configuration_id (UUID):
        body (UploadConfigurationBody): Multipart body with one part, `file`: the configuration
            package, a tar.gz built by dlt that contains `manifest.yaml`.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        ConfigurationResponse | ErrorResponse
    """
    return (
        await asyncio_detailed(
            workspace_id=workspace_id,
            configuration_id=configuration_id,
            client=client,
            body=body,
        )
    ).parsed
