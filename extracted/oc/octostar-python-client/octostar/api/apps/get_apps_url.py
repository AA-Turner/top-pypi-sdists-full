"""Get app URLs from the FastAPI backend."""

from http import HTTPStatus
from typing import Any, Dict, List, Optional
from warnings import warn

import httpx
import attr

from ...client import Client, get_default_client
from ...types import Response
from ... import errors
from ...models.get_apps_url_json_body import GetAppsUrlJsonBody


client_missing_msg = """No client was passed to this function. The default admin client will be used, but this is deprecated and will be removed soon.
Please create a client using octostar.client.make_client() and run the function via client.execute()."""


@attr.s(auto_attribs=True)
class AppUrlInfo:
    """URL information for a single app."""

    app_id: str
    app_url: str
    additional_properties: Dict[str, Any] = attr.ib(init=False, factory=dict)

    @classmethod
    def from_dict(cls, src_dict: Dict[str, Any]) -> "AppUrlInfo":
        d = src_dict.copy()
        app_id = d.pop("app_id")
        app_url = d.pop("app_url")
        info = cls(app_id=app_id, app_url=app_url)
        info.additional_properties = d
        return info


def _get_kwargs(
    *,
    client: Client = None,
    json_body: GetAppsUrlJsonBody = None,
) -> Dict[str, Any]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    base_url = client.get_base_url_v1()
    url = f"{base_url}/api/v1/apps/urls"

    headers: Dict[str, str] = client.get_headers()
    headers["Content-Type"] = "application/json"
    cookies: Dict[str, Any] = client.get_cookies()

    if not json_body:
        raise ValueError("json_body is required for getting app URLs")

    # Convert to new format
    json_data = {"app_ids": json_body.app_ids}

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
) -> Optional[List[AppUrlInfo]]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    if response.status_code == HTTPStatus.OK:
        data = response.json()
        urls = data.get("urls", [])
        return [AppUrlInfo.from_dict(item) for item in urls]
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: Client = None, response: httpx.Response
) -> Response[List[AppUrlInfo]]:
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
    *,
    client: Client = None,
    json_body: GetAppsUrlJsonBody = None,
) -> Response[List[AppUrlInfo]]:
    """Get URLs for multiple apps.

    Args:
        client: The Client with which to connect to Octostar.
        json_body: GetAppsUrlJsonBody with list of app IDs.

    Returns:
        Response with list of AppUrlInfo objects.
    """
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    kwargs = _get_kwargs(client=client, json_body=json_body)

    response = httpx.request(verify=client.verify_ssl, **kwargs)
    if response.is_error:
        print(
            f"{response.status_code} Error: {response.text} for request",
            str(kwargs),
        )
    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client = None,
    json_body: GetAppsUrlJsonBody = None,
) -> Optional[List[AppUrlInfo]]:
    """Get URLs for multiple apps.

    Args:
        client: The Client with which to connect to Octostar.
        json_body: GetAppsUrlJsonBody with list of app IDs.

    Returns:
        List of AppUrlInfo objects or None if request failed.
    """
    return sync_detailed(client=client, json_body=json_body).parsed


async def asyncio_detailed(
    *,
    client: Client = None,
    json_body: GetAppsUrlJsonBody = None,
) -> Response[List[AppUrlInfo]]:
    """Get URLs for multiple apps asynchronously.

    Args:
        client: The Client with which to connect to Octostar.
        json_body: GetAppsUrlJsonBody with list of app IDs.

    Returns:
        Response with list of AppUrlInfo objects.
    """
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    kwargs = _get_kwargs(client=client, json_body=json_body)

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client = None,
    json_body: GetAppsUrlJsonBody = None,
) -> Optional[List[AppUrlInfo]]:
    """Get URLs for multiple apps asynchronously.

    Args:
        client: The Client with which to connect to Octostar.
        json_body: GetAppsUrlJsonBody with list of app IDs.

    Returns:
        List of AppUrlInfo objects or None if request failed.
    """
    return (await asyncio_detailed(client=client, json_body=json_body)).parsed
