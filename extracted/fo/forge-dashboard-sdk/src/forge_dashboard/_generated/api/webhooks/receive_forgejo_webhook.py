from http import HTTPStatus
from typing import Any, cast
from urllib.parse import quote

import httpx

from ...client import AuthenticatedClient, Client
from ...types import Response, UNSET
from ... import errors

from ...models.error import Error
from ...models.receive_forgejo_webhook_body import ReceiveForgejoWebhookBody
from typing import cast



def _get_kwargs(
    webhook_token: str,
    *,
    body: ReceiveForgejoWebhookBody,

) -> dict[str, Any]:
    headers: dict[str, Any] = {}


    

    

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/webhooks/forgejo/{webhook_token}".format(webhook_token=quote(str(webhook_token), safe=""),),
    }

    _kwargs["json"] = body.to_dict()

    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs



def _parse_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Any | Error | None:
    if response.status_code == 204:
        response_204 = cast(Any, None)
        return response_204

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


def _build_response(*, client: AuthenticatedClient | Client, response: httpx.Response) -> Response[Any | Error]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    webhook_token: str,
    *,
    client: AuthenticatedClient | Client,
    body: ReceiveForgejoWebhookBody,

) -> Response[Any | Error]:
    """ Receive a Forgejo repository webhook delivery

     Triggers an immediate refresh for the user webhookToken identifies,
    once the request's signature header is verified against that
    user's webhook secret — `X-Forgejo-Signature` on a webhook set up
    with the "Forgejo" type, `X-Gitea-Signature` on one set up with the
    legacy "Gitea" type; both carry the same raw hex HMAC-SHA256. Every
    delivery means the same thing here — something changed, refresh —
    so nothing about the payload itself is parsed.

    Args:
        webhook_token (str):
        body (ReceiveForgejoWebhookBody): Forgejo's own event payload — its shape isn't ours to
            describe, and nothing here reads it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = _get_kwargs(
        webhook_token=webhook_token,
body=body,

    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)

def sync(
    webhook_token: str,
    *,
    client: AuthenticatedClient | Client,
    body: ReceiveForgejoWebhookBody,

) -> Any | Error | None:
    """ Receive a Forgejo repository webhook delivery

     Triggers an immediate refresh for the user webhookToken identifies,
    once the request's signature header is verified against that
    user's webhook secret — `X-Forgejo-Signature` on a webhook set up
    with the "Forgejo" type, `X-Gitea-Signature` on one set up with the
    legacy "Gitea" type; both carry the same raw hex HMAC-SHA256. Every
    delivery means the same thing here — something changed, refresh —
    so nothing about the payload itself is parsed.

    Args:
        webhook_token (str):
        body (ReceiveForgejoWebhookBody): Forgejo's own event payload — its shape isn't ours to
            describe, and nothing here reads it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return sync_detailed(
        webhook_token=webhook_token,
client=client,
body=body,

    ).parsed

async def asyncio_detailed(
    webhook_token: str,
    *,
    client: AuthenticatedClient | Client,
    body: ReceiveForgejoWebhookBody,

) -> Response[Any | Error]:
    """ Receive a Forgejo repository webhook delivery

     Triggers an immediate refresh for the user webhookToken identifies,
    once the request's signature header is verified against that
    user's webhook secret — `X-Forgejo-Signature` on a webhook set up
    with the "Forgejo" type, `X-Gitea-Signature` on one set up with the
    legacy "Gitea" type; both carry the same raw hex HMAC-SHA256. Every
    delivery means the same thing here — something changed, refresh —
    so nothing about the payload itself is parsed.

    Args:
        webhook_token (str):
        body (ReceiveForgejoWebhookBody): Forgejo's own event payload — its shape isn't ours to
            describe, and nothing here reads it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | Error]
     """


    kwargs = _get_kwargs(
        webhook_token=webhook_token,
body=body,

    )

    response = await client.get_async_httpx_client().request(
        **kwargs
    )

    return _build_response(client=client, response=response)

async def asyncio(
    webhook_token: str,
    *,
    client: AuthenticatedClient | Client,
    body: ReceiveForgejoWebhookBody,

) -> Any | Error | None:
    """ Receive a Forgejo repository webhook delivery

     Triggers an immediate refresh for the user webhookToken identifies,
    once the request's signature header is verified against that
    user's webhook secret — `X-Forgejo-Signature` on a webhook set up
    with the "Forgejo" type, `X-Gitea-Signature` on one set up with the
    legacy "Gitea" type; both carry the same raw hex HMAC-SHA256. Every
    delivery means the same thing here — something changed, refresh —
    so nothing about the payload itself is parsed.

    Args:
        webhook_token (str):
        body (ReceiveForgejoWebhookBody): Forgejo's own event payload — its shape isn't ours to
            describe, and nothing here reads it.

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | Error
     """


    return (await asyncio_detailed(
        webhook_token=webhook_token,
client=client,
body=body,

    )).parsed
