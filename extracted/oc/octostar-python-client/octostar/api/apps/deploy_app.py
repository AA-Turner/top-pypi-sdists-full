"""Deploy an app via the FastAPI backend."""

from http import HTTPStatus
from typing import Any, Dict, Optional, Union
from warnings import warn

import httpx

from ...client import Client, get_default_client
from ...types import Response, UNSET, Unset
from ... import errors
from ...models.deploy_app_json_body import DeployAppJsonBody


client_missing_msg = """No client was passed to this function. The default admin client will be used, but this is deprecated and will be removed soon.
Please create a client using octostar.client.make_client() and run the function via client.execute()."""


def _get_kwargs(
    workspace: str,
    os_entity_uid: str,
    *,
    client: Client = None,
    json_body: DeployAppJsonBody = None,
) -> Dict[str, Any]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    base_url = client.get_base_url_v1()
    url = f"{base_url}/api/v1/apps/deploy/{workspace}/{os_entity_uid}"

    headers: Dict[str, str] = client.get_headers()
    headers["Content-Type"] = "application/json"
    cookies: Dict[str, Any] = client.get_cookies()

    # Convert the old DeployAppJsonBody to the new format
    json_data = None
    if json_body:
        body_dict = json_body.to_dict()
        if body_dict.get("secrets"):
            json_data = {"secrets": body_dict["secrets"]}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_data,
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
    workspace: str,
    os_entity_uid: str,
    *,
    client: Client = None,
    json_body: DeployAppJsonBody = None,
) -> Response[Dict[str, Any]]:
    """Deploy an app from a manifest.

    Args:
        workspace: The workspace ID containing the app folder.
        os_entity_uid: The entity ID of the app folder.
        client: The Client with which to connect to Octostar.
        json_body: Optional DeployAppJsonBody with secrets.

    Returns:
        Response with deployment data including:
        - status: "success" or "error"
        - data: Updated app entity data
    """
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    kwargs = _get_kwargs(
        workspace=workspace,
        os_entity_uid=os_entity_uid,
        client=client,
        json_body=json_body,
    )

    response = httpx.request(verify=client.verify_ssl, **kwargs)
    if response.is_error:
        print(
            f"{response.status_code} Error: {response.text} for request",
            str(kwargs),
        )
    return _build_response(client=client, response=response)


def sync(
    workspace: str,
    os_entity_uid: str,
    *,
    client: Client = None,
    json_body: DeployAppJsonBody = None,
) -> Optional[Dict[str, Any]]:
    """Deploy an app from a manifest.

    Args:
        workspace: The workspace ID containing the app folder.
        os_entity_uid: The entity ID of the app folder.
        client: The Client with which to connect to Octostar.
        json_body: Optional DeployAppJsonBody with secrets.

    Returns:
        Deployment data or None if request failed.
    """
    return sync_detailed(
        workspace=workspace,
        os_entity_uid=os_entity_uid,
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(
    workspace: str,
    os_entity_uid: str,
    *,
    client: Client = None,
    json_body: DeployAppJsonBody = None,
) -> Response[Dict[str, Any]]:
    """Deploy an app from a manifest asynchronously.

    Args:
        workspace: The workspace ID containing the app folder.
        os_entity_uid: The entity ID of the app folder.
        client: The Client with which to connect to Octostar.
        json_body: Optional DeployAppJsonBody with secrets.

    Returns:
        Response with deployment data.
    """
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    kwargs = _get_kwargs(
        workspace=workspace,
        os_entity_uid=os_entity_uid,
        client=client,
        json_body=json_body,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    workspace: str,
    os_entity_uid: str,
    *,
    client: Client = None,
    json_body: DeployAppJsonBody = None,
) -> Optional[Dict[str, Any]]:
    """Deploy an app from a manifest asynchronously.

    Args:
        workspace: The workspace ID containing the app folder.
        os_entity_uid: The entity ID of the app folder.
        client: The Client with which to connect to Octostar.
        json_body: Optional DeployAppJsonBody with secrets.

    Returns:
        Deployment data or None if request failed.
    """
    return (
        await asyncio_detailed(
            workspace=workspace,
            os_entity_uid=os_entity_uid,
            client=client,
            json_body=json_body,
        )
    ).parsed
