from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast
from warnings import warn
import uuid

import httpx

from ...client import AuthenticatedClient, Client, get_default_client
from ...types import Response, UNSET, Unset
from ... import errors
from ...models.query_response_400 import QueryResponse400
from ...models.query_response_401 import QueryResponse401
from ...models.query_json_body import QueryJsonBody


client_missing_msg = """No client was passed to this function. The default admin client will be used, but this is deprecated and will be removed soon.
Please create a client using octostar.client.make_client() and run the function via client.execute()."""


def _get_kwargs(
    *,
    client: Client = None,
    json_body: QueryJsonBody,
    ontology: str,
    accept: Union[Unset, str] = "application/json",
) -> Dict[str, Any]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")

    base_url = client.get_base_url_v1()
    url = "{}/api/v1/ontology/query".format(base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    if not isinstance(accept, Unset):
        headers["Accept"] = accept

    params: Dict[str, Any] = {}
    params["ontology"] = ontology

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    # Translate SDK format to API format:
    # SDK uses {"query": "..."}, API expects {"query_id": "...", "sql": "..."}
    sdk_body = json_body.to_dict()
    json_json_body = {
        "query_id": uuid.uuid4().hex[:12],  # Generate 12-char hex query_id
        "sql": sdk_body.get("query", ""),  # Translate 'query' to 'sql'
    }
    # Preserve any additional params from SDK
    if sdk_body.get("params"):
        json_json_body["params"] = sdk_body["params"]

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
) -> Optional[Union[Dict[str, Any], QueryResponse400, QueryResponse401]]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    if response.status_code == HTTPStatus.OK:
        # Success case - return the query results as a dict
        return response.json()
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = QueryResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = QueryResponse401.from_dict(response.json())

        return response_401
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client = None, response: httpx.Response
) -> Response[Union[Dict[str, Any], QueryResponse400, QueryResponse401]]:
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
) -> Response[Union[Dict[str, Any], QueryResponse400, QueryResponse401]]:
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
    json_body: QueryJsonBody,
    ontology: str,
    accept: Union[Unset, str] = "application/json",
) -> Response[Union[Dict[str, Any], QueryResponse400, QueryResponse401]]:
    """## Execute SQL query

      This operation will execute the provided SQL query

    ### Args:
    * `ontology`: ontology (str):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.
    * `json_body`: json_body (QueryJsonBody): The SQL query to be executed

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Union[Dict[str, Any], QueryResponse400, QueryResponse401]]`
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        ontology=ontology,
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
    json_body: QueryJsonBody,
    ontology: str,
    accept: Union[Unset, str] = "application/json",
) -> Optional[Union[Dict[str, Any], QueryResponse400, QueryResponse401]]:
    """## Execute SQL query

      This operation will execute the provided SQL query

    ### Args:
    * `ontology`: ontology (str):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.
    * `json_body`: json_body (QueryJsonBody): The SQL query to be executed

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Union[Dict[str, Any], QueryResponse400, QueryResponse401]`
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        ontology=ontology,
        accept=accept,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client = None,
    json_body: QueryJsonBody,
    ontology: str,
    accept: Union[Unset, str] = "application/json",
) -> Response[Union[Dict[str, Any], QueryResponse400, QueryResponse401]]:
    """## Execute SQL query

      This operation will execute the provided SQL query

    ### Args:
    * `ontology`: ontology (str):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.
    * `json_body`: json_body (QueryJsonBody): The SQL query to be executed

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Union[Dict[str, Any], QueryResponse400, QueryResponse401]]`
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        ontology=ontology,
        accept=accept,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client = None,
    json_body: QueryJsonBody,
    ontology: str,
    accept: Union[Unset, str] = "application/json",
) -> Optional[Union[Dict[str, Any], QueryResponse400, QueryResponse401]]:
    """## Execute SQL query

      This operation will execute the provided SQL query

    ### Args:
    * `ontology`: ontology (str):
    * `Accept`: accept (Union[Unset, str]):  Default: 'application/json'.
    * `json_body`: json_body (QueryJsonBody): The SQL query to be executed

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Union[Dict[str, Any], QueryResponse400, QueryResponse401]`
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            ontology=ontology,
            accept=accept,
        )
    ).parsed
