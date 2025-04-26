from typing import Any, Dict, List, Optional, Union

import httpx

from ...client import Client
from ...models.bad_request_error import BadRequestError
from ...models.connection_files_paginated_list import ConnectionFilesPaginatedList
from ...models.list_connect_files_data_type import ListConnectFilesDataType
from ...types import Response, UNSET, Unset


def _get_kwargs(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    created_atlt: Union[Unset, str] = UNSET,
    created_atgt: Union[Unset, str] = UNSET,
    created_atlte: Union[Unset, str] = UNSET,
    created_atgte: Union[Unset, str] = UNSET,
    modified_atlt: Union[Unset, str] = UNSET,
    modified_atgt: Union[Unset, str] = UNSET,
    modified_atlte: Union[Unset, str] = UNSET,
    modified_atgte: Union[Unset, str] = UNSET,
    filename_includes: Union[Unset, str] = UNSET,
    connection_ids: Union[Unset, List[str]] = UNSET,
    connection_schema_ids: Union[Unset, List[str]] = UNSET,
    data_type: Union[Unset, ListConnectFilesDataType] = UNSET,
) -> Dict[str, Any]:
    url = "{}/benchling-connect/connection-files".format(client.base_url)

    headers: Dict[str, Any] = client.httpx_client.headers
    headers.update(client.get_headers())

    cookies: Dict[str, Any] = client.httpx_client.cookies
    cookies.update(client.get_cookies())

    json_connection_ids: Union[Unset, List[Any]] = UNSET
    if not isinstance(connection_ids, Unset):
        json_connection_ids = connection_ids

    json_connection_schema_ids: Union[Unset, List[Any]] = UNSET
    if not isinstance(connection_schema_ids, Unset):
        json_connection_schema_ids = connection_schema_ids

    json_data_type: Union[Unset, int] = UNSET
    if not isinstance(data_type, Unset):
        json_data_type = data_type.value

    params: Dict[str, Any] = {}
    if not isinstance(page_size, Unset) and page_size is not None:
        params["pageSize"] = page_size
    if not isinstance(next_token, Unset) and next_token is not None:
        params["nextToken"] = next_token
    if not isinstance(created_atlt, Unset) and created_atlt is not None:
        params["createdAt.lt"] = created_atlt
    if not isinstance(created_atgt, Unset) and created_atgt is not None:
        params["createdAt.gt"] = created_atgt
    if not isinstance(created_atlte, Unset) and created_atlte is not None:
        params["createdAt.lte"] = created_atlte
    if not isinstance(created_atgte, Unset) and created_atgte is not None:
        params["createdAt.gte"] = created_atgte
    if not isinstance(modified_atlt, Unset) and modified_atlt is not None:
        params["modifiedAt.lt"] = modified_atlt
    if not isinstance(modified_atgt, Unset) and modified_atgt is not None:
        params["modifiedAt.gt"] = modified_atgt
    if not isinstance(modified_atlte, Unset) and modified_atlte is not None:
        params["modifiedAt.lte"] = modified_atlte
    if not isinstance(modified_atgte, Unset) and modified_atgte is not None:
        params["modifiedAt.gte"] = modified_atgte
    if not isinstance(filename_includes, Unset) and filename_includes is not None:
        params["filenameIncludes"] = filename_includes
    if not isinstance(json_connection_ids, Unset) and json_connection_ids is not None:
        params["connectionIds"] = json_connection_ids
    if not isinstance(json_connection_schema_ids, Unset) and json_connection_schema_ids is not None:
        params["connectionSchemaIds"] = json_connection_schema_ids
    if not isinstance(json_data_type, Unset) and json_data_type is not None:
        params["dataType"] = json_data_type

    return {
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(
    *, response: httpx.Response
) -> Optional[Union[ConnectionFilesPaginatedList, BadRequestError]]:
    if response.status_code == 200:
        response_200 = ConnectionFilesPaginatedList.from_dict(response.json(), strict=False)

        return response_200
    if response.status_code == 400:
        response_400 = BadRequestError.from_dict(response.json(), strict=False)

        return response_400
    return None


def _build_response(
    *, response: httpx.Response
) -> Response[Union[ConnectionFilesPaginatedList, BadRequestError]]:
    return Response(
        status_code=response.status_code,
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(response=response),
    )


def sync_detailed(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    created_atlt: Union[Unset, str] = UNSET,
    created_atgt: Union[Unset, str] = UNSET,
    created_atlte: Union[Unset, str] = UNSET,
    created_atgte: Union[Unset, str] = UNSET,
    modified_atlt: Union[Unset, str] = UNSET,
    modified_atgt: Union[Unset, str] = UNSET,
    modified_atlte: Union[Unset, str] = UNSET,
    modified_atgte: Union[Unset, str] = UNSET,
    filename_includes: Union[Unset, str] = UNSET,
    connection_ids: Union[Unset, List[str]] = UNSET,
    connection_schema_ids: Union[Unset, List[str]] = UNSET,
    data_type: Union[Unset, ListConnectFilesDataType] = UNSET,
) -> Response[Union[ConnectionFilesPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        created_atlt=created_atlt,
        created_atgt=created_atgt,
        created_atlte=created_atlte,
        created_atgte=created_atgte,
        modified_atlt=modified_atlt,
        modified_atgt=modified_atgt,
        modified_atlte=modified_atlte,
        modified_atgte=modified_atgte,
        filename_includes=filename_includes,
        connection_ids=connection_ids,
        connection_schema_ids=connection_schema_ids,
        data_type=data_type,
    )

    response = client.httpx_client.get(
        **kwargs,
    )

    return _build_response(response=response)


def sync(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    created_atlt: Union[Unset, str] = UNSET,
    created_atgt: Union[Unset, str] = UNSET,
    created_atlte: Union[Unset, str] = UNSET,
    created_atgte: Union[Unset, str] = UNSET,
    modified_atlt: Union[Unset, str] = UNSET,
    modified_atgt: Union[Unset, str] = UNSET,
    modified_atlte: Union[Unset, str] = UNSET,
    modified_atgte: Union[Unset, str] = UNSET,
    filename_includes: Union[Unset, str] = UNSET,
    connection_ids: Union[Unset, List[str]] = UNSET,
    connection_schema_ids: Union[Unset, List[str]] = UNSET,
    data_type: Union[Unset, ListConnectFilesDataType] = UNSET,
) -> Optional[Union[ConnectionFilesPaginatedList, BadRequestError]]:
    """ List Benchling Connect files """

    return sync_detailed(
        client=client,
        page_size=page_size,
        next_token=next_token,
        created_atlt=created_atlt,
        created_atgt=created_atgt,
        created_atlte=created_atlte,
        created_atgte=created_atgte,
        modified_atlt=modified_atlt,
        modified_atgt=modified_atgt,
        modified_atlte=modified_atlte,
        modified_atgte=modified_atgte,
        filename_includes=filename_includes,
        connection_ids=connection_ids,
        connection_schema_ids=connection_schema_ids,
        data_type=data_type,
    ).parsed


async def asyncio_detailed(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    created_atlt: Union[Unset, str] = UNSET,
    created_atgt: Union[Unset, str] = UNSET,
    created_atlte: Union[Unset, str] = UNSET,
    created_atgte: Union[Unset, str] = UNSET,
    modified_atlt: Union[Unset, str] = UNSET,
    modified_atgt: Union[Unset, str] = UNSET,
    modified_atlte: Union[Unset, str] = UNSET,
    modified_atgte: Union[Unset, str] = UNSET,
    filename_includes: Union[Unset, str] = UNSET,
    connection_ids: Union[Unset, List[str]] = UNSET,
    connection_schema_ids: Union[Unset, List[str]] = UNSET,
    data_type: Union[Unset, ListConnectFilesDataType] = UNSET,
) -> Response[Union[ConnectionFilesPaginatedList, BadRequestError]]:
    kwargs = _get_kwargs(
        client=client,
        page_size=page_size,
        next_token=next_token,
        created_atlt=created_atlt,
        created_atgt=created_atgt,
        created_atlte=created_atlte,
        created_atgte=created_atgte,
        modified_atlt=modified_atlt,
        modified_atgt=modified_atgt,
        modified_atlte=modified_atlte,
        modified_atgte=modified_atgte,
        filename_includes=filename_includes,
        connection_ids=connection_ids,
        connection_schema_ids=connection_schema_ids,
        data_type=data_type,
    )

    async with httpx.AsyncClient() as _client:
        response = await _client.get(**kwargs)

    return _build_response(response=response)


async def asyncio(
    *,
    client: Client,
    page_size: Union[Unset, int] = 50,
    next_token: Union[Unset, str] = UNSET,
    created_atlt: Union[Unset, str] = UNSET,
    created_atgt: Union[Unset, str] = UNSET,
    created_atlte: Union[Unset, str] = UNSET,
    created_atgte: Union[Unset, str] = UNSET,
    modified_atlt: Union[Unset, str] = UNSET,
    modified_atgt: Union[Unset, str] = UNSET,
    modified_atlte: Union[Unset, str] = UNSET,
    modified_atgte: Union[Unset, str] = UNSET,
    filename_includes: Union[Unset, str] = UNSET,
    connection_ids: Union[Unset, List[str]] = UNSET,
    connection_schema_ids: Union[Unset, List[str]] = UNSET,
    data_type: Union[Unset, ListConnectFilesDataType] = UNSET,
) -> Optional[Union[ConnectionFilesPaginatedList, BadRequestError]]:
    """ List Benchling Connect files """

    return (
        await asyncio_detailed(
            client=client,
            page_size=page_size,
            next_token=next_token,
            created_atlt=created_atlt,
            created_atgt=created_atgt,
            created_atlte=created_atlte,
            created_atgte=created_atgte,
            modified_atlt=modified_atlt,
            modified_atgt=modified_atgt,
            modified_atlte=modified_atlte,
            modified_atgte=modified_atgte,
            filename_includes=filename_includes,
            connection_ids=connection_ids,
            connection_schema_ids=connection_schema_ids,
            data_type=data_type,
        )
    ).parsed
