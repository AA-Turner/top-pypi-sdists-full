from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client, get_default_client
from ...models.entity import Entity
from ...types import Response, UNSET, Unset
from ... import errors


def _get_kwargs(
    os_workspace: str,
    tag: str,
    *,
    client: Client = None,
    json_body: List[Entity],
    group: Union[Unset, None, str] = UNSET,
) -> Dict[str, Any]:
    base_url = client.get_base_url_v1()
    url = f"{base_url}/api/v1/tags/{os_workspace}/{tag}"

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    if not isinstance(group, Unset):
        params["group"] = group
    params = {k: v for k, v in params.items() if v is not None}

    return {
        "method": "delete",
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
    tag: str,
    *,
    client: Client = None,
    json_body: List[Entity],
    group: Union[Unset, None, str] = UNSET,
) -> Response[Optional[Dict[str, Any]]]:
    """## Delete Tag Relationships

    Remove tag associations from entities. Does NOT delete the tag entity itself,
    only the has_tag relationships.

    ### Args:
    * `os_workspace`: The workspace ID where the tag belongs
    * `tag`: Name or UID of the tag
    * `json_body`: List of Entity objects to untag
    * `group`: Optional group name for tag matching

    ### Returns:
    * `Response[Optional[Dict[str, Any]]]`
    """
    if not client:
        client = get_default_client()
    kwargs = _get_kwargs(
        os_workspace, tag, client=client, json_body=json_body, group=group
    )
    response = httpx.request(verify=client.verify_ssl, **kwargs)
    return _build_response(client=client, response=response)


def sync(
    os_workspace: str,
    tag: str,
    *,
    client: Client = None,
    json_body: List[Entity],
    group: Union[Unset, None, str] = UNSET,
) -> Optional[Dict[str, Any]]:
    """## Delete Tag Relationships (returns parsed body only)"""
    return sync_detailed(
        os_workspace, tag, client=client, json_body=json_body, group=group
    ).parsed


async def asyncio_detailed(
    os_workspace: str,
    tag: str,
    *,
    client: Client = None,
    json_body: List[Entity],
    group: Union[Unset, None, str] = UNSET,
) -> Response[Optional[Dict[str, Any]]]:
    """## Delete Tag Relationships (async)"""
    if not client:
        client = get_default_client()
    kwargs = _get_kwargs(
        os_workspace, tag, client=client, json_body=json_body, group=group
    )
    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(
    os_workspace: str,
    tag: str,
    *,
    client: Client = None,
    json_body: List[Entity],
    group: Union[Unset, None, str] = UNSET,
) -> Optional[Dict[str, Any]]:
    """## Delete Tag Relationships (async, returns parsed body only)"""
    return (
        await asyncio_detailed(
            os_workspace, tag, client=client, json_body=json_body, group=group
        )
    ).parsed
