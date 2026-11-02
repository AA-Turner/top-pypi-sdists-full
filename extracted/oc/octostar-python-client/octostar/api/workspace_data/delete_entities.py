from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast
from urllib.parse import quote
from warnings import warn

import httpx

from ...client import AuthenticatedClient, Client, get_default_client
from ...types import Response, UNSET
from ... import errors

from ...models.delete_entities_response_409 import DeleteEntitiesResponse409
from ...models.delete_entities_response_500 import DeleteEntitiesResponse500
from ...types import UNSET, Unset
from typing import cast, List
from typing import Union
from typing import cast
from typing import Optional
from ...models.acknowledgement import Acknowledgement
from ...models.delete_entities_response_401 import DeleteEntitiesResponse401
from typing import Dict


client_missing_msg = """No client was passed to this function. The default admin client will be used, but this is deprecated and will be removed soon.
Please create a client using octostar.client.make_client() and run the function via client.execute()."""


def _get_kwargs(
    *,
    client: Client = None,
    json_body: List[str],
    recurse: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = "application/json",
) -> Dict[str, Any]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")

    base_url = client.get_base_url_v1()
    url = "{}/api/v1/entities/delete".format(base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["Accept"] = accept

    params: Dict[str, Any] = {}
    params["recurse"] = recurse
    params["entity_ids"] = ",".join(
        quote(entity_id, safe="") for entity_id in json_body
    )

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "delete",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "follow_redirects": client.follow_redirects,
        "params": params,
    }


def _parse_response(*, client: Client = None, response: httpx.Response) -> Optional[
    Union[
        Acknowledgement,
        DeleteEntitiesResponse401,
        DeleteEntitiesResponse409,
        DeleteEntitiesResponse500,
    ]
]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    if response.status_code == HTTPStatus.OK:
        data = response.json()
        response_200 = Acknowledgement.from_dict(data)

        return response_200
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = DeleteEntitiesResponse401.from_dict(response.json())

        return response_401
    if response.status_code == HTTPStatus.CONFLICT:
        response_409 = DeleteEntitiesResponse409.from_dict(response.json())

        return response_409
    if response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR:
        response_500 = DeleteEntitiesResponse500.from_dict(response.json())

        return response_500
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Client = None, response: httpx.Response) -> Response[
    Union[
        Acknowledgement,
        DeleteEntitiesResponse401,
        DeleteEntitiesResponse409,
        DeleteEntitiesResponse500,
    ]
]:
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
) -> Response[
    Union[
        Acknowledgement,
        DeleteEntitiesResponse401,
        DeleteEntitiesResponse409,
        DeleteEntitiesResponse500,
    ]
]:
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
    json_body: List[str],
    recurse: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = "application/json",
) -> Response[
    Union[
        Acknowledgement,
        DeleteEntitiesResponse401,
        DeleteEntitiesResponse409,
        DeleteEntitiesResponse500,
    ]
]:
    """## Delete entity operation

      This operation will delete entities given their IDs

    ### Args:
    * `recurse`: recurse (Union[Unset, None, bool]):  Example: True.
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.
    * `json_body`: json_body (List[str]): The list of entity wso_ids to delete

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Union[Acknowledgement, DeleteEntitiesResponse401, DeleteEntitiesResponse409, DeleteEntitiesResponse500]]`
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        recurse=recurse,
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
    json_body: List[str],
    recurse: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = "application/json",
) -> Optional[
    Union[
        Acknowledgement,
        DeleteEntitiesResponse401,
        DeleteEntitiesResponse409,
        DeleteEntitiesResponse500,
    ]
]:
    """## Delete entity operation

      This operation will delete entities given their IDs

    ### Args:
    * `recurse`: recurse (Union[Unset, None, bool]):  Example: True.
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.
    * `json_body`: json_body (List[str]): The list of entity wso_ids to delete

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Union[Acknowledgement, DeleteEntitiesResponse401, DeleteEntitiesResponse409, DeleteEntitiesResponse500]`
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        recurse=recurse,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client = None,
    json_body: List[str],
    recurse: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = "application/json",
) -> Response[
    Union[
        Acknowledgement,
        DeleteEntitiesResponse401,
        DeleteEntitiesResponse409,
        DeleteEntitiesResponse500,
    ]
]:
    """## Delete entity operation

      This operation will delete entities given their IDs

    ### Args:
    * `recurse`: recurse (Union[Unset, None, bool]):  Example: True.
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.
    * `json_body`: json_body (List[str]): The list of entity wso_ids to delete

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Union[Acknowledgement, DeleteEntitiesResponse401, DeleteEntitiesResponse409, DeleteEntitiesResponse500]]`
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        recurse=recurse,
        accept=accept,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client = None,
    json_body: List[str],
    recurse: Union[Unset, None, bool] = False,
    accept: Union[Unset, str] = "application/json",
) -> Optional[
    Union[
        Acknowledgement,
        DeleteEntitiesResponse401,
        DeleteEntitiesResponse409,
        DeleteEntitiesResponse500,
    ]
]:
    """## Delete entity operation

      This operation will delete entities given their IDs

    ### Args:
    * `recurse`: recurse (Union[Unset, None, bool]):  Example: True.
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.
    * `json_body`: json_body (List[str]): The list of entity wso_ids to delete

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Union[Acknowledgement, DeleteEntitiesResponse401, DeleteEntitiesResponse409, DeleteEntitiesResponse500]`
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            recurse=recurse,
            accept=accept,
        )
    ).parsed
