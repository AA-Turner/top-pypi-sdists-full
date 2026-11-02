from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.settings_request import SettingsRequest
from ...models.settings_response import SettingsResponse
from typing import cast



def _get_kwargs(
    *,
    body: SettingsRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "put",
        "url": "/api/v1/settings",
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Error | SettingsResponse | None:
    if response.status_code == 200:
        response_200 = SettingsResponse.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Error | SettingsResponse]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: SettingsRequest,

) -> Response[Error | SettingsResponse]:
    """ Save the signed-in user's forge configuration

     Replaces every field except a blank token, which means "keep
    whatever's already saved" rather than "clear it" — the only
    sensible behavior for a field the browser is never shown the
    current value of. Saving triggers that user's dashboard to start
    refreshing from the new configuration.

    Args:
        body (SettingsRequest): Replaces the signed-in user's saved GitHub/Forgejo configuration.
            A blank `githubToken` or `forgejoToken` keeps whatever token is
            already saved for that forge rather than clearing it — this is
            the only way to update the username fields without having to
            resubmit a token you don't want to re-paste. githubAppInstallationId
            is different: a plain replace like githubUsername, not coalesced —
            0 or omitted really does disconnect the App. Rejected (400) if
            the server has no GitHub App configured (see
            SettingsResponse.githubAppConfigured). Theme isn't settable
            here at all — see PUT /api/v1/settings/theme.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SettingsResponse]
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
    body: SettingsRequest,

) -> Error | SettingsResponse | None:
    """ Save the signed-in user's forge configuration

     Replaces every field except a blank token, which means "keep
    whatever's already saved" rather than "clear it" — the only
    sensible behavior for a field the browser is never shown the
    current value of. Saving triggers that user's dashboard to start
    refreshing from the new configuration.

    Args:
        body (SettingsRequest): Replaces the signed-in user's saved GitHub/Forgejo configuration.
            A blank `githubToken` or `forgejoToken` keeps whatever token is
            already saved for that forge rather than clearing it — this is
            the only way to update the username fields without having to
            resubmit a token you don't want to re-paste. githubAppInstallationId
            is different: a plain replace like githubUsername, not coalesced —
            0 or omitted really does disconnect the App. Rejected (400) if
            the server has no GitHub App configured (see
            SettingsResponse.githubAppConfigured). Theme isn't settable
            here at all — see PUT /api/v1/settings/theme.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SettingsResponse
     """


    return sync_detailed(
        client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: SettingsRequest,

) -> Response[Error | SettingsResponse]:
    """ Save the signed-in user's forge configuration

     Replaces every field except a blank token, which means "keep
    whatever's already saved" rather than "clear it" — the only
    sensible behavior for a field the browser is never shown the
    current value of. Saving triggers that user's dashboard to start
    refreshing from the new configuration.

    Args:
        body (SettingsRequest): Replaces the signed-in user's saved GitHub/Forgejo configuration.
            A blank `githubToken` or `forgejoToken` keeps whatever token is
            already saved for that forge rather than clearing it — this is
            the only way to update the username fields without having to
            resubmit a token you don't want to re-paste. githubAppInstallationId
            is different: a plain replace like githubUsername, not coalesced —
            0 or omitted really does disconnect the App. Rejected (400) if
            the server has no GitHub App configured (see
            SettingsResponse.githubAppConfigured). Theme isn't settable
            here at all — see PUT /api/v1/settings/theme.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Error | SettingsResponse]
     """


    kwargs = _get_kwargs(
        body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    body: SettingsRequest,

) -> Error | SettingsResponse | None:
    """ Save the signed-in user's forge configuration

     Replaces every field except a blank token, which means "keep
    whatever's already saved" rather than "clear it" — the only
    sensible behavior for a field the browser is never shown the
    current value of. Saving triggers that user's dashboard to start
    refreshing from the new configuration.

    Args:
        body (SettingsRequest): Replaces the signed-in user's saved GitHub/Forgejo configuration.
            A blank `githubToken` or `forgejoToken` keeps whatever token is
            already saved for that forge rather than clearing it — this is
            the only way to update the username fields without having to
            resubmit a token you don't want to re-paste. githubAppInstallationId
            is different: a plain replace like githubUsername, not coalesced —
            0 or omitted really does disconnect the App. Rejected (400) if
            the server has no GitHub App configured (see
            SettingsResponse.githubAppConfigured). Theme isn't settable
            here at all — see PUT /api/v1/settings/theme.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Error | SettingsResponse
     """


    return (await asyncio_detailed(
        client=client,
body=body,

    )).parsed
