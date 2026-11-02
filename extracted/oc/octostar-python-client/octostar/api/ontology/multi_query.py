from http import HTTPStatus
from typing import Any, Dict, List, Optional, Union, cast
from warnings import warn

import httpx

from ...client import AuthenticatedClient, Client, get_default_client
from ...types import Response, UNSET
from ... import errors

from ...models.multi_query_response_400 import MultiQueryResponse400
from ...models.multi_query_json_body import MultiQueryJsonBody
from ...models.multi_query_response_401 import MultiQueryResponse401
from typing import cast
from typing import Dict


client_missing_msg = """No client was passed to this function. The default admin client will be used, but this is deprecated and will be removed soon.
Please create a client using octostar.client.make_client() and run the function via client.execute()."""


def _get_kwargs(
    *,
    client: Client = None,
    json_body: MultiQueryJsonBody,
    ontology: str,
) -> Dict[str, Any]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")

    base_url = client.get_base_url_v1()
    url = "{}/api/v1/ontology/multi_query".format(base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["ontology"] = ontology

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    json_json_body = json_body.to_dict()

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
) -> Optional[Union[MultiQueryResponse400, MultiQueryResponse401]]:
    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    if response.status_code == HTTPStatus.OK:
        # multi_query returns NDJSON (streaming), not a single JSON object
        response_200 = cast(Any, response.text)
        return response_200
    if response.status_code == HTTPStatus.BAD_REQUEST:
        response_400 = MultiQueryResponse400.from_dict(response.json())

        return response_400
    if response.status_code == HTTPStatus.UNAUTHORIZED:
        response_401 = MultiQueryResponse401.from_dict(response.json())

        return response_401
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Client = None, response: httpx.Response
) -> Response[Union[MultiQueryResponse400, MultiQueryResponse401]]:
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
) -> Response[Union[MultiQueryResponse400, MultiQueryResponse401]]:
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
    json_body: MultiQueryJsonBody,
    ontology: str,
) -> Response[Union[MultiQueryResponse400, MultiQueryResponse401]]:
    """## Execute a batch of SQL queries

      This operation will execute the provided SQL queries as a batch

    ### Args:
    * `ontology`: ontology (str):
    * `json_body`: json_body (MultiQueryJsonBody): The SQL queries to be executed

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Union[MultiQueryResponse400, MultiQueryResponse401]]`
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        ontology=ontology,
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
    json_body: MultiQueryJsonBody,
    ontology: str,
) -> Optional[Union[MultiQueryResponse400, MultiQueryResponse401]]:
    """## Execute a batch of SQL queries

      This operation will execute the provided SQL queries as a batch

    ### Args:
    * `ontology`: ontology (str):
    * `json_body`: json_body (MultiQueryJsonBody): The SQL queries to be executed

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Union[MultiQueryResponse400, MultiQueryResponse401]`
    """

    return sync_detailed(
        client=client,
        json_body=json_body,
        ontology=ontology,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client = None,
    json_body: MultiQueryJsonBody,
    ontology: str,
) -> Response[Union[MultiQueryResponse400, MultiQueryResponse401]]:
    """## Execute a batch of SQL queries

      This operation will execute the provided SQL queries as a batch

    ### Args:
    * `ontology`: ontology (str):
    * `json_body`: json_body (MultiQueryJsonBody): The SQL queries to be executed

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Union[MultiQueryResponse400, MultiQueryResponse401]]`
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()
        # raise RuntimeError("Missing client!")
    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        ontology=ontology,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client = None,
    json_body: MultiQueryJsonBody,
    ontology: str,
) -> Optional[Union[MultiQueryResponse400, MultiQueryResponse401]]:
    """## Execute a batch of SQL queries

      This operation will execute the provided SQL queries as a batch

    ### Args:
    * `ontology`: ontology (str):
    * `json_body`: json_body (MultiQueryJsonBody): The SQL queries to be executed

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Union[MultiQueryResponse400, MultiQueryResponse401]`
    """

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
            ontology=ontology,
        )
    ).parsed


from collections.abc import AsyncIterator


async def streaming_detailed(
    *,
    client: Client = None,
    json_body: MultiQueryJsonBody,
    ontology: str,
) -> AsyncIterator[Response[Union[MultiQueryResponse400, MultiQueryResponse401]]]:
    """## Execute a batch of SQL queries

      This operation will execute the provided SQL queries as a batch

    ### Args:
    * `ontology`: ontology (str):
    * `json_body`: json_body (MultiQueryJsonBody): The SQL queries to be executed

    ### Raises:
    * `errors.UnexpectedStatus`: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
    * `httpx.TimeoutException`: If the request takes longer than Client.timeout.

    ## Returns:
    * `Response[Union[MultiQueryResponse400, MultiQueryResponse401]]`
    """

    if not client:
        warn(client_missing_msg, FutureWarning, stacklevel=2)
        client = get_default_client()

    kwargs = _get_kwargs(
        client=client,
        json_body=json_body,
        ontology=ontology,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        async with _client.stream(**kwargs) as response:
            async for chunk in response.aiter_bytes():
                yield _build_chunk_response(
                    client=client, response=response, chunk=chunk
                )
