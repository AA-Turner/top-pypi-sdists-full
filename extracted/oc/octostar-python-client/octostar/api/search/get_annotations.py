"""SDK endpoint module for POST /v1/search_api/{ontology}/annotations."""

from http import HTTPStatus
from typing import Any, Dict, List, Optional

import httpx

from ...client import Client, get_default_client
from ...types import Response
from ... import errors


def _get_kwargs(
    *,
    client: Client,
    json_body: Dict[str, Any],
    ontology: str,
) -> Dict[str, Any]:
    base_url = client.get_base_url_v1()
    url = f"{base_url}/api/v1/search_api/{ontology}/annotations"

    headers: Dict[str, str] = client.get_headers()
    headers["Content-Type"] = "application/json"

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": client.get_cookies(),
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_body,
    }


def _parse_response(
    *, client: Client, response: httpx.Response
) -> Optional[Dict[str, Any]]:
    if response.status_code == HTTPStatus.OK:
        return response.json()
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client, response: httpx.Response
) -> Response[Dict[str, Any]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def _build_body(
    os_entity_uids: List[str],
    fields: Optional[List[str]],
    recurse: bool,
    merge: bool,
    max_fragments: Optional[int],
    fragment_filter: Optional[Dict[str, Any]],
    include_record: bool = False,
    collapse: bool = True,
    merge_kwargs: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    body: Dict[str, Any] = {
        "os_entity_uids": os_entity_uids,
        "recurse": recurse,
        "merge": merge,
        "max_fragments": max_fragments,
    }
    if fields is not None:
        body["fields"] = fields
    if fragment_filter is not None:
        body["fragment_filter"] = fragment_filter
    if include_record:
        body["include_record"] = True
    if not collapse:
        body["collapse"] = False
    if merge_kwargs:
        body["merge_kwargs"] = dict(merge_kwargs)
    return body


def sync_detailed(
    *,
    client: Client,
    os_entity_uids: List[str],
    fields: Optional[List[str]] = None,
    recurse: bool = True,
    merge: bool = True,
    max_fragments: Optional[int] = 10_000,
    fragment_filter: Optional[Dict[str, Any]] = None,
    include_record: bool = False,
    collapse: bool = True,
    merge_kwargs: Optional[Dict[str, Any]] = None,
    timeout: Optional[float] = 30.0,
) -> Response[Dict[str, Any]]:
    json_body = _build_body(
        os_entity_uids,
        fields,
        recurse,
        merge,
        max_fragments,
        fragment_filter,
        include_record,
        collapse,
        merge_kwargs,
    )
    kwargs = _get_kwargs(client=client, json_body=json_body, ontology=client.ontology)
    if timeout is not None:
        kwargs["timeout"] = timeout

    response = httpx.request(verify=client.verify_ssl, **kwargs)
    return _build_response(client=client, response=response)


async def asyncio_detailed(
    *,
    client: Client,
    os_entity_uids: List[str],
    fields: Optional[List[str]] = None,
    recurse: bool = True,
    merge: bool = True,
    max_fragments: Optional[int] = 10_000,
    fragment_filter: Optional[Dict[str, Any]] = None,
    include_record: bool = False,
    collapse: bool = True,
    merge_kwargs: Optional[Dict[str, Any]] = None,
    timeout: Optional[float] = 30.0,
) -> Response[Dict[str, Any]]:
    json_body = _build_body(
        os_entity_uids,
        fields,
        recurse,
        merge,
        max_fragments,
        fragment_filter,
        include_record,
        collapse,
        merge_kwargs,
    )
    kwargs = _get_kwargs(client=client, json_body=json_body, ontology=client.ontology)
    if timeout is not None:
        kwargs["timeout"] = timeout

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)
