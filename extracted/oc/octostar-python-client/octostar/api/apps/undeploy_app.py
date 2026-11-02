"""Undeploy an app via the FastAPI backend."""

from http import HTTPStatus
from typing import Any, Dict, Optional
from warnings import warn

import httpx

from ...client import Client, get_default_client
from ...types import Response
from ... import errors


client_missing_msg = """No client was passed to this function. The default admin client will be used, but this is deprecated and will be removed soon.
Please create a client using octostar.client.make_client() and run the function via client.execute()."""


def _get_kwargs(
    app_id: str,
    *,
    client: Client = None,
) -> Dict[str, Any]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    base_url = client.get_base_url_v1()
    url = f"{base_url}/api/v1/apps/{app_id}"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
    }


def _parse_response(
    *, client: Client = None, response: httpx.Response
) -> Optional[Dict[str, Any]]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    # 202 Accepted: the server starts the operation and returns before it ends.
    if response.status_code in (HTTPStatus.OK, HTTPStatus.ACCEPTED):
        return response.json()
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: Client = None, response: httpx.Response
) -> Response[Dict[str, Any]]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    app_id: str,
    *,
    client: Client = None,
) -> Response[Dict[str, Any]]:
    """Undeploy an app.

    Args:
        app_id: The app ID or alias to undeploy.
        client: The Client with which to connect to Octostar.

    Returns:
        Response with undeploy confirmation including:
        - status: Operation status
        - app_id: The undeployed app ID
    """
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    kwargs = _get_kwargs(app_id=app_id, client=client)

    response = httpx.request(verify=client.verify_ssl, **kwargs)
    if response.is_error:
        print(
            f"{response.status_code} Error: {response.text} for request",
            str(kwargs),
        )
    return _build_response(client=client, response=response)


def sync(
    app_id: str,
    *,
    client: Client = None,
) -> Optional[Dict[str, Any]]:
    """Undeploy an app.

    Args:
        app_id: The app ID or alias to undeploy.
        client: The Client with which to connect to Octostar.

    Returns:
        Undeploy confirmation data or None if request failed.
    """
    return sync_detailed(app_id=app_id, client=client).parsed


async def asyncio_detailed(
    app_id: str,
    *,
    client: Client = None,
) -> Response[Dict[str, Any]]:
    """Undeploy an app asynchronously.

    Args:
        app_id: The app ID or alias to undeploy.
        client: The Client with which to connect to Octostar.

    Returns:
        Response with undeploy confirmation.
    """
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    kwargs = _get_kwargs(app_id=app_id, client=client)

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    app_id: str,
    *,
    client: Client = None,
) -> Optional[Dict[str, Any]]:
    """Undeploy an app asynchronously.

    Args:
        app_id: The app ID or alias to undeploy.
        client: The Client with which to connect to Octostar.

    Returns:
        Undeploy confirmation data or None if request failed.
    """
    return (await asyncio_detailed(app_id=app_id, client=client)).parsed
