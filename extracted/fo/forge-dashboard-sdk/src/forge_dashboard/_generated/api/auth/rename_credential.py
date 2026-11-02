from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.credential import Credential
from ...models.error import Error
from ...models.rename_credential_request import RenameCredentialRequest
from typing import cast



def _get_kwargs(
    id: str,
    *,
    body: RenameCredentialRequest,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "patch",
        "url": "/api/v1/auth/credentials/{id}".format(id=quote(str(id), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Credential | Error | None:
    if response.status_code == 200:
        response_200 = Credential.from_dict(response.json())



        return response_200

    if response.status_code == 400:
        response_400 = Error.from_dict(response.json())



        return response_400

    if response.status_code == 401:
        response_401 = Error.from_dict(response.json())



        return response_401

    if response.status_code == 404:
        response_404 = Error.from_dict(response.json())



        return response_404

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
    id: str,
    *,
    client: AuthenticatedClient,
    body: RenameCredentialRequest,

) -> Response[Credential | Error]:
    """ Rename one of the signed-in user's own passkeys

     Changes the name a passkey is listed under, so several can be told
    apart (a password manager and a security key, say). The name is
    trimmed first, then must be 1 to 64 characters. It is a plain label:
    clients show it as text, never as markup. Only the name changes;
    which passkeys can sign in does not.

    Args:
        id (str):
        body (RenameCredentialRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Credential | Error]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    id: str,
    *,
    client: AuthenticatedClient,
    body: RenameCredentialRequest,

) -> Credential | Error | None:
    """ Rename one of the signed-in user's own passkeys

     Changes the name a passkey is listed under, so several can be told
    apart (a password manager and a security key, say). The name is
    trimmed first, then must be 1 to 64 characters. It is a plain label:
    clients show it as text, never as markup. Only the name changes;
    which passkeys can sign in does not.

    Args:
        id (str):
        body (RenameCredentialRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Credential | Error
     """


    return sync_detailed(
        id=id,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    id: str,
    *,
    client: AuthenticatedClient,
    body: RenameCredentialRequest,

) -> Response[Credential | Error]:
    """ Rename one of the signed-in user's own passkeys

     Changes the name a passkey is listed under, so several can be told
    apart (a password manager and a security key, say). The name is
    trimmed first, then must be 1 to 64 characters. It is a plain label:
    clients show it as text, never as markup. Only the name changes;
    which passkeys can sign in does not.

    Args:
        id (str):
        body (RenameCredentialRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Credential | Error]
     """


    kwargs = _get_kwargs(
        id=id,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    id: str,
    *,
    client: AuthenticatedClient,
    body: RenameCredentialRequest,

) -> Credential | Error | None:
    """ Rename one of the signed-in user's own passkeys

     Changes the name a passkey is listed under, so several can be told
    apart (a password manager and a security key, say). The name is
    trimmed first, then must be 1 to 64 characters. It is a plain label:
    clients show it as text, never as markup. Only the name changes;
    which passkeys can sign in does not.

    Args:
        id (str):
        body (RenameCredentialRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Credential | Error
     """


    return (await asyncio_detailed(
        id=id,
client=client,
body=body,

    )).parsed
