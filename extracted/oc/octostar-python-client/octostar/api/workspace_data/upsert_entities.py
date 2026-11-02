from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast
from warnings import warn

import httpx

from ...client import AuthenticatedClient, Client, get_default_client
from ...types import Response, UNSET
from ... import errors

from ...models.upsert_entity import UpsertEntity
from ...types import UNSET, Unset
from ...models.entity_response import EntityResponse
from typing import cast, List
from typing import Union
from typing import cast
from typing import Optional
from ...models.upsert_entities_response_401 import UpsertEntitiesResponse401
from typing import Dict


client_missing_msg = """No client was passed to this function. The default admin client will be used, but this is deprecated and will be removed soon.
Please create a client using octostar.client.make_client() and run the function via client.execute()."""


def _get_kwargs(
    *,
    client: Client = None,
    json_body: List["UpsertEntity"],
    asis: Union[Unset, None, bool] = UNSET,
    accept: Union[Unset, str] = "application/json",
) -> Dict[str, Any]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")

    base_url = client.get_base_url_v1()
    url = "{}/api/v1/entities/upsert".format(base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["Accept"] = accept

    params: Dict[str, Any] = {}
    params["asis"] = asis

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = []
    for json_body_item_data in json_body:
        json_body_item = json_body_item_data.to_dict()
        # Transform SDK format to API format:
        # SDK: {"entity": {...}, "relationships": [...]}
        # API: flat entity with entity_id, entity_type fields
        if "entity" in json_body_item:
            # Flatten: extract entity fields to top level
            entity_data = json_body_item["entity"]
            # Keep relationships if present
            if "relationships" in json_body_item:
                entity_data["relationships"] = json_body_item["relationships"]
            json_body_item = entity_data

        json_json_body.append(json_body_item)

    return {
        "method": "post",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "json": json_json_body,
        "params": params,
    }


def _parse_response(
    *, client: Client = None, response: httpx.Response
) -> Optional[Union[EntityResponse, UpsertEntitiesResponse401]]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    if response.status_code == HTTPStatus.OK:
        response_200 = EntityResponse.from_dict(response.json())

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = UpsertEntitiesResponse401.from_dict(response.json())

        return response_401
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client = None, response: httpx.Response
) -> Response[Union[EntityResponse, UpsertEntitiesResponse401]]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    response_kwargs = {
        "status_code": HTTPStatus(response.status_code),
        "content": response.content,
        "headers": response.headers,
        "parsed": _parse_response(client=client, response=response),
    }
    return Response(**response_kwargs)


def _build_chunk_response(
    *, client: Client = None, response: httpx.Response, chunk: bytes
) -> Response[Union[EntityResponse, UpsertEntitiesResponse401]]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    response_kwargs = {
        "status_code": HTTPStatus(response.status_code),
        "content": chunk,
        "headers": response.headers,
        "parsed": None,  # cannot parse incomplete chunks of data, we leave it to the user
    }
    return Response(**response_kwargs)


def sync_detailed(
    *,
    client: Client = None,
    json_body: List["UpsertEntity"],
    asis: Union[Unset, None, bool] = UNSET,
    accept: Union[Unset, str] = "application/json",
) -> Response[Union[EntityResponse, UpsertEntitiesResponse401]]:
    """## Insert / Update entities operation

      This operation will upsert local entities

    ### Args:
    * `asis`: asis (Union[Unset, None, bool]):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.
    * `json_body`: json_body (List['UpsertEntity']):

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Union[EntityResponse, UpsertEntitiesResponse401]]`
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        asis=asis,
        accept=accept,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )
    if response.is_error:
        print(
            f"{str(response.status_code)} Error: {response.text} for request",
            str(kwargs),
        )
    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client = None,
    json_body: List["UpsertEntity"],
    asis: Union[Unset, None, bool] = UNSET,
    accept: Union[Unset, str] = "application/json",
) -> Optional[Union[EntityResponse, UpsertEntitiesResponse401]]:
    """## Insert / Update entities operation

      This operation will upsert local entities

    ### Args:
    * `asis`: asis (Union[Unset, None, bool]):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.
    * `json_body`: json_body (List['UpsertEntity']):

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Union[EntityResponse, UpsertEntitiesResponse401]`
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        asis=asis,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client = None,
    json_body: List["UpsertEntity"],
    asis: Union[Unset, None, bool] = UNSET,
    accept: Union[Unset, str] = "application/json",
) -> Response[Union[EntityResponse, UpsertEntitiesResponse401]]:
    """## Insert / Update entities operation

      This operation will upsert local entities

    ### Args:
    * `asis`: asis (Union[Unset, None, bool]):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.
    * `json_body`: json_body (List['UpsertEntity']):

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Union[EntityResponse, UpsertEntitiesResponse401]]`
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        asis=asis,
        accept=accept,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client = None,
    json_body: List["UpsertEntity"],
    asis: Union[Unset, None, bool] = UNSET,
    accept: Union[Unset, str] = "application/json",
) -> Optional[Union[EntityResponse, UpsertEntitiesResponse401]]:
    """## Insert / Update entities operation

      This operation will upsert local entities

    ### Args:
    * `asis`: asis (Union[Unset, None, bool]):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.
    * `json_body`: json_body (List['UpsertEntity']):

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Union[EntityResponse, UpsertEntitiesResponse401]`
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            asis=asis,
            accept=accept,
        )
    ).parsed
