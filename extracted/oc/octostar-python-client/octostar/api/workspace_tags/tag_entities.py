from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client, get_default_client
from ...models.entity import Entity
from ...types import Response, UNSET, Unset
from ... import errors


def _get_kwargs(
    os_workspace: str,
    *,
    client: Client = None,
    tag: str,
    json_body: List[Entity],
    color: Union[Unset, None, str] = UNSET,
    group: Union[Unset, None, str] = UNSET,
    order: Union[Unset, None, int] = UNSET,
) -> Dict[str, Any]:
    base_url = client.get_base_url_v1()
    url = f"{base_url}/api/v1/tags/{os_workspace}/{tag}"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    if not isinstance(color, Unset):
        params["color"] = color
    if not isinstance(group, Unset):
        params["group"] = group
    if not isinstance(order, Unset):
        params["order"] = order
    params = {k: v for k, v in params.items() if v is not None}

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": {"entities": [e.to_dict() for e in json_body]},
        "params": params,
    }


def _parse_response(
    *, client: Client = None, response: httpx.Response
) -> Optional[Dict[str, Any]]:
    if response.status_code == HTTPStatus.OK:
        return response.json()
    if client and client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    return None


def _build_response(
    *, client: Client = None, response: httpx.Response
) -> Response[Optional[Dict[str, Any]]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    os_workspace: str,
    *,
    client: Client = None,
    tag: str,
    json_body: List[Entity],
    color: Union[Unset, None, str] = UNSET,
    group: Union[Unset, None, str] = UNSET,
    order: Union[Unset, None, int] = UNSET,
) -> Response[Optional[Dict[str, Any]]]:
    """## Create or Update Tag

    Create a new tag or update an existing tag and associate it with entities.

    ### Args:
    * `os_workspace`: The workspace ID where the tag belongs
    * `tag`: Name or UID of the tag
    * `json_body`: List of Entity objects to tag
    * `color`: Optional hex color code for the tag (e.g. #FF5733)
    * `group`: Optional group name for tag exclusivity
    * `order`: Optional display order

    ### Returns:
    * `Response[Optional[Dict[str, Any]]]`
    """
    if not client:
        client = get_default_client()
    kwargs = _get_kwargs(
        os_workspace,
        client=client,
        tag=tag,
        json_body=json_body,
        color=color,
        group=group,
        order=order,
    )
    response = httpx.request(verify=client.verify_ssl, **kwargs)
    return _build_response(client=client, response=response)


def sync(
    os_workspace: str,
    *,
    client: Client = None,
    tag: str,
    json_body: List[Entity],
    color: Union[Unset, None, str] = UNSET,
    group: Union[Unset, None, str] = UNSET,
    order: Union[Unset, None, int] = UNSET,
) -> Optional[Dict[str, Any]]:
    """## Create or Update Tag (returns parsed body only)"""
    return sync_detailed(
        os_workspace,
        client=client,
        tag=tag,
        json_body=json_body,
        color=color,
        group=group,
        order=order,
    ).parsed


async def asyncio_detailed(
    os_workspace: str,
    *,
    client: Client = None,
    tag: str,
    json_body: List[Entity],
    color: Union[Unset, None, str] = UNSET,
    group: Union[Unset, None, str] = UNSET,
    order: Union[Unset, None, int] = UNSET,
) -> Response[Optional[Dict[str, Any]]]:
    """## Create or Update Tag (async)"""
    if not client:
        client = get_default_client()
    kwargs = _get_kwargs(
        os_workspace,
        client=client,
        tag=tag,
        json_body=json_body,
        color=color,
        group=group,
        order=order,
    )
    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    os_workspace: str,
    *,
    client: Client = None,
    tag: str,
    json_body: List[Entity],
    color: Union[Unset, None, str] = UNSET,
    group: Union[Unset, None, str] = UNSET,
    order: Union[Unset, None, int] = UNSET,
) -> Optional[Dict[str, Any]]:
    """## Create or Update Tag (async, returns parsed body only)"""
    return (
        await asyncio_detailed(
            os_workspace,
            client=client,
            tag=tag,
            json_body=json_body,
            color=color,
            group=group,
            order=order,
        )
    ).parsed
