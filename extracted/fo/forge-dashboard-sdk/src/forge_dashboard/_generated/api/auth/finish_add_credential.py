from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.credential import Credential
from ...models.error import Error
from ...models.web_authn_ceremony_options import WebAuthnCeremonyOptions
from typing import cast



def _get_kwargs(
    *,
    body: WebAuthnCeremonyOptions,
    label: str,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    params: dict[str, Any] = {}

    params["label"] = label


    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}


    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/auth/credentials/finish",
        "params": params,
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Credential | Error | None:
    if response.status_code == 201:
        response_201 = Credential.from_dict(response.json())



        return response_201

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Credential | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: WebAuthnCeremonyOptions,
    label: str,

) -> Response[Credential | Error]:
    """ Complete an add-credential ceremony

    Args:
        label (str):
        body (WebAuthnCeremonyOptions): The WebAuthn specification's own JSON shape for
            `PublicKeyCredentialCreationOptions`/`PublicKeyCredentialRequestOptions`
            (the begin responses) and `PublicKeyCredential`
            (the finish request bodies) — passed through to and from the
            browser's own `navigator.credentials` API untouched, so this
            contract intentionally doesn't re-model WebAuthn's own schema.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Credential | Error]
     """


    kwargs = _get_kwargs(
        body=body,
label=label,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    *,
    client: AuthenticatedClient,
    body: WebAuthnCeremonyOptions,
    label: str,

) -> Credential | Error | None:
    """ Complete an add-credential ceremony

    Args:
        label (str):
        body (WebAuthnCeremonyOptions): The WebAuthn specification's own JSON shape for
            `PublicKeyCredentialCreationOptions`/`PublicKeyCredentialRequestOptions`
            (the begin responses) and `PublicKeyCredential`
            (the finish request bodies) — passed through to and from the
            browser's own `navigator.credentials` API untouched, so this
            contract intentionally doesn't re-model WebAuthn's own schema.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Credential | Error
     """


    return sync_detailed(
        client=client,
body=body,
label=label,

    ).parsed

async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: WebAuthnCeremonyOptions,
    label: str,

) -> Response[Credential | Error]:
    """ Complete an add-credential ceremony

    Args:
        label (str):
        body (WebAuthnCeremonyOptions): The WebAuthn specification's own JSON shape for
            `PublicKeyCredentialCreationOptions`/`PublicKeyCredentialRequestOptions`
            (the begin responses) and `PublicKeyCredential`
            (the finish request bodies) — passed through to and from the
            browser's own `navigator.credentials` API untouched, so this
            contract intentionally doesn't re-model WebAuthn's own schema.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Credential | Error]
     """


    kwargs = _get_kwargs(
        body=body,
label=label,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    *,
    client: AuthenticatedClient,
    body: WebAuthnCeremonyOptions,
    label: str,

) -> Credential | Error | None:
    """ Complete an add-credential ceremony

    Args:
        label (str):
        body (WebAuthnCeremonyOptions): The WebAuthn specification's own JSON shape for
            `PublicKeyCredentialCreationOptions`/`PublicKeyCredentialRequestOptions`
            (the begin responses) and `PublicKeyCredential`
            (the finish request bodies) — passed through to and from the
            browser's own `navigator.credentials` API untouched, so this
            contract intentionally doesn't re-model WebAuthn's own schema.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Credential | Error
     """


    return (await asyncio_detailed(
        client=client,
body=body,
label=label,

    )).parsed
