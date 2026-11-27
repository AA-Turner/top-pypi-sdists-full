from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.update_token_limits_json_body import UpdateTokenLimitsJsonBody
from ...types import Response


def _get_kwargs(
    token_prefix: str,
    *,
    json_body: UpdateTokenLimitsJsonBody,
) -> Dict[str, Any]:
    pass

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/users/tokens/update_limits/{token_prefix}".format(
            token_prefix=token_prefix,
        ),
        "json": json_json_body,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    token_prefix: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateTokenLimitsJsonBody,
) -> Response[Any]:
    """update expiration and allowed IPs of an existing token (owner only)

     Tightening (an earlier expiration, a narrower IP list) is always allowed on a token you
    created. Widening is allowed only as far as the calling token could mint a new token
    with the same rights, and a later expiration is capped by `max_token_expiration_days`.

    Args:
        token_prefix (str):
        json_body (UpdateTokenLimitsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        token_prefix=token_prefix,
        json_body=json_body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


async def asyncio_detailed(
    token_prefix: str,
    *,
    client: Union[AuthenticatedClient, Client],
    json_body: UpdateTokenLimitsJsonBody,
) -> Response[Any]:
    """update expiration and allowed IPs of an existing token (owner only)

     Tightening (an earlier expiration, a narrower IP list) is always allowed on a token you
    created. Widening is allowed only as far as the calling token could mint a new token
    with the same rights, and a later expiration is capped by `max_token_expiration_days`.

    Args:
        token_prefix (str):
        json_body (UpdateTokenLimitsJsonBody):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any]
    """

    kwargs = _get_kwargs(
        token_prefix=token_prefix,
        json_body=json_body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)
